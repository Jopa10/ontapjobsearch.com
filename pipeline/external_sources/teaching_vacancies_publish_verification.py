"""Verify England-wide Teaching Vacancies composition with regional isolation.

Up to a configured number of missing regional inputs may retain their previous
live pages without preventing clean regions from publishing. Data-integrity
failures remain fail-closed.
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

from external_sources.compose_northeast_admin import load_rows, text
from external_sources.compose_teaching_vacancies_regional import (
    ADMIN_SERVICE_OUTPUT_GLOB,
    canonical_rows,
    compose_rows,
    current_base_contract,
    load_approved_snapshot,
)
from external_sources.teaching_vacancies_master_review import REVIEW_NOW
from external_sources.teaching_vacancies_regional_review import region_slug

DEFAULT_MASTER_REVIEW = Path(
    "reviews/external/teaching-vacancies/england-wide-admin-service-review.csv"
)
DEFAULT_CURRENT_OUTPUT_DIR = Path("output-admin-service")
DEFAULT_SNAPSHOT_DIR = Path("output-external/teaching-vacancies-regional")
DEFAULT_EVIDENCE_DIR = Path("manifests/external/teaching-vacancies/approved")
REPORT_CONTRACT_VERSION = "teaching-vacancies-publish-verification-v1"


class PublishIntegrityError(ValueError):
    """A corruption or ambiguity for which partial publication is unsafe."""


@dataclass(frozen=True)
class RegionVerification:
    region: str
    status: str
    reason: str
    output_path: str = ""
    base_rows: int = 0
    teaching_rows: int = 0
    expired_skipped: int = 0
    duplicate_skipped: int = 0
    total: int = 0


@dataclass(frozen=True)
class PublishVerification:
    regions: tuple[RegionVerification, ...]
    max_isolated_regions: int

    @property
    def isolated_regions(self) -> tuple[str, ...]:
        return tuple(row.region for row in self.regions if row.status == "ISOLATED")

    def as_json(self) -> dict[str, object]:
        return {
            "contract_version": REPORT_CONTRACT_VERSION,
            "max_isolated_regions": self.max_isolated_regions,
            "isolated_regions": list(self.isolated_regions),
            "regions": [asdict(row) for row in self.regions],
        }


def live_review_regions(master_review: Path) -> list[str]:
    if not master_review.is_file():
        raise PublishIntegrityError(f"master review does not exist: {master_review}")
    with master_review.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    regions = sorted(
        {
            text(row.get("ontap_region"))
            for row in rows
            if row.get("review_scope") == REVIEW_NOW
            and text(row.get("ontap_region"))
        },
        key=str.casefold,
    )
    if not regions:
        raise PublishIntegrityError("England-wide review contains no LIVE regions")
    return regions


def _current_outputs_by_region(
    current_output_dir: Path,
) -> dict[str, tuple[Path, list[dict]]]:
    if not current_output_dir.is_dir():
        raise PublishIntegrityError(
            f"current output directory does not exist: {current_output_dir}"
        )
    indexed: dict[str, tuple[Path, list[dict]]] = {}
    for path in sorted(current_output_dir.glob(ADMIN_SERVICE_OUTPUT_GLOB)):
        try:
            rows = load_rows(path, required=True)
            if not rows:
                continue
            region, base_rows, _old_teaching = current_base_contract(rows)
        except ValueError as exc:
            raise PublishIntegrityError(f"invalid current output {path}: {exc}") from exc
        if not base_rows:
            raise PublishIntegrityError(
                f"external-only current admin-service output detected: {path}"
            )
        if region in indexed:
            other_path, _ = indexed[region]
            raise PublishIntegrityError(
                f"more than one current admin-service base output for {region}: "
                f"{other_path}, {path}"
            )
        indexed[region] = (path, rows)
    return indexed


def verify_publishable_regions(
    regions: list[str],
    *,
    current_output_dir: Path,
    snapshot_dir: Path,
    evidence_dir: Path,
    today: date,
    max_isolated_regions: int,
) -> PublishVerification:
    indexed = _current_outputs_by_region(current_output_dir)
    results: list[RegionVerification] = []

    for region in sorted(set(regions), key=str.casefold):
        current = indexed.get(region)
        if current is None:
            results.append(
                RegionVerification(
                    region=region,
                    status="ISOLATED",
                    reason=(
                        "no current non-empty regional base output; previous live "
                        "page must be retained"
                    ),
                )
            )
            continue

        output_path, combined = current
        slug = region_slug(region)
        snapshot_path = snapshot_dir / f"{slug}-admin-service.json"
        evidence_path = evidence_dir / f"{slug}-admin-service-evidence.json"
        if not snapshot_path.is_file() or not evidence_path.is_file():
            results.append(
                RegionVerification(
                    region=region,
                    status="ISOLATED",
                    reason=(
                        "approved regional snapshot or evidence is missing; previous "
                        "live page must be retained"
                    ),
                    output_path=str(output_path),
                )
            )
            continue

        try:
            snapshot = load_approved_snapshot(
                snapshot_path,
                evidence_dir=evidence_dir,
            )
        except ValueError as exc:
            raise PublishIntegrityError(
                f"invalid approved evidence for {region}: {exc}"
            ) from exc
        if snapshot.region != region:
            raise PublishIntegrityError(
                f"approved snapshot region {snapshot.region!r} differs from {region!r}"
            )
        try:
            expected, counts = compose_rows(
                combined,
                list(snapshot.rows),
                region=region,
                today=today,
            )
        except ValueError as exc:
            raise PublishIntegrityError(
                f"safe recomposition failed for {region}: {exc}"
            ) from exc
        if canonical_rows(expected) != canonical_rows(combined):
            raise PublishIntegrityError(
                f"{output_path} does not exactly match safe recomposition for {region}"
            )
        results.append(
            RegionVerification(
                region=region,
                status="VERIFIED",
                reason="safe recomposition exactly matches current combined output",
                output_path=str(output_path),
                base_rows=counts["base_rows"],
                teaching_rows=counts["teaching_vacancies"],
                expired_skipped=counts["expired_teaching_vacancies_skipped"],
                duplicate_skipped=counts["duplicate_teaching_vacancies_skipped"],
                total=counts["total"],
            )
        )

    return PublishVerification(
        regions=tuple(results),
        max_isolated_regions=max_isolated_regions,
    )


def enforce_isolation_threshold(report: PublishVerification) -> None:
    count = len(report.isolated_regions)
    if count > report.max_isolated_regions:
        names = ", ".join(report.isolated_regions)
        raise PublishIntegrityError(
            f"{count} Teaching Vacancies regions require isolation (maximum "
            f"{report.max_isolated_regions}): {names}"
        )


def format_report(report: PublishVerification) -> str:
    lines = [
        "## Teaching Vacancies regional publish verification",
        "",
        "| Region | Status | Base | Teaching | Total | Reason |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in report.regions:
        lines.append(
            f"| {row.region} | {row.status} | {row.base_rows} | "
            f"{row.teaching_rows} | {row.total} | {row.reason} |"
        )
    lines.extend(
        [
            "",
            f"Isolated regions: {len(report.isolated_regions)} / "
            f"{report.max_isolated_regions} permitted.",
        ]
    )
    if report.isolated_regions:
        lines.append(
            "Previous live pages retained for: " + ", ".join(report.isolated_regions) + "."
        )
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--master-review", type=Path, default=DEFAULT_MASTER_REVIEW)
    parser.add_argument(
        "--current-output-dir", type=Path, default=DEFAULT_CURRENT_OUTPUT_DIR
    )
    parser.add_argument("--snapshot-dir", type=Path, default=DEFAULT_SNAPSHOT_DIR)
    parser.add_argument("--evidence-dir", type=Path, default=DEFAULT_EVIDENCE_DIR)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--max-isolated-regions", type=int, default=3)
    parser.add_argument("--report-json", type=Path)
    parser.add_argument("--summary", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.max_isolated_regions < 0:
        raise SystemExit("STOP: max isolated regions cannot be negative")
    try:
        report = verify_publishable_regions(
            live_review_regions(args.master_review),
            current_output_dir=args.current_output_dir,
            snapshot_dir=args.snapshot_dir,
            evidence_dir=args.evidence_dir,
            today=args.today,
            max_isolated_regions=args.max_isolated_regions,
        )
        rendered = format_report(report)
        if args.report_json:
            args.report_json.parent.mkdir(parents=True, exist_ok=True)
            args.report_json.write_text(
                json.dumps(report.as_json(), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        if args.summary:
            args.summary.parent.mkdir(parents=True, exist_ok=True)
            with args.summary.open("a", encoding="utf-8") as handle:
                handle.write(rendered)
        print(rendered, end="")
        enforce_isolation_threshold(report)
    except PublishIntegrityError as exc:
        raise SystemExit(f"STOP: {exc}") from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
