from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path = [entry for entry in sys.path if Path(entry or ".").resolve() != SCRIPT_DIR]

import pandas as pd

TITLE_COL = "/Job/Position"
AREA_COL = "/Job/Area"
LOCATION_COL = "/Job/Location"
AREA_UNUSABLE_VALUES = {"", "not specified", "unknown"}


def norm(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip()).casefold()


def text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def latest_feed(input_dir: Path) -> Path:
    files = sorted(
        p for p in input_dir.iterdir()
        if p.suffix.lower() in {".xlsx", ".xls", ".xlsm"}
        and not p.name.startswith("~$")
    )
    if not files:
        raise SystemExit(f"No Excel feeds found in {input_dir}")
    dated = [(p, re.search(r"(20\d{2}-\d{2}-\d{2})", p.stem)) for p in files]
    dated = [(p, m.group(1)) for p, m in dated if m]
    return max(dated, key=lambda item: item[1])[0] if dated else files[-1]


def load_operational_regions(catalog_path: Path) -> list[str]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    regions = [str(name) for name in catalog.get("regions", {}).keys()]
    regions = [name for name in regions if name != "Northern Ireland - East"]
    if len(regions) != 33:
        raise SystemExit(
            f"Expected the operational England footprint to contain exactly 33 regions; found {len(regions)}"
        )
    return regions


def load_geo_lookups(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    area_df = pd.read_excel(path, dtype=str).fillna("")
    required = {"Area", "Cluster"}
    if not required.issubset(area_df.columns):
        raise SystemExit(f"Geo lookup missing columns: {sorted(required - set(area_df.columns))}")
    area_lookup = {
        norm(row["Area"]): text(row["Cluster"])
        for _, row in area_df.iterrows()
        if norm(row["Area"]) and text(row["Cluster"])
    }

    fallback_df = pd.read_excel(path, sheet_name="LocationFallback", dtype=str).fillna("")
    fallback_required = {"Status", "Location", "Cluster"}
    if not fallback_required.issubset(fallback_df.columns):
        raise SystemExit(
            f"LocationFallback missing columns: {sorted(fallback_required - set(fallback_df.columns))}"
        )
    fallback = {
        norm(row["Location"]): text(row["Cluster"])
        for _, row in fallback_df.iterrows()
        if norm(row["Status"]) == "auto" and norm(row["Location"]) and text(row["Cluster"])
    }
    return area_lookup, fallback


def raw_cluster(row: pd.Series, area_lookup: dict[str, str], fallback: dict[str, str]) -> str:
    area = norm(row.get(AREA_COL, ""))
    location = norm(row.get(LOCATION_COL, ""))
    if area in AREA_UNUSABLE_VALUES:
        return fallback.get(location, "Other / Unknown")
    return area_lookup.get(area, "Other / Unknown")


def operational_region(cluster: str, operational: set[str]) -> tuple[str, str]:
    if cluster == "Other / Unknown":
        return "", "geo_unknown"
    if cluster.startswith("North East - "):
        return "North East", "in_33_region_footprint"
    if cluster in operational:
        return cluster, "in_33_region_footprint"
    return "", "outside_33_region_footprint"


def load_title_families(reconciliation_csv: Path) -> tuple[dict[str, str], dict[str, str], Counter[str]]:
    df = pd.read_csv(reconciliation_csv, dtype=str, encoding="utf-8-sig").fillna("")
    required = {"title", "refined_broad_family", "reconciliation_basis", "count_in_latest_feed"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Reconciliation CSV missing columns: {sorted(missing)}")

    title_family: dict[str, str] = {}
    title_basis: dict[str, str] = {}
    family_totals: Counter[str] = Counter()
    for _, row in df.iterrows():
        key = norm(row["title"])
        if not key:
            continue
        family = text(row["refined_broad_family"])
        basis = text(row["reconciliation_basis"])
        title_family[key] = family
        title_basis[key] = basis
        try:
            n = int(float(str(row["count_in_latest_feed"])))
        except ValueError:
            n = 0
        family_totals[family] += n
    return title_family, title_basis, family_totals


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--reconciliation-csv", required=True, type=Path)
    ap.add_argument("--geo-lookup", required=True, type=Path)
    ap.add_argument("--slice-catalog", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()

    operational_regions = load_operational_regions(args.slice_catalog)
    operational_set = set(operational_regions)
    area_lookup, fallback = load_geo_lookups(args.geo_lookup)
    title_family, title_basis, family_totals = load_title_families(args.reconciliation_csv)

    feed = latest_feed(args.input_dir)
    raw = pd.read_excel(feed, dtype=str).fillna("")
    required_feed_cols = {TITLE_COL, AREA_COL, LOCATION_COL}
    missing_feed = required_feed_cols - set(raw.columns)
    if missing_feed:
        raise SystemExit(f"Feed missing columns: {sorted(missing_feed)}")

    region_counts: defaultdict[str, Counter[str]] = defaultdict(Counter)
    footprint_counts: Counter[str] = Counter()
    outside_counts: Counter[str] = Counter()
    unknown_counts: Counter[str] = Counter()
    existing_register_in_footprint: Counter[str] = Counter()

    for _, row in raw.iterrows():
        key = norm(row.get(TITLE_COL, ""))
        family = title_family.get(key)
        if not family:
            continue
        cluster = raw_cluster(row, area_lookup, fallback)
        region, status = operational_region(cluster, operational_set)
        if status == "in_33_region_footprint":
            region_counts[family][region] += 1
            footprint_counts[family] += 1
            if title_basis.get(key, "").startswith("existing_register:"):
                existing_register_in_footprint[family] += 1
        elif status == "outside_33_region_footprint":
            outside_counts[family] += 1
        else:
            unknown_counts[family] += 1

    if sum(family_totals.values()) != len(raw):
        raise SystemExit(
            f"Family totals do not reconcile to raw feed: {sum(family_totals.values())} != {len(raw)}"
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "jobg8-operational-33-region-density-current.csv"
    md_path = args.output_dir / "jobg8-operational-33-region-density-current.md"

    rows: list[dict[str, object]] = []
    for family, total in family_totals.most_common():
        if family == "Other / Unclassified":
            continue
        counts = region_counts[family]
        values = [counts.get(region, 0) for region in operational_regions]
        populated = sum(1 for n in values if n > 0)
        top = "; ".join(f"{region} ({n})" for region, n in counts.most_common(5))
        footprint = footprint_counts[family]
        existing = existing_register_in_footprint[family]
        rows.append(
            {
                "broad_family": family,
                "total_feed_jobs": total,
                "jobs_in_33_region_footprint": footprint,
                "existing_register_jobs_in_33": existing,
                "new_uncovered_jobs_in_33": footprint - existing,
                "populated_regions_out_of_33": populated,
                "median_jobs_across_all_33": statistics.median(values),
                "regions_with_5_plus": sum(1 for n in values if n >= 5),
                "regions_with_10_plus": sum(1 for n in values if n >= 10),
                "outside_33_region_footprint": outside_counts[family],
                "geo_unknown": unknown_counts[family],
                "top_regions": top,
            }
        )

    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)

    lines = [
        "# JobG8 operational 33-region density",
        "",
        f"Feed: `{feed.name}`",
        "Operational footprint: **33 England regions** from `pipeline/config/job_slice_catalog.json`, with `Northern Ireland - East` explicitly excluded to match the daily regional overview.",
        "North East geo sub-clusters are collapsed to the single operational `North East` region.",
        "Median is calculated across **all 33 operational regions, including zeroes**.",
        "",
        "| Broad family | Total feed | In 33 regions | Existing register in 33 | New / uncovered in 33 | Populated /33 | Median /33 | Regions 5+ | Regions 10+ | Outside 33 | Geo unknown | Top operational regions |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {broad_family} | {total_feed_jobs:,} | {jobs_in_33_region_footprint:,} | "
            "{existing_register_jobs_in_33:,} | {new_uncovered_jobs_in_33:,} | "
            "{populated_regions_out_of_33} | {median_jobs_across_all_33:g} | "
            "{regions_with_5_plus} | {regions_with_10_plus} | "
            "{outside_33_region_footprint:,} | {geo_unknown:,} | {top_regions} |".format(**row)
        )

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
