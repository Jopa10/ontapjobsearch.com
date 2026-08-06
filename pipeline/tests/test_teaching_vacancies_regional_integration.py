from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

from external_sources import compose_northeast_admin as northeast
from external_sources import compose_teaching_vacancies_regional as generic
from external_sources import compose_west_yorkshire_admin as legacy_west

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
from publish_verified_pages import Mapping, publish_one

TODAY = date(2026, 8, 6)


def job(
    job_id: str,
    *,
    source: str,
    region: str,
    title: str,
    company: str,
    location: str,
) -> dict:
    return {
        "job_id": job_id,
        "title": title,
        "company": company,
        "location": location,
        "region": region,
        "description": "Vacancy description",
        "apply_url": "https://example.test/" + job_id,
        "source": source,
        "posted_date": "2026-08-01",
        "closing_date": "2026-08-31",
    }


def teaching(job_id: str, region: str, *, title: str = "School Administrator") -> dict:
    return job(
        "teaching-vacancies-" + job_id,
        source="Teaching Vacancies",
        region=region,
        title=title,
        company="Example Academy",
        location="Example Town",
    )


def test_legacy_west_fallback_then_generic_takeover_is_reversible() -> None:
    region = "Yorkshire - West"
    base = job(
        "jobg8-base",
        source="JobG8",
        region=region,
        title="Service Administrator",
        company="Base Employer",
        location="Leeds",
    )
    legacy_snapshot = [teaching("legacy", region)]
    regional_snapshot = [teaching("regional", region)]

    legacy_result, _ = legacy_west.compose_rows(
        [base],
        legacy_snapshot,
        today=TODAY,
    )
    regional_result, _ = generic.compose_rows(
        legacy_result,
        regional_snapshot,
        region=region,
        today=TODAY,
    )
    rolled_back, _ = legacy_west.compose_rows(
        regional_result,
        legacy_snapshot,
        today=TODAY,
    )
    expected_legacy, _ = legacy_west.compose_rows(
        [base],
        legacy_snapshot,
        today=TODAY,
    )

    assert [row["job_id"] for row in regional_result] == [
        "teaching-vacancies-regional",
        "jobg8-base",
    ]
    assert rolled_back == expected_legacy


def test_generic_teaching_composition_preserves_nejobs_and_vonne() -> None:
    region = "North East"
    current = [
        job(
            "nejobs-1",
            source="NEJobs",
            region=region,
            title="Administrator",
            company="Council",
            location="Newcastle",
        ),
        job(
            "vonne-1",
            source="VONNE",
            region=region,
            title="Office Assistant",
            company="Charity",
            location="Durham",
        ),
        job(
            "jobg8-1",
            source="JobG8",
            region=region,
            title="Receptionist",
            company="Agency",
            location="Sunderland",
        ),
    ]

    rows, counts = generic.compose_rows(
        current,
        [teaching("north-east", region)],
        region=region,
        today=TODAY,
    )

    assert [row["source"] for row in rows] == [
        "Teaching Vacancies",
        "NEJobs",
        "VONNE",
        "JobG8",
    ]
    assert counts["base_rows"] == 3


def test_generic_composition_after_northeast_composer_preserves_all_sources() -> None:
    region = "North East"
    jobg8 = [
        job(
            "jobg8-1",
            source="JobG8",
            region=region,
            title="Receptionist",
            company="Agency",
            location="Sunderland",
        )
    ]
    nejobs = [
        job(
            "nejobs-1",
            source="NEJobs",
            region=region,
            title="Administrator",
            company="Council",
            location="Newcastle",
        )
    ]
    vonne = [
        job(
            "vonne-1",
            source="VONNE",
            region=region,
            title="Office Assistant",
            company="Charity",
            location="Durham",
        )
    ]

    north_east_rows, _ = northeast.compose_rows(
        jobg8,
        nejobs,
        vonne,
        today=TODAY,
    )
    final_rows, _ = generic.compose_rows(
        north_east_rows,
        [teaching("school", region)],
        region=region,
        today=TODAY,
    )

    assert {row["source"] for row in final_rows} == {
        "JobG8",
        "NEJobs",
        "VONNE",
        "Teaching Vacancies",
    }


def test_composed_output_passes_existing_publisher_contract(tmp_path: Path) -> None:
    region = "Yorkshire - West"
    base = job(
        "jobg8-1",
        source="JobG8",
        region=region,
        title="Service Administrator",
        company="Base Employer",
        location="Leeds",
    )
    composed, _ = generic.compose_rows(
        [base],
        [teaching("school", region)],
        region=region,
        today=TODAY,
    )
    source_path = tmp_path / "pipeline" / "output.json"
    destination_path = tmp_path / "app" / "page.json"
    source_path.parent.mkdir(parents=True)
    destination_path.parent.mkdir(parents=True)
    source_path.write_text(json.dumps(composed), encoding="utf-8")
    destination_path.write_text("[]\n", encoding="utf-8")
    mapping = Mapping(
        "Test regional admin jobs",
        region,
        "admin_service",
        Path("pipeline/output.json"),
        Path("app/page.json"),
    )

    result = publish_one(
        mapping,
        write=True,
        active_slices={(region, "admin_service")},
        root=tmp_path,
        publication_date="2026-08-06",
    )

    assert result["status"] == "published"
    published = json.loads(destination_path.read_text(encoding="utf-8"))
    assert {row["job_id"] for row in published} == {
        "jobg8-1",
        "teaching-vacancies-school",
    }


def test_existing_publisher_leaves_destination_when_composed_source_empty(
    tmp_path: Path,
) -> None:
    region = "Yorkshire - West"
    source_path = tmp_path / "pipeline" / "output.json"
    destination_path = tmp_path / "app" / "page.json"
    source_path.parent.mkdir(parents=True)
    destination_path.parent.mkdir(parents=True)
    source_path.write_text("[]\n", encoding="utf-8")
    previous = [
        job(
            "existing",
            source="JobG8",
            region=region,
            title="Existing role",
            company="Employer",
            location="Leeds",
        )
    ]
    destination_path.write_text(json.dumps(previous), encoding="utf-8")
    mapping = Mapping(
        "Test regional admin jobs",
        region,
        "admin_service",
        Path("pipeline/output.json"),
        Path("app/page.json"),
    )

    result = publish_one(
        mapping,
        write=True,
        active_slices={(region, "admin_service")},
        root=tmp_path,
        publication_date="2026-08-06",
    )

    assert result["status"] == "skipped"
    assert json.loads(destination_path.read_text(encoding="utf-8")) == previous
