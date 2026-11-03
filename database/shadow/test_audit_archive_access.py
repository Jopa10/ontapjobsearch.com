import importlib.util
from pathlib import Path
import unittest
s=importlib.util.spec_from_file_location('audit',Path(__file__).with_name('audit_archive_access.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class ReadOnlyAuditTests(unittest.TestCase):
 def test_only_read_methods_and_one_byte_object_probe(self):
  calls=[]
  class Body:
   def read(self,n):self.n=n;return b'x'
   def close(self):calls.append('close')
  class Client:
   def __getattr__(self,name):
    allowed={'get_caller_identity','get_bucket_location','get_bucket_lifecycle_configuration','get_bucket_versioning','get_object_lock_configuration','get_bucket_encryption','get_role','simulate_principal_policy','head_object','get_object'}
    if name not in allowed:raise AssertionError(name)
    def call(**kwargs):
     calls.append(name)
     if name=='get_role':return {'Role':{'AssumeRolePolicyDocument':{}}}
     if name=='get_object':self.range=kwargs['Range'];return {'Body':Body()}
     return {}
    return call
  c=Client();r=m.audit(c,c,c,['2026-11-03']);self.assertEqual(r['checks']['raw_get_2026-11-03']['result']['bytes_read'],1);self.assertEqual(c.range,'bytes=0-0');self.assertIn('close',calls)
 def test_denial_remains_unverified(self):
  class Client:
   def __getattr__(self,name):
    def deny(**kwargs):raise PermissionError()
    return deny
  c=Client();r=m.audit(c,c,c,[]);self.assertTrue(all(x['status']=='unverified' for x in r['checks'].values()))
if __name__=='__main__':unittest.main()
