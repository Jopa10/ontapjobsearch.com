from pathlib import Path
import tempfile
import unittest

from openpyxl import Workbook

from scripts.validate_jobg8_feed_health import inspect_feed, validate_health


HEADERS = [
    "/Job/DisplayReference",
    "/Job/Position",
    "/Job/AdvertiserName",
    "/Job/Area",
    "/Job/Location",
    "/Job/ApplicationURL",
    "/Job/Description",
]


def write_feed(path: Path, rows: list[list[object]]) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(HEADERS)
    for row in rows:
        sheet.append(row)
    workbook.save(path)
    workbook.close()


class ValidateJobG8FeedHealthTests(unittest.TestCase):
    def test_healthy_feed_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "healthy.xlsx"
            rows = [
                [f"ref-{i}", f"Job {i}", "Employer", "Area", "Town", f"https://example.com/{i}", "Description"]
                for i in range(100)
            ]
            write_feed(path, rows)
            self.assertEqual(validate_health(inspect_feed(path)), [])

    def test_half_blank_titles_and_urls_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.xlsx"
            rows = []
            for i in range(100):
                rows.append([
                    f"ref-{i}",
                    f"Job {i}" if i < 50 else "",
                    "Employer",
                    "Area",
                    "Town",
                    f"https://example.com/{i}" if i < 50 else "",
                    "Description",
                ])
            write_feed(path, rows)
            failures = validate_health(inspect_feed(path))
            self.assertTrue(any("Position/title" in failure for failure in failures))
            self.assertTrue(any("ApplicationURL" in failure for failure in failures))

    def test_duplicate_reference_collapse_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "duplicates.xlsx"
            rows = [
                ["same-ref", f"Job {i}", "Employer", "Area", "Town", f"https://example.com/{i}", "Description"]
                for i in range(100)
            ]
            write_feed(path, rows)
            failures = validate_health(inspect_feed(path))
            self.assertTrue(any("unique DisplayReference" in failure for failure in failures))

    def test_bad_url_shape_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad-urls.xlsx"
            rows = [
                [f"ref-{i}", f"Job {i}", "Employer", "Area", "Town", "not-a-url", "Description"]
                for i in range(100)
            ]
            write_feed(path, rows)
            failures = validate_health(inspect_feed(path))
            self.assertTrue(any("valid http(s)" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
