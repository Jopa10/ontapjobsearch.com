from pathlib import Path

import pytest

from scripts import service_admin_pipeline_live_config as configured
from review_hub import master_review


@pytest.mark.parametrize("region", [
    "North East - Tyneside, Wearside & Northumberland",
    "North East - County Durham & Darlington/Hartlepool",
])
def test_detailed_north_east_review_accepts_and_preserves_master_selection(tmp_path: Path, region: str):
    job_id = "23643_225646128"
    row = {"region": region, "job_id": job_id, "title": "Commercial Administrator",
           "town": "County Durham", "salary_text": "£30000 - £45000 per year",
           "selection_status": "POSSIBLE_SELECTION", "selector_outcome": "DAILY_REVIEW"}
    path = tmp_path / "review.md"
    configured.write_manual_review_markdown(path, [row])
    assert path.read_text().count("job_id: " + job_id) == 1
    assert region in path.read_text()
    assert master_review._patch_action(path, "job_id", job_id, "select")
    actions = configured.core._markdown_review_action_by_job_id(path.read_text())
    configured.write_manual_review_markdown(path, [row], actions)
    assert configured.core._markdown_review_action_by_job_id(path.read_text()) == {job_id: "select"}
