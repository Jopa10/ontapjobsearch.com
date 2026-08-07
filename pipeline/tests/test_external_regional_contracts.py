from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook

from external_sources.regional_contracts import (
    CATEGORY_ADMIN_SERVICE,
    DiscoveryRecord,
    load_geo_lookup,
    load_slice_authorities,
    merge_discovery_records,
    publishable_region,
    route_geography,
    slice_authority,
)


def test_source_wide_discovery_deduplicates_and_retains_provenance() -> None:
    first = DiscoveryRecord(
        source="Teaching Vacancies",
        source_job_id="123",
        canonical_url="https://example.test/jobs/123",
        title="Administrator",
        employer="Example School",
        location="Lancaster",
    )
    first.add_provenance(route="keyword", query="administrator", page=1)
    second = DiscoveryRecord(
        source="Teaching Vacancies",
        source_job_id="123",
        canonical_url="https://example.test/jobs/123/",
        title="Administrator",
        employer="Example School",
        location="Lancaster",
    )
    second.add_provenance(route="keyword", query="office", page=2)

    merged = merge_discovery_records([first, second])

    assert len(merged) == 1
    assert merged[0].location == "Lancaster"
    assert len(merged[0].discovery_routes) == 2


def test_conflicting_factual_values_block_manifest_merge() -> None:
    first = DiscoveryRecord(
        source="Teaching Vacancies",
        source_job_id="123",
        canonical_url="https://example.test/jobs/123",
        title="Administrator",
    )
    second = DiscoveryRecord(
        source="Teaching Vacancies",
        source_job_id="123",
        canonical_url="https://example.test/jobs/123",
        title="Teacher",
    )

    try:
        merge_discovery_records([first, second])
    except ValueError as exc:
        assert "conflicting factual discovery values" in str(exc)
    else:
        raise AssertionError("conflicting source facts must block the manifest")


def test_live_candidate_and_missing_slice_gating(tmp_path: Path) -> None:
    register = tmp_path / "register.csv"
    with register.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("region", "category", "status"))
        writer.writerow(("Yorkshire - West", "admin_service", "LIVE"))
        writer.writerow(("Yorkshire - East", "admin_service", "CANDIDATE"))

    authorities = load_slice_authorities(register)

    assert publishable_region(
        authorities,
        region="Yorkshire - West",
        category=CATEGORY_ADMIN_SERVICE,
    )
    assert not publishable_region(
        authorities,
        region="Yorkshire - East",
        category=CATEGORY_ADMIN_SERVICE,
    )
    assert not publishable_region(
        authorities,
        region="Lancashire - North",
        category=CATEGORY_ADMIN_SERVICE,
    )
    assert slice_authority(
        authorities,
        region="Yorkshire - East",
        category=CATEGORY_ADMIN_SERVICE,
    ).status == "CANDIDATE"


def _write_geo_lookup(path: Path) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(("location", "ontap_region"))
    sheet.append(("Lancaster", "Lancashire - North"))
    sheet.append(("LA1", "Lancashire - North"))
    sheet.append(("Hull", "Yorkshire - East"))
    workbook.save(path)


def test_geo_lookup_can_route_any_ontap_region(tmp_path: Path) -> None:
    path = tmp_path / "geo_lookup.xlsx"
    _write_geo_lookup(path)
    lookup = load_geo_lookup(path)

    result = route_geography(location="Lancaster", postcode="", lookup=lookup)

    assert result.status == "ROUTED"
    assert result.region == "Lancashire - North"
    assert result.lookup_key == "lancaster"


def test_uncertain_geography_is_retained_not_guessed(tmp_path: Path) -> None:
    path = tmp_path / "geo_lookup.xlsx"
    _write_geo_lookup(path)
    lookup = load_geo_lookup(path)

    result = route_geography(
        location="North West England",
        postcode="",
        lookup=lookup,
    )

    assert result.status == "UNRESOLVED"
    assert result.region == ""
    assert "No exact factual location match" in result.evidence

def test_shared_geo_fallback_csv_routes_missing_factual_locations(tmp_path: Path) -> None:
    path = tmp_path / "geo_lookup.xlsx"
    _write_geo_lookup(path)
    fallback = tmp_path / "location_fallbacks.csv"
    fallback.write_text(
        "lookup_value,region,status\n"
        "GU12 5PX,Surrey,AUTO\n"
        "Ash Vale,Surrey,AUTO\n"
        "LS21 2HX,Yorkshire - North,AUTO\n",
        encoding="utf-8",
    )

    lookup = load_geo_lookup(path)

    ash_vale = route_geography(
        location="Ash Vale, South East, GU12 5PX",
        postcode="GU12 5PX",
        lookup=lookup,
    )
    assert ash_vale.status == "ROUTED"
    assert ash_vale.region == "Surrey"
    assert ash_vale.lookup_key == "gu12 5px"

    askwith = route_geography(
        location="Otley, Yorkshire and the Humber, LS21 2HX",
        postcode="LS21 2HX",
        lookup=lookup,
    )
    assert askwith.status == "ROUTED"
    assert askwith.region == "Yorkshire - North"
    assert askwith.lookup_key == "ls21 2hx"

