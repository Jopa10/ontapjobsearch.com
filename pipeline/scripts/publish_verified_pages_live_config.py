"""Publish every LIVE slice, generating verified data files for config-driven pages."""
from __future__ import annotations

from . import publish_verified_pages_north_yorkshire as established
from .slice_catalog import display_title, dynamic_data_path, output_source_path
from .slice_registry import live_slices

# North-Yorkshire -> Coventry -> Sussex -> base publisher.
core = established.live.live.core


def configure_mappings() -> None:
    existing_pairs = {(mapping.region, mapping.category) for mapping in core.MAPPINGS}
    additions = []
    for region, category in sorted(live_slices()):
        pair = (region, category)
        if pair in existing_pairs:
            continue
        destination = dynamic_data_path(region, category)
        destination_path = core.REPO_ROOT / destination
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        if not destination_path.exists():
            # The established publisher intentionally requires an existing
            # destination. Seed a harmless empty array; a non-empty validated
            # source replaces it atomically, while an empty source remains hidden
            # from the dynamic site registry.
            destination_path.write_text("[]\n", encoding="utf-8")
        additions.append(
            core.Mapping(
                display_title(region, category),
                region,
                category,
                output_source_path(region, category),
                destination,
            )
        )
    if additions:
        core.MAPPINGS += tuple(additions)


configure_mappings()


def main() -> int:
    return established.main()


if __name__ == "__main__":
    raise SystemExit(main())
