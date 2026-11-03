// Explicit library entry point only: no build/HTTP/schedule invokes this today.
import assert from 'node:assert/strict';
import {contentHash,stableId,counts} from './importer.mjs';
import {importStage,measure,DEFAULT_BUDGET} from './staged-importer.mjs';
import {canonicalSelection,verifyDependencyManifest} from './selection-history.mjs';
import {attachCompactSelection,readCompactSelection} from './selection-importer.mjs';
import {encodeCompactDisplay,attachCompactDisplay,readCompactDisplay} from './display-snapshot.mjs';
import {readAppearances} from './appearance-manifest.mjs';
export function validateCompactIntegration({raw,selection,outputs}){
 assert.equal(raw.percentage,100,'Complete snapshot required');
 const context=selection.report.compactContext;
 verifyDependencyManifest(selection.report,context);canonicalSelection(selection,context);
 assert.equal(raw.archiveSha256,selection.report.archiveSha256,'Raw/selection source mismatch');
 assert.equal(raw.sourceRevision,selection.report.rulesRevision,'Source revision mismatch');
 const m=selection.report.dependencyManifest;
 assert.equal(raw.observedOn,m.runtime.environment.ONTAP_FEED_DATE||m.workbookCreated?.slice(0,10),'Effective feed date mismatch');
 assert.equal(raw.records.length,selection.sourceHashes.length);
 const known=new Map(selection.sourceHashes),records=new Map();
 for(const row of raw.records){const ref=row['/Job/DisplayReference'];assert.ok(!records.has(ref),'Duplicate raw ID');records.set(ref,row);assert.equal(contentHash(row),known.get(ref),'Raw hash differs from selector input');}
 assert.equal(records.size,known.size);
 const state=canonicalSelection(selection,context);encodeCompactDisplay(outputs,state);
 for(const rows of Object.values(outputs))for(const row of rows)assert.equal(row.apply_url,records.get(row.job_id)?.['/Job/ApplicationURL'],'Display Apply URL differs from raw source');
 return context;
}
export async function verifyCompactIntegration(client,input,{parentRunId=null,onCheckpoint=async()=>{}}={}){
 const context=validateCompactIntegration(input),{raw,selection,outputs}=input;
 const runId=stableId('run:jobg8:raw-stage:'+raw.archiveSha256+':100');
 const checkpoint=phase=>onCheckpoint({phase,runId,archiveSha256:raw.archiveSha256,feedDate:raw.observedOn});
 // These existing entry points commit independently. A failed later phase
 // leaves a recoverable withheld snapshot, never a public-ready feed.
 const imported=await importStage(client,raw,{compactSelection:true});await checkpoint('raw-accepted');
 const attached=await attachCompactSelection(client,{runId,fixture:selection,context,parentRunId});await checkpoint('selection-verified');
 await attachCompactDisplay(client,runId,outputs);await checkpoint('display-verified');
 assert.deepEqual((await readCompactSelection(client,runId)).state,canonicalSelection(selection,context));
 assert.deepEqual(await readCompactDisplay(client,runId),outputs);
 assert.deepEqual((await readAppearances(client,runId)).refs,selection.sourceHashes.map(x=>x[0]).sort());
 const after=await counts(client);
 assert.equal((await importStage(client,raw,{compactSelection:true})).replayed,true);
 assert.equal((await attachCompactSelection(client,{runId,fixture:selection,context,parentRunId})).replayed,true);
 assert.equal((await attachCompactDisplay(client,runId,outputs)).replayed,true);
 assert.deepEqual(await counts(client),after,'Complete replay changed counts');
 assert.equal(Number((await client.query("SELECT count(*)::int AS n FROM ontap_shadow.jobs WHERE publication_status<>'withheld'")).rows[0].n),0);
 const allocation=await measure(client);assert.ok(allocation.databaseBytes+64*1024*1024<DEFAULT_BUDGET,'Measured integration exceeds reserved ceiling');
 return {status:'passed',runId,importReplayed:imported.replayed,selectionReplayed:attached.replayed,completeReplayVerified:true,counts:after,allocation,expiryEnabled:false,productionChanged:false};
}
