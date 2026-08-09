#!/usr/bin/env python3
"""Scan published Ontap slices for city/locality page opportunities.

This is deliberately a reporting tool only. It never publishes, removes, or
rewrites live page JSON. The default qualification threshold is the established
Ontap baseline of six live jobs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTER = Path("pipeline/city_pages/city-page-register.json")
DEFAULT_THRESHOLD = 6
DEFAULT_NEAR_THRESHOLD = 4

GENERIC_LOCATIONS = {
    "uk",
    "united kingdom",
    "england",
    "remote",
    "home based",
    "home-based",
    "hybrid",
    "various",
    "multiple locations",
    "multiple sites",
    "nationwide",
    "regionwide",
    "not specified",
}
INSTITUTIONAL_TERMS = {
    "academy",
    "borough council",
    "city council",
    "college",
    "county council",
    "depot",
    "hospital",
    "office",
    "school",
    "town hall",
    "university",
}
WORKING_ARRANGEMENT_PARENS = re.compile(
    r"\s*\((?:[^)]*\b(?:hybrid|remote|home[- ]based|working)\b[^)]*)\)\s*$",
    re.IGNORECASE,
)
POSTCODE_TOKEN = re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b", re.IGNORECASE)


@dataclass(frozen=True)
class PublishedSlice:
    region_key: str
    slice_key: str
    json_path: Path


@dataclass(frozen=True)
class Opportunity:
    region: str
    slice: str
    locality: str
    jobs: int
    threshold: int
    status: str
    basis: str
    parent_json: str
    existing_route: str = ""


@dataclass(frozen=True)
class CityCatchment:
    display_name: str
    parent_page: Path
    route: str
    include_patterns: tuple[str, ...]
    exclude_patterns: tuple[str, ...]


def normalise(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.casefold().split())


def discover_published_slices(repo_root: Path) -> list[PublishedSlice]:
    """Return top-level regional JSONs that have a matching public route."""
    app_root = repo_root / "app"
    if not app_root.is_dir():
        return []

    found: list[PublishedSlice] = []
    for json_path in sorted(app_root.glob("*/*.json")):
        if json_path.parent.name.startswith("_"):
            continue
        route_page = json_path.with_suffix("") / "page.tsx"
        if not route_page.is_file():
            continue
        found.append(
            PublishedSlice(
                region_key=json_path.parent.name,
                slice_key=json_path.stem,
                json_path=json_path.relative_to(repo_root),
            )
        )
    return found


def load_jobs(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    if not isinstance(raw, list):
        raise ValueError(f"published slice must be a JSON array: {path}")
    jobs: list[dict[str, Any]] = []
    for item in raw:
        if isinstance(item, dict):
            jobs.append(item)
    return jobs


def simple_locality(location: Any, region: Any = "") -> str:
    """Conservatively turn a stated location into an exact locality candidate.

    We intentionally do not geocode or infer a city from employer/description
    text. This keeps discovery aligned with the Newcastle rule: stated location
    can qualify a page; contextual text cannot.
    """
    if not isinstance(location, str):
        return ""
    value = " ".join(location.strip().split())
    if not value:
        return ""

    value = WORKING_ARRANGEMENT_PARENS.sub("", value).strip()
    if "," in value:
        first = value.split(",", 1)[0].strip()
        # A clean first component such as "Southampton, Hampshire" is useful;
        # an institution/address component such as "Town Hall, ..." is not.
        value = first

    key = normalise(value)
    if not key or key in GENERIC_LOCATIONS:
        return ""
    if key == normalise(region):
        return ""
    if POSTCODE_TOKEN.search(value) or any(ch.isdigit() for ch in value):
        return ""
    if len(value) > 60 or len(value.split()) > 6:
        return ""
    if any(term in key for term in INSTITUTIONAL_TERMS):
        return ""
    return value


def canonical_display(values: Iterable[str]) -> str:
    cleaned = [value.strip() for value in values if value.strip()]
    if not cleaned:
        return ""
    counts: dict[str, int] = defaultdict(int)
    for value in cleaned:
        counts[value] += 1
    return sorted(counts, key=lambda value: (-counts[value], normalise(value), value))[0]


def load_city_catchments(register_path: Path) -> list[CityCatchment]:
    if not register_path.is_file():
        return []
    with register_path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    if not isinstance(raw, list):
        raise ValueError("city-page register must be an array")

    catchments: list[CityCatchment] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        display_name = str(item.get("display_name", "")).strip()
        parent_page = str(item.get("parent_page", "")).strip()
        route = str(item.get("route", "")).strip()
        if not display_name or not parent_page or not route:
            continue

        def patterns(field: str) -> tuple[str, ...]:
            values: list[str] = []
            for rule in item.get(field, []):
                if isinstance(rule, dict):
                    pattern = normalise(rule.get("pattern"))
                    if pattern:
                        values.append(pattern)
            return tuple(values)

        catchments.append(
            CityCatchment(
                display_name=display_name,
                parent_page=Path(parent_page),
                route=route,
                include_patterns=patterns("include_rules"),
                exclude_patterns=patterns("exclude_rules"),
            )
        )
    return catchments


def catchment_includes(job: dict[str, Any], catchment: CityCatchment) -> bool:
    """Mirror the location priority used by the live city derivation.

    Excludes win, then includes. We do not use company/summary to include a job.
    """
    location = normalise(job.get("location"))
    if not location:
        return False
    if any(pattern in location for pattern in catchment.exclude_patterns):
        return False
    return any(pattern in location for pattern in catchment.include_patterns)


def route_exists(repo_root: Path, route: str) -> bool:
    parts = [part for part in route.strip("/").split("/") if part]
    return bool(parts) and (repo_root / "app" / Path(*parts) / "page.tsx").is_file()


def status_for(count: int, threshold: int, near_threshold: int, *, live: bool = False) -> str:
    if live:
        return "LIVE"
    if count >= threshold:
        return "QUALIFIES"
    if count >= near_threshold:
        return "NEAR"
    return "BELOW"


def scan_slice_exact_locations(
    repo_root: Path,
    published_slice: PublishedSlice,
    *,
    threshold: int,
    near_threshold: int,
    claimed_job_ids: set[str] | None = None,
) -> tuple[list[Opportunity], int]:
    jobs = load_jobs(repo_root / published_slice.json_path)
    claimed = claimed_job_ids or set()
    grouped: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)

    for job in jobs:
        job_id = str(job.get("job_id", "")).strip()
        if job_id and job_id in claimed:
            continue
        locality = simple_locality(job.get("location"), job.get("region"))
        if not locality:
            continue
        if normalise(locality) == normalise(published_slice.region_key.replace("-", " ")):
            continue
        grouped[normalise(locality)].append((locality, job))

    opportunities: list[Opportunity] = []
    for members in grouped.values():
        count = len(members)
        status = status_for(count, threshold, near_threshold)
        if status == "BELOW":
            continue
        display = canonical_display(member[0] for member in members)
        opportunities.append(
            Opportunity(
                region=published_slice.region_key,
                slice=published_slice.slice_key,
                locality=display,
                jobs=count,
                threshold=threshold,
                status=status,
                basis="exact-location",
                parent_json=str(published_slice.json_path),
            )
        )
    return opportunities, len(jobs)


def scan_repository(
    repo_root: Path,
    *,
    threshold: int = DEFAULT_THRESHOLD,
    near_threshold: int = DEFAULT_NEAR_THRESHOLD,
    register_path: Path = DEFAULT_REGISTER,
) -> dict[str, Any]:
    if threshold < 1:
        raise ValueError("threshold must be at least 1")
    if near_threshold < 1 or near_threshold > threshold:
        raise ValueError("near_threshold must be between 1 and threshold")

    slices = discover_published_slices(repo_root)
    slice_by_path = {item.json_path: item for item in slices}
    catchments = load_city_catchments(repo_root / register_path)

    opportunities: list[Opportunity] = []
    claimed_by_parent: dict[Path, set[str]] = defaultdict(set)
    jobs_cache: dict[Path, list[dict[str, Any]]] = {}

    # Configured city catchments are counted first and take precedence over
    # exact-location discovery for the same jobs, preventing duplicate
    # Newcastle/Newcastle-upon-Tyne candidate rows.
    for catchment in catchments:
        parent = catchment.parent_page
        published_slice = slice_by_path.get(parent)
        if published_slice is None:
            continue
        jobs = jobs_cache.setdefault(parent, load_jobs(repo_root / parent))
        included = [job for job in jobs if catchment_includes(job, catchment)]
        for job in included:
            job_id = str(job.get("job_id", "")).strip()
            if job_id:
                claimed_by_parent[parent].add(job_id)

        live = route_exists(repo_root, catchment.route)
        count = len(included)
        status = status_for(count, threshold, near_threshold, live=live)
        if status != "BELOW":
            opportunities.append(
                Opportunity(
                    region=published_slice.region_key,
                    slice=published_slice.slice_key,
                    locality=catchment.display_name,
                    jobs=count,
                    threshold=threshold,
                    status=status,
                    basis="configured-catchment",
                    parent_json=str(parent),
                    existing_route=catchment.route if live else "",
                )
            )

    total_jobs = 0
    for published_slice in slices:
        parent = published_slice.json_path
        exact, count = scan_slice_exact_locations(
            repo_root,
            published_slice,
            threshold=threshold,
            near_threshold=near_threshold,
            claimed_job_ids=claimed_by_parent.get(parent, set()),
        )
        total_jobs += count
        opportunities.extend(exact)

    status_order = {"QUALIFIES": 0, "NEAR": 1, "LIVE": 2}
    opportunities.sort(
        key=lambda item: (
            status_order.get(item.status, 9),
            -item.jobs,
            item.region,
            item.slice,
            normalise(item.locality),
        )
    )

    return {
        "threshold": threshold,
        "near_threshold": near_threshold,
        "published_slices_scanned": len(slices),
        "jobs_scanned": total_jobs,
        "opportunities": [asdict(item) for item in opportunities],
    }


def markdown_report(result: dict[str, Any]) -> str:
    lines = [
        "# City opportunity scan",
        "",
        f"- Publish-candidate threshold: {result['threshold']} live jobs",
        f"- Near threshold: {result['near_threshold']} live jobs",
        f"- Published slices scanned: {result['published_slices_scanned']}",
        f"- Jobs scanned: {result['jobs_scanned']}",
        "",
        "| Status | Region | Slice | City/locality | Jobs | Basis |",
        "|---|---|---|---|---:|---|",
    ]
    for item in result["opportunities"]:
        lines.append(
            "| {status} | {region} | {slice} | {locality} | {jobs} | {basis} |".format(
                **item
            )
        )
    if not result["opportunities"]:
        lines.append("| — | — | — | No qualifying/near candidates | 0 | — |")
    return "\n".join(lines) + "\n"


def write_json(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    parser.add_argument("--near-threshold", type=int, default=DEFAULT_NEAR_THRESHOLD)
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Optional JSON report path (relative to repo root unless absolute).",
    )
    args = parser.parse_args()

    try:
        result = scan_repository(
            args.repo_root,
            threshold=args.threshold,
            near_threshold=args.near_threshold,
            register_path=args.register,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"city opportunity scan failed: {exc}", file=sys.stderr)
        return 1

    print(markdown_report(result), end="")
    if args.output_json:
        output = args.output_json
        if not output.is_absolute():
            output = args.repo_root / output
        write_json(output, result)
        print(f"\nJSON report written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
