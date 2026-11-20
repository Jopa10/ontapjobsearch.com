"""Probe official WMJobs public endpoints before building an ETL.

This is deliberately not a scraper or publishing component. It makes a small,
fixed number of ordinary HTTPS GET requests to official WMJobs-hosted URLs,
records status/metadata, and stops. It does not bypass access controls, log in,
submit forms, enumerate record IDs, or write any live Ontap output.
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path

USER_AGENT = (
    "Ontap external-jobs source assessment/1.0 "
    "(+https://www.ontapjobsearch.com/contact)"
)

OFFICIAL_ENDPOINTS = (
    ("main_jobs", "https://www.wmjobs.co.uk/jobs/"),
    ("birmingham_jobs", "https://www.wmjobs.co.uk/jobs/birmingham/"),
    ("solihull_jobs", "https://www.wmjobs.co.uk/jobs/solihull/"),
    ("main_sitemap", "https://www.wmjobs.co.uk/sitemap.xml"),
    ("jobs_sitemap", "https://www.wmjobs.co.uk/jobs-sitemap.xml"),
    ("jobs_rss", "https://www.wmjobs.co.uk/jobsrss/"),
    (
        "solihull_search",
        "https://solihull.wm-jobs.co.uk/members/modules/job/search.php",
    ),
    (
        "solihull_public_detail",
        "https://solihull.wm-jobs.co.uk/members/modules/job/detail.php?record=2330",
    ),
)


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.links: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        name = tag.casefold()
        if name == "title":
            self.in_title = True
        elif name == "a":
            href = dict(attrs).get("href") or ""
            if href:
                self.links.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            value = re.sub(r"\s+", " ", data).strip()
            if value:
                self.title_parts.append(value)


@dataclass
class ProbeResult:
    name: str
    requested_url: str
    final_url: str = ""
    status: int = 0
    content_type: str = ""
    byte_count: int = 0
    title: str = ""
    wmjobs_detail_links: int = 0
    robots_or_challenge_signal: str = ""
    error: str = ""


def fetch_once(name: str, url: str, timeout: int = 25) -> ProbeResult:
    result = ProbeResult(name=name, requested_url=url)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xml,text/xml;q=0.9,*/*;q=0.1",
            "Range": "bytes=0-131071",
        },
    )
    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
            context=ssl.create_default_context(),
        ) as response:
            raw = response.read(131072)
            result.status = int(response.status)
            result.final_url = response.geturl()
            result.content_type = response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        result.status = int(exc.code)
        result.final_url = exc.geturl()
        result.content_type = exc.headers.get("Content-Type", "") if exc.headers else ""
        raw = exc.read(131072)
    except (urllib.error.URLError, TimeoutError, ssl.SSLError) as exc:
        result.error = f"{type(exc).__name__}: {exc}"
        return result

    result.byte_count = len(raw)
    text = raw.decode("utf-8", "replace")
    lowered = text.casefold()
    challenge_markers = (
        "access denied",
        "request blocked",
        "captcha",
        "cloudflare",
        "incapsula",
        "akamai",
        "bot detection",
    )
    result.robots_or_challenge_signal = next(
        (marker for marker in challenge_markers if marker in lowered),
        "",
    )

    if "html" in result.content_type.casefold() or "<html" in lowered:
        parser = MetadataParser()
        parser.feed(text)
        result.title = " ".join(parser.title_parts).strip()
        detail_links = {
            urllib.parse.urljoin(result.final_url or url, href)
            for href in parser.links
            if (
                "/job/" in href.casefold()
                or "modules/job/detail.php" in href.casefold()
            )
        }
        result.wmjobs_detail_links = len(detail_links)
    elif "xml" in result.content_type.casefold() or text.lstrip().startswith("<?xml"):
        result.wmjobs_detail_links = len(
            re.findall(
                r"https?://[^<\s]+(?:/job/|modules/job/detail\.php)[^<\s]*",
                text,
                flags=re.I,
            )
        )
    return result


def run(output: Path) -> list[ProbeResult]:
    results = [fetch_once(name, url) for name, url in OFFICIAL_ENDPOINTS]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "purpose": "WMJobs official-source access assessment only",
                "safety": (
                    "No access-control bypass, login, form submission, record-ID "
                    "enumeration, ETL output or publishing action was performed."
                ),
                "results": [asdict(result) for result in results],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    accessible = [result for result in results if 200 <= result.status < 300]
    print(
        f"WMJobs source probe: {len(accessible)}/{len(results)} official "
        f"endpoints returned 2xx. Report: {output}"
    )
    if not accessible:
        raise SystemExit("STOP: no official public WMJobs endpoint was accessible")
    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reviews/external/wmjobs-source-probe.json"),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    run(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
