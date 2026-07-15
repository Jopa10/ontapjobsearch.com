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
    """Classify education-sector office roles before the legacy school hard-pass.

    Specialist/non-admin education functions remain hard passes, even when an
    admin word also appears. Clear education-sector office functions become
    HIGH_CONFIDENCE. Everything else delegates unchanged to the existing
    classifier, preserving specialist, senior, register and review behaviour.
    """
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


# process() resolves classify_title from the core module at runtime. Replacing
# that single global keeps the rest of the 2,000+ line pipeline unchanged.
core.classify_title = classify_title


def main() -> int:
    return core.main()


if __name__ == "__main__":
    raise SystemExit(main())
