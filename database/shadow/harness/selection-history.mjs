// Storage deduplication only. Complete fresh selector evidence is always required.
import assert from 'node:assert/strict';
import {gzipSync,gunzipSync} from 'node:zlib';
import {contentHash} from './importer.mjs';
export const FAMILIES=['admin_service','support_worker','customer_sales','finance_accounts','hr_recruitment','marketing','legal_assistant_paralegal','customer_service_contact_centre'];
export const MAX_HISTORY_DEPTH=6;
const MAX_JSON=256*1024*1024, MAX_ENCODED=16*1024*1024;
const hash=v=>assert.match(v,/^[a-f0-9]{64}$/);
const key=d=>d.scope+'\0'+d.ref;
const compare=(a,b)=>a<b?-1:a>b?1:0;
const sorted=rows=>[...rows].sort((a,b)=>compare(key(a),key(b)));
export function verifyDependencyManifest(report,context){
 const m=report.dependencyManifest;
 assert.equal(m?.version,1);assert.equal(m.kind,'captured-replay-inputs');
 assert.equal(m.runtimeCaptured,true);assert.equal(m.sourceUnchanged,true);
 assert.equal(contentHash(m),report.dependencyManifestSha256,'Dependency manifest checksum mismatch');
 assert.equal(m.revision,report.rulesRevision);assert.equal(m.archiveSha256,report.archiveSha256);
 assert.equal(m.outputsSha256,report.outputsSha256);hash(m.cleanWorkbookSha256);
 assert.equal(contentHash(m.files),m.sourceSha256,'Dependency inventory checksum mismatch');
 assert.ok(Object.keys(m.files).some(k=>k.startsWith('pipeline/scripts/')));
 for(const h of Object.values(m.files))hash(h);
 const registers=Object.fromEntries(Object.entries(m.files).filter(([k])=>k.startsWith('pipeline/registers/')||k.startsWith('pipeline/reviews/')));
 const geo=Object.fromEntries(Object.entries(m.files).filter(([k])=>k.startsWith('pipeline/geo/')||k.startsWith('pipeline/lookup/')));
 assert.ok(Object.keys(registers).length&&Object.keys(geo).length,'Missing dependency groups');
 assert.deepEqual(context,m.context,'Supplied compact context differs from captured inputs');
 assert.deepEqual(report.compactContext,m.context);
 assert.equal(context.selectorRevision,m.revision);
 assert.equal(context.registersSha256,contentHash(registers));
 assert.equal(context.geographySha256,contentHash(geo));
 assert.equal(context.configurationSha256,contentHash({files:m.files,runtime:m.runtime}));
 assert.equal(context.scopeRegistrySha256,contentHash(m.scope));
 assert.deepEqual(m.scope.families,FAMILIES);
 if(report.selectedByScope)assert.deepEqual(m.scope.outputScopes,Object.keys(report.selectedByScope).sort());
 const time=JSON.parse(context.timeContext);
 assert.equal(time.workbookCreated,m.workbookCreated);
 assert.equal(time.feedDateOverride,m.runtime.environment.ONTAP_FEED_DATE);
 assert.equal(time.startedAt,m.startedAt);assert.equal(time.finishedAt,m.finishedAt);
 assert.ok(Number.isFinite(Date.parse(m.startedAt))&&Date.parse(m.finishedAt)>=Date.parse(m.startedAt));
}
export function canonicalSelection(fixture,context){
 const {report,sourceHashes,decisions}=fixture;
 if(report.dependencyManifest||report.dependencyManifestSha256||report.compactContext)verifyDependencyManifest(report,context);
 assert.equal(report.exactFileOutputParity,true);assert.equal(report.unknowns,0);
 assert.match(report.rulesRevision,/^[a-f0-9]{40}$/);hash(report.archiveSha256);hash(report.outputsSha256);
 assert.equal(context.selectorRevision,report.rulesRevision);
 for(const k of ['registersSha256','geographySha256','configurationSha256','scopeRegistrySha256'])hash(context[k]);
 assert.ok(typeof context.timeContext==='string' && context.timeContext.length>0 && context.timeContext.length<500);
 assert.ok(Number.isInteger(report.cleanRecords)&&report.cleanRecords>0&&report.cleanRecords<=60000);
 assert.equal(sourceHashes.length,report.cleanRecords);
 const refs=new Set();
 for(const [ref,h] of sourceHashes){assert.ok(typeof ref==='string'&&ref.length>0&&ref.length<500&&!ref.includes('\0'));hash(h);assert.ok(!refs.has(ref),'Duplicate source ID');refs.add(ref);}
 assert.equal(decisions.length,sourceHashes.length*FAMILIES.length);
 const scopes=new Set(FAMILIES.map(x=>'production:'+x)),keys=new Set();
 for(const d of decisions){
  assert.ok(refs.has(d.ref)&&scopes.has(d.scope));assert.ok(['include','review','exclude'].includes(d.decision));
  assert.ok(typeof d.reason==='string'&&d.reason.length>0&&d.reason.length<10000);
  assert.ok(typeof d.gate==='string'&&d.gate.length<10000);
  assert.ok(Array.isArray(d.regions)&&d.regions.every(x=>typeof x==='string'&&x.length>0&&x.length<300));
  assert.equal(new Set(d.regions).size,d.regions.length);assert.equal(d.regions.length>0,d.decision==='include');
  assert.ok(!keys.has(key(d)),'Duplicate decision');keys.add(key(d));
 }
 // Order of these evidence arrays has no display meaning. Actual displayed
 // output order is represented by outputsSha256 and remains untouched.
 return {report:structuredClone(report),context:structuredClone(context),sourceHashes:[...sourceHashes].map(x=>[...x]).sort((a,b)=>compare(a[0],b[0])),decisions:sorted(decisions).map(x=>structuredClone(x))};
}
export function encodeHistory(fixture,context,parent=null){
 const current=canonicalSelection(fixture,context);
 const useParent=parent && parent.envelope.depth<MAX_HISTORY_DEPTH;
 const old=useParent?parent.state:null;
 const before=new Map((old?.decisions||[]).map(d=>[key(d),d]));
 const after=new Map(current.decisions.map(d=>[key(d),d]));
 const oldHashes=new Map(old?.sourceHashes||[]),newHashes=new Map(current.sourceHashes);
 const body={report:current.report,context:current.context,
  sourceUpserts:current.sourceHashes.filter(([k,v])=>oldHashes.get(k)!==v),
  sourceDeletes:[...oldHashes.keys()].filter(k=>!newHashes.has(k)),
  decisionUpserts:current.decisions.filter(d=>!before.has(key(d))||contentHash(d)!==contentHash(before.get(key(d)))),
  decisionDeletes:[...before.keys()].filter(k=>!after.has(k))};
 const bytes=gzipSync(Buffer.from(JSON.stringify(body)),{level:9});
 assert.ok(bytes.length<=MAX_ENCODED,'Compressed history too large');
 const envelope={version:1,kind:old?'delta':'baseline',depth:old?parent.envelope.depth+1:0,
  parentStateSha256:old?parent.envelope.stateSha256:null,stateSha256:contentHash(current),
  payloadSha256:contentHash(body),codec:'gzip-base64',payload:bytes.toString('base64'),
  changedDecisions:body.decisionUpserts.length,removedDecisions:body.decisionDeletes.length,
  changedSourceHashes:body.sourceUpserts.length,removedSources:body.sourceDeletes.length};
 // Full semantic readback is mandatory before a caller can persist this.
 assert.deepEqual(decodeHistory(envelope,old),current);
 return {envelope,state:current,compressedBytes:bytes.length,encodedBytes:Buffer.byteLength(JSON.stringify(envelope))};
}
export function decodeHistory(envelope,parentState=null){
 assert.equal(envelope.version,1);assert.equal(envelope.codec,'gzip-base64');
 assert.ok(['baseline','delta'].includes(envelope.kind));
 assert.ok(Number.isInteger(envelope.depth)&&envelope.depth>=0&&envelope.depth<=MAX_HISTORY_DEPTH);
 assert.ok(typeof envelope.payload==='string'&&envelope.payload.length<=Math.ceil(MAX_ENCODED/3)*4);
 if(envelope.kind==='delta'){assert.ok(parentState,'Missing parent');assert.ok(envelope.depth>0);assert.equal(contentHash(parentState),envelope.parentStateSha256,'Wrong parent');}
 else{assert.equal(envelope.depth,0);assert.equal(envelope.parentStateSha256,null);assert.equal(parentState,null);}
 const body=JSON.parse(gunzipSync(Buffer.from(envelope.payload,'base64'),{maxOutputLength:MAX_JSON}));
 assert.equal(contentHash(body),envelope.payloadSha256,'Corrupt payload');
 assert.equal(body.decisionUpserts.length,envelope.changedDecisions);assert.equal(body.decisionDeletes.length,envelope.removedDecisions);
 assert.equal(body.sourceUpserts.length,envelope.changedSourceHashes);assert.equal(body.sourceDeletes.length,envelope.removedSources);
 const d=new Map((parentState?.decisions||[]).map(x=>[key(x),x]));
 const h=new Map(parentState?.sourceHashes||[]);
 for(const k of body.decisionDeletes){assert.ok(d.has(k),'Unknown decision removal');d.delete(k);}
 for(const k of body.sourceDeletes){assert.ok(h.has(k),'Unknown source removal');h.delete(k);}
 for(const x of body.decisionUpserts)d.set(key(x),x);
 for(const [k,v] of body.sourceUpserts)h.set(k,v);
 const state=canonicalSelection({report:body.report,decisions:[...d.values()],sourceHashes:[...h]},body.context);
 assert.equal(contentHash(state),envelope.stateSha256,'History state mismatch');
 return state;
}
