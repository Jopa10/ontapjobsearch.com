import base64
import csv
import hashlib
import hmac
import json
import tempfile
import unittest
from pathlib import Path

from scripts.send_cpc_job_alerts import (
    _unsubscribe_token,
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

    def test_unsubscribe_token_is_signed_and_contains_only_email_identity(self):
        token = _unsubscribe_token("Person@example.com", "test-secret")
        payload, signature = token.split(".")
        expected = hmac.new(b"test-secret", payload.encode("ascii"), hashlib.sha256).digest()
        actual = base64.urlsafe_b64decode(signature + "=" * (-len(signature) % 4))
        self.assertTrue(hmac.compare_digest(expected, actual))
        decoded = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        self.assertEqual(json.loads(decoded), {"email": "person@example.com", "version": 1})

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


class PrivateDeliveryTests(unittest.TestCase):
    def test_single_recipient_and_preview_links_without_daily_updates(self):
        from unittest.mock import patch
        from scripts.send_cpc_job_alerts import send_private_test
        contact = {"email": "jpbt801@gmail.com", "listIds": [3], "attributes": {
            "ALERT_JOB_ID": "sample", "ALERT_ROLE": "HR Officer", "ALERT_LOCATION": "Warwick",
            "ALERT_CONSENT_AT": "2026-10-22", "ALERT_CONSENT_VERSION": "v1"}}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "jobs.json").write_text(json.dumps([{
                "job_id": "sample", "title": "HR Officer", "location": "Warwick",
                "source": "JobG8", "apply_url": "https://www.jobg8.com/Traffic.aspx?x"}]))
            with patch("scripts.send_cpc_job_alerts._brevo_request", side_effect=[contact, {}]) as request:
                send_private_test("jpbt801@gmail.com", "https://preview.vercel.app", root,
                                  api_key="fake", list_id=3, sender_email="jobs@example.com", secret="fake")
            self.assertEqual(request.call_count, 2)
            self.assertEqual(request.call_args_list[0].args[:2], ("GET", "/contacts/jpbt801%40gmail.com"))
            payload = request.call_args.args[3]
            self.assertEqual(payload["to"], [{"email": "jpbt801@gmail.com"}])
            self.assertIn("[Private test]", payload["subject"])
            self.assertIn("https://preview.vercel.app/job-alerts/unsubscribe?", payload["textContent"])
            self.assertIn("https://preview.vercel.app/jobs/sample", payload["textContent"])

    def test_invalid_origins_and_multiple_recipients_fail_before_api(self):
        from unittest.mock import patch
        from scripts.send_cpc_job_alerts import send_private_test, DeliveryError
        for email, origin in [
            ("a@example.com", "https://www.ontapjobsearch.com"),
            ("a@example.com,b@example.com", "https://preview.vercel.app"),
            ("a@example.com", "https://preview.vercel.app.evil.com"),
        ]:
            with patch("scripts.send_cpc_job_alerts._brevo_request") as request:
                with self.assertRaises(DeliveryError):
                    send_private_test(email, origin, Path("."), api_key="fake", list_id=3,
                                      sender_email="jobs@example.com", secret="fake")
                request.assert_not_called()

    def test_nonmember_is_never_sent_email(self):
        from unittest.mock import patch
        from scripts.send_cpc_job_alerts import send_private_test, DeliveryError
        with patch("scripts.send_cpc_job_alerts._brevo_request", return_value={
            "email": "a@example.com", "listIds": [2]}) as request:
            with self.assertRaises(DeliveryError):
                send_private_test("a@example.com", "https://preview.vercel.app", Path("."),
                                  api_key="fake", list_id=3, sender_email="jobs@example.com", secret="fake")
            self.assertEqual(request.call_count, 1)

if __name__ == "__main__":
    unittest.main()
