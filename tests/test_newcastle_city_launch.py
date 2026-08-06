import csv
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def review_rows() -> list[dict[str, str]]:
    review_path = (
        REPO_ROOT
        / "pipeline/reviews/city-pages/newcastle-service-administrator-review.csv"
    )
    with review_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class NewcastleCityLaunchTests(unittest.TestCase):
    def test_register_enables_gated_live_page(self) -> None:
        register = json.loads(
            (REPO_ROOT / "pipeline/city_pages/city-page-register.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(len(register), 1)
        city = register[0]
        self.assertEqual(city["mode"], "publish")
        self.assertEqual(city["minimum_live_jobs"], 8)
        self.assertEqual(city["route"], "/newcastle/service-administrator-jobs")
        self.assertEqual(
            city["output_json"],
            "app/_city-pages/newcastle/service-administrator-jobs.json",
        )

    def test_live_output_matches_current_review_choices(self) -> None:
        city_jobs = json.loads(
            (
                REPO_ROOT
                / "app/_city-pages/newcastle/service-administrator-jobs.json"
            ).read_text(encoding="utf-8")
        )
        city_ids = {job["job_id"] for job in city_jobs}
        included_ids = {
            row["job_id"]
            for row in review_rows()
            if row["effective_decision"] == "include"
        }

        self.assertGreaterEqual(len(city_jobs), 8)
        self.assertEqual(city_ids, included_ids)
        self.assertTrue(all(job.get("apply_url") for job in city_jobs))

        parent_jobs = json.loads(
            (
                REPO_ROOT / "app/north-east/service-administrator-jobs.json"
            ).read_text(encoding="utf-8")
        )
        self.assertTrue(city_ids.issubset({job["job_id"] for job in parent_jobs}))

    def test_review_csv_has_no_unresolved_decisions(self) -> None:
        rows = review_rows()
        counts = {decision: 0 for decision in ("include", "review", "exclude")}
        for row in rows:
            counts[row["effective_decision"]] += 1

        city_jobs = json.loads(
            (
                REPO_ROOT
                / "app/_city-pages/newcastle/service-administrator-jobs.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(counts["review"], 0)
        self.assertEqual(counts["include"], len(city_jobs))
        self.assertGreater(counts["exclude"], 0)

    def test_route_and_sitemap_use_active_city_data_gate(self) -> None:
        route_source = (
            REPO_ROOT / "app/newcastle/service-administrator-jobs/page.tsx"
        ).read_text(encoding="utf-8")
        self.assertIn("isCityPageActive", route_source)
        self.assertIn("notFound()", route_source)
        self.assertIn("newcastleServiceAdministratorPage", route_source)

        sitemap_source = (REPO_ROOT / "app/sitemap.ts").read_text(encoding="utf-8")
        self.assertIn("newcastleServiceAdministratorPage.route", sitemap_source)
        self.assertIn("minimumJobs", sitemap_source)

    def test_derived_city_json_is_not_added_to_job_detail_catalogue(self) -> None:
        source = (REPO_ROOT / "lib/published-jobs.ts").read_text(encoding="utf-8")
        self.assertIn('DERIVED_CITY_DATA_DIRECTORY = "_city-pages"', source)
        self.assertIn("entry.name === DERIVED_CITY_DATA_DIRECTORY", source)


if __name__ == "__main__":
    unittest.main()
