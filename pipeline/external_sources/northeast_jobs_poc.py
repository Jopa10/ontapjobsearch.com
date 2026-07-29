"""North East Jobs review-only ETL proof of concept.

This module deliberately does not write to Ontap's publishable JSON folders.
It reads North East Jobs' public RSS feed, title-screens the feed before making
detail-page requests, keeps only factual vacancy fields, compares candidates
with the current JobG8 workbook, and writes review reports.

Live fetching is opt-in and requires an explicit research-only acknowledgement.
North East Jobs' terms do not authorise commercial republication without
written permission.  This proof of concept therefore never stores or republishes
full vacancy descriptions.
"""
from __future__ import annotations

import argparse
import csv
import html
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree
from zoneinfo import ZoneInfo

import pandas as pd


SOURCE_NAME = "North East Jobs"
RSS_URL = "https://www.northeastjobs.org.uk/RSSJobs.aspx?orgid=62"
TERMS_URL = "https://www.northeastjobs.org.uk/termsandconditions"
ROBOTS_URL = "https://www.northeastjobs.org.uk/robots.txt"
USER_AGENT = "Ontap external-jobs research POC/1.0 (+https://www.ontapjobsearch.com/contact)"

TARGET_CLUSTERS = {
    "North East - Tyneside, Wearside & Northumberland",
    "North East - County Durham & Darlington/Hartlepool",
}
COMBINED_TARGET_REGION = "North East"
TEES_VALLEY_CLUSTER = "North East - Tees Valley"

CLEAR_TITLE_PATTERNS = (
    "administrator",
    "administration assistant",
    "administrative assistant",
    "admin assistant",
    "receptionist",
    "clerical",
    "secretary",
    "customer service advisor",
    "customer service adviser",
    "customer service assistant",
    "customer support advisor",
    "business support officer",
    "business support assistant",
    "office assistant",
    "office support",
    "call handler",
    "contact centre",
    "service administrator",
)

REVIEW_TITLE_PATTERNS = (
    "coordinator",
    "co-ordinator",
    "support officer",
    "assessment officer",
    "review officer",
    "visitor services",
    "customer support",
    "customer enabling",
    "events assistant",
    "housing assistant",
    "pmo secretariat",
    "attendance officer",
    "data and exams officer",
    "data & exams officer",
    "information management",
    "engagement officer",
    "service advisor",
    "service adviser",
)

OFFICE_CONTEXT_PATTERNS = (
    "administrative support",
    "administration support",
    "business support",
    "clerical support",
    "customer service",
    "call handling",
    "data entry",
    "office support",
    "reception service",
)

HARD_PASS_TITLE_PATTERNS = (
    "teacher",
    "teaching assistant",
    "social worker",
    "care worker",
    "care assistant",
    "support worker",
    "nurse",
    "engineer",
    "technician",
    "driver",
    "cleaner",
    "cleaning assistant",
    "catering assistant",
    "kitchen assistant",
    "cook",
    "operative",
    "labourer",
    "manager",
    "head of",
)

SPECIALIST_REVIEW_PATTERNS = (
    "finance",
    "payroll",
    "hr ",
    "human resources",
    "procurement",
    "compliance",
    "legal",
    "housing",
    "send",
    "safeguarding",
    "fundraising",
    "facilities",
    "technical",
    "examinations",
    "attendance",
    "senior",
    "lead ",
)

PRIMARY_CLEAR_PATTERNS = (
    "receptionist",
    "clerical",
    "customer service",
    "business support",
)

STRONG_SPECIALIST_PATTERNS = (
    "finance",
    "payroll",
    "procurement",
    "compliance",
    "legal",
)

INTERNAL_ONLY_PATTERNS = ("internal only", "internal applicants only")

JOBG8_COLUMNS = {
    "job_id": "/Job/DisplayReference",
    "title": "/Job/Position",
    "employer": "/Job/AdvertiserName",
    "area": "/Job/Area",
    "location": "/Job/Location",
    "description": "/Job/Description",
}

REPORT_FIELDS = [
    "title",
    "salary_text",
    "employer",
    "location",
    "posted_date",
    "closing_date",
    "classification",
    "classification_reason",
    "jobg8_check",
    "jobg8_candidate_title",
    "jobg8_candidate_employer",
    "jobg8_match_score",
    "nejobs_duplicate_check",
    "contract_type",
    "working_pattern",
    "ontap_geography",
    "source_job_id",
    "source_url",
]


@dataclass
class FeedItem:
    source_job_id: str
    title: str
    source_url: str
    teaser: str = ""
    contract_type: str = ""
    working_pattern: str = ""
    salary_text: str = ""
    closing_date: str = ""
    posted_date: str = ""
    screening_basis: str = ""


@dataclass
class Vacancy:
    source: str
    source_job_id: str
    title: str
    employer: str
    location: str
    ontap_geography: str
    contract_type: str
    working_pattern: str
    salary_text: str
    posted_date: str
    closing_date: str
    source_url: str
    screening_basis: str
    detail_status: str
    classification: str = ""
    classification_reason: str = ""
    duplicate_status: str = ""
    duplicate_reason: str = ""
    jobg8_candidate_id: str = ""
    jobg8_candidate_title: str = ""
    jobg8_candidate_advertiser: str = ""
    jobg8_match_score: str = ""
    source_duplicate_status: str = ""
    source_duplicate_reason: str = ""


def clean_text(value: object) -> str:
    if value is None or (not isinstance(value, str) and pd.isna(value)):
        return ""
    text = html.unescape(str(value)).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def normalise(value: object) -> str:
    text = clean_text(value).casefold().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalise_title(value: object) -> str:
    text = normalise(value)
    noise = {
        "full", "time", "part", "permanent", "temporary", "fixed", "term",
        "maternity", "cover", "newcastle", "durham", "sunderland", "gateshead",
    }
    return " ".join(token for token in text.split() if token not in noise)


def extract_job_id(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    query_id = urllib.parse.parse_qs(parsed.query).get("jid", [""])[0]
    if query_id:
        return query_id
    match = re.search(r"/(\d+)(?:/)?$", parsed.path)
    return match.group(1) if match else ""


def canonical_job_url(item: FeedItem) -> str:
    if item.source_job_id:
        slug = re.sub(r"[^A-Za-z0-9]+", "_", item.title).strip("_") or "_"
        return f"https://www.northeastjobs.org.uk/job/{slug}/{item.source_job_id}"
    return item.source_url.replace("http://", "https://", 1)


def extract_pipe_field(text: str, label: str) -> str:
    match = re.search(rf"{re.escape(label)}:\s*([^|\n]+)", text, re.I)
    return clean_text(match.group(1)) if match else ""


def parse_rss_xml(text: str) -> list[FeedItem]:
    root = ElementTree.fromstring(text)
    items: list[FeedItem] = []
    for node in root.findall(".//item"):
        title = clean_text(node.findtext("title"))
        url = clean_text(node.findtext("link"))
        description = clean_text(node.findtext("description"))
        source_job_id = extract_job_id(url)
        items.append(
            FeedItem(
                source_job_id=source_job_id,
                title=title,
                source_url=url,
                teaser=description.split("Contract Type:", 1)[0].strip(),
                contract_type=extract_pipe_field(description, "Contract Type"),
                working_pattern=extract_pipe_field(description, "Working Pattern"),
                salary_text=extract_pipe_field(description, "Salary"),
                closing_date=extract_pipe_field(description, "Advert End Date"),
                posted_date=clean_text(node.findtext("pubDate")),
            )
        )
    return items


def parse_rendered_rss(text: str) -> list[FeedItem]:
    """Parse the text-only rendering used when local TLS cannot read the source."""
    blocks = re.findall(
        r"^### \[(.*?)\]\((.*?)\)\n\n(.*?)(?=^### \[|\Z)",
        text,
        re.M | re.S,
    )
    items: list[FeedItem] = []
    for title, url, body in blocks:
        paragraphs = body.strip().split("\n\n")
        teaser = clean_text(paragraphs[0] if paragraphs else "")
        posted = clean_text(paragraphs[-1]) if paragraphs else ""
        source_job_id = extract_job_id(url)
        items.append(
            FeedItem(
                source_job_id=source_job_id,
                title=clean_text(title),
                source_url=clean_text(url),
                teaser=teaser,
                contract_type=extract_pipe_field(body, "Contract Type"),
                working_pattern=extract_pipe_field(body, "Working Pattern"),
                salary_text=extract_pipe_field(body, "Salary"),
                closing_date=extract_pipe_field(body, "Advert End Date"),
                posted_date=posted,
            )
        )
    return items


def parse_rss(text: str) -> list[FeedItem]:
    stripped = text.lstrip()
    if stripped.startswith("<"):
        return parse_rss_xml(text)
    return parse_rendered_rss(text)


def screen_item(item: FeedItem) -> tuple[str, str]:
    """Return fetch priority and reason; these are explicitly provisional rules."""
    title = normalise(item.title)
    teaser = normalise(item.teaser)
    hard_hits = [pattern for pattern in HARD_PASS_TITLE_PATTERNS if pattern in title]
    clear_hits = [pattern for pattern in CLEAR_TITLE_PATTERNS if pattern in title]
    review_hits = [pattern for pattern in REVIEW_TITLE_PATTERNS if pattern in title]
    context_hits = [pattern for pattern in OFFICE_CONTEXT_PATTERNS if pattern in teaser]

    # Clear office titles remain candidates even where a school or charity is
    # the setting.  Only an occupational hard pass defeats them.
    if clear_hits and not hard_hits:
        return "HC_SCREEN", "clear title: " + ", ".join(clear_hits)
    if clear_hits and hard_hits:
        return "POSS_SCREEN", (
            "clear office wording with possible occupational barrier: "
            + ", ".join(hard_hits)
        )
    if review_hits:
        return "POSS_SCREEN", "provisional review title: " + ", ".join(review_hits)
    if context_hits and not hard_hits:
        return "POSS_SCREEN", "office wording in RSS teaser: " + ", ".join(context_hits)
    return "HARD_PASS_SCREEN", (
        "clear out-of-scope title: " + ", ".join(hard_hits)
        if hard_hits
        else "no provisional service-admin signal in title or RSS teaser"
    )


def fetch_text(url: str, timeout: int = 30) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml,text/html;q=0.9,*/*;q=0.1"},
    )
    # Normal runs verify TLS.  There is intentionally no insecure fallback.
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
        return response.read().decode(response.headers.get_content_charset() or "utf-8", "replace")


def label_value(text: str, label: str) -> str:
    markdown_match = re.search(
        rf"(?im)^{re.escape(label)}:\s*\n+\s*([^\n]+)",
        text,
    )
    if markdown_match:
        return clean_text(markdown_match.group(1))

    flattened = clean_text(re.sub(r"<[^>]+>", "\n", text))
    flat_match = re.search(
        rf"{re.escape(label)}:\s*(.+?)(?=(?:Contract Type|Working Pattern|Advert Start Date|Advert End Date|Salary|Job Category|Vacancy ID|Employment Location|Post Number|Number of posts|Closing date):|$)",
        flattened,
        re.I,
    )
    return clean_text(flat_match.group(1)) if flat_match else ""


def page_title(text: str) -> str:
    rendered = re.search(r"(?im)^Title:\s*(.+)$", text)
    if rendered:
        return clean_text(rendered.group(1))
    raw = re.search(r"(?is)<title[^>]*>(.*?)</title>", text)
    return clean_text(re.sub(r"<[^>]+>", "", raw.group(1))) if raw else ""


def employer_from_page_title(page_title_text: str, vacancy_title: str) -> str:
    title = clean_text(page_title_text)
    prefix = clean_text(vacancy_title)
    if title.casefold().startswith(prefix.casefold() + " - "):
        return clean_text(title[len(prefix) + 3 :])
    parts = title.rsplit(" - ", 1)
    return clean_text(parts[1]) if len(parts) == 2 else ""


def parse_detail(text: str, feed_item: FeedItem) -> dict[str, str]:
    return {
        "employer": employer_from_page_title(page_title(text), feed_item.title),
        "location": label_value(text, "Employment Location"),
        "contract_type": label_value(text, "Contract Type") or feed_item.contract_type,
        "working_pattern": label_value(text, "Working Pattern") or feed_item.working_pattern,
        "salary_text": label_value(text, "Salary") or feed_item.salary_text,
        "posted_date": label_value(text, "Advert Start Date") or feed_item.posted_date,
        "closing_date": label_value(text, "Advert End Date") or feed_item.closing_date,
        "vacancy_id": label_value(text, "Vacancy ID") or feed_item.source_job_id,
    }


def load_geo_lookup(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    areas = pd.read_excel(path, sheet_name="Sheet1", dtype=str).fillna("")
    fallback = pd.read_excel(path, sheet_name="LocationFallback", dtype=str).fillna("")
    area_map = {
        normalise(row["Area"]): clean_text(row["Cluster"])
        for _, row in areas.iterrows()
        if clean_text(row["Area"]) and clean_text(row["Cluster"])
    }
    fallback_map = {
        normalise(row["Location"]): clean_text(row["Cluster"])
        for _, row in fallback.iterrows()
        if clean_text(row["Location"])
        and clean_text(row["Cluster"])
        and clean_text(row.get("Status")).upper() == "AUTO"
    }
    return area_map, fallback_map


def cluster_for_location(
    location: str,
    area_map: dict[str, str],
    fallback_map: dict[str, str],
) -> tuple[str, str]:
    key = normalise(location)
    if not key:
        return "", "missing location"
    if key in area_map:
        return area_map[key], "exact area"
    if key in fallback_map:
        return fallback_map[key], "approved location fallback"

    # Match the longest named area as a complete phrase in a longer address.
    padded = f" {key} "
    matches = [
        (len(area), area, cluster)
        for area, cluster in area_map.items()
        if len(area) >= 4 and f" {area} " in padded
    ]
    if matches:
        _, area, cluster = max(matches)
        return cluster, f"area found in address: {area}"

    direct = (
        ("northumberland", "North East - Tyneside, Wearside & Northumberland"),
        ("newcastle", "North East - Tyneside, Wearside & Northumberland"),
        ("gateshead", "North East - Tyneside, Wearside & Northumberland"),
        ("north tyneside", "North East - Tyneside, Wearside & Northumberland"),
        ("south tyneside", "North East - Tyneside, Wearside & Northumberland"),
        ("sunderland", "North East - Tyneside, Wearside & Northumberland"),
        ("county durham", "North East - County Durham & Darlington/Hartlepool"),
        ("darlington", "North East - County Durham & Darlington/Hartlepool"),
        ("hartlepool", "North East - County Durham & Darlington/Hartlepool"),
        ("middlesbrough", TEES_VALLEY_CLUSTER),
        ("stockton", TEES_VALLEY_CLUSTER),
        ("redcar", TEES_VALLEY_CLUSTER),
        ("cleveland", TEES_VALLEY_CLUSTER),
        ("loftus", TEES_VALLEY_CLUSTER),
        ("thornaby", TEES_VALLEY_CLUSTER),
        ("dormanstown", TEES_VALLEY_CLUSTER),
        ("guisborough", TEES_VALLEY_CLUSTER),
        ("saltburn", TEES_VALLEY_CLUSTER),
        ("marske", TEES_VALLEY_CLUSTER),
        ("yarm", TEES_VALLEY_CLUSTER),
    )
    for phrase, cluster in direct:
        if phrase in key:
            return cluster, f"geography phrase: {phrase}"
    return "", "location not mapped"


def infer_location_from_detail(
    detail_text: str,
    area_map: dict[str, str],
    fallback_map: dict[str, str],
) -> tuple[str, str, str]:
    """Use page text only as a last-resort geography hint.

    The full page is held in memory only for this check and is never added to a
    Vacancy or report.  A specific "within ... area" phrase is preferred.  A
    general page-text match is accepted only when all named places found map to
    the same Ontap cluster; this avoids guessing from pages that mention several
    different regions.
    """
    flattened = clean_text(re.sub(r"<[^>]+>", " ", detail_text))
    for pattern in (
        r"\bsettings within (?:the )?(.{2,60}?) area\b",
        r"\broles? (?:available )?(?:throughout|within) (?:the )?(.{2,60}?) area\b",
    ):
        for match in re.finditer(pattern, flattened, re.I):
            candidate = clean_text(match.group(1))
            cluster, reason = cluster_for_location(
                candidate,
                area_map,
                fallback_map,
            )
            if cluster:
                return candidate, cluster, f"specific detail-page phrase: {reason}"

    key = normalise(flattened)
    padded = f" {key} "
    matches: list[tuple[int, int, str, str]] = []
    for area, cluster in {**fallback_map, **area_map}.items():
        marker = f" {area} "
        position = padded.find(marker)
        if len(area) >= 4 and position >= 0:
            matches.append((position, -len(area), area, cluster))
    if not matches:
        return "", "", "no unambiguous geography in detail-page text"

    clusters = {match[3] for match in matches}
    if len(clusters) != 1:
        return "", "", "multiple Ontap geographies mentioned in detail-page text"

    _, _, area, cluster = min(matches)
    return area.title(), cluster, f"unambiguous detail-page place: {area}"


def load_jobg8_candidates(
    workbook: Path,
    area_map: dict[str, str],
    fallback_map: dict[str, str],
) -> list[dict[str, str]]:
    df = pd.read_excel(workbook, dtype=str).fillna("")
    missing = [column for column in JOBG8_COLUMNS.values() if column not in df.columns]
    if missing:
        raise ValueError("JobG8 workbook missing columns: " + ", ".join(missing))

    candidates: list[dict[str, str]] = []
    for _, row in df.iterrows():
        area = clean_text(row[JOBG8_COLUMNS["area"]])
        location = clean_text(row[JOBG8_COLUMNS["location"]])
        cluster, _ = cluster_for_location(area, area_map, fallback_map)
        if cluster not in TARGET_CLUSTERS:
            fallback_cluster, _ = cluster_for_location(
                location,
                area_map,
                fallback_map,
            )
            if fallback_cluster in TARGET_CLUSTERS:
                cluster = fallback_cluster
        if cluster not in TARGET_CLUSTERS:
            continue
        candidates.append(
            {
                "job_id": clean_text(row[JOBG8_COLUMNS["job_id"]]),
                "title": clean_text(row[JOBG8_COLUMNS["title"]]),
                "employer": clean_text(row[JOBG8_COLUMNS["employer"]]),
                "area": area,
                "location": location,
                "description": clean_text(row[JOBG8_COLUMNS["description"]]),
                "cluster": cluster,
            }
        )
    return candidates


def token_jaccard(left: str, right: str) -> float:
    left_tokens = set(normalise_title(left).split())
    right_tokens = set(normalise_title(right).split())
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def similarity(left: str, right: str) -> float:
    left_key = normalise(left)
    right_key = normalise(right)
    if not left_key or not right_key:
        return 0.0
    return SequenceMatcher(None, left_key, right_key).ratio()


def deduplicate(vacancy: Vacancy, jobg8_jobs: list[dict[str, str]]) -> None:
    best: tuple[float, dict[str, str], float, float, bool] | None = None
    for candidate in jobg8_jobs:
        if candidate["cluster"] != vacancy.ontap_geography:
            continue
        title_score = max(
            similarity(normalise_title(vacancy.title), normalise_title(candidate["title"])),
            token_jaccard(vacancy.title, candidate["title"]),
        )
        employer_score = similarity(vacancy.employer, candidate["employer"])
        employer_in_description = bool(
            normalise(vacancy.employer)
            and normalise(vacancy.employer) in normalise(candidate["description"])
        )
        location_score = max(
            similarity(vacancy.location, candidate["area"]),
            similarity(vacancy.location, candidate["location"]),
        )
        combined = (
            0.60 * title_score
            + 0.25 * max(employer_score, 1.0 if employer_in_description else 0.0)
            + 0.15 * location_score
        )
        if best is None or combined > best[0]:
            best = (
                combined,
                candidate,
                title_score,
                employer_score,
                employer_in_description,
            )

    if best is None:
        vacancy.duplicate_status = "UNIQUE"
        vacancy.duplicate_reason = "no JobG8 vacancy in the same Ontap geography"
        return

    score, candidate, title_score, employer_score, employer_in_description = best
    vacancy.jobg8_candidate_id = candidate["job_id"]
    vacancy.jobg8_candidate_title = candidate["title"]
    vacancy.jobg8_candidate_advertiser = candidate["employer"]
    vacancy.jobg8_match_score = f"{score:.3f}"

    if title_score >= 0.92 and (
        employer_score >= 0.85 or employer_in_description
    ):
        vacancy.duplicate_status = "DUPLICATE"
        vacancy.duplicate_reason = (
            f"strong title match ({title_score:.2f}) and "
            + (
                "ultimate employer named in JobG8 description"
                if employer_in_description
                else f"advertiser/employer match ({employer_score:.2f})"
            )
        )
    elif title_score >= 0.88 or (
        score >= 0.68 and (employer_score >= 0.45 or employer_in_description)
    ):
        vacancy.duplicate_status = "POSSIBLE_DUPLICATE"
        vacancy.duplicate_reason = (
            f"manual comparison required: combined {score:.2f}, "
            f"title {title_score:.2f}, employer {employer_score:.2f}"
        )
    else:
        vacancy.duplicate_status = "UNIQUE"
        vacancy.duplicate_reason = (
            f"best same-geography JobG8 candidate below threshold ({score:.2f})"
        )


def deduplicate_within_source(vacancies: list[Vacancy]) -> None:
    """Flag, rather than silently discard, same-source factual duplicates."""
    groups: dict[tuple[str, ...], list[Vacancy]] = {}
    for vacancy in vacancies:
        fingerprint = (
            normalise_title(vacancy.title),
            normalise(vacancy.employer),
            normalise(vacancy.location),
            normalise(vacancy.contract_type),
            normalise(vacancy.working_pattern),
            normalise(vacancy.salary_text),
            normalise(vacancy.closing_date),
        )
        groups.setdefault(fingerprint, []).append(vacancy)

    for group in groups.values():
        if len(group) < 2:
            continue
        ids = ", ".join(vacancy.source_job_id for vacancy in group)
        for vacancy in group:
            vacancy.source_duplicate_status = "POSSIBLE_SOURCE_DUPLICATE"
            vacancy.source_duplicate_reason = (
                f"same title, employer, location, contract, salary and closing date "
                f"as source vacancy IDs {ids}"
            )


def annual_salary_upper(salary_text: str) -> float | None:
    text = clean_text(salary_text).casefold()
    normalised_numbers = text.replace(",", "")
    amounts = [
        float(raw)
        for raw in re.findall(r"(?<![\d.])(\d{4,6}(?:\.\d+)?)(?![\d.])", normalised_numbers)
    ]
    if not amounts:
        amounts = [
            float(raw.replace(",", ""))
            for raw in re.findall(r"£\s*(\d[\d,]*(?:\.\d+)?)", text)
        ]
    if not amounts:
        return None
    upper = max(amounts)
    if "per hour" in text or "p/h" in text or "hourly" in text:
        upper *= 37.5 * 52
    elif "per day" in text or "daily" in text:
        upper *= 260
    elif "per week" in text or "weekly" in text:
        upper *= 52
    elif "per month" in text or "monthly" in text:
        upper *= 12
    return upper


def classify(vacancy: Vacancy, salary_review_threshold: float) -> None:
    title = normalise(vacancy.title)
    combined = normalise(f"{vacancy.title} {vacancy.screening_basis}")

    if vacancy.duplicate_status == "DUPLICATE":
        vacancy.classification = "HARD_PASS"
        vacancy.classification_reason = "confirmed JobG8 duplicate"
        return
    if vacancy.duplicate_status == "POSSIBLE_DUPLICATE":
        vacancy.classification = "POSS"
        vacancy.classification_reason = "possible JobG8 duplicate requires review"
        return
    if vacancy.source_duplicate_status == "POSSIBLE_SOURCE_DUPLICATE":
        vacancy.classification = "POSS"
        vacancy.classification_reason = "possible duplicate within North East Jobs"
        return
    if any(pattern in title for pattern in INTERNAL_ONLY_PATTERNS):
        vacancy.classification = "HARD_PASS"
        vacancy.classification_reason = "not open to external applicants"
        return

    specialist_hits = [
        pattern.strip()
        for pattern in SPECIALIST_REVIEW_PATTERNS
        if pattern in f" {title} "
    ]
    hard_hits = [
        pattern
        for pattern in HARD_PASS_TITLE_PATTERNS
        if pattern in title
    ]
    clear_hits = [
        pattern
        for pattern in CLEAR_TITLE_PATTERNS
        if pattern in title
    ]
    primary_clear_hits = [
        pattern
        for pattern in PRIMARY_CLEAR_PATTERNS
        if pattern in title
    ]
    strong_specialist_hits = [
        pattern
        for pattern in STRONG_SPECIALIST_PATTERNS
        if pattern in title
    ]
    salary_upper = annual_salary_upper(vacancy.salary_text)

    if (
        "derived geography" in vacancy.screening_basis.casefold()
        and any(
            marker in normalise(vacancy.employer)
            for marker in ("recruitment", "supply and training", "staffing")
        )
    ):
        vacancy.classification = "POSS"
        vacancy.classification_reason = (
            "agency-style advert with no structured employment location"
        )
    elif hard_hits and not clear_hits:
        vacancy.classification = "HARD_PASS"
        vacancy.classification_reason = "out-of-scope occupation: " + ", ".join(hard_hits)
    elif specialist_hits and (not primary_clear_hits or strong_specialist_hits):
        vacancy.classification = "POSS"
        vacancy.classification_reason = (
            "transferable office/service title with specialist or borderline wording: "
            + ", ".join(specialist_hits)
        )
    elif salary_upper is not None and salary_upper > salary_review_threshold:
        vacancy.classification = "POSS"
        vacancy.classification_reason = (
            f"annualised upper salary £{salary_upper:,.0f} exceeds "
            f"North East review point £{salary_review_threshold:,.0f}"
        )
    elif clear_hits:
        vacancy.classification = "HC"
        vacancy.classification_reason = "clear transferable title: " + ", ".join(clear_hits)
    elif any(pattern in combined for pattern in REVIEW_TITLE_PATTERNS):
        vacancy.classification = "POSS"
        vacancy.classification_reason = "provisional transferable-office review"
    else:
        vacancy.classification = "HARD_PASS"
        vacancy.classification_reason = "insufficient service-admin evidence"


def read_detail_snapshot(details_dir: Path, job_id: str) -> str | None:
    for suffix in (".txt", ".md", ".html"):
        path = details_dir / f"{job_id}{suffix}"
        if path.exists():
            return path.read_text(encoding="utf-8")
    return None


def build_vacancies(
    items: Iterable[FeedItem],
    *,
    area_map: dict[str, str],
    fallback_map: dict[str, str],
    details_dir: Path | None,
    fetch_live: bool,
    request_interval: float,
    max_detail_requests: int,
) -> tuple[list[Vacancy], dict[str, int], list[str]]:
    counts = {
        "feed_total": 0,
        "hard_pass_before_detail": 0,
        "detail_candidates": 0,
        "detail_failures": 0,
        "outside_target_geography": 0,
        "tees_valley_excluded": 0,
        "target_geography_candidates": 0,
    }
    vacancies: list[Vacancy] = []
    failures: list[str] = []
    fetched = 0

    for item in items:
        counts["feed_total"] += 1
        priority, reason = screen_item(item)
        item.screening_basis = reason
        if priority == "HARD_PASS_SCREEN":
            counts["hard_pass_before_detail"] += 1
            continue
        counts["detail_candidates"] += 1

        detail_text = (
            read_detail_snapshot(details_dir, item.source_job_id)
            if details_dir
            else None
        )
        detail_status = "snapshot"
        if detail_text is None and fetch_live:
            if fetched >= max_detail_requests:
                counts["detail_failures"] += 1
                failures.append(
                    f"{item.source_job_id} — {item.title}: detail-request limit reached"
                )
                continue
            if fetched:
                time.sleep(request_interval)
            fetched += 1
            try:
                detail_text = fetch_text(canonical_job_url(item))
                detail_status = "live"
            except (urllib.error.URLError, TimeoutError, ValueError) as exc:
                counts["detail_failures"] += 1
                failures.append(
                    f"{item.source_job_id} — {item.title}: {type(exc).__name__}"
                )
                continue
        if detail_text is None:
            counts["detail_failures"] += 1
            failures.append(
                f"{item.source_job_id} — {item.title}: no detail snapshot"
            )
            continue

        detail = parse_detail(detail_text, item)
        location = detail["location"]
        derived_location = ""
        cluster, geo_reason = cluster_for_location(location, area_map, fallback_map)
        geo_derived = False
        if not cluster:
            cluster, fallback_reason = cluster_for_location(
                detail["employer"],
                area_map,
                fallback_map,
            )
            if cluster:
                geo_reason = "employer-derived geography: " + fallback_reason
                geo_derived = True
                derived_location = detail["employer"]
        if not cluster:
            cluster, fallback_reason = cluster_for_location(
                item.teaser,
                area_map,
                fallback_map,
            )
            if cluster:
                geo_reason = "RSS-teaser-derived geography: " + fallback_reason
                geo_derived = True
                derived_location = item.teaser
        if not cluster:
            (
                detail_location,
                cluster,
                fallback_reason,
            ) = infer_location_from_detail(
                detail_text,
                area_map,
                fallback_map,
            )
            if cluster:
                geo_reason = "detail-text-derived geography: " + fallback_reason
                geo_derived = True
                derived_location = detail_location
        if cluster == TEES_VALLEY_CLUSTER:
            counts["tees_valley_excluded"] += 1
            continue
        if cluster not in TARGET_CLUSTERS:
            counts["outside_target_geography"] += 1
            continue

        counts["target_geography_candidates"] += 1
        if not location and geo_derived:
            location = f"{clean_text(derived_location)} (derived for filtering)"
        vacancies.append(
            Vacancy(
                source=SOURCE_NAME,
                source_job_id=detail["vacancy_id"] or item.source_job_id,
                title=item.title,
                employer=detail["employer"],
                location=location or "Not stated on detail page",
                ontap_geography=cluster,
                contract_type=detail["contract_type"],
                working_pattern=detail["working_pattern"],
                salary_text=detail["salary_text"],
                posted_date=detail["posted_date"],
                closing_date=detail["closing_date"],
                source_url=canonical_job_url(item),
                screening_basis=f"{reason}; {geo_reason}",
                detail_status=detail_status,
            )
        )
    return vacancies, counts, failures


def review_closing_date(value: str) -> str:
    """Remove the default end-of-day time while retaining meaningful deadlines."""
    return re.sub(r"\s+23:59(?::\d{2})?$", "", clean_text(value))


def review_posted_date(value: str) -> str:
    """Standardise RSS and detail-page dates for the reviewer."""
    text = clean_text(value)
    if not text or re.fullmatch(r"\d{2}/\d{2}/\d{4}", text):
        return text
    try:
        return parsedate_to_datetime(text).strftime("%d/%m/%Y")
    except (TypeError, ValueError, OverflowError):
        return text


def compact_review_text(value: str, max_characters: int) -> str:
    """Cap reviewer-facing text so GitHub's CSV preview remains usable."""
    text = clean_text(value)
    if len(text) <= max_characters:
        return text
    return text[: max_characters - 1].rstrip() + "…"


def review_row(vacancy: Vacancy) -> dict[str, str]:
    """Return the compact, human-facing review record.

    The ETL still calculates its nearest JobG8 candidate for deduplication, but
    weak candidates are deliberately hidden from the review sheet.  They add
    noise and are not credible duplicate decisions.
    """
    plausible_jobg8_match = vacancy.duplicate_status in {
        "DUPLICATE",
        "POSSIBLE_DUPLICATE",
    }
    jobg8_check = (
        vacancy.duplicate_status
        if plausible_jobg8_match
        else "No plausible JobG8 match"
    )
    source_duplicate_check = (
        vacancy.source_duplicate_reason
        if vacancy.source_duplicate_status == "POSSIBLE_SOURCE_DUPLICATE"
        else "No"
    )
    return {
        "title": compact_review_text(vacancy.title, 38),
        "salary_text": compact_review_text(vacancy.salary_text, 30),
        "employer": compact_review_text(vacancy.employer, 27),
        "location": compact_review_text(vacancy.location, 30),
        "posted_date": review_posted_date(vacancy.posted_date),
        "closing_date": review_closing_date(vacancy.closing_date),
        "classification": vacancy.classification,
        "classification_reason": vacancy.classification_reason,
        "jobg8_check": jobg8_check,
        "jobg8_candidate_title": (
            vacancy.jobg8_candidate_title if plausible_jobg8_match else ""
        ),
        "jobg8_candidate_employer": (
            vacancy.jobg8_candidate_advertiser if plausible_jobg8_match else ""
        ),
        "jobg8_match_score": (
            vacancy.jobg8_match_score if plausible_jobg8_match else ""
        ),
        "nejobs_duplicate_check": source_duplicate_check,
        "contract_type": vacancy.contract_type,
        "working_pattern": vacancy.working_pattern,
        "ontap_geography": vacancy.ontap_geography,
        "source_job_id": vacancy.source_job_id,
        "source_url": vacancy.source_url,
    }


def write_csv(path: Path, vacancies: list[Vacancy]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=REPORT_FIELDS,
            lineterminator="\n",
        )
        writer.writeheader()
        for vacancy in sorted(
            vacancies,
            key=lambda item: (
                {"HC": 0, "POSS": 1, "HARD_PASS": 2}.get(item.classification, 9),
                item.ontap_geography,
                item.title.casefold(),
            ),
        ):
            writer.writerow(review_row(vacancy))


def write_summary(
    path: Path,
    *,
    counts: dict[str, int],
    vacancies: list[Vacancy],
    jobg8_count: int,
    rss_source: str,
    failures: list[str],
) -> None:
    classification_counts = {
        label: sum(v.classification == label for v in vacancies)
        for label in ("HC", "POSS", "HARD_PASS")
    }
    duplicate_counts = {
        label: sum(v.duplicate_status == label for v in vacancies)
        for label in ("DUPLICATE", "POSSIBLE_DUPLICATE", "UNIQUE")
    }
    source_duplicate_count = sum(
        v.source_duplicate_status == "POSSIBLE_SOURCE_DUPLICATE"
        for v in vacancies
    )
    lines = [
        "# North East Jobs ETL proof-of-concept review",
        "",
        f"Run generated: {datetime.now(ZoneInfo('Europe/London')).isoformat(timespec='seconds')}",
        f"RSS input: {rss_source}",
        f"JobG8 comparison rows in target geographies: {jobg8_count}",
        "",
        "## Funnel",
        "",
        f"- RSS vacancies read: {counts['feed_total']}",
        f"- Hard-pass title/teaser screen before detail requests: {counts['hard_pass_before_detail']}",
        f"- Detail candidates: {counts['detail_candidates']}",
        f"- Detail failures or unavailable snapshots: {counts['detail_failures']}",
        f"- Outside the two target geographies: {counts['outside_target_geography']}",
        f"- Tees Valley explicitly excluded: {counts['tees_valley_excluded']}",
        f"- Target-geography candidates reviewed: {counts['target_geography_candidates']}",
        "",
        "## Detail diagnostics",
        "",
    ]
    if failures:
        lines.extend(f"- {failure}" for failure in failures)
    else:
        lines.append("- No unresolved detail-page failures.")
    lines.extend(
        [
        "",
        "## Review outcomes",
        "",
        f"- HC: {classification_counts['HC']}",
        f"- POSS: {classification_counts['POSS']}",
        f"- Hard pass: {classification_counts['HARD_PASS']}",
        f"- Confirmed JobG8 duplicates: {duplicate_counts['DUPLICATE']}",
        f"- Possible JobG8 duplicates: {duplicate_counts['POSSIBLE_DUPLICATE']}",
        f"- Likely unique to North East Jobs: {duplicate_counts['UNIQUE']}",
        f"- Rows in possible within-source duplicate groups: {source_duplicate_count}",
        "",
        "## HC and POSS roles",
        "",
        "| Decision | Vacancy | Employer | Location | Closing | JobG8 | Source duplicate |",
        "|---|---|---|---|---|---|---|",
        ]
    )
    for vacancy in sorted(
        (v for v in vacancies if v.classification in {"HC", "POSS"}),
        key=lambda item: (item.classification != "HC", item.title.casefold()),
    ):
        lines.append(
            "| "
            + " | ".join(
                [
                    vacancy.classification,
                    f"[{vacancy.title}]({vacancy.source_url})",
                    vacancy.employer or "Not parsed",
                    vacancy.location,
                    review_closing_date(vacancy.closing_date),
                    (
                        vacancy.duplicate_status
                        if vacancy.duplicate_status
                        in {"DUPLICATE", "POSSIBLE_DUPLICATE"}
                        else "No plausible match"
                    ),
                    vacancy.source_duplicate_status or "NO",
                ]
            )
            + " |"
        )
    hard_passes = [v for v in vacancies if v.classification == "HARD_PASS"]
    lines.extend(["", "## Hard passes", ""])
    if hard_passes:
        for vacancy in sorted(hard_passes, key=lambda item: item.title.casefold()):
            lines.append(
                f"- [{vacancy.title}]({vacancy.source_url}) — "
                f"{vacancy.classification_reason}."
            )
    else:
        lines.append("- None after geography and deduplication checks.")
    lines.extend(
        [
            "",
            "## Safety boundary",
            "",
            "- Review-only output; no Ontap publishable JSON is written.",
            "- Only factual vacancy fields are retained; full descriptions are not stored.",
            "- Detail pages are fetched only after a provisional title/teaser screen.",
            "- North East Jobs terms require written permission for commercial reuse of site material.",
            "- The source had no retrievable robots.txt (404) when the POC was designed.",
            "- HC/POSS rules are provisional and do not amend Ontap's permanent selection policy.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobg8", type=Path, default=Path("input/jobg8.xlsx"))
    parser.add_argument("--geo-lookup", type=Path, default=Path("geo/geo_lookup.xlsx"))
    parser.add_argument("--rss-file", type=Path)
    parser.add_argument("--details-dir", type=Path)
    parser.add_argument("--fetch-live", action="store_true")
    parser.add_argument("--acknowledge-research-only", action="store_true")
    parser.add_argument("--request-interval", type=float, default=0.5)
    parser.add_argument("--max-detail-requests", type=int, default=80)
    parser.add_argument(
        "--report-csv",
        type=Path,
        default=Path("reviews/external/northeast-jobs-review.csv"),
    )
    parser.add_argument(
        "--summary-md",
        type=Path,
        default=Path("reviews/external/northeast-jobs-summary.md"),
    )
    parser.add_argument("--salary-review-threshold", type=float, default=30_000)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.fetch_live and not args.acknowledge_research_only:
        raise SystemExit(
            "STOP: live fetching is research-only. Re-run with "
            "--acknowledge-research-only after reviewing the source terms."
        )
    if not args.fetch_live and args.rss_file is None:
        raise SystemExit("STOP: provide --rss-file or explicitly opt into --fetch-live.")

    if args.rss_file:
        rss_text = args.rss_file.read_text(encoding="utf-8")
        rss_source = str(args.rss_file)
    else:
        rss_text = fetch_text(RSS_URL)
        rss_source = RSS_URL

    items = parse_rss(rss_text)
    if not items:
        raise SystemExit("STOP: no RSS vacancies parsed; source structure may have changed.")

    area_map, fallback_map = load_geo_lookup(args.geo_lookup)
    vacancies, counts, failures = build_vacancies(
        items,
        area_map=area_map,
        fallback_map=fallback_map,
        details_dir=args.details_dir,
        fetch_live=args.fetch_live,
        request_interval=max(args.request_interval, 0.0),
        max_detail_requests=max(args.max_detail_requests, 0),
    )
    jobg8_jobs = load_jobg8_candidates(args.jobg8, area_map, fallback_map)
    for vacancy in vacancies:
        deduplicate(vacancy, jobg8_jobs)
    deduplicate_within_source(vacancies)
    for vacancy in vacancies:
        classify(vacancy, args.salary_review_threshold)

    write_csv(args.report_csv, vacancies)
    write_summary(
        args.summary_md,
        counts=counts,
        vacancies=vacancies,
        jobg8_count=len(jobg8_jobs),
        rss_source=rss_source,
        failures=failures,
    )
    print(
        f"North East Jobs POC: {counts['feed_total']} feed rows -> "
        f"{len(vacancies)} target candidates. "
        f"Reports: {args.report_csv}, {args.summary_md}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
