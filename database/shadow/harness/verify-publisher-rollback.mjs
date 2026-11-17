import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import pg from 'pg';
import {requirePreview,requireBudget,requireSameDay,unpackSnapshot,hash,MAX,RESERVE} from './publisher-safeguards.mjs';
requirePreview(process.env);
const url=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);url.searchParams.set('sslmode','verify-full');
const c=new pg.Client({connectionString:url.toString(),connectionTimeoutMillis:15000,query_timeout:120000,application_name:'ontap-preview-rollback-safeguard-test'});
const report={status:'pending',productionChanged:false,writeScope:'existing Preview publisher snapshot within rolled-back transaction'};
try{
 await c.connect();
 const before=(await c.query('SELECT feed_date::text,production_run_id::text,row_count,uncompressed_sha256,compressed_payload FROM ontap_shadow.publisher_snapshots ORDER BY feed_date DESC LIMIT 1')).rows[0];
 assert.ok(before,'No verified Preview publisher snapshot');
 const payloadBefore=hash(before.compressed_payload);
 const rows=unpackSnapshot(before.compressed_payload,before.uncompressed_sha256);
 assert.equal(rows.length,before.row_count);
 const latest=(await c.query('SELECT max(feed_date)::text AS date FROM ontap_shadow.selected_review_payload_records')).rows[0].date;
 requireSameDay(before.feed_date,latest);
 report.feedDate=before.feed_date;report.snapshotRows=rows.length;report.snapshotSha256=before.uncompressed_sha256;
 await c.query('BEGIN');
 try{
  await c.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:preview-scope-publisher'))");
  await c.query('SAVEPOINT corrupt_snapshot');
  await c.query("UPDATE ontap_shadow.publisher_snapshots SET uncompressed_sha256=$2 WHERE feed_date=$1::date",[before.feed_date,'0'.repeat(64)]);
  const bad=(await c.query('SELECT compressed_payload,uncompressed_sha256 FROM ontap_shadow.publisher_snapshots WHERE feed_date=$1::date',[before.feed_date])).rows[0];
  assert.throws(()=>unpackSnapshot(bad.compressed_payload,bad.uncompressed_sha256));
  await c.query('ROLLBACK TO SAVEPOINT corrupt_snapshot');
  const restored=(await c.query('SELECT uncompressed_sha256,compressed_payload FROM ontap_shadow.publisher_snapshots WHERE feed_date=$1::date',[before.feed_date])).rows[0];
  assert.equal(restored.uncompressed_sha256,before.uncompressed_sha256);
  assert.equal(hash(restored.compressed_payload),payloadBefore);
  assert.deepEqual(unpackSnapshot(restored.compressed_payload,restored.uncompressed_sha256),rows);
  await c.query('ROLLBACK');
  report.corruptSnapshotRejected=true;report.previousSnapshotRestoredExactly=true;report.permanentWrites=0;
 }catch(e){await c.query('ROLLBACK');throw e;}
 const after=(await c.query('SELECT uncompressed_sha256,compressed_payload FROM ontap_shadow.publisher_snapshots WHERE feed_date=$1::date',[before.feed_date])).rows[0];
 assert.equal(after.uncompressed_sha256,before.uncompressed_sha256);assert.equal(hash(after.compressed_payload),payloadBefore);
 report.databaseBytes=Number((await c.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
 assert.ok(report.databaseBytes+RESERVE<MAX);
 assert.throws(()=>requireBudget(MAX,1));
 report.storageGuardRejectedOversize=true;report.status='passed';
 await fs.mkdir('dist',{recursive:true});
 await fs.writeFile('dist/safeguard-report.json',JSON.stringify(report,null,2)+'\n');
 await fs.writeFile('dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><title>Preview rollback verification</title><h1>Preview safeguard verification passed</h1>');
 console.log('ONTAP_NEON_ROLLBACK '+JSON.stringify(report));
}finally{await c.end();}
