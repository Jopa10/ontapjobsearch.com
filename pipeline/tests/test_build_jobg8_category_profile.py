from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from scripts.build_jobg8_category_profile import build_profile


class JobG8CategoryProfileTests(unittest.TestCase):
    def test_builds_same_feed_supplier_and_published_counts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "jobg8.xlsx"
            coverage_path = root / "coverage.csv"
            output_dir = root / "published"
            output_path = root / "profile.csv"
            output_dir.mkdir()

            pd.DataFrame(
                [
                    {"/Job/DisplayReference": "1", "/Job/Classification": "Administration"},
                    {"/Job/DisplayReference": "2", "/Job/Classification": "Administration"},
                    {"/Job/DisplayReference": "3", "/Job/Classification": "Sales"},
                ]
            ).to_excel(input_path, index=False)
            coverage_path.write_text(
                "feed_date,region,family,selected_count\n2026-09-02,London,service_admin,2\n",
                encoding="utf-8",
            )
            (output_dir / "jobs.json").write_text(
                json.dumps(
                    [
                        {"job_id": "1", "source": "JobG8"},
                        {"job_id": "3", "source": "JobG8"},
                        {"job_id": "external", "source": "NHS Jobs"},
                    ]
                ),
                encoding="utf-8",
            )

            build_profile(input_path, output_path, coverage_path, [output_dir])
            with output_path.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual({row["feed_date"] for row in rows}, {"2026-09-02"})
        self.assertEqual({row["total_jobs"] for row in rows}, {"3"})
        self.assertEqual({row["published_jobg8_jobs"] for row in rows}, {"2"})
        by_category = {row["jobg8_category"]: row for row in rows}
        self.assertEqual(by_category["Administration"]["count"], "2")
        self.assertEqual(by_category["Administration"]["published_count"], "1")
        self.assertEqual(by_category["Sales"]["published_count"], "1")


if __name__ == "__main__":
    unittest.main()
