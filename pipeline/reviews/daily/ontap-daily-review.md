# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs, VONNE, Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-09-30
generated_at: 2026-09-30T08:02:49+00:00

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
| JobG8 | OK | 2026-09-30 | 3 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | STALE | 2026-09-29 | 0 | — |
| Teaching Vacancies | STALE | 2026-09-29 | 0 | — |
| NHS Jobs | OK | 2026-09-30 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 3 to review

---
action:
POSS | JobG8 | Hampshire | Eastleigh | £32780 - £35564 per year (Market Supplement, plus Enhancements) | Secure Children's Home Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 1401785578
title: Secure Children's Home Support Worker
employer: 
location: Eastleigh
region: Hampshire
salary: £32780 - £35564 per year (Market Supplement, plus Enhancements)
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 92674bb34448eae75ceaf5902a21e4a795134e15378fe6ef6178cf43202e4128
---

---
action:
POSS | JobG8 | Leicestershire | Leicestershire | £23.00 per hour | Contracts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2042976
title: Contracts Administrator
employer: 
location: Leicestershire
region: Leicestershire
salary: £23.00 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 95da93bff8268bef0d98f556b3cb0eeff8917f61a33046adacfa87433a6f6ee2
---

---
action:
POSS | JobG8 | Yorkshire - South | Sheffield | — | Assistant Management Accountant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2044207
title: Assistant Management Accountant
employer: 
location: Sheffield
region: Yorkshire - South
salary: 
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 2005a927beff1e8d1cc6dc1620e4de8168b9ec5554406773c8501c59bbbef50c
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
