"""NHS Administrative & Clerical inventory discovery and advert enrichment.

The public NHS Jobs XML search supplies discovery metadata. For the small set of
rows that Ontap's routing/classification/source-cap logic would actually publish,
we fetch the corresponding public NHS advert page and extract its job summary and
main duties. This keeps detail requests bounded to publishable rows rather than
crawling the full NHS inventory.
"""
from __future__ import annotations

import argparse
import json
import ssl
import time
import urllib.parse
import urllib.request
import warnings
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

BASE_URL = "https://www.jobs.nhs.uk/api/v1/search_xml"
STAFF_GROUP = "ADMINISTRATIVE_AND_CLERICAL"
USER_AGENT = "Ontap NHS admin inventory review/1.0 (+https://www.ontapjobsearch.com/contact)"
TOTAL_RESULTS_TOLERANCE = 15
MAX_INVENTORY_ATTEMPTS = 3


class _RetryableInventoryMovement(RuntimeError):
    """Signal a small live-inventory movement that merits a fresh sweep."""


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


def _fetch_sweep(
    *,
    max_pages: int | None,
    accept_small_movement: bool,
) -> tuple[list[dict[str, str]], int, bool]:
    first = request_page(1)
    first_rows, total_pages, total_results = parse_page(first)
    if max_pages is not None:
        total_pages = min(total_pages, max_pages)
    rows = list(first_rows)
    seen = {row["source_job_id"] for row in rows if row["source_job_id"]}
    observed_totals = {total_results} if total_results else set()
    latest_total = total_results
    page = 2
    while page <= total_pages:
        time.sleep(0.15)
        page_rows, page_count, page_total = parse_page(request_page(page))
        if page_total:
            observed_totals.add(page_total)
            latest_total = page_total
        if observed_totals and max(observed_totals) - min(observed_totals) > TOTAL_RESULTS_TOLERANCE:
            raise RuntimeError(
                "NHS totalResults moved beyond the safe fetch tolerance: "
                f"{min(observed_totals)} -> {max(observed_totals)} "
                f"(limit {TOTAL_RESULTS_TOLERANCE})"
            )
        if page_total and total_results and page_total != total_results:
            if not accept_small_movement:
                raise _RetryableInventoryMovement(
                    f"NHS totalResults changed during fetch: {total_results} -> {page_total}"
                )
            # On the final bounded attempt, follow a small increase into any newly
            # added result page. A decrease naturally leaves an empty/short last page.
            if max_pages is None:
                total_pages = max(total_pages, page_count)
            else:
                total_pages = min(max(total_pages, page_count), max_pages)
        for row in page_rows:
            source_id = row["source_job_id"]
            if not source_id or source_id in seen:
                continue
            seen.add(source_id)
            rows.append(row)
        page += 1
    return rows, latest_total, len(observed_totals) > 1


def fetch_all(*, max_pages: int | None = None) -> tuple[list[dict[str, str]], int]:
    """Fetch a coherent live inventory without failing on normal small movements.

    A changing source is swept again from page one. If all bounded attempts see a
    movement of 15 jobs or fewer, the final deduplicated sweep is accepted. A wider
    movement remains a source-level integrity failure.
    """
    last_movement: _RetryableInventoryMovement | None = None
    for attempt in range(1, MAX_INVENTORY_ATTEMPTS + 1):
        final_attempt = attempt == MAX_INVENTORY_ATTEMPTS
        try:
            rows, reported_total, moved = _fetch_sweep(
                max_pages=max_pages,
                accept_small_movement=final_attempt,
            )
        except _RetryableInventoryMovement as exc:
            last_movement = exc
            continue
        if moved:
            warnings.warn(
                "NHS inventory changed by no more than "
                f"{TOTAL_RESULTS_TOLERANCE} jobs during all fetch attempts; "
                "using the final deduplicated sweep.",
                RuntimeWarning,
                stacklevel=2,
            )
        return rows, reported_total
    raise RuntimeError(f"NHS inventory retry exhausted: {last_movement}")


class _AdvertTextParser(HTMLParser):
    """Collect useful block text while ignoring script/style content."""

    BLOCK_TAGS = {"h1", "h2", "h3", "h4", "p", "li"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.current_tag = ""
        self.current: list[str] = []
        self.blocks: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[no-untyped-def]
        tag = tag.casefold()
        if tag in {"script", "style", "noscript"}:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in self.BLOCK_TAGS:
            self._flush()
            self.current_tag = tag

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        if tag in {"script", "style", "noscript"}:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return
        if tag in self.BLOCK_TAGS and tag == self.current_tag:
            self._flush()

    def handle_data(self, data: str) -> None:
        if not self.skip_depth and self.current_tag:
            value = clean(data)
            if value:
                self.current.append(value)

    def close(self) -> None:
        super().close()
        self._flush()

    def _flush(self) -> None:
        if self.current_tag and self.current:
            value = clean(" ".join(self.current))
            if value:
                self.blocks.append((self.current_tag, value))
        self.current_tag = ""
        self.current = []


def extract_advert_description(html: bytes | str) -> str:
    """Extract public-facing summary/duties text from an NHS candidate advert."""
    text = html.decode("utf-8", errors="replace") if isinstance(html, bytes) else html
    parser = _AdvertTextParser()
    parser.feed(text)
    parser.close()

    wanted = {
        "job summary",
        "main duties of the job",
        "job responsibilities",
    }
    stop = {
        "about us",
        "details",
        "person specification",
        "employer details",
        "supporting documents",
        "privacy notice",
    }
    active = False
    parts: list[str] = []
    seen: set[str] = set()

    for tag, value in parser.blocks:
        key = value.casefold().strip()
        if tag in {"h2", "h3", "h4"}:
            if key in wanted:
                active = True
                continue
            if active and key in stop:
                active = False
                continue
        if active and tag in {"p", "li"}:
            normalized = clean(value)
            marker = normalized.casefold()
            if normalized and marker not in seen:
                seen.add(marker)
                parts.append(normalized)

    return clean(" ".join(parts))


def request_advert(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
    )
    with urllib.request.urlopen(request, timeout=30, context=ssl.create_default_context()) as response:
        return response.read()


def enrich_descriptions(
    rows: list[dict[str, str]],
    *,
    source_job_ids: set[str],
    pause_seconds: float = 0.15,
) -> tuple[list[dict[str, str]], dict[str, int]]:
    """Fetch descriptions only for the source IDs that survived Ontap publication logic."""
    enriched: list[dict[str, str]] = []
    requested = succeeded = failed = 0
    for row in rows:
        item = dict(row)
        source_id = clean(item.get("source_job_id"))
        if source_id in source_job_ids and not clean(item.get("description")):
            requested += 1
            url = clean(item.get("source_url") or item.get("apply_url"))
            try:
                if not url:
                    raise ValueError("missing source URL")
                payload = request_advert(url)
                description = extract_advert_description(payload)
                if not description:
                    raise ValueError("no advert description extracted")
                item["description"] = description
                succeeded += 1
            except Exception as exc:  # bounded per-row failure; readiness gate remains fail-closed
                item["description_fetch_error"] = clean(exc)
                failed += 1
            if pause_seconds:
                time.sleep(pause_seconds)
        enriched.append(item)
    return enriched, {"requested": requested, "succeeded": succeeded, "failed": failed}


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
