from __future__ import annotations

import unittest

from pipeline.scripts.service_admin_pipeline_core import (
    assess_part_time_finance,
    classify_title,
    owner_title_salary_rule,
    normalise_title_for_register,
)
from pipeline.scripts.pipeline_refinement import SalaryAssessment


class ServiceAdminOwnerHardFailTests(unittest.TestCase):
    def classification_for(
        self,
        title: str,
        title_register: dict[str, dict[str, str]] | None = None,
    ) -> str:
        classification, _reason, _priority, _review_status = classify_title(
            title,
            title_register,
        )
        return classification

    def test_owner_directed_specialist_roles_are_hard_fail(self) -> None:
        excluded_titles = (
            "Town Planner",
            "Graduate Town Planner",
            "Town Planning Officer",
            "Supply Chain Planner",
            "Supply Planner",
            "Demand Planner",
            "Asset Planner",
            "Asset Planner - Supply Chain",
            "Traffic Planner",
            "System Administrator - Linux & Cloud Infrastructure",
            "Technical Helpdesk Support",
            "IT Helpdesk Advisor - Dutch Speaker",
            "Service Desk Analyst",
            "L1 Service Desk Analyst",
            "Service Desk Analyst - Telephony, Avaya",
            "Product Support Analyst - Helpdesk",
            "Casualty Claims Handler",
            "Liability Claims Handler",
            "Claims Handler",
            "Credit Hire Claims Handler",
            "Subsidence Claims Handler",
            "TPA Liability Claims Handler",
        )
        for title in excluded_titles:
            with self.subTest(title=title):
                self.assertEqual("HARD_PASS", self.classification_for(title))

    def test_new_title_auto_fails_are_narrow(self) -> None:
        excluded_titles = (
            "IT Support Officer",
            "IT Helpdesk Advisor",
            "Service Desk Analyst",
            "Product Support Analyst",
            "Export Administrator",
            "Import/Export Coordinator",
            "German-speaking Coordinator",
            "Bilingual Customer Service Coordinator",
        )
        for title in excluded_titles:
            with self.subTest(title=title):
                self.assertEqual("HARD_PASS", self.classification_for(title))

        for title in (
            "Finance Assistant - Construction",
            "Service Advisor",
            "SAP Finance Assistant",
            "Customer Service Advisor",
        ):
            with self.subTest(title=title):
                self.assertNotEqual("HARD_PASS", self.classification_for(title))

    def test_import_export_in_description_is_not_a_title_auto_fail(self) -> None:
        self.assertNotEqual(
            "HARD_PASS",
            self.classification_for("Operations Coordinator"),
        )

    def test_document_controller_salary_boundaries(self) -> None:
        cases = (
            (40_000, "ok", None),
            (40_001, "ok", None),
            (45_000, "ok", None),
            (45_001, "exclude", "Document Controller salary over £45k"),
        )
        for salary, status, hard_fail in cases:
            with self.subTest(salary=salary):
                actual = owner_title_salary_rule("Document Controller - M&E", salary)
                self.assertEqual(status, actual[0])
                self.assertEqual(hard_fail, actual[2])
        self.assertEqual("review", owner_title_salary_rule("Document Controller", None)[0])

    def test_bookkeeper_and_receptionist_salary_boundary(self) -> None:
        for title in ("Bookkeeper", "Receptionist/Concierge"):
            with self.subTest(title=title):
                self.assertEqual("ok", owner_title_salary_rule(title, 40_000)[0])
                self.assertEqual("review", owner_title_salary_rule(title, 40_001)[0])
                self.assertEqual("review", owner_title_salary_rule(title, None)[0])

    def test_salary_policy_does_not_override_unrelated_titles(self) -> None:
        self.assertEqual("review", owner_title_salary_rule("Service Advisor", 49_000)[0])

    def test_general_salary_cap_is_above_50k(self) -> None:
        status, _reason, hard_fail = owner_title_salary_rule("Assistant Company Secretary", 50_001)
        self.assertEqual(("exclude", "salary over £50k"), (status, hard_fail))

    def test_part_time_finance_hourly_pay_uses_stated_hours(self) -> None:
        assessment = SalaryAssessment("review", 39_000, 37_000, "annualised upper salary")
        active, status, annual, reason = assess_part_time_finance(
            title="Senior Bookkeeper (Part Time)",
            employment_type="Part-time",
            description="20 hours per week. £20 per hour.",
            salary_period="hourly",
            salary_text="£20 per hour",
            salary_assessment=assessment,
        )
        self.assertTrue(active)
        self.assertEqual("ok", status)
        self.assertEqual(20_800, annual)
        self.assertIn("at or below £40k", reason)

    def test_part_time_finance_with_unclear_hours_is_review(self) -> None:
        assessment = SalaryAssessment("ok", 30_000, 37_000, "annual salary")
        active, status, annual, reason = assess_part_time_finance(
            title="Finance Assistant - Part Time",
            employment_type="Part-time",
            description="Competitive salary. Hours to be agreed.",
            salary_period="annual",
            salary_text="£30,000 per year",
            salary_assessment=assessment,
        )
        self.assertTrue(active)
        self.assertEqual("review", status)
        self.assertIsNone(annual)
        self.assertIn("hours are unclear", reason)

    def test_part_time_fte_salary_is_converted_to_actual_earnings(self) -> None:
        assessment = SalaryAssessment("review", 46_000, 37_000, "FTE salary")
        active, status, annual, _reason = assess_part_time_finance(
            title="Finance Manager - Part Time",
            employment_type="Part-time",
            description="20 hours per week. £46,000 full-time equivalent.",
            salary_period="annual",
            salary_text="£46,000 per year",
            salary_assessment=assessment,
        )
        self.assertTrue(active)
        self.assertEqual("ok", status)
        self.assertAlmostEqual(46_000 * 20 / 37.5, annual)

    def test_part_time_salary_bands_and_explicit_exclusions(self) -> None:
        def assess(title: str, annual_salary: float):
            return assess_part_time_finance(
                title=title,
                employment_type="Part-time",
                description="30 hours per week.",
                salary_period="annual",
                salary_text=f"£{annual_salary:,.0f} per year",
                salary_assessment=SalaryAssessment("ok", annual_salary, 37_000, "annual salary"),
            )

        self.assertEqual("review", assess("Bookkeeper Part Time", 45_000)[1])
        self.assertEqual("exclude", assess("Bookkeeper Part Time", 51_000)[1])
        self.assertEqual("exclude", assess("Finance Director Part Time", 30_000)[1])
        self.assertEqual("exclude", assess("Part-time Finance Tax Adviser", 30_000)[1])

    def test_absolute_hard_fails_override_exact_owner_include(self) -> None:
        title = "Town Planner"
        title_register = {
            normalise_title_for_register(title): {
                "classification": "HIGH_CONFIDENCE",
                "review_status": "AGREED_INCLUDE",
                "reason": "test override",
            }
        }
        self.assertEqual(
            "HARD_PASS",
            self.classification_for(title, title_register),
        )

    def test_fnol_roles_are_not_hard_failed(self) -> None:
        kept_titles = (
            "First Notification of Loss Claims Handler",
            "FNOL Motor Claims Handler",
        )
        for title in kept_titles:
            with self.subTest(title=title):
                self.assertNotEqual("HARD_PASS", self.classification_for(title))

    def test_other_agreed_keep_roles_are_not_hard_failed(self) -> None:
        kept_titles = (
            "IT Service Desk Coordinator",
            "Activities Coordinator",
            "Service Advisor",
            "Planning Administrator",
            "Customer Service & Planning Coordinator",
            "Supply Chain Coordinator",
            "Care Coordinator",
            "Family Support Coordinator",
            "Social Media & Marketing Administrator",
            "In-House Recruitment Coordinator",
        )
        for title in kept_titles:
            with self.subTest(title=title):
                self.assertNotEqual("HARD_PASS", self.classification_for(title))


if __name__ == "__main__":
    unittest.main(verbosity=2)
