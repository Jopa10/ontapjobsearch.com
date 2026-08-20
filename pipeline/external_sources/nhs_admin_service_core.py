"""NHS Administrative & Clerical -> Ontap admin/service review and composition.

This module is deliberately split into review and composition stages.

Review stage:
- consumes normalised NHS vacancy rows (JSON/CSV-friendly dictionaries);
- applies Ontap admin/service title rules;
- routes through the shared geo_lookup.xlsx contract;
- checks the current region/category slice register;
- deduplicates conservatively against current Ontap admin/service output;
- carries manual_action as data for the unified review/decision ledger.

Composition stage:
- requires a same-day completed NHS review;
- accepts only SELECTED/HC rows for LIVE admin_service slices;
- replaces the previous NHS subset while preserving every non-NHS row;
- removes expired NHS rows by replacement, not by mutating other sources;
- enforces a maximum 20% NHS share in a normal composed slice;
- writes only to a caller-supplied output directory.  The caller decides whether
  that directory is a dry-run location or the live output-admin-service folder.

The transport itself stays separate so the future official NHS External Job
Board API can replace the public discovery feed without changing these rules.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from dataclasses import dataclass, asdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

from external_sources.regional_contracts import (
    CATEGORY_ADMIN_SERVICE,
    canonical_public_region,
    load_geo_lookup,
    load_slice_authorities,
    publishable_region,
    route_geography,
)

SOURCE = "NHS Jobs"
SOURCE_KEY = "nhs"
JOB_ID_PREFIX = "nhs-"
MAX_NHS_SHARE = 0.20
DEFAULT_GEO = Path("geo/geo_lookup.xlsx")
DEFAULT_SLICE_REGISTER = Path("registers/region_category_slice_register.csv")
DEFAULT_CURRENT_OUTPUT = Path("output-admin-service")

HC_TITLE_TERMS = (
    "administrator", "administrative assistant", "admin assistant",
    "administration assistant", "clerical officer", "clerical assistant",
    "receptionist", "reception assistant", "booking clerk", "appointments clerk",
    "appointment clerk", "ward clerk", "records clerk", "medical records",
    "data administrator", "office assistant", "office administrator",
    "business support", "support officer", "personal assistant",
)
POSS_TITLE_TERMS = (
    "medical secretary", "team secretary", "coordinator", "co-ordinator",
    "project support", "service support", "patient pathway", "waiting list",
    "referral", "rota", "information officer", "data officer", "finance assistant",
)
HARD_TITLE_TERMS = (
    "manager", "head of", "director", "consultant", "nurse", "doctor",
    "therapist", "pharmacist", "scientist", "technician", "engineer",
)

REVIEW_FIELDS = (
    "review_date", "source", "source_job_id", "title", "employer", "location",
    "postcode", "region", "geo_cluster", "geography_status", "geography_reason",
    "salary_text", "employment_type", "posted_date", "closing_date", "source_url",
    "apply_url", "description", "classification", "classification_reason",
    "switchability", "slice_status", "publish_eligible", "duplicate_check",
    "duplicate_job_id", "manual_action", "final_decision", "factual_fingerprint",
)


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\xa0", " ")).strip()


def normalise(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).casefold()).strip()


def parse_date(value: object) -> date | None:
    text = clean(value)
    if not text:
        return None
    for candidate in (text[:10], text):
        try:
            return datetime.fromisoformat(candidate.replace("Z", "+00:00")).date()
        except ValueError:
            pass
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(candidate, fmt).date()
            except ValueError:
                continue
    return None


def is_open(closing_date: object, today: date) -> bool:
    parsed = parse_date(closing_date)
    return parsed is None or parsed >= today


def classify_title(title: object) -> tuple[str, str, str]:
    value = normalise(title)
    hard = [term for term in HARD_TITLE_TERMS if normalise(term) in value]
    clear = [term for term in HC_TITLE_TERMS if normalise(term) in value]
    poss = [term for term in POSS_TITLE_TERMS if normalise(term) in value]
    if hard and not clear:
        return "HARD_PASS", "HARD_PASS", "Out-of-scope/senior title: " + ", ".join(hard)
    if clear:
        return "HC", "OPEN_SWITCH", "Clear admin/service title: " + ", ".join(clear)
    if poss:
        return "POSS", "BRIDGEABLE", "Potential admin/service title: " + ", ".join(poss)
    return "POSS", "BRIDGEABLE", "Administrative & Clerical role requires title/context review"


def factual_fingerprint(row: dict[str, Any]) -> str:
    payload = {
        key: clean(row.get(key))
        for key in (
            "source", "source_job_id", "title", "employer", "location", "postcode",
            "salary_text", "employment_type", "posted_date", "closing_date",
            "source_url", "apply_url", "description", "classification",
            "classification_reason", "switchability", "region",
        )
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_current_rows(output_dir: Path = DEFAULT_CURRENT_OUTPUT) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not output_dir.is_dir():
        return rows
    for path in sorted(output_dir.glob("*-admin-service.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(value, list):
            rows.extend(dict(item) for item in value if isinstance(item, dict))
    return rows


def duplicate_against_current(candidate: dict[str, Any], current: Iterable[dict[str, Any]]) -> str:
    title = normalise(candidate.get("title"))
    employer = normalise(candidate.get("employer"))
    location = normalise(candidate.get("location"))
    if not title:
        return ""
    for row in current:
        if clean(row.get("source")).casefold() == SOURCE.casefold():
            continue
        if normalise(row.get("title")) != title:
            continue
        company = normalise(row.get("company") or row.get("advertiser_name"))
        row_location = normalise(row.get("location"))
        if employer and company and employer == company:
            return clean(row.get("job_id"))
        if employer and company and (employer in company or company in employer) and location and row_location == location:
            return clean(row.get("job_id"))
    return ""


def final_decision(classification: str, manual_action: str) -> str:
    classification = clean(classification).upper()
    action = clean(manual_action).casefold()
    if classification == "HARD_PASS":
        return "HARD_PASS"
    if action == "exclude":
        return "EXCLUDED"
    if action == "select":
        return "SELECTED"
    if classification == "HC":
        return "SELECTED"
    return "POSS"


def review_rows(
    vacancies: Iterable[dict[str, Any]],
    *,
    today: date,
    geo_path: Path = DEFAULT_GEO,
    slice_register: Path = DEFAULT_SLICE_REGISTER,
    current_output: Path = DEFAULT_CURRENT_OUTPUT,
) -> list[dict[str, str]]:
    geo = load_geo_lookup(geo_path)
    authorities = load_slice_authorities(slice_register)
    current = load_current_rows(current_output)
    output: list[dict[str, str]] = []
    seen: set[str] = set()

    for raw in vacancies:
        source_job_id = clean(raw.get("source_job_id") or raw.get("id"))
        if not source_job_id or source_job_id in seen:
            continue
        seen.add(source_job_id)
        if not is_open(raw.get("closing_date") or raw.get("closeDate"), today):
            continue

        title = clean(raw.get("title"))
        classification, switchability, reason = classify_title(title)
        location = clean(raw.get("location") or raw.get("locations"))
        postcode = clean(raw.get("postcode"))
        geo_result = route_geography(location=location, postcode=postcode, lookup=geo)
        region = canonical_public_region(geo_result.region)
        authority = authorities.get((region, CATEGORY_ADMIN_SERVICE)) if region else None
        slice_status = authority.status if authority else "UNREGISTERED"
        publish_eligible = bool(
            geo_result.status == "ROUTED"
            and region
            and publishable_region(authorities, region=region, category=CATEGORY_ADMIN_SERVICE)
        )

        row: dict[str, Any] = {
            "review_date": today.isoformat(),
            "source": SOURCE,
            "source_job_id": source_job_id,
            "title": title,
            "employer": clean(raw.get("employer") or raw.get("company")),
            "location": location,
            "postcode": postcode,
            "region": region,
            "geo_cluster": clean(geo_result.cluster),
            "geography_status": clean(geo_result.status),
            "geography_reason": clean(geo_result.evidence),
            "salary_text": clean(raw.get("salary_text") or raw.get("salary")),
            "employment_type": clean(raw.get("employment_type") or raw.get("type")),
            "posted_date": clean(raw.get("posted_date") or raw.get("postDate")),
            "closing_date": clean(raw.get("closing_date") or raw.get("closeDate")),
            "source_url": clean(raw.get("source_url") or raw.get("url")),
            "apply_url": clean(raw.get("apply_url") or raw.get("source_url") or raw.get("url")),
            "description": clean(raw.get("description")),
            "classification": classification,
            "classification_reason": reason,
            "switchability": switchability,
            "slice_status": slice_status,
            "publish_eligible": "YES" if publish_eligible else "NO",
            "duplicate_check": "NO_MATCH",
            "duplicate_job_id": "",
            "manual_action": clean(raw.get("manual_action")).casefold(),
        }
        duplicate_id = duplicate_against_current(row, current)
        if duplicate_id:
            row["duplicate_check"] = "DUPLICATE"
            row["duplicate_job_id"] = duplicate_id
            row["classification"] = "HARD_PASS"
            row["switchability"] = "HARD_PASS"
            row["classification_reason"] = "Confirmed current Ontap cross-source duplicate"
        row["final_decision"] = final_decision(row["classification"], row["manual_action"])
        row["factual_fingerprint"] = factual_fingerprint(row)
        output.append({field: clean(row.get(field)) for field in REVIEW_FIELDS})
    return output


def write_review_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def review_summary(rows: list[dict[str, str]], *, today: date) -> str:
    counts = {key: sum(row["final_decision"] == key for row in rows) for key in ("SELECTED", "POSS", "EXCLUDED", "HARD_PASS")}
    lines = [
        "# NHS Jobs admin/service review", "",
        f"review_date: {today.isoformat()}", "",
        f"- Open Administrative & Clerical rows reviewed: {len(rows)}",
        f"- Auto/remembered selected: {counts['SELECTED']}",
        f"- POSS awaiting decision: {counts['POSS']}",
        f"- Excluded: {counts['EXCLUDED']}",
        f"- HARD_PASS: {counts['HARD_PASS']}", "",
        "Edit only each `action:` line for POSS rows. Unchanged decisions are restored by the shared decision ledger.", "",
    ]
    for row in rows:
        if row["final_decision"] != "POSS":
            continue
        lines.extend([
            "---", "action:",
            f"POSS | NHS Jobs | {row['region'] or '—'} | {row['location'] or '—'} | {row['salary_text'] or '—'} | {row['title']}",
            f"source_job_id: {row['source_job_id']}",
            f"title: {row['title']}", f"employer: {row['employer']}",
            f"region: {row['region']}", f"reason: {row['switchability']}: {row['classification_reason']}",
            f"source_url: {row['source_url']}", f"factual_fingerprint: {row['factual_fingerprint']}",
            "---", "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def selected_rows_for_composition(rows: Iterable[dict[str, str]], *, today: date) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        if clean(row.get("review_date")) != today.isoformat():
            continue
        if clean(row.get("final_decision")).upper() != "SELECTED":
            continue
        if clean(row.get("publish_eligible")).upper() != "YES":
            continue
        if not is_open(row.get("closing_date"), today):
            continue
        required = ("source_job_id", "title", "employer", "location", "region", "apply_url")
        if any(not clean(row.get(field)) for field in required):
            continue
        output.append({
            "job_id": JOB_ID_PREFIX + clean(row.get("source_job_id")),
            "source": SOURCE,
            "title": clean(row.get("title")),
            "company": clean(row.get("employer")),
            "advertiser_name": clean(row.get("employer")),
            "location": clean(row.get("location")),
            "region": clean(row.get("region")),
            "salary": clean(row.get("salary_text")),
            "employment_type": clean(row.get("employment_type")),
            "posted_date": clean(row.get("posted_date")),
            "closing_date": clean(row.get("closing_date")),
            "description": clean(row.get("description")),
            "source_url": clean(row.get("source_url")),
            "apply_url": clean(row.get("apply_url")),
            "switchability": clean(row.get("switchability")),
        })
    return output


def _output_region(rows: list[dict[str, Any]]) -> str:
    regions = {canonical_public_region(row.get("region")) for row in rows if clean(row.get("region"))}
    return next(iter(regions)) if len(regions) == 1 else ""


def compose_region(current_rows: list[dict[str, Any]], candidates: list[dict[str, Any]], *, region: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    base = [dict(row) for row in current_rows if clean(row.get("source")).casefold() != SOURCE.casefold()]
    accepted: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    for candidate in candidates:
        proposed_total = len(base) + len(accepted) + 1
        proposed_nhs = len(accepted) + 1
        share = proposed_nhs / proposed_total if proposed_total else 1.0
        if share > MAX_NHS_SHARE + 1e-12:
            item = dict(candidate)
            item["deferred_reason"] = "NHS_SOURCE_SHARE_CAP"
            deferred.append(item)
            continue
        accepted.append(dict(candidate))
    return [*base, *accepted], deferred


def compose_outputs(current_dir: Path, review_rows_value: list[dict[str, str]], output_dir: Path, *, today: date) -> dict[str, Any]:
    selected = selected_rows_for_composition(review_rows_value, today=today)
    by_region: dict[str, list[dict[str, Any]]] = {}
    for row in selected:
        by_region.setdefault(clean(row.get("region")), []).append(row)

    output_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {"review_date": today.isoformat(), "regions": {}, "deferred": []}
    current_paths = sorted(current_dir.glob("*-admin-service.json")) if current_dir.is_dir() else []
    for path in current_paths:
        try:
            current = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid current output JSON: {path}") from exc
        if not isinstance(current, list) or not current:
            continue
        region = _output_region([row for row in current if isinstance(row, dict)])
        if not region:
            continue
        candidates = by_region.get(region, [])
        composed, deferred = compose_region([dict(row) for row in current if isinstance(row, dict)], candidates, region=region)
        out_path = output_dir / path.name
        out_path.write_text(json.dumps(composed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report["regions"][region] = {"base": sum(clean(row.get("source")).casefold() != SOURCE.casefold() for row in current if isinstance(row, dict)), "nhs_selected": len(candidates), "nhs_accepted": sum(clean(row.get("source")) == SOURCE for row in composed), "deferred": len(deferred), "total": len(composed), "file": str(out_path)}
        report["deferred"].extend(deferred)
    return report
