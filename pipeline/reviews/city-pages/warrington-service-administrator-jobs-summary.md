# Warrington admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/warrington-halton/service-administrator-jobs.json`
- Live route: `/warrington/service-administrator-jobs`
- Mode: `publish`
- Minimum live-job threshold: 6
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
- automatic review: 0
- automatic exclude: 2
- effective include: 3
- effective review: 0
- effective exclude: 2

## INCLUDE (3)

---
action: 
decision: include
automatic_decision: include
title: Bilingual Account Coordinator
company: Michael Page Business Support - Agency - Permanent
location: Warrington
source: JobG8
job_id: jobg8-1743227
reason: Approved conservative Warrington launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Business Support Officer
company: Hays Specialist Recruitment Limited - Agency - Permanent
location: Warrington
source: JobG8
job_id: jobg8-1733299
reason: Approved conservative Warrington launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Commercial Administrator
company: McLaren Resourcing - Agency - Permanent
location: Warrington
source: JobG8
job_id: jobg8-23643_225545989
reason: Approved conservative Warrington launch catchment.
---

## REVIEW (0)

## EXCLUDE (2)

---
action: 
decision: exclude
automatic_decision: exclude
title: Administrator
company: North Cheshire and Mersey NHS Foundation Trust (BCH)
location: Runcorn, WA7 1HB
source: NHS Jobs
job_id: nhs-5577899
reason: Separate employment market.
---

---
action: 
decision: exclude
automatic_decision: exclude
title: Data Entry & GP Liaison Administrator
company: MedPal AI Plc - Agency - Permanent
location: Runcorn
source: JobG8
job_id: jobg8-23643_225545347
reason: Separate employment market.
---
