"""Refresh and compose reviewed NHS admin/service jobs into daily pipeline output.

This is the non-interactive NHS stage used by the normal Ontap daily process.
It refreshes current Administrative & Clerical inventory, reapplies remembered
review decisions, applies the existing routing/dedupe/Tier A-before-B/20% source
cap rules, fetches descriptions only for accepted NHS rows, verifies that
non-NHS rows are unchanged, then atomically replaces the combined pipeline
outputs and same-day NHS review surfaces.
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
from external_sources.nhs_review_actions import reapply


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


def run_daily_compose(
    *,
    output_dir: Path,
    review_csv: Path,
    summary_md: Path,
    ledger_csv: Path,
    today: date,
    write: bool,
) -> dict[str, object]:
    vacancies, reported_total = inventory.fetch_all()

    with tempfile.TemporaryDirectory(prefix="ontap-nhs-daily-") as tmp_name:
        tmp = Path(tmp_name)
        tmp_review = tmp / "nhs-jobs-review.csv"
        tmp_summary = tmp / "nhs-jobs-summary.md"
        precompose = tmp / "precompose"
        composed = tmp / "composed"

        rows = nhs.review_rows(vacancies, today=today)
        nhs.write_review_csv(tmp_review, rows)
        reapplied = {"reapplied": 0, "changed_facts": 0}
        if ledger_csv.is_file():
            reapplied = reapply(tmp_review, ledger_csv)
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
            raise RuntimeError(
                "STOP: NHS advert description enrichment incomplete: "
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
            shutil.copy2(tmp_review, review_csv)
            shutil.copy2(tmp_summary, summary_md)

    result: dict[str, object] = {
        "review_date": today.isoformat(),
        "api_reported_total": reported_total,
        "reviewed_open_rows": len(rows),
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
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    result = run_daily_compose(
        output_dir=args.output_dir,
        review_csv=args.review_csv,
        summary_md=args.summary_md,
        ledger_csv=args.ledger_csv,
        today=args.today,
        write=args.write,
    )
    print(json.dumps(result, indent=2))
    if not args.write:
        print("Dry run only; pass --write to replace pipeline outputs and NHS review surfaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
