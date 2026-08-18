from __future__ import annotations

from datetime import date
from pathlib import Path

from external_sources.nhs_support_worker_discovery import classify_rows, counts, write_outputs


def test_discovery_classifies_realistic_support_worker_mix() -> None:
    rows = classify_rows(
        [
            {
                "source_job_id": "1",
                "title": "Healthcare Support Worker",
                "description": "Full training will be provided. No previous experience is required.",
            },
            {
                "source_job_id": "2",
                "title": "Healthcare Support Worker",
                "description": "Previous healthcare experience is essential.",
            },
            {
                "source_job_id": "3",
                "title": "Mental Health Support Worker",
                "description": "Experience desirable.",
            },
            {
                "source_job_id": "4",
                "title": "Senior Healthcare Support Worker",
                "description": "Full training provided.",
            },
            {"source_job_id": "5", "title": "Administrator"},
        ]
    )
    assert len(rows) == 4
    assert counts(rows) == {
        "OPEN_SWITCH": 1,
        "BRIDGEABLE": 1,
        "HEALTHCARE_EXPERIENCED": 1,
        "NHS_EXPERIENCED": 0,
        "HARD_PASS": 1,
    }


def test_write_outputs_preserves_non_support_rows_and_unchanged_action(tmp_path: Path) -> None:
    review = tmp_path / "nhs-jobs-review.csv"
    summary = tmp_path / "nhs-jobs-summary.md"
    review.write_text(
        "source_job_id,title,employer,locations,salary_text,closing_date,source_url,final_decision,manual_action,ontap_category,switchability,classification_reason,source\n"
        "a1,Administrator,Trust,Leeds,£25000,2026-08-31,https://x/a1,POSS,select,admin_service,BRIDGEABLE,review,NHS Jobs\n"
        "s1,Healthcare Support Worker,Trust,Leeds,£24000,2026-08-31,https://x/s1,POSS,exclude,support_worker,HEALTHCARE_EXPERIENCED,Previous healthcare/care experience appears essential,NHS Jobs\n",
        encoding="utf-8",
    )
    support = classify_rows(
        [
            {
                "source_job_id": "s1",
                "title": "Healthcare Support Worker",
                "employer": "Trust",
                "locations": "Leeds",
                "salary_text": "£24000",
                "closing_date": "2026-08-31",
                "source_url": "https://x/s1",
                "description": "Previous healthcare experience is essential.",
            }
        ]
    )
    report = write_outputs(
        support,
        review_csv=review,
        summary_md=summary,
        today=date(2026, 8, 18),
    )
    text = review.read_text(encoding="utf-8")
    assert "a1,Administrator" in text
    assert "s1,Healthcare Support Worker" in text
    assert ",exclude,support_worker," in text
    assert report["HEALTHCARE_EXPERIENCED"] == 1
    assert "review_date: 2026-08-18" in summary.read_text(encoding="utf-8")
