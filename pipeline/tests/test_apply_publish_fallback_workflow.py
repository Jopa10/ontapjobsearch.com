import unittest
import os
import subprocess
import tempfile
import json
from pathlib import Path


WORKFLOW = (
    Path(__file__).resolve().parents[2]
    / ".github/workflows/apply-publish-ontap-daily-review.yml"
)


class ApplyPublishFallbackWorkflowTest(unittest.TestCase):
    def test_external_source_failure_isolated_but_shared_failure_blocks_deploy(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        section = workflow.split("      - name: Dispatch current source publishers sequentially", 1)[1]
        script = section.split("        run: |\n", 1)[1].split("\n      - name:", 1)[0]
        script = "\n".join(line[10:] for line in script.splitlines())
        tail = 'shared_publish=false' + script.split('shared_publish=false', 1)[1]
        tail = tail.split('private_alert_started_epoch=', 1)[0] + '\nfi\n'
        for failure in ("nhs", "shared verified pages"):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                plan = {"publish": [{"source": "jobg8", "shared_publish_after": True}, {"source": "nhs", "shared_publish_after": True}]}
                (root / "plan.json").write_text(json.dumps(plan))
                (root / "publish-queue.tsv").write_text("jobg8\tjobg8.yml\tfalse\nnhs\tnhs.yml\tfalse\n")
                env = {**os.environ, "PLAN": str(root / "plan.json"), "RUNNER_TEMP": tmp, "GITHUB_STEP_SUMMARY": str(root / "summary"), "FAILED_SOURCE": failure}
                prefix = '''set -euo pipefail
LAST_RUN_ID=""
dispatch_one() {
  echo "DISPATCH:$1"
  LAST_RUN_ID=123
  [ "$1" != "$FAILED_SOURCE" ]
}
'''
                result = subprocess.run(["bash", "-c", prefix + tail], env=env, text=True, capture_output=True)
                if failure == "nhs":
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("DISPATCH:production deployment", result.stdout)
                    self.assertIn("NHS Jobs publisher failed", (root / "summary").read_text())
                else:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertNotIn("DISPATCH:production deployment", result.stdout)

    def run_waiter(self, responses):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        section = workflow.split("      - name: Dispatch current source publishers sequentially", 1)[1]
        script = section.split("        run: |\n", 1)[1].split("\n      - name:", 1)[0]
        script = "\n".join(line[10:] for line in script.splitlines())
        functions = script.split('python - "$PLAN" >', 1)[0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "responses").write_text(json.dumps(responses))
            fake = root / "gh"
            fake.write_text('''#!/usr/bin/env python3
import json, os, pathlib, sys
root = pathlib.Path(os.environ["FAKE_ROOT"])
rows = json.loads((root / "responses").read_text())
counter = root / "counter"
i = int(counter.read_text()) if counter.exists() else 0
counter.write_text(str(i + 1))
assert sys.argv[1:3] == ["api", "repos/owner/repo/actions/runs/123"]
row = rows[min(i, len(rows) - 1)]
if row is None:
    print("HTTP 500", file=sys.stderr)
    sys.exit(1)
print(row)
''')
            fake.chmod(0o755)
            env = {**os.environ, "PATH": f"{root}:{os.environ['PATH']}", "GH_REPO": "owner/repo", "FAKE_ROOT": str(root)}
            result = subprocess.run(
                ["bash", "-c", functions + '\nsleep() { :; }\nif wait_for_run_completion 123; then echo DEPLOY; else exit 1; fi'],
                env=env, text=True, capture_output=True, timeout=60,
            )
            calls = int((root / "counter").read_text())
            return result, calls

    def test_temporary_server_errors_recover_before_deployment(self):
        result, calls = self.run_waiter([None, "in_progress ", None, "completed success"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("DEPLOY", result.stdout)
        self.assertEqual(calls, 4)

    def test_real_failure_or_cancellation_never_deploys(self):
        for conclusion in ("failure", "cancelled", "timed_out", "skipped", ""):
            with self.subTest(conclusion=conclusion):
                result, calls = self.run_waiter([f"completed {conclusion}"])
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("DEPLOY", result.stdout)
                self.assertEqual(calls, 1)

    def test_persistent_status_outage_stops_without_deployment(self):
        result, calls = self.run_waiter([None])
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(calls, 12)
        self.assertNotIn("DEPLOY", result.stdout)

    def test_active_status_resets_consecutive_error_budget(self):
        result, calls = self.run_waiter([None] * 11 + ["queued "] + [None] * 11 + ["completed success"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, 24)

    def test_invalid_status_and_long_running_job_fail_closed(self):
        for responses, expected in ((["invalid"], 12), (["in_progress "], 720)):
            with self.subTest(responses=responses):
                result, calls = self.run_waiter(responses)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(calls, expected)
                self.assertNotIn("DEPLOY", result.stdout)

    def test_explicit_republish_uses_withhold_without_today_skip(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        section = workflow.split("      - name: Determine manual or automatic publication mode", 1)[1]
        script = section.split("        run: |\n", 1)[1].split("\n      - name:", 1)[0]
        script = "\n".join(line[10:] for line in script.splitlines())
        for approval, policy in (("PUBLISH_AVAILABLE", "withhold"), ("PUBLISH", "quarantine")):
            with self.subTest(approval=approval), tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / "output"
                env = {**os.environ, "EVENT_NAME": "workflow_dispatch", "APPROVAL": approval, "GITHUB_OUTPUT": str(output)}
                result = subprocess.run(["bash", "-c", script], env=env, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(output.read_text(), f"skip=false\nunresolved_policy={policy}\n")

    def test_external_fallback_uses_automatic_withhold_path(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn('APPROVAL" != "AUTOMATIC_FALLBACK', workflow)
        self.assertIn(
            'if [ "$EVENT_NAME" = "workflow_dispatch" ] && [ "$APPROVAL" = "PUBLISH" ]',
            workflow,
        )
        self.assertIn('echo "unresolved_policy=quarantine"', workflow)
        self.assertIn('echo "unresolved_policy=withhold"', workflow)

        manual_gate = workflow.index(
            'if [ "$EVENT_NAME" = "workflow_dispatch" ] && [ "$APPROVAL" = "PUBLISH" ]'
        )
        automatic_policy = workflow.index('echo "unresolved_policy=withhold"')
        self.assertLess(manual_gate, automatic_policy)


if __name__ == "__main__":
    unittest.main()
