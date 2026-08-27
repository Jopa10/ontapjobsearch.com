import sys
import unittest
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1] / "pipeline"
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from scripts.finance_accounts_pipeline import _based_in_conflict, classify


class FinanceAccountsPipelineTests(unittest.TestCase):
    def test_practical_transactional_titles_are_in(self):
        for title in (
            "Accounts Assistant",
            "Purchase Ledger Clerk",
            "Credit Controller",
            "Bookkeeper",
            "Payroll Coordinator",
        ):
            keep, reason = classify(title, "Day-to-day finance operations.", "Annual", "28000", "35000")
            self.assertTrue(keep, f"{title}: {reason}")

    def test_senior_and_professional_titles_are_out(self):
        for title in (
            "Accounts Senior",
            "Assistant Accountant",
            "Finance Manager",
            "Accounts Payable Specialist",
            "Financial Services Administrator",
        ):
            keep, _reason = classify(title, "Finance work.", "Annual", "30000", "40000")
            self.assertFalse(keep, title)

    def test_salary_above_ceiling_is_out(self):
        keep, reason = classify(
            "Finance Assistant", "Finance support.", "Annual", "42000", "46000"
        )
        self.assertFalse(keep)
        self.assertIn("salary", reason)

    def test_clear_based_in_market_conflict_is_withheld(self):
        reason = _based_in_conflict(
            "Hybrid role based in Derbyshire.",
            "Greater Manchester - Manchester & Salford",
            [("derbyshire", "Derbyshire"), ("manchester", "Greater Manchester - Manchester & Salford")],
        )
        self.assertIsNotNone(reason)
        self.assertIn("Derbyshire", reason)


if __name__ == "__main__":
    unittest.main()
