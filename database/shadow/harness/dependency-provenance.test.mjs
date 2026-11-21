import {test} from 'node:test';
import assert from 'node:assert/strict';
import {verifyDependencyManifest,FAMILIES} from './selection-history.mjs';
import {contentHash} from './importer.mjs';
function fixture(){
 const files={'pipeline/scripts/selector.py':'a'.repeat(64),'pipeline/registers/r.csv':'b'.repeat(64),'pipeline/geo/g.csv':'c'.repeat(64)};
 const m={version:1,kind:'captured-replay-inputs',runtimeCaptured:true,sourceUnchanged:true,revision:'d'.repeat(40),archiveSha256:'e'.repeat(64),outputsSha256:'f'.repeat(64),cleanWorkbookSha256:'1'.repeat(64),files,sourceSha256:contentHash(files),runtime:{environment:{ONTAP_FEED_DATE:null}},scope:{families:FAMILIES,outputScopes:['admin_service:Test']},workbookCreated:'2026-11-02T07:30:00',startedAt:'2026-11-03T13:00:00Z',finishedAt:'2026-11-03T13:01:00Z'};
 m.context={selectorRevision:m.revision,registersSha256:contentHash({'pipeline/registers/r.csv':files['pipeline/registers/r.csv']}),geographySha256:contentHash({'pipeline/geo/g.csv':files['pipeline/geo/g.csv']}),configurationSha256:contentHash({files,runtime:m.runtime}),scopeRegistrySha256:contentHash(m.scope),timeContext:JSON.stringify({workbookCreated:m.workbookCreated,feedDateOverride:null,startedAt:m.startedAt,finishedAt:m.finishedAt})};
 return {rulesRevision:m.revision,archiveSha256:m.archiveSha256,outputsSha256:m.outputsSha256,selectedByScope:{'admin_service:Test':0},dependencyManifest:m,dependencyManifestSha256:contentHash(m),compactContext:m.context};
}
test('captured dependencies bind exact compact context, raw source and output scopes',()=>{
 const r=fixture();verifyDependencyManifest(r,r.compactContext);
 assert.throws(()=>verifyDependencyManifest(r,{...r.compactContext,registersSha256:'0'.repeat(64)}));
 const changed=structuredClone(r);changed.outputsSha256='0'.repeat(64);assert.throws(()=>verifyDependencyManifest(changed,changed.compactContext));
});
test('changed source/runtime cannot inherit previous dependency context',()=>{
 for(const mutate of [m=>m.files['pipeline/registers/r.csv']='0'.repeat(64),m=>m.runtime.environment.ONTAP_FEED_DATE='2026-11-04']){
  const r=fixture();mutate(r.dependencyManifest);r.dependencyManifestSha256=contentHash(r.dependencyManifest);
  assert.throws(()=>verifyDependencyManifest(r,r.compactContext));
 }
});
test('historical reconstruction is not accepted as runtime evidence',()=>{
 const r=fixture();r.dependencyManifest.kind='reconstructed-commit-inventory';r.dependencyManifest.runtimeCaptured=false;
 r.dependencyManifestSha256=contentHash(r.dependencyManifest);assert.throws(()=>verifyDependencyManifest(r,r.compactContext));
});
