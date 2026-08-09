#!/usr/bin/env python3
"""Maintain seven-run local-market opportunity history and approval statuses."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.scan_city_opportunities import (
    DEFAULT_MARKET_REGISTER,
    DEFAULT_REGISTER,
    DEFAULT_THRESHOLD,
    normalise,
    scan_repository,
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


def collect_candidates(
    repo_root: Path,
    register_path: Path,
    market_register_path: Path = DEFAULT_MARKET_REGISTER,
) -> dict[str, dict[str, Any]]:
    scan = scan_repository(
        repo_root,
        threshold=DEFAULT_THRESHOLD,
        near_threshold=NEAR_THRESHOLD,
        register_path=register_path,
        market_register_path=market_register_path,
    )
    candidates: dict[str, dict[str, Any]] = {}
    for row in scan.get("opportunities", []):
        if not isinstance(row, dict):
            continue
        key = candidate_key(
            str(row.get("region", "")),
            str(row.get("slice", "")),
            str(row.get("basis", "")),
            str(row.get("locality", "")),
        )
        candidates[key] = {
            "region": str(row.get("region", "")),
            "slice": str(row.get("slice", "")),
            "locality": str(row.get("locality", "")),
            "basis": str(row.get("basis", "")),
            "jobs": int(row.get("jobs", 0)),
            "route": str(row.get("existing_route", "")),
            "active": bool(row.get("active", False)),
            "registered_market": bool(row.get("registered_market", False)),
        }
    return candidates


def load_history(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {
            "version": 2,
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
            "registered_market": bool(value.get("registered_market")),
        }
    history["version"] = 2
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


def lifecycle_status(
    *,
    current: int,
    qualifying_runs: int,
    active: bool,
    registered_market: bool = False,
) -> str:
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
    if registered_market and current > 0:
        return "BUILDING"
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
        registered_market = bool(
            candidates.get(key, {}).get(
                "registered_market", meta.get("registered_market", False)
            )
        )
        status = lifecycle_status(
            current=current,
            qualifying_runs=qualifying_runs,
            active=active,
            registered_market=registered_market,
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
        "BUILDING": 7,
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
        "- BUILDING: 1-3 current jobs in a registered local employment market",
        f"- Published slices scanned: {current_scan.get('published_slices_scanned', 0)}",
        f"- Jobs scanned: {current_scan.get('jobs_scanned', 0)}",
        f"- Registered local markets: {current_scan.get('regional_markets_defined', 0)}",
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
        lines.append("| — | — | — | No current local-market jobs | 0 | — | — |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--market-register", type=Path, default=DEFAULT_MARKET_REGISTER)
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
    register_path = args.register if args.register.is_absolute() else root / args.register
    market_register_path = (
        args.market_register
        if args.market_register.is_absolute()
        else root / args.market_register
    )

    current_scan = json.loads(current_path.read_text(encoding="utf-8"))
    candidates = collect_candidates(root, register_path, market_register_path)
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
