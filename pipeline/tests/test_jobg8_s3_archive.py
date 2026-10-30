from datetime import date
import unittest

from scripts.jobg8_s3_archive import canonical_key, dated_key_day, preservation_key, retention_cutoff


class JobG8S3ArchiveTests(unittest.TestCase):
    def test_canonical_key_is_one_object_per_calendar_day(self):
        self.assertEqual(
            canonical_key("jobg8/raw", date(2026, 8, 14)),
            "jobg8/raw/2026-08-14.zip",
        )

    def test_pre_changeover_copy_has_a_distinct_key_for_same_date(self):
        self.assertEqual(
            preservation_key("jobg8/raw", date(2026, 10, 30), "pre-changeover"),
            "jobg8/raw/2026-10-30-pre-changeover.zip",
        )

    def test_retention_recognizes_preserved_pre_changeover_copy(self):
        self.assertEqual(
            dated_key_day("jobg8/raw/2026-10-30-pre-changeover.zip", "jobg8/raw"),
            date(2026, 10, 30),
        )

    def test_retention_cutoff_keeps_exactly_ninety_calendar_dates(self):
        self.assertEqual(
            retention_cutoff(date(2026, 8, 14), 90),
            date(2026, 5, 17),
        )

    def test_dated_key_day_accepts_only_direct_daily_zip_objects(self):
        self.assertEqual(
            dated_key_day("jobg8/raw/2026-08-14.zip", "jobg8/raw"),
            date(2026, 8, 14),
        )
        self.assertIsNone(
            dated_key_day("jobg8/raw/extra/2026-08-14.zip", "jobg8/raw")
        )
        self.assertIsNone(
            dated_key_day("jobg8/raw/notes.txt", "jobg8/raw")
        )

    def test_invalid_keep_days_is_rejected(self):
        with self.assertRaises(ValueError):
            retention_cutoff(date(2026, 8, 14), 0)


if __name__ == "__main__":
    unittest.main()
