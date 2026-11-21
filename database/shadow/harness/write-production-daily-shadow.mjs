import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import pg from 'pg';
import {readMasterAppearance,upsertSelectedMaster} from './daily-master-snapshot.mjs';
import {readCurrentPublication} from './current-publication.mjs';

const EXPECTED={host:'ep-green-sunset-zaycl73a-pooler.c-2.eu-west-2.aws.neon.tech',database:'neondb',role:'ontap_prod_daily_writer'};
const sourceDir=process.env.ONTAP_PROD_SOURCE_DIR;
const connectionString=process.env.ONTAP_NEON_PROD_DAILY_WRITE_URL;
const maxBytes=1024**3,reserveBytes=64*1024**2;
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const canon=v=>Array.isArray(v)?v.map(canon):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canon(v[k])])):v;
const fingerprint=v=>hash(JSON.stringify(canon(v)));
const readJson=async name=>JSON.parse(await fs.readFile(path.join(sourceDir,name),'utf8'));

assert.ok(sourceDir,'Missing prepared Production source directory');
assert.ok(connectionString,'Missing Production daily writer connection');
const source=await readJson('daily-source.json');
const scopes=await readJson('daily-scopes.json');
const raw=await fs.readFile(path.join(sourceDir,'selected-review-payloads.json'));
const snapshot=JSON.parse(raw.toString('utf8'));
assert.equal(hash(raw),source.payloadPackageSha256,'Payload package checksum mismatch');
assert.equal(source.mode,'daily_latest');
assert.equal(source.dateProvidedByRequest,false);
assert.equal(snapshot.schemaVersion,2);
assert.equal(snapshot.feedDate,source.archiveDate);
assert.equal(snapshot.archiveKey,source.archiveKey);
assert.equal(snapshot.archiveSha256,source.archiveSha256);
assert.equal(snapshot.productionWorkflowRunId,source.productionOutputRunId);
assert.equal(snapshot.productionAppCommit,source.productionAppCommitSha);
assert.equal(snapshot.productionRunCommit,source.productionRunCommitSha);
assert.equal(snapshot.selectedIds,snapshot.records.length);
assert.equal(snapshot.selectedPayloadRecords,snapshot.records.length);
assert.ok(snapshot.records.length>0);
const ids=new Set(),positions=new Set();
for(const r of snapshot.records){
 assert.ok(r.public_id&&!ids.has(r.public_id),'Duplicate or empty selected ID');ids.add(r.public_id);
 assert.equal(r.decision,'SELECTED');
 assert.ok(Number.isInteger(r.source_row_position)&&r.source_row_position>0&&!positions.has(r.source_row_position),'Invalid or duplicate feed position');positions.add(r.source_row_position);
 assert.equal(fingerprint(r.raw_payload),r.payload_sha256,'Source payload hash mismatch');
}
const scopeIds=new Set();
for(const s of scopes){
 assert.ok(s.scope&&Array.isArray(s.jobg8Ids));
 assert.equal(new Set(s.jobg8Ids).size,s.jobg8Ids.length,'Duplicate ID in scope '+s.scope);
 for(const id of s.jobg8Ids)scopeIds.add(id);
}
assert.deepEqual([...scopeIds].sort(),[...ids].sort(),'Published scope membership differs from selected payloads');

const url=new URL(connectionString);
assert.equal(url.hostname,EXPECTED.host,'Unexpected Production Neon endpoint');
assert.equal(url.pathname.replace(/^\//,''),EXPECTED.database,'Unexpected Production database');
assert.equal(decodeURIComponent(url.username),EXPECTED.role,'Unexpected Production writer role');
assert.ok(['require','verify-full'].includes(url.searchParams.get('sslmode')),'TLS is required');
url.searchParams.set('sslmode','verify-full');
const c=new pg.Client({connectionString:url.toString(),connectionTimeoutMillis:15000,query_timeout:120000,statement_timeout:120000,application_name:'ontap-neon-production-daily-shadow'});
let connected=false,transaction=false,committed=false;
try{
 await c.connect();connected=true;
 const identity=(await c.query('SELECT current_database() AS db,current_user AS role,pg_database_size(current_database())::text AS bytes')).rows[0];
 assert.equal(identity.db,EXPECTED.database);assert.equal(identity.role,EXPECTED.role);
 assert.equal(c.connection?.stream?.encrypted,true,'TLS is not active');
 const role=(await c.query('SELECT rolsuper,rolcreatedb,rolcreaterole,rolreplication FROM pg_roles WHERE rolname=current_user')).rows[0];
 assert.ok(role);for(const k of ['rolsuper','rolcreatedb','rolcreaterole','rolreplication'])assert.equal(role[k],false,'Elevated role attribute: '+k);
 assert.equal((await c.query("SELECT has_schema_privilege(current_user,'ontap_shadow','USAGE') AS ok")).rows[0].ok,true);
 const tables=['suppliers','feed_runs','jobs','supplier_adverts','advert_appearances','selection_decisions','daily_publication_scopes','daily_refresh_receipts'];
 for(const t of tables)for(const p of ['SELECT','INSERT','UPDATE'])assert.equal((await c.query('SELECT has_table_privilege(current_user,$1,$2) AS ok',['ontap_shadow.'+t,p])).rows[0].ok,true,'Missing '+p+' privilege on '+t);
 const seq=(await c.query("SELECT pg_get_serial_sequence('ontap_shadow.suppliers','id') AS name")).rows[0].name;
 assert.ok(seq);assert.equal((await c.query('SELECT has_sequence_privilege(current_user,$1,\'USAGE\') AS ok',[seq])).rows[0].ok,true,'Missing supplier identity sequence privilege');
 const before=Number(identity.bytes),estimate=Math.max(32*1024*1024,raw.length*5+8*1024*1024);
 assert.ok(Number.isSafeInteger(before)&&before>=0&&before+estimate+reserveBytes<=maxBytes,'Production 1 GiB storage reserve check failed');
 const columns=(await c.query("SELECT table_name,column_name FROM information_schema.columns WHERE table_schema='ontap_shadow' AND (table_name='advert_appearances' AND column_name IN ('source_row_position','payload_sha256','changed_fields','change_note') OR table_name IN ('daily_publication_scopes','daily_refresh_receipts'))")).rows;
 const got=new Set(columns.map(x=>x.table_name+'.'+x.column_name));
 for(const col of ['advert_appearances.source_row_position','advert_appearances.payload_sha256','advert_appearances.changed_fields','advert_appearances.change_note','daily_publication_scopes.scope','daily_publication_scopes.jobg8_ids','daily_refresh_receipts.feed_date','daily_refresh_receipts.state_sha256'])assert.ok(got.has(col),'Production schema prerequisite missing: '+col);
 await c.query('BEGIN');transaction=true;
 await c.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
 await c.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:selected-review-full-payload'))");
 const masterWrite=await upsertSelectedMaster(c,{snapshot,scopes,source,ensureSchema:false});
 const replay=await upsertSelectedMaster(c,{snapshot,scopes,source,ensureSchema:false});
 assert.equal(replay.insertedMasterRows,0,'Identical retry inserted rows');
 assert.equal(replay.updatedPayloadRows,0,'Identical retry rewrote unchanged rows');
 for(const s of scopes)await c.query('INSERT INTO ontap_shadow.daily_publication_scopes AS t(feed_date,scope,jobg8_ids) VALUES($1::date,$2,$3::jsonb) ON CONFLICT(feed_date,scope) DO UPDATE SET jobg8_ids=excluded.jobg8_ids WHERE t.jobg8_ids IS DISTINCT FROM excluded.jobg8_ids',[snapshot.feedDate,s.scope,JSON.stringify(s.jobg8Ids)]);
 const stateSha=fingerprint({records:snapshot.records.map(({public_id,decision,payload_sha256,source_row_position})=>({public_id,decision,payload_sha256,source_row_position})),scopes});
 await c.query('INSERT INTO ontap_shadow.daily_refresh_receipts AS t(feed_date,production_commit,feed_run_id,record_count,state_sha256) VALUES($1::date,$2,$3,$4,$5) ON CONFLICT(feed_date) DO UPDATE SET production_commit=excluded.production_commit,feed_run_id=excluded.feed_run_id,record_count=excluded.record_count,state_sha256=excluded.state_sha256,completed_at=now() WHERE t.state_sha256 IS DISTINCT FROM excluded.state_sha256',[snapshot.feedDate,snapshot.productionAppCommit,snapshot.productionWorkflowRunId,ids.size,stateSha]);
 const rows=await readMasterAppearance(c,snapshot.feedDate);
 assert.equal(rows.length,ids.size,'Production row count differs from source');
 const byId=new Map(rows.map(r=>[r.public_id,r]));assert.equal(byId.size,rows.length,'Duplicate Production rows');
 for(const expected of snapshot.records){const actual=byId.get(expected.public_id);assert.ok(actual,'Missing Production row '+expected.public_id);assert.equal(actual.payload_sha256,expected.payload_sha256);assert.deepEqual(canon(actual.raw_payload),canon(expected.raw_payload));assert.equal(actual.source_row_position,expected.source_row_position);}
 const decisionRun=(await c.query("SELECT id FROM ontap_shadow.feed_runs WHERE supplier_id=(SELECT id FROM ontap_shadow.suppliers WHERE code='jobg8') AND feed_key=$1",[ 'selected-daily:'+snapshot.feedDate+':'+snapshot.archiveSha256+':'+snapshot.productionWorkflowRunId])).rows[0];
 assert.ok(decisionRun,'Missing Production feed receipt');
 const decisions=(await c.query("SELECT a.supplier_job_id AS id,d.decision,d.rules_revision,d.evidence FROM ontap_shadow.selection_decisions d JOIN ontap_shadow.supplier_adverts a ON a.id=d.advert_id WHERE d.feed_run_id=$1 AND d.scope='daily_selected'",[decisionRun.id])).rows;
 assert.equal(decisions.length,ids.size,'Decision count differs');
 for(const d of decisions){const expected=snapshot.records.find(r=>r.public_id===d.id);assert.ok(expected);assert.equal(d.decision,'include');assert.equal(d.rules_revision,snapshot.productionRunCommit);assert.equal(d.evidence.payload_sha256,expected.payload_sha256);assert.equal(d.evidence.source_row_position,expected.source_row_position);}
 const storedScopes=(await c.query('SELECT scope,jobg8_ids FROM ontap_shadow.daily_publication_scopes WHERE feed_date=$1::date ORDER BY scope',[snapshot.feedDate])).rows;
 assert.equal(storedScopes.length,scopes.length);const scopeMap=new Map(scopes.map(s=>[s.scope,s.jobg8Ids]));
 for(const s of storedScopes)assert.deepEqual(s.jobg8_ids,scopeMap.get(s.scope),'Scope order differs: '+s.scope);
 const reader=await readCurrentPublication(c);assert.equal(reader.feedDate,snapshot.feedDate);assert.deepEqual(reader.records.map(r=>r.public_id).sort(),[...ids].sort());
 for(const s of scopes)assert.deepEqual(reader.scopes.find(x=>x.scope===s.scope)?.jobg8_ids,s.jobg8Ids);
 const after=Number((await c.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
 assert.ok(after+reserveBytes<=maxBytes,'Production storage reserve breached');
 await c.query('COMMIT');transaction=false;committed=true;
 const final=await readCurrentPublication(c);assert.equal(final.feedDate,snapshot.feedDate);assert.deepEqual(final.records.map(r=>r.public_id).sort(),[...ids].sort());
 const report={status:'passed',mode:'daily_production_shadow_write',feedDate:snapshot.feedDate,sourceRunId:snapshot.productionWorkflowRunId,selectedIds:ids.size,scopeCount:scopes.length,exactIdsPayloadHashesPositionsDecisionsAndScopeArraysMatch:true,duplicateIds:0,insertedMasterRows:masterWrite.insertedMasterRows,updatedPayloadRows:masterWrite.updatedPayloadRows,unchangedMasterRows:masterWrite.unchangedMasterRows,cleanupPerformed:false,liveSiteSwitched:false,productionChanged:true,databaseBytesBefore:before,databaseBytesAfter:after,storageCeilingBytes:maxBytes,storageReserveBytes:reserveBytes,stateSha256:stateSha,writesCommitted:committed};
 console.log('ONTAP_PROD_NEON_DAILY_SHADOW_WRITE '+JSON.stringify(report));
 await fs.writeFile(process.env.ONTAP_PROD_REPORT_PATH,JSON.stringify(report,null,2)+'\n');
}catch(e){
 if(transaction)await c.query('ROLLBACK').catch(()=>{});
 console.error('Production Neon daily shadow write failed before successful commit:',e.message);
 throw e;
}finally{if(connected)await c.end().catch(()=>{});}
