#!/usr/bin/env python3
"""Derive review-only city candidates from final published regional pages."""

from __future__ import annotations

import argparse
import csv
import json
import os
import tempfile
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTER = Path("pipeline/city_pages/city-page-register.json")
VALID_DECISIONS = {"include", "review", "exclude"}
VALID_MANUAL_CHOICES = {"include", "exclude"}


@dataclass(frozen=True)
class Rule:
    pattern: str
    reason: str


@dataclass(frozen=True)
class CityConfig:
    city_key: str
    display_name: str
    category_label: str
    parent_page: Path
    review_csv: Path
    summary_md: Path
    minimum_live_jobs: int
    mode: str
    include_rules: tuple[Rule, ...]
    review_rules: tuple[Rule, ...]
    exclude_rules: tuple[Rule, ...]
    fallback_decision: str
    fallback_reason: str


def normalise(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.casefold().split())


def usable_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def parse_rules(raw_rules: Any, field_name: str) -> tuple[Rule, ...]:
    if not isinstance(raw_rules, list):
        raise ValueError(f"{field_name} must be an array")
    parsed: list[Rule] = []
    for index, raw in enumerate(raw_rules):
        if not isinstance(raw, dict):
            raise ValueError(f"{field_name}[{index}] must be an object")
        pattern = raw.get("pattern")
        reason = raw.get("reason")
        if not usable_text(pattern) or not usable_text(reason):
            raise ValueError(
                f"{field_name}[{index}] needs usable pattern and reason"
            )
        parsed.append(Rule(normalise(pattern), reason.strip()))
    return tuple(parsed)


def parse_config(raw: dict[str, Any]) -> CityConfig:
    required = (
        "city_key",
        "display_name",
        "category_label",
        "parent_page",
        "review_csv",
        "summary_md",
        "mode",
        "fallback_decision",
        "fallback_reason",
    )
    for field in required:
        if not usable_text(raw.get(field)):
            raise ValueError(f"city config needs usable {field}")

    minimum = raw.get("minimum_live_jobs")
    if not isinstance(minimum, int) or minimum < 1:
        raise ValueError("minimum_live_jobs must be a positive integer")
    if raw["mode"] != "review_only":
        raise ValueError("only review_only city configs are supported")
    if raw["fallback_decision"] not in VALID_DECISIONS:
        raise ValueError("fallback_decision must be include, review, or exclude")

    return CityConfig(
        city_key=raw["city_key"].strip(),
        display_name=raw["display_name"].strip(),
        category_label=raw["category_label"].strip(),
        parent_page=Path(raw["parent_page"]),
        review_csv=Path(raw["review_csv"]),
        summary_md=Path(raw["summary_md"]),
        minimum_live_jobs=minimum,
        mode=raw["mode"],
        include_rules=parse_rules(raw.get("include_rules", []), "include_rules"),
        review_rules=parse_rules(raw.get("review_rules", []), "review_rules"),
        exclude_rules=parse_rules(raw.get("exclude_rules", []), "exclude_rules"),
        fallback_decision=raw["fallback_decision"],
        fallback_reason=raw["fallback_reason"].strip(),
    )


def load_register(path: Path) -> tuple[CityConfig, ...]:
    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    if not isinstance(raw, list) or not all(isinstance(item, dict) for item in raw):
        raise ValueError("city-page register must be an array of objects")

    configs = tuple(parse_config(item) for item in raw)
    keys = [config.city_key for config in configs]
    if len(keys) != len(set(keys)):
        raise ValueError("city_key values must be unique")
    return configs


def load_parent_jobs(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"parent page does not exist: {path}")
    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    if not isinstance(raw, list):
        raise ValueError(f"parent page must be an array: {path}")

    jobs: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"parent row {index} is not an object")
        for field in ("job_id", "title", "location"):
            if not usable_text(item.get(field)):
                raise ValueError(f"parent row {index} has no usable {field}")
        job_id = item["job_id"].strip()
        if job_id in seen:
            raise ValueError(f"duplicate parent job_id {job_id!r}")
        seen.add(job_id)
        jobs.append(item)
    return jobs


def first_match(text: str, rules: Iterable[Rule]) -> Rule | None:
    return next((rule for rule in rules if rule.pattern in text), None)


def classify_job(job: dict[str, Any], config: CityConfig) -> tuple[str, str, str]:
    """Classify using stated location; context may exclude/review, never include."""
    location = normalise(job.get("location"))
    context = normalise(
        " ".join(str(job.get(field, "")) for field in ("company", "summary"))
    )

    matched = first_match(location, config.exclude_rules)
    if matched:
        return "exclude", matched.pattern, matched.reason
    matched = first_match(location, config.include_rules)
    if matched:
        return "include", matched.pattern, matched.reason
    matched = first_match(location, config.review_rules)
    if matched:
        return "review", matched.pattern, matched.reason

    matched = first_match(context, config.exclude_rules)
    if matched:
        return "exclude", f"context:{matched.pattern}", matched.reason
    matched = first_match(context, config.review_rules)
    if matched:
        return "review", f"context:{matched.pattern}", matched.reason
    return config.fallback_decision, "fallback", config.fallback_reason


def review_job_id(job: dict[str, Any]) -> str:
    """Return a source-identifiable ID for the review sheet only."""
    job_id = str(job.get("job_id", "")).strip()
    source = normalise(job.get("source", "JobG8"))
    if source == "jobg8" and not job_id.casefold().startswith("jobg8-"):
        return f"jobg8-{job_id}"
    return job_id


def load_review_decisions(path: Path) -> dict[str, str]:
    """Load only genuine manual overrides from the previous review sheet."""
    if not path.is_file():
        return {}

    overrides: dict[str, str] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            job_id = (row.get("job_id") or "").strip()
            decision = (
                row.get("decision")
                or row.get("reviewer_action")
                or ""
            ).strip().casefold()
            previous_automatic = (
                row.get("automatic_decision") or ""
            ).strip().casefold()

            # A pre-filled decision that still equals the previous automatic
            # result is not a manual override. Only a changed include/exclude
            # choice is carried into the next run.
            if (
                job_id
                and decision in VALID_MANUAL_CHOICES
                and decision != previous_automatic
            ):
                overrides[job_id] = decision
    return overrides


# Backwards-compatible import name used by older tests/callers.
load_review_actions = load_review_decisions


def derive_rows(
    jobs: list[dict[str, Any]],
    config: CityConfig,
    prior_actions: dict[str, str] | None = None,
) -> list[dict[str, str]]:
    overrides = prior_actions or {}
    rows: list[dict[str, str]] = []
    for job in jobs:
        automatic, rule, reason = classify_job(job, config)
        sheet_job_id = review_job_id(job)
        raw_job_id = str(job.get("job_id", "")).strip()
        decision = overrides.get(
            sheet_job_id, overrides.get(raw_job_id, automatic)
        )
        rows.append(
            {
                "decision": decision,
                "job_id": sheet_job_id,
                "title": str(job.get("title", "")).strip(),
                "company": str(job.get("company", "")).strip(),
                "location": str(job.get("location", "")).strip(),
                "source": str(job.get("source", "JobG8")).strip() or "JobG8",
                "automatic_decision": automatic,
                "effective_decision": decision,
                "reason": reason,
                "matched_rule": rule,
                "city_key": config.city_key,
            }
        )
    return rows


FIELDNAMES = (
    "decision",
    "job_id",
    "title",
    "company",
    "location",
    "source",
    "automatic_decision",
    "effective_decision",
    "reason",
    "matched_rule",
    "city_key",
)


def csv_text(rows: list[dict[str, str]]) -> str:
    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def summary_text(config: CityConfig, rows: list[dict[str, str]]) -> str:
    automatic = {decision: 0 for decision in VALID_DECISIONS}
    effective = {decision: 0 for decision in VALID_DECISIONS}
    for row in rows:
        automatic[row["automatic_decision"]] += 1
        effective[row["effective_decision"]] += 1

    threshold_met = effective["include"] >= config.minimum_live_jobs
    lines = [
        f"# {config.display_name} {config.category_label} city-page review",
        "",
        f"- Parent regional page: `{config.parent_page}`",
        f"- Mode: `{config.mode}` (no live city JSON is written)",
        f"- Minimum live-job threshold: {config.minimum_live_jobs}",
        f"- Effective included jobs: {effective['include']}",
        f"- Threshold currently met: {'yes' if threshold_met else 'no'}",
        "",
        "## How to review",
        "The first left-hand CSV column is `decision` and is pre-filled with the current include, review or exclude result.",
        "Change it to `include` or `exclude` where required. Unchanged automatic decisions are refreshed normally; genuine overrides are preserved by `job_id`.",
        "JobG8 identifiers are prefixed `jobg8-` in this review sheet only; live job IDs are unchanged.",
        "This stage still publishes nothing.",
        "",
        "## Automatic decisions",
        f"- include: {automatic['include']}",
        f"- review: {automatic['review']}",
        f"- exclude: {automatic['exclude']}",
        "",
        "## Effective decisions after saved reviewer decisions",
        f"- include: {effective['include']}",
        f"- review: {effective['review']}",
        f"- exclude: {effective['exclude']}",
        "",
        "## Review reasons",
    ]

    review_rows = [
        row for row in rows if row["effective_decision"] == "review"
    ]
    if not review_rows:
        lines.append("- None")
    else:
        for row in review_rows:
            lines.append(
                f"- `{row['job_id']}` — {row['title']} — "
                f"{row['location']}: {row['reason']}"
            )
    return "\n".join(lines) + "\n"


def process_config(
    config: CityConfig, root: Path, write_review: bool
) -> dict[str, Any]:
    review_path = root / config.review_csv
    jobs = load_parent_jobs(root / config.parent_page)
    rows = derive_rows(jobs, config, load_review_decisions(review_path))
    if write_review:
        atomic_write(review_path, csv_text(rows))
        atomic_write(root / config.summary_md, summary_text(config, rows))

    include_count = sum(
        row["effective_decision"] == "include" for row in rows
    )
    return {
        "city_key": config.city_key,
        "parent_count": len(jobs),
        "include_count": include_count,
        "review_count": sum(
            row["effective_decision"] == "review" for row in rows
        ),
        "exclude_count": sum(
            row["effective_decision"] == "exclude" for row in rows
        ),
        "threshold": config.minimum_live_jobs,
        "threshold_met": include_count >= config.minimum_live_jobs,
        "status": "written" if write_review else "dry-run",
    }


def report_text(results: list[dict[str, Any]]) -> str:
    lines = [
        "# City-page derivation report",
        "",
        "| City | Parent jobs | Include | Review | Exclude | Threshold | Met | Status |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in results:
        lines.append(
            f"| {row['city_key']} | {row['parent_count']} | "
            f"{row['include_count']} | {row['review_count']} | "
            f"{row['exclude_count']} | {row['threshold']} | "
            f"{'yes' if row['threshold_met'] else 'no'} | {row['status']} |"
        )
    lines.extend(
        [
            "",
            "This stage is review-only. It does not create, replace, or remove any live city page.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--city", action="append", default=[])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--write-review", action="store_true")
    args = parser.parse_args()

    register_path = (
        args.register
        if args.register.is_absolute()
        else REPO_ROOT / args.register
    )
    configs = load_register(register_path)
    requested = set(args.city)
    if requested:
        configs = tuple(
            config for config in configs if config.city_key in requested
        )
        missing = requested - {config.city_key for config in configs}
        if missing:
            parser.error(f"unknown city_key: {', '.join(sorted(missing))}")

    results = [
        process_config(config, REPO_ROOT, args.write_review)
        for config in configs
    ]
    print(report_text(results), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
