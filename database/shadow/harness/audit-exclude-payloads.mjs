import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import pg from 'pg';
import {requirePreview} from './publisher-safeguards.mjs';

requirePreview(process.env);
const request=JSON.parse(await fs.readFile('exclude-payload-audit-request.json','utf8'));
assert.equal(request.mode,'audit','This pass is read-only');
const u=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
u.searchParams.set('sslmode','verify-full');
const c=new pg.Client({connectionString:u.toString(),connectionTimeoutMillis:15000,query_timeout:120000,application_name:'ontap-preview-exclude-payload-audit'});
function canonical(v){
 if(Array.isArray(v))return v.map(canonical);
 if(v&&typeof v==='object')return Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])]));
 return v;
}
function payloadHash(v){return createHash('sha256').update(JSON.stringify(canonical(v))).digest('hex');}
const cte=[
"WITH decisions_by_run AS (",
" SELECT d.advert_id,r.id AS run_id,r.feed_date::text AS decision_feed_date,r.started_at,",
"  count(*) FILTER(WHERE d.scope LIKE 'production:%')::int AS family_rows,",
"  count(*) FILTER(WHERE d.scope LIKE 'production:%' AND d.decision='exclude')::int AS excluded_rows",
" FROM ontap_shadow.selection_decisions d JOIN ontap_shadow.feed_runs r ON r.id=d.feed_run_id",
" WHERE r.status='accepted' AND r.diagnostics ? 'selection_parity' AND d.scope LIKE 'production:%'",
" GROUP BY d.advert_id,r.id,r.feed_date,r.started_at",
"), latest AS (",
" SELECT DISTINCT ON(advert_id) advert_id,run_id,decision_feed_date,family_rows,excluded_rows",
" FROM decisions_by_run ORDER BY advert_id,decision_feed_date DESC,started_at DESC",
"), classified AS (",
" SELECT s.code AS supplier_code,a.id::text AS advert_id,a.supplier_job_id,a.job_id::text AS job_id,",
"  a.content_hash,a.last_seen::text AS last_seen,a.exclude_review_started_on::text AS legacy_marker,a.raw_payload,",
"  COALESCE(j.publication_status,'missing') AS publication_status,l.decision_feed_date,l.family_rows,l.excluded_rows,",
"  CASE",
"   WHEN j.publication_status='published' THEN 'published_protection'",
"   WHEN EXISTS(SELECT 1 FROM ontap_shadow.selected_review_payload_records p WHERE p.public_id=a.supplier_job_id) THEN 'historical_selected_review_protection'",
"   WHEN a.exclude_review_started_on IS NOT NULL AND EXISTS(",
"    SELECT 1 FROM ontap_shadow.selection_decisions d JOIN ontap_shadow.feed_runs r ON r.id=d.feed_run_id",
"    WHERE d.advert_id=a.id AND r.status='accepted' AND r.diagnostics ? 'selection_parity'",
"     AND d.scope LIKE 'production:%' AND d.decision IN ('include','review')",
"     AND r.feed_date>=a.exclude_review_started_on::date",
"   ) THEN 'legacy_marker_contradicted_by_later_positive'",
"   WHEN a.exclude_review_started_on IS NOT NULL THEN 'legacy_exclude_marker_candidate'",
"   WHEN l.advert_id IS NULL THEN 'no_selector_evidence'",
"   WHEN l.family_rows<>8 THEN 'incomplete_selector_decisions'",
"   WHEN l.decision_feed_date<>a.last_seen::text THEN 'decision_not_for_current_payload_date'",
"   WHEN l.excluded_rows<>8 THEN 'not_excluded_in_every_family'",
"   ELSE 'complete_date_matched_exclude_candidate'",
"  END AS classification",
" FROM ontap_shadow.supplier_adverts a",
" JOIN ontap_shadow.suppliers s ON s.id=a.supplier_id",
" LEFT JOIN ontap_shadow.jobs j ON j.id=a.job_id",
" LEFT JOIN latest l ON l.advert_id=a.id",
")"
].join('\n');
try{
 await c.connect();
 await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
 const before=Number((await c.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
 const totals=(await c.query(cte+
  "\nSELECT supplier_code,classification,count(*)::int AS payload_rows,"+
  "coalesce(sum(pg_column_size(raw_payload)),0)::text AS payload_bytes "+
  "FROM classified WHERE raw_payload IS NOT NULL GROUP BY supplier_code,classification ORDER BY supplier_code,classification")).rows;
 const daily=(await c.query(
  "SELECT count(*) FILTER(WHERE decision='EXCLUDE')::int AS exclude_rows,"+
  "count(*) FILTER(WHERE decision='EXCLUDE' AND raw_payload IS NOT NULL)::int AS exclude_payload_rows "+
  "FROM ontap_shadow.selected_review_payload_records")).rows[0];
 const markers=(await c.query(
  "SELECT count(*) FILTER(WHERE a.exclude_review_started_on IS NOT NULL)::int AS marked_adverts,"+
  "count(*) FILTER(WHERE a.exclude_review_started_on IS NOT NULL AND a.raw_payload IS NOT NULL)::int AS marked_payload_rows,"+
  "coalesce(sum(pg_column_size(a.raw_payload)) FILTER(WHERE a.exclude_review_started_on IS NOT NULL AND a.raw_payload IS NOT NULL),0)::text AS marked_payload_bytes,"+
  "count(*) FILTER(WHERE a.exclude_review_started_on IS NOT NULL AND a.raw_payload IS NOT NULL AND EXISTS(SELECT 1 FROM ontap_shadow.selected_review_payload_records p WHERE p.public_id=a.supplier_job_id))::int AS marked_historical_selected_review_rows,"+
  "count(*) FILTER(WHERE a.exclude_review_started_on IS NOT NULL AND a.raw_payload IS NOT NULL AND j.publication_status='published')::int AS marked_published_rows,"+
  "min(a.exclude_review_started_on)::text AS oldest_marker,max(a.exclude_review_started_on)::text AS newest_marker "+
  "FROM ontap_shadow.supplier_adverts a LEFT JOIN ontap_shadow.jobs j ON j.id=a.job_id")).rows[0];
 const candidateRows=(await c.query(cte+
  "\nSELECT advert_id,supplier_job_id,job_id,content_hash,raw_payload,classification "+
  "FROM classified WHERE classification IN ('legacy_exclude_marker_candidate','complete_date_matched_exclude_candidate') "+
  "AND raw_payload IS NOT NULL ORDER BY supplier_job_id")).rows;
 let hashMatches=0,hashMismatches=0,hashBytes=0;
 const candidateSamples=[];
 const validCandidates=[];
 for(const r of candidateRows){
  hashBytes+=Buffer.byteLength(JSON.stringify(canonical(r.raw_payload)));
  if(payloadHash(r.raw_payload)===r.content_hash){
   hashMatches++;
   validCandidates.push({publicId:r.supplier_job_id,advertId:r.advert_id,jobId:r.job_id,evidence:r.classification});
   if(candidateSamples.length<25)candidateSamples.push(r.supplier_job_id);
  }else hashMismatches++;
 }
 const report={
  status:'passed',mode:'read_only_audit',selectorFamilyCountRequired:8,databaseBytes:before,
  masterPayloadBreakdown:totals.map(r=>({supplier:r.supplier_code,classification:r.classification,rows:r.payload_rows,storedBytes:Number(r.payload_bytes)})),
  confirmedExcludePayloadCandidates:hashMatches,excludedPayloadHashMismatches:hashMismatches,candidateJsonBytes:hashBytes,
  excludedPayloadIdsSample:candidateSamples,
  dailySelectedReviewExcludeRows:Number(daily.exclude_rows),dailySelectedReviewExcludePayloadRows:Number(daily.exclude_payload_rows),
  legacyExcludeReviewMarkers:Number(markers.marked_adverts),legacyMarkerPayloadRows:Number(markers.marked_payload_rows),
  legacyMarkerPayloadBytes:Number(markers.marked_payload_bytes),legacyMarkerHistoricalSelectedReviewRows:Number(markers.marked_historical_selected_review_rows),
  legacyMarkerPublishedRows:Number(markers.marked_published_rows),oldestLegacyMarker:markers.oldest_marker,newestLegacyMarker:markers.newest_marker,
  productionChanged:false,dataChanged:false,readOnly:true
 };
 await c.query('COMMIT');
 await fs.mkdir('dist',{recursive:true});
 await fs.writeFile('dist/exclude-payload-audit-report.json',JSON.stringify(report,null,2)+'\n');
 await fs.writeFile('dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><h1>Read-only exclude payload audit</h1>');
 console.log('ONTAP_EXCLUDE_PAYLOAD_AUDIT '+JSON.stringify(report));
}catch(e){try{await c.query('ROLLBACK');}catch{};throw e;}
finally{await c.end();}
