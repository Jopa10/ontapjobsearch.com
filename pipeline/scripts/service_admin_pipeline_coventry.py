"""Run the live service-admin pipeline with Coventry & Warwickshire enabled."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from . import service_admin_pipeline_sussex as live

REGION = "West Midlands - Coventry & Warwickshire"
ANCHOR_TOWN = "Coventry"
OUTPUT_FILE = "coventry-warwickshire-admin-service.json"

# The Compiler 2 region label is the authoritative pipeline region. Keep a few
# normalised aliases so the same slice remains stable if a lookup label is
# shortened later.
live.core.REGION_MAP.update(
    {
        "west midlands - coventry & warwickshire": REGION,
        "coventry & warwickshire": REGION,
        "coventry warwickshire": REGION,
    }
)
live.core.OUTPUT_FILES[REGION] = OUTPUT_FILE
live.core.PUBLISH_THRESHOLDS[REGION] = 6

_ORIGINAL_LOAD_ANCHOR_TOWNS = live.core.load_anchor_towns
_ORIGINAL_MANUAL_REVIEW_PREVIEW = live.core._manual_review_preview_rows
_ORIGINAL_WRITE_MANUAL_REVIEW_MARKDOWN = live.core.write_manual_review_markdown


def load_anchor_towns(path: Path, category: str) -> dict[str, str]:
    """Add Coventry without requiring a binary workbook edit for activation."""
    output_file = live.core.OUTPUT_FILES.pop(REGION, None)
    try:
        anchors = _ORIGINAL_LOAD_ANCHOR_TOWNS(path, category)
    finally:
        if output_file is not None:
            live.core.OUTPUT_FILES[REGION] = output_file

    anchors[REGION] = ANCHOR_TOWN
    return anchors


def _manual_review_preview_rows(
    rows: list[dict[str, Any]],
    preserved_action_rows: list[dict[str, str]] | None = None,
) -> list[dict[str, Any]]:
    """Include Coventry & Warwickshire selected and possible rows in review."""
    preview_rows = _ORIGINAL_MANUAL_REVIEW_PREVIEW(rows, preserved_action_rows)
    seen = {live.core._markdown_value(row.get("job_id")) for row in preview_rows}

    for status in ("SELECTED", "POSSIBLE_SELECTION"):
        for row in live.core._markdown_review_rows(rows, REGION, status):
            job_id = live.core._markdown_value(row.get("job_id"))
            if job_id and job_id not in seen:
                preview_rows.append(row)
                seen.add(job_id)

    return preview_rows


def _coventry_markdown_sections(
    rows: list[dict[str, Any]],
    preserved_actions: dict[str, str],
) -> list[str]:
    lines: list[str] = []
    emitted: set[str] = set()
    groups = [
        ("COVENTRY & WARWICKSHIRE — SELECTED", "SELECTED", "SELECTED"),
        ("COVENTRY & WARWICKSHIRE — POSSIBLES", "POSSIBLE_SELECTION", "POSS"),
    ]

    for heading, status, decision_label in groups:
        lines.extend([f"## {heading}", ""])
        review_rows = [
            row
            for row in live.core._markdown_review_rows(rows, REGION, status)
            if live.core._markdown_value(row.get("job_id"))
            and live.core._markdown_value(row.get("job_id")) not in emitted
        ]
        if not review_rows:
            lines.extend(["_No jobs in this group._", ""])
            continue

        for row in review_rows:
            job_id = live.core._markdown_value(row.get("job_id"))
            emitted.add(job_id)
            action = preserved_actions.get(job_id, "")
            review_label = decision_label if decision_label != "POSS" else "POSS - COVENTRY & WARWICKSHIRE"
            summary = " | ".join(
                [
                    review_label,
                    live.core._markdown_value(row.get("region")),
                    live.core._markdown_value(row.get("town")),
                    live.core._markdown_value(row.get("salary_text")),
                    live.core._markdown_value(row.get("title")),
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
    """Append Coventry & Warwickshire review blocks to the established file."""
    preserved_actions = preserved_actions or {}
    non_coventry_rows = [row for row in rows if str(row.get("region", "")) != REGION]
    non_coventry_action_rows = [
        row
        for row in (preserved_action_rows or [])
        if str(row.get("region", "")) != REGION
    ]

    _ORIGINAL_WRITE_MANUAL_REVIEW_MARKDOWN(
        path,
        non_coventry_rows,
        preserved_actions,
        non_coventry_action_rows,
    )

    marker = "## ACTIVE MANUAL ACTIONS\n"
    content = path.read_text(encoding="utf-8")
    if marker not in content:
        raise RuntimeError("Service-admin review Markdown is missing the active-actions marker")

    sections = "\n".join(_coventry_markdown_sections(rows, preserved_actions))
    path.write_text(content.replace(marker, sections + marker, 1), encoding="utf-8")


live.core.load_anchor_towns = load_anchor_towns
live.core._manual_review_preview_rows = _manual_review_preview_rows
live.core.write_manual_review_markdown = write_manual_review_markdown


def main() -> int:
    return live.main()


if __name__ == "__main__":
    raise SystemExit(main())
