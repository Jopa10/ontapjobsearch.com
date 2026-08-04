"""Review-only Teaching Vacancies POC for West Yorkshire admin/service jobs.

Public GOV.UK pages only. Produces CSV/Markdown review files and has no
approved-output or publishing path.
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
from dataclasses import asdict, dataclass
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

BASE_URL = "https://teaching-vacancies.service.gov.uk"
SOURCE = "Teaching Vacancies GOV.UK"
TARGET = "West Yorkshire"
USER_AGENT = "Ontap external-jobs review POC/1.0 (+https://www.ontapjobsearch.com/contact)"
SEARCH_TERMS = ("administrator", "administrative", "receptionist", "office", "business support", "exams officer", "personal assistant")
PLACES = ("west yorkshire", "leeds", "bradford", "wakefield", "kirklees", "huddersfield", "halifax", "calderdale", "dewsbury", "batley", "keighley", "shipley", "pudsey", "morley", "horsforth", "castleford", "pontefract", "ossett", "heckmondwike", "cleckheaton", "mirfield", "sowerby bridge", "hebden bridge", "ilkley", "otley", "wetherby", "bingley", "brighouse", "elland", "normanton", "knottingley")
POSTCODES = ("BD", "HD", "HX", "LS", "WF")
HC = ("administrator", "administrative assistant", "admin assistant", "office administrator", "office assistant", "receptionist", "school secretary", "secretary", "personal assistant", "pa to", "business support assistant", "business support officer", "business services officer", "attendance officer", "admissions officer", "exams officer", "examinations officer", "student services officer", "data administrator", "finance administrator")
POSS = ("office manager", "business manager", "operations officer", "pastoral administrator", "cover manager", "data officer", "attendance manager", "admissions manager", "communications officer", "governance professional", "clerk to governors")
HARD = ("teacher", "teaching assistant", "headteacher", "deputy head", "principal", "lecturer", "social worker", "caretaker", "cleaner", "chef", "cook", "technician", "therapist", "nurse", "counsellor", "coach", "site manager", "premises manager", "midday supervisor")
FIELDS = ("source", "source_job_id", "title", "employer", "location", "salary_text", "posted_date", "closing_date", "employment_type", "description_excerpt", "source_url", "geography_status", "geography_reason", "classification", "classification_reason", "jobg8_check", "jobg8_candidate_title", "jobg8_candidate_employer", "jobg8_match_score", "manual_action", "final_decision")


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
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()


def normalise(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).casefold()).strip()


def request_text(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as response:
        return response.read().decode(response.headers.get_content_charset() or "utf-8", "replace")


def search_url(term: str, page: int = 1) -> str:
    values = {"keyword": term, "location": TARGET, "radius": "20"}
    if page > 1:
        values["page"] = str(page)
    return BASE_URL + "/jobs?" + urllib.parse.urlencode(values)


def discover_job_urls(document: str) -> list[str]:
    links = re.findall(r'href=["\']([^"\']*)["\']', document, flags=re.I)
    output: list[str] = []
    for link in links:
        absolute = urllib.parse.urljoin(BASE_URL, html.unescape(link))
        parsed = urllib.parse.urlsplit(absolute)
        if not parsed.path.startswith("/jobs/"):
            continue
        canonical = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", ""))
        if canonical not in output:
            output.append(canonical)
    return output


def parse_jobposting(document: str, url: str) -> Vacancy:
    posting = None
    scripts = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', document, flags=re.I | re.S)
    for script in scripts:
        try:
            root = json.loads(html.unescape(script).strip())
        except json.JSONDecodeError:
            continue
        candidates = root if isinstance(root, list) else root.get("@graph", [root]) if isinstance(root, dict) else []
        for item in candidates:
            if isinstance(item, dict) and (item.get("@type") == "JobPosting" or "JobPosting" in (item.get("@type") or [])):
                posting = item
                break
        if posting:
            break
    if not posting:
        raise ValueError(f"No JobPosting JSON-LD found: {url}")
    org = posting.get("hiringOrganization") or {}
    place = posting.get("jobLocation") or {}
    if isinstance(place, list):
        place = place[0] if place else {}
    address = place.get("address", {}) if isinstance(place, dict) else {}
    location = ", ".join(filter(None, (clean(address.get("addressLocality")), clean(address.get("addressRegion")), clean(address.get("postalCode")))))
    salary = posting.get("baseSalary") or ""
    if isinstance(salary, dict):
        value = salary.get("value") or {}
        if isinstance(value, dict):
            low, high, unit = value.get("minValue"), value.get("maxValue"), clean(value.get("unitText"))
            salary = f"£{low}–£{high} {unit}" if low and high else clean(low or high)
        else:
            salary = clean(value)
    identifier = posting.get("identifier") or ""
    if isinstance(identifier, dict):
        identifier = identifier.get("value") or identifier.get("name") or ""
    return Vacancy(source_job_id=clean(identifier) or urllib.parse.urlsplit(url).path.rstrip("/").split("/")[-1], title=clean(posting.get("title")), employer=clean(org.get("name") if isinstance(org, dict) else org), location=location, salary_text=clean(salary), posted_date=clean(posting.get("datePosted")), closing_date=clean(posting.get("validThrough")), employment_type=clean(posting.get("employmentType")), description_excerpt=clean(posting.get("description"))[:1200], source_url=url)


def geography(vacancy: Vacancy) -> tuple[str, str]:
    text = normalise(f"{vacancy.location} {vacancy.description_excerpt}")
    if any(normalise(place) in text for place in PLACES):
        return "IN_SCOPE", "West Yorkshire place marker"
    match = re.search(r"\b([A-Z]{1,2})\d", vacancy.location.upper())
    if match and match.group(1) in POSTCODES:
        return "IN_SCOPE", f"West Yorkshire postcode area {match.group(1)}"
    return "HARD_PASS", "No West Yorkshire location evidence"


def classify(vacancy: Vacancy) -> tuple[str, str]:
    title = normalise(vacancy.title)
    if vacancy.geography_status != "IN_SCOPE":
        return "HARD_PASS", vacancy.geography_reason
    hard = [p for p in HARD if normalise(p) in title]
    clear = [p for p in HC if normalise(p) in title]
    possible = [p for p in POSS if normalise(p) in title]
    if hard and not clear:
        return "HARD_PASS", "Out-of-scope occupation: " + ", ".join(hard)
    if clear:
        return "HC", "Clear admin/service title: " + ", ".join(clear)
    if possible:
        return "POSS", "Borderline school administration title: " + ", ".join(possible)
    duties = normalise(vacancy.description_excerpt)
    if any(term in duties for term in ("administrative support", "reception duties", "office support", "maintain records", "answer enquiries")):
        return "POSS", "Administrative duties evidenced in description"
    return "HARD_PASS", "Insufficient admin/service evidence"


def similarity(a: object, b: object) -> float:
    return SequenceMatcher(None, normalise(a), normalise(b)).ratio()


def load_jobg8(path: Path) -> list[dict]:
    if not path.exists():
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, list) else []


def compare_jobg8(vacancy: Vacancy, jobs: list[dict]) -> tuple[str, str, str, str]:
    best_score, best = 0.0, None
    for job in jobs:
        score = 0.65 * similarity(vacancy.title, job.get("title", "")) + 0.35 * similarity(vacancy.employer, job.get("advertiser_name") or job.get("company", ""))
        if score > best_score:
            best_score, best = score, job
    if not best:
        return "NO_MATCH", "", "", "0.000"
    status = "DUPLICATE" if best_score >= 0.86 else "POSSIBLE_DUPLICATE" if best_score >= 0.68 else "NO_MATCH"
    return status, clean(best.get("title")), clean(best.get("advertiser_name") or best.get("company")), f"{best_score:.3f}"


def process(vacancies: list[Vacancy], jobg8: list[dict]) -> list[Vacancy]:
    seen, output = set(), []
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
            values = asdict(vacancy)
            writer.writerow({field: values[field] for field in FIELDS})


def write_summary(path: Path, vacancies: list[Vacancy], discovered: int) -> None:
    counts = {key: sum(v.classification == key for v in vacancies) for key in ("HC", "POSS", "HARD_PASS")}
    lines = ["# Teaching Vacancies review-only summary", "", f"Generated: {date.today().isoformat()}", f"Target: {TARGET}", f"Discovered detail URLs: {discovered}", f"Parsed unique vacancies: {len(vacancies)}", f"HC: {counts['HC']}", f"POSS: {counts['POSS']}", f"HARD_PASS: {counts['HARD_PASS']}", f"Likely JobG8 duplicates: {sum(v.jobg8_check == 'DUPLICATE' for v in vacancies)}", "", "## Review candidates", ""]
    for vacancy in vacancies:
        if vacancy.classification in ("HC", "POSS") and vacancy.jobg8_check != "DUPLICATE":
            lines.append(f"- **{vacancy.classification} — {vacancy.title}** — {vacancy.employer} — {vacancy.location} — closes {vacancy.closing_date or 'not stated'}")
    lines += ["", "Review output only. No Ontap JSON or live pages were changed."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def live_urls(max_pages: int = 2) -> list[str]:
    output: list[str] = []
    for term in SEARCH_TERMS:
        for page in range(1, max_pages + 1):
            found = discover_job_urls(request_text(search_url(term, page)))
            if not found:
                break
            for url in found:
                if url not in output:
                    output.append(url)
    return output


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
    parsed = []
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
