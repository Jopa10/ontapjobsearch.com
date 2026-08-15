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
            "missing-1": {
                "action": "exclude",
                "decided_on": "2026-08-14",
                "title": "Office Administrator",
                "employer": "Example Ltd",
            },
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

    def test_review_action_captures_metadata(self) -> None:
        text = """\
---
action: exclude
SELECTED | Yorkshire - West | Leeds | £28,000 | Administrator
job_id: job-1
---
"""
        self.assertEqual(
            {
                "job-1": {
                    "action": "exclude",
                    "region": "Yorkshire - West",
                    "town": "Leeds",
                    "salary": "£28,000",
                    "title": "Administrator",
                }
            },
            persistence._explicit_action_records(text),
        )

    def test_exclusion_report_includes_date_and_is_reversible(self) -> None:
        report = persistence.render_exclusion_report(
            {
                "service_admin": {
                    "job-1": {
                        "action": "exclude",
                        "decided_on": "2026-08-15",
                        "title": "Administrator",
                        "employer": "Example Ltd",
                        "region": "Yorkshire - West",
                        "town": "Leeds",
                        "salary": "£28,000",
                    }
                },
                "support_worker": {
                    "job-2": {
                        "action": "select",
                        "decided_on": "2026-08-15",
                    }
                },
            }
        )
        self.assertIn("excluded_on: 2026-08-15", report)
        self.assertIn("employer: Example Ltd", report)
        self.assertIn("remembered_exclusions: 1", report)
        self.assertNotIn("job_id: job-2", report)

        edited = report.replace(
            "action:\ncategory: service_admin",
            "action: select\ncategory: service_admin",
            1,
        )
        self.assertEqual(
            {
                "job-1": {
                    "action": "select",
                    "title": "Administrator",
                    "employer": "Example Ltd",
                    "region": "Yorkshire - West",
                    "town": "Leeds",
                    "salary": "£28,000",
                }
            },
            persistence._exclusion_recovery_actions(edited, "service_admin"),
        )

    def test_reexclude_resets_decision_date_but_keeps_metadata(self) -> None:
        old = {
            "action": "select",
            "decided_on": "2026-08-14",
            "employer": "Example Ltd",
        }
        merged = persistence._merge_decision(
            old,
            {
                "action": "exclude",
                "title": "Administrator",
                "region": "Yorkshire - West",
                "town": "Leeds",
            },
            "2026-08-15",
        )
        self.assertEqual("exclude", merged["action"])
        self.assertEqual("2026-08-15", merged["decided_on"])
        self.assertEqual("Example Ltd", merged["employer"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
