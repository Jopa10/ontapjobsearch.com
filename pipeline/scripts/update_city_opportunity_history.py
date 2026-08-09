#!/usr/bin/env python3
"""Maintain seven-run city opportunity history and render approval statuses."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.scan_city_opportunities import (
    DEFAULT_REGISTER,
    DEFAULT_THRESHOLD,
    catchment_includes,
    discover_published_slices,
    load_city_catchments,
    load_jobs,
    normalise,
    route_exists,
    simple_locality,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_HISTORY = Path("pipeline/reports/city-opportunity-history.json")
WINDOW_RUNS = 7
REQUIRED_QUALIFYING_RUNS = 3
NEAR_THRESHOLD = 4


def candidate_key(region: str, slice_key: str, basis: str, locality: str) -> str:
    return "|".join(
        (normalise(region), normalise(slice_key), normalise(basis), normalise(locality))
    )


def active_routes(register_path: Path) -> set[str]:
    if not register_path.is_file():
        return set()
    raw = json.loads(register_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        return set()
    return {
        str(item.get("route", "")).strip()
        for item in raw
        if isinstance(item, dict)
        and str(item.get("lifecycle_state", "")).strip().casefold() == "active"
        and str(item.get("route", "")).strip()
    }


def collect_candidates(repo_root: Path, register_path: Path) -> dict[str, dict[str, Any]]:
    slices = discover_published_slices(repo_root)
    slice_by_path = {item.json_path: item for item in slices}
    catchments = load_city_catchments(repo_root / register_path)
    explicitly_active = active_routes(repo_root / register_path)

    candidates: dict[str, dict[str, Any]] = {}
    claimed_by_parent: dict[Path, set[str]] = defaultdict(set)
    jobs_cache: dict[Path, list[dict[str, Any]]] = {}

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

        key = candidate_key(
            published_slice.region_key,
            published_slice.slice_key,
            "configured-catchment",
            catchment.display_name,
        )
        candidates[key] = {
            "region": published_slice.region_key,
            "slice": published_slice.slice_key,
            "locality": catchment.display_name,
            "basis": "configured-catchment",
            "jobs": len(included),
            "route": catchment.route,
            "active": catchment.route in explicitly_active
            and route_exists(repo_root, catchment.route),
        }

    for published_slice in slices:
        jobs = jobs_cache.setdefault(
            published_slice.json_path,
            load_jobs(repo_root / published_slice.json_path),
        )
        grouped: dict[str, list[str]] = defaultdict(list)
        claimed = claimed_by_parent.get(published_slice.json_path, set())
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

        for locality_key, values in grouped.items():
            display = sorted(values, key=lambda value: (normalise(value), value))[0]
            key = candidate_key(
                published_slice.region_key,
                published_slice.slice_key,
                "exact-location",
                display,
            )
            candidates[key] = {
                "region": published_slice.region_key,
                "slice": published_slice.slice_key,
                "locality": display,
                "basis": "exact-location",
                "jobs": len(values),
                "route": "",
                "active": False,
            }

    return candidates


def load_history(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {
            "version": 1,
            "threshold": DEFAULT_THRESHOLD,
            "window_runs": WINDOW_RUNS,
            "required_qualifying_runs": REQUIRED_QUALIFYING_RUNS,
            "candidates": {},
            "snapshots": [],
        }
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("city opportunity history must be a JSON object")
    raw.setdefault("candidates", {})
    raw.setdefault("snapshots", [])
    return raw


def append_snapshot(
    history: dict[str, Any],
    candidates: dict[str, dict[str, Any]],
    *,
    run_id: str,
    run_at: str,
) -> dict[str, Any]:
    snapshots = [
        item
        for item in history.get("snapshots", [])
        if isinstance(item, dict) and str(item.get("run_id", "")) != run_id
    ]
    snapshots.append(
        {
            "run_id": run_id,
            "run_at": run_at,
            "counts": {key: int(value["jobs"]) for key, value in candidates.items()},
        }
    )
    history["snapshots"] = snapshots[-WINDOW_RUNS:]
    labels = history.setdefault("candidates", {})
    for key, value in candidates.items():
        labels[key] = {
            "region": value["region"],
            "slice": value["slice"],
            "locality": value["locality"],
            "basis": value["basis"],
            "route": value.get("route", ""),
            "active": bool(value.get("active")),
        }
    history["version"] = 1
    history["threshold"] = DEFAULT_THRESHOLD
    history["window_runs"] = WINDOW_RUNS
    history["required_qualifying_runs"] = REQUIRED_QUALIFYING_RUNS
    return history


def recent_counts(history: dict[str, Any], key: str) -> list[int]:
    values: list[int] = []
    for snapshot in history.get("snapshots", [])[-WINDOW_RUNS:]:
        counts = snapshot.get("counts", {}) if isinstance(snapshot, dict) else {}
        try:
            values.append(int(counts.get(key, 0)))
        except (TypeError, ValueError):
            values.append(0)
    return values


def lifecycle_status(*, current: int, qualifying_runs: int, active: bool) -> str:
    if active:
        return "LIVE"
    if current >= DEFAULT_THRESHOLD and qualifying_runs >= REQUIRED_QUALIFYING_RUNS:
        return "READY FOR APPROVAL"
    if current >= DEFAULT_THRESHOLD:
        return f"QUALIFIES {qualifying_runs}/{REQUIRED_QUALIFYING_RUNS}"
    if current >= NEAR_THRESHOLD:
        return "NEAR"
    if qualifying_runs >= REQUIRED_QUALIFYING_RUNS:
        return "WATCH"
    return "BELOW"


def render_report(
    current_scan: dict[str, Any],
    candidates: dict[str, dict[str, Any]],
    history: dict[str, Any],
) -> str:
    metadata = dict(history.get("candidates", {}))
    for key, value in candidates.items():
        metadata[key] = {**metadata.get(key, {}), **value}

    rows: list[dict[str, Any]] = []
    for key, meta in metadata.items():
        current = int(candidates.get(key, {}).get("jobs", 0))
        counts = recent_counts(history, key)
        qualifying_runs = sum(value >= DEFAULT_THRESHOLD for value in counts)
        active = bool(candidates.get(key, {}).get("active", meta.get("active", False)))
        status = lifecycle_status(
            current=current,
            qualifying_runs=qualifying_runs,
            active=active,
        )
        if status == "BELOW":
            continue
        rows.append(
            {
                "status": status,
                "region": meta.get("region", ""),
                "slice": meta.get("slice", ""),
                "locality": meta.get("locality", ""),
                "jobs": current,
                "history": ", ".join(str(value) for value in counts) if counts else "—",
                "qualifying_runs": qualifying_runs,
                "basis": meta.get("basis", ""),
            }
        )

    order = {
        "READY FOR APPROVAL": 0,
        "LIVE": 1,
        "QUALIFIES 2/3": 2,
        "QUALIFIES 1/3": 3,
        "QUALIFIES 0/3": 4,
        "NEAR": 5,
        "WATCH": 6,
    }
    rows.sort(
        key=lambda row: (
            order.get(row["status"], 9),
            -row["jobs"],
            row["region"],
            row["slice"],
            normalise(row["locality"]),
        )
    )

    lines = [
        "# City opportunity scan",
        "",
        f"- Publish-candidate threshold: {DEFAULT_THRESHOLD} live jobs",
        f"- Qualification history: {REQUIRED_QUALIFYING_RUNS} of the last {WINDOW_RUNS} pipeline runs at {DEFAULT_THRESHOLD}+ jobs",
        "- Publication: explicit approval required; READY FOR APPROVAL does not publish automatically",
        "- Active pages: permanent; falling below the launch threshold does not delist the route",
        f"- Published slices scanned: {current_scan.get('published_slices_scanned', 0)}",
        f"- Jobs scanned: {current_scan.get('jobs_scanned', 0)}",
        "",
        "| Status | Region | Slice | City/locality | Today | Last pipeline runs | Basis |",
        "|---|---|---|---|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['status']} | {row['region']} | {row['slice']} | {row['locality']} | "
            f"{row['jobs']} | {row['history']} | {row['basis']} |"
        )
    if not rows:
        lines.append("| — | — | — | No qualifying/near candidates | 0 | — | — |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument(
        "--register", type=Path, default=DEFAULT_REGISTER
    )
    parser.add_argument("--current-json", type=Path, required=True)
    parser.add_argument("--history-json", type=Path, default=DEFAULT_HISTORY)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--record-snapshot", action="store_true")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--run-at", default="")
    args = parser.parse_args()

    root = args.repo_root.resolve()
    current_path = args.current_json if args.current_json.is_absolute() else root / args.current_json
    history_path = args.history_json if args.history_json.is_absolute() else root / args.history_json
    output_path = args.output_md if args.output_md.is_absolute() else root / args.output_md

    current_scan = json.loads(current_path.read_text(encoding="utf-8"))
    candidates = collect_candidates(root, args.register)
    history = load_history(history_path)

    if args.record_snapshot:
        if not args.run_id:
            parser.error("--run-id is required with --record-snapshot")
        run_at = args.run_at or datetime.now(timezone.utc).isoformat()
        append_snapshot(history, candidates, run_id=args.run_id, run_at=run_at)
        history_path.parent.mkdir(parents=True, exist_ok=True)
        history_path.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_report(current_scan, candidates, history), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
