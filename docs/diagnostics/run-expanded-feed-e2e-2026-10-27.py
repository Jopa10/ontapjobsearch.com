import subprocess,sys,json,time,os,hashlib,zipfile,xml.etree.ElementTree as ET,shutil
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE/'e2e-50000'; OUT=BASE/'e2e-results';OUT.mkdir(exist_ok=True)
receipt=OUT/'receipt.json'
state=json.loads(receipt.read_text()) if receipt.exists() else {'commit':'2c61c1b137adeb1ad3047b213c837e08e16feef1','steps':[],'production_changed':False}
def save():receipt.write_text(json.dumps(state,indent=2))
def run(name,args,cwd=ROOT,expected=0,env=None):
 if any(s['name']==name and s['status']=='PASS' for s in state['steps']):return
 state['active']=name;save();t=time.monotonic()
 with (OUT/(name+'.log')).open('w') as f:
  p=subprocess.run(args,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,env=env)
 s={'name':name,'exit':p.returncode,'expected':expected,'seconds':round(time.monotonic()-t,2),'status':'PASS' if p.returncode==expected else 'FAIL'}
 state['steps'].append(s);save();print(json.dumps(s),flush=True)
 if s['status']=='FAIL':raise SystemExit(1)
def py(name,args,pipeline=False):run(name,[sys.executable,'-u',*args],ROOT/'pipeline' if pipeline else ROOT)
zip_path=BASE/'verified.zip';state['feed_sha256']=hashlib.sha256(zip_path.read_bytes()).hexdigest();save()
py('01-import-50000',['pipeline/scripts/jobg8_xml_adapter.py','--zip',str(zip_path),'--output','pipeline/input/jobg8.xlsx','--expected-min','5000','--expected-max','50000'])
py('02-health',['pipeline/scripts/validate_jobg8_feed_health.py','--input','pipeline/input/jobg8.xlsx'])
run('03-old-guard-rejects-50000',[sys.executable,'pipeline/scripts/jobg8_xml_adapter.py','--zip',str(zip_path),'--output',str(OUT/'must-not-exist.xlsx'),'--expected-max','20000'],expected=1)
assert not (OUT/'must-not-exist.xlsx').exists()
if not (OUT/'rollback-20000.zip').exists():
 with zipfile.ZipFile(zip_path) as z:
  info=z.getinfo('Jobs.xml');root=ET.fromstring(z.read('Jobs.xml'))
 for j in list(root)[20000:]:root.remove(j)
 with zipfile.ZipFile(OUT/'rollback-20000.zip','w',zipfile.ZIP_DEFLATED) as z:
  i=zipfile.ZipInfo('Jobs.xml',info.date_time);i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,ET.tostring(root))
py('04-old-guard-accepts-20000',['pipeline/scripts/jobg8_xml_adapter.py','--zip',str(OUT/'rollback-20000.zip'),'--output',str(OUT/'rollback-20000.xlsx'),'--expected-max','20000'])
py('05-old-feed-health',['pipeline/scripts/validate_jobg8_feed_health.py','--input',str(OUT/'rollback-20000.xlsx')])
py('06-duplicate-report',['pipeline/scripts/report_jobg8_potential_duplicates.py','--input','pipeline/input/jobg8.xlsx','--output',str(OUT/'potential-duplicates.csv')])
shutil.copytree(ROOT/'pipeline/output-admin-service',OUT/'approved-admin',dirs_exist_ok=True)
py('07-all-live-families',['-m','scripts.service_admin_pipeline_north_yorkshire'],True)
for i,mod in enumerate(['external_sources.compose_northeast_admin','external_sources.compose_west_yorkshire_admin','external_sources.compose_teaching_vacancies_regional']):py('08-external-'+str(i),['-m',mod,'--write'],True)
py('09-nhs-retention',['-m','external_sources.compose_nhs_admin_daily','--write','--fallback-output-dir',str(OUT/'approved-admin')],True)
py('10-enrich-admin',['-m','scripts.enrich_job_metadata','--category','admin-service'],True)
py('11-support-worker',['-m','scripts.support_worker_pipeline_live_config'],True)
py('12-enrich-support',['-m','scripts.enrich_job_metadata','--category','support-worker'],True)
py('13-family-coverage',['-m','scripts.assess_daily_family_coverage'],True)
py('14-refresh-exclusions',['-m','scripts.persistent_jobg8_review','--refresh-exclusion-report'],True)
py('15-master-review',['-m','review_hub.master_review','build'],True)
py('16-withhold-plan',['-m','review_hub.master_review','apply','--require-complete','--write','--unresolved-policy','withhold','--plan',str(OUT/'withhold-plan.json')],True)
py('17-compose-pages',['-m','scripts.publish_verified_pages_north_yorkshire','--write'],True)
py('18-accountant-guard',['pipeline/scripts/enforce_jobg8_accountant_exclusion.py','--app-dir','app'])
py('19-city-derive',['-m','scripts.derive_city_pages','--publish'],True)
py('20-city-maintain',['-m','scripts.maintain_active_city_pages'],True)
py('21-final-accountant-guard',['pipeline/scripts/enforce_jobg8_accountant_exclusion.py','--app-dir','app'])
py('22-inventory',['pipeline/scripts/live_job_source_counter.py','--app-dir','app','--reports-dir',str(OUT/'inventory')])
run('23-search',['node','--import','tsx','scripts/generate-search-index.ts'])
plan=json.loads((OUT/'withhold-plan.json').read_text());jobs=json.loads((ROOT/'generated/published-jobs.json').read_text());ids={j['job_id'] for j in jobs}
withheld={str(j['source_job_id']) for j in plan.get('withheld_jobs',[]) if j.get('source')=='JobG8' or j.get('source_key')=='jobg8'}
state['withheld_in_generated']=sorted(ids&withheld);state['canonical_jobs']=len(jobs);save();assert not (ids&withheld)
for f in (ROOT/'pipeline/input').glob('*jobg8*xlsx*'):shutil.move(str(f),str(OUT/f.name))
run('24-prisma',['node','node_modules/prisma/build/index.js','generate'])
env=os.environ.copy();env['DATABASE_URL']='postgresql://build:build@127.0.0.1:5432/build';env['NEXT_TURBOPACK_EXPERIMENTAL_USE_SYSTEM_TLS_CERTS']='1'
run('25-production-build',['node','node_modules/next/dist/bin/next','build'],env=env)
state['active']=None;state['local_complete']=True;save();print('LOCAL END-TO-END COMPLETE',flush=True)
