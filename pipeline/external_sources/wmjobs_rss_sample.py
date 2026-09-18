"""Create a small structural sample of the public WMJobs RSS feed.

The output is diagnostic only: it contains no more than five items and truncates
all text fields. It exists solely to confirm which factual fields the RSS exposes
before the review-only ETL is implemented.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import ssl
import urllib.request
from pathlib import Path
from xml.etree import ElementTree

RSS_URL = "https://www.wmjobs.co.uk/jobsrss/"
USER_AGENT = (
    "Ontap external-jobs source assessment/1.0 "
    "(+https://www.ontapjobsearch.com/contact)"
)


def clean(value: str | None, limit: int = 700) -> str:
    text = html.unescape(value or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def fetch_xml(timeout: int = 30) -> str:
    request = urllib.request.Request(
        RSS_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml,text/xml;q=0.9,*/*;q=0.1",
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


def build_sample(xml_text: str) -> dict[str, object]:
    root = ElementTree.fromstring(xml_text)
    items = root.findall(".//item")
    samples: list[dict[str, object]] = []
    for item in items[:5]:
        children = {
            child.tag.split("}")[-1]: clean(child.text)
            for child in item
            if child.text
        }
        categories = [clean(node.text, 120) for node in item.findall("category")]
        samples.append(
            {
                "available_tags": sorted(children),
                "title": children.get("title", ""),
                "link": children.get("link", ""),
                "description": children.get("description", ""),
                "pubDate": children.get("pubDate", ""),
                "guid": children.get("guid", ""),
                "categories": categories,
            }
        )
    return {
        "source": RSS_URL,
        "item_count": len(items),
        "sample_count": len(samples),
        "samples": samples,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = build_sample(fetch_xml())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"WMJobs RSS sample: {payload['item_count']} items; "
        f"wrote {payload['sample_count']} structural samples"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
