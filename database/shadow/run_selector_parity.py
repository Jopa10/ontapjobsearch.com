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
from selector_capture import Capture

PIN = '046881410cda7588c5589af808449b6e3f41c8b889955de8b57c23be426ab5bd'
FAMILIES = ['admin_service', 'support_worker', 'customer_sales', 'finance_accounts',
            'hr_recruitment', 'marketing', 'legal_assistant_paralegal', 'customer_service_contact_centre']


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def child(work, observe):
    sys.stdout.reconfigure(line_buffering=True)
    os.chdir(work / 'pipeline')
    sys.path.insert(0, str(work / 'pipeline'))
    from scripts import service_admin_pipeline_north_yorkshire as admin
    from scripts import support_worker_pipeline_live_config as support
    from scripts.slice_registry import live_slices
    from scripts.slice_catalog import category_meta, output_filename
    observer = Capture(work / 'pipeline/scripts')
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
    args = p.parse_args()
    work = args.work.resolve()
    if args.child:
        child(work, args.child == 'observed')
        return
    archive = args.archive.resolve()
    if hashlib.sha256(archive.read_bytes()).hexdigest() != PIN:
        raise ValueError('Pinned source mismatch')
    records, receipt = load_archive(archive)
    if len(records) != 43796 or receipt['conflictingIdsHeld'] != ['1401786160']:
        raise ValueError('Pinned receipt mismatch')
    if work.exists():
        raise ValueError('Use a new scratch work directory')
    work.mkdir(parents=True)
    # Use the actual production XML adapter and its source timestamp. Remove only
    # the already quarantined conflicting ID; preserve supplier order for dedupe.
    sys.path.insert(0, str(ROOT))
    from pipeline.scripts.jobg8_xml_adapter import convert, _stamp_workbook_core_timestamp
    import openpyxl
    converted = work / 'jobg8.xlsx'
    convert(archive, converted, 43798, 43798)
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
    report = {'archiveSha256': PIN, 'receipt': receipt, 'cleanRecords': len(records), 'rulesRevision': revision,
              'exactFileOutputParity': True, 'outputsSha256': digest(plain), 'scopes': len(plain), 'outcomes': counts,
              'selectedByScope': {scope: len(jobs) for scope, jobs in plain.items()},
              'selectedUniqueJobs': len({str(job['job_id']) for jobs in plain.values() for job in jobs}),
              'unknowns': sum(r['decision'] == 'unknown' for r in decisions),
              'boundary': 'JobG8 family generation only; external composition, enrichment, final publisher/city derivation and email sending were not invoked.'}
    (work / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    # No duplicate descriptions: only compact decisions and selected display rows.
    with gzip.open(work / 'selection.json.gz', 'wt') as handle:
        json.dump({'report': report, 'decisions': decisions, 'sourceHashes': [[r['/Job/DisplayReference'], digest(r)] for r in records]}, handle, ensure_ascii=False)
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
