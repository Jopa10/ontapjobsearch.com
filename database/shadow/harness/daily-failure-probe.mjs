// Explicit Preview-only fault probe; absent configuration means no action.
// Every injected failure is raised before COMMIT, so the real updater rolls back.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import pg from 'pg';
import {requirePreview,hash} from './publisher-safeguards.mjs';
import {readCurrentPublication} from './current-publication.mjs';
const canon=v=>Array.isArray(v)?v.map(canon):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canon(v[k])])):v;
const digest=v=>hash(JSON.stringify(canon(v)));
function nextDay(day){const d=new Date(day+'T00:00:00Z');d.setUTCDate(d.getUTCDate()+1);return d.toISOString().slice(0,10);}
async function view(c){
 const p=await readCurrentPublication(c);
 const receipt=(await c.query('SELECT record_count,state_sha256 FROM ontap_shadow.daily_refresh_receipts WHERE feed_date=$1::date',[p.feedDate])).rows[0];
 const total=Number((await c.query('SELECT count(*)::text AS n FROM ontap_shadow.selected_review_payload_records WHERE feed_date=$1::date',[p.feedDate])).rows[0].n);
 return {feedDate:p.feedDate,selectedIds:p.records.length,recordCount:total,scopeCount:p.scopes.length,
  digest:digest({day:p.feedDate,rows:p.records.map(r=>[r.public_id,r.payload_sha256,r.source_row_position]),scopes:p.scopes,receipt})};
}
export async function loadDailyFailureProbe(c,source){
 let config;
 try{config=JSON.parse(await fs.readFile('daily-fault-injection.json','utf8'));}
 catch(e){if(e.code==='ENOENT')return null;throw e;}
 requirePreview(process.env);
 assert.equal(config.enabled,true);assert.match(config.runToken,/^daily-[0-9]+$/);
 assert.ok(['after-payload-write','before-commit'].includes(config.stage));
 const baseline=await view(c);assert.equal(baseline.feedDate,source.archiveDate);
 assert.equal(Number((await c.query('SELECT count(*)::text AS n FROM ontap_shadow.selected_review_payload_records WHERE feed_date>$1::date',[baseline.feedDate])).rows[0].n),0,'Unexpected future feed data; do not inject');
 console.log('ONTAP_DAILY_FAILURE_BASELINE '+JSON.stringify({...baseline,stage:config.stage,runToken:config.runToken}));
 const gate=JSON.parse(await fs.readFile('failure-recovery-request.json','utf8'));
 assert.equal(gate.mode,'failure_recovery');assert.equal(gate.runToken,config.runToken);
 return {...config,baseline};
}
export async function injectDailyFailure(c,probe,stage,{snapshot,source}){
 if(!probe||probe.stage!==stage)return;
 requirePreview(process.env);
 const date=nextDay(snapshot.feedDate),id='ontap-failure-probe-'+probe.runToken+'-'+stage;
 const row=structuredClone(snapshot.records.find(r=>r.decision==='SELECTED'));
 row.public_id=id;row.decision='SELECTED';row.decision_reason='isolated uncommitted failure probe';
 row.raw_payload['/Job/DisplayReference']=id;row.raw_payload['/Job/Position']='Isolated daily refresh interruption probe';
 row.raw_payload['/Job/ApplicationURL']='https://example.invalid/uncommitted-probe';
 row.payload_sha256=digest(row.raw_payload);row.source_row_position=1;
 await c.query("INSERT INTO ontap_shadow.selected_review_payload_records(feed_date,public_id,decision,decision_reason,selector_revision,archive_sha256,raw_payload,payload_sha256,source_provenance,source_row_position) VALUES($1::date,$2,'SELECTED',$3,$4,$5,$6::jsonb,$7,$8::jsonb,1)",
 [date,id,row.decision_reason,row.selector_revision,snapshot.archiveSha256,JSON.stringify(row.raw_payload),row.payload_sha256,JSON.stringify({failureProbe:true,runToken:probe.runToken})]);
 await c.query("INSERT INTO ontap_shadow.daily_publication_scopes VALUES($1::date,'isolated-failure-probe',$2::jsonb)",[date,JSON.stringify([id])]);
 if(stage==='before-commit'){
  await c.query('INSERT INTO ontap_shadow.daily_refresh_receipts(feed_date,production_commit,feed_run_id,record_count,state_sha256) VALUES($1::date,$2,$3,1,$4)',
    [date,snapshot.productionAppCommit,snapshot.productionWorkflowRunId,digest({date,id,uncommitted:true})]);
  const writer=await view(c);assert.equal(writer.feedDate,date);assert.equal(writer.selectedIds,1);
 }else{
  const writer=await view(c);assert.equal(writer.digest,probe.baseline.digest);
 }
 const staged=Number((await c.query('SELECT count(*)::text AS n FROM ontap_shadow.selected_review_payload_records WHERE feed_date=$1::date',[date])).rows[0].n);
 assert.equal(staged,1);
 const u=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);u.searchParams.set('sslmode','verify-full');
 const observer=new pg.Client({connectionString:u.toString(),connectionTimeoutMillis:15000,query_timeout:120000,application_name:'ontap-preview-independent-failure-reader'});
 try{
  await observer.connect();
  const writerPid=(await c.query('SELECT pg_backend_pid() AS id')).rows[0].id;
  const readerPid=(await observer.query('SELECT pg_backend_pid() AS id')).rows[0].id;
  assert.notEqual(writerPid,readerPid,'Observer must use an independent backend');
  const observed=await view(observer);assert.deepEqual(observed,probe.baseline,'A reader saw a partial refresh');
  assert.equal(Number((await observer.query('SELECT count(*)::text AS n FROM ontap_shadow.selected_review_payload_records WHERE public_id=$1',[id])).rows[0].n),0);
  console.log('ONTAP_DAILY_FAILURE_VISIBILITY '+JSON.stringify({status:'passed',stage,runToken:probe.runToken,
   fictionalNextDay:date,stagedUncommittedRows:staged,readerFeedDate:observed.feedDate,readerSelectedIds:observed.selectedIds,
   readerRecordCount:observed.recordCount,readerScopeCount:observed.scopeCount,readerDigest:observed.digest,independentBackend:true,partialSetVisible:false}));
 }finally{await observer.end();}
 const error=new Error('ONTAP_EXPECTED_DAILY_INTERRUPTION:'+stage);error.code='ONTAP_EXPECTED_DAILY_INTERRUPTION';throw error;
}
export async function verifyNoDailyFailureResidue(c,day){
 const probes=Number((await c.query("SELECT count(*)::text AS n FROM ontap_shadow.selected_review_payload_records WHERE public_id LIKE 'ontap-failure-probe-%'")).rows[0].n);
 const future=Number((await c.query('SELECT count(*)::text AS n FROM ontap_shadow.daily_refresh_receipts WHERE feed_date>$1::date',[day])).rows[0].n);
 assert.equal(probes,0,'Uncommitted fault probe survived');
 assert.equal(future,0,'Uncommitted future completion receipt survived');
 return {remainingProbeRows:probes,remainingFutureReceipts:future,publication:await view(c)};
}
