# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs, VONNE, Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-10-10
generated_at: 2026-10-10T12:49:47+00:00

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
| JobG8 | OK | 2026-10-10 | 2 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | STALE | 2026-10-09 | 0 | — |
| Teaching Vacancies | STALE | 2026-10-09 | 0 | — |
| NHS Jobs | OK | 2026-10-10 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 2 to review

---
action:
POSS | JobG8 | North Scotland | Inverness | £18 - £20 per hour | Executive Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108093450
title: Executive Assistant
employer: 
location: Inverness
region: North Scotland
salary: £18 - £20 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 33ecad3ec3e82420e4d8af98b5de3f3fa7116cba371539b400a1a8908a9c8309
---

---
action:
POSS | JobG8 | Suffolk | Suffolk | £190 - £195 per daily (+ None) | Learning Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108067034
title: Learning Coordinator
employer: 
location: Suffolk
region: Suffolk
salary: £190 - £195 per daily (+ None)
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: c4780b2f955606109b2aa3f60322222fb6415f1f9f99a116c86d1b9877376b04
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
