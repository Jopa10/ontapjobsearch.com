import {test} from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs/promises';
import {PGlite} from '@electric-sql/pglite';
import {verifyCompactIntegration} from './compact-integration.mjs';
import {contentHash,stableId} from './importer.mjs';
import {FAMILIES} from './selection-history.mjs';
import {readCompactDisplay} from './display-snapshot.mjs';
const schema=await fs.readFile(new URL('../001_initial.sql',import.meta.url),'utf8');
function packet(day,ids,title='Admin'){
 const records=ids.map(ref=>({'/Job/DisplayReference':ref,'/Job/Position':title,'/Job/ApplicationURL':'https://example.org/'+ref}));
 const outputs={'admin_service:Test':records.map(r=>({job_id:r['/Job/DisplayReference'],title:r['/Job/Position'],apply_url:r['/Job/ApplicationURL']}))};
 const sha=contentHash({day,records}),revision='a'.repeat(40);
 const files={'pipeline/scripts/selector.py':'b'.repeat(64),'pipeline/registers/r.csv':'c'.repeat(64),'pipeline/geo/g.csv':'d'.repeat(64)};
 const m={version:1,kind:'captured-replay-inputs',revision,files,sourceSha256:contentHash(files),archiveSha256:sha,outputsSha256:contentHash(outputs),cleanWorkbookSha256:'e'.repeat(64),scope:{families:FAMILIES,observerModules:{},outputScopes:Object.keys(outputs)},runtime:{environment:{ONTAP_FEED_DATE:day},packages:{test:'synthetic-local-fixture'}},workbookCreated:day+'T07:30:00',startedAt:day+'T08:00:00Z',finishedAt:day+'T08:01:00Z',runtimeCaptured:true,sourceUnchanged:true};
 m.context={selectorRevision:revision,registersSha256:contentHash({'pipeline/registers/r.csv':files['pipeline/registers/r.csv']}),geographySha256:contentHash({'pipeline/geo/g.csv':files['pipeline/geo/g.csv']}),configurationSha256:contentHash({files,runtime:m.runtime}),scopeRegistrySha256:contentHash(m.scope),timeContext:JSON.stringify({workbookCreated:m.workbookCreated,feedDateOverride:day,startedAt:m.startedAt,finishedAt:m.finishedAt})};
 const report={cleanRecords:records.length,exactFileOutputParity:true,unknowns:0,rulesRevision:revision,archiveSha256:sha,outputsSha256:contentHash(outputs),selectedByScope:{'admin_service:Test':records.length},dependencyManifest:m,dependencyManifestSha256:contentHash(m),compactContext:m.context};
 const selection={report,sourceHashes:records.map(r=>[r['/Job/DisplayReference'],contentHash(r)]),decisions:FAMILIES.flatMap((family,i)=>ids.map(ref=>({ref,scope:'production:'+family,decision:i?'exclude':'include',reason:'Synthetic observed fixture',gate:'Test only',regions:i?[]:['Test']})))};
 return {raw:{records,observedOn:day,percentage:100,archiveSha256:sha,sourceRevision:revision,totalReceived:records.length,eligibleRecords:records.length,rawPayloadBytes:Buffer.byteLength(JSON.stringify(records))},selection,outputs};
}
test('complete compact path: update, absence/return, stable IDs and exact replay',async()=>{
 const db=new PGlite();try{await db.exec(schema);let parent=null;const seen=[];
 for(const [day,ids,title] of [['2026-11-02',['1','2'],'Admin'],['2026-11-03',['1'],'Office Assistant'],['2026-11-04',['1','2'],'Reception']]){
  const input=packet(day,ids,title);const r=await verifyCompactIntegration(db,input,{parentRunId:parent});seen.push(r);parent=r.runId;
  assert.equal(r.completeReplayVerified,true);assert.equal(r.expiryEnabled,false);
  assert.equal(r.counts.selection_decisions,0);assert.equal(r.counts.advert_appearances,0);
  if(day==='2026-11-03'){
   const absent=(await db.query("SELECT last_seen::text,availability FROM ontap_shadow.supplier_adverts WHERE supplier_job_id='2'")).rows[0];
   assert.equal(absent.last_seen,'2026-11-02');assert.equal(absent.availability,'seen');
  }
 }
 const returned=(await db.query("SELECT job_id,title FROM ontap_shadow.supplier_adverts WHERE supplier_job_id='2'")).rows[0];
 assert.equal(returned.job_id,stableId('job:jobg8:2'));assert.equal(returned.title,'Reception');
 assert.equal(seen.at(-1).counts.jobs,2);
 assert.equal((await readCompactDisplay(db,seen[0].runId))['admin_service:Test'][0].title,'Admin');
 }finally{await db.close();}
});
test('mismatched provenance and raw/display inputs are rejected before DB access',async()=>{
 let calls=0;const client={query(){calls++;throw Error('Unexpected database access');}};
 const bad=packet('2026-11-02',['1']);bad.selection.report.compactContext={...bad.selection.report.compactContext,geographySha256:'0'.repeat(64)};
 await assert.rejects(verifyCompactIntegration(client,bad));
 const changed=packet('2026-11-02',['1']);changed.raw.records[0]['/Job/Position']='Changed after selection';
 await assert.rejects(verifyCompactIntegration(client,changed),/Raw hash/);
 assert.equal(calls,0);
});
test('failed display phase resumes from committed raw/selection without duplicate jobs',async()=>{
 const db=new PGlite();try{await db.exec(schema);const phases=[],input=packet('2026-11-02',['1']);
 const broken={query(q,p){if(q.includes("'{compact_display}'"))throw Error('Injected display failure');return db.query(q,p);}};
 await assert.rejects(verifyCompactIntegration(broken,input,{onCheckpoint:async r=>phases.push(r.phase)}),/Injected/);
 assert.deepEqual(phases,['raw-accepted','selection-verified']);
 const r=await verifyCompactIntegration(db,input);assert.equal(r.importReplayed,true);assert.equal(r.selectionReplayed,true);assert.equal(r.counts.jobs,1);
 }finally{await db.close();}
});
