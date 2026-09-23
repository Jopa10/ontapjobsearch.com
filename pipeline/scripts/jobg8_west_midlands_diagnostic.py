#!/usr/bin/env python3
"""Review-only diagnostic for West Midlands JobG8 coverage.

Reports every job mapped to the three West Midlands lookup regions and separately
audits every raw row whose Area or Location contains "Birmingham", regardless of
where the geo lookup maps it. This script does not publish jobs or alter registers.
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
STATUSES = [
    "admin_service_selected",
    "other_registered_category_selected",
    "registered_but_not_selected",
    "unregistered_title",
]


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


def load_jobs(
    input_dir: Path,
    geo_lookup: Dict[str, str],
    registers: Dict[str, Dict[str, str]],
) -> tuple[pd.DataFrame, pd.DataFrame, List[str], List[str]]:
    files = sorted(
        path for path in input_dir.iterdir()
        if path.suffix.lower() in {".xlsx", ".xls", ".xlsm"}
        and not path.name.startswith("~$")
    )
    if not files:
        raise FileNotFoundError(f"No JobG8 Excel files found in {input_dir}")

    required = {COL_TITLE, COL_COMPANY, COL_AREA}
    target_rows: List[dict] = []
    birmingham_rows: List[dict] = []
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
        missing = required.difference(feed.columns)
        if missing:
            errors.append(f"{path.name}: missing columns {sorted(missing)}")
            continue

        valid_dates.append(date)
        for index, row in feed.iterrows():
            raw_area = norm_text(row.get(COL_AREA))
            raw_location = (
                norm_text(row.get(COL_LOCATION)) if COL_LOCATION in feed.columns else ""
            )
            region = geo_lookup.get(norm_key(raw_area), "Other / Unknown")
            mentions_birmingham = "birmingham" in norm_key(
                f"{raw_area} {raw_location}"
            )
            if region not in TARGET_REGIONS and not mentions_birmingham:
                continue

            title = norm_text(row.get(COL_TITLE))
            job_id = norm_text(row.get(COL_JOB_ID)) if COL_JOB_ID in feed.columns else ""
            if not job_id:
                job_id = f"{path.name}:{index + 2}"
            record = {
                "date": date,
                "job_id": job_id,
                "title": title,
                "company": norm_text(row.get(COL_COMPANY)) or "Unknown company",
                "raw_area": raw_area,
                "raw_location": raw_location,
                "lookup_region": region,
                "source_file": path.name,
                **classify_title(norm_key(title), registers),
            }
            if region in TARGET_REGIONS:
                target_rows.append(record)
            if mentions_birmingham:
                birmingham_rows.append(record)

    if not target_rows:
        raise RuntimeError("No jobs mapped to the target West Midlands regions.")

    target = pd.DataFrame(target_rows).drop_duplicates(
        subset=["date", "job_id", "lookup_region"]
    )
    birmingham = pd.DataFrame(birmingham_rows)
    if not birmingham.empty:
        birmingham = birmingham.drop_duplicates(
            subset=["date", "job_id", "raw_area", "raw_location"]
        )
    return target, birmingham, sorted(set(valid_dates)), errors


def build_unique_review(detail: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "lookup_region", "job_id", "title", "company", "raw_area",
        "raw_location", "diagnostic_status", "selected_categories",
        "register_matches",
    ]
    return (
        detail.groupby(columns, dropna=False)
        .agg(first_seen=("date", "min"), last_seen=("date", "max"), days_seen=("date", "nunique"))
        .reset_index()
        .sort_values(
            ["lookup_region", "diagnostic_status", "days_seen", "title"],
            ascending=[True, True, False, True],
        )
    )


def build_summary(detail: pd.DataFrame, valid_dates: List[str], month: str) -> pd.DataFrame:
    rows: List[dict] = []
    total_days = len(valid_dates)
    for region in sorted(TARGET_REGIONS):
        region_jobs = detail[detail["lookup_region"] == region]
        for status in STATUSES:
            group = region_jobs[region_jobs["diagnostic_status"] == status]
            daily = [
                int(group.loc[group["date"] == date, "job_id"].nunique())
                for date in valid_dates
            ]
            rows.append({
                "month": month,
                "lookup_region": region,
                "diagnostic_status": status,
                "unique_jobs": int(group["job_id"].nunique()),
                "unique_titles": int(group["title"].nunique()),
                "unique_companies": int(group["company"].nunique()),
                "unique_areas": int(group["raw_area"].nunique()),
                "days_with_jobs": sum(count > 0 for count in daily),
                "average_daily_active_jobs": round(sum(daily) / total_days if total_days else 0.0, 2),
                "maximum_daily_active_jobs": max(daily, default=0),
                "top_titles": "; ".join(
                    f"{title} ({count})"
                    for title, count in Counter(group["title"]).most_common(15)
                ),
            })
    return pd.DataFrame(rows)


def build_birmingham_audit(detail: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if detail.empty:
        columns = [
            "lookup_region", "job_id", "title", "company", "raw_area",
            "raw_location", "diagnostic_status", "selected_categories",
            "register_matches", "first_seen", "last_seen", "days_seen",
        ]
        return pd.DataFrame(columns=columns), pd.DataFrame(columns=[
            "lookup_region", "raw_area", "diagnostic_status", "unique_jobs",
            "unique_titles", "days_with_rows", "top_titles",
        ])

    review = build_unique_review(detail)
    summary_rows: List[dict] = []
    for (region, area, status), group in detail.groupby(
        ["lookup_region", "raw_area", "diagnostic_status"], dropna=False
    ):
        summary_rows.append({
            "lookup_region": region,
            "raw_area": area,
            "diagnostic_status": status,
            "unique_jobs": int(group["job_id"].nunique()),
            "unique_titles": int(group["title"].nunique()),
            "days_with_rows": int(group["date"].nunique()),
            "top_titles": "; ".join(
                f"{title} ({count})"
                for title, count in Counter(group["title"]).most_common(15)
            ),
        })
    summary = pd.DataFrame(summary_rows).sort_values(
        ["lookup_region", "raw_area", "diagnostic_status"]
    )
    return review, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month", required=True)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--geo-lookup", type=Path, required=True)
    parser.add_argument("--registers-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_dir = Path.cwd().parent if Path.cwd().name == "pipeline" else Path.cwd()
    geo_lookup = load_geo_lookup(args.geo_lookup)
    registers = {
        category: load_register(path)
        for category, path in discover_registers(base_dir, args.registers_dir).items()
    }
    detail, birmingham, valid_dates, errors = load_jobs(
        args.input_dir, geo_lookup, registers
    )
    summary = build_summary(detail, valid_dates, args.month)
    unique_review = build_unique_review(detail)
    birmingham_review, birmingham_summary = build_birmingham_audit(birmingham)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.output_dir / args.month
    paths = {
        "summary": Path(f"{prefix}-west-midlands-diagnostic-summary.csv"),
        "detail": Path(f"{prefix}-west-midlands-diagnostic-detail.csv"),
        "birmingham_summary": Path(f"{prefix}-birmingham-location-audit-summary.csv"),
        "birmingham_detail": Path(f"{prefix}-birmingham-location-audit-detail.csv"),
        "log": Path(f"{prefix}-west-midlands-diagnostic-log.txt"),
    }
    summary.to_csv(paths["summary"], index=False, encoding="utf-8-sig")
    unique_review.to_csv(paths["detail"], index=False, encoding="utf-8-sig")
    birmingham_summary.to_csv(paths["birmingham_summary"], index=False, encoding="utf-8-sig")
    birmingham_review.to_csv(paths["birmingham_detail"], index=False, encoding="utf-8-sig")
    paths["log"].write_text(
        "\n".join([
            f"Month: {args.month}",
            f"Valid feed days: {len(valid_dates)}",
            f"Target daily rows: {len(detail)}",
            f"Unique target jobs: {detail['job_id'].nunique()}",
            f"Birmingham-match daily rows: {len(birmingham)}",
            f"Unique Birmingham-match jobs: {birmingham['job_id'].nunique() if not birmingham.empty else 0}",
            f"Birmingham mapped regions: {'; '.join(sorted(birmingham['lookup_region'].unique())) if not birmingham.empty else ''}",
            f"Input errors: {len(errors)}",
            *[f"- {error}" for error in errors],
        ]) + "\n",
        encoding="utf-8",
    )

    print(summary.to_string(index=False))
    print("\nBirmingham location audit")
    print(birmingham_summary.to_string(index=False))
    for path in paths.values():
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
