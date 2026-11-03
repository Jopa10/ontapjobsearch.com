"""Capture replay inputs; historical Git inventory is never runtime attestation."""
import argparse
import fnmatch
import hashlib
import importlib.metadata
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import tarfile
from datetime import datetime, timezone

IGNORED = ('input', 'input-jobg8-archive', 'output-*', 'reports-*', '__pycache__')
ENTRYPOINTS = ('run_selector_parity.py', 'selector_capture.py', 'prepare_raw_stage.py',
               'dependency_provenance.py')
ENVIRONMENT = ('ONTAP_FEED_DATE', 'TZ', 'LANG', 'LC_ALL', 'PYTHONHASHSEED')


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def retained(path):
    p = Path(path)
    return (p.parts[0] == 'pipeline' and not any(
        fnmatch.fnmatchcase(part, pattern) for part in p.parts[1:] for pattern in IGNORED)
        or str(p) in {'database/shadow/' + name for name in ENTRYPOINTS})


def snapshot(root):
    root = Path(root)
    files = {}
    candidates = list((root / 'pipeline').rglob('*'))
    candidates += [root / 'database/shadow' / name for name in ENTRYPOINTS]
    for path in sorted(candidates):
        name = path.relative_to(root).as_posix()
        if not retained(name):
            continue
        if path.is_symlink():
            raise ValueError('Symlink dependency cannot be certified: ' + name)
        if path.is_file():
            files[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    if not any(x.startswith('pipeline/scripts/') for x in files):
        raise ValueError('Missing selector source')
    return files


def revision_inventory(root, revision):
    revision = subprocess.check_output(['git', 'rev-parse', '--verify', revision+'^{commit}'],
                                       cwd=root, text=True).strip()
    proc = subprocess.Popen(['git', 'archive', revision, 'pipeline', 'database/shadow'],
                            cwd=root, stdout=subprocess.PIPE)
    files = {}
    try:
        with tarfile.open(fileobj=proc.stdout, mode='r|') as archive:
            for entry in archive:
                if not retained(entry.name):
                    continue
                if entry.issym() or entry.islnk():
                    raise ValueError('Symlink dependency cannot be certified: ' + entry.name)
                if entry.isfile():
                    files[entry.name] = hashlib.sha256(archive.extractfile(entry).read()).hexdigest()
    finally:
        proc.stdout.close()
        if proc.wait() != 0:
            raise ValueError('Git inventory failed')
    return {'version': 1, 'kind': 'reconstructed-commit-inventory', 'revision': revision,
            'files': dict(sorted(files.items())), 'sourceSha256': digest(files),
            'runtimeCaptured': False, 'usableAsExecutionContext': False,
            'limitation': 'Committed candidate inputs only. Historical sparse checkout, untracked files, environment, package versions and execution time were not captured; no historical runtime attestation.'}


def start_capture(root):
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    files = snapshot(root)
    committed = revision_inventory(root, revision)['files']
    if any(committed.get(name) != checksum for name, checksum in files.items()):
        raise ValueError('Uncommitted or changed replay dependency; save code before execution')
    packages = {name: importlib.metadata.version(name) for name in ('pandas', 'openpyxl')}
    return {'version': 1, 'kind': 'captured-replay-inputs', 'revision': revision,
            'files': files, 'sourceSha256': digest(files),
            'startedAt': datetime.now(timezone.utc).isoformat(),
            'runtime': {'python': platform.python_version(), 'platform': platform.platform(),
                        'packages': packages,
                        'environment': {k: os.environ.get(k) for k in ENVIRONMENT}}}


def verify_copy(capture, target):
    # Child copies only pipeline; observer/adapter run from the captured source.
    expected = {k: v for k, v in capture['files'].items() if k.startswith('pipeline/')}
    actual = {k: v for k, v in snapshot(target).items() if k.startswith('pipeline/')}
    if actual != expected:
        raise ValueError('Scratch replay dependencies differ from captured source')


def finish_capture(capture, root, *, archive_sha256, workbook_sha256, workbook_created,
                   families, observer_modules, outputs_sha256, output_scopes):
    if snapshot(root) != capture['files']:
        raise ValueError('Source dependencies changed during replay')
    files = capture['files']
    registry = {k: v for k, v in files.items() if k.startswith(('pipeline/registers/', 'pipeline/reviews/'))}
    geography = {k: v for k, v in files.items() if k.startswith(('pipeline/geo/', 'pipeline/lookup/'))}
    if not registry or not geography:
        raise ValueError('Missing register/geography inputs')
    scope = {'families': families, 'observerModules': observer_modules,
             'outputScopes': sorted(output_scopes)}
    ended = datetime.now(timezone.utc).isoformat()
    context = {'selectorRevision': capture['revision'], 'registersSha256': digest(registry),
               'geographySha256': digest(geography),
               # Conservative: covers ALL retained source files, including other
               # configuration/reviews/manifests, plus actual package/env values.
               'configurationSha256': digest({'files': files, 'runtime': capture['runtime']}),
               'scopeRegistrySha256': digest(scope),
               'timeContext': json.dumps({'workbookCreated': workbook_created,
                   'feedDateOverride': capture['runtime']['environment']['ONTAP_FEED_DATE'],
                   'startedAt': capture['startedAt'], 'finishedAt': ended}, separators=(',', ':'))}
    return {**capture, 'finishedAt': ended, 'archiveSha256': archive_sha256,
            'cleanWorkbookSha256': workbook_sha256, 'workbookCreated': workbook_created,
            'scope': scope, 'outputsSha256': outputs_sha256, 'context': context,
            'runtimeCaptured': True, 'sourceUnchanged': True,
            'boundary': 'Actual replay source/input/runtime evidence; no selector skipping, database import, or production action.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--revision', required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    root = Path(__file__).resolve().parents[2]
    manifest = revision_inventory(root, args.revision)
    args.output.write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({k: v for k, v in manifest.items() if k != 'files'}))


if __name__ == '__main__':
    main()
