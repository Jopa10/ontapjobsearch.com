import sys
import unittest
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1] / "pipeline"
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from scripts import publish_verified_pages_sussex as publisher
from scripts.slice_registry import live_slices


class SussexAdminLaunchTests(unittest.TestCase):
    def test_sussex_admin_is_live_and_publishable(self):
        slice_key = ("Sussex", "admin_service")
        self.assertIn(slice_key, live_slices())

        mappings = {
            (mapping.region, mapping.category): (mapping.source, mapping.destination)
            for mapping in publisher.core.MAPPINGS
        }
        self.assertEqual(
            mappings[slice_key],
            (
                Path("pipeline/output-admin-service/sussex-admin-service.json"),
                Path("app/sussex/service-administrator-jobs.json"),
            ),
        )


if __name__ == "__main__":
    unittest.main()
