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
    text = re.sub(
        r"(?ms)^---\s*$\n.*?source_job_id: two\n.*?^---\s*$\n?",
        "",
        text,
        count=1,
    )
    master_md.write_text(text, encoding="utf-8")

    with pytest.raises(ValueError, match="missing 1 LIVE review block"):
        actions.apply_master_actions(
            master_csv=master_csv,
            master_summary=master_md,
            review_dir=tmp_path,
            write=False,
        )
