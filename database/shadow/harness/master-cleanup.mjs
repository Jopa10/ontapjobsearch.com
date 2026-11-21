// Actual ontap_shadow master-table cleanup. Caller owns a transaction.
// Preview-only until a production cutover is separately approved.
import assert from 'node:assert/strict';
import {gzipSync,gunzipSync} from 'node:zlib';
import {requirePreview,hash} from './publisher-safeguards.mjs';
import {readCurrentPublication} from './current-publication.mjs';
export const canonical=v=>Array.isArray(v)?v.map(canonical):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):v;
export const payloadHash=v=>hash(JSON.stringify(canonical(v)));
export function dayOffset(day,n){const d=new Date(day+'T00:00:00Z');d.setUTCDate(d.getUTCDate()+n);return d.toISOString().slice(0,10);}
function validDay(day){assert.match(day,/^\d{4}-\d{2}-\d{2}$/);assert.equal(dayOffset(day,0),day);}
export function makeMasterArchive(row){
 assert.ok(row.raw_payload);
 const packet={schemaVersion:1,advertId:row.advert_id,jobId:row.job_id,publicId:row.public_id,contentHash:row.content_hash,payloadSha256:payloadHash(row.raw_payload),payload:row.raw_payload};
 const bytes=gzipSync(Buffer.from(JSON.stringify(canonical(packet))),{level:9});
 const digest=hash(bytes);
 return {bytes,receipt:{schemaVersion:1,key:'ontap-shadow/advert-versions/'+row.advert_id+'/'+row.content_hash+'/'+digest+'.json.gz',sha256:digest,bytes:bytes.length,payloadSha256:packet.payloadSha256,advertId:row.advert_id,jobId:row.job_id,contentHash:row.content_hash}};
}
export function verifyMasterArchive(bytes,receipt){
 assert.equal(bytes.length,receipt.bytes);assert.equal(hash(bytes),receipt.sha256,'Archive checksum mismatch');
 const packet=JSON.parse(gunzipSync(bytes,{maxOutputLength:32*1024*1024}));
 assert.equal(packet.schemaVersion,1);assert.equal(packet.advertId,receipt.advertId);assert.equal(packet.jobId,receipt.jobId);assert.equal(packet.contentHash,receipt.contentHash);
 assert.equal(packet.payloadSha256,receipt.payloadSha256);assert.equal(payloadHash(packet.payload),receipt.payloadSha256);
 return packet;
}
export async function registerMasterVersion(c,row){
 const digest=payloadHash(row.raw_payload);
 await c.query('INSERT INTO ontap_shadow.advert_payload_versions(advert_id,job_id,content_hash,payload_sha256) VALUES($1,$2,$3,$4) ON CONFLICT DO NOTHING',[row.advert_id,row.job_id,row.content_hash,digest]);
 const got=(await c.query('SELECT * FROM ontap_shadow.advert_payload_versions WHERE advert_id=$1 AND content_hash=$2',[row.advert_id,row.content_hash])).rows[0];
 assert.equal(got.job_id,row.job_id);assert.equal(got.payload_sha256,digest,'Same version hash used for changed content');
 return got;
}
export async function archiveMasterVersion(c,row,store){
 const made=makeMasterArchive(row);
 const delivery=await store.putIfAbsent(made.receipt.key,made.bytes);
 assert.ok(delivery.durable===true,'Archive store has not confirmed durable delivery');
 const receipt={...made.receipt,store:delivery};
 verifyMasterArchive(await store.get(receipt.key),receipt);
 await registerMasterVersion(c,row);
 await c.query('UPDATE ontap_shadow.advert_payload_versions SET archive_receipt=$3::jsonb,archived_at=now() WHERE advert_id=$1 AND content_hash=$2',[row.advert_id,row.content_hash,JSON.stringify(receipt)]);
 return receipt;
}
export async function cleanupMasterPayloads(c,{asOfDate=new Date().toISOString().slice(0,10),mode='dry-run',store=null,testRunId=null}={}){
 requirePreview(process.env);validDay(asOfDate);assert.ok(['dry-run','apply'].includes(mode));
 await c.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
 await c.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:selected-review-full-payload'))");
 const currentPublication=await readCurrentPublication(c);const activeIds=currentPublication.records.map(r=>r.public_id);
 const params=[asOfDate,activeIds];
 let filter='';
 if(testRunId){assert.match(testRunId,/^[a-z0-9-]{1,100}$/);params.push(testRunId);filter=" AND a.match_evidence->>'cleanup_test_run'=$3";}
 const candidates=(await c.query("SELECT a.id AS advert_id,a.job_id,a.supplier_job_id,a.content_hash,a.raw_payload,a.inactive_since::text,a.availability,a.match_evidence,j.public_id,j.publication_status,(SELECT max(aa.seen_on) FROM ontap_shadow.advert_appearances aa WHERE aa.advert_id=a.id)::text AS last_selected_on FROM ontap_shadow.supplier_adverts a JOIN ontap_shadow.jobs j ON j.id=a.job_id JOIN ontap_shadow.suppliers s ON s.id=a.supplier_id WHERE s.code='jobg8' AND a.raw_payload IS NOT NULL AND (SELECT max(aa.seen_on) FROM ontap_shadow.advert_appearances aa WHERE aa.advert_id=a.id) IS NOT NULL AND (SELECT max(aa.seen_on) FROM ontap_shadow.advert_appearances aa WHERE aa.advert_id=a.id) <= $1::date - 30 AND j.publication_status <> 'published' AND NOT (a.supplier_job_id=ANY($2::text[]) OR j.public_id=ANY($2::text[]))"+filter+" ORDER BY a.id FOR UPDATE OF a,j",params)).rows;
 const result={mode,asOfDate,retentionDays:30,appearanceMetadataRetention:'No expiry configured; appearance rows are retained.',candidateIds:candidates.map(r=>r.supplier_job_id),candidateCount:candidates.length,purgedCount:0,purgedIds:[],preservedIdentities:true,productionChanged:false};
 if(mode==='dry-run')return result;
 assert.ok(store,'Verified durable archive store is required before cleanup');
 // Verify every candidate archive first, so a bad/missing archive blocks the whole batch.
 const receipts=[];
 for(const row of candidates){
  if(store.provider==='github-actions-test'){
   assert.ok(testRunId&&row.match_evidence.cleanup_test_run===testRunId,'Test archive may only purge marked test adverts');
  }else assert.equal(store.provider,'s3-immutable','Unapproved durable archive backend');
  const receipt=await archiveMasterVersion(c,row,store);
  assert.equal(receipt.payloadSha256,payloadHash(row.raw_payload));
  receipts.push(receipt);
 }
 for(const [i,row]of candidates.entries()){
  const receipt=receipts[i];
  // Revalidate the externally stored bytes immediately before clearing hot payload.
  verifyMasterArchive(await store.get(receipt.key),receipt);
  const updated=await c.query("UPDATE ontap_shadow.supplier_adverts SET raw_payload=NULL,content_purged_at=now(),availability='expired' WHERE id=$1 AND content_hash=$2 AND raw_payload IS NOT NULL AND (SELECT max(aa.seen_on) FROM ontap_shadow.advert_appearances aa WHERE aa.advert_id=$1)=$3::date AND $4::date >= $3::date + 30 RETURNING id",[row.advert_id,row.content_hash,row.last_selected_on,asOfDate]);
  assert.equal(updated.rowCount,1,'Advert changed during cleanup');
  const links=(await c.query('SELECT job_id FROM ontap_shadow.supplier_adverts WHERE id=$1',[row.advert_id])).rows[0];
  assert.equal(links.job_id,row.job_id);
  result.purgedIds.push(row.supplier_job_id);
 }
 result.purgedCount=result.purgedIds.length;return result;
}
export async function recoverMasterClick(c,eventId,store){
 const event=(await c.query('SELECT advert_id,advert_content_hash FROM ontap_shadow.activity_events WHERE id=$1',[eventId])).rows[0];
 assert.ok(event?.advert_id&&event.advert_content_hash,'Missing exact clicked version reference');
 const version=(await c.query('SELECT archive_receipt FROM ontap_shadow.advert_payload_versions WHERE advert_id=$1 AND content_hash=$2',[event.advert_id,event.advert_content_hash])).rows[0];
 assert.ok(version?.archive_receipt,'Clicked version archive missing');
 return verifyMasterArchive(await store.get(version.archive_receipt.key),version.archive_receipt);
}
export async function runMasterCleanup(c,options={}){
 await c.query('BEGIN');
 try{const result=await cleanupMasterPayloads(c,options);await c.query('COMMIT');return result;}
 catch(e){await c.query('ROLLBACK');throw e;}
}
