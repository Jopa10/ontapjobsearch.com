import sys
import unittest
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1] / "pipeline"
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from scripts.hr_recruitment_pipeline import (
    _approved_proof_market_exception,
    classify,
    is_near_duplicate,
)


class HrRecruitmentPipelineTests(unittest.TestCase):
    def test_hr_administrator_is_in(self):
        keep, reason = classify(
            "HR Administrator",
            "Support HR administration, employee records, contracts and new starters.",
            "annum",
            "28000",
            "32000",
        )
        self.assertTrue(keep, reason)

    def test_hr_advisor_is_out(self):
        keep, reason = classify(
            "HR Advisor",
            "Advise managers on employee relations, disciplinary and grievance cases.",
            "annum",
            "35000",
            "42000",
        )
        self.assertFalse(keep)
        self.assertIn("specialist", reason)

    def test_operational_hr_officer_is_in_but_advisory_officer_is_out(self):
        keep, reason = classify(
            "HR Officer",
            "Maintain employee records, issue contracts of employment and complete new starter checks.",
            "annum",
            "30000",
            "35000",
        )
        self.assertTrue(keep, reason)
        keep, reason = classify(
            "HR Officer",
            "Advise line managers on complex employee relations casework, disciplinaries and grievances.",
            "annum",
            "30000",
            "35000",
        )
        self.assertFalse(keep)

    def test_recruitment_delivery_is_in_but_agency_sales_is_out(self):
        keep, reason = classify(
            "Recruitment Resourcer",
            "Source candidates using job boards, screen applications and arrange interviews.",
            "annum",
            "26000",
            "30000",
        )
        self.assertTrue(keep, reason)
        keep, reason = classify(
            "Recruitment Resourcer",
            "Build your own desk through cold calling and new business with uncapped commission.",
            "annum",
            "26000",
            "30000",
        )
        self.assertFalse(keep)
        self.assertIn("sales", reason)

    def test_office_manager_hr_administrator_is_out(self):
        keep, reason = classify(
            "Office Manager/HR Administrator",
            "Manage the office, facilities and suppliers with occasional HR administration.",
            "annum",
            "32000",
            "38000",
        )
        self.assertFalse(keep)
        self.assertIn("management", reason)

    def test_recruitment_reporting_and_student_recruitment_are_out(self):
        keep, reason = classify(
            "Recruitment Performance, Reporting and Planning Officer",
            "Own recruitment reporting and planning for the talent acquisition function.",
            "annum",
            "32000",
            "39000",
        )
        self.assertFalse(keep)
        self.assertIn("specialist", reason)
        keep, reason = classify(
            "Recruitment and Outreach Officer",
            "Recruit students to university courses and run applicant outreach events.",
            "annum",
            "28000",
            "33000",
        )
        self.assertFalse(keep)

    def test_description_day_rate_over_ceiling_is_out(self):
        keep, reason = classify(
            "HR Administrator",
            "Six-month HR administration contract paying £275 per day.",
            "",
            "",
            "",
        )
        self.assertFalse(keep)
        self.assertIn("salary", reason)

    def test_same_place_short_form_syndication_is_deduped(self):
        seen = []
        opening = "Join the people team to maintain employee records and coordinate new starters. " * 8
        self.assertFalse(
            is_near_duplicate("People Systems Administrator", "Yorkshire - North", "York", opening + "Full copy", seen)
        )
        self.assertTrue(
            is_near_duplicate("People Systems Administrator", "Yorkshire - North", "York", opening + "Short copy", seen)
        )
        self.assertFalse(
            is_near_duplicate("People Systems Administrator", "Nottinghamshire", "Nottingham", opening + "Short copy", seen)
        )

    def test_owner_approved_ashton_tameside_proof_exception_is_narrow(self):
        conflict = (
            "advert opening location 'tameside' maps to Greater Manchester - South, "
            "not Greater Manchester - Manchester & Salford"
        )
        description = "Administrator (HR & Compliance) - Ashton Under Lyne (Tameside)."
        self.assertTrue(
            _approved_proof_market_exception(
                "Greater Manchester - Manchester & Salford", description, conflict
            )
        )
        self.assertFalse(
            _approved_proof_market_exception("London", description, conflict)
        )
        self.assertFalse(
            _approved_proof_market_exception(
                "Greater Manchester - Manchester & Salford",
                "HR Administrator based in Stockport.",
                conflict,
            )
        )


if __name__ == "__main__":
    unittest.main()
