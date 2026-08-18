from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

POSTAL_CODE_COLUMN = "/Job/PostalCode"
DEFAULT_POSTCODE_OVERRIDES_PATH = (
    Path(__file__).resolve().parents[1] / "geo" / "postcode_location_overrides.csv"
)
DESCRIPTION_POSTCODE_WINDOW = 700
DESCRIPTION_PLACE_WINDOW = 500

BROAD_AREA_KEYS = {
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
    "lancashire",
    "cumbria",
}
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
    "lancashire",
    "cumbria",
}
INVALID_REGION_KEYS = {
    "",
    "unknown",
    "not specified",
    "unmapped",
    "n/a",
    "na",
}

_UK_FULL_POSTCODE_RE = re.compile(
    r"\b([A-Z]{1,2}\d[A-Z\d]?)\s*\d\s*[A-Z]{2}\b",
    re.IGNORECASE,
)
_UK_OUTCODE_RE = re.compile(r"^[A-Z]{1,2}\d[A-Z\d]?$", re.IGNORECASE)
_UK_OUTCODE_SECTOR_RE = re.compile(
    r"^([A-Z]{1,2}\d[A-Z\d]?)\s+(\d)$",
    re.IGNORECASE,
)
_HTML_TAG_RE = re.compile(r"<[^>]+>")


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


@dataclass(frozen=True)
class DescriptionPlaceRule:
    place_key: str
    display_location: str
    region: str
    cue_pattern: re.Pattern[str]
    postcode_pattern: re.Pattern[str]
    dash_pattern: re.Pattern[str]


_DESCRIPTION_RULE_CACHE: dict[int, tuple[Mapping[str, str], tuple[DescriptionPlaceRule, ...]]] = {}


def norm(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def norm_key(value: Any) -> str:
    return norm(value).lower()


def description_text(value: Any) -> str:
    """Convert JobG8's HTML description into stable plain text for geo matching.

    Location labels are often split by markup (for example
    ``<strong>Location:</strong> Oldham``). Matching the raw HTML causes valid
    location evidence to be missed, so tags are replaced by spaces before the
    normal whitespace collapse. This is only for geography evidence; it does not
    alter the description that is published.
    """
    if value is None:
        return ""
    text = unescape(str(value)).replace("\u00a0", " ")
    text = _HTML_TAG_RE.sub(" ", text)
    return norm(text)


def _valid_region(value: Any) -> str:
    region = norm(value)
    return "" if norm_key(region) in INVALID_REGION_KEYS else region


def normalize_postcode_district(value: Any) -> str:
    """Return a UK outward code from full, outward-only, or JobG8 sector data."""
    text = norm(value).upper()
    if not text:
        return ""
    full_match = _UK_FULL_POSTCODE_RE.search(text)
    if full_match:
        return full_match.group(1).upper()
    sector_match = _UK_OUTCODE_SECTOR_RE.fullmatch(text)
    if sector_match:
        return sector_match.group(1).upper()
    if _UK_OUTCODE_RE.fullmatch(text):
        return text.upper()
    return ""


def extract_postcode_district(text: Any) -> str:
    match = _UK_FULL_POSTCODE_RE.search(description_text(text).upper())
    if not match:
        return ""
    return match.group(1).upper()


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
            region = _valid_region(row.get("region"))
            if not district or not region:
                continue
            overrides[district] = PostcodeOverride(district, display_location, region)
        return overrides


def _display_place(place_key: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[\s-]+", place_key) if part)


def _place_regex(place_key: str) -> str:
    parts = [re.escape(part) for part in re.split(r"[\s-]+", place_key) if part]
    return r"[\s-]+".join(parts)


def build_description_place_rules(
    area_lookup: Mapping[str, str],
) -> tuple[DescriptionPlaceRule, ...]:
    """Compile conservative explicit advert-place rules from the authoritative Area map."""
    rules: list[DescriptionPlaceRule] = []
    seen: set[tuple[str, str]] = set()
    for raw_place, raw_region in area_lookup.items():
        place_key = norm_key(raw_place)
        region = _valid_region(raw_region)
        if (
            not place_key
            or not region
            or place_key in BROAD_AREA_KEYS
            or len(place_key) < 4
            or (place_key, region) in seen
        ):
            continue
        seen.add((place_key, region))
        place_re = _place_regex(place_key)
        place_group = rf"(?P<place>{place_re})"
        cue_pattern = re.compile(
            rf"(?:"
            rf"\blocation\s*[:\-]\s*"
            rf"|\bbased\s+(?:in|at)\s+(?:the\s+)?"
            rf"|\blocated\s+(?:in|at)\s+(?:the\s+)?"
            rf"|\b(?:site|office|team|client|business|company)\s+"
            rf"(?:is\s+)?(?:based\s+)?(?:in|at)\s+(?:the\s+)?"
            rf"|\bjoin(?:ing)?(?:\s+us)?\s+(?:in|at)\s+(?:the\s+)?"
            rf"|\bwork(?:ing)?\s+(?:in|at)\s+(?:the\s+)?"
            rf")"
            rf"{place_group}(?:\s+area\b)?",
            re.IGNORECASE,
        )
        postcode_pattern = re.compile(
            rf"\b{place_group}\b\s*,?\s*"
            rf"[A-Z]{{1,2}}\d[A-Z\d]?(?:\s+\d(?:\s*[A-Z]{{2}})?)?\b",
            re.IGNORECASE,
        )
        dash_pattern = re.compile(
            rf"(?:^|\s[-–—]\s){place_group}(?=\s*(?:[\(\[,]|$))",
            re.IGNORECASE,
        )
        rules.append(
            DescriptionPlaceRule(
                place_key,
                _display_place(place_key),
                region,
                cue_pattern,
                postcode_pattern,
                dash_pattern,
            )
        )
    rules.sort(key=lambda item: (-len(item.place_key), item.place_key, item.region))
    return tuple(rules)


def description_place_rules_for_lookup(
    area_lookup: Mapping[str, str],
) -> tuple[DescriptionPlaceRule, ...]:
    cache_key = id(area_lookup)
    cached = _DESCRIPTION_RULE_CACHE.get(cache_key)
    if cached is not None and cached[0] is area_lookup:
        return cached[1]
    rules = build_description_place_rules(area_lookup)
    _DESCRIPTION_RULE_CACHE[cache_key] = (area_lookup, rules)
    return rules


def resolve_description_place(
    description: Any,
    rules: Sequence[DescriptionPlaceRule],
) -> tuple[str, str, str]:
    head = description_text(description)[:DESCRIPTION_PLACE_WINDOW]
    if not head:
        return "", "", ""
    for rule in rules:
        match = rule.cue_pattern.search(head)
        if match:
            return rule.region, rule.display_location, match.group(0)
        match = rule.postcode_pattern.search(head)
        if match:
            return rule.region, rule.display_location, match.group(0)
        match = rule.dash_pattern.search(head[:220])
        if match:
            return rule.region, rule.display_location, match.group(0)
    return "", "", ""


def _location_can_override_area(location: str, area: str) -> bool:
    location_key = norm_key(location)
    area_key = norm_key(area)
    if not location_key or location_key in BROAD_LOCATION_KEYS:
        return False
    if location_key == area_key:
        return False
    return area_key in BROAD_AREA_KEYS


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
    description_place_rules: Sequence[DescriptionPlaceRule] | None = None,
) -> GeoResolution:
    """Resolve JobG8 geography by precision, with broad fields deferred.

    Priority: mapped structured postcode; precise structured Location; specific
    Area; mapped advert postcode; explicit advert place; then broad Area/Location.
    """
    area = norm(row.get(area_column))
    location = norm(row.get(location_column))
    description = description_text(row.get(description_column))
    structured_postcode = norm(row.get(postal_code_column))

    area_key = norm_key(area)
    location_key = norm_key(location)
    area_region = _valid_region(area_lookup.get(area_key, ""))
    location_region = _valid_region(
        location_lookup.get(location_key, "") or area_lookup.get(location_key, "")
    )

    district = normalize_postcode_district(structured_postcode)
    postcode_match = postcode_overrides.get(district) if district else None
    if postcode_match:
        return GeoResolution(
            postcode_match.region,
            postcode_match.display_location or location or area,
            "structured_postcode",
            structured_postcode,
            district,
        )

    area_unusable = area_is_unusable(area)
    area_is_broad = area_unusable or area_key in BROAD_AREA_KEYS or not area_region

    if location_region:
        if area_is_broad and location_key not in BROAD_LOCATION_KEYS:
            return GeoResolution(
                location_region,
                location or area,
                "precise_location",
                location,
                district,
            )
        if location_region == area_region and not area_is_broad:
            return GeoResolution(
                location_region,
                location or area,
                "location_agrees_area",
                location,
                district,
            )
        if _location_can_override_area(location, area):
            return GeoResolution(
                location_region,
                location,
                "precise_location_override",
                f"{location} overrides broad Area={area}",
                district,
            )

    if area_region and not area_is_broad:
        return GeoResolution(area_region, area or location, "area", area, district)

    description_district = extract_postcode_district(description[:DESCRIPTION_POSTCODE_WINDOW])
    description_match = postcode_overrides.get(description_district) if description_district else None
    if description_match:
        return GeoResolution(
            description_match.region,
            description_match.display_location or location or area,
            "description_postcode",
            description_district,
            description_district,
        )

    place_rules = (
        tuple(description_place_rules)
        if description_place_rules is not None
        else description_place_rules_for_lookup(area_lookup)
    )
    description_region, description_town, description_evidence = resolve_description_place(
        description,
        place_rules,
    )
    if description_region:
        return GeoResolution(
            description_region,
            description_town or location or area,
            "description_place",
            description_evidence,
            district or description_district,
        )

    if area_region and not area_unusable:
        return GeoResolution(area_region, area or location, "broad_area", area, district)
    if location_region:
        return GeoResolution(location_region, location or area, "location", location, district)
    return GeoResolution(
        "",
        location or area,
        "unresolved",
        "no structured or explicit advert geography matched an authoritative lookup",
        district,
    )
