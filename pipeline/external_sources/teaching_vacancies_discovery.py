"""Source-wide Teaching Vacancies discovery and factual manifest generation.

Discovery is national. It does not search by Ontap region and it performs no
geographic or occupational classification. The primary route is Teaching
Vacancies' national Administration, HR, data and finance listing. Supplemental
UK-wide keyword routes provide coverage evidence for adverts that may have been
categorised differently by the source.

A live run is accepted only when:
* every advertised page for every route is fetched;
* page ranges and totals reconcile;
* two complete sweeps return the same URL/provenance set;
* every discovered detail page parses successfully.

The output contains factual vacancy fields and discovery provenance only. It
does not publish jobs or alter approved snapshots.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import tempfile
import time
import urllib.parse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterable
from zoneinfo import ZoneInfo

from external_sources import teaching_vacancies_etl as etl
from external_sources import teaching_vacancies_poc as poc
from external_sources.regional_contracts import (
    DiscoveryRecord,
    canonical_url,
    clean,
    merge_discovery_records,
)

BASE_URL = "https://teaching-vacancies.service.gov.uk"
SOURCE = "Teaching Vacancies GOV.UK"
SOURCE_CODE = "Teaching Vacancies"
LONDON = ZoneInfo("Europe/London")
DISCOVERY_CONTRACT_VERSION = "teaching-vacancies-national-v1"
RESULTS_PER_PAGE = 10
LIVE_REQUEST_DELAY_SECONDS = 0.4
LIVE_REQUEST_RETRY_DELAYS_SECONDS = (2.0, 5.0, 10.0)
LISTING_AUDIT_RETRY_DELAYS_SECONDS = (2.0, 5.0, 10.0)

PRIMARY_ROUTE = (
    "administration-category",
    "Administration, HR, data and finance",
    f"{BASE_URL}/administration-hr-data-finance-jobs",
)
SUPPLEMENTAL_KEYWORDS = (
    "administrator",
    "administrative",
    "receptionist",
    "office",
    "business support",
    "exams officer",
    "personal assistant",
)

MANIFEST_FIELDS = (
    "run_date",
    "source",
    "source_job_id",
    "canonical_url",
    "title",
    "employer",
    "location",
    "postcode",
    "salary_text",
    "posted_date",
    "closing_date",
    "employment_type",
    "description_excerpt",
    "first_discovery_route",
    "first_discovery_query",
    "first_discovery_page",
    "discovery_routes",
    "discovery_occurrences",
    "detail_fetch_status",
    "factual_fingerprint",
)


@dataclass(frozen=True)
class SearchRoute:
    name: str
    query: str
    url: str


@dataclass(frozen=True)
class ListingPage:
    page: int
    start: int
    end: int
    total: int
    urls: tuple[str, ...]


@dataclass(frozen=True)
class RouteSweep:
    route: SearchRoute
    total: int
    pages: int
    occurrences: int
    unique_urls: int
    records: tuple[DiscoveryRecord, ...]


RequestText = Callable[[str], str]
DetailParser = Callable[[str, str], poc.Vacancy]


def default_routes() -> tuple[SearchRoute, ...]:
    routes = [SearchRoute(*PRIMARY_ROUTE)]
    for keyword in SUPPLEMENTAL_KEYWORDS:
        routes.append(
            SearchRoute(
                name=f"keyword:{keyword}",
                query=keyword,
                url=BASE_URL
                + "/jobs?"
                + urllib.parse.urlencode({"keyword": keyword}),
            )
        )
    return tuple(routes)


def page_url(route_url: str, page: int) -> str:
    if page < 1:
        raise ValueError("page must be at least 1")
    parsed = urllib.parse.urlsplit(route_url)
    query = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))
    if page > 1:
        query["page"] = str(page)
    else:
        query.pop("page", None)
    return urllib.parse.urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urllib.parse.urlencode(query),
            "",
        )
    )


def listing_job_urls(document: str) -> tuple[str, ...]:
    links = re.findall(r'href=["\']([^"\']*)["\']', document, flags=re.I)
    urls: list[str] = []
    for link in links:
        absolute = urllib.parse.urljoin(BASE_URL, link)
        parsed = urllib.parse.urlsplit(absolute)
        path = parsed.path.rstrip("/")
        if not path.startswith("/jobs/"):
            continue
        value = canonical_url(
            urllib.parse.urlunsplit(
                (parsed.scheme, parsed.netloc, path, "", "")
            )
        )
        if value and value not in urls:
            urls.append(value)
    return tuple(urls)


def parse_listing_page(document: str, *, page: int) -> ListingPage:
    visible_text = poc.clean(document)
    match = re.search(
        r"Showing\s+([\d,]+)\s+to\s+([\d,]+)\s+of\s+([\d,]+)\s+results",
        visible_text,
        flags=re.I,
    )
    if not match:
        raise ValueError(f"listing page {page} has no result-range audit")
    start, end, total = (
        int(value.replace(",", "")) for value in match.groups()
    )
    if total < 0 or start < 0 or end < 0:
        raise ValueError(f"listing page {page} has invalid result counts")
    if total == 0:
        if start or end:
            raise ValueError(f"listing page {page} has inconsistent zero results")
    elif not (1 <= start <= end <= total):
        raise ValueError(f"listing page {page} has invalid result range")
    urls = listing_job_urls(document)
    if total and not urls:
        raise ValueError(f"listing page {page} exposes no vacancy URLs")
    return ListingPage(page=page, start=start, end=end, total=total, urls=urls)


def request_listing_page(
    route: SearchRoute,
    *,
    page: int,
    request_text: RequestText,
    retry_delays: tuple[float, ...] = LISTING_AUDIT_RETRY_DELAYS_SECONDS,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> tuple[str, ListingPage]:
    url = page_url(route.url, page)
    last_error: Exception | None = None
    attempts = len(retry_delays) + 1
    for attempt in range(attempts):
        if attempt:
            sleep_fn(retry_delays[attempt - 1])
        try:
            document = request_text(url)
            return document, parse_listing_page(document, page=page)
        except (OSError, ValueError) as exc:
            last_error = exc
    raise ValueError(
        f"{route.name} page {page} failed its result-range audit after "
        f"{attempts} attempts at {url}: {clean(last_error)}"
    )


def expected_page_range(*, page: int, total: int) -> tuple[int, int]:
    if total == 0:
        return 0, 0
    start = (page - 1) * RESULTS_PER_PAGE + 1
    end = min(page * RESULTS_PER_PAGE, total)
    return start, end


def discover_route(
    route: SearchRoute,
    *,
    request_text: RequestText,
) -> RouteSweep:
    first_document, first = request_listing_page(
        route,
        page=1,
        request_text=request_text,
    )
    pages = max(1, math.ceil(first.total / RESULTS_PER_PAGE))
    records: list[DiscoveryRecord] = []
    occurrences = 0

    for page in range(1, pages + 1):
        if page == 1:
            document, listing = first_document, first
        else:
            document, listing = request_listing_page(
                route,
                page=page,
                request_text=request_text,
            )
        if listing.total != first.total:
            raise ValueError(
                f"{route.name} total changed during sweep: "
                f"{first.total} to {listing.total}"
            )
        expected_start, expected_end = expected_page_range(
            page=page,
            total=first.total,
        )
        if (listing.start, listing.end) != (expected_start, expected_end):
            raise ValueError(
                f"{route.name} page {page} range "
                f"{listing.start}-{listing.end} does not match "
                f"{expected_start}-{expected_end}"
            )
        occurrences += len(listing.urls)
        for url in listing.urls:
            record = DiscoveryRecord(
                source=SOURCE,
                source_job_id="",
                canonical_url=url,
            )
            record.add_provenance(
                route=route.name,
                query=route.query,
                page=page,
            )
            records.append(record)

    merged = merge_discovery_records(records)
    return RouteSweep(
        route=route,
        total=first.total,
        pages=pages,
        occurrences=occurrences,
        unique_urls=len(merged),
        records=tuple(merged),
    )


def run_sweep(
    routes: Iterable[SearchRoute],
    *,
    request_text: RequestText,
) -> tuple[tuple[DiscoveryRecord, ...], tuple[RouteSweep, ...]]:
    route_sweeps = tuple(
        discover_route(route, request_text=request_text) for route in routes
    )
    records: list[DiscoveryRecord] = []
    for sweep in route_sweeps:
        records.extend(sweep.records)
    return tuple(merge_discovery_records(records)), route_sweeps


def discovery_signature(records: Iterable[DiscoveryRecord]) -> str:
    payload: list[dict[str, object]] = []
    for record in sorted(records, key=lambda item: item.stable_key()):
        routes = sorted(
            (
                clean(item.get("route")),
                clean(item.get("query")),
                int(item.get("page") or 1),
            )
            for item in record.discovery_routes
        )
        payload.append(
            {
                "url": canonical_url(record.canonical_url),
                "routes": routes,
            }
        )
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def stable_discovery(
    routes: Iterable[SearchRoute],
    *,
    request_text: RequestText,
) -> tuple[tuple[DiscoveryRecord, ...], tuple[RouteSweep, ...]]:
    route_tuple = tuple(routes)
    first_records, first_sweeps = run_sweep(
        route_tuple,
        request_text=request_text,
    )
    second_records, second_sweeps = run_sweep(
        route_tuple,
        request_text=request_text,
    )
    first_signature = discovery_signature(first_records)
    second_signature = discovery_signature(second_records)
    if first_signature != second_signature:
        first_urls = {canonical_url(row.canonical_url) for row in first_records}
        second_urls = {canonical_url(row.canonical_url) for row in second_records}
        additions = sorted(second_urls - first_urls)
        omissions = sorted(first_urls - second_urls)
        detail: list[str] = []
        if additions:
            detail.append("second-sweep additions: " + ", ".join(additions[:20]))
        if omissions:
            detail.append("second-sweep omissions: " + ", ".join(omissions[:20]))
        raise ValueError(
            "Teaching Vacancies source-wide discovery was not stable"
            + (f" ({'; '.join(detail)})" if detail else "")
        )
    first_stats = [
        (item.route.name, item.total, item.pages, item.unique_urls)
        for item in first_sweeps
    ]
    second_stats = [
        (item.route.name, item.total, item.pages, item.unique_urls)
        for item in second_sweeps
    ]
    if first_stats != second_stats:
        raise ValueError(
            "Teaching Vacancies source-wide route totals changed between sweeps"
        )
    return first_records, first_sweeps


def extract_postcode(location: str) -> str:
    match = re.search(
        r"\b([A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})\b",
        clean(location).upper(),
    )
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else ""


def detail_records(
    discovered: Iterable[DiscoveryRecord],
    *,
    request_text: RequestText,
    parse_detail: DetailParser,
) -> tuple[DiscoveryRecord, ...]:
    output: list[DiscoveryRecord] = []
    failures: list[str] = []
    for listing_record in discovered:
        url = canonical_url(listing_record.canonical_url)
        try:
            vacancy = parse_detail(request_text(url), url)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"{url} — {type(exc).__name__}: {clean(exc)}")
            continue
        record = DiscoveryRecord(
            source=SOURCE,
            source_job_id=clean(vacancy.source_job_id),
            canonical_url=url,
            title=clean(vacancy.title),
            employer=clean(vacancy.employer),
            location=clean(vacancy.location),
            postcode=extract_postcode(vacancy.location),
            salary_text=clean(vacancy.salary_text),
            posted_date=clean(vacancy.posted_date),
            closing_date=clean(vacancy.closing_date),
            employment_type=clean(vacancy.employment_type),
            description_excerpt=clean(vacancy.description_excerpt)[:1200],
        )
        for item in listing_record.discovery_routes:
            record.add_provenance(
                route=clean(item.get("route")),
                query=clean(item.get("query")),
                page=int(item.get("page") or 1),
            )
        output.append(record)
    if failures:
        raise ValueError(
            "Teaching Vacancies source-wide detail fetch was incomplete:\n- "
            + "\n- ".join(failures)
        )
    return tuple(merge_discovery_records(output))


def factual_fingerprint(record: DiscoveryRecord) -> str:
    payload = {
        field: clean(getattr(record, field))
        for field in (
            "source_job_id",
            "canonical_url",
            "title",
            "employer",
            "location",
            "postcode",
            "salary_text",
            "posted_date",
            "closing_date",
            "employment_type",
            "description_excerpt",
        )
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def manifest_rows(
    records: Iterable[DiscoveryRecord],
    *,
    run_date: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for record in sorted(records, key=lambda item: item.stable_key()):
        routes = sorted(
            record.discovery_routes,
            key=lambda item: (
                clean(item.get("route")),
                clean(item.get("query")),
                int(item.get("page") or 1),
            ),
        )
        first = routes[0] if routes else {}
        rows.append(
            {
                "run_date": run_date,
                "source": SOURCE_CODE,
                "source_job_id": clean(record.source_job_id),
                "canonical_url": canonical_url(record.canonical_url),
                "title": clean(record.title),
                "employer": clean(record.employer),
                "location": clean(record.location),
                "postcode": clean(record.postcode),
                "salary_text": clean(record.salary_text),
                "posted_date": clean(record.posted_date),
                "closing_date": clean(record.closing_date),
                "employment_type": clean(record.employment_type),
                "description_excerpt": clean(record.description_excerpt)[:1200],
                "first_discovery_route": clean(first.get("route")),
                "first_discovery_query": clean(first.get("query")),
                "first_discovery_page": int(first.get("page") or 1),
                "discovery_routes": json.dumps(
                    routes,
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                "discovery_occurrences": len(routes),
                "detail_fetch_status": "OK",
                "factual_fingerprint": factual_fingerprint(record),
            }
        )
    return rows


def csv_bytes(rows: list[dict[str, object]]) -> bytes:
    import io

    handle = io.StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue().encode("utf-8")


def write_bytes_atomic(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_handle, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    try:
        with os.fdopen(file_handle, "wb") as temp:
            temp.write(content)
            temp.flush()
            os.fsync(temp.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def default_output_paths(run_date: str) -> tuple[Path, Path]:
    root = Path("manifests/external/teaching-vacancies")
    stem = f"teaching-vacancies-discovery-{run_date}"
    return root / f"{stem}.csv", root / f"{stem}-summary.json"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch-live", action="store_true")
    parser.add_argument("--manifest-csv", type=Path)
    parser.add_argument("--summary-json", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.fetch_live:
        raise SystemExit(
            "STOP: source-wide Teaching Vacancies discovery requires --fetch-live."
        )

    now = datetime.now(LONDON)
    run_date = now.date().isoformat()
    manifest_path, summary_path = default_output_paths(run_date)
    if args.manifest_csv:
        manifest_path = args.manifest_csv
    if args.summary_json:
        summary_path = args.summary_json

    etl.install_patches()
    routes = default_routes()

    def live_request_text(url: str) -> str:
        last_error: OSError | None = None
        attempts = len(LIVE_REQUEST_RETRY_DELAYS_SECONDS) + 1
        for attempt in range(attempts):
            if attempt:
                time.sleep(LIVE_REQUEST_RETRY_DELAYS_SECONDS[attempt - 1])
            time.sleep(LIVE_REQUEST_DELAY_SECONDS)
            try:
                return poc.request_text(url)
            except OSError as exc:
                last_error = exc
        raise OSError(
            f"Teaching Vacancies request failed after {attempts} attempts: "
            f"{url} — {clean(last_error)}"
        )

    discovered, route_sweeps = stable_discovery(
        routes,
        request_text=live_request_text,
    )
    records = detail_records(
        discovered,
        request_text=live_request_text,
        parse_detail=poc.parse_jobposting,
    )
    rows = manifest_rows(records, run_date=run_date)
    manifest_content = csv_bytes(rows)
    manifest_sha256 = hashlib.sha256(manifest_content).hexdigest()

    summary = {
        "contract_version": DISCOVERY_CONTRACT_VERSION,
        "generated_at": now.isoformat(timespec="seconds"),
        "run_date": run_date,
        "source": SOURCE_CODE,
        "source_scope": "England-wide; no Ontap regional restriction",
        "stable_sweeps": 2,
        "records": len(rows),
        "manifest_sha256": manifest_sha256,
        "routes": [
            {
                "name": sweep.route.name,
                "query": sweep.route.query,
                "url": sweep.route.url,
                "reported_total": sweep.total,
                "pages_fetched_per_sweep": sweep.pages,
                "listing_occurrences_per_sweep": sweep.occurrences,
                "unique_urls_per_sweep": sweep.unique_urls,
            }
            for sweep in route_sweeps
        ],
    }

    write_bytes_atomic(manifest_path, manifest_content)
    write_bytes_atomic(
        summary_path,
        (json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode(
            "utf-8"
        ),
    )
    print(
        f"Teaching Vacancies source-wide discovery wrote {len(rows)} factual "
        f"records to {manifest_path}; evidence: {summary_path}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
