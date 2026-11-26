#!/usr/bin/env python3
"""Validate and stage privately chosen current CPC jobs during the Preview window."""

from __future__ import annotations

import json
import os
import subprocess
from datetime import date
from pathlib import Path

from pipeline.scripts.send_cpc_job_alerts import (
    PRIVATE_TEST_EMAIL,
    DeliveryError,
    all_published_cpc_jobs,
    parse_manual_job_references,
)


def main() -> int:
    report_date = os.environ.get("ONTAP_PRIVATE_REPORT_DATE", "")
    try:
        date.fromisoformat(report_date)
    except ValueError as error:
        raise DeliveryError("A current report date is required to stage Preview jobs.") from error
    if len(report_date) != 10:
        raise DeliveryError("A current report date is required to stage Preview jobs.")
    prefs_path = Path(os.environ["NEON_ALERT_PREFERENCES_OUTPUT"])
    saved = json.loads(prefs_path.read_text(encoding="utf-8"))
    if saved.get("email") != PRIVATE_TEST_EMAIL or saved.get("consentAction") != "granted":
        raise DeliveryError("Manual Preview selections require the approved recipient's active consent.")

    supplied = os.environ.get("ONTAP_PRIVATE_MANUAL_JOB_IDS", "")
    if supplied.strip():
        references = supplied
    else:
        selections_path = Path("pipeline/private_email_manual_job_ids.json")
        try:
            values = json.loads(selections_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise DeliveryError("The Preview manual-jobs file is unreadable.") from error
        if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
            raise DeliveryError("The Preview manual-jobs file must contain a list of job IDs or URLs.")
        references = " ".join(values)
    ids = parse_manual_job_references(references)
    if not ids:
        print("No manual jobs supplied; automatic matches will remain unchanged.")
        return 0
    inventory = all_published_cpc_jobs(Path(os.environ["ONTAP_PUBLISHED_APP_DIR"]))
    missing = [job_id for job_id in ids if job_id not in inventory]
    if missing:
        raise DeliveryError("Selected jobs are not current published JobG8 CPC jobs: " + ", ".join(missing))

    payload = {"action": "stageManualSelections", "reportDate": report_date, "publicIds": ids}
    subprocess.run(
        ["node", str(Path(__file__).with_name("record_neon_alert_sample.mjs"))],
        input=json.dumps(payload), text=True, check=True,
    )
    for job_id in ids:
        job = inventory[job_id]
        print(f"Staged: {job.get('title', '')} | {job.get('location', '')} | {job_id}")
    print(f"Staged {len(ids)} manual job(s) in Preview Neon.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (DeliveryError, KeyError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)
