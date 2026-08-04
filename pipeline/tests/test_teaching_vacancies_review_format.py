import csv
from pathlib import Path

from external_sources.format_teaching_vacancies_review import sort_review_csv


def test_sort_review_csv_orders_hc_then_poss_then_hard_pass(tmp_path: Path):
    path = tmp_path / "review.csv"
    fieldnames = ["classification", "title", "employer", "location"]
    rows = [
        {"classification": "HARD_PASS", "title": "Teacher", "employer": "C", "location": "Leeds"},
        {"classification": "POSS", "title": "Office Manager", "employer": "B", "location": "Bradford"},
        {"classification": "HC", "title": "Administrative Assistant", "employer": "A", "location": "Wakefield"},
    ]
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    sort_review_csv(path)

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        sorted_rows = list(csv.DictReader(handle))
    assert [row["classification"] for row in sorted_rows] == ["HC", "POSS", "HARD_PASS"]
