#!/usr/bin/env python3
"""Create an explicit per-ID evidence manifest from a scratch selector replay.

This manifest is intentionally not a PostgreSQL or final-publication receipt.
It marks missing human review and PostgreSQL readback fields as incomplete.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import gzip
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    work = args.work.resolve()
    report = read_json(work / "report.json")
    with gzip.open(work / "selection.json.gz", "rt", encoding="utf-8") as handle:
        selection = json.load(handle)
    outputs = read_json(work / "plain" / "outputs.json")
    evidence = read_json(work / "observed" / "evidence.json")

    required_report = ("archiveDate", "archiveSha256", "rulesRevision", "sourceMetadata")
    missing = [key for key in required_report if not report.get(key)]
    if missing:
        raise SystemExit("Selector report missing manifest provenance: " + ", ".join(missing))
    if selection.get("report", {}).get("archiveSha256") != report["archiveSha256"]:
        raise SystemExit("Selection evidence does not match the report feed checksum")

    output_ids: dict[str, set[str]] = {}
    output_regions: dict[tuple[str, str], set[str]] = defaultdict(set)
    for scope, rows in outputs.items():
        ids = set()
        for row in rows:
            job_id = str(row["job_id"])
            ids.add(job_id)
            family = scope.split(":", 1)[0]
            output_regions[(family, job_id)].add(scope.split(":", 1)[1])
        output_ids[scope] = ids

    per_id = []
    reviews_by_scope: dict[str, set[str]] = defaultdict(set)
    outcome_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for item in selection.get("decisions", []):
        job_id = str(item["ref"])
        scope = str(item["scope"])
        outcome = str(item.get("decision", "unknown"))
        outcome_counts[scope][outcome] += 1
        if outcome == "review":
            reviews_by_scope[scope].add(job_id)
        review_record = item.get("humanReview")
        if not isinstance(review_record, dict):
            review_record = {
                "status": "not_recorded_in_selector_replay",
                "decision": None,
                "reviewedAt": None,
                "reviewer": None,
            }
        per_id.append({
            "jobId": job_id,
            "scope": scope,
            "automatedOutcome": outcome,
            "automatedReason": item.get("reason"),
            "decisionGate": item.get("gate"),
            "finalPythonOutputRegions": sorted(output_regions.get((scope.split(":", 1)[-1], job_id), set())),
            "humanReview": review_record,
        })

    ids_by_scope = {scope: sorted(ids) for scope, ids in output_ids.items()}
    final_counts = {scope: len(ids) for scope, ids in ids_by_scope.items()}
    report_counts = {scope: dict(counts) for scope, counts in outcome_counts.items()}
    unknown_reviews = sum(row["humanReview"].get("status") == "not_recorded_in_selector_replay" for row in per_id)

    manifest = {
        "schemaVersion": 1,
        "capturedAtUtc": datetime.now(timezone.utc).isoformat(),
        "feed": {
            "date": report["archiveDate"],
            "sha256": report["archiveSha256"],
            "bytes": report["sourceMetadata"].get("sizeBytes"),
            "source": report["sourceMetadata"],
        },
        "selector": {
            "revision": report["rulesRevision"],
            "dependencyManifestSha256": report.get("dependencyManifestSha256"),
            "outputSha256": report.get("outputsSha256"),
        },
        "perId": per_id,
        "automatedOutcomeCountsByScope": report_counts,
        "finalPythonOutputIdsByScope": ids_by_scope,
        "finalPythonOutputCountsByScope": final_counts,
        "reviewIdsByScope": {scope: sorted(ids) for scope, ids in reviews_by_scope.items()},
        "completeness": {
            "humanReviewRecordsMissing": unknown_reviews,
            "humanReviewEvidencePresent": unknown_reviews == 0,
            "postgresReadback": "not_performed_by_selector_replay_workflow",
            "finalPublishedReviewList": "not_available_at_selector_replay_stage",
            "parityMayBeClaimed": False,
        },
        "notes": [
            "Python remains the selector authority.",
            "Python output membership is not a final website Published list.",
            "This artifact is not PostgreSQL readback evidence and cannot pass same-feed parity by itself.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
