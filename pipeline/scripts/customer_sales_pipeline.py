"""Generate LIVE Customer Sales / Sales Advisor slices from the current JobG8 feed.

Governed boundary:
- genuine sales-led office/contact-centre/home/hybrid roles;
- customer/service roles only with explicit sales/conversion evidence;
- Account Manager / Account Executive roles only with strong sales plus office/digital evidence;
- Sales + Service Admin overlap is valid and never an exclusion reason;
- field/in-home/event/self-employed, automotive dealership, retail/property and senior/specialist
  roles are excluded;
- campaign duplicates within a region are collapsed to one representative job.

Only region/category pairs marked LIVE in region_category_slice_register.csv are generated.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

from .service_admin_pipeline_core import (
    COL,
    build_company,
    build_salary_details,
    clean_description,
    clean_record_strings,
    format_number,
    get_posted_date,
    norm,
    norm_key,
)
from .slice_catalog import category_meta, output_filename
from .slice_registry import live_slices

CATEGORY = "customer_sales"
INPUT_PATH = Path("input/jobg8.xlsx")
GEO_PATH = Path("geo/geo_lookup.xlsx")
AREA_UNUSABLE = {"", "not specified", "unknown"}

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

SALES_EVIDENCE = [
    "commission", "uncapped commission", "sales target", "sales targets", "sales kpi", "sales kpis",
    "sales opportunity", "sales opportunities", "upsell", "up-sell", "cross-sell", "cross sell",
    "convert enquiries", "convert inquiries", "convert leads", "convert prospects", "convert interest",
    "conversion target", "conversion targets", "warm leads", "warm enquiries", "warm inquiries",
    "inbound sales", "outbound sales", "outbound calls", "outbound calling", "telesales",
    "telephone sales", "cold calling", "new business", "book appointments", "appointment setting",
    "lead generation", "sales pipeline", "close sales", "closing sales", "close deals", "closing deals",
    "booked and paid", "retention target", "renewal target", "renewals", "retain customers",
    "increase membership", "sales experience", "sales role", "selling", "revenue growth",
    "grow revenue", "account growth", "grow accounts", "business growth",
]

# Remove explicit negations before looking for contextual sales evidence. This avoids
# a pure service advert qualifying merely because it says e.g. "no selling responsibility".
NEGATED_SALES_PHRASES = [
    "no selling", "not a sales role", "not a sales position", "no sales targets",
    "non-sales role", "non sales role", "no sales responsibility", "no sales responsibilities",
]

OFFICE_EVIDENCE = [
    "office", "office-based", "office based", "hybrid", "remote", "home-based", "home based",
    "phone", "telephone", "crm", "inbound", "outbound", "email", "contact centre",
    "contact center", "call centre", "call center",
]

HARD_TITLE_EXCLUDES = [
    "field sales", "door to door", "door-to-door", "territory sales", "area sales", "regional sales",
    "sales manager", "business development manager", "head of sales", "sales director",
    "technical sales", "sales engineer", "sales engineering", "product sales engineer",
    "product sales executive", "senior sales executive", "senior sales consultant",
    "car sales", "vehicle sales", "showroom", "retail sales", "estate agent", "lettings negotiator",
    "sales negotiator", "sales administrator", "sales administration", "sales support", "sales ledger",
    "conservatory sales", "new homes sales", "service advisor - automotive", "service adviser - automotive",
    "automotive service advisor", "automotive service adviser", "aftersales advisor", "aftersales adviser",
]

CUSTOMER_TITLE_EXCLUDES = [
    "strategic customer success manager", "enterprise customer success manager",
    "senior customer success manager", "client services manager", "client service manager",
]

ACCOUNT_TITLE_TERMS = ["account manager", "account executive"]
ACCOUNT_EXCLUDES = [
    "field account manager", "field-based", "field based", "field sales", "territory",
    "area account manager", "regional account manager", "door to door", "door-to-door",
    "technical account manager", "enterprise account manager", "strategic account manager",
    "senior account manager", "national account manager", "key account manager",
    "commercial insurance", "insurance broker", "insurance brokerage", "underwriting",
    "pensions", "wealth management", "financial adviser", "financial advisor",
    "automotive", "motor trade", "car dealership", "medical device", "pharmaceutical",
]

DESCRIPTION_EXCLUDES = [
    "door to door", "door-to-door", "event-based campaigns", "face-to-face sales environments",
    "travel to different campaign locations", "subcontracted basis", "self-employed", "self employed",
    "commission-only", "commission only", "in-home consultation", "in home consultation",
    "visit customers in their homes", "visit customers at home", "travel time from your home postcode",
    "kitchen makeover", "kitchen transformation", "home improvement campaign",
]

AUTOMOTIVE_CONTEXT_EXCLUDES = [
    "car dealership", "vehicle dealership", "motor dealership", "motor group", "car dealer",
    "vehicle dealer", "main dealership", "franchised dealership", "buying their car",
    "buying a new car", "buying a used car", "new & used vehicles", "new and used vehicles",
    "used car sales", "new car sales", "vehicle presentations", "test drives",
]

RETAIL_PROPERTY_EXCLUDES = [
    "luxury retail", "retail environment", "shop floor", "estate agency", "house builder",
    "new homes development",
]

SPECIALIST_CUSTOMER_CONTEXT_EXCLUDES = [
    "wealth management", "investment management", "private banking", "institutional client",
]


def contains_any(text: str, terms: list[str]) -> list[str]:
    return [term for term in terms if term in text]


def evidence_text_without_negations(text: str) -> str:
    cleaned = text
    for phrase in NEGATED_SALES_PHRASES:
        cleaned = cleaned.replace(phrase, " ")
    return re.sub(r"\s+", " ", cleaned).strip()


def canonical_region(value: Any) -> str:
    region = norm(value)
    if region.startswith("North East - "):
        return "North East"
    return region


def load_geo() -> tuple[dict[str, str], dict[str, str]]:
    geo = pd.read_excel(GEO_PATH, dtype=str).fillna("")
    if not {"Area", "Cluster"}.issubset(geo.columns):
        raise SystemExit("STOP: geo lookup requires Area and Cluster columns")
    area_lookup = {
        norm_key(row.get("Area")): canonical_region(row.get("Cluster"))
        for _, row in geo.iterrows()
        if norm_key(row.get("Area")) and canonical_region(row.get("Cluster"))
    }

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
            region = canonical_region(row.get("Cluster"))
            if location and location not in AREA_UNUSABLE and region:
                fallback_lookup[location] = region
    return area_lookup, fallback_lookup


def resolve_region(area: Any, location: Any, area_lookup: dict[str, str], fallback_lookup: dict[str, str]) -> str:
    area_key = norm_key(area)
    if area_key not in AREA_UNUSABLE:
        return area_lookup.get(area_key, "")
    location_key = norm_key(location)
    if location_key in AREA_UNUSABLE:
        return ""
    return fallback_lookup.get(location_key, "")


def classify(title: str, description: str, employer: str) -> tuple[str, str] | None:
    t = norm_key(title)
    d = norm_key(description)
    e = norm_key(employer)
    combined = f"{t} {d}"
    context = f"{t} {d} {e}"
    sales_evidence_text = evidence_text_without_negations(combined)

    if contains_any(t, HARD_TITLE_EXCLUDES):
        return None
    if contains_any(d, DESCRIPTION_EXCLUDES):
        return None
    if contains_any(context, AUTOMOTIVE_CONTEXT_EXCLUDES):
        return None
    if contains_any(d, RETAIL_PROPERTY_EXCLUDES):
        return None

    if t == "customer engagement executive":
        return "CUSTOMER_SALES", "owner-approved exact customer-sales title"

    if contains_any(t, ACCOUNT_TITLE_TERMS):
        if contains_any(combined, ACCOUNT_EXCLUDES):
            return None
        if contains_any(sales_evidence_text, SALES_EVIDENCE) and contains_any(combined, OFFICE_EVIDENCE):
            return "CONDITIONAL_ACCOUNT_SALES", "account-based title with sales and office/digital evidence"
        return None

    direct = contains_any(t, DIRECT_TITLE_TERMS)
    if direct:
        return "DIRECT_SALES", "sales-led title: " + ", ".join(direct[:3])

    customer = contains_any(t, CUSTOMER_TITLE_TERMS)
    if customer:
        if contains_any(t, CUSTOMER_TITLE_EXCLUDES):
            return None
        if contains_any(combined, SPECIALIST_CUSTOMER_CONTEXT_EXCLUDES):
            return None
        evidence = contains_any(sales_evidence_text, SALES_EVIDENCE)
        if evidence:
            return "CUSTOMER_SALES", "customer/service role with sales evidence: " + ", ".join(evidence[:3])
    return None


def campaign_key(region: str, employer: str, description: str, title: str) -> str:
    text = norm_key(description)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\b\d{4,}\b", "#", text)
    text = re.sub(r"[^a-z0-9£%+#]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) >= 120:
        basis = f"{norm_key(region)}|{norm_key(employer)}|{text}"
    else:
        basis = f"{norm_key(region)}|{norm_key(employer)}|{norm_key(title)}|{text}"
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    active_regions = sorted(region for region, category in live_slices() if category == CATEGORY)
    if not active_regions:
        print("Customer Sales slices: none LIVE; nothing to generate")
        return 0
    if not INPUT_PATH.exists():
        raise SystemExit(f"STOP: missing {INPUT_PATH}")
    if not GEO_PATH.exists():
        raise SystemExit(f"STOP: missing {GEO_PATH}")

    feed = pd.read_excel(INPUT_PATH, dtype=str).fillna("")
    required = [
        COL["job_id"], COL["title"], COL["advertiser_name"], COL["advertiser_type"],
        COL["employment_type"], COL["area"], COL["location"], COL["apply_url"], COL["description"],
    ]
    missing = [column for column in required if column not in feed.columns]
    if missing:
        raise SystemExit("STOP: current JobG8 input missing columns: " + ", ".join(missing))

    area_lookup, fallback_lookup = load_geo()
    active = set(active_regions)
    df_columns = list(feed.columns)
    candidates: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_ids: dict[str, set[str]] = defaultdict(set)

    for _, row in feed.iterrows():
        region = resolve_region(row.get(COL["area"]), row.get(COL["location"]), area_lookup, fallback_lookup)
        if region not in active:
            continue
        job_id = norm(row.get(COL["job_id"]))
        title = norm(row.get(COL["title"]))
        apply_url = norm(row.get(COL["apply_url"]))
        raw_description = norm(row.get(COL["description"]))
        employer = norm(row.get(COL["advertiser_name"]))
        if not job_id or job_id in seen_ids[region] or not title or not raw_description or not apply_url.lower().startswith("http"):
            continue

        decision = classify(title, raw_description, employer)
        if not decision:
            continue
        classification, reason = decision
        description = clean_description(raw_description)
        if not description:
            continue
        salary_text, _salary_source = build_salary_details(row)
        item = clean_record_strings({
            "job_id": job_id,
            "title": title,
            "company": build_company(row),
            "advertiser_name": employer,
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
            "customer_sales_overlap_policy": "non-exclusive",
        })
        item["_campaign_key"] = campaign_key(region, employer, raw_description, title)
        candidates[region].append(item)
        seen_ids[region].add(job_id)

    output_dir = Path(category_meta(CATEGORY)["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    for region in active_regions:
        selected: list[dict[str, Any]] = []
        seen_campaigns: set[str] = set()
        for job in sorted(
            candidates.get(region, []),
            key=lambda item: (
                0 if item.get("customer_sales_classification") == "DIRECT_SALES" else 1,
                str(item.get("title", "")).lower(),
                str(item.get("location", "")).lower(),
            ),
        ):
            key = str(job.pop("_campaign_key", ""))
            if key and key in seen_campaigns:
                continue
            if key:
                seen_campaigns.add(key)
            selected.append(job)

        path = output_dir / output_filename(region, CATEGORY)
        path.write_text(json.dumps(selected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        employers = {norm_key(job.get("advertiser_name")) for job in selected if norm_key(job.get("advertiser_name"))}
        classes: dict[str, int] = defaultdict(int)
        for job in selected:
            classes[str(job.get("customer_sales_classification", ""))] += 1
        print(
            f"{region}: {len(selected)} Customer Sales jobs / {len(employers)} employers "
            f"(direct={classes.get('DIRECT_SALES', 0)}, customer={classes.get('CUSTOMER_SALES', 0)}, "
            f"account={classes.get('CONDITIONAL_ACCOUNT_SALES', 0)})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
