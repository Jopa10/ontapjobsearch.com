from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "pipeline" / "scripts" / "submit_indexnow.py"
SPEC = importlib.util.spec_from_file_location("submit_indexnow", MODULE_PATH)
assert SPEC and SPEC.loader
submit_indexnow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(submit_indexnow)


def test_jobs_from_text_ignores_non_job_json() -> None:
    assert submit_indexnow._jobs_from_text('{"enabled": true}') == set()
    assert submit_indexnow._jobs_from_text("not-json") == set()


def test_jobs_from_text_collects_non_empty_ids() -> None:
    content = json.dumps(
        [
            {"job_id": "job-2"},
            {"job_id": " job-1 "},
            {"title": "No ID"},
        ]
    )
    assert submit_indexnow._jobs_from_text(content) == {"job-1", "job-2"}


def test_slice_routes_match_live_page_paths() -> None:
    assert submit_indexnow._slice_routes(
        "app/west-yorkshire/support-worker.json"
    ) == {"/west-yorkshire/support-worker"}
    assert submit_indexnow._slice_routes(
        "app/north-east/support-worker-jobs.json"
    ) == {"/north-east/support-worker"}


def test_london_json_updates_both_public_slices() -> None:
    assert submit_indexnow._slice_routes(
        "app/london/service-administrator-jobs.json"
    ) == {
        "/london/service-administrator-jobs",
        "/london/outer-service-administrator-jobs",
    }


def test_all_current_urls_use_canonical_host() -> None:
    urls = submit_indexnow.all_current_urls()
    assert urls
    assert all(
        url.startswith("https://www.ontapjobsearch.com/") for url in urls
    )
    assert "https://www.ontapjobsearch.com/browse-jobs" in urls
