import tempfile
import unittest
from pathlib import Path

import pandas as pd

from scripts.report_jobg8_potential_duplicates import Vacancy, _load_vacancies, find_likely_duplicates


def vacancy(
    job_id: str,
    *,
    title: str = "Receptionist/ Office Administrator",
    advertiser: str = "Rise Technical Recruitment",
    location: str = "Gloucestershire",
    description: str = (
        "Receptionist Office Administrator £13 per hour Monday Friday 9am to 3pm Gloucester. "
        "Answering the phone, greeting visitors, scanning, filing, ordering and general administration duties."
    ),
    salary_min: str = "13",
    salary_max: str = "13",
    salary_period: str = "Hourly",
) -> Vacancy:
    return Vacancy(
        job_id=job_id,
        title=title,
        advertiser=advertiser,
        area="Gloucestershire",
        location=location,
        description=description,
        salary_min=salary_min,
        salary_max=salary_max,
        salary_period=salary_period,
    )


class JobG8PotentialDuplicateTests(unittest.TestCase):
    def test_xlsx_loader_handles_blank_cells(self):
        frame = pd.DataFrame(
            [
                {
                    "/Job/DisplayReference": "test-1",
                    "/Job/Position": "Administrator",
                    "/Job/AdvertiserName": "Example Recruiter",
                    "/Job/Area": "North East",
                    "/Job/Location": "",
                    "/Job/Description": "",
                }
            ]
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "jobg8.xlsx"
            frame.to_excel(path, index=False)
            vacancies = _load_vacancies(path)

        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].job_id, "test-1")
        self.assertEqual(vacancies[0].location, "")
        self.assertEqual(vacancies[0].description, "")
        self.assertEqual(vacancies[0].salary_min, "")

    def test_gloucestershire_style_duplicate_with_company_suffix_is_flagged(self):
        first = vacancy("23643_225476234")
        second = vacancy(
            "48c94cb9-206a-4dda-9cae-a48329b95133",
            advertiser="Rise Technical Recruitment Limited",
            description=(
                "Receptionist / Office Administrator £13p/h + Holiday + Pension. Monday - Friday (9am-3pm), "
                "Gloucester. Answering the phone, receiving and greeting visitors, scanning, filing, ordering "
                "and other general administration duties."
            ),
        )

        matches = find_likely_duplicates([first, second])

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["confidence"], "LIKELY_DUPLICATE")
        self.assertEqual(
            {matches[0]["job_id_1"], matches[0]["job_id_2"]},
            {first.job_id, second.job_id},
        )

    def test_same_job_id_is_not_reported(self):
        matches = find_likely_duplicates([vacancy("same"), vacancy("same")])
        self.assertEqual(matches, [])

    def test_same_agency_and_location_but_different_title_is_not_reported(self):
        matches = find_likely_duplicates(
            [
                vacancy("one"),
                vacancy("two", title="Customer Service Advisor"),
            ]
        )
        self.assertEqual(matches, [])

    def test_same_title_block_with_materially_different_advert_is_not_reported(self):
        matches = find_likely_duplicates(
            [
                vacancy("one"),
                vacancy(
                    "two",
                    description=(
                        "Office administrator required for a full time manufacturing support role. "
                        "Duties focus on purchase orders, stock systems, supplier invoices and production schedules."
                    ),
                    salary_min="27000",
                    salary_max="30000",
                    salary_period="Annual",
                ),
            ]
        )
        self.assertEqual(matches, [])


if __name__ == "__main__":
    unittest.main()
