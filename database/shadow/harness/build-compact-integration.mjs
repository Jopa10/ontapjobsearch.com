// Guarded, one-shot Preview integration for the pinned 5 November snapshot.
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {gunzipSync} from 'node:zlib';
import {createHash} from 'node:crypto';
import pg from 'pg';
import {contentHash} from './importer.mjs';
import {validateCompactIntegration,verifyCompactIntegration} from './compact-integration.mjs';

const PIN='866570e8e23c38863292dc3f1fedc1518a18d750012c4449b7a208e7c51d019d';
const OUTPUTS='b4f3950d3cc1f1ea1fdbaa100b8fdf47a39703a2fc83043b40022d677777a6a2';
const RULES='8bca60e82c6df07dda33d7fc47129934efb884c0';
const DB_PROJECT='noisy-fire-97386602';
const CEILING=838860800;
const RESERVE=67108864;
const EXPECTED_ZIP_SHA={
  raw:'76dda805bf5930da1793697bb4ca180beb9ca6011712d122d004d0328cd2b241',
  parity:'657e1ce3d1f6915984fd1ba8b3dbbe63bec91bf0c06c73f2b2fb20dad1cb1591',
  recovery:'14a5771c30eae98eaf595d385d3694f23ba1d45bbebcab726c8f1e93dc61e4fb'
};

function sha(bytes){return createHash('sha256').update(bytes).digest('hex');}
async function fetchZip(key,expected,maxBytes){
  const value=process.env[key];
  assert.ok(value,'Missing temporary integration artifact URL: '+key);
  const url=new URL(value);
  assert.equal(url.protocol,'https:');
  assert.ok(url.hostname.endsWith('.oaiusercontent.com'),'Unexpected artifact host');
  const response=await fetch(url,{signal:AbortSignal.timeout(120000)});
  assert.equal(response.status,200,'Artifact fetch failed for '+key);
  const bytes=Buffer.from(await response.arrayBuffer());
  assert.ok(bytes.length>0&&bytes.length<=maxBytes,'Artifact outside size bound: '+key);
  assert.equal(sha(bytes),expected,'Artifact digest mismatch: '+key);
  return bytes;
}
function extractZip(zipPath,dest,kind){
  const py=[
    'import pathlib,sys,zipfile',
    'src,dst,kind=sys.argv[1:]',
    'wanted={',
    "  'raw':['raw-stage-100.json.gz','raw-stage-100.json.gz.manifest.json'],",
    "  'parity':['report.json','selection.json.gz','dependency-manifest.json','source-request.json'],",
    "  'recovery':['plain/outputs.json','observed/outputs.json']",
    '}[kind]',
    'out=pathlib.Path(dst); out.mkdir(parents=True,exist_ok=True)',
    'with zipfile.ZipFile(src) as z:',
    '  names=set(z.namelist())',
    '  assert all(n in names for n in wanted), "Required artifact file missing"',
    '  for name in wanted:',
    '    target=out/(name.replace("/","__"))',
    '    target.write_bytes(z.read(name))'
  ].join('\n');
  execFileSync('python3',['-c',py,zipPath,dest,kind],{stdio:'inherit'});
}
async function dbPreflight(client){
  await client.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
  const ro=(await client.query('SHOW transaction_read_only')).rows[0].transaction_read_only;
  assert.equal(ro,'on','Preflight must be read-only');
  const size=Number((await client.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
  const counts=(await client.query("SELECT (SELECT count(*) FROM ontap_shadow.supplier_adverts)::int AS adverts,(SELECT count(*) FROM ontap_shadow.supplier_adverts WHERE raw_payload IS NOT NULL)::int AS payloads,(SELECT count(*) FROM ontap_shadow.jobs)::int AS jobs,(SELECT count(*) FROM ontap_shadow.feed_runs)::int AS feed_runs,(SELECT count(*) FROM ontap_shadow.jobs WHERE publication_status<>'withheld')::int AS published_jobs")).rows[0];
  const col=(await client.query("SELECT format_type(a.atttypid,a.atttypmod) AS type FROM pg_attribute a WHERE a.attrelid='ontap_shadow.supplier_adverts'::regclass AND a.attname='exclude_review_started_on' AND NOT a.attisdropped")).rows[0];
  const idx=(await client.query("SELECT to_regclass('ontap_shadow.supplier_adverts_exclude_review') IS NOT NULL AS present")).rows[0].present;
  assert.equal(col?.type,'date','Schema migration 002 is not present');
  assert.equal(idx,true,'Schema migration 002 index is missing');
  assert.deepEqual(counts,{adverts:47902,payloads:47902,jobs:47902,feed_runs:5,published_jobs:0},'Preview baseline changed since the read-only preflight');
  assert.ok(size+RESERVE<CEILING,'Preview baseline lacks the protected storage reserve');
  await client.query('COMMIT');
  return {databaseBytes:size,...counts,reviewDateColumn:col.type,reviewIndexPresent:idx,readOnly:true};
}
let integrationWriteStarted=false;
async function main(){
  assert.equal(process.env.VERCEL_ENV,'preview','Preview deployment only');
  assert.equal(process.env.VERCEL_GIT_COMMIT_REF,'feat/neon-shadow-database','Wrong Preview branch');
  assert.equal(process.env.ONTAP_SHADOW_NEON_PROJECT_ID,DB_PROJECT,'Wrong Neon project');
  const work=await fs.mkdtemp(path.join(os.tmpdir(),'ontap-neon-20261105-'));
  const rawZip=await fetchZip('ONTAP_INTEGRATION_RAW_STAGE_URL',EXPECTED_ZIP_SHA.raw,50*1024*1024);
  const parityZip=await fetchZip('ONTAP_INTEGRATION_PARITY_URL',EXPECTED_ZIP_SHA.parity,10*1024*1024);
  const recoveryZip=await fetchZip('ONTAP_INTEGRATION_RECOVERY_URL',EXPECTED_ZIP_SHA.recovery,20*1024*1024);
  const rawZipPath=path.join(work,'raw.zip'),parityZipPath=path.join(work,'parity.zip'),recoveryZipPath=path.join(work,'recovery.zip');
  await Promise.all([fs.writeFile(rawZipPath,rawZip),fs.writeFile(parityZipPath,parityZip),fs.writeFile(recoveryZipPath,recoveryZip)]);
  const rawDir=path.join(work,'raw'),parityDir=path.join(work,'parity'),recoveryDir=path.join(work,'recovery');
  extractZip(rawZipPath,rawDir,'raw');extractZip(parityZipPath,parityDir,'parity');extractZip(recoveryZipPath,recoveryDir,'recovery');
  const rawPacket=JSON.parse(gunzipSync(await fs.readFile(path.join(rawDir,'raw-stage-100.json.gz')),{maxOutputLength:384*1024*1024}));
  const rawManifest=JSON.parse(await fs.readFile(path.join(rawDir,'raw-stage-100.json.gz.manifest.json'),'utf8'));
  const selector=JSON.parse(gunzipSync(await fs.readFile(path.join(parityDir,'selection.json.gz')),{maxOutputLength:256*1024*1024}));
  const parity=JSON.parse(await fs.readFile(path.join(parityDir,'report.json'),'utf8'));
  const outputs=JSON.parse(await fs.readFile(path.join(recoveryDir,'observed__outputs.json'),'utf8'));
  const plain=JSON.parse(await fs.readFile(path.join(recoveryDir,'plain__outputs.json'),'utf8'));
  const standaloneManifest=JSON.parse(await fs.readFile(path.join(parityDir,'dependency-manifest.json'),'utf8'));
  const sourceRequestBytes=await fs.readFile(path.join(parityDir,'source-request.json'));
  const sourceRequest=JSON.parse(sourceRequestBytes.toString('utf8'));
  let selectorProvenanceRepair=null;
  assert.deepEqual(plain,outputs,'Plain and observed output files differ');
  assert.equal(rawPacket.archiveSha256,PIN);assert.equal(rawPacket.archiveDate,'2026-11-05');
  assert.equal(rawPacket.observedOn,'2026-11-05');assert.equal(rawPacket.sourceRevision,RULES);assert.equal(rawPacket.percentage,100);
  assert.deepEqual(rawPacket.receiptDiagnostics,{sourceRows:43391,uniqueSupplierIds:43389,exactRepeatRows:0,conflictingIdsHeld:['1401785815','1401786160']});assert.equal(rawPacket.eligibleRecords,43387);assert.equal(rawPacket.records.length,43387);
  assert.equal(rawManifest.archiveSha256,PIN);assert.equal(rawManifest.cleanRecords,43387);assert.equal(rawManifest.sourceRevision,RULES);
  assert.equal(parity.archiveSha256,PIN);assert.equal(parity.rulesRevision,RULES);assert.equal(parity.cleanRecords,43387);
  assert.equal(parity.exactFileOutputParity,true);assert.equal(parity.unknowns,0);assert.equal(parity.outputsSha256,OUTPUTS);
  assert.equal(selector.report.archiveSha256,PIN);assert.equal(selector.report.rulesRevision,RULES);assert.equal(selector.report.outputsSha256,OUTPUTS);
  assert.deepEqual(standaloneManifest,selector.report.dependencyManifest,'Standalone and embedded selector manifests differ');
  assert.equal(sha(sourceRequestBytes),selector.report.sourceRequestSha256,'Saved selector source request fingerprint differs');
  assert.equal(sourceRequest.date,'2026-11-05');assert.equal(sourceRequest.sourceChecksumPrerequisiteResolved,true);
  assert.equal(sourceRequest.pinnedSavedSource?.archiveChecksums?.current,PIN,'Selector request does not pin this archive');
  const capturedManifest=selector.report.dependencyManifest;
  assert.equal(contentHash(capturedManifest),selector.report.dependencyManifestSha256,'Original selector manifest checksum is invalid');
  assert.equal(capturedManifest.archiveSha256,PIN,'Selector dependency manifest must match the pinned 5 November archive');
  assert.equal(selector.sourceHashes.length,43387);assert.equal(selector.decisions.length,347096);
  assert.equal(contentHash(outputs),OUTPUTS,'Saved output checksum differs');
  validateCompactIntegration({raw:rawPacket,selection:selector,outputs});
  console.log('ONTAP_INTEGRATION_INPUT_VALIDATION passed before database connection');
  const u=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
  assert.ok(u.hostname.endsWith('.neon.tech'),'Expected Neon connection');
  assert.ok(['require','verify-full'].includes(u.searchParams.get('sslmode')),'TLS required');
  u.searchParams.set('sslmode','verify-full');
  const client=new pg.Client({connectionString:u.toString(),connectionTimeoutMillis:15000,query_timeout:120000,statement_timeout:90000,application_name:'ontap-shadow-20261105-compact-integration'});
  let preflight=null;
  try{
    await client.connect();
    preflight=await dbPreflight(client);
    const checkpoints=path.join(work,'phase-checkpoints.jsonl');
    const onCheckpoint=async event=>{
      const record={...event,loggedAt:new Date().toISOString(),deploymentId:process.env.VERCEL_DEPLOYMENT_ID||null};
      const line=JSON.stringify(record);
      await fs.appendFile(checkpoints,line+'\n');
      console.log('ONTAP_INTEGRATION_PHASE '+line);
    };
    integrationWriteStarted=true;
    const result=await verifyCompactIntegration(client,{raw:rawPacket,selection:selector,outputs},{parentRunId:null,onCheckpoint});
    assert.equal(result.status,'passed');
    assert.equal(result.expiryEnabled,false);
    assert.equal(result.productionChanged,false);
    await fs.mkdir('dist',{recursive:true});
    const receipt={status:'passed',feedDate:'2026-11-05',archiveSha256:PIN,selectorRun:42023032553,scopes:239,selectedUniqueJobs:parity.selectedUniqueJobs,outputSha256:OUTPUTS,artifactZipSha256:EXPECTED_ZIP_SHA,selectorProvenanceRepair:null,preflight,result,importAttempted:true,purgeAttempted:false,purgeDuePayloads:false,expiryEnabled:false,productionChanged:false,jobsWithheld:true};
    await fs.copyFile(checkpoints,path.join('dist','phase-checkpoints.jsonl'));
    if(selectorProvenanceRepair)await fs.writeFile(path.join('dist','selector-provenance-repair.json'),JSON.stringify(selectorProvenanceRepair,null,2)+'\\n');
    await fs.writeFile(path.join('dist','integration-result.json'),JSON.stringify(receipt,null,2)+'\n');
    await fs.writeFile(path.join('dist','index.html'),'<!doctype html><meta name="robots" content="noindex,nofollow"><title>Ontap integration receipt</title><p>Preview-only shadow integration receipt.</p>');
    console.log('ONTAP_INTEGRATION_RESULT '+JSON.stringify(receipt));
  }finally{await client.end();}
}
main().catch(error=>{
  console.error('ONTAP_INTEGRATION_FAILED '+JSON.stringify({code:error.code||error.name||'integration_failure',message:String(error.message||'').slice(0,300),integrationWriteStarted:integrationWriteStarted?'yes_phase_must_be_inspected':'no',productionChanged:false}));
  process.exitCode=1;
});
