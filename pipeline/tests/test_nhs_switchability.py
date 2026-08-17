from __future__ import annotations

from external_sources.nhs_switchability import classify_support_worker


def test_generic_healthcare_support_worker_waits_for_criteria_review() -> None:
    result = classify_support_worker("Healthcare Support Worker")
    assert result.final_decision == "POSS"
    assert result.switchability == "BRIDGEABLE"


def test_training_language_can_clear_generic_support_worker() -> None:
    result = classify_support_worker(
        "Healthcare Support Worker",
        "No previous experience is required. Full training will be provided.",
    )
    assert result.final_decision == "HC"
    assert result.switchability == "OPEN_SWITCH"


def test_nhs_experience_essential_stays_possible_not_open_switch() -> None:
    result = classify_support_worker(
        "Healthcare Assistant",
        "Previous NHS experience is essential for this post.",
    )
    assert result.final_decision == "POSS"
    assert result.switchability == "NHS_EXPERIENCED"


def test_healthcare_experience_essential_stays_possible() -> None:
    result = classify_support_worker(
        "Support Worker",
        "Previous healthcare experience is required.",
    )
    assert result.final_decision == "POSS"
    assert result.switchability == "HEALTHCARE_EXPERIENCED"


def test_specialist_context_does_not_auto_clear() -> None:
    result = classify_support_worker("Mental Health Support Worker")
    assert result.final_decision == "POSS"
    assert result.switchability == "BRIDGEABLE"


def test_senior_support_title_is_hard_pass() -> None:
    result = classify_support_worker("Senior Healthcare Support Worker")
    assert result.final_decision == "HARD_PASS"
    assert result.switchability == "HARD_PASS"


def test_professional_registration_is_hard_pass() -> None:
    result = classify_support_worker(
        "Support Worker",
        "NMC registration is required.",
    )
    assert result.final_decision == "HARD_PASS"
    assert result.switchability == "HARD_PASS"
