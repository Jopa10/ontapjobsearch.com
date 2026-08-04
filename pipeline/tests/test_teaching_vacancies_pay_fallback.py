from external_sources.teaching_vacancies_etl import parse_jobposting


def test_visible_pay_scale_fallback_when_salary_is_not_stated():
    document = """
    <script type="application/ld+json">{
      "@context":"https://schema.org","@type":"JobPosting",
      "identifier":{"value":"school-receptionist-example"},
      "title":"School Receptionist",
      "hiringOrganization":{"name":"Cross Gates Primary School"},
      "jobLocation":{"address":{"addressLocality":"Leeds","addressRegion":"West Yorkshire","postalCode":"LS15 7NB"}},
      "datePosted":"2026-07-29","validThrough":"2026-08-24T09:00:00+01:00",
      "employmentType":"PART_TIME","description":"Reception and school office support."
    }</script>
    <h3>Pay scale</h3>
    <div>Grade: Level 1 A1/B1</div>
    """
    vacancy = parse_jobposting(
        document,
        "https://teaching-vacancies.service.gov.uk/jobs/school-receptionist-example",
    )
    assert vacancy.salary_text == "Grade: Level 1 A1/B1"
