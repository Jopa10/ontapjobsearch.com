# Belfast admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/northern-ireland-east/service-administrator-jobs.json`
- Live route: `/belfast/service-administrator-jobs`
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
- automatic review: 3
- automatic exclude: 0
- effective include: 3
- effective review: 3
- effective exclude: 0

## INCLUDE (3)

---
action: 
decision: include
automatic_decision: include
title: Band 3 Clerical Officer
company: Brook Street - Agency - Permanent
location: Belfast
source: JobG8
job_id: jobg8-1943100
reason: Approved conservative Belfast launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Financial Services Administrator
company: Brook Street - Agency - Permanent
location: Belfast
source: JobG8
job_id: jobg8-1942949
reason: Approved conservative Belfast launch catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Trainee Digital Marketing Manager No experience needed (Ref: 6901)
company: Qualify Nation Recruitment - Agency - Permanent
location: Belfast
source: JobG8
job_id: jobg8-1932507
reason: Approved conservative Belfast launch catchment.
---

## REVIEW (3)

---
action: 
decision: review
automatic_decision: review
title: Commercial Vehicles Administrator
company: Briggs Equipment Ltd - Agency - Permanent
location: Lisburn
source: JobG8
job_id: jobg8-107952610
reason: No approved Belfast catchment rule matched; local review required.
---

---
action: 
decision: review
automatic_decision: review
title: Contract Administrator
company: Manpower - Agency - Permanent
location: Ballyclare
source: JobG8
job_id: jobg8-1916549
reason: No approved Belfast catchment rule matched; local review required.
---

---
action: 
decision: review
automatic_decision: review
title: Sales Coordinator
company: Brook Street UK - Agency - Permanent
location: Ballyclare
source: JobG8
job_id: jobg8-107922303
reason: No approved Belfast catchment rule matched; local review required.
---

## EXCLUDE (0)
