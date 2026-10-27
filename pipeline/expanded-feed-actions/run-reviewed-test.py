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
# Recreate the editable projection from the same captured-feed compact review,
# then use the normal master-review fanout. No selection decisions are invented.
import csv
sys.path.insert(0, str(ROOT/'pipeline'))
from scripts import service_admin_pipeline_live_config as configured
source_md = ROOT/'pipeline/reviews/jobg8/service-admin-review.md'
source_csv = ROOT/'pipeline/reviews/jobg8/service-admin-review.csv'
projection = list(csv.DictReader(source_csv.open(encoding='utf-8-sig')))
assert {row['feed_date'] for row in projection} == {'2026-10-27'}
for row in projection:
 row['selection_status'] = 'POSSIBLE_SELECTION' if row['decision'].startswith('POSS - ') else row['decision']
 row['selector_outcome'] = 'DAILY_REVIEW' if row['selection_status'] == 'POSSIBLE_SELECTION' else ''
configured.core.CURRENT_FEED_DATE = '2026-10-27'
actions = configured.core._markdown_review_action_by_job_id(source_md.read_text())
import tempfile
original = source_md.read_text()
existing_ids = {block.get('job_id') for block in configured.core._parse_markdown_review_blocks(original)}
missing_rows = [row for row in projection if row['job_id'] not in existing_ids and row['selection_status'] in {'SELECTED', 'POSSIBLE_SELECTION'}]
with tempfile.TemporaryDirectory() as folder:
 restored = Path(folder)/'review.md'
 configured.write_manual_review_markdown(restored, missing_rows, actions)
 blocks = re.findall(r'(?ms)^---[ \t]*\n.*?^---[ \t]*$', restored.read_text())
 supplement = '\n## Restored current-feed review entries\n\n' + '\n\n'.join(blocks) + '\n\n'
 source_md.write_text(original.replace('## ACTIVE MANUAL ACTIONS\n', supplement+'## ACTIVE MANUAL ACTIONS\n', 1))
print('Restored missing editable review blocks:', len(missing_rows), flush=True)
py('26b-reviewed-decision-fanout', ['-m','review_hub.master_review','apply','--require-complete','--write','--unresolved-policy','withhold','--plan',str(OUT/'reviewed-plan.json')], True)
plan = json.loads((OUT/'reviewed-plan.json').read_text())
state['unapplied_decisions'] = plan.get('unapplied_jobs', [])
save()
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
shutil.move(str(ROOT/'pipeline/input/jobg8.xlsx'), str(OUT/'reviewed-jobg8.xlsx'))
env = os.environ.copy()
env['DATABASE_URL'] = 'postgresql://build:build@127.0.0.1:5432/build'
run('41-reviewed-production-build', ['npm','run','build'], env=env)
state['active'] = None
state['clean_output_build_passed'] = True
state['local_complete'] = bool(state['saved_selection_published'])
save()
assert state['saved_selection_published'], 'Clean output built, but approved Commercial Administrator did not reach publication; see receipt'
print('REVIEWED PUBLICATION AND BUILD PASS', flush=True)
