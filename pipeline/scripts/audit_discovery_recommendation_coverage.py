#!/usr/bin/env python3
"""Audit the fail-closed discovery panel against the current published inventory."""

from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTERS = ROOT / "pipeline/registers"
REPORT = ROOT / "pipeline/reports/discovery-recommendation-coverage.csv"
SUMMARY = ROOT / "pipeline/reports/discovery-recommendation-coverage.md"
EARTH_RADIUS_MILES = 3958.7613
MAX_DISTANCE_MILES = 15.0
BROAD_LOCATIONS = {
    "bedfordshire", "berkshire", "buckinghamshire", "cambridgeshire", "cheshire",
    "city", "county durham", "derbyshire", "devon", "dorset", "essex",
    "gloucestershire", "hampshire", "hertfordshire", "kent", "lancashire",
    "leicestershire", "lincolnshire", "merseyside", "norfolk", "northamptonshire",
    "not specified", "nottinghamshire", "oxfordshire", "shropshire", "somerset",
    "staffordshire", "suffolk", "surrey", "sussex", "tyne and wear", "warwickshire",
    "wiltshire", "worcestershire", "yorkshire",
}


def normalise(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").casefold()).strip()


def read_csv(name: str) -> list[dict[str, str]]:
    with (REGISTERS / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def approved(row: dict[str, str]) -> bool:
    return (
        row.get("status") == "APPROVED"
        and row.get("active", "").upper() == "TRUE"
        and row.get("approval_status") == "APPROVED"
    )


def load_jobs() -> list[dict[str, object]]:
    jobs: dict[str, dict[str, object]] = {}
    for path in sorted((ROOT / "app").rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, list):
            continue
        for job in data:
            if isinstance(job, dict) and job.get("job_id"):
                jobs.setdefault(str(job["job_id"]), job)
    return list(jobs.values())


def employer_identity(job: dict[str, object]) -> str:
    value = str(job.get("advertiser_name") or job.get("company") or "").strip()
    return re.sub(r"\s+-\s+(?:Agency|Company)\s+-\s+.*$", "", value, flags=re.I).strip()


def rule_value(job: dict[str, object], field: str) -> str:
    if field == "source":
        return str(job.get("source") or "")
    if field == "advertiser_type":
        return str(job.get("advertiser_type") or "")
    if field == "employer_identity":
        return employer_identity(job)
    if field == "combined_text":
        return " ".join(str(job.get(key) or "") for key in (
            "company", "advertiser_name", "description", "full_description"
        ))
    return ""


def classify(job: dict[str, object], rules: list[dict[str, str]]) -> str:
    for rule in rules:
        kind = rule["match_type"]
        if kind == "fallback":
            return normalise(rule["sector"])
        value = rule_value(job, rule["match_field"])
        if kind == "exact" and normalise(value) == normalise(rule["match_value"]):
            return normalise(rule["sector"])
        if kind == "regex":
            try:
                if re.search(rule["match_value"], value, re.I):
                    return normalise(rule["sector"])
            except re.error:
                continue
    return "unknown"


def load_places() -> dict[str, list[tuple[str, str, float, float]]]:
    places: dict[str, list[tuple[str, str, float, float]]] = defaultdict(list)
    for row in read_csv("canonical_location_coordinates.csv"):
        if not approved(row):
            continue
        try:
            latitude, longitude = float(row["latitude"]), float(row["longitude"])
        except ValueError:
            continue
        places[normalise(row["canonical_location"])].append((
            row["canonical_location"], row["canonical_region"], latitude, longitude
        ))
    return places


def resolve_place(
    raw_location: object,
    region: object,
    places: dict[str, list[tuple[str, str, float, float]]],
) -> tuple[str, str, float, float] | None:
    location = str(raw_location or "")
    key = normalise(location)
    if not key or key in BROAD_LOCATIONS or key.endswith(" council"):
        return None

    def choose(candidates: list[tuple[str, str, float, float]]) -> tuple[str, str, float, float] | None:
        if not candidates:
            return None
        same_region = [item for item in candidates if normalise(item[1]) == normalise(region)]
        if len(same_region) == 1:
            return same_region[0]
        if normalise(region) == "north east":
            north_east = [item for item in candidates if normalise(item[1]).startswith("north east")]
            if len(north_east) == 1:
                return north_east[0]
        if len(candidates) == 1:
            return candidates[0]
        if len({(item[2], item[3]) for item in candidates}) == 1:
            return candidates[0]
        return None

    direct = choose(places.get(key, []))
    if direct:
        return direct
    for segment in location.split(","):
        match = choose(places.get(normalise(segment), []))
        if match:
            return match
    if "," not in location and not re.search(r"\b[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b", location, re.I):
        return None
    contained: list[tuple[str, str, float, float]] = []
    for name, candidates in places.items():
        if len(name) >= 5 and re.search(rf"(^| ){re.escape(name)}( |$)", key):
            contained.extend(candidates)
    if not contained:
        return None
    longest = max(len(normalise(item[0])) for item in contained)
    return choose([item for item in contained if len(normalise(item[0])) == longest])


def distance(left: tuple[str, str, float, float], right: tuple[str, str, float, float]) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (left[2], left[3], right[2], right[3]))
    value = (
        math.sin((lat2 - lat1) / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    )
    return EARTH_RADIUS_MILES * 2 * math.asin(math.sqrt(value))


def main() -> None:
    jobs = load_jobs()
    sector_rules = [row for row in read_csv("employer_sector_rules.csv") if approved(row)]
    sector_rules.sort(key=lambda row: (int(row["priority"]), row["rule_id"]))
    role_rules = [row for row in read_csv("role_relationships.csv") if approved(row)]
    places = load_places()

    sectors = {str(job["job_id"]): classify(job, sector_rules) for job in jobs}
    resolved = {
        str(job["job_id"]): resolve_place(job.get("location"), job.get("region"), places)
        for job in jobs
    }
    private_by_title: dict[str, list[dict[str, object]]] = defaultdict(list)
    for job in jobs:
        if sectors[str(job["job_id"])] == "private sector" and resolved[str(job["job_id"])]:
            private_by_title[normalise(job.get("title"))].append(job)

    rules_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for rule in role_rules:
        if rule["direction"] == "ONE_WAY_PUBLIC_TO_PRIVATE" and rule["target_sector_scope"] == "private_sector":
            rules_by_source[normalise(rule["source_role"])].append(rule)

    output: list[dict[str, object]] = []
    examples: list[tuple[str, str, int]] = []
    for job in jobs:
        job_id = str(job["job_id"])
        sector = sectors[job_id]
        source_place = resolved[job_id]
        candidates = [
            rule for rule in rules_by_source.get(normalise(job.get("title")), [])
            if sector in {normalise(value) for value in rule["source_sector_scope"].split("|")}
        ]
        recommendations = 0
        if sector != "unknown" and source_place and candidates:
            targets = {normalise(rule["target_role"]) for rule in candidates}
            for target in targets:
                for other in private_by_title.get(target, []):
                    other_id = str(other["job_id"])
                    if other_id != job_id and distance(source_place, resolved[other_id]) <= MAX_DISTANCE_MILES:
                        recommendations += 1

        if recommendations:
            blocker = ""
            panel_mode = "ranked_jobs"
            examples.append((str(job.get("title") or ""), employer_identity(job), recommendations))
        elif sector == "unknown":
            blocker = "source_employer_sector_unknown"
            panel_mode = "slice_fallback"
        elif not source_place:
            blocker = "source_location_unresolved_or_broad"
            panel_mode = "slice_fallback"
        elif not candidates:
            blocker = "no_exact_source_role_rule"
            panel_mode = "slice_fallback"
        else:
            blocker = "no_eligible_private_target_within_15_miles"
            panel_mode = "slice_fallback"

        output.append({
            "job_id": job_id,
            "title": job.get("title") or "",
            "employer_identity": employer_identity(job),
            "source_sector": sector,
            "location": job.get("location") or "",
            "location_resolved": "TRUE" if source_place else "FALSE",
            "applicable_role_rule_count": len(candidates),
            "recommendation_count": recommendations,
            "panel_mode": panel_mode,
            "blocker": blocker,
        })

    output.sort(key=lambda row: (row["panel_mode"] != "ranked_jobs", -int(row["recommendation_count"]), str(row["job_id"])))
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)

    panel_counts = Counter(str(row["panel_mode"]) for row in output)
    blockers = Counter(str(row["blocker"]) for row in output if row["blocker"])
    sector_counts = Counter(str(row["source_sector"]) for row in output)
    lines = [
        "# Discovery recommendation coverage",
        "",
        f"Generated from {len(jobs):,} unique published jobs. Rules remain exact-title, evidence-based and capped at 15 straight-line miles.",
        "",
        "## Outcome",
        "",
        f"- Ranked-job panels: {panel_counts['ranked_jobs']:,}",
        f"- Slice fallbacks: {panel_counts['slice_fallback']:,}",
        f"- Total eligible recommendation pairs: {sum(int(row['recommendation_count']) for row in output):,}",
        "",
        "## Fallback blockers",
        "",
    ]
    lines.extend(f"- {name}: {count:,}" for name, count in blockers.most_common())
    lines.extend(["", "## Source sectors", ""])
    lines.extend(f"- {name}: {count:,}" for name, count in sector_counts.most_common())
    lines.extend(["", "## Ranked examples", ""])
    grouped_examples: dict[tuple[str, str], tuple[int, int]] = {}
    for title, employer, count in examples:
        pages, maximum = grouped_examples.get((title, employer), (0, 0))
        grouped_examples[(title, employer)] = (pages + 1, max(maximum, count))
    lines.extend(
        f"- {title} — {employer}: {pages} page{'s' if pages != 1 else ''}, up to {maximum} eligible target{'s' if maximum != 1 else ''}"
        for (title, employer), (pages, maximum) in sorted(
            grouped_examples.items(), key=lambda item: (-item[1][1], -item[1][0], item[0][0], item[0][1])
        )[:20]
    )
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT.relative_to(ROOT)} and {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
