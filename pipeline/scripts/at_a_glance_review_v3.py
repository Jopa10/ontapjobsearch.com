"""Final review hardening for candidate requirements and setting-only matches."""
from __future__ import annotations

import re
from typing import Any

from . import at_a_glance_review_core as core

RULE_VERSION = "3"

EXTRA_STOP_HEADINGS = (
    "to be successful in this role",
    "to be successful",
    "successful applicant",
    "successful candidate",
    "candidate requirements",
    "essential criteria",
    "desirable criteria",
    "what you need to succeed",
    "what you'll need to succeed",
    "what you will need to succeed",
    "why",
)

REQUIREMENT_LINE_PATTERNS = (
    re.compile(r"^(?:you(?:'ll| will)? need|you should have)\b", re.I),
    re.compile(r"^(?:the )?(?:successful|ideal) (?:applicant|candidate)\b", re.I),
    re.compile(r"^(?:previous|relevant|proven) experience\b", re.I),
    re.compile(r"^experience of\b", re.I),
    re.compile(r"^(?:essential|desirable)(?: criteria| skills| experience)?\b", re.I),
    re.compile(r"^must (?:have|be|hold)\b", re.I),
)

STRONG_ACCOMMODATION_PATTERNS = (
    re.compile(r"\bprovid(?:e|ing) (?:safe,? )?(?:supportive )?accommodation\b", re.I),
    re.compile(r"\bhelp(?:ing)? new residents settle\b", re.I),
    re.compile(r"\bsupport(?:ing)? residents (?:in|within) (?:supported )?accommodation\b", re.I),
    re.compile(r"\bdeliver(?:ing)? accommodation support\b", re.I),
)

core.RULE_VERSION = RULE_VERSION
core.STOP_HEADINGS = tuple(dict.fromkeys(core.STOP_HEADINGS + EXTRA_STOP_HEADINGS))

_original_source_description = core.source_description
_original_duty_lines = core.duty_lines
_original_find_attributes = core.find_attributes


def source_description(job: dict[str, Any]) -> str:
    text = _original_source_description(job)
    explicit_headings = (
        "To be successful in this role",
        "To be successful",
        "Successful Applicant",
        "Successful Candidate",
        "Candidate Requirements",
        "Essential Criteria",
        "Desirable Criteria",
        "What you need to succeed",
        "What you'll need to succeed",
        "What you will need to succeed",
    )
    for heading in explicit_headings:
        text = re.sub(
            rf"(?i)(?<!\n)(?={re.escape(heading)}\b)",
            "\n",
            text,
        )
    text = re.sub(
        r"(?i)(?<=[.!?])(?=Why\s+[A-Z][^\n?]{0,60}\?)",
        "\n",
        text,
    )
    return text


def duty_lines(description: str) -> list[str]:
    lines = _original_duty_lines(description)
    return [
        line
        for line in lines
        if not any(pattern.search(core.clean_text(line)) for pattern in REQUIREMENT_LINE_PATTERNS)
    ]


def find_attributes(lines: list[str], family: str) -> list[dict[str, str]]:
    attributes = [
        item
        for item in _original_find_attributes(lines, family)
        if item["key"] != "accommodation_support"
    ]
    if family != "support":
        return attributes

    evidence = next(
        (
            core.truncate_at_word(core.clean_text(line), 180)
            for line in lines
            if any(pattern.search(core.clean_text(line)) for pattern in STRONG_ACCOMMODATION_PATTERNS)
        ),
        "",
    )
    if evidence:
        attributes.append(
            {
                "key": "accommodation_support",
                "label": "Accommodation support",
                "phrase": "accommodation support",
                "evidence": evidence,
            }
        )
    return attributes


core.source_description = source_description
core.duty_lines = duty_lines
core.find_attributes = find_attributes

build_review = core.build_review
current_card_summary = core.current_card_summary
description_hash = core.description_hash
review_job = core.review_job
word_count = core.word_count
write_csv = core.write_csv
write_markdown = core.write_markdown
main = core.main
