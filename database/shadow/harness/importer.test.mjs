import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { PGlite } from '@electric-sql/pglite';
import { importSample, importBatch, counts, stableId } from './importer.mjs';
import { verifySample } from './verify-client.mjs';
const schema=await fs.readFile(new URL('../001_initial.sql',import.meta.url),'utf8');
const fixture=JSON.parse(await fs.readFile(new URL('./sample.json',import.meta.url),'utf8'));

async function database() {
  const db=new PGlite();
  await db.exec(schema);
  return db;
}

test('20 real adverts: replay, update, gap, return and rollback against PostgreSQL',async()=>{
  const db=await database();
  try {
    const report=await verifySample(db,fixture);
    assert.equal(report.status,'passed');
    assert.equal(report.after.jobs,20);
    assert.equal(report.after.supplier_adverts,20);
    assert.equal(report.after.advert_appearances,20);
    assert.equal(report.after.selection_decisions,20);
    assert.equal(report.after.feed_runs,1);
  } finally {await db.close();}
});

test('bad input rolls back supplier/run/adverts, and older snapshots fail closed',async()=>{
  const db=await database();
  try {
    const broken=structuredClone(fixture);
    broken.records[1].job_id=broken.records[0].job_id;
    await assert.rejects(importSample(db,broken),/Duplicate/);
    assert.equal((await counts(db)).jobs,0);
    await importSample(db,fixture);
    const before=await counts(db);
    await assert.rejects(importSample(db,{...fixture,feedKey:'old',observedOn:'2026-11-01'}),/Older snapshot/);
    assert.deepEqual(await counts(db),before);
  } finally {await db.close();}
});

test('database rejects broken links and unevidenced completed applications',async()=>{
  const db=await database();
  try {
    await importSample(db,fixture);
    const rows=(await db.query('SELECT id,preferred_advert_id FROM ontap_shadow.jobs ORDER BY public_id LIMIT 2')).rows;
    await assert.rejects(db.query('UPDATE ontap_shadow.jobs SET preferred_advert_id=$1 WHERE id=$2',[rows[1].preferred_advert_id,rows[0].id]));
    await assert.rejects(db.query(`INSERT INTO ontap_shadow.activity_events(id,event_type,occurred_at,job_id) VALUES($1,'application_confirmed',now(),$2)`,[stableId('bad-conversion'),rows[0].id]));
    await db.query(`INSERT INTO ontap_shadow.activity_events(id,event_type,occurred_at,job_id) VALUES($1,'apply_click',now(),$2)`,[stableId('apply-click'),rows[0].id]);
    assert.equal((await db.query("SELECT count(*)::int AS n FROM ontap_shadow.activity_events WHERE event_type='application_confirmed'")).rows[0].n,0);
  } finally {await db.close();}
});

test('same-day new snapshots do not duplicate appearances and partial samples do not expire other jobs',async()=>{
  const db=await database();
  try {
    await importSample(db,fixture);
    await importSample(db,{...fixture,records:fixture.records.slice(0,1),feedKey:fixture.feedKey+'-partial'});
    assert.equal((await counts(db)).advert_appearances,20);
    assert.equal((await db.query("SELECT count(*)::int AS n FROM ontap_shadow.supplier_adverts WHERE availability='seen'")).rows[0].n,20);
  } finally {await db.close();}
});
