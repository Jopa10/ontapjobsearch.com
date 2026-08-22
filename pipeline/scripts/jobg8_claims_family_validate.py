from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter
from pathlib import Path

import pandas as pd

from pipeline.scripts.jobg8_insurance_claims_discovery import (
    AREA_COL,
    DESCRIPTION_COL,
    DISPLAY_REF_COL,
    LOCATION_COL,
    SALARY_MAX_COL,
    SALARY_MIN_COL,
    SALARY_PERIOD_COL,
    TITLE_COL,
    annualise,
    find_classification_col,
    is_broad_candidate,
    latest_feed,
    load_geo_lookups,
    norm,
    ontap_region,
)

# Family boundary derived from the 2026-08-22 advert-level review.
# Diagnostic validation only: this does not publish jobs or activate slices.

CLAIMS_POSITIVE_TITLE = re.compile(
    r"\b(claims?\s+(handler|administrator|admin(?:istrative)?|advisor|adviser|clerk|technician)|"
    r"(travel|motor|property|legal\s+expenses|credit\s+hire|recoveries|technical)\s+claims?\s+"
    r"(handler|advisor|adviser|administrator|clerk|technician)|"
    r"claims?\s+assistant|claims?\s+coordinator)\b",
    re.IGNORECASE,
)

INSURANCE_ADMIN_TITLE = re.compile(
    r"\binsurance\s+(administrator|admin(?:istrative)?|coordinator|co-ordinator)\b",
    re.IGNORECASE,
)

CUSTOMER_SUPPORT_TITLE = re.compile(
    r"\b(customer\s+service\s+(advisor|adviser)|senior\s+customer\s+service\s+(advisor|adviser))\b",
    re.IGNORECASE,
)

HARD_TITLE_OUT = re.compile(
    r"\b(underwriter|underwriting|actuary|actuarial|reinsurance\s+underwriter|"
    r"loss\s+adjuster|claims?\s+adjuster|desktop\s+adjuster|commercial\s+adjuster|"
    r"field\s+adjuster|solicitor|lawyer|team\s+leader|manager|director|head\s+of|"
    r"product\s+owner|account\s+executive|sales\s+executive|sales\s+specialist|sales\s+advisor|"
    r"sales\s+adviser)\b",
    re.IGNORECASE,
)

BROKING_TITLE_OUT = re.compile(
    r"\b(account\s+handler|insurance\s+advisor|insurance\s+adviser|insurance\s+technician)\b",
    re.IGNORECASE,
)

LEGAL_LITIGATION_OUT = re.compile(
    r"\b(litigated|litigation|small\s+claims\s+track|fast\s+track|file\s+handler)\b",
    re.IGNORECASE,
)

SPECIALIST_CLAIMS_OUT = re.compile(
    r"\b(large\s+loss|major\s+loss|complex\s+personal\s+injury|technical\s+claims\s+lead|"
    r"technical\s+lead|claims\s+specialist)\b",
    re.IGNORECASE,
)

FIELD_EXECUTIVE_OUT = re.compile(r"\bclaims?\s+executive\b", re.IGNORECASE)

BORDERLINE_TITLE = re.compile(
    r"\b(senior\s+coordinator\s+-\s+loss\s+prevention,?\s+legal\s+and\s+insurance|"
    r"litigated\s+motor\s+recoveries\s+claims?\s+handler|"
    r"insurance\s+claims?\s*&\s*client\s+services\s+specialist|"
    r"experienced\s+insurance\s+technician)\b",
    re.IGNORECASE,
)

CLAIMS_DESCRIPTION_SIGNAL = re.compile(
    r"\b(claims?\s+handling|claims?\s+administration|claims?\s+processing|"
    r"insurance\s+claims?|policyholder|claimants?|claim\s+progress|claim\s+resolution|"
    r"claims?\s+team|claims?\s+department)\b",
    re.IGNORECASE,
)

BROKING_DESCRIPTION_SIGNAL = re.compile(
    r"\b(broking|brokerage|market\s+risks|renewals|mid[- ]term\s+adjustments|MTAs|"
    r"new\s+business\s+quotes|portfolio\s+growth|cross[- ]sell|upsell|placement\s+of\s+new\s+business)\b",
    re.IGNORECASE,
)

SPECIALIST_DESCRIPTION_SIGNAL = re.compile(
    r"\b(Lloyd'?s\s+market|Lloyd'?s\s+syndicate|ECF|delegated\s+authority|"
    r"high[- ]value|major[- ]loss|fatalit(?:y|ies)|reinsurers?|facultative|"
    r"excess\s+of\s+loss|complex\s+loss)\b",
    re.IGNORECASE,
)


def fingerprint(title: str, description: str, location: str) -> str:
    basis = "|".join(
        [
            re.sub(r"\W+", " ", title.casefold()).strip(),
            re.sub(r"\W+", " ", description.casefold()).strip()[:1200],
            re.sub(r"\W+", " ", location.casefold()).strip(),
        ]
    )
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def boundary_decision(title: str, description: str, annual_max: float | None) -> tuple[str, str]:
    combined = f"{title} {description}"
    if annual_max is not None and annual_max > 50000:
        return "OUT", "salary maximum over £50k"
    if BORDERLINE_TITLE.search(title):
        return "BORDERLINE", "manual review retained as genuinely arguable"
    if HARD_TITLE_OUT.search(title):
        return "OUT", "adjuster/sales/legal/management/senior-specialist title boundary"
    if FIELD_EXECUTIVE_OUT.search(title):
        return "OUT", "claims executive is field/client-risk oversight rather than claims support"
    if LEGAL_LITIGATION_OUT.search(title):
        return "OUT", "substantively litigation/legal file-handling rather than claims operations"
    if SPECIALIST_CLAIMS_OUT.search(combined):
        return "OUT", "large-loss/major-loss/technical-lead specialist boundary"
    if INSURANCE_ADMIN_TITLE.search(title) and CLAIMS_DESCRIPTION_SIGNAL.search(description):
        return "IN", "insurance administration with clear claims-processing/support duties"
    if CUSTOMER_SUPPORT_TITLE.search(title) and CLAIMS_DESCRIPTION_SIGNAL.search(description):
        return "IN", "customer-service role embedded in insurance-claims handling"
    if CLAIMS_POSITIVE_TITLE.search(title):
        if SPECIALIST_DESCRIPTION_SIGNAL.search(description) and re.search(
            r"\b(adjust|Lloyd|major\s+loss|large\s+loss|fatalit|reinsur)", description, re.IGNORECASE
        ):
            return "OUT", "claims title but advert is specialist/market/large-loss work"
        return "IN", "claims handling/admin/advice/support role"
    if BROKING_TITLE_OUT.search(title):
        if CLAIMS_DESCRIPTION_SIGNAL.search(description) and not BROKING_DESCRIPTION_SIGNAL.search(description):
            return "BORDERLINE", "insurance operations title with some claims evidence but unclear family fit"
        return "OUT", "general broking/account-handling/advice rather than claims support"
    return "OUT", "broad insurance/claims hit but not within defined claims-support boundary"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--geo-lookup", type=Path, default=Path("pipeline/geo/geo_lookup.xlsx"))
    args = ap.parse_args()

    feed = latest_feed(args.input_dir)
    raw = pd.read_excel(feed, dtype=str).fillna("")
    classification_col = find_classification_col(list(raw.columns))
    area_lookup, fallback = load_geo_lookups(args.geo_lookup)

    rows: list[dict[str, object]] = []
    for _, row in raw.iterrows():
        title = norm(row.get(TITLE_COL, ""))
        description = norm(row.get(DESCRIPTION_COL, ""))
        if not is_broad_candidate(title, description):
            continue
        period = norm(row.get(SALARY_PERIOD_COL, ""))
        annual_min = annualise(row.get(SALARY_MIN_COL, ""), period)
        annual_max = annualise(row.get(SALARY_MAX_COL, ""), period)
        decision, reason = boundary_decision(title, description, annual_max)
        location = norm(row.get(LOCATION_COL, ""))
        rows.append({
            "display_reference": norm(row.get(DISPLAY_REF_COL, "")),
            "title": title,
            "location": location,
            "ontap_region": ontap_region(row.get(AREA_COL, ""), row.get(LOCATION_COL, ""), area_lookup, fallback),
            "jobg8_classification": norm(row.get(classification_col, "")) if classification_col else "",
            "salary_minimum_raw": norm(row.get(SALARY_MIN_COL, "")),
            "salary_maximum_raw": norm(row.get(SALARY_MAX_COL, "")),
            "salary_period": period,
            "annualised_minimum_estimate": annual_min,
            "annualised_maximum_estimate": annual_max,
            "boundary_decision": decision,
            "boundary_reason": reason,
            "content_fingerprint": fingerprint(title, description, location),
        })

    out = pd.DataFrame(rows)
    if out.empty:
        raise SystemExit("Claims family validation produced no broad candidates")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "jobg8-claims-family-validation-current.csv"
    md_path = args.output_dir / "jobg8-claims-family-validation-current.md"
    out.to_csv(csv_path, index=False, encoding="utf-8-sig")

    counts = Counter(out["boundary_decision"])
    in_rows = out[out["boundary_decision"] == "IN"].copy()
    borderline = out[out["boundary_decision"] == "BORDERLINE"].copy()
    unique_in = in_rows.drop_duplicates(subset=["content_fingerprint"])
    duplicate_in = len(in_rows) - len(unique_in)
    region_counts = unique_in.loc[unique_in["ontap_region"] != "Other / Unknown", "ontap_region"].value_counts()
    class_counts = unique_in["jobg8_classification"].replace("", "(blank)").value_counts()
    title_counts = unique_in["title"].value_counts().head(25)
    salary_max = pd.to_numeric(unique_in["annualised_maximum_estimate"], errors="coerce").dropna()
    over_50 = int((salary_max > 50000).sum()) if len(salary_max) else 0

    lines = [
        "# JobG8 Claims Support family validation", "", f"Feed: **{feed.name}**", f"Jobs in feed: **{len(raw):,}**",
        f"Broad insurance/claims universe: **{len(out):,}** raw rows", f"IN after advert-level boundary rules: **{len(in_rows):,}** raw rows",
        f"BORDERLINE: **{len(borderline):,}** raw rows", f"OUT: **{counts.get('OUT', 0):,}** raw rows",
        f"Content-unique IN jobs: **{len(unique_in):,}** (removed **{duplicate_in:,}** exact-content duplicate rows)", "",
        "Diagnostic only: no LIVE slice, publishing rule or production family status is changed.", "",
        "## Boundary now being tested", "",
        "- IN: claims handlers, claims administrators/clerks/advisers/technicians and clearly claims-led customer/admin support.",
        "- IN: senior claims handlers remain eligible when the advert is ordinary claims ownership and the salary is within scope.",
        "- OUT: general insurance broking/account-handler/account-executive/sales roles.",
        "- OUT: loss/claims adjusters, Lloyd's-market adjuster work, lawyers/solicitors, managers/team leaders and large/major-loss specialists.",
        "- OUT: annualised salary maximum **over £50,000**. Exactly £50,000 is not excluded by salary alone.",
        "- Legal-expenses/pre-litigation claims handling can remain IN; substantively litigated/legal file-handling is OUT.", "",
        "## Decision breakdown", "", "| Decision | Raw rows |", "|---|---:|",
    ]
    for decision in ("IN", "BORDERLINE", "OUT"):
        lines.append(f"| {decision} | {counts.get(decision, 0):,} |")
    lines += ["", "## Content-unique IN regional shape", "", "| Jobs | Ontap region |", "|---:|---|"]
    for region, count in region_counts.items():
        lines.append(f"| {count:,} | {str(region).replace('|', '/')} |")
    lines += ["", "## JobG8 classifications feeding content-unique IN jobs", "", "| Jobs | JobG8 classification |", "|---:|---|"]
    for category, count in class_counts.items():
        lines.append(f"| {count:,} | {str(category).replace('|', '/')} |")
    lines += ["", "## Recurring content-unique IN titles", "", "| Jobs | Title |", "|---:|---|"]
    for title, count in title_counts.items():
        lines.append(f"| {count:,} | {str(title).replace('|', '/')} |")
    lines += ["", "## Salary guard check", "", f"Content-unique IN jobs with usable annualised maximum: **{len(salary_max):,}**.", f"IN jobs still over £50k: **{over_50}** (must be zero)."]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(md_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
