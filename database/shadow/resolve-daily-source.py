"""Resolve today's completed production publication and its exact saved inputs."""
import base64,hashlib,io,json,os,re,subprocess,sys,urllib.request,urllib.parse,urllib.error,zipfile,xml.etree.ElementTree as ET
from datetime import datetime
import datetime as datetime_lib
from pathlib import Path
from zoneinfo import ZoneInfo
API='https://api.github.com/repos/'+os.environ['GITHUB_REPOSITORY']
class Redirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  out=super().redirect_request(req,fp,code,msg,headers,newurl)
  if out and urllib.parse.urlparse(req.full_url).netloc!=urllib.parse.urlparse(newurl).netloc:out.remove_header('Authorization')
  return out
opener=urllib.request.build_opener(Redirect())
def raw(path):
 url=path if path.startswith('https://') else API+path
 headers={'User-Agent':'ontap-neon-preview-daily'}
 if url.startswith(API):headers['Authorization']='Bearer '+os.environ['GH_TOKEN']
 try:
  with opener.open(urllib.request.Request(url,headers=headers),timeout=120) as r:return r.read()
 except urllib.error.HTTPError as e:
  body=e.read()
  try:
   root=ET.fromstring(body)
   fields={node.tag.rsplit('}',1)[-1]:(node.text or '') for node in root.iter()}
   code=fields.get('Code','unknown');message=fields.get('Message','no service error text')
  except Exception:code='unavailable';message='non-XML error response'
  raise RuntimeError('Saved source request failed: HTTP '+str(e.code)+'; '+code+': '+message) from None
def api(path):return json.loads(raw(path))
def content(path,ref):
 d=api('/contents/'+path+'?ref='+urllib.parse.quote(ref,safe=''))
 return base64.b64decode(d['content'])
def artifact_bytes(a):
 data=raw(a['archive_download_url'])
 if a.get('digest'):assert hashlib.sha256(data).hexdigest()==a['digest'].removeprefix('sha256:')
 return data
def resolve():
 runs=api('/actions/workflows/deploy-vercel-after-publish.yml/runs?branch=main&status=success&per_page=10')['workflow_runs']
 assert runs,'No successful production publication deployment'
 deploy=runs[0]
 artifacts=api('/actions/runs/'+str(deploy['id'])+'/artifacts')['artifacts']
 match=[a for a in artifacts if a['name']=='verified-production-sha' and not a['expired']]
 assert len(match)==1,'Missing verified live production commit receipt'
 z=zipfile.ZipFile(io.BytesIO(artifact_bytes(match[0])))
 names=[n for n in z.namelist() if n.endswith('verified-production-sha.txt')]
 assert len(names)==1
 app_sha=z.read(names[0]).decode().strip()
 assert re.fullmatch('[a-f0-9]{40}',app_sha)
 state=json.loads(content('pipeline/reports-daily/jobg8-daily-cycle-state.json',app_sha))
 day=max(state['completed_cycles'])
 today=datetime.now(ZoneInfo('Europe/London')).date().isoformat()
 assert day==today,('Latest completed publication is not today; no stale update',day,today)
 cycles=state['completed_cycles'][day]
 assert len(cycles)==1,('Multiple JobG8 publications for today; AM source is ambiguous',list(cycles))
 cycle=next(iter(cycles.values()))
 completed=datetime_lib.datetime.fromisoformat(cycle['completed_at'].replace('Z','+00:00')).astimezone(ZoneInfo('Europe/London'))
 assert completed.hour < 12,('Selected JobG8 source is not an AM publication',cycle['run_id'],completed.isoformat())
 feed=api('/actions/runs/'+str(cycle['run_id']))
 assert feed['head_branch']=='main' and feed['status']=='completed' and feed['conclusion']=='success'
 assert feed['path']=='.github/workflows/run-full-jobg8-daily-process.yml'
 arts=api('/actions/runs/'+str(feed['id'])+'/artifacts')['artifacts']
 arts=[a for a in arts if a['name'] in {'service-admin-output','support-worker-output'} and not a['expired']]
 assert len(arts)==2
 result={'mode':'daily_latest','archiveDate':day,'archiveKey':'jobg8/raw/'+day+'.zip',
  'productionDeploymentRunId':deploy['id'],'productionOutputRunId':feed['id'],
  'productionAppCommitSha':app_sha,'productionRunCommitSha':feed['head_sha'],
  'publishedOutputArtifacts':[{'name':a['name'],'id':a['id'],'sha256':a['digest'].removeprefix('sha256:')} for a in arts],
  'dateSelection':'latest successful production deployment receipt and its completed JobG8 cycle',
  'dateProvidedByRequest':False}
 Path('daily-source.json').write_text(json.dumps(result,indent=2)+'\n')
 with open(os.environ['GITHUB_OUTPUT'],'a') as f:
  for k,v in {'day':day,'run_id':feed['id'],'app_sha':app_sha,'run_sha':feed['head_sha'],'artifact_ids':','.join(str(a['id']) for a in arts)}.items():f.write(k+'='+str(v)+'\n')
 print('ONTAP_AUTOMATIC_DAILY_SOURCE '+json.dumps(result))
 return result
def restore_archive(source):
 # Read the saved production archive with the branch-scoped GitHub AWS identity.
 # The feed date and S3 key come only from automatic publication discovery.
 day=source['archiveDate']
 key='jobg8/raw/'+day+'.zip'
 assert source['archiveKey']==key,'Resolved archive key does not match the automatically discovered publication date'
 path=Path(os.environ['RUNNER_TEMP'])/'daily-input'/'feed.zip'
 path.parent.mkdir(parents=True,exist_ok=True)
 result=subprocess.run(
  ['aws','s3api','get-object','--bucket','ontap-jobg8-archive-179402568934-eu-west-2-an',
   '--key',key,'--expected-bucket-owner','179402568934','--region','eu-west-2',str(path)],
  text=True,capture_output=True,timeout=180)
 if result.returncode:
  message=(result.stderr or '').strip()[:600]
  raise RuntimeError('Saved S3 archive read failed through the Preview AWS role: '+message)
 data=path.read_bytes()
 assert data,'Automatically retrieved saved feed archive is empty'
 return data,{'kind':'S3 saved archive via GitHub OIDC','bucket':'ontap-jobg8-archive-179402568934-eu-west-2-an','key':key}

def main():
 source=resolve()
 archive,origin=restore_archive(source)
 target=Path(os.environ['RUNNER_TEMP'])/'daily-input';target.mkdir(parents=True, exist_ok=True)
 (target/'feed.zip').write_bytes(archive)
 source.update(archiveSha256=hashlib.sha256(archive).hexdigest(),archiveOrigin=origin)
 Path('daily-source.json').write_text(json.dumps(source,indent=2)+'\n')
 print('ONTAP_DAILY_ARCHIVE '+json.dumps({'date':source['archiveDate'],'sha256':source['archiveSha256'],'origin':origin}))
if __name__=='__main__':main()
