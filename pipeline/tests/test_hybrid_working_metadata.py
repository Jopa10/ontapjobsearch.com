from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.module3.working_arrangement import (  # noqa: E402
    NON_QUALIFYING_VALUE,
    classify_working_arrangement,
)


class HybridWorkingMetadataTests(unittest.TestCase):
    def classify(self, description: str):
        return classify_working_arrangement(
            "Administrative Assistant",
            description,
            "Leeds",
            "West Yorkshire",
        )

    def test_generic_hybrid_wording(self) -> None:
        result = self.classify("We offer hybrid working from our Leeds office.")
        self.assertEqual("hybrid", result.working_arrangement)
        self.assertEqual("Hybrid working", result.working_arrangement_text)
        self.assertIn("hybrid working", result.working_arrangement_evidence.casefold())

    def test_exact_home_and_office_day_split(self) -> None:
        result = self.classify(
            "The role is hybrid: three days in the office and two days from home."
        )
        self.assertEqual("hybrid", result.working_arrangement)
        self.assertEqual(
            "2 days from home / 3 days in office",
            result.working_arrangement_text,
        )

    def test_up_to_homeworking_arrangement(self) -> None:
        result = self.classify("You may work up to two days working from home.")
        self.assertEqual("partly_remote", result.working_arrangement)
        self.assertEqual("Up to 2 days from home", result.working_arrangement_text)

    def test_home_and_office_based_wording(self) -> None:
        result = self.classify("We provide home and office-based working.")
        self.assertEqual("hybrid", result.working_arrangement)
        self.assertEqual("Hybrid working", result.working_arrangement_text)

    def test_one_office_day_per_week_is_preserved(self) -> None:
        result = self.classify("Hybrid working with one office day per week.")
        self.assertEqual("hybrid", result.working_arrangement)
        self.assertEqual("1 office day per week", result.working_arrangement_text)

    def test_some_remote_working(self) -> None:
        result = self.classify("The position includes some remote working.")
        self.assertEqual("partly_remote", result.working_arrangement)
        self.assertEqual("Hybrid working", result.working_arrangement_text)

    def test_remote_team_false_positive(self) -> None:
        result = self.classify("You will support a remote team across the UK.")
        self.assertEqual(NON_QUALIFYING_VALUE, result.working_arrangement)
        self.assertEqual("", result.working_arrangement_text)

    def test_remote_location_false_positive(self) -> None:
        result = self.classify("Travel is required due to the remote location.")
        self.assertEqual(NON_QUALIFYING_VALUE, result.working_arrangement)

    def test_remote_training_false_positive(self) -> None:
        result = self.classify("You will deliver remote training sessions to clients.")
        self.assertEqual(NON_QUALIFYING_VALUE, result.working_arrangement)

    def test_homeworking_allowance_false_positive(self) -> None:
        result = self.classify("Benefits include a working-from-home allowance.")
        self.assertEqual(NON_QUALIFYING_VALUE, result.working_arrangement)

    def test_experience_working_remotely_false_positive(self) -> None:
        result = self.classify("Experience of working remotely would be useful.")
        self.assertEqual(NON_QUALIFYING_VALUE, result.working_arrangement)

    def test_explicitly_non_remote_advert(self) -> None:
        result = self.classify(
            "This is office-based only and remote working is not available."
        )
        self.assertEqual(NON_QUALIFYING_VALUE, result.working_arrangement)

    def test_office_attendance_alone_does_not_create_badge(self) -> None:
        result = self.classify("Regular office attendance is required in Leeds.")
        self.assertEqual(NON_QUALIFYING_VALUE, result.working_arrangement)

    def test_metadata_serialises_to_expected_json_fields(self) -> None:
        result = self.classify("Hybrid working with two days from home.")
        payload = json.loads(json.dumps(result.as_dict()))
        self.assertEqual(
            {
                "working_arrangement": "hybrid",
                "working_arrangement_text": "2 days from home",
                "working_arrangement_evidence": result.working_arrangement_evidence,
            },
            payload,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
