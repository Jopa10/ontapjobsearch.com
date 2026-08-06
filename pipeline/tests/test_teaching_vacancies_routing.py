from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pytest

from external_sources import teaching_vacancies_discovery as discovery
from external_sources import teaching_vacancies_routing as routing
from external_sources.regional_contracts import (
    SliceAuthority,
    canonical_public_region,
    route_geography,
)


def factual_row(
    source_job_id: str,
    *,
    title: str,
    location: str,
    postcode: str = "",
) -> dict[str, object]:
    return {
        "run_date": "2026-08-06",
        "source": discovery.SOURCE_CODE,
        "source_job_id": source_job_id,
        "canonical_url": (
            "https://teaching-vacancies.service.gov.uk/jobs/" + source_job_id
        ),
        "title": title,
        "employer": "Example School",
        "location": location,
        "postcode": postcode,
        "salary_text": "£25,000",
        "posted_date": "2026-08-01",
        "closing_date": "2026-08-30",
        "employment_type": "FULL_TIME",
        "description_excerpt": "Provide administrative support.",
        "first_discovery_route": "administration-category",
        "first_discovery_query": "Administration, HR, data and finance",
        "first_discovery_page": 1,
        "discovery_routes": "[]",
        "discovery_occurrences": 1,
        "detail_fetch_status": "OK",
        "factual_fingerprint": "a" * 64,
    }


def write_manifest_pair(
    tmp_path: Path,
    rows: list[dict[str, object]],
) -> tuple[Path, Path]:
    manifest_path = tmp_path / "manifest.csv"
    manifest_bytes = discovery.csv_bytes(rows)
    manifest_path.write_bytes(manifest_bytes)
    summary_path = tmp_path / "summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "source": discovery.SOURCE_CODE,
                "run_date": "2026-08-06",
                "records": len(rows),
                "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            }
        ),
        encoding="utf-8",
    )
    return manifest_path, summary_path


def authorities() -> dict[tuple[str, str], SliceAuthority]:
    return {
        ("Yorkshire - West", "admin_service"): SliceAuthority(
            "Yorkshire - West", "admin_service", "LIVE"
        ),
        ("Yorkshire - East", "admin_service"): SliceAuthority(
            "Yorkshire - East", "admin_service", "CANDIDATE"
        ),
        ("North East", "admin_service"): SliceAuthority(
            "North East", "admin_service", "LIVE"
        ),
    }


def test_verified_manifest_blocks_tampering(tmp_path: Path) -> None:
    manifest, summary = write_manifest_pair(
        tmp_path,
        [
            factual_row(
                "tv-1",
                title="Administrator",
                location="Leeds, West Yorkshire",
            )
        ],
    )
    manifest.write_text(manifest.read_text(encoding="utf-8") + "tampered", encoding="utf-8")

    with pytest.raises(ValueError, match="SHA256"):
        routing.load_verified_manifest(manifest, summary)


def test_route_rows_apply_live_candidate_and_unregistered_gates() -> None:
    rows = [
        factual_row(
            "tv-west",
            title="Administrator",
            location="Leeds, West Yorkshire, LS1 1AA",
            postcode="LS1 1AA",
        ),
        factual_row(
            "tv-east",
            title="Receptionist",
            location="Hull, East Riding of Yorkshire, HU1 1AA",
            postcode="HU1 1AA",
        ),
        factual_row(
            "tv-lancashire",
            title="Business Support Officer",
            location="Preston, Lancashire, PR1 2AB",
            postcode="PR1 2AB",
        ),
    ]
    lookup = {
        "leeds": "Yorkshire - West",
        "hull": "Yorkshire - East",
        "preston": "Lancashire - Central",
    }

    routed = routing.route_manifest_rows(
        rows,
        geo_lookup=lookup,
        authorities=authorities(),
    )
    by_id = {row["source_job_id"]: row for row in routed}

    assert by_id["tv-west"]["ontap_region"] == "Yorkshire - West"
    assert by_id["tv-west"]["slice_status"] == "LIVE"
    assert by_id["tv-west"]["publish_eligible"] == "YES"
    assert by_id["tv-east"]["ontap_region"] == "Yorkshire - East"
    assert by_id["tv-east"]["slice_status"] == "CANDIDATE"
    assert by_id["tv-east"]["publish_eligible"] == "NO"
    assert by_id["tv-lancashire"]["ontap_region"] == "Lancashire - Central"
    assert by_id["tv-lancashire"]["slice_status"] == "UNREGISTERED"
    assert by_id["tv-lancashire"]["publish_eligible"] == "NO"


def test_unresolved_geography_remains_visible() -> None:
    rows = [
        factual_row(
            "tv-unknown",
            title="Administrator",
            location="Location to be confirmed",
        )
    ]

    routed = routing.route_manifest_rows(
        rows,
        geo_lookup={"leeds": "Yorkshire - West"},
        authorities=authorities(),
    )

    assert routed[0]["geography_status"] == "UNRESOLVED"
    assert routed[0]["slice_status"] == "UNREGISTERED"
    assert routed[0]["publish_eligible"] == "NO"
    assert "No exact factual location match" in routed[0]["geography_reason"]


def test_locality_wins_before_broader_county_component() -> None:
    result = route_geography(
        location="Preston, Lancashire, PR1 2AB",
        postcode="PR1 2AB",
        lookup={
            "preston": "Lancashire - Central",
            "lancashire": "Lancashire - East",
        },
    )

    assert result.status == "ROUTED"
    assert result.region == "Lancashire - Central"
    assert result.lookup_key == "preston"
    assert result.evidence == "Exact locality match in geo_lookup.xlsx"


def test_existing_north_east_cluster_rolls_up_to_public_slice() -> None:
    result = route_geography(
        location="Newcastle upon Tyne, NE1 1AA",
        postcode="NE1 1AA",
        lookup={
            "newcastle upon tyne": (
                "North East - Tyneside, Wearside & Northumberland"
            )
        },
    )

    assert result.status == "ROUTED"
    assert result.cluster == "North East - Tyneside, Wearside & Northumberland"
    assert result.region == "North East"
    assert canonical_public_region(result.cluster) == "North East"


def test_routing_summary_keeps_candidate_and_unresolved_counts() -> None:
    rows = routing.route_manifest_rows(
        [
            factual_row("live", title="Administrator", location="Leeds"),
            factual_row("candidate", title="Receptionist", location="Hull"),
            factual_row("unknown", title="Administrator", location="Unknown place"),
        ],
        geo_lookup={
            "leeds": "Yorkshire - West",
            "hull": "Yorkshire - East",
        },
        authorities=authorities(),
    )
    summary = routing.routing_summary(
        rows,
        discovery_summary={
            "run_date": "2026-08-06",
            "manifest_sha256": "b" * 64,
        },
        routed_sha256="c" * 64,
        unresolved_sha256="d" * 64,
    )

    assert summary["records"] == 3
    assert summary["routed"] == 2
    assert summary["unresolved"] == 1
    assert summary["publish_eligible_live"] == 1
    assert summary["candidate_or_unregistered"] == 2


def test_unresolved_csv_uses_same_inspectable_contract(tmp_path: Path) -> None:
    rows = routing.route_manifest_rows(
        [factual_row("unknown", title="Administrator", location="Unknown place")],
        geo_lookup={},
        authorities=authorities(),
    )
    path = tmp_path / "unresolved.csv"
    path.write_bytes(routing.csv_content(rows))

    with path.open(newline="", encoding="utf-8") as handle:
        parsed = list(csv.DictReader(handle))

    assert parsed[0]["source_job_id"] == "unknown"
    assert parsed[0]["geography_status"] == "UNRESOLVED"
    assert parsed[0]["publish_eligible"] == "NO"
