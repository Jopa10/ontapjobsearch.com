from __future__ import annotations

import unittest

import pandas as pd

from pipeline.scripts.service_admin_pipeline_core import (
    COL,
    _process_batch,
)


def make_job(job_id: str, title: str, salary: int, description: str, period: str = "Annual"):
    return {
        COL["job_id"]: job_id,
        COL["title"]: title,
        COL["advertiser_name"]: "Example employer",
        COL["advertiser_type"]: "Direct employer",
        COL["employment_type"]: "Permanent",
        COL["area"]: "Leeds",
        COL["location"]: "Leeds",
        COL["apply_url"]: "https://example.com/apply",
        COL["description"]: description,
        COL["salary_min"]: salary,
        COL["salary_max"]: salary,
        COL["salary_period"]: period,
        COL["salary_additional"]: "",
    }


def run_rows(rows):
    outputs, reports = _process_batch(
        pd.DataFrame(rows),
        lookup={"leeds": "Yorkshire - West"},
        location_fallback_lookup={},
        overrides={},
        manual_selects=set(),
        title_register={},
    )
    return {row["job_id"]: row for row in outputs["Yorkshire - West"]}, {
        row["job_id"]: row for row in reports
    }


class ServiceAdminOwnerSelectionRuleTests(unittest.TestCase):
    def test_owner_salary_rules_flow_through_to_include_review_or_drop(self):
        jobs, reports = run_rows(
            [
                make_job("dc40", "Document Controller", 40_000, "Maintain project documents."),
                make_job("dc42", "Document Controller", 42_000, "Maintain project documents."),
                make_job("dc46", "Document Controller", 46_000, "Maintain project documents."),
                make_job("dc-unknown", "Document Controller", "", "Maintain project documents."),
                make_job("rec40", "Receptionist/Concierge", 40_000, "Welcome visitors."),
                make_job("rec41", "Receptionist", 41_000, "Welcome visitors."),
                make_job("asst40", "Assistant Accountant", 40_000, "Prepare reconciliations."),
                make_job("bookkeeper41", "Bookkeeper", 41_000, "Maintain ledgers."),
                make_job("cap51", "Assistant Company Secretary", 51_000, "Provide office support."),
            ]
        )
        self.assertIn("dc40", jobs)
        self.assertEqual("", jobs["dc40"]["_review_required"])
        self.assertIn("dc42", jobs)
        self.assertEqual("", jobs["dc42"]["_review_required"])
        self.assertNotIn("dc46", jobs)
        self.assertIn("over £45k", reports["dc46"]["reason"])
        self.assertNotIn("dc-unknown", jobs)
        self.assertIn("Salary not stated", reports["dc-unknown"]["reason"])
        self.assertEqual("", jobs["rec40"]["_review_required"])
        self.assertEqual("1", jobs["rec41"]["_review_required"])
        self.assertNotIn("asst40", jobs)
        self.assertIn("accountant/accountancy senior role", reports["asst40"]["reason"])
        self.assertEqual("1", jobs["bookkeeper41"]["_review_required"])
        self.assertNotIn("cap51", jobs)


    def test_part_time_finance_overrides_seniority_and_uses_actual_hourly_earnings(self):
        job = make_job(
            "pt-bookkeeper",
            "Senior Bookkeeper (Part Time)",
            20,
            "20 hours per week. £20 per hour. Maintain ledgers and bank reconciliations.",
            period="Hourly",
        )
        job[COL["employment_type"]] = "Part-time"
        jobs, reports = run_rows([job])
        self.assertIn("pt-bookkeeper", jobs)
        self.assertEqual("HIGH_CONFIDENCE", jobs["pt-bookkeeper"]["_title_classification"])
        self.assertEqual("", jobs["pt-bookkeeper"]["_review_required"])
        self.assertEqual(20_800, reports["pt-bookkeeper"]["annual_salary_upper"])

    def test_part_time_finance_team_leader_is_admitted_when_within_actual_pay_band(self):
        job = make_job(
            "pt-team-leader",
            "Finance Team Leader - Part Time",
            35_000,
            "20 hours per week. £35,000 actual annual salary.",
        )
        job[COL["employment_type"]] = "Part-time"
        jobs, _reports = run_rows([job])
        self.assertIn("pt-team-leader", jobs)
        self.assertEqual("HIGH_CONFIDENCE", jobs["pt-team-leader"]["_title_classification"])


    def test_part_time_finance_unknown_hours_does_not_create_a_review(self):
        job = make_job(
            "pt-unknown",
            "Finance Assistant - Part Time",
            30_000,
            "Part-time role. £30,000 per year; hours to be agreed.",
        )
        job[COL["employment_type"]] = "Part-time"
        jobs, reports = run_rows([job])
        self.assertIn("pt-unknown", jobs)
        self.assertEqual("", jobs["pt-unknown"]["_review_required"])
        self.assertNotIn("hours are unclear", reports["pt-unknown"]["reason"])

    def test_part_time_manager_still_goes_to_owner_review_with_unclear_hours(self):
        job = make_job(
            "pt-manager-unknown",
            "Finance Manager - Part Time",
            30_000,
            "Part-time role. £30,000 per year; hours to be agreed.",
        )
        job[COL["employment_type"]] = "Part-time"
        jobs, reports = run_rows([job])
        self.assertIn("pt-manager-unknown", jobs)
        self.assertEqual("1", jobs["pt-manager-unknown"]["_review_required"])
        self.assertIn("part-time manager role requires owner review", reports["pt-manager-unknown"]["reason"])


    def test_explicit_language_and_it_support_fail_but_description_only_import_export_does_not(self):
        jobs, reports = run_rows(
            [
                make_job("german", "German-speaking Coordinator", 30_000, "Coordinate appointments."),
                make_job("it", "IT Support - SAP Systems Coordinator", 30_000, "Support SAP users."),
                make_job("import-desc", "Operations Coordinator", 30_000, "Coordinate import/export paperwork."),
                make_job("sap-finance", "Finance Assistant", 30_000, "Use SAP daily to process invoices."),
                make_job("german-desc", "Operations Coordinator", 30_000, "Fluency in German is essential."),
                make_job("english", "Operations Coordinator", 30_000, "Excellent written English is essential."),
                make_job("sap-support", "SAP Systems Coordinator", 30_000, "Provide technical support for SAP users."),
            ]
        )
        self.assertNotIn("german", jobs)
        self.assertIn("german", reports)
        self.assertNotIn("it", jobs)
        self.assertIn("it", reports)
        self.assertIn("import-desc", jobs)
        self.assertIn("sap-finance", jobs)
        self.assertNotIn("german-desc", jobs)
        self.assertIn("german-desc", reports)
        self.assertIn("english", jobs)
        self.assertNotIn("sap-support", jobs)
        self.assertIn("sap-support", reports)
