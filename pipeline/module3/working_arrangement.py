"""Production metadata derived from the tested Module 3 remote-work classifier.

This module deliberately does not change Module 3's analytical classifications.
It maps credible hybrid/partial-remote decisions into the compact fields used by
Ontap's regional admin/service job JSON and job cards.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from .rules import SPLIT, classify_remote, clean_description, norm_text

QUALIFYING_CLASSIFICATION = "HYBRID_OR_PARTIAL_REMOTE"
NON_QUALIFYING_VALUE = "onsite_or_not_stated"

_NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
}
_NUMBER = r"(?:[1-5]|one|two|three|four|five)"

_UP_TO_HOME_DAYS_RE = re.compile(
    rf"\bup\s+to\s+(?P<number>{_NUMBER})\s+days?\s+(?:working\s+)?from\s+home\b",
    re.IGNORECASE,
)
_HOME_DAYS_RE = re.compile(
    rf"\b(?P<number>{_NUMBER})\s+days?\s+(?:working\s+)?from\s+home\b",
    re.IGNORECASE,
)
_HOME_DAYS_PER_WEEK_RE = re.compile(
    rf"\b(?:work(?:ing)?\s+from\s+home|home\s*working)\s+"
    rf"(?P<number>{_NUMBER})\s+days?\s+(?:a|per)\s+week\b",
    re.IGNORECASE,
)
_OFFICE_DAYS_RE = re.compile(
    rf"\b(?P<number>{_NUMBER})\s+days?\s+(?:in|at)\s+(?:the\s+)?office\b",
    re.IGNORECASE,
)
_OFFICE_DAYS_PER_WEEK_RE = re.compile(
    rf"\b(?P<number>{_NUMBER})\s+office\s+days?\s+(?:a|per)\s+week\b",
    re.IGNORECASE,
)
_WEEKDAY_HOME_RE = re.compile(
    r"\b(?P<day>monday|tuesday|wednesday|thursday|friday)s?\s+"
    r"(?:home\s*working|work(?:ing)?\s+from\s+home)\b",
    re.IGNORECASE,
)
_HOME_ON_WEEKDAY_RE = re.compile(
    r"\bwork(?:ing)?\s+from\s+home\s+(?:on\s+)?"
    r"(?P<day>monday|tuesday|wednesday|thursday|friday)s?\b",
    re.IGNORECASE,
)

# A narrow supplement for an explicit phrase named in the production brief but
# not currently covered by Module 3's analytical patterns. It is intentionally
# limited to wording that directly states a home/office working arrangement.
_EXPLICIT_HOME_OFFICE_RE = re.compile(
    r"\b(?:home\s+(?:and|&|/)\s+office[- ]based|"
    r"office\s+(?:and|&|/)\s+home[- ]based)\s+working\b",
    re.IGNORECASE,
)

# Production badges require an explicit home/remote/hybrid signal. This stricter
# gate prevents analytical phrases such as "regular office attendance" or
# "predominantly office-based" from creating a badge on their own.
_CREDIBLE_SIGNAL_RE = re.compile(
    r"\b(?:hybrid|remote\s+working|some\s+remote\s+working|"
    r"occasional\s+remote\s+working|home\s*working|"
    r"work(?:ing)?\s+from\s+home|home[- ]based)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class WorkingArrangementMetadata:
    working_arrangement: str
    working_arrangement_text: str
    working_arrangement_evidence: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def _number_value(raw: str) -> int:
    value = raw.casefold()
    return _NUMBER_WORDS.get(value, int(value) if value.isdigit() else 0)


def _days_label(number: int, noun: str = "days") -> str:
    if noun == "office days":
        return "office day" if number == 1 else "office days"
    return "day" if number == 1 else "days"


def _match_number(match: re.Match[str] | None) -> int | None:
    if not match:
        return None
    value = _number_value(match.group("number"))
    return value or None


def _exact_arrangement_text(text: str) -> str:
    up_to_home = _UP_TO_HOME_DAYS_RE.search(text)
    if up_to_home:
        home_days = _match_number(up_to_home)
        if home_days is not None:
            return f"Up to {home_days} {_days_label(home_days)} from home"

    home_match = _HOME_DAYS_RE.search(text) or _HOME_DAYS_PER_WEEK_RE.search(text)
    office_match = _OFFICE_DAYS_RE.search(text)
    home_days = _match_number(home_match)
    office_days = _match_number(office_match)

    if home_days is not None and office_days is not None:
        return (
            f"{home_days} {_days_label(home_days)} from home / "
            f"{office_days} {_days_label(office_days)} in office"
        )
    if home_days is not None:
        return f"{home_days} {_days_label(home_days)} from home"

    office_week = _OFFICE_DAYS_PER_WEEK_RE.search(text)
    office_week_days = _match_number(office_week)
    if office_week_days is not None:
        return (
            f"{office_week_days} {_days_label(office_week_days, 'office days')} "
            "per week"
        )

    if office_days is not None:
        return f"{office_days} {_days_label(office_days)} in office"

    weekday = _WEEKDAY_HOME_RE.search(text) or _HOME_ON_WEEKDAY_RE.search(text)
    if weekday:
        return f"{weekday.group('day').title()} from home"

    return "Hybrid working"


def _evidence_for_explicit_home_office(text: str) -> str:
    sentences = [norm_text(sentence) for sentence in SPLIT.split(text) if norm_text(sentence)]
    for sentence in sentences:
        if _EXPLICIT_HOME_OFFICE_RE.search(sentence):
            return sentence[:1200]
    return ""


def classify_working_arrangement(
    title: str,
    description: str,
    area: str = "",
    location: str = "",
) -> WorkingArrangementMetadata:
    """Return badge metadata without changing service/admin eligibility.

    Only Module 3's hybrid/partial-remote classification is accepted, plus one
    narrow explicit home-and-office phrase from the production brief. Fully
    remote, ambiguous, conditional, negative and false-positive classifications
    do not receive a regional hybrid badge.
    """
    combined_text = norm_text(
        " ".join(map(clean_description, (title, description, area, location)))
    )
    decision = classify_remote(title, description, area, location)

    qualifies_from_module3 = (
        decision.classification == QUALIFYING_CLASSIFICATION
        and bool(_CREDIBLE_SIGNAL_RE.search(combined_text))
    )
    explicit_home_office = bool(_EXPLICIT_HOME_OFFICE_RE.search(combined_text))

    if not (qualifies_from_module3 or explicit_home_office):
        return WorkingArrangementMetadata(NON_QUALIFYING_VALUE, "", "")

    evidence = decision.evidence if qualifies_from_module3 else ""
    if not evidence:
        evidence = _evidence_for_explicit_home_office(combined_text)

    arrangement = (
        "hybrid"
        if re.search(r"\bhybrid\b", combined_text, re.IGNORECASE)
        or explicit_home_office
        else "partly_remote"
    )
    return WorkingArrangementMetadata(
        arrangement,
        _exact_arrangement_text(combined_text),
        evidence,
    )
