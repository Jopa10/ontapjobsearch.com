# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-08-21
generated_at: 2026-08-21T10:58:10+00:00

**5 job(s) need a human decision.**

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
| JobG8 | OK | 2026-08-21 | 0 | — |
| NEJobs | OK | 2026-08-21 | 3 | — |
| VONNE | OK | 2026-08-21 | 2 | — |
| Teaching Vacancies | STALE | 2026-08-19 | 0 | — |
| NHS Jobs | OK | 2026-08-21 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 0 to review

_No new or changed human decisions required._

## NEJobs — 3 to review

---
action: select
POSS | NEJobs | North East - County Durham & Darlington/Hartlepool | Town Hall, Darlington | £25,989 per annum (pay award… | PA Support Officer
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 300972
title: PA Support Officer
employer: Darlington Borough Council
location: Town Hall, Darlington
region: North East - County Durham & Darlington/Hartlepool
salary: £25,989 per annum (pay award…
closing_date: 31/08/2026
reason: provisional transferable-office review
source_url: https://www.northeastjobs.org.uk/job/PA_Support_Officer/300972
hub_fingerprint: 0ff1c693796e419256960b1228626fbf42c1b885d5b48e4e5b84b11e64d7d5b5
---

---
action: exclude
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Culture House | Grade 4 (SCP 12 - 17) £28,598… | Digital Systems Administrator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 300715
title: Digital Systems Administrator
employer: Sunderland City Council
location: Culture House
region: North East - Tyneside, Wearside & Northumberland
salary: Grade 4 (SCP 12 - 17) £28,598…
closing_date: 02/09/2026
reason: annualised upper salary £31,022 exceeds North East review point £30,000
source_url: https://www.northeastjobs.org.uk/job/Digital_Systems_Administrator/300715
hub_fingerprint: 49e727b6f01dec75a14ed6e223ff24c3da27d9cca3a9729120df6788331ef590
---

---
action: exclude
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £32,061 to £ 33,699 per annum… | Trauma Support Coordinator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301015
title: Trauma Support Coordinator
employer: Tyne and Wear Fire and Res…
location: Tyne and Wear
region: North East - Tyneside, Wearside & Northumberland
salary: £32,061 to £ 33,699 per annum…
closing_date: 02/09/2026 12:00
reason: annualised upper salary £33,699 exceeds North East review point £30,000
source_url: https://www.northeastjobs.org.uk/job/Trauma_Support_Coordinator/301015
hub_fingerprint: 4d9f7c6ba147d32d0bdb54835c00cf192e87dcdc1b0a48232145810e4c7feb9a
---

## VONNE — 2 to review

---
action: exclude
POSS | VONNE | North East | Home-based | £25,664 Per Annum | Mentor (HEAT) - North East England
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173344
title: Mentor (HEAT) - North East England
employer: The Wise Group
location: Home-based
region: North East
salary: £25,664 Per Annum
closing_date: 27 August 2026
reason: North East geography is generic or derived and requires review
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173344
hub_fingerprint: cbe2371fb48869c31b89deaade2a23bc71f0b21d879658f5e43f76661d551bf8
---

---
action: select
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £25,334 to 26,419 Per Annum | Marketing Coordinator
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173347
title: Marketing Coordinator
employer: Age UK North Tyneside
location: Tyne and Wear
region: North East - Tyneside, Wearside & Northumberland
salary: £25,334 to 26,419 Per Annum
closing_date: Wednesday, September 2, 2026 - 12:00
reason: provisional transferable-office review
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173347
hub_fingerprint: cf873105dc37d39d1d7ccb1a0b5efd8c122a00df6edd9c63f416966f49d25698
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
