import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).parent))
import dependency_provenance as p

class Tests(unittest.TestCase):
    def tree(self, root):
        for name in ['pipeline/scripts/selector.py','pipeline/registers/r.csv','pipeline/geo/g.csv','pipeline/config/c.json']:
            path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(name)
        return p.snapshot(root)

    def test_input_output_exclusions_and_extra_dependencies(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);before=self.tree(root)
            for name in ['pipeline/input/feed.xlsx','pipeline/output-admin-service/jobs.json','pipeline/reports-daily/log.txt']:
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('generated')
            self.assertEqual(p.snapshot(root),before)
            path=root/'pipeline/config/new.json';path.write_text('new')
            self.assertNotEqual(p.snapshot(root),before)

    def test_copy_mutation_and_source_changes_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);files=self.tree(root);capture={'files':files}
            p.verify_copy(capture,root)
            (root/'pipeline/config/c.json').write_text('changed')
            with self.assertRaisesRegex(ValueError,'Scratch'):p.verify_copy(capture,root)
            with self.assertRaisesRegex(ValueError,'changed during'):p.finish_capture(capture,root,
                archive_sha256='a'*64,workbook_sha256='b'*64,workbook_created=None,
                families=[],observer_modules={},outputs_sha256='c'*64,output_scopes=[])

    def test_allowlisted_environment_and_uncommitted_guard(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);files=self.tree(root)
            with patch.object(p.subprocess,'check_output',return_value='a'*40),patch.object(p,'revision_inventory',return_value={'files':files}),patch.object(p.importlib.metadata,'version',return_value='1.0'),patch.dict(os.environ,{'ONTAP_FEED_DATE':'2026-11-02','SECRET_CONNECTION':'must-not-appear'}):
                captured=p.start_capture(root)
                self.assertNotIn('SECRET_CONNECTION',json.dumps(captured))
                result=p.finish_capture(captured,root,archive_sha256='a'*64,
                    workbook_sha256='b'*64,workbook_created='2026-11-02T07:30:00',
                    families=['admin_service'],observer_modules={'x':'admin_service'},
                    outputs_sha256='c'*64,output_scopes=['admin_service:Test'])
                self.assertEqual(json.loads(result['context']['timeContext'])['feedDateOverride'],'2026-11-02')
                self.assertTrue(result['sourceUnchanged'])
            with patch.object(p.subprocess,'check_output',return_value='a'*40),patch.object(p,'revision_inventory',return_value={'files':{}}):
                with self.assertRaisesRegex(ValueError,'Uncommitted'):p.start_capture(root)

    def test_symlinks_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);self.tree(root)
            (root/'pipeline/config/alias').symlink_to(root/'pipeline/config/c.json')
            with self.assertRaisesRegex(ValueError,'Symlink'):p.snapshot(root)

if __name__=='__main__':unittest.main()
