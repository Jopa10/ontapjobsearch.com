from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

POSTAL_CODE_COLUMN = "/Job/PostalCode"
DEFAULT_POSTCODE_OVERRIDES_PATH = (
    Path(__file__).resolve().parents[1] / "geo" / "postcode_location_overrides.csv"
)
DESCRIPTION_POSTCODE_WINDOW = 700

# These values are useful fallbacks when the area is absent, but are not precise
# enough to overrule a populated, more-specific Area when the two disagree.
BROAD_LOCATION_KEYS = {
    "",
    "city",
    "not specified",
    "unknown",
    "manchester",
    "greater manchester",
    "london",
    "north east",
    "west midlands",
    "yorkshire",
}

_UK_FULL_POSTCODE_RE = re.compile(
    r"\b([A-Z]{1,2}\d[A-Z\d]?)\s*\d\s*[A-Z]{2}\b",
    re.IGNORECASE,
)
_UK_OUTCODE_RE = re.compile(r"^[A-Z]{1,2}\d[A-Z\d]?$", re.IGNORECASE)


@dataclass(frozen=True)
class PostcodeOverride:
    district: str
    display_location: str
    region: str


@dataclass(frozen=True)
class GeoResolution:
    region: str
    town: str
    source: str
    evidence: str = ""
    postcode_district: str = ""


def norm(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def norm_key(value: Any) -> str:
    return norm(value).lower()


def normalize_postcode_district(value: Any) -> str:
    """Return a normalized UK outward code such as SK3, M22 or NE27."""
    text = norm(value).upper()
    if not text:
        return ""
    match = _UK_FULL_POSTCODE_RE.search(text)
    if match:
        return re.sub(r"\s+", "", match.group(1)).upper()
    compact = re.sub(r"\s+", "", text)
    if _UK_OUTCODE_RE.fullmatch(compact):
        return compact
    return ""


def extract_postcode_district(text: Any) -> str:
    match = _UK_FULL_POSTCODE_RE.search(norm(text).upper())
    if not match:
        return ""
    return re.sub(r"\s+", "", match.group(1)).upper()


def load_postcode_overrides(
    path: Path = DEFAULT_POSTCODE_OVERRIDES_PATH,
) -> dict[str, PostcodeOverride]:
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"postcode_district", "display_location", "region"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise SystemExit(
                "STOP: postcode_location_overrides.csv must contain columns named exactly: "
                "postcode_district, display_location, region (notes may follow)"
            )

        overrides: dict[str, PostcodeOverride] = {}
        for row in reader:
            district = normalize_postcode_district(row.get("postcode_district"))
            display_location = norm(row.get("display_location"))
            region = norm(row.get("region"))
            if not district or not region:
                continue
            overrides[district] = PostcodeOverride(
                district=district,
                display_location=display_location,
                region=region,
            )
        return overrides


def _location_is_precise(location: str, area: str) -> bool:
    location_key = norm_key(location)
    if not location_key or location_key in BROAD_LOCATION_KEYS:
        return False
    if location_key == norm_key(area):
        return False
    return True


def resolve_job_geography(
    row: Mapping[str, Any],
    *,
    area_column: str,
    location_column: str,
    description_column: str,
    area_lookup: Mapping[str, str],
    location_lookup: Mapping[str, str],
    postcode_overrides: Mapping[str, PostcodeOverride],
    area_is_unusable: Callable[[str], bool],
    postal_code_column: str = POSTAL_CODE_COLUMN,
) -> GeoResolution:
    """Resolve one JobG8 row using the strongest structured geography first.

    Priority:
      1. structured /Job/PostalCode when its district has a curated mapping;
      2. precise structured /Job/Location;
      3. structured /Job/Area;
      4. explicit postcode near the start of the advert, using the same curated map.

    A broad Location (for example ``Manchester``) is still useful when Area is
    unusable, but it does not overrule a populated Area that points elsewhere.
    """
    area = norm(row.get(area_column))
    location = norm(row.get(location_column))
    description = norm(row.get(description_column))
    structured_postcode = norm(row.get(postal_code_column))

    area_region = area_lookup.get(norm_key(area), "")
    location_region = location_lookup.get(norm_key(location), "")

    district = normalize_postcode_district(structured_postcode)
    postcode_match = postcode_overrides.get(district) if district else None
    if postcode_match:
        return GeoResolution(
            region=postcode_match.region,
            town=postcode_match.display_location or location or area,
            source="structured_postcode",
            evidence=structured_postcode,
            postcode_district=district,
        )

    if location_region:
        if area_is_unusable(area) or not area_region:
            return GeoResolution(
                region=location_region,
                town=location or area,
                source="location",
                evidence=location,
                postcode_district=district,
            )
        if location_region == area_region:
            return GeoResolution(
                region=location_region,
                town=location or area,
                source="location_agrees_area",
                evidence=location,
                postcode_district=district,
            )
        if _location_is_precise(location, area):
            return GeoResolution(
                region=location_region,
                town=location,
                source="precise_location_override",
                evidence=f"{location} overrides Area={area}",
                postcode_district=district,
            )

    if area_region:
        return GeoResolution(
            region=area_region,
            town=area or location,
            source="area",
            evidence=area,
            postcode_district=district,
        )

    description_district = extract_postcode_district(
        description[:DESCRIPTION_POSTCODE_WINDOW]
    )
    description_match = (
        postcode_overrides.get(description_district)
        if description_district
        else None
    )
    if description_match:
        return GeoResolution(
            region=description_match.region,
            town=description_match.display_location or location or area,
            source="description_postcode",
            evidence=description_district,
            postcode_district=description_district,
        )

    return GeoResolution(
        region="",
        town=location or area,
        source="unresolved",
        evidence="no structured geography matched an authoritative lookup",
        postcode_district=district,
    )
