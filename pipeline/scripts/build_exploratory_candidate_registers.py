#!/usr/bin/env python3
"""Build temporary July title registers for exploratory Ontap category discovery.

This script reads the archived daily JobG8 feeds, classifies complete job titles
against six candidate role families, and writes auditable temporary registers.
It does not modify production title registers or live pipeline outputs.
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path
from typing import Callable, Iterable, Optional

import pandas as pd

COL_JOB_ID = "/Job/DisplayReference"
COL_TITLE = "/Job/Position"

CATEGORIES = {
    "care_assistant_healthcare_assistant": "care_assistant_healthcare_assistant_candidate_register.csv",
    "teaching_sen_learning_support": "teaching_sen_learning_support_candidate_register.csv",
    "broader_customer_service": "broader_customer_service_candidate_register.csv",
    "broader_office_administration": "broader_office_administration_candidate_register.csv",
    "residential_childcare_children_support": "residential_childcare_children_support_candidate_register.csv",
    "warehouse_logistics_operative": "warehouse_logistics_operative_candidate_register.csv",
}

ROLE_LEVEL_EXCLUSIONS = [
    r"\bsenior\b", r"\bmanager\b", r"\bmanagement\b", r"\bteam leader\b",
    r"\bteam lead\b", r"\bhead of\b", r"\bdirector\b", r"\bsupervisor\b",
    r"\bdeputy\b", r"\bprincipal\b",
]


def norm_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def norm_key(value: object) -> str:
    return norm_text(value).lower()


def has(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.I) for pattern in patterns)


def excluded_level(text: str) -> bool:
    return has(text, ROLE_LEVEL_EXCLUSIONS)


def result(classification: str, reason: str) -> tuple[str, str]:
    return classification, reason


def classify_care(text: str) -> Optional[tuple[str, str]]:
    signal = has(text, [
        r"\bcare assistant\b", r"\bhealth\s*care assistant\b", r"\bcare worker\b",
        r"\bcarer\b", r"\bhome care\b", r"\bdomiciliary care\b",
        r"\bpersonal care assistant\b", r"\bnursing assistant\b",
        r"\bpatient care assistant\b", r"\bhealth\s*care support worker\b",
        r"\bclinical support worker\b", r"\bcomplex care assistant\b",
    ])
    if not signal:
        return None
    if has(text, [r"\bchildcare\b", r"\bchild care\b", r"\bchildren'?s residential\b", r"\bchildren'?s home\b"]):
        return result("HARD_PASS", "Children's residential role; assessed in the residential-childcare family instead.")
    if excluded_level(text):
        return result("HARD_PASS", "Senior, supervisory or management level falls outside the intended entry-level proposition.")
    if has(text, [
        r"\bnurse\b", r"\bnursing associate\b", r"\bsocial worker\b", r"\bdoctor\b",
        r"\bparamedic\b", r"\btherapist\b", r"\bpractitioner\b", r"\bpharmac",
        r"\bdent", r"\boptomet", r"\bpsycholog", r"\boccupational therapist\b",
    ]) and not has(text, [r"\bnursing assistant\b"]):
        return result("HARD_PASS", "Qualified or specialist clinical/professional role.")
    if has(text, [r"\bcoordinator\b", r"\badministrator\b", r"\brecruit", r"\bsales\b"]):
        return result("HARD_PASS", "Care-sector office/commercial role rather than hands-on assistant care work.")
    if has(text, [
        r"\bcare assistant\b", r"\bhealth\s*care assistant\b", r"\bcomplex care assistant\b",
        r"\bcare worker\b", r"\bdomiciliary care assistant\b", r"\bdomiciliary carer\b",
        r"\bhome care assistant\b", r"\bpersonal care assistant\b", r"\bnursing assistant\b",
        r"\bpatient care assistant\b",
    ]):
        return result("HIGH_CONFIDENCE", "Complete title clearly describes hands-on care-assistant or care-worker work.")
    if has(text, [r"\bhealth\s*care support worker\b", r"\bclinical support worker\b", r"\bhome carer\b", r"\bcarer\b"]):
        return result("ELASTIC_FIT", "Adjacent hands-on care role with clear care delivery meaning.")
    return result("REVIEW_CONTEXT_DEPENDENT", "Care wording is present but the complete title is not sufficiently specific.")


def classify_teaching(text: str) -> Optional[tuple[str, str]]:
    signal = has(text, [
        r"\bteaching assistant\b", r"\bteacher assistant\b", r"\blearning support\b",
        r"\bsen support\b", r"\bsend support\b", r"\bclassroom assistant\b",
        r"\bspecial needs assistant\b", r"\bhlta\b", r"\blearning mentor\b",
        r"\bbehavio[u]?r mentor\b", r"\bcover supervisor\b", r"\bpupil support\b",
        r"\beducation support\b", r"\bacademic support worker\b",
    ])
    if not signal:
        return None
    if excluded_level(text):
        return result("HARD_PASS", "Senior, supervisory or management level falls outside the intended entry-level proposition.")
    if has(text, [r"\bqualified teacher\b", r"\bclass teacher\b", r"\bschool teacher\b", r"\blecturer\b", r"\btutor\b", r"\bsenco\b", r"\beducational psychologist\b"]):
        return result("HARD_PASS", "Qualified teacher, tutor or education specialist rather than classroom support.")
    if has(text, [r"\bteaching assistant\b", r"\bteacher assistant\b", r"\blearning support assistant\b", r"\bsen support assistant\b", r"\bsend support assistant\b", r"\bclassroom assistant\b", r"\bspecial needs assistant\b"]):
        return result("HIGH_CONFIDENCE", "Complete title clearly describes teaching, SEN or classroom-assistant support.")
    if has(text, [r"\bhlta\b", r"\blearning mentor\b", r"\bbehavio[u]?r mentor\b", r"\bcover supervisor\b", r"\bpupil support assistant\b", r"\beducation support worker\b", r"\bacademic support worker\b"]):
        return result("ELASTIC_FIT", "Adjacent pupil-learning support role suitable for exploratory testing.")
    return result("REVIEW_CONTEXT_DEPENDENT", "Education-support wording is present but the role meaning remains ambiguous.")


def classify_customer_service(text: str) -> Optional[tuple[str, str]]:
    signal = has(text, [
        r"\bcustomer service\b", r"\bcustomer support\b", r"\bcustomer care\b",
        r"\bcall centre\b", r"\bcontact centre\b", r"\bcall handler\b",
        r"\bcustomer relations\b", r"\bcomplaints handler\b", r"\bmember services\b",
    ])
    if not signal:
        return None
    if excluded_level(text):
        return result("HARD_PASS", "Senior, supervisory or management level falls outside the intended entry-level proposition.")
    if has(text, [r"\bsales\b", r"\bbusiness development\b", r"\baccount manager\b", r"\baccount executive\b", r"\bcollections\b", r"\bdebt\b"]):
        return result("HARD_PASS", "Sales, account-management or collections role rather than service-led customer contact.")
    if has(text, [r"\bit support\b", r"\btechnical support\b", r"\bservice desk\b", r"\bhelpdesk engineer\b"]):
        return result("HARD_PASS", "Technical or IT support role rather than general customer service.")
    if has(text, [
        r"\bcustomer service (advisor|adviser|assistant|agent|representative|operative)\b",
        r"\bcustomer support (advisor|adviser|assistant|agent|representative)\b",
        r"\bcustomer care (advisor|adviser|assistant|agent)\b",
        r"\b(call|contact) centre (advisor|adviser|agent|operative|representative)\b",
        r"\bcall handler\b",
    ]):
        return result("HIGH_CONFIDENCE", "Complete title clearly describes frontline customer/contact-centre service work.")
    if has(text, [r"\bcomplaints handler\b", r"\bcustomer relations (advisor|adviser|assistant)\b", r"\bmember services (advisor|adviser|assistant)\b", r"\binbound customer\b"]):
        return result("ELASTIC_FIT", "Adjacent service-led customer contact role.")
    return result("REVIEW_CONTEXT_DEPENDENT", "Customer-service wording is present but the complete role meaning is not specific enough.")


def classify_office_admin(text: str) -> Optional[tuple[str, str]]:
    signal = has(text, [
        r"\badministrator\b", r"\badministration\b", r"\badmin assistant\b", r"\badministrative assistant\b",
        r"\breceptionist\b", r"\bsecretary\b", r"\bclerical\b", r"\bdata entry\b",
        r"\boffice assistant\b", r"\boffice coordinator\b", r"\bbooking coordinator\b",
        r"\bappointments coordinator\b", r"\bscheduling coordinator\b", r"\bproject coordinator\b",
        r"\bservice coordinator\b", r"\boperations coordinator\b",
    ])
    if not signal:
        return None
    if excluded_level(text):
        return result("HARD_PASS", "Senior, supervisory or management level falls outside the intended entry-level proposition.")
    specialist = has(text, [
        r"\baccounts?\b", r"\bfinance\b", r"\bpayroll\b", r"\bcredit control\b",
        r"\bhr\b", r"\bhuman resources\b", r"\brecruit", r"\blegal\b", r"\bconveyanc",
        r"\bsales\b", r"\bmarketing\b", r"\bprocurement\b", r"\bbuyer\b",
        r"\bwarehouse\b", r"\blogistics\b", r"\btransport\b", r"\bengineering\b",
        r"\btechnical\b", r"\bit\b", r"\bclinical\b", r"\bcare coordinator\b",
    ])
    if specialist and not has(text, [r"\breceptionist\b"]):
        return result("HARD_PASS", "Specialist-domain administration belongs outside the broad general-office proposition.")
    if has(text, [
        r"\boffice administrator\b", r"\bgeneral administrator\b", r"\badministrative assistant\b",
        r"\badmin assistant\b", r"\boffice assistant\b", r"\breceptionist\b",
        r"\bsecretary\b", r"\bclerical assistant\b", r"\bdata entry (clerk|administrator|assistant)\b",
    ]):
        return result("HIGH_CONFIDENCE", "Complete title clearly describes general office, reception or clerical administration.")
    if has(text, [
        r"\bproject administrator\b", r"\boperations administrator\b", r"\bscheduling coordinator\b",
        r"\bbooking coordinator\b", r"\bappointments coordinator\b", r"\boffice coordinator\b",
        r"\bservice coordinator\b", r"\bproject coordinator\b", r"\boperations coordinator\b",
        r"\badministrator\b",
    ]):
        return result("ELASTIC_FIT", "Broader office-based administrator or coordinator with no excluded specialist meaning.")
    return result("REVIEW_CONTEXT_DEPENDENT", "Office-administration signal is present but the title remains ambiguous.")


def classify_residential_childcare(text: str) -> Optional[tuple[str, str]]:
    signal = has(text, [
        r"\bchildren'?s residential\b", r"\bresidential child ?care\b", r"\bresidential care worker.*child",
        r"\bchildren'?s home\b", r"\bchildcare support worker\b", r"\bchildren'?s support worker\b",
        r"\bchild support worker\b", r"\byouth support worker\b", r"\bfamily support worker\b",
    ])
    if not signal:
        return None
    if excluded_level(text):
        return result("HARD_PASS", "Senior, supervisory or management level falls outside the intended entry-level proposition.")
    if has(text, [r"\bsocial worker\b", r"\bteacher\b", r"\bnurse\b", r"\btherapist\b", r"\bpractitioner\b"]):
        return result("HARD_PASS", "Qualified professional role rather than residential childcare support.")
    if has(text, [r"\bnursery\b", r"\bearly years\b", r"\bnanny\b", r"\bbabysitter\b"]) and not has(text, [r"\bresidential\b", r"\bchildren'?s home\b"]):
        return result("HARD_PASS", "Non-residential nursery or domestic childcare role.")
    if has(text, [
        r"\bresidential child ?care (worker|support worker)\b",
        r"\bchildren'?s residential support worker\b",
        r"\bresidential support worker.*child",
        r"\bchildren'?s home (support worker|care worker|worker)\b",
        r"\bsecure children'?s home support worker\b",
        r"\bnight support worker.*children'?s homes?\b",
    ]):
        return result("HIGH_CONFIDENCE", "Complete title clearly describes direct residential childcare or children's-home support.")
    if has(text, [r"\bchildren'?s support worker\b", r"\bchild support worker\b", r"\bchildcare support worker\b", r"\byouth support worker\b"]):
        return result("ELASTIC_FIT", "Direct children's support role, but residential setting is not always explicit.")
    return result("REVIEW_CONTEXT_DEPENDENT", "Children/family support wording is present without clear residential role meaning.")


def classify_warehouse(text: str) -> Optional[tuple[str, str]]:
    signal = has(text, [
        r"\bwarehouse\b", r"\blogistics operative\b", r"\bpick(er|ing)\b", r"\bpack(er|ing)\b",
        r"\bgoods in\b", r"\bgoods out\b", r"\bdespatch\b", r"\bdispatch\b",
        r"\bfulfilment\b", r"\bstockroom\b", r"\bstores operative\b", r"\bmaterial handler\b",
        r"\border picker\b",
    ])
    if not signal:
        return None
    if excluded_level(text):
        return result("HARD_PASS", "Senior, supervisory or management level falls outside the intended entry-level proposition.")
    if has(text, [r"\blogistics (coordinator|administrator|planner|analyst)\b", r"\bwarehouse administrator\b", r"\btransport planner\b"]):
        return result("HARD_PASS", "Logistics/warehouse office or specialist role rather than operative work.")
    if has(text, [r"\bhgv\b", r"\bdriver\b", r"\bcourier\b", r"\bdelivery\b"]) and not has(text, [r"\bwarehouse operative\b", r"\bwarehouse assistant\b"]):
        return result("HARD_PASS", "Driving/delivery role rather than warehouse-operative work.")
    if has(text, [
        r"\bwarehouse operative\b", r"\bwarehouse assistant\b", r"\bwarehouse worker\b",
        r"\bpickers?\s*(and|&|/)\s*packers?\b", r"\bpick(er|ing)\s*(and|&|/)\s*pack(er|ing)\b",
        r"\border picker\b", r"\bgoods (in|out) operative\b", r"\b(despatch|dispatch) operative\b",
        r"\bfulfilment operative\b", r"\bstockroom operative\b", r"\bstores operative\b",
        r"\blogistics operative\b",
    ]):
        return result("HIGH_CONFIDENCE", "Complete title clearly describes warehouse, picking/packing or logistics-operative work.")
    if has(text, [r"\bmaterial handler\b", r"\bwarehouse picker\b", r"\bwarehouse packer\b", r"\bgoods in assistant\b", r"\bstock controller\b"]):
        return result("ELASTIC_FIT", "Adjacent warehouse-handling or stock role suitable for exploratory testing.")
    return result("REVIEW_CONTEXT_DEPENDENT", "Warehouse/logistics wording is present but operative role meaning is ambiguous.")


CLASSIFIERS: dict[str, Callable[[str], Optional[tuple[str, str]]]] = {
    "care_assistant_healthcare_assistant": classify_care,
    "teaching_sen_learning_support": classify_teaching,
    "broader_customer_service": classify_customer_service,
    "broader_office_administration": classify_office_admin,
    "residential_childcare_children_support": classify_residential_childcare,
    "warehouse_logistics_operative": classify_warehouse,
}


def extract_date(path: Path) -> str:
    match = re.search(r"(20\d{2})[-_.](\d{2})[-_.](\d{2})", path.stem)
    return "-".join(match.groups()) if match else path.stem


def load_title_evidence(input_dir: Path) -> pd.DataFrame:
    records: list[dict] = []
    for path in sorted(input_dir.glob("*.xls*")):
        if path.name.startswith("~$"):
            continue
        date = extract_date(path)
        df = pd.read_excel(path, dtype=str).fillna("")
        if COL_TITLE not in df.columns:
            raise ValueError(f"{path} missing {COL_TITLE}")
        for index, row in df.iterrows():
            title = norm_text(row.get(COL_TITLE))
            if not title:
                continue
            job_id = norm_text(row.get(COL_JOB_ID)) if COL_JOB_ID in df.columns else f"{path.name}:{index+2}"
            records.append({"date": date, "job_id": job_id, "title": title, "title_key": norm_key(title)})
    if not records:
        raise RuntimeError(f"No usable titles found in {input_dir}")
    raw = pd.DataFrame(records).drop_duplicates(["date", "job_id", "title_key"])
    rows = []
    for title_key, group in raw.groupby("title_key"):
        examples = Counter(group["title"])
        rows.append({
            "title": title_key,
            "example_title": examples.most_common(1)[0][0],
            "july_occurrences": len(group),
            "days_present": group["date"].nunique(),
            "first_seen": group["date"].min(),
            "last_seen": group["date"].max(),
        })
    return pd.DataFrame(rows).sort_values(["july_occurrences", "title"], ascending=[False, True])


def run(input_dir: Path, output_dir: Path, detail_output: Path, month: str) -> None:
    evidence = load_title_evidence(input_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    detail_output.parent.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    detail_rows = []
    for category, filename in CATEGORIES.items():
        classifier = CLASSIFIERS[category]
        register_rows = []
        for row in evidence.to_dict("records"):
            classified = classifier(row["title"])
            if classified is None:
                continue
            classification, reason = classified
            output_row = {
                "title": row["title"],
                "classification": classification,
                "reason": reason,
                "example_title": row["example_title"],
                "july_occurrences": row["july_occurrences"],
                "days_present": row["days_present"],
                "first_seen": row["first_seen"],
                "last_seen": row["last_seen"],
            }
            register_rows.append(output_row)
            detail_rows.append({"month": month, "category": category, **output_row})
        register = pd.DataFrame(register_rows)
        if register.empty:
            register = pd.DataFrame(columns=["title", "classification", "reason", "example_title", "july_occurrences", "days_present", "first_seen", "last_seen"])
        register = register.sort_values(["classification", "july_occurrences", "title"], ascending=[True, False, True])
        register.to_csv(output_dir / filename, index=False, encoding="utf-8-sig")
        selected = register[register["classification"].isin(["HIGH_CONFIDENCE", "ELASTIC_FIT"])]
        manifest_rows.append({
            "category": category,
            "register_file": filename,
            "titles_considered": len(register),
            "selected_titles": len(selected),
            "high_confidence_titles": int((register["classification"] == "HIGH_CONFIDENCE").sum()),
            "elastic_fit_titles": int((register["classification"] == "ELASTIC_FIT").sum()),
            "review_titles": int((register["classification"] == "REVIEW_CONTEXT_DEPENDENT").sum()),
            "hard_pass_titles": int((register["classification"] == "HARD_PASS").sum()),
        })

    pd.DataFrame(manifest_rows).to_csv(output_dir / "category_manifest.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(detail_rows).sort_values(["category", "classification", "july_occurrences", "title"], ascending=[True, True, False, True]).to_csv(detail_output, index=False, encoding="utf-8-sig")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", required=True)
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--detail-output", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(Path(args.input_dir), Path(args.output_dir), Path(args.detail_output), args.month)
