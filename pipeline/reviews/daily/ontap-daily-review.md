# Ontap daily job review

> **READY TO REVIEW**
> All active sources are current for 2026-08-27. You can start reviewing.

review_date: 2026-08-27
generated_at: 2026-08-27T16:41:03+00:00

**29 job(s) need a human decision.**

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
| JobG8 | OK | 2026-08-27 | 3 | — |
| NEJobs | OK | 2026-08-27 | 0 | — |
| VONNE | OK | 2026-08-27 | 0 | — |
| Teaching Vacancies | OK | 2026-08-27 | 26 | — |
| NHS Jobs | OK | 2026-08-27 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

## JobG8 — 3 to review

---
action:
POSS | JobG8 | Cheshire - Warrington & Halton | Warrington | £16 - £17 per hour | Part Time Corporate Receptionist
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225537956
title: Part Time Corporate Receptionist
employer: 
location: Warrington
region: Cheshire - Warrington & Halton
salary: £16 - £17 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 5d382e36d21bd2fabdb210e3732a69e6b387f805028a129f461465e6b776af91
---

---
action:
POSS | JobG8 | London | London | £50000 - £70000 per year | Associate Planner
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225431172
title: Associate Planner
employer: 
location: London
region: London
salary: £50000 - £70000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 4269db8173249c92071df2e358d8cd0f8cbee6ec7dd4d6b91f83cf05bce2a0c8
---

---
action:
POSS | JobG8 | Oxfordshire | Oxford | £180 per daily | Live in Care Assistant to 3rd year Biology Uni Student
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 107840646
title: Live in Care Assistant to 3rd year Biology Uni Student
employer: 
location: Oxford
region: Oxfordshire
salary: £180 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: ddc02da84976db89265b19f64e69afe2b4ba8ec011d28d7072a00780882a9682
---

## NEJobs — 0 to review

_No new or changed human decisions required._

## VONNE — 0 to review

_No new or changed human decisions required._

## Teaching Vacancies — 26 to review

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
POSS | Teaching Vacancies | Cambridgeshire | Huntingdon, PE28 5TQ | £32,061.00 Annually (Actual) | Marketing & Communications Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: marketing-communications-officer-c270ff05-b00d-453f-bd88-72dd6829c693
title: Marketing & Communications Officer
employer: Meridian Trust
location: Huntingdon, PE28 5TQ
region: Cambridgeshire
salary: £32,061.00 Annually (Actual)
closing_date: 2026-09-16T08:00:00+01:00
reason: Borderline school administration title: communications officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/marketing-communications-officer-c270ff05-b00d-453f-bd88-72dd6829c693
hub_fingerprint: 0960a6d92469214dc63f10631cdc196cb8445e6a6208cf3aa7ef2765b0f3b2f2
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
POSS | Teaching Vacancies | Dorset | Poole, South West, BH17 7EP | Grade E+2, Points 7-13. Actual salary: £22,152 - £24,384 pay award pending | Data Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-manager-parkstone-grammar-school
title: Data Manager
employer: Parkstone Grammar School
location: Poole, South West, BH17 7EP
region: Dorset
salary: Grade E+2, Points 7-13. Actual salary: £22,152 - £24,384 pay award pending
closing_date: 2026-09-23T09:00:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-manager-parkstone-grammar-school
hub_fingerprint: 68b4033b6884145e13e2547186ee7fe7bdec43ff2aba3dc53f8353272829c4b7
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
action: select
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
POSS | Teaching Vacancies | Yorkshire - South | Barnsley, S75 3SP | £25,583.00 - £25,989.00 Annually (Actual) | Estates and Compliance Coordinator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: estates-and-compliance-coordinator
title: Estates and Compliance Coordinator
employer: Hcat
location: Barnsley, S75 3SP
region: Yorkshire - South
salary: £25,583.00 - £25,989.00 Annually (Actual)
closing_date: 2026-09-11T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/estates-and-compliance-coordinator
hub_fingerprint: 8bc699e906077260a1a70371088800f642fdda911e46ba5261ffb25b2e944da1
---

---
action: select
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
