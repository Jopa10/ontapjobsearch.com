"""Shared regional contracts for Ontap external-source processing.

This module deliberately reuses Ontap's two existing authorities:

* ``geo/geo_lookup.xlsx`` routes factual locations to Ontap regions.
* ``registers/region_category_slice_register.csv`` controls LIVE/CANDIDATE status.

It does not create or maintain a replacement central registry.
"""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from openpyxl import load_workbook


CATEGORY_ADMIN_SERVICE = "admin_service"
PUBLISHABLE_STATUS = "LIVE"
KNOWN_SLICE_STATUSES = {"LIVE", "CANDIDATE", "RETIRED"}


@dataclass(frozen=True)
class SliceAuthority:
    region: str
    category: str
    status: str

    @property
    def may_publish(self) -> bool:
        return self.status == PUBLISHABLE_STATUS


@dataclass(frozen=True)
class GeographyResult:
    status: str
    region: str = ""
    evidence: str = ""
    lookup_key: str = ""


@dataclass
class DiscoveryRecord:
    source: str
    source_job_id: str
    canonical_url: str
    title: str = ""
    employer: str = ""
    location: str = ""
    postcode: str = ""
    salary_text: str = ""
    posted_date: str = ""
    closing_date: str = ""
    employment_type: str = ""
    description_excerpt: str = ""
    discovery_routes: list[dict[str, object]] = field(default_factory=list)

    def stable_key(self) -> str:
        source_id = clean(self.source_job_id)
        if source_id:
            return f"id:{source_id.casefold()}"
        url = canonical_url(self.canonical_url)
        if url:
            return f"url:{url.casefold()}"
        raise ValueError("source-wide discovery row has no stable source ID or URL")

    def add_provenance(self, *, route: str, query: str, page: int) -> None:
        item = {"route": clean(route), "query": clean(query), "page": int(page)}
        if item not in self.discovery_routes:
            self.discovery_routes.append(item)

    def provenance_json(self) -> str:
        return json.dumps(self.discovery_routes, ensure_ascii=False, sort_keys=True)


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\xa0", " ")).strip()


def normalise(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).casefold()).strip()


def canonical_url(value: object) -> str:
    text = clean(value)
    return text.split("#", 1)[0].rstrip("/")


def load_slice_authorities(path: Path) -> dict[tuple[str, str], SliceAuthority]:
    if not path.is_file():
        raise ValueError(f"slice register not found: {path}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["region", "category", "status"]:
            raise ValueError(
                "slice register columns must be exactly region,category,status"
            )
        output: dict[tuple[str, str], SliceAuthority] = {}
        for line_number, row in enumerate(reader, start=2):
            region = clean(row.get("region"))
            category = clean(row.get("category"))
            status = clean(row.get("status")).upper()
            if not region or not category or status not in KNOWN_SLICE_STATUSES:
                raise ValueError(f"invalid slice register row at line {line_number}")
            key = (region, category)
            if key in output:
                raise ValueError(f"duplicate slice authority: {region} / {category}")
            output[key] = SliceAuthority(region, category, status)
    return output


def slice_authority(
    authorities: dict[tuple[str, str], SliceAuthority],
    *,
    region: str,
    category: str,
) -> SliceAuthority | None:
    """Return the explicit authority; absence never implies LIVE."""
    return authorities.get((clean(region), clean(category)))


def publishable_region(
    authorities: dict[tuple[str, str], SliceAuthority],
    *,
    region: str,
    category: str,
) -> bool:
    authority = slice_authority(authorities, region=region, category=category)
    return bool(authority and authority.may_publish)


def merge_discovery_records(records: Iterable[DiscoveryRecord]) -> list[DiscoveryRecord]:
    """Deduplicate source-wide discovery before geography or classification."""
    merged: dict[str, DiscoveryRecord] = {}
    for record in records:
        key = record.stable_key()
        current = merged.get(key)
        if current is None:
            merged[key] = record
            continue
        factual_fields = (
            "source",
            "source_job_id",
            "canonical_url",
            "title",
            "employer",
            "location",
            "postcode",
            "salary_text",
            "posted_date",
            "closing_date",
            "employment_type",
            "description_excerpt",
        )
        for field_name in factual_fields:
            old = clean(getattr(current, field_name))
            new = clean(getattr(record, field_name))
            if old and new and old != new:
                raise ValueError(
                    f"conflicting factual discovery values for {key}: {field_name}"
                )
            if not old and new:
                setattr(current, field_name, new)
        for item in record.discovery_routes:
            current.add_provenance(
                route=clean(item.get("route")),
                query=clean(item.get("query")),
                page=int(item.get("page") or 1),
            )
    return sorted(merged.values(), key=lambda item: item.stable_key())


_GEO_COLUMN_ALIASES = {
    "lookup": (
        "location",
        "location_clean",
        "lookup",
        "lookup_value",
        "area",
        "town",
        "place",
        "postcode",
        "postcode_area",
    ),
    "region": (
        "region",
        "ontap_region",
        "region_cluster",
        "cluster",
    ),
}


def _column_index(headers: list[str], aliases: tuple[str, ...]) -> int | None:
    normalised = [normalise(header).replace(" ", "_") for header in headers]
    for alias in aliases:
        target = normalise(alias).replace(" ", "_")
        if target in normalised:
            return normalised.index(target)
    return None


def load_geo_lookup(path: Path) -> dict[str, str]:
    """Load the existing workbook without assuming one historical column name."""
    if not path.is_file():
        raise ValueError(f"geographic lookup not found: {path}")
    workbook = load_workbook(path, read_only=True, data_only=True)
    worksheet = workbook.active
    rows = worksheet.iter_rows(values_only=True)
    try:
        headers = [clean(value) for value in next(rows)]
    except StopIteration as exc:
        raise ValueError("geographic lookup is empty") from exc
    lookup_index = _column_index(headers, _GEO_COLUMN_ALIASES["lookup"])
    region_index = _column_index(headers, _GEO_COLUMN_ALIASES["region"])
    if lookup_index is None or region_index is None:
        raise ValueError(
            "geographic lookup must expose a recognised location and Ontap region column"
        )
    output: dict[str, str] = {}
    for row_number, row in enumerate(rows, start=2):
        lookup_value = normalise(row[lookup_index] if lookup_index < len(row) else "")
        region = clean(row[region_index] if region_index < len(row) else "")
        if not lookup_value or not region:
            continue
        existing = output.get(lookup_value)
        if existing and existing != region:
            raise ValueError(
                f"ambiguous geographic lookup value at row {row_number}: {lookup_value}"
            )
        output[lookup_value] = region
    if not output:
        raise ValueError("geographic lookup contains no usable mappings")
    return output


def route_geography(
    *,
    location: str,
    postcode: str,
    lookup: dict[str, str],
) -> GeographyResult:
    """Route factual location evidence only; uncertain geography remains visible."""
    candidates: list[tuple[str, str]] = []
    for label, raw in (("postcode", postcode), ("location", location)):
        key = normalise(raw)
        if key:
            candidates.append((label, key))
            postcode_outward = re.match(r"^([a-z]{1,2}\d[a-z\d]?)\b", key)
            if postcode_outward:
                candidates.append(("postcode outward", postcode_outward.group(1)))
            postcode_area = re.match(r"^([a-z]{1,2})\d", key)
            if postcode_area:
                candidates.append(("postcode area", postcode_area.group(1)))
    matches: dict[str, tuple[str, str]] = {}
    for evidence_type, key in candidates:
        region = lookup.get(key)
        if region:
            matches[region] = (evidence_type, key)
    if not matches:
        return GeographyResult(
            status="UNRESOLVED",
            evidence="No exact factual location match in geo_lookup.xlsx",
        )
    if len(matches) > 1:
        return GeographyResult(
            status="UNRESOLVED",
            evidence="Conflicting factual location matches in geo_lookup.xlsx",
        )
    region, (evidence_type, key) = next(iter(matches.items()))
    return GeographyResult(
        status="ROUTED",
        region=region,
        evidence=f"Exact {evidence_type} match",
        lookup_key=key,
    )
