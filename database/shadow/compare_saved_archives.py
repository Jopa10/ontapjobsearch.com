#!/usr/bin/env python3
"""Compare two existing complete raw archives. Read-only S3 option; no imports."""
import argparse
import gzip
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
BASELINE_SHA = '0629696a63fef39d0e7bc3b4c13e6f1b46424cb96654f9794bac8410d3468d76'
BASELINE_BYTES = 8147866
BASELINE_KEY = 'ontap-shadow/display-v1/11111111-1111-5111-8111-111111111111/' + BASELINE_SHA + '.json.gz'


def checksum(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()


def load_pinned_baseline(path):
    """Read exact source hashes from the already-verified full fixture archive.

    This reuses historical evidence, not synthetic dependency metadata as proof.
    """
    if Path(path).stat().st_size != BASELINE_BYTES or checksum(path) != BASELINE_SHA:
        raise ValueError('Pinned full archive checksum/length mismatch')
    with gzip.open(path,'rb') as stream:
        data = stream.read(384 * 1024 * 1024 + 1)
    if len(data) > 384 * 1024 * 1024:
        raise ValueError('Pinned full archive exceeds decompression bound')
    packet = json.loads(data)
    del data
    if packet.get('version') != 1 or packet.get('feedDate') != '2026-11-02':
        raise ValueError('Pinned baseline identity mismatch')
    state = packet['state']
    if state['report']['archiveSha256'] != PREVIOUS_SHA:
        raise ValueError('Pinned baseline raw-source mismatch')
    refs = state['sourceHashes']
    expected = PREVIOUS_DIAGNOSTICS['uniqueSupplierIds'] - len(PREVIOUS_DIAGNOSTICS['conflictingIdsHeld'])
    if len(refs) != expected or len({row[0] for row in refs}) != expected:
        raise ValueError('Pinned baseline membership mismatch')
    import re
    if any(not isinstance(ref,str) or not ref or not re.fullmatch('[a-f0-9]{64}',h) for ref,h in refs):
        raise ValueError('Invalid pinned source hashes')
    return {'feed_date':'2026-11-02','adverts':[{'supplier_job_id':ref,'content_hash':h} for ref,h in refs]}


def compare(previous_path, current_path, measured, baseline=None):
    previous_hash, current_hash = checksum(previous_path), checksum(current_path)
    previous, current = fingerprint_archive(previous_path), fingerprint_archive(current_path)
    pin_matches = previous_hash == PREVIOUS_SHA
    if pin_matches and previous['diagnostics'] != PREVIOUS_DIAGNOSTICS:
        raise ValueError('Pinned 2 November count/quarantine differs from accepted evidence')
    previous['feed_date'], current['feed_date'] = '2026-11-02', '2026-11-03'
    daily = compare_plans(previous, current)
    old = {r['supplier_job_id']:r for r in previous['adverts']}
    new = {r['supplier_job_id']:r for r in current['adverts']}
    added = new.keys()-old.keys()
    result = {'testedAt':datetime.now(timezone.utc).isoformat(),'mode':'saved-archive-read-only',
        'turnover':daily,'archiveChecksums':{'previous':previous_hash,'current':current_hash},
        'snapshots':{day:{k:v for k,v in data.items() if k!='adverts'} for day,data in
                     [('2026-11-02',previous),('2026-11-03',current)]},
        'fieldNamesAdded':sorted(set(current['fieldNames'])-set(previous['fieldNames'])),
        'fieldNamesAbsent':sorted(set(previous['fieldNames'])-set(current['fieldNames'])),
        'addedPreviouslyQuarantined':len(added & set(previous['diagnostics']['conflictingIdsHeld'])),
        'absentNowQuarantined':len((old.keys()-new.keys()) & set(current['diagnostics']['conflictingIdsHeld'])),
        'databaseChanged':False,'productionChanged':False,'expiryApplied':False,
        'limitations':'Daily S3 turnover and Neon-baseline turnover are distinct. Raw absence is not expiry; returns without earlier complete history remain unknown. No import or 90-day certification.'}
    if pin_matches:
        budget_previous = previous
        linkage = 'exact raw ZIP matches accepted Neon source'
    elif baseline is not None:
        budget_previous = baseline
        identical = {r['supplier_job_id']:r['content_hash'] for r in baseline['adverts']} == {ref:r['content_hash'] for ref,r in old.items()}
        linkage = 'ZIP differs, clean raw hashes match pinned baseline' if identical else 'daily S3 snapshot differs from pinned Neon snapshot; budget uses pinned source hashes separately'
    else:
        result.update(databaseBaselineLink={'verified':False,'previousZipMatchesNeonPin':False},
            databaseBaselineTurnover=None,compactRawProjection=None,legacyAppendProjection=None,
            storageProjectionBlocked='Daily ZIP differs from Neon test source and no verified pinned source-hash baseline was supplied')
        return result
    baseline_turnover = compare_plans(budget_previous,current)
    prior = {r['supplier_job_id']:r for r in budget_previous['adverts']}
    changed = {ref for ref in new if ref not in prior or new[ref]['content_hash']!=prior[ref]['content_hash']}
    changed_bytes = sum(new[ref]['raw_bytes'] for ref in changed)
    array_bytes = changed_bytes + max(0,len(changed)-1)+2
    reserve = 64*1024*1024
    ceiling = min(int(measured['maximumDatabaseBytes']),800*1024*1024)
    before = int(measured['database']['bytes'])
    growth = math.ceil(array_bytes*2.5 + len(new)*2048)
    result.update(databaseBaselineLink={'verified':True,'previousZipMatchesNeonPin':pin_matches,
            'explanation':linkage,'pinnedSourceArchiveSha256':PREVIOUS_SHA},
        databaseBaselineTurnover=baseline_turnover,
        compactRawProjection={'model':'existing_compact_raw_gate_only_vs_pinned_neon_source',
            'changedOrNewAdverts':len(changed),'changedOrNewRawBytes':changed_bytes,
            'changedPayloadArrayBytes':array_bytes,'measuredDatabaseBytes':before,
            'estimatedRawGrowthBytes':growth,'reserveBytes':reserve,
            'rawRequiredWithReserveBytes':before+growth+reserve,'maximumDatabaseBytes':ceiling,
            'rawEstimateFits':before+growth+reserve<=ceiling,
            'selectionDisplayGrowthIncluded':False,'importAuthorized':False,
            'limitations':'Forecast against saved 3 November allocation; extra selection/display growth and actual Neon allocation remain unmeasured.'},
        legacyAppendProjection=project_storage(baseline_turnover,measured))
    return result


def download_saved(s3, day, target):
    return download_object(s3, 'jobg8/raw/' + day + '.zip', target)


def download_object(s3, key, target):
    if key not in {'jobg8/raw/2026-11-02.zip','jobg8/raw/2026-11-03.zip',BASELINE_KEY}:
        raise ValueError('Unapproved saved object key')
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
    p.add_argument('--baseline',type=Path,default=Path('ontap-full-display-2026-11-02.json.gz'))
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
            args.output.with_suffix('.sources.json').write_text(json.dumps(sources,indent=2)+'\n')
            baseline_path = args.baseline
            if not baseline_path.is_file():
                baseline_path = Path(folder)/'pinned-baseline.json.gz'
                sources['pinnedBaseline'] = download_object(s3,BASELINE_KEY,baseline_path)
                args.output.with_suffix('.sources.json').write_text(json.dumps(sources,indent=2)+'\n')
            baseline = load_pinned_baseline(baseline_path)
            result = compare(previous,current,measured,baseline)
            result['pinnedBaselineArchiveSha256'] = BASELINE_SHA
            result.update(s3Sources=sources,callerArn=caller['Arn'])
    else:
        if not args.previous or not args.current: p.error('Supply two local archives or --s3')
        baseline = load_pinned_baseline(args.baseline) if args.baseline.is_file() else None
        result = compare(args.previous,args.current,measured,baseline)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    summary = {k:result[k] for k in ['testedAt','turnover','databaseBaselineLink',
        'databaseBaselineTurnover','compactRawProjection','databaseChanged','productionChanged']}
    summary['sourceCounts'] = {day:snapshot['diagnostics'] for day,snapshot in result['snapshots'].items()}
    summary['outputFile'] = str(args.output)
    if result.get('storageProjectionBlocked'):
        summary['storageProjectionBlocked'] = result['storageProjectionBlocked']
    print(json.dumps(summary,indent=2))


if __name__ == '__main__': main()
