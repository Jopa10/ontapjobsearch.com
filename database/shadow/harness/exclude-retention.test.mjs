import test from 'node:test';
import assert from 'node:assert/strict';
import {PGlite} from '@electric-sql/pglite';
import {applyExcludeReviewWindow} from './exclude-retention.mjs';
import {encodeAppearances} from './appearance-manifest.mjs';
async function fixture(){
 const db=new PGlite();
 await db.exec(`CREATE SCHEMA ontap_shadow;
 CREATE TABLE ontap_shadow.feed_runs(id int PRIMARY KEY,supplier_id int,feed_date date,status text,diagnostics jsonb);
 CREATE TABLE ontap_shadow.supplier_adverts(supplier_id int,supplier_job_id text,raw_payload jsonb,exclude_review_started_on date,content_purged_at timestamptz);
 INSERT INTO ontap_shadow.supplier_adverts VALUES(1,'excluded','{"title":"exclude fixture"}',NULL,NULL),(1,'retained','{"title":"retain fixture"}',NULL,NULL);`);
 const c={query:async(sql,args=[])=>{const x=await db.query(sql,args);return {...x,rowCount:x.affectedRows??x.rows.length}}};
 await c.query('INSERT INTO ontap_shadow.feed_runs VALUES(1,1,$1,\'accepted\',$2::jsonb)',['2026-11-17',JSON.stringify({selection_status:'verified',compact_appearances:encodeAppearances(['excluded','retained'])})]);
 return {db,c};
}
test('EXCLUDE full payload survives day two and is purged at three-day boundary, retaining other adverts',async()=>{
 const {db,c}=await fixture();
 try{
  const first=await applyExcludeReviewWindow(c,{runId:1,fullyExcludedRefs:['excluded'],asOfDate:'2026-11-17'});
  assert.equal(first.purgedCount,0);
  const day2=await applyExcludeReviewWindow(c,{runId:1,fullyExcludedRefs:['excluded'],asOfDate:'2026-11-19'});
  assert.equal(day2.purgedCount,0);
  const day3=await applyExcludeReviewWindow(c,{runId:1,fullyExcludedRefs:['excluded'],asOfDate:'2026-11-20'});
  assert.deepEqual(day3.purgedRefs,['excluded']);
  const kept=(await c.query("SELECT raw_payload FROM ontap_shadow.supplier_adverts WHERE supplier_job_id='retained'")).rows[0];
  assert.ok(kept.raw_payload);
  const again=await applyExcludeReviewWindow(c,{runId:1,fullyExcludedRefs:['excluded'],asOfDate:'2026-11-20'});
  assert.equal(again.purgedCount,0);
 }finally{await db.close();}
});
test('returning eligible advert clears exclusion timer before purge',async()=>{
 const {db,c}=await fixture();
 try{
  await applyExcludeReviewWindow(c,{runId:1,fullyExcludedRefs:['excluded'],asOfDate:'2026-11-17'});
  const result=await applyExcludeReviewWindow(c,{runId:1,fullyExcludedRefs:[],asOfDate:'2026-11-20'});
  assert.equal(result.purgedCount,0);
  const row=(await c.query("SELECT raw_payload,exclude_review_started_on FROM ontap_shadow.supplier_adverts WHERE supplier_job_id='excluded'")).rows[0];
  assert.ok(row.raw_payload);assert.equal(row.exclude_review_started_on,null);
 }finally{await db.close();}
});
test('unverified feed or excluded ID outside exact feed membership is rejected without payload loss',async()=>{
 const {db,c}=await fixture();
 try{
  await assert.rejects(applyExcludeReviewWindow(c,{runId:1,fullyExcludedRefs:['outside'],asOfDate:'2026-11-20'}));
  const rows=(await c.query('SELECT raw_payload FROM ontap_shadow.supplier_adverts')).rows;
  assert.ok(rows.every(r=>r.raw_payload));
 }finally{await db.close();}
});
