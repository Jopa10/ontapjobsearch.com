from pathlib import Path


WORKFLOW = Path(__file__).parents[2] / ".github/workflows/run-full-jobg8-daily-process.yml"


def test_valid_zero_marketing_and_hr_outputs_do_not_stop_daily_jobg8() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "Marketing output is not an array" in workflow
    assert "HR / Recruitment output is not an array" in workflow
    assert "LIVE Marketing output is empty" not in workflow
    assert "LIVE HR / Recruitment output is empty" not in workflow
