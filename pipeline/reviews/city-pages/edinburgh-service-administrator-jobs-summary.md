# Edinburgh admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/edinburgh-lothians/service-administrator-jobs.json`
- Live route: `/edinburgh/service-administrator-jobs`
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
- automatic review: 2
- automatic exclude: 0
- effective include: 1
- effective review: 2
- effective exclude: 0

## INCLUDE (1)

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

## REVIEW (2)

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
title: Residential Conveyancing Paralegal
company: Reed - Agency - Permanent
location: North Berwick
source: JobG8
job_id: jobg8-2027323
reason: No approved Edinburgh catchment rule matched; local review required.
---

## EXCLUDE (0)
