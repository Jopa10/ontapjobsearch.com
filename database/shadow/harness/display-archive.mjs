// Provider-neutral archive boundary. No cleanup or scheduling is implemented.
import assert from 'node:assert/strict';import {gzipSync,gunzipSync} from 'node:zlib';import {createHash} from 'node:crypto';
import {canonicalSelection} from './selection-history.mjs';import {decodeCompactDisplay} from './display-snapshot.mjs';import {decodeAppearances} from './appearance-manifest.mjs';import {contentHash} from './importer.mjs';
const sha=b=>createHash('sha256').update(b).digest('hex');
export function makeDisplayArchive({runId,feedDate,state,display,appearances}){
 assert.match(runId,/^[a-f0-9-]{36}$/);assert.match(feedDate,/^\d{4}-\d{2}-\d{2}$/);
 assert.equal(new Date(feedDate).toISOString().slice(0,10),feedDate);
 assert.deepEqual(canonicalSelection(state,state.context),state);
 const outputs=decodeCompactDisplay(display,state),refs=decodeAppearances(appearances);
 assert.deepEqual([...refs].sort(),state.sourceHashes.map(x=>x[0]).sort(),'Archive appearance membership mismatch');
 const packet={version:1,runId,feedDate,state,display,appearances};
 const bytes=gzipSync(Buffer.from(JSON.stringify(packet)),{level:9});assert.ok(bytes.length<64*1024*1024);
 return {bytes,receipt:{version:1,key:`ontap-shadow/display-v1/${runId}/${sha(bytes)}.json.gz`,sha256:sha(bytes),bytes:bytes.length,runId,feedDate,selectionStateSha256:contentHash(state),outputsSha256:contentHash(outputs)}};
}
export function restoreDisplayArchive(bytes,receipt){
 assert.ok(Buffer.isBuffer(bytes)&&bytes.length<64*1024*1024);assert.equal(bytes.length,receipt.bytes);assert.equal(sha(bytes),receipt.sha256,'Archive checksum mismatch');
 assert.equal(receipt.key,`ontap-shadow/display-v1/${receipt.runId}/${receipt.sha256}.json.gz`,'Archive key mismatch');
 const p=JSON.parse(gunzipSync(bytes,{maxOutputLength:384*1024*1024}));assert.equal(p.version,1);assert.equal(p.runId,receipt.runId);assert.equal(p.feedDate,receipt.feedDate);
 assert.deepEqual(canonicalSelection(p.state,p.state.context),p.state);
 assert.equal(contentHash(p.state),receipt.selectionStateSha256);const outputs=decodeCompactDisplay(p.display,p.state);assert.equal(contentHash(outputs),receipt.outputsSha256);
 assert.deepEqual(decodeAppearances(p.appearances).sort(),p.state.sourceHashes.map(x=>x[0]).sort());
 return {...p,outputs};
}
export async function verifyArchiveStorage(input,store){
 // Adapter must enforce immutable put-if-absent; caller supplies approved store.
 const made=makeDisplayArchive(input);await store.putIfAbsent(made.receipt.key,made.bytes);
 const restored=restoreDisplayArchive(await store.get(made.receipt.key),made.receipt);
 assert.equal(restored.runId,input.runId);
 return {...made.receipt,readbackVerified:true};
}
export function planDisplayRetention(runs,{asOf,keepDays=7,maxHotBytes=64*1024*1024}={}){
 assert.match(asOf,/^\d{4}-\d{2}-\d{2}$/);assert.ok(Number.isInteger(keepDays)&&keepDays>=7);assert.ok(Number.isFinite(maxHotBytes)&&maxHotBytes>0&&maxHotBytes<=64*1024*1024);
 const cutoff=new Date(asOf+'T00:00:00Z');cutoff.setUTCDate(cutoff.getUTCDate()-keepDays+1);
 const day=cutoff.toISOString().slice(0,10);const candidates=[],blocked=[],kept=[];let hotBytes=0;
 const latest=runs.map(x=>x.feedDate).sort().at(-1);
 for(const r of runs){assert.ok(Number.isSafeInteger(r.displayBytes)&&r.displayBytes>=0);const a=r.archive;
  const verified=a?.readbackVerified===true&&a.runId===r.runId&&a.feedDate===r.feedDate&&a.outputsSha256===r.outputsSha256&&a.selectionStateSha256===r.selectionStateSha256;
  if(r.feedDate<day&&r.feedDate!==latest){if(verified)candidates.push(r.runId);else{blocked.push(r.runId);hotBytes+=r.displayBytes;}}
  else{kept.push(r.runId);hotBytes+=r.displayBytes;}
 }
 return {mode:'dry-run-only',keepDays,cutoff:day,kept,candidates,blocked,projectedHotDisplayBytes:hotBytes,maxHotBytes,withinBudget:hotBytes<=maxHotBytes,cleanupAuthorized:false,warning:'No data changed. Budget requires a verified immutable archive and separate transactional cleanup. Candidate receipt must be revalidated against stored bytes before any later cleanup.'};
}

// Caller supplies an approved immutable store. Records a verified pointer only;
// never removes hot display/selection/raw data or changes public inventory.
export async function archiveCompactDisplay(client,runId,store){
 const {readCompactSelection}=await import('./selection-importer.mjs');
 const {readAppearances,encodeAppearances}=await import('./appearance-manifest.mjs');
 let input;
 await client.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
 try{
  const {state,run}=await readCompactSelection(client,runId);
  assert.ok(run.diagnostics.compact_display,'Missing verified compact display');
  const seen=await readAppearances(client,runId);
  input={runId,feedDate:seen.date,state,display:run.diagnostics.compact_display,appearances:encodeAppearances(seen.refs)};
  await client.query('COMMIT');
 }catch(e){await client.query('ROLLBACK');throw e;}
 const receipt=await verifyArchiveStorage(input,store);
 await client.query('BEGIN');try{
  await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
  const current=await readCompactSelection(client,runId);assert.equal(contentHash(current.state),receipt.selectionStateSha256,'Archive source changed');
  assert.deepEqual(current.run.diagnostics.compact_display,input.display,'Display changed during archival');
  await client.query("UPDATE ontap_shadow.feed_runs SET diagnostics=jsonb_set(diagnostics,'{display_archive}',$2::jsonb) WHERE id=$1",[runId,JSON.stringify(receipt)]);
  await client.query('COMMIT');return receipt;
 }catch(e){await client.query('ROLLBACK');throw e;}
}
