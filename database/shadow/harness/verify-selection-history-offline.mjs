// Local saved-artifact verification. No network/database connection/selector run.
import fs from 'node:fs/promises';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';import {gunzipSync} from 'node:zlib';
import {encodeHistory,decodeHistory} from './selection-history.mjs';import {contentHash} from './importer.mjs';
const source=await fs.readFile(process.argv[2]);
assert.ok(source.length<20*1024*1024);
const fixtureSha256=createHash('sha256').update(source).digest('hex');
assert.equal(fixtureSha256,'7eb9b15fe9bbeb0334d179d282af5431cb41c93125d909c4209d73aacaf9c58a');
const fixture=JSON.parse(gunzipSync(source,{maxOutputLength:256*1024*1024}));
const accepted=JSON.parse(await fs.readFile(new URL('../selection-verification-2026-11-02.json',import.meta.url)));
for(const key of ['archiveSha256','rulesRevision','outputsSha256','cleanRecords'])assert.equal(fixture.report[key],accepted[key]);
// Synthetic dependency hashes are deliberate: storage validation does not
// pretend to establish historical production dependency provenance.
const context={selectorRevision:fixture.report.rulesRevision,registersSha256:'1'.repeat(64),geographySha256:'2'.repeat(64),configurationSha256:'3'.repeat(64),scopeRegistrySha256:'4'.repeat(64),timeContext:'synthetic storage verification, not dependency provenance'};
const started=Date.now();console.log('Verifying saved baseline');
const baseline=encodeHistory(fixture,context);
console.log('Baseline roundtrip passed; verifying unchanged subsequent snapshot');
const later=structuredClone(fixture);later.report.archiveSha256=contentHash({syntheticNextSnapshot:true});
const delta=encodeHistory(later,{...context,timeContext:'synthetic subsequent day, unchanged observed evidence'},baseline);
const restored=decodeHistory(delta.envelope,baseline.state);
const receipt={testedAt:new Date().toISOString(),fixtureArtifactId:13184005546,fixtureRunId:41530087079,fixtureSha256,sourceCompressedBytes:source.length,advertCount:fixture.sourceHashes.length,decisionCount:fixture.decisions.length,baselineCompressedBytes:baseline.compressedBytes,baselineEncodedBytes:baseline.encodedBytes,unchangedDeltaCompressedBytes:delta.compressedBytes,unchangedDeltaEncodedBytes:delta.encodedBytes,unchangedNewDecisionEntries:delta.envelope.changedDecisions,unchangedSourceHashEntries:delta.envelope.changedSourceHashes,exactCanonicalReadback:contentHash(restored)===delta.envelope.stateSha256,elapsedMs:Date.now()-started,scope:'Local full-fixture decision storage roundtrip; synthetic contexts; no Neon writes, new feed, selector replay or display migration'};
assert.equal(receipt.exactCanonicalReadback,true);assert.equal(receipt.unchangedNewDecisionEntries,0);
await fs.writeFile(process.argv[3],JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt));
