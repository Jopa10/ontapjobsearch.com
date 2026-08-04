"""Teaching Vacancies West Yorkshire admin/service review-only ETL POC.

Uses only public GOV.UK Teaching Vacancies search/detail pages. It discovers
candidate adverts, reads JobPosting JSON-LD, filters to the existing Ontap West
Yorkshire slice, classifies HC/POSS/HARD_PASS, compares with the current Ontap
West Yorkshire JobG8 JSON, and writes CSV/Markdown review outputs only.

It deliberately contains no approved-output or publishing path.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import ssl
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable

BASE_URL = "https://teaching-vacancies.service.gov.uk"
SEARCH_URL = BASE_URL + "/jobs"
SOURCE = "Teaching Vacancies GOV.UK"
TARGET = "West Yorkshire"
USER_AGENT = "Ontap external-jobs review POC/1.0 (+https://www.ontapjobsearch.com/contact)"
SEARCH_TERMS = ("administrator", "administrative", "receptionist", "office", "business support", "exams officer", "personal assistant")

PLACE_MARKERS = (
    "west yorkshire", "leeds", "bradford", "wakefield", "kirklees", "huddersfield",
    "halifax", "calderdale", "dewsbury", "batley", "keighley", "shipley", "pudsey",
    "morley", "horsforth", "castleford", "pontefract", "ossett", "heckmondwike",
    "cleckheaton", "mirfield", "sowerby bridge", "hebden bridge", "ilkley", "otley",
    "wetherby", "bingley", "brighouse", "elland", "normanton", "knottingley",
)
POSTCODE_PREFIXES = ("BD", "HD", "HX", "LS", "WF")

HC_PATTERNS = (
    "administrator", "administrative assistant", "admin assistant", "office administrator",
    "office assistant", "receptionist", "school secretary", "secretary", "personal assistant",
    "pa to", "business support assistant", "business support officer", "business services officer",
    "attendance officer", "admissions officer", "exams officer", "examinations officer",
    "student services officer", "data administrator", "finance administrator",
)
POSS_PATTERNS = (
    "office manager", "business manager", "operations officer", "pastoral administrator",
    "cover manager", "data officer", "attendance manager", "admissions manager",
    "communications officer", "governance professional", "clerk to governors",
)
HARD_PASS_PATTERNS = (
    "teacher", "teaching assistant", "headteacher", "deputy head", "principal", "lecturer",
    "social worker", "caretaker", "cleaner", "chef", "cook", "technician", "therapist",
    "nurse", "counsellor", "coach", "site manager", "premises manager", "midday supervisor",
)

FIELDS = (
    "source", "source_job_id", "title", "employer", "location", "salary_text",
    "posted_date", "closing_date", "employment_type", "description_excerpt", "source_url",
    "geography_status", "geography_reason", "classification", "classification_reason",
    "jobg8_check", "jobg8_candidate_title", "jobg8_candidate_employer", "jobg8_match_score",
    "manual_action", "final_decision",
)


@dataclass
class Vacancy:
    source: str = SOURCE
    source_job_id: str = ""
    title: str = ""
    employer: str = ""
    location: str = ""
    salary_text: str = ""
    posted_date: str = ""
    closing_date: str = ""
    employment_type: str = ""
    description_excerpt: str = ""
    source_url: str = ""
    geography_status: str = ""
    geography_reason: str = ""
    classification: str = ""
    classification_reason: str = ""
    jobg8_check: str = ""
    jobg8_candidate_title: str = ""
    jobg8_candidate_employer: str = ""
    jobg8_match_score: str = ""
    manual_action: str = ""
    final_decision: str = ""


def clean(value: object) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalise(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).casefold()).strip()


def request_text(url: str, timeout: int = 30) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    with urllib.request.urlopen(request, timeout=timeout, context=ssl.create_default_context()) as response:
        return response.read().decode(response.headers.get_content_charset() or "utf-8", "replace")


def search_url(term: str, page: int = 1) -> str:
    query = {"keyword": term, "location": TARGET, "radius": "20"}
    if page > 1:
        query["page"] = str(page)
    return SEARCH_URL + "?" + urllib.parse.urlencode(query)


def discover_job_urls(document: str) -> list[str]:
    links = re.findall(r'href=["\']([^"\']+/jobs/[^"\'#?]+)["\']', document, flags=re.I)
    output: list[str] = []
    for link in links:
        absolute = urllib.parse.urljoin(BASE_URL, html.unescape(link))
        path = urllib.parse.urlsplit(absolute).path
        if path == "/jobs" or not path.startswith("/jobs/"):
            continue
        if absolute not in output:
            output.append(absolute)
    return output


def _json_objects(value: object) -> Iterable[dict]:
    if isinstance(value, dict):
        yield value
        graph = value.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                if isinstance(item, dict):
                    yield item
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                yield item


def parse_jobposting(document: str, url: str) -> Vacancy:
    scripts = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', document, flags=re.I | re.S)
    posting: dict | None = None
    for script in scripts:
        try:
            value = json.loads(html.unescape(script).strip())
        except (json.JSONDecodeError, TypeError):
            continue
        for candidate in _json_objects(value):
            kind = candidate.get("@type")
            if kind == "JobPosting" or (isinstance(kind, list) and "JobPosting" in kind):
                posting = candidate
                break
        if posting:
            break
    if not posting:
        raise ValueError(f"No JobPosting JSON-LD found: {url}")

    org = posting.get("hiringOrganization") or {}
    location = posting.get("jobLocation") or {}
    if isinstance(location, list):
        location = location[0] if location else {}
    address = location.get("address") if isinstance(location, dict) else {}
    if not isinstance(address, dict):
        address = {}
    location_text = ", ".join(filter(None, [clean(address.get("addressLocality")), clean(address.get("addressRegion")), clean(address.get("postalCode"))]))

    salary = posting.get("baseSalary") or ""
    if isinstance(salary, dict):
        value = salary.get("value") or {}
        if isinstance(value, dict):
            low, high, unit = value.get("minValue"), value.get("maxValue"), clean(value.get("unitText"))
            salary = f"£{low}–£{high} {unit}" if low and high else clean(low or high)
        else:
            salary = clean(value)

    slug = urllib.parse.urlsplit(url).path.rstrip("/").split("/")[-1]
    return Vacancy(
        source_job_id=clean(posting.get("identifier", {}).get("value") if isinstance(posting.get("identifier"), dict) else posting.get("identifier")) or slug,
        title=clean(posting.get("title")), employer=clean(org.get("name") if isinstance(org, dict) else org),
        location=location_text, salary_text=clean(salary), posted_date=clean(posting.get("datePosted")),
        closing_date=clean(posting.get("validThrough")), employment_type=clean(posting.get("employmentType")),
        description_excerpt=clean(posting.get("description"))[:1200], source_url=url,
    )


def geography(vacancy: Vacancy) -> tuple[str, str]:
    text = normalise(f"{vacancy.location} {vacancy.description_excerpt}")
    if any(normalise(place) in text for place in PLACE_MARKERS):
        return "IN_SCOPE", "West Yorkshire place marker"
    postcode = re.search(r"\b([A-Z]{1,2})\d", vacancy.location.upper())
    if postcode and postcode.group(1) in POSTCODE_PREFIXES:
        return "IN_SCOPE", f"West Yorkshire postcode area {postcode.group(1)}"
    return "HARD_PASS", "No West Yorkshire location evidence"


def classify(vacancy: Vacancy) -> tuple[str, str]:
    title = normalise(vacancy.title)
    if vacancy.geography_status != "IN_SCOPE":
        return "HARD_PASS", vacancy.geography_reason
    hard = [p for p in HARD_PASS_PATTERNS if normalise(p) in title]
    hc = [p for p in HC_PATTERNS if normalise(p) in title]
    poss = [p for p in POSS_PATTERNS if normalise(p) in title]
    if hard and not hc:
        return "HARD_PASS", "Out-of-scope occupation: " + ", ".join(hard)
    if hc:
        return "HC", "Clear admin/service title: " + ", ".join(hc)
    if poss:
        return "POSS", "Borderline school administration title: " + ", ".join(poss)
    duties = normalise(vacancy.description_excerpt)
    if any(term in duties for term in ("administrative support", "reception duties", "office support", "maintain records", "answer enquiries")):
        return "POSS", "Administrative duties evidenced in description"
    return "HARD_PASS", "Insufficient admin/service evidence"


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalise(a), normalise(b)).ratio()


def load_jobg8(path: Path) -> list[dict]:
    if not path.exists():
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, list) else []


def compare_jobg8(vacancy: Vacancy, jobs: list[dict]) -> tuple[str, str, str, str]:
    best_score, best = 0.0, None
    for job in jobs:
        title_score = similarity(vacancy.title, job.get("title", ""))
        employer_score = similarity(vacancy.employer, job.get("advertiser_name") or job.get("company", ""))
        score = 0.65 * title_score + 0.35 * employer_score
        if score > best_score:
            best_score, best = score, job
    if not best:
        return "NO_MATCH", "", "", "0.000"
    status = "DUPLICATE" if best_score >= 0.86 else "POSSIBLE_DUPLICATE" if best_score >= 0.68 else "NO_MATCH"
    return status, clean(best.get("title")), clean(best.get("advertiser_name") or best.get("company")), f"{best_score:.3f}"


def process(vacancies: list[Vacancy], jobg8: list[dict]) -> list[Vacancy]:
    seen: set[str] = set()
    output: list[Vacancy] = []
    for vacancy in vacancies:
        key = normalise(f"{vacancy.title}|{vacancy.employer}|{vacancy.location}")
        if key in seen:
            continue
        seen.add(key)
        vacancy.geography_status, vacancy.geography_reason = geography(vacancy)
        vacancy.classification, vacancy.classification_reason = classify(vacancy)
        vacancy.jobg8_check, vacancy.jobg8_candidate_title, vacancy.jobg8_candidate_employer, vacancy.jobg8_match_score = compare_jobg8(vacancy, jobg8)
        if vacancy.classification == "HARD_PASS":
            vacancy.manual_action, vacancy.final_decision = "No review needed", "HARD_PASS"
        elif vacancy.jobg8_check == "DUPLICATE":
            vacancy.manual_action, vacancy.final_decision = "Confirm duplicate", "DUPLICATE"
        else:
            vacancy.manual_action, vacancy.final_decision = "Review manually", vacancy.classification
        output.append(vacancy)
    return output


def write_csv(path: Path, vacancies: list[Vacancy]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for vacancy in vacancies:
            writer.writerow({field: asdict(vacancy)[field] for field in FIELDS})


def write_summary(path: Path, vacancies: list[Vacancy], discovered: int) -> None:
    counts = {key: sum(v.classification == key for v in vacancies) for key in ("HC", "POSS", "HARD_PASS")}
    duplicates = sum(v.jobg8_check == "DUPLICATE" for v in vacancies)
    lines = [
        "# Teaching Vacancies review-only summary", "",
        f"Generated: {date.today().isoformat()}", f"Target: {TARGET}",
        f"Discovered detail URLs: {discovered}", f"Parsed unique vacancies: {len(vacancies)}",
        f"HC: {counts['HC']}", f"POSS: {counts['POSS']}", f"HARD_PASS: {counts['HARD_PASS']}",
        f"Likely JobG8 duplicates: {duplicates}", "", "## Review candidates", "",
    ]
    for v in vacancies:
        if v.classification in ("HC", "POSS") and v.jobg8_check != "DUPLICATE":
            lines.append(f"- **{v.classification} — {v.title}** — {v.employer} — {v.location} — closes {v.closing_date or 'not stated'}")
    lines += ["", "Review output only. No Ontap JSON or live pages were changed."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def live_urls(max_pages: int = 2) -> list[str]:
    urls: list[str] = []
    for term in SEARCH_TERMS:
        for page in range(1, max_pages + 1):
            found = discover_job_urls(request_text(search_url(term, page)))
            if not found:
                break
            for url in found:
                if url not in urls:
                    urls.append(url)
    return urls


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch-live", action="store_true")
    parser.add_argument("--max-pages", type=int, default=2)
    parser.add_argument("--jobg8-json", type=Path, default=Path("../app/west-yorkshire/service-administrator-jobs.json"))
    parser.add_argument("--report-csv", type=Path, default=Path("/tmp/teaching-vacancies-review.csv"))
    parser.add_argument("--summary-md", type=Path, default=Path("/tmp/teaching-vacancies-summary.md"))
    args = parser.parse_args()
    if not args.fetch_live:
        parser.error("This POC currently requires --fetch-live")
    urls = live_urls(args.max_pages)
    parsed: list[Vacancy] = []
    for url in urls:
        try:
            parsed.append(parse_jobposting(request_text(url), url))
        except (OSError, ValueError, json.JSONDecodeError):
            continue
    reviewed = process(parsed, load_jobg8(args.jobg8_json))
    write_csv(args.report_csv, reviewed)
    write_summary(args.summary_md, reviewed, len(urls))
    print(f"Teaching Vacancies: {len(urls)} URLs, {len(reviewed)} parsed; review only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
