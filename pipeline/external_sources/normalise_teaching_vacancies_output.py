"""Normalise contract labels in approved Teaching Vacancies JSON."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path(
    "output-external/west-yorkshire-teaching-vacancies-admin-service.json"
)


def clean_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalise_contract_value(value: object) -> str:
    raw = clean_text(value)
    if not raw:
        return ""

    items: list[object]
    if raw.startswith("[") and raw.endswith("]"):
        try:
            parsed = json.loads(raw.replace("'", '"'))
        except json.JSONDecodeError:
            parsed = None
        items = parsed if isinstance(parsed, list) else [raw]
    else:
        items = re.split(r"\s*[,;|/]\s*", raw)

    labels: list[str] = []
    for item in items:
        normalised = clean_text(item).replace("_", " ").casefold()
        if not normalised:
            continue
        label = normalised[:1].upper() + normalised[1:]
        if label not in labels:
            labels.append(label)
    return ", ".join(labels)


def normalise_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for source_row in rows:
        row = dict(source_row)
        original = clean_text(row.get("employment_type"))
        contract = normalise_contract_value(original)
        row["employment_type"] = contract
        if original and contract and original != contract:
            for field in ("summary", "description"):
                row[field] = str(row.get(field) or "").replace(original, contract)
        output.append(row)
    return output


def normalise_file(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError(f"approved JSON must be an array of objects: {path}")
    rows = normalise_rows(data)
    invalid = [
        str(row.get("job_id") or "<unknown>")
        for row in rows
        if "[" in clean_text(row.get("employment_type"))
        or "]" in clean_text(row.get("employment_type"))
    ]
    if invalid:
        raise ValueError("unresolved contract list syntax: " + ", ".join(invalid))
    path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, default=DEFAULT_PATH)
    args = parser.parse_args()
    count = normalise_file(args.path)
    print(f"Normalised Teaching Vacancies contracts for {count} approved jobs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
