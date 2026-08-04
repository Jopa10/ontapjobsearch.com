from pathlib import Path

from external_sources.teaching_vacancies_poc import Vacancy
from external_sources.teaching_vacancies_review import ordered, review_fingerprint, write_review_markdown


def vacancy(classification: str, source_job_id: str, title: str) -> Vacancy:
    return Vacancy(
        source_job_id=source_job_id,
        title=title,
        employer="Example School",
        location="Leeds, LS1",
        source_url=f"https://example.test/{source_job_id}",
        classification=classification,
        final_decision=classification,
        jobg8_check="NO_MATCH",
    )


def test_order_and_review_format(tmp_path: Path):
    rows = [
        vacancy("HARD_PASS", "3", "Teacher"),
        vacancy("POSS", "2", "Office Manager"),
        vacancy("HC", "1", "Administrator"),
    ]
    assert [row.classification for row in ordered(rows)] == ["HC", "POSS", "HARD_PASS"]

    path = tmp_path / "review.md"
    write_review_markdown(path, rows, "2026-08-04")
    text = path.read_text(encoding="utf-8")
    assert text.index("## HC") < text.index("## POSS")
    assert "## HARD_PASS" not in text
    assert text.count("- [ ] SELECT") == 2
    assert text.count("- [ ] EXCLUDE") == 2
    assert review_fingerprint(rows) in text
