"""Prepare a separate archive-only Preview role. Default is read-only plan; --apply creates only this role."""
import argparse,json
ACCOUNT='179402568934';ROLE='OntapNeonPreviewArchiveRole';POLICY_NAME='OntapPreviewAdvertArchiveOnly'
BUCKET='ontap-jobg8-archive-179402568934-eu-west-2-an'
TRUST={'Version':'2012-10-17','Statement':[{'Effect':'Allow','Principal':{'Federated':'arn:aws:iam::'+ACCOUNT+':oidc-provider/token.actions.githubusercontent.com'},'Action':'sts:AssumeRoleWithWebIdentity','Condition':{'StringEquals':{'token.actions.githubusercontent.com:aud':'sts.amazonaws.com','token.actions.githubusercontent.com:sub':'repo:Jopa10/ontapjobsearch.com:ref:refs/heads/feat/neon-shadow-database'}}}]}
POLICY={'Version':'2012-10-17','Statement':[
 {'Sid':'ReadVersionArchives','Effect':'Allow','Action':['s3:GetObject','s3:GetObjectVersion'],'Resource':'arn:aws:s3:::'+BUCKET+'/ontap-shadow/advert-versions/*'},
 {'Sid':'CreateOnlyNewVersionArchives','Effect':'Allow','Action':'s3:PutObject','Resource':'arn:aws:s3:::'+BUCKET+'/ontap-shadow/advert-versions/*','Condition':{'StringEquals':{'s3:if-none-match':'*','s3:x-amz-server-side-encryption':'AES256'}}}]}
def execute(iam,sts,apply=False):
 assert sts.get_caller_identity()['Account']==ACCOUNT,'Wrong AWS account'
 provider=iam.get_open_id_connect_provider(OpenIDConnectProviderArn='arn:aws:iam::'+ACCOUNT+':oidc-provider/token.actions.githubusercontent.com')
 assert 'sts.amazonaws.com' in provider['ClientIDList']
 exists=True
 try:
  role=iam.get_role(RoleName=ROLE)['Role']
  assert role['AssumeRolePolicyDocument']==TRUST,'Existing role trust differs; do not overwrite'
  assert not iam.list_attached_role_policies(RoleName=ROLE)['AttachedPolicies'],'Unexpected managed permissions on role'
  names=iam.list_role_policies(RoleName=ROLE)['PolicyNames']
  assert set(names)<={POLICY_NAME},'Unexpected inline policies on role'
  if POLICY_NAME in names:assert iam.get_role_policy(RoleName=ROLE,PolicyName=POLICY_NAME)['PolicyDocument']==POLICY,'Existing policy differs; do not overwrite'
 except iam.exceptions.NoSuchEntityException:exists=False
 result={'roleArn':'arn:aws:iam::'+ACCOUNT+':role/'+ROLE,'trust':TRUST,'policy':POLICY,'mode':'plan','existingRole':exists,'productionRoleChanged':False,'bucketLifecycleChanged':False}
 if apply:
  if not exists:iam.create_role(RoleName=ROLE,AssumeRolePolicyDocument=json.dumps(TRUST),MaxSessionDuration=3600,Description='Isolated Ontap Neon Preview immutable advert-version archive writes only')
  iam.put_role_policy(RoleName=ROLE,PolicyName=POLICY_NAME,PolicyDocument=json.dumps(POLICY))
  assert iam.get_role(RoleName=ROLE)['Role']['AssumeRolePolicyDocument']==TRUST
  assert iam.get_role_policy(RoleName=ROLE,PolicyName=POLICY_NAME)['PolicyDocument']==POLICY
  result['mode']='applied-and-readback-verified'
 return result
def main():
 import boto3
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--apply',action='store_true');args=p.parse_args()
 print(json.dumps(execute(boto3.client('iam'),boto3.client('sts'),args.apply),indent=2))
if __name__=='__main__':main()
