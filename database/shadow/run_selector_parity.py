"""Replay pinned JobG8 through unchanged production entry points in scratch only."""
import argparse
from collections import Counter
import csv
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from prepare_raw_stage import load_archive
from selector_capture import Capture, MODULES
from dependency_provenance import start_capture, verify_copy, finish_capture

PIN = '046881410cda7588c5589af808449b6e3f41c8b889955de8b57c23be426ab5bd'
FAMILIES = ['admin_service', 'support_worker', 'customer_sales', 'finance_accounts',
            'hr_recruitment', 'marketing', 'legal_assistant_paralegal', 'customer_service_contact_centre']


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def resolve_source_request(path):
    # Keep the historical command pinned exactly as before unless a caller
    # explicitly supplies the owner-verified fresh-source checkpoint.
    if path is None:
        return {'feedDate': None, 'archiveSha256': PIN, 'sizeBytes': None,
                'sourceRows': 43798, 'cleanRecords': 43796,
                'conflictingIdsHeld': ['1401786160'], 'metadata': None,
                'requestPath': None, 'requestSha256': None}

    expected_path = HERE / 'fresh-integration-prep-checkpoint-2026-11-03.json'
    if path.resolve() != expected_path.resolve():
        raise ValueError('Fresh-source request must be the pinned preparation checkpoint')
    raw = path.read_bytes()
    checkpoint = json.loads(raw)
    if checkpoint.get('sourceChecksumPrerequisiteResolved') is not True:
        raise ValueError('Pinned source checksum prerequisite is unresolved')
    pinned = checkpoint.get('pinnedSavedSource')
    if not isinstance(pinned, dict):
        raise ValueError('Missing owner-pinned saved-source metadata')
    checksum = pinned.get('archiveChecksums', {}).get('current')
    sources = pinned.get('s3Sources', {})
    matches = [(date, item) for date, item in sources.items()
               if isinstance(item, dict) and item.get('sha256') == checksum]
    if len(matches) != 1:
        raise ValueError('Pinned current source must identify exactly one S3 object')
    feed_date, item = matches[0]
    counts = checkpoint.get('expectedCurrentCounts', {})
    expected_conflicts = ['1401786160']
    if (feed_date != checkpoint.get('date')
            or item.get('key') != f'jobg8/raw/{feed_date}.zip'
            or pinned.get('bucket') != 'ontap-jobg8-archive-179402568934-eu-west-2-an'
            or pinned.get('region') != 'eu-west-2'
            or not isinstance(item.get('bytes'), int) or item['bytes'] <= 0
            or not isinstance(item.get('etag'), str) or not item['etag']
            or item.get('sha256') != checksum
            or counts.get('sourceRows') != 44432
            or counts.get('cleanRecords') != 44430
            or counts.get('conflictingIdsHeld') != expected_conflicts):
        raise ValueError('Pinned saved-source request does not match the approved 3 November feed')
    metadata = {'feedDate': feed_date, 'bucket': pinned['bucket'],
                'region': pinned['region'], 'key': item['key'],
                'sizeBytes': item['bytes'], 'etag': item['etag'],
                'sha256': item['sha256']}
    return {'feedDate': feed_date, 'archiveSha256': item['sha256'],
            'sizeBytes': item['bytes'], 'sourceRows': counts['sourceRows'],
            'cleanRecords': counts['cleanRecords'],
            'conflictingIdsHeld': expected_conflicts, 'metadata': metadata,
            'requestPath': str(path), 'requestSha256': hashlib.sha256(raw).hexdigest()}


def child(work, observe):
    sys.stdout.reconfigure(line_buffering=True)
    os.chdir(work / 'pipeline')
    sys.path.insert(0, str(work / 'pipeline'))
    from scripts import service_admin_pipeline_north_yorkshire as admin
    from scripts import support_worker_pipeline_live_config as support
    from scripts.slice_registry import live_slices
    from scripts.slice_catalog import category_meta, output_filename
    functions = []
    if observe:
        from importlib import import_module
        for name in MODULES:
            module = import_module('scripts.' + name)
            for entry in ('main', 'run_live_registered_categories', 'keep_job'):
                function = getattr(module, entry, None)
                if callable(function) and hasattr(function, '__code__'):
                    functions.append(function)
    observer = Capture(work / 'pipeline/scripts', functions)
    if observe:
        observer.__enter__()
    try:
        if admin.main() or support.main():
            raise RuntimeError('Production entry point failed')
    finally:
        if observe:
            observer.__exit__()
    outputs = {}
    for region, family in sorted(live_slices()):
        if family not in FAMILIES:
            continue
        path = Path(category_meta(family)['output_dir']) / output_filename(region, family)
        rows = json.loads(path.read_text())
        if any(row.get('source') != 'JobG8' for row in rows):
            raise RuntimeError('Unexpected non-JobG8 output')
        outputs[family + ':' + region] = rows
    (work / 'outputs.json').write_text(json.dumps(outputs, ensure_ascii=False))
    if observe:
        evidence = {family: {} for family in FAMILIES}
        for (family, ref), record in observer.records.items():
            evidence[family][ref] = record
        # Existing actual selector reports are authoritative, including review outcomes.
        for family, path in [
            ('admin_service', Path('reports-daily/decision-report-admin-service.csv')),
            ('support_worker', Path('reports-daily/decision-report-support-worker.csv')),
            ('customer_service_contact_centre', Path('output-admin-service/registered-category-decision-report.csv')),
        ]:
            with path.open(encoding='utf-8-sig') as handle:
                for row in csv.DictReader(handle):
                    ref = row['job_id'].strip()
                    state = row.get('decision', '')
                    decision = 'include' if state == 'SELECTED' else 'review' if state.startswith(('POSS', 'REVIEW')) or row.get('selector_outcome') == 'DAILY_REVIEW' else 'exclude'
                    evidence[family][ref] = {'decision': decision, 'reason': row.get('reason') or state, 'gate': 'production decision report: ' + state}
        # Actual output wins over intermediate states. Never infer exclusion from absence.
        for scope, rows in outputs.items():
            family = scope.split(':', 1)[0]
            for row in rows:
                ref = str(row['job_id'])
                prior = evidence[family].get(ref, {})
                reason = next((v for k, v in row.items() if k.endswith('_reason') and v), None)
                evidence[family][ref] = {'decision': 'include', 'reason': reason or prior.get('reason') or 'Selected by production output', 'gate': 'production output'}
        (work / 'evidence.json').write_text(json.dumps(evidence, ensure_ascii=False))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--archive', type=Path)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--child', choices=['plain', 'observed'])
    p.add_argument('--source-request', type=Path, help='Use the exact owner-pinned fresh saved-source checkpoint')
    args = p.parse_args()
    work = args.work.resolve()
    if args.child:
        child(work, args.child == 'observed')
        return
    if args.archive is None:
        raise ValueError('An archived source ZIP is required')
    archive = args.archive.resolve()
    source = resolve_source_request(args.source_request)
    actual_size = archive.stat().st_size
    actual_sha256 = hashlib.sha256(archive.read_bytes()).hexdigest()
    if actual_sha256 != source['archiveSha256']:
        raise ValueError('Saved source SHA-256 mismatch')
    if source['sizeBytes'] is not None and actual_size != source['sizeBytes']:
        raise ValueError('Saved source byte count mismatch')
    records, receipt = load_archive(archive)
    if (receipt['sourceRows'] != source['sourceRows']
            or len(records) != source['cleanRecords']
            or receipt['conflictingIdsHeld'] != source['conflictingIdsHeld']):
        raise ValueError('Saved source row/quarantine receipt mismatch')
    if source['feedDate']:
        current_date = os.environ.get('ONTAP_FEED_DATE')
        if current_date and current_date != source['feedDate']:
            raise ValueError('ONTAP_FEED_DATE conflicts with pinned source date')
        os.environ['ONTAP_FEED_DATE'] = source['feedDate']
    if work.exists():
        raise ValueError('Use a new scratch work directory')
    capture = start_capture(ROOT)
    work.mkdir(parents=True)
    if source['requestPath']:
        shutil.copy2(source['requestPath'], work / 'source-request.json')
    (work / 'dependency-start.json').write_text(json.dumps(capture, indent=2) + '\n')
    # Use the actual production XML adapter and its source timestamp. Remove only
    # the already quarantined conflicting ID; preserve supplier order for dedupe.
    sys.path.insert(0, str(ROOT))
    from pipeline.scripts.jobg8_xml_adapter import convert, _stamp_workbook_core_timestamp
    import openpyxl
    converted = work / 'jobg8.xlsx'
    convert(archive, converted, receipt['sourceRows'], receipt['sourceRows'])
    book = openpyxl.load_workbook(converted, read_only=True)
    stamp = book.properties.created
    rows = book.active.values
    columns = next(rows)
    ref_column = columns.index('/Job/DisplayReference')
    clean = openpyxl.Workbook(write_only=True)
    sheet = clean.create_sheet('Jobs')
    sheet.append(columns)
    for row in rows:
        if str(row[ref_column]) not in receipt['conflictingIdsHeld']:
            sheet.append(row)
    clean.save(work / 'clean.xlsx')
    book.close()
    _stamp_workbook_core_timestamp(work / 'clean.xlsx', stamp)
    for mode in ['plain', 'observed']:
        target = work / mode
        # Registers, frozen boundaries, geography, and current durable owner actions
        # are copied verbatim. No live output, review or store is written.
        shutil.copytree(ROOT / 'pipeline', target / 'pipeline', ignore=shutil.ignore_patterns(
            'input', 'input-jobg8-archive', 'output-*', 'reports-*', '__pycache__'))
        (target / '.git').symlink_to(ROOT / '.git', target_is_directory=True)
        (target / 'pipeline/input').mkdir()
        shutil.copy2(work / 'clean.xlsx', target / 'pipeline/input/jobg8.xlsx')
        verify_copy(capture, target)
    from concurrent.futures import ThreadPoolExecutor, wait
    def replay(mode):
        target = work / mode
        with (work / (mode + '.log')).open('w') as log:
            subprocess.run([sys.executable, str(Path(__file__).resolve()), '--work', str(target), '--child', mode], stdout=log, stderr=subprocess.STDOUT, check=True)
        print(mode + ' production replay complete', flush=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending = {pool.submit(replay, mode) for mode in ['plain', 'observed']}
        while pending:
            done, pending = wait(pending, timeout=60)
            for future in done:
                future.result()
            for mode in ['plain', 'observed']:
                log = work / (mode + '.log')
                lines = log.read_text(errors='replace').splitlines() if log.exists() else []
                print(mode + ': ' + (lines[-1][:200] if lines else 'starting'), flush=True)
    plain = json.loads((work / 'plain/outputs.json').read_text())
    observed = json.loads((work / 'observed/outputs.json').read_text())
    if plain != observed:
        raise ValueError('Observer changed production outputs')
    evidence = json.loads((work / 'observed/evidence.json').read_text())
    refs = [r['/Job/DisplayReference'] for r in records]
    memberships = {}
    for scope, jobs in plain.items():
        family, region = scope.split(':', 1)
        for job in jobs:
            memberships.setdefault((family, str(job['job_id'])), set()).add(region)
    decisions = []
    counts = {}
    for family in FAMILIES:
        for ref in refs:
            record = evidence[family].get(ref, {'decision': 'unknown', 'reason': 'No complete production decision evidence captured', 'gate': 'unknown'})
            regions = sorted(memberships.get((family, ref), set()))
            if record['decision'] == 'include' and not regions:
                record = {'decision': 'exclude', 'reason': 'Selected candidate withheld by final production output gate', 'gate': 'final output gate after selected report'}
            decisions.append({'ref': ref, 'scope': 'production:' + family, **record, 'regions': regions})
        counts[family] = dict(Counter(r['decision'] for r in decisions if r['scope'] == 'production:' + family))
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    report = {'archiveSha256': source['archiveSha256'], 'archiveDate': source['feedDate'],
              'sourceMetadata': source['metadata'], 'sourceRequestSha256': source['requestSha256'],
              'receipt': receipt, 'cleanRecords': len(records), 'rulesRevision': revision,
              'exactFileOutputParity': True, 'outputsSha256': digest(plain), 'scopes': len(plain), 'outcomes': counts,
              'selectedByScope': {scope: len(jobs) for scope, jobs in plain.items()},
              'selectedUniqueJobs': len({str(job['job_id']) for jobs in plain.values() for job in jobs}),
              'unknowns': sum(r['decision'] == 'unknown' for r in decisions),
              'boundary': 'JobG8 family generation only; external composition, enrichment, final publisher/city derivation and email sending were not invoked.'}
    manifest = finish_capture(capture, ROOT, archive_sha256=PIN,
        workbook_sha256=hashlib.sha256((work / 'clean.xlsx').read_bytes()).hexdigest(),
        workbook_created=stamp.isoformat() if stamp else None, families=FAMILIES,
        observer_modules=MODULES, outputs_sha256=report['outputsSha256'], output_scopes=plain)
    report['dependencyManifest'] = manifest
    report['dependencyManifestSha256'] = digest(manifest)
    report['compactContext'] = manifest['context']
    (work / 'dependency-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (work / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    # No duplicate descriptions: only compact decisions and selected display rows.
    with gzip.open(work / 'selection.json.gz', 'wt') as handle:
        json.dump({'report': report, 'decisions': decisions, 'sourceHashes': [[r['/Job/DisplayReference'], digest(r)] for r in records]}, handle, ensure_ascii=False)
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
