# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs, VONNE, Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-09-13
generated_at: 2026-09-13T09:19:18+00:00

**6 job(s) need a human decision.**

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
| JobG8 | OK | 2026-09-13 | 6 | — |
| NEJobs | STALE | 2026-09-12 | 0 | — |
| VONNE | STALE | 2026-09-12 | 0 | — |
| Teaching Vacancies | STALE | 2026-09-12 | 0 | — |
| NHS Jobs | OK | 2026-09-13 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 6 to review

---
action: select
POSS | JobG8 | Berkshire | Reading | £34000 - £36000 per year | Sales and Service Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225601569
title: Sales and Service Administrator
employer: 
location: Reading
region: Berkshire
salary: £34000 - £36000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 536c508fbacd989ebe467b90d949540f3a4004300e3e7da5b6869aea7faef4e8
---

---
action: select
POSS | JobG8 | Bristol & Bath | Bristol | £28000 - £32000 per year (Bonus + 33 days holiday + GP + Benef) | Technical Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225599662
title: Technical Administrator
employer: 
location: Bristol
region: Bristol & Bath
salary: £28000 - £32000 per year (Bonus + 33 days holiday + GP + Benef)
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: d954cc446f3a45f7918675617daac2371fd8cee677f6323df81cc6b48678a57c
---

---
action: select
POSS | JobG8 | Bristol & Bath | Keynsham | £35934 per year | Care Home Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225601438
title: Care Home Administrator
employer: 
location: Keynsham
region: Bristol & Bath
salary: £35934 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 0e8bf1c33ee1b847d406c400b3d37d5bea5ee2eef3dd0592ea03bfd42a77edff
---

---
action: exclude
POSS | JobG8 | London | Harrow | £35000 - £40000 per year | Company Secretary Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1849345
title: Company Secretary Administrator
employer: 
location: Harrow
region: London
salary: £35000 - £40000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 9466359e715b091f1621ad4e7b31f5a7d566e032f424e333f962df215d701a45
---

---
action: select
POSS | JobG8 | North Scotland | Inverness | £35000 per year | Commercial Sales Co-ordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 107975436
title: Commercial Sales Co-ordinator
employer: 
location: Inverness
region: North Scotland
salary: £35000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: f06951dc1d694c36e41cece7c0be648bbf71d713264fee04cbb49d865a45873b
---

---
action: select
POSS | JobG8 | Northern Ireland - East | Lisburn | £31000 per year | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2052639
title: Accounts Assistant
employer: 
location: Lisburn
region: Northern Ireland - East
salary: £31000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 531e0928c9f2e34fb004620b8d99af9365f2d45a1f41a7517f4adb1e25b3d15a
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
