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
- automatic review: 4
- automatic exclude: 6
- effective include: 5
- effective review: 4
- effective exclude: 6

## INCLUDE (5)

---
action: 
decision: include
automatic_decision: include
title: Accommodation Support Worker
company: The Society of St James - Agency - Permanent
location: Southampton
source: JobG8
job_id: jobg8-1674633
reason: Approved Southampton catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Care and Support Worker
company: The Society of St James - Agency - Permanent
location: Southampton
source: JobG8
job_id: jobg8-1642086
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
job_id: jobg8-1401784075
reason: Approved Southampton catchment.
---

---
action: 
decision: include
automatic_decision: include
title: Support Worker - Children & Young People
company: Randstad Care - Agency - Temporary
location: Southampton
source: JobG8
job_id: jobg8-58c3e926-cf9b-4aae-a931-e1c867a7b221
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
job_id: jobg8-1642087
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
title: Care Assistant (Older Adults)
company: Hampshire County Council - Company - Permanent
location: Emsworth
source: JobG8
job_id: jobg8-1401784339
reason: Broad location; review before city inclusion.
---

---
action: 
decision: review
automatic_decision: review
title: Care Assistant - Care Home
company: Barchester Healthcare - Company - Permanent
location: Hook
source: JobG8
job_id: jobg8-77b95346-e87e-49a2-ba72-135448bf136e
reason: No approved Southampton catchment rule matched; local review required.
---

---
action: 
decision: review
automatic_decision: review
title: Day Opportunities Support Worker
company: Hampshire County Council - Company - Permanent
location: Alton
source: JobG8
job_id: jobg8-1401784594
reason: Broad location; review before city inclusion.
---

## EXCLUDE (6)

---
action: 
decision: exclude
automatic_decision: exclude
title: Care Assistant - Bank - Care Home
company: Barchester Healthcare - Company - Permanent
location: Fareham
source: JobG8
job_id: jobg8-4a74d1e7-f86f-4dad-965a-206ba0f5fa61
reason: Separate employment market.
---

---
action: 
decision: exclude
automatic_decision: exclude
title: Child Support Worker
company: Randstad Care - Agency - Temporary
location: Portsmouth
source: JobG8
job_id: jobg8-62ac8011-cb52-461e-bd72-7273b61cb640
reason: Separate employment market.
---

---
action: 
decision: exclude
automatic_decision: exclude
title: Children's Home Support Worker
company: Hampshire County Council - Company - Permanent
location: Fareham
source: JobG8
job_id: jobg8-1401784414
reason: Separate employment market.
---

---
action: 
decision: exclude
automatic_decision: exclude
title: Night Care Assistant
company: Barchester Healthcare - Company - Permanent
location: Fareham
source: JobG8
job_id: jobg8-202c4b49-5e6c-46f1-879f-8421db894a5b
reason: Separate employment market.
---

---
action: 
decision: exclude
automatic_decision: exclude
title: Night Care Assistant (Adults)
company: Hampshire County Council - Company - Permanent
location: Basingstoke
source: JobG8
job_id: jobg8-1401784687
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
job_id: jobg8-1401784261
reason: Separate employment market.
---
