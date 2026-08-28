from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

import pytest

from external_sources import teaching_vacancies_publish_verification as verification
from external_sources.teaching_vacancies_regional_approved import (
    APPROVAL_CONTRACT_VERSION,
)

TODAY = date(2026, 8, 28)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def base_job(job_id: str, region: str, source: str = "JobG8") -> dict:
    return {
        "job_id": job_id,
        "title": "Administrator",
        "company": "Base Employer",
        "location": "Example Town",
        "region": region,
        "description": "Base vacancy",
        "apply_url": f"https://example.test/{job_id}",
        "source": source,
        "closing_date": "2026-09-30",
    }


def teaching_job(job_id: str, region: str) -> dict:
    return {
        "job_id": f"teaching-vacancies-{job_id}",
        "title": "School Administrator",
        "company": "Example Academy",
        "location": "Example Town",
        "region": region,
        "description": "Teaching vacancy",
        "apply_url": f"https://teaching-vacancies.service.gov.uk/jobs/{job_id}",
        "source": "Teaching Vacancies",
        "closing_date": "2026-09-30",
    }


def write_approved(
    snapshot_dir: Path,
    evidence_dir: Path,
    *,
    slug: str,
    region: str,
    rows: list[dict],
) -> None:
    snapshot_path = snapshot_dir / f"{slug}-admin-service.json"
    write_json(snapshot_path, rows)
    evidence_path = evidence_dir / f"{slug}-admin-service-evidence.json"
    write_json(
        evidence_path,
        {
            "contract_version": APPROVAL_CONTRACT_VERSION,
            "source": "Teaching Vacancies",
            "region": region,
            "category": "admin_service",
            "slice_status": "LIVE",
            "approved_snapshot_sha256": hashlib.sha256(
                snapshot_path.read_bytes()
            ).hexdigest(),
            "approved_rows": len(rows),
            "approved_job_ids": [row["job_id"] for row in rows],
        },
    )


def verify(
    tmp_path: Path,
    regions: list[str],
    *,
    maximum: int = 3,
) -> verification.PublishVerification:
    return verification.verify_publishable_regions(
        regions,
        current_output_dir=tmp_path / "current",
        snapshot_dir=tmp_path / "snapshots",
        evidence_dir=tmp_path / "evidence",
        today=TODAY,
        max_isolated_regions=maximum,
    )


def test_north_east_rollup_matches_detailed_base_regions(tmp_path: Path) -> None:
    region = "North East"
    current = tmp_path / "current" / "north-east-admin-service.json"
    snapshot = [teaching_job("school-admin", region)]
    combined = snapshot + [
        base_job("jobg8-1", "North East"),
        base_job(
            "nejobs-1",
            "North East - Tyneside, Wearside & Northumberland",
            "NEJobs",
        ),
        base_job(
            "vonne-1",
            "North East - County Durham & Darlington/Hartlepool",
            "VONNE",
        ),
    ]
    write_json(current, combined)
    write_approved(
        tmp_path / "snapshots",
        tmp_path / "evidence",
        slug="north-east",
        region=region,
        rows=snapshot,
    )

    report = verify(tmp_path, [region])

    assert report.isolated_regions == ()
    assert report.regions[0].status == "VERIFIED"
    assert report.regions[0].base_rows == 3


def test_three_missing_regions_are_isolated_while_clean_region_verifies(
    tmp_path: Path,
) -> None:
    clean_region = "Sussex"
    snapshot = [teaching_job("sussex", clean_region)]
    write_json(
        tmp_path / "current" / "sussex-admin-service.json",
        snapshot + [base_job("jobg8-sussex", clean_region)],
    )
    write_approved(
        tmp_path / "snapshots",
        tmp_path / "evidence",
        slug="sussex",
        region=clean_region,
        rows=snapshot,
    )

    report = verify(
        tmp_path,
        [clean_region, "Berkshire", "Kent", "Norfolk"],
    )
    verification.enforce_isolation_threshold(report)

    assert report.isolated_regions == ("Berkshire", "Kent", "Norfolk")
    assert next(row for row in report.regions if row.region == clean_region).status == (
        "VERIFIED"
    )


def test_four_missing_regions_exceed_threshold(tmp_path: Path) -> None:
    (tmp_path / "current").mkdir()
    report = verify(
        tmp_path,
        ["Berkshire", "Kent", "Norfolk", "Sussex"],
    )

    with pytest.raises(verification.PublishIntegrityError, match="4 Teaching"):
        verification.enforce_isolation_threshold(report)


def test_exact_recomposition_mismatch_is_always_blocking(tmp_path: Path) -> None:
    region = "Sussex"
    write_json(
        tmp_path / "current" / "sussex-admin-service.json",
        [teaching_job("old", region), base_job("jobg8-1", region)],
    )
    write_approved(
        tmp_path / "snapshots",
        tmp_path / "evidence",
        slug="sussex",
        region=region,
        rows=[teaching_job("new", region)],
    )

    with pytest.raises(verification.PublishIntegrityError, match="exactly match"):
        verify(tmp_path, [region])
