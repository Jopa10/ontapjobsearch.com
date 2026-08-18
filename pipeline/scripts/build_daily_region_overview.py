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

# The daily overview is the 33-region England set. Northern Ireland - East remains
# in the wider slice catalogue but is intentionally excluded here for now.
EXCLUDED_REGIONS = {"Northern Ireland - East"}

FAMILIES = (
    {
        "key": "service_admin",
        "label": "Service admin",
        "register_category": "admin_service",
        "source_category": "Admin/Service – Office Support",
        "decision_report": "pipeline/reports-daily/decision-report-admin-service.csv",
        "profile_category": "admin_service",
        "candidate_dir": "output-admin-service",
        "candidate_pattern": "{slug}-admin-service.json",
    },
    {
        "key": "support_worker",
        "label": "Support worker",
        "register_category": "support_worker",
        "source_category": "Support Worker – Wide",
        "decision_report": "pipeline/reports-daily/decision-report-support-worker.csv",
        "profile_category": "support_worker",
        "candidate_dir": "output-support-worker",
        "candidate_pattern": "{slug}-support-worker.json",
    },
    {
        "key": "sales_advisor",
        "label": "Sales advisor",
        "register_category": "customer_sales",
        "source_category": "Customer Sales / Sales Advisor",
        "decision_report": "",
        "profile_category": "",
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


def _git_show_main(repo_path: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "show", f"origin/main:{repo_path}"],
            cwd=REPO_ROOT,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Could not read {repo_path} from origin/main") from exc


def _main_tree_names(folder: str) -> list[str]:
    try:
        return subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", "origin/main", folder],
            cwd=REPO_ROOT,
            text=True,
        ).splitlines()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Could not inspect origin/main/{folder}") from exc


def _latest_live_source_report() -> tuple[str, str]:
    candidates = sorted(
        name
        for name in _main_tree_names("pipeline/reports-daily")
        if name.startswith("pipeline/reports-daily/live-job-source-count-")
        and name.endswith(".csv")
    )
    if not candidates:
        raise RuntimeError("No live-job-source-count report found on origin/main")
    report_path = candidates[-1]
    return report_path, _git_show_main(report_path)


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


def _load_selected_counts(repo_path: str) -> dict[str, int]:
    """Count unique SELECTED jobs by region from a main daily decision report."""
    text = _git_show_main(repo_path)
    reader = csv.DictReader(io.StringIO(text.lstrip("\ufeff")))
    if not reader.fieldnames or "region" not in reader.fieldnames:
        raise RuntimeError(f"Unexpected decision report header in {repo_path}")

    selected_ids: dict[str, set[str]] = {}
    anonymous_counts: dict[str, int] = {}
    for row in reader:
        decision = (row.get("decision") or "").strip().upper()
        selection_status = (row.get("selection_status") or "").strip().upper()
        if decision != "SELECTED" and selection_status != "SELECTED":
            continue
        region = (row.get("region") or "").strip()
        if not region:
            continue
        job_id = (row.get("job_id") or "").strip()
        if job_id:
            selected_ids.setdefault(region, set()).add(job_id)
        else:
            anonymous_counts[region] = anonymous_counts.get(region, 0) + 1

    regions = set(selected_ids) | set(anonymous_counts)
    return {
        region: len(selected_ids.get(region, set())) + anonymous_counts.get(region, 0)
        for region in regions
    }


def _load_latest_profile_counts() -> tuple[str, str, dict[tuple[str, str], int]]:
    """Latest all-region Module 2 daily counts from main.

    This is the fallback for regions the targeted daily selection pipelines did not
    assess. It prevents 'not assessed' from being silently rendered as zero.
    """
    candidates = sorted(
        name
        for name in _main_tree_names("pipeline/reports-module2")
        if name.startswith("pipeline/reports-module2/")
        and name.endswith("-module2-daily-counts.csv")
    )
    if not candidates:
        return "", "", {}

    report_path = candidates[-1]
    text = _git_show_main(report_path)
    reader = csv.DictReader(io.StringIO(text.lstrip("\ufeff")))
    required = {"date", "region", "region_scope", "category", "daily_job_count"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise RuntimeError(f"Unexpected Module 2 daily-counts header in {report_path}")

    rows = list(reader)
    dates = sorted({(row.get("date") or "").strip() for row in rows if (row.get("date") or "").strip()})
    if not dates:
        return report_path, "", {}
    latest_date = dates[-1]

    counts: dict[tuple[str, str], int] = {}
    for row in rows:
        if (row.get("date") or "").strip() != latest_date:
            continue
        # Use the ordinary lookup-region rows. Published aggregate rows can duplicate
        # the same region/category and are not needed for NOT LIVE discovery.
        if (row.get("region_scope") or "").strip() != "lookup_region":
            continue
        region = (row.get("region") or "").strip()
        category = (row.get("category") or "").strip()
        if not region or not category:
            continue
        try:
            count = int(float((row.get("daily_job_count") or "0").strip()))
        except ValueError as exc:
            raise RuntimeError(f"Invalid Module 2 count in {report_path}: {row}") from exc
        counts[(region, category)] = count
    return report_path, latest_date, counts


def _candidate_count_if_present(region_slug: str, family: dict[str, str]) -> int | None:
    candidate_path = (
        PIPELINE_ROOT
        / family["candidate_dir"]
        / family["candidate_pattern"].format(slug=region_slug)
    )
    if not candidate_path.is_file():
        return None
    return _job_count(candidate_path)


def build() -> str:
    catalog = _load_json(CATALOG)
    if not isinstance(catalog, dict) or not isinstance(catalog.get("regions"), dict):
        raise RuntimeError(f"Could not load region catalogue: {CATALOG}")

    statuses = _load_statuses()
    source_report, live_counts = _load_live_counts()
    profile_report, profile_date, profile_counts = _load_latest_profile_counts()
    decision_counts = {
        family["key"]: _load_selected_counts(family["decision_report"])
        for family in FAMILIES
        if family["decision_report"]
    }

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
            live_count = live_counts.get((region_name, family["source_category"]), 0) if is_live else 0

            candidate_count: int | None = None
            candidate_source = ""
            if not is_live:
                if family["decision_report"] and region_name in decision_counts[family["key"]]:
                    candidate_count = decision_counts[family["key"]][region_name]
                    candidate_source = "daily"
                elif family["profile_category"] and (region_name, family["profile_category"]) in profile_counts:
                    candidate_count = profile_counts[(region_name, family["profile_category"])]
                    candidate_source = "profile"
                elif family["key"] == "sales_advisor":
                    candidate_count = _candidate_count_if_present(slug, family)
                    candidate_source = "test" if candidate_count is not None else ""

            family_state[family["key"]] = {
                "live": is_live,
                "live_count": live_count,
                "candidate_count": candidate_count,
                "candidate_source": candidate_source,
                "status": status,
            }
        rows.append((region_name, slug, family_state))

    lines = [
        "# Ontap daily regional overview",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        f"> LIVE counts reconcile to `{source_report}` on `main`. For NOT LIVE Admin/Support, the daily decision report is used where that region was assessed; otherwise the latest all-region Module 2 profile is used ({profile_date or 'unavailable'}). Sales Advisor uses test-branch output only. `—` means not assessed / no current source; it does NOT mean zero.",
        "",
        "## LIVE",
        "",
        "| Region | Service admin | Support worker | Sales advisor |",
        "|---|---:|---:|---:|",
    ]

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
        cells = []
        for family in FAMILIES:
            item = state[family["key"]]
            if item["live"]:
                cells.append("")
            elif item["candidate_count"] is None:
                cells.append("—")
            else:
                cells.append(str(item["candidate_count"]))
        lines.append(f"| {region_name} | " + " | ".join(cells) + " |")

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

    lines.extend([
        "",
        "## HEADLINE",
        "",
        "| Measure | Service admin | Support worker | Sales advisor |",
        "|---|---:|---:|---:|",
        "| Live regions | " + " | ".join(f"{live_regions[f['key']]} / 33" for f in FAMILIES) + " |",
        "| Live jobs | " + " | ".join(headline_value(f["key"]) for f in FAMILIES) + " |",
        "",
        f"**Live slices: {total_live_slices} / {total_possible}.**",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
