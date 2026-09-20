# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-09-20
generated_at: 2026-09-20T16:59:43+00:00

**46 job(s) need a human decision.**

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
| VONNE | OK | 2026-09-20 | 2 | — |
| Teaching Vacancies | OK | 2026-09-20 | 43 | — |
| NHS Jobs | OK | 2026-09-20 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 1 to review

---
action:
POSS | JobG8 | Northamptonshire | Northamptonshire | £30000 - £35000 per year | Parts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225623493
title: Parts Administrator
employer: 
location: Northamptonshire
region: Northamptonshire
salary: £30000 - £35000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 561061d5e83c39c1c276d1dc88eec100b6bb2e7f9edbb8069589e0103256546c
---

## VONNE — 2 to review

---
action:
POSS | VONNE | North East | Hybrid | £ Pro Rata | Independent Advocates (2 posts)
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173435
title: Independent Advocates (2 posts)
employer: Families in Care
location: Hybrid
region: North East
salary: £ Pro Rata
closing_date: 07 October 2026
reason: North East geography is generic or derived and requires review
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173435
hub_fingerprint: adb2441cc35210452ea6c3100fe298208213dbef3cba109a86210b972e3a1f1d
---

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Newcastle | £ Pro Rata | Community Hub and Operations Lead
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173448
title: Community Hub and Operations Lead
employer: Riverside Community Health Pr…
location: Newcastle
region: North East - Tyneside, Wearside & Northumberland
salary: £ Pro Rata
closing_date: 04 October 2026
reason: transferable title with specialist or borderline wording: lead
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173448
hub_fingerprint: c31b81b042638f7dade5c7b8181fe465099ec2888c463ec7c592ddccb5014224
---

## Teaching Vacancies — 43 to review

---
action:
POSS | Teaching Vacancies | Berkshire | Reading, South East, RG1 5SL | £18,327.00 Annually (Actual) Grade 3 SCP5 30 hours per week TTO plus 5 INSET days. £26,427 FTE | Administration Support Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-support-assistant-maiden-erlegh-school-in-reading
title: Administration Support Assistant
employer: Maiden Erlegh School in Reading
location: Reading, South East, RG1 5SL
region: Berkshire
salary: £18,327.00 Annually (Actual) Grade 3 SCP5 30 hours per week TTO plus 5 INSET days. £26,427 FTE
closing_date: 2026-10-02T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-support-assistant-maiden-erlegh-school-in-reading
hub_fingerprint: bf2ce17e5e8f6359d5278bcc52faac5ac138aa4b5ba4487d4b5b05a0df05bfbd
---

---
action:
POSS | Teaching Vacancies | Berkshire | Reading, South East, RG31 6XY | £20,019.00 - £23,175.00 Annually (Actual) | Marketing and Communications Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: marketing-and-communications-officer-denefield-school-reading-berkshire
title: Marketing and Communications Officer
employer: Denefield School
location: Reading, South East, RG31 6XY
region: Berkshire
salary: £20,019.00 - £23,175.00 Annually (Actual)
closing_date: 2026-09-28T09:00:00+01:00
reason: Borderline school administration title: communications officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/marketing-and-communications-officer-denefield-school-reading-berkshire
hub_fingerprint: 49fbbe68655b48f2ef90489254247471948f3b6de9d300c26236ab0f24065d37
---

---
action:
POSS | Teaching Vacancies | Berkshire | Wokingham, South East, RG40 3RB | £28,598-£31,021 | School Operations Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: school-operations-officer-nine-mile-ride-primary-school
title: School Operations Officer
employer: Nine Mile Ride Primary School
location: Wokingham, South East, RG40 3RB
region: Berkshire
salary: £28,598-£31,021
closing_date: 2026-09-24T09:00:00+01:00
reason: Borderline school administration title: operations officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/school-operations-officer-nine-mile-ride-primary-school
hub_fingerprint: 4fc6759965aab29950a8fe42ac10f143fca9f0f50ea2a40bdc4872e87e928d2e
---

---
action:
POSS | Teaching Vacancies | Cambridgeshire | Cambridge, East of England, CB1 1EH | £30,000.00 - £35,000.00 Annually (FTE) | Finance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-officer-parkside-community-college
title: Finance Officer
employer: Parkside Community College
location: Cambridge, East of England, CB1 1EH
region: Cambridgeshire
salary: £30,000.00 - £35,000.00 Annually (FTE)
closing_date: 2026-09-21T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-officer-parkside-community-college
hub_fingerprint: ffbd660a9c06d452c8f30c85869ea091370f104ddc8bc28c5802432d5045ff8a
---

---
action:
POSS | Teaching Vacancies | Cambridgeshire | Cambridge, East of England, CB1 3RJ | £30,000.00 - £35,000.00 Annually (FTE) | Finance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-officer-coleridge-community-college
title: Finance Officer
employer: Coleridge Community College
location: Cambridge, East of England, CB1 3RJ
region: Cambridgeshire
salary: £30,000.00 - £35,000.00 Annually (FTE)
closing_date: 2026-09-21T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-officer-coleridge-community-college
hub_fingerprint: c1bbab19ab65380bea3651c4745cbf2a29448ed6e1fcb88dd4669dde11245d64
---

---
action:
POSS | Teaching Vacancies | Cambridgeshire | Cambridge, East of England, CB2 0SZ | £30,000.00 - £35,000.00 Annually (FTE) | Finance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-officer-cambridge-academy-for-science-and-technology
title: Finance Officer
employer: Cambridge Academy for Science and Technology
location: Cambridge, East of England, CB2 0SZ
region: Cambridgeshire
salary: £30,000.00 - £35,000.00 Annually (FTE)
closing_date: 2026-09-21T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-officer-cambridge-academy-for-science-and-technology
hub_fingerprint: 87350b1eb84243451e86f824527530e84bce61f0d2323b3391bfcd5081d7619f
---

---
action:
POSS | Teaching Vacancies | Cambridgeshire | Cambridge, East of England, CB2 9FD | £30,000.00 - £35,000.00 Annually (FTE) | Finance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-officer-trumpington-community-college
title: Finance Officer
employer: Trumpington Community College
location: Cambridge, East of England, CB2 9FD
region: Cambridgeshire
salary: £30,000.00 - £35,000.00 Annually (FTE)
closing_date: 2026-09-21T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-officer-trumpington-community-college
hub_fingerprint: f0b9fb17adeaaa51ce30bd9fb99efcf0228cfdc97437aba4df624631981d7d20
---

---
action:
POSS | Teaching Vacancies | Cambridgeshire | Cambridge, East of England, CB5 8ND | £30,000.00 - £35,000.00 Annually (FTE) | Finance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-officer-the-galfrid-school
title: Finance Officer
employer: The Galfrid School
location: Cambridge, East of England, CB5 8ND
region: Cambridgeshire
salary: £30,000.00 - £35,000.00 Annually (FTE)
closing_date: 2026-09-21T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-officer-the-galfrid-school
hub_fingerprint: 1e3929fce6d4e3332b093304dea101e56604c396b7eb0301fc74ea78d6802db5
---

---
action:
POSS | Teaching Vacancies | Cornwall | Liskeard, PL14 3EA | £32,046.00 - £34,811.00 Annually (FTE) Actual salary approx. £21,727 - £23,602 | Governance Professional to Trust Board and Local Governing Committees
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-to-trust-board-and-local-governing-committees-south-east-cornwall-multi-academy-regional-trust-liskeard-not-recorded
title: Governance Professional to Trust Board and Local Governing Committees
employer: South East Cornwall Multi Academy Regional Trust
location: Liskeard, PL14 3EA
region: Cornwall
salary: £32,046.00 - £34,811.00 Annually (FTE) Actual salary approx. £21,727 - £23,602
closing_date: 2026-09-22T09:00:00+01:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-to-trust-board-and-local-governing-committees-south-east-cornwall-multi-academy-regional-trust-liskeard-not-recorded
hub_fingerprint: 614f02dcbe774bf0fcb4031a1889e82358f7c8658fdd1cef4239ae2a9b38077b
---

---
action:
POSS | Teaching Vacancies | Devon | Exeter, South West, EX2 4NQ | £22,646.00 Annually (Actual) | Senior Pupil Services Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: senior-pupil-services-officer-st-leonard-s-cofe-primary-school-exeter-devon
title: Senior Pupil Services Officer
employer: St Leonard's (CofE) Primary School
location: Exeter, South West, EX2 4NQ
region: Devon
salary: £22,646.00 Annually (Actual)
closing_date: 2026-10-06T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-pupil-services-officer-st-leonard-s-cofe-primary-school-exeter-devon
hub_fingerprint: 874d567b390a213cb14ef8e95c0b35f3fe143550151095475dfcbe8c62ac1ab6
---

---
action:
POSS | Teaching Vacancies | Gloucestershire | Tewkesbury, South West, GL20 5SW | Estimated total hours of 130 annually. Hourly rate of £18-£25 depending on experience, invoiced for work undertaken | Governance Professional / Clerk to the Trust Board
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-clerk-to-the-trust-board
title: Governance Professional / Clerk to the Trust Board
employer: Abbey View
location: Tewkesbury, South West, GL20 5SW
region: Gloucestershire
salary: Estimated total hours of 130 annually. Hourly rate of £18-£25 depending on experience, invoiced for work undertaken
closing_date: 2026-09-28T23:59:00+01:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-clerk-to-the-trust-board
hub_fingerprint: 2ecf327fa122073f511553f52f332d3828da7ff7462d96ca6558b8a60cb48105
---

---
action:
POSS | Teaching Vacancies | Greater Manchester - Manchester & Salford | Manchester, North West, M23 2YS | £27,784.00 - £29,071.00 Annually (FTE) Grade 4 scp. 7-11 Actual Salary: £14,339 - £15,341 | Admin Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: admin-data-officer-saint-paul-s-catholic-high-school
title: Admin Data Officer
employer: Saint Paul's Catholic High School
location: Manchester, North West, M23 2YS
region: Greater Manchester - Manchester & Salford
salary: £27,784.00 - £29,071.00 Annually (FTE) Grade 4 scp. 7-11 Actual Salary: £14,339 - £15,341
closing_date: 2026-09-21T12:00:00+01:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/admin-data-officer-saint-paul-s-catholic-high-school
hub_fingerprint: 906a4e1a171b2bf25fb74b1f2d50f2b9e303c100f223b0126d3cf5eed48c49e2
---

---
action:
POSS | Teaching Vacancies | Greater Manchester - South | Dukinfield, North West, SK16 5BJ | £26,847.00 - £29,071.00 Annually (FTE) | Attendance and Communications Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: attendance-and-communications-officer
title: Attendance and Communications Officer
employer: Cromwell High School
location: Dukinfield, North West, SK16 5BJ
region: Greater Manchester - South
salary: £26,847.00 - £29,071.00 Annually (FTE)
closing_date: 2026-10-05T09:00:00+01:00
reason: Borderline school administration title: communications officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/attendance-and-communications-officer
hub_fingerprint: d4b885d8a92eed04075e82c1caf0791f8c68a693df548c5581eb061811946f34
---

---
action:
POSS | Teaching Vacancies | Greater Manchester - South | Stockport, North West, SK7 5JX | £15,409 - £16,162 (Actual salary) | SEND Admininstrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-admininstrator
title: SEND Admininstrator
employer: Hazel Grove High School
location: Stockport, North West, SK7 5JX
region: Greater Manchester - South
salary: £15,409 - £16,162 (Actual salary)
closing_date: 2026-09-25T09:00:59+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-admininstrator
hub_fingerprint: 8fd1b11baf3ede3e024ee8cea5a78ea22e105c90b3f2d90421d497a9fb4dfdf9
---

---
action:
POSS | Teaching Vacancies | Greater Manchester - Wigan & Bolton | Wigan, WN6 0NX | £12,024.46 - £12,607.74 Annually (Actual) | Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-assistant-mosaic-learning-trust
title: Finance Assistant
employer: Mosaic Learning Trust
location: Wigan, WN6 0NX
region: Greater Manchester - Wigan & Bolton
salary: £12,024.46 - £12,607.74 Annually (Actual)
closing_date: 2026-09-28T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-assistant-mosaic-learning-trust
hub_fingerprint: 91e3e262527fc44953d9cd9ead5e9a5328e3a59aa6ecdb50a0ab30f67a5250af
---

---
action:
POSS | Teaching Vacancies | Hertfordshire | Chorleywood, WD3 6EW | £29,540.00 Annually (FTE) | HR Advisor
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-advisor-8ec12506-6b2d-4ac4-88f7-d06bd2c562b5
title: HR Advisor
employer: Danes Educational Trust
location: Chorleywood, WD3 6EW
region: Hertfordshire
salary: £29,540.00 Annually (FTE)
closing_date: 2026-09-21T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-advisor-8ec12506-6b2d-4ac4-88f7-d06bd2c562b5
hub_fingerprint: 7d056aeefe21a69d8c19540aca4ac53508715fb10dfd2183087ec688f3f4b4c2
---

---
action:
POSS | Teaching Vacancies | Hertfordshire | Harpenden, East of England, AL5 3AE | £17.15 Hourly Grade H5. £14.98 plus £2.17 holiday pay. Total £17.15 per hour | Governance Professional/Clerk to the Governing Board
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-clerk-to-the-governing-board-roundwood-park-school-harpenden-hertfordshire
title: Governance Professional/Clerk to the Governing Board
employer: Roundwood Park School
location: Harpenden, East of England, AL5 3AE
region: Hertfordshire
salary: £17.15 Hourly Grade H5. £14.98 plus £2.17 holiday pay. Total £17.15 per hour
closing_date: 2026-10-09T07:00:00+01:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-clerk-to-the-governing-board-roundwood-park-school-harpenden-hertfordshire
hub_fingerprint: 8cb586ef4258eb0613932cb57dd2fd54db689a201e44777143c466290319fe66
---

---
action:
POSS | Teaching Vacancies | Hertfordshire | Harpenden, East of England, AL5 5FH | £24,519.00 Annually (FTE) Role is paid £12.71 plus holiday pay. Full time equivalent £24,519 | Attendance and Admin Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: attendance-and-admin-officer-katherine-warington-school
title: Attendance and Admin Officer
employer: Katherine Warington School
location: Harpenden, East of England, AL5 5FH
region: Hertfordshire
salary: £24,519.00 Annually (FTE) Role is paid £12.71 plus holiday pay. Full time equivalent £24,519
closing_date: 2026-09-23T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/attendance-and-admin-officer-katherine-warington-school
hub_fingerprint: f2c28ed78676f3562203505253bbaf6a3c39498e22cc3d09c31e53223f40bbc6
---

---
action:
POSS | Teaching Vacancies | Hertfordshire | Hemel Hempstead, East of England, HP1 2JU | £25,390.00 Annually (Actual) H5 or H6 pro rata (dependant on experience) | Office Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-manager-oakleaf-primary
title: Office Manager
employer: Oakleaf Primary
location: Hemel Hempstead, East of England, HP1 2JU
region: Hertfordshire
salary: £25,390.00 Annually (Actual) H5 or H6 pro rata (dependant on experience)
closing_date: 2026-09-21T09:00:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-manager-oakleaf-primary
hub_fingerprint: a638bf66c139c58b1244d8315adeb00c56cc3a883563eab792cf53e7bfdba04c
---

---
action:
POSS | Teaching Vacancies | Hertfordshire | Rickmansworth, South East, WD3 6ER | £26,552.00 - £28,742.00 Annually (FTE) Term time only Pro Rata salary. | Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-chenies-school
title: Administration Officer
employer: Chenies School
location: Rickmansworth, South East, WD3 6ER
region: Hertfordshire
salary: £26,552.00 - £28,742.00 Annually (FTE) Term time only Pro Rata salary.
closing_date: 2026-10-12T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-chenies-school
hub_fingerprint: e273993a18b933aec3b970776a65c37f30ef23e580bb6e404b9d06223df47e3f
---

---
action:
POSS | Teaching Vacancies | Leicestershire | Loughborough, East Midlands, LE12 6QN | £27,709.00 - £27,709.00 Annually (FTE) | Marketing and Communications Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: marketing-and-communications-officer-east-leake-academy
title: Marketing and Communications Officer
employer: East Leake Academy
location: Loughborough, East Midlands, LE12 6QN
region: Leicestershire
salary: £27,709.00 - £27,709.00 Annually (FTE)
closing_date: 2026-10-03T23:59:00+01:00
reason: Borderline school administration title: communications officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/marketing-and-communications-officer-east-leake-academy
hub_fingerprint: 2b10a4b1b4e89bdd0bebf248061b5955f2f4963335b4caf990117e5d50df9340
---

---
action:
POSS | Teaching Vacancies | Lincolnshire | Spalding, East Midlands, PE11 1JQ | Approx £25,000.00 | Finance Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-manager-the-spalding-st-john-the-baptist-church-of-england-primary-school-spalding-lincolnshire
title: Finance Manager
employer: The Spalding St John the Baptist Church of England Primary School
location: Spalding, East Midlands, PE11 1JQ
region: Lincolnshire
salary: Approx £25,000.00
closing_date: 2026-10-05T12:00:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-manager-the-spalding-st-john-the-baptist-church-of-england-primary-school-spalding-lincolnshire
hub_fingerprint: 84a70f8f5a8a0b944481cc9a1757d7b453cf2b5cef36e5776626cf774f421693
---

---
action:
POSS | Teaching Vacancies | London | Harrow, London, HA3 5RQ | £24,030.00 - £25,048.00 Annually (Actual) | Cover Supervisor Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: cover-supervisor-manager-whitefriars-school-harrow-middlesex
title: Cover Supervisor Manager
employer: Whitefriars School
location: Harrow, London, HA3 5RQ
region: London
salary: £24,030.00 - £25,048.00 Annually (Actual)
closing_date: 2026-10-01T23:59:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/cover-supervisor-manager-whitefriars-school-harrow-middlesex
hub_fingerprint: 2779f427f281f88b66f58a3e782285d2879b35779fdcc4cddc978dddd00df07c
---

---
action:
POSS | Teaching Vacancies | London | Kingston upon Thames, London, KT2 6SE | £10,038.00 - £10,625.00 Annually (Actual) | Communications Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: communications-officer-alexandra-primary-school
title: Communications Officer
employer: Alexandra Primary School
location: Kingston upon Thames, London, KT2 6SE
region: London
salary: £10,038.00 - £10,625.00 Annually (Actual)
closing_date: 2026-09-28T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/communications-officer-alexandra-primary-school
hub_fingerprint: f166568ecb5b15c7d075b94cce13d4154e3aa6bf17dc8b927eb04dcfc75ccc5b
---

---
action:
POSS | Teaching Vacancies | London | London, London, SE11 5QY | £27,629.00 - £28,842.00 Annually (Actual) | BSU Finance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: bsu-finance-officer
title: BSU Finance Officer
employer: Lilian Baylis Technology School
location: London, London, SE11 5QY
region: London
salary: £27,629.00 - £28,842.00 Annually (Actual)
closing_date: 2026-09-30T10:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/bsu-finance-officer
hub_fingerprint: 21128ed05a76068fbf75087c5347a1e2175e0f8947614370a78a65b57d10fb42
---

---
action:
POSS | Teaching Vacancies | London | London, NW4 1NA | £22,315.37 Annually (Actual) NJC 12-17 - Actual starting salary £22,315.37 | Administration Support Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-support-assistant-hasmonean-multi-academy-trust-london-not-recorded
title: Administration Support Assistant
employer: Hasmonean Multi Academy Trust
location: London, NW4 1NA
region: London
salary: £22,315.37 Annually (Actual) NJC 12-17 - Actual starting salary £22,315.37
closing_date: 2026-10-18T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-support-assistant-hasmonean-multi-academy-trust-london-not-recorded
hub_fingerprint: 90883e2861806503f9b55e8637d53c04dfd39b44df536c6d947020ba5435f5ef
---

---
action:
POSS | Teaching Vacancies | Norfolk | King's Lynn, East of England, PE30 4AW | Grade D, Point 6 – 7 £26,847 - £27,274 pa FTE Please note that the salary will be pro rata (approx. £18,639 - £18936) | Finance Assistant (with some reception cover)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-assistant-with-some-reception-cover
title: Finance Assistant (with some reception cover)
employer: Springwood High School
location: King's Lynn, East of England, PE30 4AW
region: Norfolk
salary: Grade D, Point 6 – 7 £26,847 - £27,274 pa FTE Please note that the salary will be pro rata (approx. £18,639 - £18936)
closing_date: 2026-09-29T01:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-assistant-with-some-reception-cover
hub_fingerprint: 611f4f0aa8814705bf3bf0e788c58afc4d330f4ecbdca3063b26960ea7483f58
---

---
action:
POSS | Teaching Vacancies | Norfolk | Norwich, East of England, NR5 0PX | £16,356.00 - £17,168.00 Annually (Actual) | Behaviour & Careers Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: behaviour-careers-administration-assistant
title: Behaviour & Careers Administration Assistant
employer: Ormiston Victory Academy
location: Norwich, East of England, NR5 0PX
region: Norfolk
salary: £16,356.00 - £17,168.00 Annually (Actual)
closing_date: 2026-09-25T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/behaviour-careers-administration-assistant
hub_fingerprint: f30e458daf92e59a71a1438182267f6614c61c4a639021301b026dcbe728db63
---

---
action:
POSS | Teaching Vacancies | Norfolk | Norwich, NR2 1NR | Salary: Support Staff Pay Scale I: £38,510 to £40,444 per annum | Governance Professional - Complaints and Governance Support
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-complaints-and-governance-support
title: Governance Professional - Complaints and Governance Support
employer: Inspiration Trust
location: Norwich, NR2 1NR
region: Norfolk
salary: Salary: Support Staff Pay Scale I: £38,510 to £40,444 per annum
closing_date: 2026-09-23T12:00:00+01:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-complaints-and-governance-support
hub_fingerprint: 8299c1be53536001a0adf66cbd0c07ceafa4c114e5fafe5eae1113bfacb2106f
---

---
action:
POSS | Teaching Vacancies | Norfolk | Wymondham, East of England, NR18 9SZ | £26,403 - £28,142 pa | HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-wymondham-college
title: HR Administrator
employer: Wymondham College
location: Wymondham, East of England, NR18 9SZ
region: Norfolk
salary: £26,403 - £28,142 pa
closing_date: 2026-11-07T00:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-wymondham-college
hub_fingerprint: c86b8c6c6ec760e25b91e1e47c0e17b5df2e0e5c60df609a7db1a1f901925ac9
---

---
action:
POSS | Teaching Vacancies | Nottinghamshire | Nottingham, East Midlands, NG9 3DU | £22,630.72 - £23,356.04 Annually (Actual) NJE Grade 3, Pts 5 to 7 £26,427 - £27,274 (FTE) | Attendance and Inclusion Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: attendance-and-inclusion-administration-officer
title: Attendance and Inclusion Administration Officer
employer: Alderman White School
location: Nottingham, East Midlands, NG9 3DU
region: Nottinghamshire
salary: £22,630.72 - £23,356.04 Annually (Actual) NJE Grade 3, Pts 5 to 7 £26,427 - £27,274 (FTE)
closing_date: 2026-09-30T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/attendance-and-inclusion-administration-officer
hub_fingerprint: a902d479400292cada959f94f17f4e464ec83b12288a8af563436ac1f4e27f18
---

---
action:
POSS | Teaching Vacancies | Somerset | Minehead, South West, TA24 6AY | Support Staff Pay Scale Band 5 point 7-9 | Attendance Support Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: attendance-support-officer-west-somerset-college
title: Attendance Support Officer
employer: West Somerset College
location: Minehead, South West, TA24 6AY
region: Somerset
salary: Support Staff Pay Scale Band 5 point 7-9
closing_date: 2026-10-01T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/attendance-support-officer-west-somerset-college
hub_fingerprint: c12185305b41186a764ab38a166d7939c403e99791f2fb932e774f9390526df1
---

---
action:
POSS | Teaching Vacancies | Suffolk | Brandon, East of England, IP27 0DA | £30,308 to £32,385 actual pa | Operations Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: operations-officer-glade-academy
title: Operations Officer
employer: Glade Academy
location: Brandon, East of England, IP27 0DA
region: Suffolk
salary: £30,308 to £32,385 actual pa
closing_date: 2026-09-30T23:59:00+01:00
reason: Borderline school administration title: operations officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/operations-officer-glade-academy
hub_fingerprint: 95795a0760b92f0eacaddc0ee7555a6ac7e4aa65fdd72d24e2116b779ef5fa34
---

---
action:
POSS | Teaching Vacancies | West Midlands - Coventry & Warwickshire | Coventry, CV4 9AP | £8.00 Hourly £8 per hour for the first 12 months followed by national minimum wage for age | HR Support Apprentice
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-support-apprentice-finham-park-multi-academy-trust
title: HR Support Apprentice
employer: Finham Park Multi Academy Trust
location: Coventry, CV4 9AP
region: West Midlands - Coventry & Warwickshire
salary: £8.00 Hourly £8 per hour for the first 12 months followed by national minimum wage for age
closing_date: 2026-09-24T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-support-apprentice-finham-park-multi-academy-trust
hub_fingerprint: d651326d93b16cf1808592012989f6f3ebe643baa6992d4d079b95de8f7cde51
---

---
action:
POSS | Teaching Vacancies | West Midlands - Coventry & Warwickshire | Nuneaton, CV11 4QH | £27,274 to £29,071 | Trust Finance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: trust-finance-officer-central-england-academy-trust
title: Trust Finance Officer
employer: Central England Academy Trust
location: Nuneaton, CV11 4QH
region: West Midlands - Coventry & Warwickshire
salary: £27,274 to £29,071
closing_date: 2026-10-05T08:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/trust-finance-officer-central-england-academy-trust
hub_fingerprint: 463fefa664f349efe2aa24da4163d39344647824322d8b3cfeae84a067e414ad
---

---
action:
POSS | Teaching Vacancies | West Midlands - Coventry & Warwickshire | Rugby, West Midlands, CV22 7HN | NJC05 to NJC06 £25,583.00 to £25,989.00 FTE (£22,675.13 to £23,034.99 Actual) | Adminstrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: adminstrator
title: Adminstrator
employer: Henry Hinde School
location: Rugby, West Midlands, CV22 7HN
region: West Midlands - Coventry & Warwickshire
salary: NJC05 to NJC06 £25,583.00 to £25,989.00 FTE (£22,675.13 to £23,034.99 Actual)
closing_date: 2026-10-01T00:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/adminstrator
hub_fingerprint: c74396236e08d7855150500d49c400c3c8cbfaa22166a24ec0e9572e567127fe
---

---
action:
POSS | Teaching Vacancies | West Midlands - Coventry & Warwickshire | Stratford-upon-Avon, West Midlands, CV37 9DH | Starting salary for a full-time post £32,578 to £35,570 per annum, starting point depending on experience and qualifications. Actual salary £28,944 to £31,602 per annum based on hours and weeks worked as stated, subject to any continuous service. | Attendance Improvement Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: attendance-improvement-officer-stratford-upon-avon-school-stratford-upon-avon-warwickshire
title: Attendance Improvement Officer
employer: Stratford Upon Avon School
location: Stratford-upon-Avon, West Midlands, CV37 9DH
region: West Midlands - Coventry & Warwickshire
salary: Starting salary for a full-time post £32,578 to £35,570 per annum, starting point depending on experience and qualifications. Actual salary £28,944 to £31,602 per annum based on hours and weeks worked as stated, subject to any continuous service.
closing_date: 2026-09-30T12:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/attendance-improvement-officer-stratford-upon-avon-school-stratford-upon-avon-warwickshire
hub_fingerprint: c4ef84005ed9283addac88aea115fbfbd8c487be68966015ce556b8b855cbbb7
---

---
action:
POSS | Teaching Vacancies | Wiltshire | Calne, South West, SN11 8YH | £29,064.00 - £31,022.00 Annually (FTE) NJC Grade G, £3,378-£3,605 (DOE) Actual | Clerk to Governors
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: clerk-to-governors-kingsbury-green-academy-calne-wiltshire
title: Clerk to Governors
employer: Kingsbury Green Academy
location: Calne, South West, SN11 8YH
region: Wiltshire
salary: £29,064.00 - £31,022.00 Annually (FTE) NJC Grade G, £3,378-£3,605 (DOE) Actual
closing_date: 2026-09-27T23:59:00+01:00
reason: Borderline school administration title: clerk to governors
source_url: https://teaching-vacancies.service.gov.uk/jobs/clerk-to-governors-kingsbury-green-academy-calne-wiltshire
hub_fingerprint: d242001b5198b981e7e6e4ec19ea2b9c4320511b26fe76ae9fa9ba1d2fe012f9
---

---
action:
POSS | Teaching Vacancies | Wiltshire | Trowbridge, South West, BA14 9EN | £14.59 - £15.31 Hourly term time only (+ 2 weeks) | Governance Professional
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-st-augustine-s-catholic-college
title: Governance Professional
employer: St Augustine's Catholic College
location: Trowbridge, South West, BA14 9EN
region: Wiltshire
salary: £14.59 - £15.31 Hourly term time only (+ 2 weeks)
closing_date: 2026-09-23T12:00:00+01:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-st-augustine-s-catholic-college
hub_fingerprint: fc19da250d24f0e2f5c8fc4b65acd2bea1ec639374c211f41e305901ef2df8aa
---

---
action:
POSS | Teaching Vacancies | Worcestershire | Worcester, WR4 9SG | £27,273.00 - £27,273.00 Annually (FTE) Casual zero hour contract - hourly rate | Governance Professional/Clerk
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-clerk-the-black-pear-trust
title: Governance Professional/Clerk
employer: The Black Pear Trust
location: Worcester, WR4 9SG
region: Worcestershire
salary: £27,273.00 - £27,273.00 Annually (FTE) Casual zero hour contract - hourly rate
closing_date: 2026-09-28T12:00:00+01:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-clerk-the-black-pear-trust
hub_fingerprint: 9dc42535494b0cbf026896b4154b038e08727b027f50309ded86a0640ab41cec
---

---
action:
POSS | Teaching Vacancies | Yorkshire - South | Doncaster, Yorkshire and the Humber, DN5 9DD | £26,016.00 - £26,847.00 Annually (FTE) Grade C Points 04 to 06 (£26,016 to £26,847 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary for this job starts at £14,797.10 | Administration Officer (7376)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-7376
title: Administration Officer (7376)
employer: Don Valley Academy
location: Doncaster, Yorkshire and the Humber, DN5 9DD
region: Yorkshire - South
salary: £26,016.00 - £26,847.00 Annually (FTE) Grade C Points 04 to 06 (£26,016 to £26,847 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary for this job starts at £14,797.10
closing_date: 2026-10-01T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-7376
hub_fingerprint: 1b8ec9fe0594fc1e14a01700e6306aa4602f83cd55c46c45ca73058310ac0195
---

---
action:
POSS | Teaching Vacancies | Yorkshire - South | Sheffield, Yorkshire and the Humber, S20 3GU | £24551-£26592 depending on experience | Administration and Clerical Officer - Business Support
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-and-clerical-officer-business-support
title: Administration and Clerical Officer - Business Support
employer: Halfway Nursery Infant School
location: Sheffield, Yorkshire and the Humber, S20 3GU
region: Yorkshire - South
salary: £24551-£26592 depending on experience
closing_date: 2026-09-24T12:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-and-clerical-officer-business-support
hub_fingerprint: e413f6d2cccf0b6092c65950b47b993b8f7f74af837f507edde024ef11f9f4ba
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Bradford, Yorkshire and the Humber, BD3 0DU | £11,368.00 - £11,731.00 Annually (Actual) Band 5, SCP 4 to 6, 19 hours per week, TTO plus 3 days, Wed & Thu 8:45am to 4:30pm and Fri 10:00am to 2:30pm | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-carlton-bolling-bradford-west-yorkshire
title: Administrator
employer: Carlton Bolling
location: Bradford, Yorkshire and the Humber, BD3 0DU
region: Yorkshire - West
salary: £11,368.00 - £11,731.00 Annually (Actual) Band 5, SCP 4 to 6, 19 hours per week, TTO plus 3 days, Wed & Thu 8:45am to 4:30pm and Fri 10:00am to 2:30pm
closing_date: 2026-09-25T10:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-carlton-bolling-bradford-west-yorkshire
hub_fingerprint: e7bca56a25268a752e600b6699a3cbfe2b7432e6ec235697688dfedff228cc7c
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
