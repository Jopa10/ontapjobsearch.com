// Preview-only reconstruction of the daily website inputs from Neon.
// Scope/position evidence comes from the exact completed production publisher artifacts.
// It is independently validated against Neon selected IDs and then stored/read back
// in isolated Neon Preview. It does not independently replay selection or prove
// that the placement decisions originated in Neon.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import pg from 'pg';

const MAX=838860800, RESERVE=67108864;
const canon = x => JSON.stringify(x);
const bytes = async c => Number((await c.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
const source = JSON.parse(await fs.readFile('database/shadow/website-source.json','utf8'));
assert.equal(process.env.VERCEL_ENV,'preview');
assert.equal(process.env.ONTAP_SHADOW_NEON_PROJECT_ID,'noisy-fire-97386602');
assert.match(source.feedDate,/^20\d\d-\d\d-\d\d$/);
assert.equal(source.productionRunId,43824436796); // provenance guard: replaced by source run metadata when generalized
const url = new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
assert.ok(url.hostname.endsWith('.neon.tech'));
assert.ok(['require','verify-full'].includes(url.searchParams.get('sslmode')));
url.searchParams.set('sslmode','verify-full');
const c=new pg.Client({connectionString:url.toString(),connectionTimeoutMillis:15000,query_timeout:120000,
  application_name:'ontap-preview-complete-site-parity'});
const scopes=source.outputs, names=Object.keys(scopes);
assert.ok(names.length>=200,'Incomplete region/family publication');
const rows=[];
for(const [scope,list] of Object.entries(scopes)) {
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
  scopeCount:names.length,referenceRows:rows.length,referenceJobG8Rows:0,
  neonSelectedIds:0,exactSelectedIdsMatch:false,exactApplyUrlsMatch:false,
  referenceOrigin:'verified production output artifacts',scopedPlacementOrigin:'production artifact',
  independentSelectorReplay:false,productionChanged:false,
  databaseWriteScope:'ontap_shadow.published_scope_rows (Preview only)'};
try {
 await c.connect();
 const current=(await c.query('SELECT max(feed_date)::text AS date FROM ontap_shadow.selected_review_payload_records')).rows[0]?.date;
 assert.equal(current,source.feedDate,'Production artifacts and latest Neon date differ');
 const selected=(await c.query("SELECT public_id,raw_payload->>'/Job/ApplicationURL' AS apply_url FROM ontap_shadow.selected_review_payload_records WHERE feed_date=$1::date AND decision='SELECTED' ORDER BY public_id",[current])).rows;
 const sourceSelected=rows.filter(r=>r.source==='JobG8');
 const actualIds=new Set(sourceSelected.map(r=>r.public_id));
 assert.equal(actualIds.size,selected.length,'Exact published IDs vs Neon differ');
 const byId=new Map(selected.map(r=>[r.public_id,r.apply_url]));
 for(const r of sourceSelected)assert.equal(r.display.apply_url,byId.get(r.public_id),'Apply link mismatch '+r.public_id);
 report.referenceJobG8Rows=sourceSelected.length;report.neonSelectedIds=selected.length;
 report.exactSelectedIdsMatch=true;report.exactApplyUrlsMatch=true;
 const before=await bytes(c);
 const estimated=Buffer.byteLength(canon(rows))*4+32*1024*1024;
 assert.ok(before+estimated+RESERVE<MAX,'Insufficient Neon test database headroom');
 await c.query('BEGIN');
 try{
  await c.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:preview-scope-publisher'))");
  await c.query("CREATE TABLE IF NOT EXISTS ontap_shadow.published_scope_rows (feed_date date NOT NULL,scope text NOT NULL,position integer NOT NULL,public_id text NOT NULL,source text NOT NULL,display jsonb NOT NULL,PRIMARY KEY(feed_date,scope,position))");
  for(let i=0;i<rows.length;i+=100){
   await c.query("INSERT INTO ontap_shadow.published_scope_rows(feed_date,scope,position,public_id,source,display) SELECT $1::date,t.scope,t.position,t.public_id,t.source,t.display FROM jsonb_to_recordset($2::jsonb) AS t(scope text,position int,public_id text,source text,display jsonb) ON CONFLICT(feed_date,scope,position) DO UPDATE SET public_id=excluded.public_id,source=excluded.source,display=excluded.display",
     [current,JSON.stringify(rows.slice(i,i+100))]);
  }
  await c.query('COMMIT');
 }catch(e){await c.query('ROLLBACK');throw e;}
 const query=await c.query('SELECT scope,position,public_id,source,display FROM ontap_shadow.published_scope_rows WHERE feed_date=$1::date ORDER BY scope,position',[current]);
 assert.equal(query.rows.length,rows.length,'Neon publisher rows missing');
 const output=Object.fromEntries(names.map(n=>[n,[]]));
 for(const record of query.rows){
   assert.ok(record.scope in output);
   assert.equal(record.position,output[record.scope].length,'Scope ordering differs');
   const expected=rows.find(r=>r.scope===record.scope && r.position===record.position);
   assert.deepEqual(record.display,expected.display,'Publisher row differs '+record.scope);
   output[record.scope].push(record.display);
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
const layout='app/layout.tsx';let s=await fs.readFile(layout,'utf8');
s=s.replace(/<Analytics\s*\/>/g,'').replace(/<Script\b[\s\S]*?<\/Script>/g,'');await fs.writeFile(layout,s);
execFileSync('npm',['run','build'],{stdio:'inherit',env:{...process.env,NEXT_TELEMETRY_DISABLED:'1'}});
