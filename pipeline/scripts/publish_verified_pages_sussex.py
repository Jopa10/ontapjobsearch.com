"""Publish verified pages with the live Sussex service-admin slice included."""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from . import publish_verified_pages as core

SUSSEX_ADMIN_MAPPING = core.Mapping(
    "Sussex service administrator jobs",
    "Sussex",
    "admin_service",
    Path("pipeline/output-admin-service/sussex-admin-service.json"),
    Path("app/sussex/service-administrator-jobs.json"),
)

if not any(
    mapping.region == SUSSEX_ADMIN_MAPPING.region
    and mapping.category == SUSSEX_ADMIN_MAPPING.category
    for mapping in core.MAPPINGS
):
    core.MAPPINGS += (SUSSEX_ADMIN_MAPPING,)


def main() -> int:
    return core.main()


if __name__ == "__main__":
    raise SystemExit(main())
