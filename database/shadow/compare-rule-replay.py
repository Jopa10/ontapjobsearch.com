"""Compare full-feed rule replays; all source order and non-rule files are identical."""
import csv,json
from pathlib import Path
from collections import Counter
root=Path('replay-results')
def output(version):
    files={p.name:json.loads(p.read_text(encoding='utf-8-sig')) for p in (root/('rule-replay-'+version)/'output-admin-service').glob('*.json')}
    assert files
    return files
before,after=output('before'),output('after')
assert before.keys()==after.keys()
reference={p.name:json.loads(p.read_text(encoding='utf-8-sig')) for p in Path('production-reference').rglob('*.json')}
def ids(rows):return [str(x['job_id']) for x in rows if x.get('source')=='JobG8']
parity=[name for name,rows in after.items() if name not in reference or ids(rows)!=ids(reference[name])]
assert not parity,('Revised selector differs from Tuesday production',parity)
def audit(version):
    paths=list((root/('rule-replay-'+version)/'reports-daily').glob('*decision*.csv'))
    assert len(paths)==1,paths
    rows=list(csv.DictReader(paths[0].open(encoding='utf-8-sig')))
    result={}
    for r in rows:
        key=(r['job_id'],r['excel_row'])
        assert key not in result,key
        result[key]=r
    return result
b,a=audit('before'),audit('after')
assert b.keys()==a.keys(),'Raw-feed audit membership changed'
fields=['decision','selector_outcome','selection_status','salary_review_status','qualification_status','context_status']
changes=[]
for key in b:
    old,new=b[key],a[key]
    changed=[f for f in fields if old[f]!=new[f]]
    if not changed:continue
    salary=old['salary_review_status']!=new['salary_review_status'] or ('salary' in new['reason'].lower() and old['reason']!=new['reason'])
    qualification=old['qualification_status']!=new['qualification_status'] or any(w in (old['reason']+' '+new['reason']).lower() for w in ['qualification','accountant'])
    changes.append({'jobId':key[0],'feedExcelRow':key[1],'title':new['title'],'region':new['region'],
        'changedFields':changed,'salaryRuleEvidence':salary,'qualificationRuleEvidence':qualification,
        'before':{f:old[f] for f in fields+['reason','qualification_reason','salary_text','annual_salary_upper','regional_salary_review_point']},
        'after':{f:new[f] for f in fields+['reason','qualification_reason','salary_text','annual_salary_upper','regional_salary_review_point']}})
direct_regions={x['region'] for x in changes if x['salaryRuleEvidence'] or x['qualificationRuleEvidence']}
unexplained=[x['jobId'] for x in changes if not (x['salaryRuleEvidence'] or x['qualificationRuleEvidence']) and x['region'] not in direct_regions]
all_before={j for rows in before.values() for j in ids(rows)}
all_after={j for rows in after.values() for j in ids(rows)}
scope_changes=[{'scopeFile':n,'before':len(ids(before[n])),'after':len(ids(after[n])),
    'addedIds':sorted(set(ids(after[n]))-set(ids(before[n]))),
    'removedIds':sorted(set(ids(before[n]))-set(ids(after[n]))),
    'commonOrderPreserved':[x for x in ids(before[n]) if x in set(ids(after[n]))]==[x for x in ids(after[n]) if x in set(ids(before[n]))]}
    for n in before if ids(before[n])!=ids(after[n])]
report={'status':'passed' if not unexplained else 'needs_investigation','feedDate':'2026-11-17','archiveSha256':'8638a31e4baca46665fed119fc2ddb227e48959a5da3b055189ae41d6ed55486',
    'beforeRulesCommit':'eac8997cc3a48cc1ce3cbee16c77faffc3e4ec8f','productionSourceCommit':'6e001e11000854fd211f984c7d4db9f8b40e51e1',
    'sourceFilesChanged':['pipeline/scripts/pipeline_refinement.py','pipeline/scripts/service_admin_pipeline_core.py'],
    'auditRows':len(a),'beforeOutcomeCounts':dict(Counter(r['decision'] for r in b.values())),
    'afterOutcomeCounts':dict(Counter(r['decision'] for r in a.values())),
    'changedAuditRows':len(changes),'changedJobIds':sorted({x['jobId'] for x in changes}),
    'unchangedAuditRows':len(a)-len(changes),'unexplainedChangedIds':unexplained,
    'beforeUniquePublishedAdminIds':len(all_before),'afterUniquePublishedAdminIds':len(all_after),
    'addedPublishedIds':sorted(all_after-all_before),'removedPublishedIds':sorted(all_before-all_after),
    'revisedScopesMatchedTuesdayProduction':len(after),'revisedScopeDifferencesFromProduction':parity,
    'changedScopes':scope_changes,'productionChanged':False,'neonReadbackTested':False}
Path('rule-change-report.json').write_text(json.dumps(report,indent=2)+'\n')
Path('rule-change-jobs.json').write_text(json.dumps(changes,indent=2)+'\n')
print('ONTAP_RULE_REPLAY '+json.dumps({k:v for k,v in report.items() if k not in ['changedScopes','changedJobIds']}))
assert not unexplained,unexplained
