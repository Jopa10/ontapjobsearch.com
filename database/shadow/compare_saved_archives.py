#!/usr/bin/env python3
"""Compare two existing complete raw archives. Read-only S3 option; no imports."""
import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'pipeline/scripts'))
from plan_shadow_jobg8_import import compare_plans, project_storage
from prepare_raw_stage import fingerprint_archive

BUCKET = 'ontap-jobg8-archive-179402568934-eu-west-2-an'
OWNER = '179402568934'
PREVIOUS_SHA = '046881410cda7588c5589af808449b6e3f41c8b889955de8b57c23be426ab5bd'
PREVIOUS_DIAGNOSTICS = {'sourceRows': 43798, 'uniqueSupplierIds': 43797,
                        'exactRepeatRows': 0, 'conflictingIdsHeld': ['1401786160']}
MAX_ZIP_BYTES = 128 * 1024 * 1024


def checksum(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()


def compare(previous_path, current_path, measured):
    previous_hash, current_hash = checksum(previous_path), checksum(current_path)
    if previous_hash != PREVIOUS_SHA:
        raise ValueError('2 November archive differs from accepted pinned source')
    previous, current = fingerprint_archive(previous_path), fingerprint_archive(current_path)
    if previous['diagnostics'] != PREVIOUS_DIAGNOSTICS:
        raise ValueError('2 November source count/quarantine differs from accepted evidence')
    previous['feed_date'], current['feed_date'] = '2026-11-02', '2026-11-03'
    result = compare_plans(previous, current)
    old = {r['supplier_job_id']: r for r in previous['adverts']}
    new = {r['supplier_job_id']: r for r in current['adverts']}
    added = new.keys() - old.keys()
    changed = {ref for ref in new.keys() & old.keys() if new[ref]['content_hash'] != old[ref]['content_hash']}
    changed_bytes = sum(new[ref]['raw_bytes'] for ref in added | changed)
    # Exact compact JSON array punctuation, as used by the raw import gate.
    array_bytes = changed_bytes + max(0, len(added | changed) - 1) + 2
    reserve = 64 * 1024 * 1024
    ceiling = min(int(measured['maximumDatabaseBytes']), 800 * 1024 * 1024)
    before = int(measured['database']['bytes'])
    growth = math.ceil(array_bytes * 2.5 + len(new) * 2048)
    return {'testedAt': datetime.now(timezone.utc).isoformat(), 'mode': 'saved-archive-read-only',
        'turnover': result, 'archiveChecksums': {'previous': previous_hash, 'current': current_hash},
        'snapshots': {date: {k: v for k, v in data.items() if k != 'adverts'}
                      for date, data in [('2026-11-02', previous), ('2026-11-03', current)]},
        'fieldNamesAdded': sorted(set(current['fieldNames']) - set(previous['fieldNames'])),
        'fieldNamesAbsent': sorted(set(previous['fieldNames']) - set(current['fieldNames'])),
        'addedPreviouslyQuarantined': len(added & set(previous['diagnostics']['conflictingIdsHeld'])),
        'absentNowQuarantined': len((old.keys()-new.keys()) & set(current['diagnostics']['conflictingIdsHeld'])),
        'compactRawProjection': {'model': 'existing_compact_raw_gate_only',
            'changedOrNewAdverts': len(added | changed), 'changedOrNewRawBytes': changed_bytes,
            'changedPayloadArrayBytes': array_bytes, 'measuredDatabaseBytes': before,
            'estimatedRawGrowthBytes': growth, 'reserveBytes': reserve,
            'rawRequiredWithReserveBytes': before + growth + reserve,
            'maximumDatabaseBytes': ceiling, 'rawEstimateFits': before + growth + reserve <= ceiling,
            'selectionDisplayGrowthIncluded': False, 'importAuthorized': False,
            'limitations': 'Forecast against saved 3 November measurement, not current Neon allocation. Later selection/display growth is extra. Two dates do not establish 90-day viability.'},
        'legacyAppendProjection': project_storage(result, measured),
        'databaseChanged': False, 'productionChanged': False, 'expiryApplied': False,
        'limitations': 'Raw-field comparison using one shared parser, not selected/published-job turnover. Missing means absent, not expired; returns without earlier full history remain unknown. No 90-day retention certification.'}


def download_saved(s3, day, target):
    key = 'jobg8/raw/' + day + '.zip'
    head = s3.head_object(Bucket=BUCKET, ExpectedBucketOwner=OWNER, Key=key)
    if not 0 < head['ContentLength'] <= MAX_ZIP_BYTES:
        raise ValueError('Saved archive exceeds ZIP size bound')
    response = s3.get_object(Bucket=BUCKET, ExpectedBucketOwner=OWNER, Key=key, IfMatch=head['ETag'])
    count = 0
    try:
        with Path(target).open('xb') as stream:
            while True:
                chunk = response['Body'].read(1024 * 1024)
                if not chunk: break
                count += len(chunk)
                if count > MAX_ZIP_BYTES: raise ValueError('Download exceeds ZIP size bound')
                stream.write(chunk)
    finally:
        response['Body'].close()
    if count != head['ContentLength']:
        raise ValueError('Saved archive download length mismatch')
    return {'key': key, 'bytes': count, 'etag': head['ETag'],
            'lastModified': str(head.get('LastModified')), 'sha256': checksum(target)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--s3', action='store_true', help='Read only existing 2/3 November raw ZIPs')
    p.add_argument('--previous', type=Path)
    p.add_argument('--current', type=Path)
    p.add_argument('--measurement', type=Path, default=Path('retention-measurement-2026-11-03.json'))
    p.add_argument('--output', type=Path, default=Path('ontap-current-turnover-result.json'))
    args = p.parse_args()
    measured = json.loads(args.measurement.read_text())
    if args.s3:
        if args.previous or args.current: p.error('Choose S3 or local paths')
        import boto3
        caller = boto3.client('sts', region_name='eu-west-2').get_caller_identity()
        if caller['Account'] != OWNER: raise ValueError('Wrong AWS account')
        s3 = boto3.client('s3', region_name='eu-west-2')
        if s3.get_bucket_location(Bucket=BUCKET, ExpectedBucketOwner=OWNER).get('LocationConstraint') != 'eu-west-2':
            raise ValueError('Wrong archive region')
        with tempfile.TemporaryDirectory(prefix='ontap-turnover-') as folder:
            previous, current = Path(folder)/'previous.zip', Path(folder)/'current.zip'
            sources = {day: download_saved(s3,day,path) for day,path in
                       [('2026-11-02',previous),('2026-11-03',current)]}
            result = compare(previous,current,measured)
            result.update(s3Sources=sources,callerArn=caller['Arn'])
    else:
        if not args.previous or not args.current: p.error('Supply two local archives or --s3')
        result = compare(args.previous,args.current,measured)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    summary = {k:v for k,v in result.items() if k != 'snapshots'}
    summary['snapshots'] = {day:{k:v for k,v in snapshot.items() if k != 'fieldNames'}
                            for day,snapshot in result['snapshots'].items()}
    print(json.dumps(summary,indent=2))


if __name__ == '__main__': main()
