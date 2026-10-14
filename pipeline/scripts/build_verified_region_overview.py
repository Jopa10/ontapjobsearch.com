"""Run the existing overview against the website's generated canonical inventory."""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
import sys

# This control script can run from RUNNER_TEMP while source data stays at live SHA.
sys.path.insert(0, str(Path.cwd() / 'pipeline'))
from scripts import build_daily_region_overview as overview
from scripts.live_job_source_counter import LiveInventory, LiveJob, LivePlacement, _iter_job_rows, canonical_source


def published_inventory(app_dir: Path, **_kwargs) -> LiveInventory:
    root = app_dir.parent
    published = json.loads((root / 'generated/published-jobs.json').read_text())
    aliases = json.loads((root / 'generated/published-job-canonical-ids.json').read_text())
    canonical = {row['job_id']: row for row in published}
    jobs = {}
    placements = []
    files = set()
    for path, row in _iter_job_rows(app_dir):
        job_id = str(row['job_id']).strip()
        canonical_id = aliases.get(job_id, job_id)
        if canonical_id not in canonical:
            continue
        source_file = path.relative_to(root).as_posix()
        files.add(path)
        # Preserve legitimate family placements while matching public deduplication.
        placements.append(LivePlacement(canonical_id, job_id, str(row.get('region') or 'Unspecified'), str(row.get('category') or 'Unspecified'), canonical_source(row.get('source')), source_file))
        if canonical_id not in jobs:
            item = canonical[canonical_id]
            jobs[canonical_id] = LiveJob(canonical_id, item['title'], item['location'], item['region'], item['category'], canonical_source(item['source']), item['apply_url'], source_file)
    missing = canonical.keys() - jobs.keys()
    if missing:
        raise RuntimeError(f'Published jobs lack source placements: {sorted(missing)[:5]}')
    repeated = Counter(row.canonical_job_id for row in placements)
    return LiveInventory(list(jobs.values()), placements, len(files), len(placements) - len(jobs), sum(count > 1 for count in repeated.values()))


def main() -> None:
    overview.collect_live_inventory = published_inventory
    page_inventory = overview._published_page_inventory
    def canonical_page_inventory():
        rows, counts = page_inventory()
        total = len(json.loads((Path.cwd() / 'generated/published-jobs.json').read_text()))
        counts['Total'] += total - counts['Individual job']
        counts['Individual job'] = total
        for row in rows:
            if row[0] == 'Summary' and row[1] == 'Individual job':
                row[5] = total
                row[6] = total
            if row[0] == 'Summary' and row[1] == 'All published/indexable URLs':
                row[5] = counts['Total']
        return rows, counts
    overview._published_page_inventory = canonical_page_inventory
    overview.main()


if __name__ == '__main__':
    main()
