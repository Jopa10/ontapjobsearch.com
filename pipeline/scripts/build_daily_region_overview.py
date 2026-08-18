from __future__ import annotations

from datetime import datetime
import csv
import io
import json
from pathlib import Path
import subprocess


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
        "register_category": "admin_service",
        "source_category": "Admin/Service – Office Support",
        "candidate_dir": "output-admin-service",
        "candidate_pattern": "{slug}-admin-service.json",
    },
    {
        "key": "support_worker",
        "label": "Support worker",
        "register_category": "support_worker",
        "source_category": "Support Worker – Wide",
        "candidate_dir": "output-support-worker",
        "candidate_pattern": "{slug}-support-worker.json",
    },
    {
        "key": "sales_advisor",
        "label": "Sales advisor",
        "register_category": "customer_sales",
        "source_category": "Customer Sales / Sales Advisor",
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


def _latest_live_source_report() -> tuple[str, str]:
    """Return (repo path, CSV text) from main, the source of truth for live counts."""
    try:
        names = subprocess.check_output(
            [
                "git",
                "ls-tree",
                "-r",
                "--name-only",
                "origin/main",
                "pipeline/reports-daily",
            ],
            cwd=REPO_ROOT,
            text=True,
        ).splitlines()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Could not inspect origin/main for live source reports") from exc

    candidates = sorted(
        name
        for name in names
        if name.startswith("pipeline/reports-daily/live-job-source-count-")
        and name.endswith(".csv")
    )
    if not candidates:
        raise RuntimeError("No live-job-source-count report found on origin/main")

    report_path = candidates[-1]
    try:
        text = subprocess.check_output(
            ["git", "show", f"origin/main:{report_path}"],
            cwd=REPO_ROOT,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Could not read {report_path} from origin/main") from exc
    return report_path, text


def _load_live_counts() -> tuple[str, dict[tuple[str, str], int]]:
    report_path, text = _latest_live_source_report()
    counts: dict[tuple[str, str], int] = {}
    reader = csv.DictReader(io.StringIO(text))
    required = {"level", "region", "category", "count"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise RuntimeError(f"Unexpected live source report header in {report_path}")

    for row in reader:
        if (row.get("level") or "").strip() != "region_category":
            continue
        region = (row.get("region") or "").strip()
        category = (row.get("category") or "").strip()
        if not region or not category:
            continue
        try:
            count = int((row.get("count") or "0").strip())
        except ValueError as exc:
            raise RuntimeError(f"Invalid count in {report_path}: {row}") from exc
        counts[(region, category)] = counts.get((region, category), 0) + count

    return report_path, counts


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
    source_report, live_counts = _load_live_counts()

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
            status = statuses.get((region_name, family["register_category"]), "")
            is_live = status == "LIVE"
            live_count = (
                live_counts.get((region_name, family["source_category"]), 0)
                if is_live
                else 0
            )
            candidate_count = 0 if is_live else _candidate_count(slug, family)
            family_state[family["key"]] = {
                "live": is_live,
                "live_count": live_count,
                "candidate_count": candidate_count,
                "status": status,
            }
        rows.append((region_name, slug, family_state))

    lines = [
        "# Ontap daily regional overview",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        f"> LIVE counts reconcile directly to `{source_report}` on `main`. LIVE status comes from the region/category slice register. `CHECK` means the register says LIVE but the source-of-truth report has no jobs for that slice. NOT LIVE counts come from current candidate/output files where available. `—` means zero or unavailable.",
        "",
        "## LIVE",
        "",
        "| Region | Service admin | Support worker | Sales advisor |",
        "|---|---:|---:|---:|",
    ]

    # Deliberately show all 33 regions so gaps are visible at a glance.
    for region_name, _slug, state in rows:
        live_cells = []
        for family in FAMILIES:
            item = state[family["key"]]
            if not item["live"]:
                live_cells.append("")
            elif item["live_count"] == 0:
                live_cells.append("CHECK")
            else:
                live_cells.append(str(item["live_count"]))
        lines.append(f"| {region_name} | " + " | ".join(live_cells) + " |")

    lines.extend([
        "",
        "## NOT LIVE",
        "",
        "| Region | Service admin | Support worker | Sales advisor |",
        "|---|---:|---:|---:|",
    ])
    for region_name, _slug, state in rows:
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
    checks = {
        f["key"]: sum(
            1
            for _name, _slug, state in rows
            if state[f["key"]]["live"] and state[f["key"]]["live_count"] == 0
        )
        for f in FAMILIES
    }
    total_live_slices = sum(live_regions.values())
    total_possible = len(rows) * len(FAMILIES)

    def headline_value(family_key: str) -> str:
        value = str(live_jobs[family_key])
        if checks[family_key]:
            value += f" + {checks[family_key]} CHECK"
        return value

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
            + " | ".join(headline_value(f["key"]) for f in FAMILIES)
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
