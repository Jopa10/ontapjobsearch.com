# Barnsley admin and office jobs city-page review

- Parent regional page: `app/south-yorkshire/service-administrator-jobs.json`
- Live route: `/barnsley/service-administrator-jobs`
- Mode: `publish`
- Minimum live-job threshold: 6
- Effective included jobs: 2
- Threshold currently met: no

## How to review
Edit only the `action:` line inside a job block.
Use `action: exclude` to remove a current include, or `action: select` to include a review/exclude job.
Leave `action:` blank to accept the automatic decision. A blank review remains omitted from the live page.
Jobs are grouped include first, review second and exclude last, then alphabetically by title.
JobG8 identifiers are prefixed `jobg8-` in review files only; live job IDs are unchanged.

## Counts
- automatic include: 2
- automatic review: 0
- automatic exclude: 4
- effective include: 2
- effective review: 0
- effective exclude: 4

## INCLUDE (2)

---
action: 
decision: include
automatic_decision: include
title: Administrative Assistant
company: Garland House Surgery
location: Barnsley, S73 9JX
source: NHS Jobs
job_id: nhs-5295793
reason: Approved Barnsley catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Finance Assistant
company: PRATAP PARTNERSHIP LTD - Agency - Permanent
location: Barnsley
source: JobG8
job_id: jobg8-1908708
reason: Approved Barnsley catchment.
---

## REVIEW (0)

## EXCLUDE (4)

---
action: 
decision: exclude
automatic_decision: exclude
title: Business Support Officer
company: Rotherham Parents Forum Limited - Agency - Permanent
location: Rotherham
source: JobG8
job_id: jobg8-1892135
reason: Separate employment market.
---

---
action: 
decision: exclude
automatic_decision: exclude
title: Customer Service Advisor
company: EE - Company - Permanent
location: Doncaster
source: JobG8
job_id: jobg8-20279_62308-153faf593eb64b88272f45adeaa28d87
reason: Separate employment market.
---

---
action: 
decision: exclude
automatic_decision: exclude
title: Purchase Ledger Administrator
company: Sharp Consultancy - Agency - Permanent
location: Doncaster
source: JobG8
job_id: jobg8-1899982
reason: Separate employment market.
---

---
action: 
decision: exclude
automatic_decision: exclude
title: Receptionist
company: Totley Primary School
location: Sheffield
source: Teaching Vacancies
job_id: teaching-vacancies-receptionist-totley-primary-school
reason: Separate employment market.
---
