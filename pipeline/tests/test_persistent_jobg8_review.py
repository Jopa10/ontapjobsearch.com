from __future__ import annotations

import unittest

from scripts import persistent_jobg8_review as persistence


class PersistentJobG8ReviewTests(unittest.TestCase):
    def test_patch_parser_recovers_explicit_human_actions(self) -> None:
        patch = """\
@@ -1,7 +1,7 @@
 ---
-action:
+action: select
 POSS | Region | Town | £30,000 | Administrator
 job_id: selected-1
 ---
@@ -10,7 +10,7 @@
 ---
-action:
+action: exclude
 SELECTED | Region | Town | £30,000 | Administrator
 job_id: excluded-1
 ---
"""
        self.assertEqual(
            {"selected-1": "select", "excluded-1": "exclude"},
            persistence._actions_from_patch(patch),
        )

    def test_seed_and_finalize_keep_decisions_hidden_but_durable(self) -> None:
        original = """\
# Review

feed_date: 2026-08-14

---
action:
POSS | Region | Town | £30,000 | Administrator
job_id: selected-1
---
"""
        decisions = {
            "selected-1": {"action": "select", "decided_on": "2026-08-14"},
            "missing-1": {"action": "exclude", "decided_on": "2026-08-14"},
        }

        runtime = persistence._set_review_feed_date(original, "2026-08-15")
        runtime = persistence._apply_actions(runtime, decisions)

        self.assertIn("action: select", runtime)
        self.assertIn("job_id: missing-1", runtime)
        self.assertEqual(
            {"selected-1": "select", "missing-1": "exclude"},
            persistence._explicit_actions(runtime),
        )

        final = persistence._append_store(
            persistence._clear_visible_actions(runtime),
            decisions,
        )
        self.assertNotIn("action: select", final)
        self.assertNotIn("action: exclude", final)
        self.assertEqual(decisions, persistence._load_store(final))
        self.assertEqual("2026-08-15", persistence._review_feed_date(final))

    def test_later_decision_overwrites_same_job_id(self) -> None:
        decisions = {
            "job-1": {"action": "select", "decided_on": "2026-08-13"},
        }
        decisions["job-1"] = {"action": "exclude", "decided_on": "2026-08-14"}
        text = persistence._append_store("# Review\n", decisions)
        self.assertEqual(
            {"action": "exclude", "decided_on": "2026-08-14"},
            persistence._load_store(text)["job-1"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
