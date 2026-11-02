import fs from 'node:fs/promises';
import { gunzipSync } from 'node:zlib';
import assert from 'node:assert/strict';
import pg from 'pg';
import { importStage, measure } from './staged-importer.mjs';
import { counts } from './importer.mjs';

async function main() {
  if (process.env.VERCEL_ENV!=='preview' || process.env.ONTAP_SHADOW_NEON_PROJECT_ID!=='noisy-fire-97386602') throw new Error('Wrong test environment');
  const url=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
  if (!url.hostname.endsWith('.neon.tech') || !['require','verify-full'].includes(url.searchParams.get('sslmode'))) throw new Error('Expected TLS Neon connection');
  url.searchParams.set('sslmode','verify-full');
  const fixture=JSON.parse(gunzipSync(await fs.readFile(new URL('./stage.json.gz',import.meta.url))).toString('utf8'));
  const client=new pg.Client({connectionString:url.toString(),connectionTimeoutMillis:15000,query_timeout:60000,statement_timeout:45000,application_name:'ontap-shadow-staged-raw-import'});
  try {
    await client.connect();
    const before=await measure(client);
    const beforeCounts=await counts(client);
    const imported=await importStage(client,fixture);
    const afterCounts=await counts(client);
    const replay=await importStage(client,fixture);
    assert.equal(replay.replayed,true);
    assert.deepEqual(await counts(client),afterCounts,'Replay changed row counts');
    const run=(await client.query(`SELECT id,diagnostics FROM ontap_shadow.feed_runs WHERE feed_key=$1`,[`raw-stage:${fixture.archiveSha256}:${fixture.percentage}`])).rows[0];
    const importedRows=Number((await client.query(`SELECT count(*)::int AS n FROM ontap_shadow.selection_decisions WHERE feed_run_id=$1 AND scope='raw_feed_pending_selection'`,[run.id])).rows[0].n);
    assert.equal(importedRows,fixture.records.length);
    const after=await measure(client);
    const growth=Math.max(0,after.schemaBytes-before.schemaBytes);
    // Relative to this overlapping incremental stage: estimate an entire feed's size.
    const newAdverts=afterCounts.supplier_adverts-beforeCounts.supplier_adverts;
    const bytesPerNewAdvert=Math.max(newAdverts>0?growth/newAdverts:0,after.schemaBytes/Math.max(1,afterCounts.supplier_adverts));
    const estimatedFullDatabaseBytes=Math.ceil(after.databaseBytes+Math.max(0,fixture.totalReceived-afterCounts.supplier_adverts)*bytesPerNewAdvert*1.5);
    const withinHeadroom=after.databaseBytes<fixture.maximumDatabaseBytes && estimatedFullDatabaseBytes<fixture.maximumDatabaseBytes;
    const report={status:'passed',percentage:fixture.percentage,totalReceived:fixture.totalReceived,
      importedRecords:fixture.records.length,archiveDate:fixture.archiveDate,archiveSha256:fixture.archiveSha256,
      beforeDatabaseBytes:before.databaseBytes,afterDatabaseBytes:after.databaseBytes,
      beforeSchemaBytes:before.schemaBytes,afterSchemaBytes:after.schemaBytes,
      schemaGrowthBytes:growth,newAdverts,estimatedBytesPerNewAdvert:Math.ceil(bytesPerNewAdvert),
      estimatedFullDatabaseBytes,maximumDatabaseBytes:fixture.maximumDatabaseBytes,
      beforeCounts,afterCounts,importElapsedMs:imported.elapsedMs,replayElapsedMs:replay.elapsedMs,
      duplicateProtectionPassed:true,withinHeadroom,nextStageAllowed:withinHeadroom && fixture.percentage<100,
      selectionEvidence:'unknown until same-snapshot production outcomes are attached',expiryEnabled:false};
    await fs.mkdir('dist',{recursive:true});
    await fs.writeFile('dist/report.json',JSON.stringify(report,null,2)+'\n');
    await fs.writeFile('dist/index.html','<!doctype html><html><head><meta name="robots" content="noindex,nofollow"><title>Ontap staged database test</title></head><body><h1>Ontap staged raw-feed database test</h1><p>Stage completed. Production unchanged.</p></body></html>');
    console.log('ONTAP_STAGE_REPORT '+JSON.stringify(report));
  } finally {await client.end();}
}
main().catch(error=>{
  const safe=['Storage preflight exceeds test ceiling','Wrong test environment','Stage fraction mismatch','Conflicting stage replay'];
  console.error('ONTAP_STAGE_FAILED',safe.includes(error.message)?error.message:String(error.code || 'verification_error'));
  process.exitCode=1;
});
