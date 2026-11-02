import fs from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';

try {
  if(process.env.VERCEL_ENV!=='preview') throw new Error('Preview required');
  const source=JSON.parse(await fs.readFile('source-download.json','utf8'));
  const url=new URL(source.downloadUrl);
  if(url.protocol!=='https:' || !url.hostname.endsWith('.oaiusercontent.com')) throw new Error('Unexpected temporary artifact host');
  const response=await fetch(url,{signal:AbortSignal.timeout(60000)});
  if(!response.ok) throw new Error('Source download failed');
  await fs.writeFile('source-artifact.zip',Buffer.from(await response.arrayBuffer()));
  execFileSync('python3',['-c',`import zipfile,shutil
with zipfile.ZipFile('source-artifact.zip') as a:
 names=[n for n in a.namelist() if n.rsplit('/',1)[-1]=='ontap-shadow-feed.zip']
 if len(names)!=1: raise RuntimeError('Expected one source ZIP')
 with a.open(names[0]) as src,open('source-feed.zip','wb') as dst: shutil.copyfileobj(src,dst)
`],{stdio:'pipe'});
  const actual=createHash('sha256').update(await fs.readFile('source-feed.zip')).digest('hex');
  if(actual!==source.archiveSha256) throw new Error('Source fingerprint changed');
  execFileSync('python3',['prepare_raw_stage.py','--archive','source-feed.zip','--request','stage-request.json',
    '--percentage',String(source.percentage),'--output','stage.json.gz'],{stdio:'inherit'});
  await import('./verify-stage-neon.mjs');
} catch(error) {
  console.error('ONTAP_STAGE_BOOTSTRAP_FAILED',String(error.code || 'source_or_configuration_error'));
  process.exitCode=1;
}
