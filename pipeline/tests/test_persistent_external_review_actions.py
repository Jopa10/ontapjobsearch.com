from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from external_sources import persistent_external_review_actions as persistent


FIELDS = (
    "source_job_id",
    "title",
    "employer",
    "classification",
    "classification_reason",
    "manual_action",
    "final_decision",
)


def write_csv(path: Path, *, title: str = "Customer Service Advisor") -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerow(
            {
                "source_job_id": "123",
                "title": title,
                "employer": "Example Council",
                "classification": "POSS",
                "classification_reason": "manual review required",
                "manual_action": "",
                "final_decision": "POSS",
            }
        )


def write_summary(path: Path, *, action: str = "select") -> None:
    path.write_text(
        "\n".join(
            [
                "# Review",
                "",
                "review_date: 2026-08-17",
                "",
                "- Decisions are matched by `source_job_id` and expire when the review date changes.",
                "",
                "---",
                f"action: {action}" if action else "action:",
                "POSS | North East | Newcastle | £25,000 | Customer Service Advisor",
                "source_job_id: 123",
                "---",
                "",
            ]
        ),
        encoding="utf-8",
    )


class PersistentExternalReviewActionsTests(unittest.TestCase):
    def test_unchanged_action_is_carried_and_changed_fact_is_withheld(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            review_csv = root / "review.csv"
            summary = root / "summary.md"
            ledger = root / "ledger.csv"

            write_csv(review_csv)
            write_summary(summary)
            persistent.capture_actions(summary, review_csv, ledger)

            # Simulate the next day's source refresh: same vacancy facts, blank action.
            write_csv(review_csv)
            write_summary(summary, action="")
            persistent.apply_actions(
                summary,
                review_csv,
                ledger,
                source="nejobs",
            )

            _, rows = persistent.load_review_csv(review_csv)
            self.assertEqual(rows[0]["manual_action"], "select")
            self.assertEqual(rows[0]["final_decision"], "SELECTED")
            self.assertIn("action: select", summary.read_text(encoding="utf-8"))
            self.assertIn("carried forward", summary.read_text(encoding="utf-8"))

            # A material fact change must return the vacancy to review.
            write_csv(review_csv, title="Senior Customer Service Advisor")
            write_summary(summary, action="")
            persistent.apply_actions(
                summary,
                review_csv,
                ledger,
                source="nejobs",
            )
            _, rows = persistent.load_review_csv(review_csv)
            self.assertEqual(rows[0]["manual_action"], "")
            self.assertEqual(rows[0]["final_decision"], "POSS")
            self.assertNotIn("action: select", summary.read_text(encoding="utf-8"))

    def test_vonne_copy_explains_persistent_actions(self) -> None:
        text = "- Actions are same-day only and do not publish anything.\n"
        patched = persistent.patch_summary_copy(text, "vonne")
        self.assertIn("remembered while the same vacancy review facts remain unchanged", patched)
        self.assertNotIn("same-day only", patched)


if __name__ == "__main__":
    unittest.main()
