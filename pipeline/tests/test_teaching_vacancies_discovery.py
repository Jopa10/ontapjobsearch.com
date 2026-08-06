from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from external_sources import teaching_vacancies_discovery as discovery
from external_sources import teaching_vacancies_poc as poc
from external_sources.regional_contracts import DiscoveryRecord


def listing_document(start: int, end: int, total: int, slugs: list[str]) -> str:
    links = "\n".join(f'<a href="/jobs/{slug}">{slug}</a>' for slug in slugs)
    return (
        "<html><body>"
        + links
        + f"<p>Showing <strong>{start}</strong> to <strong>{end}</strong> "
        + f"of <strong>{total}</strong> results</p></body></html>"
    )


def test_default_routes_are_national_and_include_primary_category() -> None:
    routes = discovery.default_routes()

    assert routes[0].url.endswith("/administration-hr-data-finance-jobs")
    assert routes[0].query == "Administration, HR, data and finance"
    assert any(route.query == "receptionist" for route in routes)
    assert all("location=" not in route.url for route in routes)
    assert all("radius=" not in route.url for route in routes)


def test_discover_route_exhausts_every_advertised_page() -> None:
    route = discovery.SearchRoute(
        name="administration-category",
        query="Administration, HR, data and finance",
        url="https://teaching-vacancies.service.gov.uk/administration-hr-data-finance-jobs",
    )
    documents = {
        route.url: listing_document(
            1,
            10,
            21,
            [f"vacancy-{number}" for number in range(1, 11)],
        ),
        route.url + "?page=2": listing_document(
            11,
            20,
            21,
            [f"vacancy-{number}" for number in range(11, 21)],
        ),
        route.url + "?page=3": listing_document(21, 21, 21, ["vacancy-21"]),
    }
    requested: list[str] = []

    def request_text(url: str) -> str:
        requested.append(url)
        return documents[url]

    sweep = discovery.discover_route(route, request_text=request_text)

    assert requested == list(documents)
    assert sweep.total == 21
    assert sweep.pages == 3
    assert sweep.unique_urls == 21
    vacancy_21 = next(
        row for row in sweep.records if row.canonical_url.endswith("/vacancy-21")
    )
    assert vacancy_21.discovery_routes == [
        {
            "route": "administration-category",
            "query": "Administration, HR, data and finance",
            "page": 3,
        }
    ]


def test_listing_audit_retries_a_transient_non_results_page() -> None:
    route = discovery.SearchRoute(
        "keyword:administrator",
        "administrator",
        "https://teaching-vacancies.service.gov.uk/jobs?keyword=administrator",
    )
    calls = 0
    sleeps: list[float] = []

    def request_text(_url: str) -> str:
        nonlocal calls
        calls += 1
        if calls == 1:
            return "<html><title>Temporary response</title><body>Try again</body></html>"
        return listing_document(1, 1, 1, ["administrator-role"])

    _document, listing = discovery.request_listing_page(
        route,
        page=1,
        request_text=request_text,
        retry_delays=(0.25,),
        sleep_fn=sleeps.append,
    )

    assert calls == 2
    assert sleeps == [0.25]
    assert listing.total == 1
    assert listing.urls[0].endswith("/administrator-role")


def test_explicit_zero_result_page_is_audited_without_range_text() -> None:
    route = discovery.SearchRoute(
        "keyword:business support",
        "business support",
        "https://teaching-vacancies.service.gov.uk/jobs?keyword=business+support",
    )
    document = (
        "<html><head><title>Jobs (0) sorted by newest - Teaching Vacancies</title></head>"
        "<body><h1>Jobs (0)</h1></body></html>"
    )

    listing = discovery.parse_listing_page(document, page=1)
    sweep = discovery.discover_route(route, request_text=lambda _url: document)

    assert listing == discovery.ListingPage(page=1, start=0, end=0, total=0, urls=())
    assert sweep.total == 0
    assert sweep.pages == 1
    assert sweep.records == ()


def test_zero_result_heading_cannot_hide_a_vacancy_link() -> None:
    document = (
        "<html><head><title>Jobs (0) - Teaching Vacancies</title></head>"
        "<body><h1>Jobs (0)</h1><a href='/jobs/unexpected'>Unexpected</a></body></html>"
    )

    with pytest.raises(ValueError, match="no result-range audit"):
        discovery.parse_listing_page(document, page=1)


def test_discover_route_blocks_changed_total() -> None:
    route = discovery.SearchRoute("route", "query", "https://example.test/jobs")
    documents = {
        route.url: listing_document(
            1,
            10,
            11,
            [f"vacancy-{number}" for number in range(1, 11)],
        ),
        route.url + "?page=2": listing_document(11, 11, 12, ["vacancy-11"]),
    }

    with pytest.raises(ValueError, match="total changed during sweep"):
        discovery.discover_route(
            route,
            request_text=lambda url: documents[url],
        )


def test_stable_discovery_blocks_changed_url_set() -> None:
    route = discovery.SearchRoute("route", "query", "https://example.test/jobs")
    calls = 0

    def request_text(_url: str) -> str:
        nonlocal calls
        calls += 1
        slug = "first" if calls == 1 else "second"
        return listing_document(1, 1, 1, [slug])

    with pytest.raises(ValueError, match="was not stable"):
        discovery.stable_discovery((route,), request_text=request_text)


def test_detail_records_merge_overlapping_route_provenance() -> None:
    url = "https://teaching-vacancies.service.gov.uk/jobs/admin-officer"
    first = DiscoveryRecord(
        source=discovery.SOURCE,
        source_job_id="",
        canonical_url=url,
    )
    first.add_provenance(
        route="administration-category",
        query="Administration, HR, data and finance",
        page=1,
    )
    second = DiscoveryRecord(
        source=discovery.SOURCE,
        source_job_id="",
        canonical_url=url,
    )
    second.add_provenance(
        route="keyword:administrator",
        query="administrator",
        page=2,
    )

    vacancy = poc.Vacancy(
        source_job_id="TV-123",
        title="Administration Officer",
        employer="Example School",
        location="Preston, Lancashire, PR1 2AB",
        salary_text="£25,000",
        posted_date="2026-08-01",
        closing_date="2026-08-30",
        employment_type="PART_TIME",
        description_excerpt="Provide administrative and reception support.",
        source_url=url,
    )

    records = discovery.detail_records(
        (first, second),
        request_text=lambda _url: "<html></html>",
        parse_detail=lambda _document, _url: vacancy,
    )

    assert len(records) == 1
    assert records[0].source_job_id == "TV-123"
    assert records[0].postcode == "PR1 2AB"
    assert len(records[0].discovery_routes) == 2


def test_manifest_is_factual_and_pre_geography(tmp_path: Path) -> None:
    record = DiscoveryRecord(
        source=discovery.SOURCE,
        source_job_id="TV-456",
        canonical_url="https://teaching-vacancies.service.gov.uk/jobs/receptionist",
        title="Receptionist",
        employer="Example Academy",
        location="Manchester, M1 1AA",
        postcode="M1 1AA",
        salary_text="£24,000",
        posted_date="2026-08-02",
        closing_date="2026-08-20",
        employment_type="FULL_TIME",
        description_excerpt="Front-desk and administrative duties.",
    )
    record.add_provenance(
        route="keyword:receptionist",
        query="receptionist",
        page=1,
    )

    rows = discovery.manifest_rows((record,), run_date="2026-08-06")
    content = discovery.csv_bytes(rows)
    path = tmp_path / "manifest.csv"
    path.write_bytes(content)

    with path.open(newline="", encoding="utf-8") as handle:
        parsed = list(csv.DictReader(handle))

    assert parsed[0]["source_job_id"] == "TV-456"
    assert parsed[0]["first_discovery_query"] == "receptionist"
    assert parsed[0]["detail_fetch_status"] == "OK"
    assert json.loads(parsed[0]["discovery_routes"]) == [
        {
            "page": 1,
            "query": "receptionist",
            "route": "keyword:receptionist",
        }
    ]
    assert "ontap_region" not in parsed[0]
    assert "classification" not in parsed[0]


def test_detail_failure_blocks_manifest_generation() -> None:
    record = DiscoveryRecord(
        source=discovery.SOURCE,
        source_job_id="",
        canonical_url="https://teaching-vacancies.service.gov.uk/jobs/broken",
    )
    record.add_provenance(route="route", query="query", page=1)

    with pytest.raises(ValueError, match="detail fetch was incomplete"):
        discovery.detail_records(
            (record,),
            request_text=lambda _url: (_ for _ in ()).throw(OSError("down")),
            parse_detail=lambda _document, _url: poc.Vacancy(),
        )
