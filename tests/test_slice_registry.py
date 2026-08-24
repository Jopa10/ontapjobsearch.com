import sys
import tempfile
import unittest
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1] / "pipeline"
SCRIPTS_DIR = PIPELINE_DIR / "scripts"
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from slice_catalog import dynamic_data_path, dynamic_route, output_filename
from slice_registry import candidate_slices, load_slice_register, live_slices


class SliceRegistryTests(unittest.TestCase):
    def test_register_has_unique_valid_region_category_rows(self):
        records = load_slice_register()
        pairs = {(row.region, row.category) for row in records}
        self.assertEqual(len(pairs), len(records))
        self.assertGreater(len(records), 60)
        self.assertEqual(
            sum(row.status in {"LIVE", "CANDIDATE", "RETIRED"} for row in records),
            len(records),
        )

    def test_live_rows_include_new_white_collar_admin_support_and_sales_slices(self):
        live = live_slices()
        expected = {
            ("London", "finance_accounts"),
            ("London", "customer_service_contact_centre"),
            ("London", "hr_recruitment"),
            ("London", "support_worker"),
            ("Hampshire", "customer_service_contact_centre"),
            ("Greater Manchester - Manchester & Salford", "admin_service"),
            ("Bristol & Bath", "admin_service"),
            ("Devon", "finance_accounts"),
            ("Surrey", "support_worker"),
            ("London", "customer_sales"),
            ("Yorkshire - West", "customer_sales"),
            ("Greater Manchester - Manchester & Salford", "customer_sales"),
        }
        self.assertTrue(expected.issubset(live))
        self.assertIn(("Yorkshire - North", "admin_service"), live)

    def test_immediate_live_service_admin_set_from_22_august_owner_rule(self):
        live = live_slices()
        approved = {
            "Leicestershire",
            "Cheshire - Warrington & Halton",
            "Cornwall",
            "Suffolk",
            "Derbyshire",
            "Cheshire - East",
            "Lincolnshire",
            "Merseyside - Liverpool",
            "Shropshire",
            "Greater Manchester - Wigan & Bolton",
            "West Midlands - Black Country",
        }
        self.assertTrue({(region, "admin_service") for region in approved}.issubset(live))
        for region in approved:
            self.assertTrue(output_filename(region, "admin_service").endswith("-admin-service.json"))
            self.assertTrue(dynamic_route(region, "admin_service").endswith("/service-administrator-jobs"))

    def test_customer_sales_live_set_is_exactly_the_three_approved_regions(self):
        sales_regions = {
            region for region, category in live_slices() if category == "customer_sales"
        }
        self.assertEqual(
            sales_regions,
            {
                "London",
                "Yorkshire - West",
                "Greater Manchester - Manchester & Salford",
            },
        )
        self.assertNotIn(("North East", "customer_sales"), live_slices())

    def test_marketing_live_set_is_exactly_the_four_owner_approved_regions(self):
        marketing_regions = {
            region for region, category in live_slices() if category == "marketing"
        }
        self.assertEqual(
            marketing_regions,
            {
                "London",
                "Surrey",
                "Greater Manchester - Manchester & Salford",
                "West Midlands - Birmingham & Solihull",
            },
        )
        self.assertNotIn(("Kent", "marketing"), live_slices())

    def test_hr_recruitment_live_set_is_exactly_the_six_owner_approved_regions(self):
        hr_regions = {
            region for region, category in live_slices() if category == "hr_recruitment"
        }
        self.assertEqual(
            hr_regions,
            {
                "London",
                "Yorkshire - West",
                "Berkshire",
                "Greater Manchester - Manchester & Salford",
                "Nottinghamshire",
                "West Midlands - Birmingham & Solihull",
            },
        )
        reserves = {"Sussex", "Bristol & Bath", "Essex"}
        self.assertTrue(
            {(region, "hr_recruitment") for region in reserves}.issubset(candidate_slices())
        )
        self.assertTrue(
            {(region, "hr_recruitment") for region in reserves}.isdisjoint(live_slices())
        )

    def test_close_and_deferred_slices_are_candidates_not_live(self):
        candidates = candidate_slices()
        expected = {
            ("Greater Manchester - Manchester & Salford", "customer_service_contact_centre"),
            ("Hampshire", "hr_recruitment"),
            ("Yorkshire - West", "finance_accounts"),
            ("North East", "finance_accounts"),
            ("Somerset", "support_worker"),
        }
        self.assertTrue(expected.issubset(candidates))
        self.assertTrue(expected.isdisjoint(live_slices()))
        self.assertNotIn(("London", "support_worker"), candidates)
        self.assertNotIn(("Surrey", "support_worker"), candidates)
        self.assertIn(("Buckinghamshire", "admin_service"), live_slices())

    def test_london_support_worker_live_config(self):
        from scripts import support_worker_pipeline_live_config as support_config

        self.assertIn("London", support_config.core.OUTPUT_FILES)
        self.assertEqual(
            support_config.core.OUTPUT_FILES["London"],
            "london-support-worker.json",
        )
        self.assertEqual(
            support_config.core.PUBLISH_THRESHOLDS["London"], 6
        )
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
        self.assertEqual(
            output_filename("Yorkshire - West", "customer_sales"),
            "west-yorkshire-customer-sales.json",
        )
        self.assertEqual(
            dynamic_route("Greater Manchester - Manchester & Salford", "customer_sales"),
            "/job-search/manchester-salford/customer-sales-jobs",
        )
        self.assertEqual(
            dynamic_data_path("London", "customer_sales"),
            Path("app/_city-pages/configured-slices/london/customer-sales-jobs.json"),
        )
        self.assertEqual(
            output_filename("London", "marketing"),
            "london-marketing.json",
        )
        self.assertEqual(
            dynamic_route("West Midlands - Birmingham & Solihull", "marketing"),
            "/job-search/birmingham-solihull/marketing-jobs",
        )
        self.assertEqual(
            dynamic_data_path("Surrey", "marketing"),
            Path("app/_city-pages/configured-slices/surrey/marketing-jobs.json"),
        )
        self.assertEqual(
            dynamic_route("Merseyside - Liverpool", "admin_service"),
            "/job-search/merseyside-liverpool/service-administrator-jobs",
        )
        self.assertEqual(
            dynamic_route("West Midlands - Black Country", "admin_service"),
            "/job-search/black-country/service-administrator-jobs",
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
