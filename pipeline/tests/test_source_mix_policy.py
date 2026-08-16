from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from external_sources.source_mix_policy import (
    REASON_NON_JOBG8_CAP,
    REASON_SINGLE_EXTERNAL_SOURCE_CAP,
    apply_source_mix_policy,
    prioritise_nhs_open_switch,
    workflow_summary_line,
)


def rows(source: str, count: int, *, switchability: str = "") -> list[dict]:
    return [
        {
            "job_id": f"{source}-{index}",
            "source": source,
            "switchability": switchability,
        }
        for index in range(count)
    ]


def test_single_external_source_is_capped_at_25_percent() -> None:
    base = rows("JobG8", 100)
    candidates = rows("NHS Jobs", 50)

    result = apply_source_mix_policy(base, candidates)

    assert len(result.accepted_rows) == 33
    assert len(result.deferred_rows) == 17
    assert result.metrics.non_jobg8_share < 0.25
    assert all(
        REASON_SINGLE_EXTERNAL_SOURCE_CAP in item.reasons
        for item in result.deferred_rows
    )


def test_overall_non_jobg8_cap_accounts_for_existing_external_rows() -> None:
    base = rows("JobG8", 80) + rows("Teaching Vacancies", 20)
    candidates = rows("NHS Jobs", 30)

    result = apply_source_mix_policy(base, candidates)

    assert len(result.accepted_rows) == 14
    assert len(result.deferred_rows) == 16
    assert result.metrics.non_jobg8_share <= 0.30
    assert REASON_NON_JOBG8_CAP in result.deferred_rows[0].reasons


def test_existing_rows_are_never_removed_when_slice_is_already_at_cap() -> None:
    base = rows("JobG8", 70) + rows("Teaching Vacancies", 30)

    result = apply_source_mix_policy(base, rows("NHS Jobs", 3))

    assert len(result.existing_rows) == 100
    assert result.accepted_rows == []
    assert len(result.deferred_rows) == 3


def test_jobg8_additions_are_allowed_even_when_external_mix_is_high() -> None:
    base = rows("JobG8", 60) + rows("Teaching Vacancies", 40)

    result = apply_source_mix_policy(base, rows("JobG8", 10))

    assert len(result.accepted_rows) == 10
    assert result.deferred_rows == []
    assert result.metrics.non_jobg8_share < 0.40


def test_missing_source_is_deferred_not_silently_accepted() -> None:
    result = apply_source_mix_policy(rows("JobG8", 10), [{"job_id": "x"}])

    assert result.accepted_rows == []
    assert result.deferred_rows[0].reasons == ("MISSING_SOURCE",)


def test_nhs_open_switch_rows_get_capacity_before_other_nhs_rows() -> None:
    base = rows("JobG8", 100)
    candidates = (
        rows("NHS Jobs", 5, switchability="SYSTEM_EXPERIENCED")
        + rows("NHS Jobs", 3, switchability="OPEN_SWITCH")
        + rows("NHS Jobs", 30, switchability="BRIDGEABLE")
    )
    ordered = prioritise_nhs_open_switch(candidates)

    assert [row["switchability"] for row in ordered[:3]] == ["OPEN_SWITCH"] * 3

    result = apply_source_mix_policy(base, ordered)
    accepted_open = sum(
        row["switchability"] == "OPEN_SWITCH" for row in result.accepted_rows
    )
    assert accepted_open == 3
    assert len(result.accepted_rows) == 33


def test_workflow_summary_makes_throttling_visible() -> None:
    result = apply_source_mix_policy(rows("JobG8", 4), rows("NHS Jobs", 4))
    summary = workflow_summary_line("North East Admin", result)

    assert "CAP APPLIED" in summary
    assert "deferred" in summary
    assert "non-JobG8" in summary
