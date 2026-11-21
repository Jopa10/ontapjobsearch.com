// One-off schema-only Preview migration. Never imports or purges adverts.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import pg from 'pg';

const CEILING = 838860800;
const RESERVE = 67108864;
const EXPECTED_BASELINE = { adverts:43796, payloads:43796, jobs:43796, feedRuns:4, publishedJobs:0 };
const SQL_COLUMN = 'ALTER TABLE ontap_shadow.supplier_adverts ADD COLUMN IF NOT EXISTS exclude_review_started_on date';
const SQL_INDEX = 'CREATE INDEX IF NOT EXISTS supplier_adverts_exclude_review ON ontap_shadow.supplier_adverts(exclude_review_started_on) WHERE raw_payload IS NOT NULL';
const COUNTS_SQL = [
  'SELECT',
  '(SELECT count(*) FROM ontap_shadow.supplier_adverts)::text AS adverts,',
  '(SELECT count(*) FROM ontap_shadow.supplier_adverts WHERE raw_payload IS NOT NULL)::text AS payloads,',
  '(SELECT count(*) FROM ontap_shadow.jobs)::text AS jobs,',
  '(SELECT count(*) FROM ontap_shadow.feed_runs)::text AS feed_runs,',
  "(SELECT count(*) FROM ontap_shadow.jobs WHERE publication_status <> 'withheld')::text AS published_jobs"
].join(' ');

function normalize(value) { return String(value || '').replaceAll('"', '').replace(/\s+/g, '').toLowerCase(); }

async function snapshot(client) {
  const db=(await client.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0];
  const c=(await client.query(COUNTS_SQL)).rows[0];
  return {databaseBytes:Number(db.bytes),adverts:Number(c.adverts),payloads:Number(c.payloads),
    jobs:Number(c.jobs),feedRuns:Number(c.feed_runs),publishedJobs:Number(c.published_jobs)};
}

async function verifySchema(client) {
  const col=(await client.query("SELECT format_type(a.atttypid,a.atttypmod) AS column_type FROM pg_attribute a WHERE a.attrelid='ontap_shadow.supplier_adverts'::regclass AND a.attname='exclude_review_started_on' AND NOT a.attisdropped")).rows[0];
  assert.equal(col?.column_type,'date','Review date column missing or wrong type');
  const idx=(await client.query("SELECT pg_get_indexdef(i.indexrelid) AS definition, pg_get_expr(i.indpred,i.indrelid) AS predicate FROM pg_index i WHERE i.indexrelid=to_regclass('ontap_shadow.supplier_adverts_exclude_review')")).rows[0];
  assert.ok(idx,'Review index missing');
  assert.ok(normalize(idx.definition).includes('exclude_review_started_on'),'Review index has wrong key');
  assert.ok(normalize(idx.predicate).includes('raw_payloadisnotnull'),'Review index has wrong predicate');
  return {columnType:col.column_type,indexDefinition:idx.definition,indexPredicate:idx.predicate};
}

async function main() {
  assert.equal(process.env.VERCEL_ENV,'preview','Preview deployments only');
  assert.equal(process.env.ONTAP_SHADOW_NEON_PROJECT_ID,'noisy-fire-97386602','Wrong Neon test project');
  const u=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
  assert.ok(u.hostname.endsWith('.neon.tech'),'Expected Neon host');
  assert.ok(['require','verify-full'].includes(u.searchParams.get('sslmode')),'TLS required');
  u.searchParams.set('sslmode','verify-full');
  const client=new pg.Client({connectionString:u.toString(),connectionTimeoutMillis:15000,query_timeout:60000,statement_timeout:45000,application_name:'ontap-shadow-schema-002-only'});
  const report={operation:'schema-only migration 002',previewOnly:true,neonProjectId:'noisy-fire-97386602',
    sourceCommit:process.env.VERCEL_GIT_COMMIT_SHA||null,migrationApplied:false,importAttempted:false,
    purgeAttempted:false,productionChanged:false,expectedBaseline:{...EXPECTED_BASELINE},
    ceilingBytes:CEILING,reserveBytes:RESERVE};
  try {
    await client.connect();
    await client.query('BEGIN');
    await client.query("SET LOCAL lock_timeout='5s'");
    await client.query("SET LOCAL statement_timeout='45s'");
    assert.equal((await client.query('SHOW transaction_read_only')).rows[0].transaction_read_only,'off','Preview migration connection is read-only');
    const before=await snapshot(client);report.before=before;
    const {databaseBytes:ignored,...observed}=before;
    assert.deepEqual(observed,EXPECTED_BASELINE,'Neon data baseline changed; stop before migration');
    assert.ok(before.databaseBytes+RESERVE<CEILING,'Insufficient pre-migration reserve');
    const prior=(await client.query("SELECT EXISTS(SELECT 1 FROM pg_attribute WHERE attrelid='ontap_shadow.supplier_adverts'::regclass AND attname='exclude_review_started_on' AND NOT attisdropped) AS column_exists, to_regclass('ontap_shadow.supplier_adverts_exclude_review') IS NOT NULL AS index_exists")).rows[0];
    assert.ok(prior.column_exists||!prior.index_exists,'Index exists without its column');
    if(!prior.column_exists) await client.query(SQL_COLUMN);
    if(!prior.index_exists) await client.query(SQL_INDEX);
    report.schema=await verifySchema(client);
    const after=await snapshot(client);report.after=after;
    const {databaseBytes:ignoredAfter,...observedAfter}=after;
    const {databaseBytes:ignoredBefore,...observedBefore}=before;
    assert.deepEqual(observedAfter,observedBefore,'Schema migration changed advert/job data');
    assert.ok(after.databaseBytes+RESERVE<CEILING,'Post-migration reserve check failed');
    await client.query('COMMIT');
    report.migrationApplied=!prior.column_exists||!prior.index_exists;
    report.status=report.migrationApplied?'passed-schema-migration-and-readback':'passed-idempotent-schema-readback';
    report.postCommitSchema=await verifySchema(client);
    report.postCommitDatabaseBytes=Number((await client.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
    assert.ok(report.postCommitDatabaseBytes+RESERVE<CEILING,'Post-commit reserve check failed');
  } catch(error) {
    try { await client.query('ROLLBACK'); } catch {}
    report.status='failed-rolled-back-or-idempotently-recoverable';
    report.errorCode=error.code||'guard_or_verification_failure';
    console.error('ONTAP_SCHEMA_002_FAILED '+JSON.stringify({status:report.status,errorCode:report.errorCode,importAttempted:false,purgeAttempted:false,productionChanged:false}));
    process.exitCode=1;
  } finally { await client.end(); }
  if(process.exitCode) return;
  await fs.mkdir('dist',{recursive:true});
  await fs.writeFile('dist/report.json',JSON.stringify(report,null,2)+'\n');
  await fs.writeFile('dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><title>Schema migration receipt</title><p>Schema-only migration receipt.</p>');
  console.log('ONTAP_SCHEMA_002_RESULT '+JSON.stringify(report));
}
main().catch(error=>{
  console.error('ONTAP_SCHEMA_002_FAILED '+JSON.stringify({errorCode:error.code||'guard_or_verification_failure',importAttempted:false,purgeAttempted:false,productionChanged:false}));
  process.exitCode=1;
});
