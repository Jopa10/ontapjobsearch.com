"""Canonical bounded NHS Jobs inventory runner.

The underlying review-only POC owns parsing, classification, JobG8 comparison and
output safety. This runner only tightens live HTTP behaviour: NHS search_xml supports
up to 100 listings per page, so request that maximum and sort newest first. This avoids
walking hundreds or thousands of unnecessarily small pages during inventory review.
"""
from __future__ import annotations

import ssl
import time
import urllib.error
import urllib.parse
import urllib.request

from external_sources import nhs_jobs_poc as poc

API_PAGE_LIMIT = 100
REQUEST_TIMEOUT_SECONDS = 20
MAX_REQUEST_ATTEMPTS = 3


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


def main() -> int:
    poc.request_page = request_page
    return poc.main()


if __name__ == "__main__":
    raise SystemExit(main())
