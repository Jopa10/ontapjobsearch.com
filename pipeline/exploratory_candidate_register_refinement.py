#!/usr/bin/env python3
"""Apply evidence-led review refinements to exploratory candidate registers.

The initial builder deliberately casts a moderately wide net. This module then
uses complete-title meaning to remove specialist contamination, move explicit
customer-facing office titles into the customer-service family, and exclude
misleading care matches before Module 2 sees the registers.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

SELECTED = {"HIGH_CONFIDENCE", "ELASTIC_FIT"}


def has(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.I) for pattern in patterns)


def normalise_frame(df: pd.DataFrame) -> pd.DataFrame:
    required = [
        "title", "classification", "reason", "example_title",
        "july_occurrences", "days_present", "first_seen", "last_seen",
    ]
    for column in required:
        if column not in df.columns:
            df[column] = ""
    return df[required].copy()


def set_classification(df: pd.DataFrame, mask: pd.Series, classification: str, reason: str) -> None:
    df.loc[mask, "classification"] = classification
    df.loc[mask, "reason"] = reason


def refine_care(df: pd.DataFrame) -> pd.DataFrame:
    df = normalise_frame(df)
    titles = df["title"].astype(str)
    misleading_hearing = titles.str.contains(
        r"\b(hearing care|audiology|optical|optician)\b", case=False, regex=True
    )
    set_classification(
        df,
        misleading_hearing,
        "HARD_PASS",
        "Hearing, audiology or optical retail/clinical assistant role rather than hands-on personal care.",
    )
    qualified_clinical = titles.str.contains(
        r"\b(nurse|nursing associate|paramedic|therapist|practitioner|pharmac|dentist|social worker)\b",
        case=False,
        regex=True,
    ) & ~titles.str.contains(r"\bnursing assistant\b", case=False, regex=True)
    set_classification(
        df,
        qualified_clinical,
        "HARD_PASS",
        "Qualified clinical or professional role outside the care-assistant proposition.",
    )
    return df


def refine_teaching(df: pd.DataFrame) -> pd.DataFrame:
    df = normalise_frame(df)
    titles = df["title"].astype(str)
    coordinator = titles.str.contains(
        r"\bteaching assistant co-?ordinator\b", case=False, regex=True
    )
    set_classification(
        df,
        coordinator,
        "HARD_PASS",
        "Coordination of teaching assistants rather than an entry-level classroom-support role.",
    )
    return df


def refine_office(df: pd.DataFrame) -> pd.DataFrame:
    df = normalise_frame(df)
    titles = df["title"].astype(str)

    customer_family = titles.str.contains(
        r"\b(customer service|customer services|customer support|customer care|customer relations|"
        r"customer operations|customer administrator|call centre|contact centre|client services|"
        r"member services|complaints)\b",
        case=False,
        regex=True,
    )
    set_classification(
        df,
        customer_family,
        "HARD_PASS",
        "Explicit customer-facing role assessed in the broader customer-service family instead.",
    )

    specialist_patterns = [
        r"\bifa\b", r"\bwealth\b", r"\bpensions?\b", r"\bmortgage\b",
        r"\bfinance\b", r"\bfinancial\b", r"\baccounts?\b", r"\baccountancy\b",
        r"\bcredit\b", r"\binsolvenc", r"\bbank(ing)?\b", r"\btreasury\b",
        r"\bsettlement\b", r"\bpayments?\b", r"\bpayroll\b", r"\bbilling\b",
        r"\bloan\b", r"\binsurance\b", r"\bclaims?\b", r"\brisk\b",
        r"\bcompliance\b", r"\bregulatory\b", r"\bkyc\b", r"\baml\b",
        r"\bcompany secretary\b", r"\bconveyanc", r"\blegal\b",
        r"\bexport\b", r"\bimport\b", r"\bshipping\b", r"\binventory\b",
        r"\bpurchas", r"\bprocurement\b", r"\blogistics\b", r"\blogisitics\b",
        r"\bwarehouse\b", r"\bdespatch\b", r"\bdispatch\b", r"\bfleet\b",
        r"\btransport\b", r"\bdriver services\b", r"\bhr\b",
        r"\bhuman resources\b", r"\brecruit", r"\btalent\b", r"\breward\b",
        r"\bsales\b", r"\bmarketing\b", r"\bengineering\b", r"\btechnical\b",
        r"\bconstruction\b", r"\bclinical\b", r"\bcare coordinator\b",
        r"\bclient reporting\b",
    ]
    specialist = titles.apply(lambda value: has(value, specialist_patterns))
    set_classification(
        df,
        specialist,
        "HARD_PASS",
        "Specialist-domain administration is outside the broad general-office/reception proposition.",
    )
    return df


def refine_customer(customer: pd.DataFrame, office: pd.DataFrame) -> pd.DataFrame:
    customer = normalise_frame(customer)
    office = normalise_frame(office)

    source = pd.concat([customer, office], ignore_index=True)
    source = source.sort_values(
        ["july_occurrences", "days_present"], ascending=[False, False]
    ).drop_duplicates("title", keep="first")

    customer_signal = source["title"].astype(str).str.contains(
        r"\b(customer service|customer services|customer support|customer care|customer relations|"
        r"customer operations|customer administrator|call centre|contact centre|call handler|"
        r"client services|client support|member services|complaints)\b",
        case=False,
        regex=True,
    )
    result = source[customer_signal].copy()
    titles = result["title"].astype(str)

    excluded = titles.str.contains(
        r"\b(senior|manager|management|team leader|team lead|head of|director|supervisor|lead)\b",
        case=False,
        regex=True,
    ) | titles.str.contains(
        r"\b(sales|business development|account manager|account executive|collections|debt|"
        r"technical support|it support|service desk|helpdesk engineer|pensions?|wealth|finance|"
        r"financial|insurance|audiology|optical|transport|housing officer)\b",
        case=False,
        regex=True,
    )
    result["classification"] = "REVIEW_CONTEXT_DEPENDENT"
    result["reason"] = "Customer-facing wording is present but the complete title needs role-context review."
    set_classification(
        result,
        excluded,
        "HARD_PASS",
        "Senior, sales, technical or specialist-domain role outside general customer service.",
    )

    high = titles.str.contains(
        r"\b(customer service|customer services|customer support|customer care|customer relations|"
        r"call centre|contact centre|call handler|complaints)\b",
        case=False,
        regex=True,
    ) & titles.str.contains(
        r"\b(administrator|admin|associate|advisor|adviser|agent|representative|assistant|officer|handler)\b",
        case=False,
        regex=True,
    ) & ~excluded
    set_classification(
        result,
        high,
        "HIGH_CONFIDENCE",
        "Complete title clearly describes frontline customer/contact-centre service or complaints work.",
    )

    elastic = titles.str.contains(
        r"\b(customer operations|customer administrator|client services|client support|member services)\b",
        case=False,
        regex=True,
    ) & titles.str.contains(
        r"\b(administrator|admin|associate|advisor|adviser|agent|assistant|officer|coordinator)\b",
        case=False,
        regex=True,
    ) & ~excluded
    set_classification(
        result,
        elastic,
        "ELASTIC_FIT",
        "Adjacent customer/client/member-service role with clear non-sales service meaning.",
    )
    return result


def rewrite_manifest(registers_dir: Path, files: dict[str, str]) -> None:
    rows = []
    for category, filename in files.items():
        df = pd.read_csv(registers_dir / filename, dtype=str).fillna("")
        rows.append({
            "category": category,
            "register_file": filename,
            "titles_considered": len(df),
            "selected_titles": int(df["classification"].isin(SELECTED).sum()),
            "high_confidence_titles": int((df["classification"] == "HIGH_CONFIDENCE").sum()),
            "elastic_fit_titles": int((df["classification"] == "ELASTIC_FIT").sum()),
            "review_titles": int((df["classification"] == "REVIEW_CONTEXT_DEPENDENT").sum()),
            "hard_pass_titles": int((df["classification"] == "HARD_PASS").sum()),
        })
    pd.DataFrame(rows).to_csv(
        registers_dir / "category_manifest.csv", index=False, encoding="utf-8-sig"
    )


def run(registers_dir: Path) -> None:
    files = {
        "care_assistant_healthcare_assistant": "care_assistant_healthcare_assistant_candidate_register.csv",
        "teaching_sen_learning_support": "teaching_sen_learning_support_candidate_register.csv",
        "broader_customer_service": "broader_customer_service_candidate_register.csv",
        "broader_office_administration": "broader_office_administration_candidate_register.csv",
        "residential_childcare_children_support": "residential_childcare_children_support_candidate_register.csv",
        "warehouse_logistics_operative": "warehouse_logistics_operative_candidate_register.csv",
    }
    frames = {
        category: pd.read_csv(registers_dir / filename, dtype=str).fillna("")
        for category, filename in files.items()
    }

    frames["care_assistant_healthcare_assistant"] = refine_care(
        frames["care_assistant_healthcare_assistant"]
    )
    frames["teaching_sen_learning_support"] = refine_teaching(
        frames["teaching_sen_learning_support"]
    )
    original_office = frames["broader_office_administration"].copy()
    frames["broader_customer_service"] = refine_customer(
        frames["broader_customer_service"], original_office
    )
    frames["broader_office_administration"] = refine_office(original_office)

    for category, filename in files.items():
        frame = frames[category].sort_values(
            ["classification", "july_occurrences", "title"],
            ascending=[True, False, True],
        )
        frame.to_csv(registers_dir / filename, index=False, encoding="utf-8-sig")

    rewrite_manifest(registers_dir, files)
