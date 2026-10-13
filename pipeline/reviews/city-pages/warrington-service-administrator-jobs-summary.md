# Warrington admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/warrington-halton/service-administrator-jobs.json`
- Live route: `/warrington/service-administrator-jobs`
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
- automatic exclude: 1
- effective include: 5
- effective review: 1
- effective exclude: 1

## INCLUDE (5)

---
action: 
decision: include
automatic_decision: include
title: Accounts Assistant - Purchase Ledger
company: Adele Carr Recruitment Limited - Agency - Permanent
location: Warrington
source: JobG8
job_id: jobg8-2077982
reason: Approved conservative Warrington launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Assistant Accountant
company: Michael Page Finance - Agency - Permanent
location: Warrington
source: JobG8
job_id: jobg8-2060582
reason: Approved conservative Warrington launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Assistant Accountant
company: Reed - Agency - Permanent
location: Warrington
source: JobG8
job_id: jobg8-2042291
reason: Approved conservative Warrington launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Finance Assistant
company: Adecco - Agency - Permanent
location: Warrington
source: JobG8
job_id: jobg8-2039620
reason: Approved conservative Warrington launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Presenter and Content Creator
company: Reed - Agency - Permanent
location: Warrington
source: JobG8
job_id: jobg8-2048770
reason: Approved conservative Warrington launch catchment.
---

## REVIEW (1)

---
action: 
decision: review
automatic_decision: review
title: Medical Receptionist/Administrator
company: Newtown Surgery
location: Widnes, WA8 7GD
source: NHS Jobs
job_id: nhs-5651037
reason: No approved Warrington catchment rule matched; local review required.
---

## EXCLUDE (1)

---
action: 
decision: exclude
automatic_decision: exclude
title: Payroll Administrator
company: Portfolio Payroll - Agency - Permanent
location: Runcorn
source: JobG8
job_id: jobg8-2039669
reason: Separate employment market.
---
