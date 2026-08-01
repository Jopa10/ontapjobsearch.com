from __future__ import annotations

import json
from pathlib import Path

from pipeline.scripts.attach_at_a_glance_attributes import (
    FIELD,
    attach_directory,
    attach_rows,
    attributes_for_job,
)


def admin_job() -> dict[str, str]:
    return {
        "job_id": "admin-1",
        "title": "Customer Service Administrator",
        "source": "JobG8",
        "category": "Admin/Service – Office Support",
        "description": (
            "About the Role\n"
            "Responding to customer enquiries by telephone and email.\n"
            "Maintain accurate customer records and update internal systems.\n"
            "Prepare service documents for the operations team.\n"
            "Requirements\n"
            "Previous administration experience is preferred."
        ),
    }


def test_validated_attributes_are_attached() -> None:
    rows, changed, generated = attach_rows([admin_job()])

    assert changed == 1
    assert generated == 1
    assert rows[0][FIELD] == [
        "Telephone handling",
        "Customer enquiries",
        "Email handling",
        "Records administration",
        "Systems administration",
    ]


def test_external_source_never_receives_inferred_duties() -> None:
    job = admin_job()
    job.update(source="NEJobs", at_a_glance_attributes=["Old", "Unsafe"])

    rows, changed, generated = attach_rows([job])

    assert changed == 1
    assert generated == 0
    assert FIELD not in rows[0]


def test_truncated_advert_removes_stale_attributes() -> None:
    job = admin_job()
    job["description"] += " Click apply for full job details."
    job[FIELD] = ["Old duty", "Another old duty"]

    rows, changed, generated = attach_rows([job])

    assert changed == 1
    assert generated == 0
    assert FIELD not in rows[0]


def test_same_description_produces_same_attributes() -> None:
    assert attributes_for_job(admin_job()) == attributes_for_job(admin_job())


def test_directory_dry_run_does_not_modify_source(tmp_path: Path) -> None:
    output = tmp_path / "output"
    output.mkdir()
    path = output / "jobs.json"
    original = [admin_job()]
    path.write_text(json.dumps(original), encoding="utf-8")

    totals = attach_directory(output, write=False)

    assert totals == {
        "files": 1,
        "rows": 1,
        "changed_rows": 1,
        "generated_rows": 1,
    }
    assert json.loads(path.read_text(encoding="utf-8")) == original
