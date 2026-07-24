"""Shared, data-driven policy helpers for the two JobG8 selection pipelines.

The category classifiers remain in ``service_admin_pipeline.py`` and
``support_worker_pipeline.py``.  This module only reads shared editable policy
files, assesses salary consistently, and identifies the current JobG8 feed so
manual decisions cannot leak from one daily feed into the next.
"""
from __future__ import annotations

import csv
import hashlib
import math
import os
import re
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from xml.etree import ElementTree


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
SALARY_POLICY_PATH = PIPELINE_ROOT / "config" / "regional_salary_review_thresholds.csv"
REFINEMENT_RULES_PATH = PIPELINE_ROOT / "registers" / "pipeline_refinement_rules.csv"

ANNUAL_SALARY_FACTORS = {
    "year": 1.0,
    "annual": 1.0,
    "annum": 1.0,
    "month": 12.0,
    "monthly": 12.0,
    "week": 52.0,
    "weekly": 52.0,
    "day": 260.0,
    "daily": 260.0,
    "hour": 37.5 * 52.0,
    "hourly": 37.5 * 52.0,
}
MIN_CREDIBLE_ANNUAL_SALARY = 1_000.0
MAX_CREDIBLE_ANNUAL_SALARY = 250_000.0


@dataclass(frozen=True)
class SalaryAssessment:
    """Result of comparing a job's upper salary with its regional policy."""

    status: str
    annual_upper_gbp: float | None
    review_threshold_gbp: float
    reason: str

    @property
    def review_required(self) -> bool:
        return self.status == "review"

    @property
    def corrupt(self) -> bool:
        return self.status == "corrupt"


@dataclass(frozen=True)
class ContextAssessment:
    """Result of an agreed title rule that needs description context."""

    status: str
    reason: str

    @property
    def review_required(self) -> bool:
        return self.status == "review"

    @property
    def excluded(self) -> bool:
        return self.status == "exclude"


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _parse_amount(value: Any) -> float | None:
    text = _clean_text(value).replace(",", "").replace("£", "")
    if not text:
        return None
    try:
        amount = float(text)
        return amount if math.isfinite(amount) else None
    except ValueError:
        match = re.search(r"-?\d+(?:\.\d+)?", text)
        return float(match.group(0)) if match else None


def _normalise_period(period: Any) -> str:
    text = _clean_text(period).casefold()
    for candidate in ANNUAL_SALARY_FACTORS:
        if re.search(rf"\b{re.escape(candidate)}\b", text):
            return candidate
    return ""


def _amounts_and_period_from_text(salary_text: Any) -> tuple[list[float], str]:
    text = _clean_text(salary_text)
    if not text:
        return [], ""
    amounts = [
        float(raw.replace(",", ""))
        for raw in re.findall(r"£\s*(\d[\d,]*(?:\.\d+)?)", text)
    ]
    return amounts, _normalise_period(text)


def load_salary_thresholds(path: Path = SALARY_POLICY_PATH) -> dict[str, float]:
    """Load regional upper-salary review points, including a DEFAULT row."""
    thresholds: dict[str, float] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            region = _clean_text(row.get("region"))
            threshold = _parse_amount(row.get("review_threshold_gbp"))
            if region and threshold is not None:
                thresholds[region.casefold()] = threshold
    if "default" not in thresholds:
        raise ValueError(f"Salary policy must contain a DEFAULT row: {path}")
    return thresholds


def salary_threshold_for_region(region: str, thresholds: dict[str, float]) -> float:
    return thresholds.get(_clean_text(region).casefold(), thresholds["default"])


def assess_salary(
    *,
    salary_min: Any,
    salary_max: Any,
    salary_period: Any,
    salary_text: Any,
    region: str,
    thresholds: dict[str, float],
    reviewed_ceiling_gbp: Any = None,
) -> SalaryAssessment:
    """Annualise the upper figure and apply the agreed regional review rule.

    Structured JobG8 fields take precedence.  Text parsing is used only when
    structured amounts are unavailable.  A reviewed title may carry a ceiling:
    the previous ruling remains reusable up to that pay level, while any higher
    future advert returns to POSS for another look.
    """
    amounts = [
        amount
        for amount in (_parse_amount(salary_min), _parse_amount(salary_max))
        if amount is not None
    ]
    period = _normalise_period(salary_period)
    if not amounts:
        amounts, text_period = _amounts_and_period_from_text(salary_text)
        period = text_period or period

    threshold = salary_threshold_for_region(region, thresholds)
    if not amounts:
        return SalaryAssessment("missing", None, threshold, "salary unavailable")
    if not period:
        return SalaryAssessment(
            "unassessed",
            None,
            threshold,
            "salary period unavailable; no automatic salary decision",
        )

    annual_upper = max(amounts) * ANNUAL_SALARY_FACTORS[period]
    if (
        annual_upper < MIN_CREDIBLE_ANNUAL_SALARY
        or annual_upper > MAX_CREDIBLE_ANNUAL_SALARY
    ):
        return SalaryAssessment(
            "corrupt",
            annual_upper,
            threshold,
            f"implausible annualised salary £{annual_upper:,.0f}",
        )

    reviewed_ceiling = _parse_amount(reviewed_ceiling_gbp)
    if reviewed_ceiling is not None and annual_upper <= reviewed_ceiling:
        return SalaryAssessment(
            "ok",
            annual_upper,
            threshold,
            f"within agreed title-specific reviewed ceiling £{reviewed_ceiling:,.0f}",
        )

    if annual_upper > threshold:
        return SalaryAssessment(
            "review",
            annual_upper,
            threshold,
            f"annualised upper salary £{annual_upper:,.0f} exceeds regional review point £{threshold:,.0f}",
        )

    return SalaryAssessment(
        "ok",
        annual_upper,
        threshold,
        f"annualised upper salary £{annual_upper:,.0f} is within regional review point £{threshold:,.0f}",
    )


def load_refinement_rules(
    category: str,
    path: Path = REFINEMENT_RULES_PATH,
) -> list[dict[str, str]]:
    """Load agreed exact-title refinements for one pipeline category."""
    wanted = category.casefold()
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [
            {key: _clean_text(value) for key, value in row.items()}
            for row in csv.DictReader(handle)
            if _clean_text(row.get("category")).casefold() == wanted
            and _clean_text(row.get("title"))
        ]


_MANDATORY_SPECIALIST_RE = re.compile(
    r"(?:"
    r"\b(?:must|essential|required|requirement)\b.{0,90}"
    r"\b(?:cipd|aat|acca|cima|idva|isva|social work|qualified|qualification|"
    r"customs|export|procurement|logistics|insurance|dental|healthcare)\b"
    r"|"
    r"\b(?:minimum|at least)\s+(?:two|three|four|five|2|3|4|5)\+?\s+years?"
    r".{0,50}\bexperience\b"
    r")",
    re.IGNORECASE | re.DOTALL,
)
_STATUTORY_SUPPORT_BARRIER_RE = re.compile(
    r"(?:"
    r"\bqualified social worker\b|"
    r"\bsocial work qualification\b|"
    r"\bstatutory (?:casework|case work|case management)\b|"
    r"\bmust\b.{0,80}\b(?:case management|social work qualification)\b"
    r")",
    re.IGNORECASE | re.DOTALL,
)
_DIRECT_CARE_RE = re.compile(
    r"\b(?:personal care|care needs|daily living|medication|moving and handling|"
    r"direct support|independent living|care plan|companionship|supporting (?:him|her|"
    r"them|a client|an individual).{0,40}(?:home|community|daily))\b",
    re.IGNORECASE | re.DOTALL,
)
_CORPORATE_PA_RE = re.compile(
    r"\b(?:chief executive|ceo|executive assistant|board meetings?|diary management|"
    r"minute taking|corporate office)\b",
    re.IGNORECASE,
)


def assess_context_policy(policy: str, description: Any) -> ContextAssessment:
    """Apply one of the small, explicit context policies in the rule register."""
    policy_key = _clean_text(policy).casefold()
    text = _clean_text(description)
    if not policy_key:
        return ContextAssessment("ok", "")

    if policy_key == "support_personal_assistant":
        if _CORPORATE_PA_RE.search(text):
            return ContextAssessment(
                "exclude",
                "Personal Assistant description signals a corporate/executive PA rather than direct care",
            )
        if not _DIRECT_CARE_RE.search(text):
            return ContextAssessment(
                "exclude",
                "Personal Assistant title has no explicit personal-care or direct-support context",
            )
        return ContextAssessment(
            "ok",
            "Personal Assistant description explicitly establishes personal care or direct support",
        )

    if policy_key == "family_direct_support":
        if _STATUTORY_SUPPORT_BARRIER_RE.search(text):
            return ContextAssessment(
                "exclude",
                "mandatory statutory casework or social-work requirement creates a specialist barrier",
            )
        return ContextAssessment("ok", "family support role has no explicit statutory barrier")

    if policy_key == "specialist_support_requirements":
        if _STATUTORY_SUPPORT_BARRIER_RE.search(text) or _MANDATORY_SPECIALIST_RE.search(text):
            return ContextAssessment(
                "exclude",
                "regulated qualification or substantial mandatory specialist experience is explicit",
            )
        return ContextAssessment("ok", "no regulated or substantial mandatory specialist barrier found")

    if policy_key == "specialist_requirements_review":
        if _MANDATORY_SPECIALIST_RE.search(text):
            return ContextAssessment(
                "review",
                "description appears to make specialist qualifications or substantial prior experience mandatory",
            )
        return ContextAssessment("ok", "no explicit mandatory specialist barrier found")

    return ContextAssessment("review", f"unknown context policy: {policy}")


def resolve_feed_date(job_file: Path, override: str | None = None) -> str:
    """Return a stable feed identity without consulting the wall clock.

    ``ONTAP_FEED_DATE`` is an operational override.  For normal XLSX feeds, the
    workbook's own modified/created date is authoritative.  Other file types
    use a deterministic content fingerprint so a midnight rerun cannot change
    identity and a replacement feed cannot inherit old manual actions.
    """
    configured = _clean_text(override or os.environ.get("ONTAP_FEED_DATE"))
    if configured:
        try:
            date.fromisoformat(configured)
        except ValueError as exc:
            raise ValueError("ONTAP_FEED_DATE must use YYYY-MM-DD") from exc
        return configured

    if job_file.suffix.casefold() == ".xlsx":
        try:
            with zipfile.ZipFile(job_file) as workbook:
                root = ElementTree.fromstring(workbook.read("docProps/core.xml"))
            timestamps = {
                element.tag.rsplit("}", 1)[-1]: _clean_text(element.text)
                for element in root.iter()
                if element.tag.rsplit("}", 1)[-1] in {"modified", "created"}
                and _clean_text(element.text)
            }
            for field in ("modified", "created"):
                timestamp = timestamps.get(field, "")
                if not timestamp:
                    continue
                candidate = timestamp[:10]
                date.fromisoformat(candidate)
                return candidate
        except (KeyError, ValueError, zipfile.BadZipFile, ElementTree.ParseError):
            pass

    digest = hashlib.sha256(job_file.read_bytes()).hexdigest()[:16]
    return f"sha256-{digest}"


def markdown_feed_date(text: str) -> str:
    match = re.search(r"(?im)^\s*feed_date:\s*(\S+)\s*$", text)
    return match.group(1) if match else ""
