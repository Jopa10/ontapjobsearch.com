# Ontap daily job review

> **READY TO REVIEW**
> All active sources are current for 2026-09-06. You can start reviewing.

review_date: 2026-09-06
generated_at: 2026-09-06T17:27:53+00:00

**13 job(s) need a human decision.**

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
| JobG8 | OK | 2026-09-06 | 3 | — |
| NEJobs | OK | 2026-09-06 | 0 | — |
| VONNE | OK | 2026-09-06 | 0 | — |
| Teaching Vacancies | OK | 2026-09-06 | 10 | — |
| NHS Jobs | OK | 2026-09-06 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

## JobG8 — 3 to review

---
action: select
POSS | JobG8 | Bristol & Bath | Bristol | £35000 per year | Executive Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 107932845
title: Executive Assistant
employer: 
location: Bristol
region: Bristol & Bath
salary: £35000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: d08fb2710e7aba1d3f043460cd4e5762eaf6c93d0e48146939fa87329a744e97
---

---
action: select
POSS | JobG8 | Cambridgeshire | Cambridge | £45000 per year | Service Advisor
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 107880924
title: Service Advisor
employer: 
location: Cambridge
region: Cambridgeshire
salary: £45000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 8fd7147d8c9226d89dbb1a4abe9fbdc5ef6554569548a14693584ef8af5d5efb
---

---
action: exclude
POSS | JobG8 | Oxfordshire | Oxfordshire | £44026 per year | Recruitment Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 107927202
title: Recruitment Coordinator
employer: 
location: Oxfordshire
region: Oxfordshire
salary: £44026 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: ced2775291e89cd9dee6d0d6916f87b8afd07fdf0a65f84fecd6ed32af0dd99a
---

## NEJobs — 0 to review

_No new or changed human decisions required._

## VONNE — 0 to review

_No new or changed human decisions required._

## Teaching Vacancies — 10 to review

---
action: select
POSS | Teaching Vacancies | Buckinghamshire | Milton Keynes, South East, MK10 7HE | £25,988.00 - £27,254.00 Annually (FTE) | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-brooklands-academy
title: Administrator
employer: Brooklands Academy
location: Milton Keynes, South East, MK10 7HE
region: Buckinghamshire
salary: £25,988.00 - £27,254.00 Annually (FTE)
closing_date: 2026-09-11T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-brooklands-academy
hub_fingerprint: 7191fb5804507cb5431e83433a37998b15af5ac70711379b4f2b579e16ddb470
---

---
action: select
POSS | Teaching Vacancies | Cambridgeshire | Peterborough, East of England, PE6 7JX | £14,802.00 Annually (Actual) | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-9219e9ba-082d-4b75-91ee-2e1cd2dd8f75
title: Administrator
employer: Arthur Mellows Village College
location: Peterborough, East of England, PE6 7JX
region: Cambridgeshire
salary: £14,802.00 Annually (Actual)
closing_date: 2026-09-14T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-9219e9ba-082d-4b75-91ee-2e1cd2dd8f75
hub_fingerprint: 3e5f9ed64f7da742098604816c1900d5f5dfd85e49c7035c3aa7956c1f05893f
---

---
action: select
POSS | Teaching Vacancies | London | London, London, NW10 2UF | £27,254.00 Annually (FTE) Term Time Only | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-north-brent-school
title: Administrator
employer: North Brent School
location: London, London, NW10 2UF
region: London
salary: £27,254.00 Annually (FTE) Term Time Only
closing_date: 2026-09-11T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-north-brent-school
hub_fingerprint: 898c481e106602acca25562bfac7c2417b3798e8dbfdf831142db811422bfc07
---

---
action: select
POSS | Teaching Vacancies | London | London, London, SE11 5QY | £26,857.00 - £27,240.00 Annually (Actual) Room for progression | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-lilian-baylis-technology-school
title: Receptionist
employer: Lilian Baylis Technology School
location: London, London, SE11 5QY
region: London
salary: £26,857.00 - £27,240.00 Annually (Actual) Room for progression
closing_date: 2026-09-18T10:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-lilian-baylis-technology-school
hub_fingerprint: fec4f4fd621cc0b06f9ff1820b53e9c68baaa4c63f2df821df77710884f62ef3
---

---
action: select
POSS | Teaching Vacancies | London | London, London, SW16 6NP | Grade 3 - Salary Spine point 5 to 6 - £31,086 to £31,530 (actual £28,592 to £29,002) | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-st-leonard-s-church-of-england-primary-school-london
title: Office Administrator
employer: St Leonard's Church of England Primary School
location: London, London, SW16 6NP
region: London
salary: Grade 3 - Salary Spine point 5 to 6 - £31,086 to £31,530 (actual £28,592 to £29,002)
closing_date: 2026-09-11T15:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-st-leonard-s-church-of-england-primary-school-london
hub_fingerprint: 1984d1007b1a095a4dda5ca99086c8a7bb05c0290fbf4c309e4192be1be9e493
---

---
action: select
POSS | Teaching Vacancies | London | Osterley, London, TW7 5PN | 28,195.00 - 29,852.00 | School Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: school-administrator-nishkam-school-west-london
title: School Administrator
employer: Nishkam School West London
location: Osterley, London, TW7 5PN
region: London
salary: 28,195.00 - 29,852.00
closing_date: 2026-09-18T00:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/school-administrator-nishkam-school-west-london
hub_fingerprint: 7cdf9b6f05fd677f736344207c7faa9802fdda06b6610cb8a38b28759e55904f
---

---
action: select
POSS | Teaching Vacancies | Somerset | Taunton, South West, TA2 8FT | Actual Annual Salary | Senior Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: senior-office-administrator-west-monkton-church-of-england-school
title: Senior Office Administrator
employer: West Monkton Church of England School
location: Taunton, South West, TA2 8FT
region: Somerset
salary: Actual Annual Salary
closing_date: 2026-09-10T12:00:59+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-office-administrator-west-monkton-church-of-england-school
hub_fingerprint: 983d60adfc8385d957d783b3e6b0b33e165c61d135c22ec2f92dfdcc64ea8e0a
---

---
action: select
POSS | Teaching Vacancies | West Midlands - Birmingham & Solihull | Birmingham, West Midlands, B45 0EU | £22,121.00 Annually (Actual) | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-king-edward-vi-balaam-wood-academy-birmingham-west-midlands
title: Receptionist
employer: King Edward VI Balaam Wood Academy
location: Birmingham, West Midlands, B45 0EU
region: West Midlands - Birmingham & Solihull
salary: £22,121.00 Annually (Actual)
closing_date: 2026-09-21T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-king-edward-vi-balaam-wood-academy-birmingham-west-midlands
hub_fingerprint: a1905a7e887a5f5e0f667ce28f3d2d66e460d6fe83635c756dcc383ebf0e0a48
---

---
action: select
POSS | Teaching Vacancies | West Midlands - Birmingham & Solihull | Birmingham, West Midlands, B45 9BN | £6,072.00 - £6,072.00 Annually (Actual) | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-st-james-catholic-primary-school
title: Office Administrator
employer: St James Catholic Primary School
location: Birmingham, West Midlands, B45 9BN
region: West Midlands - Birmingham & Solihull
salary: £6,072.00 - £6,072.00 Annually (Actual)
closing_date: 2026-09-16T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-st-james-catholic-primary-school
hub_fingerprint: 93794985125b820b557a999b74afac410b51ed80259c8a312909d4be586c13ee
---

---
action: select
POSS | Teaching Vacancies | West Midlands - Black Country | Wednesbury, West Midlands, WS10 7PZ | £22,828 – £23,935 | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-holyhead-primary-academy
title: Office Administrator
employer: Holyhead Primary Academy
location: Wednesbury, West Midlands, WS10 7PZ
region: West Midlands - Black Country
salary: £22,828 – £23,935
closing_date: 2026-09-13T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-holyhead-primary-academy
hub_fingerprint: 14d9d135660ee449d5023a33ffcb36825276d571431f5c12daeb2db23cccd097
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
