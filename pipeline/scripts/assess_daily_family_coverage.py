from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from . import service_admin_pipeline_core as admin
from . import support_worker_pipeline as support
from .pipeline_refinement import resolve_feed_date


CATALOG_PATH = Path("config/job_slice_catalog.json")
OUTPUT_PATH = Path("reports-daily/daily-family-coverage.csv")
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


def _prepare_family_module(module: Any, regions: dict[str, dict[str, str]]) -> None:
    # Diagnostic-only expansion: make the production selector aware of every
    # canonical overview region without changing any publish register or output.
    module.OUTPUT_FILES = {
        region: f"diagnostic-{facts['slug']}.json"
        for region, facts in regions.items()
    }
    module.PUBLISH_THRESHOLDS = {region: 6 for region in regions}
    module.ANCHOR_TOWNS = {
        region: str(facts.get("anchor_town") or region)
        for region, facts in regions.items()
    }

    for region in regions:
        module.REGION_MAP[module.norm_key(region)] = region

    # Support-worker geography has a second detail->publish mapping layer.
    if hasattr(module, "PUBLISH_REGION_BY_DETAIL_REGION"):
        module.PUBLISH_REGION_BY_DETAIL_REGION.update({region: region for region in regions})


def _assess_family(module: Any, family_key: str, regions: dict[str, dict[str, str]]) -> tuple[str, dict[str, int]]:
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

    counts = {region: len(selected.get(region, [])) for region in regions}
    missing = sorted(set(regions) - set(selected))
    if missing:
        raise RuntimeError(
            f"{family_key} selector failed to assess canonical region(s): " + ", ".join(missing)
        )
    return feed_date, counts


def main() -> int:
    regions = _load_regions()
    admin_date, admin_counts = _assess_family(admin, "service_admin", regions)
    support_date, support_counts = _assess_family(support, "support_worker", regions)
    if admin_date != support_date:
        raise RuntimeError(
            f"Family assessment feed-date mismatch: admin={admin_date}, support={support_date}"
        )

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
                "feed_date": admin_date,
                "region": region,
                "family": "service_admin",
                "selected_count": admin_counts[region],
            })
            writer.writerow({
                "feed_date": admin_date,
                "region": region,
                "family": "support_worker",
                "selected_count": support_counts[region],
            })

    print(f"Wrote {OUTPUT_PATH}: 33 regions x 2 families for feed {admin_date}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
