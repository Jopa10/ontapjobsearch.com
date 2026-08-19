from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.jobg8_xml_adapter import convert
from scripts.pipeline_refinement import resolve_feed_date


JOBS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Jobs>
  <Job>
    <DisplayReference>job-1</DisplayReference>
    <Position>Administrator</Position>
    <AdvertiserName>Example Ltd</AdvertiserName>
    <AdvertiserType>Agency</AdvertiserType>
    <EmploymentType>Permanent</EmploymentType>
    <Area>Tyne And Wear</Area>
    <Location>Newcastle upon Tyne</Location>
    <PostalCode>NE1 1AA</PostalCode>
    <ApplicationURL>https://example.test/apply</ApplicationURL>
    <Description>General administration role.</Description>
  </Job>
</Jobs>
"""


class JobG8XmlAdapterFeedDateTests(unittest.TestCase):
    def test_archive_restore_preserves_original_feed_date(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            zip_path = root / "jobg8-reviewed.zip"
            output_path = root / "jobg8.xlsx"

            info = zipfile.ZipInfo("Jobs.xml")
            info.date_time = (2026, 8, 18, 15, 30, 0)
            with zipfile.ZipFile(zip_path, "w") as archive:
                archive.writestr(info, JOBS_XML)

            convert(zip_path, output_path, 1, 10)

            self.assertEqual("2026-08-18", resolve_feed_date(output_path))


if __name__ == "__main__":
    unittest.main()
