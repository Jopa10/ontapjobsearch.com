# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-08-24
generated_at: 2026-08-24T08:24:40+00:00

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
| JobG8 | OK | 2026-08-24 | 2 | — |
| NEJobs | OK | 2026-08-24 | 0 | — |
| VONNE | OK | 2026-08-24 | 0 | — |
| Teaching Vacancies | STALE | 2026-08-23 | 0 | — |
| NHS Jobs | OK | 2026-08-24 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 2 to review

---
action: exclude
POSS | JobG8 | Shropshire | Shropshire | £28000 - £34000 per year | TPA Liability Claims Handler
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: ac37883a-9d84-4fb5-94a8-d2a287db3aa4
title: TPA Liability Claims Handler
employer: 
location: Shropshire
region: Shropshire
salary: £28000 - £34000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: d2abcf0434c126e2aa72169d69000812875253c2195ac63b8f210353e16a7eed
---

---
action: select
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | £30000 - £32000 per year | HR Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 4aeb6dcb-44ea-4503-b1f4-0ba011dd9846
title: HR Assistant
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: £30000 - £32000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 8761c5fed1b0041d4ff6859760ddbcf1a49e5432d299a7dadb5c451970e1792b
---

## NEJobs — 0 to review

_No new or changed human decisions required._

## VONNE — 0 to review

_No new or changed human decisions required._

## NHS Jobs — 0 to review

_No new or changed human decisions required._
