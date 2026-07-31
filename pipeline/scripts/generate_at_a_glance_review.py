"""Generate a review-only comparison for proposed job-card "At a glance" text.

This script never modifies published job JSON. It scans the current public app
JSON, applies deterministic evidence-based extraction rules, and writes CSV and
Markdown review outputs for human approval.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

RULE_VERSION = "1"
DEFAULT_APP_ROOT = Path("app")
DEFAULT_CSV_OUTPUT = Path("reviews/at-a-glance/at-a-glance-review.csv")
DEFAULT_MARKDOWN_OUTPUT = Path("reviews/at-a-glance/at-a-glance-review.md")

WORD_RE = re.compile(r"[A-Za-z0-9£]+(?:[’'-][A-Za-z0-9]+)*")
TRUNCATION_PATTERNS = (
    re.compile(r"\bclick apply for full job details\b", re.I),
    re.compile(r"\bclick apply for more details\b", re.I),
    re.compile(r"\bsee full job details\b", re.I),
    re.compile(r"\bfull job details(?:\s+by)?\s+click(?:ing)? apply\b", re.I),
)


@dataclass(frozen=True)
class AttributeRule:
    key: str
    label: str
    phrase: str
    patterns: tuple[re.Pattern[str], ...]
    categories: tuple[str, ...] = ("all",)


def patterns(*values: str) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(value, re.I) for value in values)


ATTRIBUTE_RULES: tuple[AttributeRule, ...] = (
    AttributeRule(
        "visitor_reception",
        "Visitor reception",
        "welcoming visitors",
        patterns(
            r"\bgreet(?:ing)? visitors\b",
            r"\bwelcome visitors\b",
            r"\bfirst point of contact for visitors\b",
            r"\breception area\b",
            r"\breception duties\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "telephone_calls",
        "Telephone handling",
        "handling telephone calls",
        patterns(
            r"\banswer(?:ing)? (?:and redirect(?:ing)? )?(?:incoming )?(?:phone|telephone) calls\b",
            r"\bmanag(?:e|ing) incoming calls\b",
            r"\btelephone enquiries\b",
            r"\bcall handling\b",
            r"\brespond(?:ing)? to (?:customer )?calls\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "customer_enquiries",
        "Customer enquiries",
        "responding to customer enquiries",
        patterns(
            r"\bcustomer enquiries\b",
            r"\bclient enquiries\b",
            r"\bcustomer quer(?:y|ies)\b",
            r"\brespond(?:ing)? to (?:general |customer |client )?enquiries\b",
            r"\bhandling (?:general |customer |client )?enquiries\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "email_inbox",
        "Email and inbox management",
        "managing emails and shared inboxes",
        patterns(
            r"\bshared (?:service )?inbox(?:es)?\b",
            r"\bmanag(?:e|ing) (?:incoming )?emails\b",
            r"\brespond(?:ing)? to (?:customer )?emails\b",
            r"\bemail enquiries\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "diary_scheduling",
        "Diary and booking coordination",
        "coordinating diaries and bookings",
        patterns(
            r"\bcoordinat(?:e|ing) diar(?:y|ies)\b",
            r"\bmanag(?:e|ing) diar(?:y|ies)\b",
            r"\bschedul(?:e|ing) meetings\b",
            r"\bschedul(?:e|ing) appointments\b",
            r"\bmeeting room bookings\b",
            r"\broom bookings\b",
            r"\bcoordinat(?:e|ing) appointments\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "records_systems",
        "Records and systems",
        "maintaining records and systems",
        patterns(
            r"\bmaintain(?:ing)? (?:accurate )?(?:customer |employee |service |job )?records\b",
            r"\bupdat(?:e|ing) (?:internal )?systems\b",
            r"\bdata entry\b",
            r"\brecords administration\b",
            r"\bmaintain(?:ing)? (?:the )?relevant systems\b",
            r"\bjob status updates\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "documents_correspondence",
        "Documents and correspondence",
        "preparing documents and correspondence",
        patterns(
            r"\bprepar(?:e|ing) documents\b",
            r"\bprepar(?:e|ing) reports\b",
            r"\bwritten correspondence\b",
            r"\bemployment contracts\b",
            r"\boffer letters\b",
            r"\bcontract changes\b",
            r"\bservice documentation\b",
            r"\bworks order documentation\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "quotations_orders",
        "Quotations and orders",
        "processing quotations and orders",
        patterns(
            r"\baccurate quotations\b",
            r"\bprepare estimates\b",
            r"\bprepar(?:e|ing) quotations\b",
            r"\braise (?:stock )?sales orders\b",
            r"\bprocess(?:ing)? (?:customer )?orders\b",
            r"\bquotations and orders\b",
            r"\bestimat(?:e|ing) (?:product )?costs\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "service_coordination",
        "Service coordination",
        "coordinating service jobs and engineer records",
        patterns(
            r"\blogging service calls\b",
            r"\bservice calls\b",
            r"\breactive and planned service jobs\b",
            r"\bengineer service records\b",
            r"\bmonitoring engineer activity\b",
            r"\bengineer call-out rotas\b",
            r"\bcustomer portals\b",
            r"\bservice sheets\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "hr_lifecycle",
        "HR lifecycle administration",
        "supporting starters, leavers and contract changes",
        patterns(
            r"\bnew starters\b",
            r"\bprocessing leavers\b",
            r"\bpre-employment checks\b",
            r"\bfull employee work cycle\b",
            r"\bemployee contracts\b",
            r"\bHR processes and procedures\b",
            r"\bflexible working\b",
            r"\bmaternity\b",
            r"\breturn to work\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "payroll_support",
        "Payroll-linked administration",
        "supporting payroll-linked administration",
        patterns(
            r"\bpayroll deadlines\b",
            r"\bHR and Payroll system\b",
            r"\bintegrated HR and Payroll\b",
            r"\bpayroll changes\b",
            r"\btimesheets\b",
            r"\btime bookings\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "mail_deliveries",
        "Mail and deliveries",
        "handling mail and deliveries",
        patterns(
            r"\bincoming and outgoing mail\b",
            r"\bmail and deliveries\b",
            r"\bpost and deliveries\b",
            r"\bhandle(?:ing)? deliveries\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "personal_care",
        "Personal care",
        "providing personal care",
        patterns(r"\bpersonal care\b", r"\bpersonal and domestic care\b"),
        ("support",),
    ),
    AttributeRule(
        "daily_living",
        "Daily living support",
        "supporting daily living",
        patterns(
            r"\baspects of daily life\b",
            r"\bdaily living\b",
            r"\bindependent living\b",
            r"\bkey life skills\b",
            r"\bdomestic care\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "community_access",
        "Community access",
        "supporting community access",
        patterns(
            r"\baccessing the community\b",
            r"\bcommunity access\b",
            r"\bsupport within the community\b",
            r"\bcommunity activities\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "medical_welfare",
        "Medical and welfare support",
        "assisting with medical and welfare needs",
        patterns(
            r"\bmedical (?:and|&) welfare needs\b",
            r"\bmedication support\b",
            r"\bhealth needs\b",
            r"\bmedical needs\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "support_plans",
        "Support plans and assessments",
        "maintaining support plans and assessments",
        patterns(
            r"\bsupport plans\b",
            r"\bSMART support plans\b",
            r"\brisk and needs assessments\b",
            r"\brisk assessments\b",
            r"\bneeds assessments\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "safeguarding",
        "Safeguarding",
        "supporting safeguarding",
        patterns(r"\bsafeguard(?:ing)?\b", r"\bprotect(?:ing)? vulnerable\b"),
        ("support",),
    ),
    AttributeRule(
        "emotional_support",
        "Emotional support",
        "providing emotional support",
        patterns(
            r"\bphysical (?:and|&) emotional support\b",
            r"\bemotional support\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "independence",
        "Promoting independence",
        "promoting independence",
        patterns(
            r"\bsupport(?:ing)? (?:service user |resident |client )?independence\b",
            r"\bempower(?:ing)? residents\b",
            r"\bachieve independence\b",
            r"\blive as independently as possible\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "incident_response",
        "Incident response",
        "responding to incidents",
        patterns(r"\brespond(?:ing)? to incidents\b", r"\bincident response\b"),
        ("support",),
    ),
    AttributeRule(
        "accommodation_support",
        "Accommodation support",
        "supporting residents in accommodation",
        patterns(
            r"\bsupported accommodation\b",
            r"\bsafe,? supportive accommodation\b",
            r"\bhelp new residents settle\b",
            r"\bresidential service\b",
        ),
        ("support",),
    ),
)


def decode_mojibake(value: str) -> str:
    return (
        value.replace("Â£", "£")
        .replace("Â", "")
        .replace("â€“", "–")
        .replace("â€”", "—")
        .replace("â€˜", "‘")
        .replace("â€™", "’")
        .replace("â€œ", "“")
        .replace("â€", "”")
        .replace("â€¢", "•")
    )


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = html.unescape(decode_mojibake(str(value))).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def strip_html(value: Any) -> str:
    text = str(value or "")
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</(?:p|div|li|h[1-6])>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return clean_text(text)


def truncate_at_word(value: str, max_chars: int) -> str:
    if len(value) <= max_chars:
        return value
    clipped = value[:max_chars]
    boundary = clipped.rfind(" ")
    safe = clipped[:boundary] if boundary > 0 else clipped
    return safe.rstrip() + "…"


def current_card_summary(job: dict[str, Any]) -> str:
    summary_source = clean_text(job.get("summary"))
    fallback_source = strip_html(
        job.get("full_description") or job.get("description") or ""
    )
    base = summary_source or fallback_source
    if not base:
        return ""
    sentence = re.split(r"(?<=[.!?])\s+", base, maxsplit=1)[0].strip()
    if sentence and len(sentence) <= 220:
        return sentence
    return truncate_at_word(base, 220)


def source_description(job: dict[str, Any]) -> str:
    return strip_html(
        job.get("full_description")
        or job.get("description")
        or job.get("/Job/Description")
        or ""
    )


def job_family(job: dict[str, Any]) -> str:
    category = clean_text(job.get("category")).casefold()
    title = clean_text(job.get("title")).casefold()
    if "support worker" in category or any(
        marker in title
        for marker in ("support worker", "care assistant", "care worker", "complex care")
    ):
        return "support"
    return "admin"


def evidence_excerpt(text: str, start: int, end: int, max_chars: int = 180) -> str:
    sentence_start = max(
        text.rfind(".", 0, start),
        text.rfind("!", 0, start),
        text.rfind("?", 0, start),
        text.rfind("\n", 0, start),
    )
    sentence_start = 0 if sentence_start < 0 else sentence_start + 1
    candidates = [
        pos
        for pos in (
            text.find(".", end),
            text.find("!", end),
            text.find("?", end),
            text.find("\n", end),
        )
        if pos >= 0
    ]
    sentence_end = min(candidates) + 1 if candidates else min(len(text), end + 120)
    excerpt = clean_text(text[sentence_start:sentence_end])
    if len(excerpt) > max_chars:
        excerpt = truncate_at_word(excerpt, max_chars)
    return excerpt


def find_attributes(description: str, family: str) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    for rule in ATTRIBUTE_RULES:
        if "all" not in rule.categories and family not in rule.categories:
            continue
        match = next(
            (
                match
                for pattern in rule.patterns
                if (match := pattern.search(description)) is not None
            ),
            None,
        )
        if match is None:
            continue
        found.append(
            {
                "key": rule.key,
                "label": rule.label,
                "phrase": rule.phrase,
                "evidence": evidence_excerpt(description, match.start(), match.end()),
            }
        )
    return found


def word_count(value: str) -> int:
    return len(WORD_RE.findall(value))


def join_phrases(phrases: list[str]) -> str:
    if not phrases:
        return ""
    if len(phrases) == 1:
        return phrases[0]
    if len(phrases) == 2:
        return f"{phrases[0]} and {phrases[1]}"
    return ", ".join(phrases[:-1]) + f" and {phrases[-1]}"


def build_summary(attributes: list[dict[str, str]]) -> tuple[str, list[dict[str, str]]]:
    if len(attributes) < 2:
        return "", []
    prefix = "The main duties described in the advert include "
    selected: list[dict[str, str]] = []
    for attribute in attributes[:6]:
        candidate = selected + [attribute]
        sentence = prefix + join_phrases([item["phrase"] for item in candidate]) + "."
        if word_count(sentence) > 25:
            break
        selected = candidate
    if len(selected) < 2:
        return "", []
    sentence = prefix + join_phrases([item["phrase"] for item in selected]) + "."
    if word_count(sentence) < 15:
        for attribute in attributes[len(selected) :]:
            candidate = selected + [attribute]
            candidate_sentence = (
                prefix + join_phrases([item["phrase"] for item in candidate]) + "."
            )
            if word_count(candidate_sentence) > 25:
                break
            selected = candidate
            sentence = candidate_sentence
            if word_count(sentence) >= 15:
                break
    if not 15 <= word_count(sentence) <= 25:
        return "", []
    return sentence, selected


def has_truncation_marker(description: str) -> bool:
    return any(pattern.search(description) for pattern in TRUNCATION_PATTERNS)


def description_hash(description: str) -> str:
    payload = f"{RULE_VERSION}\n{description}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def review_job(job: dict[str, Any], pages: Iterable[str]) -> dict[str, Any]:
    source = clean_text(job.get("source")) or "JobG8"
    description = source_description(job)
    base = {
        "job_id": clean_text(job.get("job_id")),
        "title": clean_text(job.get("title")),
        "source": source,
        "pages": " | ".join(sorted(set(pages))),
        "current_card_text": current_card_summary(job),
        "proposed_at_a_glance": "",
        "status": "omitted",
        "reason": "",
        "attributes": "",
        "evidence_json": "[]",
        "rule_version": RULE_VERSION,
        "description_hash": description_hash(description) if description else "",
    }

    if source.casefold() != "jobg8":
        base["reason"] = "external source duties are not retained for safe extraction"
        return base
    if len(description) < 120:
        base["reason"] = "description is missing or too short"
        return base
    if has_truncation_marker(description):
        base["reason"] = "description contains an explicit truncation marker"
        return base

    attributes = find_attributes(description, job_family(job))
    summary, selected = build_summary(attributes)
    if not summary:
        base["reason"] = (
            "fewer than two supported task attributes"
            if len(attributes) < 2
            else "supported attributes did not fit the 15–25 word limit"
        )
        return base

    base.update(
        {
            "proposed_at_a_glance": summary,
            "status": "generated",
            "reason": "",
            "attributes": " | ".join(item["label"] for item in selected),
            "evidence_json": json.dumps(
                [
                    {"attribute": item["label"], "evidence": item["evidence"]}
                    for item in selected
                ],
                ensure_ascii=False,
            ),
        }
    )
    return base


def iter_job_files(app_root: Path) -> Iterable[tuple[Path, list[dict[str, Any]]]]:
    for path in sorted(app_root.rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, list):
            continue
        jobs = [
            item
            for item in data
            if isinstance(item, dict)
            and (item.get("job_id") or item.get("/Job/DisplayReference"))
            and (item.get("title") or item.get("/Job/Position"))
        ]
        if jobs:
            yield path, jobs


def collect_jobs(app_root: Path) -> list[tuple[dict[str, Any], list[str]]]:
    by_id: dict[str, tuple[dict[str, Any], set[str]]] = {}
    for path, jobs in iter_job_files(app_root):
        rel = path.as_posix()
        for job in jobs:
            job_id = clean_text(job.get("job_id") or job.get("/Job/DisplayReference"))
            if not job_id:
                continue
            existing = by_id.get(job_id)
            if existing is None:
                by_id[job_id] = (job, {rel})
            else:
                existing_job, pages = existing
                pages.add(rel)
                if len(source_description(job)) > len(source_description(existing_job)):
                    by_id[job_id] = (job, pages)
    return [(job, sorted(pages)) for job, pages in by_id.values()]


CSV_FIELDS = (
    "job_id",
    "title",
    "source",
    "pages",
    "current_card_text",
    "proposed_at_a_glance",
    "status",
    "reason",
    "attributes",
    "evidence_json",
    "rule_version",
    "description_hash",
)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    generated = [row for row in rows if row["status"] == "generated"]
    omitted = [row for row in rows if row["status"] != "generated"]
    source_counts: dict[str, int] = {}
    for row in rows:
        source_counts[row["source"]] = source_counts.get(row["source"], 0) + 1

    lines = [
        "# At-a-glance review",
        "",
        f"rule_version: {RULE_VERSION}",
        f"jobs_reviewed: {len(rows)}",
        f"generated: {len(generated)}",
        f"omitted: {len(omitted)}",
        "",
        "## Source counts",
        "",
    ]
    lines.extend(f"- {source}: {count}" for source, count in sorted(source_counts.items()))
    lines.extend(["", "## Generated", ""])
    for row in generated:
        lines.extend(
            [
                "---",
                f"job_id: {row['job_id']}",
                f"title: {row['title']}",
                f"pages: {row['pages']}",
                f"current: {row['current_card_text']}",
                f"proposed: {row['proposed_at_a_glance']}",
                f"attributes: {row['attributes']}",
                f"evidence: {row['evidence_json']}",
                "---",
                "",
            ]
        )
    lines.extend(["## Omitted", ""])
    for row in omitted:
        lines.append(
            f"- {row['job_id']} — {row['title']} — {row['source']}: {row['reason']}"
        )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def build_review(app_root: Path) -> list[dict[str, Any]]:
    rows = [review_job(job, pages) for job, pages in collect_jobs(app_root)]
    return sorted(
        rows,
        key=lambda row: (
            row["status"] != "generated",
            row["source"].casefold(),
            row["title"].casefold(),
            row["job_id"],
        ),
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-root", type=Path, default=DEFAULT_APP_ROOT)
    parser.add_argument("--csv-output", type=Path, default=DEFAULT_CSV_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    rows = build_review(args.app_root)
    write_csv(args.csv_output, rows)
    write_markdown(args.markdown_output, rows)
    generated = sum(row["status"] == "generated" for row in rows)
    print(
        f"At-a-glance review: {len(rows)} unique jobs -> "
        f"{generated} generated, {len(rows) - generated} omitted. "
        f"Outputs: {args.csv_output}, {args.markdown_output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
