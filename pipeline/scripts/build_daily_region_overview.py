from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PIPELINE_ROOT.parent
CATALOG = PIPELINE_ROOT / "config" / "job_slice_catalog.json"
OUTPUT = PIPELINE_ROOT / "reports-daily" / "daily-region-overview.md"

# The current daily overview is the 33-region England set. Northern Ireland - East
# remains in the wider slice catalogue but is intentionally excluded here for now.
EXCLUDED_REGIONS = {"Northern Ireland - East"}

FAMILIES = (
    {
        "key": "service_admin",
        "label": "Service admin",
        "live_file": "service-administrator-jobs.json",
        "candidate_dir": "output-admin-service",
        "candidate_pattern": "{slug}-admin-service.json",
    },
    {
        "key": "support_worker",
        "label": "Support worker",
        "live_file": "support-worker.json",
        "candidate_dir": "output-support-worker",
        "candidate_pattern": "{slug}-support-worker.json",
    },
    {
        "key": "sales_advisor",
        "label": "Sales advisor",
        # This file does not exist on live pages yet. Keeping the future route here
        # means the report will switch from NOT LIVE to LIVE automatically when the
        # customer-sales family is eventually published.
        "live_file": "customer-sales-jobs.json",
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


def _family_count(region_slug: str, family: dict[str, str]) -> tuple[bool, int]:
    live_path = REPO_ROOT / "app" / region_slug / family["live_file"]
    if live_path.is_file():
        return True, _job_count(live_path)

    candidate_path = (
        PIPELINE_ROOT
        / family["candidate_dir"]
        / family["candidate_pattern"].format(slug=region_slug)
    )
    return False, _job_count(candidate_path)


def _cell(live: bool, count: int) -> str:
    if live:
        return str(count)
    return "—" if count == 0 else str(count)


def build() -> str:
    catalog = _load_json(CATALOG)
    if not isinstance(catalog, dict) or not isinstance(catalog.get("regions"), dict):
        raise RuntimeError(f"Could not load region catalogue: {CATALOG}")

    regions = [
        (name, facts["slug"])
        for name, facts in catalog["regions"].items()
        if name not in EXCLUDED_REGIONS
    ]
    if len(regions) != 33:
        raise RuntimeError(
            f"Daily overview expected 33 regions, found {len(regions)}. "
            "Update EXCLUDED_REGIONS or the catalogue deliberately."
        )

    rows = []
    for region_name, slug in regions:
        family_state = {}
        for family in FAMILIES:
            live, count = _family_count(slug, family)
            family_state[family["key"]] = {"live": live, "count": count}
        rows.append((region_name, slug, family_state))

    live_rows = [r for r in rows if any(v["live"] for v in r[2].values())]
    not_live_rows = [r for r in rows if not all(v["live"] for v in r[2].values())]

    lines = [
        "# Ontap daily regional overview",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "> Counts in LIVE cells are currently published jobs. Counts in NOT LIVE cells are current candidate/output jobs where available. `—` means no current candidate/output file or zero jobs.",
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
                _cell(state[f["key"]]["live"], state[f["key"]]["count"])
                if state[f["key"]]["live"]
                else ""
                for f in FAMILIES
            )
            + " |"
        )

    lines.extend(["", "## NOT LIVE", "", "| Region | Service admin | Support worker | Sales advisor |", "|---|---:|---:|---:|"])
    for region_name, _slug, state in not_live_rows:
        lines.append(
            "| "
            + region_name
            + " | "
            + " | ".join(
                "" if state[f["key"]]["live"] else _cell(False, state[f["key"]]["count"])
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
            state[f["key"]]["count"]
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
