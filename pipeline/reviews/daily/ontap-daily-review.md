# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs, VONNE, Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-09-21
generated_at: 2026-09-21T07:59:12+00:00

**2 job(s) need a human decision.**

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
| JobG8 | OK | 2026-09-21 | 2 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | STALE | 2026-09-20 | 0 | — |
| Teaching Vacancies | STALE | 2026-09-20 | 0 | — |
| NHS Jobs | OK | 2026-09-21 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 2 to review

---
action:
POSS | JobG8 | Leicestershire | Leicestershire | £32000 per year | Finance Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1909307
title: Finance Assistant
employer: 
location: Leicestershire
region: Leicestershire
salary: £32000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 4c69b7b095e6d2ba4c9fb2112c4b161d32f1713d24e1832e72b36aba0b856a7e
---

---
action:
POSS | JobG8 | Northamptonshire | Northamptonshire | £30000 - £35000 per year | Parts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225623493
title: Parts Administrator
employer: 
location: Northamptonshire
region: Northamptonshire
salary: £30000 - £35000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 561061d5e83c39c1c276d1dc88eec100b6bb2e7f9edbb8069589e0103256546c
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
