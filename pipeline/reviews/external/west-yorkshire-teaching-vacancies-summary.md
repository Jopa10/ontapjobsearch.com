# West Yorkshire Teaching Vacancies ETL proof-of-concept review

review_date: 2026-08-04
review_fingerprint: 285fdb36fffdd380c71762e322d6cef33ed4e531d418c22333d4e55ba827a426

Edit only the `action:` line in each editable block:

- For a POSS job, use `action: select` to add it or `action: exclude` to reject it.
- For a selected HC job, use `action: exclude` to remove it.
- Leave `action:` blank for no change.
- Commit the edit, then rerun the Teaching Vacancies process for the same review date.
- Decisions are matched by `source_job_id` and expire when the review date changes.

Run generated: 2026-08-04T14:21:52+01:00
Search input: https://teaching-vacancies.service.gov.uk/jobs — West Yorkshire, 20-mile radius
JobG8 comparison rows: 2

## Funnel

- Teaching Vacancies detail URLs discovered: 21
- Detail pages parsed successfully: 21
- Detail failures: 0
- West Yorkshire candidates retained: 7
- Outside or unmapped geography hard-passed: 14

## Detail diagnostics

- No unresolved detail-page failures.

## Review outcomes

- HC: 6
- POSS: 1
- Hard pass: 14
- Final selected after manual actions: 6
- Final POSS awaiting decision: 1
- Manually excluded: 0
- Confirmed JobG8 duplicates: 0
- Possible JobG8 duplicates: 0

## SELECTED

---
action:
SELECTED | West Yorkshire | Huddersfield, Yorkshire and the Humber, HD4 6JN | Not stated | Exams Officer
employer: Newsome Academy
closing_date: 2026-08-10T09:00:00+01:00
reason: Clear admin/service title: exams officer
source: Teaching Vacancies
source_job_id: exams-officer-newsome-academy-huddersfield-west-yorkshire
source_url: https://teaching-vacancies.service.gov.uk/jobs/exams-officer-newsome-academy-huddersfield-west-yorkshire
---

---
action:
SELECTED | West Yorkshire | Pontefract, Yorkshire and the Humber, WF8 4JF | Not stated | Receptionist
employer: The King's School
closing_date: 2026-08-31T10:00:00+01:00
reason: Clear admin/service title: receptionist
source: Teaching Vacancies
source_job_id: receptionist-the-king-s-school-pontefract-west-yorkshire
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-the-king-s-school-pontefract-west-yorkshire
---

---
action:
SELECTED | West Yorkshire | Otley, Yorkshire and the Humber, LS21 2HX | Not stated | School Office Administrator
employer: Askwith Primary School
closing_date: 2026-09-17T09:00:00+01:00
reason: Clear admin/service title: administrator, office administrator
source: Teaching Vacancies
source_job_id: school-office-administrator-askwith-primary-school
source_url: https://teaching-vacancies.service.gov.uk/jobs/school-office-administrator-askwith-primary-school
---

---
action:
SELECTED | West Yorkshire | Halifax, Yorkshire and the Humber, HX2 9SU | Not stated | SEND & Exam Access Arrangements Administrator
employer: The North Halifax Grammar School
closing_date: 2026-09-03T12:00:00+01:00
reason: Clear admin/service title: administrator
source: Teaching Vacancies
source_job_id: send-exam-access-arrangements-administrator
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-exam-access-arrangements-administrator
---

---
action:
SELECTED | West Yorkshire | Leeds, Yorkshire and the Humber, LS27 0AW | Not stated | Senior Administrator
employer: Fountain Primary School
closing_date: 2026-09-14T09:00:00+01:00
reason: Clear admin/service title: administrator
source: Teaching Vacancies
source_job_id: senior-administrator-fountain-primary-school-leeds-west-yorkshire
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-administrator-fountain-primary-school-leeds-west-yorkshire
---

---
action:
SELECTED | West Yorkshire | Bradford, Yorkshire and the Humber, BD13 5AD | Not stated | Specialist Administrator (SEND, Medical, Lead First Aid)
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
POSS | West Yorkshire | Wakefield, WF2 0NP | Not stated | Accomplish Hubs Business Manager, Castleford Office
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
- [Attendance Administrator](https://teaching-vacancies.service.gov.uk/jobs/attendance-administrator-kingsway-park-high-school) — No West Yorkshire location evidence.
- [Exams & Cover Officer](https://teaching-vacancies.service.gov.uk/jobs/exams-cover-officer-e-act-parkwood-academy) — No West Yorkshire location evidence.
- [EXAMS OFFICER (WITH ADMISSIONS RESPONSIBILITIES)](https://teaching-vacancies.service.gov.uk/jobs/exams-officer-with-admissions-responsibilities) — No West Yorkshire location evidence.
- [HR Administrator](https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-f587d299-5d24-4a3f-828b-04cf0952285e) — No West Yorkshire location evidence.
- [Office Manager](https://teaching-vacancies.service.gov.uk/jobs/office-manager-doncaster-utc-doncaster) — No West Yorkshire location evidence.
- [Office Manager](https://teaching-vacancies.service.gov.uk/jobs/office-manager-rivington-and-blackrod-high-school-bolton-lancashire) — No West Yorkshire location evidence.
- [Pastoral Inclusion Administrator](https://teaching-vacancies.service.gov.uk/jobs/pastoral-inclusion-administrator-handsworth-grange-community-sports-college) — No West Yorkshire location evidence.
- [Receptionist & Administrator](https://teaching-vacancies.service.gov.uk/jobs/receptionist-administrator-sheffield-park-academy) — No West Yorkshire location evidence.
- [Receptionist & Administrator (42weeks)](https://teaching-vacancies.service.gov.uk/jobs/receptionist-administrator-42weeks) — No West Yorkshire location evidence.
- [Receptionist Administrator](https://teaching-vacancies.service.gov.uk/jobs/receptionist-administrator-aacf2c27-b21f-4e85-9276-550afc946a66) — No West Yorkshire location evidence.
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
