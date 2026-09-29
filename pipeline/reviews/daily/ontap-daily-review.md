# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs, VONNE, Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-09-29
generated_at: 2026-09-29T08:37:30+00:00

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
| JobG8 | OK | 2026-09-29 | 1 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | STALE | 2026-09-28 | 0 | — |
| Teaching Vacancies | STALE | 2026-09-28 | 0 | — |
| NHS Jobs | OK | 2026-09-29 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 1 to review

---
action: exclude
POSS | JobG8 | London | London | £54,486 per annum | Interim Head of Governance & Company Secretary
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2039986
title: Interim Head of Governance & Company Secretary
employer: 
location: London
region: London
salary: £54,486 per annum
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: c9199b51259c8416bfb2f16dc1df321fd4afa5625838f8a61e1f06c513e4f4da
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
