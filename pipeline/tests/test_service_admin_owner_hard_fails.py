from __future__ import annotations

import unittest

from pipeline.scripts.service_admin_pipeline_core import (
    classify_title,
    normalise_title_for_register,
)


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
