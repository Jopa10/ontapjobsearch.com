import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts.verify_overview_production import resolve, needs_rebuild

SHA = 'c' * 40


class ProductionSourceTests(unittest.TestCase):
    @patch('scripts.verify_overview_production.subprocess.run')
    @patch('scripts.verify_overview_production.live_sha', return_value=SHA)
    def test_direct_recovery_uses_live_commit_and_checks_main_ancestry(self, live, git):
        self.assertEqual(resolve(), SHA)
        git.assert_called_once_with(['git', 'merge-base', '--is-ancestor', SHA, 'origin/main'], check=True)

    @patch('scripts.verify_overview_production.live_sha', return_value=SHA)
    def test_stale_deployment_receipt_is_rejected(self, live):
        with tempfile.TemporaryDirectory() as folder:
            receipt = Path(folder) / 'receipt'
            receipt.write_text('d' * 40)
            with self.assertRaisesRegex(RuntimeError, 'receipt'):
                resolve(receipt)

    @patch('scripts.verify_overview_production.live_sha', return_value=SHA)
    def test_changed_live_commit_blocks_report_commit(self, live):
        with self.assertRaisesRegex(RuntimeError, 'changed'):
            resolve(expected='d' * 40)

    def test_only_matching_provenance_skips_rebuild(self):
        with tempfile.TemporaryDirectory() as folder:
            report = Path(folder) / 'overview.md'
            self.assertTrue(needs_rebuild(SHA, report))
            report.write_text('Generated: yesterday\nUnique live jobs: 3,211')
            self.assertTrue(needs_rebuild(SHA, report))
            report.write_text(f'Production source commit: `{SHA}`')
            self.assertFalse(needs_rebuild(SHA, report))
            self.assertTrue(needs_rebuild('d' * 40, report))

class CanonicalInventoryTests(unittest.TestCase):
    def test_duplicate_ids_share_one_public_job_but_keep_both_family_placements(self):
        import json
        from scripts.build_verified_region_overview import published_inventory
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'app').mkdir()
            (root / 'generated').mkdir()
            row = {'job_id': '1', 'title': 'Admin', 'location': 'Leeds', 'region': 'West', 'category': 'Admin', 'source': 'JobG8', 'apply_url': 'https://example/1'}
            duplicate = dict(row, job_id='2', category='Finance')
            (root / 'app/jobs.json').write_text(json.dumps([row, duplicate]))
            (root / 'generated/published-jobs.json').write_text(json.dumps([row]))
            (root / 'generated/published-job-canonical-ids.json').write_text(json.dumps({'1': '1', '2': '1'}))
            inventory = published_inventory(root / 'app')
        self.assertEqual(len(inventory.jobs), 1)
        self.assertEqual([p.canonical_job_id for p in inventory.placements], ['1', '1'])
        self.assertEqual([p.category for p in inventory.placements], ['Admin', 'Finance'])
