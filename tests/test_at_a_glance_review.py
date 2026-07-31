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
    review_job,
    word_count,
    write_csv,
    write_markdown,
)


class AtAGlanceReviewTests(unittest.TestCase):
    def test_admin_summary_uses_supported_duties_not_opening_boilerplate(self) -> None:
        job = {
            "job_id": "service-1",
            "title": "Service Administrator",
            "source": "JobG8",
            "category": "Admin/Service – Office Support",
            "description": (
                "Your new company. An established organisation is recruiting. "
                "Managing shared service inboxes and responding to customer enquiries. "
                "Logging service calls and updating reactive and planned service jobs. "
                "Producing engineer service records and managing customer portals. "
                "Issuing weekly engineer call-out rotas."
            ),
        }

        row = review_job(job, ["app/hampshire/service-administrator-jobs.json"])

        self.assertEqual(row["status"], "generated")
        self.assertNotIn("Your new company", row["proposed_at_a_glance"])
        self.assertIn("customer enquiries", row["proposed_at_a_glance"])
        self.assertIn("service jobs and engineer records", row["proposed_at_a_glance"])
        self.assertGreaterEqual(word_count(row["proposed_at_a_glance"]), 15)
        self.assertLessEqual(word_count(row["proposed_at_a_glance"]), 25)

        evidence = json.loads(row["evidence_json"])
        self.assertTrue(evidence)
        self.assertTrue(all(item["attribute"] and item["evidence"] for item in evidence))

    def test_reception_summary_is_deterministic_and_factual(self) -> None:
        job = {
            "job_id": "reception-1",
            "title": "Receptionist",
            "source": "JobG8",
            "category": "Admin/Service – Office Support",
            "description": (
                "Greet visitors and clients, ensuring a professional first impression. "
                "Answer and redirect phone calls promptly and accurately. "
                "Manage meeting room bookings and prepare spaces for use. "
                "Handle incoming and outgoing mail and deliveries. "
                "Provide administrative support to the wider team."
            ),
        }

        first = review_job(job, ["a.json"])
        second = review_job(job, ["a.json"])

        self.assertEqual(first, second)
        self.assertEqual(first["status"], "generated")
        self.assertIn("welcoming visitors", first["proposed_at_a_glance"])
        self.assertIn("handling telephone calls", first["proposed_at_a_glance"])
        self.assertNotIn("salary", first["proposed_at_a_glance"].casefold())

    def test_support_worker_summary_uses_care_duties(self) -> None:
        job = {
            "job_id": "support-1",
            "title": "Support Worker",
            "source": "JobG8",
            "category": "Support Worker – Wide",
            "description": (
                "The role involves supporting adults with all aspects of daily life, "
                "including personal care. Accessing the community regularly and taking "
                "service users to activities. Assist with medical and welfare needs. "
                "Safeguard and support service user independence."
            ),
        }

        row = review_job(job, ["app/north-east/support-worker-jobs.json"])

        self.assertEqual(row["status"], "generated")
        self.assertIn("providing personal care", row["proposed_at_a_glance"])
        self.assertIn("supporting daily living", row["proposed_at_a_glance"])
        self.assertIn("supporting community access", row["proposed_at_a_glance"])

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
        self.assertEqual(row["proposed_at_a_glance"], "")

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
                "This is a long enough vacancy description for an administrator. "
                "The successful applicant will prepare reports. "
                "The employer offers a supportive culture, pension and annual leave."
            ),
        }

        row = review_job(job, ["admin.json"])

        self.assertEqual(row["status"], "omitted")
        self.assertEqual(row["reason"], "fewer than two supported task attributes")

    def test_description_hash_changes_with_rule_or_description(self) -> None:
        value = "Maintaining records and systems."
        self.assertEqual(description_hash(value), description_hash(value))
        self.assertNotEqual(description_hash(value), description_hash(value + " More."))
        self.assertEqual(len(description_hash(value)), 64)
        self.assertEqual(RULE_VERSION, "1")

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
                    "Greet visitors and answer incoming phone calls. "
                    "Manage meeting room bookings and maintain accurate records. "
                    "Prepare documents and correspondence for the wider team while "
                    "responding to customer enquiries throughout the working day."
                ),
            }
            first.write_text(json.dumps([job]), encoding="utf-8")
            second.write_text(json.dumps([job]), encoding="utf-8")

            rows = build_review(root)

            self.assertEqual(len(rows), 1)
            self.assertIn(first.as_posix(), rows[0]["pages"])
            self.assertIn(second.as_posix(), rows[0]["pages"])

    def test_review_outputs_are_written_without_modifying_source_json(self) -> None:
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
                        "Greet visitors and answer incoming phone calls. "
                        "Manage meeting room bookings and maintain accurate records. "
                        "Prepare documents and correspondence for the wider team while "
                        "responding to customer enquiries throughout the working day."
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
            self.assertTrue(csv_path.exists())
            self.assertTrue(markdown_path.exists())
            with csv_path.open(encoding="utf-8-sig", newline="") as handle:
                csv_rows = list(csv.DictReader(handle))
            self.assertEqual(csv_rows[0]["status"], "generated")
            self.assertIn(
                "# At-a-glance review", markdown_path.read_text(encoding="utf-8")
            )


if __name__ == "__main__":
    unittest.main()
