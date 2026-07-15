from __future__ import annotations

import unittest

from pipeline.scripts import service_admin_pipeline as core
from pipeline.scripts.service_admin_pipeline_education import anchor_sort_and_select


class GlobalManualRerunSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.original_anchor_towns = dict(core.ANCHOR_TOWNS)
        core.ANCHOR_TOWNS = {
            "Yorkshire - West": "Leeds",
            "London": "London",
        }

    def tearDown(self) -> None:
        core.ANCHOR_TOWNS = self.original_anchor_towns

    @staticmethod
    def item(job_id: str, region: str, *, manual_select: str = "") -> dict[str, object]:
        return {
            "job_id": job_id,
            "location": "Leeds" if region == "Yorkshire - West" else "London",
            "_manual_override": "",
            "_manual_select": manual_select,
            "_title_priority": core.CLASSIFICATION_PRIORITY["HIGH_CONFIDENCE"],
            "_title_classification": "HIGH_CONFIDENCE",
            "_excel_row": 2,
        }

    @staticmethod
    def report(job_id: str, region: str) -> dict[str, object]:
        return {
            "job_id": job_id,
            "region": region,
            "decision": "INCLUDED",
            "selection_status": "",
            "selection_scenario": "",
            "region_selection_message": "",
            "remaining_slots": "",
            "possible_selection_rank": "",
            "reason": "credible title",
        }

    def test_manual_rerun_does_not_auto_select_region_without_actions(self) -> None:
        outputs = {
            "Yorkshire - West": [self.item("west-selected", "Yorkshire - West", manual_select="1")],
            "London": [
                self.item("london-one", "London"),
                self.item("london-two", "London"),
            ],
        }
        rows = [
            self.report("west-selected", "Yorkshire - West"),
            self.report("london-one", "London"),
            self.report("london-two", "London"),
        ]

        selected, status = anchor_sort_and_select(outputs, rows, manual_rerun_mode=True)

        self.assertEqual(["west-selected"], [item["job_id"] for item in selected["Yorkshire - West"]])
        self.assertEqual([], selected["London"])
        self.assertEqual("SCENARIO_MANUAL_RERUN", status["London"]["scenario"])
        self.assertEqual(0, status["London"]["selected_count"])
        self.assertIn("Auto backfill disabled", status["London"]["message"])

        london_rows = [row for row in rows if row["region"] == "London"]
        self.assertTrue(all(row["selection_status"] == "POSSIBLE_SELECTION" for row in london_rows))
        self.assertTrue(all(row["decision"].startswith("POSS - LONDON") for row in london_rows))

    def test_automatic_run_keeps_existing_selection_behaviour(self) -> None:
        outputs = {"London": [self.item("london-one", "London")]}
        rows = [self.report("london-one", "London")]

        selected, _status = anchor_sort_and_select(outputs, rows, manual_rerun_mode=False)

        self.assertEqual(["london-one"], [item["job_id"] for item in selected["London"]])
        self.assertEqual("SELECTED", rows[0]["selection_status"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
