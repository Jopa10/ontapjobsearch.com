#!/usr/bin/env python3
"""Build a review-only <=15-mile locality-pair report from current live jobs."""

from __future__ import annotations

import csv
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from live_job_source_counter import collect_live_inventory

ROOT = Path(__file__).resolve().parents[2]
COORDINATES = ROOT / "pipeline/registers/canonical_location_coordinates.csv"
EXCEPTIONS = ROOT / "pipeline/registers/city_nearby_rules.csv"
OUTPUT = ROOT / "pipeline/reports/location-proximity-review.csv"
MAX_DISTANCE_MILES = 15.0

BROAD_OR_UNUSABLE = {
    "bedfordshire", "berkshire", "buckinghamshire", "cambridgeshire", "cheshire",
    "city", "county durham", "derbyshire", "devon", "dorset", "essex",
    "gloucestershire", "hampshire", "hertfordshire", "kent", "lancashire",
    "leicestershire", "lincolnshire", "merseyside", "norfolk", "northamptonshire",
    "not specified", "nottinghamshire", "oxfordshire", "shropshire", "somerset",
    "staffordshire", "suffolk", "surrey", "sussex", "tyne and wear",
    "warwickshire", "wiltshire", "worcestershire", "yorkshire",
}


@dataclass(frozen=True)
class Place:
    name: str
    region: str
    latitude: float
    longitude: float


def normalise(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").casefold()).strip()


def haversine_miles(left: Place, right: Place) -> float:
    lat1, lon1 = map(math.radians, (left.latitude, left.longitude))
    lat2, lon2 = map(math.radians, (right.latitude, right.longitude))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    value = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 3958.7613 * 2 * math.asin(math.sqrt(value))


def load_places() -> dict[str, list[Place]]:
    by_name: dict[str, list[Place]] = defaultdict(list)
    with COORDINATES.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if not row["latitude"] or not row["longitude"]:
                continue
            place = Place(
                row["canonical_location"].strip(), row["canonical_region"].strip(),
                float(row["latitude"]), float(row["longitude"]),
            )
            by_name[normalise(place.name)].append(place)
    return by_name


def choose(candidates: list[Place], region: str) -> Place | None:
    if not candidates:
        return None
    same_region = [place for place in candidates if normalise(place.region) == normalise(region)]
    if len(same_region) == 1:
        return same_region[0]
    if normalise(region) == "north east":
        north_east = [place for place in candidates if normalise(place.region).startswith("north east")]
        if len(north_east) == 1:
            return north_east[0]
    if len(candidates) == 1:
        return candidates[0]
    coordinates = {(place.latitude, place.longitude) for place in candidates}
    return candidates[0] if len(coordinates) == 1 else None


def resolve_location(raw: str, region: str, by_name: dict[str, list[Place]]) -> Place | None:
    raw_key = normalise(raw)
    if raw_key in BROAD_OR_UNUSABLE or raw_key.endswith(" council"):
        return None
    direct = choose(by_name.get(raw_key, []), region)
    if direct:
        return direct
    for segment in (part.strip() for part in raw.split(",")):
        match = choose(by_name.get(normalise(segment), []), region)
        if match:
            return match
    if "," not in raw and not re.search(r"\b[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b", raw, re.I):
        return None
    contained = [
        place
        for key, candidates in by_name.items()
        if len(key) >= 5 and re.search(rf"(?<![a-z0-9]){re.escape(key)}(?![a-z0-9])", raw_key)
        for place in candidates
    ]
    if not contained:
        return None
    longest = max(len(normalise(place.name)) for place in contained)
    return choose([place for place in contained if len(normalise(place.name)) == longest], region)


def load_exclusions() -> set[tuple[str, str, str, str]]:
    exclusions = set()
    with EXCEPTIONS.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if (
                row.get("action", "").strip() == "EXCLUDE"
                and row.get("status", "").strip() == "APPROVED"
                and row.get("active", "").strip().upper() == "TRUE"
                and row.get("approval_status", "").strip() == "APPROVED"
            ):
                exclusions.add((
                    normalise(row.get("anchor_location")), normalise(row.get("anchor_region")),
                    normalise(row.get("nearby_location")), normalise(row.get("nearby_region")),
                ))
    return exclusions


def main() -> None:
    by_name = load_places()
    inventory = collect_live_inventory(ROOT / "app")
    groups: Counter[Place] = Counter()
    unresolved: Counter[str] = Counter()
    for job in inventory.jobs:
        place = resolve_location(job.location, job.region, by_name)
        if place:
            groups[place] += 1
        else:
            unresolved[job.location] += 1

    exclusions = load_exclusions()
    rows = []
    places = sorted(groups, key=lambda place: (place.name.casefold(), place.region.casefold()))
    for anchor in places:
        for nearby in places:
            if anchor == nearby:
                continue
            distance = haversine_miles(anchor, nearby)
            if distance > MAX_DISTANCE_MILES:
                continue
            key = (
                normalise(anchor.name), normalise(anchor.region),
                normalise(nearby.name), normalise(nearby.region),
            )
            if key in exclusions:
                continue
            rows.append({
                "anchor_location": anchor.name, "anchor_region": anchor.region,
                "anchor_job_count": groups[anchor], "nearby_location": nearby.name,
                "nearby_region": nearby.region, "nearby_job_count": groups[nearby],
                "distance_miles": f"{distance:.1f}", "distance_method": "HAVERSINE_STRAIGHT_LINE",
                "max_distance_miles": f"{MAX_DISTANCE_MILES:.1f}",
                "display_location_policy": "PRESERVE_TRUE_JOB_LOCATION", "review_status": "REVIEW",
            })
    rows.sort(key=lambda row: (
        row["anchor_location"].casefold(), float(row["distance_miles"]),
        row["nearby_location"].casefold(),
    ))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "anchor_location", "anchor_region", "anchor_job_count", "nearby_location",
        "nearby_region", "nearby_job_count", "distance_miles", "distance_method",
        "max_distance_miles", "display_location_policy", "review_status",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(
        f"jobs={len(inventory.jobs)} resolved={sum(groups.values())} "
        f"unresolved={sum(unresolved.values())} localities={len(groups)} pairs={len(rows)}"
    )
    for location, count in unresolved.most_common():
        print(f"UNRESOLVED\t{count}\t{location}")


if __name__ == "__main__":
    main()
