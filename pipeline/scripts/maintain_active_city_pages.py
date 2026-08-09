#!/usr/bin/env python3
"""Keep explicitly active city pages populated even below their launch threshold.

The ordinary city derivation still applies the launch threshold. This maintenance
step runs immediately afterwards and rewrites active city JSON from the current
approved parent slice, including an empty array when there are no current jobs.
That keeps the permanent route alive without publishing stale vacancies.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.derive_city_pages import (
    atomic_write,
    derive_rows,
    live_json_text,
    load_markdown_actions,
    load_parent_jobs,
    load_review_decisions,
    merge_review_overrides,
    parse_config,
    selected_live_jobs,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTER = Path("pipeline/city_pages/city-page-register.json")


def active_entries(register_path: Path) -> list[dict[str, Any]]:
    raw = json.loads(register_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("city-page register must be an array")
    return [
        item
        for item in raw
        if isinstance(item, dict)
        and str(item.get("lifecycle_state", "")).strip().casefold() == "active"
    ]


def maintain_active_config(raw: dict[str, Any], root: Path) -> dict[str, Any]:
    config = parse_config(raw)
    if config.output_json is None:
        raise ValueError(f"active city {config.city_key} has no output_json")

    jobs = load_parent_jobs(root / config.parent_page)
    overrides = merge_review_overrides(
        load_review_decisions(root / config.review_csv),
        load_markdown_actions(root / config.summary_md),
    )
    rows = derive_rows(jobs, config, overrides)
    selected = selected_live_jobs(jobs, rows)
    atomic_write(root / config.output_json, live_json_text(selected))
    return {
        "city_key": config.city_key,
        "route": config.route,
        "jobs": len(selected),
        "launch_threshold": int(raw.get("launch_minimum_live_jobs", config.minimum_live_jobs)),
        "status": "active",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    register = args.register if args.register.is_absolute() else root / args.register
    results = [maintain_active_config(item, root) for item in active_entries(register)]

    print("# Active city-page persistence")
    print()
    print("| City | Route | Current jobs | Launch threshold | Status |")
    print("|---|---|---:|---:|---|")
    for item in results:
        print(
            f"| {item['city_key']} | {item['route']} | {item['jobs']} | "
            f"{item['launch_threshold']} | {item['status']} |"
        )
    if not results:
        print("| — | — | 0 | — | No active city pages |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
