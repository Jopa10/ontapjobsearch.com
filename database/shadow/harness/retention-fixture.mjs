// Expiry verification implementation. All mutations are restricted to pg_temp.
// Real stored advert history is never purged by this test module.
import assert from 'node:assert/strict';
import {gzipSync,gunzipSync} from 'node:zlib';
import {hash} from './publisher-safeguards.mjs';
export const canon=v=>Array.isArray(v)?v.map(canon):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canon(v[k])])):v;
export const fingerprint=v=>hash(JSON.stringify(canon(v)));
export function addDays(day,days){const d=new Date(day+'T00:00:00Z');d.setUTCDate(d.getUTCDate()+days);return d.toISOString().slice(0,10);}
function date(day){assert.match(day,/^\d{4}-\d{2}-\d{2}$/);assert.equal(addDays(day,0),day);}
export async function createFixtureTables(c){
 await c.query(`CREATE TEMP TABLE retention_jobs(public_id text PRIMARY KEY,last_seen date NOT NULL,inactive_since date,current_version text NOT NULL);
 CREATE TEMP TABLE retention_versions(public_id text REFERENCES retention_jobs(public_id),version_sha256 text NOT NULL,payload jsonb,archive_key text,archive_sha256 text,PRIMARY KEY(public_id,version_sha256));
 CREATE TEMP TABLE retention_clicks(click_id text PRIMARY KEY,visitor_stub text NOT NULL,public_id text NOT NULL,version_sha256 text NOT NULL,FOREIGN KEY(public_id,version_sha256) REFERENCES retention_versions(public_id,version_sha256));
 CREATE TEMP TABLE selected_review_payload_records(feed_date date,public_id text,decision text CHECK(decision IN ('SELECTED','REVIEW')),raw_payload jsonb,payload_sha256 text,source_row_position int,PRIMARY KEY(feed_date,public_id));
 CREATE TEMP TABLE daily_refresh_receipts(feed_date date PRIMARY KEY);
 CREATE TEMP TABLE daily_publication_scopes(feed_date date,scope text,jobg8_ids jsonb,PRIMARY KEY(feed_date,scope));`);
}
export async function applyFixtureFeed(c,{day,records}){
 date(day);
 const latest=(await c.query('SELECT max(feed_date)::text AS date FROM pg_temp.daily_refresh_receipts')).rows[0].date;
 assert.ok(!latest||latest<=day,'Older feed cannot reactivate missing jobs');
 const eligible=records.filter(r=>['SELECTED','REVIEW'].includes(r.decision));
 assert.equal(new Set(eligible.map(r=>r.id)).size,eligible.length);
 const ids=eligible.map(r=>r.id);
 await c.query('UPDATE pg_temp.retention_jobs SET inactive_since=COALESCE(inactive_since,$1::date) WHERE NOT(public_id=ANY($2::text[]))',[day,ids]);
 for(const [i,r] of eligible.entries()){
  const digest=fingerprint(r.payload);
  await c.query('INSERT INTO pg_temp.retention_jobs VALUES($1,$2::date,NULL,$3) ON CONFLICT(public_id) DO UPDATE SET last_seen=excluded.last_seen,inactive_since=NULL,current_version=excluded.current_version',[r.id,day,digest]);
  await c.query('INSERT INTO pg_temp.retention_versions(public_id,version_sha256,payload) VALUES($1,$2,$3::jsonb) ON CONFLICT(public_id,version_sha256) DO UPDATE SET payload=COALESCE(retention_versions.payload,excluded.payload)',[r.id,digest,JSON.stringify(r.payload)]);
  await c.query('INSERT INTO pg_temp.selected_review_payload_records VALUES($1::date,$2,$3,$4::jsonb,$5,$6) ON CONFLICT(feed_date,public_id) DO UPDATE SET decision=excluded.decision,raw_payload=excluded.raw_payload,payload_sha256=excluded.payload_sha256,source_row_position=excluded.source_row_position',[day,r.id,r.decision,JSON.stringify(r.payload),digest,i+1]);
 }
 await c.query("INSERT INTO pg_temp.daily_publication_scopes VALUES($1::date,'fixture-scope',$2::jsonb) ON CONFLICT(feed_date,scope) DO UPDATE SET jobg8_ids=excluded.jobg8_ids",[day,JSON.stringify(eligible.filter(r=>r.decision==='SELECTED').map(r=>r.id))]);
 await c.query('INSERT INTO pg_temp.daily_refresh_receipts VALUES($1::date) ON CONFLICT DO NOTHING',[day]);
 return {retained:eligible.length,excludedIgnored:records.length-eligible.length};
}
export async function archiveFixtureVersion(c,{id,version,archive}){
 const row=(await c.query('SELECT payload FROM pg_temp.retention_versions WHERE public_id=$1 AND version_sha256=$2',[id,version])).rows[0];
 assert.ok(row?.payload);
 assert.equal(fingerprint(row.payload),version);
 const envelope={publicId:id,versionSha256:version,payload:row.payload};
 const packed=gzipSync(Buffer.from(JSON.stringify(canon(envelope))),{level:9});
 const key=id+'/'+version+'.json.gz',digest=hash(packed);
 await archive.put(key,packed);
 const readback=await archive.get(key);
 assert.equal(hash(readback),digest);
 const got=JSON.parse(gunzipSync(readback));
 assert.equal(got.publicId,id);assert.equal(got.versionSha256,version);assert.equal(fingerprint(got.payload),version);
 await c.query('UPDATE pg_temp.retention_versions SET archive_key=$3,archive_sha256=$4 WHERE public_id=$1 AND version_sha256=$2',[id,version,key,digest]);
 return {key,compressedSha256:digest,versionSha256:version,publicId:id};
}
export async function purgeDueFixturePayloads(c,{asOfDate,archive}){
 date(asOfDate);
 const due=(await c.query('SELECT v.* FROM pg_temp.retention_versions v JOIN pg_temp.retention_jobs j USING(public_id) WHERE j.inactive_since IS NOT NULL AND j.inactive_since <= $1::date - 90 AND v.payload IS NOT NULL ORDER BY v.public_id,v.version_sha256',[asOfDate])).rows;
 // Verify every due archive before clearing any fixture payload.
 for(const row of due){
  assert.ok(row.archive_key&&row.archive_sha256,'No verified recoverable archive: '+row.public_id);
  const bytes=await archive.get(row.archive_key);
  assert.equal(hash(bytes),row.archive_sha256,'Archive checksum mismatch');
  const envelope=JSON.parse(gunzipSync(bytes));
  assert.equal(envelope.publicId,row.public_id);assert.equal(envelope.versionSha256,row.version_sha256);
  assert.equal(fingerprint(envelope.payload),row.version_sha256);
 }
 for(const row of due)await c.query('UPDATE pg_temp.retention_versions SET payload=NULL WHERE public_id=$1 AND version_sha256=$2',[row.public_id,row.version_sha256]);
 return due.map(row=>({id:row.public_id,version:row.version_sha256}));
}
export async function recoverFixtureClick(c,{clickId,archive}){
 const row=(await c.query('SELECT c.public_id,c.version_sha256,v.payload,v.archive_key,v.archive_sha256 FROM pg_temp.retention_clicks c JOIN pg_temp.retention_versions v USING(public_id,version_sha256) WHERE c.click_id=$1',[clickId])).rows[0];
 assert.ok(row,'Click/history link missing');
 let payload=row.payload;
 if(!payload){
  const packed=await archive.get(row.archive_key);assert.equal(hash(packed),row.archive_sha256);
  const e=JSON.parse(gunzipSync(packed));assert.equal(e.publicId,row.public_id);assert.equal(e.versionSha256,row.version_sha256);payload=e.payload;
 }
 assert.equal(fingerprint(payload),row.version_sha256);
 return {publicId:row.public_id,versionSha256:row.version_sha256,payload};
}
