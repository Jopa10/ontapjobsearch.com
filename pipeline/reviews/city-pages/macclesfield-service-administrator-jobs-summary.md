# Macclesfield admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/cheshire-east/service-administrator-jobs.json`
- Live route: `/macclesfield/service-administrator-jobs`
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
- automatic review: 4
- automatic exclude: 0
- effective include: 2
- effective review: 4
- effective exclude: 0

## INCLUDE (2)

---
action: 
decision: include
automatic_decision: include
title: Graduate Town Planner
company: Penguin Recruitment Ltd - Agency - Permanent
location: Macclesfield
source: JobG8
job_id: jobg8-2064949
reason: Exact approved Macclesfield workplace.
---

---
action: 
decision: include
automatic_decision: include
title: Graduate Town Planner
company: Penguin Recruitment Ltd - Agency - Permanent
location: Macclesfield
source: JobG8
job_id: jobg8-2066069
reason: Exact approved Macclesfield workplace.
---

## REVIEW (4)

---
action: 
decision: review
automatic_decision: review
title: Admin Assistant
company: Cygnet Health Care
location: Crewe, CW1 4QW
source: NHS Jobs
job_id: nhs-5637351
reason: No exact Macclesfield workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Part-Time Payroll Assistant
company: Adele Carr Recruitment Limited - Agency - Permanent
location: Wilmslow
source: JobG8
job_id: jobg8-2039760
reason: No exact Macclesfield workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: School Office Administrator
company: Highfields Academy
location: Nantwich
source: Teaching Vacancies
job_id: teaching-vacancies-school-office-administrator-highfields-academy
reason: No exact Macclesfield workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Supply Chain Coordinator
company: Shorterm Group - Agency - Permanent
location: Crewe
source: JobG8
job_id: jobg8-2065127
reason: No exact Macclesfield workplace matched; local geographic review is required.
---

## EXCLUDE (0)
