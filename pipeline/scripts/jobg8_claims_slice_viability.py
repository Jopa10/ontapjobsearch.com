from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import Counter
from pathlib import Path

import pandas as pd

from pipeline.scripts.jobg8_claims_family_validate import boundary_decision, fingerprint
from pipeline.scripts.jobg8_insurance_claims_discovery import (
    AREA_COL,
    DESCRIPTION_COL,
    LOCATION_COL,
    SALARY_MAX_COL,
    SALARY_PERIOD_COL,
    TITLE_COL,
    annualise,
    is_broad_candidate,
    load_geo_lookups,
    norm,
    ontap_region,
)

CATALOG_PATH = Path("config/job_slice_catalog.json")
EXCLUDED_REGIONS = {"Northern Ireland - East"}
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")


def dated_feeds(input_dir: Path, max_dates: int = 7) -> list[tuple[str, Path]]:
    by_date: dict[str, Path] = {}
    for path in sorted(input_dir.iterdir()):
        if path.suffix.lower() not in {".xlsx", ".xls", ".xlsm"}:
            continue
        match = DATE_RE.search(path.stem)
        if not match:
            continue
        by_date[match.group(1)] = path
    if not by_date:
        raise SystemExit(f"No dated Excel feeds found in {input_dir}")
    dates = sorted(by_date)[-max_dates:]
    return [(date, by_date[date]) for date in dates]


def canonical_regions() -> list[str]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8-sig"))
    regions = sorted([name for name in catalog.get("regions", {}) if name not in EXCLUDED_REGIONS], key=str.casefold)
    if len(regions) != 33:
        raise RuntimeError(f"Expected 33 canonical regions, found {len(regions)}")
    return regions


def assess_feed(feed: Path, regions: set[str], area_lookup: dict[str, str], fallback: dict[str, str]) -> tuple[Counter[str], int, int]:
    raw = pd.read_excel(feed, dtype=str).fillna("")
    counts: Counter[str] = Counter()
    seen: set[str] = set()
    unknown = 0
    for _, row in raw.iterrows():
        title = norm(row.get(TITLE_COL, ""))
        description = norm(row.get(DESCRIPTION_COL, ""))
        if not is_broad_candidate(title, description):
            continue
        period = norm(row.get(SALARY_PERIOD_COL, ""))
        annual_max = annualise(row.get(SALARY_MAX_COL, ""), period)
        decision, _reason = boundary_decision(title, description, annual_max)
        if decision != "IN":
            continue
        location = norm(row.get(LOCATION_COL, ""))
        fp = fingerprint(title, description, location)
        if fp in seen:
            continue
        seen.add(fp)
        region = ontap_region(row.get(AREA_COL, ""), row.get(LOCATION_COL, ""), area_lookup, fallback)
        if region in regions:
            counts[region] += 1
        else:
            unknown += 1
    return counts, len(seen), unknown


def evidence_grade(values: list[int]) -> str:
    if len(values) < 3:
        return "INSUFFICIENT_HISTORY"
    latest = values[-1]
    days_6_plus = sum(value >= 6 for value in values)
    days_4_plus = sum(value >= 4 for value in values)
    if latest >= 6 and days_6_plus >= 3:
        return "STRONG_REVIEW_CANDIDATE"
    if latest >= 4 and days_4_plus >= 3:
        return "WATCH"
    return "THIN"


def main() -> int:
    ap = argparse.ArgumentParser(description="Assess Claims Support regional recurrence across recent archived JobG8 feed dates.")
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--geo-lookup", type=Path, default=Path("pipeline/geo/geo_lookup.xlsx"))
    ap.add_argument("--max-dates", type=int, default=7)
    args = ap.parse_args()
    feeds = dated_feeds(args.input_dir, max_dates=max(1, args.max_dates))
    region_list = canonical_regions()
    region_set = set(region_list)
    area_lookup, fallback = load_geo_lookups(args.geo_lookup)
    daily_rows: list[dict[str, object]] = []
    total_by_date: dict[str, int] = {}
    unknown_by_date: dict[str, int] = {}
    for feed_date, feed in feeds:
        counts, total_unique_in, unknown = assess_feed(feed, region_set, area_lookup, fallback)
        total_by_date[feed_date] = total_unique_in
        unknown_by_date[feed_date] = unknown
        for region in region_list:
            daily_rows.append({"feed_date": feed_date, "region": region, "claims_support_count": counts.get(region, 0)})
    daily = pd.DataFrame(daily_rows)
    dates = [date for date, _ in feeds]
    latest_date = dates[-1]
    summary_rows: list[dict[str, object]] = []
    for region in region_list:
        region_daily = daily.loc[daily["region"] == region].set_index("feed_date")
        values = [int(region_daily.loc[date, "claims_support_count"]) for date in dates]
        grade = evidence_grade(values)
        summary_rows.append({
            "region": region, "days_observed": len(values), "latest_feed_date": latest_date, "latest_count": values[-1],
            "average_count": round(sum(values) / len(values), 2), "median_count": statistics.median(values),
            "minimum_count": min(values), "maximum_count": max(values), "days_with_1_plus": sum(value >= 1 for value in values),
            "days_with_4_plus": sum(value >= 4 for value in values), "days_with_6_plus": sum(value >= 6 for value in values),
            "recent_counts": " / ".join(str(value) for value in values), "evidence_grade": grade,
        })
    summary = pd.DataFrame(summary_rows).sort_values(by=["latest_count", "average_count", "region"], ascending=[False, False, True])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "jobg8-claims-slice-viability-current.csv"
    md_path = args.output_dir / "jobg8-claims-slice-viability-current.md"
    summary.to_csv(csv_path, index=False, encoding="utf-8-sig")
    strong = summary.loc[summary["evidence_grade"] == "STRONG_REVIEW_CANDIDATE"]
    watch = summary.loc[summary["evidence_grade"] == "WATCH"]
    lines = [
        "# JobG8 Claims Support regional viability diagnostic", "", f"Observed feed dates: **{len(dates)}** ({dates[0]} to {dates[-1]}).",
        f"Latest feed: **{latest_date}**.", f"Content-unique IN jobs on latest feed: **{total_by_date[latest_date]}**; unmapped/unknown region: **{unknown_by_date[latest_date]}**.", "",
        "Diagnostic only: this does not activate a slice. `STRONG_REVIEW_CANDIDATE` is deliberately an evidence signal, not an automatic LIVE gate.", "",
        "For this diagnostic, a region is `STRONG_REVIEW_CANDIDATE` when the latest feed has 6+ Claims Support jobs and at least 3 observed feed dates have 6+ jobs. `WATCH` means latest 4+ and at least 3 observed feed dates at 4+. This mirrors the existing 6+ recurrence style used elsewhere in Ontap as a conservative review signal; explicit approval is still required.", "",
        f"Strong review candidates: **{len(strong)}**.", f"Watch regions: **{len(watch)}**.", "", "## Regional evidence", "",
        "| Region | Latest | Avg | Median | 6+ days | Recent counts | Evidence |", "|---|---:|---:|---:|---:|---|---|",
    ]
    for _, row in summary.iterrows():
        lines.append(f"| {str(row['region']).replace('|', '/')} | {int(row['latest_count'])} | {float(row['average_count']):.2f} | {float(row['median_count']):.1f} | {int(row['days_with_6_plus'])} | {row['recent_counts']} | {row['evidence_grade']} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(md_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
