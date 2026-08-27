# Ontap daily job review

> **READY TO REVIEW**
> All active sources are current for 2026-08-27. You can start reviewing.

review_date: 2026-08-27
generated_at: 2026-08-27T18:24:24+00:00

**22 job(s) need a human decision.**

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
| JobG8 | OK | 2026-08-27 | 0 | — |
| NEJobs | OK | 2026-08-27 | 2 | — |
| VONNE | OK | 2026-08-27 | 1 | — |
| Teaching Vacancies | OK | 2026-08-27 | 19 | — |
| NHS Jobs | OK | 2026-08-27 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

## JobG8 — 0 to review

_No new or changed human decisions required._

## NEJobs — 2 to review

---
action:
POSS | NEJobs | North East - County Durham & Darlington/Hartlepool | Peterlee Depot (North) or Chi… | £29,071 - £32,046 | Waste Operations Support Officers
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301232
title: Waste Operations Support Officers
employer: Durham County Council
location: Peterlee Depot (North) or Chi…
region: North East - County Durham & Darlington/Hartlepool
salary: £29,071 - £32,046
closing_date: 09/09/2026
reason: annualised upper salary £32,046 exceeds North East review point £30,000
source_url: https://www.northeastjobs.org.uk/job/Waste_Operations_Support_Officers/301232
hub_fingerprint: f3c5201b4527562cfea1dd753f4cef3569a572d6e45f5afaf13818ff3ac2d0bf
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Gateshead | £29,540 - £32,061 | Annual Review Officer (SEND)
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301235
title: Annual Review Officer (SEND)
employer: Gateshead Council
location: Gateshead
region: North East - Tyneside, Wearside & Northumberland
salary: £29,540 - £32,061
closing_date: 10/09/2026
reason: transferable office/service title with specialist or borderline wording: send
source_url: https://www.northeastjobs.org.uk/job/Annual_Review_Officer_SEND/301235
hub_fingerprint: 539f1e70cedfa1d0623bddba811accf16f83ca16b211f8a136c34c51b05f31ae
---

## VONNE — 1 to review

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £29,02431,856 Pro Rata | Project Coordinator - Neuro Team
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173367
title: Project Coordinator - Neuro Team
employer: Children North East
location: Tyne and Wear
region: North East - Tyneside, Wearside & Northumberland
salary: £29,02431,856 Pro Rata
closing_date: Friday, September 11, 2026 - 12:00
reason: annualised upper salary £2,902,431,856 exceeds North East review point £30,000
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173367
hub_fingerprint: 4b73de766fa6377bed27958cd45b3006eac88a5e247386dd2c2cc4c768bae1c5
---

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
POSS | Teaching Vacancies | Worcestershire | Malvern, West Midlands, WR14 1WD | £28,598.00 - £31,022.00 Annually (FTE) | Examinations and Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: examinations-and-data-officer-dyson-perrins-cofe-academy-malvern-worcestershire
title: Examinations and Data Officer
employer: Dyson Perrins CofE Academy
location: Malvern, West Midlands, WR14 1WD
region: Worcestershire
salary: £28,598.00 - £31,022.00 Annually (FTE)
closing_date: 2026-09-02T23:59:00+01:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/examinations-and-data-officer-dyson-perrins-cofe-academy-malvern-worcestershire
hub_fingerprint: d18f74fb39819a7aba349f5681b439913cb1b9a91ea9289b85bfdbd5858ab8e7
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

---
action: select
POSS | Teaching Vacancies | Yorkshire - West | Pontefract, Yorkshire and the Humber, WF8 4JF | £20,971.00 - £21,300.00 pro rata (£24,796.00 - £25,185.00 FTE)per annum | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-the-king-s-school-pontefract-west-yorkshire
title: Receptionist
employer: The King's School
location: Pontefract, Yorkshire and the Humber, WF8 4JF
region: Yorkshire - West
salary: £20,971.00 - £21,300.00 pro rata (£24,796.00 - £25,185.00 FTE)per annum
closing_date: 2026-08-31T10:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-the-king-s-school-pontefract-west-yorkshire
hub_fingerprint: 8a699687f311a923a482da2b87ef13c03b310aa8f5744e506a899fcba06bc513
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
