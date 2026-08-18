from __future__ import annotations

from datetime import datetime
import csv
import json
from pathlib import Path


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PIPELINE_ROOT.parent
CATALOG = PIPELINE_ROOT / "config" / "job_slice_catalog.json"
REGISTER = PIPELINE_ROOT / "registers" / "region_category_slice_register.csv"
OUTPUT = PIPELINE_ROOT / "reports-daily" / "daily-region-overview.md"

# The current daily overview is the 33-region England set. Northern Ireland - East
# remains in the wider slice catalogue but is intentionally excluded here for now.
EXCLUDED_REGIONS = {"Northern Ireland - East"}

FAMILIES = (
    {
        "key": "service_admin",
        "label": "Service admin",
        "category": "admin_service",
        "route_slug": "service-administrator-jobs",
        "candidate_dir": "output-admin-service",
        "candidate_pattern": "{slug}-admin-service.json",
    },
    {
        "key": "support_worker",
        "label": "Support worker",
        "category": "support_worker",
        "route_slug": "support-worker",
        "candidate_dir": "output-support-worker",
        "candidate_pattern": "{slug}-support-worker.json",
    },
    {
        "key": "sales_advisor",
        "label": "Sales advisor",
        "category": "customer_sales",
        "route_slug": "customer-sales-jobs",
        "candidate_dir": "output-customer-sales-test",
        "candidate_pattern": "{slug}.json",
    },
)


def _load_json(path: Path):
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError):
        return None


def _job_count(path: Path) -> int:
    data = _load_json(path)
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        for key in ("jobs", "items", "results"):
            value = data.get(key)
            if isinstance(value, list):
                return len(value)
    return 0


def _load_statuses() -> dict[tuple[str, str], str]:
    statuses: dict[tuple[str, str], str] = {}
    with REGISTER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["region", "category", "status"]:
            raise RuntimeError(f"Unexpected slice register header: {reader.fieldnames}")
        for row in reader:
            region = (row.get("region") or "").strip()
            category = (row.get("category") or "").strip()
            status = (row.get("status") or "").strip().upper()
            if region and category:
                statuses[(region, category)] = status
    return statuses


def _live_count(region_slug: str, family: dict[str, str], is_live: bool) -> int:
    if not is_live:
        return 0

    static_path = REPO_ROOT / "app" / region_slug / f"{family['route_slug']}.json"
    if static_path.is_file():
        return _job_count(static_path)

    dynamic_path = (
        REPO_ROOT
        / "app"
        / "_city-pages"
        / "configured-slices"
        / region_slug
        / f"{family['route_slug']}.json"
    )
    return _job_count(dynamic_path)


def _candidate_count(region_slug: str, family: dict[str, str]) -> int:
    candidate_path = (
        PIPELINE_ROOT
        / family["candidate_dir"]
        / family["candidate_pattern"].format(slug=region_slug)
    )
    return _job_count(candidate_path)


def _cell(count: int) -> str:
    return "—" if count == 0 else str(count)


def build() -> str:
    catalog = _load_json(CATALOG)
    if not isinstance(catalog, dict) or not isinstance(catalog.get("regions"), dict):
        raise RuntimeError(f"Could not load region catalogue: {CATALOG}")

    statuses = _load_statuses()

    regions = sorted(
        (
            (name, facts["slug"])
            for name, facts in catalog["regions"].items()
            if name not in EXCLUDED_REGIONS
        ),
        key=lambda item: item[0].casefold(),
    )
    if len(regions) != 33:
        raise RuntimeError(
            f"Daily overview expected 33 regions, found {len(regions)}. "
            "Update EXCLUDED_REGIONS or the catalogue deliberately."
        )

    rows = []
    for region_name, slug in regions:
        family_state = {}
        for family in FAMILIES:
            status = statuses.get((region_name, family["category"]), "")
            is_live = status == "LIVE"
            live_count = _live_count(slug, family, is_live)
            candidate_count = 0 if is_live else _candidate_count(slug, family)
            family_state[family["key"]] = {
                "live": is_live,
                "live_count": live_count,
                "candidate_count": candidate_count,
                "status": status,
            }
        rows.append((region_name, slug, family_state))

    live_rows = [r for r in rows if any(v["live"] for v in r[2].values())]
    not_live_rows = [r for r in rows if any(not v["live"] for v in r[2].values())]

    lines = [
        "# Ontap daily regional overview",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "> LIVE status comes from the region/category slice register. LIVE counts come from the published static or configured-slice JSON. NOT LIVE counts come from current candidate/output files where available. `—` means zero or unavailable.",
        "",
        "## LIVE",
        "",
        "| Region | Service admin | Support worker | Sales advisor |",
        "|---|---:|---:|---:|",
    ]

    for region_name, _slug, state in live_rows:
        lines.append(
            "| "
            + region_name
            + " | "
            + " | ".join(
                _cell(state[f["key"]]["live_count"]) if state[f["key"]]["live"] else ""
                for f in FAMILIES
            )
            + " |"
        )

    lines.extend([
        "",
        "## NOT LIVE",
        "",
        "| Region | Service admin | Support worker | Sales advisor |",
        "|---|---:|---:|---:|",
    ])
    for region_name, _slug, state in not_live_rows:
        lines.append(
            "| "
            + region_name
            + " | "
            + " | ".join(
                "" if state[f["key"]]["live"] else _cell(state[f["key"]]["candidate_count"])
                for f in FAMILIES
            )
            + " |"
        )

    live_regions = {
        f["key"]: sum(1 for _name, _slug, state in rows if state[f["key"]]["live"])
        for f in FAMILIES
    }
    live_jobs = {
        f["key"]: sum(
            state[f["key"]]["live_count"]
            for _name, _slug, state in rows
            if state[f["key"]]["live"]
        )
        for f in FAMILIES
    }
    total_live_slices = sum(live_regions.values())
    total_possible = len(rows) * len(FAMILIES)

    lines.extend(
        [
            "",
            "## HEADLINE",
            "",
            "| Measure | Service admin | Support worker | Sales advisor |",
            "|---|---:|---:|---:|",
            "| Live regions | "
            + " | ".join(f"{live_regions[f['key']]} / 33" for f in FAMILIES)
            + " |",
            "| Live jobs | "
            + " | ".join(str(live_jobs[f["key"]]) for f in FAMILIES)
            + " |",
            "",
            f"**Live slices: {total_live_slices} / {total_possible}.**",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
