"""Generate LIVE Customer-Service slices from its audited title register.

Selection is deliberately narrow:
- exact normalised title match only;
- only HIGH_CONFIDENCE / ELASTIC_FIT register rows;
- no JobG8 Classification gate;
- existing geography and salary credibility rules remain in force;
- salary review rows are reported but not auto-published;
- once a slice is explicitly LIVE, any non-zero selected count publishes/refreshes;
- the six-job signal remains launch evidence for non-LIVE candidates only.

The JSON files sit in output-admin-service with distinct category suffixes so the
existing enrichment and commit steps can carry them without changing the
established admin selector.
"""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd

from . import service_admin_pipeline as admin
from .customer_sales_pipeline import campaign_key
from .customer_sales_production_refine import load_location_lookup, location_conflict
from .pipeline_refinement import assess_salary, load_refinement_rules, load_salary_thresholds, resolve_feed_date
from .slice_catalog import category_meta, output_filename
from .slice_registry import live_slices

INPUT_DIR = Path("input")
GEO_PATH = Path(__file__).resolve().parents[1] / "geo" / "geo_lookup.xlsx"
REGISTER_DIR = Path(__file__).resolve().parents[1] / "registers"
OUTPUT_DIR = Path("output-admin-service")
REPORT_PATH = OUTPUT_DIR / "registered-category-decision-report.csv"
SUMMARY_PATH = OUTPUT_DIR / "registered-category-selection-summary.csv"
LIVE_PUBLISH_FLOOR = 1

CATEGORIES = {
    "customer_service_contact_centre": "customer_service_contact_centre_title_classification_register.csv",
}
SELECTED_CLASSIFICATIONS = {"HIGH_CONFIDENCE", "ELASTIC_FIT"}
NE_DETAIL_REGIONS = {
    "North East - Tyneside, Wearside & Northumberland",
    "North East - County Durham & Darlington/Hartlepool",
    "North East - Tees Valley",
}
SALARY_THRESHOLDS = load_salary_thresholds()


def norm(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def key(value: Any) -> str:
    return norm(value).lower()


def find_current_feed() -> Path:
    if not INPUT_DIR.is_dir():
        raise SystemExit("STOP: pipeline/input does not exist")
    candidates = [
        path
        for path in INPUT_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".xlsx", ".xls", ".csv"}
        and not path.name.startswith("~$")
    ]
    named = [path for path in candidates if "jobg8" in path.name.lower()]
    selected = named or candidates
    if len(selected) != 1:
        names = ", ".join(path.name for path in selected) or "none"
        raise SystemExit(f"STOP: expected one current JobG8 input; found {names}")
    return selected[0]


def read_feed(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, dtype=str).fillna("")
    return pd.read_excel(path, dtype=str).fillna("")


def load_titles(category: str) -> dict[str, str]:
    path = REGISTER_DIR / CATEGORIES[category]
    if not path.is_file():
        raise SystemExit(f"STOP: missing title register: {path}")
    result: dict[str, str] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "title" not in reader.fieldnames or "classification" not in reader.fieldnames:
            raise SystemExit(f"STOP: invalid title register columns: {path.name}")
        for row in reader:
            title_key = key(row.get("title"))
            classification = norm(row.get("classification")).upper()
            if title_key and classification in SELECTED_CLASSIFICATIONS:
                result[title_key] = classification
    for row in load_refinement_rules(category):
        title_key = key(row.get("title"))
        classification = norm(row.get("classification")).upper()
        if title_key and classification in SELECTED_CLASSIFICATIONS:
            result[title_key] = classification
    return result


def load_geo() -> tuple[dict[str, str], dict[str, str]]:
    area_df = pd.read_excel(GEO_PATH, dtype=str).fillna("")
    if not {"Area", "Cluster"}.issubset(area_df.columns):
        raise SystemExit("STOP: geo lookup requires Area and Cluster")
    area_map = {
        key(row["Area"]): norm(row["Cluster"])
        for _, row in area_df.iterrows()
        if key(row["Area"]) and norm(row["Cluster"])
    }

    fallback_df = pd.read_excel(GEO_PATH, sheet_name="LocationFallback", dtype=str).fillna("")
    if not {"Status", "Location", "Cluster"}.issubset(fallback_df.columns):
        raise SystemExit("STOP: LocationFallback requires Status, Location and Cluster")
    fallback = {
        key(row["Location"]): norm(row["Cluster"])
        for _, row in fallback_df.iterrows()
        if key(row["Status"]) == "auto" and key(row["Location"]) and norm(row["Cluster"])
    }
    return area_map, fallback


def candidate_regions(raw_region: str) -> set[str]:
    result = {raw_region} if raw_region else set()
    if raw_region in NE_DETAIL_REGIONS:
        result.add("North East")
    return result


def posted_date(row: pd.Series, columns: set[str]) -> str:
    for column in admin.OPTIONAL_POSTED_DATE_COLUMNS:
        if column in columns:
            return norm(row.get(column))
    return ""


def clean_json_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        field: admin.fix_encoding(norm(value)) if isinstance(value, str) else value
        for field, value in row.items()
    }


def run_live_registered_categories() -> int:
    active = {
        (region, category)
        for region, category in live_slices()
        if category in CATEGORIES
    }
    if not active:
        print("Registered Finance/Customer-Service slices: none LIVE; nothing to generate")
        return 0

    active_categories = sorted({category for _, category in active})
    titles = {category: load_titles(category) for category in active_categories}
    area_map, fallback = load_geo()
    location_lookup = load_location_lookup()
    feed_path = find_current_feed()
    feed = read_feed(feed_path)
    columns = set(feed.columns)
    required = {
        admin.COL["job_id"],
        admin.COL["title"],
        admin.COL["advertiser_name"],
        admin.COL["employment_type"],
        admin.COL["area"],
        admin.COL["location"],
        admin.COL["apply_url"],
        admin.COL["description"],
    }
    missing = sorted(required - columns)
    if missing:
        raise SystemExit("STOP: current JobG8 input missing columns: " + ", ".join(missing))

    outputs: dict[tuple[str, str], list[dict[str, Any]]] = {pair: [] for pair in active}
    seen: dict[tuple[str, str], set[str]] = defaultdict(set)
    seen_campaigns: dict[tuple[str, str], set[str]] = defaultdict(set)
    decisions: list[dict[str, Any]] = []

    for _, row in feed.iterrows():
        title = norm(row.get(admin.COL["title"]))
        title_key = key(title)
        matched = {
            category: titles[category][title_key]
            for category in active_categories
            if title_key in titles[category]
        }
        if not matched:
            continue

        area = norm(row.get(admin.COL["area"]))
        location = norm(row.get(admin.COL["location"]))
        if admin.area_is_unusable(area):
            raw_region = fallback.get(key(location), "")
            town = location
        else:
            raw_region = area_map.get(key(area), "")
            town = area
        regions = candidate_regions(raw_region)
        if not regions:
            continue

        job_id = norm(row.get(admin.COL["job_id"]))
        apply_url = norm(row.get(admin.COL["apply_url"]))
        raw_description = norm(row.get(admin.COL["description"]))
        if not job_id or not apply_url.lower().startswith("http") or not raw_description:
            continue

        salary_text, _salary_source = admin.build_salary_details(row)
        salary_period = admin.normalise_salary_period(row)
        employment_type = norm(row.get(admin.COL["employment_type"]))
        description = admin.clean_description(raw_description)
        if not description:
            continue
        source_posted_date = posted_date(row, columns)

        for category, classification in matched.items():
            for region in sorted(regions):
                pair = (region, category)
                if pair not in active or job_id in seen[pair]:
                    continue

                conflict = location_conflict(title, raw_description, region, location_lookup)
                if conflict:
                    decisions.append(
                        {
                            "decision": "DROPPED",
                            "region": region,
                            "category": category,
                            "title": title,
                            "job_id": job_id,
                            "classification": classification,
                            "salary_text": salary_text,
                            "reason": conflict,
                        }
                    )
                    continue

                employer = norm(row.get(admin.COL["advertiser_name"]))
                campaign = campaign_key(region, employer, raw_description, title)
                if campaign in seen_campaigns[pair]:
                    decisions.append(
                        {
                            "decision": "DROPPED",
                            "region": region,
                            "category": category,
                            "title": title,
                            "job_id": job_id,
                            "classification": classification,
                            "salary_text": salary_text,
                            "reason": "duplicate employer campaign advert",
                        }
                    )
                    continue

                salary = assess_salary(
                    salary_min=row.get(admin.COL["salary_min"]),
                    salary_max=row.get(admin.COL["salary_max"]),
                    salary_period=salary_period,
                    salary_text=salary_text,
                    region=region,
                    thresholds=SALARY_THRESHOLDS,
                )
                if salary.corrupt:
                    decisions.append(
                        {
                            "decision": "DROPPED",
                            "region": region,
                            "category": category,
                            "title": title,
                            "job_id": job_id,
                            "classification": classification,
                            "salary_text": salary_text,
                            "reason": "salary credibility: " + salary.reason,
                        }
                    )
                    continue
                if salary.review_required:
                    decisions.append(
                        {
                            "decision": "POSS",
                            "region": region,
                            "category": category,
                            "title": title,
                            "job_id": job_id,
                            "classification": classification,
                            "salary_text": salary_text,
                            "reason": "salary/manual review required: " + salary.reason,
                        }
                    )
                    continue

                item = clean_json_row(
                    {
                        "job_id": job_id,
                        "title": title,
                        "company": admin.build_company(row),
                        "advertiser_name": norm(row.get(admin.COL["advertiser_name"])),
                        "advertiser_type": norm(row.get(admin.COL["advertiser_type"])),
                        "location": town,
                        "region": region,
                        "country": "UK",
                        "category": category_meta(category)["category_label"],
                        "employment_type": employment_type,
                        "salary_min": admin.format_number(row.get(admin.COL["salary_min"])),
                        "salary_max": admin.format_number(row.get(admin.COL["salary_max"])),
                        "salary_period": salary_period,
                        "salary_text": salary_text,
                        "work_pattern": norm(row.get("/Job/WorkHours")),
                        "posted_date": source_posted_date,
                        "posted_date_basis": "source" if source_posted_date else "",
                        "description": description,
                        "apply_url": apply_url,
                        "source": "JobG8",
                    }
                )
                outputs[pair].append(item)
                seen[pair].add(job_id)
                seen_campaigns[pair].add(campaign)
                decisions.append(
                    {
                        "decision": "SELECTED",
                        "region": region,
                        "category": category,
                        "title": title,
                        "job_id": job_id,
                        "classification": classification,
                        "salary_text": salary_text,
                        "reason": "exact audited register match",
                    }
                )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    publishable: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for (region, category), rows in sorted(outputs.items()):
        rows.sort(
            key=lambda item: (
                key(item.get("location")),
                key(item.get("title")),
                key(item.get("job_id")),
            )
        )
        current_rows = rows if len(rows) >= LIVE_PUBLISH_FLOOR else []
        publishable[(region, category)] = current_rows
        path = OUTPUT_DIR / output_filename(region, category)
        path.write_text(
            json.dumps(current_rows, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        if current_rows:
            print(f"{region} / {category}: {len(rows)} selected -> {path}")
        else:
            print(
                f"{region} / {category}: 0 selected; LIVE page refresh withheld"
            )

    fieldnames = [
        "decision",
        "region",
        "category",
        "title",
        "job_id",
        "classification",
        "salary_text",
        "reason",
    ]
    with REPORT_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(decisions)

    with SUMMARY_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["region", "category", "eligible_count", "published_count", "status"],
        )
        writer.writeheader()
        for pair, rows in sorted(outputs.items()):
            published_count = len(publishable[pair])
            writer.writerow(
                {
                    "region": pair[0],
                    "category": pair[1],
                    "eligible_count": len(rows),
                    "published_count": published_count,
                    "status": "PUBLISHABLE" if published_count else "BELOW_THRESHOLD",
                }
            )

    print(
        f"Registered category pipeline complete for {resolve_feed_date(feed_path)}: "
        f"{sum(len(rows) for rows in publishable.values())} publishable slice memberships "
        f"across {sum(bool(rows) for rows in publishable.values())}/{len(outputs)} LIVE slices"
    )
    return 0


def main() -> int:
    return run_live_registered_categories()


if __name__ == "__main__":
    raise SystemExit(main())
