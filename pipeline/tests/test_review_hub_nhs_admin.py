from __future__ import annotations

from datetime import date
from pathlib import Path

from review_hub import adapters, master_review

TODAY = date(2026, 8, 20)


def _write_review(root: Path) -> None:
    review_dir = root / "reviews/external"
    review_dir.mkdir(parents=True)
    (review_dir / "nhs-jobs-summary.md").write_text(
        "# NHS Jobs admin/service review\n\nreview_date: 2026-08-20\n",
        encoding="utf-8",
    )
    (review_dir / "nhs-jobs-review.csv").write_text(
        "review_date,source,source_job_id,title,employer,location,postcode,region,geo_cluster,geography_status,geography_reason,salary_text,employment_type,posted_date,closing_date,source_url,apply_url,description,classification,classification_reason,switchability,slice_status,publish_eligible,duplicate_check,duplicate_job_id,manual_action,final_decision,factual_fingerprint\n"
        "2026-08-20,NHS Jobs,nhs1,Medical Secretary,Trust A,Leeds,,Yorkshire - West,Yorkshire - West,ROUTED,exact,£28000,Full time,2026-08-19,2026-08-31,https://example.test/1,https://example.test/1,,POSS,Potential admin/service title,BRIDGEABLE,LIVE,YES,NO_MATCH,,,POSS,abc\n",
        encoding="utf-8",
    )


def test_nhs_is_future_until_first_review(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(adapters, "PIPELINE_ROOT", tmp_path)
    result = adapters.load_nhs(TODAY)
    assert result.state == "FUTURE"
    assert result.items == ()


def test_nhs_poss_stays_out_of_unified_review_but_source_publishes(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _write_review(tmp_path)
    monkeypatch.setattr(adapters, "PIPELINE_ROOT", tmp_path)
    result = adapters.load_nhs(TODAY)
    assert result.state == "OK"
    assert result.items == ()
    assert result.publish_workflow == "publish-reviewed-nhs-admin-service.yml"
    assert result.publish_requires_approval is True
    assert result.shared_publish_after is True
    assert "optional" in result.note


def test_master_routes_nhs_action_to_nhs_summary(tmp_path: Path, monkeypatch) -> None:
    _write_review(tmp_path)
    monkeypatch.setattr(master_review, "PIPELINE_ROOT", tmp_path)
    from review_hub.contracts import ParsedDecision, ReviewItem
    decision = ParsedDecision(
        "select",
        "nhs",
        ReviewItem(
            source="NHS Jobs",
            source_job_id="nhs1",
            title="Medical Secretary",
            category="admin_service",
        ),
        "fingerprint",
    )
    summary = tmp_path / "reviews/external/nhs-jobs-summary.md"
    summary.write_text(
        "---\naction:\nsource_job_id: nhs1\n---\n",
        encoding="utf-8",
    )
    master_review._route_action(decision)
    assert "action: select" in summary.read_text(encoding="utf-8")
