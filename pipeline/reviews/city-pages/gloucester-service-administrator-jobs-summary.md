# Gloucester admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/gloucestershire/service-administrator-jobs.json`
- Live route: `/gloucester/service-administrator-jobs`
- Mode: `publish`
- Minimum live-job threshold: 4
- Effective included jobs: 3
- Threshold currently met: no

## How to review
Edit only the `action:` line inside a job block.
Use `action: exclude` to remove a current include, or `action: select` to include a review/exclude job.
Leave `action:` blank to accept the automatic decision. A blank review remains omitted from the live page.
Jobs are grouped include first, review second and exclude last, then alphabetically by title.
JobG8 identifiers are prefixed `jobg8-` in review files only; live job IDs are unchanged.

## Counts
- automatic include: 3
- automatic review: 6
- automatic exclude: 0
- effective include: 3
- effective review: 6
- effective exclude: 0

## INCLUDE (3)

---
action: 
decision: include
automatic_decision: include
title: Accounts Assistant
company: Morgan McKinley - Agency - Permanent
location: Gloucester
source: JobG8
job_id: jobg8-2067302
reason: Exact approved Gloucester workplace.
---

---
action: 
decision: include
automatic_decision: include
title: Salesforce Administrator
company: UBT - Agency - Permanent
location: Gloucester
source: JobG8
job_id: jobg8-2085791
reason: Exact approved Gloucester workplace.
---

---
action: 
decision: include
automatic_decision: include
title: School Administrator
company: St James' Church of England Junior School
location: Gloucester
source: Teaching Vacancies
job_id: teaching-vacancies-school-administrator-st-james-church-of-england-junior-school
reason: Exact approved Gloucester workplace.
---

## REVIEW (6)

---
action: 
decision: review
automatic_decision: review
title: Accounts Assistant
company: Reed - Agency - Permanent
location: Gloucestershire
source: JobG8
job_id: jobg8-2050223
reason: No exact Gloucester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Administrative Assistant
company: Prospectus - Agency - Permanent
location: Cheltenham
source: JobG8
job_id: jobg8-2092958
reason: No exact Gloucester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Administrator
company: Right Now Group - Agency - Permanent
location: Gloucestershire
source: JobG8
job_id: jobg8-2053465
reason: No exact Gloucester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Marketing & Communications Executive
company: UK Electronics Skills Foundation - Agency - Permanent
location: Cirencester
source: JobG8
job_id: jobg8-2099929
reason: No exact Gloucester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Payroll Administrator
company: Robert Half - Agency - Permanent
location: Gloucestershire
source: JobG8
job_id: jobg8-2039522
reason: No exact Gloucester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Team Administrator
company: Gloucestershire Health and Care NHS Foundation Trust
location: Stroud, GL5 2HZ
source: NHS Jobs
job_id: nhs-5649232
reason: No exact Gloucester workplace matched; local geographic review is required.
---

## EXCLUDE (0)
