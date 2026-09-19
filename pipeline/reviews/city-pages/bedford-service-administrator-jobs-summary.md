# Bedford admin and office jobs city-page review

- Parent regional page: `app/_city-pages/configured-slices/bedfordshire/service-administrator-jobs.json`
- Live route: `/bedford/service-administrator-jobs`
- Mode: `publish`
- Minimum live-job threshold: 4
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
title: Accounts Assistant / Bookkeper
company: The GK Group Limited - Agency - Permanent
location: Bedford
source: JobG8
job_id: jobg8-1876034
reason: Exact approved Bedford workplace.
---

---
action: 
decision: include
automatic_decision: include
title: Administrator (Learning & Development)
company: Tate Milton Keynes - Agency - Permanent
location: Bedford
source: JobG8
job_id: jobg8-1946950
reason: Exact approved Bedford workplace.
---

---
action: 
decision: include
automatic_decision: include
title: Receptionist
company: Sharnbrook Surgery
location: Bedford, MK44 1PZ
source: NHS Jobs
job_id: nhs-5608349
reason: Exact approved Bedford workplace.
---

## REVIEW (3)

---
action: 
decision: review
automatic_decision: review
title: Accounts Assistant
company: Reed - Agency - Permanent
location: Bedfordshire
source: JobG8
job_id: jobg8-1944217
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
title: Underwriting Support Administrator
company: Burton Recruitment - Agency - Permanent
location: Bedfordshire
source: JobG8
job_id: jobg8-1916041
reason: No exact Bedford workplace matched; local geographic review is required.
---

## EXCLUDE (0)
