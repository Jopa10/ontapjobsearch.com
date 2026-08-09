#!/usr/bin/env python3
"""Scan published Ontap slices for local employment-market page opportunities.

This is deliberately a reporting tool only. It never publishes, removes, or
rewrites live page JSON. Registered regional markets are monitored independently
under every published slice in their parent region.
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
DEFAULT_MARKET_REGISTER = Path("pipeline/city_pages/opportunity-market-register.json")
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
    active: bool = False
    registered_market: bool = False


@dataclass(frozen=True)
class CityCatchment:
    display_name: str
    parent_page: Path
    route: str
    include_patterns: tuple[str, ...]
    exclude_patterns: tuple[str, ...]
    active: bool = False


@dataclass(frozen=True)
class RegionalMarket:
    region_key: str
    market_key: str
    display_name: str
    include_patterns: tuple[str, ...]
    exclude_patterns: tuple[str, ...]


def normalise(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.casefold().split())


def public_route_page(json_path: Path) -> Path | None:
    """Resolve the public page for a top-level slice JSON.

    Most routes match the JSON stem. A few legacy files retain a `-jobs`
    suffix while the public route does not (for example North East support
    worker), so try the suffix-stripped route as a compatibility fallback.
    """
    exact = json_path.with_suffix("") / "page.tsx"
    if exact.is_file():
        return exact
    if json_path.stem.endswith("-jobs"):
        legacy = json_path.parent / json_path.stem.removesuffix("-jobs") / "page.tsx"
        if legacy.is_file():
            return legacy
    return None


def discover_published_slices(repo_root: Path) -> list[PublishedSlice]:
    """Return top-level regional JSONs that have a matching public route."""
    app_root = repo_root / "app"
    if not app_root.is_dir():
        return []

    found: list[PublishedSlice] = []
    for json_path in sorted(app_root.glob("*/*.json")):
        if json_path.parent.name.startswith("_"):
            continue
        if public_route_page(json_path) is None:
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
    return [item for item in raw if isinstance(item, dict)]


def simple_locality(location: Any, region: Any = "") -> str:
    """Conservatively turn a stated location into an exact locality candidate."""
    if not isinstance(location, str):
        return ""
    value = " ".join(location.strip().split())
    if not value:
        return ""

    value = WORKING_ARRANGEMENT_PARENS.sub("", value).strip()
    if "," in value:
        value = value.split(",", 1)[0].strip()

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
    raw = json.loads(register_path.read_text(encoding="utf-8"))
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
                active=normalise(item.get("lifecycle_state")) == "active",
            )
        )
    return catchments


def load_regional_markets(register_path: Path) -> list[RegionalMarket]:
    if not register_path.is_file():
        return []
    raw = json.loads(register_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("opportunity-market register must be an array")

    markets: list[RegionalMarket] = []
    seen: set[tuple[str, str]] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"opportunity-market row {index} must be an object")
        region_key = normalise(item.get("region_key")).replace(" ", "-")
        market_key = normalise(item.get("market_key")).replace(" ", "-")
        display_name = str(item.get("display_name", "")).strip()
        include = tuple(
            normalise(value)
            for value in item.get("include_patterns", [])
            if normalise(value)
        )
        exclude = tuple(
            normalise(value)
            for value in item.get("exclude_patterns", [])
            if normalise(value)
        )
        if not region_key or not market_key or not display_name or not include:
            raise ValueError(
                f"opportunity-market row {index} needs region_key, market_key, "
                "display_name and include_patterns"
            )
        key = (region_key, market_key)
        if key in seen:
            raise ValueError(f"duplicate opportunity market: {region_key}/{market_key}")
        seen.add(key)
        markets.append(
            RegionalMarket(
                region_key=region_key,
                market_key=market_key,
                display_name=display_name,
                include_patterns=include,
                exclude_patterns=exclude,
            )
        )
    return markets


def patterns_include(
    job: dict[str, Any],
    include_patterns: tuple[str, ...],
    exclude_patterns: tuple[str, ...] = (),
) -> bool:
    location = normalise(job.get("location"))
    if not location:
        return False
    if any(pattern in location for pattern in exclude_patterns):
        return False
    return any(pattern in location for pattern in include_patterns)


def catchment_includes(job: dict[str, Any], catchment: CityCatchment) -> bool:
    return patterns_include(job, catchment.include_patterns, catchment.exclude_patterns)


def market_includes(job: dict[str, Any], market: RegionalMarket) -> bool:
    return patterns_include(job, market.include_patterns, market.exclude_patterns)


def route_exists(repo_root: Path, route: str) -> bool:
    parts = [part for part in route.strip("/").split("/") if part]
    return bool(parts) and (repo_root / "app" / Path(*parts) / "page.tsx").is_file()


def status_for(
    count: int,
    threshold: int,
    near_threshold: int,
    *,
    live: bool = False,
    registered_market: bool = False,
) -> str:
    if live:
        return "LIVE"
    if count >= threshold:
        return "QUALIFIES"
    if count >= near_threshold:
        return "NEAR"
    if registered_market and count > 0:
        return "BUILDING"
    return "BELOW"


def configured_by_parent(
    catchments: Iterable[CityCatchment],
) -> dict[Path, dict[str, CityCatchment]]:
    result: dict[Path, dict[str, CityCatchment]] = defaultdict(dict)
    for catchment in catchments:
        result[catchment.parent_page][normalise(catchment.display_name)] = catchment
    return result


def scan_repository(
    repo_root: Path,
    *,
    threshold: int = DEFAULT_THRESHOLD,
    near_threshold: int = DEFAULT_NEAR_THRESHOLD,
    register_path: Path = DEFAULT_REGISTER,
    market_register_path: Path = DEFAULT_MARKET_REGISTER,
) -> dict[str, Any]:
    if threshold < 1:
        raise ValueError("threshold must be at least 1")
    if near_threshold < 1 or near_threshold > threshold:
        raise ValueError("near_threshold must be between 1 and threshold")

    slices = discover_published_slices(repo_root)
    catchments = load_city_catchments(repo_root / register_path)
    markets = load_regional_markets(repo_root / market_register_path)
    catchment_map = configured_by_parent(catchments)
    markets_by_region: dict[str, list[RegionalMarket]] = defaultdict(list)
    for market in markets:
        markets_by_region[market.region_key].append(market)

    opportunities: list[Opportunity] = []
    total_jobs = 0

    for published_slice in slices:
        parent = published_slice.json_path
        jobs = load_jobs(repo_root / parent)
        total_jobs += len(jobs)
        claimed: set[str] = set()
        configured = catchment_map.get(parent, {})
        used_configured: set[str] = set()

        # Every registered local market is monitored independently under each
        # published category slice in its region.
        for market in markets_by_region.get(published_slice.region_key, []):
            configured_match = configured.get(normalise(market.display_name))
            if configured_match is not None:
                included = [job for job in jobs if catchment_includes(job, configured_match)]
                active = configured_match.active and route_exists(
                    repo_root, configured_match.route
                )
                basis = "configured-catchment"
                route = configured_match.route if active else ""
                used_configured.add(normalise(configured_match.display_name))
            else:
                included = [job for job in jobs if market_includes(job, market)]
                active = False
                basis = "regional-market"
                route = ""

            for job in included:
                job_id = str(job.get("job_id", "")).strip()
                if job_id:
                    claimed.add(job_id)

            count = len(included)
            status = status_for(
                count,
                threshold,
                near_threshold,
                live=active,
                registered_market=True,
            )
            opportunities.append(
                Opportunity(
                    region=published_slice.region_key,
                    slice=published_slice.slice_key,
                    locality=market.display_name,
                    jobs=count,
                    threshold=threshold,
                    status=status,
                    basis=basis,
                    parent_json=str(parent),
                    existing_route=route,
                    active=active,
                    registered_market=True,
                )
            )

        # Preserve configured live/review city pages even if a future active
        # city has not yet been added to the opportunity-market register.
        for name_key, catchment in configured.items():
            if name_key in used_configured:
                continue
            included = [job for job in jobs if catchment_includes(job, catchment)]
            for job in included:
                job_id = str(job.get("job_id", "")).strip()
                if job_id:
                    claimed.add(job_id)
            active = catchment.active and route_exists(repo_root, catchment.route)
            count = len(included)
            opportunities.append(
                Opportunity(
                    region=published_slice.region_key,
                    slice=published_slice.slice_key,
                    locality=catchment.display_name,
                    jobs=count,
                    threshold=threshold,
                    status=status_for(
                        count,
                        threshold,
                        near_threshold,
                        live=active,
                        registered_market=True,
                    ),
                    basis="configured-catchment",
                    parent_json=str(parent),
                    existing_route=catchment.route if active else "",
                    active=active,
                    registered_market=True,
                )
            )

        # Exact-location fallback remains useful for spotting a concentration
        # we forgot to register, but low-volume one-offs stay out of the report.
        grouped: dict[str, list[str]] = defaultdict(list)
        for job in jobs:
            job_id = str(job.get("job_id", "")).strip()
            if job_id and job_id in claimed:
                continue
            locality = simple_locality(job.get("location"), job.get("region"))
            if not locality:
                continue
            if normalise(locality) == normalise(
                published_slice.region_key.replace("-", " ")
            ):
                continue
            grouped[normalise(locality)].append(locality)

        for values in grouped.values():
            count = len(values)
            status = status_for(count, threshold, near_threshold)
            if status == "BELOW":
                continue
            opportunities.append(
                Opportunity(
                    region=published_slice.region_key,
                    slice=published_slice.slice_key,
                    locality=canonical_display(values),
                    jobs=count,
                    threshold=threshold,
                    status=status,
                    basis="exact-location-unregistered",
                    parent_json=str(parent),
                )
            )

    status_order = {
        "LIVE": 0,
        "QUALIFIES": 1,
        "NEAR": 2,
        "BUILDING": 3,
        "BELOW": 4,
    }
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
        "regional_markets_defined": len(markets),
        "market_rows_monitored": sum(
            1 for item in opportunities if item.registered_market
        ),
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
        f"- Registered local markets: {result.get('regional_markets_defined', 0)}",
        "",
        "| Status | Region | Slice | City/locality | Jobs | Basis |",
        "|---|---|---|---|---:|---|",
    ]
    visible = [item for item in result["opportunities"] if item["status"] != "BELOW"]
    for item in visible:
        lines.append(
            "| {status} | {region} | {slice} | {locality} | {jobs} | {basis} |".format(
                **item
            )
        )
    if not visible:
        lines.append("| — | — | — | No current local-market jobs | 0 | — |")
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
    parser.add_argument("--market-register", type=Path, default=DEFAULT_MARKET_REGISTER)
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
            market_register_path=args.market_register,
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
