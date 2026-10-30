import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from datetime import datetime
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
        self.assertEqual(cycle.resolve_cycle("workflow_dispatch", "", "changeover", now), "changeover")

    def test_completed_cycle_is_skipped_and_next_cycle_is_not(self):
        now = datetime(2026, 9, 1, 8, 35, tzinfo=ZoneInfo("Europe/London"))
        state = {"schema_version": 1, "completed_cycles": {}}
        cycle.mark_completed(state, "2026-09-01", "morning", "123", now)
        self.assertTrue(cycle.completed(state, "2026-09-01", "morning"))
        self.assertFalse(cycle.completed(state, "2026-09-01", "evening"))
        cycle.mark_completed(state, "2026-09-01", "changeover", "456", now)
        self.assertTrue(cycle.completed(state, "2026-09-01", "evening"))
        self.assertTrue(cycle.completed(state, "2026-09-01", "morning"))

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



    def test_manual_recoveries_require_reason_and_preserve_normal_cycles(self):
        script = Path(cycle.__file__).resolve()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            state = {"schema_version": 1, "completed_cycles": {}}
            now = datetime.fromisoformat("2026-09-01T10:00:00+01:00")
            cycle.mark_completed(state, "2026-09-01", "morning", "morning-run", now)
            cycle.mark_completed(state, "2026-09-01", "changeover", "changeover-run", now)
            cycle.write_state(path, state)
            base = [sys.executable, str(script), "check", "--event-name", "workflow_dispatch",
                    "--requested-cycle", "recovery", "--state", str(path),
                    "--now", now.isoformat(), "--actor", "owner"]
            missing = subprocess.run(base + ["--run-id", "1"], capture_output=True, text=True)
            self.assertNotEqual(missing.returncode, 0)
            for run_id in ("1", "2", "3"):
                args = base + ["--run-id", run_id, "--recovery-reason", "Generate new LIVE slices"]
                check = subprocess.run(args, capture_output=True, text=True, check=True)
                self.assertIn("should_run=true", check.stdout)
                args[2] = "mark"
                subprocess.run(args, capture_output=True, text=True, check=True)
                args[2] = "check"
                retry = subprocess.run(args, capture_output=True, text=True, check=True)
                self.assertIn("should_run=false", retry.stdout)
            saved = json.loads(path.read_text())
            self.assertEqual(saved["completed_cycles"], state["completed_cycles"])
            self.assertEqual(set(saved["recovery_runs"]), {"1", "2", "3"})
            self.assertEqual(saved["recovery_runs"]["3"]["actor"], "owner")
            self.assertEqual(saved["recovery_runs"]["3"]["reason"], "Generate new LIVE slices")
            self.assertTrue(cycle.completed(saved, "2026-09-01", "evening"))

    def test_recovery_cannot_be_requested_by_other_events(self):
        now = datetime.fromisoformat("2026-09-01T10:00:00+01:00")
        with self.assertRaises(ValueError):
            cycle.resolve_cycle("push", "", "recovery", now)
        self.assertEqual(cycle.resolve_cycle("schedule", "30 7 * * *", "recovery", now), "morning")
