from pathlib import Path
import unittest


class GoogleIndexingTriggerTests(unittest.TestCase):
    def test_live_inventory_changes_trigger_indexing_cleanup(self) -> None:
        workflow = (
            Path(__file__).parents[2] / ".github/workflows/google-indexing-api.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("push:", workflow)
        self.assertIn("app/**/*.json", workflow)
        self.assertRegex(workflow, r"cron: ['\"]30 19 \* \* \*['\"]")
        self.assertIn("URL_DELETED", (
            Path(__file__).parents[2] / "scripts/google-indexing-submit.ts"
        ).read_text(encoding="utf-8"))

    def test_shared_daily_quota_and_priority_configuration(self) -> None:
        root = Path(__file__).parents[2]
        workflow = (root / ".github/workflows/google-indexing-api.yml").read_text(
            encoding="utf-8"
        )
        script = (root / "scripts/google-indexing-submit.ts").read_text(
            encoding="utf-8"
        )

        self.assertRegex(workflow, r"GOOGLE_INDEXING_DAILY_QUOTA: ['\"]200['\"]")
        self.assertRegex(workflow, r"GOOGLE_INDEXING_NEW_JOBG8_RESERVE: ['\"]160['\"]")
        self.assertRegex(workflow, r"GOOGLE_INDEXING_NEW_NON_JOBG8_RESERVE: ['\"]20['\"]")
        self.assertRegex(workflow, r"GOOGLE_INDEXING_DELETION_RESERVE: ['\"]20['\"]")
        self.assertIn("America/Los_Angeles", (root / "lib/google-indexing-policy.ts").read_text(encoding="utf-8"))
        self.assertIn("legacyDeletionsNeutralised", script)
        self.assertNotIn("notifications.slice(0", script)


if __name__ == "__main__":
    unittest.main()
