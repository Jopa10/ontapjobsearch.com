import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {PGlite} from '@electric-sql/pglite';
import {budgetGate,importStage} from './staged-importer.mjs';
import {counts} from './importer.mjs';
const schema=await fs.readFile(new URL('../001_initial.sql',import.meta.url),'utf8');
const records=Array.from({length:100},(_,i)=>({'/Job/DisplayReference':String(i),'/Job/Position':'Administrator '+i,
  '/Job/ApplicationURL':'https://example.org/apply/'+i,'/Job/AdvertiserName':'Example Employer',
  '/Job/Description':'Office duties '.repeat(100),'/Job/SalaryMinimum':'25000'}));
const fixture=p=>({records:records.slice(0,p),observedOn:'2026-11-02',percentage:p,totalReceived:100,
  archiveSha256:'a'.repeat(64),sourceRevision:'test',rawPayloadBytes:10000,maximumDatabaseBytes:800*1024*1024});

test('20→50→100 stores a nested raw feed without duplicate jobs or appearances',async()=>{
 const db=new PGlite();try{
 await db.exec(schema);
 for(const percentage of [20,50,100]){
  const input=fixture(percentage);
  await importStage(db,input,{chunkSize:7});
  const current=await counts(db);
  assert.equal(current.jobs,percentage);
  assert.equal(current.supplier_adverts,percentage);
  assert.equal(current.advert_appearances,percentage);
  assert.equal((await importStage(db,input)).replayed,true);
  assert.deepEqual(await counts(db),current);
 }
 assert.equal((await db.query("SELECT count(*)::int AS n FROM ontap_shadow.selection_decisions WHERE decision='unknown'")).rows[0].n,170);
 assert.equal((await db.query("SELECT count(*)::int AS n FROM ontap_shadow.jobs WHERE publication_status='withheld'")).rows[0].n,100);
 }finally{await db.close();}
});
test('storage ceiling rejects before any records are written',async()=>{
 assert.throws(()=>budgetGate(790*1024*1024,50*1024*1024,1000),/ceiling/);
 const db=new PGlite();try{
 await db.exec(schema);
 await assert.rejects(importStage(db,{...fixture(20),maximumDatabaseBytes:1}),/ceiling/);
 assert.equal((await counts(db)).suppliers,0);
 }finally{await db.close();}
});
test('wrong fractions, duplicate IDs and conflicting replay are rejected atomically',async()=>{
 const db=new PGlite();try{
 await db.exec(schema);
 await assert.rejects(importStage(db,{...fixture(20),records:records.slice(0,19)}),/fraction/);
 const duplicate=structuredClone(fixture(20));duplicate.records[1]=duplicate.records[0];
 await assert.rejects(importStage(db,duplicate),/Duplicate/);
 await importStage(db,fixture(20));
 const before=await counts(db);
 const changed=structuredClone(fixture(20));changed.records[0]['/Job/Position']='Changed';
 await assert.rejects(importStage(db,changed),/Conflicting/);
 assert.deepEqual(await counts(db),before);
 }finally{await db.close();}
});
