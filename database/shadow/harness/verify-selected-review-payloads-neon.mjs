import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { createHash } from 'node:crypto';
import pg from 'pg';

const MAX_BYTES=838860800, RESERVE=64*1024*1024;
const hash=v=>createHash('sha256').update(v).digest('hex');
const canon=v=>Array.isArray(v)?v.map(canon):v&&typeof v==='object'
  ?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canon(v[k])])):v;
const bytes=async c=>Number((await c.query('SELECT pg_database_size(current_database())::text AS n')).rows[0].n);
async function wed(c) {
 const r=await c.query("SELECT public_id,projected_fields,snapshot_metadata FROM ontap_shadow.published_output_snapshot_records WHERE feed_date='2026-11-11'::date ORDER BY public_id");
 assert.equal(r.rows.length,5491,'Wednesday published snapshot row count changed');
 return {date:'2026-11-11',count:r.rows.length,sha256:hash(JSON.stringify(canon(r.rows)))};
}
async function run() {
 assert.equal(process.env.VERCEL_ENV,'preview','Preview only');
 assert.equal(process.env.ONTAP_SHADOW_NEON_PROJECT_ID,'noisy-fire-97386602','Wrong isolated Neon project');
 const source=JSON.parse(await fs.readFile('source-download.json','utf8'));
 assert.equal(source.mode,'selected_review_payloads');
 const raw=await fs.readFile('selected-review-payloads.json');
 assert.equal(hash(raw),source.snapshotSha256,'payload package fingerprint mismatch');
 const snapshot=JSON.parse(raw);
 assert.equal(snapshot.feedDate,source.feedDate);
 assert.equal(snapshot.productionWorkflowRunId,source.productionWorkflowRunId);
 assert.equal(snapshot.productionAppCommit,source.productionAppCommit);
 assert.equal(snapshot.productionRunCommit,source.productionRunCommit);
 assert.equal(snapshot.records.length,source.expectedRecords);
 assert.ok(snapshot.records.length>0);
 const seen=new Set();
 for(const r of snapshot.records) {
  assert.ok(r.public_id && !seen.has(r.public_id)); seen.add(r.public_id);
  assert.ok(['SELECTED','REVIEW'].includes(r.decision));
  assert.equal(r.selector_revision,snapshot.productionRunCommit);
  assert.equal(hash(JSON.stringify(canon(r.raw_payload))),r.payload_sha256,'full payload hash mismatch: '+r.public_id);
  assert.ok(r.raw_payload['/Job/Position'] && r.raw_payload['/Job/ApplicationURL']);
 }
 const url=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
 assert.ok(url.hostname.endsWith('.neon.tech') && ['require','verify-full'].includes(url.searchParams.get('sslmode')),'TLS Neon URL required');
 url.searchParams.set('sslmode','verify-full');
 const c=new pg.Client({connectionString:url.toString(),connectionTimeoutMillis:15000,query_timeout:120000,statement_timeout:90000,application_name:'ontap-shadow-selected-review-full-payload-test'});
 try {
  await c.connect();
  const before=await bytes(c), wedBefore=await wed(c);
  const estimate=Math.max(32*1024*1024,Buffer.byteLength(raw)*5);
  assert.ok(before+estimate+RESERVE<=MAX_BYTES,'Storage estimate exceeds protected Preview ceiling');
  const provenance={archiveKey:snapshot.archiveKey,archiveSha256:snapshot.archiveSha256,productionWorkflowRunId:snapshot.productionWorkflowRunId,productionRunCommit:snapshot.productionRunCommit,productionAppCommit:snapshot.productionAppCommit};
  await c.query('BEGIN');
  try {
   await c.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:selected-review-full-payload'))");
   await c.query('CREATE TABLE IF NOT EXISTS ontap_shadow.selected_review_payload_records ('+
    'feed_date date NOT NULL,public_id text NOT NULL,decision text NOT NULL CHECK (decision IN (\'SELECTED\',\'REVIEW\')),'+
    'decision_reason text NOT NULL,selector_revision text NOT NULL,archive_sha256 text NOT NULL,'+
    'raw_payload jsonb NOT NULL,payload_sha256 text NOT NULL,source_provenance jsonb NOT NULL,'+
    'created_at timestamptz NOT NULL DEFAULT now(),PRIMARY KEY(feed_date,public_id))');
   const rows=snapshot.records;
   for(let i=0;i<rows.length;i+=100) {
    await c.query('INSERT INTO ontap_shadow.selected_review_payload_records(feed_date,public_id,decision,decision_reason,selector_revision,archive_sha256,raw_payload,payload_sha256,source_provenance) '+
     'SELECT $1::date,r.public_id,r.decision,r.decision_reason,r.selector_revision,$2,r.raw_payload,r.payload_sha256,$3::jsonb '+
     'FROM jsonb_to_recordset($4::jsonb) AS r(public_id text,decision text,decision_reason text,selector_revision text,raw_payload jsonb,payload_sha256 text) '+
     'ON CONFLICT(feed_date,public_id) DO NOTHING',
     [snapshot.feedDate,snapshot.archiveSha256,JSON.stringify(provenance),JSON.stringify(rows.slice(i,i+100))]);
   }
   const got=await c.query('SELECT public_id,decision,decision_reason,selector_revision,archive_sha256,raw_payload,payload_sha256,source_provenance FROM ontap_shadow.selected_review_payload_records WHERE feed_date=$1::date ORDER BY public_id',[snapshot.feedDate]);
   assert.equal(got.rows.length,rows.length,'Neon payload row count mismatch');
   const byId=new Map(got.rows.map(r=>[r.public_id,r]));
   assert.deepEqual([...byId.keys()].sort(),rows.map(r=>r.public_id).sort(),'Neon selected/review IDs differ');
   for(const e of rows) {
    const a=byId.get(e.public_id);
    assert.equal(a.decision,e.decision); assert.equal(a.decision_reason,e.decision_reason);
    assert.equal(a.selector_revision,e.selector_revision); assert.equal(a.archive_sha256,snapshot.archiveSha256);
    assert.equal(a.payload_sha256,e.payload_sha256);
    assert.deepEqual(canon(a.raw_payload),canon(e.raw_payload),'full raw payload differs: '+e.public_id);
    assert.deepEqual(canon(a.source_provenance),canon(provenance));
   }
   const wedAfter=await wed(c); assert.deepEqual(wedAfter,wedBefore,'Wednesday snapshot changed');
   await c.query('COMMIT');
   const after=await bytes(c);
   const report={status:'passed',feedDate:snapshot.feedDate,productionWorkflowRunId:snapshot.productionWorkflowRunId,
    productionRunCommit:snapshot.productionRunCommit,productionAppCommit:snapshot.productionAppCommit,
    archiveKey:snapshot.archiveKey,archiveSha256:snapshot.archiveSha256,selectedIds:snapshot.selectedIds,
    reviewIds:snapshot.reviewIds,neonRows:got.rows.length,exactIdsMatch:true,fullPayloadAndHashesMatch:true,
    outcomeReasonAndRuleRevisionStored:true,excludedFeedPayloadsStored:0,table:'ontap_shadow.selected_review_payload_records',
    preservedWednesday:{...wedBefore,unchanged:true},databaseBytesBefore:before,databaseBytesAfter:after,
    databaseGrowthBytes:after-before,databaseHeadroomAfterBytes:MAX_BYTES-RESERVE-after,
    payloadBytes:snapshot.payloadBytes,snapshotSha256:source.snapshotSha256};
   await fs.mkdir('dist',{recursive:true});
   await fs.writeFile('dist/selected-review-readback-report.json',JSON.stringify(report,null,2)+'\n');
   await fs.writeFile('dist/selected-review-readback-manifest.json',JSON.stringify({...report,records:snapshot.records.map(({public_id,decision,payload_sha256})=>({public_id,decision,payload_sha256}))},null,2)+'\n');
   await fs.writeFile('dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><title>Ontap selected review payload verification</title><h1>Preview only</h1>');
   console.log('ONTAP_SELECTED_REVIEW_PAYLOADS '+JSON.stringify(report));
  } catch(e) { await c.query('ROLLBACK'); throw e; }
 } finally { await c.end(); }
}
run().catch(e=>{console.error('ONTAP_SELECTED_REVIEW_PAYLOADS_FAILED',e.code||e.name||'verification_error',e.name==='AssertionError'?e.message.split('\n')[0]:'');process.exitCode=1});
