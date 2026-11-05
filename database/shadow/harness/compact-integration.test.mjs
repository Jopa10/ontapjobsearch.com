import {test} from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs/promises';
import {PGlite} from '@electric-sql/pglite';
import {verifyCompactIntegration} from './compact-integration.mjs';
import {contentHash,stableId} from './importer.mjs';
import {FAMILIES} from './selection-history.mjs';
import {readCompactDisplay} from './display-snapshot.mjs';
import {classifyFullyExcludedRefs,readExcludePayloadBreakdown} from './exclude-retention.mjs';
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
function excludedPacket(day,ids){
 const input=packet(day,ids);input.outputs={};
 input.selection.decisions=input.selection.decisions.map(x=>({...x,decision:'exclude',regions:[]}));
 const report=input.selection.report,m=report.dependencyManifest,hash=contentHash(input.outputs);
 report.outputsSha256=hash;report.selectedByScope={};m.outputsSha256=hash;m.scope.outputScopes=[];
 const context={...report.compactContext,scopeRegistrySha256:contentHash(m.scope)};
 m.context=context;report.compactContext=context;report.dependencyManifestSha256=contentHash(m);
 return input;
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
test('fully excluded payload stays reviewable for three days, then purges while decisions and identity remain',async()=>{
 const db=new PGlite();try{await db.exec(schema);let first=excludedPacket('2026-11-02',['1']);
 const refs=classifyFullyExcludedRefs(first.selection);assert.deepEqual(refs,['1']);
 const day1=await verifyCompactIntegration(db,first,{excludeReviewAsOfDate:'2026-11-04'});
 const before=(await db.query("SELECT raw_payload IS NOT NULL AS retained,exclude_review_started_on::text FROM ontap_shadow.supplier_adverts WHERE supplier_job_id='1'")).rows[0];
 assert.equal(before.retained,true);assert.equal(before.exclude_review_started_on,'2026-11-02');
 const second=excludedPacket('2026-11-03',['1']);
 const day2=await verifyCompactIntegration(db,second,{parentRunId:day1.runId,excludeReviewAsOfDate:'2026-11-05'});
 assert.equal(day2.excludeRetention.purgedCount,1);
 const after=(await db.query("SELECT raw_payload,content_purged_at IS NOT NULL AS purged,exclude_review_started_on::text FROM ontap_shadow.supplier_adverts WHERE supplier_job_id='1'")).rows[0];
 assert.equal(after.raw_payload,null);assert.equal(after.purged,true);assert.equal(after.exclude_review_started_on,'2026-11-02');
 assert.equal((await db.query("SELECT count(*)::int AS n FROM ontap_shadow.jobs WHERE public_id='1'")).rows[0].n,1);
 assert.equal((await db.query('SELECT count(*)::int AS n FROM ontap_shadow.feed_runs WHERE id=$1',[day2.runId])).rows[0].n,1);
 const saved=await db.query("SELECT diagnostics->'compact_selection'->'envelope' IS NOT NULL AS retained FROM ontap_shadow.feed_runs WHERE id=$1",[day2.runId]);
 assert.equal(saved.rows[0].retained,true);
 const changed=excludedPacket('2026-11-06',['1']);changed.raw.records[0]['/Job/Position']='Changed excluded title';
 changed.raw.rawPayloadBytes=Buffer.byteLength(JSON.stringify(changed.raw.records));
 changed.selection.sourceHashes=[["1",contentHash(changed.raw.records[0])]];
 changed.selection.report.archiveSha256=changed.raw.archiveSha256=contentHash({day:'2026-11-06',records:changed.raw.records});
 changed.selection.report.dependencyManifest.archiveSha256=changed.selection.report.archiveSha256;
 changed.selection.report.dependencyManifestSha256=contentHash(changed.selection.report.dependencyManifest);
 const manifest=changed.selection.report.dependencyManifest;manifest.archiveSha256=changed.raw.archiveSha256;
 changed.selection.report.dependencyManifestSha256=contentHash(manifest);
 const day3=await verifyCompactIntegration(db,changed,{parentRunId:day2.runId,excludeReviewAsOfDate:'2026-11-08'});
 assert.equal(day3.excludeRetention.purgedCount,0);
 const renewed=(await db.query("SELECT raw_payload IS NOT NULL AS retained,exclude_review_started_on::text FROM ontap_shadow.supplier_adverts WHERE supplier_job_id='1'")).rows[0];
 assert.equal(renewed.retained,true);assert.equal(renewed.exclude_review_started_on,'2026-11-06');
 }finally{await db.close();}
});
test('read-only baseline separates fully excluded payloads from other advert payloads',async()=>{
 const db=new PGlite();try{await db.exec(schema);
 const supplier=(await db.query("INSERT INTO ontap_shadow.suppliers(code,name) VALUES('jobg8','JobG8') RETURNING id")).rows[0].id;
 const runId=stableId('baseline-run');
 await db.query(`INSERT INTO ontap_shadow.feed_runs(id,supplier_id,feed_key,feed_date,source_checksum,status,completed_at,received_count,diagnostics)
  VALUES($1,$2,'baseline','2026-11-03',$3,'accepted',now(),3,'{"selection_parity":{}}')`,[runId,supplier,'a'.repeat(64)]);
 const families=['admin_service','support_worker','customer_sales','finance_accounts','hr_recruitment','marketing','legal_assistant_paralegal','customer_service_contact_centre'];
 for(let i=1;i<=3;i++){
  const ref=String(i),jobId=stableId('baseline-job:'+ref),advertId=stableId('baseline-advert:'+ref);
  await db.query(`INSERT INTO ontap_shadow.jobs(id,public_id,title,first_seen,last_seen,publication_status) VALUES($1,$2,'Admin','2026-11-03','2026-11-03','withheld')`,[jobId,ref]);
  await db.query(`INSERT INTO ontap_shadow.supplier_adverts(id,supplier_id,supplier_job_id,job_id,title,apply_url,raw_payload,content_hash,first_seen,last_seen)
    VALUES($1,$2,$3,$4,'Admin',$5,$6,$7,'2026-11-03','2026-11-03')`,[advertId,supplier,ref,jobId,'https://example.org/'+ref,JSON.stringify({description:'x'.repeat(i*100)}),contentHash({ref,i})]);
  for(let j=0;j<(i===3?4:families.length);j++)await db.query(`INSERT INTO ontap_shadow.selection_decisions(id,advert_id,feed_run_id,scope,decision,reason,rules_revision)
    VALUES($1,$2,$3,$4,$5,'test','${'b'.repeat(40)}')`,[stableId(`baseline:${ref}:${families[j]}`),advertId,runId,'production:'+families[j],(i===1||j<7)?'exclude':'review']);
 }
 const result=await readExcludePayloadBreakdown(db);
 assert.equal(result.selector_feed_date,'2026-11-03');assert.equal(result.fully_excluded_payload_rows,'1');assert.ok(Number(result.fully_excluded_payload_bytes)>0);
 assert.equal(result.other_decided_payload_rows,'1');assert.equal(result.without_complete_selector_payload_rows,'1');
 }finally{await db.close();}
});
