from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pandas as pd

from pipeline.scripts import jobg8_module_2_live_slices as module2


class Module2SharedGeoAdapterTests(unittest.TestCase):
    def test_module2_uses_same_structured_geo_hierarchy_as_live_selector(self):
        geo_lookup = {
            "manchester": "Greater Manchester - Manchester & Salford",
            "salford": "Greater Manchester - Manchester & Salford",
            "stockport": "Greater Manchester - South",
            "oldham": "Greater Manchester - North",
        }
        location_lookup = {
            "manchester": "Greater Manchester - Manchester & Salford",
        }
        registers = {
            "admin_service": {
                "administrator": "HIGH_CONFIDENCE",
            }
        }
        rows = [
            {
                "/Job/DisplayReference": "postcode-south",
                "/Job/Position": "Administrator",
                "/Job/AdvertiserName": "Example Ltd",
                "/Job/Area": "Manchester",
                "/Job/Location": "Manchester",
                "/Job/PostalCode": "SK3 0XX",
                "/Job/Description": "Administrator role.",
            },
            {
                "/Job/DisplayReference": "description-north",
                "/Job/Position": "Administrator",
                "/Job/AdvertiserName": "Example Ltd",
                "/Job/Area": "Not Specified",
                "/Job/Location": "Manchester",
                "/Job/PostalCode": "",
                "/Job/Description": "<p><strong>Location:</strong> Oldham</p><p>Administrator role.</p>",
            },
            {
                "/Job/DisplayReference": "specific-area-south",
                "/Job/Position": "Administrator",
                "/Job/AdvertiserName": "Example Ltd",
                "/Job/Area": "Stockport",
                "/Job/Location": "Manchester",
                "/Job/PostalCode": "",
                "/Job/Description": "Administrator role.",
            },
            {
                "/Job/DisplayReference": "broad-manchester",
                "/Job/Position": "Administrator",
                "/Job/AdvertiserName": "Example Ltd",
                "/Job/Area": "Manchester",
                "/Job/Location": "Manchester",
                "/Job/PostalCode": "",
                "/Job/Description": "Administrator role in Manchester.",
            },
        ]

        with TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir)
            pd.DataFrame(rows).to_excel(input_dir / "2026-08-18.xlsx", index=False)
            expanded, dates, errors = module2.compiler.load_daily_feeds(
                input_dir,
                geo_lookup,
                location_lookup,
                registers,
            )

        self.assertEqual(["2026-08-18"], dates)
        self.assertEqual([], errors)
        by_id = expanded.set_index("job_id")
        self.assertEqual(
            "Greater Manchester - South",
            by_id.loc["postcode-south", "lookup_region"],
        )
        self.assertEqual("structured_postcode", by_id.loc["postcode-south", "geo_source"])
        self.assertEqual(
            "Greater Manchester - North",
            by_id.loc["description-north", "lookup_region"],
        )
        self.assertEqual("description_place", by_id.loc["description-north", "geo_source"])
        self.assertEqual(
            "Greater Manchester - South",
            by_id.loc["specific-area-south", "lookup_region"],
        )
        self.assertEqual(
            "Greater Manchester - Manchester & Salford",
            by_id.loc["broad-manchester", "lookup_region"],
        )


if __name__ == "__main__":
    unittest.main()
