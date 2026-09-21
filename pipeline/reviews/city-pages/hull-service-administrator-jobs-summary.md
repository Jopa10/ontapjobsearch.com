# Hull admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/east-yorkshire/service-administrator-jobs.json`
- Live route: `/hull/service-administrator-jobs`
- Mode: `publish`
- Minimum live-job threshold: 6
- Effective included jobs: 5
- Threshold currently met: no

## How to review
Edit only the `action:` line inside a job block.
Use `action: exclude` to remove a current include, or `action: select` to include a review/exclude job.
Leave `action:` blank to accept the automatic decision. A blank review remains omitted from the live page.
Jobs are grouped include first, review second and exclude last, then alphabetically by title.
JobG8 identifiers are prefixed `jobg8-` in review files only; live job IDs are unchanged.

## Counts
- automatic include: 5
- automatic review: 1
- automatic exclude: 0
- effective include: 5
- effective review: 1
- effective exclude: 0

## INCLUDE (5)

---
action: 
decision: include
automatic_decision: include
title: Administrator
company: Hull University Teaching Hospitals NHS Trust
location: Hull, HU1 3TD
source: NHS Jobs
job_id: nhs-5595156
reason: Approved conservative Hull launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Quotations & Estimating Coordinator
company: KD Recruitment Limited - Agency - Permanent
location: Hull
source: JobG8
job_id: jobg8-107894712
reason: Approved conservative Hull launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Receptionist Administrator
company: Alderman Cogan's Church of England Primary Academy
location: Hull
source: Teaching Vacancies
job_id: teaching-vacancies-receptionist-administrator-8983c99a-ea81-4d03-945c-21a86c87cb36
reason: Approved conservative Hull launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: SEND Administrator
company: Liberty Academy
location: Hull
source: Teaching Vacancies
job_id: teaching-vacancies-send-administrator-liberty-academy
reason: Approved conservative Hull launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Warranties Administrator - Automotive
company: Office Angels - Agency - Permanent
location: Hull
source: JobG8
job_id: jobg8-1939826
reason: Approved conservative Hull launch catchment.
---

## REVIEW (1)

---
action: 
decision: review
automatic_decision: review
title: Sourcing Coordinator
company: REC-REVOLUTION LTD - Agency - Permanent
location: Bridlington
source: JobG8
job_id: jobg8-107952027
reason: No approved Hull catchment rule matched; local review required.
---

## EXCLUDE (0)
