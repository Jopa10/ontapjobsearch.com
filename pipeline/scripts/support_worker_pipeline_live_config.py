"""Run support-worker selection using every LIVE support-worker slice.

This keeps the established support-worker selector as the source of truth while
allowing later regions to be activated through the central slice register and
catalog. Existing regions retain their established behaviour; additional LIVE
regions receive the same selection, salary, review and publish-threshold rules.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from . import support_worker_pipeline as core
from .slice_catalog import anchor_town, output_filename
from .slice_registry import live_slices

CATEGORY = "support_worker"
LIVE_REGIONS = sorted(region for region, category in live_slices() if category == CATEGORY)
EXTRA_REGIONS = [region for region in LIVE_REGIONS if region not in core.OUTPUT_FILES]

for region in EXTRA_REGIONS:
    core.REGION_MAP[core.norm_key(region)] = region
    core.OUTPUT_FILES[region] = output_filename(region, CATEGORY)
    core.PUBLISH_THRESHOLDS[region] = 6
    core.PUBLISH_REGION_BY_DETAIL_REGION[region] = region

_ORIGINAL_LOAD_ANCHOR_TOWNS = core.load_anchor_towns
_ORIGINAL_MANUAL_REVIEW_PREVIEW = core._manual_review_preview_rows
_ORIGINAL_WRITE_MANUAL_REVIEW_MARKDOWN = core.write_manual_review_markdown
_ORIGINAL_DECISION_REPORT_SORT_KEY = core.decision_report_sort_key


def load_anchor_towns(path: Path, category: str) -> dict[str, str]:
    """Reuse the established anchor sheet and add catalog anchors for new regions."""
    removed: dict[str, str] = {}
    for region in EXTRA_REGIONS:
        value = core.OUTPUT_FILES.pop(region, None)
        if value is not None:
            removed[region] = value
    try:
        anchors = _ORIGINAL_LOAD_ANCHOR_TOWNS(path, category)
    finally:
        core.OUTPUT_FILES.update(removed)

    for region in EXTRA_REGIONS:
        anchors[region] = anchor_town(region)
    return anchors


def _manual_review_preview_rows(
    rows: list[dict[str, Any]],
    preserved_action_rows: list[dict[str, str]] | None = None,
) -> list[dict[str, Any]]:
    preview_rows = _ORIGINAL_MANUAL_REVIEW_PREVIEW(rows, preserved_action_rows)
    seen = {core._markdown_value(row.get("job_id")) for row in preview_rows}
    for region in EXTRA_REGIONS:
        for status in ("SELECTED", "POSSIBLE_SELECTION"):
            for row in core._markdown_review_rows(rows, region, status):
                job_id = core._markdown_value(row.get("job_id"))
                if job_id and job_id not in seen:
                    preview_rows.append(row)
                    seen.add(job_id)
    return preview_rows


def _extra_markdown_sections(
    rows: list[dict[str, Any]],
    preserved_actions: dict[str, str],
) -> str:
    lines: list[str] = []
    for region in EXTRA_REGIONS:
        label = region.upper()
        for heading_suffix, status, decision_label in (
            ("SELECTED", "SELECTED", "SELECTED"),
            ("POSSIBLES", "POSSIBLE_SELECTION", "POSS"),
        ):
            lines.extend([f"## {label} — {heading_suffix}", ""])
            group_rows = core._markdown_review_rows(rows, region, status)
            if not group_rows:
                lines.extend(["_No jobs in this group._", ""])
                continue
            for row in group_rows:
                job_id = core._markdown_value(row.get("job_id"))
                action = preserved_actions.get(job_id, "")
                review_label = decision_label if decision_label == "SELECTED" else core.possible_review_label(region)
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
    return "\n".join(lines)


def write_manual_review_markdown(
    path: Path,
    rows: list[dict[str, Any]],
    preserved_actions: dict[str, str] | None = None,
    preserved_action_rows: list[dict[str, str]] | None = None,
) -> None:
    preserved_actions = preserved_actions or {}
    _ORIGINAL_WRITE_MANUAL_REVIEW_MARKDOWN(
        path,
        rows,
        preserved_actions,
        preserved_action_rows,
    )
    extra_sections = _extra_markdown_sections(rows, preserved_actions)
    if extra_sections:
        content = path.read_text(encoding="utf-8")
        if content and not content.endswith("\n"):
            content += "\n"
        path.write_text(content + "\n" + extra_sections, encoding="utf-8")


def decision_report_sort_key(row: dict[str, Any]) -> tuple[int, int, int, int, str, str]:
    region = str(row.get("region", ""))
    if region not in EXTRA_REGIONS:
        return _ORIGINAL_DECISION_REPORT_SORT_KEY(row)

    status = str(row.get("selection_status", ""))
    if status not in {"SELECTED", "POSSIBLE_SELECTION"}:
        return _ORIGINAL_DECISION_REPORT_SORT_KEY(row)

    region_index = EXTRA_REGIONS.index(region)
    top_group = 100 + region_index * 2 + (1 if status == "POSSIBLE_SELECTION" else 0)
    return (
        top_group,
        int(row.get("possible_selection_rank") or 9999),
        int(row.get("excel_row") or 999999),
        region_index,
        str(row.get("town", "")),
        str(row.get("title", "")),
    )


core.load_anchor_towns = load_anchor_towns
core._manual_review_preview_rows = _manual_review_preview_rows
core.write_manual_review_markdown = write_manual_review_markdown
core.decision_report_sort_key = decision_report_sort_key


def main() -> int:
    from . import persistent_jobg8_review as persistence

    run = persistence.prepare("support_worker")
    try:
        return core.main()
    finally:
        persistence.finalize(run)


if __name__ == "__main__":
    raise SystemExit(main())
