import { createHash } from 'node:crypto';

const namespace = Buffer.from('d4b3e1f356424af8b5e7ce3948758134', 'hex');
export function stableId(key) {
  const bytes = createHash('sha1').update(namespace).update(key).digest().subarray(0, 16);
  bytes[6] = (bytes[6] & 15) | 80;
  bytes[8] = (bytes[8] & 63) | 128;
  const hex = bytes.toString('hex');
  return `${hex.slice(0,8)}-${hex.slice(8,12)}-${hex.slice(12,16)}-${hex.slice(16,20)}-${hex.slice(20)}`;
}
function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === 'object') return Object.fromEntries(Object.keys(value).sort().map(k => [k, canonical(value[k])]));
  return value;
}
export function contentHash(value) {
  return createHash('sha256').update(JSON.stringify(canonical(value))).digest('hex');
}
function validate(input) {
  const {records, observedOn, feedKey, sourceRevision} = input;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(observedOn) || new Date(`${observedOn}T00:00:00Z`).toISOString().slice(0,10) !== observedOn) throw new Error('Invalid observation date');
  if (!Array.isArray(records) || records.length < 1 || records.length > 20) throw new Error('Sample requires 1–20 adverts');
  if (!feedKey || !sourceRevision) throw new Error('Missing snapshot provenance');
  const seen = new Set();
  for (const r of records) {
    if (String(r.source).trim().toLowerCase() !== 'jobg8' || typeof r.job_id !== 'string' || !r.job_id.trim() || !r.title?.trim()) throw new Error('Invalid JobG8 identity');
    if (seen.has(r.job_id)) throw new Error('Duplicate supplier ID');
    seen.add(r.job_id);
    const url = new URL(r.apply_url);
    if (!['https:', 'http:'].includes(url.protocol)) throw new Error('Invalid apply URL');
  }
}
function numeric(value) {
  if (value === '' || value == null) return null;
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}

// Caller owns a transaction. This sample path never infers missing/expired jobs.
export async function importBatch(client, input) {
  validate(input);
  const {records, observedOn, feedKey, sourceRevision} = input;
  await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
  const checksum = contentHash({records, observedOn, sourceRevision});
  const supplier = (await client.query(`INSERT INTO ontap_shadow.suppliers(code,name)
    VALUES ('jobg8','JobG8') ON CONFLICT(code) DO UPDATE SET name=EXCLUDED.name RETURNING id`)).rows[0].id;
  const previous = (await client.query(`SELECT id, source_checksum, status FROM ontap_shadow.feed_runs WHERE supplier_id=$1 AND feed_key=$2`,[supplier,feedKey])).rows[0];
  if (previous) {
    if (previous.source_checksum !== checksum || previous.status !== 'accepted') throw new Error('Feed identity already used for different content or incomplete import');
    return {replayed:true,received:records.length};
  }
  const latest = (await client.query(`SELECT max(last_seen)::text AS last_seen FROM ontap_shadow.supplier_adverts WHERE supplier_id=$1`,[supplier])).rows[0].last_seen;
  if (latest && observedOn < latest) throw new Error('Older snapshot refused');
  const runId = stableId(`run:jobg8:${feedKey}`);
  await client.query(`INSERT INTO ontap_shadow.feed_runs(id,supplier_id,feed_key,feed_date,source_checksum,status,received_count,rules_revision,diagnostics)
    VALUES($1,$2,$3,$4,$5,'staged',$6,$7,$8)`,[runId,supplier,feedKey,observedOn,checksum,records.length,sourceRevision,
    {sample_only:true,full_feed:false,provenance:input.provenance || 'published inventory sample'}]);
  for (const r of records) {
    const advertId = stableId(`advert:jobg8:${r.job_id}`);
    const existing = (await client.query(`SELECT id,job_id FROM ontap_shadow.supplier_adverts WHERE supplier_id=$1 AND supplier_job_id=$2 FOR UPDATE`,[supplier,r.job_id])).rows[0];
    // Preserve any existing reconciled advert -> job link, not just the initial UUID.
    const jobId = existing?.job_id || stableId(`job:jobg8:${r.job_id}`);
    const currentAdvertId = existing?.id || advertId;
    await client.query(`INSERT INTO ontap_shadow.jobs(id,public_id,title,employer,location,region,role_family,salary_min,salary_max,salary_period,salary_text,first_seen,last_seen,publication_status)
      VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$12,'withheld') ON CONFLICT(id) DO NOTHING`,
      [jobId,r.job_id,r.title,r.company || r.advertiser_name || null,r.location || null,r.region || null,r.category || null,numeric(r.salary_min),numeric(r.salary_max),r.salary_period || null,r.salary_text || null,observedOn]);
    await client.query(`INSERT INTO ontap_shadow.supplier_adverts(id,supplier_id,supplier_job_id,job_id,title,advertiser_name,location,apply_url,raw_payload,content_hash,first_seen,last_seen)
      VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$11)
      ON CONFLICT(supplier_id,supplier_job_id) DO UPDATE SET
        title=EXCLUDED.title,advertiser_name=EXCLUDED.advertiser_name,location=EXCLUDED.location,
        apply_url=EXCLUDED.apply_url,
        raw_payload=CASE WHEN supplier_adverts.content_hash IS DISTINCT FROM EXCLUDED.content_hash OR supplier_adverts.raw_payload IS NULL THEN EXCLUDED.raw_payload ELSE supplier_adverts.raw_payload END,
        content_hash=EXCLUDED.content_hash,last_seen=GREATEST(supplier_adverts.last_seen,EXCLUDED.last_seen),
        exclude_review_started_on=CASE WHEN supplier_adverts.content_hash IS DISTINCT FROM EXCLUDED.content_hash THEN NULL ELSE supplier_adverts.exclude_review_started_on END,
        content_purged_at=CASE WHEN supplier_adverts.content_hash IS DISTINCT FROM EXCLUDED.content_hash OR supplier_adverts.raw_payload IS NULL THEN NULL ELSE supplier_adverts.content_purged_at END,
        inactive_since=NULL,availability='seen'`,
      [currentAdvertId,supplier,r.job_id,jobId,r.title,r.advertiser_name || r.company || null,r.location || null,r.apply_url,r,contentHash(r),observedOn]);
    await client.query(`UPDATE ontap_shadow.jobs SET first_seen=LEAST(first_seen,$2::date),last_seen=GREATEST(last_seen,$2::date),inactive_since=NULL WHERE id=$1`,[jobId,observedOn]);
    await client.query(`UPDATE ontap_shadow.jobs SET title=$3,employer=$4,location=$5,region=$6,role_family=$7,salary_min=$8,salary_max=$9,salary_period=$10,salary_text=$11,preferred_advert_id=$12
      WHERE id=$1 AND $2::date >= first_seen AND (preferred_advert_id IS NULL OR preferred_advert_id=$12)`,
      [jobId,observedOn,r.title,r.company || r.advertiser_name || null,r.location || null,r.region || null,r.category || null,numeric(r.salary_min),numeric(r.salary_max),r.salary_period || null,r.salary_text || null,currentAdvertId]);
    await client.query(`INSERT INTO ontap_shadow.advert_appearances(advert_id,seen_on,supplier_id,feed_run_id) VALUES($1,$2,$3,$4)
      ON CONFLICT(advert_id,seen_on) DO UPDATE SET feed_run_id=EXCLUDED.feed_run_id`,[currentAdvertId,observedOn,supplier,runId]);
    await client.query(`INSERT INTO ontap_shadow.selection_decisions(id,advert_id,feed_run_id,scope,decision,reason,rules_revision,evidence)
      VALUES($1,$2,$3,'published_snapshot','include',$4,$5,$6)`,
      [stableId(`decision:${runId}:${currentAdvertId}`),currentAdvertId,runId,
      'Present in the supplied published inventory snapshot; no selection rules re-executed.',sourceRevision,
      {source_path:input.sourcePath || null,source_job_id:r.job_id,sample_only:true}]);
  }
  await client.query(`UPDATE ontap_shadow.feed_runs SET status='accepted',completed_at=now() WHERE id=$1`,[runId]);
  return {replayed:false,received:records.length};
}

export async function importSample(client,input) {
  await client.query('BEGIN');
  try {
    const result = await importBatch(client,input);
    await client.query('COMMIT');
    return result;
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  }
}

export async function counts(client) {
  const result = {};
  for (const table of ['suppliers','jobs','supplier_adverts','feed_runs','advert_appearances','selection_decisions']) {
    result[table] = Number((await client.query(`SELECT count(*)::int AS n FROM ontap_shadow.${table}`)).rows[0].n);
  }
  return result;
}
