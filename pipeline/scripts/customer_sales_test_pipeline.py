"""Branch-only Customer Sales / Sales Advisor discovery test.

Reads the current raw JobG8 XLSX and writes three inspection-only JSON files,
plus a near-miss audit. This module is deliberately separate from live family
pipelines.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from scripts.service_admin_pipeline_core import (
    COL,
    clean_description,
    clean_record_strings,
    format_number,
    get_posted_date,
    build_company,
    build_salary_details,
    norm,
    norm_key,
    read_xlsx_sheet,
)

INPUT_PATH = Path("input/jobg8.xlsx")
GEO_PATH = Path("geo/geo_lookup.xlsx")
OUTPUT_DIR = Path("output-customer-sales-test")

TARGETS = {
    "Hampshire": "hampshire.json",
    "Greater Manchester - Manchester & Salford": "manchester-salford.json",
    "Yorkshire - West": "west-yorkshire.json",
}

# Titles that are intrinsically sales-led enough to qualify without needing the
# advert to repeat sales language. Field/retail/management exclusions still win.
STRONG_TITLE_TERMS = [
    "sales advisor", "sales adviser", "customer sales", "sales consultant",
    "telesales", "inside sales", "inbound sales", "outbound sales",
    "sales agent", "telephone sales", "retention advisor", "retention adviser",
    "renewals advisor", "renewals adviser", "new business advisor", "new business adviser",
    "telemarketer", "telemarketing", "appointment setter", "lead generator",
]

# Ambiguous titles which qualify only where the advert contains BOTH genuine
# sales evidence and an office/contact-centre/home signal.
CONTEXT_TITLE_TERMS = [
    "customer service advisor", "customer service adviser", "customer advisor", "customer adviser",
    "customer service representative", "customer representative", "customer account advisor",
    "customer account adviser", "client advisor", "client adviser", "call centre agent",
    "call center agent", "call centre operator", "call center operator", "contact centre agent",
    "contact center agent", "contact centre advisor", "contact centre adviser",
    "customer success advisor", "customer success adviser", "membership advisor", "membership adviser",
    "sales executive", "business development executive", "new business executive",
    "commercial executive", "account executive",
]

# Evidence must point to an actual selling/conversion responsibility. Generic
# performance bonuses are intentionally NOT sufficient evidence.
SALES_EVIDENCE_TERMS = [
    "sales target", "sales targets", "sales opportunity", "sales opportunities",
    "convert enquiries", "convert inquiries", "convert leads", "convert prospects",
    "conversion target", "conversion targets", "upsell", "up-sell", "cross-sell", "cross sell",
    "warm leads", "warm enquiries", "warm inquiries", "qualified leads", "sales leads",
    "outbound sales", "inbound sales", "telesales", "telephone sales", "cold calling",
    "new business", "generate revenue", "revenue target", "revenue targets",
    "booked and paid", "close sales", "closing sales", "close deals", "closing deals",
    "achieve sales", "meet sales", "hit sales", "sales pipeline", "sales performance",
    "commission", "uncapped commission", "sales commission",
]

OFFICE_EVIDENCE_TERMS = [
    "contact centre", "contact center", "call centre", "call center", "office based", "office-based",
    "telephone", "phone", "inbound", "outbound", "hybrid", "work from home", "working from home", "remote",
    "crm", "customer relationship management",
]

# These exclusions are about the nature of the job, not overlap with Service
# Admin. Sales administration/support remains excluded because it supports sales
# rather than being personally sales-led.
HARD_EXCLUDE_TERMS = [
    "field sales", "door to door", "door-to-door", "territory sales", "area sales", "regional sales",
    "car sales", "vehicle sales", "showroom", "retail sales", "sales administrator", "sales administration",
    "sales support administrator", "sales ledger", "business development manager", "account manager", "sales manager",
    "estate agent", "lettings negotiator", "sales negotiator",
    "service advisor - automotive", "service adviser - automotive", "automotive service advisor",
    "automotive service adviser", "aftersales advisor", "aftersales adviser",
]

# Broad vocabulary used only for the audit. It does not select jobs; it catches
# plausible rejected roles so we can inspect what the classifier is missing.
AUDIT_TITLE_TERMS = [
    "sales", "customer", "client", "contact centre", "contact center", "call centre", "call center",
    "retention", "renewal", "new business", "business development", "commercial", "lead", "appointment",
    "membership", "account executive", "telemarket",
]

REQUIRED_COLUMNS = [
    COL["job_id"], COL["title"], COL["advertiser_name"], COL["advertiser_type"],
    COL["employment_type"], COL["area"], COL["location"], COL["apply_url"], COL["description"],
]


def contains_any(text: str, terms: list[str]) -> list[str]:
    return [term for term in terms if term in text]


def classify_with_reason(title: str, description: str) -> tuple[tuple[str, str] | None, str]:
    t = norm_key(title)
    d = norm_key(description)
    combined = f"{t} {d}"

    hard = contains_any(t, HARD_EXCLUDE_TERMS)
    if hard:
        return None, "hard exclude: " + ", ".join(hard)

    strong = contains_any(t, STRONG_TITLE_TERMS)
    if strong:
        return ("HIGH_CONFIDENCE", "strong sales-led title: " + ", ".join(strong)), "selected"

    contextual = contains_any(t, CONTEXT_TITLE_TERMS)
    if not contextual:
        return None, "no Customer Sales title match"

    sales = contains_any(combined, SALES_EVIDENCE_TERMS)
    office = contains_any(combined, OFFICE_EVIDENCE_TERMS)
    if sales and office:
        return (
            "CONTEXT_SALES",
            "customer/sales-adjacent title with sales evidence (" + ", ".join(sales[:3]) + ")",
        ), "selected"
    if not sales and not office:
        return None, "context title but no sales or office/contact-centre evidence"
    if not sales:
        return None, "context title but no genuine sales/conversion evidence"
    return None, "context title has sales evidence but no office/contact-centre/home evidence"


def load_geo() -> tuple[dict[str, str], dict[str, str]]:
    geo = read_xlsx_sheet(GEO_PATH).fillna("")
    if not {"Area", "Cluster"}.issubset(geo.columns):
        raise SystemExit("STOP: geo lookup needs Area and Cluster columns")

    area_lookup: dict[str, str] = {}
    for _, row in geo.iterrows():
        area = norm_key(row.get("Area"))
        cluster = norm(row.get("Cluster"))
        if area and cluster in TARGETS:
            area_lookup[area] = cluster

    fallback_df = read_xlsx_sheet(GEO_PATH, sheet_name="LocationFallback").fillna("")
    fallback_lookup: dict[str, str] = {}
    if {"Status", "Location", "Cluster"}.issubset(fallback_df.columns):
        for _, row in fallback_df.iterrows():
            if norm_key(row.get("Status")) != "auto":
                continue
            location = norm_key(row.get("Location"))
            cluster = norm(row.get("Cluster"))
            if location and cluster in TARGETS:
                fallback_lookup[location] = cluster

    return area_lookup, fallback_lookup


def resolve_region(area: Any, location: Any, area_lookup: dict[str, str], fallback_lookup: dict[str, str]) -> str:
    area_key = norm_key(area)
    if area_key not in {"", "not specified", "unknown"}:
        return area_lookup.get(area_key, "")
    return fallback_lookup.get(norm_key(location), "")


def main() -> None:
    if not INPUT_PATH.exists():
        raise SystemExit(f"STOP: missing {INPUT_PATH}")
    if not GEO_PATH.exists():
        raise SystemExit(f"STOP: missing {GEO_PATH}")

    df = pd.read_excel(INPUT_PATH, dtype=str).fillna("")
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise SystemExit("STOP: missing JobG8 columns: " + ", ".join(missing))

    area_lookup, fallback_lookup = load_geo()
    outputs: dict[str, list[dict[str, Any]]] = {region: [] for region in TARGETS}
    seen: dict[str, set[str]] = {region: set() for region in TARGETS}
    audit: list[dict[str, Any]] = []
    df_columns = list(df.columns)

    for _, row in df.iterrows():
        region = resolve_region(row.get(COL["area"]), row.get(COL["location"]), area_lookup, fallback_lookup)
        if region not in TARGETS:
            continue

        job_id = norm(row.get(COL["job_id"]))
        title = norm(row.get(COL["title"]))
        apply_url = norm(row.get(COL["apply_url"]))
        raw_description = norm(row.get(COL["description"]))
        if not job_id or not title or not raw_description or not apply_url.lower().startswith("http"):
            continue
        if job_id in seen[region]:
            continue

        result, rejection_reason = classify_with_reason(title, raw_description)
        if not result:
            title_key = norm_key(title)
            if contains_any(title_key, AUDIT_TITLE_TERMS):
                audit.append({
                    "job_id": job_id,
                    "title": title,
                    "advertiser_name": norm(row.get(COL["advertiser_name"])),
                    "location": norm(row.get(COL["area"])) or norm(row.get(COL["location"])),
                    "region": region,
                    "rejection_reason": rejection_reason,
                    "description_preview": clean_description(raw_description)[:700],
                    "apply_url": apply_url,
                })
            continue
        classification, reason = result

        description = clean_description(raw_description)
        salary_text, _salary_source = build_salary_details(row)
        item = clean_record_strings({
            "job_id": job_id,
            "title": title,
            "company": build_company(row),
            "advertiser_name": norm(row.get(COL["advertiser_name"])),
            "advertiser_type": norm(row.get(COL["advertiser_type"])),
            "location": norm(row.get(COL["area"])) or norm(row.get(COL["location"])),
            "region": region,
            "country": "UK",
            "category": "Customer Sales / Sales Advisor",
            "employment_type": norm(row.get(COL["employment_type"])),
            "salary_min": format_number(row.get(COL["salary_min"])),
            "salary_max": format_number(row.get(COL["salary_max"])),
            "salary_text": salary_text,
            "posted_date": get_posted_date(row, df_columns),
            "description": description,
            "apply_url": apply_url,
            "source": "JobG8",
            "customer_sales_classification": classification,
            "customer_sales_reason": reason,
        })
        outputs[region].append(item)
        seen[region].add(job_id)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for region, filename in TARGETS.items():
        jobs = sorted(
            outputs[region],
            key=lambda job: (
                0 if job.get("customer_sales_classification") == "HIGH_CONFIDENCE" else 1,
                str(job.get("title", "")).lower(),
                str(job.get("location", "")).lower(),
            ),
        )
        (OUTPUT_DIR / filename).write_text(json.dumps(jobs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{region}: {len(jobs)} Customer Sales test candidates")

    audit = sorted(audit, key=lambda row: (row["region"], row["title"].lower(), row["location"].lower()))
    (OUTPUT_DIR / "near-miss-audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Near-miss audit: {len(audit)} rejected plausible titles")


if __name__ == "__main__":
    main()
