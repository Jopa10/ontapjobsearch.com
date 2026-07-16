"""Education-aware entry point for the existing service-admin pipeline.

Education is a sector, not a job function. This module makes the narrow
classification exception required for genuine school/education office roles,
adds verified hybrid-working metadata after normal service-admin eligibility,
then delegates every other rule and all processing to service_admin_pipeline.
"""
from __future__ import annotations

import re
from typing import Any

from . import service_admin_pipeline as core

try:
    from pipeline.module3.working_arrangement import classify_working_arrangement
except ModuleNotFoundError:  # workflow runs with pipeline/ as the working directory
    from module3.working_arrangement import classify_working_arrangement

_ORIGINAL_CLASSIFY_TITLE = core.classify_title
_ORIGINAL_PROCESS = core.process
_ORIGINAL_DECISION_REPORT_FIELDNAMES = core.decision_report_fieldnames

_HYBRID_FIELDS = [
    "working_arrangement",
    "working_arrangement_text",
    "working_arrangement_evidence",
]

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


def process(*args: Any, **kwargs: Any):
    outputs, report_rows = _ORIGINAL_PROCESS(*args, **kwargs)
    metadata_by_job_id: dict[str, dict[str, str]] = {}
    for jobs in outputs.values():
        for item in jobs:
            metadata = classify_working_arrangement(
                str(item.get("title", "")),
                str(item.get("description", "")),
                str(item.get("location", "")),
                str(item.get("region", "")),
            ).as_dict()
            item.update(metadata)
            job_id = core.norm(item.get("job_id", ""))
            if job_id:
                metadata_by_job_id[job_id] = metadata
    for row in report_rows:
        metadata = metadata_by_job_id.get(core.norm(row.get("job_id", "")))
        if metadata:
            row.update(metadata)
        else:
            for field in _HYBRID_FIELDS:
                row.setdefault(field, "")
    return outputs, report_rows


def decision_report_fieldnames() -> list[str]:
    fields = list(_ORIGINAL_DECISION_REPORT_FIELDNAMES())
    insert_at = fields.index("employment_type") + 1
    for field in reversed(_HYBRID_FIELDS):
        if field not in fields:
            fields.insert(insert_at, field)
    return fields


# Add Hampshire through the existing core pipeline configuration. Geography and
# anchor-town values still come from the authoritative geo workbook.
core.REGION_MAP["hampshire"] = "Hampshire"
core.OUTPUT_FILES["Hampshire"] = "hampshire-admin-service.json"
core.PUBLISH_THRESHOLDS["Hampshire"] = 6

core.classify_title = classify_title
core.process = process
core.decision_report_fieldnames = decision_report_fieldnames

_manual_insert_at = core.MANUAL_REVIEW_FIELDNAMES.index("manual_override")
for _field in reversed(_HYBRID_FIELDS):
    if _field not in core.MANUAL_REVIEW_FIELDNAMES:
        core.MANUAL_REVIEW_FIELDNAMES.insert(_manual_insert_at, _field)


def main() -> int:
    return core.main()


if __name__ == "__main__":
    raise SystemExit(main())
