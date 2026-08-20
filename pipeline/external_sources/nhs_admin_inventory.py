"""Review-only NHS Administrative & Clerical inventory discovery.

Uses the public NHS Jobs XML search only as a discovery transport. Downstream
selection/composition is owned by nhs_admin_service.py so the eventual official
External Job Board API can replace this transport without changing Ontap rules.
"""
from __future__ import annotations

import argparse
import json
import ssl
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

BASE_URL = "https://www.jobs.nhs.uk/api/v1/search_xml"
STAFF_GROUP = "ADMINISTRATIVE_AND_CLERICAL"
USER_AGENT = "Ontap NHS admin inventory review/1.0 (+https://www.ontapjobsearch.com/contact)"


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def child(node: ET.Element, tag: str) -> str:
    item = node.find(tag)
    return clean(item.text if item is not None else "")


def request_page(page: int, *, limit: int = 100) -> bytes:
    query = urllib.parse.urlencode({
        "staffGroup": STAFF_GROUP,
        "page": page,
        "limit": limit,
        "sort": "publicationDateDesc",
    })
    request = urllib.request.Request(
        BASE_URL + "?" + query,
        headers={"User-Agent": USER_AGENT, "Accept": "application/xml,text/xml"},
    )
    with urllib.request.urlopen(request, timeout=30, context=ssl.create_default_context()) as response:
        return response.read()


def parse_page(payload: bytes | str) -> tuple[list[dict[str, str]], int, int]:
    root = ET.fromstring(payload)
    total_pages = int(child(root, ".//totalPages") or "1")
    total_results = int(child(root, ".//totalResults") or "0")
    rows: list[dict[str, str]] = []
    for node in root.findall(".//vacancyDetails"):
        locations = ", ".join(
            clean(item.text)
            for item in node.findall("locations/location")
            if clean(item.text)
        )
        rows.append({
            "source_job_id": child(node, "id"),
            "title": child(node, "title"),
            "employer": child(node, "employer"),
            "location": locations,
            "salary_text": child(node, "salary"),
            "employment_type": child(node, "type"),
            "posted_date": child(node, "postDate"),
            "closing_date": child(node, "closeDate"),
            "source_url": child(node, "url"),
            "apply_url": child(node, "url"),
            "description": "",
            "postcode": "",
        })
    return rows, total_pages, total_results


def fetch_all(*, max_pages: int | None = None) -> tuple[list[dict[str, str]], int]:
    first = request_page(1)
    first_rows, total_pages, total_results = parse_page(first)
    if max_pages is not None:
        total_pages = min(total_pages, max_pages)
    rows = list(first_rows)
    seen = {row["source_job_id"] for row in rows if row["source_job_id"]}
    for page in range(2, total_pages + 1):
        time.sleep(0.15)
        page_rows, _pages, page_total = parse_page(request_page(page))
        if page_total and total_results and page_total != total_results:
            raise RuntimeError(
                f"NHS totalResults changed during fetch: {total_results} -> {page_total}"
            )
        for row in page_rows:
            source_id = row["source_job_id"]
            if not source_id or source_id in seen:
                continue
            seen.add(source_id)
            rows.append(row)
    return rows, total_results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-pages", type=int)
    args = parser.parse_args(argv)
    rows, total = fetch_all(max_pages=args.max_pages)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps({"reported_total": total, "rows": rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"NHS admin inventory: {len(rows)} unique rows; API reported {total}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
