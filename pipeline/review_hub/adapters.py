from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
import re
from typing import Callable

from .contracts import ReviewItem, SourceResult, clean, item_from_mapping

PIPELINE_ROOT = Path(__file__).resolve().parents[1]


def _csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _metadata_date(path: Path, field: str = "review_date") -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8-sig")
    match = re.search(
        rf"(?m)^{re.escape(field)}:\s*(\d{{4}}-\d{{2}}-\d{{2}})\s*$",
        text,
    )
    return match.group(1) if match else ""


def _visible_actions(path: Path, id_field: str) -> dict[str, str]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8-sig")
    actions: dict[str, str] = {}
    for block in re.findall(r"(?ms)^---\s*$\n(.*?)^---\s*$", text):
        id_match = re.search(
            rf"(?mi)^{re.escape(id_field)}:\s*(\S+)\s*$",
            block,
        )
        action_match = re.search(
            r"(?mi)^action:\s*(select|exclude)?\s*$",
            block,
        )
        if not id_match or not action_match:
            continue
        action = clean(action_match.group(1)).casefold()
        actions[clean(id_match.group(1))] = action
    return actions


def _state(review_date: str, today: date) -> str:
    if not review_date:
        return "MISSING"
    return "OK" if review_date == today.isoformat() else "STALE"


def load_jobg8(today: date) -> SourceResult:
    specs = (
        (
            "admin_service",
            PIPELINE_ROOT / "reviews/jobg8/service-admin-review.csv",
            PIPELINE_ROOT / "reviews/jobg8/service-admin-review.md",
        ),
        (
            "support_worker",
            PIPELINE_ROOT / "reviews/jobg8/support-worker-review.csv",
            PIPELINE_ROOT / "reviews/jobg8/support-worker-review.md",
        ),
    )
    items: list[ReviewItem] = []
    dates: set[str] = set()
    try:
        for category, csv_path, md_path in specs:
            rows = _csv_rows(csv_path)
            actions = _visible_actions(md_path, "job_id")
            dates.update(
                clean(row.get("feed_date"))
                for row in rows
                if clean(row.get("feed_date"))
            )
            for row in rows:
                decision = clean(row.get("decision")).upper()
                job_id = clean(row.get("job_id"))
                if not decision.startswith("POSS") or actions.get(job_id):
                    continue
                items.append(
                    item_from_mapping(
                        "JobG8",
                        row,
                        source_job_id=job_id,
                        category=category,
                        reason="JobG8 selector marked this vacancy POSS",
                    )
                )
    except FileNotFoundError as exc:
        return SourceResult(
            "jobg8",
            "JobG8",
            "MISSING",
            "",
            note=f"missing {exc.args[0]}",
            publish_workflow="apply-jobg8-review-decisions.yml",
            shared_publish_after=True,
        )
    review_date = next(iter(dates)) if len(dates) == 1 else ""
    state = _state(review_date, today) if len(dates) <= 1 else "STALE"
    if state != "OK":
        items = []
    return SourceResult(
        "jobg8",
        "JobG8",
        state,
        review_date,
        tuple(items),
        publish_workflow="apply-jobg8-review-decisions.yml",
        shared_publish_after=True,
    )


def load_nejobs(today: date) -> SourceResult:
    csv_path = PIPELINE_ROOT / "reviews/external/northeast-jobs-review.csv"
    md_path = PIPELINE_ROOT / "reviews/external/northeast-jobs-summary.md"
    review_date = _metadata_date(md_path)
    state = _state(review_date, today)
    try:
        rows = _csv_rows(csv_path)
    except FileNotFoundError:
        return SourceResult(
            "nejobs",
            "NEJobs",
            "MISSING",
            review_date,
            publish_workflow="build-approved-nejobs-output.yml",
            publish_requires_approval=True,
            shared_publish_after=True,
        )
    items = []
    if state == "OK":
        for row in rows:
            if (
                clean(row.get("final_decision")).upper() != "POSS"
                or clean(row.get("manual_action"))
            ):
                continue
            items.append(
                item_from_mapping("NEJobs", row, category="admin_service")
            )
    return SourceResult(
        "nejobs",
        "NEJobs",
        state,
        review_date,
        tuple(items),
        publish_workflow="build-approved-nejobs-output.yml",
        publish_requires_approval=True,
        shared_publish_after=True,
    )


def load_vonne(today: date) -> SourceResult:
    csv_path = PIPELINE_ROOT / "reviews/external/vonne-review.csv"
    md_path = PIPELINE_ROOT / "reviews/external/vonne-summary.md"
    review_date = _metadata_date(md_path)
    state = _state(review_date, today)
    try:
        rows = _csv_rows(csv_path)
    except FileNotFoundError:
        return SourceResult(
            "vonne",
            "VONNE",
            "MISSING",
            review_date,
            publish_workflow="build-approved-vonne-output.yml",
            publish_requires_approval=True,
            shared_publish_after=True,
        )
    items = []
    if state == "OK":
        for row in rows:
            if (
                clean(row.get("final_decision")).upper() != "POSS"
                or clean(row.get("manual_action"))
            ):
                continue
            items.append(
                item_from_mapping("VONNE", row, category="admin_service")
            )
    return SourceResult(
        "vonne",
        "VONNE",
        state,
        review_date,
        tuple(items),
        publish_workflow="build-approved-vonne-output.yml",
        publish_requires_approval=True,
        shared_publish_after=True,
    )


def _latest_tv_review_date() -> str:
    review_dir = PIPELINE_ROOT / "reviews/external/teaching-vacancies"
    dates = {
        _metadata_date(path)
        for path in review_dir.glob("*-admin-service-summary.md")
        if path.name != "england-wide-admin-service-summary.md"
    }
    dates.discard("")
    return max(dates) if dates else ""


def _tv_review_date(today: date) -> str:
    routing_summary = (
        PIPELINE_ROOT
        / "manifests/external/teaching-vacancies"
        / f"teaching-vacancies-routing-{today.isoformat()}-summary.json"
    )
    if routing_summary.is_file() and routing_summary.stat().st_size > 0:
        return today.isoformat()
    return _latest_tv_review_date()


def load_teaching_vacancies(today: date) -> SourceResult:
    csv_path = (
        PIPELINE_ROOT
        / "reviews/external/teaching-vacancies/england-wide-admin-service-review.csv"
    )
    review_date = _tv_review_date(today)
    state = _state(review_date, today)
    try:
        rows = _csv_rows(csv_path)
    except FileNotFoundError:
        return SourceResult(
            "teaching_vacancies",
            "Teaching Vacancies",
            "MISSING",
            review_date,
            publish_workflow="publish-reviewed-teaching-vacancies-england.yml",
            publish_requires_approval=True,
        )
    items = []
    if state == "OK":
        for row in rows:
            if clean(row.get("review_scope")) != "REVIEW NOW":
                continue
            if (
                clean(row.get("final_decision")).upper() != "POSS"
                or clean(row.get("manual_action"))
            ):
                continue
            items.append(
                item_from_mapping(
                    "Teaching Vacancies",
                    row,
                    category="admin_service",
                )
            )
    return SourceResult(
        "teaching_vacancies",
        "Teaching Vacancies",
        state,
        review_date,
        tuple(items),
        publish_workflow="publish-reviewed-teaching-vacancies-england.yml",
        publish_requires_approval=True,
    )


def load_nhs(today: date) -> SourceResult:
    csv_path = PIPELINE_ROOT / "reviews/external/nhs-jobs-review.csv"
    md_path = PIPELINE_ROOT / "reviews/external/nhs-jobs-summary.md"
    if not csv_path.is_file() or not md_path.is_file():
        return SourceResult(
            "nhs",
            "NHS Jobs",
            "FUTURE",
            "",
            note="adapter ready; activates after first NHS admin/service refresh",
            publish_workflow="publish-reviewed-nhs-admin-service.yml",
            publish_requires_approval=True,
            shared_publish_after=True,
        )
    review_date = _metadata_date(md_path)
    state = _state(review_date, today)
    try:
        rows = _csv_rows(csv_path)
    except FileNotFoundError:
        return SourceResult(
            "nhs",
            "NHS Jobs",
            "MISSING",
            review_date,
            publish_workflow="publish-reviewed-nhs-admin-service.yml",
            publish_requires_approval=True,
            shared_publish_after=True,
        )
    items: list[ReviewItem] = []
    if state == "OK":
        for row in rows:
            if clean(row.get("final_decision")).upper() != "POSS":
                continue
            if clean(row.get("manual_action")):
                continue
            item = item_from_mapping(
                "NHS Jobs",
                row,
                category="admin_service",
                region=clean(row.get("region")),
                location=clean(row.get("location")),
                reason=(
                    f"{clean(row.get('switchability'))}: "
                    f"{clean(row.get('classification_reason'))}"
                ).strip(": "),
            )
            items.append(item)
    return SourceResult(
        "nhs",
        "NHS Jobs",
        state,
        review_date,
        tuple(items),
        publish_workflow="publish-reviewed-nhs-admin-service.yml",
        publish_requires_approval=True,
        shared_publish_after=True,
    )


SOURCE_LOADERS: tuple[Callable[[date], SourceResult], ...] = (
    load_jobg8,
    load_nejobs,
    load_vonne,
    load_teaching_vacancies,
    load_nhs,
)


def load_all_sources(today: date) -> list[SourceResult]:
    return [loader(today) for loader in SOURCE_LOADERS]
