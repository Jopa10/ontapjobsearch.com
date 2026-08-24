"""Generate owner-approved LIVE Marketing slices from the current JobG8 feed.

The production boundary follows the 24 August 2026 national discovery and
proof-page review. It covers practical Marketing, communications, content,
social/digital, PR, brand, CRM/email, ecommerce and paid-media delivery while
excluding senior/specialist noise, training-course adverts, salaries over
£50,000 and adverts whose copy places the job in another canonical market.
Only region/category pairs explicitly marked LIVE are generated.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

from .customer_sales_production_refine import canonical_region, load_location_lookup, location_conflict
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
    description_annualised_max,
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

CATEGORY = "marketing"
PIPELINE_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PIPELINE_ROOT / "input/jobg8.xlsx"
GEO_PATH = PIPELINE_ROOT / "geo/geo_lookup.xlsx"
CONFIG_PATH = PIPELINE_ROOT / "config/family_discovery/marketing.json"
ASSESSABLE_PATH = PIPELINE_ROOT / "config/uk_assessable_regions.json"

TRAINING_ADVERT = re.compile(
    r"\b(training\s+course|career\s+programme|study\s+programme|course\s+fees?|"
    r"fees?\s+apply|training\s+provider|guaranteed\s+(?:work\s+)?placement|"
    r"become\s+job[- ]ready)\b",
    re.IGNORECASE,
)
MARKETING_DELIVERY = re.compile(
    r"\b(marketing\s+campaigns?|digital\s+marketing|content\s+(?:creation|strategy|calendar)|"
    r"influencer\s+marketing|social\s+media\s+management|marketing\s+(?:graduate|operations|strategies|professional)|"
    r"support(?:ing)?\s+(?:both\s+)?(?:the\s+)?marketing|marketing\s+and\s+business\s+development\s+team|"
    r"social\s+media|paid\s+(?:media|search|social)|google\s+ads|meta\s+ads|ppc|seo|"
    r"public\s+relations|pr\s+professional|media\s+(?:relations|opportunities)|press\s+releases?|brand\s+(?:strategy|awareness|campaigns?)|"
    r"email\s+marketing|crm\s+campaigns?|e-?commerce|marketing\s+communications?|"
    r"campaign\s+(?:delivery|management|performance)|deliver(?:ing)?\s+(?:impactful\s+)?campaigns?|"
    r"go[- ]to[- ]market\s+strateg(?:y|ies)|communications?\s+agency|website\s+content|copywriting|"
    r"external\s+(?:affairs|engagement)|internal\s+communications?)\b",
    re.IGNORECASE,
)
CORE_CONTEXTUAL_TITLE = re.compile(
    r"\b(copy\s*writer|media\s*[&/]\s*pr|pr\s+account|"
    r"event\s+marketing|external\s+(?:affairs|engagement))\b",
    re.IGNORECASE,
)


def _load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _load_rollups() -> dict[str, str]:
    data = json.loads(ASSESSABLE_PATH.read_text(encoding="utf-8"))
    return {str(k): str(v) for k, v in data.get("detail_rollups", {}).items()}


def _based_in_conflict(description: str, region: str, lookup: list[tuple[str, str]]) -> str | None:
    """Reject a clear employer/job base in another canonical market.

    This supplements the shared opening-copy guard. It intentionally requires
    the explicit phrase "based in <place>" so customer territories and passing
    geographic references do not create false conflicts.
    """
    text = re.sub(r"\s+", " ", description.casefold())[:700]
    target = canonical_region(region).casefold()
    for place, mapped in lookup:
        if canonical_region(mapped).casefold() == target:
            continue
        if re.search(rf"\bbased\s+in(?:\s+the)?\s+{re.escape(place)}\b", text):
            return f"advert says based in {place}, which maps to {mapped}, not {region}"
    return None


def classify(
    title: str,
    description: str,
    period: str,
    salary_min: object,
    salary_max: object,
    cfg: dict[str, Any] | None = None,
) -> tuple[bool, str]:
    cfg = cfg or _load_config()
    hard_max = float(cfg.get("hard_salary_max", 50000))
    values = (
        annualise(salary_min, period),
        annualise(salary_max, period),
        description_annualised_max(description),
    )
    if any(value is not None and value > hard_max for value in values):
        return False, "salary maximum over £50k"

    if any_match(compile_many(cfg.get("specialist_out_title_patterns", [])), title):
        return False, "specialist/senior title boundary"
    if TRAINING_ADVERT.search(f"{title} {description}"):
        return False, "training-course advert boundary"

    broad = compile_many(cfg.get("broad_title_patterns", []))
    likely = compile_many(cfg.get("likely_in_title_patterns", []))
    borderline = compile_many(cfg.get("borderline_title_patterns", []))
    override = compile_many(cfg.get("borderline_override_title_patterns", []))
    description_context = compile_many(cfg.get("description_title_context_patterns", []))
    signals = [str(signal).casefold() for signal in cfg.get("description_signals", [])]
    description_hits = sum(signal in description.casefold() for signal in signals)
    description_led = (
        description_hits >= int(cfg.get("description_min_hits", 2))
        and any_match(description_context, title)
    )
    contextual_description_led = (
        any_match(description_context, title) and MARKETING_DELIVERY.search(description)
    )
    if not any_match(broad, title) and not description_led and not contextual_description_led:
        return False, "outside frozen Marketing candidate boundary"

    if any_match(override, title) or any_match(borderline, title):
        if not MARKETING_DELIVERY.search(description) and not CORE_CONTEXTUAL_TITLE.search(title):
            return False, "ambiguous title lacks substantive Marketing delivery evidence"
        return True, "advert confirms substantive Marketing delivery"

    if any_match(likely, title):
        return True, "approved Marketing family title"
    if (description_led or contextual_description_led) and MARKETING_DELIVERY.search(description):
        return True, "description-led advert confirms Marketing delivery"
    return False, "outside frozen Marketing family boundary"


def main() -> int:
    active_regions = sorted(region for region, category in live_slices() if category == CATEGORY)
    if not active_regions:
        print("Marketing slices: none LIVE; nothing to generate")
        return 0
    if not INPUT_PATH.is_file():
        raise SystemExit(f"STOP: missing {INPUT_PATH}")
    if not GEO_PATH.is_file():
        raise SystemExit(f"STOP: missing {GEO_PATH}")

    cfg = _load_config()
    rollups = _load_rollups()
    area_lookup, fallback_lookup = load_geo_lookups(GEO_PATH)
    location_lookup = load_location_lookup(GEO_PATH)
    feed = pd.read_excel(INPUT_PATH, dtype=str).fillna("")
    required = [
        COL["job_id"], TITLE_COL, COL["advertiser_name"], COL["advertiser_type"],
        COL["employment_type"], AREA_COL, LOCATION_COL, COL["apply_url"], DESCRIPTION_COL,
        SALARY_MIN_COL, SALARY_MAX_COL, SALARY_PERIOD_COL,
    ]
    missing = [column for column in required if column not in feed.columns]
    if missing:
        raise SystemExit("STOP: current JobG8 input missing Marketing columns: " + ", ".join(missing))

    active = set(active_regions)
    outputs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_content: set[str] = set()
    df_columns = list(feed.columns)

    for _, row in feed.iterrows():
        title = norm(row.get(TITLE_COL, ""))
        raw_description = norm(row.get(DESCRIPTION_COL, ""))
        if not title or not raw_description:
            continue
        keep, reason = classify(
            title,
            raw_description,
            norm(row.get(SALARY_PERIOD_COL, "")),
            row.get(SALARY_MIN_COL, ""),
            row.get(SALARY_MAX_COL, ""),
            cfg,
        )
        if not keep:
            continue

        area = norm(row.get(AREA_COL, ""))
        location = norm(row.get(LOCATION_COL, ""))
        region = rollups.get(ontap_region(area, location, area_lookup, fallback_lookup), "")
        if not region:
            region = ontap_region(area, location, area_lookup, fallback_lookup)
        if region not in active:
            continue

        conflict = location_conflict(title, raw_description, region, location_lookup)
        conflict = conflict or _based_in_conflict(raw_description, region, location_lookup)
        if conflict:
            print(f"Marketing WITHHOLD {norm(row.get(DISPLAY_REF_COL, ''))} | {title} | {conflict}")
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
        outputs[region].append(clean_record_strings({
            "job_id": job_id,
            "display_reference": norm(row.get(DISPLAY_REF_COL, "")),
            "title": title,
            "company": build_company(row),
            "advertiser_name": norm(row.get(COL["advertiser_name"])),
            "advertiser_type": norm(row.get(COL["advertiser_type"])),
            "location": location or area,
            "region": region,
            "country": "UK",
            "category": "Marketing",
            "employment_type": norm(row.get(COL["employment_type"])),
            "salary_min": format_number(row.get(COL["salary_min"])),
            "salary_max": format_number(row.get(COL["salary_max"])),
            "salary_text": salary_text,
            "posted_date": get_posted_date(row, df_columns),
            "description": description,
            "apply_url": apply_url,
            "source": "JobG8",
            "marketing_family_reason": reason,
        }))

    output_dir = Path(category_meta(CATEGORY)["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    for region in active_regions:
        jobs = sorted(outputs.get(region, []), key=lambda job: (
            str(job.get("location", "")).casefold(),
            str(job.get("title", "")).casefold(),
            norm_key(job.get("advertiser_name", "")),
        ))
        path = output_dir / output_filename(region, CATEGORY)
        path.write_text(json.dumps(jobs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Marketing {region}: {len(jobs)} jobs -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
