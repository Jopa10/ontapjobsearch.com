// Explicit allocation calibration only. Every probe write is rolled back.
import assert from 'node:assert/strict';
import {contentHash,counts} from './importer.mjs';
import {measure,DEFAULT_BUDGET} from './staged-importer.mjs';
const TABLE='ontap_shadow.compact_allocation_probe';
export async function measureCompactAllocation(client,records,{maximumBytes=DEFAULT_BUDGET}={}){
 assert.ok(Array.isArray(records)&&records.length>=1&&records.length<=7);
 assert.ok(maximumBytes>0&&maximumBytes<=DEFAULT_BUDGET);
 const reserve=64*1024*1024;
 const encodedBytes=records.reduce((n,r)=>n+Buffer.byteLength(JSON.stringify(r)),0);
 assert.ok(encodedBytes>0&&encodedBytes<64*1024*1024,'Probe size bound');
 const before=await measure(client),beforeCounts=await counts(client);
 assert.ok(before.databaseBytes+encodedBytes*3+reserve<maximumBytes,'Probe storage preflight exceeds reserved ceiling');
 let result,transaction=false;
 try{
  await client.query('BEGIN');transaction=true;
  await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
  assert.equal((await client.query('SELECT to_regclass($1)::text AS name',[TABLE])).rows[0].name,null,'Existing probe table; refuse to touch it');
  const locked=await measure(client);
  assert.ok(locked.databaseBytes+encodedBytes*3+reserve<maximumBytes,'Locked probe preflight exceeds reserved ceiling');
  // Separate normal heap/TOAST: never UPDATE/DELETE existing Ontap data.
  await client.query(`CREATE TABLE ${TABLE}(sequence integer PRIMARY KEY,diagnostics jsonb NOT NULL)`);
  const snapshots=[];
  for(let i=0;i<records.length;i++){
   await client.query(`INSERT INTO ${TABLE}(sequence,diagnostics) VALUES($1,$2::jsonb)`,[i,JSON.stringify(records[i])]);
   const stored=(await client.query(`SELECT diagnostics FROM ${TABLE} WHERE sequence=$1`,[i])).rows[0].diagnostics;
   assert.equal(contentHash(stored),contentHash(records[i]),'Probe readback mismatch');
   const relation=(await client.query(`SELECT pg_relation_size($1::regclass)::text AS heap_bytes,pg_table_size($1::regclass)::text AS table_with_toast_bytes,pg_indexes_size($1::regclass)::text AS index_bytes,pg_total_relation_size($1::regclass)::text AS total_bytes`,[TABLE])).rows[0];
   const allocated=await measure(client);
   assert.ok(allocated.databaseBytes+reserve<maximumBytes,'Measured probe exceeds reserved ceiling');
   snapshots.push({snapshots:i+1,encodedBytes:Buffer.byteLength(JSON.stringify(records[i])),relation,databaseBytes:allocated.databaseBytes});
  }
  assert.deepEqual(await counts(client),beforeCounts,'Existing importer-owned row counts changed');
  result={before,encodedBytes,snapshots,probeRows:records.length,exactJsonbReadback:true};
 }finally{
  if(transaction)await client.query('ROLLBACK');
 }
 assert.equal((await client.query('SELECT to_regclass($1)::text AS name',[TABLE])).rows[0].name,null,'Probe table survived rollback');
 assert.deepEqual(await counts(client),beforeCounts,'Counts differ after rollback');
 result.afterRollback=await measure(client);result.probeRolledBack=true;result.existingRowCountsUnchanged=true;
 result.databaseAllocationDeltaAfterRollback=result.afterRollback.databaseBytes-before.databaseBytes;
 result.limitations='Normal PostgreSQL heap/index/TOAST calibration in a rolled-back probe table. Not a fresh-feed import or exact allocation in feed_runs. Catalog/WAL allocation may change after rollback; no vacuum or reclaimed-space claim.';
 return result;
}
