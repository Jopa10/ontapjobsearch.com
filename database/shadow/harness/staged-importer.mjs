import { stableId, contentHash } from './importer.mjs';

export const DEFAULT_BUDGET = 800 * 1024 * 1024;
export function budgetGate(beforeBytes, payloadBytes, recordCount, maximumBytes=DEFAULT_BUDGET) {
  if (![beforeBytes,payloadBytes,recordCount].every(n=>Number.isFinite(n) && n>=0)) throw new Error('Invalid storage estimate');
  if (!Number.isFinite(maximumBytes) || maximumBytes > DEFAULT_BUDGET || maximumBytes <= 0) throw new Error('Invalid storage ceiling');
  const conservativeExtra = Math.ceil(payloadBytes * 2.5 + recordCount * 2048);
  if (beforeBytes + conservativeExtra > maximumBytes) throw new Error('Storage preflight exceeds test ceiling');
  return {beforeBytes,conservativeExtra,maximumBytes};
}
function number(value) {
  if (value === '' || value == null) return null;
  const n=Number(value);
  return Number.isFinite(n) ? n : null;
}
function normalize(raw) {
  const ref=raw['/Job/DisplayReference'];
  const title=raw['/Job/Position'];
  if (typeof ref!=='string' || !ref.trim() || typeof title!=='string' || !title.trim()) throw new Error('Invalid raw identity');
  const url=new URL(raw['/Job/ApplicationURL']);
  if (!['https:','http:'].includes(url.protocol)) throw new Error('Invalid apply URL');
  return {initial_id:stableId(`job:jobg8:${ref}`),advert_id:stableId(`advert:jobg8:${ref}`),ref,title,
    advertiser:raw['/Job/AdvertiserName'] || null,location:raw['/Job/Location'] || null,
    apply_url:raw['/Job/ApplicationURL'],salary_min:number(raw['/Job/SalaryMinimum']),
    salary_max:number(raw['/Job/SalaryMaximum']),salary_period:raw['/Job/SalaryPeriod'] || null,
    // Keep the raw pay fields and description. Do not invent parsed pay or rerun policy.
    salary_text:raw['/Job/SalaryAdditional'] || null,raw_payload:raw,content_hash:contentHash(raw)};
}
export async function measure(client) {
  const db=Number((await client.query('SELECT pg_database_size(current_database())::text AS n')).rows[0].n);
  const tables=(await client.query(`SELECT c.relname AS name,pg_total_relation_size(c.oid)::text AS bytes
    FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ontap_shadow' AND c.relkind='r' ORDER BY c.relname`)).rows;
  return {databaseBytes:db,schemaBytes:tables.reduce((n,r)=>n+Number(r.bytes),0),tables};
}
const definition=`initial_id uuid,advert_id uuid,ref text,title text,advertiser text,location text,apply_url text,salary_min numeric,salary_max numeric,salary_period text,salary_text text,raw_payload jsonb,content_hash text`;
const input=`jsonb_to_recordset($1::jsonb) AS r(${definition})`;

export async function importStage(client,fixture,{chunkSize=300,compactSelection=false}={}) {
  const {records,observedOn,percentage,archiveSha256,sourceRevision,totalReceived}=fixture;
  if (![20,50,100].includes(percentage) || !Array.isArray(records) || !records.length || records.length>60000 || totalReceived<records.length || totalReceived>60000) throw new Error('Invalid bounded stage');
  if (records.length!==Math.max(1,Math.floor((fixture.eligibleRecords || totalReceived)*percentage/100))) throw new Error('Stage fraction mismatch');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(observedOn) || !/^[a-f0-9]{64}$/.test(archiveSha256)) throw new Error('Missing archive provenance');
  if(compactSelection && percentage!==100) throw new Error('Compact selection requires a full snapshot');
  const normalized=records.map(normalize);
  if (new Set(normalized.map(r=>r.ref)).size!==records.length) throw new Error('Duplicate IDs');
  const sourceHash=contentHash(records);
  const feedKey=`raw-stage:${archiveSha256}:${percentage}`;
  const runId=stableId(`run:jobg8:${feedKey}`);
  const measured=await measure(client);
  budgetGate(measured.databaseBytes,fixture.rawPayloadBytes,records.length,fixture.maximumDatabaseBytes);
  const started=Date.now();
  await client.query('BEGIN');
  try {
    await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
    const supplier=(await client.query(`INSERT INTO ontap_shadow.suppliers(code,name) VALUES('jobg8','JobG8') ON CONFLICT(code) DO UPDATE SET name=EXCLUDED.name RETURNING id`)).rows[0].id;
    const previous=(await client.query('SELECT status,source_checksum,diagnostics FROM ontap_shadow.feed_runs WHERE supplier_id=$1 AND feed_key=$2',[supplier,feedKey])).rows[0];
    if (previous) {
      if (previous.status!=='accepted' || previous.source_checksum!==sourceHash) throw new Error('Conflicting stage replay');
      if(Boolean(previous.diagnostics?.selection_representation?.startsWith('compact'))!==compactSelection) throw new Error('Conflicting selection storage mode');
      await client.query('COMMIT');
      return {replayed:true,imported:records.length,elapsedMs:Date.now()-started};
    }
    await client.query(`INSERT INTO ontap_shadow.feed_runs(id,supplier_id,feed_key,feed_date,source_checksum,status,received_count,rules_revision,diagnostics)
      VALUES($1,$2,$3,$4,$5,'staged',$6,$7,$8)`,[runId,supplier,feedKey,observedOn,sourceHash,totalReceived,sourceRevision,
      {archive_sha256:archiveSha256,percentage,imported_records:records.length,partial_feed:percentage<100,expiry_enabled:false,receipt_diagnostics:fixture.receiptDiagnostics || null,...(compactSelection?{selection_representation:'compact_pending',selection_status:'pending'}:{})}]);
    for (let offset=0;offset<normalized.length;offset+=chunkSize) {
      const chunk=JSON.stringify(normalized.slice(offset,offset+chunkSize));
      const args=[chunk,supplier,observedOn];
      await client.query(`INSERT INTO ontap_shadow.jobs(id,public_id,title,employer,location,salary_min,salary_max,salary_period,salary_text,first_seen,last_seen,publication_status)
        SELECT COALESCE(a.job_id,r.initial_id),r.ref,r.title,r.advertiser,r.location,r.salary_min,r.salary_max,r.salary_period,r.salary_text,$3::date,$3::date,'withheld'
        FROM ${input} LEFT JOIN ontap_shadow.supplier_adverts a ON a.supplier_id=$2 AND a.supplier_job_id=r.ref
        ON CONFLICT(id) DO NOTHING`,args);
      await client.query(`INSERT INTO ontap_shadow.supplier_adverts(id,supplier_id,supplier_job_id,job_id,title,advertiser_name,location,apply_url,raw_payload,content_hash,first_seen,last_seen)
        SELECT COALESCE(a.id,r.advert_id),$2,r.ref,COALESCE(a.job_id,r.initial_id),r.title,r.advertiser,r.location,r.apply_url,r.raw_payload,r.content_hash,$3::date,$3::date
        FROM ${input} LEFT JOIN ontap_shadow.supplier_adverts a ON a.supplier_id=$2 AND a.supplier_job_id=r.ref
        ON CONFLICT(supplier_id,supplier_job_id) DO UPDATE SET
          title=CASE WHEN EXCLUDED.last_seen>=supplier_adverts.last_seen THEN EXCLUDED.title ELSE supplier_adverts.title END,
          advertiser_name=CASE WHEN EXCLUDED.last_seen>=supplier_adverts.last_seen THEN EXCLUDED.advertiser_name ELSE supplier_adverts.advertiser_name END,
          location=CASE WHEN EXCLUDED.last_seen>=supplier_adverts.last_seen THEN EXCLUDED.location ELSE supplier_adverts.location END,
          apply_url=CASE WHEN EXCLUDED.last_seen>=supplier_adverts.last_seen THEN EXCLUDED.apply_url ELSE supplier_adverts.apply_url END,
          raw_payload=CASE WHEN EXCLUDED.last_seen>=supplier_adverts.last_seen AND (supplier_adverts.content_hash IS DISTINCT FROM EXCLUDED.content_hash OR supplier_adverts.raw_payload IS NULL) THEN EXCLUDED.raw_payload ELSE supplier_adverts.raw_payload END,
          content_hash=CASE WHEN EXCLUDED.last_seen>=supplier_adverts.last_seen THEN EXCLUDED.content_hash ELSE supplier_adverts.content_hash END,
          first_seen=LEAST(supplier_adverts.first_seen,EXCLUDED.first_seen),last_seen=GREATEST(supplier_adverts.last_seen,EXCLUDED.last_seen),
          inactive_since=CASE WHEN EXCLUDED.last_seen>=supplier_adverts.last_seen THEN NULL ELSE supplier_adverts.inactive_since END,
          availability=CASE WHEN EXCLUDED.last_seen>=supplier_adverts.last_seen THEN 'seen' ELSE supplier_adverts.availability END`,args);
      await client.query(`UPDATE ontap_shadow.jobs j SET first_seen=LEAST(j.first_seen,$3::date),last_seen=GREATEST(j.last_seen,$3::date),
        title=CASE WHEN $3::date>=j.last_seen AND (j.preferred_advert_id IS NULL OR j.preferred_advert_id=a.id) THEN r.title ELSE j.title END,
        employer=CASE WHEN $3::date>=j.last_seen AND (j.preferred_advert_id IS NULL OR j.preferred_advert_id=a.id) THEN r.advertiser ELSE j.employer END,
        location=CASE WHEN $3::date>=j.last_seen AND (j.preferred_advert_id IS NULL OR j.preferred_advert_id=a.id) THEN r.location ELSE j.location END,
        preferred_advert_id=COALESCE(j.preferred_advert_id,a.id)
        FROM ${input} JOIN ontap_shadow.supplier_adverts a ON a.supplier_id=$2 AND a.supplier_job_id=r.ref WHERE j.id=a.job_id`,args);
      await client.query(`INSERT INTO ontap_shadow.advert_appearances(advert_id,seen_on,supplier_id,feed_run_id)
        SELECT a.id,$3::date,$2,$4 FROM ${input} JOIN ontap_shadow.supplier_adverts a ON a.supplier_id=$2 AND a.supplier_job_id=r.ref
        ON CONFLICT(advert_id,seen_on) DO UPDATE SET feed_run_id=EXCLUDED.feed_run_id`,[...args,runId]);
      if(!compactSelection) await client.query(`INSERT INTO ontap_shadow.selection_decisions(id,advert_id,feed_run_id,scope,decision,reason,rules_revision,evidence)
        SELECT (md5($4::text || ':' || a.id::text))::uuid,a.id,$4::uuid,'raw_feed_pending_selection','unknown',
        'Raw advert retained; same-snapshot production selector evidence has not been attached.',$5,
        jsonb_build_object('archive_sha256',$6::text,'observed_on',$3::text,'stage_percentage',$7::int)
        FROM ${input} JOIN ontap_shadow.supplier_adverts a ON a.supplier_id=$2 AND a.supplier_job_id=r.ref`,[...args,runId,sourceRevision,archiveSha256,percentage]);
    }
    await client.query("UPDATE ontap_shadow.feed_runs SET status='accepted',completed_at=now() WHERE id=$1",[runId]);
    await client.query('COMMIT');
    return {replayed:false,imported:records.length,elapsedMs:Date.now()-started};
  } catch(error) {
    await client.query('ROLLBACK');
    throw error;
  }
}
