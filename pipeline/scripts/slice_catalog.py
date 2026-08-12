from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOG_PATH = REPO_ROOT / "pipeline" / "config" / "job_slice_catalog.json"


@lru_cache(maxsize=1)
def load_catalog(path: Path = DEFAULT_CATALOG_PATH) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"STOP: job slice catalog not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"STOP: could not read job slice catalog: {exc}") from exc

    categories = data.get("categories")
    regions = data.get("regions")
    if not isinstance(categories, dict) or not categories:
        raise SystemExit("STOP: job slice catalog must contain a non-empty categories object")
    if not isinstance(regions, dict) or not regions:
        raise SystemExit("STOP: job slice catalog must contain a non-empty regions object")

    for category, meta in categories.items():
        if not isinstance(meta, dict):
            raise SystemExit(f"STOP: invalid category metadata for {category!r}")
        required = {"route_slug", "output_dir", "file_suffix", "display_label", "category_label"}
        missing = required - set(meta)
        if missing:
            raise SystemExit(
                f"STOP: category {category!r} missing catalog fields: {', '.join(sorted(missing))}"
            )

    seen_slugs: set[str] = set()
    for region, meta in regions.items():
        if not isinstance(meta, dict):
            raise SystemExit(f"STOP: invalid region metadata for {region!r}")
        slug = str(meta.get("slug") or "").strip()
        anchor = str(meta.get("anchor_town") or "").strip()
        if not slug or not anchor:
            raise SystemExit(f"STOP: region {region!r} requires slug and anchor_town")
        if slug in seen_slugs:
            raise SystemExit(f"STOP: duplicate region slug in job slice catalog: {slug!r}")
        seen_slugs.add(slug)

    return data


def category_names() -> set[str]:
    return set(load_catalog()["categories"])


def region_names() -> set[str]:
    return set(load_catalog()["regions"])


def category_meta(category: str) -> dict[str, str]:
    meta = load_catalog()["categories"].get(category)
    if not isinstance(meta, dict):
        raise SystemExit(f"STOP: category missing from job slice catalog: {category!r}")
    return {key: str(value) for key, value in meta.items()}


def region_meta(region: str) -> dict[str, str]:
    meta = load_catalog()["regions"].get(region)
    if not isinstance(meta, dict):
        raise SystemExit(f"STOP: region missing from job slice catalog: {region!r}")
    return {key: str(value) for key, value in meta.items()}


def region_slug(region: str) -> str:
    return region_meta(region)["slug"]


def anchor_town(region: str) -> str:
    return region_meta(region)["anchor_town"]


def route_slug(category: str) -> str:
    return category_meta(category)["route_slug"]


def output_filename(region: str, category: str) -> str:
    return f"{region_slug(region)}-{category_meta(category)['file_suffix']}.json"


def output_source_path(region: str, category: str) -> Path:
    meta = category_meta(category)
    return Path("pipeline") / meta["output_dir"] / output_filename(region, category)


def dynamic_data_path(region: str, category: str) -> Path:
    return (
        Path("app")
        / "_city-pages"
        / "configured-slices"
        / region_slug(region)
        / f"{route_slug(category)}.json"
    )


def dynamic_route(region: str, category: str) -> str:
    return f"/job-search/{region_slug(region)}/{route_slug(category)}"


def display_title(region: str, category: str) -> str:
    return f"{region} {category_meta(category)['display_label']} Jobs"
