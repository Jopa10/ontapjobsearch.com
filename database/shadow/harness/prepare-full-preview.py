"""Build-only publisher/city preparation. Never invokes workflows or external feeds."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'pipeline'))
from scripts import publish_verified_pages_live_config as configured
from scripts.derive_city_pages import load_register,process_config
from scripts.maintain_active_city_pages import active_entries,maintain_active_config
outputs=json.loads((ROOT/'shadow-db-outputs.json').read_text())
# Remove committed job inventories from this isolated build, preserving config arrays.
cleared=[]
for p in (ROOT/'app').rglob('*.json'):
 try: rows=json.loads(p.read_text())
 except (ValueError,UnicodeDecodeError): continue
 if isinstance(rows,list) and any(isinstance(r,dict) and r.get('job_id') and r.get('apply_url') for r in rows):
  p.write_text('[]\n');cleared.append(str(p.relative_to(ROOT)))
core=configured.core
pairs={(s.split(':',1)[1],s.split(':',1)[0]) for s in outputs}
results=[];destinations=set()
for m in core.MAPPINGS:
 scope=m.category+':'+m.region
 if scope not in outputs:continue
 source=ROOT/m.source;source.parent.mkdir(parents=True,exist_ok=True);source.write_text(json.dumps(outputs[scope]))
 dest=ROOT/m.destination;dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():dest.write_text('[]')
 result=core.publish_one(m,write=True,active_slices=pairs,root=ROOT,publication_date='2026-11-02',shared_dates={})
 assert result['status'] in ('published','unchanged'),result
 destinations.add(scope);results.append(result)
 if len(results)%20==0: print('ONTAP_REGIONAL_PROGRESS '+str(len(results))+'/'+str(len(outputs)),flush=True)
assert destinations==set(outputs),(len(destinations),len(outputs))
# Exactly the same city functions and pinned approvals used in the publisher.
configs=load_register(ROOT/'pipeline/city_pages/city-page-register.json')
print('ONTAP_CITY_DERIVATION_START',flush=True)
city_results=[process_config(c,ROOT,write_review=True,write_live=True) for c in configs]
active=[maintain_active_config(c,ROOT) for c in active_entries(ROOT/'pipeline/city_pages/city-page-register.json')]
report={'snapshotDate':'2026-11-02','regionalOutputs':len(results),'activeCities':active,'cityResults':city_results,'clearedInventoryFiles':len(cleared),'scope':'Pinned JobG8 snapshot only; external source composition and ongoing ingestion not exercised'}
(ROOT/'public/shadow-verification').mkdir(parents=True,exist_ok=True)
(ROOT/'public/shadow-verification/city-report.json').write_text(json.dumps(report,indent=2))
print('ONTAP_CITY_REPORT '+json.dumps({'regionalOutputs':len(results),'activeCityPages':len(active),'activeCityJobs':sum(c['jobs'] for c in active)}))
