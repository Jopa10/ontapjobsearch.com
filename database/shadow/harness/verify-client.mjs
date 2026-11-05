import assert from 'node:assert/strict';
import { importSample, importBatch, counts } from './importer.mjs';

function dayAfter(day, delta) {
  const value = new Date(`${day}T00:00:00Z`);
  value.setUTCDate(value.getUTCDate() + delta);
  return value.toISOString().slice(0,10);
}
async function advert(client,id) {
  return (await client.query(`SELECT a.id,a.job_id,j.public_id,a.title,a.content_hash,
    a.first_seen::text,a.last_seen::text,a.inactive_since::text,a.availability
    FROM ontap_shadow.supplier_adverts a JOIN ontap_shadow.jobs j ON j.id=a.job_id
    JOIN ontap_shadow.suppliers s ON s.id=a.supplier_id WHERE s.code='jobg8' AND a.supplier_job_id=$1`,[id])).rows[0];
}

export async function verifySample(client,fixture) {
  const tables=(await client.query(`SELECT table_name FROM information_schema.tables WHERE table_schema='ontap_shadow' AND table_type='BASE TABLE'`)).rows;
  assert.equal(tables.length,12,'Expected the agreed 12-table test schema');
  const before=await counts(client);
  const first=await importSample(client,fixture);
  const imported=await counts(client);
  const repeat=await importSample(client,fixture);
  assert.equal(repeat.replayed,true);
  assert.deepEqual(await counts(client),imported,'Repeat import must not add records');
  const ref=fixture.records[0].job_id;
  const original=await advert(client,ref);
  assert.equal(original.public_id,ref);
  const originalDays=(await client.query(`SELECT seen_on::text FROM ontap_shadow.advert_appearances WHERE advert_id=$1 ORDER BY seen_on`,[original.id])).rows.map(r=>r.seen_on);
  assert(originalDays.includes(fixture.observedOn));
  const nextDay=dayAfter(fixture.observedOn,1);
  const returnDay=dayAfter(fixture.observedOn,3);
  await client.query('BEGIN');
  try {
    await importBatch(client,{...fixture,observedOn:nextDay,feedKey:fixture.feedKey+'-verify-unchanged'});
    const unchanged=await advert(client,ref);
    assert.equal(unchanged.content_hash,original.content_hash);
    assert.equal(unchanged.job_id,original.job_id);
    assert.equal(unchanged.first_seen,original.first_seen);
    assert.equal(unchanged.last_seen,nextDay);
    // Simulate an advert being made inactive by a FUTURE full-feed policy.
    // The sample importer itself never infers absence/expiry from a partial batch.
    await client.query(`UPDATE ontap_shadow.supplier_adverts SET availability='missing',inactive_since=$2 WHERE id=$1`,[original.id,nextDay]);
    const changed=structuredClone(fixture);
    changed.records[0].title += ' [rollback-only update test]';
    changed.observedOn=returnDay;
    changed.feedKey += '-verify-return';
    await importBatch(client,changed);
    const returned=await advert(client,ref);
    assert.equal(returned.id,original.id);
    assert.equal(returned.job_id,original.job_id);
    assert.equal(returned.public_id,original.public_id);
    assert.equal(returned.first_seen,original.first_seen);
    assert.equal(returned.last_seen,returnDay);
    assert.notEqual(returned.content_hash,original.content_hash);
    assert.equal(returned.availability,'seen');
    assert.equal(returned.inactive_since,null);
    const days=(await client.query(`SELECT seen_on::text FROM ontap_shadow.advert_appearances WHERE advert_id=$1 ORDER BY seen_on`,[original.id])).rows.map(r=>r.seen_on);
    assert.deepEqual(days,[...new Set([...originalDays,nextDay,returnDay])].sort());
    assert(!days.includes(dayAfter(fixture.observedOn,2)),'Missing day must stay a gap');
    assert.equal((await counts(client)).jobs,imported.jobs);
  } finally {
    await client.query('ROLLBACK');
  }
  assert.deepEqual(await advert(client,ref),original,'Test changes must be rolled back');
  assert.deepEqual(await counts(client),imported);
  // A changed payload under an already accepted feed key must fail atomically.
  const conflicting=structuredClone(fixture);
  conflicting.records[0].title += ' conflicting content';
  await assert.rejects(importSample(client,conflicting),/Feed identity already used/);
  assert.deepEqual(await counts(client),imported);
  return {
    status:'passed',sampleSize:fixture.records.length,sourceRevision:fixture.sourceRevision,
    sampleObservedOn:fixture.observedOn,firstImportWasReplay:first.replayed,
    before,after:imported,
    checks:['12 tables','sample persisted','replay adds no duplicates','unchanged advert keeps hash and identity',
      'changed advert updates in place','stable public URL ID','gap remains visible','return clears inactivity',
      'verification changes rolled back','conflicting replay rejected atomically'],
    scope:'Published JobG8 sample only; full raw-feed import, exclusion reasoning and expiry policy not tested.'
  };
}
