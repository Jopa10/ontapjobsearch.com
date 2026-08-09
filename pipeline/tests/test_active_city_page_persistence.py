from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from scripts.maintain_active_city_pages import maintain_active_config


def config_raw() -> dict[str, object]:
    return {
        "city_key": "test-city-admin",
        "display_name": "Test City",
        "category_label": "admin jobs",
        "parent_page": "app/test-region/service-administrator-jobs.json",
        "review_csv": "pipeline/reviews/city-pages/test-city.csv",
        "summary_md": "pipeline/reviews/city-pages/test-city.md",
        "output_json": "app/_city-pages/test-city/service-administrator-jobs.json",
        "route": "/test-city/service-administrator-jobs",
        "minimum_live_jobs": 6,
        "launch_minimum_live_jobs": 6,
        "lifecycle_state": "active",
        "mode": "publish",
        "include_rules": [{"pattern": "test city", "reason": "Test City stated"}],
        "review_rules": [],
        "exclude_rules": [],
        "fallback_decision": "review",
        "fallback_reason": "No rule matched",
    }


def job(job_id: str, location: str = "Test City") -> dict[str, str]:
    return {
        "job_id": job_id,
        "title": f"Job {job_id}",
        "company": "Employer",
        "location": location,
        "source": "Test",
    }


class ActiveCityPagePersistenceTests(unittest.TestCase):
    def test_active_page_keeps_current_jobs_below_launch_threshold(self) -> None:
        raw = config_raw()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent = root / str(raw["parent_page"])
            parent.parent.mkdir(parents=True)
            parent.write_text(json.dumps([job("1"), job("2")]), encoding="utf-8")

            result = maintain_active_config(raw, root)

            output = root / str(raw["output_json"])
            published = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result["jobs"], 2)
            self.assertEqual([item["job_id"] for item in published], ["1", "2"])

    def test_active_page_writes_empty_array_at_zero_instead_of_disappearing(self) -> None:
        raw = config_raw()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent = root / str(raw["parent_page"])
            parent.parent.mkdir(parents=True)
            parent.write_text("[]", encoding="utf-8")

            result = maintain_active_config(raw, root)

            output = root / str(raw["output_json"])
            self.assertTrue(output.exists())
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), [])
            self.assertEqual(result["jobs"], 0)


if __name__ == "__main__":
    unittest.main()
