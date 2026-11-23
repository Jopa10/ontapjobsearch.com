"""Collect the already-published regional inventories for the Neon build path.

This reads the exact app JSON files committed to main after the GitHub-file publish.
It does not run selectors, change GitHub files, or publish anything.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
from scripts import publish_verified_pages_live_config as configured  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    scopes: dict[str, list[dict]] = {}
    source_counts: Counter[str] = Counter()
    seen_scopes: set[str] = set()

    for mapping in configured.core.MAPPINGS:
        scope = f"{mapping.category}:{mapping.region}"
        if scope in seen_scopes:
            raise SystemExit(f"Duplicate live publisher scope: {scope}")
        seen_scopes.add(scope)

        path = ROOT / mapping.destination
        if not path.is_file():
            raise SystemExit(f"Published inventory file is missing: {mapping.destination}")
        try:
            rows = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            raise SystemExit(f"Could not read {mapping.destination}: {exc}") from exc
        if not isinstance(rows, list):
            raise SystemExit(f"Published inventory is not a JSON list: {mapping.destination}")

        ids: set[str] = set()
        display_rows: list[dict] = []
        for row in rows:
            if not isinstance(row, dict):
                raise SystemExit(f"Invalid row in {mapping.destination}")
            job_id = str(row.get("job_id") or "")
            if not job_id or job_id in ids:
                raise SystemExit(f"Missing or duplicate job ID in {mapping.destination}: {job_id!r}")
            if not row.get("title") or not row.get("apply_url") or not row.get("source"):
                raise SystemExit(f"Missing title, Apply link, or source in {mapping.destination}: {job_id}")
            ids.add(job_id)
            source = str(row["source"])
            source_counts[source] += 1
            display_rows.append(row)
        scopes[scope] = display_rows

    if len(scopes) < 200:
        raise SystemExit(f"Incomplete LIVE publisher scope set: {len(scopes)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "scopeCount": len(scopes),
                "rowCount": sum(map(len, scopes.values())),
                "sourceCounts": dict(sorted(source_counts.items())),
                "scopes": scopes,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        "ONTAP_PRODUCTION_PUBLISHER_SOURCE "
        + json.dumps(
            {
                "scopes": len(scopes),
                "rows": sum(map(len, scopes.values())),
                "sources": dict(sorted(source_counts.items())),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
