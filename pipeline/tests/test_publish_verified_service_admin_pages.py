from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from scripts import publish_verified_service_admin_pages as publisher


def test_service_admin_publisher_excludes_other_categories() -> None:
    mappings = publisher.service_admin_mappings()
    assert mappings
    assert all(mapping.category == "admin_service" for mapping in mappings)
    assert all("support-worker" not in str(mapping.destination) for mapping in mappings)
    assert any(mapping.region == "Yorkshire - North" for mapping in mappings)


def test_service_admin_publisher_passes_repository_wide_stable_dates(
    monkeypatch,
) -> None:
    mapping = publisher.service_admin_mappings()[0]
    shared_dates = {"job-1": ("2026-08-01", "ontap_first_published")}
    seen: dict[str, object] = {}

    monkeypatch.setattr(publisher, "service_admin_mappings", lambda: (mapping,))
    monkeypatch.setattr(publisher.core, "live_slices", lambda: {(mapping.region, mapping.category)})
    monkeypatch.setattr(
        publisher.core,
        "load_shared_posted_dates",
        lambda mappings: shared_dates,
    )

    def publish_one(candidate, **kwargs):
        seen["mapping"] = candidate
        seen.update(kwargs)
        return {"status": "unchanged"}

    monkeypatch.setattr(publisher.core, "publish_one", publish_one)
    monkeypatch.setattr(publisher.core, "format_report", lambda results: "ok\n")
    monkeypatch.setattr(sys, "argv", ["publisher", "--dry-run"])

    assert publisher.main() == 0
    assert seen["mapping"] == mapping
    assert seen["shared_dates"] is shared_dates


def test_isolated_region_is_skipped_and_previous_live_page_retained(
    monkeypatch,
    tmp_path: Path,
    capsys,
) -> None:
    mappings = publisher.service_admin_mappings()
    isolated = mappings[0]
    clean = mappings[1]
    report_path = tmp_path / "report.json"
    report_path.write_text(
        json.dumps(
            {
                "contract_version": publisher.ISOLATION_REPORT_CONTRACT,
                "max_isolated_regions": 3,
                "isolated_regions": [isolated.region],
                "regions": [],
            }
        ),
        encoding="utf-8",
    )
    published = []

    monkeypatch.setattr(
        publisher,
        "service_admin_mappings",
        lambda: (isolated, clean),
    )
    monkeypatch.setattr(publisher.core, "live_slices", lambda: set())
    monkeypatch.setattr(publisher.core, "load_shared_posted_dates", lambda _: {})

    def publish_one(mapping, **_kwargs):
        published.append(mapping.region)
        return {
            "page_label": mapping.label,
            "source": str(mapping.source),
            "destination": str(mapping.destination),
            "selected_count": 1,
            "status": "unchanged",
            "reason": "test",
        }

    monkeypatch.setattr(publisher.core, "publish_one", publish_one)
    monkeypatch.setattr(
        sys,
        "argv",
        ["publisher", "--write", "--isolation-report", str(report_path)],
    )

    assert publisher.main() == 0
    assert published == [clean.region]
    assert "previous live destination retained" in capsys.readouterr().out


def test_isolation_report_cannot_exceed_verified_threshold(tmp_path: Path) -> None:
    report_path = tmp_path / "report.json"
    report_path.write_text(
        json.dumps(
            {
                "contract_version": publisher.ISOLATION_REPORT_CONTRACT,
                "max_isolated_regions": 3,
                "isolated_regions": ["Kent", "Sussex", "Surrey", "London"],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="exceeds"):
        publisher.isolated_regions_from_report(report_path)
