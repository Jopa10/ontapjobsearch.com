"""Apply England-wide Teaching Vacancies review actions to regional boundaries.

The England-wide Markdown file is the human review surface. This module verifies
that every LIVE, non-hard-pass block still matches the master CSV, then copies
only the action decisions into the corresponding regional review CSVs and
regenerates their Markdown summaries. It does not approve, compose or publish
jobs; those remain separate guarded stages.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
from collections import Counter
from pathlib import Path

from external_sources import teaching_vacancies_discovery as discovery
from external_sources import teaching_vacancies_master_review as master
from external_sources import teaching_vacancies_regional_approved as approval
from external_sources import teaching_vacancies_regional_review as regional
from external_sources.regional_contracts import clean

DEFAULT_REVIEW_DIR = Path("reviews/external/teaching-vacancies")
DEFAULT_MASTER_CSV = DEFAULT_REVIEW_DIR / "england-wide-admin-service-review.csv"
DEFAULT_MASTER_MD = DEFAULT_REVIEW_DIR / "england-wide-admin-service-summary.md"
VALID_ACTIONS = {"", "select", "exclude"}


def _block_value(block: str, key: str) -> str:
    match = re.search(rf"(?mi)^{re.escape(key)}:[ \t]*(.*?)[ \t]*$", block)
    return clean(match.group(1)) if match else ""


def load_master_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise ValueError(f"England-wide Teaching Vacancies CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != master.MASTER_FIELDS:
            raise ValueError("England-wide Teaching Vacancies CSV columns do not match the contract")
        rows = [dict(row) for row in reader]
    if not rows:
        raise ValueError("England-wide Teaching Vacancies CSV contains no rows")
    ids = [clean(row.get("source_job_id")) for row in rows]
    if any(not value for value in ids):
        raise ValueError("England-wide Teaching Vacancies CSV contains a blank source_job_id")
    if len(ids) != len(set(ids)):
        raise ValueError("England-wide Teaching Vacancies CSV contains duplicate source_job_id values")
    return rows


def _expected_facts(row: dict[str, str]) -> dict[str, str]:
    return {
        "employer": master._md(row.get("employer", "")),
        "closing_date": master._md(row.get("closing_date", "")),
        "reason": master._md(row.get("classification_reason", "")),
        "source_url": master._md(row.get("source_url", "")),
    }


def parse_master_actions(
    rows: list[dict[str, str]],
    summary_path: Path,
) -> dict[str, str]:
    if not summary_path.is_file():
        raise ValueError(f"England-wide Teaching Vacancies Markdown not found: {summary_path}")
    text = summary_path.read_text(encoding="utf-8-sig")
    reviewable = {
        clean(row["source_job_id"]): row
        for row in rows
        if row.get("review_scope") == master.REVIEW_NOW
        and clean(row.get("final_decision")).upper() != "HARD_PASS"
    }
    actions: dict[str, str] = {}
    for block in re.findall(r"(?ms)^---\s*$\n(.*?)^---\s*$", text):
        source_job_id = _block_value(block, "source_job_id")
        if not source_job_id:
            continue
        if source_job_id in actions:
            raise ValueError(
                f"duplicate source_job_id in England-wide Markdown: {source_job_id}"
            )
        row = reviewable.get(source_job_id)
        if row is None:
            raise ValueError(
                f"England-wide Markdown contains a non-reviewable or unknown ID: {source_job_id}"
            )
        action = _block_value(block, "action").casefold()
        if action not in VALID_ACTIONS:
            raise ValueError(
                f"invalid England-wide action for {source_job_id}: {action or '<blank>'}"
            )

        headline_match = re.search(
            r"(?m)^(SELECTED|POSS|EXCLUDED)\s*\|.*$",
            block,
        )
        expected_headline = master.review_headline(row)
        if not headline_match or clean(headline_match.group(0)) != expected_headline:
            raise ValueError(
                f"England-wide review facts changed for {source_job_id}: headline mismatch"
            )

        for key, expected in _expected_facts(row).items():
            if _block_value(block, key) != expected:
                raise ValueError(
                    f"England-wide review facts changed for {source_job_id}: {key} mismatch"
                )
        fingerprint = _block_value(block, "factual_fingerprint")
        if fingerprint and fingerprint != clean(row.get("factual_fingerprint")):
            raise ValueError(
                f"England-wide review facts changed for {source_job_id}: fingerprint mismatch"
            )
        actions[source_job_id] = action

    missing = sorted(set(reviewable) - set(actions))
    if missing:
        preview = ", ".join(missing[:8])
        suffix = " ..." if len(missing) > 8 else ""
        raise ValueError(
            f"England-wide Markdown is missing {len(missing)} LIVE review block(s): "
            f"{preview}{suffix}"
        )
    return actions


def _final_decision(row: dict[str, str], action: str) -> str:
    classification = clean(row.get("classification")).upper()
    if classification == "HARD_PASS":
        return "HARD_PASS"
    if action == "exclude":
        return "EXCLUDED"
    if action == "select":
        return "SELECTED"
    if classification == "HC":
        return "SELECTED"
    return "POSS"


def carry_existing_actions(
    current_rows: list[dict[str, str]],
    *,
    old_master_csv: Path,
    old_master_summary: Path,
) -> int:
    """Carry non-blank actions only when the exact factual vacancy is unchanged."""
    if not old_master_csv.is_file() or not old_master_summary.is_file():
        return 0
    old_rows = load_master_csv(old_master_csv)
    old_actions = parse_master_actions(old_rows, old_master_summary)
    old_by_id = {clean(row["source_job_id"]): row for row in old_rows}
    current_by_id = {clean(row["source_job_id"]): row for row in current_rows}
    carried = 0
    for source_job_id, action in old_actions.items():
        if not action:
            continue
        old = old_by_id[source_job_id]
        current = current_by_id.get(source_job_id)
        if current is None or current.get("review_scope") != master.REVIEW_NOW:
            continue
        if clean(current.get("final_decision")).upper() == "HARD_PASS":
            continue
        if (
            action == "select"
            and clean(current.get("jobg8_check")).upper()
            == "POSSIBLE_DUPLICATE"
        ):
            current["manual_action"] = ""
            current["final_decision"] = _final_decision(current, "")
            continue
        old_fingerprint = clean(old.get("factual_fingerprint"))
        current_fingerprint = clean(current.get("factual_fingerprint"))
        if not old_fingerprint or old_fingerprint != current_fingerprint:
            continue
        current["manual_action"] = action
        current["final_decision"] = _final_decision(current, action)
        carried += 1
    return carried


def _regional_rows(path: Path) -> tuple[list[dict[str, str]], bytes]:
    content = path.read_bytes()
    with io.StringIO(content.decode("utf-8-sig"), newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != regional.REVIEW_FIELDS:
            raise ValueError(f"regional review CSV columns do not match the contract: {path}")
        rows = [dict(row) for row in reader]
    return rows, content


def _regional_csv_bytes(rows: list[dict[str, str]]) -> bytes:
    handle = io.StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=regional.REVIEW_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue().encode("utf-8")


def apply_master_actions(
    *,
    master_csv: Path = DEFAULT_MASTER_CSV,
    master_summary: Path = DEFAULT_MASTER_MD,
    review_dir: Path = DEFAULT_REVIEW_DIR,
    write: bool = False,
) -> dict[str, int]:
    rows = load_master_csv(master_csv)
    actions = parse_master_actions(rows, master_summary)
    remaining = set(actions)
    changed_regions = 0

    for csv_path in sorted(review_dir.glob("*-admin-service-review.csv")):
        if csv_path.name == master_csv.name:
            continue
        region_rows, original_content = _regional_rows(csv_path)
        regional_ids = {
            clean(row.get("source_job_id"))
            for row in region_rows
            if clean(row.get("source_job_id"))
        }
        relevant = regional_ids & set(actions)
        if not relevant:
            continue

        summary_path = csv_path.with_name(csv_path.name.replace("-review.csv", "-summary.md"))
        metadata, _ = approval.parse_review_metadata(summary_path)
        regions = {clean(row.get("ontap_region")) for row in region_rows}
        if regions != {metadata.region}:
            raise ValueError(f"regional CSV contains mixed or wrong region: {csv_path}")
        if metadata.slice_status != "LIVE":
            raise ValueError(
                f"England-wide action targets non-LIVE regional boundary: {metadata.region}"
            )

        for row in region_rows:
            source_job_id = clean(row.get("source_job_id"))
            if source_job_id not in actions:
                continue
            action = actions[source_job_id]
            row["manual_action"] = action
            row["final_decision"] = _final_decision(row, action)
            remaining.discard(source_job_id)

        new_csv = _regional_csv_bytes(region_rows)
        records = [approval._review_record_from_csv(row) for row in region_rows]
        new_summary = regional.markdown_summary(
            metadata.region,
            records,
            review_date=metadata.review_date,
            routing_manifest_sha256=metadata.routing_manifest_sha256,
        ).encode("utf-8")
        old_summary = summary_path.read_bytes()
        if new_csv != original_content or new_summary != old_summary:
            changed_regions += 1
        if write:
            discovery.write_bytes_atomic(csv_path, new_csv)
            discovery.write_bytes_atomic(summary_path, new_summary)

    if remaining:
        raise ValueError(
            "England-wide actions were not found in regional review boundaries: "
            + ", ".join(sorted(remaining))
        )

    counts = Counter(actions.values())
    return {
        "reviewable": len(actions),
        "selected_actions": counts["select"],
        "excluded_actions": counts["exclude"],
        "blank_actions": counts[""],
        "regional_files_changed": changed_regions,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--master-csv", type=Path, default=DEFAULT_MASTER_CSV)
    parser.add_argument("--master-summary", type=Path, default=DEFAULT_MASTER_MD)
    parser.add_argument("--review-dir", type=Path, default=DEFAULT_REVIEW_DIR)
    parser.add_argument("--write-regional-actions", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.write_regional_actions:
        raise SystemExit(
            "STOP: add --write-regional-actions to copy the reviewed England-wide "
            "actions into regional approval boundaries."
        )
    try:
        counts = apply_master_actions(
            master_csv=args.master_csv,
            master_summary=args.master_summary,
            review_dir=args.review_dir,
            write=True,
        )
    except ValueError as exc:
        raise SystemExit(f"STOP: {exc}") from exc
    print(
        "England-wide Teaching Vacancies review synced to regional boundaries: "
        f"{counts['reviewable']} reviewable, {counts['selected_actions']} manual "
        f"select, {counts['excluded_actions']} manual exclude, "
        f"{counts['blank_actions']} unchanged; "
        f"{counts['regional_files_changed']} regional review set(s) changed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
