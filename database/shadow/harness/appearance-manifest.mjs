// Exact per-run membership: absence and return remain distinct, without daily rows.
import assert from 'node:assert/strict';import {gzipSync,gunzipSync} from 'node:zlib';import {contentHash} from './importer.mjs';
export function encodeAppearances(refs){
 assert.ok(Array.isArray(refs)&&refs.length>0&&refs.length<=60000);
 assert.ok(refs.every(r=>typeof r==='string'&&r.length>0&&r.length<500));
 assert.equal(new Set(refs).size,refs.length,'Duplicate appearance');
 const ids=[...refs].sort();const bytes=gzipSync(Buffer.from(JSON.stringify(ids)),{level:9});
 return {version:1,count:ids.length,sha256:contentHash(ids),codec:'gzip-base64',payload:bytes.toString('base64')};
}
export function decodeAppearances(saved){
 assert.equal(saved.version,1);assert.equal(saved.codec,'gzip-base64');assert.ok(saved.payload.length<=4*1024*1024);
 const ids=JSON.parse(gunzipSync(Buffer.from(saved.payload,'base64'),{maxOutputLength:32*1024*1024}));
 assert.ok(Array.isArray(ids)&&ids.length>0&&ids.length<=60000);assert.equal(ids.length,saved.count);
 assert.ok(ids.every(r=>typeof r==='string'&&r.length>0&&r.length<500));assert.equal(new Set(ids).size,ids.length);
 assert.equal(contentHash(ids),saved.sha256,'Corrupt appearance manifest');return ids;
}
export async function readAppearances(client,runId){
 const run=(await client.query("SELECT supplier_id,feed_date::text,status,diagnostics FROM ontap_shadow.feed_runs WHERE id=$1",[runId])).rows[0];
 assert.equal(run?.status,'accepted');
 if(run.diagnostics.compact_appearances)return {date:run.feed_date,refs:decodeAppearances(run.diagnostics.compact_appearances)};
 const rows=(await client.query('SELECT a.supplier_job_id AS ref FROM ontap_shadow.advert_appearances p JOIN ontap_shadow.supplier_adverts a ON a.id=p.advert_id WHERE p.feed_run_id=$1',[runId])).rows;
 return {date:run.feed_date,refs:rows.map(r=>r.ref).sort()};
}
