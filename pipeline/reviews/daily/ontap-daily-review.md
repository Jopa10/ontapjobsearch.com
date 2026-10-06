# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs, VONNE, Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-10-06
generated_at: 2026-10-06T13:29:51+00:00

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
| JobG8 | OK | 2026-10-06 | 2 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | STALE | 2026-10-05 | 0 | — |
| Teaching Vacancies | STALE | 2026-10-05 | 0 | — |
| NHS Jobs | OK | 2026-10-06 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 2 to review

---
action: exclude
POSS | JobG8 | North East - County Durham & Darlington/Hartlepool | County Durham | £33808 - £42835 per year | Apprenticeship Skills Co-ordinator in Electrical Installations
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2056773
title: Apprenticeship Skills Co-ordinator in Electrical Installations
employer: 
location: County Durham
region: North East - County Durham & Darlington/Hartlepool
salary: £33808 - £42835 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: bd722643d732c84f0e24054950ae3679e3ab200e6144423bfd97991580a1694e
---

---
action: select
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Tyne And Wear | — | Assistant Management Accountant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1884516
title: Assistant Management Accountant
employer: 
location: Tyne And Wear
region: North East - Tyneside, Wearside & Northumberland
salary: 
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 115166db68fd4dce9844cc331def21c7c8e82e720a8c5099eb6243f70bcee1ee
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
