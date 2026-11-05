import fs from 'node:fs/promises';
import { gunzipSync } from 'node:zlib';
import assert from 'node:assert/strict';
import pg from 'pg';
import { attachSelection } from './selection-importer.mjs';
import { counts } from './importer.mjs';

async function main(){
  if(process.env.VERCEL_ENV!=='preview'||process.env.ONTAP_SHADOW_NEON_PROJECT_ID!=='noisy-fire-97386602')throw new Error('Wrong test environment');
  const url=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
  if(!url.hostname.endsWith('.neon.tech')||!['require','verify-full'].includes(url.searchParams.get('sslmode')))throw new Error('TLS required');
  url.searchParams.set('sslmode','verify-full');
  const fixture=JSON.parse(gunzipSync(await fs.readFile(new URL('./selection.json.gz',import.meta.url)),{maxOutputLength:300*1024*1024}));
  assert.equal(fixture.report.cleanRecords,43796);
  const client=new pg.Client({connectionString:url.toString(),connectionTimeoutMillis:15000,query_timeout:90000,statement_timeout:60000,application_name:'ontap-shadow-selection-parity'});
  try{
    await client.connect();
    const result=await attachSelection(client,fixture);
    const afterCounts=await counts(client);
    assert.equal((await attachSelection(client,fixture)).replayed,true);
    assert.deepEqual(await counts(client),afterCounts);
    const report={...fixture.report,status:'passed',database:result,afterCounts,duplicateProtectionPassed:true,productionChanged:false};
    await fs.mkdir('dist',{recursive:true});
    await fs.writeFile('dist/report.json',JSON.stringify(report,null,2)+'\n');
    await fs.writeFile('dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><title>Ontap selector parity</title><h1>Selector parity verified</h1><p>Protected test only. Production unchanged.</p>');
    console.log('ONTAP_SELECTION_REPORT '+JSON.stringify(report));
  }finally{await client.end();}
}
main().catch(e=>{console.error('ONTAP_SELECTION_FAILED',e.code||'verification_error',e.name==='AssertionError'?e.message.split('\n')[0]:'');process.exitCode=1;});
