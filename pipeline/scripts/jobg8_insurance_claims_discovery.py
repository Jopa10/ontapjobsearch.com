from __future__ import annotations

import argparse
import math
import re
from collections import Counter
from pathlib import Path

import pandas as pd

TITLE_COL = "/Job/Position"
DESCRIPTION_COL = "/Job/Description"
AREA_COL = "/Job/Area"
LOCATION_COL = "/Job/Location"
DISPLAY_REF_COL = "/Job/DisplayReference"
SALARY_MIN_COL = "/Job/SalaryMinimum"
SALARY_MAX_COL = "/Job/SalaryMaximum"
SALARY_PERIOD_COL = "/Job/SalaryPeriod"
CLASSIFICATION_COL = "/Job/Classification"
AREA_UNUSABLE_VALUES = {"", "not specified", "unknown"}

TITLE_BROAD = re.compile(
    r"\b(claims?|insurance|underwrit(?:er|ing)?|loss\s+adjust(?:er|ing)|adjuster|"
    r"actuar(?:y|ial)|reinsurance|broker|fnol|first\s+notification\s+of\s+loss|"
    r"account\s+handler)\b",
    re.IGNORECASE,
)
DESCRIPTION_STRONG = (
    "claims handling",
    "claims handler",
    "insurance claims",
    "insurance policy",
    "policyholder",
    "policy holder",
    "underwriting",
    "first notification of loss",
    "fnol",
)
SUPPORT_TITLE = re.compile(
    r"\b(handler|administrator|administrative|advisor|adviser|assistant|processor|"
    r"coordinator|co-ordinator|assessor|customer\s+service|contact\s+centre|"
    r"first\s+response|new\s+claims?|fnol)\b",
    re.IGNORECASE,
)
CLAIM = re.compile(r"\bclaims?\b", re.IGNORECASE)
INSURANCE = re.compile(r"\binsurance\b", re.IGNORECASE)
ACCOUNT_HANDLER = re.compile(r"\baccount\s+handler\b", re.IGNORECASE)
CLAIMS_TECHNICAL = re.compile(r"\bclaims?\s+(technician|adjuster)\b|\bclaims?\s+adjuster\b", re.IGNORECASE)
SPECIALIST = re.compile(
    r"\b(underwriter|underwriting|actuary|actuarial|reinsurance|loss\s+adjuster|"
    r"field[- ]based\s+loss\s+adjuster|broker|broking)\b",
    re.IGNORECASE,
)
SENIOR_BOUNDARY = re.compile(r"\b(head|director|manager)\b", re.IGNORECASE)


def norm(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def latest_feed(input_dir: Path) -> Path:
    files = sorted(p for p in input_dir.iterdir() if p.suffix.lower() in {".xlsx", ".xls", ".xlsm"})
    if not files:
        raise SystemExit(f"No Excel feeds found in {input_dir}")
    dated = [(p, re.search(r"(20\d{2}-\d{2}-\d{2})", p.stem)) for p in files]
    dated = [(p, m.group(1)) for p, m in dated if m]
    return max(dated, key=lambda x: x[1])[0] if dated else files[-1]


def find_classification_col(columns: list[str]) -> str | None:
    if CLASSIFICATION_COL in columns:
        return CLASSIFICATION_COL
    matches = [c for c in columns if "classification" in c.casefold()]
    return matches[0] if matches else None


def parse_salary(value: object) -> float | None:
    s = norm(value)
    if not s:
        return None
    s = re.sub(r"[^0-9.\-]", "", s.replace(",", ""))
    try:
        n = float(s)
    except ValueError:
        return None
    return n if n > 0 and math.isfinite(n) else None


def annual_factor(period: object) -> float | None:
    p = norm(period).casefold()
    if not p:
        return None
    if any(k in p for k in ("annum", "annual", "year", "yearly")):
        return 1.0
    if "month" in p:
        return 12.0
    if "week" in p:
        return 52.0
    if "day" in p:
        return 260.0
    if "hour" in p:
        return 1950.0  # diagnostic approximation: 37.5 hours x 52 weeks
    return None


def annualise(value: object, period: object) -> float | None:
    n = parse_salary(value)
    factor = annual_factor(period)
    return n * factor if n is not None and factor is not None else None


def has_strong_description_signal(title: str, description: str) -> bool:
    t = title.casefold()
    d = description.casefold()
    score = sum(1 for term in DESCRIPTION_STRONG if term in d)
    return score >= 2 and bool(SUPPORT_TITLE.search(t))


def is_broad_candidate(title: str, description: str) -> bool:
    return bool(TITLE_BROAD.search(title)) or has_strong_description_signal(title, description)


def classify(title: str, description: str) -> tuple[str, str]:
    t = title.casefold()
    title_signal = bool(TITLE_BROAD.search(title))

    # Claims support is the primary seam. 'Senior' alone is deliberately not an exclusion.
    if CLAIM.search(title) and SUPPORT_TITLE.search(title) and not SENIOR_BOUNDARY.search(title):
        if CLAIMS_TECHNICAL.search(title):
            return "REVIEW_CLAIMS_TECHNICAL", "claims technician/adjuster boundary"
        return "CORE_CLAIMS_SUPPORT", "claims + support/service title"

    if ("fnol" in t or "first notification of loss" in t or "first response" in t) and SUPPORT_TITLE.search(title):
        return "CORE_CLAIMS_SUPPORT", "FNOL/first-response support title"

    if INSURANCE.search(title) and SUPPORT_TITLE.search(title) and not SPECIALIST.search(title) and not SENIOR_BOUNDARY.search(title):
        return "CORE_INSURANCE_SUPPORT", "insurance + support/service title"

    if ACCOUNT_HANDLER.search(title):
        return "REVIEW_ACCOUNT_HANDLER", "insurance/broking account-handler boundary"

    if SPECIALIST.search(title) or SENIOR_BOUNDARY.search(title):
        return "EXCLUDE_SPECIALIST", "specialist/senior insurance boundary"

    if CLAIMS_TECHNICAL.search(title):
        return "REVIEW_CLAIMS_TECHNICAL", "claims technical boundary"

    if title_signal:
        return "REVIEW_OTHER_INSURANCE", "insurance/claims title needs boundary review"

    return "REVIEW_DESCRIPTION_ONLY", "description-led insurance/claims signal"


def load_geo_lookups(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    area_df = pd.read_excel(path, dtype=str).fillna("")
    if not {"Area", "Cluster"}.issubset(area_df.columns):
        return {}, {}
    area_lookup = {
        norm(row["Area"]).casefold(): norm(row["Cluster"])
        for _, row in area_df.iterrows()
        if norm(row["Area"]) and norm(row["Cluster"])
    }
    try:
        fallback_df = pd.read_excel(path, sheet_name="LocationFallback", dtype=str).fillna("")
    except ValueError:
        return area_lookup, {}
    fallback = {
        norm(row["Location"]).casefold(): norm(row["Cluster"])
        for _, row in fallback_df.iterrows()
        if norm(row.get("Status", "")).casefold() == "auto"
        and norm(row.get("Location", ""))
        and norm(row.get("Cluster", ""))
    }
    return area_lookup, fallback


def ontap_region(area: object, location: object, area_lookup: dict[str, str], fallback: dict[str, str]) -> str:
    a = norm(area).casefold()
    loc = norm(location).casefold()
    if a in AREA_UNUSABLE_VALUES:
        return fallback.get(loc, "Other / Unknown")
    return area_lookup.get(a, "Other / Unknown")


def money(value: float | None) -> str:
    if value is None or math.isnan(value):
        return "—"
    return f"£{value:,.0f}"


def pct(n: int, d: int) -> str:
    return f"{(100*n/d):.0f}%" if d else "—"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--geo-lookup", type=Path, default=Path("pipeline/geo/geo_lookup.xlsx"))
    ap.add_argument("--soft-salary-min", type=float, default=25000)
    ap.add_argument("--soft-salary-max", type=float, default=40000)
    args = ap.parse_args()

    feed = latest_feed(args.input_dir)
    raw = pd.read_excel(feed, dtype=str).fillna("")
    if TITLE_COL not in raw.columns:
        raise SystemExit(f"Latest JobG8 feed is missing required title column {TITLE_COL}")

    classification_col = find_classification_col(list(raw.columns))
    area_lookup, fallback = load_geo_lookups(args.geo_lookup)

    rows: list[dict[str, object]] = []
    for _, row in raw.iterrows():
        title = norm(row.get(TITLE_COL, ""))
        description = norm(row.get(DESCRIPTION_COL, ""))
        if not is_broad_candidate(title, description):
            continue
        decision, reason = classify(title, description)
        period = norm(row.get(SALARY_PERIOD_COL, ""))
        annual_min = annualise(row.get(SALARY_MIN_COL, ""), period)
        annual_max = annualise(row.get(SALARY_MAX_COL, ""), period)
        vals = [x for x in (annual_min, annual_max) if x is not None]
        midpoint = sum(vals) / len(vals) if vals else None
        rows.append({
            "display_reference": norm(row.get(DISPLAY_REF_COL, "")),
            "title": title,
            "area": norm(row.get(AREA_COL, "")),
            "location": norm(row.get(LOCATION_COL, "")),
            "ontap_region": ontap_region(row.get(AREA_COL, ""), row.get(LOCATION_COL, ""), area_lookup, fallback),
            "jobg8_classification": norm(row.get(classification_col, "")) if classification_col else "",
            "salary_minimum_raw": norm(row.get(SALARY_MIN_COL, "")),
            "salary_maximum_raw": norm(row.get(SALARY_MAX_COL, "")),
            "salary_period": period,
            "annualised_minimum_estimate": annual_min,
            "annualised_maximum_estimate": annual_max,
            "annualised_midpoint_estimate": midpoint,
            "discovery_decision": decision,
            "discovery_reason": reason,
        })

    out = pd.DataFrame(rows)
    if out.empty:
        raise SystemExit("Claims/insurance discovery produced no candidates")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "jobg8-insurance-claims-discovery-current.csv"
    md_path = args.output_dir / "jobg8-insurance-claims-discovery-current.md"
    out.to_csv(csv_path, index=False, encoding="utf-8-sig")

    counts = Counter(out["discovery_decision"])
    core_mask = out["discovery_decision"].isin(["CORE_CLAIMS_SUPPORT", "CORE_INSURANCE_SUPPORT"])
    review_mask = out["discovery_decision"].str.startswith("REVIEW_")
    core = out.loc[core_mask].copy()
    review = out.loc[review_mask].copy()
    plausible = out.loc[core_mask | review_mask].copy()
    specialist = out.loc[out["discovery_decision"] == "EXCLUDE_SPECIALIST"].copy()

    salary_mid = pd.to_numeric(core["annualised_midpoint_estimate"], errors="coerce").dropna()
    salary_in = salary_mid.between(args.soft_salary_min, args.soft_salary_max, inclusive="both") if len(salary_mid) else pd.Series(dtype=bool)
    salary_below = salary_mid < args.soft_salary_min
    salary_above = salary_mid > args.soft_salary_max

    title_counts = core["title"].value_counts().head(20)
    review_title_counts = review["title"].value_counts().head(15)
    region_counts = core.loc[core["ontap_region"] != "Other / Unknown", "ontap_region"].value_counts().head(12)
    class_counts = core["jobg8_classification"].replace("", "(blank)").value_counts().head(15)

    lines = [
        "# JobG8 Insurance & Claims Support discovery audit",
        "",
        f"Feed: **{feed.name}**",
        f"Jobs in feed: **{len(raw):,}**",
        f"Broad insurance/claims candidates: **{len(out):,}**",
        f"Core support candidates: **{len(core):,}**",
        f"Boundary-review candidates: **{len(review):,}**",
        f"Specialist/senior exclusions at discovery stage: **{len(specialist):,}**",
        "",
        "Diagnostic only: this report does not change any Ontap publication or family-selection rule.",
        "",
        "## Decision breakdown",
        "",
        "| Decision | Jobs |",
        "|---|---:|",
    ]
    for decision, count in counts.most_common():
        lines.append(f"| {decision} | {count:,} |")

    lines += [
        "",
        "## Salary shape — core support only",
        "",
        f"Soft reference range: **{money(args.soft_salary_min)}–{money(args.soft_salary_max)}** (diagnostic, not a hard gate).",
        f"Core jobs with usable annualised salary: **{len(salary_mid):,} / {len(core):,}**.",
    ]
    if len(salary_mid):
        lines += [
            f"Median annualised midpoint: **{money(float(salary_mid.median()))}**.",
            f"Within soft range: **{int(salary_in.sum()):,} ({pct(int(salary_in.sum()), len(salary_mid))})**; below: **{int(salary_below.sum()):,}**; above: **{int(salary_above.sum()):,}**.",
            "Hourly/daily/weekly figures are annualised approximately for discovery only.",
        ]
    else:
        lines.append("No core candidates had a usable salary period/value pair.")

    lines += [
        "",
        "## Recurring core titles",
        "",
        "| Jobs | Title |",
        "|---:|---|",
    ]
    for title, count in title_counts.items():
        lines.append(f"| {count:,} | {str(title).replace('|', '/')} |")

    lines += [
        "",
        "## Boundary titles to inspect",
        "",
        "| Jobs | Title |",
        "|---:|---|",
    ]
    for title, count in review_title_counts.items():
        lines.append(f"| {count:,} | {str(title).replace('|', '/')} |")

    lines += [
        "",
        "## JobG8 classifications feeding core support",
        "",
        f"Classification column detected: **{classification_col or 'NONE'}**.",
        "",
        "| Jobs | JobG8 classification |",
        "|---:|---|",
    ]
    for category, count in class_counts.items():
        lines.append(f"| {count:,} | {str(category).replace('|', '/')} |")

    lines += [
        "",
        "## Core regional shape",
        "",
        "| Jobs | Ontap region |",
        "|---:|---|",
    ]
    for region, count in region_counts.items():
        lines.append(f"| {count:,} | {str(region).replace('|', '/')} |")

    lines += [
        "",
        "## Discovery interpretation",
        "",
        "- CORE_CLAIMS_SUPPORT: claims-led handler/admin/advisor/assistant/processor/coordinator/assessor/FNOL-style work; senior claims handlers are not excluded merely for the word 'senior'.",
        "- CORE_INSURANCE_SUPPORT: clearly insurance-led admin/customer-support titles without specialist underwriting/broking signals.",
        "- REVIEW_ACCOUNT_HANDLER: plausible customer/client servicing, but may be broker/sales/specialist work.",
        "- REVIEW_CLAIMS_TECHNICAL: claims-technician/adjuster boundary requiring advert review.",
        "- EXCLUDE_SPECIALIST: underwriting, actuarial, broking/loss-adjusting or manager/head/director boundary at discovery stage.",
        "- Family overlap remains allowed; a claims administrator or contact-centre claims advisor may also legitimately qualify for Service Admin or Customer Service.",
    ]

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(md_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
