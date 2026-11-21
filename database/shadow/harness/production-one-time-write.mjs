import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import crypto from 'node:crypto';
import pg from 'pg';
import {readMasterAppearance,upsertSelectedMaster} from './daily-master-snapshot.mjs';

const EXPECTED = {
  feedDate: '2026-11-21',
  archiveKey: 'jobg8/raw/2026-11-21.zip',
  archiveSha256: '84f2a54938e448f86e760f7d3117b836a4dd9217b9236a375077689e8b082852',
  productionOutputRunId: 44880614175,
  productionAppCommitSha: '9b1fb4dcc2681c593eea677e58be0f79e151f650',
  productionRunCommitSha: 'c60a6f749670b34d48e8ef85a9ea2cc86b5ee911',
  selectedCount: 5630,
  scopeCount: 256,
  host: 'ep-green-sunset-zaycl73a-pooler.c-2.eu-west-2.aws.neon.tech',
  database: 'neondb',
  role: 'ontap_prod_once_writer',
};

const maxBytes = 1024 ** 3;
const reserveBytes = 64 * 1024 ** 2;
const harnessDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(harnessDir, '..');
const sourceDir = process.env.ONTAP_PROD_SOURCE_DIR;
const connectionString = process.env.ONTAP_NEON_PROD_ONCE_WRITE_URL;

function hash(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}
function canon(value) {
  if (Array.isArray(value)) return value.map(canon);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.keys(value).sort().map(key => [key, canon(value[key])]));
  }
  return value;
}
function fingerprint(value) {
  return hash(JSON.stringify(canon(value)));
}
async function readJson(name) {
  return JSON.parse(await fs.readFile(path.join(sourceDir, name), 'utf8'));
}
function checkUniqueSource(snapshot, scopes) {
  assert.equal(snapshot.schemaVersion, 2);
  assert.equal(snapshot.feedDate, EXPECTED.feedDate);
  assert.equal(snapshot.archiveKey, EXPECTED.archiveKey);
  assert.equal(snapshot.archiveSha256, EXPECTED.archiveSha256);
  assert.equal(snapshot.productionWorkflowRunId, EXPECTED.productionOutputRunId);
  assert.equal(snapshot.productionAppCommit, EXPECTED.productionAppCommitSha);
  assert.equal(snapshot.productionRunCommit, EXPECTED.productionRunCommitSha);
  assert.equal(snapshot.selectedIds, EXPECTED.selectedCount);
  assert.equal(snapshot.selectedPayloadRecords, EXPECTED.selectedCount);
  assert.equal(snapshot.records.length, EXPECTED.selectedCount);
  assert.equal(scopes.length, EXPECTED.scopeCount);
  const ids = new Set();
  const positions = new Set();
  for (const record of snapshot.records) {
    assert.ok(record.public_id && !ids.has(record.public_id), 'Duplicate or empty source ID');
    ids.add(record.public_id);
    assert.equal(record.decision, 'SELECTED');
    assert.ok(Number.isInteger(record.source_row_position) && record.source_row_position > 0);
    assert.ok(!positions.has(record.source_row_position), 'Duplicate source position');
    positions.add(record.source_row_position);
    assert.equal(fingerprint(record.raw_payload), record.payload_sha256, 'Source payload hash mismatch');
  }
  const scopeIds = new Set();
  for (const scope of scopes) {
    assert.ok(scope.scope && Array.isArray(scope.jobg8Ids));
    assert.equal(new Set(scope.jobg8Ids).size, scope.jobg8Ids.length, 'Duplicate ID within scope');
    for (const id of scope.jobg8Ids) scopeIds.add(id);
  }
  assert.deepEqual([...scopeIds].sort(), [...ids].sort(), 'Scope IDs differ from selected source');
}

function safeReport(report) {
  const output = JSON.stringify(report, null, 2) + '\n';
  console.log('ONTAP_PROD_NEON_ONE_TIME_WRITE ' + JSON.stringify(report));
  return output;
}

assert.ok(sourceDir, 'Missing prepared source directory');
assert.ok(connectionString, 'Missing one-time Production writer connection');
const source = await readJson('daily-source.json');
const scopes = await readJson('daily-scopes.json');
const raw = await fs.readFile(path.join(sourceDir, 'selected-review-payloads.json'));
const snapshot = JSON.parse(raw.toString('utf8'));
assert.equal(hash(raw), source.payloadPackageSha256, 'Prepared payload package hash mismatch');
assert.equal(source.mode, 'daily_latest');
assert.equal(source.dateProvidedByRequest, false);
assert.equal(source.archiveDate, EXPECTED.feedDate);
assert.equal(source.archiveKey, EXPECTED.archiveKey);
assert.equal(source.archiveSha256, EXPECTED.archiveSha256);
assert.equal(source.productionOutputRunId, EXPECTED.productionOutputRunId);
assert.equal(source.productionAppCommitSha, EXPECTED.productionAppCommitSha);
assert.equal(source.productionRunCommitSha, EXPECTED.productionRunCommitSha);
assert.ok(source.archiveOrigin?.kind === 'S3 saved archive via GitHub OIDC');
checkUniqueSource(snapshot, scopes);

const url = new URL(connectionString);
assert.equal(url.hostname, EXPECTED.host, 'Writer secret points to an unexpected Neon endpoint');
assert.equal(url.pathname.replace(/^\//, ''), EXPECTED.database, 'Writer secret points to an unexpected database');
assert.equal(decodeURIComponent(url.username), EXPECTED.role, 'Writer secret uses an unexpected role');
assert.ok(['require', 'verify-full'].includes(url.searchParams.get('sslmode')), 'TLS is required');
url.searchParams.set('sslmode', 'verify-full');

const client = new pg.Client({
  connectionString: url.toString(),
  connectionTimeoutMillis: 15000,
  query_timeout: 120000,
  statement_timeout: 120000,
  application_name: 'ontap-neon-production-one-time-saturday-write',
});
let connected = false;
let transaction = false;
let committed = false;
let report;
let failureStage = 'connecting to Neon';

try {
  await client.connect();
  connected = true;
  failureStage = 'checking database identity and TLS';
  const identity = (await client.query(
    'SELECT current_database() AS database_name,current_user AS role_name,pg_database_size(current_database())::text AS database_bytes'
  )).rows[0];
  assert.equal(identity.database_name, EXPECTED.database);
  assert.equal(identity.role_name, EXPECTED.role);
  const tls = client.connection?.stream?.encrypted === true;
  assert.equal(tls, true, 'TLS is not active');

  failureStage = 'checking writer role attributes';
  const role = (await client.query(
    'SELECT rolsuper,rolcreatedb,rolcreaterole,rolreplication FROM pg_roles WHERE rolname=current_user'
  )).rows[0];
  assert.ok(role);
  assert.equal(role.rolsuper, false);
  assert.equal(role.rolcreatedb, false);
  assert.equal(role.rolcreaterole, false);
  assert.equal(role.rolreplication, false);
  failureStage = 'checking database create privilege';
  const canCreate = (await client.query(
    "SELECT has_database_privilege(current_user,current_database(),'CREATE') AS can_create"
  )).rows[0].can_create;
  assert.equal(canCreate, true, 'Temporary writer lacks schema-create permission');

  failureStage = 'database size and empty-schema checks';
  const before = Number(identity.database_bytes);
  assert.ok(Number.isSafeInteger(before) && before >= 0);
  const estimate = Math.max(32 * 1024 * 1024, raw.length * 5 + 8 * 1024 * 1024);
  assert.ok(before + estimate + reserveBytes <= maxBytes, 'Production 1 GiB storage headroom check failed');

  const existingSchema = (await client.query(
    "SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname='ontap_shadow') AS exists,count(*)::int AS tables FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ontap_shadow' AND c.relkind IN ('r','p','v','m','f')"
  )).rows[0];
  assert.equal(existingSchema.exists, false, 'Production ontap_shadow schema already exists; refusing a second setup');
  assert.equal(existingSchema.tables, 0);

  failureStage = 'schema migrations';
  await client.query('BEGIN');
  transaction = true;
  await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
  for (const migration of [
    '001_initial.sql',
    '002_exclude_review_window.sql',
    '003_feed_row_position.sql',
    '004_master_cleanup_versions.sql',
  ]) {
    const sql = await fs.readFile(path.join(repoRoot, migration), 'utf8');
    await client.query(sql);
  }

  failureStage = 'selected master write';
  const masterWrite = await upsertSelectedMaster(client, {snapshot, scopes, source});
  assert.equal(masterWrite.insertedMasterRows, EXPECTED.selectedCount);
  assert.equal(masterWrite.updatedPayloadRows, 0);
  assert.equal(masterWrite.unchangedMasterRows, 0);
  failureStage = 'publication scope receipt';
  await client.query(
    'CREATE TABLE ontap_shadow.daily_publication_scopes(feed_date date NOT NULL,scope text NOT NULL,jobg8_ids jsonb NOT NULL,PRIMARY KEY(feed_date,scope))'
  );
  for (let i = 0; i < scopes.length; i++) {
    const scope = scopes[i];
    await client.query(
      'INSERT INTO ontap_shadow.daily_publication_scopes(feed_date,scope,jobg8_ids) VALUES($1::date,$2,$3::jsonb)',
      [snapshot.feedDate, scope.scope, JSON.stringify(scope.jobg8Ids)]
    );
  }
  const stateDigest = fingerprint({
    records: snapshot.records.map(({public_id,decision,payload_sha256,source_row_position}) =>
      ({public_id,decision,payload_sha256,source_row_position})),
    scopes,
  });
  await client.query(
    'CREATE TABLE ontap_shadow.daily_refresh_receipts(feed_date date PRIMARY KEY,production_commit text NOT NULL,feed_run_id bigint NOT NULL,record_count integer NOT NULL,state_sha256 text NOT NULL,completed_at timestamptz NOT NULL DEFAULT now())'
  );
  await client.query(
    'INSERT INTO ontap_shadow.daily_refresh_receipts(feed_date,production_commit,feed_run_id,record_count,state_sha256) VALUES($1::date,$2,$3,$4,$5)',
    [snapshot.feedDate,snapshot.productionAppCommit,snapshot.productionWorkflowRunId,EXPECTED.selectedCount,stateDigest]
  );

  failureStage = 'full row, decision and scope comparison';
  const rows = await readMasterAppearance(client, snapshot.feedDate);
  assert.equal(rows.length, EXPECTED.selectedCount);
  const byId = new Map(rows.map(row => [row.public_id, row]));
  assert.equal(byId.size, rows.length, 'Duplicate master appearance IDs');
  for (const expected of snapshot.records) {
    const actual = byId.get(expected.public_id);
    assert.ok(actual, 'Missing master appearance');
    assert.equal(actual.decision, 'SELECTED');
    assert.equal(actual.payload_sha256, expected.payload_sha256);
    assert.deepEqual(canon(actual.raw_payload), canon(expected.raw_payload));
    assert.equal(actual.source_row_position, expected.source_row_position);
  }

  const feedRun = (await client.query(
    "SELECT id FROM ontap_shadow.feed_runs WHERE feed_date=$1::date AND feed_key LIKE $2 ORDER BY completed_at DESC LIMIT 1",
    [snapshot.feedDate, 'selected-daily:' + snapshot.feedDate + ':' + snapshot.archiveSha256 + ':' + snapshot.productionWorkflowRunId]
  )).rows[0];
  assert.ok(feedRun, 'Selected feed run receipt missing');
  const decisions = (await client.query(
    "SELECT a.supplier_job_id AS public_id,d.decision,d.rules_revision,d.evidence FROM ontap_shadow.selection_decisions d JOIN ontap_shadow.supplier_adverts a ON a.id=d.advert_id WHERE d.feed_run_id=$1 AND d.scope='daily_selected' ORDER BY a.supplier_job_id",
    [feedRun.id]
  )).rows;
  assert.equal(decisions.length, EXPECTED.selectedCount);
  const decisionById = new Map(decisions.map(row => [row.public_id, row]));
  assert.equal(decisionById.size, EXPECTED.selectedCount, 'Duplicate stored decisions');
  for (const expected of snapshot.records) {
    const actual = decisionById.get(expected.public_id);
    assert.ok(actual, 'Missing stored selection decision');
    assert.equal(actual.decision, 'include');
    assert.equal(actual.rules_revision, snapshot.productionRunCommit);
    assert.equal(actual.evidence.payload_sha256, expected.payload_sha256);
    assert.equal(actual.evidence.source_row_position, expected.source_row_position);
  }

  const scopeRows = (await client.query(
    'SELECT scope,jobg8_ids FROM ontap_shadow.daily_publication_scopes WHERE feed_date=$1::date ORDER BY scope',
    [snapshot.feedDate]
  )).rows;
  assert.equal(scopeRows.length, EXPECTED.scopeCount);
  const expectedScopes = new Map(scopes.map(scope => [scope.scope, scope.jobg8Ids]));
  for (const row of scopeRows) assert.deepEqual(row.jobg8_ids, expectedScopes.get(row.scope), 'Scope order mismatch');

  const tableCounts = (await client.query(
    "SELECT count(*)::int AS tables FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ontap_shadow' AND c.relkind IN ('r','p','v','m','f')"
  )).rows[0].tables;
  const databaseBytesAfter = Number((await client.query(
    'SELECT pg_database_size(current_database())::text AS bytes'
  )).rows[0].bytes);
  assert.ok(databaseBytesAfter + reserveBytes <= maxBytes, 'Production reserve would be breached');

  report = {
    status: 'passed',
    mode: 'one_time_saturday_saved_publication_write',
    feedDate: EXPECTED.feedDate,
    sourceRunId: EXPECTED.productionOutputRunId,
    selectedIds: EXPECTED.selectedCount,
    scopeCount: EXPECTED.scopeCount,
    exactIdsPayloadHashesPositionsDecisionsAndScopeArraysMatch: true,
    duplicateIds: 0,
    insertedMasterRows: masterWrite.insertedMasterRows,
    updatedPayloadRows: masterWrite.updatedPayloadRows,
    unchangedMasterRows: masterWrite.unchangedMasterRows,
    schemaTables: tableCounts,
    schemaMigrationsApplied: ['001_initial.sql','002_exclude_review_window.sql','003_feed_row_position.sql','004_master_cleanup_versions.sql'],
    cleanupPerformed: false,
    liveSiteSwitched: false,
    productionChanged: true,
    databaseBytesBefore: before,
    databaseBytesAfter,
    storageCeilingBytes: maxBytes,
    storageReserveBytes: reserveBytes,
    stateSha256: stateDigest,
    writesCommitted: false,
  };
  failureStage = 'transaction commit';
  await client.query('COMMIT');
  transaction = false;
  committed = true;
  report.writesCommitted = true;

  // Re-read committed rows and the receipt before reporting success.
  failureStage = 'committed receipt verification';
  const committedRows = await readMasterAppearance(client, snapshot.feedDate);
  assert.equal(committedRows.length, EXPECTED.selectedCount);
  const receipt = (await client.query(
    'SELECT record_count,state_sha256 FROM ontap_shadow.daily_refresh_receipts WHERE feed_date=$1::date',
    [snapshot.feedDate]
  )).rows;
  assert.equal(receipt.length, 1);
  assert.equal(receipt[0].record_count, EXPECTED.selectedCount);
  assert.equal(receipt[0].state_sha256, stateDigest);
  await fs.mkdir(path.dirname(process.env.ONTAP_PROD_REPORT_PATH), {recursive:true});
  await fs.writeFile(process.env.ONTAP_PROD_REPORT_PATH, safeReport(report));
} catch (error) {
  if (connected && transaction) {
    try { await client.query('ROLLBACK'); } catch {}
  }
  if (!report) {
    const safeMessage = String(error?.message || 'preflight_or_comparison_failed')
      .replaceAll(connectionString, '[connection redacted]')
      .replaceAll(decodeURIComponent(new URL(connectionString).password), '[password redacted]')
      .slice(0, 300);
    report = {status:'failed',failureStage,failureMessage:safeMessage,writesCommitted:committed,productionChanged:committed,cleanupPerformed:false,liveSiteSwitched:false};
  }
  if (process.env.ONTAP_PROD_REPORT_PATH) {
    try {
      await fs.mkdir(path.dirname(process.env.ONTAP_PROD_REPORT_PATH), {recursive:true});
      await fs.writeFile(process.env.ONTAP_PROD_REPORT_PATH, safeReport({...report,failureCode:error?.code||'preflight_or_comparison_failed'}));
    } catch {}
  }
  console.error('ONTAP_PROD_NEON_ONE_TIME_WRITE_FAILED', error?.code || 'preflight_or_comparison_failed', failureStage);
  process.exitCode = 1;
} finally {
  if (connected) { try { await client.end(); } catch {} }
}
