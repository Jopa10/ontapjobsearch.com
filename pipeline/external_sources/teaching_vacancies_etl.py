"""Canonical Teaching Vacancies review runner with audited fallbacks.

Teaching Vacancies' JobPosting JSON-LD does not always contain pay information,
even when the public advert displays either a Full time equivalent salary or a
Pay scale. This runner keeps the bounded POC behaviour, adds visible-page
fallbacks, retries transient source errors, requires two matching discovery
sweeps, and blocks incomplete or core-field-deficient reviews.
"""
from __future__ import annotations

import re
import sys
import time
import urllib.error
from html.parser import HTMLParser
from pathlib import Path

from external_sources import teaching_vacancies_poc as poc

_BASE_PARSE_JOBPOSTING = poc.parse_jobposting
_BASE_PROCESS = poc.process
_BASE_REQUEST_TEXT = poc.request_text
_BASE_LIVE_URLS = poc.live_urls
_BASE_LOAD_JOBG8 = poc.load_jobg8
PAY_LABELS = (
    "Full time equivalent salary",
    "Pay scale",
)
RETRYABLE_HTTP_STATUS = {429, 500, 502, 503, 504}
MAX_REQUEST_ATTEMPTS = 4
MIN_REQUEST_INTERVAL_SECONDS = 0.25
_last_request_started: float | None = None


class VisibleTextParser(HTMLParser):
    """Collect visible text nodes in document order, excluding page machinery."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(
        self,
        tag: str,
        _attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag.casefold() in {"script", "style", "noscript", "template"}:
            self._ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if (
            tag.casefold() in {"script", "style", "noscript", "template"}
            and self._ignored_depth
        ):
            self._ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        text = poc.clean(data)
        if text:
            self.parts.append(text)


def visible_label_value(document: str, label: str) -> str:
    """Return the visible value immediately following an exact page label."""
    parser = VisibleTextParser()
    parser.feed(document)
    target = poc.normalise(label)
    for index, part in enumerate(parser.parts):
        if poc.normalise(part) != target:
            continue
        for candidate in parser.parts[index + 1 : index + 5]:
            value = poc.clean(candidate)
            if value and poc.normalise(value) != target:
                return value
    return ""


def visible_pay_value(document: str) -> str:
    for label in PAY_LABELS:
        value = visible_label_value(document, label)
        if value:
            return value
    return ""


def parse_jobposting(document: str, url: str) -> poc.Vacancy:
    """Parse JSON-LD, then recover visible salary or pay scale if needed."""
    vacancy = _BASE_PARSE_JOBPOSTING(document, url)
    if not vacancy.salary_text:
        vacancy.salary_text = visible_pay_value(document)
    return vacancy


def _wait_for_request_slot() -> None:
    global _last_request_started
    now = time.monotonic()
    if _last_request_started is not None:
        remaining = MIN_REQUEST_INTERVAL_SECONDS - (
            now - _last_request_started
        )
        if remaining > 0:
            time.sleep(remaining)
    _last_request_started = time.monotonic()


def _retry_delay(exc: urllib.error.HTTPError, attempt: int) -> float:
    retry_after = exc.headers.get("Retry-After") if exc.headers else None
    try:
        return min(max(float(retry_after), 1.0), 30.0)
    except (TypeError, ValueError):
        return min(1.5 * (2**attempt), 12.0)


def request_text(url: str, timeout: int = 30) -> str:
    """Fetch politely and retry only transient HTTP failures."""
    for attempt in range(MAX_REQUEST_ATTEMPTS):
        _wait_for_request_slot()
        try:
            return _BASE_REQUEST_TEXT(url, timeout)
        except urllib.error.HTTPError as exc:
            if (
                exc.code not in RETRYABLE_HTTP_STATUS
                or attempt == MAX_REQUEST_ATTEMPTS - 1
            ):
                raise
            time.sleep(_retry_delay(exc, attempt))
    raise AssertionError("unreachable request retry state")


def stable_live_urls(max_pages: int = 2) -> list[str]:
    """Require two consecutive discovery sweeps to return the same URL set."""
    first = _BASE_LIVE_URLS(max_pages)
    second = _BASE_LIVE_URLS(max_pages)
    first_set = set(first)
    second_set = set(second)
    if first_set != second_set:
        added = sorted(second_set - first_set)
        missing = sorted(first_set - second_set)
        detail: list[str] = []
        if added:
            detail.append("second-sweep additions: " + ", ".join(added))
        if missing:
            detail.append("second-sweep omissions: " + ", ".join(missing))
        raise ValueError(
            "Teaching Vacancies discovery was not stable across two sweeps"
            + (f" ({'; '.join(detail)})" if detail else "")
        )
    return first


def load_jobg8(path: Path) -> list[dict]:
    """Load only JobG8 rows so retained Teaching vacancies do not self-match."""
    rows = _BASE_LOAD_JOBG8(path)
    return [
        row
        for row in rows
        if not poc.clean(row.get("source"))
        or poc.clean(row.get("source")).casefold() == "jobg8"
    ]


def validate_core_fields(vacancies: list[poc.Vacancy]) -> None:
    """Block an accepted regional review when core pay information is blank."""
    missing_pay = [
        vacancy.source_job_id or vacancy.title
        for vacancy in vacancies
        if vacancy.geography_status == "IN_SCOPE"
        and not poc.clean(vacancy.salary_text)
    ]
    if missing_pay:
        raise ValueError(
            "Teaching Vacancies field audit failed: in-scope adverts have no "
            "salary or pay scale after structured and visible-page extraction: "
            + ", ".join(sorted(missing_pay))
        )


def process(
    vacancies: list[poc.Vacancy],
    jobg8: list[dict],
) -> list[poc.Vacancy]:
    reviewed = _BASE_PROCESS(vacancies, jobg8)
    validate_core_fields(reviewed)
    return reviewed


def install_patches() -> None:
    poc.parse_jobposting = parse_jobposting
    poc.process = process
    poc.request_text = request_text
    poc.live_urls = stable_live_urls
    poc.load_jobg8 = load_jobg8


def _argument_path(args: list[str], option: str) -> Path:
    return Path(args[args.index(option) + 1])


def validate_complete_review(summary_path: Path) -> None:
    summary = summary_path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^- Detail failures: (\d+)\s*$", summary)
    if not match:
        raise ValueError("Teaching Vacancies review has no detail-failure audit")
    if int(match.group(1)):
        raise ValueError(
            "Teaching Vacancies review is incomplete: "
            + match.group(1)
            + " detail page(s) failed after retries"
        )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--report-csv" not in args:
        args.extend(
            [
                "--report-csv",
                "reviews/external/west-yorkshire-teaching-vacancies-review.csv",
            ]
        )
    if "--summary-md" not in args:
        args.extend(
            [
                "--summary-md",
                "reviews/external/west-yorkshire-teaching-vacancies-summary.md",
            ]
        )
    install_patches()
    result = poc.main(args)
    validate_complete_review(_argument_path(args, "--summary-md"))
    return result


if __name__ == "__main__":
    raise SystemExit(main())
