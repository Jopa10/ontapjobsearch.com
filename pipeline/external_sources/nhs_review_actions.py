"""Persist NHS review actions from the unified Ontap daily review.

This keeps NHS behaviour aligned with the existing external-source rule:
unchanged vacancy facts remember the user's select/exclude decision; changed
facts return to review.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

from review_hub.contracts import ReviewItem

LEDGER_FIELDS = ("source_job_id", "action", "hub_fingerprint", "row_fingerprint")
VALID_ACTIONS = {"select", "exclude"}


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def row_fingerprint(row: dict[str, str]) -> str:
    payload = {
        key: clean(value)
        for key, value in row.items()
        if key not in {"manual_action", "final_decision"}
    }
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def review_item(row: dict[str, str]) -> ReviewItem:
    return ReviewItem(
        source="NHS Jobs",
        source_job_id=clean(row.get("source_job_id")),
        title=clean(row.get("title")),
        employer=clean(row.get("employer")),
        location=clean(row.get("location")),
        region=clean(row.get("region")),
        category="admin_service",
        salary=clean(row.get("salary_text")),
        closing_date=clean(row.get("closing_date")),
        reason=(
            f"{clean(row.get('switchability'))}: {clean(row.get('classification_reason'))}"
        ).strip(": "),
        source_url=clean(row.get("source_url")),
    )


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def parse_master_actions(path: Path) -> dict[str, tuple[str, str]]:
    text = path.read_text(encoding="utf-8-sig")
    output: dict[str, tuple[str, str]] = {}
    for block in re.findall(r"(?ms)^---\s*$\n(.*?)^---\s*$", text):
        source_match = re.search(r"(?mi)^source_key:\s*(\S+)\s*$", block)
        if not source_match or clean(source_match.group(1)).casefold() != "nhs":
            continue
        id_match = re.search(r"(?mi)^source_job_id:\s*(\S+)\s*$", block)
        action_match = re.search(r"(?mi)^action:\s*(select|exclude)?\s*$", block)
        fingerprint_match = re.search(r"(?mi)^hub_fingerprint:\s*([a-f0-9]{64})\s*$", block)
        if not id_match or not action_match or not fingerprint_match:
            continue
        action = clean(action_match.group(1)).casefold()
        if action in VALID_ACTIONS:
            output[clean(id_match.group(1))] = (action, clean(fingerprint_match.group(1)))
    return output


def load_ledger(path: Path) -> dict[str, dict[str, str]]:
    if not path.is_file():
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != LEDGER_FIELDS:
            raise ValueError("NHS decision ledger columns do not match contract")
        return {clean(row["source_job_id"]): dict(row) for row in reader}


def write_ledger(path: Path, rows: dict[str, dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS, lineterminator="\n")
        writer.writeheader()
        for source_id in sorted(rows):
            writer.writerow(rows[source_id])


def capture_from_master(master: Path, review_csv: Path, ledger: Path) -> dict[str, int]:
    actions = parse_master_actions(master)
    _fields, rows = load_csv(review_csv)
    by_id = {clean(row.get("source_job_id")): row for row in rows}
    existing = load_ledger(ledger)
    changed = 0
    for source_id, (action, hub_fingerprint) in actions.items():
        row = by_id.get(source_id)
        if not row:
            continue
        live_hub = review_item(row).fingerprint()
        if live_hub != hub_fingerprint:
            continue
        record = {
            "source_job_id": source_id,
            "action": action,
            "hub_fingerprint": hub_fingerprint,
            "row_fingerprint": row_fingerprint(row),
        }
        if existing.get(source_id) != record:
            existing[source_id] = record
            changed += 1
    write_ledger(ledger, existing)
    return {"captured": len(actions), "changed": changed, "remembered": len(existing)}


def reapply(review_csv: Path, ledger: Path) -> dict[str, int]:
    fieldnames, rows = load_csv(review_csv)
    if "manual_action" not in fieldnames or "final_decision" not in fieldnames:
        raise ValueError("NHS review CSV lacks manual decision columns")
    remembered = load_ledger(ledger)
    matched = 0
    changed_facts = 0
    for row in rows:
        source_id = clean(row.get("source_job_id"))
        record = remembered.get(source_id)
        action = ""
        if record:
            if record["hub_fingerprint"] == review_item(row).fingerprint():
                action = clean(record["action"]).casefold()
                matched += 1
            else:
                changed_facts += 1
        row["manual_action"] = action
        classification = clean(row.get("classification")).upper()
        if classification == "HARD_PASS":
            final = "HARD_PASS"
        elif action == "select":
            final = "SELECTED"
        elif action == "exclude":
            final = "EXCLUDED"
        elif classification == "HC":
            final = "SELECTED"
        else:
            final = "POSS"
        row["final_decision"] = final
    with review_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return {"reapplied": matched, "changed_facts": changed_facts}
