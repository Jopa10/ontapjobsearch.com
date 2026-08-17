import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.published_job_daily_ledger import update_ledger


class PublishedJobDailyLedgerTests(unittest.TestCase):
    def _write_jobs(self, app_dir: Path, rows: list[dict[str, str]]) -> None:
        target = app_dir / "test" / "jobs.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(rows), encoding="utf-8")

    def _job(
        self,
        job_id: str,
        *,
        source: str = "JobG8",
        title: str = "Administrator",
    ) -> dict[str, str]:
        return {
            "job_id": job_id,
            "title": title,
            "location": "Leeds",
            "region": "Yorkshire - West",
            "category": "Admin/Service – Office Support",
            "source": source,
            "apply_url": f"https://example.test/apply/{job_id}",
        }

    def _read_csv(self, path: Path) -> list[dict[str, str]]:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_baseline_then_only_first_seen_jobs_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            app_dir = root / "app"
            reports_dir = root / "reports"

            self._write_jobs(
                app_dir,
                [self._job("A"), self._job("B", source="VONNE")],
            )
            history, daily, baseline, rows = update_ledger(
                app_dir,
                reports_dir,
                "2026-08-17",
            )

            self.assertTrue(baseline)
            self.assertEqual(rows, [])
            self.assertEqual(self._read_csv(daily), [])
            ledger = self._read_csv(history)
            self.assertEqual({row["job_id"] for row in ledger}, {"A", "B"})
            self.assertEqual(
                {row["tracking_kind"] for row in ledger},
                {"baseline_existing"},
            )

            self._write_jobs(
                app_dir,
                [
                    self._job("A"),
                    self._job("B", source="VONNE"),
                    self._job("C", source="Teaching Vacancies"),
                ],
            )
            _, daily, baseline, rows = update_ledger(
                app_dir,
                reports_dir,
                "2026-08-18",
            )

            self.assertFalse(baseline)
            self.assertEqual([row["job_id"] for row in rows], ["C"])
            new_rows = self._read_csv(daily)
            self.assertEqual(new_rows[0]["source"], "Teaching Vacancies")
            self.assertEqual(
                new_rows[0]["ontap_url"],
                "https://www.ontapjobsearch.com/jobs/C",
            )

    def test_same_day_runs_accumulate_and_reappearing_job_is_not_new_again(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            app_dir = root / "app"
            reports_dir = root / "reports"

            self._write_jobs(app_dir, [self._job("A")])
            update_ledger(app_dir, reports_dir, "2026-08-17")

            self._write_jobs(app_dir, [self._job("A"), self._job("B")])
            update_ledger(app_dir, reports_dir, "2026-08-18")
            self._write_jobs(
                app_dir,
                [
                    self._job("A"),
                    self._job("B"),
                    self._job("C", source="NEJobs"),
                ],
            )
            _, daily, _, rows = update_ledger(
                app_dir,
                reports_dir,
                "2026-08-18",
            )

            self.assertEqual({row["job_id"] for row in rows}, {"B", "C"})
            self.assertEqual(
                {row["job_id"] for row in self._read_csv(daily)},
                {"B", "C"},
            )

            self._write_jobs(
                app_dir,
                [self._job("A"), self._job("C", source="NEJobs")],
            )
            update_ledger(app_dir, reports_dir, "2026-08-19")
            self._write_jobs(
                app_dir,
                [
                    self._job("A"),
                    self._job("B"),
                    self._job("C", source="NEJobs"),
                ],
            )
            _, daily, _, rows = update_ledger(
                app_dir,
                reports_dir,
                "2026-08-20",
            )

            self.assertEqual(rows, [])
            self.assertEqual(self._read_csv(daily), [])


if __name__ == "__main__":
    unittest.main()
