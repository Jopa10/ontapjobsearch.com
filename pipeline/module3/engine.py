from __future__ import annotations

import re
from collections import Counter
from copy import copy
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from pipeline.module3.rules import (
    COL, SELECTED_CLASSIFICATIONS, SENIORITY_TERMS, classify_remote,
    clean_description, fix_encoding, norm_key, norm_text, normalise_url,
)

CONFIG = {
    "minimum_seen_ratio": 0.80, "minimum_average_daily_jobs": 6.0,
    "minimum_unique_titles": 5, "minimum_unique_companies": 3,
    "severe_top_1_company_share": 0.50, "severe_top_2_company_share": 0.70,
    "watch_minimum_average_daily_jobs": 3.0, "watch_minimum_seen_ratio": 0.50,
    "watch_minimum_peak_jobs": 6, "meaningful_decline_pct": -20.0,
}


def parse_iso_date(value: str) -> date:
    try: return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc: raise ValueError(f"Invalid date '{value}'. Expected YYYY-MM-DD.") from exc


def extract_date(path: Path) -> Optional[date]:
    for pattern, order in [
        (r"(?<!\d)(20\d{2})[-_.](\d{2})[-_.](\d{2})(?!\d)", (1, 2, 3)),
        (r"(?<!\d)(\d{2})[-_.](\d{2})[-_.](20\d{2})(?!\d)", (3, 2, 1)),
    ]:
        match = re.search(pattern, path.stem)
        if match:
            try: return date(*[int(match.group(i)) for i in order])
            except ValueError: return None
    return None


def month_folders(start: date, end: date, root: Path) -> list[Path]:
    folders, year, month = [], start.year, start.month
    while (year, month) <= (end.year, end.month):
        folders.append(root / f"{year:04d}-{month:02d}")
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    return folders


def discover_feed_files(start: date, end: date, root: Path) -> tuple[list[tuple[date, Path]], list[str]]:
    found, warnings = [], []
    for folder in month_folders(start, end, root):
        if not folder.is_dir():
            warnings.append(f"Missing archive folder: {folder}"); continue
        for path in sorted(folder.iterdir()):
            if path.name.startswith("~$") or path.suffix.casefold() not in {".xlsx", ".xls", ".xlsm"}: continue
            day = extract_date(path)
            if day is None: warnings.append(f"Skipped {path.name}: date not recognised from filename")
            elif start <= day <= end: found.append((day, path))
    return sorted(found, key=lambda x: (x[0], x[1].name.casefold())), warnings


def load_admin_register(path: Path) -> dict[str, dict[str, str]]:
    frame = pd.read_csv(path, dtype=str, encoding="utf-8-sig").fillna("")
    missing = {"title", "classification"} - set(frame.columns)
    if missing: raise ValueError(f"{path} missing required columns: {sorted(missing)}")
    register = {
        norm_key(row["title"]): {
            "classification": norm_text(row["classification"]).upper(),
            "reason": norm_text(row.get("reason", "")),
        }
        for _, row in frame.iterrows() if norm_key(row["title"])
    }
    if not register: raise ValueError(f"{path} contains no usable title rows")
    return register


def build_job_id(row: pd.Series, source_file: str, row_number: int) -> str:
    for column in (COL["display_reference"], COL["sender_reference"]):
        if norm_text(row.get(column, "")): return norm_text(row.get(column, ""))
    url = normalise_url(row.get(COL["application_url"], ""))
    return url or f"{source_file}:{row_number}"


def load_daily_feeds(files: list[tuple[date, Path]], register: dict[str, dict[str, str]]):
    rows, daily, warnings, source_rows = [], [], [], 0
    for feed_date, path in files:
        try: frame = pd.read_excel(path, dtype=str).fillna("")
        except Exception as exc:
            warnings.append(f"{path.name}: failed to read: {exc}"); continue
        missing = {COL["title"], COL["description"]} - set(frame.columns)
        if missing: warnings.append(f"{path.name}: missing columns {sorted(missing)}"); continue
        source_rows += len(frame); seen = set(); counts = Counter(); totals = Counter()
        for index, row in frame.iterrows():
            job_id = build_job_id(row, path.name, index + 2)
            if job_id in seen: continue
            seen.add(job_id)
            title = fix_encoding(row.get(COL["title"], "")); entry = register.get(norm_key(title))
            if not entry or entry["classification"] not in SELECTED_CLASSIFICATIONS: continue
            decision = classify_remote(title, row.get(COL["description"], ""), row.get(COL["area"], ""), row.get(COL["location"], ""))
            senior = bool(re.search(r"\b(?:" + "|".join(SENIORITY_TERMS) + r")\b", title, re.I))
            candidate = decision.classification in {"FULLY_REMOTE_CONFIRMED", "FULLY_REMOTE_LOCATION_RESTRICTED", "REMOTE_OPTION_AVAILABLE"}
            strict = candidate and not senior
            ukwide = strict and decision.scope == "UK_WIDE" and decision.routine_office_attendance == "no"
            record = {
                "date": feed_date.isoformat(), "source_file": path.name, "job_id": job_id, "title": title,
                "advertiser": fix_encoding(row.get(COL["advertiser"], "")) or "Unknown advertiser",
                "advertiser_type": fix_encoding(row.get(COL["advertiser_type"], "")),
                "area": fix_encoding(row.get(COL["area"], "")), "location": fix_encoding(row.get(COL["location"], "")),
                "employment_type": fix_encoding(row.get(COL["employment_type"], "")),
                "work_hours": fix_encoding(row.get(COL["work_hours"], "")),
                "salary_minimum": norm_text(row.get(COL["salary_minimum"], "")),
                "salary_maximum": norm_text(row.get(COL["salary_maximum"], "")),
                "salary_period": fix_encoding(row.get(COL["salary_period"], "")),
                "salary_additional": fix_encoding(row.get(COL["salary_additional"], "")),
                "application_url": norm_text(row.get(COL["application_url"], "")),
                "register_classification": entry["classification"], "register_reason": entry["reason"],
                "role_eligibility": "eligible", "role_exclusion_reason": "",
                "senior_or_management_flag": senior, "remote_classification": decision.classification,
                "remote_reason_code": decision.reason_code, "matched_remote_terms": decision.matched_terms,
                "remote_evidence": decision.evidence, "remote_scope": decision.scope,
                "routine_office_attendance": decision.routine_office_attendance,
                "manual_review_required": decision.manual_review_required, "register_eligible": True,
                "remote_admin_candidate": candidate, "strict_non_senior_candidate": strict,
                "uk_wide_strict_candidate": ukwide,
                "full_description": clean_description(row.get(COL["description"], "")),
            }
            rows.append(record); counts[decision.classification] += 1
            totals["eligible"] += 1; totals["signal"] += decision.classification != "NO_REMOTE_SIGNAL"
            totals["candidate"] += candidate; totals["strict"] += strict; totals["ukwide"] += ukwide
        daily.append({
            "date": feed_date.isoformat(), "total_feed_jobs": len(seen),
            "register_eligible_admin_service_jobs": totals["eligible"],
            "jobs_with_remote_keyword_signal": totals["signal"],
            "fully_remote_confirmed": counts["FULLY_REMOTE_CONFIRMED"],
            "fully_remote_location_restricted": counts["FULLY_REMOTE_LOCATION_RESTRICTED"],
            "remote_option_available": counts["REMOTE_OPTION_AVAILABLE"],
            "remote_after_training_or_probation": counts["REMOTE_AFTER_TRAINING_OR_PROBATION"],
            "hybrid_or_partial_remote": counts["HYBRID_OR_PARTIAL_REMOTE"],
            "ambiguous_remote_review": counts["AMBIGUOUS_REMOTE_REVIEW"],
            "remote_false_positive": counts["REMOTE_MENTION_FALSE_POSITIVE"],
            "explicitly_not_remote": counts["EXPLICITLY_NOT_REMOTE"],
            "business_opportunity_or_training": counts["BUSINESS_OPPORTUNITY_OR_TRAINING"],
            "remote_admin_candidates": totals["candidate"],
            "strict_non_senior_candidates": totals["strict"], "uk_wide_strict_candidates": totals["ukwide"],
        })
    if not daily: raise RuntimeError("No valid JobG8 feed files could be read for the requested date range.")
    return pd.DataFrame(rows), pd.DataFrame(daily), warnings, source_rows


def candidate_review(detail: pd.DataFrame) -> pd.DataFrame:
    cols = ["first_seen", "last_seen", "days_seen", "job_id", "title", "advertiser", "area", "location",
            "register_classification", "senior_or_management_flag", "remote_classification", "remote_reason_code",
            "remote_scope", "remote_evidence", "matched_remote_terms", "remote_admin_candidate",
            "strict_non_senior_candidate", "uk_wide_strict_candidate", "application_url", "full_description"]
    allowed = {"FULLY_REMOTE_CONFIRMED", "FULLY_REMOTE_LOCATION_RESTRICTED", "REMOTE_OPTION_AVAILABLE",
               "REMOTE_AFTER_TRAINING_OR_PROBATION", "HYBRID_OR_PARTIAL_REMOTE", "AMBIGUOUS_REMOTE_REVIEW"}
    subset = detail[detail["remote_classification"].isin(allowed)].copy()
    if subset.empty: return pd.DataFrame(columns=cols)
    result = []
    for job_id, group in subset.groupby("job_id", sort=False):
        first = group.sort_values("date").iloc[0]
        result.append({"first_seen": group["date"].min(), "last_seen": group["date"].max(),
                       "days_seen": group["date"].nunique(), "job_id": job_id,
                       **{c: first[c] for c in cols[4:]}})
    result = pd.DataFrame(result, columns=cols)
    order = {"FULLY_REMOTE_CONFIRMED": 0, "FULLY_REMOTE_LOCATION_RESTRICTED": 1, "REMOTE_OPTION_AVAILABLE": 2,
             "REMOTE_AFTER_TRAINING_OR_PROBATION": 3, "HYBRID_OR_PARTIAL_REMOTE": 4, "AMBIGUOUS_REMOTE_REVIEW": 5}
    result["_order"] = result["remote_classification"].map(order)
    return result.sort_values(["strict_non_senior_candidate", "_order", "days_seen", "title"],
                              ascending=[False, True, False, True]).drop(columns="_order")


def safe_share(a, b): return a / b if b else 0.0

def top_values(series: pd.Series, limit=10):
    return "; ".join(f"{value} ({count})" for value, count in Counter(norm_text(v) for v in series if norm_text(v)).most_common(limit))

def concentration(group: pd.DataFrame):
    counts, total = group["advertiser"].value_counts(), len(group)
    top1 = safe_share(int(counts.iloc[0]) if len(counts) else 0, total)
    top2 = safe_share(int(counts.iloc[:2].sum()) if len(counts) else 0, total)
    severe = top1 >= CONFIG["severe_top_1_company_share"] or top2 >= CONFIG["severe_top_2_company_share"]
    return round(top1 * 100, 1), round(top2 * 100, 1), "HIGH" if severe else ("MEDIUM" if top1 >= .35 or top2 >= .55 else "LOW"), severe

def recommend(avg, seen_ratio, titles, companies, peak, severe):
    if avg >= 6 and seen_ratio >= .8 and titles >= 5 and companies >= 3 and not severe:
        return "BUILD", "Meets persistence, average-volume and breadth safeguards without severe advertiser concentration."
    concerns = []
    if seen_ratio < .8: concerns.append("insufficient persistence")
    if avg < 6: concerns.append("average below 6 jobs/day")
    if titles < 5 or companies < 3: concerns.append("limited title/company breadth")
    if severe: concerns.append("severe advertiser concentration")
    watch = avg >= 3 or seen_ratio >= .5 or peak >= 6
    return ("WATCH" if watch else "REJECT"), "; ".join(concerns) or "Insufficient sustained supply."


def build_supply_summary(detail: pd.DataFrame, daily: pd.DataFrame, start: date, end: date) -> pd.DataFrame:
    masks = {
        "ALL_REMOTE_ADMIN_CANDIDATES": detail["remote_admin_candidate"],
        "STRICT_NON_SENIOR_CANDIDATES": detail["strict_non_senior_candidate"],
        "UK_WIDE_STRICT_CANDIDATES": detail["uk_wide_strict_candidate"],
        "FULLY_REMOTE_LOCATION_RESTRICTED": detail["remote_classification"].eq("FULLY_REMOTE_LOCATION_RESTRICTED"),
        "REMOTE_OPTION_AVAILABLE": detail["remote_classification"].eq("REMOTE_OPTION_AVAILABLE"),
        "REMOTE_AFTER_TRAINING_OR_PROBATION": detail["remote_classification"].eq("REMOTE_AFTER_TRAINING_OR_PROBATION"),
        "HYBRID_OR_PARTIAL_REMOTE": detail["remote_classification"].eq("HYBRID_OR_PARTIAL_REMOTE"),
    } if not detail.empty else {name: pd.Series(dtype=bool) for name in [
        "ALL_REMOTE_ADMIN_CANDIDATES", "STRICT_NON_SENIOR_CANDIDATES", "UK_WIDE_STRICT_CANDIDATES",
        "FULLY_REMOTE_LOCATION_RESTRICTED", "REMOTE_OPTION_AVAILABLE", "REMOTE_AFTER_TRAINING_OR_PROBATION",
        "HYBRID_OR_PARTIAL_REMOTE"]}
    days, rows = list(daily["date"]), []
    for name, mask in masks.items():
        group = detail.loc[mask].copy() if not detail.empty else detail.copy()
        by_date = group.groupby("date")["job_id"].nunique().to_dict() if not group.empty else {}
        counts = [int(by_date.get(day, 0)) for day in days]; seen = sum(v > 0 for v in counts)
        first, last = counts[:5], counts[-5:]; first_avg = safe_share(sum(first), len(first)); last_avg = safe_share(sum(last), len(last))
        change = ((last_avg - first_avg) / first_avg * 100) if first_avg else 0.0
        titles = group["title"].map(norm_key).nunique() if not group.empty else 0
        companies = group["advertiser"].nunique() if not group.empty else 0
        top1, top2, risk, severe = concentration(group) if not group.empty else (0.0, 0.0, "LOW", False)
        avg, ratio, peak = safe_share(sum(counts), len(days)), safe_share(seen, len(days)), max(counts) if counts else 0
        verdict, reason = recommend(avg, ratio, titles, companies, peak, severe)
        rows.append({"candidate_group": name, "start_date": start.isoformat(), "end_date": end.isoformat(),
                     "feed_days": len(days), "total_job_day_rows": len(group), "unique_jobs": group["job_id"].nunique() if not group.empty else 0,
                     "days_seen": seen, "seen_ratio_pct": round(ratio * 100, 1), "average_daily_count": round(avg, 2),
                     "minimum_daily_count": min(counts) if counts else 0, "maximum_daily_count": peak,
                     "days_with_6_plus": sum(v >= 6 for v in counts), "days_with_12_plus": sum(v >= 12 for v in counts),
                     "first_five_day_average": round(first_avg, 2), "last_five_day_average": round(last_avg, 2),
                     "direction_change_pct": round(change, 1), "unique_title_count": titles, "unique_company_count": companies,
                     "top_titles": top_values(group["title"]) if not group.empty else "", "top_companies": top_values(group["advertiser"]) if not group.empty else "",
                     "top_1_company_share_pct": top1, "top_2_company_share_pct": top2, "concentration_risk": risk,
                     "recommendation": verdict, "recommendation_reason": reason})
    return pd.DataFrame(rows)


def rule_definitions():
    rows = [
        ("EXPLICITLY_NOT_REMOTE", "Explicit wording says remote/hybrid working is unavailable or the role is onsite only."),
        ("BUSINESS_OPPORTUNITY_OR_TRAINING", "Course, programme, franchise or self-employment/business offer rather than a vacancy."),
        ("FULLY_REMOTE_CONFIRMED", "Clear evidence that the vacancy can be performed remotely without routine office attendance."),
        ("FULLY_REMOTE_LOCATION_RESTRICTED", "Fully remote/home-based but the applicant must live within a stated area or radius."),
        ("REMOTE_OPTION_AVAILABLE", "Fully remote is explicitly one option alongside hybrid or office work."),
        ("REMOTE_AFTER_TRAINING_OR_PROBATION", "Remote working starts only after training, induction, probation or another condition."),
        ("HYBRID_OR_PARTIAL_REMOTE", "Regular office/onsite attendance or a defined home/office split is required."),
        ("REMOTE_MENTION_FALSE_POSITIVE", "Remote wording describes geography, technology, teams, training or work in clients' homes."),
        ("AMBIGUOUS_REMOTE_REVIEW", "Remote wording exists but does not prove the actual working arrangement."),
        ("NO_REMOTE_SIGNAL", "No relevant remote-work wording found."),
    ]
    return pd.DataFrame(rows, columns=["classification", "definition"])


def write_excel(path: Path, summary, daily, review, detail):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, frame in [("Summary", summary), ("Daily counts", daily), ("Candidate review", review),
                            ("All eligible jobs", detail), ("Rule definitions", rule_definitions())]:
            frame.to_excel(writer, sheet_name=name, index=False)
        for sheet in writer.sheets.values():
            sheet.freeze_panes = "A2"; sheet.auto_filter.ref = sheet.dimensions; sheet.sheet_view.showGridLines = False
            for cell in sheet[1]:
                font = copy(cell.font); font.bold = True; cell.font = font
            for cells in sheet.columns:
                header = norm_text(cells[0].value).casefold(); letter = cells[0].column_letter
                width = 60 if header in {"full_description", "remote_evidence", "recommendation_reason", "definition"} else 42 if header in {"application_url", "top_titles", "top_companies", "matched_remote_terms"} else min(max(max((len(norm_text(c.value)) for c in list(cells)[:150]), default=10) + 2, 11), 30)
                sheet.column_dimensions[letter].width = width
            for row in sheet.iter_rows():
                for cell in row:
                    alignment = copy(cell.alignment); alignment.wrap_text = True; alignment.vertical = "top"; cell.alignment = alignment


def run(start: date, end: date, archive_root: Path, output_dir: Path, register_path: Path):
    if end < start: raise ValueError("End date must not precede start date.")
    files, discovery_warnings = discover_feed_files(start, end, archive_root)
    if not files: raise FileNotFoundError(f"No dated JobG8 Excel files found from {start} to {end} beneath {archive_root}")
    register = load_admin_register(register_path)
    detail, daily, load_warnings, source_rows = load_daily_feeds(files, register)
    if not detail.empty: detail = detail.sort_values(["date", "remote_admin_candidate", "title", "job_id"], ascending=[True, False, True, True])
    daily = daily.sort_values("date"); review = candidate_review(detail); summary = build_supply_summary(detail, daily, start, end)
    period = f"{start.isoformat()}_to_{end.isoformat()}"; output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "detail": output_dir / f"{period}-module3-remote-admin-detail.csv",
        "review": output_dir / f"{period}-module3-candidate-review.csv",
        "daily": output_dir / f"{period}-module3-daily-counts.csv",
        "summary": output_dir / f"{period}-module3-supply-summary.csv",
        "excel": output_dir / f"{period}-module3-wfh-results.xlsx",
        "log": output_dir / f"{period}-module3-run-log.txt",
    }
    detail.to_csv(paths["detail"], index=False, encoding="utf-8-sig"); review.to_csv(paths["review"], index=False, encoding="utf-8-sig")
    daily.to_csv(paths["daily"], index=False, encoding="utf-8-sig"); summary.to_csv(paths["summary"], index=False, encoding="utf-8-sig")
    write_excel(paths["excel"], summary, daily, review, detail)
    class_counts = detail["remote_classification"].value_counts().to_dict() if not detail.empty else {}
    lines = [f"Start date: {start}", f"End date: {end}", f"Archive root: {archive_root}",
             f"Archive folders scanned: {', '.join(map(str, month_folders(start, end, archive_root)))}",
             f"Dated files selected: {len(files)}", f"Valid feed days: {daily['date'].nunique()}",
             f"Total source rows: {source_rows}", f"Register: {register_path}", f"Register titles loaded: {len(register)}",
             f"Register-eligible job-day rows: {len(detail)}", f"Unique register-eligible jobs: {detail['job_id'].nunique() if not detail.empty else 0}",
             f"Remote admin candidate job-day rows: {int(detail['remote_admin_candidate'].sum()) if not detail.empty else 0}",
             f"Strict non-senior candidate job-day rows: {int(detail['strict_non_senior_candidate'].sum()) if not detail.empty else 0}",
             f"UK-wide strict candidate job-day rows: {int(detail['uk_wide_strict_candidate'].sum()) if not detail.empty else 0}",
             "", "Selected files:", *[f"- {day}: {path}" for day, path in files], "", "Remote classifications:",
             *[f"- {name}: {count}" for name, count in sorted(class_counts.items())], "", "Configuration:",
             *[f"- {key}: {value}" for key, value in CONFIG.items()], "", "Outputs:", *[f"- {path}" for path in paths.values()]]
    warnings = discovery_warnings + load_warnings
    if warnings: lines += ["", "Warnings:", *[f"- {warning}" for warning in warnings]]
    paths["log"].write_text("\n".join(lines), encoding="utf-8"); print("\n".join(lines)); return paths
