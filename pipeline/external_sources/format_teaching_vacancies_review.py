"""Format the West Yorkshire Teaching Vacancies review output.

Standard external-review layout:
- final_decision is the first (left-most) column
- HC rows first
- POSS rows second
- DUPLICATE rows third
- HARD_PASS rows last
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

DECISION_ORDER = {
    "HC": 0,
    "POSS": 1,
    "DUPLICATE": 2,
    "HARD_PASS": 3,
}


def sort_key(row: dict[str, str]) -> tuple[int, str, str, str]:
    decision = (row.get("final_decision") or row.get("classification") or "").strip().upper()
    return (
        DECISION_ORDER.get(decision, 99),
        (row.get("title") or "").casefold(),
        (row.get("employer") or "").casefold(),
        (row.get("location") or "").casefold(),
    )


def ordered_fieldnames(fieldnames: list[str]) -> list[str]:
    if "final_decision" not in fieldnames:
        raise ValueError("Review CSV is missing required final_decision column")
    return ["final_decision", *[name for name in fieldnames if name != "final_decision"]]


def sort_review_csv(path: Path) -> None:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if not fieldnames:
        raise ValueError(f"Review CSV has no header: {path}")

    output_fields = ordered_fieldnames(fieldnames)
    rows.sort(key=sort_key)

    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    sort_review_csv(args.csv_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
