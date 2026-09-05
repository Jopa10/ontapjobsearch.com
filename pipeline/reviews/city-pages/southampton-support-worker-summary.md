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
- automatic review: 4
- automatic exclude: 1
- effective include: 4
- effective review: 4
- effective exclude: 1

## INCLUDE (4)

---
action: 
decision: include
automatic_decision: include
title: Night Care Worker
company: Hampshire County Council - Company - Permanent
location: Southampton
source: JobG8
job_id: jobg8-1401784887
reason: Approved Southampton catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Secure Childrens Home Support Worker (Weekends)
company: Hampshire County Council - Company - Permanent
location: Southampton
source: JobG8
job_id: jobg8-1401784780
reason: Approved Southampton catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Support Worker
company: The Society of St James - Agency - Permanent
location: Southampton
source: JobG8
job_id: jobg8-1858493
reason: Approved Southampton catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Waking Night Support Worker
company: The Society of St James - Agency - Permanent
location: Southampton
source: JobG8
job_id: jobg8-1663151
reason: Approved Southampton catchment.
---

## REVIEW (4)

---
action: 
decision: review
automatic_decision: review
title: Care Assistant
company: Hampshire County Council - Company - Permanent
location: Alton
source: JobG8
job_id: jobg8-1401784493
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
job_id: jobg8-1401784767
reason: Broad location; review before city inclusion.
---

---
action: 
decision: review
automatic_decision: review
title: Day Opportunities Support Worker (HCC Care YA)
company: Hampshire County Council - Company - Permanent
location: Gosport
source: JobG8
job_id: jobg8-1401784915
reason: Broad location; review before city inclusion.
---

---
action: 
decision: review
automatic_decision: review
title: Support Worker (Out of Hours)
company: Hampshire County Council - Company - Permanent
location: Havant
source: JobG8
job_id: jobg8-1401784888
reason: Broad location; review before city inclusion.
---

## EXCLUDE (1)

---
action: 
decision: exclude
automatic_decision: exclude
title: Secure Children's Home Support Worker
company: Hampshire County Council - Company - Permanent
location: Eastleigh
source: JobG8
job_id: jobg8-1401784900
reason: Separate employment market.
---
