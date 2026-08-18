"""Branch-only Customer Sales / Sales Advisor family benchmark.

Reproduces the earlier discovery definition: genuine office/contact-centre/home/hybrid
selling, conversion, retention and renewal roles. A job may also belong to Service
Admin; overlap is explicitly allowed.
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
    "Northern Ireland - East": "northern-ireland-east.json",
    "Cheshire - Warrington & Halton": "warrington-halton.json",
    "Cornwall": "cornwall.json",
    "Yorkshire - South": "south-yorkshire.json",
}

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

# Broad doorway used in the original discovery: do not require one exact title variant.
CUSTOMER_TITLE_TERMS = [
    "customer service", "customer care", "customer support", "customer advisor", "customer adviser",
    "customer representative", "customer account", "customer success", "client service", "client services",
    "client advisor", "client adviser", "call centre", "call center", "contact centre", "contact center",
    "membership advisor", "membership adviser",
]

SALES_EVIDENCE_TERMS = [
    "commission", "uncapped commission", "sales target", "sales targets", "sales kpi", "sales kpis",
    "sales opportunity", "sales opportunities", "upsell", "up-sell", "cross-sell", "cross sell",
    "convert enquiries", "convert inquiries", "convert leads", "convert prospects", "convert interest",
    "conversion target", "conversion targets", "warm leads", "warm enquiries", "warm inquiries",
    "inbound sales", "outbound sales", "outbound calls", "outbound calling", "telesales",
    "telephone sales", "cold calling", "new business", "book appointments", "appointment setting",
    "lead generation", "sales pipeline", "close sales", "closing sales", "close deals", "closing deals",
    "booked and paid", "retention target", "renewal target", "renewals", "retain customers",
    "increase membership", "sales experience", "sales role", "selling",
]

HARD_EXCLUDE_TERMS = [
    "field sales", "door to door", "door-to-door", "territory sales", "area sales", "regional sales",
    "sales manager", "business development manager", "head of sales", "sales director",
    "technical sales", "sales engineer", "sales engineering", "product sales engineer",
    "car sales", "vehicle sales", "showroom", "retail sales", "estate agent", "lettings negotiator",
    "sales negotiator", "sales administrator", "sales administration", "sales support",
    "sales ledger", "account manager", "account executive",
    "service advisor - automotive", "service adviser - automotive", "automotive service advisor",
    "automotive service adviser", "aftersales advisor", "aftersales adviser",
]

REQUIRED_COLUMNS = [
    COL["job_id"], COL["title"], COL["advertiser_name"], COL["advertiser_type"],
    COL["employment_type"], COL["area"], COL["location"], COL["apply_url"], COL["description"],
]


def contains_any(text: str, terms: list[str]) -> list[str]:
    return [term for term in terms if term in text]


def classify(title: str, description: str) -> tuple[str, str] | None:
    t = norm_key(title)
    d = norm_key(description)
    combined = f"{t} {d}"

    hard = contains_any(t, HARD_EXCLUDE_TERMS)
    if hard:
        return None

    direct = contains_any(t, DIRECT_TITLE_TERMS)
    if direct:
        return "DIRECT_SALES", "sales-led title: " + ", ".join(direct[:3])

    customer = contains_any(t, CUSTOMER_TITLE_TERMS)
    if customer:
        evidence = contains_any(combined, SALES_EVIDENCE_TERMS)
        if evidence:
            return "CUSTOMER_SALES", "customer/service role with sales evidence: " + ", ".join(evidence[:3])

    return None


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
            if location and location not in {"not specified", "unknown"} and cluster in TARGETS:
                fallback_lookup[location] = cluster

    return area_lookup, fallback_lookup


def resolve_region(area: Any, location: Any, area_lookup: dict[str, str], fallback_lookup: dict[str, str]) -> str:
    area_key = norm_key(area)
    if area_key not in {"", "not specified", "unknown"}:
        return area_lookup.get(area_key, "")
    location_key = norm_key(location)
    if location_key in {"", "not specified", "unknown"}:
        return ""
    return fallback_lookup.get(location_key, "")


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

        result = classify(title, raw_description)
        if not result:
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
        jobs = sorted(outputs[region], key=lambda job: (
            0 if job.get("customer_sales_classification") == "DIRECT_SALES" else 1,
            str(job.get("title", "")).lower(), str(job.get("location", "")).lower(),
        ))
        (OUTPUT_DIR / filename).write_text(json.dumps(jobs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        employers = {norm_key(job.get("advertiser_name")) for job in jobs if norm_key(job.get("advertiser_name"))}
        print(f"{region}: {len(jobs)} jobs / {len(employers)} employers")


if __name__ == "__main__":
    main()
