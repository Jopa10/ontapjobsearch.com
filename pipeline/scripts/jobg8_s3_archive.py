from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from pathlib import Path
import re
from zoneinfo import ZoneInfo


_DATE_FILE_RE = re.compile(r"^(?P<day>\d{4}-\d{2}-\d{2})\.zip$")


def canonical_key(prefix: str, archive_date: date) -> str:
    clean_prefix = prefix.strip("/")
    name = f"{archive_date.isoformat()}.zip"
    return f"{clean_prefix}/{name}" if clean_prefix else name


def retention_cutoff(archive_date: date, keep_days: int) -> date:
    if keep_days < 1:
        raise ValueError("keep_days must be at least 1")
    # Including archive_date itself, keep exactly keep_days calendar dates.
    return archive_date - timedelta(days=keep_days - 1)


def dated_key_day(key: str, prefix: str) -> date | None:
    clean_prefix = prefix.strip("/")
    expected_prefix = f"{clean_prefix}/" if clean_prefix else ""
    if not key.startswith(expected_prefix):
        return None

    relative = key[len(expected_prefix) :]
    if "/" in relative:
        return None

    match = _DATE_FILE_RE.fullmatch(relative)
    if not match:
        return None

    try:
        return date.fromisoformat(match.group("day"))
    except ValueError:
        return None


def archive_and_prune(
    *,
    zip_path: Path,
    bucket: str,
    region: str,
    prefix: str,
    archive_date: date,
    keep_days: int,
    endpoint_url: str | None = None,
    prune: bool = True,
) -> tuple[str, list[str]]:
    if not zip_path.is_file() or zip_path.stat().st_size <= 0:
        raise SystemExit(f"Archive source is missing or empty: {zip_path}")
    if not bucket.strip():
        raise SystemExit("Archive bucket is empty")
    if not region.strip():
        raise SystemExit("Archive region is empty")

    try:
        import boto3
    except ImportError as exc:
        raise SystemExit("boto3 is required for JobG8 S3 archiving") from exc

    client_kwargs: dict[str, str] = {"region_name": region}
    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url
    client = boto3.client("s3", **client_kwargs)

    key = canonical_key(prefix, archive_date)
    source_size = zip_path.stat().st_size

    client.upload_file(
        str(zip_path),
        bucket,
        key,
        ExtraArgs={
            "ContentType": "application/zip",
            "ServerSideEncryption": "AES256",
        },
    )

    head = client.head_object(Bucket=bucket, Key=key)
    uploaded_size = int(head.get("ContentLength", -1))
    if uploaded_size != source_size:
        raise SystemExit(
            f"Archive verification failed for s3://{bucket}/{key}: "
            f"source={source_size} bytes, stored={uploaded_size} bytes"
        )

    deleted: list[str] = []
    if prune:
        cutoff = retention_cutoff(archive_date, keep_days)
        paginator = client.get_paginator("list_objects_v2")
        list_prefix = f"{prefix.strip('/')}/" if prefix.strip("/") else ""
        for page in paginator.paginate(Bucket=bucket, Prefix=list_prefix):
            for item in page.get("Contents", []):
                old_key = str(item.get("Key", ""))
                old_day = dated_key_day(old_key, prefix)
                if old_day is not None and old_day < cutoff:
                    client.delete_object(Bucket=bucket, Key=old_key)
                    deleted.append(old_key)

    return key, deleted


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Store one canonical JobG8 raw ZIP per day in private S3-compatible storage."
    )
    parser.add_argument("--zip", dest="zip_path", required=True, type=Path)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--prefix", default="jobg8/raw")
    parser.add_argument("--keep-days", type=int, default=90)
    parser.add_argument(
        "--skip-prune",
        action="store_true",
        help="Upload and verify only; let the S3 bucket lifecycle rule expire old objects.",
    )
    parser.add_argument("--date", dest="archive_date")
    parser.add_argument("--endpoint-url")
    args = parser.parse_args()

    if args.archive_date:
        archive_date = date.fromisoformat(args.archive_date)
    else:
        archive_date = datetime.now(ZoneInfo("Europe/London")).date()

    key, deleted = archive_and_prune(
        zip_path=args.zip_path,
        bucket=args.bucket,
        region=args.region,
        prefix=args.prefix,
        archive_date=archive_date,
        keep_days=args.keep_days,
        endpoint_url=args.endpoint_url or None,
        prune=not args.skip_prune,
    )

    print(f"Archived validated JobG8 raw feed: s3://{args.bucket}/{key}")
    if args.skip_prune:
        print("Retention: managed by the S3 bucket lifecycle rule")
    else:
        print(f"Retention: one canonical object per day, {args.keep_days} calendar days")
        if deleted:
            print(f"Deleted {len(deleted)} expired raw archive object(s)")
            for old_key in deleted:
                print(f"- {old_key}")
        else:
            print("Deleted 0 expired raw archive objects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
