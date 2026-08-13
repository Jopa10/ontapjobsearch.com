from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from pathlib import Path

import pytest

from external_sources import compose_teaching_vacancies_regional as generic
from external_sources import compose_west_yorkshire_admin as legacy_west
from external_sources import teaching_vacancies_regional_approved as approval

TODAY = date(2026, 8, 6)
NOW = datetime(2026, 8, 6, 12, 0).astimezone()


def base_job(job_id: str, region: str, *, source: str = "JobG8") -> dict:
    return {
        "job_id": job_id,
        "title": "Administrator",
        "company": "Base Employer",
        "location": "Example Town",
        "region": region,
        "description": "Base vacancy",
        "apply_url": "https://example.test/base/" + job_id,
        "source": source,
        "closing_date": "2026-08-31",
    }


def teaching_job(
    job_id: str,
    region: str,
    *,
    title: str = "School Administrator",
    company: str = "Example Academy",
    location: str = "Example Town",
    closing_date: str = "2026-08-31",
) -> dict:
    return {
        "job_id": "teaching-vacancies-" + job_id,
        "title": title,
        "company": company,
        "location": location,
        "region": region,
        "description": "Approved Teaching Vacancies role",
        "apply_url": "https://teaching-vacancies.service.gov.uk/jobs/" + job_id,
        "source": "Teaching Vacancies",
        "closing_date": closing_date,
    }


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def write_snapshot(
    snapshot_dir: Path,
    evidence_dir: Path,
    *,
    slug: str,
    region: str,
    rows: list[dict],
) -> tuple[Path, Path]:
    snapshot_path = snapshot_dir / f"{slug}-admin-service.json"
    write_json(snapshot_path, rows)
    content = snapshot_path.read_bytes()
    evidence_path = evidence_dir / f"{slug}-admin-service-evidence.json"
    write_json(
        evidence_path,
        {
            "contract_version": approval.APPROVAL_CONTRACT_VERSION,
            "source": "Teaching Vacancies",
            "region": region,
            "category": "admin_service",
            "slice_status": "LIVE",
            "approved_snapshot_sha256": hashlib.sha256(content).hexdigest(),
            "approved_rows": len(rows),
            "approved_job_ids": [row["job_id"] for row in rows],
        },
    )
    return snapshot_path, evidence_path


def write_register(path: Path, rows: list[tuple[str, str]]) -> None:
    path.write_text(
        "region,category,status\n"
        + "".join(
            f"{region},admin_service,{status}\n" for region, status in rows
        ),
        encoding="utf-8",
    )


def test_generic_west_composition_matches_legacy_behavior() -> None:
    region = "Yorkshire - West"
    current = [
        teaching_job("old", region),
        base_job("jobg8-1", region),
    ]
    approved = [teaching_job("new", region)]

    legacy_rows, legacy_counts = legacy_west.compose_rows(
        current,
        approved,
        today=TODAY,
    )
    generic_rows, generic_counts = generic.compose_rows(
        current,
        approved,
        region=region,
        today=TODAY,
    )

    assert generic_rows == legacy_rows
    assert generic_counts["base_rows"] == legacy_counts["jobg8_or_other"]
    assert (
        generic_counts["teaching_vacancies"]
        == legacy_counts["teaching_vacancies"]
    )


def test_compose_preserves_base_and_filters_expired_and_duplicate() -> None:
    region = "Sussex"
    base = base_job("jobg8-1", region)
    duplicate = teaching_job(
        "duplicate",
        region,
        title=base["title"],
        company=base["company"],
        location=base["location"],
    )
    expired = teaching_job("expired", region, closing_date="2026-08-05")
    accepted = teaching_job("accepted", region)

    rows, counts = generic.compose_rows(
        [base],
        [duplicate, expired, accepted],
        region=region,
        today=TODAY,
    )

    assert [row["job_id"] for row in rows] == [
        "teaching-vacancies-accepted",
        "jobg8-1",
    ]
    assert counts["base_rows"] == 1
    assert counts["teaching_vacancies"] == 1
    assert counts["expired_teaching_vacancies_skipped"] == 1
    assert counts["duplicate_teaching_vacancies_skipped"] == 1


def test_cross_source_school_employer_alias_is_deduplicated_conservatively() -> None:
    region = "North East"
    nejobs = base_job("nejobs-300098", region, source="NEJobs")
    nejobs.update(
        {
            "title": "Administration Assistant",
            "company": "Bishop Bewick Catholic Education Trust",
            "location": (
                "St Benet Biscop Catholic Academy, Ridge Terrace, "
                "Bedlington, NE22 6ED"
            ),
            "closing_date": "2026-08-17",
        }
    )
    teaching = teaching_job(
        "administration-assistant-st-benet",
        region,
        title="Administration Assistant",
        company="St Benet Biscop Catholic Academy",
        location="Bedlington",
        closing_date="2026-08-17",
    )
    unrelated = teaching_job(
        "administration-assistant-other-school",
        region,
        title="Administration Assistant",
        company="Northumberland Learning Partnership",
        location="Bedlington",
        closing_date="2026-08-17",
    )

    rows, counts = generic.compose_rows(
        [nejobs],
        [teaching, unrelated],
        region=region,
        today=TODAY,
    )

    assert [row["job_id"] for row in rows] == [
        "teaching-vacancies-administration-assistant-other-school",
        "nejobs-300098",
    ]
    assert counts["duplicate_teaching_vacancies_skipped"] == 1


def test_external_only_overwrite_is_blocked() -> None:
    region = "Yorkshire - West"
    with pytest.raises(ValueError, match="external-only overwrite blocked"):
        generic.compose_rows(
            [teaching_job("old", region)],
            [teaching_job("new", region)],
            region=region,
            today=TODAY,
        )


def test_missing_snapshot_retains_current_output(tmp_path: Path) -> None:
    current_dir = tmp_path / "current"
    snapshot_dir = tmp_path / "snapshots"
    evidence_dir = tmp_path / "evidence"
    register = tmp_path / "register.csv"
    current_path = current_dir / "sussex-admin-service.json"
    original = [base_job("jobg8-1", "Sussex")]
    write_json(current_path, original)
    snapshot_dir.mkdir()
    evidence_dir.mkdir()
    write_register(register, [("Sussex", "LIVE")])

    results = generic.compose_directory(
        current_output_dir=current_dir,
        snapshot_dir=snapshot_dir,
        evidence_dir=evidence_dir,
        slice_register=register,
        today=TODAY,
        write=True,
    )

    assert results[0].status == "SKIPPED"
    assert "no approved" in results[0].reason
    assert json.loads(current_path.read_text()) == original


def test_candidate_register_blocks_even_valid_live_evidence(tmp_path: Path) -> None:
    current_dir = tmp_path / "current"
    snapshot_dir = tmp_path / "snapshots"
    evidence_dir = tmp_path / "evidence"
    register = tmp_path / "register.csv"
    current_path = current_dir / "east-yorkshire-admin-service.json"
    original = [base_job("jobg8-1", "Yorkshire - East")]
    write_json(current_path, original)
    write_snapshot(
        snapshot_dir,
        evidence_dir,
        slug="east-yorkshire",
        region="Yorkshire - East",
        rows=[teaching_job("east", "Yorkshire - East")],
    )
    write_register(register, [("Yorkshire - East", "CANDIDATE")])

    results = generic.compose_directory(
        current_output_dir=current_dir,
        snapshot_dir=snapshot_dir,
        evidence_dir=evidence_dir,
        slice_register=register,
        today=TODAY,
        write=True,
    )

    output_result = next(row for row in results if row.path == current_path)
    assert output_result.status == "SKIPPED"
    assert "not LIVE" in output_result.reason
    assert json.loads(current_path.read_text()) == original


def test_tampered_snapshot_is_blocked_by_evidence_hash(tmp_path: Path) -> None:
    snapshot_dir = tmp_path / "snapshots"
    evidence_dir = tmp_path / "evidence"
    snapshot_path, _ = write_snapshot(
        snapshot_dir,
        evidence_dir,
        slug="west-yorkshire",
        region="Yorkshire - West",
        rows=[teaching_job("one", "Yorkshire - West")],
    )
    write_json(
        snapshot_path,
        [
            teaching_job("one", "Yorkshire - West"),
            teaching_job("tampered", "Yorkshire - West"),
        ],
    )

    with pytest.raises(ValueError, match="SHA256"):
        generic.load_approved_snapshots(
            snapshot_dir,
            evidence_dir=evidence_dir,
        )


def test_region_neutral_directory_composition_writes_two_live_slices(
    tmp_path: Path,
) -> None:
    current_dir = tmp_path / "current"
    snapshot_dir = tmp_path / "snapshots"
    evidence_dir = tmp_path / "evidence"
    register = tmp_path / "register.csv"
    west_path = current_dir / "west-yorkshire-admin-service.json"
    south_path = current_dir / "south-yorkshire-admin-service.json"
    customer_path = current_dir / "west-yorkshire-customer-service.json"
    write_json(west_path, [base_job("west-base", "Yorkshire - West")])
    write_json(south_path, [base_job("south-base", "Yorkshire - South")])
    customer_original = [base_job("west-customer-base", "Yorkshire - West")]
    write_json(customer_path, customer_original)
    write_snapshot(
        snapshot_dir,
        evidence_dir,
        slug="west-yorkshire",
        region="Yorkshire - West",
        rows=[teaching_job("west-external", "Yorkshire - West")],
    )
    write_snapshot(
        snapshot_dir,
        evidence_dir,
        slug="south-yorkshire",
        region="Yorkshire - South",
        rows=[teaching_job("south-external", "Yorkshire - South")],
    )
    write_register(
        register,
        [
            ("Yorkshire - West", "LIVE"),
            ("Yorkshire - South", "LIVE"),
        ],
    )

    results = generic.compose_directory(
        current_output_dir=current_dir,
        snapshot_dir=snapshot_dir,
        evidence_dir=evidence_dir,
        slice_register=register,
        today=TODAY,
        write=True,
    )

    assert {row.status for row in results} == {"WRITTEN"}
    assert {row.path for row in results} == {west_path, south_path}
    assert [row["job_id"] for row in json.loads(west_path.read_text())] == [
        "teaching-vacancies-west-external",
        "west-base",
    ]
    assert [row["job_id"] for row in json.loads(south_path.read_text())] == [
        "teaching-vacancies-south-external",
        "south-base",
    ]
    assert json.loads(customer_path.read_text()) == customer_original


def test_empty_current_output_is_left_unchanged(tmp_path: Path) -> None:
    current_dir = tmp_path / "current"
    snapshot_dir = tmp_path / "snapshots"
    evidence_dir = tmp_path / "evidence"
    register = tmp_path / "register.csv"
    current_path = current_dir / "west-yorkshire-admin-service.json"
    write_json(current_path, [])
    snapshot_dir.mkdir()
    evidence_dir.mkdir()
    write_register(register, [("Yorkshire - West", "LIVE")])

    results = generic.compose_directory(
        current_output_dir=current_dir,
        snapshot_dir=snapshot_dir,
        evidence_dir=evidence_dir,
        slice_register=register,
        today=TODAY,
        write=True,
    )

    assert results[0].status == "SKIPPED"
    assert "empty" in results[0].reason
    assert json.loads(current_path.read_text()) == []
