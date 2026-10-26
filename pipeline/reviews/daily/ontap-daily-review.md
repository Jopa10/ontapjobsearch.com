# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-10-26
generated_at: 2026-10-26T20:40:10+00:00

**71 job(s) await a human decision; 2 already answered (73 review rows).**

Edit only each `action:` line:
- `action: sel` (or `action: select`) = include the vacancy.
- `action: exc` (or `action: exclude`) = reject the vacancy.
- Leave `action:` blank while you are still deciding it.
- Up to 15 unresolved/bad action rows per source are fail-closed at job level: those jobs are withheld and flagged while the rest of that source can continue.
- More than 15 unresolved/bad action rows in one source isolate that source from the run; they do not block other clean sources.
- Unchanged decisions are remembered by the source pipelines; they should not keep returning here.
- If the vacancy facts change, its fingerprint changes and it must be reviewed again.

## Source status

| Source | Status | Review date | Needs review | Note |
|---|---|---|---:|---|
| JobG8 | OK | 2026-10-26 | 6 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | OK | 2026-10-26 | 0 | — |
| Teaching Vacancies | OK | 2026-10-26 | 67 | — |
| NHS Jobs | OK | 2026-10-26 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 6 to review

---
action:
POSS | JobG8 | Kent | Kent | — | Purchase Ledger Clerk
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225759058
title: Purchase Ledger Clerk
employer: 
location: Kent
region: Kent
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 301b42c347fd84bc78618a5b53f5e69c8146e1d550a0f2b2ec631e0b629f35c2
---

---
action:
POSS | JobG8 | London | London | — | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2180157
title: Finance Manager
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 92c09825da78ea979c959ba0b9693a7d2f9b83278ecef0a1efacda75739a3365
---

---
action: select
POSS | JobG8 | North East - County Durham & Darlington/Hartlepool | County Durham | £30000 - £45000 per year | Commercial Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225646128
title: Commercial Administrator
employer: 
location: County Durham
region: North East - County Durham & Darlington/Hartlepool
salary: £30000 - £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - title register: high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: a401fb2c409f09540bc2a16e557ccf83525a25a28708599519a0fcb38b0f439d
---

---
action: select
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Tyne And Wear | — | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2077376
title: Accounts Assistant
employer: 
location: Tyne And Wear
region: North East - Tyneside, Wearside & Northumberland
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: accounts assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: b036dae1f0c55aeb1f4a7a6c1fda34ea08aaf6741549c55cad9f52333b3d37f7
---

---
action:
POSS | JobG8 | Nottinghamshire | Nottinghamshire | £42839 - £47181 per year | HR Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225763314
title: HR Manager
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: £42839 - £47181 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: c55267e343c2f62a959bc4d2e1d6d5ec14348e1b9db77305a2b86ed36c5a3740
---

---
action:
POSS | JobG8 | Scotland Central - Fife | Fife | £13.5 - £14.5 per hour | HR Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225750573
title: HR Administrator
employer: 
location: Fife
region: Scotland Central - Fife
salary: £13.5 - £14.5 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - HR administration is transferable unless CIPD or substantial prior expertise is mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: 98c43c870876d073faa14eaba00d1aff5f321a31d585828e0f15e55c1bd3bfd6
---

## VONNE — 0 to review

_No new or changed human decisions required._

## Teaching Vacancies — 67 to review

---
action:
POSS | Teaching Vacancies | Buckinghamshire | Milton Keynes, South East, MK17 8XY | £26,824.00 Annually (FTE) | Business Support
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: business-support-glebe-farm-school-milton-keynes-buckinghamshire
title: Business Support
employer: Glebe Farm School
location: Milton Keynes, South East, MK17 8XY
region: Buckinghamshire
salary: £26,824.00 Annually (FTE)
closing_date: 2026-10-28T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/business-support-glebe-farm-school-milton-keynes-buckinghamshire
hub_fingerprint: 287cf49f1fda567a86bb12e4e9976384c8f751219d3a05457226f55619b875ec
---

---
action:
POSS | Teaching Vacancies | Buckinghamshire | Milton Keynes, South East, MK2 3HQ | £24413 - £25583 per annum | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-lift-sir-herbert-leon
title: Receptionist
employer: Lift Sir Herbert Leon
location: Milton Keynes, South East, MK2 3HQ
region: Buckinghamshire
salary: £24413 - £25583 per annum
closing_date: 2026-11-17T13:08:02+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-lift-sir-herbert-leon
hub_fingerprint: 564c4d4771b043464c6910f7634c770f823cd1895ccae79e3f0f72abb0e7e24c
---

---
action:
POSS | Teaching Vacancies | Cambridgeshire | Cambridge, East of England, CB23 7DU | £25,185.00 - £25,583.00 Annually (FTE) NJC Scale 2, Points 5 to 6. Actual salary £21,600.98 per annum (based on 37 hrs per week) on point 12 (pay award pending). | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-comberton-village-college
title: Receptionist
employer: Comberton Village College
location: Cambridge, East of England, CB23 7DU
region: Cambridgeshire
salary: £25,185.00 - £25,583.00 Annually (FTE) NJC Scale 2, Points 5 to 6. Actual salary £21,600.98 per annum (based on 37 hrs per week) on point 12 (pay award pending).
closing_date: 2026-11-02T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-comberton-village-college
hub_fingerprint: b137ff89fa275c51887dacba54b5974dd52511c454061ab2436b559c5ecc13c4
---

---
action:
POSS | Teaching Vacancies | Cambridgeshire | Cambridge, East of England, CB4 2QT | £25,823-£27,152 per annum | HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-cambridge-regional-college
title: HR Administrator
employer: Cambridge Regional College
location: Cambridge, East of England, CB4 2QT
region: Cambridgeshire
salary: £25,823-£27,152 per annum
closing_date: 2026-11-01T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-cambridge-regional-college
hub_fingerprint: 2c042a6e5bd35c719825d67f47744bd265cf4d43802c2845377a2eff615e48ad
---

---
action:
POSS | Teaching Vacancies | Cheshire - Warrington & Halton | Warrington, North West, WA2 0LN | £16,899.00 - £17,556.00 Annually (Actual) Grade 4: NJC SCP 6 to SCP 7 (Full year salary range £26,847 to £27,274; Actual Salary: £16,899 to £17,282 per annum) | Administrative Support Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-support-officer-padgate-academy-warrington
title: Administrative Support Officer
employer: Padgate Academy
location: Warrington, North West, WA2 0LN
region: Cheshire - Warrington & Halton
salary: £16,899.00 - £17,556.00 Annually (Actual) Grade 4: NJC SCP 6 to SCP 7 (Full year salary range £26,847 to £27,274; Actual Salary: £16,899 to £17,282 per annum)
closing_date: 2026-11-09T12:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-support-officer-padgate-academy-warrington
hub_fingerprint: a9e70965b87688612a80e1a56f39f07baef25e4c81cfe40cd91c2933f32b216a
---

---
action:
POSS | Teaching Vacancies | Cornwall | Liskeard, PL14 3EA | £32,046.00 - £34,811.00 Annually (FTE) Actual salary approx. £21,727 - £23,602 per annum | Governance Professional to Trust Board and Local Governing Committees
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-to-trust-board-and-local-governing-committees-1594a72d-d462-43fb-b443-b41012e611bd
title: Governance Professional to Trust Board and Local Governing Committees
employer: South East Cornwall Multi Academy Regional Trust
location: Liskeard, PL14 3EA
region: Cornwall
salary: £32,046.00 - £34,811.00 Annually (FTE) Actual salary approx. £21,727 - £23,602 per annum
closing_date: 2026-11-06T09:00:00+00:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-to-trust-board-and-local-governing-committees-1594a72d-d462-43fb-b443-b41012e611bd
hub_fingerprint: 3163723353a8c50ef50a1609120e9553eb1d28873d6c24a5a71ffa0bdd4bca16
---

---
action:
POSS | Teaching Vacancies | Derbyshire | Bakewell, East Midlands, DE45 1JA | £26,016.00 - £26,427.00 Annually (FTE) Actual Salary £14,306 to £14,532 per annum | School Business Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: school-business-assistant-lady-manners-school-bakewell-derbyshire
title: School Business Assistant
employer: Lady Manners School
location: Bakewell, East Midlands, DE45 1JA
region: Derbyshire
salary: £26,016.00 - £26,427.00 Annually (FTE) Actual Salary £14,306 to £14,532 per annum
closing_date: 2026-11-02T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/school-business-assistant-lady-manners-school-bakewell-derbyshire
hub_fingerprint: a390fbfbb469351d803783398bbade7cc9688da05466c79df40188b0dffd5ca9
---

---
action:
POSS | Teaching Vacancies | Essex | Rayleigh, SS6 9BZ | £13,583.00 - £14,255.00 Annually (Actual) Scale 5 Point 10 to 13 | Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-assistant-rayleigh-schools-trust
title: Finance Assistant
employer: Rayleigh Schools Trust
location: Rayleigh, SS6 9BZ
region: Essex
salary: £13,583.00 - £14,255.00 Annually (Actual) Scale 5 Point 10 to 13
closing_date: 2026-10-29T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-assistant-rayleigh-schools-trust
hub_fingerprint: a5f01b6b20d4b2378fac4811fcb6acf179b8eee2c8668d0a65b2f7bc650529d0
---

---
action:
POSS | Teaching Vacancies | Greater Manchester - Manchester & Salford | Manchester, North West, M20 2ET | £18,491 - £19,395 (Actual salary) | Reception and Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: reception-and-administration-assistant-didsbury-high-school
title: Reception and Administration Assistant
employer: Didsbury High School
location: Manchester, North West, M20 2ET
region: Greater Manchester - Manchester & Salford
salary: £18,491 - £19,395 (Actual salary)
closing_date: 2026-11-30T09:00:59+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/reception-and-administration-assistant-didsbury-high-school
hub_fingerprint: 60a5e8531f40a809b7c2e7c1c2c5fa8b6266493cdfde3ad5f7df63d9fb464698
---

---
action:
POSS | Teaching Vacancies | Greater Manchester - Manchester & Salford | Manchester, North West, M28 0SY | £25,820.00 - £28,323.00 Annually (FTE) United Learning Band 2 Vocational Payscale points 1 - 5 | Business Admin Apprentice - Data & Exams
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: business-admin-apprentice-data-exams
title: Business Admin Apprentice - Data & Exams
employer: The Lowry Academy
location: Manchester, North West, M28 0SY
region: Greater Manchester - Manchester & Salford
salary: £25,820.00 - £28,323.00 Annually (FTE) United Learning Band 2 Vocational Payscale points 1 - 5
closing_date: 2026-11-01T08:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/business-admin-apprentice-data-exams
hub_fingerprint: 51d985f2e6c15c7b8af98e168e590a99d9f7fcab1a6c79778b7e1479b9b7d0e1
---

---
action:
POSS | Teaching Vacancies | Hampshire | Portsmouth, South East, PO1 1FG | £22,814.00 - £24,728.00 Annually (Actual) | Administrative Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-officer-105487cf-80e2-4f7a-a8ea-cac5b40a9e6d
title: Administrative Officer
employer: Arundel Court Primary Academy and Nursery
location: Portsmouth, South East, PO1 1FG
region: Hampshire
salary: £22,814.00 - £24,728.00 Annually (Actual)
closing_date: 2026-11-01T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-officer-105487cf-80e2-4f7a-a8ea-cac5b40a9e6d
hub_fingerprint: e10153c142a24fbf7424e4458f0bf97b1284ef428c5dd5c79f428824fbd8ea91
---

---
action:
POSS | Teaching Vacancies | Kent | Gillingham, South East, ME7 2JG | £26,016.00 - £29,071.00 Annually (FTE) Medway D2 4 - 11 £22,047.56 - £25,024.19 Actual Salary | Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-assistant-barnsole-primary-school
title: Administration Assistant
employer: Barnsole Primary School
location: Gillingham, South East, ME7 2JG
region: Kent
salary: £26,016.00 - £29,071.00 Annually (FTE) Medway D2 4 - 11 £22,047.56 - £25,024.19 Actual Salary
closing_date: 2026-11-02T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-assistant-barnsole-primary-school
hub_fingerprint: 8d7524604c5697f9b6e89b95fbbb840ef5380c90866ebe8b3206ea1163a3aaa5
---

---
action:
POSS | Teaching Vacancies | Kent | Sevenoaks, South East, TN13 3LE | £12,757.00 Annually (Actual) | Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-assistant-knole-academy-sevenoaks-kent
title: Administration Assistant
employer: Knole Academy
location: Sevenoaks, South East, TN13 3LE
region: Kent
salary: £12,757.00 Annually (Actual)
closing_date: 2026-11-06T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-assistant-knole-academy-sevenoaks-kent
hub_fingerprint: 7e6118511640286346d15bf84117f3feceabbf2b249f8980d61a2267d187c233
---

---
action:
POSS | Teaching Vacancies | Kent | Tonbridge, South East, TN9 2HE | Actual Pro Rata Salary £23,599 | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-hillview-school-for-girls-tonbridge-kent
title: Administrative Assistant
employer: Hillview School for Girls
location: Tonbridge, South East, TN9 2HE
region: Kent
salary: Actual Pro Rata Salary £23,599
closing_date: 2026-10-30T23:59:59+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-hillview-school-for-girls-tonbridge-kent
hub_fingerprint: edf695bfa1d202058bb4963ac45c9604696a743789c3221f1bb7ce2006682679
---

---
action:
POSS | Teaching Vacancies | Lancashire - Central | Preston, North West, PR4 6AQ | £23,155.61 - £23,895.24 Annually (Actual) FTE £26,016 - £26,847 | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-tarleton-academy
title: Receptionist
employer: Tarleton Academy
location: Preston, North West, PR4 6AQ
region: Lancashire - Central
salary: £23,155.61 - £23,895.24 Annually (Actual) FTE £26,016 - £26,847
closing_date: 2026-11-02T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-tarleton-academy
hub_fingerprint: ebd63c01e4e5e43ea690ac4e34d3d8fb72f4809f3e973cd1bd39a5400e52b2ad
---

---
action:
POSS | Teaching Vacancies | Lancashire - East | Blackburn, North West, BB1 4ED | £34,357.00 Annually (FTE) 5 Inset days per year, plus an additional 3 planning days, at least one personal day per year | Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-officer-the-hyndburn-academy-blackburn-lancashire
title: Data Officer
employer: The Hyndburn Academy
location: Blackburn, North West, BB1 4ED
region: Lancashire - East
salary: £34,357.00 Annually (FTE) 5 Inset days per year, plus an additional 3 planning days, at least one personal day per year
closing_date: 2026-11-16T17:00:00+00:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-officer-the-hyndburn-academy-blackburn-lancashire
hub_fingerprint: 15c017ab5902be33a8f1ee4ee685a20589062efa57916b394779c771c984d67d
---

---
action:
POSS | Teaching Vacancies | Lancashire - East | Nelson, North West, BB9 0PR | £35,000.00 Annually (FTE) Local Government Pension, Health Care Cash Plan, Generous Staff Discount scheme, 3 extra inset days for planning, at least one personal leave day per year | Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-officer-marsden-heights-community-college
title: Data Officer
employer: Marsden Heights Community College
location: Nelson, North West, BB9 0PR
region: Lancashire - East
salary: £35,000.00 Annually (FTE) Local Government Pension, Health Care Cash Plan, Generous Staff Discount scheme, 3 extra inset days for planning, at least one personal leave day per year
closing_date: 2026-11-08T17:00:00+00:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-officer-marsden-heights-community-college
hub_fingerprint: 2fc0809e11b5cfb50d7e4302178cbf4260ecf179048b76635180e8c8d6beab27
---

---
action:
POSS | Teaching Vacancies | Leicestershire | Leicester, LE4 1EZ | £36,621.00 - £40,458.00 Annually (FTE) Approximate Starting Salary of £22,269.52 | Finance Business Partner
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-business-partner-discovery-schools-academies-trust-ltd
title: Finance Business Partner
employer: Discovery Schools Academies Trust Ltd
location: Leicester, LE4 1EZ
region: Leicestershire
salary: £36,621.00 - £40,458.00 Annually (FTE) Approximate Starting Salary of £22,269.52
closing_date: 2026-11-02T09:00:00+00:00
reason: Part-time finance requires actual earnings/hours and qualification checks
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-business-partner-discovery-schools-academies-trust-ltd
hub_fingerprint: 4eb23f701c13d5f7bff090bd6cb4ab968e51a07ca1a6549bc995828d7a322573
---

---
action:
POSS | Teaching Vacancies | Lincolnshire | Grimsby, Yorkshire and the Humber, DN37 9EH | £26,016.00 - £26,847.00 Annually (FTE) Grade C Points 4 to 6 (£26,016 to £26,847 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary for this role is £15,186.48. | Administration Officer (7752)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-7752
title: Administration Officer (7752)
employer: John Whitgift Academy
location: Grimsby, Yorkshire and the Humber, DN37 9EH
region: Lincolnshire
salary: £26,016.00 - £26,847.00 Annually (FTE) Grade C Points 4 to 6 (£26,016 to £26,847 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary for this role is £15,186.48.
closing_date: 2026-10-29T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-7752
hub_fingerprint: d970a3eb7ef37fb0782683fd2c0e9d159fe321941321c56248f4ffd2502a36a0
---

---
action:
POSS | Teaching Vacancies | London | Barking, London, IG11 0FU | £27,803.00 Annually (Actual) 5.12 Support Scale Already Pro-Rata | Attendance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: attendance-officer-riverside-bridge-school
title: Attendance Officer
employer: Riverside Bridge School
location: Barking, London, IG11 0FU
region: London
salary: £27,803.00 Annually (Actual) 5.12 Support Scale Already Pro-Rata
closing_date: 2026-11-03T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/attendance-officer-riverside-bridge-school
hub_fingerprint: 5286d83dac1f9538d319fc73996703d5fba1403ba378caaa20c50c425c553626
---

---
action:
POSS | Teaching Vacancies | London | Beckenham, London, BR3 1RF | £30,843.00 - £32,655.00 Annually (FTE) | Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-1d8ea2cf-23c2-491e-9778-888fe22529fb
title: Administration Officer
employer: Worsley Bridge Primary School
location: Beckenham, London, BR3 1RF
region: London
salary: £30,843.00 - £32,655.00 Annually (FTE)
closing_date: 2026-11-05T12:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-1d8ea2cf-23c2-491e-9778-888fe22529fb
hub_fingerprint: 82585250193bc9696bb0c1cb5ce6941e2639248fa246c50a1d88daf45291b745
---

---
action:
POSS | Teaching Vacancies | London | Carshalton, London, SM5 2PT | £30,408.00 - £32,655.00 Annually (FTE) | Finance & Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-administration-assistant-st-mary-s-rc-infants-school
title: Finance & Administration Assistant
employer: St Mary's RC Infants School
location: Carshalton, London, SM5 2PT
region: London
salary: £30,408.00 - £32,655.00 Annually (FTE)
closing_date: 2026-11-03T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-administration-assistant-st-mary-s-rc-infants-school
hub_fingerprint: 598884d4f0b7ea5790123f66b54a04ed06aa53f96b65d36cc940e319ccb6f160
---

---
action:
POSS | Teaching Vacancies | London | Croydon, London, CR2 6HS | £30,408 | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-harris-primary-academy-haling-park
title: Administrative Assistant
employer: Harris Primary Academy Haling Park
location: Croydon, London, CR2 6HS
region: London
salary: £30,408
closing_date: 2026-11-02T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-harris-primary-academy-haling-park
hub_fingerprint: e6c32a9cebf15174573cae81559dacfb8e739ea4e44f2dc6863d2d589c10934f
---

---
action:
POSS | Teaching Vacancies | London | Dagenham, London, RM10 7UR | £28,909.00 - £30,200.00 Annually (Actual) Salary Scale: Scale 5 (Pt12-15, £33,609 - £35,109) Prorated salary range is likely to be approx. £28,909 - £30,200 (also dependant on experience, weeks per year and continuous service) Based on working 35 hours per week, Term time only. (Subject to job evaluation) | SEND Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-administrator-eastbrook-school
title: SEND Administrator
employer: Eastbrook School
location: Dagenham, London, RM10 7UR
region: London
salary: £28,909.00 - £30,200.00 Annually (Actual) Salary Scale: Scale 5 (Pt12-15, £33,609 - £35,109) Prorated salary range is likely to be approx. £28,909 - £30,200 (also dependant on experience, weeks per year and continuous service) Based on working 35 hours per week, Term time only. (Subject to job evaluation)
closing_date: 2026-11-02T08:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-administrator-eastbrook-school
hub_fingerprint: 734d3a0331dd4511d4af8dfde72848445c10f8178c8ea092fc8a807468d93910
---

---
action:
POSS | Teaching Vacancies | London | Dagenham, London, RM9 4UN | £28,709.00 - £30,364.00 Annually (Actual) full time equivalent £31,290- £32,655 | Admin Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: admin-assistant-3fdfc1e3-6219-478b-b4d8-4889ed95e085
title: Admin Assistant
employer: Jo Richardson Community School
location: Dagenham, London, RM9 4UN
region: London
salary: £28,709.00 - £30,364.00 Annually (Actual) full time equivalent £31,290- £32,655
closing_date: 2026-11-11T08:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/admin-assistant-3fdfc1e3-6219-478b-b4d8-4889ed95e085
hub_fingerprint: 835ff8abadeb436a59a6a0946aeecaf7c339e5b48e7a7b38172f4e7728c7f4ed
---

---
action:
POSS | Teaching Vacancies | London | Feltham, London, TW13 4QP | Scale 3 (£23,507.84 - £23.844.13) | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-oak-hill-academy-west-london
title: Administrative Assistant
employer: Oak Hill Academy West London
location: Feltham, London, TW13 4QP
region: London
salary: Scale 3 (£23,507.84 - £23.844.13)
closing_date: 2026-10-30T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-oak-hill-academy-west-london
hub_fingerprint: 87fd16b2c3ec8400e1988b977b8b52085b3317ffab94bbcf1d6b976892c31449
---

---
action:
POSS | Teaching Vacancies | London | Feltham, TW13 4AB | £30,867.00 - £35,158.00 Annually (FTE) (SA6) (pay award pending) | Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-assistant-reach-schools
title: Finance Assistant
employer: Reach Schools
location: Feltham, TW13 4AB
region: London
salary: £30,867.00 - £35,158.00 Annually (FTE) (SA6) (pay award pending)
closing_date: 2026-11-06T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-assistant-reach-schools
hub_fingerprint: d3e4fa9bf6d6b3b107ce71a04a2c4284d3f90a095a437916fbcee48bf3925688
---

---
action:
POSS | Teaching Vacancies | London | Hayes, UB4 9LE | £31,288.00 - £32,655.00 Annually (Actual) | Finance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-officer-middlesex-learning-partnership
title: Finance Officer
employer: Middlesex Learning Partnership
location: Hayes, UB4 9LE
region: London
salary: £31,288.00 - £32,655.00 Annually (Actual)
closing_date: 2026-10-29T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-officer-middlesex-learning-partnership
hub_fingerprint: 934c9b4c50a97fe26169503edd07dfacb3ca0a801c7af0afd1040fe7d6dbd775
---

---
action:
POSS | Teaching Vacancies | London | London, London, E14 0AF | £33,700-£35,500 per annum | CTEC Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: ctec-administrator
title: CTEC Administrator
employer: New City College
location: London, London, E14 0AF
region: London
salary: £33,700-£35,500 per annum
closing_date: 2026-11-01T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/ctec-administrator
hub_fingerprint: 05860591e34c7ff8aead62efbe71ed2ea6340725314c3143c09f94b636a022f1
---

---
action:
POSS | Teaching Vacancies | London | London, London, E17 5SD | £26,016.00 to £26,427.00 per annum (pro rata £22,951.04 to £23,313.62 per annum) plus London Weighting £2,376.00 per annum (pro rata £2,096.08) | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-eden-girls-school-waltham-forest
title: Receptionist
employer: Eden Girls' School, Waltham Forest
location: London, London, E17 5SD
region: London
salary: £26,016.00 to £26,427.00 per annum (pro rata £22,951.04 to £23,313.62 per annum) plus London Weighting £2,376.00 per annum (pro rata £2,096.08)
closing_date: 2026-11-08T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-eden-girls-school-waltham-forest
hub_fingerprint: a3df8bfd5d5a49e0640ee2ed0ec8622bec45421d593ad112864bacdf138a63e5
---

---
action:
POSS | Teaching Vacancies | London | London, London, E17 8HA | £31,290.00 - £33,129.00 Annually (FTE) Term-Time + 5 Inset days & 4 Plus days | Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-sybourn-primary-school-london
title: Administration Officer
employer: Sybourn Primary School
location: London, London, E17 8HA
region: London
salary: £31,290.00 - £33,129.00 Annually (FTE) Term-Time + 5 Inset days & 4 Plus days
closing_date: 2026-11-06T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-sybourn-primary-school-london
hub_fingerprint: 5a82d24380536d6c2373b279786f746f894d74c44968cc8ce93b4e5cf2cff493
---

---
action:
POSS | Teaching Vacancies | London | London, London, SE11 4AX | £33,036.00 Annually (FTE) | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-evolve-academy
title: Office Administrator
employer: Evolve Academy
location: London, London, SE11 4AX
region: London
salary: £33,036.00 Annually (FTE)
closing_date: 2026-10-31T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-evolve-academy
hub_fingerprint: 1c595b8ccad4c8e5153abb23157ac455d36e90b292ccfa42c85830f2550b7947
---

---
action:
POSS | Teaching Vacancies | London | London, London, W2 5EZ | WA Scale 5, Spine Point Range 12 - 17, £26,631 - £29,184 FTE (£23,780 - £26,081 pro rata) | Sixth Form Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: sixth-form-administrator-westminster-academy
title: Sixth Form Administrator
employer: Westminster Academy
location: London, London, W2 5EZ
region: London
salary: WA Scale 5, Spine Point Range 12 - 17, £26,631 - £29,184 FTE (£23,780 - £26,081 pro rata)
closing_date: 2026-11-02T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/sixth-form-administrator-westminster-academy
hub_fingerprint: 06b1a1c423993560e9829b9b7c779bf5a3791234dd303da5eef29c194d31c0b6
---

---
action:
POSS | Teaching Vacancies | London | Northolt, London, UB5 6AG | Grade 6 Pt 18 - 20 (£36,834 - £37,935) pro rata salary of £32,725 - £33,703Ppa | Transition, Assessment and Medical/Welfare Coordinator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: transition-assessment-and-medical-welfare-coordinator
title: Transition, Assessment and Medical/Welfare Coordinator
employer: Belvue School
location: Northolt, London, UB5 6AG
region: London
salary: Grade 6 Pt 18 - 20 (£36,834 - £37,935) pro rata salary of £32,725 - £33,703Ppa
closing_date: 2026-11-12T12:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/transition-assessment-and-medical-welfare-coordinator
hub_fingerprint: 2f91bf4e979b98586e74d747ab87be6b91fd13628e183f58f542c77ceae6878e
---

---
action:
POSS | Teaching Vacancies | London | Romford, London, RM3 8HN | £29,895.10 - £32,173.39 Annually (Actual) NJC Points 14v -19, 36 hours per week, 39 weeks per year (term time only plus inset) | EHCP Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: ehcp-administrator-lime-academy-ravensbourne-romford-essex
title: EHCP Administrator
employer: Lime Academy Ravensbourne
location: Romford, London, RM3 8HN
region: London
salary: £29,895.10 - £32,173.39 Annually (Actual) NJC Points 14v -19, 36 hours per week, 39 weeks per year (term time only plus inset)
closing_date: 2026-11-01T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/ehcp-administrator-lime-academy-ravensbourne-romford-essex
hub_fingerprint: 7c62b3165ee94856f48461a354ca6201930842c18ed0e39f09295fc7efd58a8f
---

---
action:
POSS | Teaching Vacancies | London | Woodford Green, London, IG8 0TX | £32,090 and £33,053 | Admin/Finance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: admin-finance-officer-st-antony-s-catholic-primary-school
title: Admin/Finance Officer
employer: St Antony's Catholic Primary School
location: Woodford Green, London, IG8 0TX
region: London
salary: £32,090 and £33,053
closing_date: 2026-10-30T12:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/admin-finance-officer-st-antony-s-catholic-primary-school
hub_fingerprint: be5e284c5c554141ce502882457c91e8c6496f4056fc4db31e16aa2127240d5d
---

---
action:
POSS | Teaching Vacancies | London | Woodford Green, London, IG8 7DQ | £26,433.00 - £27,586.00 Annually (Actual) LBR4 (£30,288 - £31,611 full time equivalent) | Sixth Form Independent Study Supervisor
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: sixth-form-independent-study-supervisor
title: Sixth Form Independent Study Supervisor
employer: Woodbridge High School
location: Woodford Green, London, IG8 7DQ
region: London
salary: £26,433.00 - £27,586.00 Annually (Actual) LBR4 (£30,288 - £31,611 full time equivalent)
closing_date: 2026-11-09T09:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/sixth-form-independent-study-supervisor
hub_fingerprint: 6f62c9ef655ee246d733ab464506284137faf559e09117d4b260c4db5abbf749
---

---
action:
POSS | Teaching Vacancies | North East | Darlington, DL3 7AU | NJC Band 5 (SCP 7-8), £27,274 – £27,709 per annum | People Support Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: people-support-assistant
title: People Support Assistant
employer: Northern Arch Learning Partnership
location: Darlington, DL3 7AU
region: North East
salary: NJC Band 5 (SCP 7-8), £27,274 – £27,709 per annum
closing_date: 2026-10-27T12:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/people-support-assistant
hub_fingerprint: d2918b7a23dbe2747b8a15c2d053fa8086153ab79edbec387d935c96ecc0fab8
---

---
action:
POSS | Teaching Vacancies | Northamptonshire | Corby, East Midlands, NN17 5EB | £27,514.00 Annually (Actual) | Operations Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: operations-administrator-f863f96d-ca5a-492a-8206-7a0736f466c1
title: Operations Administrator
employer: Corby Business Academy
location: Corby, East Midlands, NN17 5EB
region: Northamptonshire
salary: £27,514.00 Annually (Actual)
closing_date: 2026-10-26T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/operations-administrator-f863f96d-ca5a-492a-8206-7a0736f466c1
hub_fingerprint: ac502666be695ba91102c21c4be0dc9d89b88de5c2201aee3501aeedcd603c29
---

---
action:
POSS | Teaching Vacancies | Northamptonshire | Wellingborough, East Midlands, NN8 3HB | £16,624.20 - £16,889.23 Annually (FTE) Based on NJS Scale F6 - F7, FTE salary is £26,846 - £27,274 | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-st-barnabas-church-of-england-school
title: Administrator
employer: St Barnabas Church of England School
location: Wellingborough, East Midlands, NN8 3HB
region: Northamptonshire
salary: £16,624.20 - £16,889.23 Annually (FTE) Based on NJS Scale F6 - F7, FTE salary is £26,846 - £27,274
closing_date: 2026-11-06T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-st-barnabas-church-of-england-school
hub_fingerprint: 95dfcb7090b915916c44c627cecff0fb750dcce62bd4dcf96b3d6b71042ab77c
---

---
action:
POSS | Teaching Vacancies | Nottinghamshire | Mansfield, East Midlands, NG18 2DP | £22,569.72 - £22,569.72 Annually (Actual) | Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-assistant-horizons-academy-mansfield-nottinghamshire
title: Administration Assistant
employer: Horizons Academy
location: Mansfield, East Midlands, NG18 2DP
region: Nottinghamshire
salary: £22,569.72 - £22,569.72 Annually (Actual)
closing_date: 2026-11-08T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-assistant-horizons-academy-mansfield-nottinghamshire
hub_fingerprint: 095a3e9993e6cf95c06e0e92650acc5afbe0692b6280b406c9f8256b63376f46
---

---
action:
POSS | Teaching Vacancies | Nottinghamshire | Nottingham, East Midlands, NG4 2LR | £22,753 Actual Salary (£26,016 FTE) | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-netherfield-primary-school
title: Administrative Assistant
employer: Netherfield Primary School
location: Nottingham, East Midlands, NG4 2LR
region: Nottinghamshire
salary: £22,753 Actual Salary (£26,016 FTE)
closing_date: 2026-11-08T12:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-netherfield-primary-school
hub_fingerprint: 59e3df1a17e0264c90880b181aa347f63ac5a20726614c086a6d6511e7b83d30
---

---
action:
POSS | Teaching Vacancies | Nottinghamshire | Nottingham, East Midlands, NG8 2FT | £22,507.00 - £24,527.00 Annually (Actual) The salary advertised reflects the pro rata salary for this role, based on 45.6 weeks per year. The full-time equivalent FTE salary for this position is £25,666 - 27,970 per annum. | SEND Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-administrator-fernwood-school
title: SEND Administrator
employer: Fernwood School
location: Nottingham, East Midlands, NG8 2FT
region: Nottinghamshire
salary: £22,507.00 - £24,527.00 Annually (Actual) The salary advertised reflects the pro rata salary for this role, based on 45.6 weeks per year. The full-time equivalent FTE salary for this position is £25,666 - 27,970 per annum.
closing_date: 2026-11-02T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-administrator-fernwood-school
hub_fingerprint: 735bbb6dfb8c00920602acc79a81fd3db77393ddd82c2b579d02fe9c1a609dda
---

---
action:
POSS | Teaching Vacancies | Nottinghamshire | Nottingham, East Midlands, NG9 3DU | £22,630.72 - £23,356.04 Annually (Actual) NJE Grade 3, Pts 5 to 7 £26,427 - £27,274 (FTE) | Attendance and Inclusion Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: attendance-and-inclusion-administration-officer-alderman-white-school
title: Attendance and Inclusion Administration Officer
employer: Alderman White School
location: Nottingham, East Midlands, NG9 3DU
region: Nottinghamshire
salary: £22,630.72 - £23,356.04 Annually (Actual) NJE Grade 3, Pts 5 to 7 £26,427 - £27,274 (FTE)
closing_date: 2026-11-02T09:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/attendance-and-inclusion-administration-officer-alderman-white-school
hub_fingerprint: 6c61b9df79795adb41de75bccaf1897ac3c43aa2c7fe3b9587c2e78da347fe04
---

---
action:
POSS | Teaching Vacancies | Oxfordshire | Abingdon, South East, OX14 5NL | £27,709.00 - £30,023.00 Annually (FTE) Grade 6, SCP 8 - 13. Actual salary - £19,783.71 - £21,435.86 | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-thameside-primary-school-abingdon-oxfordshire
title: Office Administrator
employer: Thameside Primary School
location: Abingdon, South East, OX14 5NL
region: Oxfordshire
salary: £27,709.00 - £30,023.00 Annually (FTE) Grade 6, SCP 8 - 13. Actual salary - £19,783.71 - £21,435.86
closing_date: 2026-11-04T12:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-thameside-primary-school-abingdon-oxfordshire
hub_fingerprint: ddd2efad18026a19d58307a5e1868ff8607af69cda2b78adfc1a1eb9106067bc
---

---
action:
POSS | Teaching Vacancies | Oxfordshire | Witney, South East, OX28 1DX | £27,151.00 - £28,981.00 Annually (Actual) Grade 7 | Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-officer-wood-green-school
title: Data Officer
employer: Wood Green School
location: Witney, South East, OX28 1DX
region: Oxfordshire
salary: £27,151.00 - £28,981.00 Annually (Actual) Grade 7
closing_date: 2026-11-04T12:00:00+00:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-officer-wood-green-school
hub_fingerprint: 03b55ddebd1a626dca6fd15a46458ff9b46bf423734e07ec26f68acf2ae9d83f
---

---
action:
POSS | Teaching Vacancies | Somerset | Taunton, TA2 7EG | FTE= £26,847, Actual= £12,427 | HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-the-oak-partnership-trust
title: HR Administrator
employer: The Oak Partnership Trust
location: Taunton, TA2 7EG
region: Somerset
salary: FTE= £26,847, Actual= £12,427
closing_date: 2026-11-03T23:59:59+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-the-oak-partnership-trust
hub_fingerprint: f5b69c3492a94b42c9cd3dfc38685a7be5bbdf434cd456ab27eb6fd610bcdc9f
---

---
action:
POSS | Teaching Vacancies | Suffolk | Beccles, East of England, NR34 7BQ | £19,350- £22,735 actual pa | Finance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-officer-beccles-high-school
title: Finance Officer
employer: Beccles High School
location: Beccles, East of England, NR34 7BQ
region: Suffolk
salary: £19,350- £22,735 actual pa
closing_date: 2026-12-20T00:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-officer-beccles-high-school
hub_fingerprint: 5b6530d9bf5f04230d9ace9f8ea873e15a31b749a5177759ae457ecfd935a246
---

---
action:
POSS | Teaching Vacancies | Surrey | Sunbury-on-Thames, South East, TW16 6LF | £24,570.00 - £26,730.00 Annually (Actual) P5 (FTE £28,700 to £31,224pa) | SEND Adminstrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-adminstrator
title: SEND Adminstrator
employer: Sunbury Manor School
location: Sunbury-on-Thames, South East, TW16 6LF
region: Surrey
salary: £24,570.00 - £26,730.00 Annually (Actual) P5 (FTE £28,700 to £31,224pa)
closing_date: 2026-11-02T09:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-adminstrator
hub_fingerprint: 8d3f1f622369904927fb2d936e92da7017300125e9979d6de93c772eedd9d0e8
---

---
action:
POSS | Teaching Vacancies | Sussex | Lewes, South East, BN7 3AE | Between £25,729 - £28,796 per annum | EAG Advisor
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: eag-advisor
title: EAG Advisor
employer: Plumpton College
location: Lewes, South East, BN7 3AE
region: Sussex
salary: Between £25,729 - £28,796 per annum
closing_date: 2026-11-01T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/eag-advisor
hub_fingerprint: 65330ec985d2cf1ad11a914e74a0b39a443c12afcf4dbe6316f31294628f1435
---

---
action:
POSS | Teaching Vacancies | Sussex | Worthing, South East, BN14 8AH | £26,268.00 Annually (Actual) Paid 47.6 week to include holiday and additional days | Finance Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-administrator-bohunt-school-worthing-worthing-west-sussex
title: Finance Administrator
employer: Bohunt School Worthing
location: Worthing, South East, BN14 8AH
region: Sussex
salary: £26,268.00 Annually (Actual) Paid 47.6 week to include holiday and additional days
closing_date: 2026-10-30T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-administrator-bohunt-school-worthing-worthing-west-sussex
hub_fingerprint: 1fa71dc737cff821fd8f1b33aa549565d7d8d65b95c5ae9f7349d18d36fe2110
---

---
action:
POSS | Teaching Vacancies | West Midlands - Birmingham & Solihull | Birmingham, West Midlands, B29 4HE | £23,408.04 - £25,392.13 Annually (Actual) SCP 12-17 | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-d9ca7417-7c7e-4daa-b266-5f0124cee80f
title: Administrator
employer: E-ACT Shenley Academy
location: Birmingham, West Midlands, B29 4HE
region: West Midlands - Birmingham & Solihull
salary: £23,408.04 - £25,392.13 Annually (Actual) SCP 12-17
closing_date: 2026-11-02T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-d9ca7417-7c7e-4daa-b266-5f0124cee80f
hub_fingerprint: 81bee0180ac6c4b2202225c815141ffc1a82763f74a38c5beef129221175c478
---

---
action:
POSS | Teaching Vacancies | West Midlands - Black Country | Halesowen, West Midlands, B63 4HY | £22,812.00 - £22,812.00 Monthly | Administration Assistant - Level 2
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-assistant-level-2-huntingtree-primary-school
title: Administration Assistant - Level 2
employer: Huntingtree Primary School
location: Halesowen, West Midlands, B63 4HY
region: West Midlands - Black Country
salary: £22,812.00 - £22,812.00 Monthly
closing_date: 2026-11-08T23:59:00+00:00
reason: Salary period needs verification
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-assistant-level-2-huntingtree-primary-school
hub_fingerprint: 8e7ea3615ad44fba107a44d85a251885d963b5c581ca1edb6b5f5264e86520d6
---

---
action:
POSS | Teaching Vacancies | West Midlands - Coventry & Warwickshire | Rugby, West Midlands, CV22 6DY | £22,318.00 - £24,756.00 Annually (Actual) | ECHP Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: echp-administrator
title: ECHP Administrator
employer: Brooke School
location: Rugby, West Midlands, CV22 6DY
region: West Midlands - Coventry & Warwickshire
salary: £22,318.00 - £24,756.00 Annually (Actual)
closing_date: 2026-11-09T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/echp-administrator
hub_fingerprint: 289b85cd9136af0ade626c87c942b47b83d2aac4de9e7d7e3584f1cc2682e940
---

---
action:
POSS | Teaching Vacancies | Wiltshire | Salisbury, South West, SP1 1QX | £26,847.00 - £27,709.00 Annually (FTE) Grade E, pay point 6-8, £26,847 - £27,709 per annum (DOE) FTE | Clerk to Governors
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: clerk-to-governors-st-andrew-s-church-of-england-voluntary-aided-primary-school-laverstock
title: Clerk to Governors
employer: St Andrew's Church of England Voluntary Aided Primary School, Laverstock
location: Salisbury, South West, SP1 1QX
region: Wiltshire
salary: £26,847.00 - £27,709.00 Annually (FTE) Grade E, pay point 6-8, £26,847 - £27,709 per annum (DOE) FTE
closing_date: 2026-11-18T23:59:00+00:00
reason: Borderline school administration title: clerk to governors
source_url: https://teaching-vacancies.service.gov.uk/jobs/clerk-to-governors-st-andrew-s-church-of-england-voluntary-aided-primary-school-laverstock
hub_fingerprint: 843580bd06ce2b6fec39b8be9f16dd22c8a51ab62c0ea23b2b0d58cb9085d048
---

---
action:
POSS | Teaching Vacancies | Wiltshire | Salisbury, South West, SP4 6JZ | £26,847.00 - £27,709.00 Annually (FTE) Grade E, pay point 6-8, £26,847 - £27,709 per annum (DOE) FTE | Clerk to Governors
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: clerk-to-governors-gomeldon-primary-school
title: Clerk to Governors
employer: Gomeldon Primary School
location: Salisbury, South West, SP4 6JZ
region: Wiltshire
salary: £26,847.00 - £27,709.00 Annually (FTE) Grade E, pay point 6-8, £26,847 - £27,709 per annum (DOE) FTE
closing_date: 2026-11-22T23:59:00+00:00
reason: Borderline school administration title: clerk to governors
source_url: https://teaching-vacancies.service.gov.uk/jobs/clerk-to-governors-gomeldon-primary-school
hub_fingerprint: b46f094eaae6940cee885eca2ad73745ee4f1c795a6b2fad08f2ac6b85c874d0
---

---
action:
POSS | Teaching Vacancies | Worcestershire | Pershore, West Midlands, WR10 2ER | £21,938.00 Annually (FTE) SC4 | Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-assistant-pinvin-cofe-academy-pershore-worcestershire
title: Finance Assistant
employer: Pinvin CofE Academy
location: Pershore, West Midlands, WR10 2ER
region: Worcestershire
salary: £21,938.00 Annually (FTE) SC4
closing_date: 2026-11-30T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-assistant-pinvin-cofe-academy-pershore-worcestershire
hub_fingerprint: 328262491bea67c72c4c3fd1afe5ccad2319bf490a63885a6820c140c6af5ce8
---

---
action:
POSS | Teaching Vacancies | Worcestershire | Worcester, WR4 9SG | £27,273.00 - £27,273.00 Annually (FTE) Casual zero hour contract - hourly rate | Governance Professional/Clerk
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-clerk-the-black-pear-trust-worcester-not-recorded
title: Governance Professional/Clerk
employer: The Black Pear Trust
location: Worcester, WR4 9SG
region: Worcestershire
salary: £27,273.00 - £27,273.00 Annually (FTE) Casual zero hour contract - hourly rate
closing_date: 2026-11-04T12:00:00+00:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-clerk-the-black-pear-trust-worcester-not-recorded
hub_fingerprint: 39f3f9a18e6c01661c51631710fe8625933be49e575ca4b3d10fd33108ad5054
---

---
action:
POSS | Teaching Vacancies | Yorkshire - East | Hull, Yorkshire and the Humber, HU4 7EB | £26,016 - £27,274 FTE, £17,694 - £18,550 Actual | Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-assistant-christopher-pickering-primary-school
title: Administration Assistant
employer: Christopher Pickering Primary School
location: Hull, Yorkshire and the Humber, HU4 7EB
region: Yorkshire - East
salary: £26,016 - £27,274 FTE, £17,694 - £18,550 Actual
closing_date: 2026-10-31T08:00:59+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-assistant-christopher-pickering-primary-school
hub_fingerprint: 3dfb95e1a9d852654abb017e498a48eccde8f2ecc1d15914f0f593f1c80d25d0
---

---
action:
POSS | Teaching Vacancies | Yorkshire - North | York, YO24 2RU | £19,740.94 - £20,616.86 Annually (Actual) Grade 5, Level 1-4 (£27,631 to £28,857 FTE) | Trust Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: trust-data-officer-excel-learning-trust
title: Trust Data Officer
employer: Excel Learning Trust
location: York, YO24 2RU
region: Yorkshire - North
salary: £19,740.94 - £20,616.86 Annually (Actual) Grade 5, Level 1-4 (£27,631 to £28,857 FTE)
closing_date: 2026-11-15T23:59:00+00:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/trust-data-officer-excel-learning-trust
hub_fingerprint: ae80d379c2539a5e78349fa075c237173b1af05d68dd801c84411d47d60780a4
---

---
action:
POSS | Teaching Vacancies | Yorkshire - North | York, Yorkshire and the Humber, YO32 4BZ | Grade 4, Level 1-4 (£25,948 to £27,188 p.a.) reduced pro rata to £22,280 to £23,345 (calculated on full time hours) | Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-dc55f46b-8083-476b-9b89-86e66dc7015f
title: Administration Officer
employer: Joseph Rowntree School
location: York, Yorkshire and the Humber, YO32 4BZ
region: Yorkshire - North
salary: Grade 4, Level 1-4 (£25,948 to £27,188 p.a.) reduced pro rata to £22,280 to £23,345 (calculated on full time hours)
closing_date: 2026-11-08T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-dc55f46b-8083-476b-9b89-86e66dc7015f
hub_fingerprint: 66215d6dea054a2084a17569ba441f7fdb901e712a223a38e40c660ed64b2b55
---

---
action:
POSS | Teaching Vacancies | Yorkshire - South | Rotherham, Yorkshire and the Humber, S60 5EJ | £26,427 to £26,847 | SEND Admin Support Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-admin-support-assistant
title: SEND Admin Support Assistant
employer: Brinsworth Academy
location: Rotherham, Yorkshire and the Humber, S60 5EJ
region: Yorkshire - South
salary: £26,427 to £26,847
closing_date: 2026-11-02T09:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-admin-support-assistant
hub_fingerprint: 524666e77a3d8f05b7a2073604539f962bf1105c7f8f2ff5c28b81bce3f594c2
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Elland, HX5 0RY | £32,578.00 - £34,811.00 Annually (Actual) | HR Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-officer-great-heights-academy-trust
title: HR Officer
employer: Great Heights Academy Trust
location: Elland, HX5 0RY
region: Yorkshire - West
salary: £32,578.00 - £34,811.00 Annually (Actual)
closing_date: 2026-11-09T09:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-officer-great-heights-academy-trust
hub_fingerprint: 01a04c84fff204f8c5affce01a6ca7a5541c4b7c7fe4cc3176b6e60f3f98c4ea
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Elland, HX5 0RY | £32,578.00 - £34,811.00 Annually (Actual) | Operations Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: operations-officer-great-heights-academy-trust
title: Operations Officer
employer: Great Heights Academy Trust
location: Elland, HX5 0RY
region: Yorkshire - West
salary: £32,578.00 - £34,811.00 Annually (Actual)
closing_date: 2026-11-02T12:00:00+00:00
reason: Borderline school administration title: operations officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/operations-officer-great-heights-academy-trust
hub_fingerprint: 1d0a7cb63fdb62935c33aa85a37883caed5c0b9d46a635059d48403d7f44187e
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Huddersfield, Yorkshire and the Humber, HD1 4ES | £25,951.00 to £27,733.00 per annum FTE | HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-greenhead-college
title: HR Administrator
employer: Greenhead College
location: Huddersfield, Yorkshire and the Humber, HD1 4ES
region: Yorkshire - West
salary: £25,951.00 to £27,733.00 per annum FTE
closing_date: 2026-11-01T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-greenhead-college
hub_fingerprint: 1e78d7227cf5a0937c6e08642988bc83861f41e570a38caaa797ab968f68073e
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Huddersfield, Yorkshire and the Humber, HD2 2JT | £25,583.00 - £25,989.00 Annually (FTE) Kirklees Grade 5 | Business Support Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: business-support-officer-854eb79b-4156-4a90-8232-676cdd7ff0a7
title: Business Support Officer
employer: All Saints Catholic College
location: Huddersfield, Yorkshire and the Humber, HD2 2JT
region: Yorkshire - West
salary: £25,583.00 - £25,989.00 Annually (FTE) Kirklees Grade 5
closing_date: 2026-11-03T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/business-support-officer-854eb79b-4156-4a90-8232-676cdd7ff0a7
hub_fingerprint: d9a8af6fd76c27ded4bd7c8e2d14249baf6deb662dd976dfdea6eaf3714b2a21
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Wetherby, Yorkshire and the Humber, LS23 6DX | £25,185-£25,989 | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-primrose-lane-primary-school
title: Office Administrator
employer: Primrose Lane Primary School
location: Wetherby, Yorkshire and the Humber, LS23 6DX
region: Yorkshire - West
salary: £25,185-£25,989
closing_date: 2026-11-06T12:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-primrose-lane-primary-school
hub_fingerprint: 36eba92fc5da13964df8312e727cd867a93079f260317d80590395d1026e2f70
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
