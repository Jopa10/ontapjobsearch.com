from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from review_hub import adapters


TODAY = date(2026, 8, 21)


def test_nhs_poss_rows_do_not_enter_unified_daily_edit_queue(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(adapters, "PIPELINE_ROOT", tmp_path)
    review_dir = tmp_path / "reviews/external"
    review_dir.mkdir(parents=True)

    (review_dir / "nhs-jobs-summary.md").write_text(
        "review_date: 2026-08-21\n",
        encoding="utf-8",
    )
    with (review_dir / "nhs-jobs-review.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_job_id",
                "title",
                "final_decision",
                "manual_action",
            ],
        )
        writer.writeheader()
        for index in range(100):
            writer.writerow(
                {
                    "source_job_id": f"nhs-{index}",
                    "title": "Borderline NHS Administrator",
                    "final_decision": "POSS",
                    "manual_action": "",
                }
            )

    result = adapters.load_nhs(TODAY)

    assert result.state == "OK"
    assert result.items == ()
    assert result.publish_workflow == "publish-reviewed-nhs-admin-service.yml"
    assert result.publish_requires_approval is True
    assert result.shared_publish_after is True
    assert "optional" in result.note
