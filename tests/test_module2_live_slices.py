import sys
import unittest
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1] / "pipeline"
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from scripts import jobg8_module_2_live_slices as compiler


class Module2LiveSliceTests(unittest.TestCase):
    def test_sussex_admin_is_treated_as_live(self):
        self.assertIn("Sussex", compiler.compiler.LIVE_SLICE_GROUPS)
        self.assertIn(
            "admin_service",
            compiler.compiler.LIVE_SLICE_GROUPS["Sussex"]["categories"],
        )

    def test_current_south_east_admin_slices_are_live(self):
        for region in ("Hampshire", "Surrey", "Kent", "Sussex"):
            with self.subTest(region=region):
                self.assertIn(
                    "admin_service",
                    compiler.compiler.LIVE_SLICE_GROUPS[region]["categories"],
                )


if __name__ == "__main__":
    unittest.main()
