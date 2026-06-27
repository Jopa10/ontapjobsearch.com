#!/usr/bin/env python3
"""
Ontap Compiler Module 1: Monthly Advertiser and Role Trend Report.

Builds two month-level CSV reports from the archived daily JobG8 Excel feeds:
- advertiser campaign summary by advertiser across the full month
- role trends by normalised title and selected register slice

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

import csv
import importlib.util

_pandas_spec = importlib.util.find_spec("pandas")
if _pandas_spec is not None:
    import pandas as pd
else:
    _shim_path = Path(__file__).resolve().with_name("pandas.py")
    _shim_spec = importlib.util.spec_from_file_location("pipeline_scripts_pandas_shim", _shim_path)
    pd = importlib.util.module_from_spec(_shim_spec)
    _shim_spec.loader.exec_module(pd)

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

VALID_ADVERTISER_TYPES = {"direct_employer", "recruitment_agency", "unknown"}
REPORT_ADVERTISER_TYPES = ["direct_employer", "recruitment_agency", "unknown"]
FEED_ADVERTISER_TYPE_MAP = {
    "direct": "direct_employer",
    "direct employer": "direct_employer",
    "direct_employer": "direct_employer",
    "employer": "direct_employer",
    "recruiter": "recruitment_agency",
    "recruitment agency": "recruitment_agency",
    "recruitment_agency": "recruitment_agency",
    "agency": "recruitment_agency",
}


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


def load_advertiser_type_lookup(path: Path) -> Dict[str, str]:
    df = pd.read_csv(path, dtype=str).fillna("")
    missing = {"advertiser", "advertiser_type"}.difference(df.columns)
    if missing:
        raise ValueError(f"{path.name} missing columns: {sorted(missing)}")

    lookup: Dict[str, str] = {}
    display_names: Dict[str, str] = {}
    for row in iter_records(df):
        advertiser = norm_text(row.get("advertiser"))
        advertiser_key = norm_key(advertiser)
        advertiser_type = norm_key(row.get("advertiser_type"))
        if not advertiser_key and not advertiser_type:
            continue
        if not advertiser_key or not advertiser_type:
            raise ValueError(f"{path.name} contains an incomplete advertiser type lookup row: advertiser='{advertiser}', advertiser_type='{advertiser_type}'")
        if advertiser_type not in VALID_ADVERTISER_TYPES:
            raise ValueError(f"{path.name} has invalid advertiser_type '{advertiser_type}' for advertiser '{advertiser}'. Valid values: {sorted(VALID_ADVERTISER_TYPES)}")
        if advertiser_key in lookup and lookup[advertiser_key] != advertiser_type:
            raise ValueError(
                f"{path.name} has conflicting advertiser_type values for normalised advertiser key "
                f"'{advertiser_key}' ({display_names[advertiser_key]!r} vs {advertiser!r}): "
                f"'{lookup[advertiser_key]}' and '{advertiser_type}'"
            )
        lookup[advertiser_key] = advertiser_type
        display_names[advertiser_key] = advertiser
    return lookup


def normalise_feed_advertiser_type(value: object) -> str:
    return FEED_ADVERTISER_TYPE_MAP.get(norm_key(value), "")


def resolve_advertiser_type(advertiser: str, rows: list[dict], advertiser_type_lookup: Dict[str, str]) -> tuple[str, str]:
    advertiser_key = norm_key(advertiser)
    if advertiser_key in advertiser_type_lookup:
        return advertiser_type_lookup[advertiser_key], "lookup"

    counts = Counter(
        resolved
        for resolved in (normalise_feed_advertiser_type(row.get("advertiser_type")) for row in rows)
        if resolved
    )
    if not counts:
        return "unknown", "unavailable"
    if len(counts) == 1:
        return next(iter(counts)), "feed"

    ranked = counts.most_common()
    if len(ranked) > 1 and ranked[0][1] == ranked[1][1]:
        return "unknown", "unavailable"
    return ranked[0][0], "feed_majority"


def load_daily_feeds(input_dir: Path, geo_lookup: Dict[str, str], registers: Dict[str, Dict[str, str]]) -> tuple[list[dict], List[str], List[str]]:
    files = sorted(path for path in input_dir.iterdir() if path.suffix.lower() in {".xlsx", ".xls", ".xlsm"} and not path.name.startswith("~$"))
    if not files:
        raise FileNotFoundError(f"No JobG8 Excel files found in {input_dir}")

    rows: List[dict] = []
    errors: List[str] = []
    valid_dates: List[str] = []
    required_cols = {COL_TITLE, COL_ADVERTISER, COL_AREA}
    seen_base: set[tuple[str, str]] = set()

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
            matched_slices = [category for category, register in registers.items() if register.get(title_key) in SELECTED_CLASSIFICATIONS]
            if not matched_slices:
                matched_slices = ["unclassified"]
            area = norm_text(row.get(COL_AREA))
            job_id = norm_text(row.get(COL_JOB_ID)) if COL_JOB_ID in df.columns else ""
            if not job_id:
                job_id = f"{path.name}:{index + 2}"
            base_key = (date, job_id)
            if base_key in seen_base:
                continue
            seen_base.add(base_key)
            rows.append({
                "month_date": date,
                "job_id": job_id,
                "title": title,
                "normalised_title": title_key or "unknown title",
                "advertiser": norm_text(row.get(COL_ADVERTISER)) or "Unknown advertiser",
                "advertiser_type": norm_text(row.get(COL_ADVERTISER_TYPE)) if COL_ADVERTISER_TYPE in df.columns else "",
                "location": area,
                "raw_location": norm_text(row.get(COL_LOCATION)) if COL_LOCATION in df.columns else "",
                "lookup_region": geo_lookup.get(norm_key(area), "Other / Unknown"),
                "source_file": path.name,
                "slices": matched_slices,
            })

    if not rows:
        raise RuntimeError("No usable JobG8 adverts were found in the monthly feeds.")
    return rows, sorted(set(valid_dates)), errors

def expand_role_slices(base_rows: list[dict]) -> list[dict]:
    expanded: list[dict] = []
    for row in base_rows:
        for slice_name in row.get("slices", []) or ["unclassified"]:
            copy = {key: value for key, value in row.items() if key != "slices"}
            copy["slice"] = slice_name
            expanded.append(copy)
    return expanded


def safe_pct(numerator: int | float, denominator: int | float) -> float:
    return round((numerator / denominator * 100.0), 1) if denominator else 0.0


def top_values(values: Iterable[object], limit: int = 8) -> str:
    return "; ".join(f"{value} ({count})" for value, count in Counter(norm_text(v) for v in values if norm_text(v)).most_common(limit))


def top_distinct_job_values(rows: list[dict], field: str, limit: int = 8) -> str:
    value_jobs: dict[str, set[str]] = {}
    for row in rows:
        value = norm_text(row.get(field))
        job_id = norm_text(row.get("job_id"))
        if value and job_id:
            value_jobs.setdefault(value, set()).add(job_id)
    ranked = sorted(value_jobs.items(), key=lambda item: (-len(item[1]), item[0]))[:limit]
    return "; ".join(f"{value} ({len(job_ids)})" for value, job_ids in ranked)


def unique_count(rows: list[dict], field: str) -> int:
    return len({row[field] for row in rows if norm_text(row.get(field))})


def group_rows(rows: list[dict], fields: tuple[str, ...]) -> dict[tuple, list[dict]]:
    grouped: dict[tuple, list[dict]] = {}
    for row in rows:
        key = tuple(row[field] for field in fields)
        grouped.setdefault(key, []).append(row)
    return grouped


def daily_counts(rows: list[dict]) -> Counter:
    return Counter(row["month_date"] for row in rows)


def window_average(counts: Counter, dates: List[str]) -> float:
    return round(sum(counts.get(date, 0) for date in dates) / len(dates), 2) if dates else 0.0


def trend_label(first_avg: float, last_avg: float, peak: int) -> str:
    GROWTH_THRESHOLD_PCT = 20.0
    DECLINE_THRESHOLD_PCT = -20.0
    SPIKE_PEAK_TO_LAST_AVG_RATIO = 2.0
    if last_avg > 0 and peak >= max(3, last_avg * SPIKE_PEAK_TO_LAST_AVG_RATIO) and last_avg <= first_avg:
        return "spike"
    change = ((last_avg - first_avg) / first_avg * 100.0) if first_avg else (100.0 if last_avg else 0.0)
    if change >= GROWTH_THRESHOLD_PCT:
        return "growing"
    if change <= DECLINE_THRESHOLD_PCT:
        return "declining"
    return "stable"


def advertiser_trend_label(first_avg: float, last_avg: float, peak: int, days_active: int, total_feed_days: int) -> str:
    GROWTH_THRESHOLD_PCT = 20.0
    DECLINE_THRESHOLD_PCT = -20.0
    SPIKE_PEAK_TO_LAST_AVG_RATIO = 3.0
    SPIKE_LAST_TO_PEAK_MAX_RATIO = 0.35
    SPIKE_MAX_ACTIVE_DAY_SHARE = 0.40

    active_day_share = (days_active / total_feed_days) if total_feed_days else 0.0
    if (
        peak >= 3
        and peak >= last_avg * SPIKE_PEAK_TO_LAST_AVG_RATIO
        and last_avg <= peak * SPIKE_LAST_TO_PEAK_MAX_RATIO
        and active_day_share <= SPIKE_MAX_ACTIVE_DAY_SHARE
    ):
        return "spike"

    change = ((last_avg - first_avg) / first_avg * 100.0) if first_avg else (100.0 if last_avg else 0.0)
    if change >= GROWTH_THRESHOLD_PCT:
        return "growing"
    if change <= DECLINE_THRESHOLD_PCT:
        return "declining"
    return "stable"


def write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_reports(base_rows: list[dict], valid_dates: List[str], month: str, advertiser_type_lookup: Optional[Dict[str, str]] = None) -> tuple[list[dict], list[dict], list[dict]]:
    campaign_rows: List[dict] = []
    role_rows: List[dict] = []
    first_window = valid_dates[:5]
    last_window = valid_dates[-5:]

    latest_feed_date = max(valid_dates) if valid_dates else ""
    advertiser_type_lookup = advertiser_type_lookup or {}

    for (advertiser,), group in group_rows(base_rows, ("advertiser",)).items():
        counts = daily_counts(group)
        first_avg = window_average(counts, first_window)
        last_avg = window_average(counts, last_window)
        feed_appearances = len(group)
        days_active = len(counts)
        unique_job_ids = {row["job_id"] for row in group if norm_text(row.get("job_id"))}
        first_seen_by_job: dict[str, str] = {}
        for row in group:
            job_id = norm_text(row.get("job_id"))
            if job_id:
                first_seen_by_job[job_id] = min(first_seen_by_job.get(job_id, row["month_date"]), row["month_date"])
        current_live_jobs = {
            row["job_id"]
            for row in group
            if latest_feed_date and row["month_date"] == latest_feed_date and norm_text(row.get("job_id"))
        }
        peak_daily_live_jobs = max(counts.values()) if counts else 0
        advertiser_type, advertiser_type_source = resolve_advertiser_type(advertiser, group, advertiser_type_lookup)
        campaign_rows.append({
            "month": month,
            "advertiser": advertiser,
            "advertiser_type": advertiser_type,
            "advertiser_type_source": advertiser_type_source,
            "unique_job_ids": len(unique_job_ids),
            "feed_appearances": feed_appearances,
            "new_jobs_first_seen": sum(1 for first_seen in first_seen_by_job.values() if first_seen.startswith(month)),
            "current_live_jobs": len(current_live_jobs),
            "unique_role_count": unique_count(group, "normalised_title"),
            "unique_roles": "; ".join(sorted({row["normalised_title"] for row in group if row["normalised_title"]})),
            "unique_location_count": unique_count(group, "location"),
            "unique_locations": "; ".join(sorted({row["location"] for row in group if row["location"]})),
            "unique_region_count": unique_count(group, "lookup_region"),
            "unique_regions": "; ".join(sorted({row["lookup_region"] for row in group if row["lookup_region"]})),
            "first_day_seen": min(counts.keys()) if counts else "",
            "last_day_seen": max(counts.keys()) if counts else "",
            "days_active": days_active,
            "average_feed_appearances_per_active_day": round(feed_appearances / days_active, 2) if days_active else 0.0,
            "peak_daily_live_jobs": peak_daily_live_jobs,
            "top_roles": top_distinct_job_values(group, "normalised_title", 10),
            "top_regions": top_distinct_job_values(group, "lookup_region", 10),
            "campaign_trend": advertiser_trend_label(first_avg, last_avg, peak_daily_live_jobs, days_active, len(valid_dates)),
            "first_five_day_live_average": first_avg,
            "last_five_day_live_average": last_avg,
            "first_vs_last_five_day_change_pct": round(((last_avg - first_avg) / first_avg * 100.0), 1) if first_avg else (100.0 if last_avg else 0.0),
        })

    role_jobs = expand_role_slices(base_rows)
    for (normalised_title, slice_name), group in group_rows(role_jobs, ("normalised_title", "slice")).items():
        counts = daily_counts(group)
        first_avg = window_average(counts, first_window)
        last_avg = window_average(counts, last_window)
        total = len(group)
        days_active = len(counts)
        advertiser_counts = Counter(row["advertiser"] for row in group)
        top_count = advertiser_counts.most_common(1)[0][1] if advertiser_counts else 0
        role_rows.append({
            "month": month,
            "normalised_title": normalised_title,
            "slice": slice_name,
            "example_live_titles": top_values((row["title"] for row in group), 5),
            "total_adverts": total,
            "days_active": days_active,
            "first_day_seen": min(counts.keys()) if counts else "",
            "last_day_seen": max(counts.keys()) if counts else "",
            "average_adverts_per_active_day": round(total / days_active, 2) if days_active else 0.0,
            "peak_daily_count": max(counts.values()) if counts else 0,
            "unique_advertisers": unique_count(group, "advertiser"),
            "unique_regions": unique_count(group, "lookup_region"),
            "unique_locations": unique_count(group, "location"),
            "top_advertisers": top_values((row["advertiser"] for row in group), 10),
            "top_regions": top_values((row["lookup_region"] for row in group), 10),
            "first_five_day_average": first_avg,
            "last_five_day_average": last_avg,
            "first_vs_last_five_day_change_pct": round(((last_avg - first_avg) / first_avg * 100.0), 1) if first_avg else (100.0 if last_avg else 0.0),
            "trend_label": trend_label(first_avg, last_avg, max(counts.values()) if counts else 0),
            "top_advertiser_share_pct": safe_pct(top_count, total),
        })

    campaign_rows.sort(key=lambda row: (-row["feed_appearances"], row["advertiser"]))
    role_rows.sort(key=lambda row: (row["normalised_title"], row["slice"]))
    advertiser_type_summary = build_advertiser_type_summary(campaign_rows, month)
    return campaign_rows, role_rows, advertiser_type_summary


def build_advertiser_type_summary(campaign_rows: list[dict], month: str) -> list[dict]:
    summary_rows: list[dict] = []
    for advertiser_type in REPORT_ADVERTISER_TYPES:
        rows = [row for row in campaign_rows if row.get("advertiser_type") == advertiser_type]
        summary_rows.append({
            "month": month,
            "advertiser_type": advertiser_type,
            "advertiser_count": len(rows),
            "unique_job_ids": sum(int(row["unique_job_ids"]) for row in rows),
            "feed_appearances": sum(int(row["feed_appearances"]) for row in rows),
            "new_jobs_first_seen": sum(int(row["new_jobs_first_seen"]) for row in rows),
            "current_live_jobs": sum(int(row["current_live_jobs"]) for row in rows),
        })
    return summary_rows


def run(input_dir: Path, output_dir: Path, month: str, geo_lookup_path: Path, registers_dir: Optional[Path] = None, advertiser_type_lookup_path: Path = Path("pipeline/lookup/advertiser_type_lookup.csv")) -> None:
    base_dir = Path.cwd()
    register_paths = discover_registers(base_dir, registers_dir)
    geo_lookup = load_geo_lookup(geo_lookup_path)
    registers = {category: load_register(path) for category, path in register_paths.items()}
    advertiser_type_lookup = load_advertiser_type_lookup(advertiser_type_lookup_path)
    expanded, valid_dates, errors = load_daily_feeds(input_dir, geo_lookup, registers)
    advertiser_campaigns, role_trends, advertiser_type_summary = build_reports(expanded, valid_dates, month, advertiser_type_lookup)

    output_dir.mkdir(parents=True, exist_ok=True)
    advertiser_path = output_dir / f"{month}-module1-advertiser-campaigns.csv"
    role_path = output_dir / f"{month}-module1-role-trends.csv"
    advertiser_type_summary_path = output_dir / f"{month}-module1-advertiser-type-summary.csv"
    write_csv(advertiser_path, advertiser_campaigns)
    write_csv(role_path, role_trends)
    write_csv(advertiser_type_summary_path, advertiser_type_summary)

    lines = [
        f"Month: {month}",
        f"Input directory: {input_dir}",
        f"Valid feed days: {len(valid_dates)}",
        f"Geo lookup: {geo_lookup_path}",
        f"Advertiser type lookup: {advertiser_type_lookup_path}",
        "Classification mode: register-only",
        "Outputs:",
        f"- {advertiser_path}",
        f"- {role_path}",
        f"- {advertiser_type_summary_path}",
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
    parser.add_argument("--advertiser-type-lookup", default="pipeline/lookup/advertiser_type_lookup.csv", help="Path to maintained advertiser type lookup CSV.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir) if args.input_dir else Path("pipeline/input-jobg8-archive") / args.month
    run(input_dir, Path(args.output_dir), args.month, Path(args.geo_lookup), Path(args.registers_dir) if args.registers_dir else None, Path(args.advertiser_type_lookup))


if __name__ == "__main__":
    main()
