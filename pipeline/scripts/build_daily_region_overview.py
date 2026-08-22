from __future__ import annotations

from datetime import datetime
import csv
import io
import json
from pathlib import Path
import subprocess


PIPELINE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PIPELINE_ROOT.parent
CATALOG = PIPELINE_ROOT / "config" / "uk_assessable_regions.json"
REGISTER = PIPELINE_ROOT / "registers" / "region_category_slice_register.csv"
OUTPUT = PIPELINE_ROOT / "reports-daily" / "daily-region-overview.md"
EXPECTED_REGION_COUNT = 73

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
        "candidate_dir": "",
        "candidate_pattern": "",
    },
)


def _load_json(path: Path):
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError):
        return None


def _count_json_data(data) -> int:
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        for key in ("jobs", "items", "results"):
            value = data.get(key)
            if isinstance(value, list):
                return len(value)
    return 0


def _job_count(path: Path) -> int:
    return _count_json_data(_load_json(path))


def _published_sales_count(region_slug: str) -> int:
    path = REPO_ROOT / "app" / "_city-pages" / "configured-slices" / region_slug / "customer-sales-jobs.json"
    return _job_count(path) if path.is_file() else 0


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
        return subprocess.check_output(["git", "show", f"origin/main:{repo_path}"], cwd=REPO_ROOT, text=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Could not read {repo_path} from origin/main") from exc


def _main_tree_names(folder: str) -> list[str]:
    try:
        return subprocess.check_output(["git", "ls-tree", "-r", "--name-only", "origin/main", folder], cwd=REPO_ROOT, text=True).splitlines()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Could not inspect origin/main/{folder}") from exc


def _latest_live_source_report() -> tuple[str, str]:
    candidates = sorted(
        name for name in _main_tree_names("pipeline/reports-daily")
        if name.startswith("pipeline/reports-daily/live-job-source-count-") and name.endswith(".csv")
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
        counts[(region, category)] = counts.get((region, category), 0) + int((row.get("count") or "0").strip())
    return report_path, counts


def _load_selected_counts(repo_path: str) -> dict[str, int]:
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
    return {region: len(selected_ids.get(region, set())) + anonymous_counts.get(region, 0) for region in regions}


def _load_latest_profile_counts() -> tuple[str, str, dict[tuple[str, str], int]]:
    candidates = sorted(
        name for name in _main_tree_names("pipeline/reports-module2")
        if name.startswith("pipeline/reports-module2/") and name.endswith("-module2-daily-counts.csv")
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
        if (row.get("date") or "").strip() != latest_date or (row.get("region_scope") or "").strip() != "lookup_region":
            continue
        region = (row.get("region") or "").strip()
        category = (row.get("category") or "").strip()
        if region and category:
            counts[(region, category)] = int(float((row.get("daily_job_count") or "0").strip()))
    return report_path, latest_date, counts


def _load_teaching_vacancies_counts(regions: list[tuple[str, str]]) -> dict[str, int]:
    folder = "pipeline/output-external/teaching-vacancies-regional"
    available = set(_main_tree_names(folder))
    counts: dict[str, int] = {}
    for region_name, slug in regions:
        path = f"{folder}/{slug}-admin-service.json"
        if path not in available:
            continue
        data = json.loads(_git_show_main(path).lstrip("\ufeff"))
        counts[region_name] = _count_json_data(data)
    return counts


def build() -> str:
    catalog = _load_json(CATALOG)
    if not isinstance(catalog, dict) or not isinstance(catalog.get("regions"), dict):
        raise RuntimeError(f"Could not load assessable region catalogue: {CATALOG}")

    statuses = _load_statuses()
    source_report, live_counts = _load_live_counts()
    _profile_report, profile_date, profile_counts = _load_latest_profile_counts()
    decision_counts = {
        family["key"]: _load_selected_counts(family["decision_report"])
        for family in FAMILIES if family["decision_report"]
    }

    regions = sorted(((name, facts["slug"]) for name, facts in catalog["regions"].items()), key=lambda item: item[0].casefold())
    declared_count = int(catalog.get("region_count") or len(regions))
    if declared_count != len(regions) or len(regions) != EXPECTED_REGION_COUNT:
        raise RuntimeError(
            f"Daily overview expected {EXPECTED_REGION_COUNT} assessable UK markets, catalogue declares {declared_count} and contains {len(regions)}."
        )

    rollups = {str(k): str(v) for k, v in catalog.get("detail_rollups", {}).items()}
    teaching_counts = _load_teaching_vacancies_counts(regions)

    def profile_count(region_name: str, category: str) -> int | None:
        direct = profile_counts.get((region_name, category))
        if direct is not None:
            return direct
        alias_total = sum(
            count for (raw_region, raw_category), count in profile_counts.items()
            if raw_category == category and rollups.get(raw_region) == region_name
        )
        return alias_total if alias_total else None

    rows = []
    for region_name, slug in regions:
        family_state = {}
        for family in FAMILIES:
            status = statuses.get((region_name, family["register_category"]), "")
            is_live = status == "LIVE"
            if is_live and family["key"] == "sales_advisor":
                live_count = _published_sales_count(slug)
            else:
                live_count = live_counts.get((region_name, family["source_category"]), 0) if is_live else 0

            candidate_count: int | None = None
            candidate_source = ""
            if not is_live:
                if family["decision_report"] and region_name in decision_counts[family["key"]]:
                    candidate_count = decision_counts[family["key"]][region_name]
                    candidate_source = "daily"
                elif family["profile_category"]:
                    candidate_count = profile_count(region_name, family["profile_category"])
                    if candidate_count is not None:
                        candidate_source = "profile"
                if family["key"] == "service_admin" and region_name in teaching_counts:
                    candidate_count = (candidate_count or 0) + teaching_counts[region_name]
                    candidate_source = (candidate_source + "+teaching").strip("+")

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
        f"> LIVE Service Admin and Support Worker counts reconcile to `{source_report}` on `main`. LIVE Sales Advisor counts come from the current published Customer Sales configured-slice JSON on `main`. The overview covers all {EXPECTED_REGION_COUNT} assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 73-market coverage has run, NOT LIVE Admin/Support may fall back to the latest all-region Module 2 profile ({profile_date or 'unavailable'}), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero.",
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

    lines.extend(["", "## NOT LIVE", "", "| Region | Service admin | Support worker | Sales advisor |", "|---|---:|---:|---:|"])
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

    live_regions = {f["key"]: sum(1 for _n, _s, state in rows if state[f["key"]]["live"]) for f in FAMILIES}
    live_jobs = {
        f["key"]: sum(state[f["key"]]["live_count"] for _n, _s, state in rows if state[f["key"]]["live"])
        for f in FAMILIES
    }
    checks = {
        f["key"]: sum(1 for _n, _s, state in rows if state[f["key"]]["live"] and state[f["key"]]["live_count"] == 0)
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
        "", "## HEADLINE", "",
        "| Measure | Service admin | Support worker | Sales advisor |",
        "|---|---:|---:|---:|",
        "| Live regions | " + " | ".join(f"{live_regions[f['key']]} / {EXPECTED_REGION_COUNT}" for f in FAMILIES) + " |",
        "| Live jobs | " + " | ".join(headline_value(f["key"]) for f in FAMILIES) + " |",
        "", f"**Live slices: {total_live_slices} / {total_possible}.**", "",
    ])
    return "\n".join(lines)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
