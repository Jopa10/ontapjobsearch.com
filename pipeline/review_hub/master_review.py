from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, datetime
import json
from pathlib import Path
import re
from typing import Iterable

from .adapters import PIPELINE_ROOT, load_all_sources
from .contracts import ParsedDecision, ReviewItem, SourceResult, VALID_ACTIONS, clean

DEFAULT_MASTER = PIPELINE_ROOT / "reviews/daily/ontap-daily-review.md"
MAX_JOB_LEVEL_QUARANTINE_PER_SOURCE = 15
UNRESOLVED_POLICIES = {"quarantine", "withhold"}


def _md(value: object) -> str:
    return clean(value).replace("|", "\\|")


def _field(block: str, key: str) -> str:
    match = re.search(
        rf"(?mi)^{re.escape(key)}:[ \t]*(.*?)[ \t]*$",
        block,
    )
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


def master_text(
    results: Iterable[SourceResult],
    *,
    today: date,
    previous: Path | None = None,
) -> str:
    results = list(results)
    carried = _existing_actions(previous) if previous else {}
    total = sum(len(result.items) for result in results if result.state == "OK")
    attention = [result for result in results if result.needs_attention]
    waiting_for = ", ".join(result.label for result in attention)
    lines = [
        "# Ontap daily job review",
        "",
    ]
    if attention:
        lines.extend(
            [
                f"> **NOT READY TO REVIEW — waiting for: {waiting_for}**",
                "> Do not start reviewing yet. Rebuild this review after those source refreshes complete.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "> **READY TO REVIEW**",
                f"> All active sources are current for {today.isoformat()}. You can start reviewing.",
                "",
            ]
        )
    lines.extend(
        [
            f"review_date: {today.isoformat()}",
            f"generated_at: {datetime.now().astimezone().isoformat(timespec='seconds')}",
            "",
            f"**{total} job(s) need a human decision.**",
            "",
            "Edit only each `action:` line:",
            "- `action: select` = include the vacancy.",
            "- `action: exclude` = reject the vacancy.",
            "- Leave `action:` blank while you are still deciding it.",
            f"- Up to {MAX_JOB_LEVEL_QUARANTINE_PER_SOURCE} unresolved/bad action rows per source are fail-closed at job level: those jobs are withheld and flagged while the rest of that source can continue.",
            f"- More than {MAX_JOB_LEVEL_QUARANTINE_PER_SOURCE} unresolved/bad action rows in one source isolate that source from the run; they do not block other clean sources.",
            "- Unchanged decisions are remembered by the source pipelines; they should not keep returning here.",
            "- If the vacancy facts change, its fingerprint changes and it must be reviewed again.",
            "",
            "## Source status",
            "",
            "| Source | Status | Review date | Needs review | Note |",
            "|---|---|---|---:|---|",
        ]
    )
    for result in results:
        lines.append(
            f"| {_md(result.label)} | {result.state} | {result.review_date or '—'} | "
            f"{len(result.items) if result.state == 'OK' else 0} | {_md(result.note) or '—'} |"
        )
    lines.append("")
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
        for item in sorted(
            result.items,
            key=lambda x: (
                x.region.casefold(),
                x.location.casefold(),
                x.title.casefold(),
                x.source_job_id,
            ),
        ):
            action = carried.get(_item_key(result.key, item), "")
            headline = " | ".join(
                (
                    "POSS",
                    _md(result.label),
                    _md(item.region) or "—",
                    _md(item.location) or "—",
                    _md(item.salary) or "—",
                    _md(item.title),
                )
            )
            lines.extend(
                [
                    "---",
                    f"action: {action}" if action else "action:",
                    headline,
                    f"source_key: {result.key}",
                    f"source: {clean(item.source)}",
                    f"category: {clean(item.category)}",
                    f"source_job_id: {clean(item.source_job_id)}",
                    f"title: {clean(item.title)}",
                    f"employer: {clean(item.employer)}",
                    f"location: {clean(item.location)}",
                    f"region: {clean(item.region)}",
                    f"salary: {clean(item.salary)}",
                    f"closing_date: {clean(item.closing_date)}",
                    f"reason: {clean(item.reason)}",
                    f"source_url: {clean(item.source_url)}",
                    f"hub_fingerprint: {item.fingerprint()}",
                    "---",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def build_master(
    path: Path = DEFAULT_MASTER,
    *,
    today: date | None = None,
) -> dict[str, object]:
    today = today or date.today()
    results = load_all_sources(today)
    attention = [result for result in results if result.needs_attention]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        master_text(results, today=today, previous=path),
        encoding="utf-8",
    )
    return {
        "review_date": today.isoformat(),
        "review_count": sum(
            len(result.items) for result in results if result.state == "OK"
        ),
        "ready_to_review": not attention,
        "waiting_for": [result.label for result in attention],
        "attention_sources": [result.key for result in attention],
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
    date_match = re.search(
        r"(?m)^review_date:[ \t]*(\d{4}-\d{2}-\d{2})[ \t]*$",
        text,
    )
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
            action = ""
        item = ReviewItem(
            source=_field(block, "source"),
            source_job_id=source_job_id,
            title=_field(block, "title"),
            employer=_field(block, "employer"),
            location=_field(block, "location"),
            region=_field(block, "region"),
            category=_field(block, "category"),
            salary=_field(block, "salary"),
            closing_date=_field(block, "closing_date"),
            reason=_field(block, "reason"),
            source_url=_field(block, "source_url"),
        )
        fingerprint = _field(block, "hub_fingerprint")
        if not item.title or not fingerprint:
            raise ValueError(
                f"incomplete master review facts for {source_key}/{source_job_id}"
            )
        key = (source_key, item.category, item.source_job_id)
        if key in seen:
            raise ValueError(f"duplicate master review item: {key}")
        seen.add(key)
        parsed.append(ParsedDecision(action, source_key, item, fingerprint))
    return date_match.group(1), parsed


def _patch_action(
    path: Path,
    id_field: str,
    source_job_id: str,
    action: str,
) -> None:
    if not path.is_file():
        raise ValueError(f"source review Markdown missing: {path}")
    text = path.read_text(encoding="utf-8-sig")
    matched = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal matched
        block = match.group(1)
        id_match = re.search(
            rf"(?mi)^{re.escape(id_field)}:[ \t]*(\S+)[ \t]*$",
            block,
        )
        if not id_match or clean(id_match.group(1)) != source_job_id:
            return match.group(0)
        if not re.search(
            r"(?mi)^action:[ \t]*(?:select|exclude)?[ \t]*$",
            block,
        ):
            raise ValueError(
                f"review block has no editable action line: {source_job_id}"
            )
        matched += 1
        block = re.sub(
            r"(?mi)^action:[ \t]*(?:select|exclude)?[ \t]*$",
            f"action: {action}",
            block,
            count=1,
        )
        return f"---\n{block}---"

    updated = re.sub(
        r"(?ms)^---\s*$\n(.*?)^---\s*$",
        replace,
        text,
    )
    if matched != 1:
        raise ValueError(
            f"expected one source review block for {source_job_id}; found {matched}"
        )
    path.write_text(updated, encoding="utf-8")


def _route_action(decision: ParsedDecision) -> None:
    if decision.source_key == "jobg8":
        if decision.item.category == "admin_service":
            path = PIPELINE_ROOT / "reviews/jobg8/service-admin-review.md"
        elif decision.item.category == "support_worker":
            path = PIPELINE_ROOT / "reviews/jobg8/support-worker-review.md"
        else:
            raise ValueError(
                f"unsupported JobG8 category: {decision.item.category}"
            )
        _patch_action(path, "job_id", decision.item.source_job_id, decision.action)
        return
    routes = {
        "nejobs": (
            PIPELINE_ROOT / "reviews/external/northeast-jobs-summary.md",
            "source_job_id",
        ),
        "vonne": (
            PIPELINE_ROOT / "reviews/external/vonne-summary.md",
            "source_job_id",
        ),
        "teaching_vacancies": (
            PIPELINE_ROOT
            / "reviews/external/teaching-vacancies/england-wide-admin-service-summary.md",
            "source_job_id",
        ),
        "nhs": (
            PIPELINE_ROOT / "reviews/external/nhs-jobs-summary.md",
            "source_job_id",
        ),
    }
    if decision.source_key not in routes:
        raise ValueError(
            f"source {decision.source_key!r} has no enabled decision adapter"
        )
    path, id_field = routes[decision.source_key]
    _patch_action(path, id_field, decision.item.source_job_id, decision.action)


def apply_master(
    path: Path = DEFAULT_MASTER,
    *,
    today: date | None = None,
    write: bool = False,
    plan_path: Path | None = None,
    require_complete: bool = False,
    unresolved_policy: str = "quarantine",
) -> dict[str, object]:
    today = today or date.today()
    if unresolved_policy not in UNRESOLVED_POLICIES:
        raise ValueError(
            f"unsupported unresolved policy: {unresolved_policy}"
        )
    review_date, decisions = parse_master(path)
    if review_date != today.isoformat():
        raise ValueError(
            f"master review is stale: {review_date}; expected {today.isoformat()}"
        )

    unresolved = [decision for decision in decisions if not decision.action]
    if unresolved_policy == "quarantine":
        unresolved_counts = Counter(
            decision.source_key for decision in unresolved
        )
        isolated_sources = {
            source
            for source, count in unresolved_counts.items()
            if count > MAX_JOB_LEVEL_QUARANTINE_PER_SOURCE
        }
        quarantined = [
            decision
            for decision in unresolved
            if decision.source_key not in isolated_sources
        ]
        withheld: list[ParsedDecision] = []
    else:
        # The scheduled day-off path must not turn an untouched review queue
        # into remembered exclusions or retain an entire source merely because
        # it has more than 15 pending decisions. Source publishers already
        # omit blank actions fail-closed, so leave them untouched for a later
        # review while refreshing each source's clean/automatic inventory.
        isolated_sources = set()
        quarantined = []
        withheld = unresolved

    del require_complete

    results = load_all_sources(today)
    by_key = {result.key: result for result in results}
    current = {
        (result.key, item.category, item.source_job_id): item
        for result in results
        if result.state == "OK"
        for item in result.items
    }
    acted = [
        decision
        for decision in decisions
        if decision.action and decision.source_key not in isolated_sources
    ]
    for decision in acted:
        result = by_key.get(decision.source_key)
        if result is None or result.state != "OK":
            isolated_sources.add(decision.source_key)
            continue
        key = (
            decision.source_key,
            decision.item.category,
            decision.item.source_job_id,
        )
        live_item = current.get(key)
        if live_item is None or decision.fingerprint != live_item.fingerprint():
            isolated_sources.add(decision.source_key)

    if isolated_sources:
        acted = [d for d in acted if d.source_key not in isolated_sources]
        quarantined = [d for d in quarantined if d.source_key not in isolated_sources]
        withheld = [d for d in withheld if d.source_key not in isolated_sources]

    quarantine_excludes = [
        ParsedDecision(
            "exclude",
            decision.source_key,
            decision.item,
            decision.fingerprint,
        )
        for decision in quarantined
    ]

    if write:
        for decision in acted:
            _route_action(decision)
        for decision in quarantine_excludes:
            _route_action(decision)

    publish_sources = [
        result
        for result in results
        if result.state == "OK"
        and result.publish_workflow
        and result.key not in isolated_sources
    ]
    plan = {
        "review_date": review_date,
        "review_items": len(decisions),
        "actions": len(acted),
        "selected": sum(d.action == "select" for d in acted),
        "excluded": sum(d.action == "exclude" for d in acted),
        "unresolved_policy": unresolved_policy,
        "quarantined": len(quarantine_excludes),
        "quarantined_jobs": [
            {
                "source": decision.source_key,
                "source_job_id": decision.item.source_job_id,
                "title": decision.item.title,
                "reason": "blank or invalid action; withheld fail-closed",
            }
            for decision in quarantined
        ],
        "withheld": len(withheld),
        "withheld_jobs": [
            {
                "source": decision.source_key,
                "source_job_id": decision.item.source_job_id,
                "title": decision.item.title,
                "reason": (
                    "blank or invalid action; withheld for this publication "
                    "without recording an exclusion"
                ),
            }
            for decision in withheld
        ],
        "isolated_sources": sorted(isolated_sources),
        "complete": len(unresolved) == 0,
        "publish": [
            {
                "source": result.key,
                "workflow": result.publish_workflow,
                "approval": result.publish_requires_approval,
                "shared_publish_after": result.shared_publish_after,
            }
            for result in publish_sources
        ],
        "attention_sources": [
            result.key for result in results if result.needs_attention
        ],
    }
    if plan_path:
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(
            json.dumps(plan, indent=2) + "\n",
            encoding="utf-8",
        )
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
    apply.add_argument("--require-complete", action="store_true")
    apply.add_argument(
        "--unresolved-policy",
        choices=sorted(UNRESOLVED_POLICIES),
        default="quarantine",
        help=(
            "quarantine blanks as explicit exclusions under the normal manual "
            "threshold, or withhold them without persisting a decision"
        ),
    )
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            report = build_master(args.output)
        else:
            report = apply_master(
                args.input,
                write=args.write,
                plan_path=args.plan,
                require_complete=args.require_complete,
                unresolved_policy=args.unresolved_policy,
            )
    except ValueError as exc:
        raise SystemExit(f"STOP: {exc}") from exc
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
