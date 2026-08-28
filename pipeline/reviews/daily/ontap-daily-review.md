# Ontap daily job review

> **READY TO REVIEW**
> All active sources are current for 2026-08-28. You can start reviewing.

review_date: 2026-08-28
generated_at: 2026-08-28T19:35:06+00:00

**21 job(s) need a human decision.**

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
| JobG8 | OK | 2026-08-28 | 4 | — |
| NEJobs | OK | 2026-08-28 | 0 | — |
| VONNE | OK | 2026-08-28 | 0 | — |
| Teaching Vacancies | OK | 2026-08-28 | 17 | — |
| NHS Jobs | OK | 2026-08-28 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

## JobG8 — 4 to review

---
action:
POSS | JobG8 | Buckinghamshire | Buckinghamshire | £20 - £21 per hour | Facilities Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225544622
title: Facilities Coordinator
employer: 
location: Buckinghamshire
region: Buckinghamshire
salary: £20 - £21 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 378f2a4057f35fe1f837ab70a808da414e7c36cb58a520612ec3d11e863a0e8d
---

---
action:
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | £40000 per year | HR Systems and reporting coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 107899847
title: HR Systems and reporting coordinator
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: £40000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 68df80c0d1d7bee93dc4fa96e5e8918a38d9b8627815fab5523aa296765a1f8b
---

---
action:
POSS | JobG8 | London | Sutton | £25000 - £40000 per year | Goods Inwards / Administration Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225545259
title: Goods Inwards / Administration Coordinator
employer: 
location: Sutton
region: London
salary: £25000 - £40000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 354ca0c6fc172291ddc80cbc17dcb1e3600e43afe2ce404980ca64822d8d1657
---

---
action:
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | £30002 per year | Service Delivery Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225435656
title: Service Delivery Coordinator
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: £30002 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 1db95a42a3b5f4d94abfab2aa254cba26801338ecab772efb07374c7b74ed34c
---

## NEJobs — 0 to review

_No new or changed human decisions required._

## VONNE — 0 to review

_No new or changed human decisions required._

## Teaching Vacancies — 17 to review

---
action: select
POSS | Teaching Vacancies | Buckinghamshire | Milton Keynes, South East, MK17 8XY | £26,824.00 Annually (FTE) Grade D, £26,824 per annum | HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-glebe-farm-school-milton-keynes-buckinghamshire
title: HR Administrator
employer: Glebe Farm School
location: Milton Keynes, South East, MK17 8XY
region: Buckinghamshire
salary: £26,824.00 Annually (FTE) Grade D, £26,824 per annum
closing_date: 2026-09-01T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-glebe-farm-school-milton-keynes-buckinghamshire
hub_fingerprint: 0a71f4f2e22076be381864c77e031a679d81e0b596f18446520d12115e40c4c1
---

---
action: select
POSS | Teaching Vacancies | Essex | Braintree, East of England, CM7 1WY | Scale 3, Point 4 – 5 | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-notley-high-school-and-braintree-sixth-form-braintree-essex
title: Receptionist
employer: Notley High School and Braintree Sixth Form
location: Braintree, East of England, CM7 1WY
region: Essex
salary: Scale 3, Point 4 – 5
closing_date: 2026-08-30T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-notley-high-school-and-braintree-sixth-form-braintree-essex
hub_fingerprint: f6b5a99b3a8eabb860c3eabbe8fa23a486f48b7931c13df53e8d146981ad93a1
---

---
action: select
POSS | Teaching Vacancies | Hertfordshire | Royston, East of England, SG8 5NJ | NJC Cambridgeshire Scale 5 Point 12 - 14 (£28,598 - £29,540 FTE per annum) £12,426.16 - £12,835.47 pro rata, plus holiday pay. | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-bassingbourn-village-college
title: Office Administrator
employer: Bassingbourn Village College
location: Royston, East of England, SG8 5NJ
region: Hertfordshire
salary: NJC Cambridgeshire Scale 5 Point 12 - 14 (£28,598 - £29,540 FTE per annum) £12,426.16 - £12,835.47 pro rata, plus holiday pay.
closing_date: 2026-08-31T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-bassingbourn-village-college
hub_fingerprint: ba718d43711414a6d5ac4c235fa40163fa9d0d440591847c4b0d5994775f830a
---

---
action: select
POSS | Teaching Vacancies | Kent | Canterbury, CT1 1NQ | £28,182.00 Annually (FTE) Actual annual salary £ 26057.39 | HR administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-the-diocese-of-canterbury-academies-trust
title: HR administrator
employer: The Diocese Of Canterbury Academies Trust
location: Canterbury, CT1 1NQ
region: Kent
salary: £28,182.00 Annually (FTE) Actual annual salary £ 26057.39
closing_date: 2026-09-07T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-the-diocese-of-canterbury-academies-trust
hub_fingerprint: 2cb63b58beb5bae384e9e052e7d9410c3f0dc582b6d8cca6b7a6e00b205fa430
---

---
action: select
POSS | Teaching Vacancies | Lincolnshire | Spalding, East Midlands, PE11 2EH | £23,973.00 - £26,409.00 Annually (Actual) G5.12-15 £27,254 - £30,024 FTE | HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-tulip-academy
title: HR Administrator
employer: Tulip Academy
location: Spalding, East Midlands, PE11 2EH
region: Lincolnshire
salary: £23,973.00 - £26,409.00 Annually (Actual) G5.12-15 £27,254 - £30,024 FTE
closing_date: 2026-09-07T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-tulip-academy
hub_fingerprint: 49188d67866c546cc12434263960a78ecc42aedcb4669b54e7c0abc7f608016f
---

---
action:
POSS | Teaching Vacancies | London | Beckenham, London, BR3 1RF | £29,856.00 - £31,611.00 Annually (FTE) | Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-worsley-bridge-primary-school-beckenham-kent
title: Administration Officer
employer: Worsley Bridge Primary School
location: Beckenham, London, BR3 1RF
region: London
salary: £29,856.00 - £31,611.00 Annually (FTE)
closing_date: 2026-09-17T12:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-worsley-bridge-primary-school-beckenham-kent
hub_fingerprint: a76df3cd94f8644b3a8afd5a6a516e8fc3af1fb1efb0f23662a69fe147fc373d
---

---
action: select
POSS | Teaching Vacancies | London | Borehamwood, East of England, WD6 2DW | £25,583.00 - £25,989.00 Annually (FTE) Hours Required: 8.30am to 3.30pm | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-summerswood-primary-school
title: Administrator
employer: Summerswood Primary School
location: Borehamwood, East of England, WD6 2DW
region: London
salary: £25,583.00 - £25,989.00 Annually (FTE) Hours Required: 8.30am to 3.30pm
closing_date: 2026-09-04T08:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-summerswood-primary-school
hub_fingerprint: 78a3e99b6bd8cb41fd331d48a203a50e9603a7e272eded8b52a439c26dd5e735
---

---
action: select
POSS | Teaching Vacancies | London | Dagenham, London, RM9 6PH | £25,514.00 Annually (Actual) | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-pathways-school
title: Administrative Assistant
employer: Pathways School
location: Dagenham, London, RM9 6PH
region: London
salary: £25,514.00 Annually (Actual)
closing_date: 2026-09-11T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-pathways-school
hub_fingerprint: 2151d7e740021a7a3c2637680e853e574a844c73d52bf6f992dca5ece18de543
---

---
action: select
POSS | Teaching Vacancies | London | London, London, E15 3DN | Scaled 3 (dependent on experience) £25,524 Pro Rata | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-ranelagh-primary-school
title: Administrative Assistant
employer: Ranelagh Primary School
location: London, London, E15 3DN
region: London
salary: Scaled 3 (dependent on experience) £25,524 Pro Rata
closing_date: 2026-09-04T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-ranelagh-primary-school
hub_fingerprint: 994387633e5f9b980010b1d7809ea0d46af0b291fdf399e613f120c2b586cafb
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
POSS | Teaching Vacancies | London | London, London, SW4 0AJ | £29,805.00 Annually (Actual) Inner London payscale Spine Point 2 | Receptionist / Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-administrator-belleville-wix-academy-london
title: Receptionist / Administrator
employer: Belleville Wix Academy
location: London, London, SW4 0AJ
region: London
salary: £29,805.00 Annually (Actual) Inner London payscale Spine Point 2
closing_date: 2026-09-09T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-administrator-belleville-wix-academy-london
hub_fingerprint: 93a10592e03ed9d3f693438018eded1145b943920f3a912cde877298ba7ec1f5
---

---
action: select
POSS | Teaching Vacancies | London | London, W12 7TF | £20,971.00 - £21,300.00 pro rata (£24,796.00 - £25,185.00 FTE)per annum | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-the-king-s-school-pontefract-west-yorkshire
title: Receptionist
employer: Ark Schools
location: London, W12 7TF
region: London
salary: £20,971.00 - £21,300.00 pro rata (£24,796.00 - £25,185.00 FTE)per annum
closing_date: 2026-08-31T10:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-the-king-s-school-pontefract-west-yorkshire
hub_fingerprint: f856de0d970257841ae088a9953612ef2e88b506f461aa7e0bb31e734152a761
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
closing_date: 2026-09-04T00:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/school-administrator-nishkam-school-west-london
hub_fingerprint: 49f608949386027b12514963c345f9f8a23231c1a6a2e4bc2f5344ca08ca33f2
---

---
action: select
POSS | Teaching Vacancies | Nottinghamshire | Nottingham, NG9 6RZ | £27,709.00 - £29,541.00 Annually (Actual) NJC8-12 | HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-the-spencer-academies-trust
title: HR Administrator
employer: The Spencer Academies Trust
location: Nottingham, NG9 6RZ
region: Nottinghamshire
salary: £27,709.00 - £29,541.00 Annually (Actual) NJC8-12
closing_date: 2026-08-31T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-the-spencer-academies-trust
hub_fingerprint: 792a44b1355bb882826eef20df22d3f839aa2537b64125da61f3107956d549cd
---

---
action: select
POSS | Teaching Vacancies | Oxfordshire | Oxford, South East, OX3 9WN | £26,824.00 Annually (FTE) Actual annual salary is £12,016 for 19.5 hours per week term time only plus 3 inset days | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-barton-park-primary-school
title: Office Administrator
employer: Barton Park Primary School
location: Oxford, South East, OX3 9WN
region: Oxfordshire
salary: £26,824.00 Annually (FTE) Actual annual salary is £12,016 for 19.5 hours per week term time only plus 3 inset days
closing_date: 2026-09-04T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-barton-park-primary-school
hub_fingerprint: 5ac2163c06159d1e25b77086c07e93aabb73a2d59fba3834fb30daa930206311
---

---
action:
POSS | Teaching Vacancies | Wiltshire | Chippenham, South West, SN14 0QT | £29,064.00 - £31,022.00 Annually (FTE) Actual Salary: £25,640 - £27,368 per annum | Admin Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: admin-officer-queen-s-crescent-school
title: Admin Officer
employer: Queen's Crescent School
location: Chippenham, South West, SN14 0QT
region: Wiltshire
salary: £29,064.00 - £31,022.00 Annually (FTE) Actual Salary: £25,640 - £27,368 per annum
closing_date: 2026-09-01T12:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/admin-officer-queen-s-crescent-school
hub_fingerprint: b26a1f91da9bd30669a73843202f0f910517397544fd38db19cc8ca785f62af1
---

---
action: select
POSS | Teaching Vacancies | Yorkshire - West | Leeds, Yorkshire and the Humber, LS19 6LX | £21,870.00 - £22,213.00 Annually (Actual) Full Time, Term time only plus 10 days | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-466b2045-c1e3-4fa9-bf7e-e43eb5901ad7
title: Administrator
employer: Benton Park School
location: Leeds, Yorkshire and the Humber, LS19 6LX
region: Yorkshire - West
salary: £21,870.00 - £22,213.00 Annually (Actual) Full Time, Term time only plus 10 days
closing_date: 2026-08-31T08:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-466b2045-c1e3-4fa9-bf7e-e43eb5901ad7
hub_fingerprint: 4278d430425769ccd9e7afd8470c5455d1a9f439c3b88dd642b2f22502b1200b
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
