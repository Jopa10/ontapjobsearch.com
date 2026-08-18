"""National reconciliation for the branch-only Customer Sales family test.

Purpose
-------
Explain how the broad Sales / Business Development discovery universe reduces to
an Ontap-style Customer Sales family and then to campaign/dedupe-adjusted regional
inventory.

Outputs
-------
- reports-daily/customer-sales-national-reconciliation.md
- reports-daily/customer-sales-national-region-counts.csv
- reports-daily/customer-sales-national-detail.csv

This is diagnostic only. It does not publish any live slice.
"""
from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

from scripts.service_admin_pipeline_core import COL, norm, norm_key

INPUT_PATH = Path("input/jobg8.xlsx")
GEO_PATH = Path("geo/geo_lookup.xlsx")
REPORT_DIR = Path("reports-daily")
MD_PATH = REPORT_DIR / "customer-sales-national-reconciliation.md"
REGION_CSV_PATH = REPORT_DIR / "customer-sales-national-region-counts.csv"
DETAIL_CSV_PATH = REPORT_DIR / "customer-sales-national-detail.csv"

# The 33 regions currently used in the daily regional overview. The national
# report also shows mapped regions outside this list separately.
ONTAP_33 = [
    "Berkshire",
    "Bristol & Bath",
    "Buckinghamshire",
    "Cambridgeshire",
    "Cumbria - North",
    "Cumbria - South",
    "Devon",
    "Dorset",
    "Essex",
    "Gloucestershire",
    "Greater Manchester - Manchester & Salford",
    "Greater Manchester - South",
    "Hampshire",
    "Hertfordshire",
    "Kent",
    "Lancashire - North",
    "London",
    "Norfolk",
    "North East",
    "Northamptonshire",
    "Nottinghamshire",
    "Oxfordshire",
    "Somerset",
    "Staffordshire",
    "Surrey",
    "Sussex",
    "West Midlands - Birmingham & Solihull",
    "West Midlands - Coventry & Warwickshire",
    "Wiltshire",
    "Yorkshire - East",
    "Yorkshire - North",
    "Yorkshire - South",
    "Yorkshire - West",
]

# Broad discovery doorway. This intentionally includes many things that the final
# family will reject: managers, field sales, specialist sales, account roles, etc.
BROAD_TITLE_TERMS = [
    "sales",
    "business development",
    "account manager",
    "account executive",
    "customer success",
    "telesales",
    "telemarketing",
    "lead generator",
    "appointment setter",
    "retention",
    "renewal",
]

DIRECT_TITLE_TERMS = [
    "sales advisor", "sales adviser", "sales executive", "sales consultant",
    "sales representative", "sales agent", "customer sales", "internal sales",
    "inside sales", "inbound sales", "outbound sales", "telephone sales", "telesales",
    "telemarketing", "telemarketer", "retention advisor", "retention adviser",
    "retention executive", "renewals advisor", "renewals adviser", "renewals executive",
    "new business advisor", "new business adviser", "new business executive",
    "business development executive", "lead generator", "appointment setter",
    "membership sales", "membership advisor", "membership adviser",
]

CUSTOMER_TITLE_TERMS = [
    "customer service", "customer care", "customer support", "customer advisor", "customer adviser",
    "customer representative", "customer account", "customer success", "client service", "client services",
    "client advisor", "client adviser", "call centre", "call center", "contact centre", "contact center",
    "membership advisor", "membership adviser",
]

ACCOUNT_TITLE_TERMS = ["account manager", "account executive"]

STRONG_SALES_EVIDENCE = [
    "commission", "uncapped commission", "sales target", "sales targets", "sales kpi", "sales kpis",
    "sales opportunity", "sales opportunities", "upsell", "up-sell", "cross-sell", "cross sell",
    "convert enquiries", "convert inquiries", "convert leads", "convert prospects", "convert interest",
    "conversion target", "conversion targets", "warm leads", "warm enquiries", "warm inquiries",
    "inbound sales", "outbound sales", "outbound calls", "outbound calling", "telesales",
    "telephone sales", "cold calling", "new business", "book appointments", "appointment setting",
    "lead generation", "sales pipeline", "close sales", "closing sales", "close deals", "closing deals",
    "booked and paid", "retention target", "renewal target", "renewals", "retain customers",
    "increase membership", "sales experience", "sales role", "selling", "revenue growth",
    "account growth", "grow accounts", "business growth",
]

OFFICE_DIGITAL_EVIDENCE = [
    "office", "office-based", "office based", "hybrid", "remote", "home-based", "home based",
    "phone", "telephone", "contact centre", "contact center", "call centre", "call center",
    "crm", "inbound", "outbound", "email",
]

TITLE_EXCLUDES = [
    "field sales", "door to door", "door-to-door", "territory sales", "area sales", "regional sales",
    "sales manager", "business development manager", "head of sales", "sales director",
    "technical sales", "sales engineer", "sales engineering", "product sales engineer",
    "product sales executive", "car sales", "vehicle sales", "showroom", "retail sales",
    "estate agent", "lettings negotiator", "sales negotiator", "sales administrator",
    "sales administration", "sales support", "sales ledger",
    "strategic customer success manager", "enterprise customer success manager",
    "senior customer success manager", "senior sales executive", "senior sales consultant",
    "national account manager", "key account manager", "strategic account manager",
    "enterprise account manager", "senior account manager", "technical account manager",
    "field account manager", "area account manager", "regional account manager",
    "service advisor - automotive", "service adviser - automotive", "automotive service advisor",
    "automotive service adviser", "aftersales advisor", "aftersales adviser",
]

DESCRIPTION_EXCLUDES = [
    "door to door", "door-to-door", "event-based campaigns", "face-to-face sales environments",
    "travel to different campaign locations", "subcontracted basis", "self-employed", "self employed",
    "commission-only", "commission only",
]

ACCOUNT_EXCLUDES = [
    "field sales", "field-based", "field based", "territory", "door to door", "door-to-door",
    "commercial insurance", "insurance broker", "insurance brokerage", "underwriting",
    "pensions", "wealth management", "financial adviser", "financial advisor",
    "automotive", "motor trade", "car dealership", "medical device", "pharmaceutical",
]

AREA_UNUSABLE = {"", "not specified", "unknown"}


def contains_any(text: str, terms: list[str]) -> list[str]:
    return [term for term in terms if term in text]


def canonical_region(cluster: str) -> str:
    value = norm(cluster)
    if value.startswith("North East - "):
        return "North East"
    return value or "Other / Unknown"


def load_geo() -> tuple[dict[str, str], dict[str, str]]:
    area_df = pd.read_excel(GEO_PATH, dtype=str).fillna("")
    if not {"Area", "Cluster"}.issubset(area_df.columns):
        raise SystemExit("STOP: geo lookup needs Area and Cluster columns")
    area_lookup: dict[str, str] = {}
    for _, row in area_df.iterrows():
        area = norm_key(row.get("Area"))
        cluster = canonical_region(row.get("Cluster"))
        if area and cluster:
            area_lookup[area] = cluster

    fallback_lookup: dict[str, str] = {}
    try:
        fallback = pd.read_excel(GEO_PATH, sheet_name="LocationFallback", dtype=str).fillna("")
    except ValueError:
        fallback = pd.DataFrame()
    if {"Status", "Location", "Cluster"}.issubset(fallback.columns):
        for _, row in fallback.iterrows():
            if norm_key(row.get("Status")) != "auto":
                continue
            location = norm_key(row.get("Location"))
            cluster = canonical_region(row.get("Cluster"))
            if location and cluster:
                fallback_lookup[location] = cluster
    return area_lookup, fallback_lookup


def resolve_region(area: Any, location: Any, area_lookup: dict[str, str], fallback_lookup: dict[str, str]) -> str:
    area_key = norm_key(area)
    if area_key not in AREA_UNUSABLE:
        return area_lookup.get(area_key, "Other / Unknown")
    location_key = norm_key(location)
    if location_key in AREA_UNUSABLE:
        return "Other / Unknown"
    return fallback_lookup.get(location_key, "Other / Unknown")


def broad_possible(title: str) -> bool:
    t = norm_key(title)
    return bool(contains_any(t, BROAD_TITLE_TERMS))


def scope_decision(title: str, description: str) -> tuple[bool, str, str]:
    t = norm_key(title)
    d = norm_key(description)
    combined = f"{t} {d}"

    title_ex = contains_any(t, TITLE_EXCLUDES)
    if title_ex:
        return False, "OUT_TITLE", "excluded title: " + ", ".join(title_ex[:3])

    desc_ex = contains_any(d, DESCRIPTION_EXCLUDES)
    if desc_ex:
        return False, "OUT_FIELD_CAMPAIGN", "field/event/self-employed signal: " + ", ".join(desc_ex[:3])

    account = contains_any(t, ACCOUNT_TITLE_TERMS)
    if account:
        account_ex = contains_any(combined, ACCOUNT_EXCLUDES)
        if account_ex:
            return False, "OUT_ACCOUNT_SPECIALIST", "account role specialist/field signal: " + ", ".join(account_ex[:3])
        sales = contains_any(combined, STRONG_SALES_EVIDENCE)
        office = contains_any(combined, OFFICE_DIGITAL_EVIDENCE)
        if sales and office:
            return True, "IN_ACCOUNT_SALES", "account role with sales + office/digital evidence"
        return False, "OUT_ACCOUNT_AMBIGUOUS", "account role lacks both strong sales and office/digital evidence"

    direct = contains_any(t, DIRECT_TITLE_TERMS)
    if direct:
        return True, "IN_DIRECT", "sales-led title: " + ", ".join(direct[:3])

    customer = contains_any(t, CUSTOMER_TITLE_TERMS)
    if customer:
        sales = contains_any(combined, STRONG_SALES_EVIDENCE)
        if sales:
            return True, "IN_CUSTOMER_SALES", "customer/service title with sales evidence: " + ", ".join(sales[:3])
        return False, "OUT_PURE_SERVICE", "customer/service title without strong sales/conversion evidence"

    return False, "OUT_OTHER_SALES", "broad sales/business-development title outside Customer Sales seam"


def normalize_campaign_text(value: Any) -> str:
    text = norm_key(value)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\b\d{4,}\b", "#", text)
    text = re.sub(r"[^a-z0-9£%+#]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def campaign_key(region: str, employer: str, description: str, title: str) -> str:
    desc = normalize_campaign_text(description)
    if len(desc) >= 120:
        basis = f"{norm_key(region)}|{norm_key(employer)}|{desc}"
    else:
        basis = f"{norm_key(region)}|{norm_key(employer)}|{norm_key(title)}|{desc}"
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def pct(n: int, d: int) -> str:
    return f"{(100.0*n/d):.1f}%" if d else "0.0%"


def main() -> None:
    if not INPUT_PATH.exists():
        raise SystemExit(f"STOP: missing {INPUT_PATH}")
    if not GEO_PATH.exists():
        raise SystemExit(f"STOP: missing {GEO_PATH}")

    df = pd.read_excel(INPUT_PATH, dtype=str).fillna("")
    required = [COL["job_id"], COL["title"], COL["advertiser_name"], COL["area"], COL["location"], COL["description"]]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise SystemExit("STOP: missing JobG8 columns: " + ", ".join(missing))

    area_lookup, fallback_lookup = load_geo()
    detail_rows: list[dict[str, Any]] = []

    for _, row in df.iterrows():
        title = norm(row.get(COL["title"]))
        if not title or not broad_possible(title):
            continue
        description = norm(row.get(COL["description"]))
        employer = norm(row.get(COL["advertiser_name"])) or "Unknown company"
        region = resolve_region(row.get(COL["area"]), row.get(COL["location"]), area_lookup, fallback_lookup)
        in_scope, decision, reason = scope_decision(title, description)
        key = campaign_key(region, employer, description, title) if in_scope else ""
        detail_rows.append({
            "job_id": norm(row.get(COL["job_id"])),
            "title": title,
            "employer": employer,
            "area": norm(row.get(COL["area"])),
            "location": norm(row.get(COL["location"])),
            "region": region,
            "in_ontap_33": region in ONTAP_33,
            "broad_possible": True,
            "in_scope": in_scope,
            "decision": decision,
            "decision_reason": reason,
            "campaign_key": key,
            "description": description,
        })

    detail = pd.DataFrame(detail_rows)
    if detail.empty:
        raise SystemExit("STOP: broad Customer Sales discovery matched zero jobs")

    # Dedupe only within a region. If one genuine national campaign appears in two
    # different regions it may still legitimately contribute one listing to each.
    detail["campaign_representative"] = False
    scoped = detail[detail["in_scope"]].copy()
    representative_indices = scoped.groupby("campaign_key", sort=False).head(1).index
    detail.loc[representative_indices, "campaign_representative"] = True

    region_rows: list[dict[str, Any]] = []
    regions = sorted(set(ONTAP_33) | set(detail["region"].astype(str)))
    for region in regions:
        g = detail[detail["region"] == region]
        in_scope = g[g["in_scope"]]
        unique = in_scope[in_scope["campaign_representative"]]
        employer_counts = unique["employer"].value_counts()
        top_employer = str(employer_counts.index[0]) if len(employer_counts) else ""
        top_count = int(employer_counts.iloc[0]) if len(employer_counts) else 0
        region_rows.append({
            "region": region,
            "in_ontap_33": region in ONTAP_33,
            "raw_broad_possibles": len(g),
            "in_scope_rows": len(in_scope),
            "campaign_deduped_jobs": len(unique),
            "duplicate_campaign_rows_removed": len(in_scope) - len(unique),
            "unique_employers": int(unique["employer"].nunique()),
            "top_employer": top_employer,
            "top_employer_jobs": top_count,
        })

    region_df = pd.DataFrame(region_rows)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    detail.to_csv(DETAIL_CSV_PATH, index=False)
    region_df.to_csv(REGION_CSV_PATH, index=False)

    total_feed = len(df)
    broad_total = len(detail)
    scoped_total = int(detail["in_scope"].sum())
    unique_total = int(detail["campaign_representative"].sum())

    d33 = detail[detail["in_ontap_33"]]
    broad_33 = len(d33)
    scoped_33 = int(d33["in_scope"].sum())
    unique_33 = int(d33["campaign_representative"].sum())

    outside = detail[(~detail["in_ontap_33"]) & (detail["region"] != "Other / Unknown")]
    unknown = detail[detail["region"] == "Other / Unknown"]

    exclusion_counts = Counter(detail.loc[~detail["in_scope"], "decision"].astype(str))

    campaigns = (
        detail[detail["in_scope"]]
        .groupby(["campaign_key", "region", "employer"], as_index=False)
        .agg(rows=("job_id", "size"), titles=("title", lambda s: "; ".join(sorted(set(s))[:3])))
    )
    campaigns = campaigns[campaigns["rows"] > 1].sort_values(["rows", "region"], ascending=[False, True])

    r33 = region_df[region_df["in_ontap_33"]].copy()
    r33 = r33.sort_values(["campaign_deduped_jobs", "in_scope_rows", "raw_broad_possibles"], ascending=False)
    outside_regions = region_df[(~region_df["in_ontap_33"]) & (region_df["region"] != "Other / Unknown")].copy()
    outside_regions = outside_regions[outside_regions["raw_broad_possibles"] > 0]
    outside_regions = outside_regions.sort_values(["campaign_deduped_jobs", "raw_broad_possibles"], ascending=False)

    lines: list[str] = []
    lines.append("# Customer Sales national reconciliation")
    lines.append("")
    lines.append("Branch-only diagnostic. Nothing here is live/published.")
    lines.append("")
    lines.append("## Funnel")
    lines.append("")
    lines.append("| Stage | All mapped/unknown rows | Ontap 33 regions |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Current JobG8 feed | {total_feed:,} | — |")
    lines.append(f"| Broad Sales / Business Development possibles | {broad_total:,} | {broad_33:,} |")
    lines.append(f"| In-scope Customer Sales rows | {scoped_total:,} ({pct(scoped_total, broad_total)} of broad) | {scoped_33:,} ({pct(scoped_33, broad_33)} of broad) |")
    lines.append(f"| Campaign/dedupe-adjusted regional jobs | {unique_total:,} | {unique_33:,} |")
    lines.append("")
    lines.append(f"Broad possibles outside the current Ontap 33 but mapped to another region: **{len(outside):,}**. Broad possibles with unknown geography: **{len(unknown):,}**.")
    lines.append("")
    lines.append("**Important:** campaign dedupe is deliberately regional. The same national campaign may count once in each genuinely relevant region, but repeated near-identical JobG8 rows inside one region count once.")
    lines.append("")
    lines.append("## Ontap 33 — regional reconciliation")
    lines.append("")
    lines.append("| Region | Broad possibles | In scope | After campaign/dedupe | Employers | Top employer |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for _, row in r33.iterrows():
        top = str(row["top_employer"])
        if top:
            top = f"{top} ({int(row['top_employer_jobs'])})"
        lines.append(
            f"| {row['region']} | {int(row['raw_broad_possibles'])} | {int(row['in_scope_rows'])} | "
            f"{int(row['campaign_deduped_jobs'])} | {int(row['unique_employers'])} | {top} |"
        )

    lines.append("")
    lines.append("## Main reasons broad possibles fall out")
    lines.append("")
    lines.append("| Rule-out bucket | Rows |")
    lines.append("|---|---:|")
    for reason, count in exclusion_counts.most_common():
        lines.append(f"| {reason} | {count} |")

    if not campaigns.empty:
        lines.append("")
        lines.append("## Largest repeated campaign groups")
        lines.append("")
        lines.append("| Region | Employer | Repeated rows | Example title(s) |")
        lines.append("|---|---|---:|---|")
        for _, row in campaigns.head(20).iterrows():
            lines.append(f"| {row['region']} | {row['employer']} | {int(row['rows'])} | {row['titles']} |")

    if not outside_regions.empty:
        lines.append("")
        lines.append("## Mapped regions outside the current Ontap 33")
        lines.append("")
        lines.append("| Region | Broad possibles | In scope | After campaign/dedupe |")
        lines.append("|---|---:|---:|---:|")
        for _, row in outside_regions.head(30).iterrows():
            lines.append(f"| {row['region']} | {int(row['raw_broad_possibles'])} | {int(row['in_scope_rows'])} | {int(row['campaign_deduped_jobs'])} |")

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The broad headline should not be treated as publishable inventory. The decision point for a third Ontap family is the campaign/dedupe-adjusted regional column, plus employer breadth and manual QA of the largest slices.")

    MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Feed rows: {total_feed}")
    print(f"Broad possibles: {broad_total}")
    print(f"In-scope rows: {scoped_total}")
    print(f"Campaign/dedupe-adjusted regional jobs: {unique_total}")
    print(f"Ontap 33 broad/in-scope/deduped: {broad_33}/{scoped_33}/{unique_33}")
    print(f"Wrote {MD_PATH}")
    print(f"Wrote {REGION_CSV_PATH}")
    print(f"Wrote {DETAIL_CSV_PATH}")


if __name__ == "__main__":
    main()
