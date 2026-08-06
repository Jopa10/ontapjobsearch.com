import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "pipeline" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from slice_registry import load_slice_register, live_slices


class SliceRegistryTests(unittest.TestCase):
    def test_register_has_sixteen_live_and_four_candidate_rows(self):
        records = load_slice_register()
        self.assertEqual(len(records), 20)
        self.assertEqual(sum(row.status == "LIVE" for row in records), 16)
        self.assertEqual(sum(row.status == "CANDIDATE" for row in records), 4)
        self.assertEqual(sum(row.status == "RETIRED" for row in records), 0)

    def test_live_rows_include_expansion_slices(self):
        self.assertEqual(
            live_slices(),
            {
                ("Yorkshire - West", "admin_service"),
                ("Yorkshire - South", "admin_service"),
                ("Yorkshire - North", "admin_service"),
                ("North East", "admin_service"),
                ("London", "admin_service"),
                ("Hampshire", "admin_service"),
                ("Surrey", "admin_service"),
                ("Kent", "admin_service"),
                ("Sussex", "admin_service"),
                ("West Midlands - Coventry & Warwickshire", "admin_service"),
                ("Yorkshire - West", "support_worker"),
                ("Yorkshire - South", "support_worker"),
                ("North East", "support_worker"),
                ("Sussex", "support_worker"),
                ("Cumbria - South", "support_worker"),
                ("Hampshire", "support_worker"),
            },
        )

    def test_candidate_rows_only_include_unactivated_scaffolds(self):
        records = load_slice_register()
        candidates = {
            (row.region, row.category)
            for row in records
            if row.status == "CANDIDATE"
        }
        self.assertEqual(
            candidates,
            {
                ("Yorkshire - East", "admin_service"),
                ("Northern Ireland - East", "admin_service"),
                ("Lancashire - North", "support_worker"),
                ("Cumbria - North", "support_worker"),
            },
        )

    def test_invalid_status_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "register.csv"
            path.write_text(
                "region,category,status\nNorth East,admin_service,MAYBE\n",
                encoding="utf-8",
            )
            with self.assertRaises(SystemExit):
                load_slice_register(path)


if __name__ == "__main__":
    unittest.main()
