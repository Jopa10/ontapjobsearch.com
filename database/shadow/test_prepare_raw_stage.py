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
 def test_missing_identity_stops_preparation(self):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/'bad.zip'
   with zipfile.ZipFile(path,'w') as archive:archive.writestr('Jobs.xml','<Jobs><Job><Position>Admin</Position></Job></Jobs>')
   with self.assertRaises(ValueError):module.load_archive(path)

if __name__=='__main__':unittest.main()
