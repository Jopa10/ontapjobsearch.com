import {test} from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs/promises';
import {PGlite} from '@electric-sql/pglite';
import {FAMILIES,canonicalSelection,encodeHistory,decodeHistory} from './selection-history.mjs';
import {attachCompactSelection,readCompactSelection} from './selection-importer.mjs';
import {importStage} from './staged-importer.mjs';import {contentHash,stableId,counts} from './importer.mjs';
const context={selectorRevision:'a'.repeat(40),registersSha256:'b'.repeat(64),geographySha256:'c'.repeat(64),configurationSha256:'d'.repeat(64),scopeRegistrySha256:'e'.repeat(64),timeContext:'2026-11-02'};
const rows=(ids)=>ids.map(ref=>({'/Job/DisplayReference':ref,'/Job/Position':'Administrator','/Job/ApplicationURL':'https://example.org/'+ref}));
const fixture=(records,day,patch={})=>({report:{cleanRecords:records.length,exactFileOutputParity:true,unknowns:0,rulesRevision:context.selectorRevision,archiveSha256:contentHash({day,records}),outputsSha256:'f'.repeat(64)},sourceHashes:records.map(r=>[r['/Job/DisplayReference'],contentHash(r)]),decisions:FAMILIES.flatMap(f=>records.map(r=>({ref:r['/Job/DisplayReference'],scope:'production:'+f,decision:'exclude',reason:'Observed excluded',gate:'Actual gate',regions:[],...patch})))});
const schema=await fs.readFile(new URL('../001_initial.sql',import.meta.url),'utf8');
const raw=(records,day)=>({records,observedOn:day,percentage:100,archiveSha256:contentHash({day,records}),sourceRevision:context.selectorRevision,totalReceived:records.length,rawPayloadBytes:Buffer.byteLength(JSON.stringify(records)),maximumDatabaseBytes:800*1024*1024});
const runId=f=>stableId('run:jobg8:raw-stage:'+f.report.archiveSha256+':100');
test('unchanged decisions stored once; dependency changes still preserve verified daily context',()=>{
 const f=fixture(rows(['1','2']),'2026-11-02'),a=encodeHistory(f,context);
 const g=fixture(rows(['1','2']),'2026-11-03'),next={...context,timeContext:'2026-11-03',registersSha256:'1'.repeat(64)};
 const b=encodeHistory(g,next,a);assert.equal(b.envelope.changedDecisions,0);assert.equal(b.envelope.changedSourceHashes,0);
 assert.deepEqual(decodeHistory(b.envelope,a.state),canonicalSelection(g,next));assert.notEqual(b.envelope.stateSha256,a.envelope.stateSha256);
});
test('change, absence and return reconstruct exact historical evidence without stale rows',()=>{
 const a=encodeHistory(fixture(rows(['1','2']),'2026-11-02'),context);
 const b=encodeHistory(fixture(rows(['1','3']),'2026-11-03',{reason:'Updated observed reason'}),context,a);
 assert.equal(b.envelope.removedDecisions,8);assert.equal(b.envelope.changedDecisions,16);
 const c=encodeHistory(fixture(rows(['1','2']),'2026-11-04'),context,b);
 assert.deepEqual(decodeHistory(c.envelope,b.state),c.state);assert.equal(c.state.decisions.length,16);
 assert.equal(a.state.decisions.find(x=>x.ref==='2').reason,'Observed excluded');
});
test('incomplete evidence, corrupted chains and wrong parents fail closed; periodic baseline bounds ancestry',()=>{
 const f=fixture(rows(['1']),'2026-11-02'),a=encodeHistory(f,context);
 const bad=structuredClone(f);bad.decisions.pop();assert.throws(()=>encodeHistory(bad,context));
 bad.decisions=structuredClone(f.decisions);bad.report.unknowns=1;assert.throws(()=>encodeHistory(bad,context));
 const b=encodeHistory(f,context,a);assert.throws(()=>decodeHistory(b.envelope,{...a.state,context:{}}),/Wrong parent/);
 const corrupt=structuredClone(a.envelope);corrupt.stateSha256='0'.repeat(64);assert.throws(()=>decodeHistory(corrupt),/mismatch/);
 let p=a;for(let i=0;i<7;i++)p=encodeHistory(f,context,p);assert.equal(p.envelope.kind,'baseline');assert.equal(p.envelope.depth,0);
});
test('PostgreSQL roundtrip, replay, changes, missing and returns preserve stable IDs; zero decision rows',async()=>{
 const db=new PGlite();try{await db.exec(schema);let parent=null;const results=[];
 for(const [day,ids] of [['2026-11-02',['1','2']],['2026-11-03',['1','2']],['2026-11-04',['1','3']],['2026-11-05',['1','2']]]){
  const records=rows(ids),f=fixture(records,day);await importStage(db,raw(records,day),{compactSelection:true});
  if(day==='2026-11-03'){
    const diag=(await db.query('SELECT diagnostics FROM ontap_shadow.feed_runs WHERE id=$1',[runId(f)])).rows[0].diagnostics;
    assert.equal(diag.compact_raw_budget.changedAdverts,0);assert.equal(diag.selection_status,'pending');
  }
  const result=await attachCompactSelection(db,{runId:runId(f),fixture:f,context:{...context,timeContext:day},parentRunId:parent});results.push(result);
  const before=await counts(db);assert.equal(before.selection_decisions,0);
  assert.equal((await attachCompactSelection(db,{runId:runId(f),fixture:f,context:{...context,timeContext:day},parentRunId:parent})).replayed,true);assert.deepEqual(await counts(db),before);
  assert.deepEqual((await readCompactSelection(db,runId(f))).state,canonicalSelection(f,{...context,timeContext:day}));parent=runId(f);
 }
 await assert.rejects(importStage(db,raw(rows(['9']),'2026-11-01'),{compactSelection:true}),/Older compact snapshot/);
 assert.equal(results[1].changedDecisions,0);assert.equal(results[2].changedDecisions,8);
 assert.equal((await counts(db)).jobs,3);assert.equal((await counts(db)).selection_decisions,0);
 const first=fixture(rows(['1','2']),'2026-11-02');assert.equal((await readCompactSelection(db,runId(first))).state.decisions.length,16);
 assert.equal((await db.query("SELECT public_id FROM ontap_shadow.jobs WHERE public_id='2'")).rows[0].public_id,'2');
 const conflict=structuredClone(first);conflict.decisions[0].reason='Conflicting';await assert.rejects(attachCompactSelection(db,{runId:runId(first),fixture:conflict,context}),/Conflicting compact replay/);
 }finally{await db.close();}
});
test('raw mismatch, partial mode and storage rejection leave compact history unattached',async()=>{
 const db=new PGlite();try{await db.exec(schema);const records=rows(['1']),f=fixture(records,'2026-11-02');
 await importStage(db,raw(records,'2026-11-02'),{compactSelection:true});
 const bad=structuredClone(f);bad.sourceHashes[0][1]='0'.repeat(64);
 await assert.rejects(attachCompactSelection(db,{runId:runId(f),fixture:bad,context}),/raw advert differs/);
 const near={query(sql,args){if(sql.includes('pg_database_size'))return Promise.resolve({rows:[{n:String(800*1024*1024-1024)}]});return db.query(sql,args);}};
 await assert.rejects(attachCompactSelection(near,{runId:runId(f),fixture:f,context}),/preflight/);
 assert.equal((await db.query('SELECT diagnostics FROM ontap_shadow.feed_runs WHERE id=$1',[runId(f)])).rows[0].diagnostics.compact_selection,undefined);
 await assert.rejects(importStage(db,{...raw(records,'2026-11-03'),percentage:20},{compactSelection:true}),/full snapshot/);
 }finally{await db.close();}
});

test('compact appearance manifests retain exact daily gaps/returns and compact display roundtrips through database',async()=>{
 const {readAppearances,encodeAppearances,decodeAppearances}=await import('./appearance-manifest.mjs');
 const {encodeCompactDisplay,decodeCompactDisplay,attachCompactDisplay,readCompactDisplay}=await import('./display-snapshot.mjs');
 const db=new PGlite();try{await db.exec(schema);let parent=null;const runs=[];
 for(const [day,ids] of [['2026-11-02',['1','2']],['2026-11-03',['1','3']],['2026-11-04',['1','2']]]){
  const records=rows(ids),f=fixture(records,day);
  f.decisions[0]={...f.decisions[0],decision:'include',regions:['Test']};
  const outputs={['admin_service:Test']:[{job_id:'1',title:'Administrator',apply_url:'https://example.org/1',salary_text:'Salary not stated'}]};
  f.report.outputsSha256=contentHash(outputs);
  await importStage(db,raw(records,day),{compactSelection:true});const id=runId(f);runs.push(id);
  await attachCompactSelection(db,{runId:id,fixture:f,context,parentRunId:parent});
  assert.deepEqual(await readAppearances(db,id),{date:day,refs:ids});
  assert.equal((await counts(db)).advert_appearances,0);
  assert.equal((await attachCompactDisplay(db,id,outputs)).replayed,false);
  assert.equal((await attachCompactDisplay(db,id,outputs)).replayed,true);
  assert.deepEqual(await readCompactDisplay(db,id),outputs);
  const {archiveCompactDisplay}=await import('./display-archive.mjs');const objects=new Map();
  const archived=await archiveCompactDisplay(db,id,{async putIfAbsent(k,v){if(!objects.has(k))objects.set(k,v);},async get(k){return objects.get(k);}});
  assert.equal(archived.readbackVerified,true);assert.deepEqual(await readCompactDisplay(db,id),outputs);

  const state=(await readCompactSelection(db,id)).state,packed=encodeCompactDisplay(outputs,state);
  assert.deepEqual(decodeCompactDisplay(packed,state),outputs);
  assert.throws(()=>decodeCompactDisplay({...packed,outputsSha256:'0'.repeat(64)},state),/Corrupt/);
  parent=id;
 }
 assert.deepEqual((await readAppearances(db,runs[0])).refs,['1','2']);
 assert.deepEqual((await readAppearances(db,runs[1])).refs,['1','3']);
 const corrupt=encodeAppearances(['1']);corrupt.sha256='0'.repeat(64);assert.throws(()=>decodeAppearances(corrupt),/Corrupt/);
 assert.throws(()=>encodeAppearances(['1','1']),/Duplicate/);
 }finally{await db.close();}
});
