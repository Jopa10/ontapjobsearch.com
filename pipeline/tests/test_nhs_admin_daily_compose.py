from __future__ import annotations

import json
from pathlib import Path

import pytest

from external_sources import nhs_admin_service as nhs
from external_sources.compose_nhs_admin_daily import verify_composition


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows), encoding="utf-8")


def base_job(job_id: str) -> dict[str, object]:
    return {
        "job_id": job_id,
        "source": "JobG8",
        "title": "Administrator",
        "apply_url": "https://example.test/base",
        "description": "Base description",
    }


def nhs_job(job_id: str) -> dict[str, object]:
    return {
        "job_id": job_id,
        "source": nhs.SOURCE,
        "title": "Administrator",
        "apply_url": "https://example.test/nhs",
        "description": "NHS description",
    }


def test_verify_composition_accepts_preserved_base_and_20_percent_cap(tmp_path: Path) -> None:
    current = tmp_path / "current"
    composed = tmp_path / "composed"
    base = [base_job(f"base-{n}") for n in range(4)]
    write_rows(current / "north-east-admin-service.json", base)
    write_rows(composed / "north-east-admin-service.json", base + [nhs_job("nhs-1")])

    result = verify_composition(current, composed)

    assert result == {"files": 1, "nhs_accepted": 1, "combined_rows": 5}


def test_verify_composition_rejects_non_nhs_changes(tmp_path: Path) -> None:
    current = tmp_path / "current"
    composed = tmp_path / "composed"
    write_rows(current / "north-east-admin-service.json", [base_job("base-1")])
    write_rows(composed / "north-east-admin-service.json", [base_job("different")])

    with pytest.raises(RuntimeError, match="non-NHS rows changed"):
        verify_composition(current, composed)


def test_verify_composition_rejects_cap_breach(tmp_path: Path) -> None:
    current = tmp_path / "current"
    composed = tmp_path / "composed"
    base = [base_job(f"base-{n}") for n in range(3)]
    write_rows(current / "north-east-admin-service.json", base)
    write_rows(composed / "north-east-admin-service.json", base + [nhs_job("nhs-1")])

    with pytest.raises(RuntimeError, match="cap breached"):
        verify_composition(current, composed)


def test_verify_composition_rejects_missing_nhs_description(tmp_path: Path) -> None:
    current = tmp_path / "current"
    composed = tmp_path / "composed"
    base = [base_job(f"base-{n}") for n in range(4)]
    missing = nhs_job("nhs-1")
    missing["description"] = ""
    write_rows(current / "north-east-admin-service.json", base)
    write_rows(composed / "north-east-admin-service.json", base + [missing])

    with pytest.raises(RuntimeError, match="no description"):
        verify_composition(current, composed)
