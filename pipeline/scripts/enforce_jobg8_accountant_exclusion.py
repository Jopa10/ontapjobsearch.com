#!/usr/bin/env python3
"""Remove owner-excluded JobG8 Accountant titles from every live app JSON page."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

try:
    from .jobg8_title_policy import is_jobg8_accountant_title
except ImportError:
    from jobg8_title_policy import is_jobg8_accountant_title


def atomic_write(path: Path, content: str) -> None:
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def enforce_exclusion(app_dir: Path) -> dict[str, int]:
    """Filter JobG8 Accountant rows from all JSON array pages under ``app_dir``."""
    removed_by_file: dict[str, int] = {}
    if not app_dir.is_dir():
        raise ValueError(f"app directory does not exist: {app_dir}")

    for path in sorted(app_dir.rglob("*.json")):
        try:
            data: Any = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, list):
            continue

        kept = [row for row in data if not (isinstance(row, dict) and is_jobg8_accountant_title(row))]
        removed_count = len(data) - len(kept)
        if not removed_count:
            continue

        atomic_write(path, json.dumps(kept, ensure_ascii=False, indent=2) + "\n")
        removed_by_file[str(path)] = removed_count

    return removed_by_file


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-dir", type=Path, default=Path("app"))
    args = parser.parse_args()

    removed = enforce_exclusion(args.app_dir)
    total = sum(removed.values())
    if not total:
        print("No JobG8 Accountant titles found in live app JSON pages.")
        return 0

    for path, count in removed.items():
        print(f"Removed {count} JobG8 Accountant title(s) from {path}")
    print(f"Removed {total} JobG8 Accountant title(s) from live app JSON pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
