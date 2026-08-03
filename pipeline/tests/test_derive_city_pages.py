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
    load_markdown_actions,
    load_review_decisions,
    markdown_review_text,
    merge_review_overrides,
    process_config,
    review_job_id,
    selected_live_jobs,
)


def config(*, mode: str = "review_only", threshold: int = 3) -> CityConfig:
    return CityConfig(
        city_key="newcastle-service-administrator",
        display_name="Newcastle",
        category_label="admin and customer-service jobs",
        parent_page=Path("app/north-east/service-administrator-jobs.json"),
        review_csv=Path("pipeline/reviews/city-pages/newcastle.csv"),
        summary_md=Path("pipeline/reviews/city-pages/newcastle.md"),
        output_json=Path("app/_city-pages/newcastle/service-administrator-jobs.json"),
        route="/newcastle/service-administrator-jobs",
        minimum_live_jobs=threshold,
        mode=mode,
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
    title: str | None = None,
    company: str = "Employer",
    summary: str = "",
    source: str = "Test",
) -> dict[str, str]:
    return {
        "job_id": job_id,
        "title": title or f"Job {job_id}",
        "company": company,
        "location": location,
        "summary": summary,
        "description": f"Full description for {job_id}",
        "apply_url": f"https://example.test/{job_id}",
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
        self.assertEqual(rows[0]["action"], "")

    def test_rows_are_sorted_include_review_exclude_then_title(self) -> None:
        jobs = [
            job("4", "Bedlington"),
            job("2", "Tyne and Wear, home-based"),
            job("3", "Newcastle"),
            job("1", "Newcastle"),
        ]
        rows = derive_rows(jobs, config())
        self.assertEqual(
            [(row["decision"], row["title"]) for row in rows],
            [
                ("include", "Job 1"),
                ("include", "Job 3"),
                ("review", "Job 2"),
                ("exclude", "Job 4"),
            ],
        )

    def test_jobg8_review_id_is_source_prefixed(self) -> None:
        row = job("abc-123", "Newcastle", source="JobG8")
        self.assertEqual(review_job_id(row), "jobg8-abc-123")
        rows = derive_rows([row], config())
        self.assertEqual(rows[0]["job_id"], "jobg8-abc-123")

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
        self.assertEqual(rows[0]["action"], "select")

    def test_csv_loader_ignores_untouched_prefilled_decisions(self) -> None:
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

    def test_markdown_loader_reads_select_and_exclude(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "review.md"
            path.write_text(
                "---\naction: select\njob_id: jobg8-1\n---\n\n"
                "---\naction: exclude\njob_id: nejobs-2\n---\n",
                encoding="utf-8",
            )
            self.assertEqual(
                load_markdown_actions(path),
                {"jobg8-1": "include", "nejobs-2": "exclude"},
            )

    def test_conflicting_csv_and_markdown_overrides_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            merge_review_overrides({"1": "include"}, {"1": "exclude"})

    def test_markdown_review_lists_every_job_with_action_line(self) -> None:
        rows = derive_rows(
            [
                job("1", "Newcastle"),
                job("2", "Tyne and Wear, home-based"),
                job("3", "Bedlington"),
            ],
            config(),
        )
        text = markdown_review_text(config(), rows)
        self.assertEqual(
            sum(line.startswith("action:") for line in text.splitlines()), 3
        )
        self.assertIn("blank review remains omitted", text)
        self.assertIn("## INCLUDE (1)", text)
        self.assertIn("## REVIEW (1)", text)
        self.assertIn("## EXCLUDE (1)", text)

    def test_selected_live_jobs_contains_only_effective_includes(self) -> None:
        jobs = [
            job("1", "Newcastle"),
            job("2", "Tyne and Wear"),
            job("3", "Bedlington"),
        ]
        rows = derive_rows(
            jobs,
            config(),
            prior_actions={"2": "include", "1": "exclude"},
        )
        selected = selected_live_jobs(jobs, rows)
        self.assertEqual([item["job_id"] for item in selected], ["2"])
        self.assertEqual(selected[0]["description"], "Full description for 2")

    def test_review_only_run_never_writes_live_json(self) -> None:
        cfg = config(mode="review_only", threshold=1)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent = root / cfg.parent_page
            parent.parent.mkdir(parents=True)
            parent.write_text(json.dumps([job("1", "Newcastle")]), encoding="utf-8")

            result = process_config(cfg, root, write_review=True, write_live=True)

            self.assertEqual(result["live_status"], "review-only")
            self.assertFalse((root / cfg.output_json).exists())

    def test_publish_writes_only_selected_jobs_and_omits_blank_review(self) -> None:
        cfg = config(mode="publish", threshold=2)
        jobs = [
            job("1", "Newcastle"),
            job("2", "Tyne and Wear"),
            job("3", "Bedlington"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent = root / cfg.parent_page
            parent.parent.mkdir(parents=True)
            parent.write_text(json.dumps(jobs), encoding="utf-8")
            markdown = root / cfg.summary_md
            markdown.parent.mkdir(parents=True)
            markdown.write_text(
                "---\naction: select\njob_id: 2\n---\n",
                encoding="utf-8",
            )

            result = process_config(cfg, root, write_review=True, write_live=True)

            self.assertEqual(result["live_status"], "published")
            published = json.loads((root / cfg.output_json).read_text(encoding="utf-8"))
            self.assertEqual({item["job_id"] for item in published}, {"1", "2"})
            self.assertNotIn("3", {item["job_id"] for item in published})

    def test_publish_removes_stale_output_below_threshold(self) -> None:
        cfg = config(mode="publish", threshold=2)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent = root / cfg.parent_page
            parent.parent.mkdir(parents=True)
            parent.write_text(json.dumps([job("1", "Newcastle")]), encoding="utf-8")
            output = root / cfg.output_json
            output.parent.mkdir(parents=True)
            output.write_text('[{"job_id":"stale"}]', encoding="utf-8")

            result = process_config(cfg, root, write_review=True, write_live=True)

            self.assertEqual(result["live_status"], "withheld-below-threshold")
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
