#!/usr/bin/env python3
"""Audit hybrid metadata in generated service-admin JSON outputs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

QUALIFYING = {"hybrid", "partly_remote"}
REMOTE_WORDS = (
    "remote",
    "home working",
    "homeworking",
    "work from home",
    "working from home",
    "hybrid",
)


def load_rows(output_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(output_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"{path} must contain a JSON array")
        for row in data:
            if not isinstance(row, dict):
                raise ValueError(f"{path} contains a non-object row")
            copied = dict(row)
            copied["_source_file"] = path.name
            rows.append(copied)
    return rows


def render_report(rows: list[dict[str, Any]], sample_size: int = 10) -> str:
    qualifying = [
        row for row in rows if str(row.get("working_arrangement", "")) in QUALIFYING
    ]
    invalid = [
        row
        for row in qualifying
        if not str(row.get("working_arrangement_text", "")).strip()
        or not str(row.get("working_arrangement_evidence", "")).strip()
    ]
    remote_mentions_without_badge = [
        row
        for row in rows
        if str(row.get("working_arrangement", "")) not in QUALIFYING
        and any(
            word in str(row.get("description", "")).casefold()
            for word in REMOTE_WORDS
        )
    ]

    lines = [
        f"TOTAL_SELECTED_ADMIN_JOBS={len(rows)}",
        f"HYBRID_JOB_COUNT={len(qualifying)}",
        f"INVALID_HYBRID_METADATA_COUNT={len(invalid)}",
        f"REMOTE_MENTION_WITHOUT_BADGE_COUNT={len(remote_mentions_without_badge)}",
        "",
        "QUALIFYING_EXAMPLES:",
    ]
    for row in qualifying[:sample_size]:
        lines.append(
            " | ".join(
                [
                    str(row.get("title", "")),
                    str(row.get("location", "")),
                    str(row.get("working_arrangement", "")),
                    str(row.get("working_arrangement_text", "")),
                    str(row.get("working_arrangement_evidence", ""))
                    .replace("\n", " ")[:500],
                    str(row.get("_source_file", "")),
                ]
            )
        )

    lines.extend(["", "REMOTE_MENTION_WITHOUT_BADGE_EXAMPLES:"])
    for row in remote_mentions_without_badge[:sample_size]:
        description = str(row.get("description", "")).replace("\n", " ")
        lines.append(
            " | ".join(
                [
                    str(row.get("title", "")),
                    str(row.get("location", "")),
                    str(row.get("working_arrangement", "")),
                    description[:500],
                    str(row.get("_source_file", "")),
                ]
            )
        )

    if invalid:
        lines.extend(["", "INVALID_HYBRID_METADATA:"])
        for row in invalid:
            lines.append(
                f"{row.get('job_id', '')} | {row.get('title', '')} | "
                f"{row.get('_source_file', '')}"
            )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output-admin-service"),
        help="Directory containing generated service-admin JSON files",
    )
    parser.add_argument("--output", type=Path, help="Optional audit text file")
    parser.add_argument("--sample-size", type=int, default=10)
    args = parser.parse_args()

    rows = load_rows(args.output_dir)
    report = render_report(rows, max(args.sample_size, 1))
    print(report, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")

    invalid_count = sum(
        1
        for row in rows
        if str(row.get("working_arrangement", "")) in QUALIFYING
        and (
            not str(row.get("working_arrangement_text", "")).strip()
            or not str(row.get("working_arrangement_evidence", "")).strip()
        )
    )
    return 1 if invalid_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
