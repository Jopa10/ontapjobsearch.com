import assert from 'node:assert/strict';
import { createHash as createSha256 } from 'node:crypto';
import fs from 'node:fs/promises';
import { gunzipSync } from 'node:zlib';
import { fileURLToPath } from 'node:url';
import pg from 'pg';
import { attachCompactSelection, readCompactSelection } from './selection-importer.mjs';
import { importStage, measure, DEFAULT_BUDGET } from './staged-importer.mjs';
import { canonicalSelection, verifyDependencyManifest } from './selection-history.mjs';
import { contentHash, counts, stableId } from './importer.mjs';

const readGzipJson = async path => JSON.parse(gunzipSync(await fs.readFile(path), { maxOutputLength: 300 * 1024 * 1024 }));

function uniqueIdsByScope(value, label) {
  assert.ok(value && typeof value === 'object' && !Array.isArray(value), `${label} must be a scope map`);
  return Object.fromEntries(Object.entries(value).map(([scope, ids]) => {
    assert.ok(Array.isArray(ids), `${label} scope ${scope} must contain ID rows`);
    const normalized = ids.map(row => String(typeof row === 'object' ? row.job_id : row)).filter(Boolean);
    assert.equal(new Set(normalized).size, normalized.length, `${label} contains duplicate IDs in ${scope}`);
    return [scope, normalized.sort()];
  }));
}

function unionIds(byScope) {
  return new Set(Object.values(byScope).flat());
}

export function validateFreshSelectionInput({ raw, selection, outputs, productionOutputs, productionReference, feedCategoryMap }) {
  assert.equal(raw.percentage, 100, 'Full dated feed required');
  assert.equal(raw.archiveDate, raw.observedOn, 'Raw feed date mismatch');
  assert.equal(raw.archiveSha256, selection.report.archiveSha256, 'Feed checksum mismatch');
  assert.equal(raw.observedOn, selection.report.archiveDate, 'Feed date differs from selector replay');
  assert.equal(raw.sourceRevision, selection.report.rulesRevision, 'Selector revision mismatch');
  assert.equal(raw.records.length, selection.sourceHashes.length, 'Raw and selector ID counts differ');
  assert.equal(selection.report.unknowns, 0, 'Selector evidence is incomplete');
  assert.equal(selection.report.exactFileOutputParity, true, 'Python output replay is not exact');
  verifyDependencyManifest(selection.report, selection.report.compactContext);
  const sourceHashes = new Map(selection.sourceHashes);
  assert.equal(sourceHashes.size, selection.sourceHashes.length, 'Duplicate selector source IDs');
  const rawHashes = new Map(raw.records.map(row => [row['/Job/DisplayReference'], contentHash(row)]));
  assert.equal(rawHashes.size, raw.records.length, 'Duplicate raw feed IDs');
  assert.deepEqual([...rawHashes].sort(), [...sourceHashes].sort(), 'Raw IDs/hashes differ from selector input');
  assert.equal(contentHash(outputs), selection.report.outputsSha256, 'Python outputs checksum mismatch');

  assert.ok(productionReference, 'Same-date production report reference is required');
  assert.equal(productionReference.feedDate, raw.observedOn, 'Production reference feed date mismatch');
  assert.ok(Number.isInteger(productionReference.administrationClassifiedPublishedIds), 'Administration report count missing');
  assert.ok(Number.isInteger(productionReference.allJobG8PublishedIds), 'All-JobG8 report count missing');
  assert.ok(feedCategoryMap && typeof feedCategoryMap === 'object' && !Array.isArray(feedCategoryMap), 'Feed category map is required');
  const feedIds = new Set(raw.records.map(row => String(row['/Job/DisplayReference'])));
  for (const id of feedIds) assert.ok(Object.hasOwn(feedCategoryMap, id), `Feed category is missing for job ${id}`);
  const pythonByScope = Object.fromEntries(Object.entries(outputs).map(([scope, rows]) => [scope, rows.map(row => String(row.job_id))]));
  const productionByScope = uniqueIdsByScope(productionOutputs, 'Same-date production outputs');
  const pythonIdsByScope = uniqueIdsByScope(pythonByScope, 'Python outputs');
  assert.deepEqual(Object.keys(productionByScope).sort(), Object.keys(pythonIdsByScope).sort(), 'Production/Python output scopes differ');
  for (const scope of Object.keys(pythonByScope).sort()) {
    assert.deepEqual(productionByScope[scope], pythonIdsByScope[scope].sort(), `Production/Python output IDs differ in ${scope}`);
  }

  const adminFeedIds = new Set(Object.entries(feedCategoryMap).filter(([, category]) => category === 'Administration').map(([id]) => id));
  const pythonPublished = unionIds(pythonByScope);
  const productionPublished = unionIds(productionByScope);
  const adminPythonIds = [...pythonPublished].filter(id => adminFeedIds.has(id)).sort();
  const adminProductionIds = [...productionPublished].filter(id => adminFeedIds.has(id)).sort();
  assert.deepEqual(adminPythonIds, adminProductionIds, 'Administration-classified Python/production IDs differ');
  assert.equal(adminPythonIds.length, productionReference.administrationClassifiedPublishedIds,
    'Administration ID set does not match its same-date report reference');
  assert.deepEqual([...pythonPublished].sort(), [...productionPublished].sort(), 'All JobG8 Python/production IDs differ');
  assert.equal(pythonPublished.size, productionReference.allJobG8PublishedIds,
    'All JobG8 ID set does not match its same-date report reference');

  const state = canonicalSelection(selection, selection.report.compactContext);
  for (const family of ['admin_service', 'support_worker', 'customer_sales', 'finance_accounts',
    'hr_recruitment', 'marketing', 'legal_assistant_paralegal', 'customer_service_contact_centre']) {
    const selected = new Set(state.decisions.filter(row => row.scope === `production:${family}` && row.decision === 'include').map(row => row.ref));
    const output = new Set(Object.entries(outputs).filter(([scope]) => scope.startsWith(`${family}:`)).flatMap(([, rows]) => rows.map(row => String(row.job_id))));
    assert.deepEqual([...output].sort(), [...selected].sort(), `${family} Python output IDs differ from selector decisions`);
  }
  return state;
}

export function buildFreshReadbackManifest({ raw, selection, outputs, productionOutputs, productionReference, feedCategoryMap, readback }) {
  const pythonOutputIdsByScope = uniqueIdsByScope(outputs, 'Python outputs');
  const adminFeedIds = new Set(Object.entries(feedCategoryMap).filter(([, category]) => category === 'Administration').map(([id]) => id));
  const pythonOutputIds = unionIds(pythonOutputIdsByScope);
  const administrationPublishedIds = [...pythonOutputIds].filter(id => adminFeedIds.has(id)).sort();
  const idsByScope = Object.fromEntries(Object.entries(outputs).map(([scope, rows]) => [
    scope, [...new Set(rows.map(row => String(row.job_id)))].sort()
  ]));
  const perId = readback.decisions.map(row => ({
    jobId: row.ref,
    scope: row.scope,
    automatedOutcome: row.decision,
    automatedReason: row.reason,
    decisionGate: row.gate,
    finalPythonOutputRegions: row.regions,
    neonReadback: { outcome: row.decision, exactMatch: true },
    humanReview: { status: 'not_available_in_selector_replay', decision: null, reviewedAt: null }
  }));
  const counts = {};
  for (const row of perId) counts[row.scope] = { ...(counts[row.scope] || {}), [row.automatedOutcome]: (counts[row.scope]?.[row.automatedOutcome] || 0) + 1 };
  return {
    schemaVersion: 2,
    feed: { date: raw.observedOn, sha256: raw.archiveSha256 },
    selector: { revision: selection.report.rulesRevision, dependencyManifestSha256: selection.report.dependencyManifestSha256, outputsSha256: selection.report.outputsSha256 },
    feedCategoryMapSha256: selection.report.feedCategoryMapSha256,
    perId,
    automatedOutcomeCountsByScope: counts,
    finalPythonOutputIdsByScope: idsByScope,
    finalPythonOutputCountsByScope: Object.fromEntries(Object.entries(idsByScope).map(([scope, ids]) => [scope, ids.length])),
    productionOutputComparison: {
      feedDate: productionReference.feedDate,
      administrationClassifiedPublishedIds: productionReference.administrationClassifiedPublishedIds,
      administrationExactIdsMatch: true,
      administrationPublishedIds,
      allJobG8PublishedIds: productionReference.allJobG8PublishedIds,
      allJobG8ExactIdsMatch: true,
      sameRunScopeIds: uniqueIdsByScope(productionOutputs, 'Same-date production outputs'),
    },
    humanReviewEvidence: { available: false, missingPerIdRecords: perId.length, reason: 'Selector replay does not contain the later human-review decision and timestamp.' },
    finalPublishedReviewEvidence: { available: false, publishedIds: null, reviewIds: null, reason: 'Requires the matching dated post-review production artifact.' },
    completeness: { postgresReadback: 'exact_per_id_match', humanReviewRecordsMissing: perId.length, finalPublishedReviewList: 'not_available', parityMayBeClaimed: false }
  };
}

export async function storeAndReadBackFreshSelection(client, input) {
  const { raw, selection } = input;
  const expected = validateFreshSelectionInput(input);
  const runId = stableId(`run:jobg8:raw-stage:${raw.archiveSha256}:100`);
  const beforeCounts = await counts(client);
  const imported = await importStage(client, raw, { compactSelection: true });
  const run = (await client.query('SELECT id,feed_date::text,rules_revision,diagnostics FROM ontap_shadow.feed_runs WHERE id=$1 AND status=\'accepted\'', [runId])).rows[0];
  assert.ok(run, 'Accepted same-feed raw import missing');
  assert.equal(run.feed_date, raw.observedOn);
  assert.equal(run.diagnostics.archive_sha256, raw.archiveSha256);
  assert.equal(run.rules_revision, selection.report.rulesRevision, 'Neon run records a different selector revision');

  const parent = (await client.query(`SELECT id FROM ontap_shadow.feed_runs
    WHERE supplier_id=(SELECT supplier_id FROM ontap_shadow.feed_runs WHERE id=$1)
      AND status='accepted' AND feed_date<$2::date AND diagnostics ? 'compact_selection'
    ORDER BY feed_date DESC LIMIT 1`, [runId, raw.observedOn])).rows[0];
  const attached = await attachCompactSelection(client, { runId, fixture: selection,
    context: selection.report.compactContext, parentRunId: parent?.id ?? null });
  const readback = await readCompactSelection(client, runId);
  assert.deepEqual(readback.state, expected, 'Neon readback differs from Python per-ID decisions');
  const afterCounts = await counts(client);
  assert.equal(Number((await client.query(`SELECT count(*)::int AS n FROM ontap_shadow.jobs
    WHERE publication_status<>'withheld'`)).rows[0].n), 0, 'A test job is not withheld');

  const replayImport = await importStage(client, raw, { compactSelection: true });
  const replaySelection = await attachCompactSelection(client, { runId, fixture: selection,
    context: selection.report.compactContext, parentRunId: parent?.id ?? null });
  assert.equal(replayImport.replayed, true);
  assert.equal(replaySelection.replayed, true);
  assert.deepEqual(await counts(client), afterCounts, 'Replay changed database counts');
  const allocation = await measure(client);
  assert.ok(allocation.databaseBytes + 64 * 1024 * 1024 < DEFAULT_BUDGET, 'Database exceeds reserved test ceiling');

  const adminFeedIds = new Set(Object.entries(input.feedCategoryMap).filter(([, category]) => category === 'Administration').map(([id]) => id));
  const allPythonOutputIds = unionIds(uniqueIdsByScope(input.outputs, 'Python outputs'));
  const adminOutputIds = new Set([...allPythonOutputIds].filter(id => adminFeedIds.has(id)));
  const allJobG8OutputIds = allPythonOutputIds.size;
  return { status: 'passed', feedDate: raw.observedOn, archiveSha256: raw.archiveSha256,
    selectorRevision: selection.report.rulesRevision, runId, rawImported: raw.records.length,
    decisionsReadBack: readback.state.decisions.length, decisionStateSha256: readback.envelope.stateSha256,
    administrationClassifiedPythonOutputIds: adminOutputIds.size,
    administrationReportReference: input.productionReference.administrationClassifiedPublishedIds,
    allJobG8PythonOutputIds: allJobG8OutputIds,
    allJobG8ReportReference: input.productionReference.allJobG8PublishedIds,
    pythonOutputsSha256: selection.report.outputsSha256,
    initialImportReplayed: imported.replayed, initialSelectionReplayed: attached.replayed,
    replayImportVerified: replayImport.replayed, replaySelectionVerified: replaySelection.replayed,
    countsBefore: beforeCounts, countsAfter: afterCounts, allocation,
    jobsWithheld: true, expiryEnabled: false, purgeExecuted: false, productionChanged: false };
}

async function main() {
  assert.equal(process.env.VERCEL_ENV, 'preview', 'Preview only');
  assert.equal(process.env.ONTAP_SHADOW_NEON_PROJECT_ID, 'noisy-fire-97386602', 'Wrong Neon test project');
  const url = new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
  assert.ok(url.hostname.endsWith('.neon.tech') && ['require', 'verify-full'].includes(url.searchParams.get('sslmode')), 'TLS Neon connection required');
  url.searchParams.set('sslmode', 'verify-full');

  const raw = await readGzipJson('raw-stage.json.gz');
  const selection = await readGzipJson('selection.json.gz');
  const outputs = JSON.parse(await fs.readFile('outputs.json', 'utf8'));
  const productionOutputs = JSON.parse(await fs.readFile('production-outputs.json', 'utf8'));
  const productionReference = JSON.parse(await fs.readFile('production-reference.json', 'utf8'));
  const categoryMapBytes = await fs.readFile('feed-category-map.json');
  assert.equal(createSha256('sha256').update(categoryMapBytes).digest('hex'), selection.report.feedCategoryMapSha256, 'Feed category map checksum mismatch');
  const feedCategoryMap = JSON.parse(categoryMapBytes.toString('utf8'));
  validateFreshSelectionInput({ raw, selection, outputs, productionOutputs, productionReference, feedCategoryMap });
  const client = new pg.Client({ connectionString: url.toString(), connectionTimeoutMillis: 15000,
    query_timeout: 120000, statement_timeout: 90000, application_name: 'ontap-shadow-fresh-selector-writeback' });
  try {
    await client.connect();
    const report = await storeAndReadBackFreshSelection(client, { raw, selection, outputs, productionOutputs, productionReference, feedCategoryMap });
    const readback = (await readCompactSelection(client, report.runId)).state;
    const manifest = buildFreshReadbackManifest({ raw, selection, outputs, productionOutputs, productionReference, feedCategoryMap, readback });
    await fs.mkdir('dist', { recursive: true });
    await fs.writeFile('dist/report.json', JSON.stringify(report, null, 2) + '\n');
    await fs.writeFile('dist/per-id-readback-manifest.json', JSON.stringify(manifest, null, 2) + '\n');
    await fs.writeFile('dist/index.html', '<!doctype html><meta name="robots" content="noindex,nofollow"><title>Ontap fresh selector readback</title><h1>Protected Neon selector readback</h1><p>All jobs remain withheld.</p>');
    console.log('ONTAP_FRESH_SELECTION_NEON_REPORT ' + JSON.stringify(report));
  } finally { await client.end(); }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch(error => {
    console.error('ONTAP_FRESH_SELECTION_NEON_FAILED', error.code || error.name || 'verification_error',
      error.name === 'AssertionError' ? error.message.split('\n')[0] : '');
    process.exitCode = 1;
  });
}
