# Ontap daily job review

> **READY TO REVIEW**
> All active sources are current for 2026-08-24. You can start reviewing.

review_date: 2026-08-24
generated_at: 2026-08-24T09:08:43+00:00

**23 job(s) need a human decision.**

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
| JobG8 | OK | 2026-08-24 | 2 | — |
| NEJobs | OK | 2026-08-24 | 0 | — |
| VONNE | OK | 2026-08-24 | 0 | — |
| Teaching Vacancies | OK | 2026-08-24 | 21 | — |
| NHS Jobs | OK | 2026-08-24 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

## JobG8 — 2 to review

---
action: exclude
POSS | JobG8 | Shropshire | Shropshire | £28000 - £34000 per year | TPA Liability Claims Handler
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: ac37883a-9d84-4fb5-94a8-d2a287db3aa4
title: TPA Liability Claims Handler
employer: 
location: Shropshire
region: Shropshire
salary: £28000 - £34000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: d2abcf0434c126e2aa72169d69000812875253c2195ac63b8f210353e16a7eed
---

---
action: select
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | £30000 - £32000 per year | HR Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 4aeb6dcb-44ea-4503-b1f4-0ba011dd9846
title: HR Assistant
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: £30000 - £32000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 8761c5fed1b0041d4ff6859760ddbcf1a49e5432d299a7dadb5c451970e1792b
---

## NEJobs — 0 to review

_No new or changed human decisions required._

## VONNE — 0 to review

_No new or changed human decisions required._

## Teaching Vacancies — 21 to review

---
action:
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
action:
POSS | Teaching Vacancies | Cambridgeshire | Ely, East of England, CB6 2JA | £26,403 | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-witchford-village-college-ely-cambridgeshire
title: Receptionist
employer: Witchford Village College
location: Ely, East of England, CB6 2JA
region: Cambridgeshire
salary: £26,403
closing_date: 2026-09-07T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-witchford-village-college-ely-cambridgeshire
hub_fingerprint: c2bd9083b377ef2f380c9151c3d7bbae3183588b779b72125d8908daea7eeef0
---

---
action:
POSS | Teaching Vacancies | Devon | Ottery St Mary, South West, EX11 1RA | Support Staff Grade C3-C6. Actual Pro Rated Salary: £21,363-£23,260. | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-the-king-s-school-ottery-st-mary-devon
title: Administrative Assistant
employer: The King's School
location: Ottery St Mary, South West, EX11 1RA
region: Devon
salary: Support Staff Grade C3-C6. Actual Pro Rated Salary: £21,363-£23,260.
closing_date: 2026-09-07T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-the-king-s-school-ottery-st-mary-devon
hub_fingerprint: f57e507c4a6cd740654cd9d41b34a3b1c5b993b07f4588e38404ddc0b2c8c105
---

---
action:
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
action:
POSS | Teaching Vacancies | Hampshire | Southampton, South East, SO30 4EJ | £24,796.00 Annually (FTE) Grade B – Step 1 - Actual Annual Salary £20,369.06 (which is equivalent to a full-time salary of £24,796) | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-ff80cc91-b028-4603-910d-80547a4ad86e
title: Receptionist
employer: Wildern School
location: Southampton, South East, SO30 4EJ
region: Hampshire
salary: £24,796.00 Annually (FTE) Grade B – Step 1 - Actual Annual Salary £20,369.06 (which is equivalent to a full-time salary of £24,796)
closing_date: 2026-09-14T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-ff80cc91-b028-4603-910d-80547a4ad86e
hub_fingerprint: a757fc700d90cb9c8b7c01ff5b089946f031589e2df57323dae78f573e37907b
---

---
action:
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
action:
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
action:
POSS | Teaching Vacancies | Kent | Sheerness, South East, ME12 3AP | £8,557.00 - £8,693.00 Annually (Actual) | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-nore-academy
title: Receptionist
employer: Nore Academy
location: Sheerness, South East, ME12 3AP
region: Kent
salary: £8,557.00 - £8,693.00 Annually (Actual)
closing_date: 2026-09-04T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-nore-academy
hub_fingerprint: 1bc4d13ea6c2ee61d760d55cbded78b35311c5e01857d2d620f75de6e289be06
---

---
action:
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
action:
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
action:
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
action:
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
action:
POSS | Teaching Vacancies | London | Romford, London, RM3 8HN | £28,939.00 - £31,144.00 Annually (Actual) NJC Points 14-19, 36 hours per week, 39 weeks per year (term time only plus inset) | EHCP Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: ehcp-administrator-lime-academy-ravensbourne
title: EHCP Administrator
employer: Lime Academy Ravensbourne
location: Romford, London, RM3 8HN
region: London
salary: £28,939.00 - £31,144.00 Annually (Actual) NJC Points 14-19, 36 hours per week, 39 weeks per year (term time only plus inset)
closing_date: 2026-09-03T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/ehcp-administrator-lime-academy-ravensbourne
hub_fingerprint: 675c421b5e2025421aac51f36597db2c76b2eedbb1f6fef665e6cd552457ea1c
---

---
action:
POSS | Teaching Vacancies | Northamptonshire | Northampton, East Midlands, NN6 8PT | £26,846.00 Annually (FTE) £ 8217.92 actual salary | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-guilsborough-church-of-england-primary-school
title: Administrator
employer: Guilsborough Church of England Primary School
location: Northampton, East Midlands, NN6 8PT
region: Northamptonshire
salary: £26,846.00 Annually (FTE) £ 8217.92 actual salary
closing_date: 2026-08-24T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-guilsborough-church-of-england-primary-school
hub_fingerprint: 22b1e8be9c881daaaa578ae19feadbfb3c5b984dcf69d9788454c15371e3da67
---

---
action:
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
action:
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
action:
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
POSS | Teaching Vacancies | Sussex | Hove, South East, BN3 6ND | £29,064 | Administrative Assistants
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistants-cardinal-newman-catholic-school
title: Administrative Assistants
employer: Cardinal Newman Catholic School
location: Hove, South East, BN3 6ND
region: Sussex
salary: £29,064
closing_date: 2026-09-01T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistants-cardinal-newman-catholic-school
hub_fingerprint: 83b1640099c80f61be914a0e895179ea8fb5e9ead48d5e2757076c944c262350
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Knottingley, Yorkshire and the Humber, WF11 0BZ | £29,540.00 - £32,061.00 Annually (FTE) Grade F Points 14 to 19 (£29,540 to £32,061) Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary per annum for this job starts at £15,121.29 | Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-officer-2291e2c5-eec2-437c-a38c-78271e026f45
title: Data Officer
employer: De Lacy Academy
location: Knottingley, Yorkshire and the Humber, WF11 0BZ
region: Yorkshire - West
salary: £29,540.00 - £32,061.00 Annually (FTE) Grade F Points 14 to 19 (£29,540 to £32,061) Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary per annum for this job starts at £15,121.29
closing_date: 2026-09-01T23:59:00+01:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-officer-2291e2c5-eec2-437c-a38c-78271e026f45
hub_fingerprint: 8b12060fb4abb194d18a936722bba42871b57ebec6994531641d9447f68034a6
---

---
action:
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
