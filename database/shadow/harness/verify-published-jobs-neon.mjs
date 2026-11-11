import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import pg from 'pg';
import { contentHash, stableId } from './importer.mjs';

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

async function upsertSnapshot(client, snapshot) {
  const supplier = (await client.query(
    "INSERT INTO ontap_shadow.suppliers(code,name) VALUES ('jobg8','JobG8') " +
    "ON CONFLICT(code) DO UPDATE SET name=EXCLUDED.name RETURNING id"
  )).rows[0].id;
  const publicIds = snapshot.records.map(row => row.job_id);
  const existing = await client.query(
    'SELECT j.public_id,j.id AS job_id,a.id AS advert_id ' +
    'FROM ontap_shadow.jobs j LEFT JOIN ontap_shadow.supplier_adverts a ' +
    'ON a.job_id=j.id AND a.supplier_id=$1 WHERE j.public_id=ANY($2::text[])',
    [supplier, publicIds],
  );
  const byPublicId = new Map(existing.rows.map(row => [row.public_id, row]));
  const jobs = [];
  const adverts = [];
  for (const row of snapshot.records) {
    const previous = byPublicId.get(row.job_id);
    const jobId = previous?.job_id || stableId('job:jobg8:' + row.job_id);
    const advertId = previous?.advert_id || stableId('advert:jobg8:' + row.job_id);
    const evidence = {
      ...row.classification_evidence,
      published_output_snapshot: {
        date: snapshot.feedDate,
        workflow_run_id: snapshot.productionWorkflowRunId,
        artifact_id: snapshot.productionArtifactId,
        artifact_sha256: snapshot.productionArtifactSha256,
        source_artifacts: snapshot.productionArtifacts,
        final_published_app_commit_sha: snapshot.productionAppCommitSha,
        snapshot_at: snapshot.productionAppSnapshotAt,
      },
    };
    jobs.push({
      id: jobId, public_id: row.job_id, title: row.title,
      employer: row.employer ?? null, location: row.location ?? null,
      region: row.region ?? null, role_family: row.role_family ?? null,
      salary_min: numeric(row.salary_min), salary_max: numeric(row.salary_max),
      salary_period: row.salary_period ?? null, salary_text: row.salary_text ?? null,
      classification_evidence: evidence,
    });
    const compactContent = {
      job_id: row.job_id, title: row.title, employer: row.employer ?? null,
      advertiser_name: row.advertiser_name ?? null,
      location: row.location ?? null, region: row.region ?? null,
      role_family: row.role_family ?? null, salary_min: numeric(row.salary_min),
      salary_max: numeric(row.salary_max), salary_period: row.salary_period ?? null,
      salary_text: row.salary_text ?? null, apply_url: row.apply_url,
    };
    adverts.push({
      id: advertId, supplier_job_id: row.job_id, job_id: jobId,
      title: row.title, advertiser_name: row.advertiser_name ?? row.employer ?? null,
      location: row.location ?? null, apply_url: row.apply_url,
      content_hash: contentHash(compactContent),
    });
  }

  const chunkSize = 250;
  for (let offset = 0; offset < jobs.length; offset += chunkSize) {
    const chunk = jobs.slice(offset, offset + chunkSize);
    await client.query(
      'INSERT INTO ontap_shadow.jobs ' +
      '(id,public_id,title,employer,location,region,role_family,salary_min,salary_max,salary_period,salary_text,classification_evidence,first_seen,last_seen,publication_status) ' +
      'SELECT r.id::uuid,r.public_id,r.title,r.employer,r.location,r.region,r.role_family,r.salary_min,r.salary_max,r.salary_period,r.salary_text,r.classification_evidence,$2::date,$2::date,\'published\' ' +
      'FROM jsonb_to_recordset($1::jsonb) AS r(id text,public_id text,title text,employer text,location text,region text,role_family text,salary_min numeric,salary_max numeric,salary_period text,salary_text text,classification_evidence jsonb) ' +
      'ON CONFLICT(id) DO UPDATE SET title=EXCLUDED.title,employer=EXCLUDED.employer,location=EXCLUDED.location,region=EXCLUDED.region,role_family=EXCLUDED.role_family,salary_min=EXCLUDED.salary_min,salary_max=EXCLUDED.salary_max,salary_period=EXCLUDED.salary_period,salary_text=EXCLUDED.salary_text,classification_evidence=EXCLUDED.classification_evidence,first_seen=LEAST(ontap_shadow.jobs.first_seen,EXCLUDED.first_seen),last_seen=GREATEST(ontap_shadow.jobs.last_seen,EXCLUDED.last_seen),inactive_since=NULL,publication_status=\'published\'',
      [JSON.stringify(chunk), snapshot.feedDate],
    );
  }
  for (let offset = 0; offset < adverts.length; offset += chunkSize) {
    const chunk = adverts.slice(offset, offset + chunkSize);
    await client.query(
      'INSERT INTO ontap_shadow.supplier_adverts (id,supplier_id,supplier_job_id,job_id,title,advertiser_name,location,apply_url,content_hash,first_seen,last_seen) ' +
      'SELECT r.id::uuid,$2,r.supplier_job_id,r.job_id::uuid,r.title,r.advertiser_name,r.location,r.apply_url,r.content_hash,$3::date,$3::date ' +
      'FROM jsonb_to_recordset($1::jsonb) AS r(id text,supplier_job_id text,job_id text,title text,advertiser_name text,location text,apply_url text,content_hash text) ' +
      'ON CONFLICT(supplier_id,supplier_job_id) DO UPDATE SET job_id=EXCLUDED.job_id,title=EXCLUDED.title,advertiser_name=EXCLUDED.advertiser_name,location=EXCLUDED.location,apply_url=EXCLUDED.apply_url,content_hash=CASE WHEN ontap_shadow.supplier_adverts.raw_payload IS NULL THEN EXCLUDED.content_hash ELSE ontap_shadow.supplier_adverts.content_hash END,last_seen=GREATEST(ontap_shadow.supplier_adverts.last_seen,EXCLUDED.last_seen),inactive_since=NULL,availability=\'seen\'',
      [JSON.stringify(chunk), supplier, snapshot.feedDate],
    );
  }
  await client.query(
    'UPDATE ontap_shadow.jobs j SET preferred_advert_id=a.id FROM ontap_shadow.supplier_adverts a ' +
    'WHERE j.public_id=ANY($1::text[]) AND a.job_id=j.id AND a.supplier_id=$2',
    [publicIds, supplier],
  );
  return { publicIds };
}

async function verifySnapshot(client, snapshot, source, expectedIds) {
  const result = await client.query(
    'SELECT j.public_id,j.title,j.employer,j.location,j.region,j.role_family,j.salary_min::text AS salary_min,j.salary_max::text AS salary_max,j.salary_period,j.salary_text,j.publication_status,j.classification_evidence,a.advertiser_name,a.apply_url ' +
    'FROM ontap_shadow.jobs j JOIN ontap_shadow.supplier_adverts a ON a.job_id=j.id JOIN ontap_shadow.suppliers s ON s.id=a.supplier_id ' +
    'WHERE s.code=\'jobg8\' AND j.public_id=ANY($1::text[])',
    [[...expectedIds]],
  );
  assert.equal(result.rows.length, expectedIds.size, 'Neon row count differs from published ID set');
  const actualById = new Map(result.rows.map(row => [row.public_id, row]));
  assert.deepEqual([...actualById.keys()].sort(), [...expectedIds].sort(), 'Neon IDs differ from published output');
  const fieldDifferences = [];
  for (const expectedRow of snapshot.records) {
    const actual = actualById.get(expectedRow.job_id);
    const expected = projectExpected(expectedRow);
    const evidence = actual.classification_evidence;
    const actualProjection = {
      title: actual.title, employer: actual.employer, advertiser_name: actual.advertiser_name,
      location: actual.location,
      region: actual.region, role_family: actual.role_family,
      salary_min: normalizedNumber(actual.salary_min), salary_max: normalizedNumber(actual.salary_max),
      salary_period: actual.salary_period, salary_text: actual.salary_text, apply_url: actual.apply_url,
      appearances: evidence.published_output_appearances, categories: evidence.categories,
      regions: evidence.regions, locations: evidence.locations,
    };
    if (actual.publication_status !== 'published' ||
      JSON.stringify(canonical(actualProjection)) !== JSON.stringify(canonical(expected))) {
      if (fieldDifferences.length < 20) fieldDifferences.push(expectedRow.job_id);
    }
  }
  assert.equal(fieldDifferences.length, 0, 'Neon projected fields differ for IDs: ' + fieldDifferences.join(', '));
  const allPublished = await client.query(
    "SELECT public_id FROM ontap_shadow.jobs WHERE publication_status='published' ORDER BY public_id",
  );
  assert.deepEqual(allPublished.rows.map(row => row.public_id), [...expectedIds].sort(),
    'Neon has published jobs outside or missing from today’s snapshot');
  const counts = await client.query(
    "SELECT (SELECT count(*)::int FROM ontap_shadow.jobs WHERE publication_status='published') AS published_jobs, " +
    "(SELECT count(*)::int FROM ontap_shadow.supplier_adverts a JOIN ontap_shadow.suppliers s ON s.id=a.supplier_id " +
    "JOIN ontap_shadow.jobs j ON j.id=a.job_id WHERE s.code='jobg8' AND j.publication_status='published') AS published_adverts",
  );
  return {
    status: 'passed', feedDate: snapshot.feedDate,
    productionWorkflowRunId: source.productionWorkflowRunId,
    productionArtifactId: source.productionArtifactId,
    productionArtifactSha256: source.productionArtifactSha256,
    productionArtifacts: source.productionArtifacts,
    productionAppCommitSha: source.productionAppCommitSha,
    productionAppSnapshotAt: source.productionAppSnapshotAt,
    publishedOutputRows: snapshot.jobg8OutputRows,
    uniquePublishedJobG8Ids: expectedIds.size,
    neonJobRows: result.rows.length,
    neonPublishedRows: counts.rows[0].published_jobs,
    neonPublishedAdverts: counts.rows[0].published_adverts,
    exactIdsMatch: true, exactKeyFieldsMatch: true,
    fieldsCompared: ['title','employer','advertiser_name','location','region','role_family','salary_min','salary_max','salary_period','salary_text','apply_url','published_output_appearances'],
    fullDescriptionsStored: false,
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
    const estimatedGrowth = Math.max(8 * 1024 * 1024, projectionBytes * 3);
    assert.ok(beforeBytes + estimatedGrowth + RESERVED_HEADROOM_BYTES <= MAX_DATABASE_BYTES,
      'Published snapshot would exceed the protected database ceiling (' + beforeBytes + ' bytes before write)');
    const existingPublished = await client.query(
      "SELECT public_id FROM ontap_shadow.jobs WHERE publication_status='published' ORDER BY public_id",
    );
    const currentIds = existingPublished.rows.map(row => row.public_id);
    assert.ok(currentIds.length === 0 || JSON.stringify(currentIds) === JSON.stringify([...expectedIds].sort()),
      'Neon already contains a different published-job set; refusing to overwrite it in this one-day test');
    await client.query('BEGIN');
    try {
      await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:published-output'))");
      const { publicIds } = await upsertSnapshot(client, snapshot);
      const report = await verifySnapshot(client, snapshot, source, expectedIds);
      assert.equal(publicIds.length, expectedIds.size);
      await client.query('COMMIT');
      report.databaseBytesBefore = beforeBytes;
      report.databaseBytesAfter = await readDbBytes(client);
      report.databaseGrowthBytes = report.databaseBytesAfter - beforeBytes;
      report.databaseHeadroomAfterBytes = MAX_DATABASE_BYTES - RESERVED_HEADROOM_BYTES - report.databaseBytesAfter;
      report.snapshotSha256 = snapshotSha256;
      report.readback = 'exact IDs and projected published fields';
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
