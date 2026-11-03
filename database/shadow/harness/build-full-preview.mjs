// Build-only, read-only database export. Production build command never calls this.
import fs from 'node:fs/promises';import assert from 'node:assert/strict';import {execFileSync} from 'node:child_process';import pg from 'pg';
import {reconstruct} from './display-snapshot.mjs';import {contentHash} from './importer.mjs';
async function main(){
 assert.equal(process.env.VERCEL_ENV,'preview');assert.equal(process.env.ONTAP_SHADOW_NEON_PROJECT_ID,'noisy-fire-97386602');
 const receipt=JSON.parse(await fs.readFile('database/shadow/selection-verification-2026-11-02.json'));const u=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);assert.ok(u.hostname.endsWith('.neon.tech'));assert.ok(['require','verify-full'].includes(u.searchParams.get('sslmode')));u.searchParams.set('sslmode','verify-full');
 const c=new pg.Client({connectionString:u.toString(),connectionTimeoutMillis:15000,query_timeout:90000});let outputs;
 try{await c.connect();await c.query('BEGIN READ ONLY');
 const run=(await c.query("SELECT id,diagnostics FROM ontap_shadow.feed_runs WHERE feed_key=$1 AND status='accepted'",['raw-stage:'+receipt.archiveSha256+':100'])).rows[0];assert.equal(run?.diagnostics.display_snapshot?.outputs_sha256,receipt.outputsSha256);
 const rows=(await c.query(`SELECT scope,evidence->'displayRows' AS "displayRows" FROM ontap_shadow.selection_decisions WHERE feed_run_id=$1 AND scope LIKE 'production:%' AND decision='include'`,[run.id])).rows;
 outputs=reconstruct(rows,Object.keys(receipt.selectedByScope));assert.equal(contentHash(outputs),receipt.outputsSha256,'Database display snapshot drift');await c.query('COMMIT');}finally{await c.end();}
 await fs.writeFile('shadow-db-outputs.json',JSON.stringify(outputs));
 execFileSync('python3',['-m','pip','install','--disable-pip-version-check','--target','/tmp/ontap-preview-python','openpyxl==3.1.5'],{stdio:'inherit'});
 execFileSync('python3',['database/shadow/harness/prepare-full-preview.py'],{stdio:'inherit',env:{...process.env,PYTHONPATH:'/tmp/ontap-preview-python'}});
 // No analytics on a private test; real presentation components are unchanged.
 const layout='app/layout.tsx';let s=await fs.readFile(layout,'utf8');s=s.replace(/<Analytics\s*\/>/g,'').replace(/<Script\b[\s\S]*?<\/Script>/g,'');await fs.writeFile(layout,s);
 execFileSync('npm',['run','build'],{stdio:'inherit',env:{...process.env,NEXT_TELEMETRY_DISABLED:'1'}});
 console.log('ONTAP_FULL_PREVIEW_BUILD_PASSED '+JSON.stringify({exactSnapshotHash:receipt.outputsSha256,scopes:Object.keys(outputs).length,databaseReadOnly:true,productionChanged:false}));
}
main().catch(e=>{console.error('ONTAP_FULL_PREVIEW_FAILED',e.code||e.message);process.exitCode=1;});
