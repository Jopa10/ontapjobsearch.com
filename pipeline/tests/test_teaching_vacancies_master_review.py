from __future__ import annotations

import csv
import io
from pathlib import Path

from external_sources import teaching_vacancies_master_review as master


def write_review(path: Path, *, region: str, source_job_id: str) -> None:
    fields = [field for field in master.MASTER_FIELDS if field != "regional_slice"]
    row = {field: "" for field in fields}
    row.update(
        {
            "final_decision": "SELECTED",
            "title": "Administrator",
            "salary_text": "£25,000",
            "classification_reason": "Clear admin/service title: administrator",
            "ontap_region": region,
            "source_job_id": source_job_id,
        }
    )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def test_master_review_combines_regions_and_orders_requested_columns(
    tmp_path: Path,
) -> None:
    write_review(
        tmp_path / "west-yorkshire-admin-service-review.csv",
        region="Yorkshire - West",
        source_job_id="west",
    )
    write_review(
        tmp_path / "north-east-admin-service-review.csv",
        region="North East",
        source_job_id="north-east",
    )

    rows = master.build_master_rows(tmp_path)
    content = master.master_csv_bytes(rows).decode("utf-8")
    parsed = list(csv.DictReader(io.StringIO(content)))

    assert tuple(parsed[0])[:5] == (
        "final_decision",
        "title",
        "salary_text",
        "regional_slice",
        "classification_reason",
    )
    assert [row["regional_slice"] for row in parsed] == [
        "North East / admin_service",
        "Yorkshire - West / admin_service",
    ]
    assert {row["source_job_id"] for row in parsed} == {"north-east", "west"}
