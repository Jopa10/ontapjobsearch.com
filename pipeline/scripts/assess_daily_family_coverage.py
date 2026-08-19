from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from . import service_admin_pipeline_core as admin
from . import support_worker_pipeline as support
from .pipeline_refinement import resolve_feed_date


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

    # The family process() functions resolve lookup Cluster values through
    # REGION_MAP. Keep all existing special mappings, then add the canonical
    # 33-region names as identity mappings for the diagnostic pass.
    for region in regions:
        module.REGION_MAP[module.norm_key(region)] = region

    # Support-worker geography has a second detail->publish mapping layer.
    if hasattr(module, "PUBLISH_REGION_BY_DETAIL_REGION"):
        module.PUBLISH_REGION_BY_DETAIL_REGION.update({region: region for region in regions})


def _assess_family(
    module: Any,
    family_key: str,
    regions: dict[str, dict[str, str]],
) -> tuple[str, dict[str, int]]:
    """Run the existing production family selector across all canonical regions."""
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

    manual = module.load_manual_decisions(feed_date)
    title_register = module.load_title_register()
    outputs, report_rows = module.process(
        job_df,
        lookup,
        fallback,
        manual.overrides,
        manual.selections,
        title_register,
    )
    selected, _status = module.anchor_sort_and_select(
        outputs,
        report_rows,
        manual_rerun_mode=manual.rerun_mode,
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


def _apply_to_overview(
    feed_date: str,
    admin_counts: dict[str, int],
    support_counts: dict[str, int],
) -> None:
    """Replace NOT LIVE Admin/Support cells with same-day production-rule counts."""
    if not OVERVIEW_PATH.is_file():
        raise RuntimeError(f"Daily overview must be built before assessment: {OVERVIEW_PATH}")

    statuses = _load_statuses()
    lines = OVERVIEW_PATH.read_text(encoding="utf-8").splitlines()
    in_not_live = False
    seen_regions: set[str] = set()
    patched: list[str] = []

    for line in lines:
        if line.startswith("> LIVE counts reconcile"):
            patched.append(
                line.split(". NOT LIVE", 1)[0]
                + f". NOT LIVE Service Admin and Support Worker are assessed from the current JobG8 feed ({feed_date}) across all 33 canonical regions using the production family selectors and canonical geo. Sales Advisor remains test-only; `—` there means not assessed / no current source."
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


def main() -> int:
    regions = _load_regions()
    admin_date, admin_counts = _assess_family(admin, "service_admin", regions)
    support_date, support_counts = _assess_family(support, "support_worker", regions)
    if admin_date != support_date:
        raise RuntimeError(
            f"Family assessment feed-date mismatch: admin={admin_date}, support={support_date}"
        )

    _write_coverage_csv(admin_date, regions, admin_counts, support_counts)
    _apply_to_overview(admin_date, admin_counts, support_counts)

    print(f"Wrote {OUTPUT_PATH}: 33 regions x 2 families for feed {admin_date}")
    print(f"Updated {OVERVIEW_PATH} NOT LIVE Admin/Support counts from same-day assessment")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
