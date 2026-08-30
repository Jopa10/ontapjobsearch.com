import unittest

import pandas as pd

from pipeline.scripts.jobg8_selection_audit_export import COL, classify_status, effective_salary, resolve_region, salary_band


class JobG8SelectionAuditExportTest(unittest.TestCase):
    def test_salary_bands_use_annualised_midpoint(self):
        self.assertEqual(salary_band(20_000, 34_000), "£20k–<£35k")
        self.assertEqual(salary_band(35_000, 45_000), "£35k–£45k")
        self.assertEqual(salary_band(50_000, 60_000), "Over £45k")
        self.assertEqual(salary_band(None, None), "Below £20k / unknown")

    def test_status_precedence_and_live_market_evidence(self):
        register = {("Yorkshire - West", "admin_service"): "LIVE"}
        self.assertEqual(classify_status("1", "Yorkshire - West", [], [], {"1"}, register)[0], "Published")
        self.assertEqual(classify_status("2", "Devon", ["admin_service"], [], set(), register)[0], "Governed match; market not LIVE")
        live_unpublished = classify_status("3", "Yorkshire - West", ["admin_service"], [], set(), register)
        self.assertEqual(live_unpublished[0], "Governed match in LIVE market; not published")
        self.assertIn("reason is not established", live_unpublished[1])
        self.assertEqual(classify_status("4", "Yorkshire - West", [], ["admin_service: OUT_OF_SCOPE"], set(), register)[0], "Governed register rejection")
        self.assertEqual(classify_status("5", "Yorkshire - West", [], [], set(), register)[0], "No governed register match")

    def test_effective_salary_uses_selector_description_fallback(self):
        row = pd.Series({
            COL["salary_min"]: "",
            COL["salary_max"]: "",
            COL["salary_period"]: "",
            COL["description"]: "Customer support role. Pay is £13.50 per hour plus benefits.",
        })
        source, salary_text, annual_min, annual_max = effective_salary(row)
        self.assertEqual(source, "description_fallback")
        self.assertEqual(salary_text, "£13.50 per hour")
        self.assertEqual(annual_min, 26_325)
        self.assertEqual(annual_max, 26_325)

    def test_effective_salary_keeps_missing_salary_as_missing(self):
        row = pd.Series({
            COL["salary_min"]: "",
            COL["salary_max"]: "",
            COL["salary_period"]: "",
            COL["description"]: "Customer support role with competitive benefits.",
        })
        self.assertEqual(effective_salary(row), ("missing", "", None, None))

    def test_salary_additional_only_is_annualised(self):
        row = pd.Series({
            COL["salary_min"]: "",
            COL["salary_max"]: "",
            COL["salary_period"]: "Annual",
            "/Job/SalaryAdditional": "£14.00 - £14.50/hour",
            COL["description"]: "Routine administration role.",
        })
        source, salary_text, annual_min, annual_max = effective_salary(row)
        self.assertEqual(source, "structured")
        self.assertIn("£14.50", salary_text)
        self.assertEqual(annual_min, 27_300)
        self.assertEqual(annual_max, 28_275)

    def test_generic_city_area_uses_precise_location(self):
        row = pd.Series({COL["area"]: "City", COL["location"]: "Sheffield"})
        self.assertEqual(resolve_region(row, {"city": "London"}, {"sheffield": "Yorkshire - South"}), "Yorkshire - South")


if __name__ == "__main__":
    unittest.main()
