from external_sources.normalise_teaching_vacancies_output import (
    normalise_contract_value,
    normalise_rows,
)


def test_single_contract_value_is_humanised():
    assert normalise_contract_value("FULL_TIME") == "Full time"


def test_list_contract_value_is_humanised():
    assert normalise_contract_value("['full time', 'temporary']") == (
        "Full time, temporary"
    )


def test_contract_list_syntax_is_removed_from_published_text():
    rows = normalise_rows(
        [
            {
                "job_id": "teaching-vacancies-example",
                "employment_type": "['full time', 'temporary']",
                "summary": "Example role. ['full time', 'temporary']; £21,196.",
                "description": (
                    "The source lists the employment type as "
                    "['full time', 'temporary']."
                ),
            }
        ]
    )
    row = rows[0]
    assert row["employment_type"] == "Full time, temporary"
    assert "['" not in row["summary"]
    assert "['" not in row["description"]
    assert "Full time, temporary" in row["summary"]
    assert "Full time, temporary" in row["description"]
