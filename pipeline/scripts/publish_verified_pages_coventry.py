"""Publish verified pages with Coventry & Warwickshire included."""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from . import publish_verified_pages_sussex as live

COVENTRY_WARWICKSHIRE_MAPPING = live.core.Mapping(
    "Coventry & Warwickshire service administrator jobs",
    "West Midlands - Coventry & Warwickshire",
    "admin_service",
    Path("pipeline/output-admin-service/coventry-warwickshire-admin-service.json"),
    Path("app/coventry-warwickshire/service-administrator-jobs.json"),
)

if not any(
    mapping.region == COVENTRY_WARWICKSHIRE_MAPPING.region
    and mapping.category == COVENTRY_WARWICKSHIRE_MAPPING.category
    for mapping in live.core.MAPPINGS
):
    live.core.MAPPINGS += (COVENTRY_WARWICKSHIRE_MAPPING,)


def main() -> int:
    return live.main()


if __name__ == "__main__":
    raise SystemExit(main())
