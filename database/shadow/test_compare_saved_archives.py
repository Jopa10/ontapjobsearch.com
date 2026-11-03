import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
sys.path.insert(0, str(Path(__file__).parent))
import compare_saved_archives as compare
from prepare_raw_stage import fingerprint_archive, load_archive


def job(ref,title='Admin'):
    return f'<Job><DisplayReference>{ref}</DisplayReference><Position>{title}</Position><ApplicationURL>https://example.org/{ref}</ApplicationURL><Description>Office &amp; reception</Description></Job>'

def archive(path, rows):
    with zipfile.ZipFile(path,'w') as z:z.writestr('Jobs.xml','<Jobs>'+''.join(rows)+'</Jobs>')

class Tests(unittest.TestCase):
    def test_streamed_hashes_match_existing_loader_and_quarantine(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'feed.zip';archive(path,[job('1'),job('1'),job('2'),job('2','Changed'),job('3')])
            old,diag=load_archive(path);summary=fingerprint_archive(path)
            self.assertEqual(summary['diagnostics'],diag)
            expected={r['/Job/DisplayReference']:hashlib.sha256(json.dumps(r,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest() for r in old}
            self.assertEqual({r['supplier_job_id']:r['content_hash'] for r in summary['adverts']},expected)
            self.assertNotIn('Office',json.dumps(summary))
    def test_current_turnover_and_compact_budget_are_forecasts_only(self):
        with tempfile.TemporaryDirectory() as folder:
            previous,current=Path(folder)/'old.zip',Path(folder)/'new.zip'
            archive(previous,[job('1'),job('2'),job('3')]);archive(current,[job('1'),job('2','Changed'),job('4')])
            measured={'maximumDatabaseBytes':800*1024*1024,'database':{'bytes':407347200},'adverts':{'rows':3},'tables':[{'name':n,'total_bytes':300} for n in ['supplier_adverts','jobs','advert_appearances','selection_decisions']],'decisions':[{'scope':'production:admin_service','rows':24}]}
            with patch.object(compare,'PREVIOUS_SHA',compare.checksum(previous)),patch.object(compare,'PREVIOUS_DIAGNOSTICS',fingerprint_archive(previous)['diagnostics']):
                r=compare.compare(previous,current,measured)
            self.assertEqual([r['turnover'][k] for k in ['unchanged','changed','added_vs_previous','absent_vs_previous']],[1,1,1,1])
            self.assertIsNone(r['turnover']['returned_from_earlier_history'])
            self.assertFalse(r['expiryApplied']);self.assertFalse(r['databaseChanged'])
            self.assertFalse(r['compactRawProjection']['selectionDisplayGrowthIncluded'])
            self.assertFalse(r['compactRawProjection']['importAuthorized'])
    def test_wrong_pin_fails_before_parse(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'feed.zip';archive(path,[job('1')])
            with self.assertRaisesRegex(ValueError,'pinned source'):compare.compare(path,path,{})
    def test_read_only_s3_download_pins_etag_and_owner(self):
        class S3:
            def head_object(self,**kw):
                assert kw['ExpectedBucketOwner']==compare.OWNER
                return {'ContentLength':3,'ETag':'pinned'}
            def get_object(self,**kw):
                assert kw['IfMatch']=='pinned';assert kw['Key']=='jobg8/raw/2026-11-03.zip'
                return {'Body':io.BytesIO(b'zip')}
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/'feed.zip';r=compare.download_saved(S3(),'2026-11-03',target)
            self.assertEqual(r['bytes'],3);self.assertEqual(target.read_bytes(),b'zip')
    def test_missing_identity_and_conflict_threshold_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'feed.zip';archive(path,['<Job><Position>Admin</Position></Job>'])
            with self.assertRaises(ValueError):fingerprint_archive(path)
            archive(path,[x for n in range(16) for x in [job(str(n)),job(str(n),'Changed')]])
            with self.assertRaisesRegex(ValueError,'15 conflicting'):fingerprint_archive(path)

if __name__=='__main__':unittest.main()
