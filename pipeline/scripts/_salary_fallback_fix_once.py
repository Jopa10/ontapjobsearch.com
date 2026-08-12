from pathlib import Path

path = Path('pipeline/scripts/service_admin_pipeline_core.py')
text = path.read_text(encoding='utf-8')
start = text.index('def extract_salary_from_description(raw_description: Any) -> str:\n')
end = text.index('def build_salary_details(row: pd.Series) -> tuple[str, str]:\n', start)

replacement = '''def extract_salary_from_description(raw_description: Any) -> str:
    """
    Secondary salary fallback for JobG8 rows where structured salary columns are blank.

    Safety rules:
    - prefer explicit £ amounts with a nearby pay period from /Job/Description;
    - also accept a tightly-scoped annual line such as "Up to 28,000" or
      "Salary: 32,500" when the whole line is only a salary statement;
    - never infer from similar roles, title, employer, or location;
    - return blank if no clear explicit salary phrase is present.
    """
    raw = norm(raw_description)
    if not raw:
        return ""

    cleaned = clean_description(raw)
    if not cleaned:
        return ""

    # Some JobG8 advertisers omit both the pound sign and pay-period field but
    # put a standalone annual salary statement in the advert body. Keep this
    # deliberately strict: the whole line must be salary-shaped, and values
    # without an explicit period need an "Up to" or "Salary" cue.
    annual_line = re.compile(
        r"^\\s*(?:(?P<salary>salary)\\s*:?\\s*)?"
        r"(?:(?P<prefix>up\\s+to|from)\\s+)?"
        r"(?P<amount>\\d{2,3}(?:,\\d{3})+)"
        r"(?:\\s*(?P<period>per\\s+annum|per\\s+year|a\\s+year|annually|annual|p\\.?a\\.?))?"
        r"\\s*$",
        flags=re.IGNORECASE,
    )
    for line in cleaned.splitlines():
        match = annual_line.match(line)
        if not match:
            continue
        if not match.group('period') and not (match.group('salary') or match.group('prefix')):
            continue
        amount_text = match.group('amount')
        amount_value = int(amount_text.replace(',', ''))
        if not 10_000 <= amount_value <= 250_000:
            continue
        prefix = (match.group('prefix') or '').lower()
        if prefix.startswith('up'):
            return f"Up to £{amount_text} per year"
        if prefix == 'from':
            return f"From £{amount_text} per year"
        return f"£{amount_text} per year"

    text = re.sub(r"\\s+", " ", cleaned).strip()
    if not text or "£" not in text:
        return ""

    amount = r"£\\s*\\d{1,3}(?:,\\d{3})*(?:\\.\\d{1,2})?"
    range_amount = rf"{amount}(?:\\s*(?:-|–|—|to)\\s*{amount})?"
    period = (
        r"(?:"
        r"per\\s+(?:hour|hr|annum|year|sleep[- ]?in|shift|week|month|day)"
        r"|an\\s+hour|a\\s+year"
        r"|p/?h|ph|hourly|annually|annual"
        r")"
    )
    salary_phrase = rf"{range_amount}\\s*(?:{period})"
    chained_salary_phrase = rf"{salary_phrase}(?:\\s*(?:\\+|and|plus)\\s*{salary_phrase})*"

    match = re.search(chained_salary_phrase, text, flags=re.IGNORECASE)
    if not match:
        return ""

    extracted = match.group(0).strip(" .;,:")
    extracted = re.sub(r"\\s+", " ", extracted)
    extracted = re.sub(r"£\\s+", "£", extracted)
    extracted = re.sub(r"\\bph\\b", "per hour", extracted, flags=re.IGNORECASE)
    extracted = re.sub(r"\\bp/h\\b", "per hour", extracted, flags=re.IGNORECASE)
    extracted = re.sub(r"\\bannually\\b", "per year", extracted, flags=re.IGNORECASE)
    extracted = re.sub(r"\\bannual\\b", "per year", extracted, flags=re.IGNORECASE)
    extracted = re.sub(r"\\ban hour\\b", "per hour", extracted, flags=re.IGNORECASE)
    extracted = re.sub(r"\\ba year\\b", "per year", extracted, flags=re.IGNORECASE)
    extracted = re.sub(r"sleep[ -]in", "sleep-in", extracted, flags=re.IGNORECASE)

    if "£" not in extracted:
        return ""
    if not re.search(r"\\b(per hour|per hr|per annum|per year|per sleep-in|per shift|per week|per month|per day|hourly)\\b", extracted, flags=re.IGNORECASE):
        return ""

    return fix_encoding(extracted)

'''

path.write_text(text[:start] + replacement + text[end:], encoding='utf-8')

test_path = Path('pipeline/tests/test_salary_description_fallback.py')
test_path.write_text('''import unittest\n\nfrom scripts import service_admin_pipeline_core as core\n\n\nclass SalaryDescriptionFallbackTests(unittest.TestCase):\n    def test_standalone_up_to_without_currency_is_annual_salary(self):\n        self.assertEqual(\n            core.extract_salary_from_description("Permanent role\\n\\nUp to 28,000\\n\\nBased in Bristol"),\n            "Up to £28,000 per year",\n        )\n\n    def test_salary_label_without_currency_is_annual_salary(self):\n        self.assertEqual(\n            core.extract_salary_from_description("Salary: 32,500"),\n            "£32,500 per year",\n        )\n\n    def test_non_salary_large_number_is_not_misread(self):\n        self.assertEqual(\n            core.extract_salary_from_description("We support up to 28,000 customers each year."),\n            "",\n        )\n\n    def test_small_up_to_number_is_not_misread_as_annual_salary(self):\n        self.assertEqual(core.extract_salary_from_description("Up to 500"), "")\n\n    def test_existing_explicit_currency_period_fallback_still_works(self):\n        self.assertEqual(\n            core.extract_salary_from_description("Pay is £14.50 per hour plus benefits"),\n            "£14.50 per hour",\n        )\n\n\nif __name__ == "__main__":\n    unittest.main()\n''', encoding='utf-8')
