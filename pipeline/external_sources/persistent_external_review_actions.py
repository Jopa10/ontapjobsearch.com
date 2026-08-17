"""Persist explicit NEJobs and VONNE review actions across refresh dates.

The source-specific review generators intentionally remain conservative and
same-day guarded for publishing. This helper adds a separate durable memory for
explicit human ``select`` / ``exclude`` actions:

1. ``capture`` reads committed Markdown actions and fingerprints the matching
   CSV review facts into a small ledger.
2. The normal source review runs and regenerates today's review.
3. ``apply`` restores a remembered action only when the current CSV facts have
   the same fingerprint. Changed vacancies therefore return to review.

The ledger does not approve or publish anything. Same-day source review and
explicit PUBLISH gates remain unchanged.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


LEDGER_FIELDS = ("source_job_id", "action", "fingerprint")
VALID_ACTIONS = {"select", "exclude"}
VOLATILE_FINGERPRINT_FIELDS = {
    "manual_action",
    "final_decision",
    "detail_status",
    "jobg8_match_score",
    "nejobs_match_score",
}


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def load_review_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise ValueError(f"review CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        if "source_job_id" not in fieldnames:
            raise ValueError(f"review CSV has no source_job_id column: {path}")
        rows = [dict(row) for row in reader]
    return fieldnames, rows


def row_fingerprint(row: dict[str, str]) -> str:
    payload = {
        key: clean(value)
        for key, value in row.items()
        if key not in VOLATILE_FINGERPRINT_FIELDS
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def parse_summary_actions(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8-sig")
    actions: dict[str, str] = {}
    for block in re.findall(r"(?ms)^---\s*$\n(.*?)^---\s*$", text):
        id_match = re.search(
            r"(?mi)^source_job_id:\s*([^\s]+)\s*$",
            block,
        )
        action_match = re.search(
            r"(?mi)^action:\s*(select|exclude)?\s*$",
            block,
        )
        if not id_match or not action_match:
            continue
        action = clean(action_match.group(1)).casefold()
        if action in VALID_ACTIONS:
            actions[clean(id_match.group(1))] = action
    return actions


def load_ledger(path: Path) -> dict[str, dict[str, str]]:
    if not path.is_file():
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != LEDGER_FIELDS:
            raise ValueError(f"decision ledger columns do not match contract: {path}")
        rows = [dict(row) for row in reader]
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        source_job_id = clean(row.get("source_job_id"))
        action = clean(row.get("action")).casefold()
        fingerprint = clean(row.get("fingerprint"))
        if not source_job_id or action not in VALID_ACTIONS:
            raise ValueError(f"invalid decision ledger row in {path}: {row!r}")
        if not re.fullmatch(r"[a-f0-9]{64}", fingerprint):
            raise ValueError(
                f"invalid decision fingerprint for {source_job_id} in {path}"
            )
        result[source_job_id] = {
            "source_job_id": source_job_id,
            "action": action,
            "fingerprint": fingerprint,
        }
    return result


def write_ledger(path: Path, decisions: dict[str, dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS, lineterminator="\n")
        writer.writeheader()
        for source_job_id in sorted(decisions):
            writer.writerow(decisions[source_job_id])


def capture_actions(summary: Path, review_csv: Path, ledger: Path) -> dict[str, int]:
    actions = parse_summary_actions(summary)
    _, rows = load_review_csv(review_csv)
    by_id = {clean(row.get("source_job_id")): row for row in rows}
    decisions = load_ledger(ledger)
    changed = 0

    for source_job_id, action in actions.items():
        row = by_id.get(source_job_id)
        if row is None:
            raise ValueError(
                f"Markdown action references an ID missing from review CSV: {source_job_id}"
            )
        new_record = {
            "source_job_id": source_job_id,
            "action": action,
            "fingerprint": row_fingerprint(row),
        }
        if decisions.get(source_job_id) != new_record:
            decisions[source_job_id] = new_record
            changed += 1

    if changed or not ledger.exists():
        write_ledger(ledger, decisions)

    print(
        f"Captured {len(actions)} explicit review action(s); "
        f"{changed} ledger decision(s) changed; {len(decisions)} remembered total."
    )
    return {
        "explicit_actions": len(actions),
        "ledger_changes": changed,
        "remembered_total": len(decisions),
    }


def final_decision(classification: str, action: str) -> str:
    classification = clean(classification).upper()
    if classification == "HARD_PASS":
        return "HARD_PASS"
    if action == "exclude":
        return "EXCLUDED"
    if action == "select":
        return "SELECTED"
    if classification == "HC":
        return "SELECTED"
    return "POSS"


def write_review_csv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def patch_summary_blocks(text: str, actions: dict[str, str]) -> str:
    def replace_block(match: re.Match[str]) -> str:
        block = match.group(1)
        id_match = re.search(
            r"(?mi)^source_job_id:\s*([^\s]+)\s*$",
            block,
        )
        if not id_match:
            return match.group(0)
        source_job_id = clean(id_match.group(1))
        action = actions.get(source_job_id, "")
        replacement = f"action: {action}" if action else "action:"
        block = re.sub(
            r"(?mi)^action:\s*(?:select|exclude)?\s*$",
            replacement,
            block,
            count=1,
        )
        return f"---\n{block}---"

    return re.sub(r"(?ms)^---\s*$\n(.*?)^---\s*$", replace_block, text)


def patch_summary_copy(text: str, source: str) -> str:
    source = source.casefold()
    if source == "nejobs":
        text = text.replace(
            "- Commit the edit, then rerun the NEJobs process for the same review date.",
            "- Commit the edit; the review workflow will remember the decision.",
        )
        text = text.replace(
            "- Decisions are matched by `source_job_id` and expire when the review date changes.",
            "- Decisions are carried forward only while the same vacancy review facts remain unchanged.",
        )
    elif source == "vonne":
        text = text.replace(
            "- Actions are same-day only and do not publish anything.",
            "- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.",
        )
    else:
        raise ValueError(f"unsupported source: {source}")
    return text


def patch_summary_counts(text: str, rows: list[dict[str, str]]) -> str:
    counts = {
        "SELECTED": sum(clean(row.get("final_decision")).upper() == "SELECTED" for row in rows),
        "POSS": sum(clean(row.get("final_decision")).upper() == "POSS" for row in rows),
        "EXCLUDED": sum(clean(row.get("final_decision")).upper() == "EXCLUDED" for row in rows),
    }
    text = re.sub(
        r"(?m)^- Final selected after (?:(?:same-day|remembered/manual|manual) actions): \d+\s*$",
        f"- Final selected after remembered/manual actions: {counts['SELECTED']}",
        text,
    )
    text = re.sub(
        r"(?m)^- Final POSS awaiting decision: \d+\s*$",
        f"- Final POSS awaiting decision: {counts['POSS']}",
        text,
    )
    text = re.sub(
        r"(?m)^- Manually excluded: \d+\s*$",
        f"- Manually excluded: {counts['EXCLUDED']}",
        text,
    )
    return text


def apply_actions(
    summary: Path,
    review_csv: Path,
    ledger: Path,
    *,
    source: str,
) -> dict[str, int]:
    decisions = load_ledger(ledger)
    fieldnames, rows = load_review_csv(review_csv)
    if "manual_action" not in fieldnames or "final_decision" not in fieldnames:
        raise ValueError(f"review CSV lacks manual decision columns: {review_csv}")

    current_actions: dict[str, str] = {}
    matched = 0
    changed_facts = 0
    current_ids = {clean(row.get("source_job_id")) for row in rows}

    for row in rows:
        source_job_id = clean(row.get("source_job_id"))
        remembered = decisions.get(source_job_id)
        action = ""
        if remembered:
            if remembered["fingerprint"] == row_fingerprint(row):
                action = remembered["action"]
                matched += 1
            else:
                changed_facts += 1
        row["manual_action"] = action
        row["final_decision"] = final_decision(row.get("classification", ""), action)
        if action:
            current_actions[source_job_id] = action

    write_review_csv(review_csv, fieldnames, rows)

    if not summary.is_file():
        raise ValueError(f"review Markdown not found: {summary}")
    text = summary.read_text(encoding="utf-8-sig")
    text = patch_summary_blocks(text, current_actions)
    text = patch_summary_copy(text, source)
    text = patch_summary_counts(text, rows)
    summary.write_text(text, encoding="utf-8")

    absent = sum(source_job_id not in current_ids for source_job_id in decisions)
    print(
        f"Reapplied {matched} remembered decision(s); "
        f"{changed_facts} current vacancy decision(s) withheld because review facts changed; "
        f"{absent} remembered vacancy/vacancies not present in this review."
    )
    return {
        "reapplied": matched,
        "changed_facts": changed_facts,
        "absent": absent,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture = subparsers.add_parser("capture")
    capture.add_argument("--summary", type=Path, required=True)
    capture.add_argument("--csv", dest="review_csv", type=Path, required=True)
    capture.add_argument("--ledger", type=Path, required=True)

    apply = subparsers.add_parser("apply")
    apply.add_argument("--summary", type=Path, required=True)
    apply.add_argument("--csv", dest="review_csv", type=Path, required=True)
    apply.add_argument("--ledger", type=Path, required=True)
    apply.add_argument("--source", choices=("nejobs", "vonne"), required=True)

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "capture":
        capture_actions(args.summary, args.review_csv, args.ledger)
    else:
        apply_actions(
            args.summary,
            args.review_csv,
            args.ledger,
            source=args.source,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
