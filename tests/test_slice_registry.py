import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "pipeline" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from slice_catalog import dynamic_data_path, dynamic_route, output_filename
from slice_registry import candidate_slices, load_slice_register, live_slices


class SliceRegistryTests(unittest.TestCase):
    def test_register_tracks_expanded_feed_launch_and_watch_slices(self):
        records = load_slice_register()
        self.assertEqual(len(records), 63)
        live_count = sum(row.status == "LIVE" for row in records)
        candidate_count = sum(row.status == "CANDIDATE" for row in records)
        retired_count = sum(row.status == "RETIRED" for row in records)
        self.assertEqual(live_count + candidate_count + retired_count, 63)
        self.assertEqual(retired_count, 0)
        self.assertGreaterEqual(live_count, 35)
        self.assertGreaterEqual(candidate_count, 27)

    def test_live_rows_include_new_white_collar_and_admin_slices(self):
        live = live_slices()
        expected = {
            ("London", "finance_accounts"),
            ("London", "customer_service_contact_centre"),
            ("London", "hr_recruitment"),
            ("Hampshire", "customer_service_contact_centre"),
            ("Greater Manchester - Manchester & Salford", "admin_service"),
            ("Bristol & Bath", "admin_service"),
            ("Devon", "finance_accounts"),
        }
        self.assertTrue(expected.issubset(live))
        self.assertIn(("Yorkshire - North", "admin_service"), live)

    def test_close_and_deferred_slices_are_candidates_not_live(self):
        candidates = candidate_slices()
        expected = {
            ("Greater Manchester - Manchester & Salford", "customer_service_contact_centre"),
            ("Hampshire", "hr_recruitment"),
            ("Yorkshire - West", "finance_accounts"),
            ("North East", "finance_accounts"),
            ("Somerset", "support_worker"),
            ("Surrey", "support_worker"),
            ("Buckinghamshire", "admin_service"),
        }
        self.assertTrue(expected.issubset(candidates))
        self.assertTrue(expected.isdisjoint(live_slices()))
        self.assertIn(
            ("London", "support_worker"),
            candidates | live_slices(),
        )

    def test_london_support_worker_live_config_when_promoted(self):
        if ("London", "support_worker") not in live_slices():
            self.skipTest("London support worker is still a candidate")
        import support_worker_pipeline_live_config as support_config

        self.assertIn("London", support_config.core.OUTPUT_FILES)
        self.assertEqual(
            support_config.core.OUTPUT_FILES["London"],
            "london-support-worker.json",
        )
        self.assertEqual(support_config.core.PUBLISH_THRESHOLDS["London"], 6)
        self.assertEqual(support_config.core.REGION_MAP["london"], "London")

    def test_catalog_generates_stable_paths(self):
        self.assertEqual(
            output_filename("Greater Manchester - Manchester & Salford", "admin_service"),
            "manchester-salford-admin-service.json",
        )
        self.assertEqual(
            output_filename("London", "finance_accounts"),
            "london-finance-accounts.json",
        )
        self.assertEqual(
            dynamic_route("London", "finance_accounts"),
            "/job-search/london/finance-accounts-jobs",
        )
        self.assertEqual(
            dynamic_data_path("London", "finance_accounts"),
            Path("app/_city-pages/configured-slices/london/finance-accounts-jobs.json"),
        )
        self.assertEqual(
            output_filename("London", "support_worker"),
            "london-support-worker.json",
        )
        self.assertEqual(
            dynamic_route("London", "support_worker"),
            "/job-search/london/support-worker",
        )
        self.assertEqual(
            dynamic_data_path("London", "support_worker"),
            Path("app/_city-pages/configured-slices/london/support-worker.json"),
        )

    def test_invalid_status_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "register.csv"
            path.write_text(
                "region,category,status\nNorth East,admin_service,MAYBE\n",
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit):
                load_slice_register(path)

    def test_unknown_region_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "register.csv"
            path.write_text(
                "region,category,status\nAtlantis,admin_service,LIVE\n",
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit):
                load_slice_register(path)


if __name__ == "__main__":
    unittest.main()
