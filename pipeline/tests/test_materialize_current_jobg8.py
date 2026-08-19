from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import materialize_current_jobg8 as current


class MaterializeCurrentJobG8Tests(unittest.TestCase):
    def test_clear_pipeline_input_removes_feed_file_types_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("old.xlsx", "old.xls", "old.xlsm", "old.csv", "keep.txt"):
                (root / name).write_text("x", encoding="utf-8")

            current.clear_pipeline_input(root)

            self.assertFalse((root / "old.xlsx").exists())
            self.assertFalse((root / "old.xls").exists())
            self.assertFalse((root / "old.xlsm").exists())
            self.assertFalse((root / "old.csv").exists())
            self.assertTrue((root / "keep.txt").exists())

    def test_materialize_uses_one_shared_download_and_converter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            zip_path = root / "jobg8.zip"
            output = root / "input" / "jobg8.xlsx"
            stale = output.parent / "stale.csv"
            output.parent.mkdir(parents=True)
            stale.write_text("old", encoding="utf-8")

            def fake_download(feed_url: str, target: Path, attempts: int = 4, timeout: int = 180) -> None:
                self.assertEqual("https://example.test/feed", feed_url)
                target.write_bytes(b"zip")

            def fake_convert(source: Path, target: Path, minimum: int, maximum: int) -> int:
                self.assertEqual(zip_path, source)
                self.assertEqual(5000, minimum)
                self.assertEqual(20000, maximum)
                target.write_bytes(b"xlsx")
                return 9876

            with patch.object(current, "download", side_effect=fake_download), patch.object(
                current, "convert", side_effect=fake_convert
            ):
                count = current.materialize(
                    "https://example.test/feed",
                    zip_path=zip_path,
                    output_path=output,
                )

            self.assertEqual(9876, count)
            self.assertTrue(output.exists())
            self.assertFalse(stale.exists())

    def test_blank_feed_url_fails_before_network_access(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, "JOBG8_FEED_URL"):
                current.download("", Path(tmp) / "jobg8.zip", attempts=1)


if __name__ == "__main__":
    unittest.main()
