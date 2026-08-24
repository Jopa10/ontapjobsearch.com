"""Run service-admin using every LIVE admin slice from the slice register.

This wraps the established Sussex/Coventry chain rather than replacing its
selection logic. North Yorkshire and all later regions are added from the
central slice register/catalog. Finance and Customer Service keep their audited
title-register selector; HR / Recruitment, Customer Sales, Legal Assistant /
Paralegal and Marketing then use their separately frozen family boundaries
against the same current JobG8 input and explicit LIVE register gate.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from . import service_admin_pipeline_coventry as established
from .slice_catalog import anchor_town, output_filename
from .slice_registry import live_slices

# Coventry -> Sussex -> guarded service_admin_pipeline proxy.
core = established.live.core
CATEGORY = "admin_service"

LIVE_REGIONS = sorted(region for region, category in live_slices() if category == CATEGORY)
EXTRA_REGIONS = [region for region in LIVE_REGIONS if region not in core.OUTPUT_FILES]

for region in EXTRA_REGIONS:
    core.REGION_MAP[core.norm_key(region)] = region
    core.OUTPUT_FILES[region] = output_filename(region, CATEGORY)
    core.PUBLISH_THRESHOLDS[region] = 6

# Retain the common North Yorkshire aliases previously supplied by the dedicated wrapper.
if "Yorkshire - North" in LIVE_REGIONS:
    core.REGION_MAP.update({"yorkshire - north": "Yorkshire - North", "yorkshire north": "Yorkshire - North", "north yorkshire": "Yorkshire - North"})

_ORIGINAL_LOAD_ANCHOR_TOWNS = core.load_anchor_towns
_ORIGINAL_MANUAL_REVIEW_PREVIEW = core._manual_review_preview_rows
_ORIGINAL_WRITE_MANUAL_REVIEW_MARKDOWN = core.write_manual_review_markdown


def load_anchor_towns(path: Path, category: str) -> dict[str, str]:
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


def _manual_review_preview_rows(rows: list[dict[str, Any]], preserved_action_rows: list[dict[str, str]] | None = None) -> list[dict[str, Any]]:
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


def _extra_markdown_sections(rows: list[dict[str, Any]], preserved_actions: dict[str, str]) -> list[str]:
    lines: list[str] = []
    emitted: set[str] = set()
    for region in EXTRA_REGIONS:
        label = region.upper()
        for heading_suffix, status, decision_label in (("SELECTED", "SELECTED", "SELECTED"), ("POSSIBLES", "POSSIBLE_SELECTION", "POSS")):
            lines.extend([f"## {label} — {heading_suffix}", ""])
            group_rows = [row for row in core._markdown_review_rows(rows, region, status) if core._markdown_value(row.get("job_id")) and core._markdown_value(row.get("job_id")) not in emitted]
            if not group_rows:
                lines.extend(["_No jobs in this group._", ""])
                continue
            for row in group_rows:
                job_id = core._markdown_value(row.get("job_id"))
                emitted.add(job_id)
                action = preserved_actions.get(job_id, "")
                review_label = decision_label if decision_label == "SELECTED" else f"POSS - {label}"
                summary = " | ".join([review_label, core._markdown_value(row.get("region")), core._markdown_value(row.get("town")), core._markdown_value(row.get("salary_text")), core._markdown_value(row.get("title"))])
                lines.extend(["---", f"action: {action}" if action else "action:", summary, f"job_id: {job_id}", "---", ""])
    return lines


def write_manual_review_markdown(path: Path, rows: list[dict[str, Any]], preserved_actions: dict[str, str] | None = None, preserved_action_rows: list[dict[str, str]] | None = None) -> None:
    preserved_actions = preserved_actions or {}
    extras = set(EXTRA_REGIONS)
    base_rows = [row for row in rows if str(row.get("region", "")) not in extras]
    base_action_rows = [row for row in (preserved_action_rows or []) if str(row.get("region", "")) not in extras]
    _ORIGINAL_WRITE_MANUAL_REVIEW_MARKDOWN(path, base_rows, preserved_actions, base_action_rows)
    marker = "## ACTIVE MANUAL ACTIONS\n"
    content = path.read_text(encoding="utf-8")
    if marker not in content:
        raise RuntimeError("Service-admin review Markdown is missing the active-actions marker")
    sections = "\n".join(_extra_markdown_sections(rows, preserved_actions))
    if sections:
        content = content.replace(marker, sections + marker, 1)
    path.write_text(content, encoding="utf-8")


core.load_anchor_towns = load_anchor_towns
core._manual_review_preview_rows = _manual_review_preview_rows
core.write_manual_review_markdown = write_manual_review_markdown


def main() -> int:
    result = established.main()
    if result:
        return result
    from .registered_category_pipeline import run_live_registered_categories
    result = run_live_registered_categories()
    if result:
        return result
    from .hr_recruitment_pipeline import main as run_live_hr_recruitment
    result = run_live_hr_recruitment()
    if result:
        return result
    from .customer_sales_pipeline import main as run_live_customer_sales
    result = run_live_customer_sales()
    if result:
        return result
    from .customer_sales_production_refine import main as refine_live_customer_sales
    result = refine_live_customer_sales()
    if result:
        return result
    from .legal_assistant_pipeline import main as run_live_legal_assistant
    result = run_live_legal_assistant()
    if result:
        return result
    from .marketing_pipeline import main as run_live_marketing
    return run_live_marketing()


if __name__ == "__main__":
    raise SystemExit(main())
