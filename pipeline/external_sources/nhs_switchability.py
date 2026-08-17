"""Pure NHS switchability rules shared by the review-only NHS ETL.

This module does not fetch, publish or compose vacancies. It only classifies an
already-normalised NHS vacancy so the NHS review feed can use the same HC/POSS/
HARD_PASS discipline as the rest of Ontap.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalise(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).casefold()).strip()


ADMIN_SERVICE = "admin_service"
SUPPORT_WORKER = "support_worker"

SUPPORT_TITLE_TERMS = (
    "support worker",
    "healthcare support worker",
    "health care support worker",
    "healthcare assistant",
    "health care assistant",
    "care assistant",
    "care worker",
)

# These titles can still contain the word "support" but are not ordinary
# support-worker inventory for Ontap.
SUPPORT_HARD_TITLE_TERMS = (
    "senior",
    "lead",
    "team leader",
    "manager",
    "coordinator",
    "co-ordinator",
    "registered nurse",
    "nursing associate",
    "assistant practitioner",
    "therapist",
    "occupational therapist",
    "physiotherapist",
    "social worker",
    "psychologist",
)

# A specialist context does not automatically reject the role, but it must not
# auto-clear as an open switch purely because the title says Support Worker.
SUPPORT_CONTEXT_REVIEW_TERMS = (
    "mental health",
    "learning disability",
    "learning disabilities",
    "autism",
    "forensic",
    "rehabilitation",
    "recovery",
    "community",
    "maternity",
    "paediatric",
    "pediatric",
)

NHS_EXPERIENCE_ESSENTIAL_PATTERNS = (
    r"(?:essential|required|must have|you will need)[^.]{0,80}\bnhs experience\b",
    r"\bprevious nhs experience (?:is )?(?:essential|required)\b",
    r"\bexperience (?:of|within|in) the nhs (?:is )?(?:essential|required)\b",
)

HEALTHCARE_EXPERIENCE_ESSENTIAL_PATTERNS = (
    r"(?:essential|required|must have|you will need)[^.]{0,100}\b(?:healthcare|health care|care) experience\b",
    r"\bprevious (?:healthcare|health care|care) experience (?:is )?(?:essential|required)\b",
    r"\bexperience (?:in|within) (?:a )?(?:healthcare|health care|care) setting (?:is )?(?:essential|required)\b",
)

HARD_REQUIREMENT_PATTERNS = (
    r"\bregistered (?:nurse|professional)\b",
    r"\bnmc registration\b",
    r"\bhcpc registration\b",
    r"\bprofessional registration\b",
    r"\bnvq level [34]\b",
    r"\bcare certificate (?:is )?(?:essential|required)\b",
)

BRIDGEABLE_PATTERNS = (
    r"\btraining (?:will be|is) provided\b",
    r"\bfull training\b",
    r"\bno previous experience (?:is )?required\b",
    r"\bexperience (?:is )?desirable\b",
    r"\bexperience preferred\b",
    r"\bor equivalent experience\b",
)


@dataclass(frozen=True)
class NHSClassification:
    category: str
    final_decision: str
    switchability: str
    reason: str


def _matches_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def is_support_worker_title(title: object) -> bool:
    value = normalise(title)
    return any(normalise(term) in value for term in SUPPORT_TITLE_TERMS)


def classify_support_worker(title: object, criteria_text: object = "") -> NHSClassification:
    """Classify an NHS support-worker candidate for Ontap review.

    The title can nominate a job for the support-worker family, but it can never
    by itself prove OPEN_SWITCH. Essential requirements take precedence.
    """
    title_norm = normalise(title)
    criteria = clean(criteria_text)

    if not is_support_worker_title(title):
        return NHSClassification(
            SUPPORT_WORKER,
            "HARD_PASS",
            "OUT_OF_SCOPE",
            "Title is not in the NHS support-worker candidate family",
        )

    hard_title_hits = [
        term for term in SUPPORT_HARD_TITLE_TERMS if normalise(term) in title_norm
    ]
    if hard_title_hits:
        return NHSClassification(
            SUPPORT_WORKER,
            "HARD_PASS",
            "HARD_PASS",
            "Senior/qualified/specialist title: " + ", ".join(hard_title_hits),
        )

    if _matches_any(criteria, HARD_REQUIREMENT_PATTERNS):
        return NHSClassification(
            SUPPORT_WORKER,
            "HARD_PASS",
            "HARD_PASS",
            "Essential qualification/professional-registration barrier",
        )

    if _matches_any(criteria, NHS_EXPERIENCE_ESSENTIAL_PATTERNS):
        return NHSClassification(
            SUPPORT_WORKER,
            "POSS",
            "NHS_EXPERIENCED",
            "Previous NHS experience appears essential",
        )

    if _matches_any(criteria, HEALTHCARE_EXPERIENCE_ESSENTIAL_PATTERNS):
        return NHSClassification(
            SUPPORT_WORKER,
            "POSS",
            "HEALTHCARE_EXPERIENCED",
            "Previous healthcare/care experience appears essential",
        )

    specialist_hits = [
        term for term in SUPPORT_CONTEXT_REVIEW_TERMS if normalise(term) in title_norm
    ]
    if specialist_hits:
        return NHSClassification(
            SUPPORT_WORKER,
            "POSS",
            "BRIDGEABLE",
            "Specialist support context requires advert review: "
            + ", ".join(specialist_hits),
        )

    if criteria and _matches_any(criteria, BRIDGEABLE_PATTERNS):
        return NHSClassification(
            SUPPORT_WORKER,
            "HC",
            "OPEN_SWITCH",
            "Advert explicitly supports training, equivalent or non-essential experience",
        )

    # Safe default: a generic NHS support-worker title is a candidate, not proof
    # that a private-sector switcher can credibly apply today.
    return NHSClassification(
        SUPPORT_WORKER,
        "POSS",
        "BRIDGEABLE",
        "Generic NHS support-worker title; essential criteria still require review",
    )
