from __future__ import annotations

import hashlib
from datetime import date
from pathlib import Path

from external_sources import compose_teaching_vacancies_regional as generic

REPO_ROOT = Path(__file__).resolve().parents[2]
PIPELINE_ROOT = REPO_ROOT / "pipeline"
WORKFLOWS = (
    REPO_ROOT / ".github/workflows/run-service-admin-pipeline.yml",
    REPO_ROOT / ".github/workflows/run-full-jobg8-daily-process.yml",
)


def test_daily_workflows_keep_legacy_fallback_before_generic_composer() -> None:
    expected = (
        "python -m external_sources.compose_northeast_admin --write",
        "python -m external_sources.compose_west_yorkshire_admin --write",
        "python -m external_sources.compose_teaching_vacancies_regional --write",
    )
    for path in WORKFLOWS:
        text = path.read_text(encoding="utf-8")
        positions = [text.index(command) for command in expected]
        assert positions == sorted(positions), path
        assert all(text.count(command) == 1 for command in expected), path


def test_generic_composer_dry_run_does_not_mutate_outputs() -> None:
    output_dir = PIPELINE_ROOT / "output-admin-service"
    snapshots = PIPELINE_ROOT / "output-external/teaching-vacancies-regional"
    evidence = PIPELINE_ROOT / "manifests/external/teaching-vacancies/approved"
    register = PIPELINE_ROOT / "registers/region_category_slice_register.csv"
    before = {
        path: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in output_dir.glob("*.json")
    }

    results = generic.compose_directory(
        current_output_dir=output_dir,
        snapshot_dir=snapshots,
        evidence_dir=evidence,
        slice_register=register,
        today=date(2026, 8, 6),
        write=False,
    )

    after = {
        path: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in output_dir.glob("*.json")
    }
    assert before == after
    assert results
    # A dry-run may legitimately report WOULD_WRITE when an approved snapshot
    # differs from the current base output; the non-mutation check above is the
    # safety invariant.
    assert all(row.status in {"SKIPPED", "UNCHANGED", "WOULD_WRITE"} for row in results)
