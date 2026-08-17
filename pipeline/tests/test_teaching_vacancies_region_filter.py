from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

from external_sources import compose_teaching_vacancies_regional as generic
from external_sources import teaching_vacancies_regional_approved as approval

TODAY = date(2026, 8, 6)


def base_job(job_id: str, region: str) -> dict:
    return {
        "job_id": job_id,
        "title": "Administrator",
        "company": "Base Employer",
        "location": "Example Town",
        "region": region,
        "description": "Base vacancy",
        "apply_url": "https://example.test/" + job_id,
        "source": "JobG8",
        "closing_date": "2026-08-31",
    }


def teaching_job(job_id: str, region: str) -> dict:
    return {
        "job_id": "teaching-vacancies-" + job_id,
        "title": "School Administrator",
        "company": "Example Academy",
        "location": "Example Town",
        "region": region,
        "description": "Approved external vacancy",
        "apply_url": "https://teaching-vacancies.service.gov.uk/jobs/" + job_id,
        "source": "Teaching Vacancies",
        "closing_date": "2026-08-31",
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
) -> None:
    rows = [teaching_job(slug, region)]
    snapshot_path = snapshot_dir / f"{slug}-admin-service.json"
    write_json(snapshot_path, rows)
    write_json(
        evidence_dir / f"{slug}-admin-service-evidence.json",
        {
            "contract_version": approval.APPROVAL_CONTRACT_VERSION,
            "source": "Teaching Vacancies",
            "region": region,
            "category": "admin_service",
            "slice_status": "LIVE",
            "approved_snapshot_sha256": hashlib.sha256(
                snapshot_path.read_bytes()
            ).hexdigest(),
            "approved_rows": 1,
            "approved_job_ids": [rows[0]["job_id"]],
        },
    )


def test_region_filter_writes_only_requested_region(tmp_path: Path) -> None:
    current_dir = tmp_path / "current"
    snapshot_dir = tmp_path / "snapshots"
    evidence_dir = tmp_path / "evidence"
    register = tmp_path / "register.csv"
    west = current_dir / "west-admin-service.json"
    south = current_dir / "south-admin-service.json"
    write_json(west, [base_job("west-base", "Yorkshire - West")])
    write_json(south, [base_job("south-base", "Yorkshire - South")])
    write_snapshot(
        snapshot_dir,
        evidence_dir,
        slug="west-yorkshire",
        region="Yorkshire - West",
    )
    write_snapshot(
        snapshot_dir,
        evidence_dir,
        slug="south-yorkshire",
        region="Yorkshire - South",
    )
    register.write_text(
        "region,category,status\n"
        "Yorkshire - West,admin_service,LIVE\n"
        "Yorkshire - South,admin_service,LIVE\n",
        encoding="utf-8",
    )
    south_before = south.read_bytes()

    results = generic.compose_directory(
        current_output_dir=current_dir,
        snapshot_dir=snapshot_dir,
        evidence_dir=evidence_dir,
        slice_register=register,
        today=TODAY,
        write=True,
        regions={"Yorkshire - West"},
    )

    assert [row["job_id"] for row in json.loads(west.read_text())] == [
        "teaching-vacancies-west-yorkshire",
        "west-base",
    ]
    assert south.read_bytes() == south_before
    south_result = next(row for row in results if row.path == south)
    assert south_result.status == "SKIPPED"
    assert "not requested" in south_result.reason
