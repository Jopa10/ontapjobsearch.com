from __future__ import annotations

import unittest

from pipeline.scripts.generate_at_a_glance_review import RULE_VERSION, review_job


class AtAGlanceReviewV3Tests(unittest.TestCase):
    def test_candidate_correspondence_is_not_treated_as_a_duty(self) -> None:
        job = {
            "job_id": "hr-requirements",
            "title": "HR Administrator",
            "source": "JobG8",
            "category": "Admin/Service – Office Support",
            "description": (
                "About the Role\n"
                "Processing new starters, carrying out pre-employment checks, and "
                "processing leavers.\n"
                "To be successful in this role\n"
                "Experience of producing accurate written correspondence, including "
                "employment contracts and offer letters."
            ),
        }

        row = review_job(job, ["hr.json"])

        self.assertEqual(row["status"], "generated")
        self.assertIn("pre-employment checks", row["proposed_at_a_glance"])
        self.assertIn("starter and leaver processing", row["proposed_at_a_glance"])
        self.assertNotIn("correspondence", row["proposed_at_a_glance"].casefold())
        self.assertNotIn("Correspondence", row["attributes"])

    def test_supported_accommodation_setting_alone_is_not_a_duty(self) -> None:
        job = {
            "job_id": "setting-only",
            "title": "Support Worker",
            "source": "JobG8",
            "category": "Support Worker – Wide",
            "description": (
                "About the Role\n"
                "You will work at a supported accommodation service.\n"
                "Complete support plans and risk and needs assessments.\n"
                "Successful Applicant\n"
                "Previous housing experience is required."
            ),
        }

        row = review_job(job, ["support.json"])

        self.assertEqual(row["status"], "generated")
        self.assertNotIn("accommodation support", row["proposed_at_a_glance"].casefold())
        self.assertNotIn("Accommodation support", row["attributes"])

    def test_explicit_accommodation_duty_is_retained(self) -> None:
        job = {
            "job_id": "explicit-accommodation",
            "title": "Young People Support Worker",
            "source": "JobG8",
            "category": "Support Worker – Wide",
            "description": (
                "In this role\n"
                "Provide safe, supportive accommodation for young people.\n"
                "Create support plans and complete risk and needs assessments.\n"
                "Candidate Requirements\n"
                "Previous experience is desirable."
            ),
        }

        row = review_job(job, ["support.json"])

        self.assertEqual(row["status"], "generated")
        self.assertIn("accommodation support", row["proposed_at_a_glance"].casefold())
        self.assertIn("Accommodation support", row["attributes"])
        self.assertEqual(RULE_VERSION, "3")


if __name__ == "__main__":
    unittest.main()
