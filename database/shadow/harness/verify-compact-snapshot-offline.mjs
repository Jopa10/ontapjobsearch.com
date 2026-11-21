import {verifyArchiveStorage,restoreDisplayArchive} from './display-archive.mjs';
import path from 'node:path';
// Reuses saved artifacts; no supplier, database or selector execution.
import fs from 'node:fs/promises';import assert from 'node:assert/strict';import {gunzipSync} from 'node:zlib';import {createHash} from 'node:crypto';
import {canonicalSelection} from './selection-history.mjs';import {encodeAppearances,decodeAppearances} from './appearance-manifest.mjs';import {encodeCompactDisplay,decodeCompactDisplay} from './display-snapshot.mjs';import {contentHash} from './importer.mjs';
const bytes=await fs.readFile(process.argv[2]);assert.equal(createHash('sha256').update(bytes).digest('hex'),'7eb9b15fe9bbeb0334d179d282af5431cb41c93125d909c4209d73aacaf9c58a');
const fixture=JSON.parse(gunzipSync(bytes,{maxOutputLength:256*1024*1024}));
const receipt=JSON.parse(await fs.readFile(new URL('../selection-verification-2026-11-02.json',import.meta.url)));
assert.equal(fixture.report.archiveSha256,receipt.archiveSha256);assert.equal(fixture.report.outputsSha256,receipt.outputsSha256);
const outputs=JSON.parse(await fs.readFile(process.argv[3]));assert.equal(contentHash(outputs),receipt.outputsSha256);
const context={selectorRevision:fixture.report.rulesRevision,registersSha256:'1'.repeat(64),geographySha256:'2'.repeat(64),configurationSha256:'3'.repeat(64),scopeRegistrySha256:'4'.repeat(64),timeContext:'synthetic local storage verification only'};
const state=canonicalSelection(fixture,context);const membership=encodeAppearances(fixture.sourceHashes.map(x=>x[0]));assert.deepEqual(decodeAppearances(membership),fixture.sourceHashes.map(x=>x[0]).sort());
const display=encodeCompactDisplay(outputs,state);assert.deepEqual(decodeCompactDisplay(display,state),outputs);
const result={testedAt:new Date().toISOString(),sourceSelectionArtifact:13184005546,sourceDisplayArtifact:13183730978,sourceRun:41530087079,outputsSha256:receipt.outputsSha256,advertCount:membership.count,regionalOutputs:Object.keys(outputs).length,displayEntries:Object.values(outputs).reduce((n,r)=>n+r.length,0),appearanceEncodedBytes:Buffer.byteLength(JSON.stringify(membership)),displayEncodedBytes:Buffer.byteLength(JSON.stringify(display)),exactAppearanceReadback:true,exactDisplayReadback:true,neonWrites:false,productionChanged:false,scope:'Local complete saved-snapshot codec verification, synthetic dependency context; no current turnover or Neon allocation proof'};
if(process.argv[5]){
 const folder=process.argv[5];await fs.mkdir(folder,{recursive:true});
 const store={async putIfAbsent(key,bytes){const target=path.join(folder,key);await fs.mkdir(path.dirname(target),{recursive:true});try{await fs.writeFile(target,bytes,{flag:'wx'});}catch(e){if(e.code!=='EEXIST')throw e;}},async get(key){return fs.readFile(path.join(folder,key));}};
 const archive=await verifyArchiveStorage({runId:'11111111-1111-5111-8111-111111111111',feedDate:'2026-11-02',state,display,appearances:membership},store);
 const restored=restoreDisplayArchive(await store.get(archive.key),archive);
 assert.deepEqual(restored.outputs,outputs);assert.deepEqual(restored.state,state);
 result.archive={...archive,storageVerification:'local immutable-file adapter only; remote provider not configured',syntheticRunId:true,exactStandaloneRecovery:true};
 result.proposedSevenDayHotDisplayBytes=result.displayEncodedBytes*7;
}
await fs.writeFile(process.argv[4],JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
