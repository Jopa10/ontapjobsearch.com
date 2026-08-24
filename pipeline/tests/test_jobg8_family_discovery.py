from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from pipeline.scripts import jobg8_family_discovery


class FamilyDiscoveryTests(unittest.TestCase):
    def test_unknown_area_uses_safe_location_fallback(self) -> None:
        area_lookup = {"aylesford": "Kent"}
        fallback = {"kent": "Kent", "essex": "Essex"}

        self.assertEqual(
            jobg8_family_discovery.ontap_region("Ditton", "Kent", area_lookup, fallback),
            "Kent",
        )
        self.assertEqual(
            jobg8_family_discovery.ontap_region("Hutton", "Essex", area_lookup, fallback),
            "Essex",
        )
        self.assertEqual(
            jobg8_family_discovery.ontap_region("Ditton", "Cheshire", area_lookup, fallback),
            "Other / Unknown",
        )

    def test_known_area_remains_authoritative_over_location_fallback(self) -> None:
        self.assertEqual(
            jobg8_family_discovery.ontap_region(
                "Aylesford",
                "Essex",
                {"aylesford": "Kent"},
                {"essex": "Essex"},
            ),
            "Kent",
        )

    def test_description_day_rate_is_annualised(self) -> None:
        self.assertEqual(
            jobg8_family_discovery.description_annualised_max("Contract: £300-£400 per day"),
            104000.0,
        )
        self.assertEqual(
            jobg8_family_discovery.description_annualised_max("Salary: £50,000 per year"),
            50000.0,
        )

    def test_borderline_override_precedes_likely_title_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_dir = root / "input"
            output_dir = root / "output"
            input_dir.mkdir()

            pd.DataFrame(
                [
                    {
                        "/Job/Position": "Sales & Marketing Coordinator",
                        "/Job/Description": "Runs marketing campaigns and social media activity.",
                        "/Job/Area": "London",
                        "/Job/Location": "London",
                        "/Job/DisplayReference": "mixed-1",
                        "/Job/SalaryMinimum": "30000",
                        "/Job/SalaryMaximum": "35000",
                        "/Job/SalaryPeriod": "Annual",
                        "/Job/Classification": "Sales & Marketing",
                    }
                ]
            ).to_excel(input_dir / "2026-08-24.xlsx", index=False)

            geo_path = root / "geo.xlsx"
            pd.DataFrame([{"Area": "London", "Cluster": "London"}]).to_excel(geo_path, index=False)
            markets_path = root / "markets.json"
            markets_path.write_text(
                json.dumps({"region_count": 1, "regions": {"London": {}}, "detail_rollups": {}}),
                encoding="utf-8",
            )
            config_path = root / "family.json"
            config_path.write_text(
                json.dumps(
                    {
                        "family_key": "marketing",
                        "display_name": "Marketing",
                        "broad_title_patterns": [r"\bmarketing\b"],
                        "likely_in_title_patterns": [r"\bmarketing\s+coordinator\b"],
                        "borderline_override_title_patterns": [r"\bsales\s+&\s+marketing\b"],
                        "viability_floor": 1,
                    }
                ),
                encoding="utf-8",
            )

            argv = [
                "jobg8_family_discovery.py",
                "--input-dir",
                str(input_dir),
                "--config",
                str(config_path),
                "--output-dir",
                str(output_dir),
                "--geo-lookup",
                str(geo_path),
                "--assessable-regions",
                str(markets_path),
            ]
            with patch.object(sys, "argv", argv):
                self.assertEqual(jobg8_family_discovery.main(), 0)

            result = pd.read_csv(
                output_dir / "jobg8-marketing-discovery-current.csv", dtype=str
            ).fillna("")
            self.assertEqual(result.loc[0, "provisional_decision"], "BORDERLINE")
            self.assertEqual(
                result.loc[0, "provisional_reason"],
                "mixed/ambiguous title requires advert-context review",
            )


if __name__ == "__main__":
    unittest.main()
