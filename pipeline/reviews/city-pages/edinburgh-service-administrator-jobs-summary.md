# Edinburgh admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/edinburgh-lothians/service-administrator-jobs.json`
- Live route: `/edinburgh/service-administrator-jobs`
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
- automatic review: 3
- automatic exclude: 0
- effective include: 4
- effective review: 3
- effective exclude: 0

## INCLUDE (4)

---
action: 
decision: include
automatic_decision: include
title: Administrator Reception
company: Reed - Agency - Permanent
location: Edinburgh
source: JobG8
job_id: jobg8-2063301
reason: Approved conservative Edinburgh launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Finance Assistant
company: Robert Half - Agency - Permanent
location: Edinburgh
source: JobG8
job_id: jobg8-1977269
reason: Approved conservative Edinburgh launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: HR Assistant
company: ICONIC RESOURCING LTD - Agency - Permanent
location: Edinburgh
source: JobG8
job_id: jobg8-1933959
reason: Approved conservative Edinburgh launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Paralegal
company: AWD online - Agency - Permanent
location: Edinburgh
source: JobG8
job_id: jobg8-2059086
reason: Approved conservative Edinburgh launch catchment.
---

## REVIEW (3)

---
action: 
decision: review
automatic_decision: review
title: HR Assistant
company: ICONIC RESOURCING LTD - Agency - Permanent
location: Tranent
source: JobG8
job_id: jobg8-1950430
reason: No approved Edinburgh catchment rule matched; local review required.
---

---
action: 
decision: review
automatic_decision: review
title: Logistics Coordinator
company: Owen Daniels - Agency - Permanent
location: Livingston
source: JobG8
job_id: jobg8-2051830
reason: No approved Edinburgh catchment rule matched; local review required.
---

---
action: 
decision: review
automatic_decision: review
title: Residential Conveyancing Paralegal
company: Reed - Agency - Permanent
location: North Berwick
source: JobG8
job_id: jobg8-2027323
reason: No approved Edinburgh catchment rule matched; local review required.
---

## EXCLUDE (0)
