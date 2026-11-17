"""Build-only publisher/city preparation. Never invokes workflows or external feeds."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'pipeline'))
from scripts import publish_verified_pages_live_config as configured
from scripts.derive_city_pages import load_register,process_config
from scripts.maintain_active_city_pages import active_entries,maintain_active_config
outputs=json.loads((ROOT/'shadow-db-outputs.json').read_text())
meta_path=ROOT/'shadow-preview-metadata.json'
snapshot_date=json.loads(meta_path.read_text())['date'] if meta_path.exists() else '2026-11-02'
# Remove committed job inventories from this isolated build, preserving config arrays.
cleared=[]
reference_inventories={}
for p in (ROOT/'app').rglob('*.json'):
 try: rows=json.loads(p.read_text())
 except (ValueError,UnicodeDecodeError): continue
 if isinstance(rows,list) and any(isinstance(r,dict) and r.get('job_id') and r.get('apply_url') for r in rows):
  reference_inventories[str(p.relative_to(ROOT))]=rows
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
 result=core.publish_one(m,write=True,active_slices=pairs,root=ROOT,publication_date=snapshot_date,shared_dates={})
 assert result['status'] in ('published','unchanged'),result
 destinations.add(scope);results.append(result)
 if len(results)%20==0: print('ONTAP_REGIONAL_PROGRESS '+str(len(results))+'/'+str(len(outputs)),flush=True)
assert destinations==set(outputs),(len(destinations),len(outputs))
# Exactly the same city functions and pinned approvals used in the publisher.
configs=load_register(ROOT/'pipeline/city_pages/city-page-register.json')
print('ONTAP_CITY_DERIVATION_START',flush=True)
city_results=[process_config(c,ROOT,write_review=True,write_live=True) for c in configs]
active=[maintain_active_config(c,ROOT) for c in active_entries(ROOT/'pipeline/city_pages/city-page-register.json')]
# Compare actual generated inventories with the pinned production checkout.
differences=[];source_totals={};checked=0
for filename,expected in reference_inventories.items():
 path=ROOT/filename
 actual=json.loads(path.read_text()) if path.exists() else []
 def key(r):return (str(r.get('job_id','')),str(r.get('source','')),str(r.get('apply_url','')))
 e,a=[key(r) for r in expected],[key(r) for r in actual]
 checked+=1
 for r in actual:
  src=str(r.get('source','unknown'));source_totals[src]=source_totals.get(src,0)+1
 if e!=a:
  es,ass=set(e),set(a)
  differences.append({'path':filename,'productionCount':len(e),'previewCount':len(a),
   'missingIds':[v[0] for v in e if v not in ass],
   'extraIds':[v[0] for v in a if v not in es],
   'sameMembers':es==ass,'sameOrder':e==a})
report={'snapshotDate':snapshot_date,'regionalOutputs':len(results),'activeCities':active,'cityResults':city_results,'clearedInventoryFiles':len(cleared),
 'scope':'Tuesday Neon-backed publisher snapshot with existing approved external inputs',
 'productionInventoryFilesCompared':checked,'inventoryDifferences':differences,'sourceOccurrencesInComparedFiles':source_totals,
 'exactPublishedInventoryMembershipAndOrder':not differences}
(ROOT/'public/shadow-verification').mkdir(parents=True,exist_ok=True)
(ROOT/'public/shadow-verification/city-report.json').write_text(json.dumps(report,indent=2))
print('ONTAP_CITY_REPORT '+json.dumps({'regionalOutputs':len(results),'activeCityPages':len(active),'activeCityJobs':sum(c['jobs'] for c in active)}))

print('ONTAP_WEBSITE_INVENTORY_COMPARISON '+json.dumps({'files':checked,'differentFiles':len(differences),'differences':differences[:20],'sourceOccurrences':source_totals}),flush=True)
