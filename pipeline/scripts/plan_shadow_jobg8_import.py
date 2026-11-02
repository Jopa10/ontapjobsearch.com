#!/usr/bin/env python3
"""Offline import preflight. No network, database writes or selection decisions.

Read the existing XML adapter's XLSX, retaining all supplied jobs. Optionally
compare a same-feed snapshot exported from the existing published inventories.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
from uuid import UUID, uuid5
from openpyxl import load_workbook

NAMESPACE = UUID('d4b3e1f3-5642-4af8-b5e7-ce3948758134')
FIELDS = ('/Job/DisplayReference', '/Job/Position', '/Job/ApplicationURL')


def build_plan(rows, feed_date: str, published=None):
    date.fromisoformat(feed_date)
    seen = set()
    adverts = []
    for row in rows:
        values = {str(k): '' if v is None else str(v).strip() for k, v in row.items()}
        ref, title, url = (values.get(k, '') for k in FIELDS)
        if not ref or not title or not url:
            raise ValueError('Missing supplier ID, title or apply URL; no import accepted')
        if ref in seen:
            raise ValueError(f'Duplicate supplier ID: {ref}; reconcile before import')
        seen.add(ref)
        content = json.dumps(values, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
        adverts.append({
            'supplier_job_id': ref,
            'advert_id': str(uuid5(NAMESPACE, f'advert:jobg8:{ref}')),
            'initial_job_id': str(uuid5(NAMESPACE, f'job:jobg8:{ref}')),
            # Existing /jobs/[job_id] route preserved; never derive from title.
            'initial_public_id': ref,
            'seen_on': feed_date,
            'content_hash': hashlib.sha256(content.encode()).hexdigest(),
        })
    published_ids = set()
    for row in published or []:
        if str(row.get('source', '')).lower() != 'jobg8':
            continue
        ref = str(row.get('job_id', '')).strip()
        if not ref:
            raise ValueError('Published JobG8 record has no job_id')
        published_ids.add(ref)
    return {
        'mode': 'offline-preflight-only', 'feed_date': feed_date,
        'supplied': len(adverts), 'appearance_rows': len(adverts),
        'published_in_feed': len(published_ids & seen),
        'published_absent_from_feed': sorted(published_ids - seen),
        'unpublished_in_feed': len(seen - published_ids) if published is not None else None,
        'selection_note': 'Reuse production selector evidence; unpublished does not mean excluded. Missing evidence remains unknown.',
        'adverts': adverts,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--feed-xlsx', type=Path, required=True)
    parser.add_argument('--feed-date', required=True, help='Actual supplier feed date, not execution date')
    parser.add_argument('--published-json', type=Path, help='Optional array of jobs from the SAME completed feed/publish snapshot')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    workbook = load_workbook(args.feed_xlsx, read_only=True, data_only=True)
    try:
        rows = workbook.active.iter_rows(values_only=True)
        header = next(rows)
        if len(set(header)) != len(header):
            raise ValueError('Duplicate spreadsheet columns')
        if not set(FIELDS).issubset(header):
            raise ValueError('Missing required JobG8 columns')
        published = json.loads(args.published_json.read_text()) if args.published_json else None
        if published is not None and not isinstance(published, list):
            raise ValueError('Published snapshot must be a JSON array')
        plan = build_plan((dict(zip(header, row)) for row in rows), args.feed_date, published)
    finally:
        workbook.close()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps({k: v for k, v in plan.items() if k != 'adverts'}))


if __name__ == '__main__':
    main()
