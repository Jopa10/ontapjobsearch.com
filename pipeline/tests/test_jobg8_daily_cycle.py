import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from scripts import jobg8_daily_cycle as cycle


class JobG8DailyCycleTests(unittest.TestCase):
    def test_scheduled_runs_resolve_from_their_cron_expression(self):
        now = datetime(2026, 9, 1, 15, 0, tzinfo=ZoneInfo("Europe/London"))
        self.assertEqual(cycle.resolve_cycle("schedule", "30 7 * * *", "auto", now), "morning")
        self.assertEqual(cycle.resolve_cycle("schedule", "30 15 * * *", "auto", now), "evening")

    def test_external_request_uses_its_explicit_cycle(self):
        now = datetime(2026, 9, 1, 8, 35, tzinfo=ZoneInfo("Europe/London"))
        self.assertEqual(cycle.resolve_cycle("workflow_dispatch", "", "morning", now), "morning")
        self.assertEqual(cycle.resolve_cycle("workflow_dispatch", "", "evening", now), "evening")

    def test_completed_cycle_is_skipped_and_next_cycle_is_not(self):
        now = datetime(2026, 9, 1, 8, 35, tzinfo=ZoneInfo("Europe/London"))
        state = {"schema_version": 1, "completed_cycles": {}}
        cycle.mark_completed(state, "2026-09-01", "morning", "123", now)
        self.assertTrue(cycle.completed(state, "2026-09-01", "morning"))
        self.assertFalse(cycle.completed(state, "2026-09-01", "evening"))

    def test_marker_state_is_small_and_valid_json(self):
        state = {"schema_version": 1, "completed_cycles": {}}
        for day in ("2026-08-30", "2026-08-31", "2026-09-01"):
            cycle.mark_completed(
                state, day, "morning", "123", datetime.fromisoformat(f"{day}T08:35:00+01:00")
            )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            cycle.write_state(path, state)
            self.assertEqual(json.loads(path.read_text())["completed_cycles"].keys(), {"2026-08-31", "2026-09-01"})

