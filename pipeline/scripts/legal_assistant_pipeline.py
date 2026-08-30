"""Generate LIVE Legal Assistant / Paralegal slices from the current JobG8 feed.

Boundary is the owner-approved Legal family frozen on 23-24 August 2026:
- include genuine legal assistants, legal secretaries/PAs/admin and paralegals;
- paralegals may own files/caseloads;
- exclude standalone conveyancing fee earners, qualified-lawyer/specialist titles and team leaders;
- exclude salary maxima over £50,000;
- content-dedupe syndicated adverts;
- only region/category pairs marked LIVE in the slice register are generated.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

from .jobg8_family_discovery import (
    AREA_COL,
    DESCRIPTION_COL,
    DISPLAY_REF_COL,
    LOCATION_COL,
    SALARY_MAX_COL,
    SALARY_MIN_COL,
    SALARY_PERIOD_COL,
    TITLE_COL,
    annualise,
    any_match,
    compile_many,
    content_dedupe_key,
    load_geo_lookups,
    norm,
    ontap_region,
)
from .service_admin_pipeline_core import (
    COL,
    build_company,
    build_salary_details,
    clean_description,
    clean_record_strings,
    format_number,
    get_posted_date,
    norm_key,
)
from .slice_catalog import category_meta, output_filename
from .slice_registry import live_slices

CATEGORY = "legal_assistant_paralegal"
INPUT_PATH = Path("input/jobg8.xlsx")
GEO_PATH = Path("geo/geo_lookup.xlsx")
CONFIG_PATH = Path("config/family_discovery/legal_assistant_paralegal.json")
ASSESSABLE_PATH = Path("config/uk_assessable_regions.json")
OWNER_APPROVED_EXACT_TITLES = {
    "legal operations administrator (7 months ftc)",
    "legal enquiry advisor",
}

# Advert-level rules approved during the discovery review. These deliberately
# solve only the two observed generic-title IN cases and the one departmental-lead OUT edge.
DESCRIPTION_IN = re.compile(r"\b(legal\s+secretary|legal\s+assistant)\b", re.IGNORECASE)
DESCRIPTION_OUT = re.compile(
    r"\b(lead\s+(?:role\s+)?(?:in|within)\s+the\s+residential\s+conveyancing\s+department|"
    r"head\s+of\s+(?:the\s+)?(?:legal|conveyancing|litigation|probate)\b)",
    re.IGNORECASE,
)


def _load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _load_rollups() -> dict[str, str]:
    data = json.loads(ASSESSABLE_PATH.read_text(encoding="utf-8"))
    return {str(k): str(v) for k, v in data.get("detail_rollups", {}).items()}


def _include(title: str, description: str, period: str, salary_min: object, salary_max: object, cfg: dict[str, Any]) -> tuple[bool, str]:
    hard_max = float(cfg.get("hard_salary_max", 50000))
    annual_min = annualise(salary_min, period)
    annual_max = annualise(salary_max, period)
    if any(v is not None and v > hard_max for v in (annual_min, annual_max)):
        return False, "salary maximum over £50k"

    specialist_out = compile_many(cfg.get("specialist_out_title_patterns", []))
    if any_match(specialist_out, title):
        return False, "specialist/senior title boundary"
    if DESCRIPTION_OUT.search(description):
        return False, "department-lead/senior advert boundary"

    if norm_key(title) in OWNER_APPROVED_EXACT_TITLES:
        return True, "owner-approved exact Legal family title"

    likely = compile_many(cfg.get("likely_in_title_patterns", []))
    if any_match(likely, title):
        return True, "approved Legal family title"

    # Description-led discovery is allowed only where the advert itself explicitly
    # states Legal Secretary / Legal Assistant; this covers generic source titles
    # such as 'Legal' or 'Part-Time PA' without widening to generic PA/admin work.
    if DESCRIPTION_IN.search(description):
        return True, "explicit Legal Secretary/Legal Assistant advert wording"
    return False, "outside frozen Legal family boundary"


def main() -> int:
    active_regions = sorted(region for region, category in live_slices() if category == CATEGORY)
    if not active_regions:
        print("Legal Assistant / Paralegal slices: none LIVE; nothing to generate")
        return 0
    if not INPUT_PATH.is_file():
        raise SystemExit(f"STOP: missing {INPUT_PATH}")
    if not GEO_PATH.is_file():
        raise SystemExit(f"STOP: missing {GEO_PATH}")

    cfg = _load_config()
    rollups = _load_rollups()
    area_lookup, fallback_lookup = load_geo_lookups(GEO_PATH)
    feed = pd.read_excel(INPUT_PATH, dtype=str).fillna("")
    required = [
        COL["job_id"], TITLE_COL, COL["advertiser_name"], COL["advertiser_type"],
        COL["employment_type"], AREA_COL, LOCATION_COL, COL["apply_url"], DESCRIPTION_COL,
        SALARY_MIN_COL, SALARY_MAX_COL, SALARY_PERIOD_COL,
    ]
    missing = [column for column in required if column not in feed.columns]
    if missing:
        raise SystemExit("STOP: current JobG8 input missing Legal columns: " + ", ".join(missing))

    active = set(active_regions)
    outputs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_content: set[str] = set()
    df_columns = list(feed.columns)

    for _, row in feed.iterrows():
        title = norm(row.get(TITLE_COL, ""))
        raw_description = norm(row.get(DESCRIPTION_COL, ""))
        if not title or not raw_description:
            continue

        period = norm(row.get(SALARY_PERIOD_COL, ""))
        keep, reason = _include(
            title,
            raw_description,
            period,
            row.get(SALARY_MIN_COL, ""),
            row.get(SALARY_MAX_COL, ""),
            cfg,
        )
        if not keep:
            continue

        area = norm(row.get(AREA_COL, ""))
        location = norm(row.get(LOCATION_COL, ""))
        region = ontap_region(area, location, area_lookup, fallback_lookup)
        region = rollups.get(region, region)
        if region not in active:
            continue

        fingerprint = content_dedupe_key(title, location, raw_description)
        if fingerprint in seen_content:
            continue
        seen_content.add(fingerprint)

        job_id = norm(row.get(COL["job_id"]))
        apply_url = norm(row.get(COL["apply_url"]))
        description = clean_description(raw_description)
        if not job_id or not apply_url.lower().startswith("http") or not description:
            continue

        salary_text, _salary_source = build_salary_details(row)
        item = clean_record_strings({
            "job_id": job_id,
            "display_reference": norm(row.get(DISPLAY_REF_COL, "")),
            "title": title,
            "company": build_company(row),
            "advertiser_name": norm(row.get(COL["advertiser_name"])),
            "advertiser_type": norm(row.get(COL["advertiser_type"])),
            "location": location or area,
            "region": region,
            "country": "UK",
            "category": "Legal Assistant / Paralegal",
            "employment_type": norm(row.get(COL["employment_type"])),
            "salary_min": format_number(row.get(COL["salary_min"])),
            "salary_max": format_number(row.get(COL["salary_max"])),
            "salary_text": salary_text,
            "posted_date": get_posted_date(row, df_columns),
            "description": description,
            "apply_url": apply_url,
            "source": "JobG8",
            "legal_family_reason": reason,
        })
        outputs[region].append(item)

    output_dir = Path(category_meta(CATEGORY)["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    for region in active_regions:
        jobs = sorted(
            outputs.get(region, []),
            key=lambda job: (
                str(job.get("location", "")).casefold(),
                str(job.get("title", "")).casefold(),
                norm_key(job.get("advertiser_name", "")),
            ),
        )
        path = output_dir / output_filename(region, CATEGORY)
        path.write_text(json.dumps(jobs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Legal Assistant / Paralegal {region}: {len(jobs)} jobs -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
