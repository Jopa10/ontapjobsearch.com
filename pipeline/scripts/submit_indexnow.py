#!/usr/bin/env python3
"""Submit changed public Ontap URLs to IndexNow.

The script compares two Git revisions, finds live slice JSON files that changed,
and submits the affected slice and per-job pages. Removed job URLs are included
so search engines can recrawl them and observe that they no longer exist.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable


SITE_URL = "https://www.ontapjobsearch.com"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
KEY = "fa15c7c6a1111c3fe7ec57afc723d64b"
KEY_LOCATION = f"{SITE_URL}/{KEY}.txt"
ROOT = Path(__file__).resolve().parents[2]
APP_DIR = ROOT / "app"


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        text=True,
        capture_output=True,
    )


def _jobs_from_text(content: str) -> set[str]:
    try:
        rows = json.loads(content)
    except (json.JSONDecodeError, TypeError):
        return set()
    if not isinstance(rows, list):
        return set()
    return {
        str(row["job_id"]).strip()
        for row in rows
        if isinstance(row, dict) and str(row.get("job_id", "")).strip()
    }


def _jobs_at_revision(revision: str, path: str) -> set[str]:
    result = _git("show", f"{revision}:{path}", check=False)
    if result.returncode != 0:
        return set()
    return _jobs_from_text(result.stdout)


def _slice_routes(path: str) -> set[str]:
    relative = Path(path).relative_to("app").with_suffix("").as_posix()

    if relative == "london/service-administrator-jobs":
        return {
            "/london/service-administrator-jobs",
            "/london/outer-service-administrator-jobs",
        }

    candidates = [relative]
    if relative.endswith("-jobs"):
        candidates.append(relative[: -len("-jobs")])

    for candidate in candidates:
        if (APP_DIR / candidate / "page.tsx").exists():
            return {f"/{candidate}"}
    return set()


def _changed_json_paths(before: str, after: str) -> set[str]:
    result = _git("diff", "--name-only", before, after, "--", "app")
    return {
        path
        for path in result.stdout.splitlines()
        if path.startswith("app/") and path.endswith(".json")
    }


def changed_urls(before: str, after: str) -> list[str]:
    routes = {"/", "/browse-jobs"}
    job_ids: set[str] = set()
    changed_paths = _changed_json_paths(before, after)
    if not changed_paths:
        return []

    for path in changed_paths:
        routes.update(_slice_routes(path))
        job_ids.update(_jobs_at_revision(before, path))
        job_ids.update(_jobs_at_revision(after, path))

    urls = {f"{SITE_URL}{route}" for route in routes}
    urls.update(f"{SITE_URL}/jobs/{job_id}" for job_id in job_ids)
    return sorted(urls)


def all_current_urls() -> list[str]:
    routes = {"/", "/browse-jobs"}
    job_ids: set[str] = set()

    for path in APP_DIR.rglob("*.json"):
        relative = path.relative_to(ROOT).as_posix()
        content = path.read_text(encoding="utf-8")
        ids = _jobs_from_text(content)
        if not ids:
            continue
        routes.update(_slice_routes(relative))
        job_ids.update(ids)

    urls = {f"{SITE_URL}{route}" for route in routes}
    urls.update(f"{SITE_URL}/jobs/{job_id}" for job_id in job_ids)
    return sorted(urls)


def submit(urls: Iterable[str]) -> int:
    url_list = sorted(set(urls))
    if not url_list:
        print("No changed public URLs to submit to IndexNow.")
        return 0

    payload = json.dumps(
        {
            "host": "www.ontapjobsearch.com",
            "key": KEY,
            "keyLocation": KEY_LOCATION,
            "urlList": url_list,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.status
    except urllib.error.HTTPError as error:
        status = error.code
        if status not in {200, 202}:
            raise

    if status not in {200, 202}:
        raise RuntimeError(f"Unexpected IndexNow response: HTTP {status}")

    print(f"Submitted {len(url_list)} public URLs to IndexNow (HTTP {status}).")
    for url in url_list:
        print(f"- {url}")
    return len(url_list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", default="HEAD^")
    parser.add_argument("--after", default="HEAD")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Submit all currently published slice and job URLs for initial setup.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    urls = all_current_urls() if args.all else changed_urls(args.before, args.after)

    if args.dry_run:
        print("\n".join(urls))
        print(f"Would submit {len(urls)} public URLs to IndexNow.")
        return 0

    submit(urls)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
