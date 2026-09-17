# Sheffield admin and office jobs city-page review

- Parent regional page: `app/south-yorkshire/service-administrator-jobs.json`
- Live route: `/sheffield/service-administrator-jobs`
- Mode: `publish`
- Minimum live-job threshold: 6
- Effective included jobs: 1
- Threshold currently met: no

## How to review
Edit only the `action:` line inside a job block.
Use `action: exclude` to remove a current include, or `action: select` to include a review/exclude job.
Leave `action:` blank to accept the automatic decision. A blank review remains omitted from the live page.
Jobs are grouped include first, review second and exclude last, then alphabetically by title.
JobG8 identifiers are prefixed `jobg8-` in review files only; live job IDs are unchanged.

## Counts
- automatic include: 1
- automatic review: 0
- automatic exclude: 5
- effective include: 1
- effective review: 0
- effective exclude: 5

## INCLUDE (1)

---
action: 
decision: include
automatic_decision: include
title: Receptionist
company: Totley Primary School
location: Sheffield
source: Teaching Vacancies
job_id: teaching-vacancies-receptionist-totley-primary-school
reason: Approved Sheffield catchment.
---

## REVIEW (0)

## EXCLUDE (5)

---
action: 
decision: exclude
automatic_decision: exclude
title: Administrative Assistant
company: Garland House Surgery
location: Barnsley, S73 9JX
source: NHS Jobs
job_id: nhs-5295793
reason: Separate employment market.
---

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
title: Finance Assistant
company: PRATAP PARTNERSHIP LTD - Agency - Permanent
location: Barnsley
source: JobG8
job_id: jobg8-1908708
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
