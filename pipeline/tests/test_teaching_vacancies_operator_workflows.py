from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REVIEW_WORKFLOW = (
    REPO_ROOT / ".github/workflows/run-teaching-vacancies-regional-review.yml"
)
APPROVAL_WORKFLOW = (
    REPO_ROOT / ".github/workflows/build-approved-teaching-vacancies-regional.yml"
)
LEGACY_REVIEW = REPO_ROOT / ".github/workflows/run-teaching-vacancies-review.yml"
LEGACY_APPROVAL = (
    REPO_ROOT / ".github/workflows/build-approved-teaching-vacancies-output.yml"
)


def test_regional_review_workflow_is_review_only_and_complete() -> None:
    text = REVIEW_WORKFLOW.read_text(encoding="utf-8")
    commands = (
        "external_sources.teaching_vacancies_discovery",
        "external_sources.teaching_vacancies_routing",
        "external_sources.teaching_vacancies_regional_review",
    )
    positions = [text.index(command) for command in commands]
    assert positions == sorted(positions)
    assert "git diff --exit-code --" in text
    assert "pipeline/output-external" in text
    assert "pipeline/output-admin-service" in text
    assert "app" in text
    assert "teaching_vacancies_regional_approved" not in text
    assert "compose_teaching_vacancies_regional --write" not in text


def test_regional_approval_workflow_is_live_gated_and_region_scoped() -> None:
    text = APPROVAL_WORKFLOW.read_text(encoding="utf-8")
    assert 'if [ "$APPROVAL" != "PUBLISH" ]' in text
    assert "publishable_region" in text
    assert "teaching_vacancies_regional_approved" in text
    assert "compose_teaching_vacancies_regional" in text
    assert '--region "$REGION"' in text
    assert "expected one current base output" in text
    assert "combined regional output is external-only" in text
    assert "git diff --exit-code -- app" in text


def test_legacy_west_operator_workflows_remain_for_rollback() -> None:
    assert LEGACY_REVIEW.is_file()
    assert LEGACY_APPROVAL.is_file()
    assert "West Yorkshire" in LEGACY_REVIEW.read_text(encoding="utf-8")
    assert "compose_west_yorkshire_admin --write" in LEGACY_APPROVAL.read_text(
        encoding="utf-8"
    )
