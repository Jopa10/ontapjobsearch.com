# Ontap daily job review

> **READY TO REVIEW**
> All active sources are current for 2026-09-17. You can start reviewing.

review_date: 2026-09-17
generated_at: 2026-09-17T16:58:31+00:00

**66 job(s) need a human decision.**

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
| JobG8 | OK | 2026-09-17 | 3 | — |
| NEJobs | OK | 2026-09-17 | 21 | — |
| VONNE | OK | 2026-09-17 | 2 | — |
| Teaching Vacancies | OK | 2026-09-17 | 40 | — |
| NHS Jobs | OK | 2026-09-17 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

## JobG8 — 3 to review

---
action:
POSS | JobG8 | Bedfordshire | Bedfordshire | £30000 - £35000 per year | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1944217
title: Accounts Assistant
employer: 
location: Bedfordshire
region: Bedfordshire
salary: £30000 - £35000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 4ebc48d624444b4ab6982179b917ca3a95c34d58124e3d049415d834a3197e24
---

---
action:
POSS | JobG8 | London | London | £40000 - £45000 per year | Accounts Assistant Credit Control
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1944215
title: Accounts Assistant Credit Control
employer: 
location: London
region: London
salary: £40000 - £45000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 1892e99a5fcf42fcefdc98123224dc63dcc7c8c6d748cddd963b17ab6267e8aa
---

---
action:
POSS | JobG8 | West Midlands - Birmingham & Solihull | Birmingham | £30,024 per annum | Admissions Avoidance Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 1939152
title: Admissions Avoidance Coordinator
employer: 
location: Birmingham
region: West Midlands - Birmingham & Solihull
salary: £30,024 per annum
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: e347b53ce953e813f5fe6d055ef34f31abd1c410b2ec8b7a697caedfd17142ab
---

## NEJobs — 21 to review

---
action:
POSS | NEJobs | North East - County Durham & Darlington/Hartlepool | Bishop Auckland | NALC Pay Scale LC1 spine poin… | Administrative Support Officer
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 302111
title: Administrative Support Officer
employer: Bishop Auckland Town Counc…
location: Bishop Auckland
region: North East - County Durham & Darlington/Hartlepool
salary: NALC Pay Scale LC1 spine poin…
closing_date: 30/09/2026 17:00
reason: annualised upper salary £62,489,700 exceeds North East review point £30,000
source_url: https://www.northeastjobs.org.uk/job/Administrative_Support_Officer/302111
hub_fingerprint: 3f1a1698396127e1e03e49f69eb38c30c1b91b2e702839e4486952760c77ece1
---

---
action:
POSS | NEJobs | North East - County Durham & Darlington/Hartlepool | Durham (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 256127
title: School Administrator
employer: First Class Supply & Train…
location: Durham (derived for filtering)
region: North East - County Durham & Darlington/Hartlepool
salary: From £14.54 - £15.20 per hour
closing_date: 31/01/2027
reason: agency-style advert with no structured employment location
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256127
hub_fingerprint: 02d2e89ca14b162b57fcbd858fc250bd82e0937959c0a0192f12755389f344ed
---

---
action:
POSS | NEJobs | North East - County Durham & Darlington/Hartlepool | Start Whitby Street Hartlepoo… | £32,578 - £34,811 per annum | Recovery Coordinator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301502
title: Recovery Coordinator
employer: Hartlepool Borough Council
location: Start Whitby Street Hartlepoo…
region: North East - County Durham & Darlington/Hartlepool
salary: £32,578 - £34,811 per annum
closing_date: 28/09/2026
reason: annualised upper salary £34,811 exceeds North East review point £30,000
source_url: https://www.northeastjobs.org.uk/job/Recovery_Coordinator/301502
hub_fingerprint: 9af1bf03b13ebdcd65d19e018a47f8b9fcd849d2fe4c7e03009eebebb284b6fc
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Bunny Hill Centre, Sunderland | £32046 - £34811 per annum (pr… | SEND Support Officer
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 302096
title: SEND Support Officer
employer: Together for Children - Su…
location: Bunny Hill Centre, Sunderland
region: North East - Tyneside, Wearside & Northumberland
salary: £32046 - £34811 per annum (pr…
closing_date: 29/09/2026
reason: transferable office/service title with specialist or borderline wording: send
source_url: https://www.northeastjobs.org.uk/job/SEND_Support_Officer/302096
hub_fingerprint: 8bd5696a8b0e24dc7b9acb24a607c71a5d41ed40498ba65daf39a2056c2f2638
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | City Hall, Plater Way, Sunder… | Grade 6 (SCP 22-25) £34,811 -… | Links for Life Coordinator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301406
title: Links for Life Coordinator
employer: Sunderland City Council
location: City Hall, Plater Way, Sunder…
region: North East - Tyneside, Wearside & Northumberland
salary: Grade 6 (SCP 22-25) £34,811 -…
closing_date: 27/09/2026
reason: annualised upper salary £37,563 exceeds North East review point £30,000
source_url: https://www.northeastjobs.org.uk/job/Links_for_Life_Coordinator/301406
hub_fingerprint: 69242a3a40a1200595139926c015b855f27d78d2987a68ae3b8ac51dc822aff5
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | County Hall MORPETH, United K… | £29,542 - 32,046 | Virtual School Education Support Offi…
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301765
title: Virtual School Education Support Offi…
employer: Northumberland County Coun…
location: County Hall MORPETH, United K…
region: North East - Tyneside, Wearside & Northumberland
salary: £29,542 - 32,046
closing_date: 23/09/2026 00:00
reason: annualised upper salary £32,046 exceeds North East review point £30,000
source_url: https://www.northeastjobs.org.uk/job/Virtual_School_Education_Support_Officer/301765
hub_fingerprint: d19ecc25cdec0e4e617b22c59e7cb01bb91f48095b44c0e3cbdbb962179228bf
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Gateshead | £27,709 - £29,071 | Holiday Activities and Food Programme…
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301954
title: Holiday Activities and Food Programme…
employer: Gateshead Council
location: Gateshead
region: North East - Tyneside, Wearside & Northumberland
salary: £27,709 - £29,071
closing_date: 27/09/2026
reason: provisional transferable-office review
source_url: https://www.northeastjobs.org.uk/job/Holiday_Activities_and_Food_Programme_Support_Officer/301954
hub_fingerprint: 247c84e1545d920df7951309f4c49c7c0495bc13ef6e08ee81906564e15681c9
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Harry Watts Academy, Ramillie… | £30,023 - £32,046 per annum.… | Lead Administrator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 302073
title: Lead Administrator
employer: Prosper Learning Trust
location: Harry Watts Academy, Ramillie…
region: North East - Tyneside, Wearside & Northumberland
salary: £30,023 - £32,046 per annum.…
closing_date: 05/10/2026 12:00
reason: transferable office/service title with specialist or borderline wording: lead
source_url: https://www.northeastjobs.org.uk/job/Lead_Administrator/302073
hub_fingerprint: 26d6ea8541727f591e707170920a0d38873261ca73bdf1b68531d5f847087d83
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Houghton Le Spring (derived f… | £27,274 to £29,071 (actual pr… | Attendance Administrator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301579
title: Attendance Administrator
employer: AIM High Academy Trust
location: Houghton Le Spring (derived f…
region: North East - Tyneside, Wearside & Northumberland
salary: £27,274 to £29,071 (actual pr…
closing_date: 21/09/2026 12:00
reason: transferable office/service title with specialist or borderline wording: attendance
source_url: https://www.northeastjobs.org.uk/job/Attendance_Administrator/301579
hub_fingerprint: 941798f28349950be7fc8bec2a95514382e736ea982ae5eccf4f8632c13ca3c8
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Housing Options and Homelessn… | £34,811 pa | Armed Forces Support Officer
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301778
title: Armed Forces Support Officer
employer: South Tyneside Council
location: Housing Options and Homelessn…
region: North East - Tyneside, Wearside & Northumberland
salary: £34,811 pa
closing_date: 24/09/2026 12:00
reason: annualised upper salary £34,811 exceeds North East review point £30,000
source_url: https://www.northeastjobs.org.uk/job/Armed_Forces_Support_Officer/301778
hub_fingerprint: 446cee5bb0fe0912dc5849afa83426d11377f90b279f1b6de7b992eaaea6b30a
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Middlefields, South Shields | £26,847 pa | Support Officer
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301983
title: Support Officer
employer: South Tyneside Council
location: Middlefields, South Shields
region: North East - Tyneside, Wearside & Northumberland
salary: £26,847 pa
closing_date: 22/09/2026 12:00
reason: provisional transferable-office review
source_url: https://www.northeastjobs.org.uk/job/Support_Officer/301983
hub_fingerprint: 598001e7e6272dbad7b5b56f0e895349ce45d88603fd24c75927e1029062ac74
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Newcastle (derived for filter… | From £14.54 - £15.20 per hour | School Administrator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 256122
title: School Administrator
employer: First Class Supply & Train…
location: Newcastle (derived for filter…
region: North East - Tyneside, Wearside & Northumberland
salary: From £14.54 - £15.20 per hour
closing_date: 31/01/2027
reason: agency-style advert with no structured employment location
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256122
hub_fingerprint: 0ba7c836bbec59052f0c965a0b13e26af5a2f8ffabbf1c95d24f91cdd90b6c0c
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Newcastle City Council (deriv… | £37,563 - £41,177 per annum | Housing Support Officer
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 300255
title: Housing Support Officer
employer: Newcastle City Council
location: Newcastle City Council (deriv…
region: North East - Tyneside, Wearside & Northumberland
salary: £37,563 - £41,177 per annum
closing_date: 21/09/2026 22:59
reason: transferable office/service title with specialist or borderline wording: housing
source_url: https://www.northeastjobs.org.uk/job/Housing_Support_Officer/300255
hub_fingerprint: b0a51b79c7ec9b332772b9d59a9593659b3ace2234f2594ca389a8b5573ee6bc
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | North Tyneside (derived for f… | From £14.54 - £15.20 per hour | School Administrator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 256121
title: School Administrator
employer: First Class Supply & Train…
location: North Tyneside (derived for f…
region: North East - Tyneside, Wearside & Northumberland
salary: From £14.54 - £15.20 per hour
closing_date: 31/01/2027
reason: agency-style advert with no structured employment location
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256121
hub_fingerprint: 47d8496b6175c959954a45a27c0555bd1ba8bdc45682bd57a2b4e2d9ac5da221
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Northumberland (derived for f… | From £14.54 - £15.20 per hour | School Administrator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 256120
title: School Administrator
employer: First Class Supply & Train…
location: Northumberland (derived for f…
region: North East - Tyneside, Wearside & Northumberland
salary: From £14.54 - £15.20 per hour
closing_date: 31/01/2027
reason: agency-style advert with no structured employment location
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256120
hub_fingerprint: be47dd99b3ea974cad9b194554b2b279d41e9137d4f9f7575ff13c3c018c3662
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Northumberland County Council… | £32,578 - 35,570 | Family Group Conference Coordinator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301692
title: Family Group Conference Coordinator
employer: Northumberland County Coun…
location: Northumberland County Council…
region: North East - Tyneside, Wearside & Northumberland
salary: £32,578 - 35,570
closing_date: 22/09/2026 00:00
reason: annualised upper salary £35,570 exceeds North East review point £30,000
source_url: https://www.northeastjobs.org.uk/job/Family_Group_Conference_Coordinator/301692
hub_fingerprint: 23df96a120c34fad815f07f0c14784798b3b4b909b27563fa6f805b3a1a21899
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | School Administrators require… | From £14.54 - £15.20 per hour | School Administrator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 256124
title: School Administrator
employer: First Class Supply & Train…
location: School Administrators require…
region: North East - Tyneside, Wearside & Northumberland
salary: From £14.54 - £15.20 per hour
closing_date: 31/01/2027
reason: agency-style advert with no structured employment location
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256124
hub_fingerprint: 68d5de6b0187dc6bcceddb9b4c479d0f3065d7a664fdc37d6bdded20332bf2a9
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | School Administrators require… | From £14.54 - £15.20per hour | School Administrator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 256125
title: School Administrator
employer: First Class Supply & Train…
location: School Administrators require…
region: North East - Tyneside, Wearside & Northumberland
salary: From £14.54 - £15.20per hour
closing_date: 31/01/2027
reason: agency-style advert with no structured employment location
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256125
hub_fingerprint: 0aacf8728c4710002f9830aa5cfac4a17584f5a50230c6779e4a8cf7969a92bf
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | South Tyneside Council (deriv… | £34,811 pa pro rata | Therapy Coordinator, 15 hpw (Term Tim…
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 302085
title: Therapy Coordinator, 15 hpw (Term Tim…
employer: South Tyneside Council
location: South Tyneside Council (deriv…
region: North East - Tyneside, Wearside & Northumberland
salary: £34,811 pa pro rata
closing_date: 02/10/2026 12:00
reason: annualised upper salary £34,811 exceeds North East review point £30,000
source_url: https://www.northeastjobs.org.uk/job/Therapy_Coordinator_15_hpw_Term_Time_Only_Bamburgh_School/302085
hub_fingerprint: f67b2680e4f53366377ac79b7cae7b8db9308fc3e3dbbd52370f90c91e808d23
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Sunderland (derived for filte… | From £14.54 - £15.20 per hour | School Administrator
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 256126
title: School Administrator
employer: First Class Supply & Train…
location: Sunderland (derived for filte…
region: North East - Tyneside, Wearside & Northumberland
salary: From £14.54 - £15.20 per hour
closing_date: 31/01/2027
reason: agency-style advert with no structured employment location
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256126
hub_fingerprint: b0014dd6e1e200c4df94de74bbca6de8c25cd3d36c1581236228bf07f316e3e4
---

---
action:
POSS | NEJobs | North East - Tyneside, Wearside & Northumberland | Walbottle Village Primary Sch… | £30,023 - £32,046 per annum p… | Attendance Officer
source_key: nejobs
source: NEJobs
category: admin_service
source_job_id: 301699
title: Attendance Officer
employer: Valour Multi Academy Trust
location: Walbottle Village Primary Sch…
region: North East - Tyneside, Wearside & Northumberland
salary: £30,023 - £32,046 per annum p…
closing_date: 21/09/2026 12:00
reason: transferable office/service title with specialist or borderline wording: attendance
source_url: https://www.northeastjobs.org.uk/job/Attendance_Officer/301699
hub_fingerprint: bb0a3c34c6e31bb578dad2a3a36369e680b5f122f86025d5a585f17b22eb295a
---

## VONNE — 2 to review

---
action:
POSS | VONNE | North East - County Durham & Darlington/Hartlepool | County Durham | £27,476 Per Annum | HR Administrator
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173410
title: HR Administrator
employer: Durham Cathedral
location: County Durham
region: North East - County Durham & Darlington/Hartlepool
salary: £27,476 Per Annum
closing_date: Friday, October 2, 2026 - 09:00
reason: transferable title with specialist or borderline wording: hr
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173410
hub_fingerprint: ec66fc3ca8c415471f51de328c7664c740b3c78a5ee28d7a398631ace1555f86
---

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Gateshead | £ Per Annum | Support Worker - Young People's 16+ Suppo…
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 171330
title: Support Worker - Young People's 16+ Suppo…
employer: Oasis Community Housing
location: Gateshead
region: North East - Tyneside, Wearside & Northumberland
salary: £ Per Annum
closing_date: 30 September 2026
reason: possible cross-source duplicate requires review
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=171330
hub_fingerprint: 97850c56d43de246e678011e9c360a2ce47a85694dee615f06b5093c12f974e5
---

## Teaching Vacancies — 40 to review

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
POSS | Teaching Vacancies | Berkshire | Reading, South East, RG1 5SL | £21,362.00 Annually (Actual) Grade 4 ( SCP 7-11) Term Time Only plus 5 INSET days. FTE £26,402 | Administrative Support Assistant - Pastoral
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-support-assistant-pastoral
title: Administrative Support Assistant - Pastoral
employer: Maiden Erlegh School in Reading
location: Reading, South East, RG1 5SL
region: Berkshire
salary: £21,362.00 Annually (Actual) Grade 4 ( SCP 7-11) Term Time Only plus 5 INSET days. FTE £26,402
closing_date: 2026-09-17T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-support-assistant-pastoral
hub_fingerprint: a4829cd1c0c9670ce0ced117cc730a934f49140da9ee94a09381a434570d8eb5
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
POSS | Teaching Vacancies | Essex | Rayleigh, SS6 7DD | £14,458.51 - £14,657.94 Annually (Actual) | Trust Finance Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: trust-finance-manager-schools-for-every-child
title: Trust Finance Manager
employer: Schools For Every Child
location: Rayleigh, SS6 7DD
region: Essex
salary: £14,458.51 - £14,657.94 Annually (Actual)
closing_date: 2026-09-25T12:00:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/trust-finance-manager-schools-for-every-child
hub_fingerprint: 62f2d30b181e267f96595525ce671c63bd30f59014d27d0f0ce2b5f023cf2aab
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
POSS | Teaching Vacancies | London | Croydon, London, CR0 2EA | £22,428.61 - £23,747.62 Annually (Actual) TPA 8 / NJC 6 - 10 - £30,841 - £32,655pa FTE | Finance & Admin Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-admin-assistant-broadmead-primary-school
title: Finance & Admin Assistant
employer: Broadmead Primary School
location: Croydon, London, CR0 2EA
region: London
salary: £22,428.61 - £23,747.62 Annually (Actual) TPA 8 / NJC 6 - 10 - £30,841 - £32,655pa FTE
closing_date: 2026-09-23T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-admin-assistant-broadmead-primary-school
hub_fingerprint: 4f0116840ff48bb80e1a3458cd5e5fe84b9e7d8cf0621aa0f7aa008995ce0191
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
POSS | Teaching Vacancies | London | London, EC4R 2SP | £24,004.70 - £24,895.91 Annually (Actual) | Governance Clerk
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-clerk-skinners-academies-trust
title: Governance Clerk
employer: Skinners' Academies Trust
location: London, EC4R 2SP
region: London
salary: £24,004.70 - £24,895.91 Annually (Actual)
closing_date: 2026-09-19T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-clerk-skinners-academies-trust
hub_fingerprint: f92205272bf757f0e7e9d82df59f47b0ba736398f8cb67702de1ae8fad5a6f73
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
POSS | Teaching Vacancies | Norfolk | Swaffham, East of England, PE37 7DZ | £20,301.39 - £22,713.69 Annually (Actual) £26,403 - £29,540 FTE - NJC Point 7 - Point 14 | HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-3181ac7d-997b-421c-bef0-d2cf34b118f1
title: HR Administrator
employer: The Nicholas Hamond Academy
location: Swaffham, East of England, PE37 7DZ
region: Norfolk
salary: £20,301.39 - £22,713.69 Annually (Actual) £26,403 - £29,540 FTE - NJC Point 7 - Point 14
closing_date: 2026-09-18T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-3181ac7d-997b-421c-bef0-d2cf34b118f1
hub_fingerprint: 64c8d24acb19ed8550cc147d8709b0b5c0e475a8fa02dfc354b7c529b20883da
---

---
action:
POSS | Teaching Vacancies | Norfolk | Thetford, East of England, IP26 4PE | £20,301.39 - £22,713.69 Annually (Actual) £26,403 - £29,540 FTE - NJC Point 7 - Point 14 | HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-iceni-secondary-academy-thetford-norfolk
title: HR Administrator
employer: Iceni Secondary Academy
location: Thetford, East of England, IP26 4PE
region: Norfolk
salary: £20,301.39 - £22,713.69 Annually (Actual) £26,403 - £29,540 FTE - NJC Point 7 - Point 14
closing_date: 2026-09-18T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-iceni-secondary-academy-thetford-norfolk
hub_fingerprint: c9fae85cca050124329b79301710123d4f9c1aa4c5d1892f89fff372f137ee11
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
POSS | Teaching Vacancies | Northamptonshire | Kettering, East Midlands, NN14 4AE | £26,846.00 - £27,274.00 Annually (FTE) Pro rata to £20,261.08 to £20,584.10 | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-cranford-cofe-primary-school
title: Administrator
employer: Cranford CofE Primary School
location: Kettering, East Midlands, NN14 4AE
region: Northamptonshire
salary: £26,846.00 - £27,274.00 Annually (FTE) Pro rata to £20,261.08 to £20,584.10
closing_date: 2026-09-25T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-cranford-cofe-primary-school
hub_fingerprint: 1c83ed24cd4c3947ed66e1be0d709121c14f6a10e1e7c210a46b9b3235e6643d
---

---
action:
POSS | Teaching Vacancies | Northamptonshire | Wellingborough, East Midlands, NN29 7PH | NJC Grade J, points 27 to 31 DOE | Trust Executive Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: trust-executive-assistant-wollaston-school
title: Trust Executive Assistant
employer: Wollaston School
location: Wellingborough, East Midlands, NN29 7PH
region: Northamptonshire
salary: NJC Grade J, points 27 to 31 DOE
closing_date: 2026-09-18T12:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/trust-executive-assistant-wollaston-school
hub_fingerprint: a8d8dbcdb04bc07f776b93b99d76a1696e353e2212919a0345f2df3b0d4071b9
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
