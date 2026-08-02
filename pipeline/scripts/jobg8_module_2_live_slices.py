"""Compiler Module 2 entry point with the current Ontap live-slice register reflected."""
from __future__ import annotations

from . import jobg8_module_2_monthly_category_profiler as compiler

compiler.LIVE_SLICE_GROUPS.update(
    {
        "London": {
            "published_region": "London",
            "lookup_regions": ["London"],
            "categories": {"admin_service"},
        },
        "Hampshire": {
            "published_region": "Hampshire",
            "lookup_regions": ["Hampshire"],
            "categories": {"admin_service", "support_worker"},
        },
        "Surrey": {
            "published_region": "Surrey",
            "lookup_regions": ["Surrey"],
            "categories": {"admin_service"},
        },
        "Kent": {
            "published_region": "Kent",
            "lookup_regions": ["Kent"],
            "categories": {"admin_service"},
        },
        "Sussex": {
            "published_region": "Sussex",
            "lookup_regions": ["Sussex"],
            "categories": {"admin_service", "support_worker"},
        },
        "Cumbria - South": {
            "published_region": "Cumbria - South",
            "lookup_regions": ["Cumbria - South"],
            "categories": {"support_worker"},
        },
    }
)


def main() -> int:
    return compiler.main()


if __name__ == "__main__":
    raise SystemExit(main())
