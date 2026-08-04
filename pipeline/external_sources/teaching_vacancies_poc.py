"""Review-only Teaching Vacancies ETL for West Yorkshire admin/service jobs.

The process mirrors Ontap's NEJobs and VONNE review workflow: it fetches public
vacancy pages, applies bounded geography/classification/deduplication rules,
loads same-day ``action:`` edits from the Markdown summary, and writes a CSV
plus an editable Markdown review. It has no approved-output or publishing path.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import ssl
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from zoneinfo import ZoneInfo

BASE_URL = "https://teaching-vacancies.service.gov.uk"
SOURCE = "Teaching Vacancies GOV.UK"
TARGET = "West Yorkshire"
USER_AGENT = "Ontap external-jobs review POC/1.0 (+https://www.ontapjobsearch.com/contact)"
SEARCH_TERMS = (
    "administrator",
    "administrative",
    "receptionist",
    "office",
    "business support",
    "exams officer",
    "personal assistant",
)
PLACES = (
    "west yorkshire", "leeds", "bradford", "wakefield", "kirklees",
    "huddersfield", "halifax", "calderdale", "dewsbury", "batley", "keighley",
    "shipley", "pudsey", "morley", "horsforth", "castleford", "pontefract",
    "ossett", "heckmondwike", "cleckheaton", "mirfield", "sowerby bridge",
    "hebden bridge", "ilkley", "otley", "wetherby", "bingley", "brighouse",
    "elland", "normanton", "knottingley",
)
POSTCODES = ("BD", "HD", "HX", "LS", "WF")
HC = (
    "administrator", "administrative assistant", "admin assistant",
    "office administrator", "office assistant", "receptionist",
    "school secretary", "secretary", "personal assistant", "pa to",
    "business support assistant", "business support officer",
    "business services officer", "attendance officer", "admissions officer",
    "exams officer", "examinations officer", "student services officer",
    "data administrator", "finance administrator",
)
POSS = (
    "office manager", "business manager", "operations officer",
    "pastoral administrator", "cover manager", "data officer",
    "attendance manager", "admissions manager", "communications officer",
    "governance professional", "clerk to governors",
)
HARD = (
    "teacher", "teaching assistant", "headteacher", "deputy head", "principal",
    "lecturer", "social worker", "caretaker", "cleaner", "chef", "cook",
    "technician", "therapist", "nurse", "counsellor", "coach", "site manager",
    "premises manager", "midday supervisor",
)
REPORT_FIELDS = (
    "final_decision",
    "title",
    "salary_text",
    "employer",
    "location",
    "posted_date",
    "closing_date",
    "classification",
    "classification_reason",
    "jobg8_check",
    "jobg8_candidate_title",
    "jobg8_candidate_employer",
    "jobg8_match_score",
    "employment_type",
    "geography_status",
    "geography_reason",
    "source_job_id",
    "source_url",
    "manual_action",
    "source",
)


@dataclass
class Vacancy:
    source: str = SOURCE
    source_job_id: str = ""
    title: str = ""
    employer: str = ""
    location: str = ""
    salary_text: str = ""
    posted_date: str = ""
    closing_date: str = ""
    employment_type: str = ""
    description_excerpt: str = ""
    source_url: str = ""
    geography_status: str = ""
    geography_reason: str = ""
    classification: str = ""
    classification_reason: str = ""
    jobg8_check: str = ""
    jobg8_candidate_title: str = ""
    jobg8_candidate_employer: str = ""
    jobg8_match_score: str = ""
    manual_action: str = ""
    final_decision: str = ""


@dataclass
class ManualDecisionState:
    selections: set[str]
    exclusions: set[str]
    reviewed_ids: set[str] = field(default_factory=set)
    review_date: str = ""
    review_fingerprint: str = ""
    rerun_mode: bool = False
    load_warning: str = ""


def empty_manual_decisions(load_warning: str = "") -> ManualDecisionState:
    return ManualDecisionState(
        selections=set(),
        exclusions=set(),
        load_warning=load_warning,
    )


def clean(value: object) -> str:
    text = html.unescape(str(value or "")).replace("\xa0", " ")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()


def normalise(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", clean(value).casefold()).strip()


def request_text(url: str, timeout: int = 30) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(
        request,
        timeout=timeout,
        context=ssl.create_default_context(),
    ) as response:
        return response.read().decode(
            response.headers.get_content_charset() or "utf-8",
            "replace",
        )


def search_url(term: str, page: int = 1) -> str:
    values = {"keyword": term, "location": TARGET, "radius": "20"}
    if page > 1:
        values["page"] = str(page)
    return BASE_URL + "/jobs?" + urllib.parse.urlencode(values)


def discover_job_urls(document: str) -> list[str]:
    links = re.findall(r'href=["\']([^"\']*)["\']', document, flags=re.I)
    output: list[str] = []
    for link in links:
        absolute = urllib.parse.urljoin(BASE_URL, html.unescape(link))
        parsed = urllib.parse.urlsplit(absolute)
        if not parsed.path.startswith("/jobs/"):
            continue
        canonical = urllib.parse.urlunsplit(
            (parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "")
        )
        if canonical not in output:
            output.append(canonical)
    return output


def parse_jobposting(document: str, url: str) -> Vacancy:
    posting = None
    scripts = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        document,
        flags=re.I | re.S,
    )
    for script in scripts:
        try:
            root = json.loads(html.unescape(script).strip())
        except json.JSONDecodeError:
            continue
        candidates = (
            root
            if isinstance(root, list)
            else root.get("@graph", [root])
            if isinstance(root, dict)
            else []
        )
        for item in candidates:
            item_type = item.get("@type") if isinstance(item, dict) else None
            if isinstance(item, dict) and (
                item_type == "JobPosting"
                or "JobPosting" in (item_type or [])
            ):
                posting = item
                break
        if posting:
            break
    if not posting:
        raise ValueError(f"No JobPosting JSON-LD found: {url}")

    organisation = posting.get("hiringOrganization") or {}
    place = posting.get("jobLocation") or {}
    if isinstance(place, list):
        place = place[0] if place else {}
    address = place.get("address", {}) if isinstance(place, dict) else {}
    location = ", ".join(
        filter(
            None,
            (
                clean(address.get("addressLocality")),
                clean(address.get("addressRegion")),
                clean(address.get("postalCode")),
            ),
        )
    )

    salary = posting.get("baseSalary") or ""
    if isinstance(salary, dict):
        value = salary.get("value") or {}
        if isinstance(value, dict):
            low = value.get("minValue")
            high = value.get("maxValue")
            unit = clean(value.get("unitText"))
            salary = (
                f"£{low}–£{high} {unit}"
                if low and high
                else clean(low or high)
            )
        else:
            salary = clean(value)

    identifier = posting.get("identifier") or ""
    if isinstance(identifier, dict):
        identifier = identifier.get("value") or identifier.get("name") or ""

    return Vacancy(
        source_job_id=clean(identifier)
        or urllib.parse.urlsplit(url).path.rstrip("/").split("/")[-1],
        title=clean(posting.get("title")),
        employer=clean(
            organisation.get("name")
            if isinstance(organisation, dict)
            else organisation
        ),
        location=location,
        salary_text=clean(salary),
        posted_date=clean(posting.get("datePosted")),
        closing_date=clean(posting.get("validThrough")),
        employment_type=clean(posting.get("employmentType")),
        description_excerpt=clean(posting.get("description"))[:1200],
        source_url=url,
    )


def geography(vacancy: Vacancy) -> tuple[str, str]:
    text = normalise(f"{vacancy.location} {vacancy.description_excerpt}")
    if any(normalise(place) in text for place in PLACES):
        return "IN_SCOPE", "West Yorkshire place marker"
    postcode_match = re.search(r"\b([A-Z]{1,2})\d", vacancy.location.upper())
    if postcode_match and postcode_match.group(1) in POSTCODES:
        return (
            "IN_SCOPE",
            f"West Yorkshire postcode area {postcode_match.group(1)}",
        )
    return "HARD_PASS", "No West Yorkshire location evidence"


def classify(vacancy: Vacancy) -> tuple[str, str]:
    title = normalise(vacancy.title)
    if vacancy.geography_status != "IN_SCOPE":
        return "HARD_PASS", vacancy.geography_reason

    hard_hits = [pattern for pattern in HARD if normalise(pattern) in title]
    clear_hits = [pattern for pattern in HC if normalise(pattern) in title]
    possible_hits = [pattern for pattern in POSS if normalise(pattern) in title]

    if hard_hits and not clear_hits:
        return "HARD_PASS", "Out-of-scope occupation: " + ", ".join(hard_hits)
    if clear_hits:
        return "HC", "Clear admin/service title: " + ", ".join(clear_hits)
    if possible_hits:
        return (
            "POSS",
            "Borderline school administration title: "
            + ", ".join(possible_hits),
        )

    duties = normalise(vacancy.description_excerpt)
    if any(
        term in duties
        for term in (
            "administrative support",
            "reception duties",
            "office support",
            "maintain records",
            "answer enquiries",
        )
    ):
        return "POSS", "Administrative duties evidenced in description"
    return "HARD_PASS", "Insufficient admin/service evidence"


def similarity(first: object, second: object) -> float:
    return SequenceMatcher(None, normalise(first), normalise(second)).ratio()


def load_jobg8(path: Path) -> list[dict]:
    if not path.exists():
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, list) else []


def compare_jobg8(
    vacancy: Vacancy,
    jobs: list[dict],
) -> tuple[str, str, str, str]:
    best_score = 0.0
    best = None
    for job in jobs:
        score = (
            0.65 * similarity(vacancy.title, job.get("title", ""))
            + 0.35
            * similarity(
                vacancy.employer,
                job.get("advertiser_name") or job.get("company", ""),
            )
        )
        if score > best_score:
            best_score = score
            best = job
    if not best:
        return "NO_MATCH", "", "", "0.000"

    status = (
        "DUPLICATE"
        if best_score >= 0.86
        else "POSSIBLE_DUPLICATE"
        if best_score >= 0.68
        else "NO_MATCH"
    )
    return (
        status,
        clean(best.get("title")),
        clean(best.get("advertiser_name") or best.get("company")),
        f"{best_score:.3f}",
    )


def process(vacancies: list[Vacancy], jobg8: list[dict]) -> list[Vacancy]:
    seen: set[str] = set()
    output: list[Vacancy] = []
    for vacancy in vacancies:
        key = normalise(
            f"{vacancy.title}|{vacancy.employer}|{vacancy.location}"
        )
        if key in seen:
            continue
        seen.add(key)

        vacancy.geography_status, vacancy.geography_reason = geography(vacancy)
        vacancy.classification, vacancy.classification_reason = classify(vacancy)
        (
            vacancy.jobg8_check,
            vacancy.jobg8_candidate_title,
            vacancy.jobg8_candidate_employer,
            vacancy.jobg8_match_score,
        ) = compare_jobg8(vacancy, jobg8)

        if vacancy.jobg8_check == "DUPLICATE":
            vacancy.classification = "HARD_PASS"
            vacancy.classification_reason = "Confirmed JobG8 duplicate"
        elif (
            vacancy.jobg8_check == "POSSIBLE_DUPLICATE"
            and vacancy.classification != "HARD_PASS"
        ):
            vacancy.classification = "POSS"
            vacancy.classification_reason = (
                "Possible JobG8 duplicate requires review"
            )

        output.append(vacancy)
    return output


def load_manual_decisions_from_markdown(
    path: Path,
    current_review_date: str,
) -> ManualDecisionState:
    """Load same-day ``action:`` edits from the Markdown review."""
    if not path.exists():
        return empty_manual_decisions()
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return empty_manual_decisions(
            f"manual review could not be read: {exc}"
        )

    date_match = re.search(
        r"(?mi)^review_date:\s*(\d{4}-\d{2}-\d{2})\s*$",
        text,
    )
    review_date = date_match.group(1) if date_match else ""
    if not review_date:
        return empty_manual_decisions(
            "manual review has no review_date; actions ignored"
        )
    if review_date != current_review_date:
        return empty_manual_decisions(
            f"manual review date {review_date} is not {current_review_date}; "
            "old actions ignored"
        )

    fingerprint_match = re.search(
        r"(?mi)^review_fingerprint:\s*([a-f0-9]{64})\s*$",
        text,
    )
    fingerprint = (
        fingerprint_match.group(1) if fingerprint_match else ""
    )

    selections: set[str] = set()
    exclusions: set[str] = set()
    reviewed_ids: set[str] = set()
    for block in re.findall(r"(?ms)^---\s*$\n(.*?)^---\s*$", text):
        action_match = re.search(
            r"(?mi)^action:\s*(select|exclude)?\s*$",
            block,
        )
        id_match = re.search(
            r"(?mi)^source_job_id:\s*(\S+)\s*$",
            block,
        )
        if not action_match or not id_match:
            continue
        action = clean(action_match.group(1)).casefold()
        source_job_id = clean(id_match.group(1))
        reviewed_ids.add(source_job_id)
        if action == "select":
            selections.add(source_job_id)
        elif action == "exclude":
            exclusions.add(source_job_id)

    selections.difference_update(exclusions)
    return ManualDecisionState(
        selections=selections,
        exclusions=exclusions,
        reviewed_ids=reviewed_ids,
        review_date=review_date,
        review_fingerprint=fingerprint,
        rerun_mode=bool(selections or exclusions),
    )


def manual_action_for(
    vacancy: Vacancy,
    decisions: ManualDecisionState,
) -> str:
    if vacancy.source_job_id in decisions.exclusions:
        return "exclude"
    if vacancy.source_job_id in decisions.selections:
        return "select"
    return ""


def final_decision_for(
    vacancy: Vacancy,
    decisions: ManualDecisionState,
) -> str:
    if vacancy.classification == "HARD_PASS":
        return "HARD_PASS"
    if vacancy.source_job_id in decisions.exclusions:
        return "EXCLUDED"
    if vacancy.source_job_id in decisions.selections:
        return "SELECTED"
    if vacancy.classification == "HC":
        return "SELECTED"
    return "POSS"


def review_fingerprint(vacancies: list[Vacancy]) -> str:
    rows = [
        {
            "source_job_id": vacancy.source_job_id,
            "title": clean(vacancy.title),
            "employer": clean(vacancy.employer),
            "location": clean(vacancy.location),
            "salary_text": clean(vacancy.salary_text),
            "posted_date": clean(vacancy.posted_date),
            "closing_date": clean(vacancy.closing_date),
            "employment_type": clean(vacancy.employment_type),
            "classification": vacancy.classification,
            "jobg8_check": vacancy.jobg8_check,
        }
        for vacancy in vacancies
        if vacancy.classification != "HARD_PASS"
    ]
    rows.sort(key=lambda row: row["source_job_id"])
    payload = json.dumps(
        rows,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def compact(value: str, maximum: int) -> str:
    text = clean(value)
    if len(text) <= maximum:
        return text
    return text[: maximum - 1].rstrip() + "…"


def review_row(
    vacancy: Vacancy,
    decisions: ManualDecisionState,
) -> dict[str, str]:
    plausible_match = vacancy.jobg8_check in {
        "DUPLICATE",
        "POSSIBLE_DUPLICATE",
    }
    return {
        "final_decision": final_decision_for(vacancy, decisions),
        "title": compact(vacancy.title, 42),
        "salary_text": compact(vacancy.salary_text, 30),
        "employer": compact(vacancy.employer, 30),
        "location": compact(vacancy.location, 38),
        "posted_date": vacancy.posted_date,
        "closing_date": vacancy.closing_date,
        "classification": vacancy.classification,
        "classification_reason": vacancy.classification_reason,
        "jobg8_check": (
            vacancy.jobg8_check
            if plausible_match
            else "No plausible JobG8 match"
        ),
        "jobg8_candidate_title": (
            vacancy.jobg8_candidate_title if plausible_match else ""
        ),
        "jobg8_candidate_employer": (
            vacancy.jobg8_candidate_employer if plausible_match else ""
        ),
        "jobg8_match_score": (
            vacancy.jobg8_match_score if plausible_match else ""
        ),
        "employment_type": vacancy.employment_type,
        "geography_status": vacancy.geography_status,
        "geography_reason": vacancy.geography_reason,
        "source_job_id": vacancy.source_job_id,
        "source_url": vacancy.source_url,
        "manual_action": manual_action_for(vacancy, decisions),
        "source": vacancy.source,
    }


def write_csv(
    path: Path,
    vacancies: list[Vacancy],
    decisions: ManualDecisionState | None = None,
) -> None:
    decisions = decisions or empty_manual_decisions()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=REPORT_FIELDS,
            lineterminator="\n",
        )
        writer.writeheader()
        for vacancy in sorted(
            vacancies,
            key=lambda item: (
                {
                    "SELECTED": 0,
                    "POSS": 1,
                    "EXCLUDED": 2,
                    "HARD_PASS": 3,
                }.get(final_decision_for(item, decisions), 9),
                item.title.casefold(),
                item.employer.casefold(),
            ),
        ):
            writer.writerow(review_row(vacancy, decisions))


def safe_markdown(value: str) -> str:
    return clean(value).replace("|", "/")


def write_summary(
    path: Path,
    vacancies: list[Vacancy],
    discovered: int,
    decisions: ManualDecisionState | None = None,
    *,
    review_date: str | None = None,
    jobg8_count: int = 0,
    failures: list[str] | None = None,
) -> None:
    decisions = decisions or empty_manual_decisions()
    failures = failures or []
    review_date = review_date or datetime.now(
        ZoneInfo("Europe/London")
    ).date().isoformat()

    classification_counts = {
        label: sum(v.classification == label for v in vacancies)
        for label in ("HC", "POSS", "HARD_PASS")
    }
    final_counts = {
        label: sum(final_decision_for(v, decisions) == label for v in vacancies)
        for label in ("SELECTED", "POSS", "EXCLUDED", "HARD_PASS")
    }
    in_scope = sum(v.geography_status == "IN_SCOPE" for v in vacancies)
    outside = sum(v.geography_status != "IN_SCOPE" for v in vacancies)
    confirmed_duplicates = sum(v.jobg8_check == "DUPLICATE" for v in vacancies)
    possible_duplicates = sum(
        v.jobg8_check == "POSSIBLE_DUPLICATE" for v in vacancies
    )

    lines = [
        "# Teaching Vacancies ETL proof-of-concept review",
        "",
        f"review_date: {review_date}",
        f"review_fingerprint: {review_fingerprint(vacancies)}",
        "",
        "Edit only the `action:` line in each editable block:",
        "",
        "- For a POSS job, use `action: select` to add it or `action: exclude` to reject it.",
        "- For a selected HC job, use `action: exclude` to remove it.",
        "- Leave `action:` blank for no change.",
        "- Commit the edit, then rerun the Teaching Vacancies process for the same review date.",
        "- Decisions are matched by `source_job_id` and expire when the review date changes.",
        "",
        "Run generated: "
        + datetime.now(ZoneInfo("Europe/London")).isoformat(timespec="seconds"),
        f"Search input: {BASE_URL}/jobs — {TARGET}, 20-mile radius",
        f"JobG8 comparison rows: {jobg8_count}",
        "",
        "## Funnel",
        "",
        f"- Teaching Vacancies detail URLs discovered: {discovered}",
        f"- Detail pages parsed successfully: {len(vacancies)}",
        f"- Detail failures: {len(failures)}",
        f"- West Yorkshire candidates retained: {in_scope}",
        f"- Outside or unmapped geography hard-passed: {outside}",
        "",
        "## Detail diagnostics",
        "",
    ]
    if failures:
        lines.extend(f"- {failure}" for failure in failures)
    else:
        lines.append("- No unresolved detail-page failures.")

    lines.extend(
        [
            "",
            "## Review outcomes",
            "",
            f"- HC: {classification_counts['HC']}",
            f"- POSS: {classification_counts['POSS']}",
            f"- Hard pass: {classification_counts['HARD_PASS']}",
            f"- Final selected after manual actions: {final_counts['SELECTED']}",
            f"- Final POSS awaiting decision: {final_counts['POSS']}",
            f"- Manually excluded: {final_counts['EXCLUDED']}",
            f"- Confirmed JobG8 duplicates: {confirmed_duplicates}",
            f"- Possible JobG8 duplicates: {possible_duplicates}",
        ]
    )
    if decisions.load_warning:
        lines.extend(["", f"- Manual review warning: {decisions.load_warning}"])

    def append_editable_block(vacancy: Vacancy) -> None:
        action = manual_action_for(vacancy, decisions)
        decision = final_decision_for(vacancy, decisions)
        lines.extend(
            [
                "---",
                f"action: {action}" if action else "action:",
                " | ".join(
                    [
                        decision,
                        TARGET,
                        safe_markdown(vacancy.location),
                        safe_markdown(vacancy.salary_text or "Not stated"),
                        safe_markdown(vacancy.title),
                    ]
                ),
                f"employer: {safe_markdown(vacancy.employer or 'Not parsed')}",
                f"closing_date: {safe_markdown(vacancy.closing_date)}",
                f"reason: {safe_markdown(vacancy.classification_reason)}",
                "source: Teaching Vacancies",
                f"source_job_id: {vacancy.source_job_id}",
                f"source_url: {vacancy.source_url}",
                "---",
                "",
            ]
        )

    for heading, status in (
        ("SELECTED", "SELECTED"),
        ("POSS — choose SELECT or EXCLUDE", "POSS"),
        ("EXCLUDED BY REVIEW", "EXCLUDED"),
    ):
        matching = sorted(
            (
                vacancy
                for vacancy in vacancies
                if final_decision_for(vacancy, decisions) == status
            ),
            key=lambda item: item.title.casefold(),
        )
        lines.extend(["", f"## {heading}", ""])
        if matching:
            for vacancy in matching:
                append_editable_block(vacancy)
        else:
            lines.append("- None.")

    hard_passes = [
        vacancy
        for vacancy in vacancies
        if final_decision_for(vacancy, decisions) == "HARD_PASS"
    ]
    lines.extend(["", "## HARD_PASS", ""])
    if hard_passes:
        for vacancy in sorted(
            hard_passes,
            key=lambda item: item.title.casefold(),
        ):
            lines.append(
                f"- [{vacancy.title}]({vacancy.source_url}) — "
                f"{vacancy.classification_reason}."
            )
    else:
        lines.append("- None after geography and deduplication checks.")

    lines.extend(
        [
            "",
            "## Safety boundary",
            "",
            "- The process writes CSV and Markdown review outputs only.",
            "- It has no command-line option or function that writes approved or live JSON.",
            "- It does not change `pipeline/output-external`, `pipeline/output-admin-service`, or `app`.",
            "- Only factual fields and a short classification excerpt are retained.",
            "- Source attribution and the original Teaching Vacancies URL are preserved.",
            "- HC/POSS rules are provisional and do not amend Ontap's permanent selection policy.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def live_urls(max_pages: int = 2) -> list[str]:
    output: list[str] = []
    for term in SEARCH_TERMS:
        for page in range(1, max_pages + 1):
            found = discover_job_urls(request_text(search_url(term, page)))
            if not found:
                break
            for url in found:
                if url not in output:
                    output.append(url)
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch-live", action="store_true")
    parser.add_argument("--max-pages", type=int, default=2)
    parser.add_argument(
        "--jobg8-json",
        type=Path,
        default=Path("../app/west-yorkshire/service-administrator-jobs.json"),
    )
    parser.add_argument(
        "--report-csv",
        type=Path,
        default=Path("reviews/external/teaching-vacancies-review.csv"),
    )
    parser.add_argument(
        "--summary-md",
        type=Path,
        default=Path("reviews/external/teaching-vacancies-summary.md"),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.fetch_live:
        raise SystemExit("STOP: this POC currently requires --fetch-live.")

    review_date = datetime.now(
        ZoneInfo("Europe/London")
    ).date().isoformat()
    decisions = load_manual_decisions_from_markdown(
        args.summary_md,
        review_date,
    )

    urls = live_urls(args.max_pages)
    parsed: list[Vacancy] = []
    failures: list[str] = []
    for url in urls:
        try:
            parsed.append(parse_jobposting(request_text(url), url))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(
                f"{url} — {type(exc).__name__}"
            )

    jobg8 = load_jobg8(args.jobg8_json)
    reviewed = process(parsed, jobg8)
    write_csv(args.report_csv, reviewed, decisions)
    write_summary(
        args.summary_md,
        reviewed,
        len(urls),
        decisions,
        review_date=review_date,
        jobg8_count=len(jobg8),
        failures=failures,
    )
    selected_count = sum(
        final_decision_for(vacancy, decisions) == "SELECTED"
        for vacancy in reviewed
    )
    print(
        f"Teaching Vacancies POC: {len(urls)} URLs -> "
        f"{len(reviewed)} parsed -> {selected_count} selected. "
        f"Reports: {args.report_csv}, {args.summary_md}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
