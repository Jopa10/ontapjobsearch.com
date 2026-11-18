import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import pg from 'pg';
import {requirePreview,hash,MAX,RESERVE} from './publisher-safeguards.mjs';
import {readCurrentPublication} from './current-publication.mjs';
import {readMasterAppearance,upsertSelectedMaster} from './daily-master-snapshot.mjs';
import {runMasterCleanup} from './master-cleanup.mjs';

requirePreview(process.env);
const request=JSON.parse(await fs.readFile('daily-refresh-request.json','utf8'));
assert.equal(request.mode,'today','Refresh request must remain in today mode');
assert.ok(Number.isInteger(request.attempt)&&request.attempt>0);
assert.equal(Object.keys(request).some(k=>/date|run.?id|artifact.?id|commit/i.test(k)),false,'Do not pin date or production identifiers in request');
const reset=JSON.parse(await fs.readFile('daily-reset-request.json','utf8'));
assert.notEqual(reset.enabled,true,'Neon reset is forbidden for this refresh');
const source=JSON.parse(await fs.readFile('daily-source.json','utf8'));
assert.equal(source.mode,'daily_latest');assert.equal(source.dateProvidedByRequest,false);
assert.ok(source.archiveOrigin,'Saved feed archive origin is missing');
const raw=await fs.readFile('selected-review-payloads.json');
assert.equal(hash(raw),source.payloadPackageSha256);
const snapshot=JSON.parse(raw);
assert.equal(snapshot.schemaVersion,2);assert.equal(snapshot.selectedPayloadRecords,snapshot.records.length);
assert.equal(snapshot.feedDate,source.archiveDate);assert.equal(snapshot.archiveSha256,source.archiveSha256);
assert.equal(snapshot.productionAppCommit,source.productionAppCommitSha);
assert.equal(snapshot.productionWorkflowRunId,source.productionOutputRunId);
const scopes=JSON.parse(await fs.readFile('daily-scopes.json','utf8'));
const canon=v=>Array.isArray(v)?v.map(canon):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canon(v[k])])):v;
const fingerprint=v=>hash(JSON.stringify(canon(v)));
const expectedProvenance={archiveKey:snapshot.archiveKey,archiveSha256:snapshot.archiveSha256,productionWorkflowRunId:snapshot.productionWorkflowRunId,productionRunCommit:snapshot.productionRunCommit,productionAppCommit:snapshot.productionAppCommit};
const seen=new Set(),positions=new Set();
for(const row of snapshot.records){
 assert.ok(row.public_id&&!seen.has(row.public_id));seen.add(row.public_id);
 assert.equal(row.decision,'SELECTED');
 assert.ok(Number.isInteger(row.source_row_position)&&row.source_row_position>0&&!positions.has(row.source_row_position));
 positions.add(row.source_row_position);
 assert.equal(fingerprint(row.raw_payload),row.payload_sha256,'Source payload hash mismatch '+row.public_id);
}
assert.equal(snapshot.selectedIds,seen.size);
assert.equal(scopes.length,256,'Unexpected current publication scope count');
assert.deepEqual([...new Set(scopes.flatMap(s=>s.jobg8Ids))].sort(),[...seen].sort(),'Scope IDs differ from selected source');
for(const s of scopes)assert.equal(new Set(s.jobg8Ids).size,s.jobg8Ids.length,'Duplicate ID in scope '+s.scope);

const url=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);url.searchParams.set('sslmode','verify-full');
const c=new pg.Client({connectionString:url.toString(),connectionTimeoutMillis:15000,query_timeout:120000,application_name:'ontap-preview-daily-master-refresh'});
const table='ontap_shadow.selected_review_payload_records';
const legacyRows=async()=> (await c.query('SELECT public_id,decision,raw_payload,payload_sha256,source_row_position FROM '+table+' WHERE feed_date=$1::date ORDER BY public_id',[snapshot.feedDate])).rows;
const verifyMaster=async()=>{
 const rows=await readMasterAppearance(c,snapshot.feedDate);
 assert.equal(rows.length,snapshot.records.length,'Master appearance count differs from selected source');
 const byId=new Map(rows.map(r=>[r.public_id,r]));
 assert.equal(byId.size,rows.length,'Duplicate selected appearance IDs');
 for(const expected of snapshot.records){
  const actual=byId.get(expected.public_id);assert.ok(actual,'Missing selected master appearance '+expected.public_id);
  assert.equal(actual.decision,'SELECTED');
  assert.equal(actual.payload_sha256,expected.payload_sha256,'Appearance hash differs '+expected.public_id);
  assert.deepEqual(canon(actual.raw_payload),canon(expected.raw_payload),'Master full payload differs '+expected.public_id);
  assert.equal(actual.source_row_position,expected.source_row_position,'Appearance position differs '+expected.public_id);
 }
 const supplier=(await c.query("SELECT id FROM ontap_shadow.suppliers WHERE code='jobg8'")).rows[0];
 const master=(await c.query("SELECT supplier_job_id,count(*)::int AS n FROM ontap_shadow.supplier_adverts WHERE supplier_id=$1 GROUP BY supplier_job_id HAVING count(*)<>1",[supplier.id])).rows;
 assert.equal(master.length,0,'Duplicate master advert identities');
 const run=(await c.query('SELECT id FROM ontap_shadow.feed_runs WHERE supplier_id=$1 AND feed_date=$2::date AND feed_key LIKE $3 ORDER BY completed_at DESC LIMIT 1',[supplier.id,snapshot.feedDate,'selected-daily:'+snapshot.feedDate+':%'])).rows[0];
 assert.ok(run,'Selected master feed run is missing');
 const decisions=(await c.query("SELECT a.supplier_job_id AS public_id,d.decision,d.reason,d.rules_revision,d.evidence FROM ontap_shadow.selection_decisions d JOIN ontap_shadow.supplier_adverts a ON a.id=d.advert_id WHERE d.feed_run_id=$1 AND d.scope='daily_selected' ORDER BY a.supplier_job_id",[run.id])).rows;
 assert.equal(decisions.length,snapshot.records.length,'Selection decision count differs');
 const decisionById=new Map(decisions.map(r=>[r.public_id,r]));
 for(const expected of snapshot.records){
  const d=decisionById.get(expected.public_id);assert.ok(d,'Missing decision '+expected.public_id);
  assert.equal(d.decision,'include');assert.equal(d.rules_revision,snapshot.productionRunCommit);
  assert.equal(d.evidence.payload_sha256,expected.payload_sha256);
  assert.equal(d.evidence.source_row_position,expected.source_row_position);
 }
 const notes=rows.filter(r=>r.change_note);
 for(const row of notes){
  assert.ok(row.change_note.length<=240,'Changed-field note is too long');
  assert.match(row.change_note,/^[a-z0-9 _;]+ updated(?:; [a-z0-9 _]+ updated)*$/,'Changed-field note contains more than brief labels');
 }
 return {rows,runId:run.id,decisions:decisions.length,changedNotes:notes.length};
};
try{
 await c.connect();
 const before=Number((await c.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
 const estimate=Math.max(32*1024*1024,Buffer.byteLength(raw)*5+8*1024*1024);
 assert.ok(before+estimate+RESERVE<=MAX,'Storage estimate exceeds protected Preview ceiling');
 await c.query('BEGIN');
 try{
  await c.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
  await c.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:selected-review-full-payload'))");
  const prior=(await c.query('SELECT max(feed_date)::text AS date FROM ontap_shadow.daily_refresh_receipts WHERE feed_date<$1::date',[snapshot.feedDate])).rows[0].date;
  const previousRows=prior?(await c.query("SELECT j.public_id,aa.payload_sha256 FROM ontap_shadow.advert_appearances aa JOIN ontap_shadow.supplier_adverts a ON a.id=aa.advert_id JOIN ontap_shadow.jobs j ON j.id=a.job_id JOIN ontap_shadow.suppliers s ON s.id=aa.supplier_id WHERE s.code='jobg8' AND aa.seen_on=$1::date",[prior])).rows:[];
  const previousById=new Map(previousRows.map(r=>[r.public_id,r.payload_sha256]));
  const currentById=new Map(snapshot.records.map(r=>[r.public_id,r.payload_sha256]));
  const addedIds=[...seen].filter(id=>!previousById.has(id)).sort();
  const absentIds=[...previousById.keys()].filter(id=>!seen.has(id)).sort();
  const changedIds=[...seen].filter(id=>previousById.has(id)&&previousById.get(id)!==currentById.get(id)).sort();
  const masterWrite=await upsertSelectedMaster(c,{snapshot,scopes,source});
  const idempotentReplay=await upsertSelectedMaster(c,{snapshot,scopes,source});
  assert.equal(idempotentReplay.insertedMasterRows,0,'Identical refresh inserted duplicate master rows');
  assert.equal(idempotentReplay.updatedPayloadRows,0,'Identical refresh rewrote unchanged master payloads');
  await c.query('CREATE TABLE IF NOT EXISTS ontap_shadow.daily_publication_scopes(feed_date date NOT NULL,scope text NOT NULL,jobg8_ids jsonb NOT NULL,PRIMARY KEY(feed_date,scope))');
  for(const s of scopes)await c.query('INSERT INTO ontap_shadow.daily_publication_scopes AS t VALUES($1::date,$2,$3::jsonb) ON CONFLICT(feed_date,scope) DO UPDATE SET jobg8_ids=excluded.jobg8_ids WHERE t.jobg8_ids IS DISTINCT FROM excluded.jobg8_ids',[snapshot.feedDate,s.scope,JSON.stringify(s.jobg8Ids)]);
  const orders=(await c.query('SELECT scope,jobg8_ids FROM ontap_shadow.daily_publication_scopes WHERE feed_date=$1::date ORDER BY scope',[snapshot.feedDate])).rows;
  assert.equal(orders.length,scopes.length);
  const expectedScopes=new Map(scopes.map(s=>[s.scope,s.jobg8Ids]));
  for(const s of orders)assert.deepEqual(s.jobg8_ids,expectedScopes.get(s.scope),'Scope order differs: '+s.scope);
  const stateDigest=fingerprint({records:snapshot.records.map(({public_id,decision,payload_sha256,source_row_position})=>({public_id,decision,payload_sha256,source_row_position})),scopes});
  await c.query('CREATE TABLE IF NOT EXISTS ontap_shadow.daily_refresh_receipts(feed_date date PRIMARY KEY,production_commit text NOT NULL,feed_run_id bigint NOT NULL,record_count integer NOT NULL,state_sha256 text NOT NULL,completed_at timestamptz NOT NULL DEFAULT now())');
  await c.query('INSERT INTO ontap_shadow.daily_refresh_receipts(feed_date,production_commit,feed_run_id,record_count,state_sha256) VALUES($1::date,$2,$3,$4,$5) ON CONFLICT(feed_date) DO UPDATE SET production_commit=excluded.production_commit,feed_run_id=excluded.feed_run_id,record_count=excluded.record_count,state_sha256=excluded.state_sha256 WHERE daily_refresh_receipts.state_sha256 IS DISTINCT FROM excluded.state_sha256',[snapshot.feedDate,snapshot.productionAppCommit,snapshot.productionWorkflowRunId,seen.size,stateDigest]);
  const master=await verifyMaster();
  const visible=await readCurrentPublication(c);
  assert.equal(visible.feedDate,snapshot.feedDate);
  assert.deepEqual(visible.records.map(r=>r.public_id).sort(),[...seen].sort(),'Current reader exposed a stale or incomplete set');
  for(const s of scopes){const got=visible.scopes.find(x=>x.scope===s.scope);assert.deepEqual(got?.jobg8_ids,s.jobg8Ids);}
  // Delete only the migrated selected rows for this date, after master and current-reader verification.
  const legacy=await legacyRows();
  const legacySelected=legacy.filter(r=>r.decision==='SELECTED');
  let removedLegacyPayloadRows=0;
  if(legacySelected.length){
   assert.equal(legacySelected.length,snapshot.records.length,'Legacy selected row set is partial; keep it intact');
   assert.deepEqual(legacySelected.map(r=>r.public_id).sort(),[...seen].sort(),'Legacy selected IDs do not match master source');
   const legacyById=new Map(legacySelected.map(r=>[r.public_id,r]));
   for(const expected of snapshot.records){
    const row=legacyById.get(expected.public_id);
    assert.equal(row.payload_sha256,expected.payload_sha256);
    assert.equal(row.source_row_position,expected.source_row_position);
    assert.deepEqual(canon(row.raw_payload),canon(expected.raw_payload));
   }
   const del=await c.query("DELETE FROM "+table+" WHERE feed_date=$1::date AND decision='SELECTED' AND public_id=ANY($2::text[])",[snapshot.feedDate,[...seen]]);
   assert.equal(del.rowCount,snapshot.records.length,'Did not remove exactly the migrated Wednesday selected payload copies');
   removedLegacyPayloadRows=del.rowCount;
  }
  const leftover=(await c.query("SELECT count(*)::int AS n FROM "+table+" WHERE feed_date=$1::date AND decision='SELECTED'",[snapshot.feedDate])).rows[0].n;
  assert.equal(leftover,0,'Legacy selected full payload rows remain for this date');
  const afterDeleteVisible=await readCurrentPublication(c);
  assert.deepEqual(afterDeleteVisible.records.map(r=>r.public_id).sort(),[...seen].sort(),'Current reader depends on deleted legacy rows');
  const after=Number((await c.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
  assert.ok(after+RESERVE<=MAX,'Post-write Preview reserve breached');
  await c.query('COMMIT');
  const active=await readCurrentPublication(c);
  assert.equal(active.feedDate,snapshot.feedDate);
  const cleanup=await runMasterCleanup(c,{asOfDate:snapshot.feedDate,mode:'dry-run'});
  assert.equal(cleanup.mode,'dry-run');assert.equal(cleanup.purgedCount,0);
  const tracking=(await c.query("SELECT count(*)::int AS n FROM ontap_shadow.supplier_adverts a JOIN ontap_shadow.suppliers s ON s.id=a.supplier_id WHERE s.code='jobg8' AND a.raw_payload IS NOT NULL AND NOT EXISTS(SELECT 1 FROM ontap_shadow.advert_appearances aa WHERE aa.advert_id=a.id)")).rows[0].n;
  const report={status:'passed',mode:'automatic_daily_master_refresh',feedDate:snapshot.feedDate,dateProvidedByRequest:false,amSourceGuardPassed:true,productionOutputRunId:snapshot.productionWorkflowRunId,selectedIds:seen.size,
   reviewOnlyRowsSaved:0,excludedRowsSaved:0,masterPayloadRows:seen.size,appearanceRows:master.rows.length,decisionRows:master.decisions,
   exactIdsPayloadsHashesPositionsDecisionsMatch:true,scopeCount:scopes.length,exactScopeOrderingMatch:true,
   insertedMasterRows:masterWrite.insertedMasterRows,updatedPayloadRows:masterWrite.updatedPayloadRows,unchangedMasterRows:masterWrite.unchangedMasterRows,
   changedFieldNotes:master.changedNotes,legacySelectedPayloadRowsRemoved:removedLegacyPayloadRows,legacySelectedRowsRemaining:leftover,
   previousNeonFeedDate:prior,previousNeonSelected:previousById.size,addedIds,absentIds,changedIds,
   currentPublicationReaderUsesMasterAndAppearances:true,legacyDeletionDidNotChangeCurrentSet:true,
   masterCleanupDryRun:cleanup,masterRowsMissingAppearanceTracking:tracking,
   appearanceMetadataRetention:'No automatic expiry is configured; dated appearance rows are retained.',
   databaseBytesBefore:before,databaseBytesAfter:after,estimatedAdmissionBytes:estimate,maximumBytes:MAX,reserveBytes:RESERVE,
   identicalReplayRowsToWrite:idempotentReplay.insertedMasterRows+idempotentReplay.updatedPayloadRows,duplicates:0,productionChanged:false,expiryChanged:false};
  await fs.mkdir('dist',{recursive:true});await fs.writeFile('dist/daily-refresh-report.json',JSON.stringify(report,null,2)+'\n');
  await fs.writeFile('dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><h1>Neon daily master refresh passed</h1>');
  console.log('ONTAP_DAILY_MASTER_REFRESH '+JSON.stringify(report));
 }catch(e){await c.query('ROLLBACK');throw e;}
}finally{await c.end();}
