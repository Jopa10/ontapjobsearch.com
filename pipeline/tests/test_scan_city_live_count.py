from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from scripts.scan_city_opportunities import scan_repository  # noqa: E402


def job(job_id: str, location: str) -> dict[str, str]:
    return {
        "job_id": job_id,
        "title": f"Job {job_id}",
        "location": location,
        "region": "North East",
    }


class ActiveCityCountTests(unittest.TestCase):
    def test_active_city_reports_derived_live_json_count(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent_jobs = [
                job("1", "Newcastle"),
                job("2", "Newcastle upon Tyne"),
                job("3", "Gateshead"),
                job("4", "North Tyneside"),
                job("5", "Wideopen"),
                job("6", "Shiremoor"),
                job("7", "South Tyneside"),
                job("8", "North East (hybrid)"),
            ]

            region = root / "app" / "north-east"
            region.mkdir(parents=True)
            (region / "service-administrator-jobs.json").write_text(
                json.dumps(parent_jobs), encoding="utf-8"
            )
            route = region / "service-administrator-jobs"
            route.mkdir()
            (route / "page.tsx").write_text("export default function Page() {}", encoding="utf-8")

            city_route = root / "app" / "newcastle" / "service-administrator-jobs"
            city_route.mkdir(parents=True)
            (city_route / "page.tsx").write_text("export default function Page() {}", encoding="utf-8")

            derived = root / "app" / "_city-pages" / "newcastle"
            derived.mkdir(parents=True)
            (derived / "service-administrator-jobs.json").write_text(
                json.dumps(parent_jobs), encoding="utf-8"
            )

            register = root / "pipeline" / "city_pages"
            register.mkdir(parents=True)
            (register / "city-page-register.json").write_text(
                json.dumps(
                    [
                        {
                            "display_name": "Newcastle",
                            "parent_page": "app/north-east/service-administrator-jobs.json",
                            "route": "/newcastle/service-administrator-jobs",
                            "output_json": "app/_city-pages/newcastle/service-administrator-jobs.json",
                            "lifecycle_state": "active",
                            "include_rules": [
                                {"pattern": "newcastle"},
                                {"pattern": "gateshead"},
                                {"pattern": "north tyneside"},
                                {"pattern": "wideopen"},
                                {"pattern": "shiremoor"},
                            ],
                            "exclude_rules": [],
                        }
                    ]
                ),
                encoding="utf-8",
            )
            (register / "opportunity-market-register.json").write_text(
                json.dumps(
                    [
                        {
                            "region_key": "north-east",
                            "market_key": "newcastle",
                            "display_name": "Newcastle",
                            "include_patterns": ["newcastle"],
                        }
                    ]
                ),
                encoding="utf-8",
            )

            result = scan_repository(root)
            newcastle = next(
                row for row in result["opportunities"] if row["locality"] == "Newcastle"
            )

            self.assertEqual(newcastle["jobs"], 8)
            self.assertEqual(newcastle["status"], "LIVE")
            self.assertEqual(newcastle["basis"], "active-city-json")


if __name__ == "__main__":
    unittest.main()
