"""Review-only Lever London POC. Writes review CSV/MD only; never publishes."""
from __future__ import annotations

import argparse, csv, hashlib, html, json, re, sys, urllib.error, urllib.parse, urllib.request
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

SOURCE = "Lever direct employers"
REGION = "London"
UA = "Ontap external-jobs review POC/1.0 (+https://www.ontapjobsearch.com/contact)"
CONFIG = ROOT / "config/lever-employers.json"
CSV_OUT = ROOT / "reviews/external/london-lever-review.csv"
MD_OUT = ROOT / "reviews/external/london-lever-summary.md"
REGISTERS = (
    ("HR / Recruitment", "hr_recruitment_title_classification_register.csv"),
    ("Customer Service / Contact Centre", "customer_service_contact_centre_title_classification_register.csv"),
    ("Finance / Accounts", "finance_accounts_title_classification_register.csv"),
)
FIELDS = (
    "final_decision","title","employer","location","salary_text","posted_date","closing_date",
    "employment_type","workplace_type","category","classification","classification_reason",
    "duplicate_status","duplicate_candidate_title","duplicate_candidate_employer","duplicate_score",
    "source_job_id","source_url","apply_url","lever_site","manual_action","source",
)


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", html.unescape(str(value or ""))).strip()


def key(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).casefold()).strip()


def api_base(instance: str) -> str:
    return "https://api.eu.lever.co" if instance.casefold() == "eu" else "https://api.lever.co"


def get_json(url: str) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def load_sites(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [
        {"employer": clean(x.get("employer")), "site": clean(x.get("site")), "instance": clean(x.get("instance")) or "global"}
        for x in data if isinstance(x, dict) and x.get("enabled", True) and clean(x.get("employer")) and clean(x.get("site"))
    ]


def is_london(raw: dict[str, Any]) -> tuple[bool, str]:
    cats = raw.get("categories") if isinstance(raw.get("categories"), dict) else {}
    locs = [clean(cats.get("location"))]
    if isinstance(cats.get("allLocations"), list):
        locs += [clean(x) for x in cats["allLocations"]]
    locs = list(dict.fromkeys(x for x in locs if x))
    return any("london" in key(x).split() for x in locs), " | ".join(locs)


def salary(raw: dict[str, Any]) -> str:
    if clean(raw.get("salaryDescriptionPlain")):
        return clean(raw["salaryDescriptionPlain"])
    value = raw.get("salaryRange")
    if not isinstance(value, dict):
        return ""
    amounts = [str(x) for x in (value.get("min"), value.get("max")) if x not in (None, "")]
    return clean(" ".join(x for x in (clean(value.get("currency")), "–".join(amounts), clean(value.get("interval"))) if x))


def to_row(site: dict[str, str], raw: dict[str, Any]) -> dict[str, str] | None:
    london, location = is_london(raw)
    if not london:
        return None
    job_id, title = clean(raw.get("id")), clean(raw.get("text"))
    source_url, apply_url = clean(raw.get("hostedUrl")), clean(raw.get("applyUrl"))
    if not job_id or not title or not source_url.startswith("http") or not apply_url.startswith("http"):
        return None
    cats = raw.get("categories") if isinstance(raw.get("categories"), dict) else {}
    return {
        "title": title, "employer": site["employer"], "location": location, "salary_text": salary(raw),
        "posted_date": "", "closing_date": "", "employment_type": clean(cats.get("commitment")),
        "workplace_type": clean(raw.get("workplaceType")), "source_job_id": f"lever-{site['site']}-{job_id}",
        "source_url": source_url, "apply_url": apply_url, "lever_site": site["site"], "manual_action": "",
        "source": SOURCE, "category": "", "classification": "", "classification_reason": "",
        "duplicate_status": "", "duplicate_candidate_title": "", "duplicate_candidate_employer": "",
        "duplicate_score": "", "final_decision": "",
    }


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
    out = []
    for path in dict.fromkeys(paths):
        for row in json_rows(path):
            employer = clean(row.get("advertiser_name") or row.get("company") or row.get("employer"))
            title = clean(row.get("title"))
            if employer and title:
                out.append({"employer": employer, "title": title, "location": clean(row.get("location") or row.get("town"))})
    return out


def sim(a: str, b: str) -> float:
    return SequenceMatcher(None, key(a), key(b)).ratio()


def dedupe(row: dict[str, str], existing: list[dict[str, str]]) -> None:
    best_score, best = 0.0, None
    for old in existing:
        score = .45 * sim(row["employer"], old["employer"]) + .45 * sim(row["title"], old["title"]) + .10 * (sim(row["location"], old["location"]) if old["location"] else .5)
        if score > best_score:
            best_score, best = score, old
    row["duplicate_score"] = f"{best_score:.3f}" if best else ""
    if not best:
        row["duplicate_status"] = "ADDITIONAL"; return
    exact = key(row["employer"]) == key(best["employer"]) and key(row["title"]) == key(best["title"])
    if exact or best_score >= .92:
        status = "CONFIRMED_DUPLICATE"
    elif best_score >= .78:
        status = "POSSIBLE_DUPLICATE"
    else:
        status = "ADDITIONAL"
    row["duplicate_status"] = status
    if status != "ADDITIONAL":
        row["duplicate_candidate_title"], row["duplicate_candidate_employer"] = best["title"], best["employer"]


def auto_decision(row: dict[str, str]) -> str:
    if row["duplicate_status"] == "CONFIRMED_DUPLICATE": return "EXCLUDED"
    if row["classification"] in {"HARD_PASS", "OUT_OF_SCOPE"}: return "HARD_PASS"
    if row["duplicate_status"] == "POSSIBLE_DUPLICATE": return "POSS"
    return "SELECTED" if row["classification"] == "HIGH_CONFIDENCE" else "POSS"


def review_fingerprint(rows: list[dict[str, str]]) -> str:
    keep = [{k: row[k] for k in ("source_job_id","title","employer","location","salary_text","category","classification","duplicate_status","source_url","apply_url")} for row in rows]
    return hashlib.sha256(json.dumps(sorted(keep, key=lambda x: x["source_job_id"]), ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def prior_actions(path: Path, date: str, fp: str) -> dict[str, str]:
    if not path.is_file(): return {}
    text = path.read_text(encoding="utf-8-sig")
    if f"review_date: {date}" not in text or f"review_fingerprint: {fp}" not in text: return {}
    out = {}
    for block in re.findall(r"(?ms)^---\s*$\n(.*?)^---\s*$", text):
        ident = re.search(r"(?mi)^source_job_id:\s*(\S+)\s*$", block)
        action = re.search(r"(?mi)^action:\s*(select|exclude)?\s*$", block)
        if ident and action and clean(action.group(1)):
            out[clean(ident.group(1))] = clean(action.group(1)).casefold()
    return out


def rank(value: str) -> int:
    return {"SELECTED":0,"POSS":1,"EXCLUDED":2,"HARD_PASS":3}.get(value,9)


def write_outputs(rows: list[dict[str, str]], notes: list[str], csv_path: Path, md_path: Path) -> None:
    fp = review_fingerprint(rows); date = datetime.now(ZoneInfo("Europe/London")).date().isoformat()
    actions = prior_actions(md_path, date, fp)
    for row in rows:
        action = actions.get(row["source_job_id"], "")
        row["manual_action"] = action
        row["final_decision"] = "SELECTED" if action == "select" else "EXCLUDED" if action == "exclude" else auto_decision(row)
    rows.sort(key=lambda x: (rank(x["final_decision"]), x["employer"].casefold(), x["title"].casefold()))
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader(); writer.writerows(rows)
    counts = {d: sum(r["final_decision"] == d for r in rows) for d in ("SELECTED","POSS","EXCLUDED","HARD_PASS")}
    additional = sum(r["duplicate_status"] == "ADDITIONAL" and r["final_decision"] in {"SELECTED","POSS"} for r in rows)
    lines = ["# London Lever direct-employer review","",f"review_date: {date}",f"review_fingerprint: {fp}","","Edit only the action: line","",f"source: {SOURCE}",f"region: {REGION}",f"jobs_in_review: {len(rows)}",f"likely_additional_reviewable: {additional}",f"outcomes: SELECTED {counts['SELECTED']} | POSS {counts['POSS']} | EXCLUDED {counts['EXCLUDED']} | HARD_PASS {counts['HARD_PASS']}","safety: review-only POC; no approved-output or publishing path","","field_note: Lever Postings API does not supply posted/closing dates; blanks mean not supplied by source","","fetch_notes:"]
    lines += [f"- {n}" for n in notes]
    for decision in ("SELECTED","POSS","EXCLUDED","HARD_PASS"):
        lines += ["", "## POSS — choose SELECT or EXCLUDE" if decision == "POSS" else f"## {decision}", ""]
        matches = [r for r in rows if r["final_decision"] == decision]
        if not matches: lines.append("None.")
        for r in matches:
            lines += ["---",f"action: {r['manual_action']}",f"{decision} | London | {r['location']} | {r['salary_text'] or 'salary not stated'} | {r['title']}",f"employer: {r['employer']}","closing_date: not supplied by Lever Postings API",f"reason: {r['classification_reason']}; duplicate={r['duplicate_status']}",f"source: {SOURCE}",f"source_job_id: {r['source_job_id']}",f"source_url: {r['source_url']}",f"apply_url: {r['apply_url']}","---"]
    md_path.write_text("\n".join(lines).rstrip()+"\n", encoding="utf-8")
    print(f"Lever London POC: {len(rows)} London; {additional} likely additional reviewable; review files written")


def run(config: Path, csv_path: Path, md_path: Path) -> int:
    sites = load_sites(config); rows: list[dict[str,str]] = []; notes = []
    for site in sites:
        url = f"{api_base(site['instance'])}/v0/postings/{urllib.parse.quote(site['site'])}?mode=json"
        try: payload = get_json(url)
        except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            notes.append(f"{site['employer']} ({site['site']}) fetch failed: {exc}"); continue
        if not isinstance(payload, list): notes.append(f"{site['employer']} ({site['site']}) invalid payload"); continue
        before = len(rows)
        rows += [job for raw in payload if isinstance(raw, dict) and (job := to_row(site, raw))]
        notes.append(f"{site['employer']} ({site['site']}): {len(payload)} published; {len(rows)-before} London")
    if not rows: raise SystemExit("STOP: no London Lever vacancies fetched")
    exact, admin_register, existing = exact_category_titles(), admin.load_title_register(), current_london()
    for row in rows: classify(row, exact, admin_register); dedupe(row, existing)
    write_outputs(rows, notes, csv_path, md_path); return 0


def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--config", type=Path, default=CONFIG); p.add_argument("--review-csv", type=Path, default=CSV_OUT); p.add_argument("--review-md", type=Path, default=MD_OUT); a = p.parse_args()
    return run(a.config, a.review_csv, a.review_md)

if __name__ == "__main__": raise SystemExit(main())
