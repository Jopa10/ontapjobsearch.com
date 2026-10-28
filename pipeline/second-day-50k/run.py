import subprocess, sys, json, time, os, hashlib, zipfile, base64, lzma, shutil
from pathlib import Path
ROOT=Path.cwd(); OUT=ROOT/'test-results'; OUT.mkdir(exist_ok=True)
state={'source_sha':'ec47ea496fcb896d8c50ad349f05c5cec6816d24','feed_date':'2026-10-28','production_changed':False,'steps':[]}
def save(): (OUT/'receipt.json').write_text(json.dumps(state,indent=2))
def run(name,args,pipeline=False):
 state['active']=name; save(); print('START '+name,flush=True); start=time.monotonic()
 with (OUT/(name+'.log')).open('w') as log:
  p=subprocess.run(args,cwd=ROOT/'pipeline' if pipeline else ROOT,stdout=log,stderr=subprocess.STDOUT)
 state['steps'].append({'name':name,'exit':p.returncode,'seconds':round(time.monotonic()-start,2)});save()
 if p.returncode: print((OUT/(name+'.log')).read_text()[-10000:],flush=True);raise SystemExit(p.returncode)
def py(name,args,pipeline=False):run(name,[sys.executable,'-u',*args],pipeline)
fixture=ROOT/'pipeline/second-day-50k'; info=json.loads((fixture/'feed-info.json').read_text())
raw=lzma.decompress(base64.b64decode(''.join(p.read_text() for p in sorted((fixture/'feed').glob('part-*')))))
assert hashlib.sha256(raw).hexdigest()==info['xml_sha256'];assert info['date_time'][:3]==[2026,10,28]
with zipfile.ZipFile(OUT/'verified.zip','w',zipfile.ZIP_DEFLATED) as z:
 item=zipfile.ZipInfo('Jobs.xml',tuple(info['date_time']));item.compress_type=zipfile.ZIP_DEFLATED;z.writestr(item,raw)
state['feed']=info;save();del raw
shutil.rmtree(fixture/'feed')
shutil.copytree(ROOT/'pipeline/output-admin-service',OUT/'approved-admin',dirs_exist_ok=True)
py('01-adapt',['pipeline/scripts/jobg8_xml_adapter.py','--zip',str(OUT/'verified.zip'),'--output','pipeline/input/jobg8.xlsx','--expected-min','5000','--expected-max','50000'])
py('02-health',['pipeline/scripts/validate_jobg8_feed_health.py','--input','pipeline/input/jobg8.xlsx'])
py('03-first-select',['-m','scripts.service_admin_pipeline_north_yorkshire'],True)
py('04-first-support',['-m','scripts.support_worker_pipeline_live_config'],True)
py('05-master',['-m','review_hub.master_review','build'],True)
py('06-decisions',['-m','review_hub.master_review','apply','--write','--require-complete','--unresolved-policy','withhold','--plan',str(OUT/'reviewed-plan.json')],True)
py('07-reviewed-select',['-m','scripts.service_admin_pipeline_north_yorkshire'],True)
for i,mod in enumerate(['external_sources.compose_northeast_admin','external_sources.compose_west_yorkshire_admin','external_sources.compose_teaching_vacancies_regional']):py('08-external-'+str(i),['-m',mod,'--write'],True)
py('09-nhs',['-m','external_sources.compose_nhs_admin_daily','--write','--fallback-output-dir',str(OUT/'approved-admin')],True)
py('10-admin-enrich',['-m','scripts.enrich_job_metadata','--category','admin-service'],True)
py('11-support',['-m','scripts.support_worker_pipeline_live_config'],True)
py('12-support-enrich',['-m','scripts.enrich_job_metadata','--category','support-worker'],True)
py('13-exclusions',['-m','scripts.persistent_jobg8_review','--refresh-exclusion-report'],True)
py('14-compose',['-m','scripts.publish_verified_pages_north_yorkshire','--write'],True)
py('15-cities',['-m','scripts.derive_city_pages','--publish'],True)
py('16-city-maintain',['-m','scripts.maintain_active_city_pages'],True)
py('17-accountant',['pipeline/scripts/enforce_jobg8_accountant_exclusion.py','--app-dir','app'])
run('18-search',['node','--import','tsx','scripts/generate-search-index.ts'])
sys.path.insert(0,str(ROOT/'pipeline'))
from scripts.enrich_job_metadata import read_feed,metadata_by_job_id
conflicts=set();metadata_by_job_id(read_feed(ROOT/'pipeline/input/jobg8.xlsx'),conflicted_job_ids=conflicts)
jobs=json.loads((ROOT/'generated/published-jobs.json').read_text());ids={str(j['job_id']) for j in jobs}
assert not ids & conflicts,'Conflicting IDs published'
from collections import Counter
import csv, xml.etree.ElementTree as ET
received=Counter(); categories={}
with zipfile.ZipFile(OUT/'verified.zip').open('Jobs.xml') as handle:
 for _,job in ET.iterparse(handle,events=['end']):
  if job.tag=='Job':
   category=job.findtext('Classification','(blank)');received[category]+=1;categories[job.findtext('DisplayReference')]=category;job.clear()
assert sum(received.values())==50000
published={str(j['job_id']) for j in jobs if j['source']=='JobG8'}
assert not published-categories.keys()
classified=Counter(categories[j] for j in published)
state['canonical_jobs']=len(jobs);state['sources']=dict(Counter(j['source'] for j in jobs));state['conflicts_withheld']=sorted(conflicts);save()
py('19-profile',['pipeline/scripts/build_jobg8_category_profile.py','--input','pipeline/input/jobg8.xlsx','--coverage','pipeline/reports-daily/daily-family-coverage.csv','--published-output-dir','pipeline/output-admin-service','--published-output-dir','pipeline/output-support-worker','--output','pipeline/reports-daily/jobg8-feed-category-profile.csv'])
with (ROOT/'pipeline/reports-daily/jobg8-feed-category-profile.csv').open('w',newline='') as handle:
 writer=csv.writer(handle);writer.writerow(['feed_date','total_jobs','published_jobg8_jobs','jobg8_category','count','published_count'])
 for category,count in received.most_common():writer.writerow(['2026-10-28',50000,len(published),category,count,classified[category]])
from scripts import build_verified_region_overview as verified,build_daily_region_overview as overview,live_job_source_counter as counter
snapshot=verified.published_inventory(ROOT/'app')
counter.collect_live_jobs=lambda *_a,**_k:(snapshot.jobs,snapshot.job_json_files,snapshot.duplicate_rows_ignored)
counter.build_reports(ROOT/'app',ROOT/'pipeline/reports-daily','2026-10-28')
overview._git_show_report_ref=lambda p:(ROOT/p).read_text()
overview._report_tree_names=lambda p:sorted(str(f.relative_to(ROOT)) for f in (ROOT/p).rglob('*') if f.is_file())
overview._upsert_jobg8_history=lambda _p:None
overview.OUTPUT=OUT/'daily-region-overview-50k-2026-10-28.md'
verified.main()
overview.OUTPUT.write_text(overview.OUTPUT.read_text().replace('# Ontap daily regional overview','# Ontap daily regional overview — 50k TEST, 28 October 2026\n\nIsolated test inventory. Production unchanged. Historical columns are production history.',1))
py('20-workbook',['pipeline/scripts/export_daily_region_overview_xlsx.py','--markdown',str(overview.OUTPUT),'--output',str(OUT/'daily-region-overview-50k-2026-10-28.xlsx')])
shutil.move(str(ROOT/'pipeline/input/jobg8.xlsx'),str(OUT/'fresh-jobg8.xlsx'))
os.environ['DATABASE_URL']='postgresql://build:build@127.0.0.1:5432/build'
run('21-build',['npm','run','build'])
run('22-package',['tar','-czf',str(OUT/'preview-snapshot.tar.gz'),'app','generated','pipeline/output-admin-service','pipeline/output-support-worker','pipeline/reviews','pipeline/reports-daily'])
state['active']=None;state['processing_build_complete']=True;state['limits']=['No deployment or HTTP preview verification','No AWS archive upload','External data may be retained from approved source snapshot'];save()
print(json.dumps(state),flush=True)
