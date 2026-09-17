# Bedford admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/bedfordshire/service-administrator-jobs.json`
- Live route: `/bedford/service-administrator-jobs`
- Mode: `publish`
- Minimum live-job threshold: 4
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
- automatic review: 4
- automatic exclude: 0
- effective include: 1
- effective review: 4
- effective exclude: 0

## INCLUDE (1)

---
action: 
decision: include
automatic_decision: include
title: Accounts Assistant / Bookkeper
company: The GK Group Limited - Agency - Permanent
location: Bedford
source: JobG8
job_id: jobg8-1876034
reason: Exact approved Bedford workplace.
---

## REVIEW (4)

---
action: 
decision: review
automatic_decision: review
title: Administrator
company: HUC
location: Luton, LU1 2SE
source: NHS Jobs
job_id: nhs-5603469
reason: No exact Bedford workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Early Careers Coordinator
company: BPHA - Agency - Permanent
location: Bedfordshire
source: JobG8
job_id: jobg8-1849342
reason: No exact Bedford workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Procurement Administrator
company: Cranfield University - Agency - Permanent
location: Bedfordshire
source: JobG8
job_id: jobg8-415093
reason: No exact Bedford workplace matched; local geographic review is required.
---

---
action: 
decision: review
automatic_decision: review
title: Secretary
company: Candidate Source - Agency - Permanent
location: Bedfordshire
source: JobG8
job_id: jobg8-107991156
reason: No exact Bedford workplace matched; local geographic review is required.
---

## EXCLUDE (0)
