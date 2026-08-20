"""Registry-driven NHS admin/service selection.

The stable review/composition implementation is retained in nhs_admin_service_core.
This public module replaces its hard-coded title classifier with the dedicated
NHS title registry and adds HC Tier A/B publication priority.
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from external_sources import nhs_admin_service_core as core

SOURCE = core.SOURCE
SOURCE_KEY = core.SOURCE_KEY
JOB_ID_PREFIX = core.JOB_ID_PREFIX
MAX_NHS_SHARE = core.MAX_NHS_SHARE
DEFAULT_GEO = core.DEFAULT_GEO
DEFAULT_SLICE_REGISTER = core.DEFAULT_SLICE_REGISTER
DEFAULT_CURRENT_OUTPUT = core.DEFAULT_CURRENT_OUTPUT
DEFAULT_TITLE_REGISTRY = Path("registers/nhs_admin_service_title_registry")

clean = core.clean
normalise = core.normalise
parse_date = core.parse_date
is_open = core.is_open
factual_fingerprint = core.factual_fingerprint
duplicate_against_current = core.duplicate_against_current
final_decision = core.final_decision
load_current_rows = core.load_current_rows
_CORE_SELECTED_ROWS = core.selected_rows_for_composition
_CORE_COMPOSE_REGION = core.compose_region

REVIEW_FIELDS = tuple(
    list(core.REVIEW_FIELDS[:19])
    + ["hc_tier"]
    + list(core.REVIEW_FIELDS[19:])
)


def load_title_registry(path: Path = DEFAULT_TITLE_REGISTRY) -> dict[str, dict[str, str]]:
    files = sorted(path.glob("*.csv")) if path.is_dir() else ([path] if path.is_file() else [])
    if not files:
        raise FileNotFoundError(f"NHS admin/service title registry not found or empty: {path}")
    registry: dict[str, dict[str, str]] = {}
    for registry_file in files:
        with registry_file.open(encoding="utf-8-sig", newline="") as handle:
            rows = csv.DictReader(handle)
            fields = set(rows.fieldnames or [])
            if "classification" not in fields or not ({"title_key", "title"} & fields):
                raise ValueError(f"Invalid NHS title registry columns: {registry_file}")
            for raw in rows:
                key = normalise(raw.get("title_key") or raw.get("title"))
                if not key:
                    continue
                classification = clean(raw.get("classification")).upper()
                tier = clean(raw.get("hc_tier")).upper()
                if classification not in {"HC", "POSS", "HARD_PASS"}:
                    raise ValueError(f"Invalid NHS registry classification for {key!r}")
                if classification == "HC" and tier not in {"A", "B"}:
                    raise ValueError(f"HC NHS registry title requires Tier A/B: {key!r}")
                if classification != "HC":
                    tier = ""
                entry = {
                    "classification": classification,
                    "hc_tier": tier,
                    "switchability": (
                        "OPEN_SWITCH" if classification == "HC"
                        else "HARD_PASS" if classification == "HARD_PASS"
                        else "BRIDGEABLE"
                    ),
                }
                if key in registry and registry[key] != entry:
                    raise ValueError(f"Conflicting NHS registry entries for {key!r}")
                registry[key] = entry
    return registry


def classify_title(
    title: object,
    *,
    registry_path: Path = DEFAULT_TITLE_REGISTRY,
    registry: dict[str, dict[str, str]] | None = None,
) -> tuple[str, str, str, str]:
    lookup = registry if registry is not None else load_title_registry(registry_path)
    entry = lookup.get(normalise(title))
    if not entry:
        return (
            "POSS", "BRIDGEABLE",
            "Unseen NHS Administrative & Clerical title; registry review required", "",
        )
    return (
        entry["classification"], entry["switchability"],
        "NHS admin/service title registry", entry["hc_tier"],
    )


def review_rows(
    vacancies: Iterable[dict[str, Any]], *, today: date,
    geo_path: Path = DEFAULT_GEO,
    slice_register: Path = DEFAULT_SLICE_REGISTER,
    current_output: Path = DEFAULT_CURRENT_OUTPUT,
    title_registry: Path = DEFAULT_TITLE_REGISTRY,
) -> list[dict[str, str]]:
    registry = load_title_registry(title_registry)
    original = core.classify_title

    def bridge(title: object) -> tuple[str, str, str]:
        classification, switchability, reason, _tier = classify_title(title, registry=registry)
        return classification, switchability, reason

    core.classify_title = bridge
    try:
        rows = core.review_rows(
            vacancies, today=today, geo_path=geo_path,
            slice_register=slice_register, current_output=current_output,
        )
    finally:
        core.classify_title = original

    for row in rows:
        _classification, _switchability, _reason, tier = classify_title(
            row.get("title"), registry=registry
        )
        row["hc_tier"] = tier if clean(row.get("classification")).upper() == "HC" else ""
    return [{field: clean(row.get(field)) for field in REVIEW_FIELDS} for row in rows]


def write_review_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def review_summary(rows: list[dict[str, str]], *, today: date) -> str:
    text = core.review_summary(rows, today=today)
    a = sum(r.get("final_decision") == "SELECTED" and r.get("hc_tier") == "A" for r in rows)
    b = sum(r.get("final_decision") == "SELECTED" and r.get("hc_tier") == "B" for r in rows)
    marker = "- Auto/remembered selected:"
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(marker):
            lines[i + 1:i + 1] = [f"- Selected HC Tier A: {a}", f"- Selected HC Tier B: {b}"]
            break
    return "\n".join(lines).rstrip() + "\n"


def selected_rows_for_composition(
    rows: Iterable[dict[str, str]], *, today: date
) -> list[dict[str, Any]]:
    rows_list = list(rows)
    selected = _CORE_SELECTED_ROWS(rows_list, today=today)
    tier_by_id = {clean(r.get("source_job_id")): clean(r.get("hc_tier")) for r in rows_list}
    for row in selected:
        source_id = clean(row.get("job_id"))
        if source_id.startswith(JOB_ID_PREFIX):
            source_id = source_id[len(JOB_ID_PREFIX):]
        row["hc_tier"] = tier_by_id.get(source_id, "")
    return selected


def _candidate_sort_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
    tier_rank = {"A": 0, "B": 1}.get(clean(row.get("hc_tier")).upper(), 2)
    switch_rank = {
        "OPEN_SWITCH": 0, "PURE_SWITCH": 0,
        "BRIDGEABLE": 1, "POSSIBLE_SWITCH": 1,
        "NHS_EXPERIENCE_NEEDED": 2,
    }.get(clean(row.get("switchability")).upper(), 3)
    posted = parse_date(row.get("posted_date"))
    return (tier_rank, switch_rank, -posted.toordinal() if posted else 0, normalise(row.get("title")))


def compose_region(
    current_rows: list[dict[str, Any]], candidates: list[dict[str, Any]], *, region: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _CORE_COMPOSE_REGION(current_rows, sorted(candidates, key=_candidate_sort_key), region=region)


def compose_outputs(
    current_dir: Path, review_rows_value: list[dict[str, str]], output_dir: Path, *, today: date
) -> dict[str, Any]:
    original_selected = core.selected_rows_for_composition
    original_compose = core.compose_region
    core.selected_rows_for_composition = selected_rows_for_composition
    core.compose_region = compose_region
    try:
        return core.compose_outputs(current_dir, review_rows_value, output_dir, today=today)
    finally:
        core.selected_rows_for_composition = original_selected
        core.compose_region = original_compose
