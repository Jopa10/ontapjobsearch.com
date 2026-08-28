from pipeline.scripts.jobg8_refine_other_families import annualised_salary, salary_band


def test_salary_band_uses_annualised_midpoint_and_boundaries():
    assert salary_band("20000", "34999", "Annual") == "£20k–<£35k"
    assert salary_band("35000", "45000", "Annual") == "£35k–£45k"
    assert salary_band("45001", "", "Annual") == "Over £45k"


def test_salary_band_annualises_non_annual_pay():
    assert annualised_salary("15", "Hourly") == 29250
    assert salary_band("15", "", "Hourly") == "£20k–<£35k"


def test_salary_band_treats_five_figure_value_as_annual_despite_bad_period():
    assert annualised_salary("28000", "Weekly") == 28000
    assert salary_band("28000", "32000", "Weekly") == "£20k–<£35k"


def test_salary_band_combines_missing_and_below_20k():
    assert salary_band("", "", "") == "Below £20k / unknown"
    assert salary_band("18000", "19000", "Annual") == "Below £20k / unknown"
