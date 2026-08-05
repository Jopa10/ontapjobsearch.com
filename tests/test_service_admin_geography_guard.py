import importlib.util
import sys
import unittest
from pathlib import Path

import pandas as pd

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


service_admin = load_script("service_admin_pipeline")


class ServiceAdminGeographyGuardTests(unittest.TestCase):
    def test_generic_city_area_is_treated_as_ambiguous(self):
        self.assertTrue(service_admin.area_is_unusable("City"))
        self.assertTrue(service_admin.area_is_unusable(" city "))
        self.assertFalse(service_admin.area_is_unusable("London"))

    def test_northern_ireland_evidence_is_removed_from_london_outputs(self):
        job_id_col = service_admin.COL["job_id"]
        title_col = service_admin.COL["title"]
        area_col = service_admin.COL["area"]
        location_col = service_admin.COL["location"]
        description_col = service_admin.COL["description"]

        job_df = pd.DataFrame(
            [
                {
                    job_id_col: "ni-1",
                    title_col: "Administrator (Part time 12-15 hours)",
                    area_col: "City",
                    location_col: "City",
                    description_col: "A Belfast-based role with hybrid working.",
                },
                {
                    job_id_col: "london-1",
                    title_col: "Office Administrator",
                    area_col: "London",
                    location_col: "London",
                    description_col: "Office administrator role in Central London.",
                },
            ]
        )

        def fake_original_process(*_args, **_kwargs):
            return (
                {
                    "London": [
                        {"job_id": "ni-1", "title": "Administrator"},
                        {"job_id": "london-1", "title": "Office Administrator"},
                    ]
                },
                [
                    {
                        "job_id": "ni-1",
                        "decision": "INCLUDED",
                        "selection_status": "SELECTED",
                        "region": "London",
                        "reason": "included",
                    },
                    {
                        "job_id": "london-1",
                        "decision": "INCLUDED",
                        "selection_status": "SELECTED",
                        "region": "London",
                        "reason": "included",
                    },
                ],
            )

        original_process = service_admin._ORIGINAL_PROCESS
        service_admin._ORIGINAL_PROCESS = fake_original_process
        try:
            outputs, report_rows = service_admin.process(
                job_df,
                {"city": "London", "london": "London"},
                {},
                {},
                set(),
                {},
            )
        finally:
            service_admin._ORIGINAL_PROCESS = original_process

        self.assertEqual(
            ["london-1"],
            [item["job_id"] for item in outputs["London"]],
        )

        blocked = next(row for row in report_rows if row["job_id"] == "ni-1")
        self.assertEqual("DROPPED", blocked["decision"])
        self.assertEqual("", blocked["selection_status"])
        self.assertEqual("geography_guard", blocked["geo_source"])
        self.assertIn("Northern Ireland", blocked["reason"])

        retained = next(row for row in report_rows if row["job_id"] == "london-1")
        self.assertEqual("INCLUDED", retained["decision"])

    def test_belfast_in_title_is_strong_location_evidence(self):
        row = {
            service_admin.COL["title"]: "Cemeteries Administrator - Belfast City Council",
            service_admin.COL["location"]: "City",
            service_admin.COL["description"]: "Administrative vacancy.",
        }
        self.assertTrue(service_admin.has_northern_ireland_location_evidence(row))


if __name__ == "__main__":
    unittest.main()
