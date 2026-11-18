import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import pg from 'pg';
import {loadDailyFailureProbe,injectDailyFailure,verifyNoDailyFailureResidue} from './daily-failure-probe.mjs';
import {readCurrentPublication} from './current-publication.mjs';
import {runMasterCleanup} from './master-cleanup.mjs';
import {gunzipSync} from 'node:zlib';
import {requirePreview,hash,MAX,RESERVE} from './publisher-safeguards.mjs';
requirePreview(process.env);
const source=JSON.parse(await fs.readFile('daily-source.json','utf8'));
assert.equal(source.mode,'daily_latest');assert.equal(source.dateProvidedByRequest,false);
const raw=await fs.readFile('selected-review-payloads.json');
assert.equal(hash(raw),source.payloadPackageSha256);
const snapshot=JSON.parse(raw);
assert.equal(snapshot.feedDate,source.archiveDate);assert.equal(snapshot.archiveSha256,source.archiveSha256);
assert.equal(snapshot.productionAppCommit,source.productionAppCommitSha);
assert.equal(snapshot.productionWorkflowRunId,source.productionOutputRunId);
const scopes=JSON.parse(await fs.readFile('daily-scopes.json','utf8'));
const canon=v=>Array.isArray(v)?v.map(canon):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canon(v[k])])):v;
const fingerprint=v=>hash(JSON.stringify(canon(v)));
const expectedProvenance={archiveKey:snapshot.archiveKey,archiveSha256:snapshot.archiveSha256,productionWorkflowRunId:snapshot.productionWorkflowRunId,productionRunCommit:snapshot.productionRunCommit,productionAppCommit:snapshot.productionAppCommit};
const fields=['decision','decision_reason','selector_revision','source_row_position','payload_sha256'];
const seen=new Set(),positions=new Set();
for(const row of snapshot.records){
 assert.ok(row.public_id&&!seen.has(row.public_id));seen.add(row.public_id);
 assert.ok(['SELECTED','REVIEW'].includes(row.decision));
 assert.ok(Number.isInteger(row.source_row_position)&&row.source_row_position>0&&!positions.has(row.source_row_position));positions.add(row.source_row_position);
 assert.equal(fingerprint(row.raw_payload),row.payload_sha256);
}
const selected=new Set(snapshot.records.filter(r=>r.decision==='SELECTED').map(r=>r.public_id));
assert.deepEqual([...new Set(scopes.flatMap(s=>s.jobg8Ids))].sort(),[...selected].sort());
for(const s of scopes)assert.equal(new Set(s.jobg8Ids).size,s.jobg8Ids.length,'Duplicate within scope '+s.scope);
const u=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);u.searchParams.set('sslmode','verify-full');
const c=new pg.Client({connectionString:u.toString(),connectionTimeoutMillis:15000,query_timeout:120000,application_name:'ontap-preview-automatic-daily-refresh'});
const columns='public_id,decision,decision_reason,selector_revision,archive_sha256,raw_payload,payload_sha256,source_provenance,source_row_position';
const table='ontap_shadow.selected_review_payload_records';
const read=async()=> (await c.query('SELECT '+columns+' FROM '+table+' WHERE feed_date=$1::date ORDER BY public_id',[snapshot.feedDate])).rows;
function different(a,b){return !a||fields.some(f=>a[f]!==b[f])||a.archive_sha256!==snapshot.archiveSha256||fingerprint(a.source_provenance)!==fingerprint(expectedProvenance);}
try{
 await c.connect();
 const failureProbe=await loadDailyFailureProbe(c,source);
 const beforeBytes=Number((await c.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
 await c.query('BEGIN');
 try{
  await c.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:selected-review-full-payload'))");
  const latest=(await c.query('SELECT max(feed_date)::text AS date FROM '+table)).rows[0].date;
  assert.ok(!latest||latest<=snapshot.feedDate,'Refuse an older feed over a newer Neon snapshot');
  const existing=await read(),byId=new Map(existing.map(r=>[r.public_id,r]));
  assert.ok(existing.every(r=>seen.has(r.public_id)),'Existing same-day IDs differ; do not silently retain or delete unexpected rows');
  const delta=snapshot.records.filter(r=>different(byId.get(r.public_id),r));
  const newRows=delta.filter(r=>!byId.has(r.public_id));
  const changedPayloads=delta.filter(r=>byId.has(r.public_id)&&byId.get(r.public_id).payload_sha256!==r.payload_sha256);
  const metadataOnly=delta.length-newRows.length-changedPayloads.length;
  const bulky=[...newRows,...changedPayloads];
  const payloadBytes=bulky.reduce((n,r)=>n+Buffer.byteLength(JSON.stringify(r)),0);
  const metadataBytes=delta.reduce((n,r)=>n+Buffer.byteLength(JSON.stringify({...r,raw_payload:undefined})),0);
  const estimate=Math.max(32*1024*1024,payloadBytes*5+metadataBytes*3+8*1024*1024);
  console.log('ONTAP_DAILY_REFRESH_STORAGE_ADMISSION '+JSON.stringify({databaseBytesBefore:beforeBytes,estimatedAdmissionBytes:estimate,maximumBytes:MAX,reserveBytes:RESERVE,remainingBytesBeforeReserve:MAX-RESERVE-beforeBytes,payloadBytes,metadataBytes,newRows:newRows.length,changedPayloadRows:changedPayloads.length,metadataOnlyRows:metadataOnly}));
  assert.ok(beforeBytes+estimate+RESERVE<=MAX,'Storage estimate exceeds protected Preview ceiling');
  for(let i=0;i<delta.length;i+=100)await c.query(
   'INSERT INTO '+table+' AS t(feed_date,public_id,decision,decision_reason,selector_revision,archive_sha256,raw_payload,payload_sha256,source_provenance,source_row_position) '+
   'SELECT $1::date,r.public_id,r.decision,r.decision_reason,r.selector_revision,$2,r.raw_payload,r.payload_sha256,$3::jsonb,r.source_row_position '+
   'FROM jsonb_to_recordset($4::jsonb) AS r(public_id text,decision text,decision_reason text,selector_revision text,raw_payload jsonb,payload_sha256 text,source_row_position integer) '+
   'ON CONFLICT(feed_date,public_id) DO UPDATE SET decision=excluded.decision,decision_reason=excluded.decision_reason,selector_revision=excluded.selector_revision,archive_sha256=excluded.archive_sha256,'+
   'raw_payload=CASE WHEN t.payload_sha256 IS DISTINCT FROM excluded.payload_sha256 THEN excluded.raw_payload ELSE t.raw_payload END,payload_sha256=excluded.payload_sha256,source_provenance=excluded.source_provenance,source_row_position=excluded.source_row_position',
   [snapshot.feedDate,snapshot.archiveSha256,JSON.stringify(expectedProvenance),JSON.stringify(delta.slice(i,i+100))]);
  await injectDailyFailure(c,failureProbe,'after-payload-write',{snapshot,source});
  const got=await read(),gotById=new Map(got.map(r=>[r.public_id,r]));
  assert.equal(got.length,snapshot.records.length);
  assert.deepEqual([...gotById.keys()].sort(),[...seen].sort());
  for(const e of snapshot.records){
   const a=gotById.get(e.public_id);
   assert.equal(different(a,e),false,'Decision/provenance differs '+e.public_id);
   assert.equal(fingerprint(a.raw_payload),e.payload_sha256,'Payload hash differs '+e.public_id);
   assert.deepEqual(canon(a.raw_payload),canon(e.raw_payload));
  }
  // Run the same change detector again: a repeated daily refresh must write zero rows.
  const replayDelta=snapshot.records.filter(r=>different(gotById.get(r.public_id),r));
  assert.equal(replayDelta.length,0,'Identical refresh would rewrite rows');
  await c.query('CREATE TABLE IF NOT EXISTS ontap_shadow.daily_publication_scopes(feed_date date NOT NULL,scope text NOT NULL,jobg8_ids jsonb NOT NULL,PRIMARY KEY(feed_date,scope))');
  for(const s of scopes)await c.query('INSERT INTO ontap_shadow.daily_publication_scopes AS t VALUES($1::date,$2,$3::jsonb) ON CONFLICT(feed_date,scope) DO UPDATE SET jobg8_ids=excluded.jobg8_ids WHERE t.jobg8_ids IS DISTINCT FROM excluded.jobg8_ids',[snapshot.feedDate,s.scope,JSON.stringify(s.jobg8Ids)]);
  const orders=(await c.query('SELECT scope,jobg8_ids FROM ontap_shadow.daily_publication_scopes WHERE feed_date=$1::date ORDER BY scope',[snapshot.feedDate])).rows;
  assert.equal(orders.length,scopes.length);
  const expectedScopes=new Map(scopes.map(s=>[s.scope,s.jobg8Ids]));
  for(const s of orders)assert.deepEqual(s.jobg8_ids,expectedScopes.get(s.scope));
  const previousBuild=(await c.query('SELECT compressed_payload,uncompressed_sha256 FROM ontap_shadow.publisher_snapshots WHERE feed_date=$1::date',[snapshot.feedDate])).rows[0];
  let previousPreviewBuildMatches=null;
  if(previousBuild){
   const bytes=gunzipSync(previousBuild.compressed_payload);
   assert.equal(hash(bytes),previousBuild.uncompressed_sha256);
   const rows=JSON.parse(bytes),actual=new Map();
   for(const r of rows)if(r.source==='JobG8'){if(!actual.has(r.scope))actual.set(r.scope,[]);actual.get(r.scope).push(r.public_id);}
   for(const s of scopes)assert.deepEqual(actual.get(s.scope)||[],s.jobg8Ids,'Automatic refresh differs from verified website Preview scope '+s.scope);
   previousPreviewBuildMatches=true;
  }
  const stateDigest=fingerprint({records:snapshot.records.map(({public_id,decision,payload_sha256,source_row_position})=>({public_id,decision,payload_sha256,source_row_position})),scopes});
  await c.query('CREATE TABLE IF NOT EXISTS ontap_shadow.daily_refresh_receipts(feed_date date PRIMARY KEY,production_commit text NOT NULL,feed_run_id bigint NOT NULL,record_count integer NOT NULL,state_sha256 text NOT NULL,completed_at timestamptz NOT NULL DEFAULT now())');
  await c.query('INSERT INTO ontap_shadow.daily_refresh_receipts(feed_date,production_commit,feed_run_id,record_count,state_sha256) VALUES($1::date,$2,$3,$4,$5) ON CONFLICT(feed_date) DO UPDATE SET production_commit=excluded.production_commit,feed_run_id=excluded.feed_run_id,record_count=excluded.record_count,state_sha256=excluded.state_sha256 WHERE daily_refresh_receipts.state_sha256 IS DISTINCT FROM excluded.state_sha256',[snapshot.feedDate,snapshot.productionAppCommit,snapshot.productionWorkflowRunId,got.length,stateDigest]);
  const afterBytes=Number((await c.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
  assert.ok(afterBytes+RESERVE<=MAX,'Post-write Preview reserve breached');
  await injectDailyFailure(c,failureProbe,'before-commit',{snapshot,source});
  await c.query('COMMIT');
  const active=(await c.query('SELECT feed_date::text,record_count,state_sha256 FROM ontap_shadow.daily_refresh_receipts ORDER BY feed_date DESC LIMIT 1')).rows[0];
  assert.equal(active.feed_date,snapshot.feedDate);assert.equal(active.record_count,got.length);assert.equal(active.state_sha256,stateDigest);
  const visible=await readCurrentPublication(c);
  assert.equal(visible.feedDate,snapshot.feedDate);
  assert.deepEqual(visible.records.map(r=>r.public_id).sort(),[...selected].sort());
  const masterCleanupPlan=await runMasterCleanup(c,{asOfDate:snapshot.feedDate,mode:'dry-run'});
  const failureResidue=await verifyNoDailyFailureResidue(c,snapshot.feedDate);
  const report={failureResidue,masterCleanupPlan,currentPublicationReaderVerified:true,status:'passed',mode:'automatic_daily_refresh',feedDate:snapshot.feedDate,dateProvidedByRequest:false,productionDeploymentRunId:source.productionDeploymentRunId,productionOutputRunId:snapshot.productionWorkflowRunId,productionCommit:snapshot.productionAppCommit,selectedIds:selected.size,reviewOnlyIds:got.length-selected.size,reviewListIds:snapshot.reviewIds,neonRows:got.length,
   exactIdsAndDecisionsMatch:true,fullPayloadAndHashesMatch:true,exactFeedPositionsMatch:true,scopeCount:scopes.length,exactScopeOrderingMatch:true,
   insertedRows:newRows.length,updatedPayloadRows:changedPayloads.length,metadataOnlyUpdatedRows:metadataOnly,unchangedRows:snapshot.records.length-delta.length,
   identicalReplayRowsToWrite:0,duplicates:0,activeFeedDate:active.feed_date,existingVerifiedPreviewScopesMatch:previousPreviewBuildMatches,excludedPayloadsWritten:0,
   databaseBytesBefore:beforeBytes,databaseBytesAfter:afterBytes,estimatedAdmissionBytes:estimate,productionChanged:false,expiryChanged:false};
  await fs.mkdir('dist',{recursive:true});await fs.writeFile('dist/daily-refresh-report.json',JSON.stringify(report,null,2)+'\n');
  await fs.writeFile('dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><h1>Neon automatic daily refresh passed</h1>');
  console.log('ONTAP_AUTOMATIC_DAILY_REFRESH '+JSON.stringify(report));
 }catch(e){await c.query('ROLLBACK');throw e;}
}finally{await c.end();}
