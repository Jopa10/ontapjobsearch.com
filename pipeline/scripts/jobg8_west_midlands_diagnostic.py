#!/usr/bin/env python3
"""Review-only diagnostic for West Midlands JobG8 coverage.

Reads an archived month of raw JobG8 feeds and reports every job mapped to the
three West Midlands lookup regions. Titles are assessed against the same six
registers and selected classifications used by Compiler Module 2.

This script does not publish jobs or alter any register.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Dict, List

import pandas as pd

from scripts.jobg8_module_2_monthly_category_profiler import (
    COL_AREA,
    COL_COMPANY,
    COL_JOB_ID,
    COL_LOCATION,
    COL_TITLE,
    REGISTER_SPECS,
    SELECTED_CLASSIFICATIONS,
    discover_registers,
    extract_date,
    load_geo_lookup,
    load_register,
    norm_key,
    norm_text,
)

TARGET_REGIONS = {
    "West Midlands - Birmingham & Solihull",
    "West Midlands - Black Country",
    "West Midlands - Coventry & Warwickshire",
}


def classify_title(title_key: str, registers: Dict[str, Dict[str, str]]) -> dict:
    matches = {
        category: register[title_key]
        for category, register in registers.items()
        if title_key in register
    }
    selected = sorted(
        category
        for category, classification in matches.items()
        if classification in SELECTED_CLASSIFICATIONS
    )

    if "admin_service" in selected:
        status = "admin_service_selected"
    elif selected:
        status = "other_registered_category_selected"
    elif matches:
        status = "registered_but_not_selected"
    else:
        status = "unregistered_title"

    return {
        "diagnostic_status": status,
        "selected_categories": "; ".join(selected),
        "register_matches": "; ".join(
            f"{category}:{classification}"
            for category, classification in sorted(matches.items())
        ),
    }


def load_target_jobs(
    input_dir: Path,
    geo_lookup: Dict[str, str],
    registers: Dict[str, Dict[str, str]],
) -> tuple[pd.DataFrame, List[str], List[str]]:
    files = sorted(
        path
        for path in input_dir.iterdir()
        if path.suffix.lower() in {".xlsx", ".xls", ".xlsm"}
        and not path.name.startswith("~$")
    )
    if not files:
        raise FileNotFoundError(f"No JobG8 Excel files found in {input_dir}")

    required_columns = {COL_TITLE, COL_COMPANY, COL_AREA}
    rows: List[dict] = []
    valid_dates: List[str] = []
    errors: List[str] = []

    for path in files:
        date = extract_date(path)
        if not date:
            errors.append(f"{path.name}: date not recognised from filename")
            continue

        try:
            feed = pd.read_excel(path, dtype=str).fillna("")
        except Exception as exc:
            errors.append(f"{path.name}: failed to read: {exc}")
            continue

        missing = required_columns.difference(feed.columns)
        if missing:
            errors.append(f"{path.name}: missing columns {sorted(missing)}")
            continue

        valid_dates.append(date)
        for index, row in feed.iterrows():
            raw_area = norm_text(row.get(COL_AREA))
            region = geo_lookup.get(norm_key(raw_area), "Other / Unknown")
            if region not in TARGET_REGIONS:
                continue

            title = norm_text(row.get(COL_TITLE))
            title_key = norm_key(title)
            job_id = norm_text(row.get(COL_JOB_ID)) if COL_JOB_ID in feed.columns else ""
            if not job_id:
                job_id = f"{path.name}:{index + 2}"

            assessment = classify_title(title_key, registers)
            rows.append(
                {
                    "date": date,
                    "job_id": job_id,
                    "title": title,
                    "company": norm_text(row.get(COL_COMPANY)) or "Unknown company",
                    "raw_area": raw_area,
                    "raw_location": (
                        norm_text(row.get(COL_LOCATION))
                        if COL_LOCATION in feed.columns
                        else ""
                    ),
                    "lookup_region": region,
                    "source_file": path.name,
                    **assessment,
                }
            )

    if not rows:
        raise RuntimeError("No jobs mapped to the three target West Midlands regions.")

    detail = pd.DataFrame(rows).drop_duplicates(
        subset=["date", "job_id", "lookup_region"]
    )
    return detail, sorted(set(valid_dates)), errors


def build_unique_job_review(detail: pd.DataFrame) -> pd.DataFrame:
    group_columns = [
        "lookup_region",
        "job_id",
        "title",
        "company",
        "raw_area",
        "raw_location",
        "diagnostic_status",
        "selected_categories",
        "register_matches",
    ]
    review = (
        detail.groupby(group_columns, dropna=False)
        .agg(
            first_seen=("date", "min"),
            last_seen=("date", "max"),
            days_seen=("date", "nunique"),
        )
        .reset_index()
    )
    return review.sort_values(
        ["lookup_region", "diagnostic_status", "days_seen", "title"],
        ascending=[True, True, False, True],
    )


def build_summary(detail: pd.DataFrame, valid_dates: List[str], month: str) -> pd.DataFrame:
    rows: List[dict] = []
    total_days = len(valid_dates)

    for region in sorted(TARGET_REGIONS):
        region_jobs = detail[detail["lookup_region"] == region]
        for status in [
            "admin_service_selected",
            "other_registered_category_selected",
            "registered_but_not_selected",
            "unregistered_title",
        ]:
            group = region_jobs[region_jobs["diagnostic_status"] == status]
            daily_counts = [
                int(group.loc[group["date"] == date, "job_id"].nunique())
                for date in valid_dates
            ]
            title_counts = Counter(group["title"])
            rows.append(
                {
                    "month": month,
                    "lookup_region": region,
                    "diagnostic_status": status,
                    "unique_jobs": int(group["job_id"].nunique()),
                    "unique_titles": int(group["title"].nunique()),
                    "unique_companies": int(group["company"].nunique()),
                    "unique_areas": int(group["raw_area"].nunique()),
                    "days_with_jobs": sum(count > 0 for count in daily_counts),
                    "average_daily_active_jobs": round(
                        sum(daily_counts) / total_days if total_days else 0.0, 2
                    ),
                    "maximum_daily_active_jobs": max(daily_counts, default=0),
                    "top_titles": "; ".join(
                        f"{title} ({count})"
                        for title, count in title_counts.most_common(15)
                    ),
                }
            )

    return pd.DataFrame(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--geo-lookup", type=Path, required=True)
    parser.add_argument("--registers-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_dir = Path.cwd().parent if Path.cwd().name == "pipeline" else Path.cwd()

    geo_lookup = load_geo_lookup(args.geo_lookup)
    register_paths = discover_registers(base_dir, args.registers_dir)
    registers = {
        category: load_register(path)
        for category, path in register_paths.items()
    }

    detail, valid_dates, errors = load_target_jobs(
        args.input_dir,
        geo_lookup,
        registers,
    )
    unique_review = build_unique_job_review(detail)
    summary = build_summary(detail, valid_dates, args.month)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / f"{args.month}-west-midlands-diagnostic-summary.csv"
    detail_path = args.output_dir / f"{args.month}-west-midlands-diagnostic-detail.csv"
    log_path = args.output_dir / f"{args.month}-west-midlands-diagnostic-log.txt"

    summary.to_csv(summary_path, index=False, encoding="utf-8-sig")
    unique_review.to_csv(detail_path, index=False, encoding="utf-8-sig")
    log_path.write_text(
        "\n".join(
            [
                f"Month: {args.month}",
                f"Valid feed days: {len(valid_dates)}",
                f"First feed day: {valid_dates[0] if valid_dates else ''}",
                f"Last feed day: {valid_dates[-1] if valid_dates else ''}",
                f"Target daily rows: {len(detail)}",
                f"Unique target jobs: {detail['job_id'].nunique()}",
                f"Input errors: {len(errors)}",
                *[f"- {error}" for error in errors],
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(summary.to_string(index=False))
    print(f"Wrote {summary_path}")
    print(f"Wrote {detail_path}")
    print(f"Wrote {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
