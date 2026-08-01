from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from pipeline.scripts.generate_at_a_glance_review import (
    RULE_VERSION,
    build_review,
    current_card_summary,
    description_hash,
    duty_lines,
    review_job,
    word_count,
    write_csv,
    write_markdown,
)


class AtAGlanceReviewTests(unittest.TestCase):
    def test_admin_summary_uses_duties_not_opening_boilerplate(self) -> None:
        job = {
            "job_id": "service-1",
            "title": "Service Administrator",
            "source": "JobG8",
            "category": "Admin/Service – Office Support",
            "description": (
                "Your new company\nAn established organisation is recruiting.\n"
                "Your new role\n"
                "Managing shared service inboxes and responding to customer enquiries.\n"
                "Logging service calls and updating reactive and planned service jobs.\n"
                "Producing engineer service records and managing customer portals.\n"
                "Issuing weekly engineer call-out rotas.\n"
                "What you'll need to succeed\nPrevious administration experience."
            ),
        }

        row = review_job(job, ["app/hampshire/service-administrator-jobs.json"])

        self.assertEqual(row["status"], "generated")
        self.assertNotIn("Your new company", row["proposed_at_a_glance"])
        self.assertIn("customer enquiries", row["proposed_at_a_glance"])
        self.assertIn("service-call coordination", row["proposed_at_a_glance"])
        self.assertLessEqual(word_count(row["proposed_at_a_glance"]), 22)

        evidence = json.loads(row["evidence_json"])
        self.assertTrue(evidence)
        self.assertTrue(all(item["attribute"] and item["evidence"] for item in evidence))

    def test_duty_sections_stop_before_requirements_and_benefits(self) -> None:
        description = (
            "About the Role\n"
            "Greet visitors and answer incoming phone calls.\n"
            "Maintain accurate records.\n"
            "What we're looking for\n"
            "Experience of payroll systems is desirable.\n"
            "Benefits\n"
            "Timesheets can be completed on mobile devices."
        )

        lines = duty_lines(description)

        self.assertIn("Greet visitors and answer incoming phone calls.", lines)
        self.assertIn("Maintain accurate records.", lines)
        self.assertNotIn("Experience of payroll systems is desirable.", lines)
        self.assertNotIn("Timesheets can be completed on mobile devices.", lines)

    def test_medical_admin_ignores_benefit_timesheets(self) -> None:
        job = {
            "job_id": "medical-1",
            "title": "Medical Administrator",
            "source": "JobG8",
            "category": "Admin/Service – Office Support",
            "description": (
                "The key duties and requirements are:\n"
                "- Taking enquiries from clients over email and the phone\n"
                "- Meet and greet patients\n"
                "- Uploading referrals on the patient management system\n"
                "- Liaising with clients and clinicians to arrange appointments\n"
                "- Collating reports and correspondence to a high standard\n"
                "- Coordinating incoming and outgoing mail\n"
                "- Completing detailed and accurate records\n"
                "We'd love to speak to candidates who:\n"
                "- Have administration experience\n"
                "Amazing Benefits:\n"
                "- Timesheets can be completed on mobile devices"
            ),
        }

        row = review_job(job, ["app/kent/service-administrator-jobs.json"])

        self.assertEqual(row["status"], "generated")
        self.assertIn("visitor reception", row["proposed_at_a_glance"])
        self.assertIn("telephone handling", row["proposed_at_a_glance"])
        self.assertNotIn("payroll", row["proposed_at_a_glance"].casefold())

    def test_reception_flexible_working_does_not_become_hr_duty(self) -> None:
        job = {
            "job_id": "reception-1",
            "title": "Receptionist - Bank - Care Home",
            "source": "JobG8",
            "category": "Admin/Service – Office Support",
            "description": (
                "ABOUT THE ROLEThis is a casual, part-time role offering flexible working.\n"
                "You can expect to answer phone calls, greet visitors, manage the "
                "reception area and show prospective residents around.\n"
                "We might also need you to carry out typing, photocopying and filing.\n"
                "ABOUT YOUYou'll need to be professional.\n"
                "REWARDS PACKAGECompetitive pay."
            ),
        }

        row = review_job(job, ["app/kent/service-administrator-jobs.json"])

        self.assertEqual(row["status"], "generated")
        self.assertIn("visitor reception", row["proposed_at_a_glance"])
        self.assertIn("telephone handling", row["proposed_at_a_glance"])
        self.assertNotIn("starter", row["proposed_at_a_glance"].casefold())
        self.assertNotIn("contract changes", row["proposed_at_a_glance"].casefold())

    def test_support_worker_summary_uses_care_duties(self) -> None:
        job = {
            "job_id": "support-1",
            "title": "Support Worker",
            "source": "JobG8",
            "category": "Support Worker – Wide",
            "description": (
                "About the Role\n"
                "The role involves supporting adults with all aspects of daily life, "
                "including personal care.\n"
                "Accessing the community regularly.\n"
                "Your Day-to-Day\n"
                "Assist with medical and welfare needs.\n"
                "Safeguard.\n"
                "You are\nA good communicator."
            ),
        }

        row = review_job(job, ["app/north-east/support-worker-jobs.json"])

        self.assertEqual(row["status"], "generated")
        self.assertIn("personal care", row["proposed_at_a_glance"])
        self.assertIn("daily-living support", row["proposed_at_a_glance"])
        self.assertIn("community access", row["proposed_at_a_glance"])
        self.assertIn("safeguarding", row["proposed_at_a_glance"])

    def test_explicitly_truncated_job_is_omitted(self) -> None:
        job = {
            "job_id": "truncated-1",
            "title": "Complex Care Assistant",
            "source": "JobG8",
            "category": "Support Worker – Wide",
            "description": (
                "Support an individual with personal care and community access. "
                "This role is advertised under a Genuine Occupational Requirement. "
                "Click apply for full job details"
            ),
        }

        row = review_job(job, ["support.json"])

        self.assertEqual(row["status"], "omitted")
        self.assertEqual(
            row["reason"],
            "description contains an explicit truncation marker",
        )

    def test_external_source_is_omitted_when_duties_are_not_retained(self) -> None:
        job = {
            "job_id": "nejobs-123",
            "title": "Administration Assistant",
            "source": "NEJobs",
            "category": "Admin/Service – Office Support",
            "summary": (
                "Administration Assistant with Example Council in Durham. "
                "Permanent; Full time; £25,000."
            ),
            "description": (
                "Example Council is recruiting for this vacancy in Durham. "
                "Use the original North East Jobs advert to check the complete duties."
            ),
        }

        row = review_job(job, ["north-east.json"])

        self.assertEqual(row["status"], "omitted")
        self.assertEqual(
            row["reason"],
            "external source duties are not retained for safe extraction",
        )

    def test_job_with_fewer_than_two_task_attributes_is_omitted(self) -> None:
        job = {
            "job_id": "thin-1",
            "title": "Administrator",
            "source": "JobG8",
            "category": "Admin/Service – Office Support",
            "description": (
                "About the Role\n"
                "The successful applicant will prepare reports.\n"
                "What we're looking for\n"
                "The employer values attention to detail and communication."
            ),
        }

        row = review_job(job, ["admin.json"])

        self.assertEqual(row["status"], "omitted")
        self.assertIn(
            row["reason"],
            {
                "fewer than two supported task attributes",
                "no reliable duties section found",
            },
        )

    def test_description_hash_is_versioned_and_deterministic(self) -> None:
        value = "Maintaining records and systems."
        self.assertEqual(description_hash(value), description_hash(value))
        self.assertNotEqual(description_hash(value), description_hash(value + " More."))
        self.assertEqual(len(description_hash(value)), 64)
        self.assertEqual(RULE_VERSION, "3")

    def test_current_card_summary_matches_existing_first_sentence_behaviour(self) -> None:
        job = {
            "summary": "",
            "description": (
                "Your new company. The actual role includes managing service calls "
                "and customer enquiries."
            ),
        }
        self.assertEqual(current_card_summary(job), "Your new company.")

    def test_build_review_deduplicates_jobs_across_live_pages(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "app"
            first = root / "one" / "jobs.json"
            second = root / "two" / "jobs.json"
            first.parent.mkdir(parents=True)
            second.parent.mkdir(parents=True)
            job = {
                "job_id": "duplicate-1",
                "title": "Receptionist",
                "source": "JobG8",
                "category": "Admin/Service – Office Support",
                "description": (
                    "Duties\n"
                    "Greet visitors and answer incoming phone calls.\n"
                    "Manage meeting room bookings and maintain accurate records.\n"
                    "Requirements\nPrevious administration experience."
                ),
            }
            first.write_text(json.dumps([job]), encoding="utf-8")
            second.write_text(json.dumps([job]), encoding="utf-8")

            rows = build_review(root)

            self.assertEqual(len(rows), 1)
            self.assertIn(first.as_posix(), rows[0]["pages"])
            self.assertIn(second.as_posix(), rows[0]["pages"])

    def test_review_outputs_do_not_modify_source_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            app_root = root / "app"
            source_path = app_root / "region" / "jobs.json"
            source_path.parent.mkdir(parents=True)
            jobs = [
                {
                    "job_id": "write-1",
                    "title": "Receptionist",
                    "source": "JobG8",
                    "category": "Admin/Service – Office Support",
                    "description": (
                        "Duties\n"
                        "Greet visitors and answer incoming phone calls.\n"
                        "Manage meeting room bookings and maintain accurate records.\n"
                        "Requirements\nPrevious administration experience."
                    ),
                }
            ]
            source_content = json.dumps(jobs, indent=2)
            source_path.write_text(source_content, encoding="utf-8")

            rows = build_review(app_root)
            csv_path = root / "review.csv"
            markdown_path = root / "review.md"
            write_csv(csv_path, rows)
            write_markdown(markdown_path, rows)

            self.assertEqual(source_path.read_text(encoding="utf-8"), source_content)
            with csv_path.open(encoding="utf-8-sig", newline="") as handle:
                csv_rows = list(csv.DictReader(handle))
            self.assertEqual(csv_rows[0]["status"], "generated")
            self.assertIn(
                "# At-a-glance review", markdown_path.read_text(encoding="utf-8")
            )


if __name__ == "__main__":
    unittest.main()
