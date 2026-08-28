# Warrington admin and customer-service jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/warrington-halton/service-administrator-jobs.json`
- Live route: `/warrington/service-administrator-jobs`
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
- automatic exclude: 3
- effective include: 2
- effective review: 0
- effective exclude: 3

## INCLUDE (2)

---
action: 
decision: include
automatic_decision: include
title: Sales Coordinator - Architecture
company: Locker Group Ltd - Agency - Permanent
location: Warrington
source: JobG8
job_id: jobg8-107709595
reason: Approved conservative Warrington launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Support Coordinator
company: Creative Support - Agency - Permanent
location: Warrington
source: JobG8
job_id: jobg8-107907094
reason: Approved conservative Warrington launch catchment.
---

## REVIEW (0)

## EXCLUDE (3)

---
action: 
decision: exclude
automatic_decision: exclude
title: Accounts Administrator
company: Building Careers UK Ltd - Agency - Permanent
location: Runcorn
source: JobG8
job_id: jobg8-107752866
reason: Separate employment market.
---

---
action: 
decision: exclude
automatic_decision: exclude
title: Administration Assistant
company: Mersey Care NHS Foundation Trust
location: Runcorn, WA7 2DA
source: NHS Jobs
job_id: nhs-5567496
reason: Separate employment market.
---

---
action: 
decision: exclude
automatic_decision: exclude
title: Finance Assistant
company: MedPal AI Plc - Agency - Permanent
location: Runcorn
source: JobG8
job_id: jobg8-107824915
reason: Separate employment market.
---
