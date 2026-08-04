# Teaching Vacancies ETL proof-of-concept review

review_date: 2026-08-04
review_fingerprint: 429a1d8f34eb4bd60289a81e7dcd432c788b73e5eb55fc1c06d98e66aa7033c1

Edit only the `action:` line in each editable block:

- For a POSS job, use `action: select` to add it or `action: exclude` to reject it.
- For a selected HC job, use `action: exclude` to remove it.
- Leave `action:` blank for no change.
- Commit the edit, then rerun the Teaching Vacancies process for the same review date.
- Decisions are matched by `source_job_id` and expire when the review date changes.

Run generated: 2026-08-04T15:14:25+01:00
Search input: https://teaching-vacancies.service.gov.uk/jobs — West Yorkshire, 20-mile radius
JobG8 comparison rows: 2

## Funnel

- Teaching Vacancies detail URLs discovered: 33
- Detail pages parsed successfully: 33
- Detail failures: 0
- West Yorkshire candidates retained: 12
- Outside or unmapped geography hard-passed: 21

## Detail diagnostics

- No unresolved detail-page failures.

## Review outcomes

- HC: 11
- POSS: 1
- Hard pass: 21
- Final selected after manual actions: 11
- Final POSS awaiting decision: 1
- Manually excluded: 0
- Confirmed JobG8 duplicates: 0
- Possible JobG8 duplicates: 0

## SELECTED

---
action: select
SELECTED | West Yorkshire | Leeds, Yorkshire and the Humber, LS12 5AW | B1 (SCP 4-6) £26,016 - £26,846, Actual Salary: £24,098 - £24,867 | Administrative Assistant
employer: Ryecroft Academy
closing_date: 2026-08-06T15:00:00+01:00
reason: Clear admin/service title: administrative assistant
source: Teaching Vacancies
source_job_id: administrative-assistant-74b028fb-5ae2-473b-9dd0-4cfe3d33f1dc
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-74b028fb-5ae2-473b-9dd0-4cfe3d33f1dc
---

---
action: select
SELECTED | West Yorkshire | Pudsey, Yorkshire and the Humber, LS28 7ND | £22,218.00 - £22,927.00 Annually (Actual) Term tiume plus 10 days. Your individual working pattern will be agreed with your line manager to ensure the operational needs of the school are met. | Administrative Assistant
employer: Pudsey Grammar School
closing_date: 2026-08-14T08:00:00+01:00
reason: Clear admin/service title: administrative assistant
source: Teaching Vacancies
source_job_id: administrative-assistant-pudsey-grammar-school-pudsey-west-yorkshire
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-pudsey-grammar-school-pudsey-west-yorkshire
---

---
action: exclude
SELECTED | West Yorkshire | Huddersfield, Yorkshire and the Humber, HD4 6JN | £28,262.00 - £30,199.00 Annually (Actual) Scale 6, SCP 18-22 (FTE £31,537 - £33,699), 37 Hours Per Week, Term Time Plus 10 Days | Exams Officer
employer: Newsome Academy
closing_date: 2026-08-10T09:00:00+01:00
reason: Clear admin/service title: exams officer
source: Teaching Vacancies
source_job_id: exams-officer-newsome-academy-huddersfield-west-yorkshire
source_url: https://teaching-vacancies.service.gov.uk/jobs/exams-officer-newsome-academy-huddersfield-west-yorkshire
---

---
action: exclude
SELECTED | West Yorkshire | Castleford, Yorkshire and the Humber, WF10 3JU | £27,915.00 - £30,377.00 Annually (Actual) Grade 7 SCP 19-23 Term Time + 5 Days | Personal Assistant to Headteacher
employer: Airedale Academy
closing_date: 2026-08-06T08:00:00+01:00
reason: Clear admin/service title: personal assistant
source: Teaching Vacancies
source_job_id: personal-assistant-to-headteacher-airedale-academy
source_url: https://teaching-vacancies.service.gov.uk/jobs/personal-assistant-to-headteacher-airedale-academy
---

---
action: select
SELECTED | West Yorkshire | Pontefract, Yorkshire and the Humber, WF8 4JF | £20,971.00 - £21,300.00 pro rata (£24,796.00 - £25,185.00 FTE)per annum | Receptionist
employer: The King's School
closing_date: 2026-08-31T10:00:00+01:00
reason: Clear admin/service title: receptionist
source: Teaching Vacancies
source_job_id: receptionist-the-king-s-school-pontefract-west-yorkshire
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-the-king-s-school-pontefract-west-yorkshire
---

---
action: select
SELECTED | West Yorkshire | Bradford, Yorkshire and the Humber, BD4 7RH | £25,989.00 - £28,142.00 Annually (FTE) Band 6, SCP 6 to SCP 11 (actual salary £22,350 - £24,202 per annum) | Receptionist/Administrator
employer: Oastlers School
closing_date: 2026-08-31T23:59:00+01:00
reason: Clear admin/service title: administrator, receptionist
source: Teaching Vacancies
source_job_id: receptionist-administrator-49a47934-628e-47bf-b7a9-6fe782d91f05
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-administrator-49a47934-628e-47bf-b7a9-6fe782d91f05
---

---
action: select
SELECTED | West Yorkshire | Otley, Yorkshire and the Humber, LS21 2HX | £21,196 | School Office Administrator
employer: Askwith Primary School
closing_date: 2026-09-17T09:00:00+01:00
reason: Clear admin/service title: administrator, office administrator
source: Teaching Vacancies
source_job_id: school-office-administrator-askwith-primary-school
source_url: https://teaching-vacancies.service.gov.uk/jobs/school-office-administrator-askwith-primary-school
---

---
action: exclude
SELECTED | West Yorkshire | Leeds, Yorkshire and the Humber, LS15 7NB | Grade: Level 1 A1/B1 | School Receptionist
employer: Cross Gates Primary School
closing_date: 2026-08-24T09:00:00+01:00
reason: Clear admin/service title: receptionist
source: Teaching Vacancies
source_job_id: school-receptionist-cross-gates-primary-school
source_url: https://teaching-vacancies.service.gov.uk/jobs/school-receptionist-cross-gates-primary-school
---

---
action: exclude
SELECTED | West Yorkshire | Halifax, Yorkshire and the Humber, HX2 9SU | £24,939.00 - £29,387.00 Annually (Actual) Term time plus 5 days | SEND & Exam Access Arrangements Administrator
employer: The North Halifax Grammar School
closing_date: 2026-09-03T12:00:00+01:00
reason: Clear admin/service title: administrator
source: Teaching Vacancies
source_job_id: send-exam-access-arrangements-administrator
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-exam-access-arrangements-administrator
---

---
action: select
SELECTED | West Yorkshire | Leeds, Yorkshire and the Humber, LS27 0AW | £21,043.00 - £22,429.00 Annually (Actual) | Senior Administrator
employer: Fountain Primary School
closing_date: 2026-09-14T09:00:00+01:00
reason: Clear admin/service title: administrator
source: Teaching Vacancies
source_job_id: senior-administrator-fountain-primary-school-leeds-west-yorkshire
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-administrator-fountain-primary-school-leeds-west-yorkshire
---

---
action: exclude
SELECTED | West Yorkshire | Bradford, Yorkshire and the Humber, BD13 5AD | £28,142.00 Annually (FTE) Band 7 – Point 11–17, 37 hours per week, term-time only + 5 days (39 weeks). £28,142 FTE (£24,314.688 actual) | Specialist Administrator (SEND, Medical, Lead First Aid)
employer: Parkside School
closing_date: 2026-08-31T23:59:00+01:00
reason: Clear admin/service title: administrator
source: Teaching Vacancies
source_job_id: specialist-administrator-send-medical-lead-first-aid
source_url: https://teaching-vacancies.service.gov.uk/jobs/specialist-administrator-send-medical-lead-first-aid
---


## POSS — choose SELECT or EXCLUDE

---
action:
POSS | West Yorkshire | Wakefield, WF2 0NP | £35,412.00 - £38,220.00 Annually (FTE) | Accomplish Hubs Business Manager, Castleford Office
employer: Accomplish Multi Academy Trust Limited
closing_date: 2026-08-20T23:59:00+01:00
reason: Borderline school administration title: business manager
source: Teaching Vacancies
source_job_id: accomplish-hubs-business-manager-castleford-office-accomplish-multi-academy-trust-limited
source_url: https://teaching-vacancies.service.gov.uk/jobs/accomplish-hubs-business-manager-castleford-office-accomplish-multi-academy-trust-limited
---


## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Administration Assistant and Receptionist](https://teaching-vacancies.service.gov.uk/jobs/administration-assistant-and-receptionist-king-edward-vii-school-sheffield-south-yorkshire) — No West Yorkshire location evidence.
- [Administrative Assistant](https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-harrogate-grove-road-community-primary-school-harrogate-north-yorkshire) — No West Yorkshire location evidence.
- [Administrative Assistant](https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-de44776f-dcb5-4d81-aa5e-7a81c54602f7) — No West Yorkshire location evidence.
- [Attendance Administrator](https://teaching-vacancies.service.gov.uk/jobs/attendance-administrator-kingsway-park-high-school) — No West Yorkshire location evidence.
- [Exams & Cover Officer](https://teaching-vacancies.service.gov.uk/jobs/exams-cover-officer-e-act-parkwood-academy) — No West Yorkshire location evidence.
- [EXAMS OFFICER (WITH ADMISSIONS RESPONSIBILITIES)](https://teaching-vacancies.service.gov.uk/jobs/exams-officer-with-admissions-responsibilities) — No West Yorkshire location evidence.
- [HR Administrator](https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-f587d299-5d24-4a3f-828b-04cf0952285e) — No West Yorkshire location evidence.
- [HR Administrator](https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-whalley-range-11-18-high-school) — No West Yorkshire location evidence.
- [HR Administrator](https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-parrs-wood-high-school) — No West Yorkshire location evidence.
- [Office Manager](https://teaching-vacancies.service.gov.uk/jobs/office-manager-doncaster-utc-doncaster) — No West Yorkshire location evidence.
- [Office Manager](https://teaching-vacancies.service.gov.uk/jobs/office-manager-rivington-and-blackrod-high-school-bolton-lancashire) — No West Yorkshire location evidence.
- [Pastoral Inclusion Administrator](https://teaching-vacancies.service.gov.uk/jobs/pastoral-inclusion-administrator-handsworth-grange-community-sports-college) — No West Yorkshire location evidence.
- [Receptionist & Administrator](https://teaching-vacancies.service.gov.uk/jobs/receptionist-administrator-sheffield-park-academy) — No West Yorkshire location evidence.
- [Receptionist & Administrator (42weeks)](https://teaching-vacancies.service.gov.uk/jobs/receptionist-administrator-42weeks) — No West Yorkshire location evidence.
- [Receptionist Administrator](https://teaching-vacancies.service.gov.uk/jobs/receptionist-administrator-aacf2c27-b21f-4e85-9276-550afc946a66) — No West Yorkshire location evidence.
- [SEND Administrative Assistant](https://teaching-vacancies.service.gov.uk/jobs/send-administrative-assistant-westfield-school-sheffield) — No West Yorkshire location evidence.
- [SEND Administrator](https://teaching-vacancies.service.gov.uk/jobs/send-administrator-aston-academy-sheffield-south-yorkshire) — No West Yorkshire location evidence.
- [Senior Administrative Officer](https://teaching-vacancies.service.gov.uk/jobs/senior-administrative-officer-manor-church-of-england-academy) — No West Yorkshire location evidence.
- [Sixth Form Supervisor and Administrator](https://teaching-vacancies.service.gov.uk/jobs/sixth-form-supervisor-and-administrator) — No West Yorkshire location evidence.
- [Sport Centre Receptionist](https://teaching-vacancies.service.gov.uk/jobs/sport-centre-receptionist-oldham-sixth-form-college) — No West Yorkshire location evidence.
- [Sport Centre Receptionist: Apprenticeship](https://teaching-vacancies.service.gov.uk/jobs/sport-centre-receptionist-apprenticeship) — No West Yorkshire location evidence.

## Safety boundary

- The process writes CSV and Markdown review outputs only.
- It has no command-line option or function that writes approved or live JSON.
- It does not change `pipeline/output-external`, `pipeline/output-admin-service`, or `app`.
- Only factual fields and a short classification excerpt are retained.
- Source attribution and the original Teaching Vacancies URL are preserved.
- HC/POSS rules are provisional and do not amend Ontap's permanent selection policy.
