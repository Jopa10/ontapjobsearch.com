// Preview-only reconstruction of the daily website inputs from Neon.
// Scope/position evidence comes from the exact completed production publisher artifacts.
// It is independently validated against Neon selected IDs and then stored/read back
// in isolated Neon Preview. It does not independently replay selection or prove
// that the placement decisions originated in Neon.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import pg from 'pg';
import {readCurrentPublication} from './current-publication.mjs';
import {requirePreview,requireBudget,requireSameDay,unpackSnapshot} from './publisher-safeguards.mjs';
import {gzipSync,gunzipSync} from 'node:zlib';
import {createHash} from 'node:crypto';

const MAX=838860800, RESERVE=67108864;
const canon = x => JSON.stringify(x);
const bytes = async c => Number((await c.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
const source = JSON.parse(await fs.readFile('database/shadow/website-source.json','utf8'));
requirePreview(process.env);
assert.equal(process.env.VERCEL_ENV,'preview');
assert.equal(process.env.ONTAP_SHADOW_NEON_PROJECT_ID,'noisy-fire-97386602');
assert.match(source.feedDate,/^20\d\d-\d\d-\d\d$/);
assert.ok(Number.isInteger(source.productionRunId) && source.productionRunId > 0, 'Missing completed publication run provenance');
const url = new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
assert.ok(url.hostname.endsWith('.neon.tech'));
assert.ok(['require','verify-full'].includes(url.searchParams.get('sslmode')));
url.searchParams.set('sslmode','verify-full');
const c=new pg.Client({connectionString:url.toString(),connectionTimeoutMillis:15000,query_timeout:120000,
  application_name:'ontap-preview-complete-site-parity'});
const scopes=source.outputs, names=Object.keys(scopes), extra=source.additionalOutputs || {};
assert.ok(names.length>=200,'Incomplete LIVE region/family publication');
const rows=[];
for(const [scope,list] of [...Object.entries(scopes), ...Object.entries(extra).map(([filename,list])=>['artifact:'+filename,list])]) {
  assert.ok(Array.isArray(list));
  const seen=new Set();
  for(const [position,row] of list.entries()) {
    assert.ok(row.job_id && row.title && row.apply_url);
    assert.ok(!seen.has(String(row.job_id)), 'Duplicate ID in '+scope);
    seen.add(String(row.job_id));
    rows.push({scope,position,public_id:String(row.job_id),source:String(row.source||''),display:row});
  }
}
let report={feedDate:source.feedDate,productionRunId:source.productionRunId,
  scopeCount:names.length,additionalArtifactScopes:Object.keys(extra).length,referenceRows:rows.length,referenceJobG8Rows:0,
  neonSelectedIds:0,exactSelectedIdsMatch:false,exactApplyUrlsMatch:false,
  referenceOrigin:'verified production output artifacts',scopedPlacementOrigin:'production artifact',
  independentSelectorReplay:false,productionChanged:false,
  databaseWriteScope:'ontap_shadow.publisher_snapshots (Preview only)'};
try {
 await c.connect();
 const publication=await readCurrentPublication(c);
 const current=publication.feedDate;
 requireSameDay(source.feedDate,current);
 const selected=publication.records.map(r=>({public_id:r.public_id,apply_url:r.raw_payload['/Job/ApplicationURL']}));
 const sourceSelected=rows.filter(r=>r.source==='JobG8');
 const actualIds=new Set(sourceSelected.map(r=>r.public_id));
 assert.equal(actualIds.size,selected.length,'Exact published IDs vs Neon differ');
 const byId=new Map(selected.map(r=>[r.public_id,r.apply_url]));
 for(const r of sourceSelected)assert.equal(r.display.apply_url,byId.get(r.public_id),'Apply link mismatch '+r.public_id);
 report.referenceJobG8Rows=sourceSelected.length;report.neonSelectedIds=selected.length;
 report.exactSelectedIdsMatch=true;report.exactApplyUrlsMatch=true;
 const before=await bytes(c);
 const serialized=Buffer.from(canon(rows)), packed=gzipSync(serialized,{level:9});
 const sha256=b=>createHash('sha256').update(b).digest('hex');
 const digest=sha256(serialized);
 const estimated=packed.length*4+32*1024*1024;
 requireBudget(before,packed.length);
 await c.query('BEGIN');
 try{
  await c.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:preview-scope-publisher'))");
  await c.query("CREATE TABLE IF NOT EXISTS ontap_shadow.publisher_snapshots (feed_date date PRIMARY KEY,production_run_id bigint NOT NULL,row_count integer NOT NULL,uncompressed_sha256 text NOT NULL,compressed_payload bytea NOT NULL)");
  // Prove transaction rollback on this isolated snapshot before making the final write.
  await c.query('SAVEPOINT rollback_probe');
  await c.query("INSERT INTO ontap_shadow.publisher_snapshots VALUES($1::date,$2,$3,$4,$5) ON CONFLICT(feed_date) DO UPDATE SET production_run_id=excluded.production_run_id,row_count=excluded.row_count,uncompressed_sha256=excluded.uncompressed_sha256,compressed_payload=excluded.compressed_payload",[current,source.productionRunId,rows.length,digest,packed]);
  await c.query('ROLLBACK TO SAVEPOINT rollback_probe');
  await c.query("INSERT INTO ontap_shadow.publisher_snapshots VALUES($1::date,$2,$3,$4,$5) ON CONFLICT(feed_date) DO UPDATE SET production_run_id=excluded.production_run_id,row_count=excluded.row_count,uncompressed_sha256=excluded.uncompressed_sha256,compressed_payload=excluded.compressed_payload",[current,source.productionRunId,rows.length,digest,packed]);
  assert.ok(await bytes(c)+RESERVE<MAX,'Post-write Neon headroom breached');
  await c.query('COMMIT');
 }catch(e){await c.query('ROLLBACK');throw e;}
 const snapshot=(await c.query('SELECT * FROM ontap_shadow.publisher_snapshots WHERE feed_date=$1::date',[current])).rows[0];
 const unpacked=gunzipSync(snapshot.compressed_payload);
 assert.equal(sha256(unpacked),digest,'Snapshot hash differs');
 assert.equal(snapshot.uncompressed_sha256,digest);
 assert.equal(String(snapshot.production_run_id),String(source.productionRunId));
 const readbackRows=unpackSnapshot(snapshot.compressed_payload,digest);
 assert.equal(readbackRows.length,rows.length,'Neon publisher rows missing');
 assert.deepEqual(readbackRows,rows,'Neon publisher snapshot differs');
 report.snapshotStorage='gzip JSON with SHA-256 verification';
 report.snapshotBytes=serialized.length;report.compressedSnapshotBytes=packed.length;
 report.snapshotSha256=digest;
 report.rollbackProbeExecuted=true;
 const expectedByPosition = new Map(rows.map(r=>[r.scope+':'+r.position,r]));
 const query={rows:readbackRows.sort((a,b)=>a.scope.localeCompare(b.scope)||a.position-b.position)};
 const output=Object.fromEntries(names.map(n=>[n,[]]));
 const readbackPositions=new Map();
 for(const record of query.rows){
   assert.equal(record.position,readbackPositions.get(record.scope) ?? 0,'Scope ordering differs');
   readbackPositions.set(record.scope,record.position+1);
   const expected=expectedByPosition.get(record.scope+':'+record.position);
   assert.deepEqual(record.display,expected.display,'Publisher row differs '+record.scope);
   if(record.scope in output) output[record.scope].push(record.display);
 }
 await fs.writeFile('shadow-db-outputs.json',JSON.stringify(output));
 await fs.writeFile('shadow-preview-metadata.json',JSON.stringify({date:current,...report}));
 report.databaseBytesBefore=before;report.databaseBytesAfter=await bytes(c);
 assert.ok(report.databaseBytesAfter+RESERVE<MAX,'Post-write Neon headroom breached');
 await fs.mkdir('public/shadow-verification',{recursive:true});
 await fs.writeFile('public/shadow-verification/publisher-readback.json',JSON.stringify({...report,readbackStatus:'passed'},null,2));
 console.log('ONTAP_NEON_PUBLISHER_READBACK_PASS '+JSON.stringify(report));
}finally{await c.end().catch(()=>{});}
execFileSync('python3',['-m','pip','install','--disable-pip-version-check','--target','/tmp/ontap-preview-python','openpyxl==3.1.5'],{stdio:'inherit'});
execFileSync('python3',['database/shadow/harness/prepare-full-preview.py'],{stdio:'inherit',env:{...process.env,PYTHONPATH:'/tmp/ontap-preview-python'}});
// Remove large build-only source evidence before Next.js/Vercel trace their runtime bundles.
// The validated readback report remains available under public/shadow-verification.
await fs.rm('database/shadow/website-source.json',{force:true});
await fs.rm('shadow-db-outputs.json',{force:true});
await fs.rm('shadow-preview-metadata.json',{force:true});
const layout='app/layout.tsx';let s=await fs.readFile(layout,'utf8');
s=s.replace(/<Analytics\s*\/>/g,'').replace(/<Script\b[\s\S]*?<\/Script>/g,'');await fs.writeFile(layout,s);
execFileSync('npm',['run','build'],{stdio:'inherit',env:{...process.env,NEXT_TELEMETRY_DISABLED:'1'}});
