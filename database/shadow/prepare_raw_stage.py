"""Prepare deterministic nested samples from one archived JobG8 ZIP. No network."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET
import zipfile


def flatten(node, path, out):
    children = list(node)
    if not children:
        key = '/' + '/'.join(path)
        value = (node.text or '').strip()
        if not out.get(key):
            out[key] = value
    for child in children:
        flatten(child, path + [child.tag.rsplit('}', 1)[-1]], out)


def load_archive(path):
    with zipfile.ZipFile(path) as archive:
        names = [n for n in archive.namelist() if Path(n).name.lower() == 'jobs.xml']
        if len(names) != 1:
            raise ValueError('Expected exactly one Jobs.xml')
        with archive.open(names[0]) as handle:
            root = ET.parse(handle).getroot()
    by_id = {}
    conflicting_ids = set()
    total_rows = 0
    exact_repeats = 0
    for node in root.iter():
        if node.tag.rsplit('}', 1)[-1].lower() != 'job':
            continue
        row = {}
        flatten(node, ['Job'], row)
        ref = row.get('/Job/DisplayReference', '').strip()
        if not ref or not row.get('/Job/Position') or not row.get('/Job/ApplicationURL'):
            raise ValueError('Missing supplier identity, title or apply URL in archive')
        total_rows += 1
        if ref in by_id:
            if row == by_id[ref]:
                exact_repeats += 1
            else:
                conflicting_ids.add(ref)
        else:
            by_id[ref] = row
    if len(conflicting_ids) > 15:
        raise ValueError(f'Source integrity review needed: {len(conflicting_ids)} conflicting IDs')
    rows = [row for ref, row in by_id.items() if ref not in conflicting_ids]
    if not 1 <= total_rows <= 60000 or not rows:
        raise ValueError('Archive outside bounded 1–60,000 record test capacity')
    # Hash ordering spreads sectors/locations; prefixes are nested at every stage.
    rows = sorted(rows, key=lambda r: hashlib.sha256(r['/Job/DisplayReference'].encode()).hexdigest())
    return rows, {'sourceRows': total_rows, 'uniqueSupplierIds': len(by_id),
                  'exactRepeatRows': exact_repeats, 'conflictingIdsHeld': sorted(conflicting_ids)}


def prepare(path, percentage, archive_date, revision, budget):
    rows, diagnostics = load_archive(path)
    selected = rows[:max(1, len(rows) * percentage // 100)]
    payload_bytes = sum(len(json.dumps(r, ensure_ascii=False).encode()) for r in selected)
    return {'archiveDate': archive_date, 'observedOn': archive_date,
            'archiveSha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'sourceRevision': revision, 'percentage': percentage, 'totalReceived': diagnostics['sourceRows'],
            'eligibleRecords': len(rows), 'receiptDiagnostics': diagnostics,
            'rawPayloadBytes': payload_bytes, 'maximumDatabaseBytes': budget,
            'records': selected}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--request', type=Path, required=True)
    p.add_argument('--percentage', type=int, choices=[20, 50, 100], required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    request = json.loads(args.request.read_text())
    result = prepare(args.archive, args.percentage, request['archiveDate'],
                     request['sourceRevision'], request['maximumDatabaseBytes'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(args.output, 'wt', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False)
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}))
