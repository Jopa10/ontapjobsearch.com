"""
Compatibility entry point for the admin/service pipeline with geography safeguards.

The established selector remains in ``service_admin_pipeline_core.py``. This
module owns the geography corrections used by the live selector:

- ``/Job/PostalCode`` is consulted first when its postcode district has a
  curated region mapping;
- a precise ``/Job/Location`` can override a broader ``/Job/Area``;
- ``/Job/Area`` remains the normal fallback when it is specific and valid;
- an explicit postcode near the start of the advert remains a last-resort
  correction through the same curated postcode register;
- the generic JobG8 ``/Job/Area`` value ``City`` is treated as unusable;
- rows resolved to London are removed when strong Northern Ireland location
  evidence contradicts that mapping.

Only LIVE regions are still published. A job resolved to a non-live region is
reported there and excluded from the wrong live output rather than being
silently absorbed by a neighbouring live slice.
"""
from __future__ import annotations

import re
import sys
import types
from pathlib import Path
from typing import Any

try:
    from . import jobg8_geo_resolver as _geo
    from . import service_admin_pipeline_core as _core
except ImportError:  # direct script/test loading
    import jobg8_geo_resolver as _geo
    import service_admin_pipeline_core as _core


_ORIGINAL_AREA_IS_UNUSABLE = _core.area_is_unusable
_ORIGINAL_PROCESS = _core.process

AMBIGUOUS_AREA_KEYS = {"city"}
POSTCODE_LOCATION_OVERRIDES_PATH = _geo.DEFAULT_POSTCODE_OVERRIDES_PATH
POSTCODE_DESCRIPTION_WINDOW = _geo.DESCRIPTION_POSTCODE_WINDOW
POSTAL_CODE_COLUMN = _geo.POSTAL_CODE_COLUMN

_NORTHERN_IRELAND_HEADLINE_RE = re.compile(
    r"\b(?:belfast|londonderry|derriaghy|northern ireland|l['’]?derry|derry)\b",
    re.IGNORECASE,
)
_NORTHERN_IRELAND_DESCRIPTION_RE = re.compile(
    r"\b(?:belfast|londonderry|derriaghy|l['’]?derry|derry)"
    r"(?:\s+city\s+centre)?(?:-based|\s+based)?\b"
    r"|\bbased\s+(?:in|at)\s+"
    r"(?:belfast|londonderry|derriaghy|l['’]?derry|derry)\b"
    r"|\bnorthern\s+ireland\b",
    re.IGNORECASE,
)
_GEOGRAPHY_CONFLICT_REASON = (
    "geographic contradiction: London mapping conflicts with Northern Ireland location evidence"
)


def area_is_unusable(area: str) -> bool:
    """Treat generic ``City`` as ambiguous rather than as the City of London."""
    return _ORIGINAL_AREA_IS_UNUSABLE(area) or _core.norm_key(area) in AMBIGUOUS_AREA_KEYS


def normalize_postcode_district(value: Any) -> str:
    """Compatibility export for existing tests/callers."""
    return _geo.normalize_postcode_district(value)


def extract_postcode_district(text: Any) -> str:
    """Compatibility export for existing tests/callers."""
    return _geo.extract_postcode_district(text)


def load_postcode_location_overrides(
    path: Path = POSTCODE_LOCATION_OVERRIDES_PATH,
) -> dict[str, str]:
    """Return postcode-district -> display-location for legacy display callers."""
    return {
        district: item.display_location
        for district, item in _geo.load_postcode_overrides(path).items()
        if item.display_location
    }


def postcode_location_overrides_by_job_id(job_df: Any) -> dict[str, str]:
    """Resolve explicit description postcodes through the curated override register."""
    postcode_lookup = load_postcode_location_overrides()
    if not postcode_lookup:
        return {}

    overrides: dict[str, str] = {}
    for _, row in job_df.iterrows():
        description = _core.norm(row.get(_core.COL["description"]))
        district = extract_postcode_district(description[:POSTCODE_DESCRIPTION_WINDOW])
        display_location = postcode_lookup.get(district, "")
        job_id = _core.norm(row.get(_core.COL["job_id"]))
        if job_id and display_location:
            overrides[job_id] = display_location
    return overrides


def _clean_cluster(value: Any) -> str:
    raw = _core.norm(value)
    if not raw:
        return ""
    mapped = _core.REGION_MAP.get(_core.norm_key(raw), raw)
    return _core.COMBINED_OUTPUT_REGION_MAP.get(mapped, mapped)


def build_complete_geo_lookups(
    path: Path | None = None,
) -> tuple[dict[str, str], dict[str, str]]:
    """Load all configured geo clusters, including regions that are not LIVE.

    The core pipeline historically discarded lookup clusters it did not publish.
    For correct routing we still need to *recognise* those clusters so a job is
    excluded from the wrong live slice instead of being pulled into it.
    """
    lookup_path = path or _core.DEFAULT_GEO_LOOKUP_PATH
    area_df = _core.read_xlsx_sheet(lookup_path)
    location_df = _core.read_xlsx_sheet(lookup_path, sheet_name="LocationFallback")

    area_lookup: dict[str, str] = {}
    for _, row in area_df.iterrows():
        area = _core.norm_key(row.get("Area"))
        region = _clean_cluster(row.get("Cluster"))
        if area and region:
            area_lookup[area] = region

    location_lookup: dict[str, str] = {}
    for _, row in location_df.iterrows():
        if _core.norm_key(row.get("Status")) != "auto":
            continue
        location = _core.norm_key(row.get("Location"))
        region = _clean_cluster(row.get("Cluster"))
        if location and region:
            location_lookup[location] = region

    return area_lookup, location_lookup


def resolve_job_geography(
    row: Any,
    area_lookup: dict[str, str],
    location_lookup: dict[str, str],
    postcode_overrides: dict[str, _geo.PostcodeOverride] | None = None,
) -> _geo.GeoResolution:
    """Resolve one row through postcode -> precise location -> area -> advert postcode."""
    return _geo.resolve_job_geography(
        row,
        area_column=_core.COL["area"],
        location_column=_core.COL["location"],
        description_column=_core.COL["description"],
        area_lookup=area_lookup,
        location_lookup=location_lookup,
        postcode_overrides=postcode_overrides or _geo.load_postcode_overrides(),
        area_is_unusable=area_is_unusable,
        postal_code_column=POSTAL_CODE_COLUMN,
    )


def prepare_structured_geography(
    job_df: Any,
    lookup: dict[str, str],
    location_fallback_lookup: dict[str, str],
) -> tuple[Any, dict[str, str], dict[str, str], dict[str, _geo.GeoResolution]]:
    """Prepare a copy of the feed so the unchanged core selector sees resolved regions."""
    full_area_lookup, full_location_lookup = build_complete_geo_lookups()
    # Preserve caller/test additions while giving the resolver visibility of all
    # regions in the authoritative workbook.
    full_area_lookup.update(lookup)
    full_location_lookup.update(location_fallback_lookup)
    postcode_overrides = _geo.load_postcode_overrides()

    prepared = job_df.copy()
    augmented_lookup = dict(lookup)
    resolutions: dict[str, _geo.GeoResolution] = {}

    for idx, row in job_df.iterrows():
        job_id = _core.norm(row.get(_core.COL["job_id"]))
        resolution = resolve_job_geography(
            row,
            full_area_lookup,
            full_location_lookup,
            postcode_overrides,
        )
        if job_id:
            resolutions[job_id] = resolution
        if not resolution.region:
            continue

        resolved_town = (
            _core.norm(resolution.town)
            or _core.norm(row.get(_core.COL["location"]))
            or _core.norm(row.get(_core.COL["area"]))
        )
        if not resolved_town:
            continue

        # The established core routes by Area and also uses Area as the town for
        # anchor-town ranking. Put the resolved town there and augment its lookup
        # rather than inventing a synthetic token that would distort ranking.
        prepared.at[idx, _core.COL["area"]] = resolved_town
        augmented_lookup[_core.norm_key(resolved_town)] = resolution.region

    return prepared, augmented_lookup, full_location_lookup, resolutions


def apply_structured_geography_metadata(
    outputs: dict[str, list[dict[str, Any]]],
    report_rows: list[dict[str, Any]],
    resolutions: dict[str, _geo.GeoResolution],
) -> None:
    """Restore truthful town/source metadata after the unchanged selector runs."""
    for items in outputs.values():
        for item in items:
            resolution = resolutions.get(_core.norm(item.get("job_id")))
            if not resolution or not resolution.region:
                continue
            if resolution.town:
                item["location"] = resolution.town
            if "region" in item:
                item["region"] = resolution.region

    for report in report_rows:
        resolution = resolutions.get(_core.norm(report.get("job_id")))
        if not resolution or not resolution.region:
            continue
        if resolution.town and "town" in report:
            report["town"] = resolution.town
        report["region"] = resolution.region
        if "geo_source" in report:
            report["geo_source"] = resolution.source


def apply_postcode_location_overrides(
    outputs: dict[str, list[dict[str, Any]]],
    report_rows: list[dict[str, Any]],
    overrides: dict[str, str],
) -> None:
    """Retain the old advert-postcode display correction as a final fallback."""
    if not overrides:
        return

    for items in outputs.values():
        for item in items:
            job_id = _core.norm(item.get("job_id"))
            display_location = overrides.get(job_id, "")
            if display_location:
                item["location"] = display_location

    for report in report_rows:
        job_id = _core.norm(report.get("job_id"))
        display_location = overrides.get(job_id, "")
        if not display_location:
            continue
        if "town" in report:
            report["town"] = display_location
        if "location" in report:
            report["location"] = display_location
        if "geo_source" in report and report.get("geo_source") not in {
            "structured_postcode",
            "description_postcode",
        }:
            report["geo_source"] = "description_postcode_display_override"


def has_northern_ireland_location_evidence(row: Any) -> bool:
    """Return True for strong Northern Ireland evidence in a JobG8 row."""
    headline_values = [
        _core.norm(row.get(_core.COL["title"])),
        _core.norm(row.get(_core.COL["location"])),
    ]
    headline = " ".join(value for value in headline_values if value)
    description = _core.norm(row.get(_core.COL["description"]))
    return bool(
        _NORTHERN_IRELAND_HEADLINE_RE.search(headline)
        or _NORTHERN_IRELAND_DESCRIPTION_RE.search(description)
    )


def _mapped_region_before_guard(
    row: Any,
    lookup: dict[str, str],
    location_fallback_lookup: dict[str, str],
) -> str:
    """Resolve the region the prepared core pipeline would assign."""
    area = _core.norm_key(row.get(_core.COL["area"]))
    location = _core.norm_key(row.get(_core.COL["location"]))
    region = lookup.get(area) or location_fallback_lookup.get(location, "")
    return _core.COMBINED_OUTPUT_REGION_MAP.get(region, region)


def _geography_conflict_job_ids(
    job_df: Any,
    lookup: dict[str, str],
    location_fallback_lookup: dict[str, str],
) -> set[str]:
    blocked: set[str] = set()
    for _, row in job_df.iterrows():
        if _mapped_region_before_guard(row, lookup, location_fallback_lookup) != "London":
            continue
        if not has_northern_ireland_location_evidence(row):
            continue
        job_id = _core.norm(row.get(_core.COL["job_id"]))
        if job_id:
            blocked.add(job_id)
    return blocked


def process(
    job_df: Any,
    lookup: dict[str, str],
    location_fallback_lookup: dict[str, str],
    overrides: dict[str, str],
    manual_selects: set[str],
    title_register: dict[str, dict[str, str]],
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    """Resolve geography first, then run the established selector unchanged."""
    prepared_df, augmented_lookup, full_location_lookup, resolutions = (
        prepare_structured_geography(job_df, lookup, location_fallback_lookup)
    )
    blocked_ids = _geography_conflict_job_ids(
        prepared_df,
        augmented_lookup,
        full_location_lookup,
    )
    description_postcode_overrides = postcode_location_overrides_by_job_id(job_df)

    outputs, report_rows = _ORIGINAL_PROCESS(
        prepared_df,
        augmented_lookup,
        full_location_lookup,
        overrides,
        manual_selects,
        title_register,
    )

    apply_structured_geography_metadata(outputs, report_rows, resolutions)
    apply_postcode_location_overrides(
        outputs,
        report_rows,
        description_postcode_overrides,
    )

    if not blocked_ids:
        return outputs, report_rows

    for region, items in outputs.items():
        outputs[region] = [
            item for item in items if _core.norm(item.get("job_id")) not in blocked_ids
        ]

    for report in report_rows:
        if _core.norm(report.get("job_id")) not in blocked_ids:
            continue
        report["decision"] = "DROPPED"
        report["selection_status"] = ""
        report["selection_scenario"] = ""
        report["region_selection_message"] = ""
        report["remaining_slots"] = ""
        report["possible_selection_rank"] = ""
        report["region"] = "London"
        report["geo_source"] = "geography_guard"
        report["reason"] = _GEOGRAPHY_CONFLICT_REASON

    return outputs, report_rows


# Patch the implementation module so its existing main() and internal call sites
# use the guarded functions, then re-export its API for compatibility.
_core.area_is_unusable = area_is_unusable
_core.process = process

for _name in dir(_core):
    if not _name.startswith("__"):
        globals().setdefault(_name, getattr(_core, _name))


class _PipelineModule(types.ModuleType):
    """Forward later test/caller assignments to the implementation module."""

    def __getattr__(self, name: str) -> Any:
        return getattr(_core, name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name != "_core" and hasattr(_core, name):
            setattr(_core, name, value)
        super().__setattr__(name, value)


_module = sys.modules.get(__name__)
if _module is not None and not isinstance(_module, _PipelineModule):
    _module.__class__ = _PipelineModule


if __name__ == "__main__":
    _core.main()
