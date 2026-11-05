import {test} from 'node:test';import assert from 'node:assert/strict';
import {canonicalSelection,FAMILIES} from './selection-history.mjs';import {encodeCompactDisplay} from './display-snapshot.mjs';import {encodeAppearances} from './appearance-manifest.mjs';import {makeDisplayArchive,restoreDisplayArchive,verifyArchiveStorage,planDisplayRetention} from './display-archive.mjs';import {contentHash} from './importer.mjs';
const context={selectorRevision:'a'.repeat(40),registersSha256:'b'.repeat(64),geographySha256:'c'.repeat(64),configurationSha256:'d'.repeat(64),scopeRegistrySha256:'e'.repeat(64),timeContext:'test'};
function input(){const outputs={'admin_service:Test':[{job_id:'1',title:'Admin',apply_url:'https://example.org/1',salary_text:'DOE'}]};
 const state=canonicalSelection({report:{exactFileOutputParity:true,unknowns:0,rulesRevision:context.selectorRevision,archiveSha256:'f'.repeat(64),outputsSha256:contentHash(outputs),cleanRecords:1},sourceHashes:[['1','0'.repeat(64)]],decisions:FAMILIES.map((f,i)=>({ref:'1',scope:'production:'+f,decision:i?'exclude':'include',reason:'Actual reason',gate:'Gate',regions:i?[]:['Test']}))},context);
 return {runId:'11111111-1111-5111-8111-111111111111',feedDate:'2026-11-02',state,display:encodeCompactDisplay(outputs,state),appearances:encodeAppearances(['1'])};}
test('archive restore is self-contained and exact; immutable provider readback required',async()=>{const x=input(),objects=new Map();const store={async putIfAbsent(k,v){if(!objects.has(k))objects.set(k,v);},async get(k){return objects.get(k);}};
 const receipt=await verifyArchiveStorage(x,store);assert.equal(receipt.readbackVerified,true);assert.deepEqual(restoreDisplayArchive(await store.get(receipt.key),receipt).state,x.state);
 assert.deepEqual(await verifyArchiveStorage(x,store),receipt);assert.equal(objects.size,1);
});
test('corrupt bytes, wrong run and incomplete readback cannot verify archive',async()=>{const x=input(),a=makeDisplayArchive(x);assert.throws(()=>restoreDisplayArchive(Buffer.from('bad'),a.receipt));assert.throws(()=>restoreDisplayArchive(a.bytes,{...a.receipt,runId:'wrong'}));
 await assert.rejects(verifyArchiveStorage(x,{async putIfAbsent(){},async get(){return Buffer.from('bad');}}));
});
test('retention dry-run keeps latest seven days and blocks missing or wrong receipts',()=>{const x=input(),a=makeDisplayArchive(x).receipt;const old={runId:x.runId,feedDate:x.feedDate,displayBytes:6000000,outputsSha256:a.outputsSha256,selectionStateSha256:a.selectionStateSha256};const latest={...old,runId:'latest',feedDate:'2026-11-12'};
 let p=planDisplayRetention([old,latest],{asOf:'2026-11-12'});assert.deepEqual(p.blocked,[old.runId]);assert.equal(p.cleanupAuthorized,false);
 p=planDisplayRetention([{...old,archive:{...a,readbackVerified:true}},latest],{asOf:'2026-11-12'});assert.deepEqual(p.candidates,[old.runId]);assert.deepEqual(p.kept,['latest']);
 assert.throws(()=>planDisplayRetention([old],{asOf:'2026-11-12',keepDays:1}));
});
