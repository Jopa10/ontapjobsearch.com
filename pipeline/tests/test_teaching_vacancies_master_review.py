from __future__ import annotations

import csv
import io
from pathlib import Path

from external_sources import teaching_vacancies_master_review as master


def write_review(
    path: Path, *, region: str, source_job_id: str, slice_status: str
) -> None:
    fields = [
        field
        for field in master.MASTER_FIELDS
        if field not in {"regional_slice", "review_scope"}
    ]
    row = {field: "" for field in fields}
    row.update(
        {
            "final_decision": "SELECTED",
            "title": "Administrator",
            "salary_text": "£25,000",
            "classification": "HC",
            "classification_reason": "Clear admin/service title: administrator",
            "employer": "Example School",
            "location": "Leeds",
            "closing_date": "2026-08-31",
            "ontap_region": region,
            "slice_status": slice_status,
            "source_job_id": source_job_id,
            "source_url": f"https://example.test/{source_job_id}",
            "factual_fingerprint": f"fp-{source_job_id}",
        }
    )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def test_master_review_marks_live_regions_and_writes_summary(tmp_path: Path) -> None:
    write_review(
        tmp_path / "west-yorkshire-admin-service-review.csv",
        region="Yorkshire - West",
        source_job_id="west",
        slice_status="LIVE",
    )
    write_review(
        tmp_path / "bedfordshire-admin-service-review.csv",
        region="Bedfordshire",
        source_job_id="beds",
        slice_status="UNREGISTERED",
    )

    rows = master.build_master_rows(tmp_path)
    content = master.master_csv_bytes(rows).decode("utf-8")
    parsed = list(csv.DictReader(io.StringIO(content)))

    assert tuple(parsed[0])[:6] == (
        "final_decision",
        "title",
        "salary_text",
        "regional_slice",
        "classification_reason",
        "review_scope",
    )
    assert [row["review_scope"] for row in parsed] == [
        master.REVIEW_NOW,
        master.DEFERRED,
    ]
    assert [row["source_job_id"] for row in parsed] == ["west", "beds"]

    summary = master.master_summary_text(rows)
    assert "REVIEW NOW (LIVE regions): **1**" in summary
    assert "DEFERRED - REGION NOT LIVE: **1**" in summary
    assert "## YORKSHIRE - WEST — SELECTED" in summary
    assert "## YORKSHIRE - WEST — EXCLUDED BY REVIEW" in summary
    assert "action:" in summary
    assert "SELECTED | Yorkshire - West | Leeds | £25,000 | Administrator" in summary
    assert "employer: Example School" in summary
    assert "closing_date: 2026-08-31" in summary
    assert "factual_fingerprint: fp-west" in summary
    assert "source_job_id: west" in summary
    assert "source_url: https://example.test/west" in summary
    assert "## DEFERRED REGIONS — NOT FOR MANUAL REVIEW" in summary
    assert "Bedfordshire / admin_service" in summary
    assert "source_job_id: beds" not in summary
