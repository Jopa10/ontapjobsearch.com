from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import math

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "pipeline" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import pipeline_refinement as policy  # noqa: E402
import service_admin_pipeline as admin  # noqa: E402
import support_worker_pipeline as support  # noqa: E402


class SalaryPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.thresholds = policy.load_salary_thresholds()

    def assess(self, *, salary_min="", salary_max="", period="Year", region="Yorkshire - West", ceiling=""):
        return policy.assess_salary(
            salary_min=salary_min,
            salary_max=salary_max,
            salary_period=period,
            salary_text="",
            region=region,
            thresholds=self.thresholds,
            reviewed_ceiling_gbp=ceiling,
        )

    def test_london_sussex_and_hampshire_use_higher_boundary(self) -> None:
        for region in ("London", "Sussex", "Hampshire"):
            with self.subTest(region=region):
                self.assertEqual(35000, policy.salary_threshold_for_region(region, self.thresholds))
        self.assertEqual(30000, policy.salary_threshold_for_region("North East", self.thresholds))

    def test_upper_range_figure_drives_review(self) -> None:
        assessment = self.assess(salary_min="28000", salary_max="31000")
        self.assertEqual("review", assessment.status)
        self.assertEqual(31000, assessment.annual_upper_gbp)

    def test_boundary_itself_is_not_review(self) -> None:
        assessment = self.assess(salary_max="35000", region="London")
        self.assertEqual("ok", assessment.status)

    def test_reviewed_title_ceiling_prevents_repeat_until_salary_rises(self) -> None:
        self.assertEqual(
            "ok",
            self.assess(salary_max="32000", ceiling="32000").status,
        )
        self.assertEqual(
            "review",
            self.assess(salary_max="32001", ceiling="32000").status,
        )

    def test_obviously_corrupt_monthly_salary_is_excluded(self) -> None:
        assessment = self.assess(salary_max="4", period="Month")
        self.assertEqual("corrupt", assessment.status)

    def test_blank_structured_values_fall_back_to_description_salary(self) -> None:
        assessment = policy.assess_salary(
            salary_min=math.nan,
            salary_max=math.nan,
            salary_period="Annual",
            salary_text="£4 per month",
            region="North East",
            thresholds=self.thresholds,
        )
        self.assertEqual("corrupt", assessment.status)
        self.assertEqual(48, assessment.annual_upper_gbp)

    def test_missing_salary_is_distinct_from_corrupt_salary(self) -> None:
        assessment = self.assess(salary_min="", salary_max="", period="")
        self.assertEqual("missing", assessment.status)


class ContextPolicyTests(unittest.TestCase):
    def test_personal_assistant_requires_direct_care_context(self) -> None:
        missing = policy.assess_context_policy(
            "support_personal_assistant",
            "Diary management and board meeting support for the CEO.",
        )
        direct = policy.assess_context_policy(
            "support_personal_assistant",
            "Provide personal care, medication support and help with daily living.",
        )
        self.assertTrue(missing.excluded)
        self.assertEqual("ok", direct.status)

    def test_family_support_excludes_explicit_statutory_casework_barrier(self) -> None:
        assessment = policy.assess_context_policy(
            "family_direct_support",
            "A social work qualification is essential for statutory case management.",
        )
        self.assertTrue(assessment.excluded)


class ManualReviewFeedDateTests(unittest.TestCase):
    def assert_date_scoped_actions(self, module) -> None:
        original_path = module.MANUAL_REVIEW_MD_PATH
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                path = Path(temp_dir) / "review.md"
                module.MANUAL_REVIEW_MD_PATH = path
                path.write_text(
                    "\n".join(
                        [
                            "# Review",
                            "",
                            "feed_date: 2026-07-24",
                            "",
                            "---",
                            "action: select",
                            "POSS | Region | Town | £30,000 | Administrator",
                            "job_id: job-1",
                            "---",
                        ]
                    ),
                    encoding="utf-8",
                )

                same_feed = module.load_manual_decisions_from_markdown("2026-07-24")
                next_feed = module.load_manual_decisions_from_markdown("2026-07-25")
                self.assertTrue(same_feed.rerun_mode)
                self.assertEqual({"job-1"}, same_feed.selections)
                self.assertFalse(next_feed.rerun_mode)
                self.assertEqual(set(), next_feed.selections)
                self.assertIn("old actions ignored", next_feed.load_warning)
        finally:
            module.MANUAL_REVIEW_MD_PATH = original_path

    def test_service_admin_actions_are_feed_scoped(self) -> None:
        self.assert_date_scoped_actions(admin)

    def test_support_worker_actions_are_feed_scoped(self) -> None:
        self.assert_date_scoped_actions(support)

    def test_live_workbook_date_is_stable(self) -> None:
        self.assertEqual(
            "2026-07-24",
            policy.resolve_feed_date(ROOT / "pipeline" / "input" / "jobg8.xlsx"),
        )


class AgreedTitleRuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.admin_register = admin.load_title_register()
        cls.support_register = support.load_title_register()

    def test_admin_specialist_and_general_titles(self) -> None:
        cases = {
            "Internal Sales Administrator": "HIGH_CONFIDENCE",
            "Care Coordinator": "HIGH_CONFIDENCE",
            "Pensions Administrator": "HARD_PASS",
            "Legal Secretary": "HARD_PASS",
            "Property Administrator": "HARD_PASS",
        }
        for title, expected in cases.items():
            with self.subTest(title=title):
                self.assertEqual(expected, admin.classify_title(title, self.admin_register)[0])

    def test_support_personal_assistant_uses_context_rule(self) -> None:
        result = support.classify_title("Personal Assistant", self.support_register)
        self.assertEqual("REVIEW_CONTEXT_DEPENDENT", result[0])
        rule = self.support_register[support.normalise_title_for_register("Personal Assistant")]
        self.assertEqual("support_personal_assistant", rule["context_policy"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
