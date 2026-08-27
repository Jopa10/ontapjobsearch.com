from __future__ import annotations

import sys

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
