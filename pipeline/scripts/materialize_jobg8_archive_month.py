from __future__ import annotations

import argparse
import calendar
from datetime import date, datetime
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo


_MONTH_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
_EXCEL_SUFFIXES = {".xlsx", ".xls", ".xlsm"}


def month_bounds(month: str) -> tuple[date, date]:
    if not _MONTH_RE.fullmatch(month):
        raise ValueError(f"Invalid month '{month}'; expected YYYY-MM")
    year, month_number = (int(part) for part in month.split("-"))
    last_day = calendar.monthrange(year, month_number)[1]
    return date(year, month_number, 1), date(year, month_number, last_day)


def expected_s3_days(month: str, s3_start_date: date, today: date) -> list[date]:
    month_start, month_end = month_bounds(month)
    start = max(month_start, s3_start_date)
    end = min(month_end, today)
    if start > end:
        return []
    return [date.fromordinal(value) for value in range(start.toordinal(), end.toordinal() + 1)]


def copy_legacy_excel(legacy_dir: Path, output_dir: Path) -> int:
    if not legacy_dir.is_dir():
        return 0

    copied = 0
    for source in sorted(legacy_dir.iterdir()):
        if not source.is_file() or source.suffix.lower() not in _EXCEL_SUFFIXES:
            continue
        shutil.copy2(source, output_dir / source.name)
        copied += 1
    return copied


def materialize_s3_days(
    *,
    client,
    bucket: str,
    prefix: str,
    days: list[date],
    output_dir: Path,
    adapter_path: Path,
    expected_min: int,
    expected_max: int,
) -> int:
    clean_prefix = prefix.strip("/")
    count = 0

    with tempfile.TemporaryDirectory(prefix="jobg8-s3-zips-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        for archive_day in days:
            filename = f"{archive_day.isoformat()}.zip"
            key = f"{clean_prefix}/{filename}" if clean_prefix else filename
            local_zip = temp_dir / filename
            target_xlsx = output_dir / f"{archive_day.isoformat()}.xlsx"

            try:
                client.download_file(bucket, key, str(local_zip))
            except Exception as exc:
                raise SystemExit(
                    f"Expected JobG8 archive object could not be downloaded: "
                    f"s3://{bucket}/{key}: {exc}"
                ) from exc

            subprocess.run(
                [
                    sys.executable,
                    str(adapter_path),
                    "--zip",
                    str(local_zip),
                    "--output",
                    str(target_xlsx),
                    "--expected-min",
                    str(expected_min),
                    "--expected-max",
                    str(expected_max),
                ],
                check=True,
            )
            count += 1

    return count


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a temporary monthly JobG8 Excel archive from legacy repo files "
            "plus the private S3 daily raw ZIP archive."
        )
    )
    parser.add_argument("--month", required=True)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--legacy-dir", type=Path)
    parser.add_argument("--prefix", default="jobg8/raw")
    parser.add_argument("--s3-start-date", default="2026-08-14")
    parser.add_argument("--adapter", type=Path, default=Path("pipeline/scripts/jobg8_xml_adapter.py"))
    parser.add_argument("--expected-min", type=int, default=5000)
    parser.add_argument("--expected-max", type=int, default=20000)
    args = parser.parse_args()

    month_bounds(args.month)
    s3_start_date = date.fromisoformat(args.s3_start_date)
    today = datetime.now(ZoneInfo("Europe/London")).date()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for existing in args.output_dir.iterdir():
        if existing.is_file():
            existing.unlink()
        elif existing.is_dir():
            shutil.rmtree(existing)

    legacy_count = 0
    if args.legacy_dir is not None:
        legacy_count = copy_legacy_excel(args.legacy_dir, args.output_dir)

    days = expected_s3_days(args.month, s3_start_date, today)
    s3_count = 0
    if days:
        try:
            import boto3
        except ImportError as exc:
            raise SystemExit("boto3 is required to materialize the JobG8 S3 archive") from exc

        client = boto3.client("s3", region_name=args.region)
        s3_count = materialize_s3_days(
            client=client,
            bucket=args.bucket,
            prefix=args.prefix,
            days=days,
            output_dir=args.output_dir,
            adapter_path=args.adapter,
            expected_min=args.expected_min,
            expected_max=args.expected_max,
        )

    excel_files = sorted(
        path for path in args.output_dir.iterdir()
        if path.is_file() and path.suffix.lower() in _EXCEL_SUFFIXES
    )
    if not excel_files:
        raise SystemExit(
            f"No JobG8 Excel files materialized for {args.month}; "
            "neither legacy repo input nor S3 archive supplied data"
        )

    print(f"Materialized JobG8 month: {args.month}")
    print(f"Legacy Excel files copied: {legacy_count}")
    print(f"S3 daily ZIPs converted: {s3_count}")
    print(f"Final daily Excel files available: {len(excel_files)}")
    print(f"Temporary compiler input: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
