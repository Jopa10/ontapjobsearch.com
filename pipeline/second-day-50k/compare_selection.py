"""Compare the changed selector with the preserved same-input successful day-three run."""
from pathlib import Path
import csv,json,tarfile,hashlib
from collections import Counter
ROOT=Path.cwd();OUT=ROOT/'test-results';BASE=ROOT/'.selection-baseline'
# download-artifact preserves the test-results path in the saved archive.
def baseline_file(name):
 matches=list(BASE.rglob(name));assert len(matches)==1,(name,matches);return matches[0]
def write_csv(name,rows,fields):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
old_receipt=json.loads(baseline_file('receipt.json').read_text());new_receipt=json.loads((OUT/'receipt.json').read_text())
assert old_receipt['feed']['xml_sha256']==new_receipt['feed']['xml_sha256'],'Comparison requires the exact same captured XML'
with tarfile.open(baseline_file('preview-snapshot.tar.gz')) as tar:
 before=json.load(tar.extractfile('generated/published-jobs.json'))
 before_report=list(csv.DictReader(__import__('io').TextIOWrapper(tar.extractfile('pipeline/reports-daily/decision-report-admin-service.csv'),encoding='utf-8-sig')))
after=json.loads((ROOT/'generated/published-jobs.json').read_text())
with (ROOT/'pipeline/reports-daily/decision-report-admin-service.csv').open(encoding='utf-8-sig') as f:after_report=list(csv.DictReader(f))
key=lambda r:(r['source'],str(r['job_id']))
b={key(r):r for r in before};a={key(r):r for r in after}
br={str(r['job_id']):r for r in before_report};ar={str(r['job_id']):r for r in after_report}
changes=[]
for k in sorted(set(a)^set(b)):
 j=a.get(k,b.get(k));old=br.get(k[1],{});new=ar.get(k[1],{})
 changes.append(dict(change='added' if k in a else 'removed',source=k[0],job_id=k[1],title=j['title'],location=j['location'],region=j['region'],salary_text=j.get('salary_text',''),old_reason=old.get('reason',''),new_reason=new.get('reason',''),selector_outcome=new.get('selector_outcome','')))
fields=['change','source','job_id','title','location','region','salary_text','old_reason','new_reason','selector_outcome']
write_csv('selection-inventory-changes.csv',changes,fields)
selector_changes=[]
for jid in sorted(set(br)|set(ar)):
 x=br.get(jid,{});y=ar.get(jid,{})
 if (x.get('selector_outcome'),x.get('region'),x.get('salary_text'))!=(y.get('selector_outcome'),y.get('region'),y.get('salary_text')):
  selector_changes.append(dict(job_id=jid,title=y.get('title',x.get('title')),town=y.get('town',x.get('town')),old_outcome=x.get('selector_outcome'),new_outcome=y.get('selector_outcome'),old_region=x.get('region'),new_region=y.get('region'),old_reason=x.get('reason'),new_reason=y.get('reason'),old_salary=x.get('salary_text'),new_salary=y.get('salary_text')))
write_csv('selection-selector-changes.csv',selector_changes,['job_id','title','town','old_outcome','new_outcome','old_region','new_region','old_reason','new_reason','old_salary','new_salary'])
summary={'baseline_run':40848659957,'feed_xml_sha256':new_receipt['feed']['xml_sha256'],'before':dict(Counter(j['source'] for j in before)),'after':dict(Counter(j['source'] for j in after)),'published_changes':dict(Counter((r['change']+' '+r['source']) for r in changes)),'before_selector_outcomes':dict(Counter(r['selector_outcome'] for r in before_report)),'after_selector_outcomes':dict(Counter(r['selector_outcome'] for r in after_report)),'selector_changed_rows':len(selector_changes),'conflict_ids_equal':set(old_receipt['conflicts_withheld'])==set(new_receipt['conflicts_withheld']),'production_changed':False}
assert summary['conflict_ids_equal'],'Quarantine set changed unexpectedly'
(OUT/'selection-comparison.json').write_text(json.dumps(summary,indent=2))
(OUT/'selection-comparison.md').write_text('# Service Admin selector comparison — isolated test only\n\n'+json.dumps(summary,indent=2)+'\n\nJob-level inventory and selector change CSVs are attached. Added jobs require inspection before release approval. No production merge, feed switch, deployment or email is performed.\n')
print(json.dumps(summary,indent=2))
