import sys
import unittest
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1] / "pipeline"
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from scripts.customer_sales_pipeline import classify


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


if __name__ == "__main__":
    unittest.main()
