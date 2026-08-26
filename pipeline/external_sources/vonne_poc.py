"""VONNE review-only external vacancy ETL proof of concept.

This module deliberately has no publishing mode. It reads VONNE's public Job
Finder listing, fetches detail pages only where useful, retains factual vacancy
fields, filters to Ontap's agreed North East geography, compares candidates
with JobG8 and the currently approved North East Jobs subset, classifies each
retained vacancy, and writes CSV and Markdown review outputs.

Full source descriptions are never stored in a Vacancy or written to reports.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import ssl
import sys
import time
import urllib.error
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
    COMBINED_TARGET_REGION,
    HARD_PASS_TITLE_PATTERNS,
    INTERNAL_ONLY_PATTERNS,
    PRIMARY_CLEAR_PATTERNS,
    REVIEW_TITLE_PATTERNS,
    SPECIALIST_REVIEW_PATTERNS,
    STRONG_SPECIALIST_PATTERNS,
    TARGET_CLUSTERS,
    TEES_VALLEY_CLUSTER,
    ManualDecisionState,
    Vacancy,
    annual_salary_upper,
    clean_text,
    cluster_for_location,
    deduplicate_within_source,
    empty_manual_decisions,
    load_geo_lookup,
    load_jobg8_candidates,
    normalise,
    normalise_title,
    parse_source_datetime,
    similarity,
    token_jaccard,
)

SOURCE_NAME = "VONNE"
SOURCE_CODE = "VONNE"
LIST_URL = "https://www.vonne.org.uk/vonne-jobs"
TERMS_URL = "https://www.vonne.org.uk/terms-and-conditions"
ROBOTS_URL = "https://www.vonne.org.uk/robots.txt"
USER_AGENT = (
    "Ontap external-jobs research POC/1.0 "
    "(+https://www.ontapjobsearch.com/contact)"
)

TEES_EXCLUSION_MARKERS = (
    "tees valley",
    "middlesbrough",
    "stockton",
    "redcar",
    "cleveland",
    "guisborough",
    "saltburn",
    "thornaby",
    "yarm",
)

GENERIC_NORTH_EAST_MARKERS = (
    "north east",
    "north-east",
    "regionwide",
    "region wide",
    "home-based",
    "home based",
    "hybrid",
    "remote",
)

VONNE_TARGET_ALIASES = {
    "tyne and wear": "North East - Tyneside, Wearside & Northumberland",
    "t&w": "North East - Tyneside, Wearside & Northumberland",
}

VONNE_HARD_PASS_TITLE_PATTERNS = HARD_PASS_TITLE_PATTERNS + (
    "chief executive",
    "ceo",
    "chair",
    "trustee",
    "volunteer",
    "consultancy",
    "consultant",
    "youth worker",
    "worker",
    "project worker",
    "family worker",
    "practitioner",
    "producer",
)

VONNE_REVIEW_TITLE_PATTERNS = REVIEW_TITLE_PATTERNS + (
    "programme officer",
    "project officer",
    "outreach officer",
    "engagement officer",
    "coordinator",
    "co-ordinator",
)

REPORT_FIELDS = [
    "source",
    "tracking_key",
    "title",
    "salary_text",
    "employer",
    "location",
    "based",
    "closing_date",
    "contract_type",
    "role_type",
    "hours",
    "role_description",
    "classification",
    "classification_reason",
    "geography_status",
    "geography_reason",
    "ontap_geography",
    "jobg8_check",
    "jobg8_candidate_title",
    "jobg8_candidate_employer",
    "jobg8_match_score",
    "nejobs_check",
    "nejobs_candidate_title",
    "nejobs_candidate_employer",
    "nejobs_match_score",
    "vonne_duplicate_check",
    "vacancy_fingerprint",
    "source_job_id",
    "source_url",
    "detail_status",
    "manual_action",
    "final_decision",
]


@dataclass
class ListingItem:
    source_job_id: str
    title: str
    employer: str
    location: str
    salary_text: str
    closing_date: str
    source_url: str


@dataclass
class VonneVacancy(Vacancy):
    role_type: str = ""
    based: str = ""
    hours: str = ""
    role_description: str = ""
    geography_status: str = ""
    geography_reason: str = ""
    nejobs_duplicate_status: str = ""
    nejobs_duplicate_reason: str = ""
    nejobs_candidate_id: str = ""
    nejobs_candidate_title: str = ""
    nejobs_candidate_employer: str = ""
    nejobs_match_score: str = ""


class ListingHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.records: dict[str, dict[str, object]] = {}
        self.order: list[str] = []
        self.current_id = ""
        self.anchor_id = ""
        self.anchor_text: list[str] = []

    @staticmethod
    def _cid(href: str) -> str:
        parsed = urllib.parse.urljoin(LIST_URL, href)
        return clean_text(
            urllib.parse.parse_qs(
                urllib.parse.urlsplit(parsed).query
            ).get("cid", [""])[0]
        )

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag.casefold() != "a":
            return
        href = dict(attrs).get("href") or ""
        if "vonne-jobs-details" not in href:
            return
        cid = self._cid(href)
        if not cid:
            return
        if cid not in self.records:
            self.records[cid] = {
                "source_job_id": cid,
                "source_url": urllib.parse.urljoin(LIST_URL, href),
                "title": "",
                "body": [],
            }
            self.order.append(cid)
        self.current_id = cid
        self.anchor_id = cid
        self.anchor_text = []

    def handle_data(self, data: str) -> None:
        text = clean_text(data)
        if not text:
            return
        if self.anchor_id:
            self.anchor_text.append(text)
        elif self.current_id:
            body = self.records[self.current_id]["body"]
            assert isinstance(body, list)
            body.append(text)

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() != "a" or not self.anchor_id:
            return
        text = clean_text(" ".join(self.anchor_text))
        record = self.records[self.anchor_id]
        if (
            text.casefold() != "find out more"
            and not clean_text(record["title"])
        ):
            record["title"] = text
        self.anchor_id = ""
        self.anchor_text = []


def extract_label(lines: list[str], label: str) -> str:
    wanted = normalise(label)
    for index, line in enumerate(lines):
        line_text = clean_text(line)
        if not line_text:
            continue
        normal = normalise(line_text)
        if normal == wanted:
            return (
                clean_text(lines[index + 1])
                if index + 1 < len(lines)
                else ""
            )
        prefix = label.rstrip(":") + ":"
        if line_text.casefold().startswith(prefix.casefold()):
            return clean_text(line_text[len(prefix) :])
    return ""


def listing_record_to_item(record: dict[str, object]) -> ListingItem:
    body = [
        clean_text(value)
        for value in record.get("body", [])
        if clean_text(value)
    ]
    labels = ("Salary", "Location", "Closing Date")
    employer = ""
    for line in body:
        if line.casefold() in {"find out more", "job finder"}:
            continue
        if any(
            line.casefold().startswith(label.casefold() + ":")
            for label in labels
        ):
            continue
        employer = line
        break
    return ListingItem(
        source_job_id=clean_text(record.get("source_job_id")),
        title=clean_text(record.get("title")),
        employer=employer,
        location=extract_label(body, "Location"),
        salary_text=extract_label(body, "Salary"),
        closing_date=extract_label(body, "Closing Date"),
        source_url=clean_text(record.get("source_url")),
    )


def parse_listing_html(text: str) -> list[ListingItem]:
    parser = ListingHTMLParser()
    parser.feed(text)
    items = [
        listing_record_to_item(parser.records[cid])
        for cid in parser.order
    ]
    return [item for item in items if item.source_job_id and item.title]


def parse_listing_markdown(text: str) -> list[ListingItem]:
    starts = list(
        re.finditer(
            r"(?m)^###\s+\[(?P<title>[^\]]+)\]"
            r"\((?P<url>[^\n)]*vonne-jobs-details\?cid="
            r"(?P<cid>\d+)[^\n)]*)\)\s*$",
            text,
        )
    )
    items: list[ListingItem] = []
    for index, match in enumerate(starts):
        end = (
            starts[index + 1].start()
            if index + 1 < len(starts)
            else len(text)
        )
        block = text[match.end() : end]
        lines = [
            clean_text(re.sub(r"^[*\-]\s*", "", line))
            for line in block.splitlines()
        ]
        lines = [line for line in lines if line]
        employer = ""
        for line in lines:
            if line.casefold() == "find out more" or line.startswith("["):
                continue
            if any(
                line.casefold().startswith(label)
                for label in (
                    "salary:",
                    "location:",
                    "closing date:",
                )
            ):
                continue
            employer = line
            break
        items.append(
            ListingItem(
                source_job_id=match.group("cid"),
                title=clean_text(match.group("title")),
                employer=employer,
                location=extract_label(lines, "Location"),
                salary_text=extract_label(lines, "Salary"),
                closing_date=extract_label(lines, "Closing Date"),
                source_url=urllib.parse.urljoin(
                    LIST_URL,
                    html.unescape(match.group("url")),
                ),
            )
        )
    return items


def parse_listing(text: str) -> list[ListingItem]:
    if text.lstrip().startswith("<"):
        return parse_listing_html(text)
    return parse_listing_markdown(text)


class DetailHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self.in_title = False
        self.title_parts: list[str] = []
        self.in_h1 = False
        self.h1_parts: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        _attrs: list[tuple[str, str | None]],
    ) -> None:
        name = tag.casefold()
        if name == "title":
            self.in_title = True
        elif name == "h1":
            self.in_h1 = True

    def handle_endtag(self, tag: str) -> None:
        name = tag.casefold()
        if name == "title":
            self.in_title = False
        elif name == "h1":
            self.in_h1 = False

    def handle_data(self, data: str) -> None:
        text = clean_text(data)
        if not text:
            return
        self.lines.append(text)
        if self.in_title:
            self.title_parts.append(text)
        if self.in_h1:
            self.h1_parts.append(text)


def title_and_employer(
    value: str,
    fallback_title: str,
    fallback_employer: str,
) -> tuple[str, str]:
    text = clean_text(value)
    text = re.sub(r"\s*[|\-]\s*VONNE.*$", "", text, flags=re.I)
    text = re.sub(r"^Job:\s*", "", text, flags=re.I)
    match = re.match(r"(.+?)\s+at\s+(.+)$", text, flags=re.I)
    if match:
        return clean_text(match.group(1)), clean_text(match.group(2))
    return clean_text(fallback_title), clean_text(fallback_employer)


def parse_detail(text: str, item: ListingItem) -> dict[str, str]:
    if text.lstrip().startswith("<"):
        parser = DetailHTMLParser()
        parser.feed(text)
        lines = parser.lines
        heading = (
            clean_text(" ".join(parser.h1_parts))
            or clean_text(" ".join(parser.title_parts))
        )
    else:
        lines = [
            clean_text(line)
            for line in text.splitlines()
            if clean_text(line)
        ]
        heading = extract_label(lines, "Title")
        if not heading:
            heading = next(
                (
                    line.lstrip("# ")
                    for line in lines
                    if line.startswith("#")
                ),
                "",
            )
    title, employer = title_and_employer(
        heading,
        item.title,
        item.employer,
    )
    return {
        "title": title,
        "employer": employer,
        "contract_type": extract_label(lines, "Contract Type"),
        "role_type": extract_label(lines, "Role Type"),
        "hours": extract_label(lines, "Hours"),
        "closing_date": (
            extract_label(lines, "Application deadline")
            or item.closing_date
        ),
        "based": extract_label(lines, "Based"),
        "salary_text": extract_label(lines, "Salary") or item.salary_text,
        "location": extract_label(lines, "Location") or item.location,
        "role_description": extract_label(lines, "Role description"),
    }


RETRYABLE_HTTP_STATUS = {408, 425, 429, 500, 502, 503, 504}


def fetch_text(
    url: str,
    timeout: int = 30,
    *,
    max_attempts: int = 4,
    retry_delay: float = 5.0,
) -> str:
    """Fetch one VONNE page with bounded transient-network retries."""
    attempts = max(int(max_attempts), 1)
    base_delay = max(float(retry_delay), 0.0)
    last_error: BaseException | None = None

    for attempt in range(1, attempts + 1):
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": (
                    "text/html,application/xhtml+xml;q=0.9,*/*;q=0.1"
                ),
                "Accept-Language": "en-GB,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "close",
            },
        )
        context = ssl.create_default_context()
        try:
            with urllib.request.urlopen(
                request,
                timeout=timeout,
                context=context,
            ) as response:
                return response.read().decode(
                    response.headers.get_content_charset() or "utf-8",
                    "replace",
                )
        except urllib.error.HTTPError as exc:
            if exc.code not in RETRYABLE_HTTP_STATUS:
                raise
            last_error = exc
        except (
            urllib.error.URLError,
            TimeoutError,
            ConnectionError,
            ssl.SSLError,
        ) as exc:
            last_error = exc

        if attempt >= attempts:
            assert last_error is not None
            raise last_error

        delay = min(base_delay * (2 ** (attempt - 1)), 30.0)
        print(
            f"VONNE fetch attempt {attempt}/{attempts} failed for {url}: "
            f"{type(last_error).__name__}; retrying in {delay:g}s.",
            file=sys.stderr,
        )
        time.sleep(delay)

    raise RuntimeError("VONNE fetch retry loop ended unexpectedly")


def read_detail_snapshot(
    details_dir: Path,
    source_job_id: str,
) -> str | None:
    for suffix in (".html", ".txt", ".md"):
        path = details_dir / f"{source_job_id}{suffix}"
        if path.exists():
            return path.read_text(encoding="utf-8")
    return None


def screen_item(item: ListingItem) -> tuple[str, str]:
    title = normalise(item.title)
    clear_hits = [
        pattern
        for pattern in CLEAR_TITLE_PATTERNS
        if pattern in title
    ]
    review_hits = [
        pattern
        for pattern in VONNE_REVIEW_TITLE_PATTERNS
        if pattern in title
    ]
    hard_hits = [
        pattern
        for pattern in VONNE_HARD_PASS_TITLE_PATTERNS
        if pattern in title
    ]
    if clear_hits and not hard_hits:
        return "HC_SCREEN", "clear title: " + ", ".join(clear_hits)
    if clear_hits or review_hits:
        return "POSS_SCREEN", "borderline transferable title"
    if hard_hits:
        return (
            "HARD_PASS_SCREEN",
            "clear out-of-scope title: " + ", ".join(hard_hits),
        )
    return (
        "HARD_PASS_SCREEN",
        "no provisional service-admin signal in title",
    )


def alias_cluster(value: str) -> tuple[str, str]:
    key = normalise(value)
    for phrase, cluster in VONNE_TARGET_ALIASES.items():
        if normalise(phrase) in key:
            return cluster, f"VONNE location alias: {phrase}"
    return "", ""


def geography_for_item(
    *,
    title: str,
    employer: str,
    location: str,
    based: str,
    area_map: dict[str, str],
    fallback_map: dict[str, str],
) -> tuple[str, str, str]:
    explicit = " | ".join(
        value
        for value in (location, based)
        if clean_text(value)
    )
    exclusion_evidence = " | ".join((title, explicit))
    exclusion_key = normalise(exclusion_evidence)
    exclusion_cluster, exclusion_reason = cluster_for_location(
        exclusion_evidence,
        area_map,
        fallback_map,
    )
    if exclusion_cluster == TEES_VALLEY_CLUSTER or any(
        normalise(marker) in exclusion_key
        for marker in TEES_EXCLUSION_MARKERS
    ):
        return (
            TEES_VALLEY_CLUSTER,
            "EXCLUDED",
            exclusion_reason or "explicit Tees Valley wording",
        )

    for value, label in (
        (location, "location"),
        (based, "based"),
    ):
        cluster, reason = cluster_for_location(
            value,
            area_map,
            fallback_map,
        )
        if not cluster:
            cluster, reason = alias_cluster(value)
        if cluster in TARGET_CLUSTERS:
            return cluster, "CONFIRMED", f"{label}: {reason}"
        if cluster == TEES_VALLEY_CLUSTER:
            return cluster, "EXCLUDED", f"{label}: {reason}"

    employer_cluster, employer_reason = cluster_for_location(
        employer,
        area_map,
        fallback_map,
    )
    if employer_cluster in TARGET_CLUSTERS:
        return (
            employer_cluster,
            "DERIVED_REVIEW",
            "employer-derived geography: " + employer_reason,
        )
    if employer_cluster == TEES_VALLEY_CLUSTER:
        return (
            employer_cluster,
            "EXCLUDED",
            "employer-derived geography: " + employer_reason,
        )

    generic_text = normalise(explicit)
    if any(
        normalise(marker) in generic_text
        for marker in GENERIC_NORTH_EAST_MARKERS
    ):
        return (
            COMBINED_TARGET_REGION,
            "GENERIC_REVIEW",
            "generic VONNE location requires manual North East check",
        )
    return (
        "",
        "OUTSIDE_OR_UNMAPPED",
        "no accepted North East location could be confirmed",
    )


def make_vacancy(
    item: ListingItem,
    detail: dict[str, str],
    *,
    screening_reason: str,
    detail_status: str,
    area_map: dict[str, str],
    fallback_map: dict[str, str],
) -> VonneVacancy:
    title = detail.get("title") or item.title
    employer = detail.get("employer") or item.employer
    location = detail.get("location") or item.location
    based = detail.get("based", "")
    cluster, geography_status, geography_reason = geography_for_item(
        title=title,
        employer=employer,
        location=location,
        based=based,
        area_map=area_map,
        fallback_map=fallback_map,
    )
    return VonneVacancy(
        source=SOURCE_NAME,
        source_job_id=item.source_job_id,
        title=title,
        employer=employer,
        location=location or based or "Not stated",
        ontap_geography=cluster,
        contract_type=detail.get("contract_type", ""),
        working_pattern=detail.get("hours", ""),
        salary_text=(
            detail.get("salary_text")
            or item.salary_text
        ),
        posted_date="",
        closing_date=(
            detail.get("closing_date")
            or item.closing_date
        ),
        source_url=item.source_url,
        screening_basis=screening_reason,
        detail_status=detail_status,
        role_type=detail.get("role_type", ""),
        based=based,
        hours=detail.get("hours", ""),
        role_description=detail.get("role_description", ""),
        geography_status=geography_status,
        geography_reason=geography_reason,
    )


def build_vacancies(
    items: Iterable[ListingItem],
    *,
    area_map: dict[str, str],
    fallback_map: dict[str, str],
    details_dir: Path | None,
    fetch_live: bool,
    request_interval: float,
    max_detail_requests: int,
) -> tuple[list[VonneVacancy], dict[str, int], list[str]]:
    counts = {
        "listing_total": 0,
        "detail_candidates": 0,
        "detail_fetched": 0,
        "detail_failures": 0,
        "hard_pass_without_detail": 0,
        "tees_valley_excluded": 0,
        "outside_or_unmapped": 0,
        "target_candidates": 0,
        "generic_geography_review": 0,
    }
    failures: list[str] = []
    vacancies: list[VonneVacancy] = []
    fetched = 0

    for item in items:
        counts["listing_total"] += 1
        priority, reason = screen_item(item)
        detail: dict[str, str] = {}
        detail_status = "not_fetched_hard_pass"
        if priority != "HARD_PASS_SCREEN":
            counts["detail_candidates"] += 1
            detail_text = (
                read_detail_snapshot(
                    details_dir,
                    item.source_job_id,
                )
                if details_dir
                else None
            )
            if detail_text is not None:
                detail = parse_detail(detail_text, item)
                detail_status = "snapshot"
            elif fetch_live and fetched < max_detail_requests:
                if fetched:
                    time.sleep(request_interval)
                fetched += 1
                try:
                    detail = parse_detail(
                        fetch_text(item.source_url),
                        item,
                    )
                    detail_status = "live"
                    counts["detail_fetched"] += 1
                except (
                    urllib.error.URLError,
                    TimeoutError,
                    ValueError,
                ) as exc:
                    detail_status = "failed_listing_fallback"
                    counts["detail_failures"] += 1
                    failures.append(
                        f"{item.source_job_id} — {item.title}: "
                        f"{type(exc).__name__}"
                    )
            else:
                detail_status = "missing_listing_fallback"
                counts["detail_failures"] += 1
                failures.append(
                    f"{item.source_job_id} — {item.title}: "
                    "no detail snapshot"
                )
        else:
            counts["hard_pass_without_detail"] += 1

        vacancy = make_vacancy(
            item,
            detail,
            screening_reason=reason,
            detail_status=detail_status,
            area_map=area_map,
            fallback_map=fallback_map,
        )
        if vacancy.geography_status == "EXCLUDED":
            counts["tees_valley_excluded"] += 1
            continue
        if vacancy.geography_status == "OUTSIDE_OR_UNMAPPED":
            counts["outside_or_unmapped"] += 1
            continue
        if vacancy.geography_status in {
            "GENERIC_REVIEW",
            "DERIVED_REVIEW",
        }:
            counts["generic_geography_review"] += 1
        counts["target_candidates"] += 1
        vacancies.append(vacancy)
    return vacancies, counts, failures


def deduplicate_jobg8(
    vacancy: VonneVacancy,
    jobg8_jobs: list[dict[str, str]],
) -> None:
    best: tuple[
        float,
        dict[str, str],
        float,
        float,
        bool,
    ] | None = None
    for candidate in jobg8_jobs:
        if (
            vacancy.ontap_geography in TARGET_CLUSTERS
            and candidate["cluster"] != vacancy.ontap_geography
        ):
            continue
        title_score = max(
            similarity(
                normalise_title(vacancy.title),
                normalise_title(candidate["title"]),
            ),
            token_jaccard(
                vacancy.title,
                candidate["title"],
            ),
        )
        employer_score = similarity(
            vacancy.employer,
            candidate["employer"],
        )
        employer_in_description = bool(
            normalise(vacancy.employer)
            and normalise(vacancy.employer)
            in normalise(candidate["description"])
        )
        location_score = max(
            similarity(
                vacancy.location,
                candidate["area"],
            ),
            similarity(
                vacancy.location,
                candidate["location"],
            ),
        )
        combined = (
            0.60 * title_score
            + 0.25
            * max(
                employer_score,
                1.0 if employer_in_description else 0.0,
            )
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
        vacancy.duplicate_reason = (
            "no JobG8 vacancy in the accepted North East geographies"
        )
        return
    (
        score,
        candidate,
        title_score,
        employer_score,
        employer_in_description,
    ) = best
    vacancy.jobg8_candidate_id = candidate["job_id"]
    vacancy.jobg8_candidate_title = candidate["title"]
    vacancy.jobg8_candidate_advertiser = candidate["employer"]
    vacancy.jobg8_match_score = f"{score:.3f}"
    if title_score >= 0.92 and (
        employer_score >= 0.85
        or employer_in_description
    ):
        vacancy.duplicate_status = "DUPLICATE"
        vacancy.duplicate_reason = (
            "strong title and employer evidence"
        )
    elif title_score >= 0.88 or (
        score >= 0.68
        and (
            employer_score >= 0.45
            or employer_in_description
        )
    ):
        vacancy.duplicate_status = "POSSIBLE_DUPLICATE"
        vacancy.duplicate_reason = (
            f"manual comparison required: combined {score:.2f}"
        )
    else:
        vacancy.duplicate_status = "UNIQUE"
        vacancy.duplicate_reason = (
            f"best JobG8 candidate below threshold ({score:.2f})"
        )


def load_nejobs_candidates(
    path: Path,
    *,
    now: datetime | None = None,
) -> list[dict[str, str]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(
            "approved NEJobs JSON must contain a list"
        )
    candidates: list[dict[str, str]] = []
    current = now or datetime.now(ZoneInfo("Europe/London"))
    if current.tzinfo is None:
        current = current.replace(tzinfo=ZoneInfo("Europe/London"))
    for row in data:
        if not isinstance(row, dict):
            continue
        closing_value = (
            clean_text(row.get("closing_datetime"))
            or clean_text(row.get("closing_date"))
        )
        closing_deadline = parse_source_datetime(
            closing_value,
            end_of_day_when_date_only=True,
        )
        if (
            closing_deadline is not None
            and closing_deadline < current
        ):
            continue
        candidates.append(
            {
                "job_id": clean_text(row.get("job_id")),
                "title": clean_text(row.get("title")),
                "employer": clean_text(row.get("company")),
                "location": clean_text(row.get("location")),
                "salary_text": clean_text(
                    row.get("salary_text")
                ),
            }
        )
    return candidates


def salary_match_score(left: str, right: str) -> float:
    left_value = annual_salary_upper(left)
    right_value = annual_salary_upper(right)
    if left_value is None or right_value is None:
        return 0.0
    difference = abs(left_value - right_value) / max(
        left_value,
        right_value,
        1.0,
    )
    if difference <= 0.01:
        return 1.0
    if difference <= 0.05:
        return 0.8
    if difference <= 0.12:
        return 0.5
    return 0.0


def deduplicate_nejobs(
    vacancy: VonneVacancy,
    candidates: list[dict[str, str]],
) -> None:
    best: tuple[
        float,
        dict[str, str],
        float,
        float,
        float,
        float,
    ] | None = None
    for candidate in candidates:
        title_score = max(
            similarity(
                normalise_title(vacancy.title),
                normalise_title(candidate["title"]),
            ),
            token_jaccard(
                vacancy.title,
                candidate["title"],
            ),
        )
        employer_score = similarity(
            vacancy.employer,
            candidate["employer"],
        )
        location_score = similarity(
            vacancy.location,
            candidate["location"],
        )
        salary_score = salary_match_score(
            vacancy.salary_text,
            candidate["salary_text"],
        )
        combined = (
            0.52 * title_score
            + 0.30 * employer_score
            + 0.10 * location_score
            + 0.08 * salary_score
        )
        if best is None or combined > best[0]:
            best = (
                combined,
                candidate,
                title_score,
                employer_score,
                location_score,
                salary_score,
            )
    if best is None:
        vacancy.nejobs_duplicate_status = "UNIQUE"
        vacancy.nejobs_duplicate_reason = (
            "no approved NEJobs vacancy available for comparison"
        )
        return
    (
        score,
        candidate,
        title_score,
        employer_score,
        location_score,
        salary_score,
    ) = best
    vacancy.nejobs_candidate_id = candidate["job_id"]
    vacancy.nejobs_candidate_title = candidate["title"]
    vacancy.nejobs_candidate_employer = candidate["employer"]
    vacancy.nejobs_match_score = f"{score:.3f}"
    if (
        title_score >= 0.92
        and employer_score >= 0.85
        and (
            location_score >= 0.55
            or salary_score >= 0.8
        )
    ):
        vacancy.nejobs_duplicate_status = "DUPLICATE"
        vacancy.nejobs_duplicate_reason = (
            "strong title, ultimate-employer and supporting factual match"
        )
    elif (
        title_score >= 0.88
        and employer_score >= 0.55
    ) or (
        score >= 0.70
        and employer_score >= 0.45
    ):
        vacancy.nejobs_duplicate_status = "POSSIBLE_DUPLICATE"
        vacancy.nejobs_duplicate_reason = (
            f"manual comparison required: combined {score:.2f}"
        )
    else:
        vacancy.nejobs_duplicate_status = "UNIQUE"
        vacancy.nejobs_duplicate_reason = (
            "best approved NEJobs candidate below threshold "
            f"({score:.2f})"
        )


def classify(
    vacancy: VonneVacancy,
    salary_review_threshold: float,
) -> None:
    title = normalise(vacancy.title)
    role_type = normalise(vacancy.role_type)
    contract_type = normalise(vacancy.contract_type)

    if vacancy.duplicate_status == "DUPLICATE":
        vacancy.classification = "HARD_PASS"
        vacancy.classification_reason = (
            "confirmed JobG8 duplicate"
        )
        return
    if vacancy.nejobs_duplicate_status == "DUPLICATE":
        vacancy.classification = "HARD_PASS"
        vacancy.classification_reason = (
            "confirmed approved NEJobs duplicate"
        )
        return
    if (
        vacancy.duplicate_status == "POSSIBLE_DUPLICATE"
        or vacancy.nejobs_duplicate_status
        == "POSSIBLE_DUPLICATE"
    ):
        vacancy.classification = "POSS"
        vacancy.classification_reason = (
            "possible cross-source duplicate requires review"
        )
        return
    if (
        vacancy.source_duplicate_status
        == "POSSIBLE_SOURCE_DUPLICATE"
    ):
        vacancy.classification = "POSS"
        vacancy.classification_reason = (
            "possible duplicate within VONNE"
        )
        return
    hard_title_hits = [
        pattern
        for pattern in VONNE_HARD_PASS_TITLE_PATTERNS
        if pattern in title
    ]
    clear_title_hits = [
        pattern
        for pattern in CLEAR_TITLE_PATTERNS
        if pattern in title
    ]
    if hard_title_hits and not clear_title_hits:
        vacancy.classification = "HARD_PASS"
        vacancy.classification_reason = (
            "out-of-scope VONNE occupation"
        )
        return
    if vacancy.geography_status in {
        "GENERIC_REVIEW",
        "DERIVED_REVIEW",
    }:
        vacancy.classification = "POSS"
        vacancy.classification_reason = (
            "North East geography is generic or derived "
            "and requires review"
        )
        return
    if vacancy.detail_status in {
        "failed_listing_fallback",
        "missing_listing_fallback",
    }:
        vacancy.classification = "POSS"
        vacancy.classification_reason = (
            "detail page unavailable; listing facts require review"
        )
        return
    if role_type and role_type != "employment":
        vacancy.classification = "HARD_PASS"
        vacancy.classification_reason = (
            "VONNE role type is not employment: "
            f"{vacancy.role_type}"
        )
        return
    if any(
        pattern in title
        for pattern in INTERNAL_ONLY_PATTERNS
    ):
        vacancy.classification = "HARD_PASS"
        vacancy.classification_reason = (
            "not open to external applicants"
        )
        return
    if any(
        pattern in title
        for pattern in VONNE_HARD_PASS_TITLE_PATTERNS
    ):
        clear_hits = [
            pattern
            for pattern in CLEAR_TITLE_PATTERNS
            if pattern in title
        ]
        if not clear_hits:
            vacancy.classification = "HARD_PASS"
            vacancy.classification_reason = (
                "out-of-scope VONNE occupation"
            )
            return
    if any(
        marker in contract_type
        for marker in (
            "consultancy",
            "freelance",
            "voluntary",
            "unpaid",
        )
    ):
        vacancy.classification = "HARD_PASS"
        vacancy.classification_reason = (
            "not a standard employed vacancy"
        )
        return

    specialist_hits = [
        pattern.strip()
        for pattern in SPECIALIST_REVIEW_PATTERNS
        if pattern in f" {title} "
    ]
    clear_hits = [
        pattern
        for pattern in CLEAR_TITLE_PATTERNS
        if pattern in title
    ]
    primary_hits = [
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

    if specialist_hits and (
        not primary_hits
        or strong_specialist_hits
    ):
        vacancy.classification = "POSS"
        vacancy.classification_reason = (
            "transferable title with specialist or borderline wording: "
            + ", ".join(specialist_hits)
        )
    elif (
        salary_upper is not None
        and salary_upper > salary_review_threshold
    ):
        vacancy.classification = "POSS"
        vacancy.classification_reason = (
            f"annualised upper salary £{salary_upper:,.0f} exceeds "
            "North East review point "
            f"£{salary_review_threshold:,.0f}"
        )
    elif clear_hits:
        vacancy.classification = "HC"
        vacancy.classification_reason = (
            "clear transferable title: "
            + ", ".join(clear_hits)
        )
    elif any(
        pattern in title
        for pattern in VONNE_REVIEW_TITLE_PATTERNS
    ):
        vacancy.classification = "POSS"
        vacancy.classification_reason = (
            "provisional transferable-office review"
        )
    else:
        vacancy.classification = "HARD_PASS"
        vacancy.classification_reason = (
            "insufficient service-admin evidence"
        )


def load_manual_decisions_from_markdown(
    path: Path,
    current_review_date: str,
) -> ManualDecisionState:
    if not path.exists():
        return empty_manual_decisions()
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return empty_manual_decisions(
            f"manual review could not be read: {exc}"
        )
    date_match = re.search(
        r"(?mi)^review_date:\s*(\d{4}-\d{2}-\d{2})\s*$",
        text,
    )
    review_date = date_match.group(1) if date_match else ""
    if review_date != current_review_date:
        return empty_manual_decisions(
            "old or missing review_date; actions ignored"
        )
    selections: set[str] = set()
    exclusions: set[str] = set()
    reviewed_ids: set[str] = set()
    fingerprint_match = re.search(
        r"(?mi)^review_fingerprint:\s*([a-f0-9]{64})\s*$",
        text,
    )
    for block in re.findall(
        r"(?ms)^---\s*$\n(.*?)^---\s*$",
        text,
    ):
        action_match = re.search(
            r"(?mi)^action:\s*(select|exclude)?\s*$",
            block,
        )
        id_match = re.search(
            r"(?mi)^source_job_id:\s*([^\s]+)\s*$",
            block,
        )
        if not action_match or not id_match:
            continue
        source_job_id = clean_text(id_match.group(1))
        reviewed_ids.add(source_job_id)
        action = clean_text(action_match.group(1)).casefold()
        if action == "select":
            selections.add(source_job_id)
        elif action == "exclude":
            exclusions.add(source_job_id)
    selections.difference_update(exclusions)
    return ManualDecisionState(
        selections=selections,
        exclusions=exclusions,
        reviewed_ids=reviewed_ids,
        review_date=review_date,
        review_fingerprint=(
            fingerprint_match.group(1)
            if fingerprint_match
            else ""
        ),
        rerun_mode=bool(selections or exclusions),
    )


def manual_action_for(
    vacancy: VonneVacancy,
    decisions: ManualDecisionState,
) -> str:
    if vacancy.source_job_id in decisions.exclusions:
        return "exclude"
    if vacancy.source_job_id in decisions.selections:
        return "select"
    return ""


def final_decision_for(
    vacancy: VonneVacancy,
    decisions: ManualDecisionState,
) -> str:
    if vacancy.classification == "HARD_PASS":
        return "HARD_PASS"
    if vacancy.source_job_id in decisions.exclusions:
        return "EXCLUDED"
    if vacancy.source_job_id in decisions.selections:
        return "SELECTED"
    if vacancy.classification == "HC":
        return "SELECTED"
    return "POSS"


def vacancy_review_facts(vacancy: VonneVacancy) -> dict[str, str]:
    """Return the exact factual/classification evidence reviewed for one job."""
    return {
        "source_job_id": vacancy.source_job_id,
        "title": vacancy.title,
        "employer": vacancy.employer,
        "location": vacancy.location,
        "salary_text": vacancy.salary_text,
        "closing_date": vacancy.closing_date,
        "classification": vacancy.classification,
        "geography_status": vacancy.geography_status,
        "jobg8": vacancy.duplicate_status,
        "nejobs": vacancy.nejobs_duplicate_status,
    }


def vacancy_review_fingerprint(vacancy: VonneVacancy) -> str:
    payload = json.dumps(
        vacancy_review_facts(vacancy),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def review_fingerprint(
    vacancies: Iterable[VonneVacancy],
) -> str:
    rows = [vacancy_review_facts(vacancy) for vacancy in vacancies]
    rows.sort(key=lambda row: row["source_job_id"])
    payload = json.dumps(
        rows,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def compact(value: str, limit: int) -> str:
    text = clean_text(value)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def review_row(
    vacancy: VonneVacancy,
    decisions: ManualDecisionState | None = None,
) -> dict[str, str]:
    decisions = decisions or empty_manual_decisions()
    plausible_jobg8 = vacancy.duplicate_status in {
        "DUPLICATE",
        "POSSIBLE_DUPLICATE",
    }
    plausible_nejobs = vacancy.nejobs_duplicate_status in {
        "DUPLICATE",
        "POSSIBLE_DUPLICATE",
    }
    return {
        "source": SOURCE_CODE,
        "tracking_key": f"vonne-{vacancy.source_job_id}",
        "title": compact(vacancy.title, 42),
        "salary_text": compact(vacancy.salary_text, 32),
        "employer": compact(vacancy.employer, 30),
        "location": compact(vacancy.location, 32),
        "based": compact(vacancy.based, 28),
        "closing_date": vacancy.closing_date,
        "contract_type": vacancy.contract_type,
        "role_type": vacancy.role_type,
        "hours": vacancy.hours,
        "role_description": vacancy.role_description,
        "classification": vacancy.classification,
        "classification_reason": vacancy.classification_reason,
        "geography_status": vacancy.geography_status,
        "geography_reason": vacancy.geography_reason,
        "ontap_geography": vacancy.ontap_geography,
        "jobg8_check": (
            vacancy.duplicate_status
            if plausible_jobg8
            else "No plausible JobG8 match"
        ),
        "jobg8_candidate_title": (
            vacancy.jobg8_candidate_title
            if plausible_jobg8
            else ""
        ),
        "jobg8_candidate_employer": (
            vacancy.jobg8_candidate_advertiser
            if plausible_jobg8
            else ""
        ),
        "jobg8_match_score": (
            vacancy.jobg8_match_score
            if plausible_jobg8
            else ""
        ),
        "nejobs_check": (
            vacancy.nejobs_duplicate_status
            if plausible_nejobs
            else "No plausible approved NEJobs match"
        ),
        "nejobs_candidate_title": (
            vacancy.nejobs_candidate_title
            if plausible_nejobs
            else ""
        ),
        "nejobs_candidate_employer": (
            vacancy.nejobs_candidate_employer
            if plausible_nejobs
            else ""
        ),
        "nejobs_match_score": (
            vacancy.nejobs_match_score
            if plausible_nejobs
            else ""
        ),
        "vonne_duplicate_check": (
            vacancy.source_duplicate_reason
            if vacancy.source_duplicate_status
            else "No"
        ),
        "vacancy_fingerprint": vacancy_review_fingerprint(vacancy),
        "source_job_id": vacancy.source_job_id,
        "source_url": vacancy.source_url,
        "detail_status": vacancy.detail_status,
        "manual_action": manual_action_for(
            vacancy,
            decisions,
        ),
        "final_decision": final_decision_for(
            vacancy,
            decisions,
        ),
    }


def write_csv(
    path: Path,
    vacancies: list[VonneVacancy],
    decisions: ManualDecisionState,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=REPORT_FIELDS,
            lineterminator="\n",
        )
        writer.writeheader()
        for vacancy in sorted(
            vacancies,
            key=lambda item: (
                {
                    "SELECTED": 0,
                    "POSS": 1,
                    "EXCLUDED": 2,
                    "HARD_PASS": 3,
                }.get(
                    final_decision_for(item, decisions),
                    9,
                ),
                item.ontap_geography,
                item.title.casefold(),
            ),
        ):
            writer.writerow(review_row(vacancy, decisions))


def write_summary(
    path: Path,
    *,
    counts: dict[str, int],
    vacancies: list[VonneVacancy],
    decisions: ManualDecisionState,
    review_date: str,
    jobg8_count: int,
    nejobs_count: int,
    listing_source: str,
    failures: list[str],
) -> None:
    outcomes = {
        label: sum(
            vacancy.classification == label
            for vacancy in vacancies
        )
        for label in ("HC", "POSS", "HARD_PASS")
    }
    final = {
        label: sum(
            final_decision_for(vacancy, decisions) == label
            for vacancy in vacancies
        )
        for label in (
            "SELECTED",
            "POSS",
            "EXCLUDED",
            "HARD_PASS",
        )
    }
    lines = [
        "# VONNE ETL proof-of-concept review",
        "",
        f"review_date: {review_date}",
        f"review_fingerprint: {review_fingerprint(vacancies)}",
        "",
        (
            "This implementation is review-only. It has no "
            "approved-JSON or publishing mode."
        ),
        "",
        "Edit only the `action:` line in editable blocks:",
        (
            "- `action: select` promotes a POSS vacancy "
            "for discussion."
        ),
        (
            "- `action: exclude` rejects a POSS vacancy "
            "or removes an HC vacancy."
        ),
        "- Actions are same-day only and do not publish anything.",
        "",
        (
            "Run generated: "
            + datetime.now(ZoneInfo("Europe/London")).isoformat(
                timespec="seconds"
            )
        ),
        f"Listing input: {listing_source}",
        f"JobG8 comparison rows: {jobg8_count}",
        f"Approved NEJobs comparison rows: {nejobs_count}",
        "",
        "## Funnel",
        f"- VONNE listings read: {counts['listing_total']}",
        (
            "- Detail-page candidates: "
            f"{counts['detail_candidates']}"
        ),
        (
            "- Detail pages fetched successfully: "
            f"{counts['detail_fetched']}"
        ),
        (
            "- Detail failures/listing fallbacks: "
            f"{counts['detail_failures']}"
        ),
        (
            "- Obvious hard passes not detail-fetched: "
            f"{counts['hard_pass_without_detail']}"
        ),
        (
            "- Tees Valley explicitly excluded: "
            f"{counts['tees_valley_excluded']}"
        ),
        (
            "- Outside or unmapped geography excluded: "
            f"{counts['outside_or_unmapped']}"
        ),
        (
            "- Generic/derived geography rows requiring review: "
            f"{counts['generic_geography_review']}"
        ),
        (
            "- Retained target candidates: "
            f"{counts['target_candidates']}"
        ),
        "",
        "## Outcomes",
        f"- HC: {outcomes['HC']}",
        f"- POSS: {outcomes['POSS']}",
        f"- HARD_PASS: {outcomes['HARD_PASS']}",
        (
            "- Final selected after same-day actions: "
            f"{final['SELECTED']}"
        ),
        (
            "- Final POSS awaiting decision: "
            f"{final['POSS']}"
        ),
        f"- Manually excluded: {final['EXCLUDED']}",
        "",
        "## Detail diagnostics",
    ]
    if failures:
        lines.extend(f"- {failure}" for failure in failures)
    else:
        lines.append("- No unresolved detail-page failures.")

    def safe(value: str) -> str:
        return clean_text(value).replace("|", "/")

    def append_block(vacancy: VonneVacancy) -> None:
        action = manual_action_for(vacancy, decisions)
        lines.extend(
            [
                "---",
                f"action: {action}" if action else "action:",
                " | ".join(
                    [
                        final_decision_for(
                            vacancy,
                            decisions,
                        ),
                        safe(vacancy.ontap_geography),
                        safe(vacancy.location),
                        safe(vacancy.salary_text),
                        safe(vacancy.title),
                    ]
                ),
                (
                    "employer: "
                    + safe(vacancy.employer or "Not parsed")
                ),
                f"closing_date: {safe(vacancy.closing_date)}",
                (
                    "geography: "
                    f"{safe(vacancy.geography_status)} — "
                    f"{safe(vacancy.geography_reason)}"
                ),
                f"reason: {safe(vacancy.classification_reason)}",
                f"source: {SOURCE_CODE}",
                f"tracking_key: vonne-{vacancy.source_job_id}",
                (
                    "vacancy_fingerprint: "
                    f"{vacancy_review_fingerprint(vacancy)}"
                ),
                f"source_job_id: {vacancy.source_job_id}",
                f"source_url: {vacancy.source_url}",
                "---",
                "",
            ]
        )

    for heading, status in (
        ("SELECTED", "SELECTED"),
        ("POSS — choose SELECT or EXCLUDE", "POSS"),
        ("EXCLUDED BY REVIEW", "EXCLUDED"),
    ):
        lines.extend(["", f"## {heading}", ""])
        matching = [
            vacancy
            for vacancy in vacancies
            if final_decision_for(vacancy, decisions) == status
        ]
        if matching:
            for vacancy in sorted(
                matching,
                key=lambda row: (
                    row.ontap_geography,
                    row.title.casefold(),
                ),
            ):
                append_block(vacancy)
        else:
            lines.append("- None.")

    lines.extend(["", "## HARD_PASS", ""])
    hard_passes = [
        vacancy
        for vacancy in vacancies
        if vacancy.classification == "HARD_PASS"
    ]
    if hard_passes:
        for vacancy in sorted(
            hard_passes,
            key=lambda row: row.title.casefold(),
        ):
            lines.append(
                f"- [{vacancy.title}]({vacancy.source_url}) — "
                f"{vacancy.classification_reason}."
            )
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "## Safety boundary",
            (
                "- The script writes CSV and Markdown review "
                "outputs only."
            ),
            (
                "- There is no command-line option or function "
                "that writes approved or live JSON."
            ),
            (
                "- It does not change `pipeline/output-external`, "
                "`pipeline/output-admin-service`, `app`, or "
                "existing workflows."
            ),
            (
                "- Only factual fields are retained; full VONNE "
                "role descriptions are not stored."
            ),
            (
                "- Source attribution remains `VONNE`, with stable "
                "`vonne-<cid>` tracking keys and original source URLs."
            ),
            (
                "- VONNE's website terms prohibit unauthorised "
                "reproduction; this POC is intentionally bounded "
                "and review-only."
            ),
            (
                "- Generic `Hybrid`, `Home-based` and `Regionwide` "
                "locations are forced to POSS unless a target "
                "geography is confirmed."
            ),
            (
                "- Tees Valley wording is explicitly excluded using "
                "Ontap's existing North East rules."
            ),
            (
                "- Monday/Thursday operation is not scheduled in this "
                "POC; it can be aligned later if the review proves "
                "reliable."
            ),
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args(
    argv: list[str] | None = None,
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--jobg8",
        type=Path,
        default=Path("input/jobg8.xlsx"),
    )
    parser.add_argument(
        "--geo-lookup",
        type=Path,
        default=Path("geo/geo_lookup.xlsx"),
    )
    parser.add_argument(
        "--nejobs-json",
        type=Path,
        default=Path(
            "output-external/northeast-jobs-admin-service.json"
        ),
    )
    parser.add_argument("--listing-file", type=Path)
    parser.add_argument("--details-dir", type=Path)
    parser.add_argument("--fetch-live", action="store_true")
    parser.add_argument(
        "--acknowledge-source-terms",
        action="store_true",
    )
    parser.add_argument(
        "--request-interval",
        type=float,
        default=0.5,
    )
    parser.add_argument(
        "--max-detail-requests",
        type=int,
        default=60,
    )
    parser.add_argument(
        "--salary-review-threshold",
        type=float,
        default=30_000,
    )
    parser.add_argument(
        "--report-csv",
        type=Path,
        default=Path("reviews/external/vonne-review.csv"),
    )
    parser.add_argument(
        "--summary-md",
        type=Path,
        default=Path("reviews/external/vonne-summary.md"),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.fetch_live and not args.acknowledge_source_terms:
        raise SystemExit(
            "STOP: live fetching requires explicit acknowledgement "
            "that VONNE's source terms have been reviewed."
        )
    if not args.fetch_live and args.listing_file is None:
        raise SystemExit(
            "STOP: provide --listing-file or explicitly opt into "
            "--fetch-live."
        )

    if args.listing_file:
        listing_text = args.listing_file.read_text(
            encoding="utf-8"
        )
        listing_source = str(args.listing_file)
    else:
        listing_text = fetch_text(LIST_URL)
        listing_source = LIST_URL
    items = parse_listing(listing_text)
    if not items:
        raise SystemExit(
            "STOP: no VONNE listings parsed; source structure "
            "may have changed."
        )

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
    jobg8_jobs = load_jobg8_candidates(
        args.jobg8,
        area_map,
        fallback_map,
    )
    nejobs_jobs = load_nejobs_candidates(args.nejobs_json)
    for vacancy in vacancies:
        deduplicate_jobg8(vacancy, jobg8_jobs)
        deduplicate_nejobs(vacancy, nejobs_jobs)
    deduplicate_within_source(vacancies)
    for vacancy in vacancies:
        classify(vacancy, args.salary_review_threshold)

    review_date = datetime.now(
        ZoneInfo("Europe/London")
    ).date().isoformat()
    decisions = load_manual_decisions_from_markdown(
        args.summary_md,
        review_date,
    )
    write_csv(args.report_csv, vacancies, decisions)
    write_summary(
        args.summary_md,
        counts=counts,
        vacancies=vacancies,
        decisions=decisions,
        review_date=review_date,
        jobg8_count=len(jobg8_jobs),
        nejobs_count=len(nejobs_jobs),
        listing_source=listing_source,
        failures=failures,
    )
    selected_count = sum(
        final_decision_for(vacancy, decisions) == "SELECTED"
        for vacancy in vacancies
    )
    print(
        f"VONNE review-only POC: {counts['listing_total']} "
        f"listings -> {len(vacancies)} retained candidates -> "
        f"{selected_count} selected for review. Reports: "
        f"{args.report_csv}, {args.summary_md}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
