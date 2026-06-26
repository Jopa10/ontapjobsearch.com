#!/usr/bin/env python3
"""
Ontap Compiler Module 2: Monthly Category Profiler

Purpose
-------
Analyse every region × registered category across a folder of daily JobG8 feeds.

Inputs
------
- Daily JobG8 Excel files for one month.
- geo_lookup.xlsx with columns: Area, Cluster.
- Six external title-classification registers.

Outputs
-------
- <month>-module2-category-validation.csv
- <month>-module2-daily-counts.csv
- <month>-module2-unknown-location-detail.csv
- <month>-module2-run-log.txt

Classification remains register-only:
- HIGH_CONFIDENCE and ELASTIC_FIT are selected.
- A job may contribute to more than one registered category.
- No hard-coded family fallback is used.

Recommendation thresholds are deliberately kept in the CONFIG section below so
they can be reviewed and changed without rewriting the analysis logic.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path = [
    entry
    for entry in sys.path
    if Path(entry or ".").resolve() != SCRIPT_DIR
]

import pandas as pd


# ---------------------------------------------------------------------------
# CONFIG: recommendation and diagnostic thresholds
# ---------------------------------------------------------------------------

CONFIG = {
    # Core persistence/volume test used for BUILD or MAINTAIN.
    "minimum_seen_ratio": 0.80,
    "minimum_average_daily_jobs": 6.0,

    # Breadth safeguards.
    "minimum_unique_titles": 5,
    "minimum_unique_companies": 3,
    "minimum_unique_locations": 3,

    # Concentration diagnostics.
    "severe_top_1_company_share": 0.50,
    "severe_top_2_company_share": 0.70,

    # WATCH floor: enough evidence to keep under review even if not build-ready.
    "watch_minimum_average_daily_jobs": 3.0,
    "watch_minimum_seen_ratio": 0.50,
    "watch_minimum_peak_jobs": 6,

    # Direction/campaign diagnostics.
    "meaningful_decline_pct": -20.0,
    "campaign_driven_decline_share": 0.60,
}

SELECTED_CLASSIFICATIONS = {"HIGH_CONFIDENCE", "ELASTIC_FIT"}

REGISTER_SPECS = {
    "support_worker": [
        "support_worker_title_classification_register*.csv",
    ],
    "admin_service": [
        "admin_service_title_classification_register*.csv",
    ],
    "finance_accounts": [
        "finance_accounts_title_classification_register*.csv",
    ],
    "customer_service_contact_centre": [
        "customer_service_contact_centre_title_classification_register*.csv",
    ],
    "warehouse_logistics": [
        "warehouse_logistics_title_classification_register*.csv",
    ],
    "hr_recruitment": [
        "hr_recruitment_title_classification_register*.csv",
    ],
}

# Existing live Ontap slices.
# Yorkshire - West and Yorkshire - South map directly to the current
# geo_lookup Cluster values.
# The published North East page aggregates the three lookup regions below.
LIVE_SLICE_GROUPS = {
    "Yorkshire - West": {
        "published_region": "Yorkshire - West",
        "lookup_regions": ["Yorkshire - West"],
        "categories": {"support_worker", "admin_service"},
    },
    "Yorkshire - South": {
        "published_region": "Yorkshire - South",
        "lookup_regions": ["Yorkshire - South"],
        "categories": {"support_worker", "admin_service"},
    },
    "North East": {
        "published_region": "North East",
        "lookup_regions": [
            "North East - Tyneside, Wearside & Northumberland",
            "North East - County Durham & Darlington/Hartlepool",
            "North East - Tees Valley",
        ],
        "categories": {"support_worker", "admin_service"},
    },
}

COL_JOB_ID = "/Job/DisplayReference"
COL_TITLE = "/Job/Position"
COL_COMPANY = "/Job/AdvertiserName"
COL_AREA = "/Job/Area"
COL_LOCATION = "/Job/Location"


# ---------------------------------------------------------------------------
# Normalisation and input discovery
# ---------------------------------------------------------------------------

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
    matches = [p for p in matches if not p.name.startswith("~$")]
    if not matches:
        return None
    return max(matches, key=lambda p: (p.stat().st_mtime, p.name.lower()))


def discover_registers(base_dir: Path, registers_dir: Optional[Path]) -> Dict[str, Path]:
    search_dirs = []
    if registers_dir:
        search_dirs.append(registers_dir)
    search_dirs.extend([
        base_dir / "pipeline" / "registers",
        base_dir / "registers",
        base_dir,
    ])

    resolved: Dict[str, Path] = {}
    missing: List[str] = []
    for category, patterns in REGISTER_SPECS.items():
        found = find_latest_matching_file(search_dirs, patterns)
        if found:
            resolved[category] = found
        else:
            missing.append(category)

    if missing:
        raise FileNotFoundError(
            "Missing required register(s): " + ", ".join(missing)
        )
    return resolved


# ---------------------------------------------------------------------------
# Geography and register loading
# ---------------------------------------------------------------------------

def load_geo_lookup(path: Path) -> Dict[str, str]:
    df = pd.read_excel(path, dtype=str).fillna("")
    required = {"Area", "Cluster"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Geo lookup missing columns: {sorted(missing)}")

    lookup: Dict[str, str] = {}
    for _, row in df.iterrows():
        area = norm_key(row["Area"])
        cluster = norm_text(row["Cluster"])
        if area and cluster:
            lookup[area] = cluster

    if not lookup:
        raise ValueError("Geo lookup contains no usable Area → Cluster mappings.")
    return lookup


def load_register(path: Path) -> Dict[str, str]:
    df = pd.read_csv(path, dtype=str).fillna("")
    required = {"title", "classification"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{path.name} missing columns: {sorted(missing)}")

    title_map: Dict[str, str] = {}
    for _, row in df.iterrows():
        title = norm_key(row["title"])
        classification = norm_text(row["classification"]).upper()
        if title:
            title_map[title] = classification
    return title_map


# ---------------------------------------------------------------------------
# Feed loading and register-only expansion
# ---------------------------------------------------------------------------

def load_daily_feeds(
    input_dir: Path,
    geo_lookup: Dict[str, str],
    registers: Dict[str, Dict[str, str]],
) -> tuple[pd.DataFrame, List[str], List[str]]:
    files = sorted(
        p for p in input_dir.iterdir()
        if p.suffix.lower() in {".xlsx", ".xls", ".xlsm"}
        and not p.name.startswith("~$")
    )
    if not files:
        raise FileNotFoundError(f"No JobG8 Excel files found in {input_dir}")

    rows: List[dict] = []
    errors: List[str] = []
    valid_dates: List[str] = []

    required_cols = {COL_TITLE, COL_COMPANY, COL_AREA}

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

        for index, row in df.iterrows():
            title = norm_text(row.get(COL_TITLE))
            title_key = norm_key(title)
            area = norm_text(row.get(COL_AREA))
            raw_location = (
                norm_text(row.get(COL_LOCATION))
                if COL_LOCATION in df.columns
                else ""
            )
            area_key = norm_key(area)
            region = geo_lookup.get(area_key, "Other / Unknown")
            if region == "Other / Unknown":
                unknown_reason = (
                    "blank_or_missing_area"
                    if not area_key
                    else "area_not_found_in_geo_lookup"
                )
            else:
                unknown_reason = ""
            company = norm_text(row.get(COL_COMPANY)) or "Unknown company"
            job_id = norm_text(row.get(COL_JOB_ID)) if COL_JOB_ID in df.columns else ""
            if not job_id:
                job_id = f"{path.name}:{index + 2}"

            matched_categories = [
                category
                for category, register in registers.items()
                if register.get(title_key) in SELECTED_CLASSIFICATIONS
            ]

            for category in matched_categories:
                rows.append({
                    "date": date,
                    "job_id": job_id,
                    "title": title,
                    "title_key": title_key,
                    "company": company,
                    "location": area,
                    "raw_location": raw_location,
                    "lookup_region": region,
                    "unknown_reason": unknown_reason,
                    "category": category,
                    "source_file": path.name,
                })

    if not rows:
        raise RuntimeError("No jobs matched HIGH_CONFIDENCE or ELASTIC_FIT in the six registers.")

    expanded = pd.DataFrame(rows).drop_duplicates(
        subset=["date", "job_id", "category", "lookup_region"]
    )
    return expanded, sorted(set(valid_dates)), errors


# ---------------------------------------------------------------------------
# Live-page aggregation
# ---------------------------------------------------------------------------

def add_published_region_rows(expanded: pd.DataFrame) -> pd.DataFrame:
    """
    Preserve all geo_lookup regions as their own analytical regions, then add one
    extra aggregated North East row-set for the live combined North East page.
    """
    frames = [expanded.assign(report_region=expanded["lookup_region"],
                              region_scope="lookup_region")]

    north_east = LIVE_SLICE_GROUPS["North East"]
    combined = expanded[
        expanded["lookup_region"].isin(north_east["lookup_regions"])
    ].copy()
    if not combined.empty:
        combined["report_region"] = north_east["published_region"]
        combined["region_scope"] = "published_aggregate"
        frames.append(combined)

    return pd.concat(frames, ignore_index=True)


def is_live_slice(report_region: str, category: str) -> bool:
    group = LIVE_SLICE_GROUPS.get(report_region)
    return bool(group and category in group["categories"])


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def safe_share(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def top_values(series: pd.Series, limit: int = 8) -> str:
    values = [norm_text(v) for v in series if norm_text(v)]
    return "; ".join(
        f"{value} ({count})"
        for value, count in Counter(values).most_common(limit)
    )


def first_last_window(valid_dates: List[str], size: int = 5) -> tuple[List[str], List[str]]:
    return valid_dates[:size], valid_dates[-size:]


def decline_diagnostic(group: pd.DataFrame, first_dates: List[str], last_dates: List[str]) -> dict:
    first = group[group["date"].isin(first_dates)]
    last = group[group["date"].isin(last_dates)]

    first_avg = len(first) / len(first_dates) if first_dates else 0.0
    last_avg = len(last) / len(last_dates) if last_dates else 0.0
    direction_pct = ((last_avg - first_avg) / first_avg * 100.0) if first_avg else 0.0

    if direction_pct > CONFIG["meaningful_decline_pct"]:
        return {
            "decline_type": "no_meaningful_decline",
            "decline_explanation": "",
            "first_avg": first_avg,
            "last_avg": last_avg,
            "direction_pct": direction_pct,
        }

    first_company_counts = first["company"].value_counts()
    leading_companies = list(first_company_counts.head(2).index)

    first_without = first[~first["company"].isin(leading_companies)]
    last_without = last[~last["company"].isin(leading_companies)]
    first_without_avg = len(first_without) / len(first_dates) if first_dates else 0.0
    last_without_avg = len(last_without) / len(last_dates) if last_dates else 0.0

    total_decline = max(first_avg - last_avg, 0.0)
    residual_decline = max(first_without_avg - last_without_avg, 0.0)
    campaign_share = max(0.0, 1.0 - safe_share(residual_decline, total_decline)) if total_decline else 0.0

    if leading_companies and campaign_share >= CONFIG["campaign_driven_decline_share"]:
        decline_type = "mainly_large_campaigns_disappearing"
        explanation = (
            f"Top early advertiser(s) {', '.join(leading_companies)} account for "
            f"approximately {campaign_share:.0%} of the measured decline."
        )
    else:
        decline_type = "broad_based_decline"
        explanation = (
            "The decline remains material after removing the two largest "
            "first-window advertisers."
        )

    return {
        "decline_type": decline_type,
        "decline_explanation": explanation,
        "first_avg": first_avg,
        "last_avg": last_avg,
        "direction_pct": direction_pct,
    }


def concentration_metrics(group: pd.DataFrame) -> dict:
    counts = group["company"].value_counts()
    total = len(group)
    top1_share = safe_share(int(counts.iloc[0]) if len(counts) >= 1 else 0, total)
    top2_share = safe_share(int(counts.iloc[:2].sum()) if len(counts) >= 1 else 0, total)

    severe = (
        top1_share >= CONFIG["severe_top_1_company_share"]
        or top2_share >= CONFIG["severe_top_2_company_share"]
    )

    if severe:
        risk = "HIGH"
    elif top1_share >= 0.35 or top2_share >= 0.55:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "top_1_company_share_pct": round(top1_share * 100, 1),
        "top_2_company_share_pct": round(top2_share * 100, 1),
        "concentration_risk": risk,
        "severe_concentration": severe,
    }


def recommendation(metrics: dict, live: bool) -> tuple[str, str]:
    persistence_ok = metrics["seen_ratio"] >= CONFIG["minimum_seen_ratio"]
    volume_ok = metrics["average_daily_count"] >= CONFIG["minimum_average_daily_jobs"]
    breadth_ok = (
        metrics["unique_title_count"] >= CONFIG["minimum_unique_titles"]
        and metrics["unique_company_count"] >= CONFIG["minimum_unique_companies"]
        and metrics["unique_location_count"] >= CONFIG["minimum_unique_locations"]
    )
    concentration_ok = not metrics["severe_concentration"]

    if persistence_ok and volume_ok and breadth_ok and concentration_ok:
        verdict = "MAINTAIN" if live else "BUILD"
        reason = (
            "Meets persistence, average-volume and breadth safeguards without "
            "severe advertiser concentration."
        )
        return verdict, reason

    watch_evidence = (
        metrics["average_daily_count"] >= CONFIG["watch_minimum_average_daily_jobs"]
        or metrics["seen_ratio"] >= CONFIG["watch_minimum_seen_ratio"]
        or metrics["highest_daily_count"] >= CONFIG["watch_minimum_peak_jobs"]
    )

    concerns: List[str] = []
    if not persistence_ok:
        concerns.append("insufficient persistence")
    if not volume_ok:
        concerns.append("average below 6 jobs/day")
    if not breadth_ok:
        concerns.append("limited title/company/location breadth")
    if not concentration_ok:
        concerns.append("severe advertiser concentration")
    if metrics["direction_pct"] <= CONFIG["meaningful_decline_pct"]:
        concerns.append(metrics["decline_type"].replace("_", " "))

    if watch_evidence:
        return "WATCH", "; ".join(dict.fromkeys(concerns))
    return "REJECT", "; ".join(dict.fromkeys(concerns)) or "Insufficient sustained supply."


# ---------------------------------------------------------------------------
# Report builders
# ---------------------------------------------------------------------------

def build_reports(expanded: pd.DataFrame, valid_dates: List[str], month: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    report_jobs = add_published_region_rows(expanded)
    first_dates, last_dates = first_last_window(valid_dates)

    summary_rows: List[dict] = []
    daily_rows: List[dict] = []

    grouped = report_jobs.groupby(["report_region", "region_scope", "category"], dropna=False)

    for (region, scope, category), group in grouped:
        daily_counts = {
            date: int(group.loc[group["date"] == date, "job_id"].nunique())
            for date in valid_dates
        }
        counts = list(daily_counts.values())
        if not counts or max(counts) == 0:
            continue

        for date, count in daily_counts.items():
            daily_rows.append({
                "month": month,
                "date": date,
                "region": region,
                "region_scope": scope,
                "category": category,
                "daily_job_count": count,
            })

        concentration = concentration_metrics(group)
        decline = decline_diagnostic(group, first_dates, last_dates)

        days_seen = sum(1 for value in counts if value > 0)
        metrics = {
            "seen_ratio": safe_share(days_seen, len(valid_dates)),
            "average_daily_count": sum(counts) / len(counts),
            "highest_daily_count": max(counts),
            "unique_title_count": group["title_key"].nunique(),
            "unique_company_count": group["company"].nunique(),
            "unique_location_count": group["location"].nunique(),
            "severe_concentration": concentration["severe_concentration"],
            "direction_pct": decline["direction_pct"],
            "decline_type": decline["decline_type"],
        }

        live = is_live_slice(region, category)
        verdict, reason = recommendation(metrics, live)

        summary_rows.append({
            "month": month,
            "region": region,
            "region_scope": scope,
            "category": category,
            "existing_live_page": "yes" if live else "no",
            "recommendation": verdict,
            "recommendation_reason": reason,
            "total_jobs": int(group["job_id"].nunique()),
            "feed_days": len(valid_dates),
            "days_seen": days_seen,
            "seen_ratio_pct": round(metrics["seen_ratio"] * 100, 1),
            "average_daily_count": round(metrics["average_daily_count"], 2),
            "minimum_daily_count": min(counts),
            "maximum_daily_count": max(counts),
            "days_with_6_plus": sum(1 for value in counts if value >= 6),
            "days_with_12_plus": sum(1 for value in counts if value >= 12),
            "first_five_day_average": round(decline["first_avg"], 2),
            "last_five_day_average": round(decline["last_avg"], 2),
            "direction_change_pct": round(decline["direction_pct"], 1),
            "decline_type": decline["decline_type"],
            "decline_explanation": decline["decline_explanation"],
            "unique_title_count": metrics["unique_title_count"],
            "unique_company_count": metrics["unique_company_count"],
            "unique_location_count": metrics["unique_location_count"],
            "top_titles": top_values(group["title"], 10),
            "top_companies": top_values(group["company"], 10),
            "top_1_company_share_pct": concentration["top_1_company_share_pct"],
            "top_2_company_share_pct": concentration["top_2_company_share_pct"],
            "concentration_risk": concentration["concentration_risk"],
        })

    summary = pd.DataFrame(summary_rows)
    daily = pd.DataFrame(daily_rows)

    if not summary.empty:
        recommendation_order = {"BUILD": 0, "MAINTAIN": 1, "WATCH": 2, "REJECT": 3}
        summary["_order"] = summary["recommendation"].map(recommendation_order)
        summary = summary.sort_values(
            ["_order", "category", "average_daily_count", "region"],
            ascending=[True, True, False, True],
        ).drop(columns="_order")

    if not daily.empty:
        daily = daily.sort_values(["category", "region", "date"])

    return summary, daily


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(
    input_dir: Path,
    output_dir: Path,
    month: str,
    geo_lookup_path: Path,
    registers_dir: Optional[Path] = None,
) -> None:
    base_dir = Path.cwd()
    register_paths = discover_registers(base_dir, registers_dir)
    geo_lookup = load_geo_lookup(geo_lookup_path)
    registers = {
        category: load_register(path)
        for category, path in register_paths.items()
    }

    expanded, valid_dates, errors = load_daily_feeds(
        input_dir=input_dir,
        geo_lookup=geo_lookup,
        registers=registers,
    )

    summary, daily = build_reports(expanded, valid_dates, month)

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / f"{month}-module2-category-validation.csv"
    daily_path = output_dir / f"{month}-module2-daily-counts.csv"
    unknown_path = output_dir / f"{month}-module2-unknown-location-detail.csv"
    log_path = output_dir / f"{month}-module2-run-log.txt"

    summary.to_csv(summary_path, index=False, encoding="utf-8-sig")
    daily.to_csv(daily_path, index=False, encoding="utf-8-sig")

    unknown_detail = expanded.loc[
        expanded["lookup_region"].eq("Other / Unknown"),
        [
            "date",
            "job_id",
            "title",
            "company",
            "location",
            "raw_location",
            "category",
            "source_file",
            "unknown_reason",
        ],
    ].copy()
    unknown_detail = unknown_detail.rename(columns={"location": "raw_area"})
    unknown_detail = unknown_detail.sort_values(
        ["category", "date", "raw_area", "title", "job_id"]
    )
    unknown_detail.to_csv(unknown_path, index=False, encoding="utf-8-sig")

    log_lines = [
        f"Month: {month}",
        f"Input directory: {input_dir}",
        f"Valid feed days: {len(valid_dates)}",
        f"First feed day: {valid_dates[0] if valid_dates else ''}",
        f"Last feed day: {valid_dates[-1] if valid_dates else ''}",
        f"Selected register-expanded job rows: {len(expanded)}",
        f"Geo lookup: {geo_lookup_path}",
        f"Geo areas loaded: {len(geo_lookup)}",
        "Classification mode: register-only",
        "Selected classifications: HIGH_CONFIDENCE, ELASTIC_FIT",
        "North East published page: aggregated from three geo_lookup regions",
        "",
        "Registers:",
        *[
            f"- {category}: {path} ({len(registers[category])} titles)"
            for category, path in register_paths.items()
        ],
        "",
        "Recommendation configuration:",
        *[f"- {key}: {value}" for key, value in CONFIG.items()],
        "",
        "Outputs:",
        f"- {summary_path}",
        f"- {daily_path}",
        f"- {unknown_path}",
    ]

    if errors:
        log_lines.extend(["", "Input warnings/errors:", *[f"- {item}" for item in errors]])

    log_path.write_text("\n".join(log_lines), encoding="utf-8")
    print("\n".join(log_lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ontap Compiler Module 2 monthly region × category profiler."
    )
    parser.add_argument("--month", required=True, help="Month in YYYY-MM format.")
    parser.add_argument(
        "--input-dir",
        default=None,
        help="Folder containing daily JobG8 Excel files. Default: pipeline/input-jobg8-archive/<month>",
    )
    parser.add_argument(
        "--output-dir",
        default="pipeline/reports-module2",
        help="Output folder.",
    )
    parser.add_argument(
        "--geo-lookup",
        default="pipeline/geo/geo_lookup.xlsx",
        help="Path to geo_lookup.xlsx.",
    )
    parser.add_argument(
        "--registers-dir",
        default="pipeline/registers",
        help="Optional folder containing the six register CSV files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = (
        Path(args.input_dir)
        if args.input_dir
        else Path("pipeline/input-jobg8-archive") / args.month
    )
    run(
        input_dir=input_dir,
        output_dir=Path(args.output_dir),
        month=args.month,
        geo_lookup_path=Path(args.geo_lookup),
        registers_dir=Path(args.registers_dir) if args.registers_dir else None,
    )


if __name__ == "__main__":
    main()
