"""Publish every LIVE slice through the established verified-page guard.

Existing static pages keep their established destinations. New configured slices
are written beneath app/_city-pages/configured-slices so the existing city-data
commit stage carries them without widening the publisher workflow allowlist.
"""
from __future__ import annotations

from pathlib import Path

from . import publish_verified_pages_coventry as established
from .slice_catalog import display_title, dynamic_data_path, output_source_path
from .slice_registry import live_slices

# Coventry -> Sussex -> base verified publisher.
core = established.live.core

NORTH_YORKSHIRE_MAPPING = core.Mapping(
    "North Yorkshire service administrator jobs",
    "Yorkshire - North",
    "admin_service",
    Path("pipeline/output-admin-service/north-yorkshire-admin-service.json"),
    Path("app/north-yorkshire/service-administrator-jobs.json"),
)


def _add_mapping(mapping: core.Mapping) -> None:
    if any(
        existing.region == mapping.region and existing.category == mapping.category
        for existing in core.MAPPINGS
    ):
        return
    core.MAPPINGS += (mapping,)


def configure_mappings() -> None:
    _add_mapping(NORTH_YORKSHIRE_MAPPING)
    existing_pairs = {(mapping.region, mapping.category) for mapping in core.MAPPINGS}

    for region, category in sorted(live_slices()):
        pair = (region, category)
        if pair in existing_pairs:
            continue

        destination = dynamic_data_path(region, category)
        destination_path = core.REPO_ROOT / destination
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        if not destination_path.exists():
            # The established publisher validates that a destination already
            # exists before an atomic replacement. An empty seed is invisible to
            # the site because dynamic routes require a non-empty data array.
            destination_path.write_text("[]\n", encoding="utf-8")

        _add_mapping(
            core.Mapping(
                display_title(region, category),
                region,
                category,
                output_source_path(region, category),
                destination,
            )
        )
        existing_pairs.add(pair)


configure_mappings()


def main() -> int:
    return established.main()


if __name__ == "__main__":
    raise SystemExit(main())
