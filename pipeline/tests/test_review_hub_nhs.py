from __future__ import annotations

from datetime import date
from pathlib import Path

from review_hub import adapters
from review_hub.nhs_decisions import write_decision

TODAY = date(2026, 8, 17)


def test_nhs_remains_future_until_review_output_exists(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(adapters, "PIPELINE_ROOT", tmp_path)
    result = adapters.load_nhs(TODAY)
    assert result.state == "FUTURE"
    assert result.items == ()


def _write_review_fixture(tmp_path: Path) -> Path:
    review_dir = tmp_path / "reviews/external"
    review_dir.mkdir(parents=True)
    (review_dir / "nhs-jobs-summary.md").write_text(
        "review_date: 2026-08-17\n",
        encoding="utf-8",
    )
    (review_dir / "nhs-jobs-review.csv").write_text(
        "source_job_id,title,employer,locations,salary_text,closing_date,final_decision,manual_action,ontap_category,switchability,classification_reason,source_url\n"
        "a1,Borderline Administrator,Trust A,Leeds,£28000,2026-08-31,POSS,,admin_service,BRIDGEABLE,Needs advert review,https://example.test/a1\n"
        "s1,Healthcare Support Worker,Trust B,Sheffield,£25000,2026-08-31,POSS,,support_worker,HEALTHCARE_EXPERIENCED,Healthcare experience essential,https://example.test/s1\n"
        "s2,Support Worker,Trust C,York,£24000,2026-08-31,HC,,support_worker,OPEN_SWITCH,Training provided,https://example.test/s2\n"
        "s3,Support Worker,Trust D,Hull,£24000,2026-08-31,POSS,exclude,support_worker,BRIDGEABLE,Already decided,https://example.test/s3\n",
        encoding="utf-8",
    )
    return review_dir


def test_nhs_loads_only_unresolved_poss_across_categories(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(adapters, "PIPELINE_ROOT", tmp_path)
    _write_review_fixture(tmp_path)

    result = adapters.load_nhs(TODAY)
    assert result.state == "OK"
    assert len(result.items) == 2
    assert {item.category for item in result.items} == {"admin_service", "support_worker"}
    assert {item.source_job_id for item in result.items} == {"a1", "s1"}
    support = next(item for item in result.items if item.source_job_id == "s1")
    assert support.reason.startswith("HEALTHCARE_EXPERIENCED:")


def test_nhs_remembers_decision_until_vacancy_fingerprint_changes(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(adapters, "PIPELINE_ROOT", tmp_path)
    review_dir = _write_review_fixture(tmp_path)

    first = adapters.load_nhs(TODAY)
    support = next(item for item in first.items if item.source_job_id == "s1")
    write_decision(
        review_dir / "nhs-jobs-decisions.csv",
        category=support.category,
        source_job_id=support.source_job_id,
        hub_fingerprint=support.fingerprint(),
        action="select",
        title=support.title,
    )

    remembered = adapters.load_nhs(TODAY)
    assert "s1" not in {item.source_job_id for item in remembered.items}

    csv_path = review_dir / "nhs-jobs-review.csv"
    csv_path.write_text(
        csv_path.read_text(encoding="utf-8").replace(
            "Healthcare experience essential",
            "Changed essential criteria requires fresh review",
        ),
        encoding="utf-8",
    )
    changed = adapters.load_nhs(TODAY)
    assert "s1" in {item.source_job_id for item in changed.items}


def test_nhs_stale_output_blocks_daily_review_readiness(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(adapters, "PIPELINE_ROOT", tmp_path)
    review_dir = tmp_path / "reviews/external"
    review_dir.mkdir(parents=True)
    (review_dir / "nhs-jobs-summary.md").write_text(
        "review_date: 2026-08-16\n",
        encoding="utf-8",
    )
    (review_dir / "nhs-jobs-review.csv").write_text(
        "source_job_id,title,final_decision,manual_action\n"
        "s1,Support Worker,POSS,\n",
        encoding="utf-8",
    )

    result = adapters.load_nhs(TODAY)
    assert result.state == "STALE"
    assert result.items == ()
    assert result.needs_attention is True
