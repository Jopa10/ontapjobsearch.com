import subprocess, sys, json, time, os, hashlib, zipfile, shutil, re
from pathlib import Path
ROOT = Path.cwd()
OUT = ROOT / 'test-results'
OUT.mkdir(exist_ok=True)
BASE = ROOT
zip_path = OUT / 'verified.zip'
state = {'steps': [], 'production_changed': False, 'local_complete': False}
receipt = OUT / 'receipt.json'
def save(): receipt.write_text(json.dumps(state, indent=2))
def run(name, args, cwd=ROOT, expected=0, env=None):
 state['active'] = name; save(); start = time.monotonic()
 print('START ' + name, flush=True)
 with (OUT / (name + '.log')).open('w') as log:
  result = subprocess.run(args, cwd=cwd, stdout=log, stderr=subprocess.STDOUT, env=env)
 step = {'name': name, 'exit': result.returncode, 'expected': expected, 'seconds': round(time.monotonic()-start, 2), 'status': 'PASS' if result.returncode == expected else 'FAIL'}
 state['steps'].append(step); save(); print(json.dumps(step), flush=True)
 if step['status'] == 'FAIL':
  print((OUT / (name + '.log')).read_text()[-12000:], flush=True)
  raise SystemExit(1)
def py(name, args, pipeline=False): run(name, [sys.executable, '-u', *args], ROOT/'pipeline' if pipeline else ROOT)
shutil.copytree(ROOT/'pipeline/output-admin-service', OUT/'approved-admin', dirs_exist_ok=True)
py('26-reviewed-feed-restore',['pipeline/scripts/jobg8_xml_adapter.py','--zip',str(zip_path),'--output','pipeline/input/jobg8.xlsx','--expected-min','5000','--expected-max','50000'])
py('27-reviewed-all-families',['-m','scripts.service_admin_pipeline_north_yorkshire'],True)
for i,mod in enumerate(['external_sources.compose_northeast_admin','external_sources.compose_west_yorkshire_admin','external_sources.compose_teaching_vacancies_regional']):py('28-reviewed-external-'+str(i),['-m',mod,'--write'],True)
py('29-reviewed-nhs',['-m','external_sources.compose_nhs_admin_daily','--write','--fallback-output-dir',str(OUT/'approved-admin')],True)
py('30-reviewed-enrich-admin',['-m','scripts.enrich_job_metadata','--category','admin-service'],True)
py('31-reviewed-support',['-m','scripts.support_worker_pipeline_live_config'],True)
py('32-reviewed-enrich-support',['-m','scripts.enrich_job_metadata','--category','support-worker'],True)
py('33-reviewed-profile',['pipeline/scripts/build_jobg8_category_profile.py','--input','pipeline/input/jobg8.xlsx','--coverage','pipeline/reports-daily/daily-family-coverage.csv','--published-output-dir','pipeline/output-admin-service','--published-output-dir','pipeline/output-support-worker','--output','pipeline/reports-daily/jobg8-feed-category-profile.csv'])
py('34-reviewed-exclusions',['-m','scripts.persistent_jobg8_review','--refresh-exclusion-report'],True)
py('35-reviewed-compose',['-m','scripts.publish_verified_pages_north_yorkshire','--write'],True)
py('36-reviewed-city-derive',['-m','scripts.derive_city_pages','--publish'],True)
py('37-reviewed-city-maintain',['-m','scripts.maintain_active_city_pages'],True)
py('38-reviewed-accountant-guard',['pipeline/scripts/enforce_jobg8_accountant_exclusion.py','--app-dir','app'])
py('39-reviewed-ledger',['-m','scripts.published_job_daily_ledger','--app-dir',str(ROOT/'app'),'--reports-dir',str(ROOT/'pipeline/reports-daily')],True)
run('40-reviewed-search',['node','--import','tsx','scripts/generate-search-index.ts'])
jobs = json.loads((ROOT/'generated/published-jobs.json').read_text())
ids = {str(job['job_id']) for job in jobs}
aliases = json.loads((ROOT/'generated/published-job-canonical-ids.json').read_text())
approved_id = '23643_225646128'
state['saved_selection_published'] = approved_id in ids or aliases.get(approved_id) in ids
state['canonical_jobs'] = len(jobs)
conflicts = set(json.loads((ROOT/'pipeline/expanded-feed-actions/metadata-conflicts.json').read_text())['conflicts'])
state['conflicting_ids_published'] = sorted(ids & conflicts)
sys.path.insert(0, str(ROOT/'pipeline'))
from scripts.slice_registry import live_slices
from scripts.slice_catalog import output_source_path
groups = {}
master = (ROOT/'pipeline/reviews/daily/ontap-daily-review.md').read_text()
for block in re.split(r'(?m)^---\s*$', master):
 def value(key):
  match = re.search(r'(?m)^'+key+r':[ \t]*(.*)$', block)
  return match.group(1).strip() if match else ''
 if value('source_key') == 'jobg8' and value('action').lower() not in {'select','sel','exclude','exc'}:
  groups.setdefault(value('category'), set()).add(value('source_job_id'))
leaks = []
for region, category in live_slices():
 source = ROOT/output_source_path(region, category)
 if not source.exists(): continue
 rows = json.loads(source.read_text())
 if isinstance(rows, dict): rows = rows.get('jobs', [])
 for row in rows:
  job_id = str(row.get('job_id', row.get('id', '')))
  if job_id in groups.get(category, set()): leaks.append({'file':str(source.relative_to(ROOT)), 'job_id':job_id})
state['same_family_withholding_leaks'] = leaks
save()
assert not state['conflicting_ids_published'], 'Conflicting metadata IDs reached published output'
assert not leaks, 'Unanswered jobs reached their withheld family'
assert state['saved_selection_published'], 'Existing approved Commercial Administrator did not reach reviewed publication'
shutil.move(str(ROOT/'pipeline/input/jobg8.xlsx'), str(OUT/'reviewed-jobg8.xlsx'))
env = os.environ.copy()
env['DATABASE_URL'] = 'postgresql://build:build@127.0.0.1:5432/build'
run('41-reviewed-production-build', ['npm','run','build'], env=env)
state['active'] = None
state['local_complete'] = True
save()
print('REVIEWED PUBLICATION AND BUILD PASS', flush=True)
