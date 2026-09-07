# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs, VONNE, Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-09-07
generated_at: 2026-09-07T08:40:08+00:00

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
| JobG8 | OK | 2026-09-07 | 2 | — |
| NEJobs | STALE | 2026-09-06 | 0 | — |
| VONNE | STALE | 2026-09-06 | 0 | — |
| Teaching Vacancies | STALE | 2026-09-06 | 0 | — |
| NHS Jobs | OK | 2026-09-07 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 2 to review

---
action:
POSS | JobG8 | Berkshire | Reading | £15.54 per hour | Sales Support Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225565308
title: Sales Support Administrator
employer: 
location: Reading
region: Berkshire
salary: £15.54 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: f921ac1fa634ed109df4a4be14c09441bb1f0f5fdd842fb41053c0056b73e7c7
---

---
action:
POSS | JobG8 | Northern Ireland - East | Lisburn | £16.68 per hour | HR Administrator - Lisburn
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2050078
title: HR Administrator - Lisburn
employer: 
location: Lisburn
region: Northern Ireland - East
salary: £16.68 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 0fd9d9a750bb65060dbee12ce9d1cff32f5ee2c9b9fe30ad6e12e766874072f5
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
