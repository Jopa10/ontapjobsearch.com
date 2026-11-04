import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import pg from 'pg';

async function main(){
  assert.equal(process.env.VERCEL_ENV,'preview','Preview only');
  assert.equal(process.env.VERCEL_GIT_COMMIT_REF,'feat/neon-shadow-database','Wrong branch');
  assert.equal(process.env.ONTAP_SHADOW_NEON_PROJECT_ID,'noisy-fire-97386602','Wrong Neon project');
  const url=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
  assert.ok(url.hostname.endsWith('.neon.tech'));
  assert.ok(['require','verify-full'].includes(url.searchParams.get('sslmode')));
  url.searchParams.set('sslmode','verify-full');
  const client=new pg.Client({connectionString:url.toString(),connectionTimeoutMillis:15000,query_timeout:30000,statement_timeout:20000,application_name:'ontap-readonly-feed-runs-size-check-20261104'});
  try{
    await client.connect();
    await client.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
    const readOnly=(await client.query('SHOW transaction_read_only')).rows[0].transaction_read_only;
    assert.equal(readOnly,'on');
    const databaseBytes=Number((await client.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
    const relation=(await client.query(`
      SELECT pg_total_relation_size(c.oid)::text AS total_bytes,
             pg_relation_size(c.oid)::text AS main_fork_bytes,
             pg_indexes_size(c.oid)::text AS index_bytes,
             CASE WHEN c.reltoastrelid=0 THEN '0' ELSE pg_total_relation_size(c.reltoastrelid)::text END AS toast_total_bytes,
             CASE WHEN c.reltoastrelid=0 THEN '0' ELSE pg_relation_size(c.reltoastrelid)::text END AS toast_heap_bytes,
             CASE WHEN c.reltoastrelid=0 THEN '0' ELSE pg_indexes_size(c.reltoastrelid)::text END AS toast_index_bytes
      FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
      WHERE n.nspname='ontap_shadow' AND c.relname='feed_runs' AND c.relkind='r'
    `)).rows[0];
    assert.ok(relation,'feed_runs relation missing');
    const runs=(await client.query(`
      SELECT feed_date::text AS feed_date, status, received_count,
             pg_column_size(diagnostics)::int AS diagnostics_stored_bytes,
             pg_column_size(diagnostics->'compact_appearances')::int AS compact_appearances_stored_bytes,
             pg_column_size(diagnostics->'compact_selection')::int AS compact_selection_stored_bytes,
             pg_column_size(diagnostics->'compact_display')::int AS compact_display_stored_bytes,
             pg_column_size(diagnostics->'selection_parity')::int AS selection_parity_stored_bytes,
             pg_column_size(diagnostics->'display_snapshot')::int AS display_snapshot_stored_bytes,
             octet_length(diagnostics->'compact_selection'->'envelope'->>'payload') AS compact_selection_base64_bytes,
             octet_length(diagnostics->'compact_display'->>'payload') AS compact_display_base64_bytes,
             ARRAY(SELECT jsonb_object_keys(diagnostics)) AS diagnostic_keys
      FROM ontap_shadow.feed_runs ORDER BY feed_date,created_at,id
    `)).rows;
    assert.equal(runs.length,5,'Feed run baseline changed during diagnostic');
    const publishedJobs=Number((await client.query(`SELECT count(*)::int AS n FROM ontap_shadow.jobs WHERE publication_status<>'withheld'`)).rows[0].n);
    assert.equal(publishedJobs,0,'Unexpected published jobs');
    const report={status:'passed',readOnly:true,measuredAtUtc:new Date().toISOString(),databaseBytes,feedRunsRelation:Object.fromEntries(Object.entries(relation).map(([k,v])=>[k,Number(v)])),feedRunRows:runs,publishedJobs,scope:'Read-only size attribution for feed_runs and its compact diagnostic fields; no payload values or IDs read.'};
    await client.query('COMMIT');
    await fs.mkdir('dist',{recursive:true});
    await fs.writeFile('dist/feed-runs-storage-diagnostic.json',JSON.stringify(report,null,2)+'\\n');
    await fs.writeFile('dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><title>Read-only storage diagnostic</title><p>feed_runs size diagnostic passed; read-only.</p>');
    console.log('ONTAP_FEED_RUNS_STORAGE_DIAGNOSTIC '+JSON.stringify(report));
  }finally{await client.end();}
}
main().catch(error=>{console.error('ONTAP_FEED_RUNS_STORAGE_DIAGNOSTIC_FAILED '+JSON.stringify({code:error.code||error.name||'diagnostic_failure',message:String(error.message||'').slice(0,300)}));process.exitCode=1;});
