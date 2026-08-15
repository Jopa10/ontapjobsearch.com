"""Persist explicit JobG8 manual review decisions across daily feed dates.

The existing selectors intentionally scope review actions to one feed date.  This
wrapper layer preserves only explicit human ``action: select`` / ``exclude``
choices by JobG8 ``job_id`` and replays them temporarily before each run.

The persisted store lives in a hidden HTML comment at the bottom of the existing
Markdown review file, so the current GitHub Actions commit allow-list does not
need to change.  After the selector runs, visible ``action:`` fields are cleared
again; the hidden store remains the durable source of truth.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .pipeline_refinement import resolve_feed_date

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PIPELINE_ROOT.parent
REVIEW_DIR = PIPELINE_ROOT / "reviews" / "jobg8"
INPUT_DIR = PIPELINE_ROOT / "input"

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
        decisions[str(job_id)] = {
            "action": action,
            "decided_on": str(value.get("decided_on") or ""),
        }
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


def _explicit_actions(text: str) -> dict[str, str]:
    actions: dict[str, str] = {}
    for block in _review_blocks(text):
        action_match = re.search(r"(?m)^action:\s*(select|exclude)\s*$", block, re.I)
        job_match = re.search(r"(?m)^job_id:\s*(\S+)\s*$", block)
        if action_match and job_match:
            actions[job_match.group(1)] = action_match.group(1).lower()
    return actions


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


def prepare(category: str) -> PersistenceRun:
    """Capture new human actions, then seed all persisted actions for this run."""
    if category not in CATEGORY_FILES:
        raise ValueError(f"Unsupported JobG8 review category: {category}")

    review_md, review_csv = CATEGORY_FILES[category]
    current_feed_date = resolve_feed_date(_find_jobg8_file())
    text = review_md.read_text(encoding="utf-8-sig") if review_md.exists() else ""

    decisions = _load_store(text)
    if not decisions:
        decisions = _bootstrap_decisions(category)

    # Only capture visible edits if the review itself belongs to this feed date.
    # This prevents stale generated actions from an older daily file being
    # mistaken for a fresh human judgement.
    if _review_feed_date(text) == current_feed_date:
        for job_id, action in _explicit_actions(text).items():
            decisions[job_id] = {
                "action": action,
                "decided_on": current_feed_date,
            }

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
