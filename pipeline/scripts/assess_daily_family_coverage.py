from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from . import persistent_jobg8_review as persistence
from . import service_admin_pipeline_live_config as admin_config
from . import support_worker_pipeline_live_config as support_config
from .pipeline_refinement import resolve_feed_date


# Import through the config-driven production wrappers, not the bare family
# modules. This preserves the same established wrapper mutations used by the
# live daily pipelines before we expand them in-memory to all 33 regions.
admin = admin_config.core
support = support_config.core

CATALOG_PATH = Path("config/job_slice_catalog.json")
REGISTER_PATH = Path("registers/region_category_slice_register.csv")
OUTPUT_PATH = Path("reports-daily/daily-family-coverage.csv")
OVERVIEW_PATH = Path("reports-daily/daily-region-overview.md")
EXCLUDED_REGIONS = {"Northern Ireland - East"}


def _load_regions() -> dict[str, dict[str, str]]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8-sig"))
    regions = {
        name: facts
        for name, facts in catalog.get("regions", {}).items()
        if name not in EXCLUDED_REGIONS
    }
    if len(regions) != 33:
        raise RuntimeError(f"Expected 33 daily overview regions, found {len(regions)}")
    return regions


def _load_statuses() -> dict[tuple[str, str], str]:
    statuses: dict[tuple[str, str], str] = {}
    with REGISTER_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["region", "category", "status"]:
            raise RuntimeError(f"Unexpected slice register header: {reader.fieldnames}")
        for row in reader:
            region = (row.get("region") or "").strip()
            category = (row.get("category") or "").strip()
            status = (row.get("status") or "").strip().upper()
            if region and category:
                statuses[(region, category)] = status
    return statuses


def _prepare_family_module(module: Any, regions: dict[str, dict[str, str]]) -> None:
    """Expand one production selector in-memory for diagnostic coverage only."""
    module.OUTPUT_FILES = {
        region: f"diagnostic-{facts['slug']}.json"
        for region, facts in regions.items()
    }
    module.PUBLISH_THRESHOLDS = {region: 6 for region in regions}
    module.ANCHOR_TOWNS = {
        region: str(facts.get("anchor_town") or region)
        for region, facts in regions.items()
    }

    # Keep every special mapping installed by the production wrappers, then add
    # canonical 33-region identity mappings for regions that are normally NOT LIVE.
    for region in regions:
        module.REGION_MAP[module.norm_key(region)] = region

    # Support-worker geography has a second detail->publish mapping layer.
    if hasattr(module, "PUBLISH_REGION_BY_DETAIL_REGION"):
        module.PUBLISH_REGION_BY_DETAIL_REGION.update({region: region for region in regions})


def _persistent_actions(category: str) -> tuple[dict[str, str], set[str]]:
    """Read the same durable human decisions used by production, without mutating reviews."""
    decisions = persistence._load_category_store(category)
    overrides: dict[str, str] = {}
    selections: set[str] = set()
    for job_id, record in decisions.items():
        action = str(record.get("action") or "").strip().lower()
        if action == "exclude":
            overrides[job_id] = "FORCE_EXCLUDE"
        elif action == "select":
            selections.add(job_id)
    return overrides, selections


def _assess_family(
    module: Any,
    family_key: str,
    persistence_category: str,
    regions: dict[str, dict[str, str]],
) -> tuple[str, dict[str, int]]:
    """Run the production family selector against the already-materialized current feed."""
    _prepare_family_module(module, regions)

    job_file = module.find_input_file(module.JOB_FILE_KEYWORDS)
    lookup_file = module.find_lookup_file(job_file)
    feed_date = resolve_feed_date(job_file)

    job_df = module.read_table(job_file)
    module.validate_job_columns(job_df)
    lookup_df = module.read_xlsx_sheet(lookup_file)
    fallback_df = module.read_xlsx_sheet(lookup_file, sheet_name="LocationFallback")
    lookup = module.build_lookup(lookup_df)
    fallback = module.build_location_fallback_lookup(fallback_df)

    overrides, selections = _persistent_actions(persistence_category)
    title_register = module.load_title_register()
    outputs, report_rows = module.process(
        job_df,
        lookup,
        fallback,
        overrides,
        selections,
        title_register,
    )
    selected, _status = module.anchor_sort_and_select(
        outputs,
        report_rows,
        manual_rerun_mode=bool(overrides or selections),
        previously_selected_ids=set(),
    )

    missing = sorted(set(regions) - set(selected))
    if missing:
        raise RuntimeError(
            f"{family_key} selector failed to assess canonical region(s): " + ", ".join(missing)
        )
    return feed_date, {region: len(selected[region]) for region in regions}


def _write_coverage_csv(
    feed_date: str,
    regions: dict[str, dict[str, str]],
    admin_counts: dict[str, int],
    support_counts: dict[str, int],
) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["feed_date", "region", "family", "selected_count"],
            lineterminator="\n",
        )
        writer.writeheader()
        for region in sorted(regions, key=str.casefold):
            writer.writerow({
                "feed_date": feed_date,
                "region": region,
                "family": "service_admin",
                "selected_count": admin_counts[region],
            })
            writer.writerow({
                "feed_date": feed_date,
                "region": region,
                "family": "support_worker",
                "selected_count": support_counts[region],
            })


def _load_coverage_csv() -> tuple[str, dict[str, int], dict[str, int]]:
    if not OUTPUT_PATH.is_file():
        raise RuntimeError(f"Missing daily family coverage: {OUTPUT_PATH}")
    dates: set[str] = set()
    counts: dict[str, dict[str, int]] = {"service_admin": {}, "support_worker": {}}
    with OUTPUT_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"feed_date", "region", "family", "selected_count"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise RuntimeError(f"Unexpected daily family coverage header: {reader.fieldnames}")
        for row in reader:
            feed_date = (row.get("feed_date") or "").strip()
            region = (row.get("region") or "").strip()
            family = (row.get("family") or "").strip()
            if feed_date:
                dates.add(feed_date)
            if family not in counts or not region:
                continue
            counts[family][region] = int((row.get("selected_count") or "0").strip())
    if len(dates) != 1:
        raise RuntimeError(f"Daily family coverage must contain one feed date, found {sorted(dates)}")
    regions = _load_regions()
    for family, family_counts in counts.items():
        missing = sorted(set(regions) - set(family_counts))
        if missing:
            raise RuntimeError(f"Coverage missing {family} region(s): " + ", ".join(missing))
    return next(iter(dates)), counts["service_admin"], counts["support_worker"]


def _apply_to_overview(
    feed_date: str,
    admin_counts: dict[str, int],
    support_counts: dict[str, int],
) -> None:
    """Replace NOT LIVE Admin/Support cells with the same-feed diagnostic counts."""
    if not OVERVIEW_PATH.is_file():
        raise RuntimeError(f"Daily overview must be built before coverage is applied: {OVERVIEW_PATH}")

    statuses = _load_statuses()
    lines = OVERVIEW_PATH.read_text(encoding="utf-8").splitlines()
    in_not_live = False
    seen_regions: set[str] = set()
    patched: list[str] = []

    for line in lines:
        if line.startswith("> LIVE Service Admin") or line.startswith("> LIVE counts reconcile"):
            live_prefix = line.split(". NOT LIVE", 1)[0]
            patched.append(
                live_prefix
                + f". NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed ({feed_date}) used by the production family run, across all 33 canonical regions with the config-driven production wrappers, persistent review decisions and canonical geo. Sales Advisor is now a LIVE registered family where the slice register says LIVE; its LIVE counts come from the current published Customer Sales configured-slice JSON. NOT LIVE Sales Advisor remains `—` until a governed 33-region daily assessment is wired into this overview."
            )
            continue

        if line == "## NOT LIVE":
            in_not_live = True
            patched.append(line)
            continue
        if line == "## HEADLINE":
            in_not_live = False
            patched.append(line)
            continue

        if in_not_live and line.startswith("| ") and not line.startswith("| Region ") and not line.startswith("|---"):
            cells = [cell.strip() for cell in line.split("|")]
            if len(cells) >= 6:
                region = cells[1]
                if region in admin_counts and region in support_counts:
                    cells[2] = "" if statuses.get((region, "admin_service"), "") == "LIVE" else str(admin_counts[region])
                    cells[3] = "" if statuses.get((region, "support_worker"), "") == "LIVE" else str(support_counts[region])
                    line = "| " + " | ".join(cells[1:-1]) + " |"
                    seen_regions.add(region)
        patched.append(line)

    missing = sorted(set(admin_counts) - seen_regions)
    if missing:
        raise RuntimeError("Overview NOT LIVE table missing canonical region(s): " + ", ".join(missing))

    OVERVIEW_PATH.write_text("\n".join(patched) + "\n", encoding="utf-8")


def build_coverage() -> tuple[str, dict[str, int], dict[str, int]]:
    regions = _load_regions()
    admin_date, admin_counts = _assess_family(
        admin, "service_admin", "service_admin", regions
    )
    support_date, support_counts = _assess_family(
        support, "support_worker", "support_worker", regions
    )
    if admin_date != support_date:
        raise RuntimeError(
            f"Family assessment feed-date mismatch: admin={admin_date}, support={support_date}"
        )
    _write_coverage_csv(admin_date, regions, admin_counts, support_counts)
    return admin_date, admin_counts, support_counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply-existing",
        action="store_true",
        help="Apply the already-generated daily-family-coverage.csv to the overview without re-reading JobG8.",
    )
    args = parser.parse_args()

    if args.apply_existing:
        feed_date, admin_counts, support_counts = _load_coverage_csv()
        _apply_to_overview(feed_date, admin_counts, support_counts)
        print(f"Applied {OUTPUT_PATH} to {OVERVIEW_PATH}")
        return 0

    feed_date, _admin_counts, _support_counts = build_coverage()
    print(f"Wrote {OUTPUT_PATH}: 33 regions x 2 families for feed {feed_date}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
