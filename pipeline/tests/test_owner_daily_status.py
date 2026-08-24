from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path

from review_hub.contracts import SourceResult
from scripts import owner_daily_status as status


TODAY = date(2026, 8, 24)
NOW = datetime(2026, 8, 24, 11, 20, tzinfo=timezone.utc)
REPO_ROOT = Path(__file__).resolve().parents[2]


def source_results() -> list[SourceResult]:
    return [
        SourceResult(key, label, "OK", TODAY.isoformat())
        for key, label in (
            ("jobg8", "JobG8"),
            ("teaching_vacancies", "Teaching Vacancies"),
            ("nhs", "NHS Jobs"),
            ("nejobs", "NEJobs"),
            ("vonne", "VONNE"),
        )
    ]


def run(
    workflow: str,
    minute: int,
    *,
    event: str = "workflow_dispatch",
    conclusion: str = "success",
) -> status.Run:
    created = datetime(2026, 8, 24, 10, minute, tzinfo=timezone.utc)
    return status.Run(
        workflow=workflow,
        event=event,
        status="completed" if conclusion else "in_progress",
        conclusion=conclusion,
        created_at=created,
        updated_at=created,
        url=f"https://example.test/{workflow}/{minute}",
    )


def evidence(tmp_path: Path) -> tuple[Path, Path]:
    review = tmp_path / "ontap-daily-review.md"
    review.write_text(
        "# Review\n\n> **READY TO REVIEW**\n\nreview_date: 2026-08-24\n",
        encoding="utf-8",
    )
    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "live-job-source-count-2026-08-24.csv").write_text(
        "report_date,level,source,region,category,count\n"
        "2026-08-24,total,All,,,1775\n",
        encoding="utf-8",
    )
    return review, reports


def completed_runs(*, automatic: bool = False) -> list[status.Run]:
    apply = run(
        status.APPLY_WORKFLOW,
        0,
        event="schedule" if automatic else "workflow_dispatch",
    )
    children = [
        run(workflow, index + 1)
        for index, workflow in enumerate(status.SOURCE_PUBLISHERS)
    ]
    return children + [
        apply,
        run(status.VERIFIED_WORKFLOW, 10),
        run(status.DEPLOY_WORKFLOW, 15, event="workflow_run"),
    ]


def build(tmp_path: Path, runs: list[status.Run], **kwargs: object) -> status.DailyStatus:
    review, reports = evidence(tmp_path)
    return status.build_status(
        today=TODAY,
        now=NOW,
        runs=runs,
        source_results=source_results(),
        master_review=review,
        reports_dir=reports,
        require_publish=bool(kwargs.get("require_publish", True)),
    )


def test_complete_manual_cycle_is_one_green_owner_status(tmp_path: Path) -> None:
    result = build(tmp_path, completed_runs())

    assert result.ready is True
    assert result.publish_state == "PUBLISHED SUCCESSFULLY"
    assert result.publish_mode == "MANUAL"
    assert result.exit_code == 0
    assert "READY TO EDIT — YES" in result.markdown
    assert "manual review published" in result.markdown


def test_complete_automatic_cycle_explains_1145_reason(tmp_path: Path) -> None:
    result = build(tmp_path, completed_runs(automatic=True))

    assert result.publish_mode == "AUTOMATIC"
    assert result.exit_code == 0
    assert "no successful manual publish was recorded before 11:45" in result.markdown


def test_failed_source_is_visible_even_when_final_deployment_succeeds(
    tmp_path: Path,
) -> None:
    runs = completed_runs()
    failed_name = status.SOURCE_PUBLISHERS[2]
    runs = [item for item in runs if item.workflow != failed_name]
    runs.append(run(failed_name, 6, conclusion="failure"))

    result = build(tmp_path, runs)

    assert result.publish_state == "PUBLISHED WITH SOURCE HELD"
    assert result.exit_code == 1
    assert "production updated" in result.markdown
    assert "**FAILURE**" in result.markdown


def test_morning_status_can_be_green_before_publication(tmp_path: Path) -> None:
    result = build(tmp_path, [], require_publish=False)

    assert result.ready is True
    assert result.publish_state == "NOT YET PUBLISHED"
    assert result.exit_code == 0


def test_stale_source_makes_ready_to_edit_no(tmp_path: Path) -> None:
    review, reports = evidence(tmp_path)
    sources = source_results()
    sources[1] = SourceResult(
        "teaching_vacancies",
        "Teaching Vacancies",
        "STALE",
        "2026-08-23",
    )

    result = status.build_status(
        today=TODAY,
        now=NOW,
        runs=[],
        source_results=sources,
        master_review=review,
        reports_dir=reports,
        require_publish=False,
    )

    assert result.ready is False
    assert result.exit_code == 1
    assert "READY TO EDIT — NO" in result.markdown
    assert "Teaching Vacancies fetch | **NOT READY**" in result.markdown


def test_owner_workflow_runs_at_both_checkpoints_and_after_key_events() -> None:
    workflow = (
        REPO_ROOT / ".github/workflows/ontap-daily-status.yml"
    ).read_text(encoding="utf-8")

    assert "name: Ontap daily status" in workflow
    assert 'cron: "15 9 * * *"' in workflow
    assert 'cron: "15 12 * * *"' in workflow
    assert "- Ontap daily review" in workflow
    assert "- Deploy Ontap production after publish" in workflow
    for publisher in (
        "run-full-jobg8-daily-process.yml",
        "run-teaching-vacancies-regional-review.yml",
        "refresh-nhs-admin-service-review.yml",
        "run-nejobs-review.yml",
        "run-vonne-review.yml",
        "ontap-daily-review.yml",
        "apply-publish-ontap-daily-review.yml",
        "apply-jobg8-review-decisions.yml",
        "build-approved-nejobs-output.yml",
        "build-approved-vonne-output.yml",
        "publish-reviewed-teaching-vacancies-england.yml",
        "publish-reviewed-nhs-admin-service.yml",
        "publish-verified-pages.yml",
        "deploy-vercel-after-publish.yml",
    ):
        assert publisher in workflow
