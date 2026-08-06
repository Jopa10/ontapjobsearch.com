"""Route a verified Teaching Vacancies manifest through Ontap geography.

This is a non-publishing stage. It verifies the source-wide discovery evidence,
uses ``geo_lookup.xlsx`` for factual routing, records unresolved geography, and
attaches the existing LIVE/CANDIDATE slice authority. It performs no occupational
classification, approval, composition or page publishing.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
from typing import Iterable

from external_sources import teaching_vacancies_discovery as discovery
from external_sources.regional_contracts import (
    CATEGORY_ADMIN_SERVICE,
    SliceAuthority,
    clean,
    load_geo_lookup,
    load_slice_authorities,
    route_geography,
    slice_authority,
)

ROUTING_CONTRACT_VERSION = "teaching-vacancies-routing-v1"
ROUTING_FIELDS = discovery.MANIFEST_FIELDS + (
    "geo_cluster",
    "ontap_region",
    "geography_status",
    "geography_reason",
    "geography_lookup_key",
    "slice_category",
    "slice_status",
    "publish_eligible",
)

REQUIRED_FACTUAL_FIELDS = (
    "source_job_id",
    "canonical_url",
    "title",
    "employer",
    "location",
    "closing_date",
    "factual_fingerprint",
)


def load_discovery_summary(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise ValueError(f"discovery summary not found: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"discovery summary is not valid JSON: {path}") from exc
    if not isinstance(value, dict):
        raise ValueError("discovery summary must be a JSON object")
    if clean(value.get("source")) != discovery.SOURCE_CODE:
        raise ValueError("discovery summary has an unexpected source")
    if not clean(value.get("run_date")):
        raise ValueError("discovery summary has no run_date")
    if not clean(value.get("manifest_sha256")):
        raise ValueError("discovery summary has no manifest_sha256")
    return value


def _verified_manifest_bytes(
    manifest_path: Path,
    summary: dict[str, object],
) -> bytes:
    if not manifest_path.is_file():
        raise ValueError(f"discovery manifest not found: {manifest_path}")
    content = manifest_path.read_bytes()
    actual = hashlib.sha256(content).hexdigest()
    expected = clean(summary.get("manifest_sha256"))
    if actual != expected:
        raise ValueError(
            "Teaching Vacancies manifest SHA256 does not match its discovery summary"
        )
    return content


def load_verified_manifest(
    manifest_path: Path,
    summary_path: Path,
) -> tuple[list[dict[str, str]], dict[str, object]]:
    summary = load_discovery_summary(summary_path)
    content = _verified_manifest_bytes(manifest_path, summary)
    with io.StringIO(content.decode("utf-8-sig"), newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != discovery.MANIFEST_FIELDS:
            raise ValueError(
                "Teaching Vacancies manifest columns do not match the factual contract"
            )
        rows = [dict(row) for row in reader]
    if not rows:
        raise ValueError("Teaching Vacancies manifest contains no factual records")
    declared_records = int(summary.get("records") or 0)
    if declared_records != len(rows):
        raise ValueError(
            f"manifest record count {len(rows)} does not match summary {declared_records}"
        )

    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    for row_number, row in enumerate(rows, start=2):
        if clean(row.get("source")) != discovery.SOURCE_CODE:
            raise ValueError(f"manifest row {row_number} has an unexpected source")
        if clean(row.get("detail_fetch_status")) != "OK":
            raise ValueError(f"manifest row {row_number} has no successful detail audit")
        missing = [field for field in REQUIRED_FACTUAL_FIELDS if not clean(row.get(field))]
        if missing:
            raise ValueError(
                f"manifest row {row_number} is missing factual fields: "
                + ", ".join(missing)
            )
        source_job_id = clean(row["source_job_id"])
        canonical_url = clean(row["canonical_url"]).rstrip("/")
        if source_job_id.casefold() in seen_ids:
            raise ValueError(f"duplicate source_job_id in manifest: {source_job_id}")
        if canonical_url.casefold() in seen_urls:
            raise ValueError(f"duplicate canonical_url in manifest: {canonical_url}")
        seen_ids.add(source_job_id.casefold())
        seen_urls.add(canonical_url.casefold())
    return rows, summary


def route_manifest_rows(
    rows: Iterable[dict[str, str]],
    *,
    geo_lookup: dict[str, str],
    authorities: dict[tuple[str, str], SliceAuthority],
    category: str = CATEGORY_ADMIN_SERVICE,
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for source_row in rows:
        row = {field: clean(source_row.get(field)) for field in discovery.MANIFEST_FIELDS}
        geography = route_geography(
            location=row["location"],
            postcode=row["postcode"],
            lookup=geo_lookup,
        )
        authority = (
            slice_authority(
                authorities,
                region=geography.region,
                category=category,
            )
            if geography.status == "ROUTED"
            else None
        )
        slice_status = authority.status if authority else "UNREGISTERED"
        publish_eligible = bool(
            geography.status == "ROUTED"
            and authority
            and authority.may_publish
        )
        row.update(
            {
                "geo_cluster": geography.cluster,
                "ontap_region": geography.region,
                "geography_status": geography.status,
                "geography_reason": geography.evidence,
                "geography_lookup_key": geography.lookup_key,
                "slice_category": category,
                "slice_status": slice_status,
                "publish_eligible": "YES" if publish_eligible else "NO",
            }
        )
        output.append(row)
    return sorted(
        output,
        key=lambda row: (
            row["geography_status"] != "ROUTED",
            row["ontap_region"].casefold(),
            row["title"].casefold(),
            row["source_job_id"],
        ),
    )


def csv_content(rows: Iterable[dict[str, str]]) -> bytes:
    handle = io.StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=ROUTING_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue().encode("utf-8")


def routing_summary(
    rows: list[dict[str, str]],
    *,
    discovery_summary: dict[str, object],
    routed_sha256: str,
    unresolved_sha256: str,
) -> dict[str, object]:
    regions = Counter(
        row["ontap_region"]
        for row in rows
        if row["geography_status"] == "ROUTED"
    )
    slice_statuses = Counter(row["slice_status"] for row in rows)
    return {
        "contract_version": ROUTING_CONTRACT_VERSION,
        "source": discovery.SOURCE_CODE,
        "run_date": clean(discovery_summary.get("run_date")),
        "discovery_manifest_sha256": clean(
            discovery_summary.get("manifest_sha256")
        ),
        "records": len(rows),
        "routed": sum(row["geography_status"] == "ROUTED" for row in rows),
        "unresolved": sum(row["geography_status"] == "UNRESOLVED" for row in rows),
        "publish_eligible_live": sum(row["publish_eligible"] == "YES" for row in rows),
        "candidate_or_unregistered": sum(
            row["slice_status"] != "LIVE" for row in rows
        ),
        "region_counts": dict(sorted(regions.items())),
        "slice_status_counts": dict(sorted(slice_statuses.items())),
        "routed_csv_sha256": routed_sha256,
        "unresolved_csv_sha256": unresolved_sha256,
    }


def default_output_paths(run_date: str) -> tuple[Path, Path, Path]:
    root = Path("manifests/external/teaching-vacancies")
    return (
        root / f"teaching-vacancies-routed-{run_date}.csv",
        root / f"teaching-vacancies-unresolved-{run_date}.csv",
        root / f"teaching-vacancies-routing-{run_date}-summary.json",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-csv", type=Path, required=True)
    parser.add_argument("--discovery-summary-json", type=Path, required=True)
    parser.add_argument(
        "--geo-lookup",
        type=Path,
        default=Path("geo/geo_lookup.xlsx"),
    )
    parser.add_argument(
        "--slice-register",
        type=Path,
        default=Path("registers/region_category_slice_register.csv"),
    )
    parser.add_argument("--routed-csv", type=Path)
    parser.add_argument("--unresolved-csv", type=Path)
    parser.add_argument("--routing-summary-json", type=Path)
    parser.add_argument("--write-routing", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.write_routing:
        raise SystemExit(
            "STOP: add --write-routing to create non-publishing routing evidence."
        )
    source_rows, discovery_summary = load_verified_manifest(
        args.manifest_csv,
        args.discovery_summary_json,
    )
    lookup = load_geo_lookup(args.geo_lookup)
    authorities = load_slice_authorities(args.slice_register)
    rows = route_manifest_rows(
        source_rows,
        geo_lookup=lookup,
        authorities=authorities,
    )
    run_date = clean(discovery_summary.get("run_date"))
    routed_path, unresolved_path, summary_path = default_output_paths(run_date)
    if args.routed_csv:
        routed_path = args.routed_csv
    if args.unresolved_csv:
        unresolved_path = args.unresolved_csv
    if args.routing_summary_json:
        summary_path = args.routing_summary_json

    unresolved_rows = [
        row for row in rows if row["geography_status"] == "UNRESOLVED"
    ]
    routed_bytes = csv_content(rows)
    unresolved_bytes = csv_content(unresolved_rows)
    summary = routing_summary(
        rows,
        discovery_summary=discovery_summary,
        routed_sha256=hashlib.sha256(routed_bytes).hexdigest(),
        unresolved_sha256=hashlib.sha256(unresolved_bytes).hexdigest(),
    )

    discovery.write_bytes_atomic(routed_path, routed_bytes)
    discovery.write_bytes_atomic(unresolved_path, unresolved_bytes)
    discovery.write_bytes_atomic(
        summary_path,
        (json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )
    print(
        f"Teaching Vacancies routing wrote {summary['routed']} routed and "
        f"{summary['unresolved']} unresolved records; no jobs were published."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
