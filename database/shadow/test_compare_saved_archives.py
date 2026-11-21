import gzip
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
    def test_wrong_pin_blocks_budget_without_verified_baseline(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'feed.zip';archive(path,[job('1')])
            result=compare.compare(path,path,{})
            self.assertIsNone(result['compactRawProjection'])
            self.assertFalse(result['databaseBaselineLink']['verified'])
            self.assertEqual(result['turnover']['unchanged'],1)
    def test_distinct_daily_and_neon_snapshots_use_correct_budget_baseline(self):
        with tempfile.TemporaryDirectory() as folder:
            previous,current=Path(folder)/'daily-old.zip',Path(folder)/'daily-new.zip'
            archive(previous,[job('1')]);archive(current,[job('1')])
            baseline={'feed_date':'2026-11-02','adverts':[{'supplier_job_id':'1','content_hash':'0'*64}]}
            measured=json.loads(Path(__file__).with_name('retention-measurement-2026-11-03.json').read_text())
            result=compare.compare(previous,current,measured,baseline)
            self.assertEqual(result['turnover']['changed'],0)
            self.assertEqual(result['databaseBaselineTurnover']['changed'],1)
            self.assertEqual(result['compactRawProjection']['changedOrNewAdverts'],1)
            self.assertFalse(result['databaseBaselineLink']['previousZipMatchesNeonPin'])
            self.assertTrue(result['databaseBaselineLink']['verified'])
    def test_pinned_archive_checksum_and_source_hashes_verified(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'baseline.gz'
            packet={'version':1,'feedDate':'2026-11-02','state':{'report':{'archiveSha256':compare.PREVIOUS_SHA},'sourceHashes':[['1','a'*64]]}}
            path.write_bytes(gzip.compress(json.dumps(packet).encode()))
            with self.assertRaisesRegex(ValueError,'checksum'):compare.load_pinned_baseline(path)
            with patch.object(compare,'BASELINE_SHA',compare.checksum(path)),patch.object(compare,'BASELINE_BYTES',path.stat().st_size),patch.object(compare,'PREVIOUS_DIAGNOSTICS',{'uniqueSupplierIds':1,'conflictingIdsHeld':[]}):
                result=compare.load_pinned_baseline(path)
                self.assertEqual(result['adverts'][0]['content_hash'],'a'*64)

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
    def test_november_four_pin_requires_exact_archive_and_conflict_receipt(self):
        with tempfile.TemporaryDirectory() as folder:
            previous,current=Path(folder)/'old.zip',Path(folder)/'new.zip'
            archive(previous,[job('1')]);archive(current,[job('1')])
            digest=compare.checksum(current)
            diag=fingerprint_archive(current)['diagnostics']
            measured={'maximumDatabaseBytes':800*1024*1024,'database':{'bytes':400000000},
                      'adverts':{'rows':1},'tables':[{'name':n,'total_bytes':300} for n in ['supplier_adverts','jobs','advert_appearances','selection_decisions']],
                      'decisions':[{'scope':'production:admin_service','rows':8}],
                      'sevenSnapshotCalibrationBytes':51_003_392}
            baseline={'feed_date':'2026-11-02','adverts':[{'supplier_job_id':'1','content_hash':diag and '0'*64}]}
            with patch.dict(compare.PINNED_CURRENT_ARCHIVES,{'2026-11-04':digest}), \\
                 patch.dict(compare.PINNED_CURRENT_DIAGNOSTICS,{'2026-11-04':diag}):
                result=compare.compare(previous,current,measured,baseline,current_date='2026-11-04')
            self.assertEqual(result['snapshots']['2026-11-04']['diagnostics'],diag)
            self.assertEqual(result['combinedIllustrativeForecast']['sevenSnapshotCalibrationBytes'],51_003_392)
            self.assertFalse(result['combinedIllustrativeForecast']['importAuthorized'])
            with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):
                compare.compare(previous,current,measured,baseline,current_date='2026-11-04',
                                expected_current_sha256='f'*64)

    def test_download_allows_only_declared_fresh_archive_key(self):
        class S3:
            def head_object(self,**kw):
                assert kw['Key']=='jobg8/raw/2026-11-04.zip'
                return {'ContentLength':3,'ETag':'pinned'}
            def get_object(self,**kw):
                assert kw['IfMatch']=='pinned';return {'Body':io.BytesIO(b'zip')}
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/'fresh.zip'
            out=compare.download_saved(S3(),'2026-11-04',target)
            self.assertEqual(out['bytes'],3)
            self.assertEqual(out['key'],'jobg8/raw/2026-11-04.zip')

    def test_missing_identity_and_conflict_threshold_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'feed.zip';archive(path,['<Job><Position>Admin</Position></Job>'])
            with self.assertRaises(ValueError):fingerprint_archive(path)
            archive(path,[x for n in range(16) for x in [job(str(n)),job(str(n),'Changed')]])
            with self.assertRaisesRegex(ValueError,'15 conflicting'):fingerprint_archive(path)

if __name__=='__main__':unittest.main()
