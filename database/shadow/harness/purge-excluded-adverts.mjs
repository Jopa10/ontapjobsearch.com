import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import pg from 'pg';
import {requirePreview} from './publisher-safeguards.mjs';

requirePreview(process.env);
const request=JSON.parse(await fs.readFile('exclude-payload-purge-request.json','utf8'));
assert.equal(request.mode,'purge','This workflow only clears reviewed exclude payloads');
assert.equal(request.allowPayloadRemoval,true,'Explicit payload-removal flag required');
const MAX_DB=800*1024*1024, RESERVE=64*1024*1024, BATCH=250;
const u=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
u.searchParams.set('sslmode','verify-full');
const c=new pg.Client({connectionString:u.toString(),connectionTimeoutMillis:15000,query_timeout:120000,application_name:'ontap-preview-exclude-payload-purge'});
function canonical(v){
 if(Array.isArray(v))return v.map(canonical);
 if(v&&typeof v==='object')return Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])]));
 return v;
}
function payloadHash(v){return createHash('sha256').update(JSON.stringify(canonical(v))).digest('hex');}

// Classification is deliberately the same strict rule as the successful audit:
// preserve published adverts, all saved SELECTED/REVIEW history, and any advert
// with a later positive decision; accept only legacy exclude markers or a
// current, date-matched, all-eight-family EXCLUDE decision.
const cte=`WITH decision_rows AS MATERIALIZED (
 SELECT d.advert_id,r.id AS run_id,r.feed_date::date AS decision_feed_date,r.started_at,d.scope,d.decision
 FROM ontap_shadow.selection_decisions d
 JOIN ontap_shadow.feed_runs r ON r.id=d.feed_run_id
 WHERE r.status='accepted' AND r.diagnostics ? 'selection_parity'
   AND d.scope LIKE 'production:%'
), decisions_by_run AS MATERIALIZED (
 SELECT advert_id,run_id,decision_feed_date,started_at,count(*)::int AS family_rows,
  count(*) FILTER(WHERE decision='exclude')::int AS excluded_rows
 FROM decision_rows GROUP BY advert_id,run_id,decision_feed_date,started_at
), latest AS MATERIALIZED (
 SELECT DISTINCT ON(advert_id) advert_id,decision_feed_date,family_rows,excluded_rows
 FROM decisions_by_run ORDER BY advert_id,decision_feed_date DESC,started_at DESC
), later_positive AS MATERIALIZED (
 SELECT advert_id,max(decision_feed_date) AS latest_positive_date
 FROM decision_rows WHERE decision IN ('include','review') GROUP BY advert_id
), historical_ids AS MATERIALIZED (
 SELECT public_id FROM ontap_shadow.selected_review_payload_records GROUP BY public_id
), classified AS (
 SELECT a.id AS advert_uuid,a.supplier_job_id,a.content_hash,a.raw_payload,
  a.exclude_review_started_on,h.public_id IS NOT NULL AS has_selected_review_history,
  COALESCE(j.publication_status,'missing') AS publication_status,
  lp.latest_positive_date,l.advert_id AS latest_decision_advert,l.decision_feed_date,l.family_rows,l.excluded_rows,
  CASE
   WHEN j.publication_status='published' THEN 'protected'
   WHEN h.public_id IS NOT NULL THEN 'protected'
   WHEN a.exclude_review_started_on IS NOT NULL AND lp.latest_positive_date>=a.exclude_review_started_on::date THEN 'protected'
   WHEN a.exclude_review_started_on IS NOT NULL THEN 'legacy_exclude_marker_candidate'
   WHEN l.advert_id IS NULL OR l.family_rows<>8 OR l.decision_feed_date<>a.last_seen::date OR l.excluded_rows<>8 THEN 'protected'
   ELSE 'complete_date_matched_exclude_candidate'
  END AS classification,
  s.code AS supplier_code
 FROM ontap_shadow.supplier_adverts a
 JOIN ontap_shadow.suppliers s ON s.id=a.supplier_id
 LEFT JOIN ontap_shadow.jobs j ON j.id=a.job_id
 LEFT JOIN latest l ON l.advert_id=a.id
 LEFT JOIN historical_ids h ON h.public_id=a.supplier_job_id
 LEFT JOIN later_positive lp ON lp.advert_id=a.id
)`;
try{
 await c.connect();
 const initialBytes=Number((await c.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
 assert.ok(initialBytes+RESERVE<=MAX_DB,'Database is already above the 800 MiB ceiling with 64 MiB reserve');
 let clearedRows=0,clearedPayloadBytes=0,hashMismatches=0,skippedIds=[];
 let stoppedByStorageGuard=false,guardDatabaseBytes=0;
 await c.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
 const candidates=(await c.query(cte+`
  SELECT x.advert_uuid::text AS advert_id,x.supplier_job_id,x.content_hash,x.raw_payload,
    pg_column_size(x.raw_payload)::text AS stored_bytes
  FROM classified x
  JOIN ontap_shadow.supplier_adverts a ON a.id=x.advert_uuid
  WHERE x.supplier_code='jobg8' AND x.raw_payload IS NOT NULL
    AND x.classification IN ('legacy_exclude_marker_candidate','complete_date_matched_exclude_candidate')
  ORDER BY x.supplier_job_id
  FOR UPDATE OF a
 `)).rows;
 const valid=[];
 for(const row of candidates){
  if(payloadHash(row.raw_payload)===row.content_hash){
   valid.push({id:row.advert_id,content_hash:row.content_hash});
   clearedPayloadBytes+=Number(row.stored_bytes);
  }else{
   hashMismatches++;skippedIds.push(row.supplier_job_id);
  }
 }
 assert.equal(hashMismatches,0,'Payload hash mismatch; no rows were changed');
 const conservativeGrowth=Math.max(16*1024*1024,valid.length*2048);
 if(initialBytes+RESERVE+conservativeGrowth>MAX_DB){
  await c.query('ROLLBACK');
  stoppedByStorageGuard=true;guardDatabaseBytes=initialBytes;
 }else{
  for(let i=0;i<valid.length;i+=1000){
   const chunk=valid.slice(i,i+1000);
   const changed=(await c.query(`UPDATE ontap_shadow.supplier_adverts a
    SET raw_payload=NULL,content_purged_at=now()
    FROM jsonb_to_recordset($1::jsonb) AS x(id uuid,content_hash text)
    WHERE a.id=x.id AND a.content_hash=x.content_hash AND a.raw_payload IS NOT NULL
    RETURNING a.id`,[JSON.stringify(chunk)])).rows;
   assert.equal(changed.length,chunk.length,'Candidate set changed; transaction rolled back');
   clearedRows+=changed.length;
   const liveBytes=Number((await c.query("SELECT pg_database_size(current_database())::text AS bytes")).rows[0].bytes);
   if(liveBytes+RESERVE>MAX_DB){
    await c.query('ROLLBACK');
    clearedRows=0;clearedPayloadBytes=0;
    stoppedByStorageGuard=true;guardDatabaseBytes=initialBytes;
    break;
   }
  }
  if(!stoppedByStorageGuard) await c.query('COMMIT');
 }
 const finalBytes=Number((await c.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
 assert.ok(finalBytes+RESERVE<=MAX_DB,'Final database size would breach the 64 MiB reserve');
 const remaining=(await c.query(cte+`
  SELECT count(*)::int AS rows
  FROM classified
  WHERE supplier_code='jobg8' AND raw_payload IS NOT NULL
    AND classification IN ('legacy_exclude_marker_candidate','complete_date_matched_exclude_candidate')
 `)).rows[0].rows;
 const report={status:stoppedByStorageGuard?'stopped_at_storage_guard':'completed',mode:'preview_payload_cleanup',
  clearedRows,estimatedPayloadBytesCleared:clearedPayloadBytes,hashMismatches,hashMismatchIds:skippedIds.slice(0,25),
  remainingConfirmedCandidates:Number(remaining),databaseBytesBeforeCleanup:initialBytes,databaseBytesAfterCleanup:finalBytes,
  storageCeilingBytes:MAX_DB,reserveBytes:RESERVE,stoppedAtDatabaseBytes:guardDatabaseBytes||null,
  productionChanged:false,decisionAndIdentityRowsDeleted:0};
 await fs.mkdir('dist',{recursive:true});
 await fs.writeFile('dist/exclude-payload-purge-report.json',JSON.stringify(report,null,2)+'\n');
 await fs.writeFile('dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><h1>Preview exclude payload cleanup</h1>');
 console.log('ONTAP_EXCLUDE_PAYLOAD_PURGE '+JSON.stringify(report));
 assert.equal(hashMismatches,0,'Hash mismatch found; review the report before continuing');
}catch(e){try{await c.query('ROLLBACK');}catch{};throw e;}
finally{await c.end();}
