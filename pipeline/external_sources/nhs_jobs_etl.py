"""Canonical NHS Jobs inventory runner.

The underlying review-only POC owns parsing, classification, JobG8 comparison and
output safety. This runner tightens live HTTP behaviour and pre-normalises the current
JobG8 comparison corpus. Scoring and thresholds remain identical to the POC; the
optimisation simply avoids repeating the same string normalisation millions of times.
"""
from __future__ import annotations

import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

from external_sources import nhs_jobs_poc as poc

API_PAGE_LIMIT = 100
REQUEST_TIMEOUT_SECONDS = 20
MAX_REQUEST_ATTEMPTS = 3
_ORIGINAL_LOAD_CURRENT_JOBG8 = poc.load_current_jobg8


def request_page(page: int, timeout: int = REQUEST_TIMEOUT_SECONDS) -> bytes:
    query = urllib.parse.urlencode(
        {
            "staffGroup": poc.STAFF_GROUP,
            "page": page,
            "limit": API_PAGE_LIMIT,
            "sort": "publicationDateDesc",
        }
    )
    request = urllib.request.Request(
        poc.BASE_URL + "?" + query,
        headers={
            "User-Agent": poc.USER_AGENT,
            "Accept": "application/xml,text/xml",
        },
    )
    for attempt in range(MAX_REQUEST_ATTEMPTS):
        if attempt:
            time.sleep(min(2**attempt, 8))
        try:
            with urllib.request.urlopen(
                request,
                timeout=timeout,
                context=ssl.create_default_context(),
            ) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError):
            if attempt == MAX_REQUEST_ATTEMPTS - 1:
                raise
    raise AssertionError("unreachable")


def load_current_jobg8(output_dir: Path) -> list[dict]:
    jobs = _ORIGINAL_LOAD_CURRENT_JOBG8(output_dir)
    for job in jobs:
        employer = job.get("advertiser_name") or job.get("company", "")
        job["_nhs_norm_title"] = poc.normalise(job.get("title", ""))
        job["_nhs_norm_employer"] = poc.normalise(employer)
    return jobs


def compare_jobg8(vacancy: poc.Vacancy, jobs: list[dict]) -> tuple[str, str, str, str]:
    vacancy_title = poc.normalise(vacancy.title)
    vacancy_employer = poc.normalise(vacancy.employer)
    best_score = 0.0
    best: dict | None = None

    for job in jobs:
        job_title = job.get("_nhs_norm_title")
        if job_title is None:
            job_title = poc.normalise(job.get("title", ""))
        job_employer = job.get("_nhs_norm_employer")
        if job_employer is None:
            job_employer = poc.normalise(
                job.get("advertiser_name") or job.get("company", "")
            )
        title_score = SequenceMatcher(None, vacancy_title, job_title).ratio()
        employer_score = SequenceMatcher(None, vacancy_employer, job_employer).ratio()
        score = 0.65 * title_score + 0.35 * employer_score
        if score > best_score:
            best_score = score
            best = job

    if not best:
        return "NO_MATCH", "", "", "0.000"
    status = (
        "DUPLICATE" if best_score >= 0.86 else
        "POSSIBLE_DUPLICATE" if best_score >= 0.68 else
        "NO_MATCH"
    )
    return (
        status,
        poc.clean(best.get("title")),
        poc.clean(best.get("advertiser_name") or best.get("company")),
        f"{best_score:.3f}",
    )


def main() -> int:
    poc.request_page = request_page
    poc.load_current_jobg8 = load_current_jobg8
    poc.compare_jobg8 = compare_jobg8
    return poc.main()


if __name__ == "__main__":
    raise SystemExit(main())
