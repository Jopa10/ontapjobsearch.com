import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import pg from 'pg';
import {requirePreview,hash} from './publisher-safeguards.mjs';
import {readCurrentPublication} from './current-publication.mjs';
import {payloadHash,dayOffset,makeMasterArchive,verifyMasterArchive,registerMasterVersion,archiveMasterVersion,cleanupMasterPayloads,recoverMasterClick} from './master-cleanup.mjs';
requirePreview(process.env);
const request=JSON.parse(await fs.readFile('master-cleanup-request.json','utf8'));
assert.ok(['archive','apply-test'].includes(request.phase));assert.match(request.runToken,/^cleanup-[0-9]+$/);
const root=path.resolve(request.phase==='archive'?'dist/master-cleanup-archives':'master-cleanup-archives');
const uuid=key=>{const h=hash(request.runToken+':'+key).slice(0,32);return h.slice(0,8)+'-'+h.slice(8,12)+'-'+h.slice(12,16)+'-'+h.slice(16,20)+'-'+h.slice(20);};
const u=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);u.searchParams.set('sslmode','verify-full');
const c=new pg.Client({connectionString:u.toString(),connectionTimeoutMillis:15000,query_timeout:120000,application_name:'ontap-preview-real-master-cleanup-verification'});
const manifest=[];
const report={status:'pending',phase:request.phase,runToken:request.runToken,productionChanged:false,usesActualMasterTables:true,realAdvertsPurged:0};
function digestCurrent(x){return payloadHash({day:x.feedDate,ids:x.records.map(r=>[r.public_id,r.payload_sha256]),scopes:x.scopes});}
async function setup(current){
 const supplier=(await c.query("SELECT id FROM ontap_shadow.suppliers WHERE code='jobg8'")).rows[0].id;
 const sample=current.records[0].raw_payload,day=current.feedDate;
 const unused=(await c.query("SELECT t.public_id FROM ontap_shadow.selected_review_payload_records t LEFT JOIN ontap_shadow.jobs j ON j.public_id=t.public_id LEFT JOIN ontap_shadow.supplier_adverts a ON a.supplier_job_id=t.public_id AND a.supplier_id=$2 WHERE t.feed_date=$1::date AND t.decision='SELECTED' AND j.id IS NULL AND a.id IS NULL ORDER BY t.public_id LIMIT 1",[day,supplier])).rows[0]?.public_id;
 assert.ok(unused,'Need one current selected ID not yet copied into the legacy master for the active-ID guard test');
 const cases=[
  {name:'age89',age:89,status:'withheld',available:'missing'},
  {name:'age90',age:90,status:'expired',available:'missing'},
  {name:'age91',age:91,status:'expired',available:'missing'},
  {name:'returned',age:91,status:'withheld',available:'seen',inactive:false},
  {name:'published',age:91,status:'published',available:'missing'},
  {name:'current-selected',age:91,status:'withheld',available:'missing',publicId:unused}
 ];
 const rows=[];
 for(const test of cases){
  const id=request.runToken+'-'+test.name,jobId=uuid(test.name+'job'),advertId=uuid(test.name+'advert');
  const publicId=test.publicId||id;
  const payload=structuredClone(sample);payload['/Job/DisplayReference']=id;payload['/Job/Position']='Ontap cleanup test '+test.name;payload['/Job/ApplicationURL']='https://example.invalid/cleanup-test';
  const version=payloadHash(payload),inactive=test.inactive===false?null:dayOffset(day,-test.age);
  const lastSeen=test.inactive===false?day:dayOffset(day,-test.age-1);
  await c.query('INSERT INTO ontap_shadow.jobs(id,public_id,title,employer,first_seen,last_seen,inactive_since,publication_status) VALUES($1,$2,$3,$4,$5::date,$6::date,$7::date,$8)',[jobId,publicId,payload['/Job/Position'],'Synthetic cleanup verification',dayOffset(day,-120),lastSeen,inactive,test.status]);
  await c.query("INSERT INTO ontap_shadow.supplier_adverts(id,supplier_id,supplier_job_id,job_id,title,apply_url,raw_payload,content_hash,first_seen,last_seen,inactive_since,availability,match_evidence) VALUES($1,$2,$3,$4,$5,$6,$7::jsonb,$8,$9::date,$10::date,$11::date,$12,$13::jsonb)",[advertId,supplier,id,jobId,payload['/Job/Position'],payload['/Job/ApplicationURL'],JSON.stringify(payload),version,dayOffset(day,-120),lastSeen,inactive,test.available,JSON.stringify({cleanup_test_run:request.runToken})]);
  await c.query('UPDATE ontap_shadow.jobs SET preferred_advert_id=$2 WHERE id=$1',[jobId,advertId]);
  const row={...test,advert_id:advertId,job_id:jobId,supplier_job_id:id,public_id:publicId,raw_payload:payload,content_hash:version};
  await registerMasterVersion(c,row);rows.push(row);
 }
 const ninety=rows.find(r=>r.name==='age90');
 const eventId=uuid('click');
 await c.query("INSERT INTO ontap_shadow.activity_events(id,event_type,occurred_at,job_id,advert_id,source_page,advert_content_hash) VALUES($1,'apply_click',now(),$2,$3,'synthetic-cleanup-test',$4)",[eventId,ninety.job_id,ninety.advert_id,ninety.content_hash]);
 const old={...ninety,raw_payload:structuredClone(ninety.raw_payload)};
 const revised=structuredClone(ninety.raw_payload);revised['/Job/Position']+=' later revision';
 ninety.raw_payload=revised;ninety.content_hash=payloadHash(revised);
 await c.query('UPDATE ontap_shadow.supplier_adverts SET raw_payload=$2::jsonb,content_hash=$3,title=$4 WHERE id=$1',[ninety.advert_id,JSON.stringify(revised),ninety.content_hash,revised['/Job/Position']]);
 await registerMasterVersion(c,ninety);
 return {day,rows,old,eventId};
}
try{
 await c.connect();
 // Additive version/archive metadata only; no cleanup is performed by migration.
 await c.query(await fs.readFile('master-cleanup-migration.sql','utf8'));
 const current=await readCurrentPublication(c),before=digestCurrent(current);
 report.currentSelectedIds=current.records.length;report.currentScopeCount=current.scopes.length;
 await c.query('BEGIN');
 try{
  const fixture=await setup(current),{day,rows,old,eventId}=fixture;
  report.asOfDate=day;report.testJobCount=rows.length;
  if(request.phase==='archive'){
   for(const row of [old,...rows.filter(r=>['age90','age91'].includes(r.name))]){
    const made=makeMasterArchive(row),file=path.resolve(root,made.receipt.key);
    assert.ok(file.startsWith(root+'/'));await fs.mkdir(path.dirname(file),{recursive:true});await fs.writeFile(file,made.bytes);
    verifyMasterArchive(await fs.readFile(file),made.receipt);manifest.push(made.receipt);
   }
   await fs.mkdir('dist',{recursive:true});
   await fs.writeFile('dist/master-cleanup-manifest.json',JSON.stringify({runToken:request.runToken,archives:manifest},null,2)+'\n');
   report.status='passed';report.archivesPrepared=manifest.length;report.payloadsCleared=0;
  }else{
   assert.ok(Number.isInteger(request.durableArtifactId)&&request.durableArtifactId>0);
   const saved=JSON.parse(await fs.readFile('master-cleanup-manifest.json','utf8'));assert.equal(saved.runToken,request.runToken);
   const byKey=new Map(saved.archives.map(a=>[a.key,a]));
   let hidden=null,corrupted=null;
   const store={provider:'github-actions-test',
    putIfAbsent:async(key,bytes)=>{
     const receipt=byKey.get(key);assert.ok(receipt,'Archive not in durable artifact manifest');
     const onDisk=await fs.readFile(path.resolve(root,key));assert.equal(hash(onDisk),receipt.sha256);assert.equal(hash(bytes),receipt.sha256);
     return {provider:'github-actions-test',durable:true,artifactId:request.durableArtifactId,runToken:request.runToken};
    },
    get:async key=>{
     if(key===hidden)throw new Error('Verified archive temporarily unavailable');
     const bytes=await fs.readFile(path.resolve(root,key));if(key===corrupted){const b=Buffer.from(bytes);b[b.length-1]^=255;return b;}return bytes;
    }};
   // Preserve the exact clicked older version before current-version cleanup.
   await archiveMasterVersion(c,old,store);
   const options={asOfDate:day,testRunId:request.runToken};
   const plan=await cleanupMasterPayloads(c,{...options,mode:'dry-run'});
   const expected=rows.filter(r=>['age90','age91'].includes(r.name)).map(r=>r.supplier_job_id).sort();
   assert.deepEqual([...plan.candidateIds].sort(),expected);
   const failureKey=makeMasterArchive(rows.find(r=>r.name==='age91')).receipt.key;
   await c.query('SAVEPOINT missing_archive');hidden=failureKey;
   await assert.rejects(cleanupMasterPayloads(c,{...options,mode:'apply',store}),/temporarily unavailable/);
   await c.query('ROLLBACK TO SAVEPOINT missing_archive');await c.query('RELEASE SAVEPOINT missing_archive');hidden=null;
   assert.equal((await c.query("SELECT count(*)::int AS n FROM ontap_shadow.supplier_adverts WHERE match_evidence->>'cleanup_test_run'=$1 AND raw_payload IS NOT NULL",[request.runToken])).rows[0].n,6);
   await c.query('SAVEPOINT corrupt_archive');corrupted=failureKey;
   await assert.rejects(cleanupMasterPayloads(c,{...options,mode:'apply',store}),/Archive checksum mismatch/);
   await c.query('ROLLBACK TO SAVEPOINT corrupt_archive');await c.query('RELEASE SAVEPOINT corrupt_archive');corrupted=null;
   assert.equal((await c.query("SELECT count(*)::int AS n FROM ontap_shadow.supplier_adverts WHERE match_evidence->>'cleanup_test_run'=$1 AND raw_payload IS NOT NULL",[request.runToken])).rows[0].n,6);
   const result=await cleanupMasterPayloads(c,{...options,mode:'apply',store});
   assert.equal(result.purgedCount,2);assert.deepEqual([...result.purgedIds].sort(),expected);
   const states=(await c.query("SELECT supplier_job_id,raw_payload IS NOT NULL AS has_payload,content_purged_at IS NOT NULL AS purged FROM ontap_shadow.supplier_adverts WHERE match_evidence->>'cleanup_test_run'=$1 ORDER BY supplier_job_id",[request.runToken])).rows;
   for(const row of rows){
    const state=states.find(s=>s.supplier_job_id===row.supplier_job_id);
    assert.equal(state.has_payload,!['age90','age91'].includes(row.name));
   }
   const recovered=await recoverMasterClick(c,eventId,store);assert.equal(payloadHash(recovered.payload),payloadHash(old.raw_payload));
   assert.equal(recovered.contentHash,old.content_hash);assert.notEqual(recovered.contentHash,rows.find(r=>r.name==='age90').content_hash);
   assert.equal((await c.query('SELECT count(*)::int AS n FROM ontap_shadow.jobs WHERE id=ANY($1::uuid[])',[rows.map(r=>r.job_id)])).rows[0].n,6);
   assert.equal((await c.query('SELECT count(*)::int AS n FROM ontap_shadow.activity_events WHERE id=$1',[eventId])).rows[0].n,1);
   await c.query('SAVEPOINT protect_history');
   await assert.rejects(c.query('DELETE FROM ontap_shadow.supplier_adverts WHERE id=$1',[old.advert_id]),e=>e.code==='23503');
   await c.query('ROLLBACK TO SAVEPOINT protect_history');await c.query('RELEASE SAVEPOINT protect_history');
   const repeated=await cleanupMasterPayloads(c,{...options,mode:'apply',store});assert.equal(repeated.purgedCount,0);
   report.status='passed';report.boundaryResults={day89:'retained',day90:'archived-and-cleared',day91:'archived-and-cleared'};
   report.returnedAdvertRetained=true;report.publishedAdvertProtected=true;report.latestSelectedAdvertProtected=true;
   report.missingArchiveBlockedEntireBatch=true;report.corruptArchiveBlockedEntireBatch=true;
   report.syntheticMasterPayloadsCleared=2;report.identitiesPreserved=6;report.clickEventsPreserved=1;
   report.originalClickedVersionRecovered=true;report.secondCleanupPurged=0;report.durableArchiveArtifactId=request.durableArtifactId;
   report.fixtureIds=rows.map(r=>r.supplier_job_id);
  }
  await c.query('ROLLBACK');
 }catch(e){await c.query('ROLLBACK');throw e;}
 assert.equal((await c.query("SELECT count(*)::int AS n FROM ontap_shadow.supplier_adverts WHERE match_evidence->>'cleanup_test_run'=$1",[request.runToken])).rows[0].n,0);
 assert.equal(digestCurrent(await readCurrentPublication(c)),before);
 report.syntheticFixturesRolledBack=true;report.existingPublicationUnchanged=true;
 await fs.mkdir('dist',{recursive:true});await fs.writeFile('dist/master-cleanup-report.json',JSON.stringify(report,null,2)+'\n');
 await fs.writeFile('dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><h1>Master cleanup verification</h1>');
 console.log('ONTAP_MASTER_CLEANUP '+JSON.stringify(report));
}finally{await c.end();}
