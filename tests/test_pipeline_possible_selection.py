import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "pipeline" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def load_script(module_name):
    script = ROOT / "pipeline" / "scripts" / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, script)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


support_worker = load_script("support_worker_pipeline")
service_admin = load_script("service_admin_pipeline")

support_worker.ANCHOR_TOWNS = {"Yorkshire - West": "Leeds"}
service_admin.ANCHOR_TOWNS = {"Yorkshire - West": "Leeds"}


def make_item(job_id, row, *, manual_select="", title_classification="ELASTIC_FIT", location="Bradford"):
    return {
        "job_id": job_id,
        "title": f"Credible Role {job_id}",
        "location": location,
        "_excel_row": row,
        "_title_priority": 2,
        "_title_classification": title_classification,
        "_manual_select": manual_select,
    }


def make_report_row(item, region="Yorkshire - West"):
    return {
        "job_id": item["job_id"],
        "title": item["title"],
        "region": region,
        "decision": "INCLUDED",
        "selection_status": "",
        "reason": "",
    }


class PossibleSelectionReviewTests(unittest.TestCase):
    def assert_all_possible_rows_are_preserved(self, module):
        selected = make_item("selected", 1, manual_select="1", location="Leeds")
        possibles = [make_item(f"possible-{idx}", idx + 2) for idx in range(8)]
        outputs = {"Yorkshire - West": [selected, *possibles]}
        report_rows = [make_report_row(item) for item in outputs["Yorkshire - West"]]

        final_outputs, region_status = module.anchor_sort_and_select(
            outputs,
            report_rows,
            manual_rerun_mode=True,
        )

        self.assertEqual([row["job_id"] for row in final_outputs["Yorkshire - West"]], ["selected"])
        self.assertEqual(region_status["Yorkshire - West"]["selected_count"], 1)

        possible_rows = [row for row in report_rows if row.get("selection_status") == "POSSIBLE_SELECTION"]
        self.assertEqual([row["job_id"] for row in possible_rows], [item["job_id"] for item in possibles])
        self.assertEqual([row["possible_selection_rank"] for row in possible_rows], list(range(1, 9)))

    def test_support_worker_includes_all_credible_possible_rows_without_changing_selected_output(self):
        self.assert_all_possible_rows_are_preserved(support_worker)

    def test_service_admin_includes_all_credible_possible_rows_without_changing_selected_output(self):
        self.assert_all_possible_rows_are_preserved(service_admin)

    def test_support_worker_driver_specific_remains_hard_pass(self):
        classification, reason, priority, stability = support_worker.classify_title("Support Worker Driver Specific")
        self.assertEqual(classification, "HARD_PASS")
        self.assertEqual(priority, support_worker.CLASSIFICATION_PRIORITY["HARD_PASS"])
        self.assertIn("driver", reason.lower())


if __name__ == "__main__":
    unittest.main()
