from __future__ import annotations

from scripts import publish_verified_service_admin_pages as publisher


def test_service_admin_publisher_excludes_other_categories() -> None:
    mappings = publisher.service_admin_mappings()
    assert mappings
    assert all(mapping.category == "admin_service" for mapping in mappings)
    assert all("support-worker" not in str(mapping.destination) for mapping in mappings)
    assert any(mapping.region == "Yorkshire - North" for mapping in mappings)
