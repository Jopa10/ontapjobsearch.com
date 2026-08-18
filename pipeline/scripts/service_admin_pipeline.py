"""
Compatibility entry point for the admin/service pipeline with geography safeguards.

The established implementation remains unchanged in
``service_admin_pipeline_core.py``. This module applies small, auditable guards:

- the generic JobG8 ``/Job/Area`` value ``City`` is treated as unusable and
  must resolve through the authoritative ``LocationFallback`` sheet;
- rows mapped to London are removed when their title, location or description
  contains strong Northern Ireland location evidence;
- an explicit UK postcode near the start of the advert can correct an
  inaccurate structured display location through the curated
  ``geo/postcode_location_overrides.csv`` register.
"""
from __future__ import annotations

import csv
import re
import sys
import types
from pathlib import Path
from typing import Any

try:
    from . import service_admin_pipeline_core as _core
except ImportError:  # direct script/test loading
    import service_admin_pipeline_core as _core


_ORIGINAL_AREA_IS_UNUSABLE = _core.area_is_unusable
_ORIGINAL_PROCESS = _core.process

AMBIGUOUS_AREA_KEYS = {"city"}
POSTCODE_LOCATION_OVERRIDES_PATH = (
    Path(__file__).resolve().parents[1] / "geo" / "postcode_location_overrides.csv"
)
POSTCODE_DESCRIPTION_WINDOW = 600

_UK_POSTCODE_RE = re.compile(
    r"\b([A-Z]{1,2}\d[A-Z\d]?)\s*\d\s*[A-Z]\s*[A-Z]\b",
    re.IGNORECASE,
)
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
    """Normalize a postcode district/outcode such as ``NE27`` or ``EC1A``."""
    return re.sub(r"\s+", "", _core.norm(value)).upper()


def extract_postcode_district(text: Any) -> str:
    """Return the first explicit UK postcode district found in ``text``."""
    match = _UK_POSTCODE_RE.search(_core.norm(text))
    if not match:
        return ""
    return normalize_postcode_district(match.group(1))


def load_postcode_location_overrides(
    path: Path = POSTCODE_LOCATION_OVERRIDES_PATH,
) -> dict[str, str]:
    """Load curated postcode-district -> display-location corrections."""
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        required = {"postcode_district", "display_location"}
        if not required.issubset(fieldnames):
            raise SystemExit(
                "STOP: postcode_location_overrides.csv must contain columns named exactly: "
                "postcode_district, display_location"
            )

        overrides: dict[str, str] = {}
        for row in reader:
            district = normalize_postcode_district(row.get("postcode_district"))
            display_location = _core.norm(row.get("display_location"))
            if district and display_location:
                overrides[district] = display_location
        return overrides


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


def apply_postcode_location_overrides(
    outputs: dict[str, list[dict[str, Any]]],
    report_rows: list[dict[str, Any]],
    overrides: dict[str, str],
) -> None:
    """Correct user-visible location labels without changing selection/ranking."""
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
        if "geo_source" in report:
            report["geo_source"] = "postcode_override"


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
    """Resolve the region the unguarded pipeline would have assigned."""
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
    """Run the established pipeline, then enforce geography corrections/guards."""
    blocked_ids = _geography_conflict_job_ids(job_df, lookup, location_fallback_lookup)
    postcode_overrides = postcode_location_overrides_by_job_id(job_df)
    outputs, report_rows = _ORIGINAL_PROCESS(
        job_df,
        lookup,
        location_fallback_lookup,
        overrides,
        manual_selects,
        title_register,
    )

    apply_postcode_location_overrides(outputs, report_rows, postcode_overrides)

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
