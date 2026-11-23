import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import pg from 'pg';
import { gzipSync, gunzipSync } from 'node:zlib';
import { readCurrentPublication } from './current-publication.mjs';

const EXPECTED = {
  host: 'ep-green-sunset-zaycl73a-pooler.c-2.eu-west-2.aws.neon.tech',
  database: 'neondb',
  role: 'ontap_prod_daily_writer',
};
const MAX_BYTES = 838860800;
const RESERVE_BYTES = 67108864;
const sourcePath = process.env.ONTAP_PUBLISHER_SOURCE_PATH;
const connectionString = process.env.ONTAP_NEON_PROD_DAILY_WRITE_URL;
const outputsPath = process.env.ONTAP_NEON_PUBLISHER_OUTPUTS_PATH;
const reportPath = process.env.ONTAP_PROD_PUBLISHER_REPORT_PATH;
const runId = Number(process.env.GITHUB_RUN_ID);
const hash = (value) => crypto.createHash('sha256').update(value).digest('hex');

assert.ok(sourcePath && outputsPath && reportPath, 'Missing Production publisher file paths');
assert.ok(connectionString, 'Missing Production Neon writer connection');
assert.ok(Number.isSafeInteger(runId) && runId > 0, 'Missing GitHub workflow run ID');

const source = JSON.parse(await fs.readFile(sourcePath, 'utf8'));
assert.equal(source.schemaVersion, 1);
assert.ok(source.scopeCount >= 200, 'Incomplete LIVE publisher scope set');
assert.equal(Object.keys(source.scopes).length, source.scopeCount);

const url = new URL(connectionString);
assert.equal(url.hostname, EXPECTED.host, 'Unexpected Production Neon endpoint');
assert.equal(url.pathname.replace(/^\//, ''), EXPECTED.database, 'Unexpected Production database');
assert.equal(decodeURIComponent(url.username), EXPECTED.role, 'Unexpected Production writer role');
assert.ok(['require', 'verify-full'].includes(url.searchParams.get('sslmode')), 'TLS is required');
url.searchParams.set('sslmode', 'verify-full');

const client = new pg.Client({
  connectionString: url.toString(),
  connectionTimeoutMillis: 15000,
  query_timeout: 120000,
  statement_timeout: 120000,
  application_name: 'ontap-neon-production-publisher-snapshot',
});
let connected = false;
let inTransaction = false;
let committed = false;

try {
  await client.connect();
  connected = true;
  const identity = (await client.query(
    'SELECT current_database() AS db,current_user AS role,pg_database_size(current_database())::text AS bytes'
  )).rows[0];
  assert.equal(identity.db, EXPECTED.database);
  assert.equal(identity.role, EXPECTED.role);
  assert.equal(client.connection?.stream?.encrypted, true, 'TLS is not active');

  const publication = await readCurrentPublication(client);
  const selectedById = new Map(publication.records.map((row) => [
    String(row.public_id),
    String(row.raw_payload['/Job/ApplicationURL'] ?? ''),
  ]));
  assert.ok(selectedById.size > 0, 'No current selected JobG8 records in Production Neon');

  const rows = [];
  const scopes = [];
  let rowCount = 0;
  for (const [scope, displayRows] of Object.entries(source.scopes)) {
    assert.ok(Array.isArray(displayRows), 'Scope is not a list: ' + scope);
    const ids = new Set();
    const jobg8Ids = [];
    for (const [position, display] of displayRows.entries()) {
      const publicId = String(display.job_id ?? '');
      assert.ok(publicId && display.title && display.apply_url && display.source,
        'Published row is missing an ID, title, Apply link, or source in ' + scope);
      assert.ok(!ids.has(publicId), 'Duplicate ID in ' + scope + ': ' + publicId);
      ids.add(publicId);
      if (display.source === 'JobG8') {
        jobg8Ids.push(publicId);
        assert.ok(selectedById.has(publicId), 'JobG8 row is absent from Neon selection: ' + publicId);
        assert.equal(String(display.apply_url), selectedById.get(publicId),
          'Published Apply link differs from Neon: ' + publicId);
      }
      rows.push({ scope, position, public_id: publicId, source: String(display.source), display });
    }
    scopes.push({ scope, jobg8Ids });
    rowCount += displayRows.length;
  }
  assert.equal(rowCount, source.rowCount, 'Prepared publisher row count differs');
  const publishedJobg8Ids = [...new Set(rows.filter((row) => row.source === 'JobG8').map((row) => row.public_id))].sort();
  assert.deepEqual(publishedJobg8Ids, [...selectedById.keys()].sort(),
    'Published JobG8 inventory differs from the current Neon selection');
  for (const scope of scopes) {
    const expected = publication.scopes.find((row) => row.scope === scope.scope);
    assert.ok(expected, 'Neon selection is missing publication scope: ' + scope.scope);
    assert.deepEqual(scope.jobg8Ids, expected.jobg8_ids, 'JobG8 order differs in scope: ' + scope.scope);
  }
  assert.equal(scopes.length, publication.scopes.length, 'Published scope count differs from Neon');

  const serialized = Buffer.from(JSON.stringify(rows), 'utf8');
  const compressed = gzipSync(serialized, { level: 9 });
  const digest = hash(serialized);
  const before = Number(identity.bytes);
  assert.ok(Number.isSafeInteger(before) && before >= 0, 'Invalid Production database size');
  assert.ok(before + compressed.length * 4 + 32 * 1024 * 1024 + RESERVE_BYTES <= MAX_BYTES,
    'Production Neon storage reserve check failed');

  const columns = (await client.query(
    "SELECT column_name FROM information_schema.columns " +
    "WHERE table_schema='ontap_shadow' AND table_name='publisher_snapshots'"
  )).rows.map((row) => row.column_name);
  for (const name of ['feed_date', 'production_run_id', 'row_count', 'uncompressed_sha256', 'compressed_payload']) {
    assert.ok(columns.includes(name), 'Production publisher snapshot migration is missing column: ' + name);
  }
  for (const privilege of ['SELECT', 'INSERT', 'UPDATE', 'DELETE']) {
    assert.equal((await client.query(
      'SELECT has_table_privilege(current_user,$1,$2) AS ok',
      ['ontap_shadow.publisher_snapshots', privilege]
    )).rows[0].ok, true, 'Missing ' + privilege + ' privilege on publisher_snapshots');
  }

  await client.query('BEGIN');
  inTransaction = true;
  await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:publisher-snapshot'))");
  const prunedSnapshots = await client.query(
    'DELETE FROM ontap_shadow.publisher_snapshots WHERE feed_date <> $1::date',
    [publication.feedDate]
  );
  await client.query(
    'INSERT INTO ontap_shadow.publisher_snapshots ' +
    '(feed_date,production_run_id,row_count,uncompressed_sha256,compressed_payload) ' +
    'VALUES($1::date,$2,$3,$4,$5) ' +
    'ON CONFLICT(feed_date) DO UPDATE SET ' +
    'production_run_id=excluded.production_run_id,row_count=excluded.row_count,' +
    'uncompressed_sha256=excluded.uncompressed_sha256,compressed_payload=excluded.compressed_payload',
    [publication.feedDate, runId, rows.length, digest, compressed]
  );
  const snapshotCount = Number((await client.query(
    'SELECT COUNT(*)::text AS count FROM ontap_shadow.publisher_snapshots'
  )).rows[0].count);
  assert.equal(snapshotCount, 1, 'Production Neon must retain only the current publisher snapshot');
  const afterWrite = Number((await client.query(
    'SELECT pg_database_size(current_database())::text AS bytes'
  )).rows[0].bytes);
  assert.ok(afterWrite + RESERVE_BYTES <= MAX_BYTES, 'Production storage reserve breached');
  await client.query('COMMIT');
  inTransaction = false;
  committed = true;

  const stored = (await client.query(
    'SELECT feed_date::text AS feed_date,production_run_id::text AS production_run_id,' +
    'row_count,uncompressed_sha256,compressed_payload ' +
    'FROM ontap_shadow.publisher_snapshots WHERE feed_date=$1::date',
    [publication.feedDate]
  )).rows[0];
  assert.ok(stored, 'Production snapshot readback is missing');
  assert.equal(stored.feed_date, publication.feedDate);
  assert.equal(stored.production_run_id, String(runId));
  assert.equal(stored.row_count, rows.length);
  assert.equal(stored.uncompressed_sha256, digest);
  const unpacked = gunzipSync(stored.compressed_payload);
  assert.equal(hash(unpacked), digest, 'Production snapshot SHA-256 readback mismatch');
  const readbackRows = JSON.parse(unpacked.toString('utf8'));
  assert.deepEqual(readbackRows, rows, 'Production snapshot rows differ after readback');

  const outputs = Object.fromEntries(scopes.map(({ scope }) => [scope, []]));
  const nextPosition = new Map();
  for (const row of readbackRows) {
    assert.equal(row.position, nextPosition.get(row.scope) ?? 0, 'Stored scope ordering is not contiguous: ' + row.scope);
    nextPosition.set(row.scope, row.position + 1);
    assert.ok(row.scope in outputs, 'Stored snapshot has an unexpected scope: ' + row.scope);
    outputs[row.scope].push(row.display);
  }
  for (const scope of scopes) {
    assert.equal(nextPosition.get(scope.scope) ?? 0, source.scopes[scope.scope].length,
      'Stored scope row count differs: ' + scope.scope);
  }

  await fs.writeFile(outputsPath, JSON.stringify(outputs), 'utf8');
  await fs.writeFile(
    path.resolve(path.dirname(outputsPath), 'shadow-preview-metadata.json'),
    JSON.stringify({ date: publication.feedDate, productionRunId: runId, snapshotSha256: digest }),
    'utf8'
  );
  const report = {
    status: 'passed',
    feedDate: publication.feedDate,
    productionRunId: runId,
    selectedJobG8Ids: selectedById.size,
    scopeCount: scopes.length,
    publisherRows: rows.length,
    exactJobG8IdsMatch: true,
    exactJobG8ScopeOrderMatch: true,
    exactApplyUrlsMatch: true,
    fullSnapshotReadbackMatch: true,
    snapshotSha256: digest,
    snapshotBytes: serialized.length,
    compressedSnapshotBytes: compressed.length,
    databaseBytesBefore: before,
    databaseBytesAfter: afterWrite,
    previousSnapshotsRemoved: prunedSnapshots.rowCount,
    retention: 'latest publisher snapshot only',
    productionChanged: committed,
    siteDeployOccurredInSnapshotStep: false,
  };
  await fs.writeFile(reportPath, JSON.stringify(report, null, 2) + '\n', 'utf8');
  console.log('ONTAP_PROD_PUBLISHER_SNAPSHOT ' + JSON.stringify(report));
} catch (error) {
  if (inTransaction) await client.query('ROLLBACK').catch(() => {});
  console.error('Production publisher snapshot failed:', error instanceof Error ? error.message : String(error));
  throw error;
} finally {
  if (connected) await client.end().catch(() => {});
}
