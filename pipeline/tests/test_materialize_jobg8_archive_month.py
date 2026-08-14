from datetime import date
from pathlib import Path
import tempfile
import unittest

from scripts.materialize_jobg8_archive_month import (
    copy_legacy_excel,
    expected_s3_days,
    month_bounds,
)


class MaterializeJobG8ArchiveMonthTests(unittest.TestCase):
    def test_month_bounds(self):
        self.assertEqual(
            month_bounds("2026-08"),
            (date(2026, 8, 1), date(2026, 8, 31)),
        )

    def test_s3_days_start_only_when_private_archive_begins(self):
        self.assertEqual(
            expected_s3_days(
                "2026-08",
                date(2026, 8, 14),
                date(2026, 8, 16),
            ),
            [date(2026, 8, 14), date(2026, 8, 15), date(2026, 8, 16)],
        )

    def test_future_month_has_no_expected_s3_days(self):
        self.assertEqual(
            expected_s3_days(
                "2026-09",
                date(2026, 8, 14),
                date(2026, 8, 16),
            ),
            [],
        )

    def test_legacy_copy_uses_excel_files_only(self):
        with tempfile.TemporaryDirectory() as source_name, tempfile.TemporaryDirectory() as output_name:
            source = Path(source_name)
            output = Path(output_name)
            (source / "2026-08-01.xlsx").write_bytes(b"xlsx")
            (source / "notes.txt").write_text("ignore", encoding="utf-8")

            copied = copy_legacy_excel(source, output)

            self.assertEqual(copied, 1)
            self.assertTrue((output / "2026-08-01.xlsx").is_file())
            self.assertFalse((output / "notes.txt").exists())


if __name__ == "__main__":
    unittest.main()
