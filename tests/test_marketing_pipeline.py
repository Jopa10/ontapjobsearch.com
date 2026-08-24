import sys
import unittest
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1] / "pipeline"
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from scripts.marketing_pipeline import _based_in_conflict, classify


class MarketingPipelineTests(unittest.TestCase):
    def test_practical_marketing_title_is_in(self):
        keep, reason = classify(
            "Marketing Executive",
            "Plan and deliver digital marketing campaigns, email marketing and website content.",
            "annum",
            "30000",
            "35000",
        )
        self.assertTrue(keep, reason)

    def test_contextual_paid_media_title_needs_delivery_evidence(self):
        keep, reason = classify(
            "Paid Media Specialist",
            "Manage Google Ads, Meta Ads and paid social campaigns for agency clients.",
            "annum",
            "30000",
            "35000",
        )
        self.assertTrue(keep, reason)
        keep, reason = classify(
            "Paid Media Specialist",
            "Provide general commercial support and maintain spreadsheets.",
            "annum",
            "30000",
            "35000",
        )
        self.assertFalse(keep)
        self.assertIn("lacks substantive", reason)

    def test_mixed_title_requires_marketing_delivery(self):
        keep, reason = classify(
            "Sales and Marketing Coordinator",
            "Coordinate marketing campaigns, create social media content and report campaign performance.",
            "annum",
            "28000",
            "32000",
        )
        self.assertTrue(keep, reason)
        keep, reason = classify(
            "Sales and Marketing Coordinator",
            "Support the sales team, manage orders and update the CRM.",
            "annum",
            "28000",
            "32000",
        )
        self.assertFalse(keep)

    def test_description_only_day_rate_over_ceiling_is_out(self):
        keep, reason = classify(
            "Communications Officer",
            "Internal communications contract paying £250 per day.",
            "",
            "",
            "",
        )
        self.assertFalse(keep)
        self.assertIn("salary", reason)

    def test_training_course_advert_is_out(self):
        keep, reason = classify(
            "Social Media Manager Trainee",
            "Start our social media training course; course fees apply before placement.",
            "",
            "",
            "",
        )
        self.assertFalse(keep)
        self.assertIn("training-course", reason)

    def test_clear_based_in_market_conflict_is_withheld(self):
        lookup = [("derbyshire", "Derbyshire"), ("manchester", "Greater Manchester - Manchester & Salford")]
        reason = _based_in_conflict(
            "Manchester hybrid. Join a growing digital agency based in Derbyshire.",
            "Greater Manchester - Manchester & Salford",
            lookup,
        )
        self.assertIsNotNone(reason)
        self.assertIn("Derbyshire", reason)


if __name__ == "__main__":
    unittest.main()
