import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
spec = importlib.util.spec_from_file_location('prepare', Path(__file__).with_name('prepare_raw_stage.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class PrepareTests(unittest.TestCase):
 def test_nested_stages_and_source_fingerprint(self):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/'feed.zip'
   jobs=''.join(f'<Job><DisplayReference>{i}</DisplayReference><Position>Admin {i}</Position><ApplicationURL>https://example.org/{i}</ApplicationURL></Job>' for i in range(100))
   with zipfile.ZipFile(path,'w') as archive:archive.writestr('Jobs.xml','<Jobs>'+jobs+'</Jobs>')
   a=module.prepare(path,20,'2026-11-02','test',800*1024*1024)
   b=module.prepare(path,50,'2026-11-02','test',800*1024*1024)
   c=module.prepare(path,100,'2026-11-02','test',800*1024*1024)
   self.assertEqual(a['records'],b['records'][:20]);self.assertEqual(b['records'],c['records'][:50])
   self.assertEqual(a['archiveSha256'],c['archiveSha256']);self.assertEqual(c['totalReceived'],100)
 def test_exact_duplicates_collapse_and_conflicting_ids_are_held(self):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/'dupes.zip'
   def job(ref,title):return f'<Job><DisplayReference>{ref}</DisplayReference><Position>{title}</Position><ApplicationURL>https://example.org/{ref}</ApplicationURL></Job>'
   xml='<Jobs>'+job('1','Admin')*2+job('2','Office')+job('2','Different')+job('3','Reception')+'</Jobs>'
   with zipfile.ZipFile(path,'w') as archive:archive.writestr('Jobs.xml',xml)
   result=module.prepare(path,100,'2026-11-02','test',800*1024*1024)
   self.assertEqual(result['totalReceived'],5)
   self.assertEqual(result['eligibleRecords'],2)
   self.assertEqual(result['receiptDiagnostics']['exactRepeatRows'],1)
   self.assertEqual(result['receiptDiagnostics']['conflictingIdsHeld'],['2'])
   self.assertEqual({r['/Job/DisplayReference'] for r in result['records']},{'1','3'})
 def test_missing_identity_stops_preparation(self):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/'bad.zip'
   with zipfile.ZipFile(path,'w') as archive:archive.writestr('Jobs.xml','<Jobs><Job><Position>Admin</Position></Job></Jobs>')
   with self.assertRaises(ValueError):module.load_archive(path)

if __name__=='__main__':unittest.main()
