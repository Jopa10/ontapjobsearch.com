import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import pg from 'pg';

const MAX_DATABASE_BYTES = 838860800;
const RESERVED_HEADROOM_BYTES = 64 * 1024 * 1024;
const hashBytes = value => createHash('sha256').update(value).digest('hex');
const readJson = async path => JSON.parse(await fs.readFile(path, 'utf8'));
const numeric = value => {
  if (value == null || value === '') return null;
  const result = Number(value);
  if (!Number.isFinite(result)) throw new Error('Invalid salary number');
  return result;
};
const normalizedNumber = value => value == null ? null : Number(value);
const canonical = value => Array.isArray(value) ? value.map(canonical)
  : value && typeof value === 'object'
    ? Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])]))
    : value;

function validateSnapshot(snapshot, source) {
  assert.equal(snapshot.schemaVersion, 1);
  assert.equal(snapshot.feedDate, source.feedDate);
  assert.equal(snapshot.productionWorkflowRunId, source.productionWorkflowRunId);
  assert.equal(snapshot.productionArtifactId, source.productionArtifactId);
  assert.equal(snapshot.productionArtifactSha256, source.productionArtifactSha256);
  assert.deepEqual(snapshot.productionArtifacts, source.productionArtifacts);
  assert.equal(snapshot.productionAppCommitSha, source.productionAppCommitSha);
  assert.equal(snapshot.productionAppSnapshotAt, source.productionAppSnapshotAt);
  assert.equal(snapshot.uniqueJobG8Ids, source.expectedUniqueJobG8Ids);
  assert.equal(snapshot.jobg8OutputRows, source.expectedJobG8Rows);
  assert.ok(Array.isArray(snapshot.records));
  assert.equal(snapshot.records.length, source.expectedUniqueJobG8Ids);
  const ids = new Set();
  for (const row of snapshot.records) {
    assert.ok(typeof row.job_id === 'string' && row.job_id.trim());
    assert.ok(typeof row.title === 'string' && row.title.trim());
    assert.ok(typeof row.apply_url === 'string' && /^https?:\/\//.test(row.apply_url));
    assert.ok(row.classification_evidence && Array.isArray(row.classification_evidence.published_output_appearances));
    assert.ok(row.classification_evidence.published_output_appearances.length > 0);
    assert.ok(!Object.hasOwn(row, 'description'), 'Full advert descriptions must not be stored by this test');
    assert.ok(!Object.hasOwn(row, 'raw_payload'), 'Raw adverts must not be stored by this test');
    assert.ok(!ids.has(row.job_id), 'Duplicate JobG8 ID in compact snapshot');
    ids.add(row.job_id);
  }
  return ids;
}

function projectExpected(row) {
  const evidence = row.classification_evidence;
  return {
    title: row.title, employer: row.employer ?? null, advertiser_name: row.advertiser_name ?? null,
    location: row.location ?? null,
    region: row.region ?? null, role_family: row.role_family ?? null,
    salary_min: numeric(row.salary_min), salary_max: numeric(row.salary_max),
    salary_period: row.salary_period ?? null, salary_text: row.salary_text ?? null,
    apply_url: row.apply_url, appearances: evidence.published_output_appearances,
    categories: evidence.categories, regions: evidence.regions, locations: evidence.locations,
  };
}

async function readDbBytes(client) {
  return Number((await client.query('SELECT pg_database_size(current_database())::text AS n')).rows[0].n);
}

async function captureExistingPublishedSet(client) {
  const result = await client.query(
    "SELECT j.public_id,j.title,j.employer,j.location,j.region,j.role_family," +
    "j.salary_min::text AS salary_min,j.salary_max::text AS salary_max,j.salary_period,j.salary_text," +
    "a.advertiser_name,a.apply_url," +
    "j.classification_evidence->'published_output_snapshot'->>'date' AS snapshot_date " +
    "FROM ontap_shadow.jobs j " +
    "JOIN ontap_shadow.supplier_adverts a ON a.job_id=j.id " +
    "JOIN ontap_shadow.suppliers s ON s.id=a.supplier_id " +
    "WHERE s.code='jobg8' AND j.publication_status='published' ORDER BY j.public_id",
  );
  assert.equal(result.rows.length, 5491, 'Wednesday published set count changed before the Thursday snapshot');
  assert.ok(result.rows.every(row => row.snapshot_date === '2026-11-11'),
    'Existing published JobG8 rows are not the verified Wednesday snapshot');
  const ids = result.rows.map(row => row.public_id);
  assert.equal(new Set(ids).size, 5491, 'Existing Wednesday set contains duplicate IDs');
  return { date: '2026-11-11', count: result.rows.length,
    sha256: hashBytes(JSON.stringify(canonical(result.rows))) };
}

function snapshotMetadata(snapshot, source) {
  return {
    feedDate: snapshot.feedDate,
    productionWorkflowRunId: source.productionWorkflowRunId,
    productionArtifactId: source.productionArtifactId,
    productionArtifactSha256: source.productionArtifactSha256,
    productionArtifacts: source.productionArtifacts,
    productionAppCommitSha: source.productionAppCommitSha,
    productionAppSnapshotAt: source.productionAppSnapshotAt,
  };
}

async function storeSnapshot(client, snapshot, source) {
  await client.query(
    'CREATE TABLE IF NOT EXISTS ontap_shadow.published_output_snapshot_records (' +
    'feed_date date NOT NULL, public_id text NOT NULL, projected_fields jsonb NOT NULL, ' +
    'snapshot_metadata jsonb NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), ' +
    'PRIMARY KEY (feed_date, public_id))',
  );
  const metadata = snapshotMetadata(snapshot, source);
  const records = snapshot.records.map(row => ({
    public_id: row.job_id, projected_fields: projectExpected(row), snapshot_metadata: metadata,
  }));
  for (let offset = 0; offset < records.length; offset += 200) {
    await client.query(
      'INSERT INTO ontap_shadow.published_output_snapshot_records ' +
      '(feed_date,public_id,projected_fields,snapshot_metadata) ' +
      'SELECT $1::date,r.public_id,r.projected_fields,r.snapshot_metadata ' +
      'FROM jsonb_to_recordset($2::jsonb) AS r(public_id text,projected_fields jsonb,snapshot_metadata jsonb) ' +
      'ON CONFLICT (feed_date,public_id) DO NOTHING',
      [snapshot.feedDate, JSON.stringify(records.slice(offset, offset + 200))],
    );
  }
  return { publicIds: records.map(row => row.public_id), metadata };
}

async function verifySnapshot(client, snapshot, expectedIds, expectedMetadata) {
  const result = await client.query(
    'SELECT public_id,projected_fields,snapshot_metadata ' +
    'FROM ontap_shadow.published_output_snapshot_records WHERE feed_date=$1::date ORDER BY public_id',
    [snapshot.feedDate],
  );
  assert.equal(result.rows.length, expectedIds.size, 'Neon dated snapshot row count differs from published ID set');
  const actualById = new Map(result.rows.map(row => [row.public_id, row]));
  assert.deepEqual([...actualById.keys()].sort(), [...expectedIds].sort(),
    'Neon dated snapshot IDs differ from published output');
  for (const expectedRow of snapshot.records) {
    const actual = actualById.get(expectedRow.job_id);
    assert.deepEqual(canonical(actual.projected_fields), canonical(projectExpected(expectedRow)),
      'Neon checked fields differ for published ID ' + expectedRow.job_id);
    assert.deepEqual(canonical(actual.snapshot_metadata), canonical(expectedMetadata),
      'Neon snapshot provenance differs for published ID ' + expectedRow.job_id);
  }
  return {
    status: 'passed',
    feedDate: snapshot.feedDate,
    productionWorkflowRunId: expectedMetadata.productionWorkflowRunId,
    productionArtifactId: expectedMetadata.productionArtifactId,
    productionArtifactSha256: expectedMetadata.productionArtifactSha256,
    productionArtifacts: expectedMetadata.productionArtifacts,
    productionAppCommitSha: expectedMetadata.productionAppCommitSha,
    productionAppSnapshotAt: expectedMetadata.productionAppSnapshotAt,
    publishedOutputRows: snapshot.jobg8OutputRows,
    uniquePublishedJobG8Ids: expectedIds.size,
    neonSnapshotRows: result.rows.length,
    exactIdsMatch: true,
    exactKeyFieldsMatch: true,
    fieldsCompared: ['title','employer','advertiser_name','location','region','role_family','salary_min','salary_max','salary_period','salary_text','apply_url','published_output_appearances'],
    fullDescriptionsStored: false,
    snapshotTable: 'ontap_shadow.published_output_snapshot_records',
  };
}

export async function runPublishedJobsReadback() {
  assert.equal(process.env.VERCEL_ENV, 'preview', 'Preview only');
  assert.equal(process.env.ONTAP_SHADOW_NEON_PROJECT_ID, 'noisy-fire-97386602', 'Wrong Neon test project');
  const source = await readJson('source-download.json');
  assert.equal(source.mode, 'published_snapshot');
  const bytes = await fs.readFile('published-snapshot.json');
  const snapshotSha256 = hashBytes(bytes);
  assert.equal(snapshotSha256, source.snapshotSha256, 'Published snapshot fingerprint mismatch');
  const snapshot = JSON.parse(bytes.toString('utf8'));
  const expectedIds = validateSnapshot(snapshot, source);
  const url = new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
  assert.ok(url.hostname.endsWith('.neon.tech') && ['require','verify-full'].includes(url.searchParams.get('sslmode')),
    'TLS Neon connection required');
  url.searchParams.set('sslmode', 'verify-full');
  const client = new pg.Client({
    connectionString: url.toString(), connectionTimeoutMillis: 15000,
    query_timeout: 120000, statement_timeout: 90000,
    application_name: 'ontap-shadow-published-output-writeback',
  });
  try {
    await client.connect();
    const beforeBytes = await readDbBytes(client);
    const projectionBytes = Buffer.byteLength(JSON.stringify(snapshot.records));
    const estimatedGrowth = Math.max(32 * 1024 * 1024, projectionBytes * 6);
    assert.ok(beforeBytes + estimatedGrowth + RESERVED_HEADROOM_BYTES <= MAX_DATABASE_BYTES,
      'Published snapshot would exceed the protected database ceiling (' + beforeBytes + ' bytes before write)');
    const previousPublishedSet = await captureExistingPublishedSet(client);
    await client.query('BEGIN');
    try {
      await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:published-output'))");
      const { publicIds, metadata } = await storeSnapshot(client, snapshot, source);
      const report = await verifySnapshot(client, snapshot, expectedIds, metadata);
      assert.equal(publicIds.length, expectedIds.size);
      const preservedPublishedSet = await captureExistingPublishedSet(client);
      assert.deepEqual(preservedPublishedSet, previousPublishedSet,
        'Wednesday published records changed while storing Thursday snapshot');
      report.preservedPreviousPublishedSet = { ...preservedPublishedSet, unchanged: true };
      await client.query('COMMIT');
      report.databaseBytesBefore = beforeBytes;
      report.databaseBytesAfter = await readDbBytes(client);
      report.databaseGrowthBytes = report.databaseBytesAfter - beforeBytes;
      report.databaseHeadroomAfterBytes = MAX_DATABASE_BYTES - RESERVED_HEADROOM_BYTES - report.databaseBytesAfter;
      report.snapshotSha256 = snapshotSha256;
      report.readback = 'exact dated IDs, provenance, and projected published fields';
      await fs.mkdir('dist', { recursive: true });
      await fs.writeFile('dist/published-readback-report.json', JSON.stringify(report, null, 2) + '\n');
      await fs.writeFile('dist/published-readback-manifest.json', JSON.stringify({
        ...report,
        publishedJobIds: [...expectedIds].sort(),
        sourceArtifacts: source.productionArtifacts,
        productionAppCommitSha: source.productionAppCommitSha,
        productionAppSnapshotAt: source.productionAppSnapshotAt,
      }, null, 2) + '\n');
      await fs.writeFile('dist/index.html', '<!doctype html><meta name="robots" content="noindex,nofollow"><title>Ontap published job readback</title><h1>Isolated Neon published-job readback</h1><p>This is a Preview-only verification.</p>');
      console.log('ONTAP_PUBLISHED_JOBS_NEON_REPORT ' + JSON.stringify(report));
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    }
  } finally {
    await client.end();
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  runPublishedJobsReadback().catch(error => {
    console.error('ONTAP_PUBLISHED_JOBS_NEON_FAILED', error.code || error.name || 'verification_error',
      error.name === 'AssertionError' ? error.message.split('\n')[0] : '');
    process.exitCode = 1;
  });
}
