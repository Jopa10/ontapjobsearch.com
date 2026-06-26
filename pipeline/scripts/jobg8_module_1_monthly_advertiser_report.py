#!/usr/bin/env python3
"""
Ontap Compiler Module 1: Monthly Advertiser and Role Trend Report.

Builds two month-level CSV reports from the archived daily JobG8 Excel feeds:
- advertiser campaign summary by advertiser/category/region
- role trends by registered category/region, including top advertiser share

Inputs are intentionally repo-native only: the monthly archive folder,
pipeline/geo/geo_lookup.xlsx, and pipeline/registers/*.csv.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import csv
import pandas as pd

SELECTED_CLASSIFICATIONS = {"HIGH_CONFIDENCE", "ELASTIC_FIT"}

REGISTER_SPECS = {
    "support_worker": ["support_worker_title_classification_register*.csv"],
    "admin_service": ["admin_service_title_classification_register*.csv"],
    "finance_accounts": ["finance_accounts_title_classification_register*.csv"],
    "customer_service_contact_centre": ["customer_service_contact_centre_title_classification_register*.csv"],
    "warehouse_logistics": ["warehouse_logistics_title_classification_register*.csv"],
    "hr_recruitment": ["hr_recruitment_title_classification_register*.csv"],
}

LIVE_SLICE_GROUPS = {
    "North East": [
        "North East - Tyneside, Wearside & Northumberland",
        "North East - County Durham & Darlington/Hartlepool",
        "North East - Tees Valley",
    ],
}

COL_JOB_ID = "/Job/DisplayReference"
COL_TITLE = "/Job/Position"
COL_ADVERTISER = "/Job/AdvertiserName"
COL_ADVERTISER_TYPE = "/Job/AdvertiserType"
COL_AREA = "/Job/Area"
COL_LOCATION = "/Job/Location"


def norm_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def norm_key(value: object) -> str:
    return norm_text(value).lower()


def extract_date(path: Path) -> Optional[str]:
    match = re.search(r"(20\d{2})[-_.](\d{2})[-_.](\d{2})", path.stem)
    if not match:
        return None
    return "-".join(match.groups())


def find_latest_matching_file(search_dirs: Iterable[Path], patterns: List[str]) -> Optional[Path]:
    matches: List[Path] = []
    for folder in search_dirs:
        if not folder.exists():
            continue
        for pattern in patterns:
            matches.extend(folder.glob(pattern))
    matches = [path for path in matches if not path.name.startswith("~$")]
    return max(matches, key=lambda path: (path.stat().st_mtime, path.name.lower())) if matches else None


def discover_registers(base_dir: Path, registers_dir: Optional[Path]) -> Dict[str, Path]:
    search_dirs = []
    if registers_dir:
        search_dirs.append(registers_dir)
    search_dirs.extend([base_dir / "pipeline" / "registers", base_dir / "registers", base_dir])

    resolved: Dict[str, Path] = {}
    missing: List[str] = []
    for category, patterns in REGISTER_SPECS.items():
        found = find_latest_matching_file(search_dirs, patterns)
        if found:
            resolved[category] = found
        else:
            missing.append(category)
    if missing:
        raise FileNotFoundError("Missing required register(s): " + ", ".join(missing))
    return resolved


def iter_records(df: object) -> Iterable[dict]:
    for _, row in df.iterrows():
        yield dict(row)


def load_geo_lookup(path: Path) -> Dict[str, str]:
    df = pd.read_excel(path, dtype=str).fillna("")
    missing = {"Area", "Cluster"}.difference(df.columns)
    if missing:
        raise ValueError(f"Geo lookup missing columns: {sorted(missing)}")
    lookup = {
        norm_key(row.get("Area")): norm_text(row.get("Cluster"))
        for row in iter_records(df)
        if norm_key(row.get("Area")) and norm_text(row.get("Cluster"))
    }
    if not lookup:
        raise ValueError("Geo lookup contains no usable Area → Cluster mappings.")
    return lookup


def load_register(path: Path) -> Dict[str, str]:
    df = pd.read_csv(path, dtype=str).fillna("")
    missing = {"title", "classification"}.difference(df.columns)
    if missing:
        raise ValueError(f"{path.name} missing columns: {sorted(missing)}")
    return {
        norm_key(row.get("title")): norm_text(row.get("classification")).upper()
        for row in iter_records(df)
        if norm_key(row.get("title"))
    }


def load_daily_feeds(input_dir: Path, geo_lookup: Dict[str, str], registers: Dict[str, Dict[str, str]]) -> tuple[list[dict], List[str], List[str]]:
    files = sorted(path for path in input_dir.iterdir() if path.suffix.lower() in {".xlsx", ".xls", ".xlsm"} and not path.name.startswith("~$"))
    if not files:
        raise FileNotFoundError(f"No JobG8 Excel files found in {input_dir}")

    rows: List[dict] = []
    errors: List[str] = []
    valid_dates: List[str] = []
    required_cols = {COL_TITLE, COL_ADVERTISER, COL_AREA}
    seen: set[tuple[str, str, str, str]] = set()

    for path in files:
        date = extract_date(path)
        if not date:
            errors.append(f"{path.name}: date not recognised from filename")
            continue
        try:
            df = pd.read_excel(path, dtype=str).fillna("")
        except Exception as exc:
            errors.append(f"{path.name}: failed to read: {exc}")
            continue
        missing = required_cols.difference(df.columns)
        if missing:
            errors.append(f"{path.name}: missing columns {sorted(missing)}")
            continue
        valid_dates.append(date)
        for index, row in enumerate(iter_records(df)):
            title = norm_text(row.get(COL_TITLE))
            title_key = norm_key(title)
            matched_categories = [category for category, register in registers.items() if register.get(title_key) in SELECTED_CLASSIFICATIONS]
            if not matched_categories:
                continue
            area = norm_text(row.get(COL_AREA))
            job_id = norm_text(row.get(COL_JOB_ID)) if COL_JOB_ID in df.columns else ""
            if not job_id:
                job_id = f"{path.name}:{index + 2}"
            base = {
                "month_date": date,
                "job_id": job_id,
                "title": title,
                "title_key": title_key,
                "advertiser": norm_text(row.get(COL_ADVERTISER)) or "Unknown advertiser",
                "advertiser_type": norm_text(row.get(COL_ADVERTISER_TYPE)) if COL_ADVERTISER_TYPE in df.columns else "",
                "location": area,
                "raw_location": norm_text(row.get(COL_LOCATION)) if COL_LOCATION in df.columns else "",
                "lookup_region": geo_lookup.get(norm_key(area), "Other / Unknown"),
                "source_file": path.name,
            }
            for category in matched_categories:
                key = (date, job_id, category, base["lookup_region"])
                if key not in seen:
                    seen.add(key)
                    rows.append({**base, "category": category})

    if not rows:
        raise RuntimeError("No jobs matched HIGH_CONFIDENCE or ELASTIC_FIT in the registers.")
    return rows, sorted(set(valid_dates)), errors


def add_report_regions(expanded: list[dict]) -> list[dict]:
    rows = [{**row, "report_region": row["lookup_region"], "region_scope": "lookup_region"} for row in expanded]
    for aggregate_region, lookup_regions in LIVE_SLICE_GROUPS.items():
        for row in expanded:
            if row["lookup_region"] in lookup_regions:
                rows.append({**row, "report_region": aggregate_region, "region_scope": "published_aggregate"})
    return rows


def safe_pct(numerator: int | float, denominator: int | float) -> float:
    return round((numerator / denominator * 100.0), 1) if denominator else 0.0


def top_values(values: Iterable[object], limit: int = 8) -> str:
    return "; ".join(f"{value} ({count})" for value, count in Counter(norm_text(v) for v in values if norm_text(v)).most_common(limit))


def unique_count(rows: list[dict], field: str) -> int:
    return len({row[field] for row in rows})


def group_rows(rows: list[dict], fields: tuple[str, ...]) -> dict[tuple, list[dict]]:
    grouped: dict[tuple, list[dict]] = {}
    for row in rows:
        key = tuple(row[field] for field in fields)
        grouped.setdefault(key, []).append(row)
    return grouped


def daily_unique_counts(rows: list[dict]) -> Counter:
    by_day: dict[str, set[str]] = {}
    for row in rows:
        by_day.setdefault(row["month_date"], set()).add(row["job_id"])
    return Counter({date: len(ids) for date, ids in by_day.items()})


def write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_reports(expanded: list[dict], valid_dates: List[str], month: str) -> tuple[list[dict], list[dict]]:
    report_jobs = add_report_regions(expanded)
    campaign_rows: List[dict] = []
    role_rows: List[dict] = []

    for (region, scope, category, advertiser), group in group_rows(report_jobs, ("report_region", "region_scope", "category", "advertiser")).items():
        daily_counts = daily_unique_counts(group)
        total_jobs = unique_count(group, "job_id")
        days_seen = sum(1 for value in daily_counts.values() if value > 0)
        campaign_rows.append({
            "month": month,
            "region": region,
            "region_scope": scope,
            "category": category,
            "advertiser": advertiser,
            "advertiser_type": top_values((row["advertiser_type"] for row in group), 3),
            "total_jobs": total_jobs,
            "feed_days": len(valid_dates),
            "days_seen": days_seen,
            "seen_ratio_pct": safe_pct(days_seen, len(valid_dates)),
            "average_daily_jobs": round(total_jobs / len(valid_dates), 2) if valid_dates else 0.0,
            "maximum_daily_jobs": max(daily_counts.values()) if daily_counts else 0,
            "first_seen_date": min(daily_counts.keys()) if daily_counts else "",
            "last_seen_date": max(daily_counts.keys()) if daily_counts else "",
            "top_titles": top_values((row["title"] for row in group), 8),
            "top_locations": top_values((row["location"] for row in group), 8),
        })

    for (region, scope, category), group in group_rows(report_jobs, ("report_region", "region_scope", "category")).items():
        daily_counts = daily_unique_counts(group)
        advertiser_counts = Counter()
        advertiser_jobs: dict[str, set[str]] = {}
        for row in group:
            advertiser_jobs.setdefault(row["advertiser"], set()).add(row["job_id"])
        for advertiser, ids in advertiser_jobs.items():
            advertiser_counts[advertiser] = len(ids)
        total_jobs = unique_count(group, "job_id")
        all_daily_counts = [daily_counts.get(date, 0) for date in valid_dates]
        top_advertiser, top_count = advertiser_counts.most_common(1)[0] if advertiser_counts else ("", 0)
        role_rows.append({
            "month": month,
            "region": region,
            "region_scope": scope,
            "category": category,
            "total_jobs": total_jobs,
            "feed_days": len(valid_dates),
            "days_seen": sum(1 for value in all_daily_counts if value > 0),
            "seen_ratio_pct": safe_pct(sum(1 for value in all_daily_counts if value > 0), len(valid_dates)),
            "average_daily_jobs": round(total_jobs / len(valid_dates), 2) if valid_dates else 0.0,
            "minimum_daily_jobs": min(all_daily_counts) if all_daily_counts else 0,
            "maximum_daily_jobs": max(all_daily_counts) if all_daily_counts else 0,
            "unique_title_count": unique_count(group, "title_key"),
            "unique_advertiser_count": unique_count(group, "advertiser"),
            "unique_location_count": unique_count(group, "location"),
            "top_advertiser": top_advertiser,
            "top_advertiser_share_pct": safe_pct(top_count, total_jobs),
            "top_titles": top_values((row["title"] for row in group), 10),
            "top_advertisers": top_values((row["advertiser"] for row in group), 10),
            "top_locations": top_values((row["location"] for row in group), 10),
        })

    campaign_rows.sort(key=lambda row: (row["category"], row["region"], -row["total_jobs"], row["advertiser"]))
    role_rows.sort(key=lambda row: (row["category"], row["region"]))
    return campaign_rows, role_rows


def run(input_dir: Path, output_dir: Path, month: str, geo_lookup_path: Path, registers_dir: Optional[Path] = None) -> None:
    base_dir = Path.cwd()
    register_paths = discover_registers(base_dir, registers_dir)
    geo_lookup = load_geo_lookup(geo_lookup_path)
    registers = {category: load_register(path) for category, path in register_paths.items()}
    expanded, valid_dates, errors = load_daily_feeds(input_dir, geo_lookup, registers)
    advertiser_campaigns, role_trends = build_reports(expanded, valid_dates, month)

    output_dir.mkdir(parents=True, exist_ok=True)
    advertiser_path = output_dir / f"{month}-module1-advertiser-campaigns.csv"
    role_path = output_dir / f"{month}-module1-role-trends.csv"
    write_csv(advertiser_path, advertiser_campaigns)
    write_csv(role_path, role_trends)

    lines = [
        f"Month: {month}",
        f"Input directory: {input_dir}",
        f"Valid feed days: {len(valid_dates)}",
        f"Geo lookup: {geo_lookup_path}",
        "Classification mode: register-only",
        "Outputs:",
        f"- {advertiser_path}",
        f"- {role_path}",
    ]
    if errors:
        lines.extend(["Input warnings/errors:", *[f"- {error}" for error in errors]])
    print("\n".join(lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ontap Compiler Module 1 monthly advertiser and role trend report.")
    parser.add_argument("--month", required=True, help="Month in YYYY-MM format.")
    parser.add_argument("--input-dir", default=None, help="Default: pipeline/input-jobg8-archive/<month>")
    parser.add_argument("--output-dir", default="pipeline/reports-module1", help="Output folder.")
    parser.add_argument("--geo-lookup", default="pipeline/geo/geo_lookup.xlsx", help="Path to geo_lookup.xlsx.")
    parser.add_argument("--registers-dir", default="pipeline/registers", help="Folder containing register CSV files.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir) if args.input_dir else Path("pipeline/input-jobg8-archive") / args.month
    run(input_dir, Path(args.output_dir), args.month, Path(args.geo_lookup), Path(args.registers_dir) if args.registers_dir else None)


if __name__ == "__main__":
    main()
