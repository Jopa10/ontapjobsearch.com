import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import copy,tempfile,unittest
import prepare_archive_lifecycle as m
class Tests(unittest.TestCase):
 def test_only_raw_prefix_changes(self):
  before=copy.deepcopy(m.EXPECTED);after=m.proposal(before)
  self.assertEqual(after['Rules'][0]['Expiration'],{'Days':93});self.assertEqual(after['Rules'][0]['Filter'],{'Prefix':'jobg8/raw/'});self.assertEqual(before,m.EXPECTED)
  with self.assertRaises(ValueError):m.proposal({'Rules':[]})
 def test_plan_no_writes_apply_backup_readback(self):
  class Client:
   def __init__(self):self.config=copy.deepcopy(m.EXPECTED);self.writes=0
   def get_bucket_lifecycle_configuration(self,**kw):return self.config
   def get_paginator(self,name):return self
   def paginate(self,**kw):return [{'CommonPrefixes':[{'Prefix':'jobg8/'}] if not kw['Prefix'] else [{'Prefix':'jobg8/raw/'}]}]
   def put_bucket_lifecycle_configuration(self,**kw):self.writes+=1;self.config=kw['LifecycleConfiguration']
  c=Client();self.assertFalse(m.execute(c)['applied']);self.assertEqual(c.writes,0)
  with tempfile.TemporaryDirectory() as d:
   r=m.execute(c,True,Path(d));self.assertTrue(Path(r['backup_file']).is_file());self.assertTrue(r['readback_verified']);self.assertEqual(c.writes,1)
 def test_unknown_prefix_blocks(self):
  class Client:
   def get_paginator(self,n):return self
   def paginate(self,**kw):return [{'CommonPrefixes':[{'Prefix':'unrelated/'}]}]
  with self.assertRaises(ValueError):m.check_prefixes(Client())
if __name__=='__main__':unittest.main()
