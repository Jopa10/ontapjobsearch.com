"""Education-aware entry point for the existing service-admin pipeline.

Education is a sector, not a job function. This module makes the narrow
classification exception required for genuine school/education office roles,
then delegates every other rule and all processing to service_admin_pipeline.
"""
from __future__ import annotations

import re
from typing import Any

from . import service_admin_pipeline as core

_ORIGINAL_CLASSIFY_TITLE = core.classify_title
_ORIGINAL_ANCHOR_SORT_AND_SELECT = core.anchor_sort_and_select

_EDUCATION_SECTOR_RE = re.compile(r"\b(?:school|academy|college|education)\b", re.IGNORECASE)

_EDUCATION_ADMIN_FUNCTION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("administrator", re.compile(r"\badministrator\b", re.IGNORECASE)),
    ("admin", re.compile(r"\badmin\b", re.IGNORECASE)),
    ("administration", re.compile(r"\badministration\b", re.IGNORECASE)),
    ("administrative", re.compile(r"\badministrative\b", re.IGNORECASE)),
    ("reception", re.compile(r"\breception(?:ist)?\b", re.IGNORECASE)),
    ("office manager", re.compile(r"\boffice manager\b", re.IGNORECASE)),
    ("office administrator", re.compile(r"\boffice administrator\b", re.IGNORECASE)),
    ("office assistant", re.compile(r"\boffice assistant\b", re.IGNORECASE)),
    ("attendance", re.compile(r"\battendance\b", re.IGNORECASE)),
    ("admissions", re.compile(r"\badmissions?\b", re.IGNORECASE)),
    ("records", re.compile(r"\brecords?\b", re.IGNORECASE)),
    ("data entry", re.compile(r"\bdata entry\b", re.IGNORECASE)),
    ("diary support", re.compile(r"\bdiary support\b", re.IGNORECASE)),
    ("business support", re.compile(r"\bbusiness support\b", re.IGNORECASE)),
    ("clerical", re.compile(r"\bclerical\b", re.IGNORECASE)),
    ("secretary", re.compile(r"\bsecretar(?:y|ial)\b", re.IGNORECASE)),
)

_NON_ADMIN_EDUCATION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("teacher", re.compile(r"\bteachers?\b", re.IGNORECASE)),
    ("teaching", re.compile(r"\bteaching\b", re.IGNORECASE)),
    ("teaching assistant", re.compile(r"\bteaching assistants?\b", re.IGNORECASE)),
    ("classroom assistant", re.compile(r"\bclassroom assistants?\b", re.IGNORECASE)),
    ("learning support", re.compile(r"\blearning[- ]support\b", re.IGNORECASE)),
    ("cover supervisor", re.compile(r"\bcover supervisors?\b", re.IGNORECASE)),
    ("tutor", re.compile(r"\btutors?\b", re.IGNORECASE)),
    ("lecturer", re.compile(r"\blecturers?\b", re.IGNORECASE)),
    ("pastoral", re.compile(r"\bpastoral\b", re.IGNORECASE)),
    ("behaviour support", re.compile(r"\bbehaviou?r[- ]support\b", re.IGNORECASE)),
    ("SEN", re.compile(r"\bSEN\b", re.IGNORECASE)),
    ("SEND", re.compile(r"\bSEND\b", re.IGNORECASE)),
    ("SEMH", re.compile(r"\bSEMH\b", re.IGNORECASE)),
    (
        "specialist education practitioner",
        re.compile(r"\bspecialist education practitioners?\b", re.IGNORECASE),
    ),
)


def _matching_labels(title: str, patterns: tuple[tuple[str, re.Pattern[str]], ...]) -> list[str]:
    return [label for label, pattern in patterns if pattern.search(title)]


def classify_title(
    title: str,
    title_register: dict[str, dict[str, str]] | None = None,
) -> tuple[str, str, int, str]:
    """Classify education-sector office roles before the legacy school hard-pass."""
    clean_title = core.norm(title)

    specialist_hits = _matching_labels(clean_title, _NON_ADMIN_EDUCATION_PATTERNS)
    if specialist_hits:
        classification = "HARD_PASS"
        return (
            classification,
            "non-admin education title pattern: " + ", ".join(specialist_hits),
            core.CLASSIFICATION_PRIORITY[classification],
            "STABLE",
        )

    if _EDUCATION_SECTOR_RE.search(clean_title):
        admin_hits = _matching_labels(clean_title, _EDUCATION_ADMIN_FUNCTION_PATTERNS)
        if admin_hits:
            classification = "HIGH_CONFIDENCE"
            return (
                classification,
                "education sector with office/admin function: " + ", ".join(admin_hits),
                core.CLASSIFICATION_PRIORITY[classification],
                "STABLE",
            )

    return _ORIGINAL_CLASSIFY_TITLE(title, title_register)


def anchor_sort_and_select(
    outputs: dict[str, list[dict[str, Any]]],
    report_rows: list[dict[str, Any]],
    manual_rerun_mode: bool = False,
    previously_selected_ids: set[str] | None = None,
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    """Apply manual rerun mode consistently to every configured region.

    The legacy selector only enters its manual branch when a region already has
    a SELECT/FORCE_INCLUDE action. During a global manual rerun that left regions
    without actions, notably London, on automatic full selection. A temporary
    guard item makes those regions enter the same manual branch; it is removed
    before outputs and reports are returned.
    """
    if not manual_rerun_mode:
        return _ORIGINAL_ANCHOR_SORT_AND_SELECT(
            outputs,
            report_rows,
            manual_rerun_mode=False,
            previously_selected_ids=previously_selected_ids,
        )

    guarded_outputs = {region: list(items) for region, items in outputs.items()}
    guard_ids: dict[str, str] = {}

    for region, items in guarded_outputs.items():
        has_manual_state = any(
            item.get("_manual_override") == "FORCE_INCLUDE"
            or str(item.get("_manual_select", "")).strip() == "1"
            for item in items
        )
        if has_manual_state:
            continue

        guard_id = f"__global_manual_rerun_guard__:{region}"
        guard_ids[region] = guard_id
        items.append({
            "job_id": guard_id,
            "location": core.ANCHOR_TOWNS[region],
            "_manual_override": "FORCE_INCLUDE",
            "_manual_select": "",
            "_title_priority": core.CLASSIFICATION_PRIORITY["HIGH_CONFIDENCE"],
            "_title_classification": "HIGH_CONFIDENCE",
            "_excel_row": 999999999,
        })

    final_outputs, region_status = _ORIGINAL_ANCHOR_SORT_AND_SELECT(
        guarded_outputs,
        report_rows,
        manual_rerun_mode=True,
        previously_selected_ids=previously_selected_ids,
    )

    for region, guard_id in guard_ids.items():
        final_outputs[region] = [
            item for item in final_outputs.get(region, [])
            if str(item.get("job_id", "")) != guard_id
        ]
        status = region_status[region]
        status["selected_count"] = len(final_outputs[region])
        status["credible_total"] = max(0, int(status["credible_total"]) - 1)
        status["high_confidence_count"] = max(0, int(status["high_confidence_count"]) - 1)
        status["message"] = (
            f"{region} manual rerun: 0 current-feed manual_select row(s) applied; "
            "0 selected. Auto backfill disabled."
        )
        for row in report_rows:
            if str(row.get("region", "")) == region:
                row["region_selection_message"] = status["message"]

    return final_outputs, region_status


# The core pipeline resolves these globals at runtime. Replacing only these two
# functions keeps all other classification, geo, deduplication and output rules unchanged.
core.classify_title = classify_title
core.anchor_sort_and_select = anchor_sort_and_select


def main() -> int:
    return core.main()


if __name__ == "__main__":
    raise SystemExit(main())
