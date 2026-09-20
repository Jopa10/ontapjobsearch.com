# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs, VONNE, Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-09-20
generated_at: 2026-09-20T07:53:22+00:00

**1 job(s) need a human decision.**

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
| JobG8 | OK | 2026-09-20 | 1 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | STALE | 2026-09-19 | 0 | — |
| Teaching Vacancies | STALE | 2026-09-19 | 0 | — |
| NHS Jobs | OK | 2026-09-20 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 1 to review

---
action:
POSS | JobG8 | Merseyside - Liverpool | Liverpool | £40000 per year | Executive Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 107992608
title: Executive Assistant
employer: 
location: Liverpool
region: Merseyside - Liverpool
salary: £40000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: f28e82be98faaeb6eddda4c4fea277c6f5910026ebd4146f8628cf3872689e1f
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
