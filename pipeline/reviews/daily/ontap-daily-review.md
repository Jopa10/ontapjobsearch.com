# Ontap daily job review

> **READY TO REVIEW**
> All active sources are current for 2026-08-19. You can start reviewing.

review_date: 2026-08-19
generated_at: 2026-08-19T15:26:10+00:00

**29 job(s) need a human decision.**

Edit only each `action:` line:
- `action: select` = include the vacancy.
- `action: exclude` = reject the vacancy.
- Leave `action:` blank while you are still deciding it.
- The apply/publish workflow stops if any review item is still blank.
- Unchanged decisions are remembered by the source pipelines; they should not keep returning here.
- If the vacancy facts change, its fingerprint changes and it must be reviewed again.

## Source status

| Source | Status | Review date | Needs review | Note |
|---|---|---|---:|---|
| JobG8 | OK | 2026-08-19 | 4 | — |
| NEJobs | OK | 2026-08-19 | 0 | — |
| VONNE | OK | 2026-08-19 | 1 | — |
| Teaching Vacancies | OK | 2026-08-19 | 24 | — |
| NHS Jobs | FUTURE | — | 0 | adapter reserved; enable when NHS ingestion/review output is live |

## JobG8 — 4 to review

---
action: select
POSS | JobG8 | Bristol & Bath | Bristol | £15.83 - £17.95 per hour ((DOE)) | Finance & P2P Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 107863384
title: Finance & P2P Coordinator
employer: 
location: Bristol
region: Bristol & Bath
salary: £15.83 - £17.95 per hour ((DOE))
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 49c8686b7e7bbab7489f642146287b85797502c6b6745f996b84fc8082da3740
---

---
action: exclude
POSS | JobG8 | London | London | £22.78 per hour | Voids Administrator £22.78ph Southwark
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225510823
title: Voids Administrator £22.78ph Southwark
employer: 
location: London
region: London
salary: £22.78 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: ac46c4870bb812621b2ce44359e95ea601ed0b57b9b5a79755bbdbd283a3db46
---

---
action: exclude
POSS | JobG8 | Sussex | Sussex | £35000 - £45000 per year | Paraplanner
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: e49388ec-f35c-47c0-9694-51d60279812f
title: Paraplanner
employer: 
location: Sussex
region: Sussex
salary: £35000 - £45000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: af49338f4da3a2ba2b3f4aa6fd26dc39a3602d21c4ea886d5a962499270a8386
---

---
action: exclude
POSS | JobG8 | Yorkshire - North | York | £270 - £450 per daily | Interim Assistant Company Secretary/ Co-Sec Consultant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 8dda51f6-2fab-4c90-b591-83c818915198
title: Interim Assistant Company Secretary/ Co-Sec Consultant
employer: 
location: York
region: Yorkshire - North
salary: £270 - £450 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 02b32db518fc6ac80bca76fac23a2aff01abcd5cff2882069f6adf9dc339b4a5
---

## NEJobs — 0 to review

_No new or changed human decisions required._

## VONNE — 1 to review

---
action: select
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Northumberland | £31,005 Pro Rata | Community Engagement Tutor - Ashington Le…
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173341
title: Community Engagement Tutor - Ashington Le…
employer: Northern Learning Trust
location: Northumberland
region: North East - Tyneside, Wearside & Northumberland
salary: £31,005 Pro Rata
closing_date: 07 September 2026
reason: annualised upper salary £31,005 exceeds North East review point £30,000
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173341
hub_fingerprint: 2c6352550d888da09e5500ef21a008421b061df680e61497fbc6f0b3931c091c
---

## Teaching Vacancies — 24 to review

---
action: select
POSS | Teaching Vacancies | Cambridgeshire | Huntingdon, East of England, PE29 7DD | £25,583.00 - £25,989.00 Annually (FTE) NJC Scale 3, Points 5 to 6 . Actual salary £22,439.24 per annum on point 5. | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-st-peter-s-school
title: Office Administrator
employer: St Peter's School
location: Huntingdon, East of England, PE29 7DD
region: Cambridgeshire
salary: £25,583.00 - £25,989.00 Annually (FTE) NJC Scale 3, Points 5 to 6 . Actual salary £22,439.24 per annum on point 5.
closing_date: 2026-09-04T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-st-peter-s-school
hub_fingerprint: 98903f09aba0182997e8e97d60fa4a83200bb1dccdaa254e5b9084f29a953502
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
POSS | Teaching Vacancies | Dorset | Bournemouth, South West, BH10 4EX | £13,461.00 - £18,054.00 Annually (Actual) Term time only | Business and Administration Apprentice
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: business-and-administration-apprentice
title: Business and Administration Apprentice
employer: Glenmoor Academy
location: Bournemouth, South West, BH10 4EX
region: Dorset
salary: £13,461.00 - £18,054.00 Annually (Actual) Term time only
closing_date: 2026-08-31T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/business-and-administration-apprentice
hub_fingerprint: 29092433ad441a3397e241d3b9eee616a4ca92dd9902e8102671ae2f467eb5ba
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
POSS | Teaching Vacancies | London | Croydon, London, CR0 6NA | 19,807 FTE - £20,392 FTE. NJC Grade 5 SCP 13 - 15 (Outer London) | Admin Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: admin-assistant-chaffinch-brook-school
title: Admin Assistant
employer: Chaffinch Brook School
location: Croydon, London, CR0 6NA
region: London
salary: 19,807 FTE - £20,392 FTE. NJC Grade 5 SCP 13 - 15 (Outer London)
closing_date: 2026-08-28T00:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/admin-assistant-chaffinch-brook-school
hub_fingerprint: 1f010a519f80bac9ba99219721c8700348f43fb1a5ace5688a367e9649cd60ed
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
POSS | Teaching Vacancies | London | London, London, SE21 7AL | £30,225.00 - £31,530.00 Annually (FTE) Salary will be pro-rated for weeks and hours worked | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-dulwich-hamlet-junior-school
title: Administrative Assistant
employer: Dulwich Hamlet Junior School
location: London, London, SE21 7AL
region: London
salary: £30,225.00 - £31,530.00 Annually (FTE) Salary will be pro-rated for weeks and hours worked
closing_date: 2026-08-25T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-dulwich-hamlet-junior-school
hub_fingerprint: 045c10321854cbbe81a795fa45d18acb8929c7302c41abb52e4721e215a0a6b6
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
POSS | Teaching Vacancies | London | Upminster, London, RM14 1SF | £29,434 - £31,155 | Receptionist (Part-time)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-part-time-hall-mead-school
title: Receptionist (Part-time)
employer: Hall Mead School
location: Upminster, London, RM14 1SF
region: London
salary: £29,434 - £31,155
closing_date: 2026-09-07T15:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-part-time-hall-mead-school
hub_fingerprint: c2a445a9444eb71954d447a1dba190868daaec7ebb18ef6ca54d908f1e290fa5
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
action: select
POSS | Teaching Vacancies | Yorkshire - South | Doncaster, Yorkshire and the Humber, DN12 3LZ | £25,185.00 - £25,989.00 Annually (FTE) Grade C Points 4 to 6 (£25,185 to £25,989 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary per annum for this job starts at £19,481.25. | Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-morley-place-academy-doncaster-south-yorkshire
title: Administration Officer
employer: Morley Place Academy
location: Doncaster, Yorkshire and the Humber, DN12 3LZ
region: Yorkshire - South
salary: £25,185.00 - £25,989.00 Annually (FTE) Grade C Points 4 to 6 (£25,185 to £25,989 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary per annum for this job starts at £19,481.25.
closing_date: 2026-08-31T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-morley-place-academy-doncaster-south-yorkshire
hub_fingerprint: 543883dc6816bb7519a48ac1ca6c246c1f2944834e874a169de453b5f4ca5c43
---
