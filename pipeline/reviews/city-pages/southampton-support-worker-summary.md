# Southampton support worker jobs city-page review

- Parent regional page: `app/hampshire/support-worker.json`
- Live route: `/southampton/support-worker`
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
- automatic review: 5
- automatic exclude: 3
- effective include: 5
- effective review: 5
- effective exclude: 3

## INCLUDE (5)

---
action: 
decision: include
automatic_decision: include
title: Female Support Worker
company: Avenues Group - Company - Permanent
location: Southampton
source: JobG8
job_id: jobg8-559639887195039334437341
reason: Approved Southampton catchment.
---

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
title: Support worker
company: Cygnet - Agency - Permanent
location: Southampton
source: JobG8
job_id: jobg8-2055937
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

## REVIEW (5)

---
action: 
decision: review
automatic_decision: review
title: Care Assistant
company: Hampshire County Council - Company - Permanent
location: Alton
source: JobG8
job_id: jobg8-1401785277
reason: Broad location; review before city inclusion.
---

---
action: 
decision: review
automatic_decision: review
title: Care Assistant
company: TRIDENT HEALTHCARE SOLUTIONS LIMITED - Agency - Permanent
location: Alton
source: JobG8
job_id: jobg8-1980850
reason: No approved Southampton catchment rule matched; local review required.
---

---
action: 
decision: review
automatic_decision: review
title: Female Support Worker
company: Avenues Group - Company - Permanent
location: Tadley
source: JobG8
job_id: jobg8-559639887195039334437340
reason: No approved Southampton catchment rule matched; local review required.
---

---
action: 
decision: review
automatic_decision: review
title: Female Support Worker
company: SeeAbility - Agency - Permanent
location: Tadley
source: JobG8
job_id: jobg8-108059180
reason: No approved Southampton catchment rule matched; local review required.
---

---
action: 
decision: review
automatic_decision: review
title: Support Worker
company: Avenues Group - Company - Permanent
location: Tadley
source: JobG8
job_id: jobg8-635330054620761292837340
reason: No approved Southampton catchment rule matched; local review required.
---

## EXCLUDE (3)

---
action: 
decision: exclude
automatic_decision: exclude
title: Care Assistant
company: Hampshire County Council - Company - Permanent
location: Winchester
source: JobG8
job_id: jobg8-1401785443
reason: Separate employment market.
---

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
title: Secure Children's Home Support Worker
company: Hampshire County Council - Company - Permanent
location: Eastleigh
source: JobG8
job_id: jobg8-1401785578
reason: Separate employment market.
---
