import importlib.util,io,json,os,subprocess,tempfile,unittest,zipfile
from datetime import datetime as RealDatetime
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('daily_source',Path(__file__).with_name('resolve-daily-source.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ResolverTests(unittest.TestCase):
 def run_case(self,clock_day,feed_day,receipt=True):
  class Clock:
   @staticmethod
   def now(tz):return RealDatetime.fromisoformat(clock_day+'T12:00:00').replace(tzinfo=tz)
  app='b'*40;run_sha='a'*40;feed_run=int(feed_day.replace('-',''))
  state={'completed_cycles':{feed_day:{'morning':{'run_id':str(feed_run),'completed_at':feed_day+'T08:20:00+00:00'}}}}
  def api(path):
   if path.startswith('/actions/workflows/'):return {'workflow_runs':[{'id':77}]}
   if path=='/actions/runs/77/artifacts':return {'artifacts':[{'id':1,'name':'verified-production-sha','expired':False}] if receipt else []}
   if path=='/actions/runs/'+str(feed_run):return {'id':feed_run,'head_branch':'main','status':'completed','conclusion':'success','path':'.github/workflows/run-full-jobg8-daily-process.yml','head_sha':run_sha}
   if path=='/actions/runs/'+str(feed_run)+'/artifacts':return {'artifacts':[{'id':i,'name':name,'expired':False,'digest':'sha256:'+'c'*64} for i,name in enumerate(['service-admin-output','support-worker-output'],10)]}
   raise AssertionError(path)
  buffer=io.BytesIO()
  with zipfile.ZipFile(buffer,'w') as z:z.writestr('verified-production-sha.txt',app)
  previous=os.getcwd()
  with tempfile.TemporaryDirectory() as tmp:
   os.chdir(tmp)
   try:
    with patch.object(m,'datetime',Clock),patch.object(m,'api',api),patch.object(m,'content',lambda p,r:json.dumps(state).encode()),patch.object(m,'artifact_bytes',lambda a:buffer.getvalue()),patch.dict(os.environ,{'GITHUB_OUTPUT':str(Path(tmp)/'outputs')}):
     return m.resolve()
   finally:os.chdir(previous)
 def test_same_logic_follows_tuesday_then_wednesday_without_date_input(self):
  for day in ['2026-11-17','2026-11-18']:
   r=self.run_case(day,day)
   self.assertEqual(r['archiveDate'],day)
   self.assertEqual(r['archiveKey'],'jobg8/raw/'+day+'.zip')
   self.assertFalse(r['dateProvidedByRequest'])
   self.assertEqual(r['productionOutputRunId'],int(day.replace('-','')))
 def test_yesterdays_publication_cannot_be_used_as_todays(self):
  with self.assertRaises(AssertionError):self.run_case('2026-11-18','2026-11-17')
 def test_saved_feed_uses_automatically_derived_s3_key_without_url_secret(self):
  source={'archiveDate':'2026-11-20','archiveKey':'jobg8/raw/2026-11-20.zip'}
  with tempfile.TemporaryDirectory() as tmp:
   def get_object(args,**kwargs):
    self.assertEqual(args[:4],['aws','s3api','get-object','--bucket'])
    self.assertEqual(args[args.index('--key')+1],'jobg8/raw/2026-11-20.zip')
    self.assertEqual(args[args.index('--expected-bucket-owner')+1],'179402568934')
    Path(args[-1]).write_bytes(b'saved-zip')
    return subprocess.CompletedProcess(args,0,'{}','')
   clean={k:v for k,v in os.environ.items() if k!='ONTAP_SAVED_FEED_URL'}
   clean['RUNNER_TEMP']=tmp
   with patch.object(m.subprocess,'run',side_effect=get_object),patch.dict(os.environ,clean,clear=True):
    data,origin=m.restore_archive(source)
  self.assertEqual(data,b'saved-zip')
  self.assertEqual(origin['kind'],'S3 saved archive via GitHub OIDC')
  self.assertEqual(origin['key'],'jobg8/raw/2026-11-20.zip')
 def test_missing_verified_live_commit_receipt_stops_discovery(self):
  with self.assertRaises(AssertionError):self.run_case('2026-11-18','2026-11-18',receipt=False)
if __name__=='__main__':unittest.main()
