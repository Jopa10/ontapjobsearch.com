"""Interrupt the actual daily Preview deploy twice, then retry normally."""
import json,os,re,subprocess,sys
from pathlib import Path
cli=sys.argv[1];root=Path(os.environ['RUNNER_TEMP'])
gate=json.loads(Path('failure-recovery-request.json').read_text())
assert gate['mode']=='failure_recovery'
fault=Path('daily-fault-injection.json')
base=[cli,'deploy','--yes','--target=preview','--scope','ontap1','--token',os.environ['VERCEL_TOKEN']]
def parse_marker(text,marker):
 matches=re.findall(re.escape(marker)+r'\s+(\{[^\n]+\})',text)
 assert matches,'Missing '+marker
 return json.loads(matches[-1])
def deploy(logname):
 p=subprocess.run(base,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 text=p.stdout
 path=root/logname;path.write_text(text)
 if p.returncode:
  urls=re.findall(r'https://[^\s]+\.vercel\.app',text)
  if urls and 'ONTAP_DAILY_FAILURE_VISIBILITY' not in text:
   logs=subprocess.run([cli,'inspect',urls[-1],'--logs','--scope','ontap1','--token',os.environ['VERCEL_TOKEN']],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   text+='\n'+logs.stdout;path.write_text(text)
 return p.returncode,text
failures=[]
try:
 for stage in ['after-payload-write','before-commit']:
  fault.write_text(json.dumps({'enabled':True,'runToken':gate['runToken'],'stage':stage}))
  status,log=deploy('daily-failure-'+stage+'.log')
  if status==0:raise AssertionError('Expected deliberate interruption instead of successful deployment: '+stage)
  if 'ONTAP_EXPECTED_DAILY_INTERRUPTION' not in log:
   print(log[-12000:]);raise AssertionError('Deployment failed for an unexpected reason')
  baseline=parse_marker(log,'ONTAP_DAILY_FAILURE_BASELINE')
  observed=parse_marker(log,'ONTAP_DAILY_FAILURE_VISIBILITY')
  assert observed['status']=='passed' and observed['stage']==stage
  assert observed['partialSetVisible'] is False and observed['independentBackend'] is True
  assert observed['readerDigest']==baseline['digest']
  assert observed['readerRecordCount']==baseline['recordCount']
  failures.append({'baseline':baseline,'observation':observed,'expectedFailureConfirmed':True})
  print('ONTAP_DAILY_EXPECTED_FAILURE '+json.dumps(observed),flush=True)
 assert failures[0]['baseline']['digest']==failures[1]['baseline']['digest'],'First failed transaction did not restore the exact original set'
 fault.unlink()
 status,log=deploy('daily-deploy.log')
 if status:
  print(log[-12000:]);raise AssertionError('Normal retry failed')
 urls=re.findall(r'https://[^\s]+\.vercel\.app',log);assert urls,'Retry deployment URL missing'
 with (root/'daily-refresh-report.json').open('wb') as out:
  p=subprocess.run([cli,'curl','/daily-refresh-report.json','--deployment',urls[-1],'--scope','ontap1'],stdout=out,stderr=subprocess.PIPE)
  assert p.returncode==0,p.stderr.decode()[-600:]
 retry=json.loads((root/'daily-refresh-report.json').read_text())
 assert retry['status']=='passed' and retry['duplicates']==0
 assert retry['exactIdsAndDecisionsMatch'] and retry['fullPayloadAndHashesMatch'] and retry['exactScopeOrderingMatch']
 residue=retry['failureResidue']
 assert residue['remainingProbeRows']==0 and residue['remainingFutureReceipts']==0
 assert residue['publication']['digest']==failures[0]['baseline']['digest'],'Normal retry did not restore exact original publication'
 assert retry['insertedRows']==0 and retry['updatedPayloadRows']==0 and retry['metadataOnlyUpdatedRows']==0
 report={'status':'passed','test':'actual daily workflow interruption and normal retry','faults':failures,
  'previousCompleteSetRemainedVisible':True,'partialNewSetVisible':False,'rollbackRestoredExactDigest':True,
  'normalRetryPassed':True,'retryDate':retry['feedDate'],'selectedIds':retry['selectedIds'],'records':retry['neonRows'],'scopes':retry['scopeCount'],
  'duplicates':0,'probeRowsRemaining':0,'futureCompletionReceiptsRemaining':0,'retryRowsWritten':0,'productionChanged':False,
  'testData':'one clearly marked fictional next-day record per aborted transaction; never committed'}
 (root/'daily-failure-recovery-report.json').write_text(json.dumps(report,indent=2)+'\n')
 print('ONTAP_DAILY_FAILURE_RECOVERY '+json.dumps(report),flush=True)
finally:
 fault.unlink(missing_ok=True)
