import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "pipeline" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def load_script(module_name):
    script = SCRIPTS_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, script)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


service_admin = load_script("service_admin_pipeline")
support_worker = load_script("support_worker_pipeline")

NORTH_EAST_PUBLISH_CLUSTERS = [
    "North East - Tyneside, Wearside & Northumberland",
    "North East - County Durham & Darlington/Hartlepool",
]
TEES_VALLEY = "North East - Tees Valley"


class NorthEastPublishScopeTests(unittest.TestCase):
    def test_service_admin_combines_only_the_two_approved_clusters(self):
        self.assertEqual(
            list(service_admin.COMBINED_OUTPUT_REGION_MAP),
            NORTH_EAST_PUBLISH_CLUSTERS,
        )
        self.assertEqual(
            service_admin.REGION_MAP["north east - tees valley"],
            TEES_VALLEY,
        )
        self.assertNotIn(TEES_VALLEY, service_admin.OUTPUT_FILES)

    def test_support_worker_combines_only_the_two_approved_clusters(self):
        self.assertEqual(
            support_worker.NORTH_EAST_DETAILED_REGIONS,
            NORTH_EAST_PUBLISH_CLUSTERS,
        )
        self.assertEqual(
            support_worker.REGION_MAP["north east - tees valley"],
            TEES_VALLEY,
        )
        self.assertEqual(
            support_worker.publish_region_for(TEES_VALLEY),
            TEES_VALLEY,
        )
        self.assertNotIn(TEES_VALLEY, support_worker.OUTPUT_FILES)


if __name__ == "__main__":
    unittest.main()
