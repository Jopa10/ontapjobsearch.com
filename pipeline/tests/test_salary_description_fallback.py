import unittest

from scripts import service_admin_pipeline_core as core


class SalaryDescriptionFallbackTests(unittest.TestCase):
    def test_standalone_up_to_without_currency_is_annual_salary(self):
        self.assertEqual(
            core.extract_salary_from_description("Permanent role\n\nUp to 28,000\n\nBased in Bristol"),
            "Up to £28,000 per year",
        )

    def test_salary_label_without_currency_is_annual_salary(self):
        self.assertEqual(
            core.extract_salary_from_description("Salary: 32,500"),
            "£32,500 per year",
        )

    def test_non_salary_large_number_is_not_misread(self):
        self.assertEqual(
            core.extract_salary_from_description("We support up to 28,000 customers each year."),
            "",
        )

    def test_small_up_to_number_is_not_misread_as_annual_salary(self):
        self.assertEqual(core.extract_salary_from_description("Up to 500"), "")

    def test_existing_explicit_currency_period_fallback_still_works(self):
        self.assertEqual(
            core.extract_salary_from_description("Pay is £14.50 per hour plus benefits"),
            "£14.50 per hour",
        )

    def test_annual_salary_is_not_misread_as_hourly_rate(self):
        self.assertEqual(
            core.extract_salary_from_description(
                "Salary: £13,928.53 Hourly rate: £13.35 per hour rising to £13.66 per hour"
            ),
            "£13.35 per hour",
        )


if __name__ == "__main__":
    unittest.main()
