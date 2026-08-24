"""Generate owner-approved LIVE HR / Recruitment slices from JobG8.

The production boundary freezes the 24 August 2026 national discovery and
proof-page review. It covers accessible HR, People, in-house recruitment,
onboarding and L&D administration or coordination, while excluding advisory,
managerial, specialist and agency-sales recruitment work. It also applies the
£50,000 ceiling, content dedupe and advert-location safeguards before writing
only region/category pairs explicitly marked LIVE.
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

CATEGORY = "hr_recruitment"
PIPELINE_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PIPELINE_ROOT / "input/jobg8.xlsx"
GEO_PATH = PIPELINE_ROOT / "geo/geo_lookup.xlsx"
CONFIG_PATH = PIPELINE_ROOT / "config/family_discovery/hr_recruitment.json"
ASSESSABLE_PATH = PIPELINE_ROOT / "config/uk_assessable_regions.json"

TRAINING_ADVERT = re.compile(
    r"\b(training\s+course|career\s+programme|study\s+programme|course\s+fees?|"
    r"fees?\s+apply|training\s+provider|guaranteed\s+(?:work\s+)?placement)\b",
    re.IGNORECASE,
)
MIXED_OFFICE_MANAGEMENT = re.compile(
    r"\b(?:office|facilities)\s+manager\b.*\bhr\b|\bhr\b.*\b(?:office|facilities)\s+manager\b",
    re.IGNORECASE,
)
HR_DELIVERY = re.compile(
    r"\b(hr\s+administration|human\s+resources?|people\s+(?:team|operations?|services?)|"
    r"employee\s+(?:life\s*cycle|records?)|personnel\s+records?|contracts?\s+of\s+employment|"
    r"new\s+starters?|onboarding|pre[- ]employment\s+checks?|right\s+to\s+work|"
    r"hris|hr\s+systems?|absence\s+records?|learning\s+and\s+development|l&d)\b",
    re.IGNORECASE,
)
RECRUITMENT_DELIVERY = re.compile(
    r"\b(candidate\s+(?:sourcing|screening|compliance)|source\s+candidates?|job\s+boards?|"
    r"applicant\s+tracking\s+systems?|recruitment\s+(?:administration|process|delivery)|"
    r"talent\s+acquisition|arrang(?:e|ing)\s+interviews?|booking\s+candidates?|"
    r"pre[- ]employment\s+checks?|right\s+to\s+work)\b",
    re.IGNORECASE,
)
ADVISORY_CASEWORK = re.compile(
    r"\b(employee\s+relations?|er\s+casework|complex\s+casework|disciplinar(?:y|ies)|"
    r"grievances?|tribunals?|tupe|collective\s+consultation|advise\s+(?:line\s+)?managers?|"
    r"strategic\s+hr|business\s+partner)\b",
    re.IGNORECASE,
)
AGENCY_SALES = re.compile(
    r"\b(uncapped\s+commission|business\s+development|new\s+business|sales\s+targets?|"
    r"client\s+development|cold\s+call(?:ing)?|build\s+(?:your|a)\s+desk|360\s+recruitment)\b",
    re.IGNORECASE,
)
ADJACENT_OR_SPECIALIST_ROLE = re.compile(
    r"\b(recruitment\s+performance.*\b(?:reporting|planning)|"
    r"(?:student|course|apprentice)\s+recruitment|recruitment\s+(?:and\s+)?outreach|"
    r"volunteer\s+recruitment|talent\s+acquisition\s+(?:partner|strategy)|"
    r"adviser\s+onboarding|finance\s+administrators?|business\s+support\s+administrators?|"
    r"executive\s+assistants?|pa\s*(?:&|and)\s*team\s+administrators?|"
    r"production\s+co-?ordinators?)\b",
    re.IGNORECASE,
)
GENERIC_SUPPORT_TITLE = re.compile(
    r"\b(administrators?|assistants?|co-?ordinators?|officers?|data\s+administrators?|"
    r"training\s+administrators?|onboarding\s+administrators?)\b",
    re.IGNORECASE,
)


def _load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _load_rollups() -> dict[str, str]:
    data = json.loads(ASSESSABLE_PATH.read_text(encoding="utf-8"))
    return {str(key): str(value) for key, value in data.get("detail_rollups", {}).items()}


def _based_in_conflict(description: str, region: str, lookup: list[tuple[str, str]]) -> str | None:
    text = re.sub(r"\s+", " ", description.casefold())[:700]
    target = canonical_region(region).casefold()
    for place, mapped in lookup:
        if canonical_region(mapped).casefold() == target:
            continue
        if re.search(rf"\bbased\s+in(?:\s+the)?\s+{re.escape(place)}\b", text):
            return f"advert says based in {place}, which maps to {mapped}, not {region}"
    return None


def _near_duplicate_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", re.sub(r"<[^>]+>", " ", value.casefold()))


def is_near_duplicate(
    title: str,
    region: str,
    place: str,
    description: str,
    seen: list[tuple[str, str, str, str]],
) -> bool:
    """Catch same-place syndication where one copy is a shortened advert.

    A long shared opening is required as well as the same normalised title,
    canonical market and source place. This deliberately does not collapse a
    legitimate multi-location advert represented in two different markets.
    """
    signature = (
        norm_key(title),
        canonical_region(region).casefold(),
        norm_key(place),
        _near_duplicate_text(description),
    )
    for previous in seen:
        if signature[:3] != previous[:3]:
            continue
        current_text = signature[3]
        previous_text = previous[3]
        shared = min(len(current_text), len(previous_text), 320)
        if shared >= 240 and current_text[:shared] == previous_text[:shared]:
            return True
    seen.append(signature)
    return False


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

    combined = f"{title} {description}"
    if any_match(compile_many(cfg.get("specialist_out_title_patterns", [])), title):
        return False, "specialist/senior title boundary"
    if TRAINING_ADVERT.search(combined):
        return False, "training-course advert boundary"
    if ADJACENT_OR_SPECIALIST_ROLE.search(title):
        return False, "adjacent/specialist role outside employee HR and recruitment support"
    if re.search(r"\btalent\s+acquisition\b", title, re.IGNORECASE) and re.search(
        r"\b(talent\s+acquisition\s+partner|strategic\s+(?:talent|recruitment)|talent\s+strategy)\b",
        description,
        re.IGNORECASE,
    ):
        return False, "strategic Talent Acquisition boundary"
    if MIXED_OFFICE_MANAGEMENT.search(title):
        return False, "office/facilities management is the core occupation"

    broad = compile_many(cfg.get("broad_title_patterns", []))
    likely = compile_many(cfg.get("likely_in_title_patterns", []))
    borderline = compile_many(cfg.get("borderline_title_patterns", []))
    override = compile_many(cfg.get("borderline_override_title_patterns", []))
    description_context = compile_many(cfg.get("description_title_context_patterns", []))
    signals = [str(signal).casefold() for signal in cfg.get("description_signals", [])]
    description_hits = sum(signal in description.casefold() for signal in signals)
    description_led = (
        description_hits >= int(cfg.get("description_min_hits", 3))
        and any_match(description_context, title)
    )
    if not any_match(broad, title) and not description_led:
        return False, "outside frozen HR / Recruitment candidate boundary"

    if any_match(likely, title) and not any_match(override, title):
        return True, "approved HR / Recruitment support title"

    title_folded = title.casefold()
    delivery = bool(HR_DELIVERY.search(description) or RECRUITMENT_DELIVERY.search(description))
    if re.search(r"\bhr\s+officers?\b", title_folded):
        if not delivery or ADVISORY_CASEWORK.search(description):
            return False, "HR Officer advert is advisory/generalist rather than administration-centred"
        return True, "advert confirms operational HR administration"

    if re.search(r"\b(recruit|resourc|talent\s+acquisition)", title_folded):
        if AGENCY_SALES.search(description):
            return False, "agency recruitment sales/business-development boundary"
        if RECRUITMENT_DELIVERY.search(description):
            return True, "advert confirms recruitment sourcing/coordination delivery"
        return False, "ambiguous recruitment title lacks substantive delivery evidence"

    if any_match(override, title) or any_match(borderline, title):
        if delivery and not ADVISORY_CASEWORK.search(description):
            return True, "advert confirms substantive HR / Recruitment delivery"
        return False, "ambiguous title lacks substantive HR / Recruitment delivery evidence"

    if description_led and GENERIC_SUPPORT_TITLE.search(title) and delivery:
        return True, "description-led advert confirms HR / Recruitment support delivery"
    return False, "outside frozen HR / Recruitment family boundary"


def main() -> int:
    active_regions = sorted(region for region, category in live_slices() if category == CATEGORY)
    if not active_regions:
        print("HR / Recruitment slices: none LIVE; nothing to generate")
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
        raise SystemExit("STOP: current JobG8 input missing HR / Recruitment columns: " + ", ".join(missing))

    active = set(active_regions)
    outputs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_content: set[str] = set()
    seen_near: list[tuple[str, str, str, str]] = []
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
        raw_region = ontap_region(area, location, area_lookup, fallback_lookup)
        region = rollups.get(raw_region, raw_region)
        if region not in active:
            continue

        conflict = location_conflict(title, raw_description, region, location_lookup)
        conflict = conflict or _based_in_conflict(raw_description, region, location_lookup)
        if conflict:
            print(f"HR / Recruitment WITHHOLD {norm(row.get(DISPLAY_REF_COL, ''))} | {title} | {conflict}")
            continue

        fingerprint = content_dedupe_key(title, location, raw_description)
        if fingerprint in seen_content:
            continue
        if is_near_duplicate(title, region, area or location, raw_description, seen_near):
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
            "category": "HR / Recruitment",
            "employment_type": norm(row.get(COL["employment_type"])),
            "salary_min": format_number(row.get(COL["salary_min"])),
            "salary_max": format_number(row.get(COL["salary_max"])),
            "salary_text": salary_text,
            "posted_date": get_posted_date(row, df_columns),
            "description": description,
            "apply_url": apply_url,
            "source": "JobG8",
            "hr_recruitment_family_reason": reason,
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
        print(f"HR / Recruitment {region}: {len(jobs)} jobs -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
