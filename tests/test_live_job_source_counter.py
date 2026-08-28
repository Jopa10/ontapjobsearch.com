from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from pipeline.scripts.live_job_source_counter import (
    build_reports,
    canonical_source,
    collect_live_inventory,
    collect_live_jobs,
)


def _job(
    job_id: str,
    *,
    source: str = "JobG8",
    title: str = "Administrator",
    location: str = "Leeds",
    region: str = "West Yorkshire",
    category: str = "Admin/Service",
    apply_url: str | None = None,
    closing_date: str | None = None,
    closing_datetime: str | None = None,
) -> dict[str, str]:
    row = {
        "job_id": job_id,
        "title": title,
        "location": location,
        "region": region,
        "category": category,
        "apply_url": apply_url or f"https://example.com/jobs/{job_id}",
        "source": source,
    }
    if closing_date is not None:
        row["closing_date"] = closing_date
    if closing_datetime is not None:
        row["closing_datetime"] = closing_datetime
    return row


class LiveJobSourceCounterTests(unittest.TestCase):
    def test_source_aliases_are_normalised_without_guessing_unknown_values(self) -> None:
        self.assertEqual(canonical_source("jobg8"), "JobG8")
        self.assertEqual(canonical_source("North East Jobs"), "NEJobs")
        self.assertEqual(canonical_source("VONNE Jobs"), "VONNE")
        self.assertEqual(canonical_source("Future Provider"), "Future Provider")
        self.assertEqual(canonical_source(""), "Unknown")

    def test_counts_only_job_arrays_and_deduplicates_published_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            app = root / "app"
            reports = root / "pipeline" / "reports-daily"
            (app / "north-east").mkdir(parents=True)
            (app / "west-yorkshire").mkdir(parents=True)

            (app / "north-east" / "admin.json").write_text(
                json.dumps(
                    [
                        _job("jobg8-1"),
                        _job(
                            "nejobs-1",
                            source="North East Jobs",
                            location="Durham",
                            region="North East",
                        ),
                        _job(
                            "vonne-1",
                            source="VONNE",
                            location="Newcastle",
                            region="North East",
                        ),
                    ]
                ),
                encoding="utf-8",
            )
            (app / "west-yorkshire" / "admin.json").write_text(
                json.dumps(
                    [
                        _job("jobg8-1"),
                        _job(
                            "duplicate-url-new-id",
                            apply_url="https://example.com/jobs/jobg8-1?utm_source=copy",
                        ),
                        _job("jobg8-2", location="Bradford"),
                    ]
                ),
                encoding="utf-8",
            )
            (app / "not-jobs.json").write_text(
                json.dumps([{"name": "not a vacancy"}]),
                encoding="utf-8",
            )

            result = build_reports(app, reports, "2026-08-01")

            self.assertEqual(result.total_live_jobs, 4)
            self.assertEqual(result.jobg8_jobs, 2)
            self.assertEqual(result.external_jobs, 2)
            self.assertEqual(result.source_counts["NEJobs"], 1)
            self.assertEqual(result.source_counts["VONNE"], 1)
            self.assertEqual(result.job_json_files, 2)
            self.assertEqual(result.duplicate_rows_ignored, 2)
            inventory = collect_live_inventory(app)
            self.assertEqual(len(inventory.placements), 6)
            self.assertEqual(inventory.jobs_with_repeated_rows, 1)
            self.assertEqual(
                [placement.canonical_job_id for placement in inventory.placements].count("jobg8-1"),
                3,
            )
            self.assertTrue(result.daily_report_path.exists())
            self.assertTrue(result.history_path.exists())

    def test_expired_rows_are_not_counted_as_live(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            app = root / "app"
            reports = root / "pipeline" / "reports-daily"
            app.mkdir(parents=True)
            (app / "jobs.json").write_text(
                json.dumps(
                    [
                        _job("jobg8-1"),
                        _job("vonne-expired", source="VONNE", closing_date="2026-08-11"),
                        _job("vonne-live", source="VONNE", closing_date="2026-08-16"),
                        _job("nejobs-bad-date", source="NEJobs", closing_date="not-a-date"),
                    ]
                ),
                encoding="utf-8",
            )

            result = build_reports(app, reports, "2026-08-12")

            self.assertEqual(result.total_live_jobs, 3)
            self.assertEqual(result.jobg8_jobs, 1)
            self.assertEqual(result.external_jobs, 2)
            self.assertEqual(result.source_counts["VONNE"], 1)
            self.assertEqual(result.source_counts["NEJobs"], 1)

    def test_history_has_one_row_per_day_and_replaces_same_day(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            app = root / "app"
            reports = root / "pipeline" / "reports-daily"
            app.mkdir(parents=True)
            live_file = app / "jobs.json"

            live_file.write_text(
                json.dumps([_job("jobg8-1"), _job("nejobs-1", source="NEJobs")]),
                encoding="utf-8",
            )
            build_reports(app, reports, "2026-08-01")

            live_file.write_text(
                json.dumps(
                    [
                        _job("jobg8-1"),
                        _job("jobg8-2"),
                        _job("nejobs-1", source="NEJobs"),
                    ]
                ),
                encoding="utf-8",
            )
            build_reports(app, reports, "2026-08-01")
            build_reports(app, reports, "2026-08-02")

            with (reports / "live-job-source-history.csv").open(
                encoding="utf-8", newline=""
            ) as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(
                [row["report_date"] for row in rows],
                ["2026-08-01", "2026-08-02"],
            )
            self.assertEqual(rows[0]["total_live_jobs"], "3")
            self.assertEqual(rows[0]["jobg8_jobs"], "2")
            self.assertEqual(rows[0]["external_jobs"], "1")
            self.assertEqual(rows[0]["nejobs_jobs"], "1")

    def test_conflicting_sources_for_same_job_id_stop_the_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            app = Path(temp) / "app"
            app.mkdir()
            (app / "one.json").write_text(
                json.dumps([_job("same-id", source="JobG8")]),
                encoding="utf-8",
            )
            (app / "two.json").write_text(
                json.dumps([_job("same-id", source="NEJobs")]),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Conflicting sources"):
                collect_live_jobs(app)


if __name__ == "__main__":
    unittest.main()
