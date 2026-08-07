from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"STOP: expected exactly one patch target in {path}; found {count}."
        )
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


poc = Path("pipeline/external_sources/teaching_vacancies_poc.py")

replace_once(
    poc,
    '''HARD = (\n    "teacher", "teaching assistant", "headteacher", "deputy head", "principal",\n    "lecturer", "social worker", "caretaker", "cleaner", "chef", "cook",\n    "technician", "therapist", "nurse", "counsellor", "coach", "site manager",\n    "premises manager", "midday supervisor",\n)\nREPORT_FIELDS = (\n''',
    '''HARD = (\n    "teacher", "teaching assistant", "headteacher", "deputy head", "principal",\n    "lecturer", "social worker", "caretaker", "cleaner", "chef", "cook",\n    "technician", "therapist", "nurse", "counsellor", "coach", "site manager",\n    "premises manager", "midday supervisor",\n)\nHC_TITLE_PREFIXES = (\n    "administration assistant",\n    "admin clerical officer",\n    "business administration operations assistant",\n)\nMANAGER_POSS_MAX_SALARY = 28_000\nREPORT_FIELDS = (\n''',
)

replace_once(
    poc,
    '''def classify(vacancy: Vacancy) -> tuple[str, str]:\n    title = normalise(vacancy.title)\n''',
    '''def annual_salary_ceiling(salary_text: str) -> float | None:\n    """Return the highest plausible annual £ amount stated in salary text."""\n    amounts: list[float] = []\n    for match in re.finditer(\n        r"£\\s*([0-9][0-9,]*(?:\\.[0-9]+)?)",\n        clean(salary_text),\n    ):\n        try:\n            amount = float(match.group(1).replace(",", ""))\n        except ValueError:\n            continue\n        # Ignore hourly rates and other small £ figures.\n        if amount >= 1_000:\n            amounts.append(amount)\n    return max(amounts) if amounts else None\n\n\ndef classify(vacancy: Vacancy) -> tuple[str, str]:\n    title = normalise(vacancy.title)\n''',
)

replace_once(
    poc,
    '''    hard_hits = [pattern for pattern in HARD if normalise(pattern) in title]\n    clear_hits = [pattern for pattern in HC if normalise(pattern) in title]\n    possible_hits = [pattern for pattern in POSS if normalise(pattern) in title]\n\n    if hard_hits and not clear_hits:\n        return "HARD_PASS", "Out-of-scope occupation: " + ", ".join(hard_hits)\n    if clear_hits:\n        return "HC", "Clear admin/service title: " + ", ".join(clear_hits)\n''',
    '''    hard_hits = [pattern for pattern in HARD if normalise(pattern) in title]\n    clear_hits = [pattern for pattern in HC if normalise(pattern) in title]\n    clear_prefix_hits = [\n        pattern for pattern in HC_TITLE_PREFIXES if title.startswith(pattern)\n    ]\n    possible_hits = [pattern for pattern in POSS if normalise(pattern) in title]\n\n    if hard_hits and not clear_hits and not clear_prefix_hits:\n        return "HARD_PASS", "Out-of-scope occupation: " + ", ".join(hard_hits)\n\n    if re.search(r"\\bmanager\\b", title):\n        ceiling = annual_salary_ceiling(vacancy.salary_text)\n        if ceiling is not None and ceiling < MANAGER_POSS_MAX_SALARY:\n            return (\n                "POSS",\n                "Manager title below £28,000 salary ceiling requires review",\n            )\n        if ceiling is None:\n            return (\n                "HARD_PASS",\n                "Manager title without salary evidence below £28,000",\n            )\n        return (\n            "HARD_PASS",\n            f"Manager title salary ceiling £{ceiling:,.0f} is not below £28,000",\n        )\n\n    if clear_hits or clear_prefix_hits:\n        hits = clear_hits + clear_prefix_hits\n        return "HC", "Clear admin/service title: " + ", ".join(hits)\n''',
)

regional_tests = Path("pipeline/tests/test_teaching_vacancies_regional_review.py")
text = regional_tests.read_text(encoding="utf-8")
marker = "def test_tv_refined_title_and_manager_salary_rules()"
if marker not in text:
    text = text.rstrip() + '''\n\n\ndef test_tv_refined_title_and_manager_salary_rules() -> None:\n    records = classify(\n        [\n            routed_row(\n                "admin-assistant",\n                title="Administration Assistant",\n                salary="£25,185 - £26,403",\n            ),\n            routed_row(\n                "senior-admin-assistant",\n                title="Senior Administration Assistant",\n                salary="£23,701 - £27,506",\n            ),\n            routed_row(\n                "clerical-officer",\n                title="Admin & Clerical Officer Level 2 Rowan School",\n                salary="£26,403 - £28,598 pro rata",\n            ),\n            routed_row(\n                "business-admin-ops",\n                title="Business Administration & Operations Assistant",\n                salary="£25,583 - £25,989",\n            ),\n            routed_row(\n                "low-manager",\n                title="Cover Manager",\n                salary="£18,867 - £21,152 Annually (Actual)",\n            ),\n            routed_row(\n                "high-manager",\n                title="Office Manager",\n                salary="£33,699 - £39,153 Annually (FTE)",\n            ),\n            routed_row(\n                "crossing-manager",\n                title="Office Manager",\n                salary="£27,521 - £29,362 Annually (Actual)",\n            ),\n            routed_row(\n                "grade-only-manager",\n                title="Business Manager",\n                salary="Grade 8, SCP 37-SCP 39",\n            ),\n        ]\n    )\n    by_id = {row.vacancy.source_job_id: row for row in records}\n\n    assert review.decision_for(by_id["admin-assistant"]) == "SELECTED"\n    assert review.decision_for(by_id["senior-admin-assistant"]) == "POSS"\n    assert review.decision_for(by_id["clerical-officer"]) == "SELECTED"\n    assert review.decision_for(by_id["business-admin-ops"]) == "SELECTED"\n    assert review.decision_for(by_id["low-manager"]) == "POSS"\n    assert review.decision_for(by_id["high-manager"]) == "HARD_PASS"\n    assert review.decision_for(by_id["crossing-manager"]) == "HARD_PASS"\n    assert review.decision_for(by_id["grade-only-manager"]) == "HARD_PASS"\n    assert (\n        by_id["high-manager"].vacancy.classification_reason\n        == "Manager title salary ceiling £39,153 is not below £28,000"\n    )\n''' + "\n"
    regional_tests.write_text(text, encoding="utf-8")
