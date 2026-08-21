import sys
import unittest
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1] / "pipeline"
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from scripts.customer_sales_pipeline import classify
from scripts.customer_sales_production_refine import keep_job


class CustomerSalesPipelineTests(unittest.TestCase):
    def test_direct_office_sales_is_in(self):
        result = classify(
            "Business Development Executive",
            "Office based role using CRM, telephone prospecting and new business targets.",
            "Example Recruitment",
        )
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "DIRECT_SALES")

    def test_service_role_needs_real_sales_evidence(self):
        result = classify(
            "Customer Service Representative",
            "Handle enquiries, identify sales opportunities, upsell and convert enquiries to bookings.",
            "Pickfords",
        )
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "CUSTOMER_SALES")
        self.assertIsNone(
            classify(
                "Customer Service Administrator",
                "Answer customer questions and update records with no selling responsibility.",
                "Example Ltd",
            )
        )

    def test_service_admin_overlap_is_not_an_exclusion(self):
        result = classify(
            "Internal Sales Executive",
            "Office role handling customer enquiries, orders, account administration and sales targets.",
            "Trade Supplier",
        )
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "DIRECT_SALES")

    def test_account_roles_are_guarded(self):
        result = classify(
            "Account Manager",
            "Hybrid office role using CRM to grow accounts, cross-sell and deliver revenue growth by phone and email.",
            "Example Ltd",
        )
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "CONDITIONAL_ACCOUNT_SALES")
        self.assertIsNone(
            classify(
                "Account Manager",
                "Wealth management role supporting financial advisers and pension clients from the office.",
                "Example Wealth",
            )
        )

    def test_field_home_campaign_sales_is_out(self):
        self.assertIsNone(
            classify(
                "Sales Executive",
                "Self-employed home improvement campaign with in-home consultation and commission-only earnings.",
                "Citrus Connect",
            )
        )
        self.assertIsNone(
            classify(
                "Sales Executive",
                "Kitchen transformation appointments supplied across your local area.",
                "Citrus Connect",
            )
        )

    def test_automotive_dealership_sales_is_out(self):
        self.assertIsNone(
            classify(
                "Sales Executive",
                "Meet customers, arrange test drives and sell new and used vehicles.",
                "Status Motor Group",
            )
        )

    def test_property_and_retail_sales_is_out(self):
        self.assertIsNone(
            classify(
                "New Homes Sales Advisor",
                "Work on a new homes development for a house builder.",
                "Example Homes",
            )
        )
        self.assertIsNone(
            classify(
                "Luxury Sales Consultant",
                "Luxury retail environment with shop floor selling.",
                "Example Retail",
            )
        )

    def test_specialist_customer_service_is_out(self):
        self.assertIsNone(
            classify(
                "Client Services Manager - Wealth Management",
                "Office based wealth management client service role with new business administration.",
                "Example Wealth",
            )
        )

    def test_final_qa_removes_weak_customer_service(self):
        keep, reason = keep_job(
            {
                "title": "Part-time Customer Service Administrator",
                "description": "Make outbound calls to customers to update records and answer service queries.",
                "advertiser_name": "Example Ltd",
                "region": "Yorkshire - West",
                "customer_sales_classification": "CUSTOMER_SALES",
            },
            [],
        )
        self.assertFalse(keep)
        self.assertIn("no strong sales/conversion evidence", reason)

    def test_final_qa_keeps_real_service_sales_crossover(self):
        keep, reason = keep_job(
            {
                "title": "Customer Service Representative",
                "description": "Handle enquiries, identify sales opportunities, upsell and convert enquiries to bookings.",
                "advertiser_name": "Example Ltd",
                "region": "Greater Manchester - Manchester & Salford",
                "customer_sales_classification": "CUSTOMER_SALES",
            },
            [],
        )
        self.assertTrue(keep, reason)

    def test_final_qa_rejects_title_location_conflict(self):
        keep, reason = keep_job(
            {
                "title": "Bournemouth- Sales Executive",
                "description": "Join our new office and convert warm leads.",
                "advertiser_name": "Example Ltd",
                "region": "Greater Manchester - Manchester & Salford",
                "customer_sales_classification": "DIRECT_SALES",
            },
            [("bournemouth", "Dorset")],
        )
        self.assertFalse(keep)
        self.assertIn("title location", reason)

    def test_final_qa_rejects_opening_location_conflict(self):
        keep, reason = keep_job(
            {
                "title": "Luxury Sales Consultant",
                "description": "Luxury Sales Consultant Belfast. Join a premium retail business selling luxury jewellery and fine timepieces.",
                "advertiser_name": "Example Ltd",
                "region": "London",
                "customer_sales_classification": "DIRECT_SALES",
            },
            [("belfast", "Northern Ireland - East")],
        )
        self.assertFalse(keep)
        self.assertIn("advert opening location", reason)

    def test_final_qa_does_not_treat_plain_renewals_as_sales(self):
        keep, reason = keep_job(
            {
                "title": "Client Service Specialist",
                "description": "Support consultants with administration, client queries and healthcare scheme renewals.",
                "advertiser_name": "Example Benefits",
                "region": "London",
                "customer_sales_classification": "CUSTOMER_SALES",
            },
            [],
        )
        self.assertFalse(keep)
        self.assertIn("no strong sales/conversion evidence", reason)

    def test_final_qa_rejects_face_to_face_event_campaigns_across_customer_sales(self):
        keep, reason = keep_job(
            {
                "title": "Sales & Customer Service Advisor - No Experience Required",
                "description": "Represent client campaigns through face-to-face customer engagement at high-footfall venues, retail spaces and events. Close sales using a tablet.",
                "advertiser_name": "Example Recruitment",
                "region": "London",
                "customer_sales_classification": "CUSTOMER_SALES",
            },
            [],
        )
        self.assertFalse(keep)
        self.assertIn("field/event/self-employed sales signal", reason)

    def test_final_qa_rejects_specialist_investment_account_sales(self):
        keep, reason = keep_job(
            {
                "title": "Account Manager",
                "description": "Advise private clients on rare cask assets and introduce new investment opportunities within a supply-constrained asset class.",
                "advertiser_name": "Example Vintners",
                "region": "London",
                "customer_sales_classification": "CONDITIONAL_ACCOUNT_SALES",
            },
            [],
        )
        self.assertFalse(keep)
        self.assertIn("specialist investment/account-sales signal", reason)


if __name__ == "__main__":
    unittest.main()
