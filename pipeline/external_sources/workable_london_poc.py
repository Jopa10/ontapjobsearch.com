"""Review-only Workable London POC. Writes review CSV/MD only; never publishes."""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import service_admin_pipeline_core as admin  # noqa: E402

SOURCE = "Workable XML job feed"
REGION = "London"
FEED_URL = "https://www.workable.com/boards/workable.xml"
UA = "Ontap external-jobs review POC/1.0 (+https://www.ontapjobsearch.com/contact)"
CSV_OUT = ROOT / "reviews/external/london-workable-review.csv"
MD_OUT = ROOT / "reviews/external/london-workable-summary.md"
REGISTERS = (
    ("HR / Recruitment", "hr_recruitment_title_classification_register.csv"),
    ("Customer Service / Contact Centre", "customer_service_contact_centre_title_classification_register.csv"),
    ("Finance / Accounts", "finance_accounts_title_classification_register.csv"),
)
FIELDS = (
    "final_decision", "title", "employer", "location", "salary_text", "salary_status",
    "salary_evidence", "posted_date", "closing_date", "employment_type", "workplace_type",
    "source_category", "category", "classification", "classification_reason", "duplicate_status",
    "duplicate_candidate_title", "duplicate_candidate_employer", "duplicate_score",
    "source_job_id", "source_url", "apply_url", "manual_action", "source",
)

MONEY_RANGE = re.compile(
    r"(?ix)"
    r"(?P<prefix>£|GBP\s*)"
    r"(?P<lo>\d{2,3}(?:,\d{3})?(?:\.\d+)?)\s*(?P<lok>k)?"
    r"\s*(?:-|–|—|to)\s*"
    r"(?:(?:£|GBP\s*)\s*)?"
    r"(?P<hi>\d{2,3}(?:,\d{3})?(?:\.\d+)?)\s*(?P<hik>k)?"
)
MONEY_SINGLE = re.compile(
    r"(?ix)(?P<prefix>£|GBP\s*)(?P<value>\d{2,3}(?:,\d{3})?(?:\.\d+)?)\s*(?P<k>k)?"
)
SALARY_CUES = ("salary", "compensation", "pay range", "pay:", "per annum", "p.a.", " pa ", "annual")


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", html.unescape(str(value or ""))).strip()


def key(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).casefold()).strip()


def strip_html(value: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", value or "")
    text = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>", "\n", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return clean(text)


def money_to_int(raw: str, has_k: bool) -> int | None:
    try:
        val = float(raw.replace(",", ""))
    except ValueError:
        return None
    if has_k:
        val *= 1000
    elif val < 1000:
        return None
    out = int(round(val))
    return out if 15000 <= out <= 250000 else None


def salary_from_description(description_html: str) -> tuple[str, str, str]:
    text = strip_html(description_html)
    if not text:
        return "", "MISSING", ""

    candidates: list[tuple[int, str, str]] = []
    ranges = list(MONEY_RANGE.finditer(text))
    for match in ranges:
        lo = money_to_int(match.group("lo"), bool(match.group("lok")))
        hi = money_to_int(match.group("hi"), bool(match.group("hik")))
        if lo is None or hi is None or lo > hi:
            continue
        start, end = match.span()
        context = text[max(0, start - 90): min(len(text), end + 90)]
        cue = any(c in context.casefold() for c in SALARY_CUES)
        score = 3 if cue else 2
        formatted = f"£{lo:,}–£{hi:,}"
        candidates.append((score, formatted, clean(context)))

    for match in MONEY_SINGLE.finditer(text):
        amount = money_to_int(match.group("value"), bool(match.group("k")))
        if amount is None:
            continue
        start, end = match.span()
        if any(r.start() <= start < r.end() for r in ranges):
            continue
        context = text[max(0, start - 90): min(len(text), end + 90)]
        cue = any(c in context.casefold() for c in SALARY_CUES)
        if not cue:
            continue
        candidates.append((1, f"£{amount:,}", clean(context)))

    if not candidates:
        return "", "MISSING", ""
    candidates.sort(key=lambda x: (-x[0], len(x[2])))
    _score, salary, evidence = candidates[0]
    return salary, "USABLE_REVIEW", evidence


def child_text(elem: ET.Element, name: str) -> str:
    child = elem.find(name)
    return clean(child.text if child is not None else "")


def is_london(city: str, state: str, country: str) -> bool:
    loc = key(" ".join([city, state]))
    if "london" not in loc.split():
        return False
    c = key(country)
    return c in {"", "gb", "uk", "gbr", "united kingdom", "england"}


def source_row(elem: ET.Element) -> dict[str, str] | None:
    title = child_text(elem, "title")
    employer = child_text(elem, "company")
    city = child_text(elem, "city")
    state = child_text(elem, "state")
    country = child_text(elem, "country")
    if not is_london(city, state, country):
        return None

    job_id = child_text(elem, "referencenumber")
    url = child_text(elem, "url")
    if not title or not employer or not job_id or not url.startswith("http"):
        return None

    description = child_text(elem, "description")
    salary_text, salary_status, salary_evidence = salary_from_description(description)
    location = ", ".join(dict.fromkeys(x for x in (city, state, country) if x))
    remote = child_text(elem, "remote").casefold()
    workplace = "Remote" if remote == "true" else ""
    return {
        "title": title,
        "employer": employer,
        "location": location,
        "salary_text": salary_text,
        "salary_status": salary_status,
        "salary_evidence": salary_evidence,
        "posted_date": child_text(elem, "date"),
        "closing_date": "",
        "employment_type": child_text(elem, "jobtype"),
        "workplace_type": workplace,
        "source_category": child_text(elem, "category"),
        "category": "",
        "classification": "",
        "classification_reason": "",
        "duplicate_status": "",
        "duplicate_candidate_title": "",
        "duplicate_candidate_employer": "",
        "duplicate_score": "",
        "source_job_id": f"workable-{job_id}",
        "source_url": url,
        "apply_url": url,
        "manual_action": "",
        "source": SOURCE,
    }


def fetch_london_jobs(url: str) -> tuple[list[dict[str, str]], dict[str, int]]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/xml,text/xml"})
    rows: list[dict[str, str]] = []
    total = 0
    with urllib.request.urlopen(req, timeout=120) as response:
        for _event, elem in ET.iterparse(response, events=("end",)):
            if elem.tag.rsplit("}", 1)[-1] != "job":
                continue
            total += 1
            row = source_row(elem)
            if row is not None:
                rows.append(row)
            elem.clear()
    return rows, {"feed_jobs": total, "london_jobs": len(rows)}


def exact_category_titles() -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    for category, filename in REGISTERS:
        path = ROOT / "registers" / filename
        if not path.is_file():
            continue
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                cls = clean(row.get("classification")).upper()
                title = key(row.get("title"))
                if title and cls in {"HIGH_CONFIDENCE", "ELASTIC_FIT"}:
                    out.setdefault(title, (category, cls))
    return out


def classify(row: dict[str, str], exact: dict[str, tuple[str, str]], admin_register: dict[str, dict[str, str]]) -> None:
    hit = exact.get(key(row["title"]))
    if hit:
        row["category"], row["classification"] = hit
        row["classification_reason"] = f"existing {hit[0]} title register exact match"
        return
    cls, reason, _priority, _status = admin.classify_title(row["title"], admin_register)
    row["category"] = "Admin/Service – Office Support"
    row["classification"], row["classification_reason"] = cls, reason


def json_rows(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return [x for x in data if isinstance(x, dict)] if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def current_london() -> list[dict[str, str]]:
    paths = list((ROOT / "output-admin-service").glob("london-*.json"))
    paths += list((ROOT / "output-support-worker").glob("london-*.json"))
    paths += list((ROOT / "output-external").glob("**/london-*.json"))
    out: list[dict[str, str]] = []
    for path in dict.fromkeys(paths):
        for row in json_rows(path):
            employer = clean(row.get("advertiser_name") or row.get("company") or row.get("employer"))
            title = clean(row.get("title"))
            if employer and title:
                out.append({
                    "employer": employer,
                    "title": title,
                    "location": clean(row.get("location") or row.get("town")),
                })
    return out


def sim(a: str, b: str) -> float:
    return SequenceMatcher(None, key(a), key(b)).ratio()


def dedupe(row: dict[str, str], existing: list[dict[str, str]]) -> None:
    best_score, best = 0.0, None
    for old in existing:
        score = (
            .45 * sim(row["employer"], old["employer"])
            + .45 * sim(row["title"], old["title"])
            + .10 * (sim(row["location"], old["location"]) if old["location"] else .5)
        )
        if score > best_score:
            best_score, best = score, old
    row["duplicate_score"] = f"{best_score:.3f}" if best else ""
    if not best:
        row["duplicate_status"] = "ADDITIONAL"
        return
    exact = key(row["employer"]) == key(best["employer"]) and key(row["title"]) == key(best["title"])
    if exact or best_score >= .92:
        status = "CONFIRMED_DUPLICATE"
    elif best_score >= .78:
        status = "POSSIBLE_DUPLICATE"
    else:
        status = "ADDITIONAL"
    row["duplicate_status"] = status
    if status != "ADDITIONAL":
        row["duplicate_candidate_title"] = best["title"]
        row["duplicate_candidate_employer"] = best["employer"]


def auto_decision(row: dict[str, str]) -> str:
    if row["salary_status"] != "USABLE_REVIEW":
        return "HARD_PASS"
    if row["duplicate_status"] == "CONFIRMED_DUPLICATE":
        return "EXCLUDED"
    if row["classification"] in {"HARD_PASS", "OUT_OF_SCOPE"}:
        return "HARD_PASS"
    if row["duplicate_status"] == "POSSIBLE_DUPLICATE":
        return "POSS"
    return "SELECTED" if row["classification"] == "HIGH_CONFIDENCE" else "POSS"


def review_fingerprint(rows: list[dict[str, str]]) -> str:
    keep = [
        {k: row[k] for k in (
            "source_job_id", "title", "employer", "location", "salary_text", "salary_status",
            "category", "classification", "duplicate_status", "source_url", "apply_url"
        )}
        for row in rows
    ]
    return hashlib.sha256(
        json.dumps(sorted(keep, key=lambda x: x["source_job_id"]), ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()


def prior_actions(path: Path, date: str, fp: str) -> dict[str, str]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8-sig")
    if f"review_date: {date}" not in text or f"review_fingerprint: {fp}" not in text:
        return {}
    out: dict[str, str] = {}
    for block in re.findall(r"(?ms)^---\s*$\n(.*?)^---\s*$", text):
        ident = re.search(r"(?mi)^source_job_id:\s*(\S+)\s*$", block)
        action = re.search(r"(?mi)^action:\s*(select|exclude)?\s*$", block)
        if ident and action and clean(action.group(1)):
            out[clean(ident.group(1))] = clean(action.group(1)).casefold()
    return out


def rank(value: str) -> int:
    return {"SELECTED": 0, "POSS": 1, "EXCLUDED": 2, "HARD_PASS": 3}.get(value, 9)


def write_outputs(
    rows: list[dict[str, str]],
    stats: dict[str, int],
    csv_path: Path,
    md_path: Path,
) -> None:
    fp = review_fingerprint(rows)
    date = datetime.now(ZoneInfo("Europe/London")).date().isoformat()
    actions = prior_actions(md_path, date, fp)
    for row in rows:
        action = actions.get(row["source_job_id"], "")
        row["manual_action"] = action
        row["final_decision"] = (
            "SELECTED" if action == "select"
            else "EXCLUDED" if action == "exclude"
            else auto_decision(row)
        )

    rows.sort(key=lambda x: (rank(x["final_decision"]), x["employer"].casefold(), x["title"].casefold()))
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    counts = {d: sum(r["final_decision"] == d for r in rows) for d in ("SELECTED", "POSS", "EXCLUDED", "HARD_PASS")}
    salary_jobs = sum(r["salary_status"] == "USABLE_REVIEW" for r in rows)
    reviewable_salary = [
        r for r in rows
        if r["salary_status"] == "USABLE_REVIEW"
        and r["duplicate_status"] == "ADDITIONAL"
        and r["final_decision"] in {"SELECTED", "POSS"}
    ]
    salary_pct = (100 * salary_jobs / len(rows)) if rows else 0.0

    lines = [
        "# London Workable review",
        "",
        f"review_date: {date}",
        f"review_fingerprint: {fp}",
        "",
        "Edit only the action: line",
        "",
        f"source: {SOURCE}",
        f"region: {REGION}",
        f"feed_jobs_seen: {stats['feed_jobs']}",
        f"london_jobs_in_feed: {stats['london_jobs']}",
        f"salary_published_london_jobs: {salary_jobs}",
        f"salary_coverage_london: {salary_pct:.1f}%",
        f"likely_additional_reviewable_with_salary: {len(reviewable_salary)}",
        f"outcomes: SELECTED {counts['SELECTED']} | POSS {counts['POSS']} | EXCLUDED {counts['EXCLUDED']} | HARD_PASS {counts['HARD_PASS']}",
        "safety: review-only POC; no approved-output or publishing path",
        "",
        "field_note: Workable XML supplies posted date and application URL but no closing-date field.",
        "salary_note: salary is extracted conservatively from advert description text; every salary-bearing row includes a salary_evidence snippet for manual verification.",
    ]

    for decision in ("SELECTED", "POSS", "EXCLUDED", "HARD_PASS"):
        lines += ["", "## POSS — choose SELECT or EXCLUDE" if decision == "POSS" else f"## {decision}", ""]
        matches = [r for r in rows if r["final_decision"] == decision]
        if not matches:
            lines.append("None.")
        for r in matches:
            lines += [
                "---",
                f"action: {r['manual_action']}",
                f"{decision} | London | {r['location']} | {r['salary_text'] or 'salary not stated'} | {r['title']}",
                f"employer: {r['employer']}",
                f"posted_date: {r['posted_date'] or 'not supplied'}",
                "closing_date: not supplied by Workable XML feed",
                f"salary_evidence: {r['salary_evidence'] or 'none'}",
                f"reason: {r['classification_reason']}; duplicate={r['duplicate_status']}",
                f"source: {SOURCE}",
                f"source_job_id: {r['source_job_id']}",
                f"source_url: {r['source_url']}",
                f"apply_url: {r['apply_url']}",
                "---",
            ]

    md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(
        f"Workable London POC: {len(rows)} London; {salary_jobs} salary-bearing "
        f"({salary_pct:.1f}%); {len(reviewable_salary)} likely additional reviewable with salary"
    )


def run(feed_url: str, csv_path: Path, md_path: Path) -> int:
    try:
        rows, stats = fetch_london_jobs(feed_url)
    except (urllib.error.URLError, TimeoutError, ET.ParseError) as exc:
        raise SystemExit(f"STOP: Workable feed fetch/parse failed: {exc}") from exc
    if not rows:
        raise SystemExit("STOP: no London Workable vacancies fetched")

    exact = exact_category_titles()
    admin_register = admin.load_title_register()
    existing = current_london()
    for row in rows:
        classify(row, exact, admin_register)
        dedupe(row, existing)

    write_outputs(rows, stats, csv_path, md_path)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed-url", default=FEED_URL)
    parser.add_argument("--review-csv", type=Path, default=CSV_OUT)
    parser.add_argument("--review-md", type=Path, default=MD_OUT)
    args = parser.parse_args()
    return run(args.feed_url, args.review_csv, args.review_md)


if __name__ == "__main__":
    raise SystemExit(main())
