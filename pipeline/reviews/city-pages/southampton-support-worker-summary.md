# Southampton support worker jobs city-page review

- Parent regional page: `app/hampshire/support-worker.json`
- Live route: `/southampton/support-worker`
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
- automatic exclude: 3
- effective include: 4
- effective review: 3
- effective exclude: 3

## INCLUDE (4)

---
action: 
decision: include
automatic_decision: include
title: Healthcare Assistant
company: Thema Healthcare - Agency - Permanent
location: Southampton
source: JobG8
job_id: jobg8-1958886
reason: Approved Southampton catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Part-Time Support Worker
company: Cygnet - Agency - Permanent
location: Southampton
source: JobG8
job_id: jobg8-1932858
reason: Approved Southampton catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Support Worker (Days)
company: Cygnet - Agency - Permanent
location: Southampton
source: JobG8
job_id: jobg8-1898106
reason: Approved Southampton catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Support Worker (Learning Disabilities)
company: Cygnet - Agency - Permanent
location: Southampton
source: JobG8
job_id: jobg8-1856912
reason: Approved Southampton catchment.
---

## REVIEW (3)

---
action: 
decision: review
automatic_decision: review
title: Children's Home Support Worker
company: Hampshire County Council - Company - Permanent
location: Romsey
source: JobG8
job_id: jobg8-1401785505
reason: Broad location; review before city inclusion.
---

---
action: 
decision: review
automatic_decision: review
title: Children's Homes Support Worker
company: Hampshire County Council - Company - Permanent
location: Romsey
source: JobG8
job_id: jobg8-1401785354
reason: Broad location; review before city inclusion.
---

---
action: 
decision: review
automatic_decision: review
title: Healthcare Assistant
company: Advantage Angels Ltd - Agency - Contract
location: Ryde
source: JobG8
job_id: jobg8-107856243
reason: No approved Southampton catchment rule matched; local review required.
---

## EXCLUDE (3)

---
action: 
decision: exclude
automatic_decision: exclude
title: Children's Homes Support Worker
company: Hampshire County Council - Company - Permanent
location: Winchester
source: JobG8
job_id: jobg8-1401785482
reason: Separate employment market.
---

---
action: 
decision: exclude
automatic_decision: exclude
title: Learning Support Assistant
company: Prospero Teaching - Agency - Permanent
location: Eastleigh
source: JobG8
job_id: jobg8-1875238
reason: Separate employment market.
---

---
action: 
decision: exclude
automatic_decision: exclude
title: Specialist Care Support Worker Winchester
company: SCA Care - Agency - Permanent
location: Winchester
source: JobG8
job_id: jobg8-108004872
reason: Separate employment market.
---
