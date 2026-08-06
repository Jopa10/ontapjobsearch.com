"""Publish verified pages with North Yorkshire included."""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from . import publish_verified_pages_coventry as live

NORTH_YORKSHIRE_MAPPING = live.live.core.Mapping(
    "North Yorkshire service administrator jobs",
    "Yorkshire - North",
    "admin_service",
    Path("pipeline/output-admin-service/north-yorkshire-admin-service.json"),
    Path("app/north-yorkshire/service-administrator-jobs.json"),
)

if not any(
    mapping.region == NORTH_YORKSHIRE_MAPPING.region
    and mapping.category == NORTH_YORKSHIRE_MAPPING.category
    for mapping in live.live.core.MAPPINGS
):
    live.live.core.MAPPINGS += (NORTH_YORKSHIRE_MAPPING,)


def main() -> int:
    return live.main()


if __name__ == "__main__":
    raise SystemExit(main())
