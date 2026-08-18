"""Add agreed conditional account-based sales roles to the branch-only test family.

The core pass deliberately excludes generic Account Manager / Account Executive titles.
This second pass brings back only those that are clearly sales-led and office/contact-
centre/home/hybrid, while rejecting field, senior and specialist-market account roles.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from scripts.customer_sales_test_pipeline import TARGETS, load_geo, resolve_region
from scripts.service_admin_pipeline_core import (
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

INPUT_PATH = Path("input/jobg8.xlsx")
OUTPUT_DIR = Path("output-customer-sales-test")

CONDITIONAL_TITLES = ["account manager", "account executive"]
SALES_EVIDENCE = [
    "sales target", "sales targets", "sales pipeline", "new business", "commission",
    "upsell", "up-sell", "cross-sell", "cross sell", "revenue growth", "grow revenue",
    "grow accounts", "account growth", "business growth", "selling", "sales opportunities",
    "sales opportunity", "convert leads", "lead generation", "retention", "renewals",
]
OFFICE_EVIDENCE = [
    "office", "office-based", "office based", "hybrid", "remote", "home-based", "home based",
    "phone", "telephone", "crm", "inbound", "outbound", "email",
]
EXCLUDES = [
    "field account manager", "field-based", "field based", "field sales", "territory",
    "area account manager", "regional account manager", "door to door", "door-to-door",
    "technical account manager", "enterprise account manager", "strategic account manager",
    "senior account manager", "national account manager", "key account manager",
    "commercial insurance", "insurance broker", "insurance brokerage", "underwriting",
    "pensions", "wealth management", "financial adviser", "financial advisor",
    "automotive", "motor trade", "car dealership", "medical device", "pharmaceutical",
]


def has_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def main() -> None:
    df = pd.read_excel(INPUT_PATH, dtype=str).fillna("")
    area_lookup, fallback_lookup = load_geo()
    df_columns = list(df.columns)

    outputs: dict[str, list[dict]] = {}
    seen: dict[str, set[str]] = {}
    filenames = {region: filename for region, filename in TARGETS.items()}
    for region, filename in filenames.items():
        path = OUTPUT_DIR / filename
        jobs = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
        outputs[region] = jobs
        seen[region] = {str(job.get("job_id", "")) for job in jobs}

    added: dict[str, int] = {region: 0 for region in TARGETS}

    for _, row in df.iterrows():
        title = norm(row.get(COL["title"]))
        title_key = norm_key(title)
        if not title or not has_any(title_key, CONDITIONAL_TITLES):
            continue

        description_raw = norm(row.get(COL["description"]))
        combined = f"{title_key} {norm_key(description_raw)}"
        if has_any(combined, EXCLUDES):
            continue
        if not has_any(combined, SALES_EVIDENCE):
            continue
        if not has_any(combined, OFFICE_EVIDENCE):
            continue

        region = resolve_region(
            row.get(COL["area"]), row.get(COL["location"]), area_lookup, fallback_lookup
        )
        if region not in TARGETS:
            continue

        job_id = norm(row.get(COL["job_id"]))
        apply_url = norm(row.get(COL["apply_url"]))
        if not job_id or job_id in seen[region] or not apply_url.lower().startswith("http"):
            continue

        description = clean_description(description_raw)
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
            "customer_sales_classification": "CONDITIONAL_ACCOUNT_SALES",
            "customer_sales_reason": "account-based title with sales and office/digital evidence",
        })
        outputs[region].append(item)
        seen[region].add(job_id)
        added[region] += 1

    for region, filename in filenames.items():
        jobs = sorted(outputs[region], key=lambda job: (
            0 if job.get("customer_sales_classification") == "DIRECT_SALES" else 1,
            str(job.get("title", "")).lower(), str(job.get("location", "")).lower(),
        ))
        (OUTPUT_DIR / filename).write_text(json.dumps(jobs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{region}: +{added[region]} conditional account sales; {len(jobs)} total before QA refinement")


if __name__ == "__main__":
    main()
