import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {PGlite} from '@electric-sql/pglite';
import {attachSelection,PIN} from './selection-importer.mjs';
import {importStage} from './staged-importer.mjs';
import {contentHash,counts} from './importer.mjs';
const schema=await fs.readFile(new URL('../001_initial.sql',import.meta.url),'utf8');
const records=Array.from({length:3},(_,i)=>({'/Job/DisplayReference':String(i),'/Job/Position':'Administrator','/Job/ApplicationURL':'https://example.org/'+i}));
const families=['admin_service','support_worker','customer_sales','finance_accounts','hr_recruitment','marketing','legal_assistant_paralegal','customer_service_contact_centre'];
const fixture=()=>({report:{archiveSha256:PIN,exactFileOutputParity:true,unknowns:0,rulesRevision:'b'.repeat(40),cleanRecords:3,outputsSha256:'c'.repeat(64)},sourceHashes:records.map(r=>[r['/Job/DisplayReference'],contentHash(r)]),decisions:families.flatMap(f=>records.map((r,i)=>({ref:r['/Job/DisplayReference'],scope:'production:'+f,decision:['include','review','exclude'][i],reason:'Actual production reason '+i,gate:'Observed gate',regions:i===0?['Test region']:[]})))});
const raw={records,observedOn:'2026-11-02',percentage:100,archiveSha256:PIN,sourceRevision:'a'.repeat(40),totalReceived:3,rawPayloadBytes:1000,maximumDatabaseBytes:800*1024*1024};
test('exact decisions persist, repeat adds nothing, jobs remain withheld, conflicting evidence fails',async()=>{
 const db=new PGlite();try{
 await db.exec(schema);await importStage(db,raw);
 const f=fixture();const result=await attachSelection(db,f);assert.equal(result.decisionCount,24);
 const before=await counts(db);assert.equal((await attachSelection(db,f)).replayed,true);assert.deepEqual(await counts(db),before);
 assert.equal((await db.query("SELECT count(*)::int AS n FROM ontap_shadow.jobs WHERE publication_status='withheld'")).rows[0].n,3);
 const bad=fixture();bad.decisions[0].reason='Changed';await assert.rejects(attachSelection(db,bad),/Conflicting selector replay/);
 assert.deepEqual(await counts(db),before);
 }finally{await db.close();}
});
test('different database content rolls back before attaching decisions',async()=>{
 const db=new PGlite();try{await db.exec(schema);await importStage(db,raw);const before=await counts(db);
 await db.query("UPDATE ontap_shadow.supplier_adverts SET content_hash='wrong' WHERE supplier_job_id='1'");
 await assert.rejects(attachSelection(db,fixture()),/differs from pinned/);assert.deepEqual(await counts(db),before);
 }finally{await db.close();}
});
test('unknown, duplicate and wrong archive evidence rejected before database access',async()=>{
 const db={query(){throw new Error('Database must not be touched');}};
 let f=fixture();f.report.unknowns=1;await assert.rejects(attachSelection(db,f),/Incomplete/);
 f=fixture();f.decisions[1]=f.decisions[0];await assert.rejects(attachSelection(db,f),/Duplicate/);
 f=fixture();f.report.archiveSha256='d'.repeat(64);await assert.rejects(attachSelection(db,f),/Wrong pinned/);
});

test('storage ceiling stops attachment before BEGIN or writes',async()=>{
 let calls=0;
 const client={async query(sql){calls++;if(sql.includes('pg_database_size'))return {rows:[{n:String(800*1024*1024)}]};if(sql.includes('pg_class'))return {rows:[]};throw new Error('Write reached');}};
 await assert.rejects(attachSelection(client,fixture()),/storage preflight exceeds ceiling/);
 assert.equal(calls,2);
});
