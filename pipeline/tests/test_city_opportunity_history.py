from __future__ import annotations

import sys
import unittest
from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINE_ROOT))

from scripts.update_city_opportunity_history import (
    REQUIRED_QUALIFYING_RUNS,
    WINDOW_RUNS,
    append_snapshot,
    lifecycle_status,
    recent_counts,
)


class CityOpportunityHistoryTests(unittest.TestCase):
    def test_ready_requires_three_qualifying_runs_and_current_six(self) -> None:
        self.assertEqual(REQUIRED_QUALIFYING_RUNS, 3)
        self.assertEqual(WINDOW_RUNS, 7)
        self.assertEqual(
            lifecycle_status(current=7, qualifying_runs=3, active=False),
            "READY FOR APPROVAL",
        )
        self.assertEqual(
            lifecycle_status(current=7, qualifying_runs=2, active=False),
            "QUALIFIES 2/3",
        )

    def test_active_page_stays_live_even_at_zero(self) -> None:
        self.assertEqual(
            lifecycle_status(current=0, qualifying_runs=0, active=True),
            "LIVE",
        )

    def test_history_keeps_only_last_seven_runs(self) -> None:
        history = {"candidates": {}, "snapshots": []}
        key = "region|slice|exact-location|city"
        for index in range(1, 10):
            append_snapshot(
                history,
                {
                    key: {
                        "region": "region",
                        "slice": "slice",
                        "locality": "City",
                        "basis": "exact-location",
                        "jobs": index,
                        "route": "",
                        "active": False,
                    }
                },
                run_id=str(index),
                run_at=f"2026-08-{index:02d}T12:00:00Z",
            )
        self.assertEqual(recent_counts(history, key), [3, 4, 5, 6, 7, 8, 9])

    def test_rerun_same_pipeline_run_replaces_snapshot(self) -> None:
        history = {"candidates": {}, "snapshots": []}
        key = "region|slice|exact-location|city"
        base = {
            key: {
                "region": "region",
                "slice": "slice",
                "locality": "City",
                "basis": "exact-location",
                "jobs": 6,
                "route": "",
                "active": False,
            }
        }
        append_snapshot(history, base, run_id="123", run_at="one")
        base[key]["jobs"] = 8
        append_snapshot(history, base, run_id="123", run_at="two")
        self.assertEqual(len(history["snapshots"]), 1)
        self.assertEqual(recent_counts(history, key), [8])


if __name__ == "__main__":
    unittest.main()
