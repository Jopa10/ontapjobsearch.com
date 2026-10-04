# Worcester admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/worcestershire/service-administrator-jobs.json`
- Live route: `/worcester/service-administrator-jobs`
- Mode: `publish`
- Minimum live-job threshold: 4
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
- automatic review: 6
- automatic exclude: 0
- effective include: 2
- effective review: 6
- effective exclude: 0

## INCLUDE (2)

---
action: 
decision: include
automatic_decision: include
title: Receptionist
company: Spring Gardens Group Medical Practice
location: Worcester, WR1 2BS
source: NHS Jobs
job_id: nhs-5633214
reason: Exact approved Worcester workplace.
---

---
action: 
decision: include
automatic_decision: include
title: Wedding & Events Co-ordinator
company: Four Squared - Agency - Permanent
location: Worcester
source: JobG8
job_id: jobg8-2055604
reason: Exact approved Worcester workplace.
---

## REVIEW (6)

---
action: 
decision: review
automatic_decision: review
title: Administrator (SEND Department)
company: Tenbury High Ormiston Academy
location: Tenbury Wells
source: Teaching Vacancies
job_id: teaching-vacancies-administrator-send-department-tenbury-high-ormiston-academy
reason: No exact Worcester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Care Coordinator
company: Agincare Group - Agency - Permanent
location: Worcestershire
source: JobG8
job_id: jobg8-108053865
reason: No exact Worcester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Finance Assistant
company: SF Partners - Agency - Permanent
location: Pershore
source: JobG8
job_id: jobg8-2045457
reason: No exact Worcester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Mortgage Administrator
company: Reed - Agency - Permanent
location: Bromsgrove
source: JobG8
job_id: jobg8-1980547
reason: No exact Worcester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Office Administrator
company: Stourport Primary Academy
location: Stourport-on-Severn
source: Teaching Vacancies
job_id: teaching-vacancies-office-administrator-stourport-primary-academy-stourport-on-severn-worcestershire
reason: No exact Worcester workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Receptionist/Administrator
company: Ipsley CofE Middle School
location: Redditch
source: Teaching Vacancies
job_id: teaching-vacancies-receptionist-administrator-ipsley-cofe-middle-school-redditch
reason: No exact Worcester workplace matched; local geographic review is required.
---

## EXCLUDE (0)
