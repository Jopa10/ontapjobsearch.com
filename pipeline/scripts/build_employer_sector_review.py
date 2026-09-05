#!/usr/bin/env python3
"""Expand high-confidence employer identities and build a review-only sector audit."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "pipeline/registers/employer_sector_rules.csv"
OUTPUT = ROOT / "pipeline/reports/employer-sector-review.csv"


def normalise(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def employer_identity(job: dict[str, object]) -> str:
    value = str(job.get("advertiser_name") or job.get("company") or "").strip()
    return re.sub(
        r"\s+-\s+(?:Agency|Company)\s+-\s+.*$", "", value, flags=re.IGNORECASE
    ).strip()


def load_jobs() -> list[dict[str, object]]:
    jobs: dict[str, dict[str, object]] = {}
    for path in sorted((ROOT / "app").rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, list):
            continue
        for job in data:
            if isinstance(job, dict) and job.get("job_id"):
                jobs.setdefault(str(job["job_id"]), job)
    return list(jobs.values())


def ordered(rules: list[dict[str, str]]) -> list[dict[str, str]]:
    kind_order = {"exact": 0, "regex": 1, "fallback": 2}
    return sorted(
        rules,
        key=lambda row: (
            int(row["priority"]), kind_order.get(row["match_type"], 9), row["rule_id"]
        ),
    )


def matches(rule: dict[str, str], job: dict[str, object]) -> bool:
    field, kind, value = rule["match_field"], rule["match_type"], rule["match_value"]
    if kind == "fallback":
        return True
    if field == "source":
        values = [job.get("source", "")]
    elif field == "advertiser_type":
        values = [job.get("advertiser_type", "")]
    elif field == "employer_identity":
        values = [employer_identity(job)]
    elif field == "combined_text":
        values = [
            " ".join(
                str(job.get(key) or "")
                for key in ("company", "advertiser_name", "description", "full_description")
            )
        ]
    else:
        return False
    if kind == "exact":
        return any(normalise(candidate) == normalise(value) for candidate in values)
    if kind == "regex":
        return any(re.search(value, str(candidate), re.IGNORECASE) for candidate in values)
    return False


def classify(
    job: dict[str, object], rules: list[dict[str, str]]
) -> dict[str, str]:
    for rule in ordered(rules):
        if matches(rule, job):
            return rule
    raise RuntimeError("Employer-sector register has no fallback rule")


def main() -> None:
    with REGISTER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rules = list(reader)
    generated_reason = (
        "Exact current employer identity confirmed by high-strength repository rule evidence"
    )
    rules = [rule for rule in rules if rule["reason"] != generated_reason]
    jobs = load_jobs()

    evidence: dict[str, list[tuple[dict[str, object], dict[str, str]]]] = defaultdict(list)
    labels: dict[str, str] = {}
    for job in jobs:
        identity = employer_identity(job)
        if not identity:
            continue
        key = normalise(identity)
        labels.setdefault(key, identity)
        evidence[key].append((job, classify(job, rules)))

    existing_exact = {
        normalise(rule["match_value"])
        for rule in rules
        if rule["match_field"] == "employer_identity" and rule["match_type"] == "exact"
    }
    additions = 0
    for key, observations in evidence.items():
        if key in existing_exact:
            continue
        strong_observations = [
            rule for _, rule in observations
            if (
                rule["evidence_strength"] == "HIGH"
                and rule["sector"] != "unknown"
                and rule["match_field"] in {"employer_identity", "source"}
            )
        ]
        strong = {rule["sector"] for rule in strong_observations}
        if len(strong_observations) != len(observations) or len(strong) != 1:
            continue
        sector = next(iter(strong))
        supporting = sorted({
            rule["rule_id"]
            for _, rule in observations
            if rule["evidence_strength"] == "HIGH" and rule["sector"] == sector
        })
        rules.append({
            "rule_id": "",
            "match_field": "employer_identity",
            "match_type": "exact",
            "match_value": labels[key],
            "sector": sector,
            "evidence_strength": "HIGH",
            "on_conflict": sector,
            "status": "REVIEW",
            "active": "FALSE",
            "priority": "0",
            "reason": "Exact current employer identity confirmed by high-strength repository rule evidence",
            "evidence_reference": (
                f"current published app inventory; supporting draft rules {','.join(supporting)}"
            ),
            "approval_status": "PENDING",
            "approved_by": "",
            "approved_date": "",
            "approval_notes": "",
        })
        existing_exact.add(key)
        additions += 1

    rules = ordered(rules)
    for number, rule in enumerate(rules, 1):
        rule["rule_id"] = f"ES{number:03d}"
    with REGISTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rules)

    audit: dict[str, dict[str, object]] = {}
    for job in jobs:
        identity = employer_identity(job) or "(blank employer identity)"
        key = normalise(identity)
        rule = classify(job, rules)
        item = audit.setdefault(key, {
            "employer_identity": identity,
            "job_count": 0,
            "sources": set(),
            "advertiser_types": set(),
            "sectors": set(),
            "matched_rule_ids": set(),
            "evidence_strengths": set(),
            "example_titles": [],
        })
        item["job_count"] += 1
        item["sources"].add(str(job.get("source") or ""))
        item["advertiser_types"].add(str(job.get("advertiser_type") or ""))
        item["sectors"].add(rule["sector"])
        item["matched_rule_ids"].add(rule["rule_id"])
        item["evidence_strengths"].add(rule["evidence_strength"])
        title = str(job.get("title") or "").strip()
        if title and title not in item["example_titles"] and len(item["example_titles"]) < 3:
            item["example_titles"].append(title)

    output_rows = []
    for item in audit.values():
        sectors = sorted(item["sectors"])
        sector = sectors[0] if len(sectors) == 1 else "unknown"
        output_rows.append({
            "employer_identity": item["employer_identity"],
            "job_count": item["job_count"],
            "sources": "|".join(sorted(x for x in item["sources"] if x)),
            "advertiser_types": "|".join(sorted(x for x in item["advertiser_types"] if x)),
            "draft_sector": sector,
            "matched_rule_ids": "|".join(sorted(item["matched_rule_ids"])),
            "evidence_strength": "|".join(sorted(item["evidence_strengths"])),
            "review_status": "REVIEW_UNKNOWN" if sector == "unknown" else "REVIEW_CLASSIFIED",
            "example_titles": " | ".join(item["example_titles"]),
        })
    output_rows.sort(key=lambda row: (
        row["draft_sector"] != "unknown", -int(row["job_count"]),
        row["employer_identity"].casefold(),
    ))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    output_fields = [
        "employer_identity", "job_count", "sources", "advertiser_types",
        "draft_sector", "matched_rule_ids", "evidence_strength",
        "review_status", "example_titles",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)

    print(
        f"jobs={len(jobs)} employers={len(output_rows)} exact_rules_added={additions} "
        f"unknown_employers={sum(row['draft_sector']=='unknown' for row in output_rows)} "
        f"unknown_jobs={sum(int(row['job_count']) for row in output_rows if row['draft_sector']=='unknown')}"
    )


if __name__ == "__main__":
    main()
