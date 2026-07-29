from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.scripts import service_admin_pipeline  # noqa: E402
from pipeline.scripts import support_worker_pipeline  # noqa: E402


class ReviewOutputPathTests(unittest.TestCase):
    def test_jobg8_review_outputs_share_a_dedicated_folder(self) -> None:
        expected = Path("reviews") / "jobg8"

        self.assertEqual(expected, service_admin_pipeline.MANUAL_DIR)
        self.assertEqual(expected, support_worker_pipeline.MANUAL_DIR)

    def test_service_admin_review_filenames_are_unchanged(self) -> None:
        self.assertEqual(
            Path("reviews/jobg8/service-admin-review.csv"),
            service_admin_pipeline.MANUAL_REVIEW_CSV_PATH,
        )
        self.assertEqual(
            Path("reviews/jobg8/service-admin-review.md"),
            service_admin_pipeline.MANUAL_REVIEW_MD_PATH,
        )

    def test_support_worker_review_filenames_are_unchanged(self) -> None:
        self.assertEqual(
            Path("reviews/jobg8/support-worker-review.csv"),
            support_worker_pipeline.MANUAL_REVIEW_CSV_PATH,
        )
        self.assertEqual(
            Path("reviews/jobg8/support-worker-review.md"),
            support_worker_pipeline.MANUAL_REVIEW_MD_PATH,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
