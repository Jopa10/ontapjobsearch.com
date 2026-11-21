#!/usr/bin/env python3
"""Build a compact, date-pinned projection from applied JobG8 output artifacts."""
import argparse
import json
import re
from pathlib import Path

CORE_FIELDS = ("title", "employer", "advertiser_name", "apply_url", "salary_min", "salary_max", "salary_period", "salary_text")
EXPECTED_ARTIFACT_NAMES = {"service-admin-output", "support-worker-output"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--production-run-id", type=int, required=True)
    parser.add_argument("--artifact-id", type=int, required=True, help="Primary artifact ID (service-admin)")
    parser.add_argument("--source-artifacts-json", required=True)
    parser.add_argument("--production-app-commit-sha", required=True)
    parser.add_argument("--production-app-snapshot-at", required=True)
    parser.add_argument("--expected-json-files", type=int, required=True)
    parser.add_argument("--expected-jobg8-rows", type=int, required=True)
    parser.add_argument("--expected-unique-jobg8-ids", type=int, required=True)
    parser.add_argument("--archive-sha256", required=True, help="Primary artifact digest")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if not re.fullmatch(r"20\d\d-\d\d-\d\d", args.date):
        raise SystemExit("Invalid publication date")
    if not re.fullmatch(r"[a-f0-9]{64}", args.archive_sha256):
        raise SystemExit("Invalid primary artifact SHA-256")
    if not re.fullmatch(r"[a-f0-9]{40}", args.production_app_commit_sha):
        raise SystemExit("Invalid final production app commit SHA")
    artifacts = json.loads(args.source_artifacts_json)
    if not isinstance(artifacts, list) or len(artifacts) != 2:
        raise SystemExit("Expected both Thursday production output artifacts")
    if {item.get("name") for item in artifacts} != EXPECTED_ARTIFACT_NAMES:
        raise SystemExit("Unexpected applied output artifact names")
    for item in artifacts:
        if (not isinstance(item.get("id"), int) or item["id"] <= 0
                or not re.fullmatch(r"[a-f0-9]{64}", item.get("sha256", ""))):
            raise SystemExit("Invalid applied output artifact ID or digest")
    primary = next(item for item in artifacts if item["name"] == "service-admin-output")
    if primary["id"] != args.artifact_id or primary["sha256"] != args.archive_sha256:
        raise SystemExit("Primary artifact ID/digest does not match the recorded artifact list")

    root = Path(args.input)
    files = sorted(root.rglob("*.json"))
    if len(files) != args.expected_json_files:
        raise SystemExit(f"Expected {args.expected_json_files} JSON output files; found {len(files)}")

    records = {}
    jobg8_rows = 0
    for path in files:
        try:
            rows = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            raise SystemExit(f"Cannot parse production output {path.name}: {exc}")
        if not isinstance(rows, list):
            raise SystemExit(f"Production output is not a row list: {path.name}")
        scope = path.relative_to(root).as_posix()
        for row in rows:
            if not isinstance(row, dict) or str(row.get("source", "")).strip() != "JobG8":
                continue
            jobg8_rows += 1
            job_id = str(row.get("job_id", "")).strip()
            title = str(row.get("title", "")).strip()
            apply_url = str(row.get("apply_url", "")).strip()
            if not job_id or not title or not apply_url.startswith(("https://", "http://")):
                raise SystemExit(f"Invalid published JobG8 record in {path.name}")
            employer = row.get("company") or row.get("advertiser_name") or None
            normalized = {
                "job_id": job_id,
                "title": title,
                "employer": employer,
                "advertiser_name": row.get("advertiser_name") or employer,
                "apply_url": apply_url,
                "salary_min": row.get("salary_min"),
                "salary_max": row.get("salary_max"),
                "salary_period": row.get("salary_period") or None,
                "salary_text": row.get("salary_text") or None,
            }
            appearance = {
                "scope": scope,
                "location": row.get("location") or None,
                "region": row.get("region") or None,
                "category": row.get("category") or None,
            }
            if job_id not in records:
                records[job_id] = {**normalized, "_appearances": {}}
            existing = records[job_id]
            for field in CORE_FIELDS:
                if existing[field] != normalized[field]:
                    raise SystemExit(f"Conflicting {field} values for JobG8 ID {job_id}")
            prior_appearance = existing["_appearances"].get(scope)
            if prior_appearance is not None and prior_appearance != appearance:
                raise SystemExit(f"Conflicting duplicate rows for JobG8 ID {job_id} in scope {scope}")
            existing["_appearances"][scope] = appearance

    if jobg8_rows != args.expected_jobg8_rows:
        raise SystemExit(f"Expected {args.expected_jobg8_rows} JobG8 output rows; found {jobg8_rows}")
    if len(records) != args.expected_unique_jobg8_ids:
        raise SystemExit(f"Expected {args.expected_unique_jobg8_ids} unique JobG8 IDs; found {len(records)}")

    compact = []
    for job_id in sorted(records):
        record = records[job_id]
        appearances = [record["_appearances"][scope] for scope in sorted(record["_appearances"])]
        categories = sorted({x["category"] for x in appearances if x["category"]})
        regions = sorted({x["region"] for x in appearances if x["region"]})
        locations = sorted({x["location"] for x in appearances if x["location"]})
        record.pop("_appearances")
        compact.append({
            **record,
            "location": locations[0] if len(locations) == 1 else None,
            "region": regions[0] if len(regions) == 1 else None,
            "role_family": categories[0] if len(categories) == 1 else None,
            "classification_evidence": {
                "categories": categories,
                "regions": regions,
                "locations": locations,
                "published_output_appearances": appearances,
            },
        })

    payload = {
        "schemaVersion": 1,
        "feedDate": args.date,
        "productionWorkflowRunId": args.production_run_id,
        "productionArtifactId": args.artifact_id,
        "productionArtifactSha256": args.archive_sha256,
        "productionArtifacts": artifacts,
        "productionAppCommitSha": args.production_app_commit_sha,
        "productionAppSnapshotAt": args.production_app_snapshot_at,
        "productionOutputJsonFiles": len(files),
        "jobg8OutputRows": jobg8_rows,
        "uniqueJobG8Ids": len(compact),
        "recordProjection": "jobs table fields only; full descriptions/raw adverts omitted",
        "records": compact,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({
        "feedDate": args.date,
        "productionWorkflowRunId": args.production_run_id,
        "productionArtifacts": artifacts,
        "productionAppCommitSha": args.production_app_commit_sha,
        "productionOutputJsonFiles": len(files),
        "jobg8OutputRows": jobg8_rows,
        "uniqueJobG8Ids": len(compact),
        "recordProjection": payload["recordProjection"],
    }, sort_keys=True))

if __name__ == "__main__":
    main()
