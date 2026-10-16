import csv
import tempfile
import unittest
from pathlib import Path

from scripts.send_cpc_job_alerts import (
    is_cpc_job,
    matches_alert,
    new_cpc_jobs,
)


class CpcJobAlertMatchingTests(unittest.TestCase):
    def setUp(self):
        self.job = {
            "job_id": "job-1",
            "source": "JobG8",
            "apply_url": "https://www.jobg8.com/Traffic.aspx?token=abc",
            "title": "Class 2 CPC Driver",
            "category": "Transport",
            "description": "CPC driver role delivering locally.",
            "location": "Bristol",
            "region": "South West",
            "salary_text": "£15 - £17 per hour",
        }

    def test_cpc_requires_jobg8_source_and_traffic_destination(self):
        self.assertTrue(is_cpc_job("JobG8", self.job["apply_url"]))
        self.assertFalse(is_cpc_job("WhatJobs", self.job["apply_url"]))
        self.assertFalse(is_cpc_job("JobG8", "https://example.com/apply"))
        self.assertFalse(is_cpc_job("JobG8", "https://jobg8.com/Traffic.aspx?x"))

    def test_alert_matches_role_location_and_overlapping_salary(self):
        attributes = {
            "ALERT_ROLE": "CPC Driver",
            "ALERT_LOCATION": "Bristol",
            "ALERT_SALARY": "£14 - £16 per hour",
        }
        self.assertTrue(matches_alert(attributes, self.job))

    def test_alert_rejects_different_role_location_or_salary(self):
        self.assertFalse(matches_alert({
            "ALERT_ROLE": "CPC Driver",
            "ALERT_LOCATION": "Leeds",
            "ALERT_SALARY": "",
        }, self.job))
        self.assertFalse(matches_alert({
            "ALERT_ROLE": "Care Assistant",
            "ALERT_LOCATION": "Bristol",
            "ALERT_SALARY": "",
        }, self.job))
        self.assertFalse(matches_alert({
            "ALERT_ROLE": "CPC Driver",
            "ALERT_LOCATION": "Bristol",
            "ALERT_SALARY": "£20 per hour",
        }, self.job))

    def test_unknown_job_salary_does_not_hide_an_otherwise_matching_job(self):
        job = {**self.job, "salary_text": "", "salary_min": "", "salary_max": ""}
        self.assertTrue(matches_alert({
            "ALERT_ROLE": "CPC Driver",
            "ALERT_LOCATION": "Bristol",
            "ALERT_SALARY": "£14 - £16 per hour",
        }, job))

    def test_daily_report_and_published_data_gate_the_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            app = root / "app"
            app.mkdir()
            (app / "jobs.json").write_text(
                '[{"job_id":"job-1","source":"JobG8","apply_url":"https://www.jobg8.com/Traffic.aspx?x","title":"CPC Driver","location":"Bristol"}]',
                encoding="utf-8",
            )
            report = root / "new.csv"
            with report.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=[
                    "first_seen_date", "tracking_kind", "source", "job_id"
                ])
                writer.writeheader()
                writer.writerow({
                    "first_seen_date": "2026-10-16",
                    "tracking_kind": "newly_published",
                    "source": "JobG8",
                    "job_id": "job-1",
                })
                writer.writerow({
                    "first_seen_date": "2026-10-16",
                    "tracking_kind": "baseline_existing",
                    "source": "JobG8",
                    "job_id": "old-job",
                })
            jobs = new_cpc_jobs(report, app, "2026-10-16")
            self.assertEqual([job["job_id"] for job in jobs], ["job-1"])
            self.assertEqual(jobs[0]["ontap_url"], "https://www.ontapjobsearch.com/jobs/job-1")


if __name__ == "__main__":
    unittest.main()
