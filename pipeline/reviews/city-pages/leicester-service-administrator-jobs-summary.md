# Leicester admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/leicestershire/service-administrator-jobs.json`
- Live route: `/leicester/service-administrator-jobs`
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
- automatic review: 1
- automatic exclude: 0
- effective include: 2
- effective review: 1
- effective exclude: 0

## INCLUDE (2)

---
action: 
decision: include
automatic_decision: include
title: Commercial Property Secretary
company: Allstaff Recruitment - Agency - Permanent
location: Leicester
source: JobG8
job_id: jobg8-1869342
reason: Exact approved Leicester workplace.
---

---
action: 
decision: include
automatic_decision: include
title: Part Time Accounts Assistant
company: Macildowie Recruitment and Retention - Agency - Permanent
location: Leicester
source: JobG8
job_id: jobg8-1936448
reason: Exact approved Leicester workplace.
---

## REVIEW (1)

---
action: 
decision: review
automatic_decision: review
title: Accounts Payable Co-ordinator
company: Mixxos Group - Agency - Permanent
location: Leicestershire
source: JobG8
job_id: jobg8-1908964
reason: No exact Leicester workplace matched; local geographic review is required.
---

## EXCLUDE (0)
