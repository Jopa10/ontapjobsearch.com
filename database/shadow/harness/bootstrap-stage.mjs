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
  const bytes=Buffer.from(await response.arrayBuffer());
  if(source.mode==='selection_parity' && bytes.length>25*1024*1024) throw new Error('Selection artifact too large');
  await fs.writeFile('source-artifact.zip',bytes);
  if(source.mode==='selection_parity') {
    if(!/^[a-f0-9]{64}$/.test(source.fixtureSha256)) throw new Error('Missing selection fingerprint');
    execFileSync('python3',['-c',`import zipfile,shutil
with zipfile.ZipFile('source-artifact.zip') as a:
 names=[n for n in a.namelist() if n.rsplit('/',1)[-1]=='selection.json.gz']
 if len(names)!=1 or a.getinfo(names[0]).file_size>20*1024*1024: raise RuntimeError('Invalid compact selection fixture')
 with a.open(names[0]) as src,open('selection.json.gz','wb') as dst: shutil.copyfileobj(src,dst)
`],{stdio:'pipe'});
    const actual=createHash('sha256').update(await fs.readFile('selection.json.gz')).digest('hex');
    if(actual!==source.fixtureSha256) throw new Error('Selection fingerprint changed');
    await import('./verify-selection-neon.mjs');
  } else {
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
  }
} catch(error) {
  console.error('ONTAP_STAGE_BOOTSTRAP_FAILED',String(error.code || 'source_or_configuration_error'));
  process.exitCode=1;
}
