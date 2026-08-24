from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from review_hub.contracts import ReviewItem, SourceResult
from review_hub import master_review

TODAY = date(2026, 8, 17)


def item(
    *,
    title: str = "Borderline Administrator",
    source_job_id: str = "abc-123",
) -> ReviewItem:
    return ReviewItem(
        source="Test Source",
        source_job_id=source_job_id,
        title=title,
        employer="Example Employer",
        location="Leeds",
        region="Yorkshire - West",
        category="admin_service",
        salary="£29,000",
        closing_date="2026-08-31",
        reason="borderline classification",
        source_url=f"https://example.test/jobs/{source_job_id}",
    )


def result(review_item: ReviewItem | None = None) -> SourceResult:
    values = (review_item,) if review_item else ()
    return result_many(values)


def result_many(review_items: tuple[ReviewItem, ...]) -> SourceResult:
    return SourceResult(
        "test",
        "Test Source",
        "OK",
        TODAY.isoformat(),
        review_items,
        publish_workflow="test-publish.yml",
        publish_requires_approval=True,
        shared_publish_after=True,
    )


def test_master_is_single_editable_surface_with_source_status(tmp_path: Path) -> None:
    path = tmp_path / "ontap-daily-review.md"
    text = master_review.master_text(
        [
            result(item()),
            SourceResult("stale", "Stale Source", "STALE", "2026-08-16"),
            SourceResult("nhs", "NHS Jobs", "FUTURE", "", note="reserved"),
        ],
        today=TODAY,
        previous=path,
    )
    path.write_text(text, encoding="utf-8")

    review_date, decisions = master_review.parse_master(path)
    assert review_date == TODAY.isoformat()
    assert len(decisions) == 1
    assert decisions[0].source_key == "test"
    assert decisions[0].item.title == "Borderline Administrator"
    assert decisions[0].fingerprint == item().fingerprint()
    assert "NOT READY TO REVIEW — waiting for: Stale Source" in text
    assert "Do not start reviewing yet" in text
    assert "| Stale Source | STALE |" in text
    assert "| NHS Jobs | FUTURE |" in text
    assert "must not be treated as zero inventory" in text
    assert "Up to 15 unresolved/bad action rows per source" in text


def test_master_ready_banner_ignores_future_sources(tmp_path: Path) -> None:
    path = tmp_path / "ontap-daily-review.md"
    text = master_review.master_text(
        [
            result(item()),
            SourceResult("nhs", "NHS Jobs", "FUTURE", "", note="reserved"),
        ],
        today=TODAY,
        previous=path,
    )

    assert "> **READY TO REVIEW**" in text
    assert f"All active sources are current for {TODAY.isoformat()}" in text
    assert "NOT READY TO REVIEW" not in text


def test_master_carries_decision_only_when_fingerprint_unchanged(tmp_path: Path) -> None:
    path = tmp_path / "ontap-daily-review.md"
    first = master_review.master_text([result(item())], today=TODAY, previous=path)
    path.write_text(first.replace("action:\n", "action: select\n", 1), encoding="utf-8")

    second = master_review.master_text([result(item())], today=TODAY, previous=path)
    assert "---\naction: select\nPOSS |" in second

    changed = master_review.master_text(
        [result(item(title="Changed title"))],
        today=TODAY,
        previous=path,
    )
    assert "---\naction: select\nPOSS |" not in changed
    assert "---\naction:\nPOSS |" in changed


def test_apply_validates_current_fingerprint_and_builds_publish_plan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "ontap-daily-review.md"
    text = master_review.master_text([result(item())], today=TODAY, previous=path)
    path.write_text(text.replace("action:\n", "action: select\n", 1), encoding="utf-8")

    routed = []
    monkeypatch.setattr(master_review, "load_all_sources", lambda today: [result(item())])
    monkeypatch.setattr(master_review, "_route_action", routed.append)

    plan = master_review.apply_master(
        path,
        today=TODAY,
        write=True,
        require_complete=True,
    )
    assert len(routed) == 1
    assert routed[0].action == "select"
    assert plan["actions"] == 1
    assert plan["complete"] is True
    assert plan["quarantined"] == 0
    assert plan["isolated_sources"] == []
    assert plan["publish"] == [
        {
            "source": "test",
            "workflow": "test-publish.yml",
            "approval": True,
            "shared_publish_after": True,
        }
    ]


def test_up_to_15_blank_actions_are_quarantined_and_source_continues(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    review_items = tuple(item(source_job_id=f"job-{index}") for index in range(15))
    source = result_many(review_items)
    path = tmp_path / "ontap-daily-review.md"
    path.write_text(
        master_review.master_text([source], today=TODAY, previous=path),
        encoding="utf-8",
    )
    routed = []
    monkeypatch.setattr(master_review, "load_all_sources", lambda today: [source])
    monkeypatch.setattr(master_review, "_route_action", routed.append)

    plan = master_review.apply_master(
        path,
        today=TODAY,
        write=True,
        require_complete=True,
    )

    assert plan["quarantined"] == 15
    assert plan["isolated_sources"] == []
    assert len(routed) == 15
    assert all(decision.action == "exclude" for decision in routed)
    assert plan["publish"][0]["source"] == "test"


def test_more_than_15_blank_actions_isolates_source_not_whole_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    review_items = tuple(item(source_job_id=f"job-{index}") for index in range(16))
    source = result_many(review_items)
    path = tmp_path / "ontap-daily-review.md"
    path.write_text(
        master_review.master_text([source], today=TODAY, previous=path),
        encoding="utf-8",
    )
    routed = []
    monkeypatch.setattr(master_review, "load_all_sources", lambda today: [source])
    monkeypatch.setattr(master_review, "_route_action", routed.append)

    plan = master_review.apply_master(
        path,
        today=TODAY,
        write=True,
        require_complete=True,
    )

    assert plan["quarantined"] == 0
    assert plan["isolated_sources"] == ["test"]
    assert plan["publish"] == []
    assert routed == []


def test_automatic_withhold_keeps_large_blank_queue_publishable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    review_items = tuple(item(source_job_id=f"job-{index}") for index in range(20))
    source = result_many(review_items)
    path = tmp_path / "ontap-daily-review.md"
    path.write_text(
        master_review.master_text([source], today=TODAY, previous=path),
        encoding="utf-8",
    )
    routed = []
    monkeypatch.setattr(master_review, "load_all_sources", lambda today: [source])
    monkeypatch.setattr(master_review, "_route_action", routed.append)

    plan = master_review.apply_master(
        path,
        today=TODAY,
        write=True,
        unresolved_policy="withhold",
    )

    assert plan["unresolved_policy"] == "withhold"
    assert plan["withheld"] == 20
    assert plan["quarantined"] == 0
    assert plan["isolated_sources"] == []
    assert plan["complete"] is False
    assert plan["publish"][0]["source"] == "test"
    assert routed == []


def test_automatic_withhold_still_isolates_changed_review_facts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "ontap-daily-review.md"
    text = master_review.master_text([result(item())], today=TODAY, previous=path)
    path.write_text(text.replace("action:\n", "action: select\n", 1), encoding="utf-8")
    monkeypatch.setattr(
        master_review,
        "load_all_sources",
        lambda today: [result(item(title="Changed after review"))],
    )

    plan = master_review.apply_master(
        path,
        today=TODAY,
        unresolved_policy="withhold",
    )

    assert plan["isolated_sources"] == ["test"]
    assert plan["publish"] == []


def test_invalid_action_is_treated_as_job_level_quarantine(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = result(item())
    path = tmp_path / "ontap-daily-review.md"
    text = master_review.master_text([source], today=TODAY, previous=path)
    path.write_text(text.replace("action:\n", "action: exlcude\n", 1), encoding="utf-8")
    routed = []
    monkeypatch.setattr(master_review, "load_all_sources", lambda today: [source])
    monkeypatch.setattr(master_review, "_route_action", routed.append)

    plan = master_review.apply_master(path, today=TODAY, write=True, require_complete=True)

    assert plan["quarantined"] == 1
    assert routed[0].action == "exclude"


def test_apply_isolates_source_when_vacancy_changed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "ontap-daily-review.md"
    text = master_review.master_text([result(item())], today=TODAY, previous=path)
    path.write_text(text.replace("action:\n", "action: exclude\n", 1), encoding="utf-8")
    monkeypatch.setattr(
        master_review,
        "load_all_sources",
        lambda today: [result(item(title="Changed after review"))],
    )

    plan = master_review.apply_master(path, today=TODAY, write=False)
    assert plan["isolated_sources"] == ["test"]
    assert plan["publish"] == []


def test_patch_action_changes_only_matching_block(tmp_path: Path) -> None:
    path = tmp_path / "review.md"
    path.write_text(
        "---\naction:\njob_id: one\n---\n\n"
        "---\naction:\njob_id: two\n---\n",
        encoding="utf-8",
    )
    master_review._patch_action(path, "job_id", "two", "exclude")
    text = path.read_text(encoding="utf-8")
    assert "action:\njob_id: one" in text
    assert "action: exclude\njob_id: two" in text
