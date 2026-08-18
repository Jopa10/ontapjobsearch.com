import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "pipeline" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def load_script(module_name: str):
    script = SCRIPTS_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, script)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


geo = load_script("jobg8_geo_resolver")


class StructuredJobG8GeographyTests(unittest.TestCase):
    def setUp(self):
        self.area_col = "/Job/Area"
        self.location_col = "/Job/Location"
        self.description_col = "/Job/Description"
        self.postcode_col = "/Job/PostalCode"
        self.area_lookup = {
            "manchester": "Greater Manchester - Manchester & Salford",
            "stockport": "Greater Manchester - South",
            "salford": "Greater Manchester - Manchester & Salford",
        }
        self.location_lookup = dict(self.area_lookup)
        self.postcodes = geo.load_postcode_overrides(
            ROOT / "pipeline" / "geo" / "postcode_location_overrides.csv"
        )

    def resolve(self, row):
        return geo.resolve_job_geography(
            row,
            area_column=self.area_col,
            location_column=self.location_col,
            description_column=self.description_col,
            area_lookup=self.area_lookup,
            location_lookup=self.location_lookup,
            postcode_overrides=self.postcodes,
            area_is_unusable=lambda value: str(value or "").strip().lower()
            in {"", "not specified", "unknown", "city"},
            postal_code_column=self.postcode_col,
        )

    def test_structured_postcode_beats_broad_manchester_fields(self):
        result = self.resolve(
            {
                self.area_col: "Manchester",
                self.location_col: "Manchester",
                self.postcode_col: "SK3 0XX",
                self.description_col: "Administrator role in Greater Manchester.",
            }
        )
        self.assertEqual("Greater Manchester - South", result.region)
        self.assertEqual("Stockport", result.town)
        self.assertEqual("structured_postcode", result.source)
        self.assertEqual("SK3", result.postcode_district)

    def test_precise_location_beats_broader_area(self):
        result = self.resolve(
            {
                self.area_col: "Manchester",
                self.location_col: "Stockport",
                self.postcode_col: "",
                self.description_col: "Office administrator.",
            }
        )
        self.assertEqual("Greater Manchester - South", result.region)
        self.assertEqual("Stockport", result.town)
        self.assertEqual("precise_location_override", result.source)

    def test_broad_location_does_not_override_specific_area(self):
        result = self.resolve(
            {
                self.area_col: "Stockport",
                self.location_col: "Manchester",
                self.postcode_col: "",
                self.description_col: "Office administrator.",
            }
        )
        self.assertEqual("Greater Manchester - South", result.region)
        self.assertEqual("Stockport", result.town)
        self.assertEqual("area", result.source)

    def test_area_remains_fallback_when_location_missing(self):
        result = self.resolve(
            {
                self.area_col: "Salford",
                self.location_col: "",
                self.postcode_col: "",
                self.description_col: "Administrator.",
            }
        )
        self.assertEqual("Greater Manchester - Manchester & Salford", result.region)
        self.assertEqual("Salford", result.town)
        self.assertEqual("area", result.source)

    def test_description_postcode_is_last_resort(self):
        result = self.resolve(
            {
                self.area_col: "Not Specified",
                self.location_col: "Unmapped",
                self.postcode_col: "",
                self.description_col: "Location: Stockport SK4 2AA. Office administrator.",
            }
        )
        self.assertEqual("Greater Manchester - South", result.region)
        self.assertEqual("Stockport", result.town)
        self.assertEqual("description_postcode", result.source)

    def test_unmapped_structured_postcode_falls_through_safely(self):
        result = self.resolve(
            {
                self.area_col: "Salford",
                self.location_col: "Salford",
                self.postcode_col: "ZZ1 1ZZ",
                self.description_col: "Administrator.",
            }
        )
        self.assertEqual("Greater Manchester - Manchester & Salford", result.region)
        self.assertEqual("location_agrees_area", result.source)


if __name__ == "__main__":
    unittest.main()
