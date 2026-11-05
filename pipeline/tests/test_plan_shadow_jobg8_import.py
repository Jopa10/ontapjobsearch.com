import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).parents[1] / 'scripts/plan_shadow_jobg8_import.py'
spec = importlib.util.spec_from_file_location('shadow_plan', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def job(ref='123', title='Administrator'):
    return {'/Job/DisplayReference': ref, '/Job/Position': title,
            '/Job/ApplicationURL': 'https://example.org/apply', '/Job/Description': 'Office work'}


class ShadowPlanTests(unittest.TestCase):
    def test_identity_and_hash_survive_days_and_return_after_gap(self):
        monday = module.build_plan([job()], '2026-11-02')['adverts'][0]
        friday = module.build_plan([job()], '2026-11-06')['adverts'][0]
        for field in ('advert_id', 'initial_job_id', 'initial_public_id', 'content_hash'):
            self.assertEqual(monday[field], friday[field])
        self.assertNotEqual(monday['seen_on'], friday['seen_on'])

    def test_update_changes_content_not_identity_or_public_url(self):
        old = module.build_plan([job()], '2026-11-02')['adverts'][0]
        new = module.build_plan([job(title='Office Assistant')], '2026-11-03')['adverts'][0]
        self.assertEqual(old['initial_public_id'], new['initial_public_id'])
        self.assertEqual(old['initial_job_id'], new['initial_job_id'])
        self.assertNotEqual(old['content_hash'], new['content_hash'])

    def test_rejected_jobs_are_retained_without_inventing_selector_reasons(self):
        plan = module.build_plan([job('123'), job('456')], '2026-11-02', [
            {'source': 'JobG8', 'job_id': '123'}, {'source': 'JobG8', 'job_id': '123'},
            {'source': 'JobG8', 'job_id': '999'}, {'source': 'nhs', 'job_id': 'nhs-1'}])
        self.assertEqual(plan['supplied'], 2)
        self.assertEqual(plan['published_in_feed'], 1)
        self.assertEqual(plan['unpublished_in_feed'], 1)
        self.assertEqual(plan['published_absent_from_feed'], ['999'])
        self.assertIn('unknown', plan['selection_note'])

    def test_no_snapshot_does_not_mean_nothing_published(self):
        self.assertIsNone(module.build_plan([job()], '2026-11-02')['unpublished_in_feed'])

    def test_duplicate_or_incomplete_identifiers_fail_before_any_import(self):
        for rows in ([job(), job()], [job(ref='')], [job(title='')]):
            with self.assertRaises(ValueError):
                module.build_plan(rows, '2026-11-02')

    def test_invalid_feed_date_rejected(self):
        with self.assertRaises(ValueError):
            module.build_plan([job()], 'tomorrow')


if __name__ == '__main__':
    unittest.main()
