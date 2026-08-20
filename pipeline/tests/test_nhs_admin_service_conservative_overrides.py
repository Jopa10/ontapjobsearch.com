from __future__ import annotations

from external_sources import nhs_admin_service as nhs


def test_poss_overrides_can_safely_downgrade_hc_registry_titles() -> None:
    assert nhs.classify_title("Network Administrator")[0:2] == ("POSS", "BRIDGEABLE")
    assert nhs.classify_title("SQL Database Administrator")[0:2] == ("POSS", "BRIDGEABLE")
    assert nhs.classify_title("Business Support Manager")[0:2] == ("POSS", "BRIDGEABLE")
    assert nhs.classify_title("Administrator and Health Care Support Worker")[0:2] == ("POSS", "BRIDGEABLE")
    assert nhs.classify_title("Medical Receptionist Team Lead")[0:2] == ("POSS", "BRIDGEABLE")


def test_clear_admin_titles_remain_auto_selected() -> None:
    assert nhs.classify_title("Administrator")[0:2] == ("HC", "OPEN_SWITCH")
    assert nhs.classify_title("Medical Receptionist")[0:2] == ("HC", "OPEN_SWITCH")
