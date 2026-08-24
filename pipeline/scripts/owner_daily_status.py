"""Build the single owner-facing status for Ontap's daily operating cycle."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date, datetime
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

from review_hub.adapters import load_all_sources
from review_hub.contracts import SourceResult


LONDON = ZoneInfo("Europe/London")
PIPELINE_ROOT = Path(__file__).resolve().parents[1]
MASTER_REVIEW = PIPELINE_ROOT / "reviews/daily/ontap-daily-review.md"

SOURCE_CHECKS = (
    ("jobg8", "JobG8 feed uploaded"),
    ("teaching_vacancies", "Teaching Vacancies fetch"),
    ("nhs", "NHS Jobs fetch"),
    ("nejobs", "NEJobs scrape"),
    ("vonne", "VONNE scrape"),
)
SOURCE_REFRESH_WORKFLOWS = {
    "jobg8": ("Run full JobG8 daily process",),
    "teaching_vacancies": ("Run Teaching Vacancies regional review",),
    "nhs": (
        "Run full JobG8 daily process",
        "Refresh NHS admin/service review",
    ),
    "nejobs": ("Run NEJobs review",),
    "vonne": ("Run VONNE review",),
}

APPLY_WORKFLOW = "Apply and publish Ontap daily review"
SOURCE_PUBLISHERS = (
    "Apply JobG8 review decisions",
    "Build approved NEJobs output",
    "Build approved VONNE output",
    "Publish reviewed Teaching Vacancies England-wide",
    "Publish reviewed NHS admin/service",
)
VERIFIED_WORKFLOW = "Publish verified pages"
DEPLOY_WORKFLOW = "Deploy Ontap production after publish"


@dataclass(frozen=True)
class Run:
    workflow: str
    event: str
    status: str
    conclusion: str
    created_at: datetime
    updated_at: datetime
    url: str

    @classmethod
    def from_mapping(cls, row: dict[str, object]) -> "Run":
        created = _timestamp(str(row.get("createdAt") or ""))
        updated_raw = str(row.get("updatedAt") or "")
        return cls(
            workflow=str(row.get("workflowName") or ""),
            event=str(row.get("event") or ""),
            status=str(row.get("status") or ""),
            conclusion=str(row.get("conclusion") or ""),
            created_at=created,
            updated_at=_timestamp(updated_raw) if updated_raw else created,
            url=str(row.get("url") or ""),
        )


@dataclass(frozen=True)
class DailyStatus:
    markdown: str
    ready: bool
    publish_state: str
    publish_mode: str
    exit_code: int


def _timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _md(value: object) -> str:
    return str(value or "—").replace("|", "\\|").replace("\n", " ").strip()


def _link(label: str, url: str) -> str:
    return f"[{label}]({url})" if url else label


def _today_runs(runs: list[Run], today: date) -> list[Run]:
    return [run for run in runs if run.created_at.astimezone(LONDON).date() == today]


def _latest(
    runs: list[Run],
    workflow: str,
    *,
    event: str | None = None,
    after: datetime | None = None,
    conclusion: str | None = None,
) -> Run | None:
    matches = [
        run
        for run in runs
        if run.workflow == workflow
        and (event is None or run.event == event)
        and (after is None or run.created_at >= after)
        and (conclusion is None or run.conclusion == conclusion)
    ]
    return max(matches, key=lambda run: run.created_at) if matches else None


def _latest_any(runs: list[Run], workflows: tuple[str, ...]) -> Run | None:
    matches = [run for run in runs if run.workflow in workflows]
    return max(matches, key=lambda run: run.created_at) if matches else None


def _master_review_ready(path: Path, today: date) -> tuple[bool, str]:
    if not path.is_file():
        return False, "daily review file is missing"
    text = path.read_text(encoding="utf-8-sig")
    match = re.search(r"(?m)^review_date:\s*(\d{4}-\d{2}-\d{2})\s*$", text)
    review_date = match.group(1) if match else ""
    ready = review_date == today.isoformat() and "> **READY TO REVIEW**" in text
    if ready:
        return True, f"current review dated {review_date}"
    return False, f"review date {review_date or 'missing'}; READY banner not current"


def _live_report(path: Path, today: date) -> tuple[bool, str]:
    if not path.is_file():
        return False, "today's live-source report is missing"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    totals = [
        row
        for row in rows
        if row.get("report_date") == today.isoformat() and row.get("level") == "total"
    ]
    if len(totals) != 1:
        return False, "today's live-source report has no unique total"
    return True, f"{totals[0].get('count', '—')} live jobs recorded"


def _run_result(run: Run | None) -> tuple[str, str]:
    if run is None:
        return "MISSING", "no run found after this publication started"
    label = run.conclusion.upper() if run.conclusion else run.status.upper()
    when = run.updated_at.astimezone(LONDON).strftime("%H:%M")
    return label, _link(f"{when} run", run.url)


def build_status(
    *,
    today: date,
    now: datetime,
    runs: list[Run],
    source_results: list[SourceResult],
    master_review: Path,
    reports_dir: Path,
    require_publish: bool,
) -> DailyStatus:
    runs = _today_runs(runs, today)
    by_key = {result.key: result for result in source_results}
    readiness_rows: list[tuple[str, str, str]] = []
    ready = True
    for key, label in SOURCE_CHECKS:
        result = by_key.get(key)
        ok = result is not None and result.state == "OK"
        ready = ready and ok
        evidence = (
            f"current source review dated {result.review_date}"
            if ok and result
            else (result.note or f"source status is {result.state}")
            if result
            else "source adapter result is missing"
        )
        refresh_run = _latest_any(runs, SOURCE_REFRESH_WORKFLOWS[key])
        if refresh_run:
            refresh_result, refresh_evidence = _run_result(refresh_run)
            evidence += f"; latest refresh {refresh_result}: {refresh_evidence}"
        readiness_rows.append((label, "OK" if ok else "NOT READY", evidence))

    review_ok, review_evidence = _master_review_ready(master_review, today)
    ready = ready and review_ok
    readiness_rows.append(
        ("Daily review file generated", "OK" if review_ok else "NOT READY", review_evidence)
    )
    review_run = _latest_any(runs, ("Ontap daily review",))
    if review_run:
        review_result, run_evidence = _run_result(review_run)
        label, result, evidence = readiness_rows[-1]
        readiness_rows[-1] = (
            label,
            result,
            f"{evidence}; latest workflow {review_result}: {run_evidence}",
        )

    lines = [
        "# Ontap daily status",
        "",
        f"Generated {now.astimezone(LONDON).strftime('%d %B %Y at %H:%M')} UK time.",
        "",
        f"## 1. READY TO EDIT — {'YES' if ready else 'NO'}",
        "",
        "| Daily input | Result | Evidence |",
        "|---|---|---|",
    ]
    lines.extend(
        f"| {_md(label)} | **{result}** | {_md(evidence)} |"
        for label, result, evidence in readiness_rows
    )

    manual = _latest(
        runs,
        APPLY_WORKFLOW,
        event="workflow_dispatch",
        conclusion="success",
    )
    automatic = _latest(
        runs,
        APPLY_WORKFLOW,
        event="schedule",
        conclusion="success",
    )
    if manual:
        anchor = manual
        mode = "MANUAL"
    elif automatic:
        anchor = automatic
        mode = "AUTOMATIC"
    else:
        anchor = None
        mode = ""

    lines.extend(["", "## 2. PUBLISH STATUS"])
    if anchor is None:
        latest_attempt = _latest(runs, APPLY_WORKFLOW)
        if latest_attempt and latest_attempt.status != "completed":
            publish_state = "IN PROGRESS"
            lines.extend(
                [
                    "",
                    "**IN PROGRESS — the daily publish has started but has not completed.**",
                    "",
                    _link("Open the current publish run", latest_attempt.url),
                ]
            )
        elif latest_attempt:
            publish_state = "FAILED"
            lines.extend(
                [
                    "",
                    "**PUBLISH FAILED — today's apply/publish run did not succeed.**",
                    "",
                    _link("Open the failed publish run", latest_attempt.url),
                ]
            )
        else:
            publish_state = "NOT YET PUBLISHED"
            lines.extend(
                [
                    "",
                    "**NOT YET PUBLISHED — no successful manual or automatic publish is recorded today.**",
                ]
            )
        exit_code = 1 if (require_publish or not ready) else 0
        return DailyStatus("\n".join(lines) + "\n", ready, publish_state, mode, exit_code)

    publication_rows: list[tuple[str, str, str]] = []
    source_ok = True
    for workflow in SOURCE_PUBLISHERS:
        run = _latest(runs, workflow, after=anchor.created_at)
        result, evidence = _run_result(run)
        ok = result == "SUCCESS"
        source_ok = source_ok and ok
        publication_rows.append((workflow, "OK" if ok else result, evidence))

    verified = _latest(runs, VERIFIED_WORKFLOW, after=anchor.created_at)
    verified_result, verified_evidence = _run_result(verified)
    verified_ok = verified_result == "SUCCESS"
    publication_rows.append(
        ("Verified pages produced", "OK" if verified_ok else verified_result, verified_evidence)
    )

    deployed = _latest(runs, DEPLOY_WORKFLOW, after=anchor.created_at)
    deploy_result, deploy_evidence = _run_result(deployed)
    deploy_ok = deploy_result == "SUCCESS"
    publication_rows.append(
        ("Production deployment verified", "OK" if deploy_ok else deploy_result, deploy_evidence)
    )

    live_ok, live_evidence = _live_report(
        reports_dir / f"live-job-source-count-{today.isoformat()}.csv",
        today,
    )
    publication_rows.append(
        ("Published source report generated", "OK" if live_ok else "MISSING", live_evidence)
    )

    complete = source_ok and verified_ok and deploy_ok and live_ok
    critical_complete = verified_ok and deploy_ok and live_ok
    completion = (
        (deployed or verified or anchor).updated_at.astimezone(LONDON).strftime("%H:%M")
    )
    if complete:
        publish_state = "PUBLISHED SUCCESSFULLY"
        if mode == "AUTOMATIC":
            headline = (
                f"**PUBLISHED SUCCESSFULLY — automatic publish completed at {completion} "
                "because no successful manual publish was recorded before 11:45.**"
            )
        else:
            headline = f"**PUBLISHED SUCCESSFULLY — manual review published at {completion}.**"
    elif critical_complete:
        publish_state = "PUBLISHED WITH SOURCE HELD"
        headline = (
            "**PUBLISHED WITH A SOURCE HELD — production updated, but at least one "
            "source publisher needs attention.**"
        )
    else:
        publish_state = "PUBLISH INCOMPLETE"
        headline = (
            "**PUBLISH INCOMPLETE — verified pages and production deployment have not "
            "both completed successfully.**"
        )

    lines.extend(
        [
            "",
            headline,
            "",
            f"Publication mode: **{mode}** — {_link('open apply/publish run', anchor.url)}",
            "",
            "| Publication check | Result | Evidence |",
            "|---|---|---|",
        ]
    )
    lines.extend(
        f"| {_md(label)} | **{result}** | {_md(evidence)} |"
        for label, result, evidence in publication_rows
    )

    exit_code = 0 if ready and complete else 1
    return DailyStatus("\n".join(lines) + "\n", ready, publish_state, mode, exit_code)


def _load_runs(path: Path) -> list[Run]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("runs JSON must contain an array")
    return [Run.from_mapping(row) for row in payload]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-json", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--require-publish", action="store_true")
    parser.add_argument("--date", type=date.fromisoformat)
    args = parser.parse_args(argv)

    now = datetime.now().astimezone()
    today = args.date or now.astimezone(LONDON).date()
    status = build_status(
        today=today,
        now=now,
        runs=_load_runs(args.runs_json),
        source_results=load_all_sources(today),
        master_review=MASTER_REVIEW,
        reports_dir=PIPELINE_ROOT / "reports-daily",
        require_publish=args.require_publish,
    )
    with args.summary.open("a", encoding="utf-8") as handle:
        handle.write(status.markdown)
    print(status.markdown)
    if status.exit_code:
        print(f"::error::Ontap daily status requires attention: {status.publish_state}")
    return status.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
