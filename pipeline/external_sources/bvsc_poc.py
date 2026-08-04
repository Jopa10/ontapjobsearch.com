"""BVSC Charity Jobs West Midlands review-only ETL proof of concept.

Bounded to Birmingham & Solihull and Ontap admin/service roles. This module has
no approval, composition or publishing mode. It writes review CSV/Markdown only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import ssl
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

from external_sources.northeast_jobs_poc import (
    CLEAR_TITLE_PATTERNS,
    HARD_PASS_TITLE_PATTERNS,
    PRIMARY_CLEAR_PATTERNS,
    REVIEW_TITLE_PATTERNS,
    SPECIALIST_REVIEW_PATTERNS,
    STRONG_SPECIALIST_PATTERNS,
    Vacancy,
    annual_salary_upper,
    clean_text,
    deduplicate_within_source,
    load_jobg8_candidates,
    normalise,
    normalise_title,
    similarity,
    token_jaccard,
)

SOURCE_NAME = "BVSC Charity Jobs West Midlands"
SOURCE_CODE = "BVSC"
LIST_URL = "https://www.bvsc.org/pages/site/bvsc-charity-jobs-wm/category/vacancies"
USER_AGENT = "Ontap external-jobs research POC/1.0 (+https://www.ontapjobsearch.com/contact)"
TARGET_GEOGRAPHY = "Birmingham & Solihull"

BIRMINGHAM_MARKERS = (
    "birmingham", "edgbaston", "selly oak", "ladywood", "digbeth",
    "balsall heath", "northfield", "erdington", "handsworth", "harborne",
    "mosesley", "moseley", "kings heath", "kings norton", "aston",
    "small heath", "sparkbrook", "sparkhill", "bordesley", "b1 ", "b2 ",
    "b3 ", "b4 ", "b5 ", "b6 ", "b7 ", "b8 ", "b9 ", "b10 ",
    "b11 ", "b12 ", "b13 ", "b14 ", "b15 ", "b16 ", "b17 ",
    "b18 ", "b19 ", "b20 ", "b21 ", "b23 ", "b24 ", "b25 ",
    "b26 ", "b27 ", "b28 ", "b29 ", "b30 ", "b31 ", "b32 ",
    "b33 ", "b34 ", "b35 ", "b36 ", "b37 ", "b38 ", "b40 ",
)
SOLIHULL_MARKERS = (
    "solihull", "shirley", "knowle", "dorridge", "olton", "chelmsley wood",
    "castle bromwich", "b90 ", "b91 ", "b92 ", "b93 ", "b94 ",
)
OUT_OF_SCOPE_MARKERS = (
    "coventry", "warwick", "warwickshire", "wolverhampton", "walsall",
    "dudley", "sandwell", "west bromwich", "stourbridge", "gloucester",
    "stafford", "staffordshire", "worcester", "worcestershire",
)
GENERIC_LOCATION_MARKERS = ("hybrid", "home based", "home-based", "remote", "west midlands")

BVSC_HARD_PASS_TITLE_PATTERNS = HARD_PASS_TITLE_PATTERNS + (
    "chief executive", "ceo", "director", "trustee", "chair", "volunteer",
    "support worker", "youth worker", "coach", "advocate", "chef", "cook",
    "fundraiser", "fundraising", "development worker", "project manager",
)
BVSC_REVIEW_TITLE_PATTERNS = REVIEW_TITLE_PATTERNS + (
    "project assistant", "project officer", "programme officer", "coordinator",
    "co-ordinator", "information officer", "membership officer", "connector",
)

REPORT_FIELDS = [
    "source", "tracking_key", "title", "employer", "location", "salary_text",
    "closing_date", "description_excerpt", "apply_url", "classification",
    "classification_reason", "geography_status", "geography_reason",
    "ontap_geography", "jobg8_check", "jobg8_candidate_title",
    "jobg8_candidate_employer", "jobg8_match_score", "external_check",
    "external_candidate_source", "external_candidate_title",
    "external_candidate_employer", "external_match_score", "bvsc_duplicate_check",
    "source_job_id", "source_url", "detail_status", "manual_action", "final_decision",
]


@dataclass
class ListingItem:
    source_job_id: str
    title: str
    employer: str
    location: str
    closing_date: str
    source_url: str


@dataclass
class BvscVacancy(Vacancy):
    description_excerpt: str = ""
    apply_url: str = ""
    geography_status: str = ""
    geography_reason: str = ""
    external_duplicate_status: str = ""
    external_duplicate_reason: str = ""
    external_candidate_source: str = ""
    external_candidate_title: str = ""
    external_candidate_employer: str = ""
    external_match_score: str = ""


class TextHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self.links: list[tuple[str, str]] = []
        self._href = ""
        self._anchor: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() == "a":
            self._href = dict(attrs).get("href") or ""
            self._anchor = []

    def handle_data(self, data: str) -> None:
        value = clean_text(data)
        if not value:
            return
        self.lines.append(value)
        if self._href:
            self._anchor.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "a" and self._href:
            self.links.append((clean_text(" ".join(self._anchor)), self._href))
            self._href = ""
            self._anchor = []


def slug_id(url: str) -> str:
    path = urllib.parse.urlsplit(url).path.rstrip("/")
    slug = path.rsplit("/", 1)[-1]
    return hashlib.sha256(slug.encode("utf-8")).hexdigest()[:16]


def _field(lines: list[str], labels: Iterable[str]) -> str:
    for line in lines:
        for label in labels:
            match = re.match(rf"^{re.escape(label)}\s*:\s*(.+)$", line, re.I)
            if match:
                return clean_text(match.group(1))
    return ""


def parse_listing(text: str) -> list[ListingItem]:
    parser = TextHTMLParser()
    parser.feed(text)
    vacancy_links: list[tuple[str, str]] = []
    seen: set[str] = set()
    for title, href in parser.links:
        absolute = urllib.parse.urljoin(LIST_URL, href)
        path = urllib.parse.urlsplit(absolute).path.casefold()
        if not title or absolute in seen:
            continue
        if "/vacancy" not in path and not any(word in path for word in ("assistant", "officer", "administrator", "reception")):
            continue
        seen.add(absolute)
        vacancy_links.append((title, absolute))

    items: list[ListingItem] = []
    for index, (title, url) in enumerate(vacancy_links):
        next_title = vacancy_links[index + 1][0] if index + 1 < len(vacancy_links) else ""
        try:
            start = parser.lines.index(title)
        except ValueError:
            start = 0
        end = len(parser.lines)
        if next_title:
            try:
                end = parser.lines.index(next_title, start + 1)
            except ValueError:
                pass
        block = parser.lines[start + 1:end]
        summary = next((line for line in block if "closing date" in line.casefold()), "")
        employer = clean_text(re.split(r"\.\s*Closing Date\s*:", summary, flags=re.I)[0])
        closing = ""
        match = re.search(r"Closing Date\s*:\s*(.+?)(?:\.\s*Read more|$)", summary, re.I)
        if match:
            closing = clean_text(match.group(1)).replace("Closing Date:", "").strip()
        location = _field(block, ("Location",))
        items.append(ListingItem(slug_id(url), title, employer, location, closing, url))
    return items


def parse_detail(text: str, item: ListingItem) -> dict[str, str]:
    parser = TextHTMLParser()
    parser.feed(text)
    lines = parser.lines
    title = _field(lines, ("Job Title",)) or item.title
    salary = _field(lines, ("Salary", "Pay"))
    location = _field(lines, ("Location", "Based at", "Base")) or item.location
    closing = _field(lines, ("Closing date for applications", "Closing Date", "Application deadline")) or item.closing_date
    employer = item.employer
    if not employer:
        heading = next((line for line in lines if "," in line and "closing date" in line.casefold()), "")
        employer = clean_text(heading.split(",", 1)[0])
    apply_url = ""
    for label, href in parser.links:
        label_n = normalise(label)
        if any(term in label_n for term in ("apply", "application form", "submit application")):
            apply_url = urllib.parse.urljoin(item.source_url, href)
            break
    if not apply_url:
        for label, href in parser.links:
            if href.casefold().startswith("mailto:"):
                apply_url = href
                break
    body_start = 0
    for idx, line in enumerate(lines):
        if normalise(line) in {normalise(title), normalise(item.title)}:
            body_start = idx + 1
            break
    description = clean_text(" ".join(lines[body_start:]))[:1200]
    return {
        "title": title,
        "employer": employer,
        "location": location,
        "salary_text": salary,
        "closing_date": closing,
        "description_excerpt": description,
        "apply_url": apply_url,
    }


def fetch_text(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.1"})
    with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as response:
        return response.read().decode(response.headers.get_content_charset() or "utf-8", "replace")


def geography(location: str, description: str) -> tuple[str, str]:
    text = normalise(f"{location} {description}")
    if any(normalise(marker) in text for marker in OUT_OF_SCOPE_MARKERS):
        return "HARD_PASS", "Explicitly outside Birmingham & Solihull"
    if any(normalise(marker) in text for marker in BIRMINGHAM_MARKERS):
        return "IN_SCOPE", "Explicit Birmingham location"
    if any(normalise(marker) in text for marker in SOLIHULL_MARKERS):
        return "IN_SCOPE", "Explicit Solihull location"
    if any(normalise(marker) in text for marker in GENERIC_LOCATION_MARKERS):
        return "POSS", "Generic hybrid/remote/West Midlands location requires review"
    return "POSS", "Location is not explicit enough for Birmingham & Solihull"


def classify(vacancy: BvscVacancy) -> tuple[str, str]:
    title = normalise(vacancy.title)
    context = normalise(f"{vacancy.title} {vacancy.description_excerpt}")
    if vacancy.geography_status == "HARD_PASS":
        return "HARD_PASS", vacancy.geography_reason
    hard = [p for p in BVSC_HARD_PASS_TITLE_PATTERNS if p in title]
    clear = [p for p in CLEAR_TITLE_PATTERNS if p in title]
    review = [p for p in BVSC_REVIEW_TITLE_PATTERNS if p in title]
    specialist = [p for p in SPECIALIST_REVIEW_PATTERNS if p in context]
    if hard and not clear:
        return "HARD_PASS", f"Hard-pass title: {hard[0]}"
    if vacancy.geography_status == "POSS":
        return "POSS", vacancy.geography_reason
    if clear:
        if any(p in context for p in STRONG_SPECIALIST_PATTERNS) and not any(p in title for p in PRIMARY_CLEAR_PATTERNS):
            return "POSS", "Admin/service title with specialist context"
        return "HC", f"Clear admin/service title: {clear[0]}"
    if review:
        return "POSS", f"Borderline admin/service title: {review[0]}"
    if "administrative" in context or "customer service" in context or "office support" in context:
        return "POSS", "Office/service duties appear in description but title is not clear"
    return "HARD_PASS", "No sufficient admin/service evidence"


def duplicate_against(vacancy: BvscVacancy, candidates: list[dict[str, str]]) -> tuple[str, str, str, str, str]:
    best: tuple[float, dict[str, str] | None] = (0.0, None)
    for candidate in candidates:
        title_score = similarity(normalise_title(vacancy.title), normalise_title(candidate.get("title", "")))
        employer_score = similarity(normalise(vacancy.employer), normalise(candidate.get("employer", "")))
        location_score = token_jaccard(normalise(vacancy.location), normalise(candidate.get("location", "")))
        score = 0.5 * title_score + 0.4 * employer_score + 0.1 * location_score
        if score > best[0]:
            best = (score, candidate)
    score, candidate = best
    if not candidate:
        return "NO_MATCH", "", "", "", "0.000"
    status = "DUPLICATE" if score >= 0.86 else "POSSIBLE_DUPLICATE" if score >= 0.68 else "NO_MATCH"
    return status, candidate.get("source", ""), candidate.get("title", ""), candidate.get("employer", ""), f"{score:.3f}"


def load_external_candidates(paths: Iterable[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        if not path.exists():
            continue
        if path.suffix.casefold() == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            values = data if isinstance(data, list) else data.get("jobs", [])
            for row in values:
                rows.append({"source": clean_text(row.get("source", path.stem)), "title": clean_text(row.get("title")), "employer": clean_text(row.get("employer")), "location": clean_text(row.get("location"))})
    return rows


def report_row(v: BvscVacancy) -> dict[str, str]:
    external = v.external_duplicate_reason.split("|") if v.external_duplicate_reason else ["", "", "", ""]
    return {
        "source": SOURCE_NAME, "tracking_key": f"bvsc-{v.source_job_id}", "title": v.title,
        "employer": v.employer, "location": v.location, "salary_text": v.salary_text,
        "closing_date": v.closing_date, "description_excerpt": v.description_excerpt,
        "apply_url": v.apply_url, "classification": v.classification,
        "classification_reason": v.classification_reason, "geography_status": v.geography_status,
        "geography_reason": v.geography_reason, "ontap_geography": v.ontap_geography,
        "jobg8_check": v.duplicate_status, "jobg8_candidate_title": v.jobg8_candidate_title,
        "jobg8_candidate_employer": v.jobg8_candidate_advertiser, "jobg8_match_score": v.jobg8_match_score,
        "external_check": v.external_duplicate_status, "external_candidate_source": v.external_candidate_source,
        "external_candidate_title": v.external_candidate_title, "external_candidate_employer": v.external_candidate_employer,
        "external_match_score": v.external_match_score, "bvsc_duplicate_check": v.source_duplicate_status,
        "source_job_id": v.source_job_id, "source_url": v.source_url, "detail_status": v.detail_status,
        "manual_action": "", "final_decision": "REVIEW_ONLY",
    }


def write_reports(vacancies: list[BvscVacancy], csv_path: Path, md_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REPORT_FIELDS)
        writer.writeheader()
        writer.writerows(report_row(v) for v in vacancies)
    counts = {key: sum(v.classification == key for v in vacancies) for key in ("HC", "POSS", "HARD_PASS")}
    lines = [
        "# BVSC review-only proof of concept", "",
        f"Generated: {datetime.now(ZoneInfo('Europe/London')).isoformat(timespec='seconds')}",
        f"Scope: {TARGET_GEOGRAPHY}; admin/service only.",
        "Publishing: disabled. No live-page or approved-output path exists.", "",
        f"- HC: {counts['HC']}", f"- POSS: {counts['POSS']}", f"- HARD_PASS: {counts['HARD_PASS']}", "",
        "## Review rows", "",
    ]
    for v in vacancies:
        lines += [f"### [{v.classification}] {v.title}", f"- Employer: {v.employer or 'Not stated'}", f"- Location: {v.location or 'Not stated'}", f"- Salary: {v.salary_text or 'Not stated'}", f"- Closing: {v.closing_date or 'Not stated/open-ended'}", f"- Reason: {v.classification_reason}", f"- JobG8: {v.duplicate_status or 'NO_MATCH'}", f"- External: {v.external_duplicate_status or 'NO_MATCH'}", f"- Source: {v.source_url}", "- action:", ""]
    md_path.write_text("\n".join(lines), encoding="utf-8")


def run(args: argparse.Namespace) -> list[BvscVacancy]:
    listing_text = fetch_text(LIST_URL) if args.fetch_live else Path(args.listing_file).read_text(encoding="utf-8")
    items = parse_listing(listing_text)
    details_dir = Path(args.details_dir) if args.details_dir else None
    vacancies: list[BvscVacancy] = []
    for item in items:
        detail_text = ""
        status = "not fetched"
        if details_dir:
            for suffix in (".html", ".txt", ".md"):
                path = details_dir / f"{item.source_job_id}{suffix}"
                if path.exists():
                    detail_text = path.read_text(encoding="utf-8"); status = "snapshot"; break
        elif args.fetch_live:
            try:
                detail_text = fetch_text(item.source_url); status = "live"
            except Exception as exc:  # review output should survive one broken advert
                status = f"fetch error: {type(exc).__name__}"
        detail = parse_detail(detail_text, item) if detail_text else {
            "title": item.title, "employer": item.employer, "location": item.location,
            "salary_text": "", "closing_date": item.closing_date,
            "description_excerpt": "", "apply_url": "",
        }
        geo_status, geo_reason = geography(detail["location"], detail["description_excerpt"])
        vacancy = BvscVacancy(
            source=SOURCE_NAME, source_job_id=item.source_job_id, title=detail["title"],
            employer=detail["employer"], location=detail["location"], ontap_geography=TARGET_GEOGRAPHY,
            contract_type="", working_pattern="", salary_text=detail["salary_text"], posted_date="",
            closing_date=detail["closing_date"], source_url=item.source_url, screening_basis="title+detail",
            detail_status=status, description_excerpt=detail["description_excerpt"], apply_url=detail["apply_url"],
            geography_status=geo_status, geography_reason=geo_reason,
        )
        vacancy.classification, vacancy.classification_reason = classify(vacancy)
        vacancies.append(vacancy)

    deduplicate_within_source(vacancies)
    jobg8 = load_jobg8_candidates(Path(args.jobg8)) if Path(args.jobg8).exists() else []
    external = load_external_candidates(Path(p) for p in args.external_json)
    for vacancy in vacancies:
        status, _, title, employer, score = duplicate_against(vacancy, jobg8)
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
        if vacancy.classification == "HC" and status in {"DUPLICATE", "POSSIBLE_DUPLICATE"}:
            vacancy.classification = "POSS"
            vacancy.classification_reason = "Possible existing external-source duplicate requires review"
    write_reports(vacancies, Path(args.report_csv), Path(args.summary_md))
    return vacancies


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--fetch-live", action="store_true")
    source.add_argument("--listing-file")
    parser.add_argument("--details-dir")
    parser.add_argument("--jobg8", default="input/jobg8.xlsx")
    parser.add_argument("--external-json", action="append", default=["output-external/northeast-jobs-admin-service.json", "output-external/vonne-admin-service.json"])
    parser.add_argument("--report-csv", default="reviews/external/bvsc-review.csv")
    parser.add_argument("--summary-md", default="reviews/external/bvsc-summary.md")
    return parser


def main() -> int:
    run(build_parser().parse_args())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
