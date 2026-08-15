"""Persist explicit JobG8 manual review decisions across daily feed dates.

The existing selectors intentionally scope review actions to one feed date. This
wrapper layer preserves only explicit human ``action: select`` / ``exclude``
choices by JobG8 ``job_id`` and replays them temporarily before each run.

The persisted store lives in a hidden HTML comment at the bottom of each existing
Markdown review file. A combined human-facing ``jobg8-exclusion-list.md`` is
generated from those stores so exclusions can be reviewed, dated, and reversed.
After the selector runs, visible ``action:`` fields are cleared again; the hidden
stores remain the durable source of truth.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from .pipeline_refinement import resolve_feed_date

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PIPELINE_ROOT.parent
REVIEW_DIR = PIPELINE_ROOT / "reviews" / "jobg8"
INPUT_DIR = PIPELINE_ROOT / "input"
EXCLUSION_REPORT_PATH = REVIEW_DIR / "jobg8-exclusion-list.md"

STORE_MARKER = "ONTAP_PERSISTENT_DECISIONS_V1"
STORE_RE = re.compile(
    rf"\n?<!--\s*{STORE_MARKER}\s*\n(.*?)\n-->\s*$",
    flags=re.DOTALL,
)

CATEGORY_FILES = {
    "service_admin": (
        REVIEW_DIR / "service-admin-review.md",
        REVIEW_DIR / "service-admin-review.csv",
    ),
    "support_worker": (
        REVIEW_DIR / "support-worker-review.md",
        REVIEW_DIR / "support-worker-review.csv",
    ),
}

CATEGORY_LABELS = {
    "service_admin": "SERVICE / ADMIN",
    "support_worker": "SUPPORT WORKER",
}

FEED_COLUMNS = {
    "job_id": "/Job/DisplayReference",
    "employer": "/Job/AdvertiserName",
    "title": "/Job/Position",
    "location": "/Job/Location",
}

# One-time bootstrap from the user's explicit review-edit commits immediately
# before persistence was introduced. Later commits win for the same job_id.
BOOTSTRAP_COMMITS = {
    "service_admin": [
        ("2026-08-13", "50089cfc676ea5dd4926d5778c160b4dd14c7e74"),
        ("2026-08-14", "286b5b8134190769d876733877b462ce7608af9c"),
    ],
    "support_worker": [
        ("2026-08-14", "07a3032abcf9f76f3569a31f2ffe0376e9f3b1d4"),
    ],
}


@dataclass
class PersistenceRun:
    category: str
    review_md: Path
    review_csv: Path
    current_feed_date: str
    decisions: dict[str, dict[str, str]]


def _normalise_action(value: Any) -> str:
    action = str(value or "").strip().lower()
    return action if action in {"select", "exclude"} else ""


def _clean(value: Any) -> str:
    text = str(value or "").strip()
    return "" if text.lower() == "nan" else text


def _strip_store(text: str) -> str:
    return STORE_RE.sub("", text).rstrip() + "\n"


def _load_store(text: str) -> dict[str, dict[str, str]]:
    match = STORE_RE.search(text)
    if not match:
        return {}
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError:
        return {}
    raw = payload.get("decisions", {}) if isinstance(payload, dict) else {}
    decisions: dict[str, dict[str, str]] = {}
    if not isinstance(raw, dict):
        return decisions
    for job_id, value in raw.items():
        if not isinstance(value, dict):
            continue
        action = _normalise_action(value.get("action"))
        if not job_id or not action:
            continue
        record = {
            "action": action,
            "decided_on": _clean(value.get("decided_on")),
        }
        for field in ("title", "employer", "region", "town", "salary"):
            cleaned = _clean(value.get(field))
            if cleaned:
                record[field] = cleaned
        decisions[str(job_id)] = record
    return decisions


def _append_store(text: str, decisions: dict[str, dict[str, str]]) -> str:
    text = _strip_store(text).rstrip()
    payload = json.dumps(
        {"version": 1, "decisions": dict(sorted(decisions.items()))},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return f"{text}\n\n<!-- {STORE_MARKER}\n{payload}\n-->\n"


def _review_feed_date(text: str) -> str:
    match = re.search(r"(?m)^feed_date:\s*(\d{4}-\d{2}-\d{2})\s*$", text)
    return match.group(1) if match else ""


def _set_review_feed_date(text: str, feed_date: str) -> str:
    if re.search(r"(?m)^feed_date:\s*.*$", text):
        return re.sub(
            r"(?m)^feed_date:\s*.*$",
            f"feed_date: {feed_date}",
            text,
            count=1,
        )
    lines = text.splitlines()
    insert_at = 1 if lines else 0
    lines[insert_at:insert_at] = ["", f"feed_date: {feed_date}"]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def _review_blocks(text: str) -> list[str]:
    return re.findall(r"(?ms)^---\s*\n(.*?)^---\s*$", text)


def _review_block_metadata(block: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(
            r"^(?:SELECTED|POSS)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*)$",
            line,
        )
        if not match:
            continue
        region, town, salary, title = match.groups()
        metadata.update(
            {
                "region": region.strip(),
                "town": town.strip(),
                "salary": salary.strip(),
                "title": title.strip(),
            }
        )
        break
    return {key: value for key, value in metadata.items() if value}


def _explicit_action_records(text: str) -> dict[str, dict[str, str]]:
    actions: dict[str, dict[str, str]] = {}
    for block in _review_blocks(text):
        action_match = re.search(r"(?m)^action:\s*(select|exclude)\s*$", block, re.I)
        job_match = re.search(r"(?m)^job_id:\s*(\S+)\s*$", block)
        if action_match and job_match:
            actions[job_match.group(1)] = {
                "action": action_match.group(1).lower(),
                **_review_block_metadata(block),
            }
    return actions


def _explicit_actions(text: str) -> dict[str, str]:
    return {
        job_id: value["action"]
        for job_id, value in _explicit_action_records(text).items()
    }


def _apply_actions(text: str, decisions: dict[str, dict[str, str]]) -> str:
    existing_ids: set[str] = set()

    def replace_block(match: re.Match[str]) -> str:
        block = match.group(0)
        job_match = re.search(r"(?m)^job_id:\s*(\S+)\s*$", block)
        if not job_match:
            return block
        job_id = job_match.group(1)
        existing_ids.add(job_id)
        decision = decisions.get(job_id)
        if not decision:
            return block
        action = decision["action"]
        if re.search(r"(?m)^action:.*$", block):
            return re.sub(r"(?m)^action:.*$", f"action: {action}", block, count=1)
        return block

    seeded = re.sub(r"(?ms)^---\s*\n.*?^---\s*$", replace_block, text)

    missing = [
        (job_id, value["action"])
        for job_id, value in decisions.items()
        if job_id not in existing_ids
    ]
    if not missing:
        return seeded

    lines = [
        seeded.rstrip(),
        "",
        "## PERSISTED MANUAL ACTIONS — RUNTIME",
        "",
    ]
    for job_id, action in sorted(missing):
        lines.extend(
            [
                "---",
                f"action: {action}",
                "PERSISTED | | | |",
                f"job_id: {job_id}",
                "---",
                "",
            ]
        )
    return "\n".join(lines)


def _clear_visible_actions(text: str) -> str:
    return re.sub(
        r"(?m)^action:\s*(?:select|exclude)\s*$",
        "action:",
        text,
    )


def _find_jobg8_file() -> Path:
    candidates = [
        path
        for path in INPUT_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".xlsx", ".xls", ".xlsm", ".csv"}
        and ("jobg8" in path.name.lower() or "jobs" in path.name.lower())
    ]
    if len(candidates) == 1:
        return candidates[0]
    preferred = INPUT_DIR / "jobg8.xlsx"
    if preferred.exists():
        return preferred
    raise RuntimeError(
        "Could not identify one current JobG8 input file for persistent review decisions."
    )


def _feed_metadata(path: Path) -> dict[str, dict[str, str]]:
    if path.suffix.lower() == ".csv":
        frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    else:
        frame = pd.read_excel(path, dtype=str, keep_default_na=False)
    job_column = FEED_COLUMNS["job_id"]
    if job_column not in frame.columns:
        return {}

    metadata: dict[str, dict[str, str]] = {}
    for _, row in frame.iterrows():
        job_id = _clean(row.get(job_column))
        if not job_id:
            continue
        record: dict[str, str] = {}
        for key in ("employer", "title", "location"):
            column = FEED_COLUMNS[key]
            if column in frame.columns:
                value = _clean(row.get(column))
                if value:
                    record[key] = value
        metadata[job_id] = record
    return metadata


def _ensure_commit_available(sha: str) -> None:
    present = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if present.returncode == 0:
        return
    subprocess.run(
        ["git", "fetch", "--no-tags", "--depth=1", "origin", sha],
        cwd=REPO_ROOT,
        check=True,
    )


def _actions_from_patch(patch: str) -> dict[str, str]:
    actions: dict[str, str] = {}
    pending = ""
    for raw_line in patch.splitlines():
        line = raw_line[1:] if raw_line[:1] in {"+", "-", " "} else raw_line
        if raw_line.startswith("+action:"):
            pending = _normalise_action(line.split(":", 1)[1])
            continue
        if pending:
            match = re.match(r"\s*job_id:\s*(\S+)\s*$", line)
            if match:
                actions[match.group(1)] = pending
                pending = ""
                continue
        if raw_line.startswith("@@"):
            pending = ""
    return actions


def _bootstrap_decisions(category: str) -> dict[str, dict[str, str]]:
    review_md, _ = CATEGORY_FILES[category]
    relative_review = review_md.relative_to(REPO_ROOT).as_posix()
    decisions: dict[str, dict[str, str]] = {}
    for decided_on, sha in BOOTSTRAP_COMMITS.get(category, []):
        _ensure_commit_available(sha)
        shown = subprocess.run(
            [
                "git",
                "show",
                "--format=",
                "--unified=1",
                sha,
                "--",
                relative_review,
            ],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        for job_id, action in _actions_from_patch(shown.stdout).items():
            decisions[job_id] = {"action": action, "decided_on": decided_on}
    return decisions


def _exclusion_recovery_actions(text: str, category: str) -> dict[str, dict[str, str]]:
    actions: dict[str, dict[str, str]] = {}
    for block in _review_blocks(text):
        category_match = re.search(r"(?m)^category:\s*(\S+)\s*$", block)
        action_match = re.search(r"(?m)^action:\s*select\s*$", block, re.I)
        job_match = re.search(r"(?m)^job_id:\s*(\S+)\s*$", block)
        if not (category_match and action_match and job_match):
            continue
        if category_match.group(1) != category:
            continue
        metadata: dict[str, str] = {"action": "select"}
        for field in ("title", "employer", "region", "town", "salary"):
            field_match = re.search(rf"(?m)^{field}:\s*(.*?)\s*$", block)
            if field_match and field_match.group(1).strip():
                metadata[field] = field_match.group(1).strip()
        actions[job_match.group(1)] = metadata
    return actions


def _merge_decision(
    existing: dict[str, str] | None,
    action_record: dict[str, str],
    decided_on: str,
    feed_record: dict[str, str] | None = None,
) -> dict[str, str]:
    merged = dict(existing or {})
    merged["action"] = action_record["action"]
    merged["decided_on"] = decided_on

    if feed_record:
        if feed_record.get("employer"):
            merged["employer"] = feed_record["employer"]
        if feed_record.get("title") and not action_record.get("title"):
            merged["title"] = feed_record["title"]
        if feed_record.get("location") and not action_record.get("town"):
            merged["town"] = feed_record["location"]

    for field in ("title", "employer", "region", "town", "salary"):
        value = _clean(action_record.get(field))
        if value:
            merged[field] = value
    return merged


def prepare(category: str) -> PersistenceRun:
    """Capture new human actions, then seed all persisted actions for this run."""
    if category not in CATEGORY_FILES:
        raise ValueError(f"Unsupported JobG8 review category: {category}")

    review_md, review_csv = CATEGORY_FILES[category]
    feed_path = _find_jobg8_file()
    current_feed_date = resolve_feed_date(feed_path)
    text = review_md.read_text(encoding="utf-8-sig") if review_md.exists() else ""

    decisions = _load_store(text)
    if not decisions:
        decisions = _bootstrap_decisions(category)

    # A remembered exclusion can be reversed from the combined exclusion list.
    # The reversal is captured before the normal review edits; if the same ID
    # somehow has edits in both places, the normal current review wins.
    if EXCLUSION_REPORT_PATH.exists():
        exclusion_text = EXCLUSION_REPORT_PATH.read_text(encoding="utf-8-sig")
        for job_id, action_record in _exclusion_recovery_actions(
            exclusion_text, category
        ).items():
            decisions[job_id] = _merge_decision(
                decisions.get(job_id),
                action_record,
                current_feed_date,
            )

    # Only capture visible edits if the review itself belongs to this feed date.
    # This prevents stale generated actions from an older daily file being
    # mistaken for a fresh human judgement.
    if _review_feed_date(text) == current_feed_date:
        action_records = _explicit_action_records(text)
        feed_records = _feed_metadata(feed_path) if action_records else {}
        for job_id, action_record in action_records.items():
            decisions[job_id] = _merge_decision(
                decisions.get(job_id),
                action_record,
                current_feed_date,
                feed_records.get(job_id),
            )

    runtime_text = _strip_store(text)
    runtime_text = _set_review_feed_date(runtime_text, current_feed_date)
    runtime_text = _apply_actions(runtime_text, decisions)
    review_md.parent.mkdir(parents=True, exist_ok=True)
    review_md.write_text(runtime_text, encoding="utf-8")

    return PersistenceRun(
        category=category,
        review_md=review_md,
        review_csv=review_csv,
        current_feed_date=current_feed_date,
        decisions=decisions,
    )


def _clear_csv_actions(path: Path) -> None:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if not fieldnames:
        return
    changed = False
    for row in rows:
        for field in ("manual_override", "manual_select"):
            if field in row and row.get(field):
                row[field] = ""
                changed = True
    if not changed:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def finalize(run: PersistenceRun) -> None:
    """Return the review files to clean human-facing form and persist the store."""
    if run.review_md.exists():
        text = run.review_md.read_text(encoding="utf-8-sig")
        text = _clear_visible_actions(_strip_store(text))
        text = _append_store(text, run.decisions)
        run.review_md.write_text(text, encoding="utf-8")
    _clear_csv_actions(run.review_csv)


def _load_category_store(category: str) -> dict[str, dict[str, str]]:
    review_md, _ = CATEGORY_FILES[category]
    if not review_md.exists():
        return {}
    return _load_store(review_md.read_text(encoding="utf-8-sig"))


def _report_value(value: Any) -> str:
    return _clean(value).replace("\n", " ").replace("\r", " ")


def render_exclusion_report(
    category_decisions: dict[str, dict[str, dict[str, str]]],
) -> str:
    total = sum(
        1
        for decisions in category_decisions.values()
        for record in decisions.values()
        if record.get("action") == "exclude"
    )
    lines = [
        "# JobG8 exclusion list",
        "",
        "This is the durable list of jobs explicitly excluded during manual review.",
        "The `excluded_on` date is the day the exclusion decision was made.",
        "",
        "To restore a job, edit only its `action:` line to `action: select`.",
        "On the next JobG8 run that exact job ID will be restored and removed from this list.",
        "",
        f"remembered_exclusions: {total}",
        "",
    ]

    for category in ("service_admin", "support_worker"):
        label = CATEGORY_LABELS[category]
        excluded = [
            (job_id, record)
            for job_id, record in category_decisions.get(category, {}).items()
            if record.get("action") == "exclude"
        ]
        excluded.sort(
            key=lambda item: (
                item[1].get("decided_on", ""),
                item[1].get("title", ""),
                item[0],
            ),
            reverse=True,
        )
        lines.extend([f"## {label} — EXCLUDED", ""])
        if not excluded:
            lines.extend(["No remembered exclusions.", ""])
            continue
        for job_id, record in excluded:
            lines.extend(
                [
                    "---",
                    "action:",
                    f"category: {category}",
                    f"excluded_on: {_report_value(record.get('decided_on'))}",
                    f"title: {_report_value(record.get('title'))}",
                    f"employer: {_report_value(record.get('employer'))}",
                    f"region: {_report_value(record.get('region'))}",
                    f"town: {_report_value(record.get('town'))}",
                    f"salary: {_report_value(record.get('salary'))}",
                    f"job_id: {job_id}",
                    "---",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def refresh_exclusion_report() -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    category_decisions = {
        category: _load_category_store(category)
        for category in CATEGORY_FILES
    }
    EXCLUSION_REPORT_PATH.write_text(
        render_exclusion_report(category_decisions),
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Refresh the combined persistent JobG8 exclusion list."
    )
    parser.add_argument(
        "--refresh-exclusion-report",
        action="store_true",
        help="Regenerate jobg8-exclusion-list.md from the persistent decision stores.",
    )
    args = parser.parse_args(argv)
    if not args.refresh_exclusion_report:
        parser.error("--refresh-exclusion-report is required")
    refresh_exclusion_report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
