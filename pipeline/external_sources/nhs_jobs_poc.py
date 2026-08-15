"""Review-only NHS Jobs ETL for Ontap administrative/clerical inventory.

Uses the public NHS Jobs Self-Serve XML endpoint. This module deliberately has
no approved-output, composition or live-publishing path. It exists to measure
inventory, normalise factual vacancy fields and compare likely duplicates with
Ontap's currently selected JobG8 jobs while reuse permission is confirmed.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import date, datetime
from difflib import SequenceMatcher
from pathlib import Path
from zoneinfo import ZoneInfo

BASE_URL = "https://www.jobs.nhs.uk/api/v1/search_xml"
SOURCE = "NHS Jobs"
STAFF_GROUP = "ADMINISTRATIVE_AND_CLERICAL"
USER_AGENT = "Ontap NHS Jobs inventory review/1.0 (+https://www.ontapjobsearch.com/contact)"
UK = ZoneInfo("Europe/London")
MAX_REQUEST_ATTEMPTS = 4
MIN_REQUEST_INTERVAL_SECONDS = 0.25

HC_TITLE_TERMS = (
    "administrator", "administrative assistant", "admin assistant",
    "administration assistant", "clerical officer", "clerical assistant",
    "receptionist", "reception assistant", "secretary", "personal assistant",
    "business support", "booking clerk", "appointments clerk", "appointment clerk",
    "ward clerk", "records clerk", "medical records", "data administrator",
    "office assistant", "office administrator", "support officer",
)
POSS_TITLE_TERMS = (
    "medical secretary", "team secretary", "coordinator", "co-ordinator",
    "project support", "service support", "patient pathway", "waiting list",
    "referral", "rota", "information officer", "data officer", "finance assistant",
)
HARD_TITLE_TERMS = (
    "manager", "head of", "director", "consultant", "nurse", "doctor",
    "therapist", "pharmacist", "scientist", "technician", "engineer",
)
REPORT_FIELDS = (
    "final_decision", "title", "employer", "locations", "salary_text",
    "job_reference", "employment_type", "posted_date", "closing_date",
    "source_job_id", "source_url", "classification", "classification_reason",
    "jobg8_check", "jobg8_candidate_title", "jobg8_candidate_employer",
    "jobg8_match_score", "source",
)


@dataclass
class Vacancy:
    source: str = SOURCE
    source_job_id: str = ""
    title: str = ""
    employer: str = ""
    locations: str = ""
    salary_text: str = ""
    job_reference: str = ""
    employment_type: str = ""
    posted_date: str = ""
    closing_date: str = ""
    source_url: str = ""
    classification: str = ""
    classification_reason: str = ""
    jobg8_check: str = ""
    jobg8_candidate_title: str = ""
    jobg8_candidate_employer: str = ""
    jobg8_match_score: str = ""
    final_decision: str = ""


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalise(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).casefold()).strip()


def child_text(node: ET.Element, tag: str) -> str:
    child = node.find(tag)
    return clean(child.text if child is not None else "")


def parse_xml(document: bytes | str) -> tuple[list[Vacancy], int, int]:
    root = ET.fromstring(document)
    total_pages = int(child_text(root, ".//totalPages") or "1")
    total_results = int(child_text(root, ".//totalResults") or "0")
    rows: list[Vacancy] = []
    for node in root.findall(".//vacancyDetails"):
        locations = ", ".join(
            clean(item.text) for item in node.findall("locations/location") if clean(item.text)
        )
        rows.append(
            Vacancy(
                source_job_id=child_text(node, "id"),
                title=child_text(node, "title"),
                employer=child_text(node, "employer"),
                locations=locations,
                salary_text=child_text(node, "salary"),
                job_reference=child_text(node, "reference"),
                employment_type=child_text(node, "type"),
                closing_date=child_text(node, "closeDate"),
                posted_date=child_text(node, "postDate"),
                source_url=child_text(node, "url"),
            )
        )
    return rows, total_pages, total_results


def request_page(page: int, timeout: int = 30) -> bytes:
    query = urllib.parse.urlencode({"staffGroup": STAFF_GROUP, "page": page})
    request = urllib.request.Request(
        BASE_URL + "?" + query,
        headers={"User-Agent": USER_AGENT, "Accept": "application/xml,text/xml"},
    )
    for attempt in range(MAX_REQUEST_ATTEMPTS):
        if attempt:
            time.sleep(min(2**attempt, 8))
        try:
            with urllib.request.urlopen(
                request, timeout=timeout, context=ssl.create_default_context()
            ) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError):
            if attempt == MAX_REQUEST_ATTEMPTS - 1:
                raise
    raise AssertionError("unreachable")


def fetch_live(max_pages: int | None = None) -> tuple[list[Vacancy], int]:
    all_rows: list[Vacancy] = []
    seen_ids: set[str] = set()
    page = 1
    total_pages = 1
    total_results = 0
    while page <= total_pages:
        document = request_page(page)
        rows, reported_pages, reported_results = parse_xml(document)
        total_pages = reported_pages
        total_results = reported_results
        if max_pages is not None:
            total_pages = min(total_pages, max_pages)
        for row in rows:
            key = row.source_job_id or normalise(
                f"{row.title}|{row.employer}|{row.locations}|{row.closing_date}"
            )
            if key in seen_ids:
                continue
            seen_ids.add(key)
            all_rows.append(row)
        page += 1
        if page <= total_pages:
            time.sleep(MIN_REQUEST_INTERVAL_SECONDS)
    return all_rows, total_results


def parse_date(value: str) -> date | None:
    value = clean(value)
    if not value:
        return None
    candidates = (value[:10], value)
    for candidate in candidates:
        try:
            return datetime.fromisoformat(candidate.replace("Z", "+00:00")).date()
        except ValueError:
            pass
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(candidate, fmt).date()
            except ValueError:
                continue
    return None


def is_open(vacancy: Vacancy, today: date) -> bool:
    closing = parse_date(vacancy.closing_date)
    return closing is None or closing >= today


def classify(vacancy: Vacancy) -> tuple[str, str]:
    title = normalise(vacancy.title)
    hard = [term for term in HARD_TITLE_TERMS if normalise(term) in title]
    clear = [term for term in HC_TITLE_TERMS if normalise(term) in title]
    possible = [term for term in POSS_TITLE_TERMS if normalise(term) in title]
    if hard and not clear:
        return "HARD_PASS", "Out-of-scope/senior title: " + ", ".join(hard)
    if clear:
        return "HC", "Clear administrative/service title: " + ", ".join(clear)
    if possible:
        return "POSS", "Potential administrative/service title: " + ", ".join(possible)
    return "POSS", "Administrative & Clerical staff-group role requires title review"


def similarity(first: object, second: object) -> float:
    return SequenceMatcher(None, normalise(first), normalise(second)).ratio()


def load_current_jobg8(output_dir: Path) -> list[dict]:
    jobs: list[dict] = []
    if not output_dir.exists():
        return jobs
    for path in sorted(output_dir.glob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(value, list):
            continue
        for row in value:
            if not isinstance(row, dict):
                continue
            source = clean(row.get("source"))
            if source and source.casefold() != "jobg8":
                continue
            jobs.append(row)
    return jobs


def compare_jobg8(vacancy: Vacancy, jobs: list[dict]) -> tuple[str, str, str, str]:
    best_score = 0.0
    best: dict | None = None
    for job in jobs:
        score = (
            0.65 * similarity(vacancy.title, job.get("title", ""))
            + 0.35 * similarity(
                vacancy.employer,
                job.get("advertiser_name") or job.get("company", ""),
            )
        )
        if score > best_score:
            best_score = score
            best = job
    if not best:
        return "NO_MATCH", "", "", "0.000"
    status = (
        "DUPLICATE" if best_score >= 0.86 else
        "POSSIBLE_DUPLICATE" if best_score >= 0.68 else
        "NO_MATCH"
    )
    return (
        status,
        clean(best.get("title")),
        clean(best.get("advertiser_name") or best.get("company")),
        f"{best_score:.3f}",
    )


def process(vacancies: list[Vacancy], jobg8: list[dict], today: date) -> list[Vacancy]:
    output: list[Vacancy] = []
    for vacancy in vacancies:
        if not is_open(vacancy, today):
            continue
        vacancy.classification, vacancy.classification_reason = classify(vacancy)
        (
            vacancy.jobg8_check,
            vacancy.jobg8_candidate_title,
            vacancy.jobg8_candidate_employer,
            vacancy.jobg8_match_score,
        ) = compare_jobg8(vacancy, jobg8)
        if vacancy.jobg8_check == "DUPLICATE":
            vacancy.final_decision = "HARD_PASS"
            vacancy.classification_reason = "Confirmed current JobG8 duplicate"
        elif vacancy.jobg8_check == "POSSIBLE_DUPLICATE" and vacancy.classification != "HARD_PASS":
            vacancy.final_decision = "POSS"
            vacancy.classification_reason = "Possible JobG8 duplicate requires review"
        else:
            vacancy.final_decision = vacancy.classification
        output.append(vacancy)
    return output


def write_csv(path: Path, vacancies: list[Vacancy]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REPORT_FIELDS)
        writer.writeheader()
        for vacancy in vacancies:
            row = asdict(vacancy)
            writer.writerow({field: row.get(field, "") for field in REPORT_FIELDS})


def write_summary(path: Path, vacancies: list[Vacancy], reported_total: int, jobg8_count: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    counts = {label: sum(v.final_decision == label for v in vacancies) for label in ("HC", "POSS", "HARD_PASS")}
    duplicates = sum(v.jobg8_check == "DUPLICATE" for v in vacancies)
    possible_dupes = sum(v.jobg8_check == "POSSIBLE_DUPLICATE" for v in vacancies)
    lines = [
        "# NHS Jobs Administrative & Clerical inventory review",
        "",
        f"- Review date: {datetime.now(UK).date().isoformat()}",
        f"- NHS API reported Administrative & Clerical vacancies: {reported_total}",
        f"- Open vacancies parsed for review: {len(vacancies)}",
        f"- HC: {counts['HC']}",
        f"- POSS: {counts['POSS']}",
        f"- HARD_PASS: {counts['HARD_PASS']}",
        f"- Current JobG8 comparison rows: {jobg8_count}",
        f"- Confirmed JobG8 duplicates: {duplicates}",
        f"- Possible JobG8 duplicates: {possible_dupes}",
        "",
        "## Safety boundary",
        "",
        "This is a review-only inventory measurement. It does not write approved external JSON,",
        "change any live Ontap page, copy NHS detail-page descriptions, or create a publishing path.",
        "Public redistribution remains gated on Ontap confirming the appropriate NHS Jobs job-board",
        "API/reuse route and any attribution requirements.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--fetch-live", action="store_true")
    source.add_argument("--xml-file", type=Path)
    parser.add_argument("--acknowledge-source-terms", action="store_true")
    parser.add_argument("--max-pages", type=int)
    parser.add_argument("--jobg8-dir", type=Path, default=Path("output-admin-service"))
    parser.add_argument("--report-csv", type=Path, default=Path("reviews/external/nhs-jobs-admin-clerical-review.csv"))
    parser.add_argument("--summary-md", type=Path, default=Path("reviews/external/nhs-jobs-admin-clerical-summary.md"))
    args = parser.parse_args(argv)

    if args.fetch_live and not args.acknowledge_source_terms:
        parser.error("--fetch-live requires --acknowledge-source-terms")

    if args.fetch_live:
        vacancies, reported_total = fetch_live(args.max_pages)
    else:
        payload = args.xml_file.read_bytes()
        vacancies, _pages, reported_total = parse_xml(payload)

    jobg8 = load_current_jobg8(args.jobg8_dir)
    reviewed = process(vacancies, jobg8, datetime.now(UK).date())
    write_csv(args.report_csv, reviewed)
    write_summary(args.summary_md, reviewed, reported_total, len(jobg8))
    print(f"NHS Jobs review written: {len(reviewed)} open rows; API reported {reported_total} total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
