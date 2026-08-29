from __future__ import annotations

import unittest

from pipeline.scripts import customer_sales_pipeline
from pipeline.scripts import finance_accounts_pipeline
from pipeline.scripts import hr_recruitment_pipeline
from pipeline.scripts import registered_category_pipeline
from pipeline.scripts import support_worker_pipeline


class OwnerReviewedMissedTitleTests(unittest.TestCase):
    def test_finance_exact_exceptions_are_in(self) -> None:
        for title in (
            "Accounts Payable Analyst",
            "Accounts Payable Analyst Hybrid",
            "Assistant Accountant (Hybrid)",
            "Finance Administration Officer",
        ):
            with self.subTest(title=title):
                keep, _reason = finance_accounts_pipeline.classify(
                    title, "Practical finance operations", "Annual", 26000, 33000
                )
                self.assertTrue(keep)

    def test_hr_payroll_administrator_is_in(self) -> None:
        keep, _reason = hr_recruitment_pipeline.classify(
            "HR and Payroll Administrator",
            "Employee records, HR administration and payroll support",
            "Annual",
            28000,
            28000,
        )
        self.assertTrue(keep)

    def test_customer_engagement_executive_is_sales_eligible(self) -> None:
        decision = customer_sales_pipeline.classify(
            "Customer Engagement Executive",
            "Customer service and office-based sales activity",
            "Example employer",
        )
        self.assertIsNotNone(decision)

    def test_customer_service_refinements_feed_production_loader(self) -> None:
        titles = registered_category_pipeline.load_titles("customer_service_contact_centre")
        for title in (
            "Customer Success and Training Executive",
            "Customer Support Specialist Long Term Temp",
            "Customer Care Coordinator",
            "Customer Account Manager",
            "Customer Engagement Officer",
            "Customer Service Advisor (4 on/ 4 off days)",
            "Customer Service Consultant",
            "Customer Engagement Executive",
            "Digital Customer Success Executive",
        ):
            with self.subTest(title=title):
                self.assertIn(registered_category_pipeline.key(title), titles)

    def test_owner_reviewed_support_titles_override_generic_exclusions(self) -> None:
        register = support_worker_pipeline.load_title_register()
        for title in (
            "Female Support Worker (Driver)",
            "Female Support Practitioner (UK Driving Licence)",
            "Female Only Bank Support Practitioner",
            "FEMALE Support Workers(DRIVERS only)",
            "Flexible Bank Support Coordinator",
            "Housing Support Worker",
            "Housing Management Worker",
            "Housing and Support Officer",
            "Housing Support Officer",
        ):
            with self.subTest(title=title):
                classification, _reason, _priority, _review = support_worker_pipeline.classify_title(
                    title, register
                )
                self.assertEqual("HIGH_CONFIDENCE", classification)


if __name__ == "__main__":
    unittest.main(verbosity=2)
