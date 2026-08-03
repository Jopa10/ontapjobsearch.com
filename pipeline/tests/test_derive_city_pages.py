from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from scripts.derive_city_pages import (  # noqa: E402
    CityConfig,
    FIELDNAMES,
    Rule,
    classify_job,
    derive_rows,
    load_review_decisions,
    process_config,
    review_job_id,
)


def config() -> CityConfig:
    return CityConfig(
        city_key="newcastle-service-administrator",
        display_name="Newcastle",
        category_label="service-administrator jobs",
        parent_page=Path("app/north-east/service-administrator-jobs.json"),
        review_csv=Path("pipeline/reviews/city-pages/newcastle.csv"),
        summary_md=Path("pipeline/reviews/city-pages/newcastle.md"),
        minimum_live_jobs=3,
        mode="review_only",
        include_rules=(
            Rule("newcastle", "Newcastle stated"),
            Rule("north tyneside", "Normal Newcastle catchment"),
            Rule("shiremoor", "Metro-connected Newcastle catchment"),
            Rule("wideopen", "Normal Newcastle catchment"),
        ),
        review_rules=(
            Rule("tyne and wear", "Broad Tyne and Wear location"),
            Rule("home-based", "Home-based eligibility needs review"),
            Rule("regionwide", "Broad regional location"),
        ),
        exclude_rules=(
            Rule("bedlington", "Outside agreed catchment"),
            Rule("durham", "Separate employment area"),
        ),
        fallback_decision="review",
        fallback_reason="No rule matched",
    )


def job(
    job_id: str,
    location: str,
    *,
    company: str = "Employer",
    summary: str = "",
    source: str = "Test",
) -> dict[str, str]:
    return {
        "job_id": job_id,
        "title": f"Job {job_id}",
        "company": company,
        "location": location,
        "summary": summary,
        "source": source,
    }


class CityPageDerivationTests(unittest.TestCase):
    def test_decision_is_first_csv_column(self) -> None:
        self.assertEqual(FIELDNAMES[0], "decision")

    def test_decision_is_prefilled_with_automatic_result(self) -> None:
        rows = derive_rows([job("1", "Newcastle")], config())
        self.assertEqual(rows[0]["automatic_decision"], "include")
        self.assertEqual(rows[0]["decision"], "include")
        self.assertEqual(rows[0]["effective_decision"], "include")

    def test_jobg8_review_id_is_source_prefixed(self) -> None:
        row = job("abc-123", "Newcastle", source="JobG8")
        self.assertEqual(review_job_id(row), "jobg8-abc-123")
        rows = derive_rows([row], config())
        self.assertEqual(rows[0]["job_id"], "jobg8-abc-123")

    def test_existing_source_prefixes_are_unchanged(self) -> None:
        self.assertEqual(
            review_job_id(job("nejobs-123", "Newcastle", source="NEJobs")),
            "nejobs-123",
        )
        self.assertEqual(
            review_job_id(job("vonne-123", "Newcastle", source="VONNE")),
            "vonne-123",
        )

    def test_agreed_newcastle_locations_are_included(self) -> None:
        cfg = config()
        for location in (
            "Newcastle upon Tyne",
            "Shiremoor office",
            "Wideopen, Newcastle upon Tyne",
            "North Tyneside",
            "Newcastle / Regionwide",
        ):
            with self.subTest(location=location):
                decision, _, _ = classify_job(job("1", location), cfg)
                self.assertEqual(decision, "include")

    def test_tynewear_home_based_is_review(self) -> None:
        decision, rule, reason = classify_job(
            job("1", "Tyne and Wear, home-based"), config()
        )
        self.assertEqual(decision, "review")
        self.assertEqual(rule, "tyne and wear")
        self.assertIn("Broad", reason)

    def test_bedlington_is_excluded_even_with_newcastle_postal_wording(self) -> None:
        decision, rule, _ = classify_job(
            job("1", "Bedlington, Newcastle upon Tyne postal area"), config()
        )
        self.assertEqual(decision, "exclude")
        self.assertEqual(rule, "bedlington")

    def test_context_can_exclude_but_never_include(self) -> None:
        cfg = config()
        decision, rule, _ = classify_job(
            job("1", "Town Hall", company="Durham County Council"), cfg
        )
        self.assertEqual((decision, rule), ("exclude", "context:durham"))

        decision, rule, _ = classify_job(
            job("2", "Town Hall", company="Newcastle City Council"), cfg
        )
        self.assertEqual((decision, rule), ("review", "fallback"))

    def test_saved_override_is_retained_and_effective(self) -> None:
        rows = derive_rows(
            [job("1", "Tyne and Wear, home-based")],
            config(),
            prior_actions={"1": "include"},
        )
        self.assertEqual(rows[0]["automatic_decision"], "review")
        self.assertEqual(rows[0]["decision"], "include")
        self.assertEqual(rows[0]["effective_decision"], "include")

    def test_loader_ignores_untouched_prefilled_decisions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["decision", "job_id", "automatic_decision"],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "job_id": "1",
                        "decision": "include",
                        "automatic_decision": "include",
                    }
                )
                writer.writerow(
                    {
                        "job_id": "2",
                        "decision": "exclude",
                        "automatic_decision": "review",
                    }
                )
            self.assertEqual(load_review_decisions(path), {"2": "exclude"})

    def test_process_writes_prefilled_review_but_no_live_city_page(self) -> None:
        cfg = config()
        jobs = [
            job("1", "Newcastle"),
            job("2", "Shiremoor"),
            job("3", "North Tyneside"),
            job("4", "Tyne and Wear, home-based"),
            job("5", "Bedlington"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent = root / cfg.parent_page
            parent.parent.mkdir(parents=True)
            parent.write_text(json.dumps(jobs), encoding="utf-8")

            result = process_config(cfg, root, True)

            self.assertTrue((root / cfg.review_csv).is_file())
            self.assertTrue((root / cfg.summary_md).is_file())
            self.assertFalse(
                (root / "app/newcastle/service-administrator-jobs.json").exists()
            )
            with (root / cfg.review_csv).open(
                "r", encoding="utf-8", newline=""
            ) as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["decision"], "include")
            self.assertEqual(result["include_count"], 3)
            self.assertEqual(result["review_count"], 1)
            self.assertEqual(result["exclude_count"], 1)
            self.assertTrue(result["threshold_met"])


if __name__ == "__main__":
    unittest.main()
