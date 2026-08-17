from __future__ import annotations

import argparse
from datetime import date, datetime
import json
from pathlib import Path
import re
from typing import Iterable

from .adapters import PIPELINE_ROOT, load_all_sources
from .contracts import ParsedDecision, ReviewItem, SourceResult, VALID_ACTIONS, clean

DEFAULT_MASTER = PIPELINE_ROOT / "reviews/daily/ontap-daily-review.md"


def _md(value: object) -> str:
    return clean(value).replace("|", "\\|")


def _field(block: str, key: str) -> str:
    match = re.search(rf"(?mi)^{re.escape(key)}:\s*(.*?)\s*$", block)
    return clean(match.group(1)) if match else ""


def _blocks(text: str) -> list[str]:
    return re.findall(r"(?ms)^---\s*$\n(.*?)^---\s*$", text)


def _existing_actions(path: Path) -> dict[tuple[str, str, str, str], str]:
    if not path.is_file():
        return {}
    actions: dict[tuple[str, str, str, str], str] = {}
    for block in _blocks(path.read_text(encoding="utf-8-sig")):
        action = _field(block, "action").casefold()
        if action not in {"select", "exclude"}:
            continue
        key = (
            _field(block, "source_key"),
            _field(block, "category"),
            _field(block, "source_job_id"),
            _field(block, "hub_fingerprint"),
        )
        if all(key):
            actions[key] = action
    return actions


def _item_key(source_key: str, item: ReviewItem) -> tuple[str, str, str, str]:
    return (source_key, item.category, item.source_job_id, item.fingerprint())


def master_text(results: Iterable[SourceResult], *, today: date, previous: Path | None = None) -> str:
    results = list(results)
    carried = _existing_actions(previous) if previous else {}
    total = sum(len(result.items) for result in results if result.state == "OK")
    attention = [result for result in results if result.needs_attention]
    lines = [
        "# Ontap daily job review",
        "",
        f"review_date: {today.isoformat()}",
        f"generated_at: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        f"**{total} job(s) need a human decision.**",
        "",
        "Edit only each `action:` line:",
        "- `action: select` = include the vacancy.",
        "- `action: exclude` = reject the vacancy.",
        "- Leave `action:` blank if you are not deciding it yet.",
        "- Unchanged decisions are remembered by the source pipelines; they should not keep returning here.",
        "- If the vacancy facts change, its fingerprint changes and it must be reviewed again.",
        "",
        "## Source status",
        "",
        "| Source | Status | Review date | Needs review | Note |",
        "|---|---|---|---:|---|",
    ]
    for result in results:
        lines.append(
            f"| {_md(result.label)} | {result.state} | {result.review_date or '—'} | "
            f"{len(result.items) if result.state == 'OK' else 0} | {_md(result.note) or '—'} |"
        )
    lines.extend([""])
    if attention:
        lines.extend(
            [
                "> **Attention:** one or more active source reviews are stale or missing. "
                "Those sources contribute no jobs to this file and must not be treated as zero inventory.",
                "",
            ]
        )

    for result in results:
        if result.state != "OK":
            continue
        lines.extend([f"## {result.label} — {len(result.items)} to review", ""])
        if not result.items:
            lines.extend(["_No new or changed human decisions required._", ""])
            continue
        ordered = sorted(
            result.items,
            key=lambda item: (
                item.region.casefold(),
                item.location.casefold(),
                item.title.casefold(),
                item.source_job_id,
            ),
        )
        for item in ordered:
            action = carried.get(_item_key(result.key, item), "")
            headline = " | ".join(
                value
                for value in (
                    "POSS",
                    result.label,
                    _md(item.region),
                    _md(item.location),
                    _md(item.salary),
                    _md(item.title),
                )
                if value
            )
            lines.extend(
                [
                    "---",
                    f"action: {action}" if action else "action:",
                    headline,
                    f"source_key: {result.key}",
                    f"source: {_md(item.source)}",
                    f"category: {_md(item.category)}",
                    f"source_job_id: {_md(item.source_job_id)}",
                    f"employer: {_md(item.employer)}",
                    f"closing_date: {_md(item.closing_date)}",
                    f"reason: {_md(item.reason)}",
                    f"source_url: {_md(item.source_url)}",
                    f"hub_fingerprint: {item.fingerprint()}",
                    "---",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def build_master(path: Path = DEFAULT_MASTER, *, today: date | None = None) -> dict[str, object]:
    today = today or date.today()
    results = load_all_sources(today)
    text = master_text(results, today=today, previous=path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return {
        "review_date": today.isoformat(),
        "review_count": sum(len(result.items) for result in results if result.state == "OK"),
        "attention_sources": [result.key for result in results if result.needs_attention],
        "sources": [
            {
                "key": result.key,
                "label": result.label,
                "state": result.state,
                "review_date": result.review_date,
                "review_count": len(result.items) if result.state == "OK" else 0,
            }
            for result in results
        ],
    }


def parse_master(path: Path = DEFAULT_MASTER) -> tuple[str, list[ParsedDecision]]:
    if not path.is_file():
        raise ValueError(f"master review not found: {path}")
    text = path.read_text(encoding="utf-8-sig")
    date_match = re.search(r"(?m)^review_date:\s*(\d{4}-\d{2}-\d{2})\s*$", text)
    if not date_match:
        raise ValueError("master review has no review_date")
    parsed: list[ParsedDecision] = []
    seen: set[tuple[str, str, str]] = set()
    for block in _blocks(text):
        source_key = _field(block, "source_key")
        source_job_id = _field(block, "source_job_id")
        if not source_key or not source_job_id:
            continue
        action = _field(block, "action").casefold()
        if action not in VALID_ACTIONS:
            raise ValueError(f"invalid action for {source_key}/{source_job_id}: {action!r}")
        item = ReviewItem(
            source=_field(block, "source"),
            source_job_id=source_job_id,
            title=_headline_title(block),
            employer=_field(block, "employer"),
            location=_headline_part(block, -3),
            region=_headline_part(block, -4),
            category=_field(block, "category"),
            salary=_headline_part(block, -2),
            closing_date=_field(block, "closing_date"),
            reason=_field(block, "reason"),
            source_url=_field(block, "source_url"),
        )
        fingerprint = _field(block, "hub_fingerprint")
        key = (source_key, item.category, item.source_job_id)
        if key in seen:
            raise ValueError(f"duplicate master review item: {key}")
        seen.add(key)
        parsed.append(ParsedDecision(action, source_key, item, fingerprint))
    return date_match.group(1), parsed


def _headline(block: str) -> list[str]:
    line = next((clean(line) for line in block.splitlines() if clean(line).startswith("POSS |")), "")
    return [clean(part.replace("\\|", "|")) for part in line.split("|")] if line else []


def _headline_title(block: str) -> str:
    parts = _headline(block)
    return parts[-1] if parts else ""


def _headline_part(block: str, position: int) -> str:
    parts = _headline(block)
    try:
        return parts[position]
    except IndexError:
        return ""


def _patch_action(path: Path, id_field: str, source_job_id: str, action: str) -> None:
    if not path.is_file():
        raise ValueError(f"source review Markdown missing: {path}")
    text = path.read_text(encoding="utf-8-sig")
    matched = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal matched
        block = match.group(1)
        id_match = re.search(rf"(?mi)^{re.escape(id_field)}:\s*(\S+)\s*$", block)
        if not id_match or clean(id_match.group(1)) != source_job_id:
            return match.group(0)
        if not re.search(r"(?mi)^action:\s*(?:select|exclude)?\s*$", block):
            raise ValueError(f"review block has no editable action line: {source_job_id}")
        matched += 1
        block = re.sub(
            r"(?mi)^action:\s*(?:select|exclude)?\s*$",
            f"action: {action}",
            block,
            count=1,
        )
        return f"---\n{block}---"

    updated = re.sub(r"(?ms)^---\s*$\n(.*?)^---\s*$", replace, text)
    if matched != 1:
        raise ValueError(f"expected one source review block for {source_job_id}; found {matched}")
    path.write_text(updated, encoding="utf-8")


def _route_action(decision: ParsedDecision) -> None:
    if decision.source_key == "jobg8":
        if decision.item.category == "admin_service":
            path = PIPELINE_ROOT / "reviews/jobg8/service-admin-review.md"
        elif decision.item.category == "support_worker":
            path = PIPELINE_ROOT / "reviews/jobg8/support-worker-review.md"
        else:
            raise ValueError(f"unsupported JobG8 category: {decision.item.category}")
        _patch_action(path, "job_id", decision.item.source_job_id, decision.action)
    elif decision.source_key == "nejobs":
        _patch_action(
            PIPELINE_ROOT / "reviews/external/northeast-jobs-summary.md",
            "source_job_id",
            decision.item.source_job_id,
            decision.action,
        )
    elif decision.source_key == "vonne":
        _patch_action(
            PIPELINE_ROOT / "reviews/external/vonne-summary.md",
            "source_job_id",
            decision.item.source_job_id,
            decision.action,
        )
    elif decision.source_key == "teaching_vacancies":
        _patch_action(
            PIPELINE_ROOT / "reviews/external/teaching-vacancies/england-wide-admin-service-summary.md",
            "source_job_id",
            decision.item.source_job_id,
            decision.action,
        )
    else:
        raise ValueError(f"source {decision.source_key!r} has no enabled decision adapter")


def apply_master(
    path: Path = DEFAULT_MASTER,
    *,
    today: date | None = None,
    write: bool = False,
    plan_path: Path | None = None,
) -> dict[str, object]:
    today = today or date.today()
    review_date, decisions = parse_master(path)
    if review_date != today.isoformat():
        raise ValueError(f"master review is stale: {review_date}; expected {today.isoformat()}")

    results = load_all_sources(today)
    by_key = {result.key: result for result in results}
    current: dict[tuple[str, str, str], ReviewItem] = {}
    for result in results:
        if result.state != "OK":
            continue
        for item in result.items:
            current[(result.key, item.category, item.source_job_id)] = item

    acted = [decision for decision in decisions if decision.action]
    for decision in acted:
        result = by_key.get(decision.source_key)
        if result is None or result.state != "OK":
            raise ValueError(f"source {decision.source_key} is not current and cannot be applied")
        key = (decision.source_key, decision.item.category, decision.item.source_job_id)
        live_item = current.get(key)
        if live_item is None:
            raise ValueError(f"review item is no longer unresolved/current: {key}")
        if not decision.fingerprint or decision.fingerprint != live_item.fingerprint():
            raise ValueError(f"vacancy facts changed since review for {decision.source_key}/{decision.item.source_job_id}")

    if write:
        for decision in acted:
            _route_action(decision)

    publish_sources = [
        result
        for result in results
        if result.state == "OK" and result.publish_workflow
    ]
    plan = {
        "review_date": review_date,
        "actions": len(acted),
        "selected": sum(decision.action == "select" for decision in acted),
        "excluded": sum(decision.action == "exclude" for decision in acted),
        "publish": [
            {
                "source": result.key,
                "workflow": result.publish_workflow,
                "approval": result.publish_requires_approval,
                "shared_publish_after": result.shared_publish_after,
            }
            for result in publish_sources
        ],
        "attention_sources": [result.key for result in results if result.needs_attention],
    }
    if plan_path:
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    return plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("--output", type=Path, default=DEFAULT_MASTER)
    apply = sub.add_parser("apply")
    apply.add_argument("--input", type=Path, default=DEFAULT_MASTER)
    apply.add_argument("--write", action="store_true")
    apply.add_argument("--plan", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            report = build_master(args.output)
        else:
            report = apply_master(args.input, write=args.write, plan_path=args.plan)
    except ValueError as exc:
        raise SystemExit(f"STOP: {exc}") from exc
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
