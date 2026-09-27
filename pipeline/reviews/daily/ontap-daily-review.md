# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-09-27
generated_at: 2026-09-27T15:19:05+00:00

**53 job(s) need a human decision.**

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
| JobG8 | OK | 2026-09-27 | 7 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | OK | 2026-09-27 | 1 | — |
| Teaching Vacancies | OK | 2026-09-27 | 45 | — |
| NHS Jobs | OK | 2026-09-27 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 7 to review

---
action: select
POSS | JobG8 | North East - County Durham & Darlington/Hartlepool | County Durham | — | Assistant Accountant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1895111
title: Assistant Accountant
employer: 
location: County Durham
region: North East - County Durham & Darlington/Hartlepool
salary: 
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 85aec96a9044c07b3cc586f56b3c170c42cd69587f1bb785629747c859ba959d
---

---
action: select
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Newcastle | £40000 per year | Assistant Accountant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1944301
title: Assistant Accountant
employer: 
location: Newcastle
region: North East - Tyneside, Wearside & Northumberland
salary: £40000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 049624f751fee4aaa997771a517481c20149578d80f867ed22d9a2b7a5edd499
---

---
action: select
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Tyne And Wear | — | Assistant Accountant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1946149
title: Assistant Accountant
employer: 
location: Tyne And Wear
region: North East - Tyneside, Wearside & Northumberland
salary: 
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 02a2199f75ed38771a20ce32e461db20251d8ab300cc980c3e110fb4e856aef9
---

---
action: select
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Tyne And Wear | — | Assistant Management Accountant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1856074
title: Assistant Management Accountant
employer: 
location: Tyne And Wear
region: North East - Tyneside, Wearside & Northumberland
salary: 
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 8c0dc53058cfab26a2662345a3acabe6a237ab6496d8687fc0847f9916eb8711
---

---
action: select
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Tyne And Wear | — | Assistant Management Accountant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1895961
title: Assistant Management Accountant
employer: 
location: Tyne And Wear
region: North East - Tyneside, Wearside & Northumberland
salary: 
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 8ad9facae662d4b5f2dc01295c1b19f74644fb00cbf1c9cff66b14ec43830f26
---

---
action: exclude
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Tyne And Wear | — | HR Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1907001
title: HR Administrator
employer: 
location: Tyne And Wear
region: North East - Tyneside, Wearside & Northumberland
salary: 
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 95e162776f7accdf470d9b3a97e6235f7088be6a46f5fb332a9e859fb511cda2
---

---
action: select
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Tyne And Wear | £35000 - £45000 per year | Procurement & Logistics Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225599266
title: Procurement & Logistics Coordinator
employer: 
location: Tyne And Wear
region: North East - Tyneside, Wearside & Northumberland
salary: £35000 - £45000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 08af131013252fb6d47b2f6d707edfa1439547d7292f796318de5e0e0bda33d8
---

## VONNE — 1 to review

---
action:
POSS | VONNE | North East | Regionwide | £29,542 to 30,515 Pro Rata | Going Green Together Project Officer (Mat…
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173468
title: Going Green Together Project Officer (Mat…
employer: VONNE
location: Regionwide
region: North East
salary: £29,542 to 30,515 Pro Rata
closing_date: Monday, October 12, 2026 - 11:59
reason: North East geography is generic or derived and requires review
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173468
hub_fingerprint: a93e500526be086d27835c303bb8954f57892aeaffbab7bbdfa02948393f374c
---

## Teaching Vacancies — 45 to review

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
POSS | Teaching Vacancies | Berkshire | Reading, South East, RG5 3EU | £26,176.00 - £28,395.00 Annually (Actual) Term time only plus 10 additional days | Senior Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: senior-finance-assistant-the-bulmershe-school
title: Senior Finance Assistant
employer: The Bulmershe School
location: Reading, South East, RG5 3EU
region: Berkshire
salary: £26,176.00 - £28,395.00 Annually (Actual) Term time only plus 10 additional days
closing_date: 2026-10-23T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-finance-assistant-the-bulmershe-school
hub_fingerprint: 181a5d1ee58d25113d476ef0cb345a8810f62b57717ec4328fed4c7d205c7d90
---

---
action:
POSS | Teaching Vacancies | Devon | Exeter, South West, EX1 2SN | £27,709.00 - £29,070.00 Annually (FTE) | Senior Pupil Services officer - 2 days/week
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: senior-pupil-services-officer-2-days-week-st-michael-s-church-of-england-primary-academy
title: Senior Pupil Services officer - 2 days/week
employer: St Michael's Church of England Primary Academy
location: Exeter, South West, EX1 2SN
region: Devon
salary: £27,709.00 - £29,070.00 Annually (FTE)
closing_date: 2026-10-16T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-pupil-services-officer-2-days-week-st-michael-s-church-of-england-primary-academy
hub_fingerprint: 874fd5e563c0f31c90cfb0bbbbbd1382dcea96a71f54fe744943f09bd2c09961
---

---
action:
POSS | Teaching Vacancies | Devon | Exeter, South West, EX2 4NQ | £27,709.00 - £29,070.00 Annually (FTE) | Senior Pupil Services Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: senior-pupil-services-officer-st-leonard-s-cofe-primary-school-exeter-devon
title: Senior Pupil Services Officer
employer: St Leonard's (CofE) Primary School
location: Exeter, South West, EX2 4NQ
region: Devon
salary: £27,709.00 - £29,070.00 Annually (FTE)
closing_date: 2026-10-06T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-pupil-services-officer-st-leonard-s-cofe-primary-school-exeter-devon
hub_fingerprint: f02d5c9ed2fafb41c34e46885d6d69d10dca6017f59d8472336f034734803f1d
---

---
action:
POSS | Teaching Vacancies | Gloucestershire | Tewkesbury, South West, GL20 5SW | £18.00 - £25.00 Hourly Estimated total hours of 130 annually. Hourly rate of £18-£25 depending on experience, invoiced for work undertaken | Governance Professional / Clerk to the Trust Board
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-clerk-to-the-trust-board
title: Governance Professional / Clerk to the Trust Board
employer: Abbey View
location: Tewkesbury, South West, GL20 5SW
region: Gloucestershire
salary: £18.00 - £25.00 Hourly Estimated total hours of 130 annually. Hourly rate of £18-£25 depending on experience, invoiced for work undertaken
closing_date: 2026-10-12T23:59:00+01:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-clerk-to-the-trust-board
hub_fingerprint: 7236d19a95c6caac14eb68bfa0f91a7b5df86fd61184efc9a8aa2fdc8f253ebd
---

---
action:
POSS | Teaching Vacancies | Greater Manchester - Manchester & Salford | Manchester, North West, M19 1FS | £27,274.00 - £29,071.00 Annually (Actual) NJC Grade 4, Points 7-11 | Administrative Support Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-support-assistant-levenshulme-high-school
title: Administrative Support Assistant
employer: Levenshulme High School
location: Manchester, North West, M19 1FS
region: Greater Manchester - Manchester & Salford
salary: £27,274.00 - £29,071.00 Annually (Actual) NJC Grade 4, Points 7-11
closing_date: 2026-10-07T08:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-support-assistant-levenshulme-high-school
hub_fingerprint: 6f397dfa2089095dcbae6fe489da1f4cbdf40c02ccc5cee3fff051a1a8bf9bee
---

---
action:
POSS | Teaching Vacancies | Greater Manchester - Manchester & Salford | Manchester, North West, M19 1FS | £23,460.00 - £25,006.00 Annually (Actual) NJC Grade 4, Points 7-11 | Inclusion Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: inclusion-administration-officer
title: Inclusion Administration Officer
employer: Levenshulme High School
location: Manchester, North West, M19 1FS
region: Greater Manchester - Manchester & Salford
salary: £23,460.00 - £25,006.00 Annually (Actual) NJC Grade 4, Points 7-11
closing_date: 2026-09-28T08:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/inclusion-administration-officer
hub_fingerprint: 0914d63eb39be8f7002b32be4bd43278bcf83716f21cfe1c605c023b3890c7cd
---

---
action:
POSS | Teaching Vacancies | Greater Manchester - Manchester & Salford | Manchester, North West, M40 9GJ | Grade 5 - £30,023 - £33,119 | School Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: school-administrator-camberwell-park-specialist-support-school
title: School Administrator
employer: Camberwell Park Specialist Support School
location: Manchester, North West, M40 9GJ
region: Greater Manchester - Manchester & Salford
salary: Grade 5 - £30,023 - £33,119
closing_date: 2026-10-04T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/school-administrator-camberwell-park-specialist-support-school
hub_fingerprint: 44c6eb004c83e8cdd9b67b3751585eb85159f5eb0afbec14e86105c0dbcac2e3
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
POSS | Teaching Vacancies | Greater Manchester - Wigan & Bolton | Bolton, North West, BL3 1NG | £26,847.00 - £29,071.00 Annually (Actual) 25 hours per week 9.30am to 2.30pm actual salary is between £15,533.19 to £16,552.07 | Senior Clerical Assistant (Maternity Cover)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: senior-clerical-assistant-maternity-cover
title: Senior Clerical Assistant (Maternity Cover)
employer: Ladywood School
location: Bolton, North West, BL3 1NG
region: Greater Manchester - Wigan & Bolton
salary: £26,847.00 - £29,071.00 Annually (Actual) 25 hours per week 9.30am to 2.30pm actual salary is between £15,533.19 to £16,552.07
closing_date: 2026-11-08T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-clerical-assistant-maternity-cover
hub_fingerprint: b79929d0274d13b1ebdff34c0614a3e22fb61c892001c357e3a5aa054e106cd8
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
POSS | Teaching Vacancies | Hertfordshire | Chorleywood, WD3 6EW | £30,515.00 Annually (FTE) | HR Advisor
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-advisor-d40681c8-89e4-43bc-8af3-fdfdebca5b15
title: HR Advisor
employer: Danes Educational Trust
location: Chorleywood, WD3 6EW
region: Hertfordshire
salary: £30,515.00 Annually (FTE)
closing_date: 2026-10-12T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-advisor-d40681c8-89e4-43bc-8af3-fdfdebca5b15
hub_fingerprint: 7404ca84e55a4935b886c413cd7cd7fc7cf9b0880ed973bdcb3e17e60f5b400f
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
POSS | Teaching Vacancies | Hertfordshire | Hemel Hempstead, East of England, HP1 2JU | £25,390.00 Annually (Actual) H5/6 pro rata | Office Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-manager-oakleaf-primary-hemel-hempstead-hertfordshire
title: Office Manager
employer: Oakleaf Primary
location: Hemel Hempstead, East of England, HP1 2JU
region: Hertfordshire
salary: £25,390.00 Annually (Actual) H5/6 pro rata
closing_date: 2026-10-07T09:00:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-manager-oakleaf-primary-hemel-hempstead-hertfordshire
hub_fingerprint: 02d6df878c213cbf68d3e06e65821d8825025a3407895dca772d8aa02cc45313
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
POSS | Teaching Vacancies | Hertfordshire | St Albans, East of England, AL4 0XB | £15,169.00 Annually (Actual) Plus fringe £425 | KS4 Pastoral and Administrative Support (H4)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: ks4-pastoral-and-administrative-support-h4
title: KS4 Pastoral and Administrative Support (H4)
employer: Beaumont School
location: St Albans, East of England, AL4 0XB
region: Hertfordshire
salary: £15,169.00 Annually (Actual) Plus fringe £425
closing_date: 2026-10-05T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/ks4-pastoral-and-administrative-support-h4
hub_fingerprint: 7693754c50cb3342d68a31fac08aae131860f6d86bbdc6b787066f972f319ef1
---

---
action:
POSS | Teaching Vacancies | Hertfordshire | Stevenage, SG1 5BZ | £12,521.00 - £13,197.00 Annually (Actual) | Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-assistant-brighter-futures-educational-trust
title: Finance Assistant
employer: Brighter Futures Educational Trust
location: Stevenage, SG1 5BZ
region: Hertfordshire
salary: £12,521.00 - £13,197.00 Annually (Actual)
closing_date: 2026-10-02T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-assistant-brighter-futures-educational-trust
hub_fingerprint: d0610cb11873e141f57bbad3aaa145298cd0410bde603671eac3ef62fa8c1a3b
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
POSS | Teaching Vacancies | London | Barking, London, IG11 9AG | £32,372.00 - £33,343.00 Annually (Actual) Scale 6 (Point 18 – £36,693 to Point 20 – £37,794 Full time) Prorated salary range is likely to be approx: £32,372 – £33,343, (dependant on experience, week per year and continuous service). Based on working 35 hours per week, Term time plus 10 days. | Exams and Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: exams-and-data-officer-001df384-4611-4e33-97d4-7c89842c0e25
title: Exams and Data Officer
employer: Barking Abbey School, A Specialist Sports and Humanities College
location: Barking, London, IG11 9AG
region: London
salary: £32,372.00 - £33,343.00 Annually (Actual) Scale 6 (Point 18 – £36,693 to Point 20 – £37,794 Full time) Prorated salary range is likely to be approx: £32,372 – £33,343, (dependant on experience, week per year and continuous service). Based on working 35 hours per week, Term time plus 10 days.
closing_date: 2026-10-16T09:00:00+01:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/exams-and-data-officer-001df384-4611-4e33-97d4-7c89842c0e25
hub_fingerprint: 950c33a0d72f2fd8fb378a63f9f1ce6dd4a46f90fa0aa49c2b14bd2c7c010fa2
---

---
action:
POSS | Teaching Vacancies | London | Isleworth, London, TW7 5DB | £33,129.00 - £35,109.00 Annually (FTE) NJC Scale 5 £33,129 to £35,109 (pro rata) Pro rata salary based on working 36 hours a week for 5 days a week, 39 weeks per annum (N.B. this is ‘term time’ i.e. 195 days) | SEND Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-administrator-bolder-academy
title: SEND Administrator
employer: Bolder Academy
location: Isleworth, London, TW7 5DB
region: London
salary: £33,129.00 - £35,109.00 Annually (FTE) NJC Scale 5 £33,129 to £35,109 (pro rata) Pro rata salary based on working 36 hours a week for 5 days a week, 39 weeks per annum (N.B. this is ‘term time’ i.e. 195 days)
closing_date: 2026-10-12T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-administrator-bolder-academy
hub_fingerprint: c6cb935c71c84c1d57fc773a1a00ebdfb9846aa86e2f732e43223c3c59f33fb9
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
POSS | Teaching Vacancies | London | London, London, NW6 7BH | £29,856.00 Annually (FTE) GLPC SC3 SP6 - Actual starting salary 14378.10 | Admin with Reception Duties-for sixth form site at Harlesden Road NW10 3RN
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: admin-with-reception-duties-for-sixth-form-site-at-harlesden-road-nw10-3rn
title: Admin with Reception Duties-for sixth form site at Harlesden Road NW10 3RN
employer: The Avenue School
location: London, London, NW6 7BH
region: London
salary: £29,856.00 Annually (FTE) GLPC SC3 SP6 - Actual starting salary 14378.10
closing_date: 2026-10-05T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/admin-with-reception-duties-for-sixth-form-site-at-harlesden-road-nw10-3rn
hub_fingerprint: d88adec5f049bb3cd08a8948472b0442a474cdd01462f2cb65396bf410fc38cb
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
POSS | Teaching Vacancies | London | Twickenham, London, TW2 5LH | £24,600 to £25,697 per annum | Cover & Lettings Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: cover-lettings-administrator
title: Cover & Lettings Administrator
employer: Waldegrave School
location: Twickenham, London, TW2 5LH
region: London
salary: £24,600 to £25,697 per annum
closing_date: 2026-10-05T09:00:59+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/cover-lettings-administrator
hub_fingerprint: 3a7bcc6ec401c7329c594a2350f4df39355d38210a35e50f03bcd1ab2b5e1f3c
---

---
action:
POSS | Teaching Vacancies | Merseyside - Liverpool | Liverpool, North West, L26 0TY | £28,153.00 - £31,015.00 Annually (FTE) | SEND / Pastoral Senior Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-pastoral-senior-administration-officer
title: SEND / Pastoral Senior Administration Officer
employer: Finch Woods Academy
location: Liverpool, North West, L26 0TY
region: Merseyside - Liverpool
salary: £28,153.00 - £31,015.00 Annually (FTE)
closing_date: 2026-10-22T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-pastoral-senior-administration-officer
hub_fingerprint: ce61bf7b69b543daf40054330972d57d1fd80d061762ff7debbf2df5eba32da8
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
POSS | Teaching Vacancies | Norfolk | Norwich, East of England, NR10 3PX | £13.69 per hour | Clerical Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: clerical-assistant-spixworth-infant-school
title: Clerical Assistant
employer: Spixworth Infant School
location: Norwich, East of England, NR10 3PX
region: Norfolk
salary: £13.69 per hour
closing_date: 2026-10-07T01:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/clerical-assistant-spixworth-infant-school
hub_fingerprint: d819e237ea609104b9736198ba29a29b06f8a7d6a34e31da130fd877d3cf9bea
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
POSS | Teaching Vacancies | Sussex | Eastbourne, South East, BN22 9EE | FTE: £26,017.00 - £26,429.00 (actual salary: £21,167.55 to £21,502.76) | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-91c2bb10-6af8-4419-845b-e5add4b37610
title: Administrative Assistant
employer: Heron Park Primary Academy
location: Eastbourne, South East, BN22 9EE
region: Sussex
salary: FTE: £26,017.00 - £26,429.00 (actual salary: £21,167.55 to £21,502.76)
closing_date: 2026-10-16T00:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-91c2bb10-6af8-4419-845b-e5add4b37610
hub_fingerprint: 5d8d5a3f7904e5f2fe854acc5ca59aa059a73a107939c553fdbe6412c2f29243
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
POSS | Teaching Vacancies | Wiltshire | Swindon, SN4 9DL | £14.20 - £15.90 Hourly | Clerk to Governors
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: clerk-to-governors-grove-learning-trust
title: Clerk to Governors
employer: Grove Learning Trust
location: Swindon, SN4 9DL
region: Wiltshire
salary: £14.20 - £15.90 Hourly
closing_date: 2026-11-02T23:59:00+00:00
reason: Borderline school administration title: clerk to governors
source_url: https://teaching-vacancies.service.gov.uk/jobs/clerk-to-governors-grove-learning-trust
hub_fingerprint: c40077e13386562f829dcfcaa363dac20cade2e9ea8f815d4b44168b9afce998
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
POSS | Teaching Vacancies | Yorkshire - East | Hull, Yorkshire and the Humber, HU3 1UP | £30,515.00 - £33,119.00 Annually (FTE) Grade F Points 14 to 19 (£30,515 to £33,119 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary for this role starts at £26,362.80 | Data Officer (7483)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-officer-7483
title: Data Officer (7483)
employer: Hull Trinity House Academy
location: Hull, Yorkshire and the Humber, HU3 1UP
region: Yorkshire - East
salary: £30,515.00 - £33,119.00 Annually (FTE) Grade F Points 14 to 19 (£30,515 to £33,119 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary for this role starts at £26,362.80
closing_date: 2026-10-06T23:59:00+01:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-officer-7483
hub_fingerprint: 6dcf5ee8aa816dd83be5a929476119fb2e452aeb00b06332b14e3d358ca17ecc
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
POSS | Teaching Vacancies | Yorkshire - South | Rotherham, Yorkshire and the Humber, S66 8AB | Band E Point 7 to 11 £27,264 to £29,071 per annum Actual Salary £23,433 - £24,977 | Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-officer-maltby-academy
title: Data Officer
employer: Maltby Academy
location: Rotherham, Yorkshire and the Humber, S66 8AB
region: Yorkshire - South
salary: Band E Point 7 to 11 £27,264 to £29,071 per annum Actual Salary £23,433 - £24,977
closing_date: 2026-10-05T09:00:00+01:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-officer-maltby-academy
hub_fingerprint: 599fa2126065e53b4cf0e6bb595d24427f7a0f11c984c573157b84b576f364a7
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Knottingley, Yorkshire and the Humber, WF11 0PJ | £30,515.00 - £33,119.00 Annually (FTE) Grade F Points 14 to 19 (£30,515 to £33,119 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary per annum for this job starts at £13,893.91. | SEN Support Officer (7557)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: sen-support-officer-7557
title: SEN Support Officer (7557)
employer: Simpson's Lane Academy
location: Knottingley, Yorkshire and the Humber, WF11 0PJ
region: Yorkshire - West
salary: £30,515.00 - £33,119.00 Annually (FTE) Grade F Points 14 to 19 (£30,515 to £33,119 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary per annum for this job starts at £13,893.91.
closing_date: 2026-10-07T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/sen-support-officer-7557
hub_fingerprint: 144d54717f8d11225f66752198699d03eadd15a2338f474262bcacabaccc8d98
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Leeds, Yorkshire and the Humber, LS16 5AG | Grade C2 SCP 15-19, actual salary £25,823-£27,575 | Deputy Student Services Manager & Attendance Lead
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: deputy-student-services-manager-attendance-lead
title: Deputy Student Services Manager & Attendance Lead
employer: Lawnswood School
location: Leeds, Yorkshire and the Humber, LS16 5AG
region: Yorkshire - West
salary: Grade C2 SCP 15-19, actual salary £25,823-£27,575
closing_date: 2026-10-05T09:00:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/deputy-student-services-manager-attendance-lead
hub_fingerprint: 1f735e7d7eff4ec21b18d375aaa9f282e0d5997e2c0baf394ac9ff486c5f9241
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Leeds, Yorkshire and the Humber, LS16 5EA | £35,837.00 - £37,629.00 Annually (Actual) | Exams and Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: exams-and-data-officer-abbey-grange-church-of-england-academy
title: Exams and Data Officer
employer: Abbey Grange Church of England Academy
location: Leeds, Yorkshire and the Humber, LS16 5EA
region: Yorkshire - West
salary: £35,837.00 - £37,629.00 Annually (Actual)
closing_date: 2026-10-12T09:00:00+01:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/exams-and-data-officer-abbey-grange-church-of-england-academy
hub_fingerprint: 36ecc516582918b43ea846731daafca8dec5541652242b8f325b3b2e795398b1
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
