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
            "title": "Receptionist",
            "category": "Admin/Service – Office Support",
            "description": "Reception duties.",
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
            "ALERT_ROLE": "Receptionist",
            "ALERT_LOCATION": "Bristol",
            "ALERT_SALARY": "£14 - £16 per hour",
        }
        self.assertTrue(matches_alert(attributes, self.job))

    def test_alert_rejects_different_role_location_or_salary(self):
        self.assertFalse(matches_alert({
            "ALERT_ROLE": "Receptionist",
            "ALERT_LOCATION": "Leeds",
            "ALERT_SALARY": "",
        }, self.job))
        self.assertFalse(matches_alert({
            "ALERT_ROLE": "Care Assistant",
            "ALERT_LOCATION": "Bristol",
            "ALERT_SALARY": "",
        }, self.job))
        self.assertFalse(matches_alert({
            "ALERT_ROLE": "Receptionist",
            "ALERT_LOCATION": "Bristol",
            "ALERT_SALARY": "£20 per hour",
        }, self.job))

    def test_unknown_job_salary_does_not_hide_an_otherwise_matching_job(self):
        job = {**self.job, "salary_text": "", "salary_min": "", "salary_max": ""}
        self.assertTrue(matches_alert({
            "ALERT_ROLE": "Receptionist",
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
                '[{"job_id":"job-1","source":"JobG8","apply_url":"https://www.jobg8.com/Traffic.aspx?x","title":"Receptionist","location":"Bristol"}]',
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
            "ALERT_JOB_ID": "sample", "ALERT_ROLE": "HR Assistant", "ALERT_LOCATION": "Warwick",
            "ALERT_CONSENT_AT": "2026-10-22", "ALERT_CONSENT_VERSION": "v1"}}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "jobs.json").write_text(json.dumps([{
                "job_id": "sample", "title": "HR Assistant", "location": "Warwick",
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


class PrivateDailyTests(unittest.TestCase):
    def setUp(self):
        self.contact = {"id": 1, "email": "jpbt801@gmail.com", "listIds": [3], "attributes": {
            "ALERT_ROLE": "Accounts Assistant", "ALERT_LOCATION": "Leeds",
            "ALERT_CONSENT_AT": "2026-10-22", "ALERT_CONSENT_VERSION": "v1"}}
        self.job = {"job_id": "new-job", "title": "Accounts Assistant", "location": "Leeds"}

    def run_private(self, dry_run, contact=None, list_id=3, branch="refs/heads/feat/cpc-job-alerts-brevo", workflow="", verified_sha=None, matched_sample=False, recipient=None):
        import argparse
        from unittest.mock import patch
        from scripts.send_cpc_job_alerts import private_daily_test
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "newly-published-jobs-2026-10-22.csv").write_text("job_id\\n")
            args = argparse.Namespace(date="2026-10-22", reports_dir=root, app_dir=root, dry_run=dry_run, verified_production_sha=verified_sha, private_matching_sample=matched_sample, private_recipient=recipient)
            with patch.dict("os.environ", {"GITHUB_REF": branch, "GITHUB_WORKFLOW": workflow}), \
                 patch("scripts.send_cpc_job_alerts.new_cpc_jobs", return_value=[self.job]), \
                 patch("scripts.send_cpc_job_alerts._brevo_request", side_effect=[contact or self.contact, {}, {}]) as request:
                private_daily_test(args, api_key="fake", list_id=list_id, sender_email="jobs@example.com", secret="fake")
                return request.call_args_list

    def test_dry_run_fetches_only_fixed_contact_without_sending_or_updating(self):
        calls = self.run_private(True)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].args[:2], ("GET", "/contacts/jpbt801%40gmail.com"))

    def test_real_daily_match_sends_only_fixed_recipient_with_preview_links_and_records_date(self):
        calls = self.run_private(False)
        self.assertEqual([call.args[0] for call in calls], ["GET", "POST", "PUT"])
        payload = calls[1].args[3]
        self.assertEqual(payload["to"], [{"email": "jpbt801@gmail.com"}])
        self.assertIn("[Private daily test]", payload["subject"])
        self.assertIn("https://www.ontapjobsearch.com/jobs/new-job", payload["textContent"])
        self.assertIn("https://ontapjobsearchcom-git-feat-cpc-job-alerts-brevo-ontap1.vercel.app/job-alerts/unsubscribe?", payload["textContent"])
        import uuid
        self.assertEqual(str(uuid.UUID(payload["headers"]["idempotencyKey"])), payload["headers"]["idempotencyKey"])
        self.assertEqual(calls[2].args[3], {"attributes": {"ALERT_LAST_SENT_DATE": "2026-10-22"}})

    def test_unsubscribed_or_unconsented_contact_is_rejected(self):
        from scripts.send_cpc_job_alerts import DeliveryError
        for contact in [{**self.contact, "listIds": []},
                        {**self.contact, "listUnsubscribed": [3]},
                        {**self.contact, "email": "anything@gmail.com"},
                        {**self.contact, "attributes": {}},
                        {**self.contact, "emailBlacklisted": True}]:
            with self.assertRaises(DeliveryError):
                self.run_private(False, contact)

    def test_same_date_is_not_sent_again(self):
        contact = {**self.contact, "attributes": {**self.contact["attributes"], "ALERT_LAST_SENT_DATE": "2026-10-22"}}
        self.assertEqual(len(self.run_private(False, contact)), 1)

    def test_no_matching_jobs_means_no_email(self):
        contact = {**self.contact, "attributes": {**self.contact["attributes"], "ALERT_LOCATION": "Bristol"}}
        self.assertEqual(len(self.run_private(False, contact)), 1)

    def test_native_private_workflow_requires_main_exact_name_and_verified_sha(self):
        calls = self.run_private(True, branch="refs/heads/main",
                                 workflow="Send private CPC job alerts after publish", verified_sha="a" * 40)
        self.assertEqual(len(calls), 1)
        from scripts.send_cpc_job_alerts import DeliveryError
        for kwargs in [
            {"workflow": "Other workflow", "verified_sha": "a" * 40},
            {"workflow": "Send private CPC job alerts after publish", "verified_sha": None},
            {"workflow": "Send private CPC job alerts after publish", "verified_sha": "bad"},
        ]:
            with self.assertRaises(DeliveryError):
                self.run_private(True, branch="refs/heads/main", **kwargs)


    def test_matched_sample_sends_fixed_recipient_without_daily_state_update(self):
        from datetime import datetime, timezone
        from unittest.mock import patch
        # The sample has its own date validation; freeze only the UTC clock.
        with patch("datetime.datetime") as clock:
            clock.now.return_value = datetime(2026, 10, 22, tzinfo=timezone.utc)
            contact = {**self.contact, "attributes": {**self.contact["attributes"],
                       "ALERT_LAST_SENT_DATE": "2026-10-22"}}
            calls = self.run_private(False, contact, workflow="Private CPC daily matching test",
                                     matched_sample=True)
        self.assertEqual([call.args[0] for call in calls], ["GET", "POST"])
        payload = calls[1].args[3]
        self.assertEqual(payload["to"], [{"email": "jpbt801@gmail.com"}])
        self.assertIn("[Private matching test]", payload["subject"])
        self.assertIn("https://www.ontapjobsearch.com/jobs/new-job", payload["textContent"])
        self.assertIn("ALERT_LAST_SENT_DATE", str(contact["attributes"]))
        self.assertIn("idempotencyKey", payload["headers"])

    def test_matched_sample_rejects_wrong_workflow_dry_run_or_old_report(self):
        from scripts.send_cpc_job_alerts import DeliveryError
        for kwargs in ({"workflow": "Other workflow"}, {"workflow": "Private CPC daily matching test"}):
            with self.assertRaises(DeliveryError):
                self.run_private(False, matched_sample=True, **kwargs)
        with self.assertRaises(DeliveryError):
            self.run_private(True, workflow="Private CPC daily matching test", matched_sample=True)

    def test_matched_sample_rejects_no_matching_jobs_without_send(self):
        from datetime import datetime, timezone
        from unittest.mock import patch
        from scripts.send_cpc_job_alerts import DeliveryError
        with patch("datetime.datetime") as clock:
            clock.now.return_value = datetime(2026, 10, 22, tzinfo=timezone.utc)
            contact = {**self.contact, "attributes": {**self.contact["attributes"], "ALERT_LOCATION": "Bristol"}}
            with self.assertRaises(DeliveryError):
                self.run_private(False, contact, workflow="Private CPC daily matching test", matched_sample=True)

    def test_wrong_branch_or_list_fails_before_brevo(self):
        from scripts.send_cpc_job_alerts import DeliveryError
        for kwargs in [{"list_id": 2}, {"branch": "refs/heads/main"}]:
            with self.assertRaises(DeliveryError):
                self.run_private(False, **kwargs)




    def test_second_approved_recipient_has_independent_digest_token_and_daily_guard(self):
        email = "jnabon1108@gmail.com"
        contact = {**self.contact, "id": 2, "email": email}
        calls = self.run_private(False, contact, recipient=email)
        self.assertEqual(calls[0].args[:2], ("GET", "/contacts/jnabon1108%40gmail.com"))
        payload = calls[1].args[3]
        self.assertEqual(payload["to"], [{"email": email}])
        first_key = self.run_private(False)[1].args[3]["headers"]["idempotencyKey"]
        self.assertNotEqual(payload["headers"]["idempotencyKey"], first_key)
        self.assertIn("jnabon1108%40gmail.com", calls[2].args[1])
        payload_token = payload["textContent"].split("token=")[1].strip().split(".")[0]
        self.assertEqual(json.loads(base64.urlsafe_b64decode(payload_token + "=" * (-len(payload_token) % 4)))["email"], email)
        already_sent = {**contact, "attributes": {**contact["attributes"], "ALERT_LAST_SENT_DATE": "2026-10-22"}}
        self.assertEqual(len(self.run_private(False, already_sent, recipient=email)), 1)

    def test_second_recipient_cannot_read_first_contact_or_send_without_consent(self):
        from scripts.send_cpc_job_alerts import DeliveryError
        for contact in [self.contact, {**self.contact, "email": "jnabon1108@gmail.com", "listIds": []},
                        {**self.contact, "email": "jnabon1108@gmail.com", "emailBlacklisted": True},
                        {**self.contact, "email": "jnabon1108@gmail.com", "listUnsubscribed": [3]}]:
            with self.assertRaises(DeliveryError):
                self.run_private(False, contact, recipient="jnabon1108@gmail.com")
        with self.assertRaises(DeliveryError):
            self.run_private(False, recipient="other@example.com")



class AgreedMatchingRulesTests(unittest.TestCase):
    def job(self, **changes):
        return {"title": "Accounts Assistant", "location": "Leeds", "region": "Yorkshire - West",
                "salary_text": "£25,000 - £30,000 per year", **changes}

    def attrs(self, **changes):
        return {"ALERT_ROLE": "Finance Assistant", "ALERT_LOCATION": "Leeds",
                "ALERT_SALARY": "£28-32k", **changes}

    def test_every_agreed_group_matches_its_equivalents(self):
        from scripts.send_cpc_job_alerts import ROLE_GROUPS
        for group, titles in ROLE_GROUPS.items():
            for title in titles:
                with self.subTest(group=group, title=title):
                    self.assertTrue(matches_alert(self.attrs(ALERT_ROLE=titles[0]), self.job(title=title)))

    def test_related_but_separate_roles_and_description_mentions_do_not_match(self):
        for role, title in [
            ("Receptionist", "Office Administrator"), ("Bookkeeper", "Accounts Assistant"),
            ("HR Assistant", "Recruitment Assistant"), ("Legal Assistant", "Paralegal"),
            ("Customer Service Advisor", "Service Advisor"), ("Credit Controller", "Sales Ledger Clerk"),
            ("Administrator", "Linux Systems Administrator"), ("Administrator", "Payroll Administrator"),
            ("Support Worker", "Senior Support Worker"), ("Marketing Assistant", "SEO Assistant"),
            ("Project Administrator", "Project Administrator"), ("Front of House", "Front of House"),
        ]:
            with self.subTest(role=role, title=title):
                self.assertFalse(matches_alert(self.attrs(ALERT_ROLE=role),
                    self.job(title=title, description=role, full_description=role)))

    def test_reception_and_work_pattern_variants(self):
        for title in ["Part-time Receptionist", "Receptionist - Dental Practice", "Receptionist (Dental Practice)"]:
            self.assertTrue(matches_alert(self.attrs(ALERT_ROLE="Receptionist"), self.job(title=title)))
        self.assertTrue(matches_alert(self.attrs(ALERT_ROLE="Part-time Accounts Assistant"),
                                      self.job(title="Finance Assistant")))


    def test_contract_duration_preserves_the_agreed_role_group(self):
        # Published Leeds example: job 23643_225740595, £29–31k annually.
        for title in (
            "Finance Assistant - 12 Month Contract",
            "Finance Assistant – 12-month FTC",
            "Finance Assistant (6 months fixed-term contract)",
            "12 Month Contract Finance Assistant",
            "Finance Assistant - FTC",
        ):
            with self.subTest(title=title):
                job = self.job(title=title, salary_text="£29000 - £31000 per year")
                self.assertTrue(matches_alert(self.attrs(), job))
                self.assertTrue(matches_alert(self.attrs(ALERT_ROLE=title),
                                              self.job(title="Finance Assistant")))
                self.assertFalse(matches_alert(self.attrs(ALERT_LOCATION="Bradford"), job))
                self.assertFalse(matches_alert(self.attrs(ALERT_SALARY="£35-40k"), job))

    def test_contract_qualifier_does_not_broaden_roles(self):
        for title in (
            "Senior Finance Assistant - 12 Month Contract",
            "Finance Manager - 12 Month Contract",
            "Finance Assistant / Bookkeeper - 12 Month Contract",
            "Project Administrator - 12 Month Contract",
            "Finance Assistant - 12 Month Contract Manager",
        ):
            with self.subTest(title=title):
                self.assertFalse(matches_alert(self.attrs(), self.job(title=title)))

    def test_ledgers_are_one_group(self):
        self.assertTrue(matches_alert(self.attrs(ALERT_ROLE="Purchase Ledger Clerk"),
                                      self.job(title="Accounts Receivable Assistant")))

    def test_city_does_not_expand_to_region_or_nearby_place(self):
        for location in ["Bradford", "West Yorkshire", "Leeds Road, Bradford"]:
            self.assertFalse(matches_alert(self.attrs(), self.job(location=location)))
        self.assertTrue(matches_alert(self.attrs(), self.job(location="Leeds, West Yorkshire")))
        self.assertFalse(matches_alert(self.attrs(ALERT_LOCATION="York"), self.job(location="Yorkshire")))
        self.assertFalse(matches_alert(self.attrs(ALERT_LOCATION="London"),
                                      self.job(location="Sutton Coldfield", region="West Midlands - Birmingham & Solihull")))

    def test_explicit_region_matches_exact_governed_market(self):
        for region in ["Yorkshire - West", "west-yorkshire"]:
            self.assertTrue(matches_alert(self.attrs(ALERT_LOCATION=region), self.job(location="Bradford")))
        self.assertFalse(matches_alert(self.attrs(ALERT_LOCATION="Yorkshire"), self.job(location="Bradford")))
        self.assertFalse(matches_alert(self.attrs(ALERT_LOCATION="Yorkshire - West"),
                                       self.job(region="Yorkshire - South")))

    def test_overlap_and_separated_ranges(self):
        self.assertTrue(matches_alert(self.attrs(), self.job()))
        self.assertFalse(matches_alert(self.attrs(), self.job(salary_text="£33-35k")))
        self.assertTrue(matches_alert(self.attrs(), self.job(salary_text="£32k")))
        self.assertFalse(matches_alert(self.attrs(), self.job(salary_text="£20,000 - £25,000 annually")))

    def test_missing_and_uncomparable_pay_are_labelled(self):
        from scripts.send_cpc_job_alerts import _salary_decision, _email_html
        for salary in ["", "Competitive", "DOE", "Grade 6 Point 21 - 26"]:
            self.assertEqual(_salary_decision("£28-32k", self.job(salary_text=salary)),
                             (True, "Salary not stated"))
        decision = _salary_decision("£28-32k", self.job(salary_text="£15 per hour"))
        self.assertTrue(decision[0])
        self.assertIn("not comparable", decision[1])
        self.assertIn("Salary not stated", _email_html([self.job(salary_text="Competitive")], "https://example.com")[1])

    def test_hourly_rates_compare_directly_and_convert_only_with_clear_hours(self):
        self.assertTrue(matches_alert(self.attrs(ALERT_SALARY="£14-16 per hour"),
                                      self.job(salary_text="£15 per hour")))
        self.assertFalse(matches_alert(self.attrs(ALERT_SALARY="£20 per hour"),
                                       self.job(salary_text="£15 per hour")))
        # £15 x 20 x 52 = £15,600 actual annual earnings.
        self.assertFalse(matches_alert(self.attrs(), self.job(salary_text="£15 per hour",
                                       description="20 hours per week", employment_type="Part-time")))
        self.assertTrue(matches_alert(self.attrs(ALERT_SALARY="£15-16k"),
                                      self.job(salary_text="£15 per hour", description="20 hours per week")))
        self.assertTrue(matches_alert(self.attrs(), self.job(salary_text="£15 per hour",
                                      description="20-25 hours per week")))

    def test_part_time_actual_earnings_and_unclear_fte(self):
        from scripts.send_cpc_job_alerts import _salary_decision
        self.assertFalse(matches_alert(self.attrs(), self.job(salary_text="£16k per year",
                                       employment_type="Part-time")))
        result = _salary_decision("£28-32k", self.job(salary_text="£40k FTE", employment_type="Part-time"))
        self.assertTrue(result[0])
        self.assertIn("actual part-time pay unclear", result[1])
        self.assertFalse(matches_alert(self.attrs(), self.job(
            salary_text="£40k FTE; actual annual salary: £20k", employment_type="Part-time")))

    def test_fte_is_converted_when_both_sets_of_hours_are_explicit(self):
        from scripts.send_cpc_job_alerts import _salary_decision
        job = self.job(salary_text="£40,000 FTE per year",
                       description="Part-time: 20 hours per week. Full-time: 40 hours.")
        result = _salary_decision("£19-21k", job)
        self.assertTrue(result[0])
        self.assertIn("£20,000", result[1])
        self.assertFalse(_salary_decision("£28-32k", job)[0])

    def test_compact_hourly_rate_and_pay_without_a_period(self):
        from scripts.send_cpc_job_alerts import _salary_range, _salary_decision
        self.assertEqual(_salary_range("£15.50ph"), (15.5, 15.5, "hour"))
        result = _salary_decision("£28-32k", self.job(salary_text="£15"))
        self.assertTrue(result[0])
        self.assertIn("£15", result[1])
        self.assertIn("not comparable", result[1])

    def test_pay_parser_ignores_hours_and_bonus_numbers(self):
        from scripts.send_cpc_job_alerts import _salary_range
        self.assertEqual(_salary_range("£25-30k per year, 20 hours per week"), (25000, 30000, "year"))
        self.assertEqual(_salary_range("£15.50-£17.25 per hour + £500 bonus"), (15.5, 17.25, "hour"))

    def test_configured_family_inventory_is_included_without_city_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            app = root / "app"
            family = app / "_city-pages" / "configured-slices" / "west-yorkshire"
            family.mkdir(parents=True)
            row = {**self.job(), "job_id": "finance-1", "source": "JobG8",
                   "apply_url": "https://www.jobg8.com/Traffic.aspx?x"}
            (family / "finance-accounts-jobs.json").write_text(json.dumps([row]))
            city = app / "_city-pages" / "leeds"
            city.mkdir()
            (city / "jobs.json").write_text(json.dumps([{**row, "job_id": "city-only"}]))
            report = root / "new.csv"
            report.write_text("first_seen_date,tracking_kind,source,job_id\n"
                              "2026-10-24,newly_published,JobG8,finance-1\n"
                              "2026-10-24,newly_published,JobG8,city-only\n")
            self.assertEqual([j["job_id"] for j in new_cpc_jobs(report, app, "2026-10-24")], ["finance-1"])


if __name__ == "__main__":
    unittest.main()

class MultipleAlertTests(unittest.TestCase):
    def test_union_preserves_each_alert_role_location_and_salary_and_deduplicates(self):
        from scripts.send_cpc_job_alerts import matching_jobs
        attrs = {"ALERT_PREFERENCES": json.dumps([
            {"role": "Accounts Assistant", "location": "London", "salary": "£27-30k"},
            {"role": "Receptionist", "location": "Leeds", "salary": "£24-26k"},
            {"role": "Finance Assistant", "location": "London", "salary": "£29-32k"},
        ])}
        jobs = [
            {"job_id": "1", "title": "Accounts Assistant", "location": "London", "region": "London", "salary_text": "£30k"},
            {"job_id": "2", "title": "Receptionist", "location": "Leeds", "salary_text": "£25k"},
            {"job_id": "3", "title": "Accounts Assistant", "location": "Leeds", "salary_text": "£28k"},
            {"job_id": "4", "title": "Receptionist", "location": "Leeds", "salary_text": "£35k"},
        ]
        result = matching_jobs(attrs, jobs + jobs)
        self.assertEqual([j["job_id"] for j in result], ["1", "2"])
        self.assertEqual(len(result), 2)

    def test_malformed_storage_fails_closed_and_legacy_still_matches(self):
        from scripts.send_cpc_job_alerts import matching_jobs, DeliveryError
        job = {"job_id": "1", "title": "Accounts Assistant", "location": "London", "region": "London"}
        for raw in ("broken", "{}", '[{"role":"Accounts Assistant"}]'):
            with self.assertRaises(DeliveryError):
                matching_jobs({"ALERT_PREFERENCES": raw}, [job])
        self.assertEqual(len(matching_jobs({"ALERT_ROLE": "Accounts Assistant",
                         "ALERT_LOCATION": "London"}, [job])), 1)

    def test_multiple_alerts_send_one_digest_and_keep_daily_guard(self):
        from unittest.mock import patch
        from scripts.send_cpc_job_alerts import send_digest, PRIVATE_TEST_EMAIL, PRIVATE_TEST_ORIGIN
        contact = {"id": 123, "email": PRIVATE_TEST_EMAIL, "attributes": {
            "ALERT_PREFERENCES": json.dumps([
                {"role": "Accounts Assistant", "location": "Leeds", "salary": ""},
                {"role": "Finance Assistant", "location": "Leeds", "salary": ""},
                {"role": "Receptionist", "location": "Bristol", "salary": ""},
            ])}}
        jobs = [{"job_id": "1", "title": "Accounts Assistant", "location": "Leeds"},
                {"job_id": "2", "title": "Receptionist", "location": "Bristol"}]
        with patch("scripts.send_cpc_job_alerts._brevo_request", return_value={}) as api:
            sent = send_digest(contact, jobs + jobs, report_date="2026-10-26", api_key="fake",
                               sender_email="jobs@ontapjobsearch.com", unsubscribe_secret="fake",
                               site_url=PRIVATE_TEST_ORIGIN, private_test=True)
            self.assertTrue(sent)
            self.assertEqual([c.args[0] for c in api.call_args_list], ["POST", "PUT"])
            payload = api.call_args_list[0].args[3]
            self.assertIn("2 new CPC jobs", payload["subject"])
            self.assertEqual(payload["to"], [{"email": PRIVATE_TEST_EMAIL}])
            self.assertEqual(payload["textContent"].count("/jobs/1"), 1)
            self.assertIn("idempotencyKey", payload["headers"])
            contact["attributes"]["ALERT_LAST_SENT_DATE"] = "2026-10-26"
            api.reset_mock()
            self.assertFalse(send_digest(contact, jobs, report_date="2026-10-26", api_key="fake",
                             sender_email="jobs@ontapjobsearch.com", unsubscribe_secret="fake",
                             site_url=PRIVATE_TEST_ORIGIN, private_test=True))
            api.assert_not_called()
