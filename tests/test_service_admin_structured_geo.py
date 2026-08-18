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
            "city": "London",
            "not specified": "unknown",
            "london": "London",
            "manchester": "Greater Manchester - Manchester & Salford",
            "salford": "Greater Manchester - Manchester & Salford",
            "stockport": "Greater Manchester - South",
            "cheadle": "Greater Manchester - South",
            "sale": "Greater Manchester - South",
            "ashton-under-lyne": "Greater Manchester - South",
            "tameside": "Greater Manchester - South",
            "bury": "Greater Manchester - North",
            "heywood": "Greater Manchester - North",
            "middleton": "Greater Manchester - North",
            "oldham": "Greater Manchester - North",
            "bolton": "Greater Manchester - Wigan & Bolton",
            "trafford": "Greater Manchester - South",
        }
        self.location_lookup = {
            "manchester": "Greater Manchester - Manchester & Salford",
            "london": "London",
        }
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

    def test_jobg8_outcode_sector_keeps_outcode(self):
        self.assertEqual("M21", geo.normalize_postcode_district("M21 0"))
        self.assertEqual("M3", geo.normalize_postcode_district("M3 5"))
        self.assertEqual("M35", geo.normalize_postcode_district("M35"))

    def test_precise_location_uses_authoritative_area_lookup(self):
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
        self.assertEqual("precise_location", result.source)

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

    def test_city_area_never_overrides_manchester_location(self):
        result = self.resolve(
            {
                self.area_col: "City",
                self.location_col: "Manchester",
                self.postcode_col: "M1",
                self.description_col: "Helpdesk role in Manchester city centre.",
            }
        )
        self.assertEqual("Greater Manchester - Manchester & Salford", result.region)
        self.assertEqual("Manchester", result.town)
        self.assertEqual("location", result.source)

    def test_unknown_cluster_never_overrides_london_location(self):
        result = self.resolve(
            {
                self.area_col: "Not Specified",
                self.location_col: "London",
                self.postcode_col: "",
                self.description_col: "Administrator with a London employer.",
            }
        )
        self.assertEqual("London", result.region)
        self.assertEqual("London", result.town)
        self.assertEqual("location", result.source)

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

    def test_description_based_in_stockport_overrides_generic_manchester(self):
        result = self.resolve(
            {
                self.area_col: "Not Specified",
                self.location_col: "Manchester",
                self.postcode_col: "",
                self.description_col: "Office Administrator. This is a role with a growing business based in the Stockport area.",
            }
        )
        self.assertEqual("Greater Manchester - South", result.region)
        self.assertEqual("Stockport", result.town)
        self.assertEqual("description_place", result.source)

    def test_description_location_cheadle_routes_south(self):
        result = self.resolve(
            {
                self.area_col: "Not Specified",
                self.location_col: "Manchester",
                self.postcode_col: "",
                self.description_col: "Receptionist. Location: Cheadle. Immediate start.",
            }
        )
        self.assertEqual("Greater Manchester - South", result.region)
        self.assertEqual("Cheadle", result.town)
        self.assertEqual("description_place", result.source)

    def test_html_wrapped_location_label_routes_oldham(self):
        result = self.resolve(
            {
                self.area_col: "Not Specified",
                self.location_col: "Manchester",
                self.postcode_col: "",
                self.description_col: "<p><strong>Job Title:</strong> Administrator</p><p><strong>Location:</strong> <strong>Oldham</strong></p>",
            }
        )
        self.assertEqual("Greater Manchester - North", result.region)
        self.assertEqual("Oldham", result.town)
        self.assertEqual("description_place", result.source)

    def test_html_wrapped_team_location_routes_bury(self):
        result = self.resolve(
            {
                self.area_col: "Not Specified",
                self.location_col: "Manchester",
                self.postcode_col: "",
                self.description_col: "<p>Could you be our missing piece?</p><p>Join our support <strong>team in Bury</strong> as a Service Coordinator.</p>",
            }
        )
        self.assertEqual("Greater Manchester - North", result.region)
        self.assertEqual("Bury", result.town)
        self.assertEqual("description_place", result.source)

    def test_description_place_can_route_other_greater_manchester_slices(self):
        cases = [
            ("Data Entry Clerk Heywood, OL10 1AA. Long-term work.", "Greater Manchester - North", "Heywood"),
            ("Service Coordinator. Join our team in Bury as a Service Coordinator.", "Greater Manchester - North", "Bury"),
            ("Administrator, Bolton BL6 6AA. Six month contract.", "Greater Manchester - Wigan & Bolton", "Bolton"),
            ("Administrator - Ashton Under Lyne (Tameside). Part time.", "Greater Manchester - South", "Ashton Under Lyne"),
            ("Document Controller. Join us in Sale, Cheshire with flexible start times.", "Greater Manchester - South", "Sale"),
        ]
        for description, expected_region, expected_town in cases:
            with self.subTest(description=description):
                result = self.resolve(
                    {
                        self.area_col: "Not Specified",
                        self.location_col: "Manchester",
                        self.postcode_col: "",
                        self.description_col: description,
                    }
                )
                self.assertEqual(expected_region, result.region)
                self.assertEqual(expected_town, result.town)
                self.assertEqual("description_place", result.source)

    def test_incidental_trafford_park_branch_does_not_reroute(self):
        result = self.resolve(
            {
                self.area_col: "Not Specified",
                self.location_col: "Manchester",
                self.postcode_col: "",
                self.description_col: "Data Entry Clerk Heywood. For more information call our Trafford Park branch on 0161 000 0000.",
            }
        )
        self.assertEqual("Greater Manchester - Manchester & Salford", result.region)
        self.assertEqual("location", result.source)

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
