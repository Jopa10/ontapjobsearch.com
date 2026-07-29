import json
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[1]
JOBS_PATH = ROOT / "app" / "north-east" / "service-administrator-jobs.json"


class NorthEastJobsPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        jobs = json.loads(JOBS_PATH.read_text(encoding="utf-8-sig"))
        cls.preview_jobs = [job for job in jobs if job.get("source") == "NEJobs"]

    def test_preview_contains_two_distinct_nejobs_roles(self):
        self.assertEqual(2, len(self.preview_jobs))
        self.assertEqual(
            {"nejobs-299480", "nejobs-299953"},
            {job["job_id"] for job in self.preview_jobs},
        )

    def test_preview_uses_ontap_summaries_not_full_source_adverts(self):
        for job in self.preview_jobs:
            with self.subTest(job_id=job["job_id"]):
                description = job["description"]
                self.assertGreaterEqual(len(description), 200)
                self.assertLess(len(description), 800)
                self.assertNotIn("WHAT IS INVOLVED?", description)
                self.assertNotIn("HOW TO APPLY", description)
                self.assertNotIn("<", description)

    def test_apply_links_identify_ontap_referrals(self):
        for job in self.preview_jobs:
            with self.subTest(job_id=job["job_id"]):
                parsed = urlparse(job["apply_url"])
                query = parse_qs(parsed.query)
                self.assertEqual("www.northeastjobs.org.uk", parsed.netloc)
                self.assertEqual(["ontap"], query["utm_source"])
                self.assertEqual(["referral"], query["utm_medium"])
                self.assertEqual(["nejobs_pilot"], query["utm_campaign"])

    def test_preview_keeps_source_and_freshness_fields(self):
        for job in self.preview_jobs:
            with self.subTest(job_id=job["job_id"]):
                self.assertEqual("NEJobs", job["source"])
                self.assertRegex(job["posted_date"], r"^\d{4}-\d{2}-\d{2}$")
                self.assertRegex(job["closing_date"], r"^\d{4}-\d{2}-\d{2}$")


if __name__ == "__main__":
    unittest.main()
