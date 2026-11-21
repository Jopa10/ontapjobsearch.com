import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import pg from 'pg';
import {requirePreview,hash} from './publisher-safeguards.mjs';
import {readCurrentPublication} from './current-publication.mjs';
import {canon,fingerprint,addDays,createFixtureTables,applyFixtureFeed,archiveFixtureVersion,purgeDueFixturePayloads,recoverFixtureClick} from './retention-fixture.mjs';
requirePreview(process.env);
const u=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);u.searchParams.set('sslmode','verify-full');
const c=new pg.Client({connectionString:u.toString(),connectionTimeoutMillis:15000,query_timeout:120000,application_name:'ontap-preview-temporary-retention-tests'});
const report={status:'pending',scope:'real Neon readback plus simulated dates in pg_temp only',productionChanged:false,existingJobRecordsChanged:false,productionExpiryEnabled:false,tests:[]};
const archiveRoot=path.resolve('dist/retention-archives'),manifest=[];
const archive={
 put:async(key,bytes)=>{const file=path.resolve(archiveRoot,key);assert.ok(file.startsWith(archiveRoot+'/'));await fs.mkdir(path.dirname(file),{recursive:true});await fs.writeFile(file,bytes);},
 get:async key=>{const file=path.resolve(archiveRoot,key);assert.ok(file.startsWith(archiveRoot+'/'));return fs.readFile(file);}
};
async function scenario(name,fn){
 await c.query('SAVEPOINT scenario');
 try{const result=await fn();report.tests.push({test:name,status:'passed',...result});}
 finally{await c.query('ROLLBACK TO SAVEPOINT scenario');await c.query('RELEASE SAVEPOINT scenario');}
}
function publicationDigest(x){return fingerprint({date:x.feedDate,records:x.records.map(({public_id,payload_sha256,source_row_position})=>({public_id,payload_sha256,source_row_position})),scopes:x.scopes});}
try{
 await c.connect();
 const current=await readCurrentPublication(c);
 assert.ok(current.records.length>=3);
 const beforeDigest=publicationDigest(current),base=current.feedDate;
 const samples=current.records.slice(0,3);
 for(const s of samples)assert.equal(fingerprint(s.raw_payload),s.payload_sha256);
 const [a,b,r]=samples.map((s,i)=>({id:'retention-fixture-'+String(i+1),decision:i===2?'REVIEW':'SELECTED',payload:s.raw_payload}));
 report.realCurrentFeedDate=current.feedDate;report.realCurrentSelectedIds=current.records.length;report.realCurrentScopeCount=current.scopes.length;
 report.fixturePayloadSourceIds=samples.map(s=>s.public_id);
 const excludedBefore=Number((await c.query("SELECT count(*)::text AS n FROM ontap_shadow.selected_review_payload_records WHERE decision='EXCLUDE'")).rows[0].n);
 assert.equal(excludedBefore,0);report.actualDailyExcludePayloadRows=0;
 await c.query('BEGIN');
 try{
  await createFixtureTables(c);
  await scenario('1_missing_jobs_not_published_from_retained_or_partial_data',async()=>{
   await applyFixtureFeed(c,{day:base,records:[a,b,r]});
   const next=addDays(base,1);
   await applyFixtureFeed(c,{day:next,records:[a,r]});
   const old=(await c.query('SELECT count(*)::int AS n FROM pg_temp.selected_review_payload_records WHERE public_id=$1',[b.id])).rows[0].n;
   assert.equal(old,1,'Old advert history was deleted instead of filtered');
   // An incomplete later feed must not become visible before its completion receipt.
   await c.query("INSERT INTO pg_temp.selected_review_payload_records VALUES($1::date,'incomplete-future-fixture','SELECTED',$2::jsonb,$3,1)",[addDays(base,2),JSON.stringify(b.payload),fingerprint(b.payload)]);
   const latest=await readCurrentPublication(c,{schema:'pg_temp'});
   assert.equal(latest.feedDate,next);assert.deepEqual(latest.records.map(x=>x.public_id),[a.id]);
   return {previousSelected:2,currentSelected:1,missingIdsExcluded:[b.id],reviewNotPublished:true,oldPayloadRetained:true,incompleteFutureFeedIgnored:true};
  });
  await scenario('2_ninety_day_boundary_return_and_timer_reset',async()=>{
   await applyFixtureFeed(c,{day:base,records:[b]});
   const missing=addDays(base,1);
   await applyFixtureFeed(c,{day:missing,records:[]});
   const inactive=(await c.query('SELECT inactive_since::text AS d FROM pg_temp.retention_jobs WHERE public_id=$1',[b.id])).rows[0].d;
   assert.equal(inactive,missing);
   await c.query('SAVEPOINT missing_branch');
   assert.equal((await purgeDueFixturePayloads(c,{asOfDate:addDays(missing,89),archive})).length,0);
   await assert.rejects(purgeDueFixturePayloads(c,{asOfDate:addDays(missing,90),archive}),/No verified recoverable archive/);
   assert.ok((await c.query('SELECT payload FROM pg_temp.retention_versions WHERE public_id=$1',[b.id])).rows[0].payload);
   await c.query('ROLLBACK TO SAVEPOINT missing_branch');await c.query('RELEASE SAVEPOINT missing_branch');
   const returned=addDays(missing,45);
   await applyFixtureFeed(c,{day:returned,records:[b]});
   const job=(await c.query('SELECT public_id,inactive_since FROM pg_temp.retention_jobs')).rows[0];
   assert.equal(job.public_id,b.id);assert.equal(job.inactive_since,null);
   assert.equal((await c.query('SELECT count(*)::int AS n FROM pg_temp.retention_jobs')).rows[0].n,1);
   const missingAgain=addDays(returned,1);
   await applyFixtureFeed(c,{day:missingAgain,records:[]});
   assert.equal((await c.query('SELECT inactive_since::text AS d FROM pg_temp.retention_jobs')).rows[0].d,missingAgain);
   assert.equal((await purgeDueFixturePayloads(c,{asOfDate:addDays(missing,90),archive})).length,0);
   return {retentionDays:90,day89PayloadRetained:true,day90WithoutArchiveBlocked:true,returnKeepsId:true,returnClearsInactivity:true,nextAbsenceStartsNewTimer:true,duplicateIdentities:0};
  });
  await scenario('3_exclude_payloads_are_never_saved_by_current_process',async()=>{
   const marker='DO_NOT_STORE_EXCLUDED_PAYLOAD';
   const result=await applyFixtureFeed(c,{day:base,records:[a,r,{id:'excluded-fixture',decision:'EXCLUDE',payload:{title:marker}}]});
   assert.equal(result.excludedIgnored,1);
   assert.equal((await c.query('SELECT count(*)::int AS n FROM pg_temp.retention_versions')).rows[0].n,2);
   assert.equal((await c.query("SELECT count(*)::int AS n FROM pg_temp.retention_versions WHERE public_id='excluded-fixture' OR payload::text LIKE $1",['%'+marker+'%'])).rows[0].n,0);
   assert.equal((await c.query("SELECT count(*)::int AS n FROM pg_temp.selected_review_payload_records WHERE decision='EXCLUDE'")).rows[0].n,0);
   return {selectedPayloadsSaved:1,reviewPayloadsSaved:1,excludePayloadsSaved:0,threeDayExcludeStorageEnabled:false};
  });
  await scenario('4_verified_archive_cleanup_and_exact_clicked_version_recovery',async()=>{
   const id=b.id,v1=fingerprint(b.payload);
   await applyFixtureFeed(c,{day:base,records:[b]});
   await c.query('INSERT INTO pg_temp.retention_clicks VALUES($1,$2,$3,$4)',['fixture-click','synthetic-test-visitor',id,v1]);
   const changed=structuredClone(b.payload);
   changed['/Job/Position']=String(changed['/Job/Position'])+' [simulated later advert revision]';
   const v2=fingerprint(changed);
   await applyFixtureFeed(c,{day:addDays(base,1),records:[{...b,payload:changed}]});
   assert.notEqual(v1,v2);
   assert.equal((await recoverFixtureClick(c,{clickId:'fixture-click',archive})).versionSha256,v1);
   const missing=addDays(base,2);
   await applyFixtureFeed(c,{day:missing,records:[]});
   for(const version of [v1,v2])manifest.push(await archiveFixtureVersion(c,{id,version,archive}));
   const first=manifest[0],original=await archive.get(first.key);
   const corrupt=Buffer.from(original);corrupt[corrupt.length-1]^=255;await archive.put(first.key,corrupt);
   await assert.rejects(purgeDueFixturePayloads(c,{asOfDate:addDays(missing,90),archive}),/Archive checksum mismatch/);
   assert.equal((await c.query('SELECT count(*)::int AS n FROM pg_temp.retention_versions WHERE payload IS NOT NULL')).rows[0].n,2);
   await archive.put(first.key,original);
   const purged=await purgeDueFixturePayloads(c,{asOfDate:addDays(missing,90),archive});
   assert.equal(purged.length,2);
   assert.equal((await c.query('SELECT count(*)::int AS n FROM pg_temp.retention_versions WHERE payload IS NOT NULL')).rows[0].n,0);
   assert.equal((await c.query('SELECT count(*)::int AS n FROM pg_temp.retention_jobs')).rows[0].n,1);
   assert.equal((await c.query('SELECT count(*)::int AS n FROM pg_temp.retention_clicks')).rows[0].n,1);
   const recovered=await recoverFixtureClick(c,{clickId:'fixture-click',archive});
   assert.equal(recovered.versionSha256,v1);assert.deepEqual(canon(recovered.payload),canon(b.payload));
   assert.notEqual(fingerprint(recovered.payload),v2);
   await c.query('SAVEPOINT protect_identity');
   await assert.rejects(c.query('DELETE FROM pg_temp.retention_jobs WHERE public_id=$1',[id]),e=>e.code==='23503');
   await c.query('ROLLBACK TO SAVEPOINT protect_identity');await c.query('RELEASE SAVEPOINT protect_identity');
   return {archivedVersions:2,day90FixturePayloadsCleared:2,archiveCorruptionBlockedCleanup:true,permanentIdPreserved:true,clickHistoryPreserved:true,clickedVersionRecoveredExactly:true,laterVersionDidNotReplaceClick:true,identityDeletionBlockedByForeignKey:true,archiveBackend:'verified gzip files exported as test evidence; production S3 purge not enabled'};
  });
  await c.query('ROLLBACK');
 }catch(e){await c.query('ROLLBACK');throw e;}
 const after=await readCurrentPublication(c);
 assert.equal(publicationDigest(after),beforeDigest,'Existing daily publication changed');
 assert.equal((await c.query("SELECT to_regclass('pg_temp.retention_jobs')::text AS name")).rows[0].name,null);
 report.status='passed';report.testCount=report.tests.length;report.existingPublicationUnchanged=true;report.temporaryTestTablesRolledBack=true;report.actualPayloadsPurged=0;
 await fs.mkdir('dist',{recursive:true});
 await fs.writeFile('dist/retention-archive-manifest.json',JSON.stringify({schemaVersion:1,fixturesOnly:true,archives:manifest},null,2)+'\n');
 await fs.writeFile('dist/retention-test-report.json',JSON.stringify(report,null,2)+'\n');
 await fs.writeFile('dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><h1>Four Preview expiry and retention simulations passed</h1>');
 console.log('ONTAP_FOUR_RETENTION_TESTS '+JSON.stringify(report));
}finally{await c.end();}
