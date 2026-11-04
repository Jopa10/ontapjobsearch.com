import assert from 'node:assert/strict';
import {decodeAppearances} from './appearance-manifest.mjs';

const DAY_MS=24*60*60*1000;
export const EXCLUDE_REVIEW_DAYS=3;

function validDate(value){
  assert.match(value,/^\d{4}-\d{2}-\d{2}$/,'Invalid review date');
  assert.equal(new Date(`${value}T00:00:00Z`).toISOString().slice(0,10),value,'Invalid review date');
  return value;
}

export function classifyFullyExcludedRefs(state){
  const refs=new Set(state.sourceHashes.map(([ref])=>ref));
  const decisions=new Map([...refs].map(ref=>[ref,[]]));
  for(const row of state.decisions){
    if(row.scope.startsWith('production:')) decisions.get(row.ref)?.push(row.decision);
  }
  const families=new Set(state.decisions.filter(x=>x.scope.startsWith('production:')).map(x=>x.scope));
  assert.ok(families.size>0,'Missing production-family decisions');
  for(const [ref,outcomes] of decisions){
    assert.equal(outcomes.length,families.size,`Incomplete production decisions for ${ref}`);
  }
  return [...refs].filter(ref=>decisions.get(ref).every(x=>x==='exclude')).sort();
}

// Read-only preflight used before the additive migration and fresh import.
export async function readExcludePayloadBreakdown(client){
  return (await client.query(`WITH latest AS (
    SELECT r.id,r.feed_date::text AS feed_date FROM ontap_shadow.feed_runs r
    JOIN ontap_shadow.suppliers s ON s.id=r.supplier_id
    WHERE s.code='jobg8' AND r.status='accepted' AND r.diagnostics ? 'selection_parity'
    ORDER BY r.feed_date DESC,r.started_at DESC LIMIT 1
  ), outcomes AS (
    SELECT d.advert_id,count(*) FILTER(WHERE d.scope LIKE 'production:%')::int AS family_rows,
      count(*) FILTER(WHERE d.scope LIKE 'production:%' AND d.decision='exclude')::int AS excluded_rows
    FROM ontap_shadow.selection_decisions d JOIN latest r ON r.id=d.feed_run_id GROUP BY d.advert_id
  )
  SELECT (SELECT feed_date FROM latest) AS selector_feed_date,
    count(*) FILTER(WHERE a.raw_payload IS NOT NULL AND o.family_rows=8 AND o.excluded_rows=8)::text AS fully_excluded_payload_rows,
    coalesce(sum(pg_column_size(a.raw_payload)) FILTER(WHERE a.raw_payload IS NOT NULL AND o.family_rows=8 AND o.excluded_rows=8),0)::text AS fully_excluded_payload_bytes,
    count(*) FILTER(WHERE a.raw_payload IS NOT NULL AND o.family_rows=8 AND o.excluded_rows<8)::text AS other_decided_payload_rows,
    coalesce(sum(pg_column_size(a.raw_payload)) FILTER(WHERE a.raw_payload IS NOT NULL AND o.family_rows=8 AND o.excluded_rows<8),0)::text AS other_decided_payload_bytes,
    count(*) FILTER(WHERE a.raw_payload IS NOT NULL AND (o.family_rows IS NULL OR o.family_rows<>8))::text AS without_complete_selector_payload_rows,
    coalesce(sum(pg_column_size(a.raw_payload)) FILTER(WHERE a.raw_payload IS NOT NULL AND (o.family_rows IS NULL OR o.family_rows<>8)),0)::text AS without_complete_selector_payload_bytes
  FROM ontap_shadow.supplier_adverts a LEFT JOIN outcomes o ON o.advert_id=a.id`)).rows[0];
}

// Called only after the exact selector state is attached to an accepted run.
// The caller controls asOfDate in tests; production callers use today's UTC date.
export async function applyExcludeReviewWindow(client,{runId,fullyExcludedRefs,asOfDate=new Date().toISOString().slice(0,10)}){
  validDate(asOfDate);
  assert.ok(Array.isArray(fullyExcludedRefs));
  const excluded=new Set(fullyExcludedRefs);
  assert.equal(excluded.size,fullyExcludedRefs.length,'Duplicate excluded advert reference');
  await client.query('BEGIN');
  try{
    await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
    const run=(await client.query(`SELECT id,supplier_id,feed_date::text,diagnostics FROM ontap_shadow.feed_runs
      WHERE id=$1 AND status='accepted' FOR UPDATE`,[runId])).rows[0];
    assert.ok(run,'Missing accepted feed run');
    assert.equal(run.diagnostics.selection_status,'verified','Selection must be attached before retention');
    const members=decodeAppearances(run.diagnostics.compact_appearances);
    assert.ok(Array.isArray(members),'Missing exact run membership');
    const memberRefs=new Set(members);
    for(const ref of excluded) assert.ok(memberRefs.has(ref),'Excluded advert is outside this run');
    const excludedRefs=[...excluded];
    await client.query(`UPDATE ontap_shadow.supplier_adverts a SET
      exclude_review_started_on=CASE WHEN x.ref IS NOT NULL THEN COALESCE(a.exclude_review_started_on,$3::date) ELSE NULL END,
      content_purged_at=CASE WHEN x.ref IS NULL AND a.exclude_review_started_on IS NOT NULL THEN NULL ELSE a.content_purged_at END
      FROM jsonb_to_recordset($1::jsonb) AS x(ref text)
      WHERE a.supplier_id=$2 AND a.supplier_job_id=x.ref`,[JSON.stringify(excludedRefs.map(ref=>({ref}))),run.supplier_id,run.feed_date]);
    // Clear stale exclusion state for every non-excluded member in this run.
    await client.query(`UPDATE ontap_shadow.supplier_adverts a SET exclude_review_started_on=NULL,
      content_purged_at=CASE WHEN a.raw_payload IS NOT NULL THEN NULL ELSE a.content_purged_at END
      WHERE a.supplier_id=$1 AND a.supplier_job_id=ANY($2::text[]) AND NOT (a.supplier_job_id=ANY($3::text[]))`,
      [run.supplier_id,members,excludedRefs]);
    const due=(await client.query(`SELECT count(*)::int AS payload_rows,
      coalesce(sum(pg_column_size(raw_payload)),0)::text AS payload_bytes
      FROM ontap_shadow.supplier_adverts WHERE supplier_id=$1 AND raw_payload IS NOT NULL
        AND exclude_review_started_on IS NOT NULL AND exclude_review_started_on <= $2::date - $3::int`,
      [run.supplier_id,asOfDate,EXCLUDE_REVIEW_DAYS])).rows[0];
    const purged=(await client.query(`UPDATE ontap_shadow.supplier_adverts
      SET raw_payload=NULL,content_purged_at=now()
      WHERE supplier_id=$1 AND raw_payload IS NOT NULL AND exclude_review_started_on IS NOT NULL
        AND exclude_review_started_on <= $2::date - $3::int
      RETURNING supplier_job_id`,[run.supplier_id,asOfDate,EXCLUDE_REVIEW_DAYS])).rows;
    const remaining=(await client.query(`SELECT count(*)::int AS payload_rows,
      coalesce(sum(pg_column_size(raw_payload)),0)::text AS payload_bytes
      FROM ontap_shadow.supplier_adverts WHERE supplier_id=$1 AND raw_payload IS NOT NULL`,[run.supplier_id])).rows[0];
    await client.query('COMMIT');
    return {excludedCount:excluded.size,purgedCount:purged.length,purgedRefs:purged.map(x=>x.supplier_job_id).sort(),
      dueBeforePurge:{payloadRows:Number(due.payload_rows),payloadBytes:Number(due.payload_bytes)},
      payloadRows:Number(remaining.payload_rows),payloadBytes:Number(remaining.payload_bytes),asOfDate,reviewDays:EXCLUDE_REVIEW_DAYS};
  }catch(error){await client.query('ROLLBACK');throw error;}
}
