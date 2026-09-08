# Ontap daily job review

> **READY TO REVIEW**
> All active sources are current for 2026-09-08. You can start reviewing.

review_date: 2026-09-08
generated_at: 2026-09-08T12:16:57+00:00

**31 job(s) need a human decision.**

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
| JobG8 | OK | 2026-09-08 | 0 | — |
| NEJobs | OK | 2026-09-08 | 3 | — |
| VONNE | OK | 2026-09-08 | 2 | — |
| Teaching Vacancies | OK | 2026-09-08 | 26 | — |
| NHS Jobs | OK | 2026-09-08 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

## JobG8 — 0 to review

_No new or changed human decisions required._

## NEJobs — 3 to review

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

## VONNE — 2 to review

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Northumberland | £29,998 to 33,000 Per Annum | Community Transport Network and Operation…
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173398
title: Community Transport Network and Operation…
employer: WATBus Community Tranport
location: Northumberland
region: North East - Tyneside, Wearside & Northumberland
salary: £29,998 to 33,000 Per Annum
closing_date: Monday, September 21, 2026 - 12:00
reason: annualised upper salary £33,000 exceeds North East review point £30,000
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173398
hub_fingerprint: 68d99b823ecc28062ab9df5b70ef3119dcfa7636d6e6b1a2ece7de4844337638
---

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Regionwide | £16,393 Per Annum | Community Engagement Officer
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173396
title: Community Engagement Officer
employer: West End Refugee Service
location: Regionwide
region: North East - Tyneside, Wearside & Northumberland
salary: £16,393 Per Annum
closing_date: Sunday, October 4, 2026 - 23:59
reason: provisional transferable-office review
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173396
hub_fingerprint: f4b4859830f8c2ef0db61f0bcd973dc92f2241ddcd575c9adafe13af726321c5
---

## Teaching Vacancies — 26 to review

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
POSS | Teaching Vacancies | Buckinghamshire | Milton Keynes, South East, MK10 7HE | £25,988.00 - £27,254.00 Annually (FTE) | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-brooklands-academy
title: Administrator
employer: Brooklands Academy
location: Milton Keynes, South East, MK10 7HE
region: Buckinghamshire
salary: £25,988.00 - £27,254.00 Annually (FTE)
closing_date: 2026-09-11T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-brooklands-academy
hub_fingerprint: 7191fb5804507cb5431e83433a37998b15af5ac70711379b4f2b579e16ddb470
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
POSS | Teaching Vacancies | Cambridgeshire | Peterborough, East of England, PE6 7JX | £14,802.00 Annually (Actual) | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-9219e9ba-082d-4b75-91ee-2e1cd2dd8f75
title: Administrator
employer: Arthur Mellows Village College
location: Peterborough, East of England, PE6 7JX
region: Cambridgeshire
salary: £14,802.00 Annually (Actual)
closing_date: 2026-09-14T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-9219e9ba-082d-4b75-91ee-2e1cd2dd8f75
hub_fingerprint: 3e5f9ed64f7da742098604816c1900d5f5dfd85e49c7035c3aa7956c1f05893f
---

---
action:
POSS | Teaching Vacancies | Hampshire | Southampton, South East, SO30 4EJ | £25,614.00 Annually (FTE) Grade B – Step 1 - Actual Annual Salary £21,041.02 (which is equivalent to a full-time salary of £25,614 | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-1dcaf299-1719-4cef-a999-af235a29010e
title: Receptionist
employer: Wildern School
location: Southampton, South East, SO30 4EJ
region: Hampshire
salary: £25,614.00 Annually (FTE) Grade B – Step 1 - Actual Annual Salary £21,041.02 (which is equivalent to a full-time salary of £25,614
closing_date: 2026-09-14T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-1dcaf299-1719-4cef-a999-af235a29010e
hub_fingerprint: e7ed49cede7be201db5b9035a63cc947436b9121c27346d0ad9a048ad48041b2
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
POSS | Teaching Vacancies | London | London, London, NW10 2UF | £27,254.00 Annually (FTE) Term Time Only | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-north-brent-school
title: Administrator
employer: North Brent School
location: London, London, NW10 2UF
region: London
salary: £27,254.00 Annually (FTE) Term Time Only
closing_date: 2026-09-11T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-north-brent-school
hub_fingerprint: 898c481e106602acca25562bfac7c2417b3798e8dbfdf831142db811422bfc07
---

---
action:
POSS | Teaching Vacancies | London | London, London, SE11 5QY | £26,857.00 - £27,240.00 Annually (Actual) Room for progression | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-lilian-baylis-technology-school
title: Receptionist
employer: Lilian Baylis Technology School
location: London, London, SE11 5QY
region: London
salary: £26,857.00 - £27,240.00 Annually (Actual) Room for progression
closing_date: 2026-09-18T10:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-lilian-baylis-technology-school
hub_fingerprint: fec4f4fd621cc0b06f9ff1820b53e9c68baaa4c63f2df821df77710884f62ef3
---

---
action:
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
closing_date: 2026-09-18T00:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/school-administrator-nishkam-school-west-london
hub_fingerprint: 7cdf9b6f05fd677f736344207c7faa9802fdda06b6610cb8a38b28759e55904f
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
closing_date: 2026-09-10T12:00:59+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-office-administrator-west-monkton-church-of-england-school
hub_fingerprint: 983d60adfc8385d957d783b3e6b0b33e165c61d135c22ec2f92dfdcc64ea8e0a
---

---
action:
POSS | Teaching Vacancies | West Midlands - Birmingham & Solihull | Birmingham, West Midlands, B28 8BB | £28,598.00 - £34,434.00 Annually (FTE) | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-yorkmead-junior-and-infant-school-birmingham-west-midlands
title: Office Administrator
employer: Yorkmead Junior and Infant School
location: Birmingham, West Midlands, B28 8BB
region: West Midlands - Birmingham & Solihull
salary: £28,598.00 - £34,434.00 Annually (FTE)
closing_date: 2026-10-05T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-yorkmead-junior-and-infant-school-birmingham-west-midlands
hub_fingerprint: 9b32191e5e262b521f6910ed8ae7afc72747bfc4c42bf8d41e3f63146e75a7fb
---

---
action:
POSS | Teaching Vacancies | West Midlands - Birmingham & Solihull | Birmingham, West Midlands, B45 0EU | £22,121.00 Annually (Actual) | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-king-edward-vi-balaam-wood-academy-birmingham-west-midlands
title: Receptionist
employer: King Edward VI Balaam Wood Academy
location: Birmingham, West Midlands, B45 0EU
region: West Midlands - Birmingham & Solihull
salary: £22,121.00 Annually (Actual)
closing_date: 2026-09-21T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-king-edward-vi-balaam-wood-academy-birmingham-west-midlands
hub_fingerprint: a1905a7e887a5f5e0f667ce28f3d2d66e460d6fe83635c756dcc383ebf0e0a48
---

---
action:
POSS | Teaching Vacancies | West Midlands - Birmingham & Solihull | Birmingham, West Midlands, B45 9BN | £6,072.00 - £6,072.00 Annually (Actual) | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-st-james-catholic-primary-school
title: Office Administrator
employer: St James Catholic Primary School
location: Birmingham, West Midlands, B45 9BN
region: West Midlands - Birmingham & Solihull
salary: £6,072.00 - £6,072.00 Annually (Actual)
closing_date: 2026-09-16T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-st-james-catholic-primary-school
hub_fingerprint: 93794985125b820b557a999b74afac410b51ed80259c8a312909d4be586c13ee
---

---
action:
POSS | Teaching Vacancies | West Midlands - Birmingham & Solihull | Solihull, West Midlands, B93 9AS | £8,804.90 Annually (Actual) Point 5-10 | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-bentley-heath-church-of-england-primary-school-solihull-west-midlands
title: Office Administrator
employer: Bentley Heath Church of England Primary School
location: Solihull, West Midlands, B93 9AS
region: West Midlands - Birmingham & Solihull
salary: £8,804.90 Annually (Actual) Point 5-10
closing_date: 2026-09-21T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-bentley-heath-church-of-england-primary-school-solihull-west-midlands
hub_fingerprint: 834ee7e5a7431debe66c7645bf55d0e9b4be0b4f197004569c1e4920b1f0bddd
---

---
action:
POSS | Teaching Vacancies | West Midlands - Coventry & Warwickshire | Coventry, West Midlands, CV3 2LP | £9,039.00 - £9,183.00 Annually (Actual) NJC pay scale Grade E 5-6 | Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-assistant-st-bartholomew-s-church-of-england-academy
title: Administration Assistant
employer: St Bartholomew's Church of England Academy
location: Coventry, West Midlands, CV3 2LP
region: West Midlands - Coventry & Warwickshire
salary: £9,039.00 - £9,183.00 Annually (Actual) NJC pay scale Grade E 5-6
closing_date: 2026-09-13T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-assistant-st-bartholomew-s-church-of-england-academy
hub_fingerprint: 7db5e7b280f02cca10caa3cb2d327a0018223e9b6a3dd3a4d37e373990bd287e
---

---
action:
POSS | Teaching Vacancies | Wiltshire | Chippenham, South West, SN15 1HE | £26,016.00 - £26,847.00 Annually (FTE) Actual Salary: £19,152-£19,763 per annum | Admin Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: admin-assistant-ivy-lane-primary-school
title: Admin Assistant
employer: Ivy Lane Primary School
location: Chippenham, South West, SN15 1HE
region: Wiltshire
salary: £26,016.00 - £26,847.00 Annually (FTE) Actual Salary: £19,152-£19,763 per annum
closing_date: 2026-09-25T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/admin-assistant-ivy-lane-primary-school
hub_fingerprint: 90ced07b3735f661a2fad5d151efd9c1f952aa29a6435b687e4076bc85c2c0ee
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Leeds, Yorkshire and the Humber, LS26 8EX | £22,373.00 - £23,087.00 Annually (Actual) Band 5, SCP 4 to 6, 37 hours per week, TTO plus 5 days | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-oulton-academy
title: Administrator
employer: Oulton Academy
location: Leeds, Yorkshire and the Humber, LS26 8EX
region: Yorkshire - West
salary: £22,373.00 - £23,087.00 Annually (Actual) Band 5, SCP 4 to 6, 37 hours per week, TTO plus 5 days
closing_date: 2026-09-21T10:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-oulton-academy
hub_fingerprint: f3e371a1949c58161632c40c7569f9e47f0a8086ce13b4293363a6ee14289b5f
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
