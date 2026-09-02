from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path

import pandas as pd


ID_COLUMN = "/Job/DisplayReference"
CATEGORY_COLUMN = "/Job/Classification"


def _text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def load_published_jobg8_ids(output_dirs: list[Path]) -> set[str]:
    published_ids: set[str] = set()
    for output_dir in output_dirs:
        for path in sorted(output_dir.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            if not isinstance(data, list):
                continue
            for job in data:
                if not isinstance(job, dict) or job.get("source") != "JobG8":
                    continue
                job_id = _text(job.get("job_id"))
                if job_id:
                    published_ids.add(job_id)
    return published_ids


def load_feed_date(coverage_path: Path) -> str:
    with coverage_path.open("r", encoding="utf-8-sig", newline="") as handle:
        dates = {(row.get("feed_date") or "").strip() for row in csv.DictReader(handle)}
    if len(dates) != 1 or not next(iter(dates)):
        raise RuntimeError(f"Expected exactly one feed date in {coverage_path}, found {dates}")
    return dates.pop()


def build_profile(
    input_path: Path,
    output_path: Path,
    coverage_path: Path,
    output_dirs: list[Path],
) -> None:
    feed = pd.read_excel(input_path, dtype=object)
    missing = {ID_COLUMN, CATEGORY_COLUMN} - set(feed.columns)
    if missing:
        raise RuntimeError(f"JobG8 input is missing required columns: {sorted(missing)}")

    feed_date = load_feed_date(coverage_path)
    categories_by_id: dict[str, str] = {}
    supplied_counts: Counter[str] = Counter()
    for _, row in feed.iterrows():
        job_id = _text(row.get(ID_COLUMN))
        category = _text(row.get(CATEGORY_COLUMN)) or "(blank)"
        supplied_counts[category] += 1
        if job_id:
            categories_by_id[job_id] = category

    published_ids = load_published_jobg8_ids(output_dirs)
    published_counts = Counter(
        categories_by_id.get(job_id, "Published JobG8 ID absent from current feed")
        for job_id in published_ids
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "feed_date",
                "total_jobs",
                "published_jobg8_jobs",
                "jobg8_category",
                "count",
                "published_count",
            ],
        )
        writer.writeheader()
        categories = set(supplied_counts) | set(published_counts)
        for category in sorted(
            categories,
            key=lambda item: (-supplied_counts.get(item, 0), item.casefold()),
        ):
            writer.writerow(
                {
                    "feed_date": feed_date,
                    "total_jobs": len(feed),
                    "published_jobg8_jobs": len(published_ids),
                    "jobg8_category": category,
                    "count": supplied_counts.get(category, 0),
                    "published_count": published_counts.get(category, 0),
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--coverage", required=True, type=Path)
    parser.add_argument("--published-output-dir", required=True, action="append", type=Path)
    args = parser.parse_args()
    build_profile(args.input, args.output, args.coverage, args.published_output_dir)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
