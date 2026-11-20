"""WMJobs Birmingham & Solihull admin/service review-only ETL POC.

The public WMJobs RSS feed is the only main-site route used. Normal WMJobs
search/detail pages return access-denied responses to automated clients, so this
module does not fetch, proxy or bypass them. It extracts the factual fields
available in RSS, filters to Birmingham & Solihull, compares candidates with
current JobG8 and approved external-source outputs, classifies HC/POSS/HARD_PASS,
and writes CSV/Markdown review reports only.
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
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree
from zoneinfo import ZoneInfo

from external_sources.northeast_jobs_poc import (
    CLEAR_TITLE_PATTERNS,
    HARD_PASS_TITLE_PATTERNS,
    PRIMARY_CLEAR_PATTERNS,
    REVIEW_TITLE_PATTERNS,
    SPECIALIST_REVIEW_PATTERNS,
    STRONG_SPECIALIST_PATTERNS,
    Vacancy,
    clean_text,
    deduplicate_within_source,
    load_geo_lookup,
    load_jobg8_candidates,
    normalise,
    normalise_title,
    similarity,
    token_jaccard,
)

SOURCE_NAME = "WMJobs"
SOURCE_CODE = "WMJobs"
RSS_URL = "https://www.wmjobs.co.uk/jobsrss/"
USER_AGENT = (
    "Ontap external-jobs research POC/1.0 "
    "(+https://www.ontapjobsearch.com/contact)"
)
TARGET_GEOGRAPHY = "Birmingham & Solihull"

BIRMINGHAM_MARKERS = (
    "birmingham",
    "edgbaston",
    "selly oak",
    "ladywood",
    "digbeth",
    "balsall heath",
    "northfield",
    "erdington",
    "handsworth",
    "harborne",
    "moseley",
    "kings heath",
    "kings norton",
    "aston",
    "small heath",
    "sparkbrook",
    "sparkhill",
    "bordesley",
    "smiths wood",
    "smith's wood",
)
SOLIHULL_MARKERS = (
    "solihull",
    "shirley",
    "knowle",
    "dorridge",
    "olton",
    "chelmsley wood",
    "castle bromwich",
    "the core",
)
TARGET_POSTCODE_PREFIXES = (
    "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9",
    "b10", "b11", "b12", "b13", "b14", "b15", "b16", "b17",
    "b18", "b19", "b20", "b21", "b23", "b24", "b25", "b26",
    "b27", "b28", "b29", "b30", "b31", "b32", "b33", "b34",
    "b35", "b36", "b37", "b38", "b40", "b90", "b91", "b92",
    "b93", "b94",
)
OUT_OF_SCOPE_MARKERS = (
    "coventry",
    "warwick",
    "warwickshire",
    "wolverhampton",
    "walsall",
    "dudley",
    "sandwell",
    "west bromwich",
    "stourbridge",
    "stafford",
    "staffordshire",
    "worcester",
    "worcestershire",
    "shropshire",
    "herefordshire",
    "newcastle registration office",
)
GENERIC_LOCATION_MARKERS = (
    "hybrid",
    "home based",
    "home-based",
    "remote",
    "west midlands",
    "flexible",
)

WMJOBS_HARD_PASS_TITLE_PATTERNS = HARD_PASS_TITLE_PATTERNS + (
    "principal lawyer",
    "lawyer",
    "solicitor",
    "director",
    "chief executive",
    "headteacher",
    "teacher",
    "social worker",
    "occupational therapist",
    "planner",
    "surveyor",
    "inspector",
    "engineer",
    "trading standards",
    "environmental health",
)
WMJOBS_REVIEW_TITLE_PATTERNS = REVIEW_TITLE_PATTERNS + (
    "registration officer",
    "benefits assessor",
    "revenues officer",
    "housing officer",
    "brokerage officer",
    "project assistant",
    "project officer",
    "programme officer",
    "coordinator",
    "co-ordinator",
    "customer adviser",
    "customer advisor",
    "box office assistant",
)

REPORT_FIELDS = [
    "source",
    "tracking_key",
    "title",
    "employer",
    "location",
    "salary_text",
    "posted_date",
    "closing_date",
    "description_excerpt",
    "apply_url",
    "classification",
    "classification_reason",
    "geography_status",
    "geography_reason",
    "ontap_geography",
    "jobg8_check",
    "jobg8_candidate_title",
    "jobg8_candidate_employer",
    "jobg8_match_score",
    "external_check",
    "external_candidate_source",
    "external_candidate_title",
    "external_candidate_employer",
    "external_match_score",
    "wmjobs_duplicate_check",
    "source_job_id",
    "source_url",
    "detail_status",
    "manual_action",
    "final_decision",
]


@dataclass
class RssItem:
    source_job_id: str
    title: str
    employer: str
    salary_text: str
    location: str
    description_excerpt: str
    posted_date: str
    closing_date: str
    source_url: str


@dataclass
class WmjobsVacancy(Vacancy):
    description_excerpt: str = ""
    apply_url: str = ""
    geography_status: str = ""
    geography_reason: str = ""
    external_duplicate_status: str = ""
    external_candidate_source: str = ""
    external_candidate_title: str = ""
    external_candidate_employer: str = ""
    external_match_score: str = ""


def strip_markup(value: str | None) -> str:
    text = html.unescape(value or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def source_job_id(url: str) -> str:
    match = re.search(r"/job/(\d+)/", urllib.parse.urlsplit(url).path)
    return match.group(1) if match else ""


def split_feed_title(value: str) -> tuple[str, str]:
    text = clean_text(value)
    if ":" not in text:
        return "", text
    employer, title = text.split(":", 1)
    return clean_text(employer), clean_text(title)


def _salary_and_description(text: str, employer: str) -> tuple[str, str]:
    cleaned = strip_markup(text)
    marker = f": {employer}:" if employer else ""
    if marker and marker.casefold() in cleaned.casefold():
        index = cleaned.casefold().find(marker.casefold())
        return clean_text(cleaned[:index]), clean_text(cleaned[index + len(marker):])
    parts = cleaned.split(":", 2)
    if len(parts) == 3:
        return clean_text(parts[0]), clean_text(parts[2])
    return "", cleaned


def postcode_hint(text: str) -> str:
    match = re.search(r"\b(B\d{1,2}[A-Z]?\s*\d[A-Z]{2})\b", text, flags=re.I)
    return clean_text(match.group(1).upper()) if match else ""


def location_hint(employer: str, title: str, description: str) -> str:
    combined = clean_text(f"{employer} {title} {description}")
    normal = normalise(combined)
    for marker in BIRMINGHAM_MARKERS:
        if normalise(marker) in normal:
            return "Birmingham"
    for marker in SOLIHULL_MARKERS:
        if normalise(marker) in normal:
            return "Solihull"
    postcode = postcode_hint(combined)
    if postcode:
        prefix = re.match(r"[A-Z]+\d+", postcode.replace(" ", ""))
        if prefix and prefix.group(0).casefold() in TARGET_POSTCODE_PREFIXES:
            return postcode
    for marker in OUT_OF_SCOPE_MARKERS:
        if normalise(marker) in normal:
            return marker.title()
    if any(normalise(marker) in normal for marker in GENERIC_LOCATION_MARKERS):
        return "Hybrid / flexible"
    return "Not explicit in RSS"


def closing_date_hint(description: str) -> str:
    patterns = (
        r"closing date(?: for applications)?\s*[:\-]?\s*([^.;]{4,50})",
        r"applications close\s*[:\-]?\s*([^.;]{4,50})",
    )
    for pattern in patterns:
        match = re.search(pattern, description, flags=re.I)
        if match:
            return clean_text(match.group(1))
    return ""


def parse_rss(text: str) -> list[RssItem]:
    root = ElementTree.fromstring(text)
    items: list[RssItem] = []
    for node in root.findall(".//item"):
        raw_title = clean_text(node.findtext("title"))
        employer, title = split_feed_title(raw_title)
        url = clean_text(node.findtext("link"))
        raw_description = node.findtext("description") or ""
        salary, description = _salary_and_description(raw_description, employer)
        location = location_hint(employer, title, description)
        items.append(
            RssItem(
                source_job_id=source_job_id(url),
                title=title,
                employer=employer,
                salary_text=salary,
                location=location,
                description_excerpt=description[:1000],
                posted_date=clean_text(node.findtext("pubDate")),
                closing_date=closing_date_hint(description),
                source_url=url,
            )
        )
    return [item for item in items if item.source_job_id and item.title]


def fetch_rss(timeout: int = 30) -> str:
    request = urllib.request.Request(
        RSS_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml,text/xml;q=0.9,*/*;q=0.1",
        },
    )
    with urllib.request.urlopen(
        request,
        timeout=timeout,
        context=ssl.create_default_context(),
    ) as response:
        return response.read().decode(
            response.headers.get_content_charset() or "utf-8",
            "replace",
        )


def geography(item: RssItem) -> tuple[str, str]:
    combined = normalise(
        f"{item.employer} {item.title} {item.location} {item.description_excerpt}"
    )
    if any(normalise(marker) in combined for marker in OUT_OF_SCOPE_MARKERS):
        return "HARD_PASS", "Explicitly outside Birmingham & Solihull"
    if any(normalise(marker) in combined for marker in BIRMINGHAM_MARKERS):
        return "IN_SCOPE", "Explicit Birmingham wording in RSS"
    if any(normalise(marker) in combined for marker in SOLIHULL_MARKERS):
        return "IN_SCOPE", "Explicit Solihull wording in RSS"
    if "solihull metropolitan borough council" in combined:
        return "IN_SCOPE", "Solihull Council employer; RSS role is hybrid/flexible"
    postcode = postcode_hint(combined)
    if postcode:
        outward = re.match(r"[A-Z]+\d+", postcode.replace(" ", ""))
        if outward and outward.group(0).casefold() in TARGET_POSTCODE_PREFIXES:
            return "IN_SCOPE", f"Target-area postcode in RSS: {postcode}"
    if any(normalise(marker) in combined for marker in GENERIC_LOCATION_MARKERS):
        return "POSS", "Generic hybrid/flexible geography requires review"
    return "POSS", "RSS does not state geography clearly enough"


def classify(vacancy: WmjobsVacancy) -> tuple[str, str]:
    title = normalise(vacancy.title)
    context = normalise(f"{vacancy.title} {vacancy.description_excerpt}")
    if vacancy.geography_status == "HARD_PASS":
        return "HARD_PASS", vacancy.geography_reason

    hard_hits = [pattern for pattern in WMJOBS_HARD_PASS_TITLE_PATTERNS if pattern in title]
    clear_hits = [pattern for pattern in CLEAR_TITLE_PATTERNS if pattern in title]
    review_hits = [pattern for pattern in WMJOBS_REVIEW_TITLE_PATTERNS if pattern in title]
    specialist_hits = [
        pattern.strip()
        for pattern in SPECIALIST_REVIEW_PATTERNS
        if pattern in f" {context} "
    ]

    if hard_hits and not clear_hits:
        return "HARD_PASS", "Out-of-scope occupation: " + ", ".join(hard_hits)
    if vacancy.geography_status == "POSS":
        return "POSS", vacancy.geography_reason
    if clear_hits:
        if (
            any(pattern in context for pattern in STRONG_SPECIALIST_PATTERNS)
            and not any(pattern in title for pattern in PRIMARY_CLEAR_PATTERNS)
        ):
            return "POSS", "Admin/service title with strong specialist context"
        if specialist_hits and not any(pattern in title for pattern in PRIMARY_CLEAR_PATTERNS):
            return "POSS", (
                "Transferable title with specialist wording: "
                + ", ".join(specialist_hits)
            )
        return "HC", "Clear admin/service title: " + ", ".join(clear_hits)
    if review_hits:
        return "POSS", "Borderline admin/service title: " + ", ".join(review_hits)
    if any(
        marker in context
        for marker in (
            "administrative support",
            "customer service",
            "office support",
            "answer enquiries",
            "maintain records",
            "frontline service",
        )
    ):
        return "POSS", "Office/service duties appear in RSS description"
    return "HARD_PASS", "Insufficient admin/service evidence"


def _candidate_value(candidate: object, name: str) -> str:
    if isinstance(candidate, dict):
        return clean_text(candidate.get(name, ""))
    return clean_text(getattr(candidate, name, ""))


def duplicate_against(
    vacancy: WmjobsVacancy,
    candidates: list[object],
) -> tuple[str, str, str, str, str]:
    best_score = 0.0
    best: object | None = None
    for candidate in candidates:
        title_score = similarity(
            normalise_title(vacancy.title),
            normalise_title(_candidate_value(candidate, "title")),
        )
        employer_score = similarity(
            normalise(vacancy.employer),
            normalise(_candidate_value(candidate, "employer")),
        )
        location_score = token_jaccard(
            normalise(vacancy.location),
            normalise(_candidate_value(candidate, "location")),
        )
        score = 0.5 * title_score + 0.4 * employer_score + 0.1 * location_score
        if score > best_score:
            best_score = score
            best = candidate
    if best is None:
        return "NO_MATCH", "", "", "", "0.000"
    status = (
        "DUPLICATE"
        if best_score >= 0.86
        else "POSSIBLE_DUPLICATE"
        if best_score >= 0.68
        else "NO_MATCH"
    )
    return (
        status,
        _candidate_value(best, "source"),
        _candidate_value(best, "title"),
        _candidate_value(best, "employer"),
        f"{best_score:.3f}",
    )


def load_external_candidates(paths: Iterable[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        if not path.exists() or path.suffix.casefold() != ".json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        values = data if isinstance(data, list) else data.get("jobs", [])
        for row in values:
            rows.append(
                {
                    "source": clean_text(row.get("source", path.stem)),
                    "title": clean_text(row.get("title")),
                    "employer": clean_text(row.get("employer")),
                    "location": clean_text(row.get("location")),
                }
            )
    return rows


def iso_posted_date(value: str) -> str:
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        return ""
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=ZoneInfo("Europe/London"))
    return parsed.astimezone(ZoneInfo("Europe/London")).date().isoformat()


def report_row(vacancy: WmjobsVacancy) -> dict[str, str]:
    return {
        "source": SOURCE_NAME,
        "tracking_key": f"wmjobs-{vacancy.source_job_id}",
        "title": vacancy.title,
        "employer": vacancy.employer,
        "location": vacancy.location,
        "salary_text": vacancy.salary_text,
        "posted_date": iso_posted_date(vacancy.posted_date),
        "closing_date": vacancy.closing_date,
        "description_excerpt": vacancy.description_excerpt,
        "apply_url": vacancy.apply_url,
        "classification": vacancy.classification,
        "classification_reason": vacancy.classification_reason,
        "geography_status": vacancy.geography_status,
        "geography_reason": vacancy.geography_reason,
        "ontap_geography": vacancy.ontap_geography,
        "jobg8_check": vacancy.duplicate_status,
        "jobg8_candidate_title": vacancy.jobg8_candidate_title,
        "jobg8_candidate_employer": vacancy.jobg8_candidate_advertiser,
        "jobg8_match_score": vacancy.jobg8_match_score,
        "external_check": vacancy.external_duplicate_status,
        "external_candidate_source": vacancy.external_candidate_source,
        "external_candidate_title": vacancy.external_candidate_title,
        "external_candidate_employer": vacancy.external_candidate_employer,
        "external_match_score": vacancy.external_match_score,
        "wmjobs_duplicate_check": vacancy.source_duplicate_status,
        "source_job_id": vacancy.source_job_id,
        "source_url": vacancy.source_url,
        "detail_status": vacancy.detail_status,
        "manual_action": "",
        "final_decision": "REVIEW_ONLY",
    }


def write_reports(
    vacancies: list[WmjobsVacancy],
    csv_path: Path,
    markdown_path: Path,
    feed_count: int,
) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=REPORT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for vacancy in sorted(
            vacancies,
            key=lambda item: (
                {"HC": 0, "POSS": 1, "HARD_PASS": 2}.get(item.classification, 9),
                item.title.casefold(),
            ),
        ):
            writer.writerow(report_row(vacancy))

    counts = {
        label: sum(vacancy.classification == label for vacancy in vacancies)
        for label in ("HC", "POSS", "HARD_PASS")
    }
    lines = [
        "# WMJobs ETL proof-of-concept review",
        "",
        f"Generated: {datetime.now(ZoneInfo('Europe/London')).isoformat(timespec='seconds')}",
        f"Scope: {TARGET_GEOGRAPHY}; admin/service only.",
        f"Public RSS items read: {feed_count}",
        f"Target/review rows retained: {len(vacancies)}",
        "Publishing: disabled. No approved-output or live-page path exists.",
        "",
        "## Source limitation",
        "",
        "- WMJobs search and job-detail pages reject automated access.",
        "- This POC uses only the intended public RSS feed and does not bypass that block.",
        "- RSS supplies no reliable closing-date field; missing closing dates remain explicit.",
        "- The original WMJobs job URL is retained for manual checking and application.",
        "",
        "## Outcomes",
        "",
        f"- HC: {counts['HC']}",
        f"- POSS: {counts['POSS']}",
        f"- HARD_PASS: {counts['HARD_PASS']}",
        "",
        "## Review rows",
        "",
    ]
    for vacancy in sorted(
        vacancies,
        key=lambda item: (
            {"HC": 0, "POSS": 1, "HARD_PASS": 2}.get(item.classification, 9),
            item.title.casefold(),
        ),
    ):
        lines.extend(
            [
                f"### [{vacancy.classification}] {vacancy.title}",
                f"- Employer: {vacancy.employer or 'Not stated'}",
                f"- Location: {vacancy.location or 'Not explicit in RSS'}",
                f"- Salary: {vacancy.salary_text or 'Not stated'}",
                f"- Posted: {iso_posted_date(vacancy.posted_date) or 'Not stated'}",
                f"- Closing: {vacancy.closing_date or 'Not supplied by RSS'}",
                f"- Reason: {vacancy.classification_reason}",
                f"- Geography: {vacancy.geography_reason}",
                f"- JobG8: {vacancy.duplicate_status or 'NO_MATCH'}",
                f"- External: {vacancy.external_duplicate_status or 'NO_MATCH'}",
                f"- Source: {vacancy.source_url}",
                "- action:",
                "",
            ]
        )
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text("\n".join(lines), encoding="utf-8")


def build_vacancies(items: list[RssItem]) -> list[WmjobsVacancy]:
    vacancies: list[WmjobsVacancy] = []
    for item in items:
        geography_status, geography_reason = geography(item)
        vacancy = WmjobsVacancy(
            source=SOURCE_NAME,
            source_job_id=item.source_job_id,
            title=item.title,
            employer=item.employer,
            location=item.location,
            ontap_geography=TARGET_GEOGRAPHY,
            contract_type="",
            working_pattern="",
            salary_text=item.salary_text,
            posted_date=item.posted_date,
            closing_date=item.closing_date,
            source_url=item.source_url,
            screening_basis="WMJobs public RSS title and description",
            detail_status="rss-only; automated detail access blocked",
            description_excerpt=item.description_excerpt,
            apply_url=item.source_url,
            geography_status=geography_status,
            geography_reason=geography_reason,
        )
        vacancy.classification, vacancy.classification_reason = classify(vacancy)
        if geography_status != "HARD_PASS" or vacancy.classification != "HARD_PASS":
            vacancies.append(vacancy)
        elif any(
            pattern in normalise(vacancy.title)
            for pattern in CLEAR_TITLE_PATTERNS + WMJOBS_REVIEW_TITLE_PATTERNS
        ):
            vacancies.append(vacancy)
    return vacancies


def run(args: argparse.Namespace) -> list[WmjobsVacancy]:
    rss_text = (
        fetch_rss()
        if args.fetch_live
        else Path(args.rss_file).read_text(encoding="utf-8")
    )
    items = parse_rss(rss_text)
    if not items:
        raise SystemExit("STOP: no WMJobs RSS items parsed")
    vacancies = build_vacancies(items)
    deduplicate_within_source(vacancies)

    jobg8: list[object] = []
    jobg8_path = Path(args.jobg8)
    if jobg8_path.exists():
        area_map, fallback_map = load_geo_lookup(Path(args.geo_lookup))
        jobg8 = load_jobg8_candidates(jobg8_path, area_map, fallback_map)
    external = load_external_candidates(Path(path) for path in args.external_json)

    for vacancy in vacancies:
        status, _source, title, employer, score = duplicate_against(vacancy, jobg8)
        vacancy.duplicate_status = status
        vacancy.jobg8_candidate_title = title
        vacancy.jobg8_candidate_advertiser = employer
        vacancy.jobg8_match_score = score

        status, source, title, employer, score = duplicate_against(vacancy, external)
        vacancy.external_duplicate_status = status
        vacancy.external_candidate_source = source
        vacancy.external_candidate_title = title
        vacancy.external_candidate_employer = employer
        vacancy.external_match_score = score
        if vacancy.classification == "HC" and status in {
            "DUPLICATE",
            "POSSIBLE_DUPLICATE",
        }:
            vacancy.classification = "POSS"
            vacancy.classification_reason = (
                "Possible existing external-source duplicate requires review"
            )

    write_reports(
        vacancies,
        Path(args.report_csv),
        Path(args.summary_md),
        len(items),
    )
    print(
        f"WMJobs review-only POC: {len(items)} RSS items -> "
        f"{len(vacancies)} Birmingham/Solihull review rows"
    )
    return vacancies


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--fetch-live", action="store_true")
    source.add_argument("--rss-file")
    parser.add_argument("--jobg8", default="input/jobg8.xlsx")
    parser.add_argument("--geo-lookup", default="geo/geo_lookup.xlsx")
    parser.add_argument(
        "--external-json",
        action="append",
        default=[
            "output-external/northeast-jobs-admin-service.json",
            "output-external/vonne-admin-service.json",
        ],
    )
    parser.add_argument(
        "--report-csv",
        default="reviews/external/wmjobs-review.csv",
    )
    parser.add_argument(
        "--summary-md",
        default="reviews/external/wmjobs-summary.md",
    )
    return parser


def main() -> int:
    run(build_parser().parse_args())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
