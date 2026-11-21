// Isolated Preview-only feasibility check: can existing Python selectors generate
// region/family placements from the currently stored SELECTED + REVIEW raw adverts?
// This is explicitly NOT full-feed parity: excluded feed rows are not retained.
import pg from 'pg';
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
const dateRequest=JSON.parse(await fs.readFile('independent-neon-subset-request.json','utf8'));
assert.equal(process.env.VERCEL_ENV,'preview');
assert.equal(process.env.ONTAP_SHADOW_NEON_PROJECT_ID,'noisy-fire-97386602');
const url = new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
assert.ok(url.hostname.endsWith('.neon.tech'));
assert.ok(['require','verify-full'].includes(url.searchParams.get('sslmode')));
url.searchParams.set('sslmode','verify-full');
const c=new pg.Client({connectionString:url.toString(),connectionTimeoutMillis:15000,query_timeout:120000});
let records, reference;
try {
 await c.connect();await c.query('BEGIN READ ONLY');
 const current=(await c.query('SELECT max(feed_date)::text AS day FROM ontap_shadow.selected_review_payload_records')).rows[0].day;
 assert.equal(current,dateRequest.archiveDate);
 records=(await c.query('SELECT public_id,decision,raw_payload,source_row_position FROM ontap_shadow.selected_review_payload_records WHERE feed_date=$1::date ORDER BY source_row_position',[current])).rows;
 reference=(await c.query("SELECT scope,position,public_id,source FROM ontap_shadow.published_scope_rows WHERE feed_date=$1::date AND source='JobG8' ORDER BY scope,position",[current])).rows;
 await c.query('COMMIT');
}finally{await c.end().catch(()=>{});}
assert.ok(records.every(r=>Number.isInteger(r.source_row_position)&&r.source_row_position>0),'Missing 1-based source feed-row positions');
assert.equal(new Set(records.map(r=>r.source_row_position)).size,records.length,'Duplicate source feed-row positions');
const selected=records.filter(r=>r.decision==='SELECTED');
assert.equal(selected.length,5246);
assert.ok(records.length>5500);
assert.ok(reference.length>6400,'Incomplete 250-scope publisher reference');
const keys=[...new Set(records.flatMap(x=>Object.keys(x.raw_payload)))].sort();
const csv = x=>'"'+String(x??'').replaceAll('"','""')+'"';
await fs.mkdir('pipeline/input',{recursive:true});
const f='pipeline/input/jobg8.csv';
await fs.writeFile(f, keys.map(csv).join(',')+'\n'+records.map(x=>keys.map(k=>csv(x.raw_payload[k])).join(',')).join('\n')+'\n');
console.log('ONTAP_NEON_SELECTED_SUBSET_INPUT',{day:dateRequest.archiveDate,rows:records.length,selected:selected.length,review:records.length-selected.length,columns:keys.length});
execFileSync('python3',['-m','pip','install','--disable-pip-version-check','--target','/tmp/ontap-subset-python','pandas','openpyxl==3.1.5','boto3'],{stdio:'inherit'});
const env={...process.env,PYTHONPATH:'/tmp/ontap-subset-python'};
// The unmodified multi-family Python pipeline expects a single .xlsx feed.
const convert = [
 'import csv',
 'from openpyxl import Workbook',
 'from pathlib import Path',
 "src=Path('pipeline/input/jobg8.csv')",
 "dst=Path('pipeline/input/jobg8.xlsx')",
 'book=Workbook(write_only=True)',
 "sheet=book.create_sheet(title='Jobs')",
 "with src.open(newline='',encoding='utf-8') as handle:",
 '    for row in csv.reader(handle): sheet.append(row)',
 'book.save(dst)',
 'src.unlink()',
 "print('ONTAP_NEON_SUBSET_XLSX_READY',dst.stat().st_size)"
].join('\n');
execFileSync('python3',['-c',convert],{stdio:'inherit',env});
const commands=[
 ['-m','scripts.service_admin_pipeline_north_yorkshire'],
 ['-m','scripts.enrich_job_metadata','--category','admin-service'],
 ['-m','scripts.support_worker_pipeline_live_config'],
 ['-m','scripts.enrich_job_metadata','--category','support-worker']
];
for(const args of commands){console.log('ONTAP_SUBSET_SELECTOR_START',args.join(' '));execFileSync('python3',args,{stdio:'inherit',cwd:'pipeline',env,timeout:1200000});}
const reg=await fs.readFile('pipeline/registers/region_category_slice_register.csv','utf8');
const entries=reg.trim().split(/\r?\n/).slice(1).map(x=>x.split(',')).filter(x=>x[2]==='LIVE');
const catalog=JSON.parse(await fs.readFile('pipeline/config/job_slice_catalog.json','utf8'));
const expected=new Map(), produced=new Map();
const outputToScope=new Map();
for(const [region,category] of entries){
  const meta=catalog.categories[category],slug=catalog.regions[region]?.slug;
  assert.ok(slug,'Missing catalog location '+region);
  const filename=slug+'-'+meta.file_suffix+'.json';
  assert.ok(!outputToScope.has(filename),'Duplicate LIVE output '+filename);
  outputToScope.set(filename,category+':'+region);
}
assert.equal(entries.length,250,'Preview register must match all 250 production LIVE scopes');
for(const r of reference){
  const scope=r.scope.startsWith('artifact:')?outputToScope.get(r.scope.slice('artifact:'.length)):r.scope;
  assert.ok(scope,'Unmapped production additional artifact: '+r.scope);
  assert.ok([...outputToScope.values()].includes(scope),'Artifact scope not currently LIVE: '+scope);
  if(!expected.has(scope))expected.set(scope,[]);
  expected.get(scope).push(r.public_id);
}
for(const [region,category] of entries){
 const meta=catalog.categories[category],slug=catalog.regions[region].slug;
 const filename=slug+'-'+meta.file_suffix+'.json';
 const rows=JSON.parse(await fs.readFile(path.join('pipeline',meta.output_dir,filename),'utf8'));
 produced.set(category+':'+region,rows.filter(x=>x.source==='JobG8').map(x=>String(x.job_id)));
}
const scopes=[...produced.keys()];
const known=new Set(selected.map(x=>x.public_id));
const allRefIds=new Set(reference.map(r=>r.public_id));
const ids=new Set([...produced.values()].flat());
const exact=[], orderOnly=[], membership=[];
const familyStats={};
const allMissing=new Set(),allExtra=new Set();
for(const k of scopes){
 const a=produced.get(k),b=expected.get(k)||[];
 const x=new Set(a),y=new Set(b);
 const m=b.filter(id=>!x.has(id)),e=a.filter(id=>!y.has(id));
 const family=k.split(':')[0];
 if(!familyStats[family])familyStats[family]={scopes:0,exact:0,orderOnly:0,membershipDifferent:0,referenceOccurrences:0,generatedOccurrences:0,missingOccurrences:0,extraOccurrences:0};
 const stat=familyStats[family];stat.scopes++;stat.referenceOccurrences+=b.length;stat.generatedOccurrences+=a.length;
 stat.missingOccurrences+=m.length;stat.extraOccurrences+=e.length;
 m.forEach(v=>allMissing.add(v));e.forEach(v=>allExtra.add(v));
 if(JSON.stringify(a)===JSON.stringify(b)){exact.push(k);stat.exact++;}
 else if(!m.length&&!e.length){orderOnly.push(k);stat.orderOnly++;}
 else {membership.push({scope:k,actual:a.length,reference:b.length,missing:m,extra:e,
   missingInNeonSelected:m.filter(id=>!known.has(id)),
   unexpectedButStored:e.filter(id=>known.has(id))});stat.membershipDifferent++;}
}
const report={status:!membership.length&&!orderOnly.length?'matched':'differences',
 feedDate:dateRequest.archiveDate,input:'Neon raw selected + review adverts ordered by original JobG8 feed-row position; no published output artifact used as selector input',
 sourceRowPositionField:'source_row_position',sourceRowPositionRows:records.length,sourceRowPositionsUnique:true,
 inputRows:records.length,neonSelected:selected.length,referenceRows:reference.length,
 liveScopes:scopes.length,referenceLiveScopes:expected.size,exactScopes:exact.length,orderOnlyScopes:orderOnly.length,membershipDifferentScopes:membership.length,
 familyStats,referenceUniqueLiveIds:allRefIds.size,generatedUniqueIds:ids.size,
 missingUniqueLiveIds:[...allRefIds].filter(id=>!ids.has(id)).length,
 extraUniqueLiveIds:[...ids].filter(id=>!allRefIds.has(id)).length,
 referenceLiveIdsOutsideNeonSelected:[...allRefIds].filter(id=>!known.has(id)).length,
 referenceLiveIdsOutsideNeonSelectedSample:[...allRefIds].filter(id=>!known.has(id)).slice(0,30),
 missingInNeonSelected:[...allMissing].filter(id=>!known.has(id)).length,
 missingDespitePresentInNeonSelected:[...allMissing].filter(id=>known.has(id)).length,
 generatedIdsNotInNeonSelected:[...ids].filter(id=>!known.has(id)).slice(0,30),
 missingGlobalIds:[...allRefIds].filter(id=>!ids.has(id)).slice(0,50),
 extraGlobalIds:[...ids].filter(id=>!allRefIds.has(id)).slice(0,50),
 membershipDifferences:membership,
 orderOnlyExamples:orderOnly.slice(0,20).map(k=>({scope:k,referenceFirst:(expected.get(k)||[]).slice(0,8),generatedFirst:produced.get(k).slice(0,8)})),
 scopeInputReconstructionIndependent:true,fullFeedAvailable:false,
 excludedRawRecordsSupplied:false,fullProductionParityEstablished:false,
 publishedArtifactsUsedAsSelectorInput:false,databaseWrites:false,productionChanged:false};
await fs.mkdir('dist',{recursive:true});
await fs.writeFile('dist/selected-subset-replay-report.json',JSON.stringify(report,null,2));
console.log('ONTAP_NEON_SUBSET_REPLAY_RESULT '+JSON.stringify({status:report.status,exact:report.exactScopes,orderOnly:report.orderOnlyScopes,membershipDifferent:report.membershipDifferentScopes,referenceUniqueLiveIds:report.referenceUniqueLiveIds,generatedUniqueIds:report.generatedUniqueIds,familyStats:report.familyStats}));
await fs.writeFile('dist/index.html','<html><head><meta name="robots" content="noindex,nofollow"/></head><body><h1>Ontap Preview selected-only selector replay</h1><p>See <a href="/selected-subset-replay-report.json">report</a>.</p></body></html>');
