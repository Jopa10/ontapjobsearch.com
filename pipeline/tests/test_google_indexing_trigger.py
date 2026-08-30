from pathlib import Path
import unittest


class GoogleIndexingTriggerTests(unittest.TestCase):
    def test_live_inventory_changes_trigger_indexing_cleanup(self) -> None:
        workflow = (
            Path(__file__).parents[2] / ".github/workflows/google-indexing-api.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("push:", workflow)
        self.assertIn("app/**/*.json", workflow)
        self.assertIn('cron: "30 19 * * *"', workflow)
        self.assertIn("URL_DELETED", (
            Path(__file__).parents[2] / "scripts/google-indexing-submit.ts"
        ).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
