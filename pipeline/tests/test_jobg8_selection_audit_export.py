import unittest

from pipeline.scripts.jobg8_selection_audit_export import classify_status, salary_band


class JobG8SelectionAuditExportTest(unittest.TestCase):
    def test_salary_bands_use_annualised_midpoint(self):
        self.assertEqual(salary_band(20_000, 34_000), "£20k–<£35k")
        self.assertEqual(salary_band(35_000, 45_000), "£35k–£45k")
        self.assertEqual(salary_band(50_000, 60_000), "Over £45k")
        self.assertEqual(salary_band(None, None), "Below £20k / unknown")

    def test_status_precedence_and_live_market_evidence(self):
        register = {("Yorkshire - West", "admin_service"): "LIVE"}
        self.assertEqual(classify_status("1", "Yorkshire - West", [], [], {"1"}, register)[0], "Published")
        self.assertEqual(classify_status("2", "Devon", ["admin_service"], [], set(), register)[0], "Selected but market not LIVE")
        self.assertIn("otherwise withheld", classify_status("3", "Yorkshire - West", ["admin_service"], [], set(), register)[0])
        self.assertEqual(classify_status("4", "Yorkshire - West", [], ["admin_service: OUT_OF_SCOPE"], set(), register)[0], "Assessed and rejected")
        self.assertEqual(classify_status("5", "Yorkshire - West", [], [], set(), register)[0], "Not matched to any governed family")


if __name__ == "__main__":
    unittest.main()
