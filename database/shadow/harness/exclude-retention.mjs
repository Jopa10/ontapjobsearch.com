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

// Retired on 18 November 2026. Excluded full payloads are never retained in Neon.
export async function applyExcludeReviewWindow(){
  throw new Error('EXCLUDE payload retention is disabled; use the selected/review-only daily write path');
}
