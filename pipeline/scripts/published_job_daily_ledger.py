#!/usr/bin/env python3
"""Record jobs first published by Ontap, with a source-labelled daily CSV."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

from scripts.live_job_source_counter import LiveJob, collect_live_jobs


FIELDS = [
    "first_seen_date",
    "tracking_kind",
    "source",
    "job_id",
    "title",
    "location",
    "region",
    "category",
    "ontap_url",
    "apply_url",
]


class LedgerError(RuntimeError):
    pass


def _read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return []
        missing = [field for field in FIELDS if field not in reader.fieldnames]
        if missing:
            raise LedgerError(
                f"Published-job first-seen history is missing columns: {', '.join(missing)}"
            )
        return [
            {field: (row.get(field) or "").strip() for field in FIELDS}
            for row in reader
            if (row.get("job_id") or "").strip()
        ]


def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _row(job: LiveJob, report_date: str, tracking_kind: str) -> dict[str, str]:
    return {
        "first_seen_date": report_date,
        "tracking_kind": tracking_kind,
        "source": job.source,
        "job_id": job.job_id,
        "title": job.title,
        "location": job.location,
        "region": job.region,
        "category": job.category,
        "ontap_url": f"https://www.ontapjobsearch.com/jobs/{quote(job.job_id, safe='')}",
        "apply_url": job.apply_url,
    }


def update_ledger(
    app_dir: Path,
    reports_dir: Path,
    report_date: str,
) -> tuple[Path, Path, bool, list[dict[str, str]]]:
    try:
        report_day = date.fromisoformat(report_date)
    except ValueError as exc:
        raise LedgerError(f"Report date must be YYYY-MM-DD: {report_date!r}") from exc

    london_now = datetime.now(ZoneInfo("Europe/London"))
    report_now = london_now if report_day == london_now.date() else None
    jobs, _, _ = collect_live_jobs(app_dir, as_of=report_day, now=report_now)

    history_path = reports_dir / "published-job-first-seen-history.csv"
    daily_path = reports_dir / f"newly-published-jobs-{report_date}.csv"
    baseline_initialized = not history_path.exists()
    rows = _read_rows(history_path)
    known = {row["job_id"]: row for row in rows}
    tracking_kind = "baseline_existing" if baseline_initialized else "newly_published"

    for job in sorted(
        jobs,
        key=lambda item: (item.source.casefold(), item.title.casefold(), item.job_id),
    ):
        previous = known.get(job.job_id)
        if previous:
            if previous["source"] and previous["source"] != job.source:
                raise LedgerError(
                    f"Historical source conflict for job_id {job.job_id!r}: "
                    f"{previous['source']!r} vs {job.source!r}"
                )
            continue
        item = _row(job, report_date, tracking_kind)
        rows.append(item)
        known[job.job_id] = item

    rows.sort(
        key=lambda item: (
            item["first_seen_date"],
            item["source"].casefold(),
            item["title"].casefold(),
            item["job_id"],
        )
    )
    _write_rows(history_path, rows)

    daily_rows = [
        item
        for item in rows
        if item["first_seen_date"] == report_date
        and item["tracking_kind"] == "newly_published"
    ]
    daily_rows.sort(
        key=lambda item: (
            item["source"].casefold(),
            item["title"].casefold(),
            item["job_id"],
        )
    )
    _write_rows(daily_path, daily_rows)
    return history_path, daily_path, baseline_initialized, daily_rows


def _default_report_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Maintain Ontap's first-published job ledger and daily new-job list."
    )
    parser.add_argument("--app-dir", type=Path, default=Path("app"))
    parser.add_argument(
        "--reports-dir", type=Path, default=Path("pipeline/reports-daily")
    )
    parser.add_argument("--date", default=_default_report_date())
    args = parser.parse_args()

    history_path, daily_path, baseline_initialized, daily_rows = update_ledger(
        args.app_dir,
        args.reports_dir,
        args.date,
    )

    print(f"## Newly published job ledger — {args.date}")
    print()
    if baseline_initialized:
        print("- Baseline established from jobs already live on Ontap; none are labelled new.")
    else:
        counts = Counter(row["source"] for row in daily_rows)
        print(f"- Newly published jobs: {len(daily_rows)}")
        for source, count in sorted(counts.items()):
            print(f"  - {source}: {count}")
    print(f"- Daily job list: `{daily_path.as_posix()}`")
    print(f"- Permanent first-seen history: `{history_path.as_posix()}`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
