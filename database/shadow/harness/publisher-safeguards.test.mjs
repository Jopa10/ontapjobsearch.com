import test from 'node:test';
import assert from 'node:assert/strict';
import {requirePreview,requireBudget,packSnapshot,unpackSnapshot,requireSameDay,MAX,RESERVE} from './publisher-safeguards.mjs';
const env={VERCEL_ENV:'preview',ONTAP_SHADOW_NEON_PROJECT_ID:'noisy-fire-97386602',ONTAP_SHADOW_DATABASE_URL:'postgresql://test:test@fixture.neon.tech/db?sslmode=verify-full'};
test('reject production environment, wrong project and missing TLS before connecting',()=>{
 assert.equal(requirePreview(env),true);
 for(const delta of [{VERCEL_ENV:'production'},{ONTAP_SHADOW_NEON_PROJECT_ID:'other'},{ONTAP_SHADOW_DATABASE_URL:'postgresql://test:test@fixture.neon.tech/db'}])
  assert.throws(()=>requirePreview({...env,...delta}));
});
test('storage reserve blocks oversized input',()=>{
 requireBudget(668901376,5000000);
 assert.throws(()=>requireBudget(MAX-RESERVE,1));
});
test('reject stale date across a daily rollover',()=>{
 requireSameDay('2026-11-18','2026-11-18');
 assert.throws(()=>requireSameDay('2026-11-17','2026-11-18'));
});
test('compressed snapshot preserves exact IDs payloads and positions; corrupt data is rejected',()=>{
 const rows=[{scope:'a',position:0,public_id:'1',display:{title:'Office admin',apply_url:'https://example.test/a'}},{scope:'a',position:1,public_id:'2',display:{title:'Receptionist'}}];
 const p=packSnapshot(rows);
 assert.deepEqual(unpackSnapshot(p.packed,p.sha256),rows);
 assert.throws(()=>unpackSnapshot(p.packed,'0'.repeat(64)));
 const corrupt=Buffer.from(p.packed);corrupt[10]^=255;
 assert.throws(()=>unpackSnapshot(corrupt,p.sha256));
});
