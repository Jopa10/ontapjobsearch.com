import fs from 'node:fs/promises';
import pg from 'pg';
import { verifySample } from './verify-client.mjs';

// Runs once during a deliberately requested Preview build. No HTTP DB endpoint.
async function main() {
  if (process.env.VERCEL_ENV !== 'preview') throw new Error('Preview-only verification');
  if (process.env.ONTAP_SHADOW_NEON_PROJECT_ID !== 'noisy-fire-97386602') throw new Error('Wrong Neon test project');
  const connectionString=process.env.ONTAP_SHADOW_DATABASE_URL;
  if (!connectionString) throw new Error('Missing shadow connection');
  const url=new URL(connectionString);
  if (!url.hostname.endsWith('.neon.tech') || url.searchParams.get('sslmode') !== 'require') throw new Error('Expected TLS Neon connection');
  const fixture=JSON.parse(await fs.readFile(new URL('./sample.json',import.meta.url),'utf8'));
  const client=new pg.Client({connectionString,connectionTimeoutMillis:15000,query_timeout:15000,statement_timeout:10000,application_name:'ontap-shadow-sample-verification'});
  try {
    await client.connect();
    const report=await verifySample(client,fixture);
    report.databaseBytes=Number((await client.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
    await fs.mkdir('dist',{recursive:true});
    await fs.writeFile('dist/report.json',JSON.stringify(report,null,2)+'\n');
    await fs.writeFile('dist/index.html','<!doctype html><html><head><meta name="robots" content="noindex,nofollow"><title>Ontap database test</title></head><body><h1>Ontap database sample verification passed</h1><p>20 JobG8 adverts. Production publication unchanged.</p></body></html>');
    console.log('ONTAP_SHADOW_VERIFICATION '+JSON.stringify(report));
  } finally {
    await client.end();
  }
}
main().catch(error=>{
  // Never log connection strings, payloads or errors containing credentials.
  console.error('ONTAP_SHADOW_VERIFICATION_FAILED',String(error.code || 'verification_error'));
  process.exitCode=1;
});
