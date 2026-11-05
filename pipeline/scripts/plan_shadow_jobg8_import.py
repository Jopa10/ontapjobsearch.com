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
    from openpyxl import load_workbook
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--feed-xlsx', type=Path, required=True)
    parser.add_argument('--feed-date', required=True, help='Actual supplier feed date, not execution date')
    parser.add_argument('--published-json', type=Path, help='Optional array of jobs from the SAME completed feed/publish snapshot')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--previous-feed-xlsx', type=Path, help='Previous COMPLETE saved raw feed, same adapter format')
    parser.add_argument('--previous-feed-date')
    parser.add_argument('--quarantine-duplicates', action='store_true', help='Offline only: collapse exact repeats and hold up to 15 conflicting IDs')
    parser.add_argument('--storage-receipt', type=Path, help='Saved read-only measured storage JSON')
    args = parser.parse_args()
    if bool(args.previous_feed_xlsx) != bool(args.previous_feed_date):
        parser.error('Previous feed path and date must be supplied together')
    if args.storage_receipt and not args.previous_feed_xlsx:
        parser.error('Storage projection requires previous full snapshot')
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
        values = list(dict(zip(header, row)) for row in rows)
        diagnostics = None
        if args.quarantine_duplicates:
            values, diagnostics = quarantine_rows(values)
        plan = build_plan(values, args.feed_date, published)
        if diagnostics is not None:
            plan['duplicate_diagnostics'] = diagnostics
    finally:
        workbook.close()
    if args.previous_feed_xlsx:
        previous = load_xlsx_plan(args.previous_feed_xlsx, args.previous_feed_date, args.quarantine_duplicates)
        plan['turnover'] = compare_plans(previous, plan)
        plan['snapshot_checksums'] = {
            'previous': hashlib.sha256(args.previous_feed_xlsx.read_bytes()).hexdigest(),
            'current': hashlib.sha256(args.feed_xlsx.read_bytes()).hexdigest(),
            'previous_duplicate_diagnostics': previous.get('duplicate_diagnostics'),
        }
        if args.storage_receipt:
            plan['storage_projection'] = project_storage(plan['turnover'], json.loads(args.storage_receipt.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps({k: v for k, v in plan.items() if k != 'adverts'}))


# Offline storage planning only. No lifecycle state is inferred or written.
def compare_plans(previous, current, earlier_ids=None):
    """Compare canonical full-input hashes; returns absence, never expiry."""
    if current['feed_date'] <= previous['feed_date']:
        raise ValueError('Current feed date must be after previous feed date')
    old = {x['supplier_job_id']: x for x in previous['adverts']}
    new = {x['supplier_job_id']: x for x in current['adverts']}
    overlap = old.keys() & new.keys()
    changed = {k for k in overlap if old[k]['content_hash'] != new[k]['content_hash']}
    added = new.keys() - old.keys()
    returned = added & set(earlier_ids) if earlier_ids is not None else None
    return {
        'previous_date': previous['feed_date'], 'current_date': current['feed_date'],
        'previous_count': len(old), 'current_count': len(new),
        'overlap': len(overlap), 'unchanged': len(overlap - changed),
        'changed': len(changed), 'added_vs_previous': len(added),
        'absent_vs_previous': len(old.keys() - new.keys()),
        'returned_from_earlier_history': len(returned) if returned is not None else None,
        'note': 'Absence is not expiry. Returns require earlier full ID history; otherwise unknown.',
    }


def project_storage(comparison, measured, *, safety_factor=1.5, reserve_bytes=64*1024*1024):
    """Conservative admission estimate for EXISTING append-per-run importer.

    Nine decisions = eight family scopes plus raw-stage unknowns; no assumed
    cleanup, index reclamation, decision reuse or narrowed retention.
    """
    if safety_factor < 1.5 or reserve_bytes < 64*1024*1024:
        raise ValueError('Storage headroom cannot be reduced')
    tables = {x['name']: int(x['total_bytes']) for x in measured['tables']}
    adverts = int(measured['adverts']['rows'])
    production_rows = sum(int(x['rows']) for x in measured['decisions'] if x['scope'].startswith('production:'))
    if adverts <= 0 or production_rows <= 0:
        raise ValueError('Missing measured storage baseline')
    per_identity = (tables['supplier_adverts'] + tables['jobs']) / adverts
    per_appearance = tables['advert_appearances'] / adverts
    # Include all current test/display allocation in the production unit cost:
    # deliberately conservative, not a claim of exact marginal disk growth.
    per_decision = tables['selection_decisions'] / production_rows
    n = comparison['current_count']
    pieces = {
        'new_identity_bytes': comparison['added_vs_previous'] * per_identity,
        'changed_payload_overlap_bytes': comparison['changed'] * per_identity,
        'daily_appearance_bytes': n * per_appearance,
        'nine_scoped_decision_bytes': n * 9 * per_decision,
    }
    growth = int(sum(pieces.values()) * safety_factor + 0.999999)
    current = int(measured['database']['bytes'])
    ceiling = min(int(measured['maximumDatabaseBytes']), 800*1024*1024)
    return {
        'model': 'existing_append_per_run_nine_scopes_no_cleanup',
        'components_before_headroom': {k: int(v + 0.999999) for k,v in pieces.items()},
        'safety_factor': safety_factor, 'reserve_bytes': reserve_bytes,
        'measured_database_bytes': current, 'projected_growth_bytes': growth,
        'projected_database_bytes': current + growth,
        'required_with_reserve_bytes': current + growth + reserve_bytes,
        'maximum_database_bytes': ceiling,
        'estimate_fits': current + growth + reserve_bytes < ceiling,
        'import_authorized': False,
        'limitations': 'Allocation-based estimate for comparable payload sizes; prewrite live measurement and payload-size checks still required. Not a 90-day or provider-usage certification.',
    }


def load_xlsx_plan(path, feed_date, quarantine=False):
    from openpyxl import load_workbook
    workbook = load_workbook(path, read_only=True, data_only=True)
    try:
        rows = workbook.active.iter_rows(values_only=True)
        header = next(rows)
        if len(set(header)) != len(header) or not set(FIELDS).issubset(header):
            raise ValueError('Invalid previous spreadsheet headers')
        values = list(dict(zip(header, row)) for row in rows)
        diagnostics = None
        if quarantine:
            values, diagnostics = quarantine_rows(values)
        result = build_plan(values, feed_date)
        if diagnostics is not None:
            result['duplicate_diagnostics'] = diagnostics
        return result
    finally:
        workbook.close()


def quarantine_rows(rows):
    known, conflicts, repeats, count = {}, set(), 0, 0
    for row in rows:
        count += 1
        row = {str(k): '' if v is None else str(v).strip() for k,v in row.items()}
        ref = row.get(FIELDS[0], '')
        if not ref or not row.get(FIELDS[1]) or not row.get(FIELDS[2]):
            raise ValueError('Missing identity, title or apply URL')
        if ref in known:
            if row == known[ref]:
                repeats += 1
            else:
                conflicts.add(ref)
        else:
            known[ref] = row
    if len(conflicts) > 15:
        raise ValueError('More than 15 conflicting IDs: source integrity review required')
    return [r for k,r in known.items() if k not in conflicts], {
        'source_rows': count, 'unique_ids': len(known), 'exact_repeat_rows': repeats,
        'conflicting_ids_held': sorted(conflicts),
    }


if __name__ == '__main__':
    main()
