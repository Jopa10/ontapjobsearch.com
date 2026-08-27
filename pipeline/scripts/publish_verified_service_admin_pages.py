#!/usr/bin/env python3
"""Publish only verified LIVE service-admin pages.

This wrapper uses the existing verified-page contract and current mappings but
excludes support-worker mappings, so source-specific admin refreshes cannot
change an unrelated category.
"""
from __future__ import annotations

import argparse

from . import publish_verified_pages_north_yorkshire as latest

core = latest.live.live.core


def service_admin_mappings():
    return tuple(mapping for mapping in core.MAPPINGS if mapping.category == "admin_service")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    mappings = service_admin_mappings()
    if not mappings:
        raise SystemExit("STOP: no service-admin verified-page mappings are configured.")
    active_slices = core.live_slices()
    shared_dates = core.load_shared_posted_dates(core.MAPPINGS)
    results = [
        core.publish_one(
            mapping,
            write=args.write,
            active_slices=active_slices,
            shared_dates=shared_dates,
        )
        for mapping in mappings
    ]
    print(core.format_report(results), end="")
    return 1 if any(row["status"] == "failed" for row in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
