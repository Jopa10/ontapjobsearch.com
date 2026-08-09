from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from scripts.scan_city_opportunities import (
    DEFAULT_THRESHOLD,
    discover_published_slices,
    scan_repository,
    simple_locality,
)


def job(job_id: str, location: str, region: str = "Yorkshire - South") -> dict[str, str]:
    return {
        "job_id": job_id,
        "title": f"Job {job_id}",
        "location": location,
        "region": region,
    }


class CityOpportunityScanTests(unittest.TestCase):
    def make_slice(
        self,
        root: Path,
        region_key: str,
        slice_key: str,
        jobs: list[dict[str, str]],
    ) -> None:
        region = root / "app" / region_key
        region.mkdir(parents=True, exist_ok=True)
        (region / f"{slice_key}.json").write_text(json.dumps(jobs), encoding="utf-8")
        route = region / slice_key
        route.mkdir(parents=True, exist_ok=True)
        (route / "page.tsx").write_text("export default function Page() {}", encoding="utf-8")

    def test_default_threshold_is_historical_six(self) -> None:
        self.assertEqual(DEFAULT_THRESHOLD, 6)

    def test_discovers_only_json_with_matching_public_route(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_slice(
                root,
                "south-yorkshire",
                "service-administrator-jobs",
                [job("1", "Sheffield")],
            )
            orphan = root / "app" / "south-yorkshire" / "orphan.json"
            orphan.write_text("[]", encoding="utf-8")
            hidden = root / "app" / "_city-pages"
            hidden.mkdir(parents=True)
            (hidden / "newcastle.json").write_text("[]", encoding="utf-8")

            slices = discover_published_slices(root)
            self.assertEqual(
                [(item.region_key, item.slice_key) for item in slices],
                [("south-yorkshire", "service-administrator-jobs")],
            )

    def test_sheffield_six_qualifies_and_five_is_near(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            jobs = [job(str(i), "Sheffield") for i in range(1, 7)]
            jobs.extend(job(str(i), "Rotherham") for i in range(7, 12))
            self.make_slice(root, "south-yorkshire", "service-administrator-jobs", jobs)

            result = scan_repository(root)
            rows = {
                (row["locality"], row["status"], row["jobs"])
                for row in result["opportunities"]
            }
            self.assertIn(("Sheffield", "QUALIFIES", 6), rows)
            self.assertIn(("Rotherham", "NEAR", 5), rows)

    def test_scans_multiple_regions_and_categories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_slice(
                root,
                "hampshire",
                "service-administrator-jobs",
                [job(str(i), "Southampton", "Hampshire") for i in range(6)],
            )
            self.make_slice(
                root,
                "west-yorkshire",
                "support-worker",
                [job(f"w{i}", "Leeds", "Yorkshire - West") for i in range(6)],
            )

            result = scan_repository(root)
            qualifying = {
                (row["region"], row["slice"], row["locality"])
                for row in result["opportunities"]
                if row["status"] == "QUALIFIES"
            }
            self.assertIn(
                ("hampshire", "service-administrator-jobs", "Southampton"),
                qualifying,
            )
            self.assertIn(("west-yorkshire", "support-worker", "Leeds"), qualifying)
            self.assertEqual(result["published_slices_scanned"], 2)
            self.assertEqual(result["jobs_scanned"], 12)

    def test_configured_catchment_reuses_newcastle_rules_and_suppresses_duplicate_exact_row(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            jobs = [
                job("1", "Newcastle upon Tyne", "North East"),
                job("2", "Newcastle", "North East"),
                job("3", "Gateshead", "North East"),
                job("4", "North Tyneside", "North East"),
                job("5", "Wideopen", "North East"),
                job("6", "Shiremoor", "North East"),
                job("7", "Bedlington", "North East"),
            ]
            self.make_slice(root, "north-east", "service-administrator-jobs", jobs)
            route = root / "app" / "newcastle" / "service-administrator-jobs"
            route.mkdir(parents=True)
            (route / "page.tsx").write_text("export default function Page() {}", encoding="utf-8")
            register = root / "pipeline" / "city_pages"
            register.mkdir(parents=True)
            (register / "city-page-register.json").write_text(
                json.dumps(
                    [
                        {
                            "display_name": "Newcastle",
                            "parent_page": "app/north-east/service-administrator-jobs.json",
                            "route": "/newcastle/service-administrator-jobs",
                            "include_rules": [
                                {"pattern": "newcastle"},
                                {"pattern": "gateshead"},
                                {"pattern": "north tyneside"},
                                {"pattern": "wideopen"},
                                {"pattern": "shiremoor"},
                            ],
                            "exclude_rules": [{"pattern": "bedlington"}],
                        }
                    ]
                ),
                encoding="utf-8",
            )

            result = scan_repository(root)
            rows = result["opportunities"]
            newcastle = [row for row in rows if row["locality"] == "Newcastle"]
            self.assertEqual(len(newcastle), 1)
            self.assertEqual(newcastle[0]["jobs"], 6)
            self.assertEqual(newcastle[0]["status"], "LIVE")
            self.assertEqual(newcastle[0]["basis"], "configured-catchment")
            self.assertFalse(
                any(
                    row["basis"] == "exact-location"
                    and row["locality"]
                    in {"Newcastle", "Newcastle upon Tyne", "Gateshead"}
                    for row in rows
                )
            )

    def test_scanner_is_read_only_for_live_page_data(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            jobs = [job(str(i), "Coventry", "West Midlands") for i in range(5)]
            self.make_slice(
                root,
                "coventry-warwickshire",
                "service-administrator-jobs",
                jobs,
            )
            live_json = (
                root
                / "app"
                / "coventry-warwickshire"
                / "service-administrator-jobs.json"
            )
            before = live_json.read_bytes()

            scan_repository(root)

            self.assertEqual(live_json.read_bytes(), before)

    def test_simple_locality_is_conservative(self) -> None:
        self.assertEqual(
            simple_locality("Southampton, Hampshire", "Hampshire"),
            "Southampton",
        )
        self.assertEqual(
            simple_locality("Coventry (hybrid working)", "West Midlands"),
            "Coventry",
        )
        self.assertEqual(simple_locality("Town Hall, Darlington", "North East"), "")
        self.assertEqual(
            simple_locality(
                "St Benet Biscop Catholic Academy, Bedlington",
                "North East",
            ),
            "",
        )
        self.assertEqual(simple_locality("North East", "North East"), "")


if __name__ == "__main__":
    unittest.main()
