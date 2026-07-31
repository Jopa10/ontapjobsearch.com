"""Review-only extraction and output logic for proposed job-card summaries."""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any, Iterable

from .at_a_glance_rules import (
    ATTRIBUTE_RULES,
    DEFAULT_APP_ROOT,
    DEFAULT_CSV_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT,
    DUTY_HEADINGS,
    INSERT_HEADING_BREAKS,
    RULE_VERSION,
    STOP_HEADINGS,
    TRUNCATION_PATTERNS,
    WORD_RE,
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


def multiline_text(value: Any) -> str:
    text = html.unescape(decode_mojibake(str(value or ""))).replace("\xa0", " ")
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</(?:p|div|li|h[1-6])>", "\n", text, flags=re.I)
    text = re.sub(r"<li[^>]*>", "\n- ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    heading_pattern = "|".join(re.escape(value) for value in INSERT_HEADING_BREAKS)
    text = re.sub(
        rf"(?<=[.!?])\s*({heading_pattern})",
        r"\n\1",
        text,
        flags=re.I,
    )
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def strip_html(value: Any) -> str:
    text = html.unescape(decode_mojibake(str(value or ""))).replace("\xa0", " ")
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
    return multiline_text(
        job.get("full_description")
        or job.get("description")
        or job.get("/Job/Description")
        or ""
    )


def heading_match(line: str, headings: tuple[str, ...]) -> tuple[bool, str]:
    key = re.sub(r"[^a-z0-9' -]+", " ", line.casefold())
    key = re.sub(r"\s+", " ", key).strip(" -:")
    for heading in headings:
        if key == heading:
            return True, ""
        if key.startswith(heading):
            remainder = line[len(heading) :].lstrip(" :-")
            return True, remainder
    return False, ""


def duty_lines(description: str) -> list[str]:
    lines = [line.strip() for line in description.splitlines() if line.strip()]
    if not lines:
        return []

    has_duty_heading = any(heading_match(line, DUTY_HEADINGS)[0] for line in lines)
    captured: list[str] = []
    active = not has_duty_heading

    for line in lines:
        is_duty, remainder = heading_match(line, DUTY_HEADINGS)
        if is_duty:
            active = True
            if remainder:
                captured.append(remainder)
            continue

        is_stop, _ = heading_match(line, STOP_HEADINGS)
        if is_stop:
            if active and captured:
                active = False
            continue

        if active:
            captured.append(line)

    return [
        line
        for line in captured
        if len(clean_text(line)) >= 4
        and clean_text(line).casefold() not in {"the", "your"}
    ]


def job_family(job: dict[str, Any]) -> str:
    category = clean_text(job.get("category")).casefold()
    title = clean_text(job.get("title")).casefold()
    if "support worker" in category or any(
        marker in title
        for marker in ("support worker", "care assistant", "care worker", "complex care")
    ):
        return "support"
    return "admin"


def find_attributes(lines: list[str], family: str) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    for rule in ATTRIBUTE_RULES:
        if family not in rule.categories:
            continue
        evidence = ""
        for line in lines:
            clean_line = clean_text(line)
            if any(pattern.search(clean_line) for pattern in rule.patterns):
                evidence = truncate_at_word(clean_line, 180)
                break
        if evidence:
            found.append(
                {
                    "key": rule.key,
                    "label": rule.label,
                    "phrase": rule.phrase,
                    "evidence": evidence,
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

    prefix = "Key duties include "
    selected: list[dict[str, str]] = []
    for attribute in attributes[:7]:
        candidate = selected + [attribute]
        sentence = prefix + join_phrases([item["phrase"] for item in candidate]) + "."
        if word_count(sentence) > 22:
            break
        selected = candidate
        if len(selected) == 5:
            break

    if len(selected) < 2:
        return "", []
    return (
        prefix + join_phrases([item["phrase"] for item in selected]) + ".",
        selected,
    )


def has_truncation_marker(description: str) -> bool:
    flat = clean_text(description)
    return any(pattern.search(flat) for pattern in TRUNCATION_PATTERNS)


def description_hash(description: str) -> str:
    payload = f"{RULE_VERSION}\n{description}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def review_job(job: dict[str, Any], pages: Iterable[str]) -> dict[str, Any]:
    source = clean_text(job.get("source")) or "JobG8"
    description = source_description(job)
    lines = duty_lines(description)
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
    if len(clean_text(description)) < 120:
        base["reason"] = "description is missing or too short"
        return base
    if has_truncation_marker(description):
        base["reason"] = "description contains an explicit truncation marker"
        return base
    if not lines:
        base["reason"] = "no reliable duties section found"
        return base

    attributes = find_attributes(lines, job_family(job))
    summary, selected = build_summary(attributes)
    if not summary:
        base["reason"] = "fewer than two supported task attributes"
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
    reason_counts: dict[str, int] = {}
    for row in rows:
        source_counts[row["source"]] = source_counts.get(row["source"], 0) + 1
        if row["reason"]:
            reason_counts[row["reason"]] = reason_counts.get(row["reason"], 0) + 1

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
    lines.extend(["", "## Omission reasons", ""])
    lines.extend(f"- {reason}: {count}" for reason, count in sorted(reason_counts.items()))
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
        f"At-a-glance review v{RULE_VERSION}: {len(rows)} unique jobs -> "
        f"{generated} generated, {len(rows) - generated} omitted. "
        f"Outputs: {args.csv_output}, {args.markdown_output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
