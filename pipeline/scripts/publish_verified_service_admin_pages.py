#!/usr/bin/env python3
"""Publish only verified LIVE service-admin pages.

This wrapper uses the existing verified-page contract and current mappings but
excludes support-worker mappings, so source-specific admin refreshes cannot
change an unrelated category.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import publish_verified_pages_north_yorkshire as latest

core = latest.live.live.core
ISOLATION_REPORT_CONTRACT = "teaching-vacancies-publish-verification-v1"
MAX_ISOLATED_REGIONS = 3


def service_admin_mappings():
    return tuple(mapping for mapping in core.MAPPINGS if mapping.category == "admin_service")


def isolated_regions_from_report(path: Path | None) -> set[str]:
    if path is None:
        return set()
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid regional isolation report {path}: {exc}") from exc
    if not isinstance(report, dict):
        raise ValueError("regional isolation report must be a JSON object")
    if report.get("contract_version") != ISOLATION_REPORT_CONTRACT:
        raise ValueError("regional isolation report has an unexpected contract version")
    values = report.get("isolated_regions")
    if not isinstance(values, list) or any(
        not isinstance(value, str) or not value.strip() for value in values
    ):
        raise ValueError("regional isolation report has invalid isolated regions")
    regions = {value.strip() for value in values}
    if len(regions) != len(values):
        raise ValueError("regional isolation report contains duplicate regions")
    maximum = report.get("max_isolated_regions")
    if maximum != MAX_ISOLATED_REGIONS:
        raise ValueError("regional isolation report has an unexpected threshold")
    if len(regions) > MAX_ISOLATED_REGIONS:
        raise ValueError("regional isolation report exceeds its permitted threshold")
    return regions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument(
        "--isolation-report",
        type=Path,
        help="Verified TV regional report whose named pages must retain live state.",
    )
    args = parser.parse_args()

    mappings = service_admin_mappings()
    if not mappings:
        raise SystemExit("STOP: no service-admin verified-page mappings are configured.")
    active_slices = core.live_slices()
    shared_dates = core.load_shared_posted_dates(core.MAPPINGS)
    try:
        isolated_regions = isolated_regions_from_report(args.isolation_report)
    except ValueError as exc:
        raise SystemExit(f"STOP: {exc}") from exc
    unknown_isolations = isolated_regions - {mapping.region for mapping in mappings}
    if unknown_isolations:
        raise SystemExit(
            "STOP: regional isolation report names unmapped service-admin regions: "
            + ", ".join(sorted(unknown_isolations, key=str.casefold))
        )
    results = []
    for mapping in mappings:
        if mapping.region in isolated_regions:
            results.append(
                {
                    "page_label": mapping.label,
                    "source": str(mapping.source),
                    "destination": str(mapping.destination),
                    "selected_count": 0,
                    "status": "skipped",
                    "reason": (
                        "Teaching Vacancies regional input isolated; previous live "
                        "destination retained"
                    ),
                }
            )
            continue
        results.append(
            core.publish_one(
                mapping,
                write=args.write,
                active_slices=active_slices,
                shared_dates=shared_dates,
            )
        )
    print(core.format_report(results), end="")
    return 1 if any(row["status"] == "failed" for row in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
