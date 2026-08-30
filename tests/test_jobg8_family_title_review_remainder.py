from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "pipeline" / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from pipeline.scripts import customer_sales_pipeline as sales
from pipeline.scripts import finance_accounts_pipeline as finance
from pipeline.scripts import hr_recruitment_pipeline as hr
from pipeline.scripts import legal_assistant_pipeline as legal
from pipeline.scripts import registered_category_pipeline as customer_service
from pipeline.scripts import service_admin_pipeline as admin


class OwnerApprovedRemainderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.admin_register = admin.load_title_register()

    def test_service_admin_exact_titles_override_only_their_old_broad_exclusions(self) -> None:
        approved = (
            "Operations Administration Support",
            "Operations Officer - £27k-£30k - REMOTE",
            "Production Administrator",
            "Production Office Coordinator",
            "Temporary Order Processor",
            "Sales Order Processor (Hybrid)",
            "Scanning & Processing Assistant",
            "Reception - Canon Birmingham",
            "Reception - Maternity Cover",
            "Reception Admin £28k! Full time & Part time available",
            "Reception",
            "Reception - Chester",
            "Service Admin (Office Based)",
            "Sales Admin - Global Company! £27k-£30k",
            "Warehouse Admin",
            "Transport Administration Assistant",
            "Transport Admin (Days)",
            "Operations Assistant - Supply Chain & Procurement",
            "Operations Assistant - Stock, Purchasing & Logistics",
            "Operations Assistant (Eve)",
            "Operational Support Officer AO",
            "Production Planner / Customer Service Coordinator",
        )
        for title in approved:
            with self.subTest(title=title):
                self.assertEqual("HIGH_CONFIDENCE", admin.classify_title(title, self.admin_register)[0])

        # Exact refinements must not weaken the surrounding generic exclusions.
        self.assertEqual("HARD_PASS", admin.classify_title("Warehouse Operative", self.admin_register)[0])
        self.assertEqual("HARD_PASS", admin.classify_title("Transport Manager", self.admin_register)[0])
        self.assertEqual("HARD_PASS", admin.classify_title("Production Manager", self.admin_register)[0])

    def test_explicit_mixed_payroll_pensions_hr_title_remains_held(self) -> None:
        title = "Payroll , Pensions and HR Administrator (Hybrid)"
        self.assertEqual("HARD_PASS", admin.classify_title(title, self.admin_register)[0])

    def test_finance_and_customer_service_exact_additions(self) -> None:
        self.assertTrue(finance.classify("Payroll And Workforce Admin", "Payroll support", "Annual", 28000, 30000)[0])
        customer_titles = customer_service.load_titles("customer_service_contact_centre")
        for title in (
            "Temporary Order Processor",
            "Order Management Administrator",
            "Production Planner / Customer Service Coordinator",
        ):
            with self.subTest(title=title):
                self.assertIn(customer_service.key(title), customer_titles)

    def test_customer_sales_exact_additions_do_not_widen_nearby_admin(self) -> None:
        approved = (
            "Inside Sale Advisor",
            "Sales Development Executive",
            "Sales Development Representative",
            "Sales Co Ordinator",
            "Sales Coordinator",
            "Junior Sales Admin (Full Training and Career Progression)",
            "Junior Sales Person (MSP / Cyber Security)",
        )
        for title in approved:
            with self.subTest(title=title):
                self.assertIsNotNone(sales.classify(title, "Office role", "Example Ltd"))
        self.assertIsNone(sales.classify("Sales Administrator", "Office administration only", "Example Ltd"))

    def test_legal_and_hr_exact_additions(self) -> None:
        cfg = json.loads((ROOT / "pipeline/config/family_discovery/legal_assistant_paralegal.json").read_text())
        for title in ("Legal Operations Administrator (7 months FTC)", "Legal Enquiry Advisor"):
            with self.subTest(title=title):
                self.assertTrue(legal._include(title, "Legal support", "Annual", 25000, 30000, cfg)[0])

        for title in (
            "Recruitment and Compliance Administrator",
            "Learning And Development Advisor",
            "Learning & Development Advisor",
            "Learning and Development Advisor",
            "Learning and Development Trainer",
        ):
            with self.subTest(title=title):
                self.assertTrue(hr.classify(title, "Employee learning support", "Annual", 28000, 32000)[0])


if __name__ == "__main__":
    unittest.main()
