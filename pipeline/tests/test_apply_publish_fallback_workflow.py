import unittest
from pathlib import Path


WORKFLOW = (
    Path(__file__).resolve().parents[2]
    / ".github/workflows/apply-publish-ontap-daily-review.yml"
)


class ApplyPublishFallbackWorkflowTest(unittest.TestCase):
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
