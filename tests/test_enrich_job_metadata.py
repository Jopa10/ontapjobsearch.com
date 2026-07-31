from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pandas as pd
import pytest

MODULE_PATH = Path(__file__).parents[1] / "pipeline" / "scripts" / "enrich_job_metadata.py"
spec = importlib.util.spec_from_file_location("enrich_job_metadata", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def test_jobg8_metadata_is_added_without_overwriting_core_fields():
    frame = pd.DataFrame(
        [
            {
                "/Job/DisplayReference": "job-1",
                "/Job/AdvertiserName": "Example Recruitment",
                "/Job/AdvertiserType": "Agency",
                "/Job/WorkHours": "Full time",
                "/Job/SalaryPeriod": "Annual",
            }
        ]
    )
    metadata = module.metadata_by_job_id(frame)
    rows, changed, unmatched = module.enrich_rows(
        [
            {
                "job_id": "job-1",
                "title": "Administrator",
                "company": "Example Recruitment - Agency - Permanent",
                "source": "JobG8",
            }
        ],
        metadata,
    )

    assert unmatched == []
    assert changed == 1
    assert rows[0]["title"] == "Administrator"
    assert rows[0]["advertiser_name"] == "Example Recruitment"
    assert rows[0]["advertiser_type"] == "Agency"
    assert rows[0]["work_pattern"] == "Full time"
    assert rows[0]["salary_period"] == "Annual"
    assert rows[0]["posted_date_basis"] == ""


def test_external_source_keeps_its_factual_work_pattern():
    rows, changed, unmatched = module.enrich_rows(
        [
            {
                "job_id": "nejobs-1",
                "company": "Example Council",
                "source": "NEJobs",
                "work_pattern": "Part time",
            }
        ],
        {},
    )

    assert unmatched == []
    assert changed == 1
    assert rows[0]["advertiser_name"] == "Example Council"
    assert rows[0]["work_pattern"] == "Part time"
    assert rows[0]["advertiser_type"] == ""
    assert rows[0]["salary_period"] == ""
    assert rows[0]["posted_date_basis"] == ""


def test_unmatched_jobg8_rows_are_retained_without_guessing(tmp_path: Path):
    output = tmp_path / "output"
    output.mkdir()
    original = [{"job_id": "missing", "source": "JobG8", "title": "Old row"}]
    (output / "jobs.json").write_text(json.dumps(original), encoding="utf-8")

    totals = module.enrich_directory(output, {}, write=False)

    assert totals["unmatched_rows"] == 1
    assert json.loads((output / "jobs.json").read_text(encoding="utf-8")) == original


def test_source_posted_date_is_marked_explicitly():
    frame = pd.DataFrame(
        [
            {
                "/Job/DisplayReference": "job-2",
                "/Job/AdvertiserName": "Employer",
                "/Job/AdvertiserType": "Company",
                "/Job/PostedDate": "2026-07-30",
            }
        ]
    )
    metadata = module.metadata_by_job_id(frame)
    assert metadata["job-2"]["posted_date_basis"] == "source"
