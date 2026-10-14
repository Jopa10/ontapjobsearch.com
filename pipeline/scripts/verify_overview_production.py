"""Resolve the overview source from the live site's version, never from latest main."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import urllib.request

VERSION_URL = 'https://www.ontapjobsearch.com/api/deployment-version'


def live_sha() -> str:
    request = urllib.request.Request(VERSION_URL, headers={'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(request, timeout=30) as response:
        sha = json.load(response).get('version', '')
    if not isinstance(sha, str) or not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise RuntimeError('Production did not return a valid source commit SHA.')
    return sha


def resolve(receipt: Path | None = None, expected: str | None = None) -> str:
    sha = live_sha()
    if receipt is not None and receipt.read_text().strip() != sha:
        raise RuntimeError('Deployment receipt no longer matches live production.')
    if expected is not None and expected != sha:
        raise RuntimeError('Production changed while the overview was being built; retry against the new live commit.')
    subprocess.run(['git', 'merge-base', '--is-ancestor', sha, 'origin/main'], check=True)
    return sha


def needs_rebuild(sha: str, report: Path) -> bool:
    return not report.exists() or f'Production source commit: `{sha}`' not in report.read_text(encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path)
    parser.add_argument('--check-sha')
    parser.add_argument('--report', type=Path, default=Path('pipeline/reports-daily/daily-region-overview.md'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    sha = resolve(args.receipt, args.check_sha)
    output = f'sha={sha}\nrebuild={str(needs_rebuild(sha, args.report)).lower()}\n'
    if args.output:
        with args.output.open('a', encoding='utf-8') as handle:
            handle.write(output)
    print(output, end='')


if __name__ == '__main__':
    main()
