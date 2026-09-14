# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs, VONNE, Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-09-14
generated_at: 2026-09-14T08:27:28+00:00

**3 job(s) need a human decision.**

Edit only each `action:` line:
- `action: select` = include the vacancy.
- `action: exclude` = reject the vacancy.
- Leave `action:` blank while you are still deciding it.
- Up to 15 unresolved/bad action rows per source are fail-closed at job level: those jobs are withheld and flagged while the rest of that source can continue.
- More than 15 unresolved/bad action rows in one source isolate that source from the run; they do not block other clean sources.
- Unchanged decisions are remembered by the source pipelines; they should not keep returning here.
- If the vacancy facts change, its fingerprint changes and it must be reviewed again.

## Source status

| Source | Status | Review date | Needs review | Note |
|---|---|---|---:|---|
| JobG8 | OK | 2026-09-14 | 3 | — |
| NEJobs | STALE | 2026-09-13 | 0 | — |
| VONNE | STALE | 2026-09-13 | 0 | — |
| Teaching Vacancies | STALE | 2026-09-13 | 0 | — |
| NHS Jobs | OK | 2026-09-14 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 3 to review

---
action: select
POSS | JobG8 | Staffordshire | Staffordshire | £35000 per year | Procurement and Stock Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225601163
title: Procurement and Stock Administrator
employer: 
location: Staffordshire
region: Staffordshire
salary: £35000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 4c48185b0b68da8d18e02d2e4c9e26e4fb85e0f0698f014aa61a975d75180c8c
---

---
action: exclude
POSS | JobG8 | Suffolk | Suffolk | £45000 per year | Commercial Claims Handler
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 107968791
title: Commercial Claims Handler
employer: 
location: Suffolk
region: Suffolk
salary: £45000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: c2a9cd2d4f1dd6804b278054f4e7edd5f582c28d7b795fe379dd58157f3c2d07
---

---
action: select
POSS | JobG8 | Yorkshire - South | Sheffield | £200 - £250 per daily | HR Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225599384
title: HR Administrator
employer: 
location: Sheffield
region: Yorkshire - South
salary: £200 - £250 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: a84d2714ea0039333f1cf9c52a61867bf9c9f5048965864f1eb9e40037c6ce51
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
