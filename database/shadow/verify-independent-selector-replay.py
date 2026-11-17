#!/usr/bin/env python3
"""Independent, isolated selector replay vs completed production outputs.

The reference is used ONLY for validation, never as input to selectors.
All reads/writes are on the GitHub runner checkout. No live publication.
"""
import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--production-output',required=True,type=Path)
p.add_argument('--selector-root',required=True,type=Path,help='Exact production repository checkout used for replay')
p.add_argument('--report',required=True,type=Path)
a=p.parse_args()
root=a.selector_root.resolve()
sys.path.insert(0,str(root/'pipeline'))
from scripts import publish_verified_pages_live_config as configured
production=a.production_output
mappings=configured.core.MAPPINGS
details=[]
reference_ids=set()
produced_ids=set()
extra=0
for m in mappings:
    src=root/Path(m.source)
    ref=production/src.name
    if not ref.is_file() or not src.is_file():
        raise SystemExit(f'Missing independently generated or reference scope: {src.name}')
    actual=json.loads(src.read_text(encoding='utf-8-sig'))
    expected=json.loads(ref.read_text(encoding='utf-8-sig'))
    if not isinstance(actual,list) or not isinstance(expected,list):
        raise SystemExit(f'Invalid output: {src.name}')
    actual_j=[r for r in actual if r.get('source')=='JobG8']
    expected_j=[r for r in expected if r.get('source')=='JobG8']
    actual_ids=[str(r['job_id']) for r in actual_j]
    expected_ids=[str(r['job_id']) for r in expected_j]
    produced_ids.update(actual_ids)
    reference_ids.update(expected_ids)
    if actual_ids!=expected_ids:
        details.append({
           'scope':m.category+':'+m.region,'file':src.name,
           'expected':len(expected_ids),'actual':len(actual_ids),
           'missing':sorted(set(expected_ids)-set(actual_ids))[:12],
           'extra':sorted(set(actual_ids)-set(expected_ids))[:12],
           'sameMembers':set(expected_ids)==set(actual_ids)
        })
unmapped=sorted({p.name for p in production.glob('*.json')}-{m.source.name for m in mappings})
report={'status':'passed' if not details and produced_ids==reference_ids else 'difference',
        'test':'isolated Python selectors against archived same-day raw feed',
        'scopeCount':len(mappings),'scopesWithDifferences':len(details),
        'uniqueReferenceJobG8Ids':len(reference_ids),'uniqueGeneratedJobG8Ids':len(produced_ids),
        'missingGlobalIds':sorted(reference_ids-produced_ids)[:50],
        'extraGlobalIds':sorted(produced_ids-reference_ids)[:50],
        'differentScopes':details[:70],
        'additionalReferenceArtifacts':unmapped,
        'productionChanged':False,'referenceUsedForSelection':False,
        'neonWriteTested':False}
a.report.parent.mkdir(parents=True,exist_ok=True)
a.report.write_text(json.dumps(report,indent=2)+'\n')
print('ONTAP_INDEPENDENT_SELECTOR_REPLAY '+json.dumps({k:v for k,v in report.items() if k not in ('differentScopes','additionalReferenceArtifacts')}))
if details:
    print('First differing scopes: '+json.dumps(details[:5]))
if not produced_ids:raise SystemExit('STOP: replay generated no JobG8 jobs')
