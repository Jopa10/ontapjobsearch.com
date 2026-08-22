# Ontap daily job review

> **READY TO REVIEW**
> All active sources are current for 2026-08-22. You can start reviewing.

review_date: 2026-08-22
generated_at: 2026-08-22T10:50:41+00:00

**35 job(s) need a human decision.**

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
| JobG8 | OK | 2026-08-22 | 0 | — |
| NEJobs | OK | 2026-08-22 | 2 | — |
| VONNE | OK | 2026-08-22 | 0 | — |
| Teaching Vacancies | OK | 2026-08-22 | 33 | — |
| NHS Jobs | OK | 2026-08-22 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

## JobG8 — 0 to review

_No new or changed human decisions required._

## NEJobs — 2 to review

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
closing_date: 07/09/2026
reason: provisional transferable-office review
source_url: https://www.northeastjobs.org.uk/job/PA_Support_Officer/300972
hub_fingerprint: 0d54ebed6320ca9ca9c51d880324e49d8664d1020a69eef51141ba8fb0322a64
---

---
action: exclude
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Adult Social Care, Support Co… | £33,699 pa | Senior Support Coordinator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301056
title: Senior Support Coordinator
employer: South Tyneside Council
location: Adult Social Care, Support Co…
region: North East - Tyneside, Wearside & Northumberland
salary: £33,699 pa
closing_date: 11/09/2026 12:00
reason: transferable office/service title with specialist or borderline wording: senior
source_url: https://www.northeastjobs.org.uk/job/Senior_Support_Coordinator/301056
hub_fingerprint: ca2b8abad3c29153773256bc164707680711698f65dceb3561f052e18d80fe4c
---

## VONNE — 0 to review

_No new or changed human decisions required._

## Teaching Vacancies — 33 to review

---
action: select
POSS | Teaching Vacancies | Buckinghamshire | Milton Keynes, South East, MK17 8XY | £26,824.00 Annually (FTE) | Business Support
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: business-support-glebe-farm-school
title: Business Support
employer: Glebe Farm School
location: Milton Keynes, South East, MK17 8XY
region: Buckinghamshire
salary: £26,824.00 Annually (FTE)
closing_date: 2026-09-07T12:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/business-support-glebe-farm-school
hub_fingerprint: ff4e2fa439f30511242c8d92266a4d4581425b7f47787e842c48314faf13f703
---

---
action: select
POSS | Teaching Vacancies | Buckinghamshire | Milton Keynes, South East, MK17 8XY | £32,061.00 Annually (FTE) Grade F, £32, 061 full time equivalent | Executive Assistant to the Senior Leadership Team
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: executive-assistant-to-the-senior-leadership-team-glebe-farm-school
title: Executive Assistant to the Senior Leadership Team
employer: Glebe Farm School
location: Milton Keynes, South East, MK17 8XY
region: Buckinghamshire
salary: £32,061.00 Annually (FTE) Grade F, £32, 061 full time equivalent
closing_date: 2026-09-07T12:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/executive-assistant-to-the-senior-leadership-team-glebe-farm-school
hub_fingerprint: 5ebc0c4cecb3fa782ceb7fd0c3c1c6bb762b6c9a5a02c008010e427400a27dfc
---

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
POSS | Teaching Vacancies | Buckinghamshire | Milton Keynes, South East, MK7 6BZ | £26,923.00 Annually (Actual) | Office Administrator: EVC and Cover Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-evc-and-cover-manager-kents-hill-park-all-through-school
title: Office Administrator: EVC and Cover Manager
employer: Kents Hill Park all-through school
location: Milton Keynes, South East, MK7 6BZ
region: Buckinghamshire
salary: £26,923.00 Annually (Actual)
closing_date: 2026-09-08T12:00:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-evc-and-cover-manager-kents-hill-park-all-through-school
hub_fingerprint: 63cfb64e263d15aa1d1a0013494a910387380fe346d7bbca5db4b02877761c39
---

---
action: select
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
action: select
POSS | Teaching Vacancies | Devon | Exeter, EX5 3JG | FTE £25660 | Hub Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hub-administrator-cornerstone-academy-trust
title: Hub Administrator
employer: Cornerstone Academy Trust
location: Exeter, EX5 3JG
region: Devon
salary: FTE £25660
closing_date: 2026-08-23T23:59:59+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hub-administrator-cornerstone-academy-trust
hub_fingerprint: 8632b93a2797ae5da57cd72759bf5db5019cabff662d3086a3bc6e64b7a6ddc6
---

---
action: select
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
action: exclude
POSS | Teaching Vacancies | Hertfordshire | Chorleywood, WD3 6EW | £29,540.00 Annually (FTE) | HR Advisor
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-advisor-danes-educational-trust-chorleywood-not-recorded
title: HR Advisor
employer: Danes Educational Trust
location: Chorleywood, WD3 6EW
region: Hertfordshire
salary: £29,540.00 Annually (FTE)
closing_date: 2026-08-24T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-advisor-danes-educational-trust-chorleywood-not-recorded
hub_fingerprint: 68a628ac7a3086e1d665e629c7922d7567866426c544e90613f5ee61b4513d1b
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
POSS | Teaching Vacancies | London | Harrow, London, HA3 5RQ | £24,030.00 - £25,048.00 Annually (Actual) | Cover Supervisor Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: cover-supervisor-manager-whitefriars-school
title: Cover Supervisor Manager
employer: Whitefriars School
location: Harrow, London, HA3 5RQ
region: London
salary: £24,030.00 - £25,048.00 Annually (Actual)
closing_date: 2026-08-27T23:59:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/cover-supervisor-manager-whitefriars-school
hub_fingerprint: d2d816f046cb8cbc9a1c40b39436bd277fce6aeda4dc7b90e6a8929f8e728ca2
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
POSS | Teaching Vacancies | London | London, London, E20 2AE | £32,442.00 - £32,442.00 Annually (FTE) Inner London NJC 08 - £32,442 FTE, £28,496 pro rata | Senior Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: senior-administrator-bobby-moore-academy-london
title: Senior Administrator
employer: Bobby Moore Academy
location: London, London, E20 2AE
region: London
salary: £32,442.00 - £32,442.00 Annually (FTE) Inner London NJC 08 - £32,442 FTE, £28,496 pro rata
closing_date: 2026-08-23T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-administrator-bobby-moore-academy-london
hub_fingerprint: 5ec1e2a1d7ab713105ecd69444e5fe6d5692e9c36d1f11adaa190ea148288e72
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
POSS | Teaching Vacancies | London | London, London, W14 9BL | £35,827 – £38,754 per annum | Executive Assistant – Data Protection & Information Governance
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: executive-assistant-data-protection-information-governance
title: Executive Assistant – Data Protection & Information Governance
employer: Ealing, Hammersmith and West London College
location: London, London, W14 9BL
region: London
salary: £35,827 – £38,754 per annum
closing_date: 2026-09-04T12:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/executive-assistant-data-protection-information-governance
hub_fingerprint: 1eae465e73faf83186d4d44dccd3e7d08243c0d186c6744cedfaa0cd004c3f2e
---

---
action: select
POSS | Teaching Vacancies | London | Mitcham, London, CR4 2HZ | £13,007 (FTE Salary is £29,436) | Finance Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-administrator-beecholme-primary-school
title: Finance Administrator
employer: Beecholme Primary School
location: Mitcham, London, CR4 2HZ
region: London
salary: £13,007 (FTE Salary is £29,436)
closing_date: 2026-08-30T23:59:59+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-administrator-beecholme-primary-school
hub_fingerprint: db9c5ea983ebe8fce144fa268013c83ef7bdc700ae4cce7040a8730837afb91e
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
action: select
POSS | Teaching Vacancies | London | Sutton, SM3 8AB | £13,395.00 Annually (Actual) £33,129 (FTE) | HR Admin Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-admin-assistant-girls-learning-trust
title: HR Admin Assistant
employer: Girls' Learning Trust
location: Sutton, SM3 8AB
region: London
salary: £13,395.00 Annually (Actual) £33,129 (FTE)
closing_date: 2026-08-23T22:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-admin-assistant-girls-learning-trust
hub_fingerprint: 6de58d7f4564e60c00d239b014a71503e131ba7e65cb43111c8f90ca2e6d3ab3
---

---
action: select
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
action: exclude
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
closing_date: 2026-09-02T17:00:59+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-office-administrator-west-monkton-church-of-england-school
hub_fingerprint: b862f751d754649c3ff7f0a2eb133bdfdf6eee13390d7a0ca940f9cca8982d11
---

---
action: select
POSS | Teaching Vacancies | Somerset | Taunton, South West, TA4 2NE | £12,046 – 13,138 | Data Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-manager-kingsmead-academy
title: Data Manager
employer: Kingsmead Academy
location: Taunton, South West, TA4 2NE
region: Somerset
salary: £12,046 – 13,138
closing_date: 2026-09-06T23:59:59+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-manager-kingsmead-academy
hub_fingerprint: 6e2d92ee72be12f36bf0728afd7148e9c50bdd478c309a523fc73e63d57923f4
---

---
action: exclude
POSS | Teaching Vacancies | Somerset | Taunton, South West, TA4 2NE | £26,837 - £28,931 (CLF Grade C) | Senior Administration Assistant (SEND)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: senior-administration-assistant-send
title: Senior Administration Assistant (SEND)
employer: Kingsmead Academy
location: Taunton, South West, TA4 2NE
region: Somerset
salary: £26,837 - £28,931 (CLF Grade C)
closing_date: 2026-09-21T23:59:59+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-administration-assistant-send
hub_fingerprint: 5821db37bf6bd6fe6fb66851cb9aac5a9090962d76269fa6ce8b6ff2fc1f4c89
---

---
action: select
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
action: exclude
POSS | Teaching Vacancies | West Midlands - Birmingham & Solihull | Birmingham, B11 3ND | Circa £ 85,000.00 -negotiable dependent on candidate experience and qualifications. | Chief Finance and Operations Officer (CFOO)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: chief-finance-and-operations-officer-cfoo-create-partnership-trust
title: Chief Finance and Operations Officer (CFOO)
employer: Create Partnership Trust
location: Birmingham, B11 3ND
region: West Midlands - Birmingham & Solihull
salary: Circa £ 85,000.00 -negotiable dependent on candidate experience and qualifications.
closing_date: 2026-09-07T09:00:00+01:00
reason: Borderline school administration title: operations officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/chief-finance-and-operations-officer-cfoo-create-partnership-trust
hub_fingerprint: 984a648b116b744ad437bdfaa698fb38c6830bf5c7ce41084caa6ce39b28d924
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
