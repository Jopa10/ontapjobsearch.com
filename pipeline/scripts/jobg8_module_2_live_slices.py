"""Compiler Module 2 entry point using live slices and shared JobG8 geography."""
from __future__ import annotations

from . import jobg8_module_2_geo_adapter
from . import jobg8_module_2_monthly_category_profiler as compiler
from .slice_registry import live_slices

NE_LOOKUP_REGIONS = [
    "North East - Tyneside, Wearside & Northumberland",
    "North East - County Durham & Darlington/Hartlepool",
    "North East - Tees Valley",
]


def configure_live_slice_groups() -> None:
    groups: dict[str, dict[str, object]] = {}
    for region, category in sorted(live_slices()):
        group = groups.setdefault(
            region,
            {
                "published_region": region,
                "lookup_regions": NE_LOOKUP_REGIONS if region == "North East" else [region],
                "categories": set(),
            },
        )
        categories = group["categories"]
        assert isinstance(categories, set)
        categories.add(category)

    compiler.LIVE_SLICE_GROUPS.clear()
    compiler.LIVE_SLICE_GROUPS.update(groups)


jobg8_module_2_geo_adapter.install(compiler)
configure_live_slice_groups()


def main() -> int:
    return compiler.main()


if __name__ == "__main__":
    raise SystemExit(main())
