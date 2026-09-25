import unittest

from scripts.pipeline_refinement import assess_salary, load_salary_thresholds, salary_threshold_for_region


class SalaryPolicyFamilyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.thresholds = load_salary_thresholds()

    def test_admin_service_has_new_non_london_and_london_points(self):
        self.assertEqual(37_000, salary_threshold_for_region("Berkshire", self.thresholds, "admin_service"))
        self.assertEqual(42_000, salary_threshold_for_region("London", self.thresholds, "admin_service"))

    def test_admin_service_jobs_through_new_points_pass_salary_review(self):
        outside_london = assess_salary(
            salary_min="32000", salary_max="36000", salary_period="Annual", salary_text="",
            region="Berkshire", thresholds=self.thresholds, family="admin_service",
        )
        london = assess_salary(
            salary_min="40000", salary_max="42000", salary_period="Annual", salary_text="",
            region="London", thresholds=self.thresholds, family="admin_service",
        )
        self.assertEqual("ok", outside_london.status)
        self.assertEqual("ok", london.status)

    def test_hourly_salary_is_annualised_against_new_admin_service_point(self):
        assessment = assess_salary(
            salary_min="17", salary_max="20", salary_period="Hourly", salary_text="",
            region="Berkshire", thresholds=self.thresholds, family="admin_service",
        )
        self.assertEqual(39_000, assessment.annual_upper_gbp)
        self.assertEqual("review", assessment.status)

    def test_other_families_keep_their_existing_shared_thresholds(self):
        self.assertEqual(30_000, salary_threshold_for_region("Berkshire", self.thresholds, "support_worker"))
        self.assertEqual(35_000, salary_threshold_for_region("London", self.thresholds, "customer_service_contact_centre"))
        support_worker = assess_salary(
            salary_min="32000", salary_max="36000", salary_period="Annual", salary_text="",
            region="Berkshire", thresholds=self.thresholds, family="support_worker",
        )
        self.assertEqual("review", support_worker.status)


if __name__ == "__main__":
    unittest.main()
