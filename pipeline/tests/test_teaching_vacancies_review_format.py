import csv
from pathlib import Path

from external_sources.format_teaching_vacancies_review import sort_review_csv


def test_sort_review_csv_orders_decisions_and_moves_final_decision_first(tmp_path: Path):
    path = tmp_path / "review.csv"
    fieldnames = ["classification", "title", "employer", "location", "final_decision"]
    rows = [
        {"classification": "HARD_PASS", "title": "Teacher", "employer": "C", "location": "Leeds", "final_decision": "HARD_PASS"},
        {"classification": "HC", "title": "Receptionist", "employer": "D", "location": "Leeds", "final_decision": "HC"},
        {"classification": "POSS", "title": "Office Manager", "employer": "B", "location": "Bradford", "final_decision": "POSS"},
        {"classification": "HC", "title": "Administrative Assistant", "employer": "A", "location": "Wakefield", "final_decision": "HC"},
    ]
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    sort_review_csv(path)

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        sorted_rows = list(reader)
        assert reader.fieldnames[0] == "final_decision"

    assert [row["final_decision"] for row in sorted_rows] == ["HC", "HC", "POSS", "HARD_PASS"]
