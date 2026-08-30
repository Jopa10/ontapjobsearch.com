from __future__ import annotations

import unittest

from pipeline.scripts import customer_sales_pipeline
from pipeline.scripts import finance_accounts_pipeline
from pipeline.scripts import hr_recruitment_pipeline
from pipeline.scripts import registered_category_pipeline
from pipeline.scripts import service_admin_pipeline_core
from pipeline.scripts import support_worker_pipeline


class OwnerReviewedMissedTitleTests(unittest.TestCase):
    def test_finance_exact_exceptions_are_in(self) -> None:
        for title in (
            "Accounts Payable Analyst",
            "Accounts Payable Analyst Hybrid",
            "Assistant Accountant (Hybrid)",
            "Finance Administration Officer",
            "Purchase Ledger Clerk Role",
            "Accounts Payable Clerk",
            "Accounts Receivable Clerk",
            "Accounts Administrator (legal)",
            "HR Operations/ Payroll Coordinator",
            "Payroll & Finance Coordinator",
            "Payroll Systems Assistant",
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
            "Customer Tech Support Advisor",
            "Customer Support Agent",
            "Customer Service Clerk",
            "Customer Care Assistant",
        ):
            with self.subTest(title=title):
                self.assertIn(registered_category_pipeline.key(title), titles)

    def test_owner_reviewed_admin_titles_are_in(self) -> None:
        register = service_admin_pipeline_core.load_title_register()
        for title in (
            "Admin with Excel",
            "Booking Clerk",
            "Office / Events Administrator",
            "Bank Receptionist",
            "Business Support Assistant",
            "Operations Assistant",
            "Executive Assistant",
            "Personal Assistant to the Head of Prep",
            "Service Department Coordinator",
        ):
            with self.subTest(title=title):
                classification, *_ = service_admin_pipeline_core.classify_title(title, register)
                self.assertIn(classification, {"HIGH_CONFIDENCE", "ELASTIC_FIT"})

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
            "Care Assistant- Daleview",
            "Support Worker - O'Hanlon House",
            "Care Assistant - Drivers Only",
            "Floating Support Worker - Young Persons",
            "Support Worker - Supported Housing - Bristol",
            "Live in Care Assistant to Medical Sciences Uni Student",
            "Live-In Personal Assistant for Law Student at University",
            "Live in Care Assistant to 3rd year Biology Uni Student",
            "Live-in Care Assistant for a Graphic Design Student",
        ):
            with self.subTest(title=title):
                classification, _reason, _priority, _review = support_worker_pipeline.classify_title(
                    title, register
                )
                self.assertEqual("HIGH_CONFIDENCE", classification)


    def test_fourth_sweep_registered_titles_are_governed(self) -> None:
        expected = {
            "admin_service": (
                "PA Executive Assistant",
                "Production Planning Administrator",
                "Admin Assistant",
                "Customer Support / Admin Support Roles",
                "Production Administrator",
                "Administration Support",
                "Maintenance Helpdesk Administrator",
                "Administrator / Business Support",
                "Administration Assistant - Part Time",
                "Business Support Coordinator",
            ),
            "finance_accounts": (
                "Payroll Administrator (Part Time)",
                "Payroll & Benefits Administrator",
                "Payroll Support Administrator",
                "Book Keeper - Part Time",
                "Payroll Associate (Part Time/Full Time - Accountancy Practice)",
                "Payroll , Pensions and HR Administrator (Hybrid)",
            ),
            "legal_assistant_paralegal": (
                "Legal Secretary 12 month FTC",
                "Legal Secretary / Legal Administration",
                "Legal Secretary / Legal Assistant",
                "Paralegal",
            ),
            "hr_recruitment": ("People and Operations Assistant",),
            "customer_sales": ("Sales Coordinator", "Sales Coordinator Construction"),
        }
        for family, family_titles in expected.items():
            governed = registered_category_pipeline.load_titles(family)
            for title in family_titles:
                with self.subTest(family=family, title=title):
                    self.assertIn(registered_category_pipeline.key(title), governed)

    def test_fourth_sweep_direct_care_titles_override_generic_exclusions(self) -> None:
        register = support_worker_pipeline.load_title_register()
        for title in (
            "Day Centre Support Worker",
            "Care Assistant Nursing - Dayshift - Ratheane",
            "Mental Health Support Worker - Thatcham, Berkshire",
            "Support Worker (Weekend)",
            "Support Worker Flexible Across Services",
            "Support Worker (part time)",
            "Care Assistant (Care homes)",
            "Care Assistant (Nights)",
            "Housing Support Worker (Casual)",
            "Care Assistant - Female Only - Driver Only",
            "Support Worker Waking Nights",
        ):
            with self.subTest(title=title):
                classification, _reason, _priority, _review = support_worker_pipeline.classify_title(
                    title, register
                )
                self.assertEqual("HIGH_CONFIDENCE", classification)


if __name__ == "__main__":
    unittest.main(verbosity=2)
