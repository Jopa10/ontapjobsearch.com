#!/usr/bin/env python3
"""Count jobs in final published app JSON and maintain private daily reports."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from zoneinfo import ZoneInfo


BASE_HISTORY_FIELDS = [
    "report_date",
    "total_live_jobs",
    "jobg8_jobs",
    "external_jobs",
]

SOURCE_ALIASES = {
    "jobg8": "JobG8",
    "jobg8com": "JobG8",
    "nejobs": "NEJobs",
    "northeastjobs": "NEJobs",
    "northeastjobsorguk": "NEJobs",
    "vonne": "VONNE",
    "vonnejobs": "VONNE",
}


@dataclass(frozen=True)
class LiveJob:
    job_id: str
    title: str
    location: str
    region: str
    category: str
    source: str
    apply_url: str
    source_file: str


@dataclass(frozen=True)
class CountResult:
    report_date: str
    total_live_jobs: int
    jobg8_jobs: int
    external_jobs: int
    source_counts: dict[str, int]
    region_category_counts: dict[tuple[str, str, str], int]
    job_json_files: int
    duplicate_rows_ignored: int
    daily_report_path: Path
    history_path: Path


def _text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def canonical_source(value: object) -> str:
    raw = _text(value)
    if not raw:
        return "Unknown"
    alias_key = re.sub(r"[^a-z0-9]+", "", raw.lower())
    return SOURCE_ALIASES.get(alias_key, raw)


def _normalise_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def _canonical_apply_url(value: str) -> str:
    """Remove fragments and common click-tracking parameters for duplicate checks."""
    try:
        parts = urlsplit(value.strip())
    except ValueError:
        return value.strip()

    ignored_keys = {"gclid", "fbclid", "msclkid"}
    query = [
        (key, val)
        for key, val in parse_qsl(parts.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in ignored_keys
    ]
    return urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            parts.path.rstrip("/") or "/",
            urlencode(sorted(query)),
            "",
        )
    )


def _row_is_live(
    row: dict[str, object],
    *,
    as_of: date,
    now: datetime | None = None,
) -> bool:
    """Filter rows only when a provider supplied a parseable closing deadline.

    JobG8 rows commonly have no closing date, so missing or malformed deadlines
    remain countable rather than being guessed expired. For today's report an
    explicit closing time is respected; historical reports use the calendar day.
    """
    deadline_text = _text(row.get("closing_datetime"))
    if deadline_text:
        try:
            deadline = datetime.fromisoformat(deadline_text)
        except ValueError:
            return True
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=ZoneInfo("Europe/London"))
        london_deadline = deadline.astimezone(ZoneInfo("Europe/London"))
        if london_deadline.date() < as_of:
            return False
        if london_deadline.date() > as_of:
            return True
        if now is None:
            return True
        current = now
        if current.tzinfo is None:
            current = current.replace(tzinfo=ZoneInfo("Europe/London"))
        return london_deadline >= current.astimezone(ZoneInfo("Europe/London"))

    closing_text = _text(row.get("closing_date"))
    if not closing_text:
        return True
    try:
        closing_day = date.fromisoformat(closing_text)
    except ValueError:
        return True
    return closing_day >= as_of


def _iter_job_rows(app_dir: Path) -> Iterable[tuple[Path, dict[str, object]]]:
    for json_path in sorted(app_dir.rglob("*.json")):
        try:
            parsed = json.loads(json_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(parsed, list):
            continue
        for row in parsed:
            if not isinstance(row, dict):
                continue
            if not (
                _text(row.get("job_id"))
                and _text(row.get("title"))
                and _text(row.get("apply_url"))
            ):
                continue
            yield json_path, row


def collect_live_jobs(
    app_dir: Path,
    *,
    as_of: date | None = None,
    now: datetime | None = None,
) -> tuple[list[LiveJob], int, int]:
    """Return unique live jobs, job JSON file count and ignored duplicate row count."""
    if not app_dir.is_dir():
        raise FileNotFoundError(f"Published app directory not found: {app_dir}")

    jobs: list[LiveJob] = []
    seen_ids: dict[str, LiveJob] = {}
    seen_fingerprints: dict[tuple[str, str, str], LiveJob] = {}
    job_files: set[Path] = set()
    duplicate_rows_ignored = 0

    for json_path, row in _iter_job_rows(app_dir):
        job_files.add(json_path)
        if as_of is not None and not _row_is_live(row, as_of=as_of, now=now):
            continue
        job = LiveJob(
            job_id=_text(row.get("job_id")),
            title=_text(row.get("title")),
            location=_text(row.get("location")) or "Unspecified",
            region=_text(row.get("region")) or "Unspecified",
            category=_text(row.get("category")) or "Unspecified",
            source=canonical_source(row.get("source")),
            apply_url=_text(row.get("apply_url")),
            source_file=json_path.relative_to(app_dir.parent).as_posix(),
        )

        existing = seen_ids.get(job.job_id)
        if existing:
            if existing.source != job.source:
                raise ValueError(
                    f"Conflicting sources for job_id {job.job_id!r}: "
                    f"{existing.source!r} in {existing.source_file} and "
                    f"{job.source!r} in {job.source_file}"
                )
            duplicate_rows_ignored += 1
            continue

        fingerprint = (
            _canonical_apply_url(job.apply_url),
            _normalise_text(job.title),
            _normalise_text(job.location),
        )
        existing = seen_fingerprints.get(fingerprint)
        if existing:
            if existing.source != job.source:
                raise ValueError(
                    "Conflicting sources for duplicate vacancy fingerprint: "
                    f"{existing.source!r} in {existing.source_file} and "
                    f"{job.source!r} in {job.source_file}"
                )
            duplicate_rows_ignored += 1
            continue

        seen_ids[job.job_id] = job
        seen_fingerprints[fingerprint] = job
        jobs.append(job)

    return jobs, len(job_files), duplicate_rows_ignored


def _provider_field(source: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", source.lower()).strip("_") or "unknown"
    return f"{slug}_jobs"


def _write_daily_report(
    report_path: Path,
    report_date: str,
    total: int,
    jobg8: int,
    external: int,
    source_counts: Counter[str],
    region_category_counts: Counter[tuple[str, str, str]],
) -> None:
    rows: list[dict[str, object]] = [
        {
            "report_date": report_date,
            "level": "total",
            "source": "All",
            "region": "",
            "category": "",
            "count": total,
        },
        {
            "report_date": report_date,
            "level": "source_summary",
            "source": "JobG8",
            "region": "",
            "category": "",
            "count": jobg8,
        },
        {
            "report_date": report_date,
            "level": "source_summary",
            "source": "External",
            "region": "",
            "category": "",
            "count": external,
        },
    ]

    for source, count in sorted(source_counts.items(), key=lambda item: item[0].casefold()):
        rows.append(
            {
                "report_date": report_date,
                "level": "provider",
                "source": source,
                "region": "",
                "category": "",
                "count": count,
            }
        )

    for (source, region, category), count in sorted(
        region_category_counts.items(),
        key=lambda item: tuple(part.casefold() for part in item[0]),
    ):
        rows.append(
            {
                "report_date": report_date,
                "level": "region_category",
                "source": source,
                "region": region,
                "category": category,
                "count": count,
            }
        )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["report_date", "level", "source", "region", "category", "count"],
        )
        writer.writeheader()
        writer.writerows(rows)


def _read_history(history_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not history_path.exists():
        return BASE_HISTORY_FIELDS.copy(), []
    with history_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return BASE_HISTORY_FIELDS.copy(), []
        return list(reader.fieldnames), [dict(row) for row in reader]


def _write_history(
    history_path: Path,
    report_date: str,
    total: int,
    jobg8: int,
    external: int,
    source_counts: Counter[str],
) -> None:
    old_fields, old_rows = _read_history(history_path)
    provider_fields = {
        _provider_field(source) for source in source_counts if source != "JobG8"
    }
    existing_provider_fields = {
        field for field in old_fields if field not in BASE_HISTORY_FIELDS
    }
    fields = BASE_HISTORY_FIELDS + sorted(existing_provider_fields | provider_fields)

    new_row = {field: "0" for field in fields}
    new_row.update(
        {
            "report_date": report_date,
            "total_live_jobs": str(total),
            "jobg8_jobs": str(jobg8),
            "external_jobs": str(external),
        }
    )
    for source, count in source_counts.items():
        if source != "JobG8":
            new_row[_provider_field(source)] = str(count)

    by_date: dict[str, dict[str, str]] = {}
    for row in old_rows:
        row_date = (row.get("report_date") or "").strip()
        if not row_date:
            continue
        normalised = {field: (row.get(field) or "0") for field in fields}
        normalised["report_date"] = row_date
        by_date[row_date] = normalised
    by_date[report_date] = new_row

    history_path.parent.mkdir(parents=True, exist_ok=True)
    with history_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row_date in sorted(by_date):
            writer.writerow(by_date[row_date])


def build_reports(app_dir: Path, reports_dir: Path, report_date: str) -> CountResult:
    try:
        report_day = date.fromisoformat(report_date)
    except ValueError as exc:
        raise ValueError(f"Report date must be YYYY-MM-DD: {report_date!r}") from exc

    london_now = datetime.now(ZoneInfo("Europe/London"))
    report_now = london_now if report_day == london_now.date() else None
    jobs, job_file_count, duplicate_rows_ignored = collect_live_jobs(
        app_dir,
        as_of=report_day,
        now=report_now,
    )
    source_counts: Counter[str] = Counter(job.source for job in jobs)
    region_category_counts: Counter[tuple[str, str, str]] = Counter(
        (job.source, job.region, job.category) for job in jobs
    )
    total = len(jobs)
    jobg8 = source_counts.get("JobG8", 0)
    external = total - jobg8

    report_path = reports_dir / f"live-job-source-count-{report_date}.csv"
    history_path = reports_dir / "live-job-source-history.csv"
    _write_daily_report(
        report_path,
        report_date,
        total,
        jobg8,
        external,
        source_counts,
        region_category_counts,
    )
    _write_history(history_path, report_date, total, jobg8, external, source_counts)

    return CountResult(
        report_date=report_date,
        total_live_jobs=total,
        jobg8_jobs=jobg8,
        external_jobs=external,
        source_counts=dict(source_counts),
        region_category_counts=dict(region_category_counts),
        job_json_files=job_file_count,
        duplicate_rows_ignored=duplicate_rows_ignored,
        daily_report_path=report_path,
        history_path=history_path,
    )


def _default_report_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Count final live jobs from published app JSON files."
    )
    parser.add_argument("--app-dir", type=Path, default=Path("app"))
    parser.add_argument(
        "--reports-dir", type=Path, default=Path("pipeline/reports-daily")
    )
    parser.add_argument("--date", default=_default_report_date())
    args = parser.parse_args()

    result = build_reports(args.app_dir, args.reports_dir, args.date)
    print(f"## Live job source count — {result.report_date}")
    print()
    print(f"- Final published job JSON files: {result.job_json_files}")
    print(f"- Total live jobs: {result.total_live_jobs}")
    print(f"- JobG8 jobs: {result.jobg8_jobs}")
    print(f"- Externally sourced jobs: {result.external_jobs}")
    for source, count in sorted(result.source_counts.items()):
        if source != "JobG8":
            print(f"- {source} jobs: {count}")
    print(f"- Duplicate published rows ignored: {result.duplicate_rows_ignored}")
    print(f"- Daily CSV: `{result.daily_report_path.as_posix()}`")
    print(f"- Rolling history: `{result.history_path.as_posix()}`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
