# Ontap daily job review

> **READY TO REVIEW**
> All active sources are current for 2026-08-28. You can start reviewing.

review_date: 2026-08-28
generated_at: 2026-08-28T09:35:20+00:00

**24 job(s) need a human decision.**

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
| NEJobs | OK | 2026-08-28 | 1 | — |
| VONNE | OK | 2026-08-28 | 0 | — |
| Teaching Vacancies | OK | 2026-08-28 | 19 | — |
| NHS Jobs | OK | 2026-08-28 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

## JobG8 — 4 to review

---
action: exclude
POSS | JobG8 | Dorset | Dorset | £200 per daily | Project Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 107671295
title: Project Coordinator
employer: 
location: Dorset
region: Dorset
salary: £200 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 7d244c384ff821b3ac4c3bf81ffd38f44af2967aa261d77f9c2ce90e88fb430a
---

---
action: exclude
POSS | JobG8 | Dorset | Dorset | £40000 per year | Project Coordinator (Construction / Scaffolding / Renewables)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 107724530
title: Project Coordinator (Construction / Scaffolding / Renewables)
employer: 
location: Dorset
region: Dorset
salary: £40000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: b24a2265b2932891fe1e7dce7fd5d29db5816eb4eecd946ea89685b82515f157
---

---
action: exclude
POSS | JobG8 | Essex | Essex | £40000 per year | QUALITY & PROCESS COORDINATOR
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1713560
title: QUALITY & PROCESS COORDINATOR
employer: 
location: Essex
region: Essex
salary: £40000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: d4fd22ba1f7d4f913839e6e494d6695d0e1e29a69f33f18fe71201c67e4270c2
---

---
action: select
POSS | JobG8 | Staffordshire | Staffordshire | £30000 - £35000 per year | Operations Administrator - Stock & Logistics
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225543588
title: Operations Administrator - Stock & Logistics
employer: 
location: Staffordshire
region: Staffordshire
salary: £30000 - £35000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 615ad690d9f8d23953f1313cf29ff3a326567ace7a261df7eff4944016e7fe6e
---

## NEJobs — 1 to review

---
action: select
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Eddie Ferguson House, Blyth,… | £32,578 - £35,570 | Tenant Engagement Officer
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301243
title: Tenant Engagement Officer
employer: Northumberland County Coun…
location: Eddie Ferguson House, Blyth,…
region: North East - Tyneside, Wearside & Northumberland
salary: £32,578 - £35,570
closing_date: 20/09/2026
reason: annualised upper salary £35,570 exceeds North East review point £30,000
source_url: https://www.northeastjobs.org.uk/job/Tenant_Engagement_Officer/301243
hub_fingerprint: 55fa0a81f5c8619f4d5c4619ac26b5d165cfafe2785d74f5e861387cab73659f
---

## VONNE — 0 to review

_No new or changed human decisions required._

## Teaching Vacancies — 19 to review

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
POSS | Teaching Vacancies | Cambridgeshire | Huntingdon, PE28 5TQ | £32,061.00 Annually (Actual) | Marketing & Communications Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: marketing-communications-officer-2a432f35-1c7d-4c5e-90a3-e035ce925749
title: Marketing & Communications Officer
employer: Meridian Trust
location: Huntingdon, PE28 5TQ
region: Cambridgeshire
salary: £32,061.00 Annually (Actual)
closing_date: 2026-09-16T08:00:00+01:00
reason: Borderline school administration title: communications officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/marketing-communications-officer-2a432f35-1c7d-4c5e-90a3-e035ce925749
hub_fingerprint: 145b23dd3c74d385cba0a56aa77da35465248529dfc79df0811446a199ed1b5b
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
POSS | Teaching Vacancies | Hampshire | Portsmouth, South East, PO1 5PF | TSAT Pay Group 3 pro rata to £23,701 - £27,506 for hours and weeks stated (£26,866 - £31,179 FTE) | Senior Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: senior-administration-assistant-the-portsmouth-academy
title: Senior Administration Assistant
employer: The Portsmouth Academy
location: Portsmouth, South East, PO1 5PF
region: Hampshire
salary: TSAT Pay Group 3 pro rata to £23,701 - £27,506 for hours and weeks stated (£26,866 - £31,179 FTE)
closing_date: 2026-09-01T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-administration-assistant-the-portsmouth-academy
hub_fingerprint: b51ef4500ba7502c994d9f0bd527b01dd86d7c7f108a9b0985450a7a02fc0537
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
POSS | Teaching Vacancies | Lincolnshire | Grimsby, Yorkshire and the Humber, DN31 2ES | £25,185.00 - £25,989.00 Annually (FTE) Grade C Points 4 to 6 (£25,185 to £25,989 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary per annum for this job starts at £21,758.06. | Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-macaulay-primary-academy
title: Administration Officer
employer: Macaulay Primary Academy
location: Grimsby, Yorkshire and the Humber, DN31 2ES
region: Lincolnshire
salary: £25,185.00 - £25,989.00 Annually (FTE) Grade C Points 4 to 6 (£25,185 to £25,989 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary per annum for this job starts at £21,758.06.
closing_date: 2026-09-02T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-macaulay-primary-academy
hub_fingerprint: e460dc3abc1a9d40f396210a6e6bded4ec394c1efd846100517457068114f5ee
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
POSS | Teaching Vacancies | Oxfordshire | Faringdon, South East, SN7 7LB | £25,185.00 - £25,584.00 Annually (FTE) Support Staff NJC grade 4, SCP 4-5. 37 hours per week/38 weeks per year. Actual annual salary in the region of £21,116.65 - £21,451.20 | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-faringdon-community-college-faringdon-oxfordshire
title: Receptionist
employer: Faringdon Community College
location: Faringdon, South East, SN7 7LB
region: Oxfordshire
salary: £25,185.00 - £25,584.00 Annually (FTE) Support Staff NJC grade 4, SCP 4-5. 37 hours per week/38 weeks per year. Actual annual salary in the region of £21,116.65 - £21,451.20
closing_date: 2026-08-28T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-faringdon-community-college-faringdon-oxfordshire
hub_fingerprint: 08f6053263c1a6101e06492181ee0bd18df9b610e3d2b6475d560f92c2a2c99d
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
