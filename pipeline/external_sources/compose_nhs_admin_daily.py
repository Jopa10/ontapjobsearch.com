"""Refresh and compose reviewed NHS admin/service jobs into daily pipeline output.

This is the non-interactive NHS stage used by the normal Ontap daily process.
It captures any valid manual NHS decisions already present in the unified review,
refreshes current Administrative & Clerical inventory, reapplies remembered
review decisions, applies the existing routing/dedupe/Tier A-before-B/20% source
cap rules, fetches descriptions only for accepted NHS rows, verifies that
non-NHS rows are unchanged, then atomically replaces the combined pipeline
outputs and NHS review surfaces.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import tempfile
from datetime import date
from pathlib import Path

from external_sources import nhs_admin_inventory as inventory
from external_sources import nhs_admin_service as nhs
from external_sources.nhs_admin_dry_run import accepted_nhs_source_ids
from external_sources.nhs_review_actions import capture_from_master, reapply


def load_review_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def verify_composition(current_dir: Path, composed_dir: Path) -> dict[str, int]:
    source = nhs.SOURCE.casefold()
    files = accepted = total = 0
    for out in sorted(composed_dir.glob("*-admin-service.json")):
        current_path = current_dir / out.name
        if not current_path.is_file():
            raise RuntimeError(f"STOP: composed NHS output has no current base file: {out.name}")
        current = json.loads(current_path.read_text(encoding="utf-8"))
        composed = json.loads(out.read_text(encoding="utf-8"))
        old_base = [r for r in current if str(r.get("source", "")).strip().casefold() != source]
        new_base = [r for r in composed if str(r.get("source", "")).strip().casefold() != source]
        if old_base != new_base:
            raise RuntimeError(f"STOP: non-NHS rows changed in {out.name}")
        nhs_rows = [r for r in composed if str(r.get("source", "")).strip().casefold() == source]
        if composed and len(nhs_rows) / len(composed) > nhs.MAX_NHS_SHARE + 1e-12:
            raise RuntimeError(f"STOP: NHS share cap breached in {out.name}")
        if any(not str(r.get("apply_url", "")).strip() for r in nhs_rows):
            raise RuntimeError(f"STOP: NHS row with no apply_url in {out.name}")
        if any(not str(r.get("description", "")).strip() for r in nhs_rows):
            raise RuntimeError(f"STOP: NHS row with no description in {out.name}")
        files += 1
        accepted += len(nhs_rows)
        total += len(composed)
    if not files:
        raise RuntimeError("STOP: NHS composition produced no admin/service output files")
    return {"files": files, "nhs_accepted": accepted, "combined_rows": total}


def retain_last_approved_nhs(
    *,
    output_dir: Path,
    approved_output_dir: Path,
    today: date,
    write: bool,
) -> dict[str, object]:
    """Recompose the last approved NHS subset against the fresh non-NHS base."""
    with tempfile.TemporaryDirectory(prefix="ontap-nhs-retained-") as tmp_name:
        composed_dir = Path(tmp_name) / "composed"
        composed_dir.mkdir(parents=True, exist_ok=True)
        regions: dict[str, dict[str, object]] = {}
        total_retained = total_deferred = total_duplicates = 0

        current_paths = sorted(output_dir.glob("*-admin-service.json"))
        if not current_paths:
            raise RuntimeError("STOP: no fresh Service Admin outputs available for NHS fallback")

        for current_path in current_paths:
            approved_path = approved_output_dir / current_path.name
            current = json.loads(current_path.read_text(encoding="utf-8"))
            if not isinstance(current, list):
                raise RuntimeError(f"STOP: invalid fresh Service Admin output: {current_path}")
            if approved_path.is_file():
                approved = json.loads(approved_path.read_text(encoding="utf-8"))
                if not isinstance(approved, list):
                    raise RuntimeError(f"STOP: invalid approved NHS fallback: {approved_path}")
            else:
                approved = []

            candidates: list[dict[str, object]] = []
            duplicate_count = 0
            for raw in approved:
                if not isinstance(raw, dict) or nhs.clean(raw.get("source")).casefold() != nhs.SOURCE.casefold():
                    continue
                candidate = dict(raw)
                if not nhs.clean(candidate.get("apply_url")) or not nhs.clean(candidate.get("description")):
                    raise RuntimeError(
                        f"STOP: approved NHS fallback row is incomplete in {approved_path.name}"
                    )
                duplicate_probe = {
                    **candidate,
                    "employer": candidate.get("company") or candidate.get("advertiser_name"),
                }
                if nhs.duplicate_against_current(duplicate_probe, current):
                    duplicate_count += 1
                    continue
                candidates.append(candidate)

            region = next(
                (
                    nhs.clean(row.get("region"))
                    for row in [*current, *candidates]
                    if isinstance(row, dict) and nhs.clean(row.get("region"))
                ),
                current_path.stem,
            )
            composed, deferred = nhs.compose_region(current, candidates, region=region)
            (composed_dir / current_path.name).write_text(
                json.dumps(composed, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            retained = sum(
                nhs.clean(row.get("source")).casefold() == nhs.SOURCE.casefold()
                for row in composed
            )
            regions[region] = {
                "file": current_path.name,
                "approved_candidates": len(candidates),
                "retained": retained,
                "deferred_by_cap": len(deferred),
                "withheld_as_fresh_duplicate": duplicate_count,
            }
            total_retained += retained
            total_deferred += len(deferred)
            total_duplicates += duplicate_count

        safety = verify_composition(output_dir, composed_dir)
        if write:
            for path in composed_dir.glob("*-admin-service.json"):
                shutil.copy2(path, output_dir / path.name)

    return {
        "review_date": today.isoformat(),
        "source_status": "ISOLATED_RETAINED_LAST_APPROVED",
        "retained_nhs_jobs": total_retained,
        "deferred_by_cap": total_deferred,
        "withheld_as_fresh_duplicate": total_duplicates,
        "regions": regions,
        "safety": safety,
        "written": write,
    }


def run_daily_compose(
    *,
    output_dir: Path,
    review_csv: Path,
    summary_md: Path,
    ledger_csv: Path,
    master_review: Path,
    today: date,
    write: bool,
) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="ontap-nhs-daily-") as tmp_name:
        tmp = Path(tmp_name)
        tmp_review = tmp / "nhs-jobs-review.csv"
        tmp_summary = tmp / "nhs-jobs-summary.md"
        tmp_ledger = tmp / "nhs-jobs-decisions.csv"
        precompose = tmp / "precompose"
        composed = tmp / "composed"

        if ledger_csv.is_file():
            shutil.copy2(ledger_csv, tmp_ledger)

        captured = {"captured": 0, "changed": 0, "remembered": 0}
        if master_review.is_file() and review_csv.is_file():
            captured = capture_from_master(master_review, review_csv, tmp_ledger)

        vacancies, reported_total = inventory.fetch_all()
        rows = nhs.review_rows(vacancies, today=today)
        nhs.write_review_csv(tmp_review, rows)
        reapplied = {"reapplied": 0, "changed_facts": 0}
        if tmp_ledger.is_file():
            reapplied = reapply(tmp_review, tmp_ledger)
        rows = load_review_rows(tmp_review)

        # First composition uses lightweight NHS search metadata only. This identifies
        # exactly which NHS jobs survive routing, dedupe, tier ordering and the cap.
        nhs.compose_outputs(output_dir, rows, precompose, today=today)
        accepted_ids = accepted_nhs_source_ids(precompose)

        # Fetch full advert text only for the NHS jobs that would actually be published.
        enriched, enrichment = inventory.enrich_descriptions(rows, source_job_ids=accepted_ids)
        if enrichment["requested"] != len(accepted_ids):
            raise RuntimeError(
                "STOP: NHS description request count did not match accepted jobs: "
                f"accepted={len(accepted_ids)} requested={enrichment['requested']}"
            )
        if enrichment["failed"] or enrichment["succeeded"] != len(accepted_ids):
            raise inventory.NHSUpstreamUnavailable(
                "NHS advert description enrichment unavailable: "
                f"accepted={len(accepted_ids)} succeeded={enrichment['succeeded']} "
                f"failed={enrichment['failed']}"
            )

        nhs.write_review_csv(tmp_review, enriched)
        tmp_summary.write_text(nhs.review_summary(enriched, today=today), encoding="utf-8")
        composition = nhs.compose_outputs(output_dir, enriched, composed, today=today)
        safety = verify_composition(output_dir, composed)

        if write:
            for path in composed.glob("*-admin-service.json"):
                shutil.copy2(path, output_dir / path.name)
            review_csv.parent.mkdir(parents=True, exist_ok=True)
            summary_md.parent.mkdir(parents=True, exist_ok=True)
            ledger_csv.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(tmp_review, review_csv)
            shutil.copy2(tmp_summary, summary_md)
            if tmp_ledger.is_file():
                shutil.copy2(tmp_ledger, ledger_csv)

    result: dict[str, object] = {
        "review_date": today.isoformat(),
        "api_reported_total": reported_total,
        "reviewed_open_rows": len(rows),
        "captured_decisions": captured,
        "remembered_decisions": reapplied,
        "accepted_after_source_cap": len(accepted_ids),
        "description_enrichment": enrichment,
        "safety": safety,
        "composition": composition,
        "written": write,
    }
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("output-admin-service"))
    parser.add_argument(
        "--review-csv", type=Path, default=Path("reviews/external/nhs-jobs-review.csv")
    )
    parser.add_argument(
        "--summary-md", type=Path, default=Path("reviews/external/nhs-jobs-summary.md")
    )
    parser.add_argument(
        "--ledger-csv", type=Path, default=Path("reviews/external/nhs-jobs-decisions.csv")
    )
    parser.add_argument(
        "--master-review", type=Path, default=Path("reviews/daily/ontap-daily-review.md")
    )
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--fallback-output-dir",
        type=Path,
        help="Last approved combined outputs to retain when the NHS source is unavailable.",
    )
    args = parser.parse_args(argv)

    try:
        result = run_daily_compose(
            output_dir=args.output_dir,
            review_csv=args.review_csv,
            summary_md=args.summary_md,
            ledger_csv=args.ledger_csv,
            master_review=args.master_review,
            today=args.today,
            write=args.write,
        )
    except inventory.NHSUpstreamUnavailable as exc:
        if not args.write or args.fallback_output_dir is None:
            raise
        result = retain_last_approved_nhs(
            output_dir=args.output_dir,
            approved_output_dir=args.fallback_output_dir,
            today=args.today,
            write=True,
        )
        result["warning"] = str(exc)
        print(f"::warning title=NHS source isolated::{exc}; retained last approved NHS state")
    print(json.dumps(result, indent=2))
    if not args.write:
        print("Dry run only; pass --write to replace pipeline outputs and NHS review surfaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
