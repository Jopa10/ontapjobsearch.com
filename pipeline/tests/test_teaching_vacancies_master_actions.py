from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

import pytest

from external_sources import teaching_vacancies_master_actions as actions
from external_sources import teaching_vacancies_master_review as master
from external_sources import teaching_vacancies_poc as poc
from external_sources import teaching_vacancies_regional_review as review


def make_record(
    source_job_id: str,
    *,
    classification: str,
    title: str,
    region: str = "Hampshire",
    slice_status: str = "LIVE",
) -> review.ReviewRecord:
    reasons = {
        "HC": "Clear admin/service title: administrator",
        "POSS": "Borderline school administration title: business manager",
    }
    vacancy = poc.Vacancy(
        source_job_id=source_job_id,
        title=title,
        employer="Example School",
        location="Southampton, SO1 1AA",
        salary_text="£25,000",
        posted_date="2026-08-01",
        closing_date="2026-09-01T12:00:00+01:00",
        employment_type="FULL_TIME",
        source_url=f"https://teaching-vacancies.service.gov.uk/jobs/{source_job_id}",
        geography_status="IN_SCOPE",
        geography_reason="Exact location fallback match",
        classification=classification,
        classification_reason=reasons[classification],
        jobg8_check="NO_MATCH",
        jobg8_match_score="0.000",
    )
    return review.ReviewRecord(
        vacancy=vacancy,
        ontap_region=region,
        geo_cluster=region,
        geography_reason="Exact location fallback match",
        geography_lookup_key="southampton",
        slice_status=slice_status,
        publish_eligible="YES" if slice_status == "LIVE" else "NO",
        factual_fingerprint=hashlib.sha256(source_job_id.encode()).hexdigest(),
        discovery_routes="[]",
    )


def write_region(review_dir: Path, records: list[review.ReviewRecord]) -> None:
    region = records[0].ontap_region
    csv_path, md_path = review.review_paths(review_dir, region)
    csv_path.write_bytes(review.review_csv_bytes(records))
    md_path.write_text(
        review.markdown_summary(
            region,
            records,
            review_date="2026-08-06",
            routing_manifest_sha256="a" * 64,
        ),
        encoding="utf-8",
    )


def set_action(text: str, source_job_id: str, action: str) -> str:
    pattern = re.compile(r"(?ms)(^---\s*$\n)(.*?)(^---\s*$)")

    def replace(match: re.Match[str]) -> str:
        block = match.group(2)
        if f"source_job_id: {source_job_id}" not in block:
            return match.group(0)
        block = re.sub(
            r"(?m)^action:[ \t]*.*$",
            f"action: {action}" if action else "action:",
            block,
            count=1,
        )
        return match.group(1) + block + match.group(3)

    return pattern.sub(replace, text)


def remove_block(text: str, source_job_id: str) -> str:
    """Remove exactly one review block without spanning adjacent blocks."""
    pattern = re.compile(r"(?ms)(^---\s*$\n)(.*?)(^---\s*$\n?)")
    removed = False

    def replace(match: re.Match[str]) -> str:
        nonlocal removed
        block = match.group(2)
        if removed or f"source_job_id: {source_job_id}" not in block:
            return match.group(0)
        removed = True
        return ""

    result = pattern.sub(replace, text)
    if not removed:
        raise AssertionError(f"review block not found: {source_job_id}")
    return result


def read_csv(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["source_job_id"]: row for row in csv.DictReader(handle)}


def test_master_actions_update_regional_review_boundaries(tmp_path: Path) -> None:
    write_region(
        tmp_path,
        [
            make_record("selected", classification="HC", title="Administrator"),
            make_record("possible", classification="POSS", title="Business Manager"),
        ],
    )
    write_region(
        tmp_path,
        [
            make_record(
                "deferred",
                classification="HC",
                title="Administrator",
                region="Bedfordshire",
                slice_status="UNREGISTERED",
            )
        ],
    )

    master_rows = master.build_master_rows(tmp_path)
    master_csv = tmp_path / "england-wide-admin-service-review.csv"
    master_md = tmp_path / "england-wide-admin-service-summary.md"
    master_csv.write_bytes(master.master_csv_bytes(master_rows))
    text = master.master_summary_text(master_rows)
    text = set_action(text, "selected", "exclude")
    text = set_action(text, "possible", "select")
    master_md.write_text(text, encoding="utf-8")

    counts = actions.apply_master_actions(
        master_csv=master_csv,
        master_summary=master_md,
        review_dir=tmp_path,
        write=True,
    )

    hampshire_csv, hampshire_md = review.review_paths(tmp_path, "Hampshire")
    rows = read_csv(hampshire_csv)
    assert rows["selected"]["manual_action"] == "exclude"
    assert rows["selected"]["final_decision"] == "EXCLUDED"
    assert rows["possible"]["manual_action"] == "select"
    assert rows["possible"]["final_decision"] == "SELECTED"

    summary = hampshire_md.read_text(encoding="utf-8")
    assert "action: exclude" in summary
    assert "action: select" in summary
    assert "## EXCLUDED BY REVIEW" in summary
    assert "EXCLUDED | Hampshire" in summary
    assert counts["reviewable"] == 2
    assert counts["selected_actions"] == 1
    assert counts["excluded_actions"] == 1

    deferred_csv, deferred_md = review.review_paths(tmp_path, "Bedfordshire")
    deferred = read_csv(deferred_csv)
    assert deferred["deferred"]["manual_action"] == ""
    assert deferred_md.is_file()


def test_master_actions_reject_tampered_review_facts(tmp_path: Path) -> None:
    write_region(
        tmp_path,
        [make_record("selected", classification="HC", title="Administrator")],
    )
    master_rows = master.build_master_rows(tmp_path)
    master_csv = tmp_path / "england-wide-admin-service-review.csv"
    master_md = tmp_path / "england-wide-admin-service-summary.md"
    master_csv.write_bytes(master.master_csv_bytes(master_rows))
    text = master.master_summary_text(master_rows).replace(
        "employer: Example School",
        "employer: Different School",
    )
    master_md.write_text(text, encoding="utf-8")

    with pytest.raises(ValueError, match="employer mismatch"):
        actions.apply_master_actions(
            master_csv=master_csv,
            master_summary=master_md,
            review_dir=tmp_path,
            write=False,
        )


def test_master_actions_require_every_live_review_block(tmp_path: Path) -> None:
    write_region(
        tmp_path,
        [
            make_record("one", classification="HC", title="Administrator"),
            make_record("two", classification="POSS", title="Office Manager"),
        ],
    )
    master_rows = master.build_master_rows(tmp_path)
    master_csv = tmp_path / "england-wide-admin-service-review.csv"
    master_md = tmp_path / "england-wide-admin-service-summary.md"
    master_csv.write_bytes(master.master_csv_bytes(master_rows))
    text = master.master_summary_text(master_rows)
    text = remove_block(text, "two")
    assert "source_job_id: one" in text
    assert "source_job_id: two" not in text
    master_md.write_text(text, encoding="utf-8")

    with pytest.raises(ValueError, match="missing 1 editable LIVE review block"):
        actions.apply_master_actions(
            master_csv=master_csv,
            master_summary=master_md,
            review_dir=tmp_path,
            write=False,
        )


def test_resolved_selection_carries_from_csv_without_editable_block(
    tmp_path: Path,
) -> None:
    old_dir = tmp_path / "old"
    old_dir.mkdir()
    old_record = make_record(
        "remembered",
        classification="POSS",
        title="Admin Assistant",
    )
    old_record.manual_action = "select"
    write_region(old_dir, [old_record])
    old_rows = master.build_master_rows(old_dir)

    old_csv = tmp_path / "old-master.csv"
    old_md = tmp_path / "old-master.md"
    old_csv.write_bytes(master.master_csv_bytes(old_rows))
    old_md.write_text(master.master_summary_text(old_rows), encoding="utf-8")
    assert "source_job_id: remembered" not in old_md.read_text(encoding="utf-8")

    current_dir = tmp_path / "current"
    current_dir.mkdir()
    current_record = make_record(
        "remembered",
        classification="POSS",
        title="Admin Assistant",
    )
    write_region(current_dir, [current_record])
    current_rows = master.build_master_rows(current_dir)

    carried = actions.carry_existing_actions(
        current_rows,
        old_master_csv=old_csv,
        old_master_summary=old_md,
    )

    assert carried == 1
    assert current_rows[0]["manual_action"] == "select"
    assert current_rows[0]["final_decision"] == "SELECTED"


def test_resolved_selection_carries_when_old_markdown_still_has_block(
    tmp_path: Path,
) -> None:
    old_dir = tmp_path / "old"
    old_dir.mkdir()
    old_record = make_record(
        "remembered",
        classification="POSS",
        title="Admin Assistant",
    )
    write_region(old_dir, [old_record])
    unresolved_rows = master.build_master_rows(old_dir)
    stale_markdown = master.master_summary_text(unresolved_rows)

    old_record.manual_action = "select"
    write_region(old_dir, [old_record])
    resolved_rows = master.build_master_rows(old_dir)
    old_csv = tmp_path / "old-master.csv"
    old_md = tmp_path / "old-master.md"
    old_csv.write_bytes(master.master_csv_bytes(resolved_rows))
    old_md.write_text(stale_markdown, encoding="utf-8")

    current_dir = tmp_path / "current"
    current_dir.mkdir()
    write_region(
        current_dir,
        [
            make_record(
                "remembered",
                classification="POSS",
                title="Admin Assistant",
            )
        ],
    )
    current_rows = master.build_master_rows(current_dir)

    carried = actions.carry_existing_actions(
        current_rows,
        old_master_csv=old_csv,
        old_master_summary=old_md,
    )

    assert carried == 1
    assert current_rows[0]["manual_action"] == "select"
    assert current_rows[0]["final_decision"] == "SELECTED"

    with pytest.raises(ValueError, match="non-reviewable or unknown ID"):
        actions.parse_master_actions(resolved_rows, old_md)


def test_master_carry_does_not_reselect_possible_jobg8_duplicate(
    tmp_path: Path,
) -> None:
    old_dir = tmp_path / "old"
    old_dir.mkdir()
    old_record = make_record(
        "possible-duplicate",
        classification="POSS",
        title="Admin Assistant",
    )
    old_record.vacancy.jobg8_check = "POSSIBLE_DUPLICATE"
    old_record.manual_action = "select"
    write_region(old_dir, [old_record])
    old_rows = master.build_master_rows(old_dir)

    old_csv = tmp_path / "old-master.csv"
    old_md = tmp_path / "old-master.md"
    old_csv.write_bytes(master.master_csv_bytes(old_rows))
    old_md.write_text(master.master_summary_text(old_rows), encoding="utf-8")

    current_dir = tmp_path / "current"
    current_dir.mkdir()
    current_record = make_record(
        "possible-duplicate",
        classification="POSS",
        title="Admin Assistant",
    )
    current_record.vacancy.jobg8_check = "POSSIBLE_DUPLICATE"
    write_region(current_dir, [current_record])
    current_rows = master.build_master_rows(current_dir)

    carried = actions.carry_existing_actions(
        current_rows,
        old_master_csv=old_csv,
        old_master_summary=old_md,
    )

    assert carried == 0
    assert current_rows[0]["manual_action"] == ""
    assert current_rows[0]["final_decision"] == "POSS"
