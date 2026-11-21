import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import pg from 'pg';
import {canonicalSelection,encodeHistory,decodeHistory,FAMILIES} from './selection-history.mjs';
import {encodeAppearances,decodeAppearances} from './appearance-manifest.mjs';
import {reconstruct,encodeCompactDisplay,decodeCompactDisplay} from './display-snapshot.mjs';
import {contentHash} from './importer.mjs';
import {measureCompactAllocation} from './compact-allocation.mjs';
const PIN='046881410cda7588c5589af808449b6e3f41c8b889955de8b57c23be426ab5bd';
async function main(){
 assert.equal(process.env.VERCEL_ENV,'preview');
 assert.equal(process.env.ONTAP_SHADOW_NEON_PROJECT_ID,'noisy-fire-97386602');
 const u=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
 assert.ok(u.hostname.endsWith('.neon.tech'));
 assert.ok(['require','verify-full'].includes(u.searchParams.get('sslmode')));u.searchParams.set('sslmode','verify-full');
 const saved=JSON.parse(await fs.readFile('selection-receipt.json','utf8'));
 const historic=JSON.parse(await fs.readFile('historical-source.json','utf8'));
 assert.equal(saved.archiveSha256,PIN);assert.equal(historic.revision,saved.rulesRevision);
 assert.equal(contentHash(historic.files),historic.sourceSha256);
 const reportKeys=['archiveSha256','receipt','cleanRecords','rulesRevision','exactFileOutputParity','outputsSha256','scopes','outcomes','selectedByScope','selectedUniqueJobs','unknowns','boundary'];
 const report=Object.fromEntries(reportKeys.map(k=>[k,saved[k]]));
 const c=new pg.Client({connectionString:u.toString(),connectionTimeoutMillis:15000,query_timeout:120000,statement_timeout:90000,application_name:'ontap-shadow-compact-allocation-probe'});
 let fixture,outputs,runId;
 try{
  await c.connect();await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
  try{
   const run=(await c.query(`SELECT r.id,r.supplier_id,r.diagnostics FROM ontap_shadow.feed_runs r JOIN ontap_shadow.suppliers s ON s.id=r.supplier_id WHERE s.code='jobg8' AND r.feed_key=$1 AND r.status='accepted'`,['raw-stage:'+PIN+':100'])).rows[0];
   assert.ok(run);runId=run.id;
   assert.equal(run.diagnostics.selection_parity.checksum,saved.database.checksum);
   assert.equal(run.diagnostics.display_snapshot.outputs_sha256,report.outputsSha256);
   const sources=(await c.query('SELECT supplier_job_id AS ref,content_hash FROM ontap_shadow.supplier_adverts WHERE supplier_id=$1',[run.supplier_id])).rows;
   assert.equal(sources.length,43796);
   const sha=x=>createHash('sha256').update(x).digest('hex');
   sources.sort((a,b)=>sha(a.ref).localeCompare(sha(b.ref)));
   const order=new Map(sources.map((r,i)=>[r.ref,i]));
   const decisions=(await c.query(`SELECT a.supplier_job_id AS ref,d.scope,d.decision,d.reason,d.evidence->>'gate' AS gate,d.evidence->'regions' AS regions FROM ontap_shadow.selection_decisions d JOIN ontap_shadow.supplier_adverts a ON a.id=d.advert_id WHERE d.feed_run_id=$1 AND d.scope LIKE 'production:%'`,[run.id])).rows;
   decisions.sort((a,b)=>FAMILIES.indexOf(a.scope.slice(11))-FAMILIES.indexOf(b.scope.slice(11))||order.get(a.ref)-order.get(b.ref));
   fixture={report,decisions,sourceHashes:sources.map(r=>[r.ref,r.content_hash])};
   assert.equal(contentHash(fixture),saved.database.checksum,'Saved DB evidence differs from original selector fixture');
   const display=(await c.query(`SELECT d.scope,d.evidence->'displayRows' AS "displayRows" FROM ontap_shadow.selection_decisions d WHERE d.feed_run_id=$1 AND d.scope LIKE 'production:%' AND d.decision='include'`,[run.id])).rows;
   outputs=reconstruct(display,Object.keys(report.selectedByScope));
   assert.equal(contentHash(outputs),report.outputsSha256);assert.equal(Object.keys(outputs).length,239);
   await c.query('COMMIT');
  }catch(e){await c.query('ROLLBACK');throw e;}
  console.log('ONTAP_COMPACT_ALLOCATION_SOURCE '+JSON.stringify({runId,adverts:fixture.sourceHashes.length,decisions:fixture.decisions.length,scopes:Object.keys(outputs).length,exactFixtureChecksum:true}));
  // These hashes describe reconstructed committed candidates, NOT historical
  // execution attestation. This run only calibrates storage of saved evidence.
  const group=prefixes=>Object.fromEntries(Object.entries(historic.files).filter(([k])=>prefixes.some(p=>k.startsWith(p))));
  const context={selectorRevision:report.rulesRevision,registersSha256:contentHash(group(['pipeline/registers/','pipeline/reviews/'])),geographySha256:contentHash(group(['pipeline/geo/','pipeline/lookup/'])),configurationSha256:historic.sourceSha256,scopeRegistrySha256:contentHash({families:FAMILIES,scopes:Object.keys(outputs).sort()}),timeContext:'Allocation-only reconstructed source inventory; historical runtime unknown'};
  const baseline=encodeHistory(fixture,context);
  const appearances=encodeAppearances(fixture.sourceHashes.map(x=>x[0]));
  assert.deepEqual(decodeAppearances(appearances),fixture.sourceHashes.map(x=>x[0]).sort());
  const baseDisplay=encodeCompactDisplay(outputs,baseline.state);
  assert.deepEqual(decodeCompactDisplay(baseDisplay,baseline.state),outputs);
  const nextContext={...context,timeContext:'Allocation-only synthetic unchanged subsequent snapshot; not a fresh feed'};
  const delta=encodeHistory(fixture,nextContext,baseline);
  assert.equal(delta.envelope.changedDecisions,0);assert.equal(delta.envelope.changedSourceHashes,0);
  assert.deepEqual(decodeHistory(delta.envelope,baseline.state),canonicalSelection(fixture,nextContext));
  const nextDisplay={...baseDisplay,selectionStateSha256:contentHash(delta.state)};
  assert.deepEqual(decodeCompactDisplay(nextDisplay,delta.state),outputs);
  const record=(selection,display)=>({probeOnly:true,selection_representation:'compact_v1',selection_status:'verified',compact_selection:{parentRunId:selection.envelope.kind==='delta'?runId:null,envelope:selection.envelope},compact_appearances:appearances,compact_display:display});
  const records=[record(baseline,baseDisplay),...Array.from({length:6},()=>record(delta,nextDisplay))];
  const allocation=await measureCompactAllocation(c,records);
  const result={status:'passed',measuredAt:new Date().toISOString(),maximumDatabaseBytes:838860800,fixtureArchiveSha256:PIN,outputsSha256:report.outputsSha256,sourceRunId:runId,adverts:43796,decisions:350368,scopes:239,selectionBaselineEncodedBytes:baseline.encodedBytes,unchangedDeltaEncodedBytes:delta.encodedBytes,displayEncodedBytes:Buffer.byteLength(JSON.stringify(baseDisplay)),appearanceEncodedBytes:Buffer.byteLength(JSON.stringify(appearances)),allocation,
   reconstructionOnlyHistoricalProvenance:true,syntheticSubsequentDays:true,scenario:'One real saved-snapshot compact payload plus six copies of a synthetic unchanged-day payload. Seven-display allocation calibration, not seven actual feed days.',freshFeedImported:false,existingRecordsChanged:false,cleanupExecuted:false,productionChanged:false,ninetyDayFreeViabilityProven:false};
  await fs.mkdir('compact-allocation-dist',{recursive:true});await fs.writeFile('compact-allocation-dist/report.json',JSON.stringify(result,null,2)+'\n');
  await fs.writeFile('compact-allocation-dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><title>Ontap compact allocation calibration</title><p>Probe completed and rolled back. Existing records unchanged.</p>');
  console.log('ONTAP_COMPACT_ALLOCATION_REPORT '+JSON.stringify(result));
 }finally{await c.end();}
}
main().catch(e=>{console.error('ONTAP_COMPACT_ALLOCATION_FAILED',e.code||String(e.message).split('\n')[0].slice(0,220));process.exitCode=1;});
