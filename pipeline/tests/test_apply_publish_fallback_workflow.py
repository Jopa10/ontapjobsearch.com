import unittest
import os
import subprocess
import tempfile
from pathlib import Path


WORKFLOW = (
    Path(__file__).resolve().parents[2]
    / ".github/workflows/apply-publish-ontap-daily-review.yml"
)


class ApplyPublishFallbackWorkflowTest(unittest.TestCase):
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
