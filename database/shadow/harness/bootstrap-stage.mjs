import fs from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import path from 'node:path';

try {
  if(process.env.VERCEL_ENV!=='preview') throw new Error('Preview required');
  const source=JSON.parse(await fs.readFile('source-download.json','utf8'));
  let bytes;
  if(source.localArtifact) {
    const localPath=path.resolve(process.cwd(),source.localArtifact);
    if(path.dirname(localPath)!==process.cwd() || path.basename(localPath)!=='source-artifact.zip') throw new Error('Unexpected local artifact path');
    bytes=await fs.readFile(localPath);
  } else {
    const url=new URL(source.downloadUrl);
    if(url.protocol!=='https:' || !url.hostname.endsWith('.oaiusercontent.com')) throw new Error('Unexpected temporary artifact host');
    const response=await fetch(url,{signal:AbortSignal.timeout(60000)});
    if(!response.ok) throw new Error('Source download failed');
    bytes=Buffer.from(await response.arrayBuffer());
  }
  if(source.mode==='selection_parity' && bytes.length>25*1024*1024) throw new Error('Selection artifact too large');
  if(source.mode==='fresh_selection_neon' && bytes.length>200*1024*1024) throw new Error('Fresh selector artifact too large');
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
  } else if(source.mode==='fresh_selection_neon') {
    for(const key of ['rawStageSha256','fixtureSha256','outputsSha256','productionOutputsSha256','productionReferenceSha256','feedCategoryMapSha256']) if(!/^[a-f0-9]{64}$/.test(source[key]||'')) throw new Error('Missing fresh selector artifact fingerprint');
    execFileSync('python3',['-c',`import zipfile,shutil
with zipfile.ZipFile('source-artifact.zip') as a:
 expected={'raw-stage.json.gz','selection.json.gz','plain/outputs.json','production-outputs.json','production-reference.json','feed-category-map.json'}
 for name in expected:
  matches=[n for n in a.namelist() if n==name]
  if len(matches)!=1: raise RuntimeError('Missing or duplicate '+name)
  with a.open(matches[0]) as src,open(name.rsplit('/',1)[-1],'wb') as dst: shutil.copyfileobj(src,dst)
`],{stdio:'pipe'});
    const rawHash=createHash('sha256').update(await fs.readFile('raw-stage.json.gz')).digest('hex');
    const selectionHash=createHash('sha256').update(await fs.readFile('selection.json.gz')).digest('hex');
    const outputsHash=createHash('sha256').update(await fs.readFile('outputs.json')).digest('hex');
    const productionOutputsHash=createHash('sha256').update(await fs.readFile('production-outputs.json')).digest('hex');
    const productionReferenceHash=createHash('sha256').update(await fs.readFile('production-reference.json')).digest('hex');
    const feedCategoryMapHash=createHash('sha256').update(await fs.readFile('feed-category-map.json')).digest('hex');
    if(rawHash!==source.rawStageSha256 || selectionHash!==source.fixtureSha256 || outputsHash!==source.outputsSha256
      || productionOutputsHash!==source.productionOutputsSha256 || productionReferenceHash!==source.productionReferenceSha256
      || feedCategoryMapHash!==source.feedCategoryMapSha256) throw new Error('Fresh selector artifact fingerprint changed');
    const verifier = await import('./verify-fresh-selection-neon.mjs');
    await verifier.runFreshSelectionReadback();
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
  const detail=String(error.message || '').split('\\n')[0].slice(0,160);
  console.error('ONTAP_STAGE_BOOTSTRAP_FAILED',String(error.code || error.name || 'source_or_configuration_error'),detail);
  process.exitCode=1;
}
