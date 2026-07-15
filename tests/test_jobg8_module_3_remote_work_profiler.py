from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from pipeline.module3.engine import load_admin_register, load_daily_feeds
from pipeline.module3.rules import classify_remote


def decide(title: str, description: str):
    return classify_remote(title, description, "", "")


def test_fully_remote_data_protection_administrator():
    result = decide("Data Protection Administrator", "Data Protection Administrator. Fully Remote. Six-month contract.")
    assert result.classification == "FULLY_REMOTE_CONFIRMED"
    assert "Fully Remote" in result.evidence


def test_facilities_administrator_remote_home_based():
    result = decide("Facilities Administrator (Remote)", "Location: Home-Based. Working remotely, you will support the team.")
    assert result.classification == "FULLY_REMOTE_CONFIRMED"


def test_hybrid_accounts_administrator():
    result = decide("Accounts Administrator", "Hybrid working: three days from home and two days in the office.")
    assert result.classification == "HYBRID_OR_PARTIAL_REMOTE"
    assert result.routine_office_attendance == "yes"


def test_remote_after_probation():
    result = decide("HR Administrator", "Office based during probation. Remote working after probation has been completed.")
    assert result.classification == "REMOTE_AFTER_TRAINING_OR_PROBATION"


def test_remote_geographical_location_false_positive():
    assert decide("Head Receptionist", "This resort is in a remote location in the Scottish Highlands.").classification == "REMOTE_MENTION_FALSE_POSITIVE"


def test_managing_remote_team_false_positive():
    assert decide("Customer Account Administrator", "Office-based role supporting a remote customer service team.").classification == "REMOTE_MENTION_FALSE_POSITIVE"


def test_remote_tutor_training_false_positive():
    assert decide("Business Administrator Apprentice", "You will attend remote tutor-led training sessions once a month.").classification == "REMOTE_MENTION_FALSE_POSITIVE"


def test_explicitly_not_remote_overrides_keyword():
    assert decide("Administrator - Estate Agency / Lettings", "This is not a remote role. It is office based.").classification == "EXPLICITLY_NOT_REMOTE"


def test_wfh_allowance_is_not_remote_confirmation():
    result = decide("Academic Administrator", "Benefits include a working-from-home allowance for office equipment.")
    assert result.classification in {"REMOTE_MENTION_FALSE_POSITIVE", "AMBIGUOUS_REMOTE_REVIEW"}


def test_virtual_assistant_business_offer_is_not_vacancy():
    result = decide("Administrative Assistant (Work from Home, UK)", "Build your own successful Virtual Assistant business with our step-by-step programme. Charge clients per hour.")
    assert result.classification == "BUSINESS_OPPORTUNITY_OR_TRAINING"


def test_location_restricted_home_based_role():
    result = decide("Care Coordinator (Home-Based)", "Home-Based role. You must live within a 20-minute drive of Hull.")
    assert result.classification == "FULLY_REMOTE_LOCATION_RESTRICTED"
    assert result.scope == "LOCATION_RESTRICTED"


def test_remote_option_available():
    result = decide("Client Experience Coordinator", "Location: Remote, hybrid or office-based (Cottingham).")
    assert result.classification == "REMOTE_OPTION_AVAILABLE"
    assert result.routine_office_attendance == "no"


def test_senior_flag_keeps_remote_but_not_strict(tmp_path):
    path = tmp_path / "jobg8-2026-07-15.xlsx"
    register_path = tmp_path / "register.csv"
    pd.DataFrame([{"title": "Senior Administrator", "classification": "HIGH_CONFIDENCE", "reason": "test"}]).to_csv(register_path, index=False)
    pd.DataFrame([{"/Job/DisplayReference": "A1", "/Job/Position": "Senior Administrator", "/Job/Description": "Fully remote role across the UK.", "/Job/AdvertiserName": "Example Ltd"}]).to_excel(path, index=False)
    detail, _, _, _ = load_daily_feeds([(date(2026, 7, 15), path)], load_admin_register(register_path))
    assert bool(detail.iloc[0]["remote_admin_candidate"]) is True
    assert bool(detail.iloc[0]["strict_non_senior_candidate"]) is False


def test_negation_wins_over_positive_keyword():
    assert decide("Administrator", "Remote working is not available for this fully office-based role.").classification == "EXPLICITLY_NOT_REMOTE"


def test_daily_deduplication_counts_same_job_once(tmp_path):
    path = tmp_path / "jobg8-2026-07-15.xlsx"
    register_path = tmp_path / "register.csv"
    pd.DataFrame([{"title": "Administrator", "classification": "HIGH_CONFIDENCE", "reason": "test"}]).to_csv(register_path, index=False)
    duplicate = {"/Job/DisplayReference": "DUP-1", "/Job/Position": "Administrator", "/Job/Description": "Fully remote role.", "/Job/AdvertiserName": "Example Ltd"}
    pd.DataFrame([duplicate, duplicate]).to_excel(path, index=False)
    detail, daily, _, _ = load_daily_feeds([(date(2026, 7, 15), path)], load_admin_register(register_path))
    assert len(detail) == 1
    assert int(daily.iloc[0]["remote_admin_candidates"]) == 1
