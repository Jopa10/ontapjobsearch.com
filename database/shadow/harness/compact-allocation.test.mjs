import {test} from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs/promises';
import {PGlite} from '@electric-sql/pglite';
import {measureCompactAllocation} from './compact-allocation.mjs';
const schema=await fs.readFile(new URL('../001_initial.sql',import.meta.url),'utf8');
test('normal heap/TOAST allocation readback rolls back table and preserves existing rows',async()=>{
 const db=new PGlite();try{await db.exec(schema);await db.query("INSERT INTO ontap_shadow.suppliers(code,name) VALUES('untouched','Existing supplier')");
 const records=[{probeOnly:true,payload:'abc'.repeat(10000)},{probeOnly:true,payload:'xyz'.repeat(10000)}];
 const result=await measureCompactAllocation(db,records);
 assert.equal(result.probeRolledBack,true);assert.equal(result.existingRowCountsUnchanged,true);
 assert.equal(result.snapshots.length,2);assert.ok(Number(result.snapshots[1].relation.total_bytes)>0);
 assert.equal((await db.query("SELECT name FROM ontap_shadow.suppliers WHERE code='untouched'")).rows[0].name,'Existing supplier');
 }finally{await db.close();}
});
test('preflight ceiling rejects without starting a write transaction',async()=>{
 const db=new PGlite();try{await db.exec(schema);const sql=[];
 const client={query(q,p){sql.push(q);if(q.includes('pg_database_size'))return Promise.resolve({rows:[{n:'838860799'}]});return db.query(q,p);}};
 await assert.rejects(measureCompactAllocation(client,[{payload:'x'}]),/preflight/);
 assert.ok(!sql.includes('BEGIN'));assert.ok(!sql.some(q=>q.startsWith('CREATE')));
 }finally{await db.close();}
});
test('failed readback rolls back and removes probe relation',async()=>{
 const db=new PGlite();try{await db.exec(schema);
 const client={query(q,p){if(q.startsWith('SELECT diagnostics FROM ontap_shadow.compact_allocation_probe'))return Promise.resolve({rows:[{diagnostics:{corrupt:true}}]});return db.query(q,p);}};
 await assert.rejects(measureCompactAllocation(client,[{payload:'valid'}]),/readback mismatch/);
 assert.equal((await db.query("SELECT to_regclass('ontap_shadow.compact_allocation_probe')::text AS name")).rows[0].name,null);
 }finally{await db.close();}
});
test('pre-existing probe relation is preserved, never replaced',async()=>{
 const db=new PGlite();try{await db.exec(schema);await db.exec("CREATE TABLE ontap_shadow.compact_allocation_probe(marker text);INSERT INTO ontap_shadow.compact_allocation_probe VALUES('keep')");
 await assert.rejects(measureCompactAllocation(db,[{payload:'x'}]),/Existing probe/);
 assert.equal((await db.query('SELECT marker FROM ontap_shadow.compact_allocation_probe')).rows[0].marker,'keep');
 }finally{await db.close();}
});
