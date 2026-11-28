# Hull admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/east-yorkshire/service-administrator-jobs.json`
- Live route: `/hull/service-administrator-jobs`
- Mode: `publish`
- Minimum live-job threshold: 6
- Effective included jobs: 4
- Threshold currently met: no

## How to review
Edit only the `action:` line inside a job block.
Use `action: exclude` to remove a current include, or `action: select` to include a review/exclude job.
Leave `action:` blank to accept the automatic decision. A blank review remains omitted from the live page.
Jobs are grouped include first, review second and exclude last, then alphabetically by title.
JobG8 identifiers are prefixed `jobg8-` in review files only; live job IDs are unchanged.

## Counts
- automatic include: 4
- automatic review: 4
- automatic exclude: 0
- effective include: 4
- effective review: 4
- effective exclude: 0

## INCLUDE (4)

---
action: 
decision: include
automatic_decision: include
title: Account Coordinator
company: Prestige Recruitment Specialists - Agency - Permanent
location: Hull
source: JobG8
job_id: jobg8-23643_225798510
reason: Approved conservative Hull launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Administrator
company: Hull University Teaching Hospitals NHS Trust
location: Hull, HU16 5JQ
source: NHS Jobs
job_id: nhs-5756114
reason: Approved conservative Hull launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Office Coordinator
company: Adecco - Agency - Permanent
location: Hull
source: JobG8
job_id: jobg8-23643_225875657
reason: Approved conservative Hull launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Treasury Administrator
company: GlobalData UK Ltd - Company - Permanent
location: Hull
source: JobG8
job_id: jobg8-23643_225818060
reason: Approved conservative Hull launch catchment.
---

## REVIEW (4)

---
action: 
decision: review
automatic_decision: review
title: Finance Assistant
company: Consortium Professional Recruitment Ltd - Agency - Permanent
location: Hessle
source: JobG8
job_id: jobg8-23643_225848634
reason: No approved Hull catchment rule matched; local review required.
---

---
action: 
decision: review
automatic_decision: review
title: Material & Logistics Planner
company: Rullion Limited - Agency - Temporary
location: Goole
source: JobG8
job_id: jobg8-108339348
reason: No approved Hull catchment rule matched; local review required.
---

---
action: 
decision: review
automatic_decision: review
title: Project Administrator
company: Consortium Professional Recruitment Ltd - Agency - Permanent
location: Brough
source: JobG8
job_id: jobg8-23643_225797818
reason: No approved Hull catchment rule matched; local review required.
---

---
action: 
decision: review
automatic_decision: review
title: Temporary Bookkeeper
company: KD Recruitment - Agency - Contract
location: Bridlington
source: JobG8
job_id: jobg8-23643_225788061
reason: No approved Hull catchment rule matched; local review required.
---

## EXCLUDE (0)
