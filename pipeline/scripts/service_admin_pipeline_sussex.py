"""Run the established service-admin pipeline with the approved Sussex slice enabled."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from . import service_admin_pipeline as core
from . import service_admin_pipeline_education as education

core.REGION_MAP["sussex"] = "Sussex"
core.OUTPUT_FILES["Sussex"] = "sussex-admin-service.json"
core.PUBLISH_THRESHOLDS["Sussex"] = 6

_ORIGINAL_MANUAL_REVIEW_PREVIEW = core._manual_review_preview_rows
_ORIGINAL_WRITE_MANUAL_REVIEW_MARKDOWN = core.write_manual_review_markdown


def _manual_review_preview_rows(
    rows: list[dict[str, Any]],
    preserved_action_rows: list[dict[str, str]] | None = None,
) -> list[dict[str, Any]]:
    """Include Sussex selected and possible rows in the compact review preview."""
    preview_rows = _ORIGINAL_MANUAL_REVIEW_PREVIEW(rows, preserved_action_rows)
    seen = {core._markdown_value(row.get("job_id")) for row in preview_rows}

    for status in ("SELECTED", "POSSIBLE_SELECTION"):
        for row in core._markdown_review_rows(rows, "Sussex", status):
            job_id = core._markdown_value(row.get("job_id"))
            if job_id and job_id not in seen:
                preview_rows.append(row)
                seen.add(job_id)

    return preview_rows


def _sussex_markdown_sections(
    rows: list[dict[str, Any]],
    preserved_actions: dict[str, str],
) -> list[str]:
    lines: list[str] = []
    emitted: set[str] = set()
    groups = [
        ("SUSSEX — SELECTED", "SELECTED", "SELECTED"),
        ("SUSSEX — POSSIBLES", "POSSIBLE_SELECTION", "POSS"),
    ]

    for heading, status, decision_label in groups:
        lines.extend([f"## {heading}", ""])
        review_rows = [
            row
            for row in core._markdown_review_rows(rows, "Sussex", status)
            if core._markdown_value(row.get("job_id"))
            and core._markdown_value(row.get("job_id")) not in emitted
        ]
        if not review_rows:
            lines.extend(["_No jobs in this group._", ""])
            continue

        for row in review_rows:
            job_id = core._markdown_value(row.get("job_id"))
            emitted.add(job_id)
            action = preserved_actions.get(job_id, "")
            review_label = decision_label if decision_label != "POSS" else "POSS - SUSSEX"
            summary = " | ".join(
                [
                    review_label,
                    core._markdown_value(row.get("region")),
                    core._markdown_value(row.get("town")),
                    core._markdown_value(row.get("salary_text")),
                    core._markdown_value(row.get("title")),
                ]
            )
            lines.extend(
                [
                    "---",
                    f"action: {action}" if action else "action:",
                    summary,
                    f"job_id: {job_id}",
                    "---",
                    "",
                ]
            )

    return lines


def write_manual_review_markdown(
    path: Path,
    rows: list[dict[str, Any]],
    preserved_actions: dict[str, str] | None = None,
    preserved_action_rows: list[dict[str, str]] | None = None,
) -> None:
    """Add Sussex review blocks without changing the established core formatter."""
    preserved_actions = preserved_actions or {}
    non_sussex_rows = [row for row in rows if str(row.get("region", "")) != "Sussex"]
    non_sussex_action_rows = [
        row
        for row in (preserved_action_rows or [])
        if str(row.get("region", "")) != "Sussex"
    ]

    _ORIGINAL_WRITE_MANUAL_REVIEW_MARKDOWN(
        path,
        non_sussex_rows,
        preserved_actions,
        non_sussex_action_rows,
    )

    marker = "## ACTIVE MANUAL ACTIONS\n"
    content = path.read_text(encoding="utf-8")
    if marker not in content:
        raise RuntimeError("Service-admin review Markdown is missing the active-actions marker")

    sussex_sections = "\n".join(_sussex_markdown_sections(rows, preserved_actions))
    path.write_text(
        content.replace(marker, sussex_sections + marker, 1),
        encoding="utf-8",
    )


core._manual_review_preview_rows = _manual_review_preview_rows
core.write_manual_review_markdown = write_manual_review_markdown


def main() -> int:
    return education.main()


if __name__ == "__main__":
    raise SystemExit(main())
