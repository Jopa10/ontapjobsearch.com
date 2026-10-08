# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-10-08
generated_at: 2026-10-08T20:02:22+00:00

**59 job(s) need a human decision.**

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
| JobG8 | OK | 2026-10-08 | 6 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | OK | 2026-10-08 | 9 | — |
| Teaching Vacancies | OK | 2026-10-08 | 44 | — |
| NHS Jobs | OK | 2026-10-08 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 6 to review

---
action:
POSS | JobG8 | Berkshire | Berkshire | — | Assistant Management Accountant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2089676
title: Assistant Management Accountant
employer: 
location: Berkshire
region: Berkshire
salary: 
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 783bc9ebbd2b766fba5f4ed6a6961ea9575f4015e6e99e9c05672763e0c96983
---

---
action:
POSS | JobG8 | Greater Manchester - North | Oldham | — | Assistant Accountant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2075771
title: Assistant Accountant
employer: 
location: Oldham
region: Greater Manchester - North
salary: 
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 084d95b7923807af06d9100292629875f182ce0c5a8e300815d02061c05b15af
---

---
action:
POSS | JobG8 | Kent | Kent | £21 - £24 per hour | Interim Part time Finance Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2093129
title: Interim Part time Finance Assistant
employer: 
location: Kent
region: Kent
salary: £21 - £24 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: fa4dfcb0f6e6ec922bcbf9e4312825561c40ac2ccf0958011ef913d080728565
---

---
action:
POSS | JobG8 | Lancashire - East | Blackburn | £27463 - £29947 per year | Assistant Accountant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2075598
title: Assistant Accountant
employer: 
location: Blackburn
region: Lancashire - East
salary: £27463 - £29947 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: baccc93524bc97dab9cdeb7b4723d1a2653230304e7293eeccb829ca635dd77d
---

---
action:
POSS | JobG8 | Lancashire - East | Blackburn | £35000 - £40000 per year | Credit Controllers
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2089047
title: Credit Controllers
employer: 
location: Blackburn
region: Lancashire - East
salary: £35000 - £40000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 5f07aeea688fdf7ece5b88fdfd8891c9c1e35c40e2552e515a26acca45b2ba8d
---

---
action:
POSS | JobG8 | Somerset | Somerset | — | Assistant Management Accountant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2092599
title: Assistant Management Accountant
employer: 
location: Somerset
region: Somerset
salary: 
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 6e970637ea678af2e766551f88e2525181b33f8b2b31525c3c825a38e4d0101c
---

## VONNE — 9 to review

---
action:
POSS | VONNE | North East | Regionwide | £29,542 to 30,515 Pro Rata | Going Green Together Project Officer (Mat…
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173468
title: Going Green Together Project Officer (Mat…
employer: VONNE
location: Regionwide
region: North East
salary: £29,542 to 30,515 Pro Rata
closing_date: Monday, October 12, 2026 - 11:59
reason: North East geography is generic or derived and requires review
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173468
hub_fingerprint: a93e500526be086d27835c303bb8954f57892aeaffbab7bbdfa02948393f374c
---

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Gateshead | £33,323 Per Annum | Business Support Coach
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173500
title: Business Support Coach
employer: Society Matters CIC
location: Gateshead
region: North East - Tyneside, Wearside & Northumberland
salary: £33,323 Per Annum
closing_date: 02 November 2026
reason: annualised upper salary £33,323 exceeds North East review point £30,000
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173500
hub_fingerprint: 9bbb8d10f73c17f8d4b630bcd6693c7b5a21d009e2c36ec6281f04d785f7f314
---

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Gateshead | £50,565 Per Annum | Solicitor
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173501
title: Solicitor
employer: Citizens Advice Gateshead
location: Gateshead
region: North East - Tyneside, Wearside & Northumberland
salary: £50,565 Per Annum
closing_date: 30 October 2026
reason: possible cross-source duplicate requires review
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173501
hub_fingerprint: 9d8facef757bd59e94c1af3d295c59d05b1a85b4967f63fea57fd6cba8bdb51e
---

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | South Tyneside | £15 Per Hour | Project Lead (STARCH)
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173401
title: Project Lead (STARCH)
employer: Churches Together in South Ty…
location: South Tyneside
region: North East - Tyneside, Wearside & Northumberland
salary: £15 Per Hour
closing_date: 30 October 2026
reason: transferable title with specialist or borderline wording: lead
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173401
hub_fingerprint: 745c52bdc73cf1fa6ff1edb614650a47144ec1a5370d7739027bf755617668bd
---

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £28,366 to 31,518 Pro Rata | Grant Holder Support Officer
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 172176
title: Grant Holder Support Officer
employer: Inspire South Tyneside
location: Tyne and Wear
region: North East - Tyneside, Wearside & Northumberland
salary: £28,366 to 31,518 Pro Rata
closing_date: Monday, October 26, 2026 - 17:00
reason: annualised upper salary £31,518 exceeds North East review point £30,000
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=172176
hub_fingerprint: 73aa505bd9a80f0d2b0e403e35b9a8c7b5896ea55b4f2cc962b3d60eeca22c06
---

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £28,366 to 31,518 Per Annum | Grant Holder Support Officer
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173484
title: Grant Holder Support Officer
employer: Connected Voice
location: Tyne and Wear
region: North East - Tyneside, Wearside & Northumberland
salary: £28,366 to 31,518 Per Annum
closing_date: Monday, October 26, 2026 - 17:00
reason: annualised upper salary £31,518 exceeds North East review point £30,000
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173484
hub_fingerprint: 0692f1655cde36573d37490cebfc62d248e248acf96051f5abb3adb9ee059f60
---

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £28,366 to 31,518 Pro Rata | Grant Holder Support Officer
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173497
title: Grant Holder Support Officer
employer: North Tyneside VODA
location: Tyne and Wear
region: North East - Tyneside, Wearside & Northumberland
salary: £28,366 to 31,518 Pro Rata
closing_date: Monday, October 26, 2026 - 17:00
reason: annualised upper salary £31,518 exceeds North East review point £30,000
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173497
hub_fingerprint: 26f73ba2c9818e136b261ec34499bb9fe3c1dbd8c27fb76159b3125be9f6225b
---

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £28,366 to 31,518 Pro Rata | Grant Holder Support Officer
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173508
title: Grant Holder Support Officer
employer: Voluntary and Community Actio…
location: Tyne and Wear
region: North East - Tyneside, Wearside & Northumberland
salary: £28,366 to 31,518 Pro Rata
closing_date: Monday, October 26, 2026 - 17:00
reason: annualised upper salary £31,518 exceeds North East review point £30,000
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173508
hub_fingerprint: 28840b037de54b9377a1ac9a230f3ebeabea6deb822aa34ae8c90ac2df73eda4
---

---
action:
POSS | VONNE | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £30,303 to 35,781 Per Annum | Housing Coordinator
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173522
title: Housing Coordinator
employer: The Angelou Centre
location: Tyne and Wear
region: North East - Tyneside, Wearside & Northumberland
salary: £30,303 to 35,781 Per Annum
closing_date: Saturday, October 31, 2026 - 05:00
reason: possible cross-source duplicate requires review
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173522
hub_fingerprint: 9a791612fd8851212007fe3180c86bf4bca74b3d791b1bdff6ecbd0cf2f1d62a
---

## Teaching Vacancies — 44 to review

---
action:
POSS | Teaching Vacancies | Bedfordshire | Dunstable, East of England, LU5 5AB | £24,792.00 - £26,425.00 Annually (Actual) | Data Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-manager-all-saints-academy-dunstable
title: Data Manager
employer: All Saints Academy Dunstable
location: Dunstable, East of England, LU5 5AB
region: Bedfordshire
salary: £24,792.00 - £26,425.00 Annually (Actual)
closing_date: 2026-10-13T09:00:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-manager-all-saints-academy-dunstable
hub_fingerprint: a3f6670a7c80caf349ae9b7dab56b2b5206262ad404d82d0807683118af1b737
---

---
action:
POSS | Teaching Vacancies | Berkshire | Reading, South East, RG5 3EU | £26,176.00 - £28,395.00 Annually (Actual) Term time only plus 10 additional days | Senior Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: senior-finance-assistant-the-bulmershe-school
title: Senior Finance Assistant
employer: The Bulmershe School
location: Reading, South East, RG5 3EU
region: Berkshire
salary: £26,176.00 - £28,395.00 Annually (Actual) Term time only plus 10 additional days
closing_date: 2026-10-23T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-finance-assistant-the-bulmershe-school
hub_fingerprint: 181a5d1ee58d25113d476ef0cb345a8810f62b57717ec4328fed4c7d205c7d90
---

---
action:
POSS | Teaching Vacancies | Buckinghamshire | Milton Keynes, South East, MK17 7AA | £23,130.12 Annually (Actual) Grade C1, £25, 989 Full time equivalent | Business Support (Level 1)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: business-support-level-1-b4e89671-af8b-4563-bce3-fee0f7ec4d1e
title: Business Support (Level 1)
employer: St Mary's Wavendon CofE Primary
location: Milton Keynes, South East, MK17 7AA
region: Buckinghamshire
salary: £23,130.12 Annually (Actual) Grade C1, £25, 989 Full time equivalent
closing_date: 2026-10-20T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/business-support-level-1-b4e89671-af8b-4563-bce3-fee0f7ec4d1e
hub_fingerprint: bc39b0c6913b078ecee3976a014209d7237b1d1ba1b762f8daa764f9626f7525
---

---
action:
POSS | Teaching Vacancies | Devon | Axminster, South West, EX13 7LX | £27,709.00 - £29,070.00 Annually (FTE) | Senior Pupil Services Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: senior-pupil-services-officer-all-saints-church-of-england-primary-school
title: Senior Pupil Services Officer
employer: All Saints Church of England Primary School
location: Axminster, South West, EX13 7LX
region: Devon
salary: £27,709.00 - £29,070.00 Annually (FTE)
closing_date: 2026-10-16T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-pupil-services-officer-all-saints-church-of-england-primary-school
hub_fingerprint: 0812a97a14455536f13ec6b71280988704744416d892b350bf4cff030419f1dd
---

---
action:
POSS | Teaching Vacancies | Devon | Exeter, South West, EX1 2SN | £27,709.00 - £29,070.00 Annually (FTE) | Senior Pupil Services officer - 2 days/week
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: senior-pupil-services-officer-2-days-week-st-michael-s-church-of-england-primary-academy
title: Senior Pupil Services officer - 2 days/week
employer: St Michael's Church of England Primary Academy
location: Exeter, South West, EX1 2SN
region: Devon
salary: £27,709.00 - £29,070.00 Annually (FTE)
closing_date: 2026-10-16T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/senior-pupil-services-officer-2-days-week-st-michael-s-church-of-england-primary-academy
hub_fingerprint: 874fd5e563c0f31c90cfb0bbbbbd1382dcea96a71f54fe744943f09bd2c09961
---

---
action:
POSS | Teaching Vacancies | Devon | Okehampton, South West, EX20 1PW | £24,400.00 - £26,014.00 Annually (Actual) NJC Grade D - Scale Point 8 to 12 | Data Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-manager-ede70353-55db-4cf7-a540-0e0c7cfc4b8a
title: Data Manager
employer: Okehampton College
location: Okehampton, South West, EX20 1PW
region: Devon
salary: £24,400.00 - £26,014.00 Annually (Actual) NJC Grade D - Scale Point 8 to 12
closing_date: 2026-10-13T23:59:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-manager-ede70353-55db-4cf7-a540-0e0c7cfc4b8a
hub_fingerprint: 0a8628bc959c37734efad450945d6d238b6b83d149816d94750b9e7c17f14e76
---

---
action:
POSS | Teaching Vacancies | Essex | Clacton On Sea, CO15 6DZ | £28,608.00 - £30,023.00 Annually (Actual) Local Government Scale 5, Point 10-13 | People Operations Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: people-operations-officer-the-sigma-trust
title: People Operations Officer
employer: The Sigma Trust
location: Clacton On Sea, CO15 6DZ
region: Essex
salary: £28,608.00 - £30,023.00 Annually (Actual) Local Government Scale 5, Point 10-13
closing_date: 2026-10-12T09:00:00+01:00
reason: Borderline school administration title: operations officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/people-operations-officer-the-sigma-trust
hub_fingerprint: e78f1c5dbd7678f22841220038e12b25df394a89f5b6dc61da320c1dfabe3f87
---

---
action:
POSS | Teaching Vacancies | Gloucestershire | Tewkesbury, South West, GL20 5SW | £18.00 - £25.00 Hourly Estimated total hours of 130 annually. Hourly rate of £18-£25 depending on experience, invoiced for work undertaken | Governance Professional / Clerk to the Trust Board
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-clerk-to-the-trust-board
title: Governance Professional / Clerk to the Trust Board
employer: Abbey View
location: Tewkesbury, South West, GL20 5SW
region: Gloucestershire
salary: £18.00 - £25.00 Hourly Estimated total hours of 130 annually. Hourly rate of £18-£25 depending on experience, invoiced for work undertaken
closing_date: 2026-10-12T23:59:00+01:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-clerk-to-the-trust-board
hub_fingerprint: 7236d19a95c6caac14eb68bfa0f91a7b5df86fd61184efc9a8aa2fdc8f253ebd
---

---
action:
POSS | Teaching Vacancies | Greater Manchester - Manchester & Salford | Manchester, North West, M15 4ZB | £14.14 per hour | Reception and Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: reception-and-administration-assistant-crown-street-primary-school
title: Reception and Administration Assistant
employer: Crown Street Primary School
location: Manchester, North West, M15 4ZB
region: Greater Manchester - Manchester & Salford
salary: £14.14 per hour
closing_date: 2026-10-17T09:00:59+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/reception-and-administration-assistant-crown-street-primary-school
hub_fingerprint: c9eb27c8e172140ebc8b78e7a4b158609510b744af885c9290676d078d4e1823
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
closing_date: 2026-10-19T09:00:59+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/reception-and-administration-assistant-didsbury-high-school
hub_fingerprint: 27399c91a357f076f7b80a3c4da522241944517ba134c7c2e10252c3c841822f
---

---
action:
POSS | Teaching Vacancies | Greater Manchester - North | Oldham, North West, OL9 0BN | 28,148.50 - 30,733.73 | MIS Systems and Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: mis-systems-and-data-officer
title: MIS Systems and Data Officer
employer: North Chadderton School
location: Oldham, North West, OL9 0BN
region: Greater Manchester - North
salary: 28,148.50 - 30,733.73
closing_date: 2026-11-02T12:00:00+00:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/mis-systems-and-data-officer
hub_fingerprint: be02beac6901e6d1acd83b0438d87f5a4245db2e08cd4b47bb2e981d72aa2d60
---

---
action:
POSS | Teaching Vacancies | Hertfordshire | Chorleywood, WD3 6EW | £30,515.00 Annually (FTE) | HR Advisor
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-advisor-d40681c8-89e4-43bc-8af3-fdfdebca5b15
title: HR Advisor
employer: Danes Educational Trust
location: Chorleywood, WD3 6EW
region: Hertfordshire
salary: £30,515.00 Annually (FTE)
closing_date: 2026-10-12T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-advisor-d40681c8-89e4-43bc-8af3-fdfdebca5b15
hub_fingerprint: 7404ca84e55a4935b886c413cd7cd7fc7cf9b0880ed973bdcb3e17e60f5b400f
---

---
action:
POSS | Teaching Vacancies | Hertfordshire | Harpenden, East of England, AL5 3AE | £17.15 Hourly Grade H5. £14.98 plus £2.17 holiday pay. Total £17.15 per hour | Governance Professional/Clerk to the Governing Board
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-clerk-to-the-governing-board-roundwood-park-school-harpenden-hertfordshire
title: Governance Professional/Clerk to the Governing Board
employer: Roundwood Park School
location: Harpenden, East of England, AL5 3AE
region: Hertfordshire
salary: £17.15 Hourly Grade H5. £14.98 plus £2.17 holiday pay. Total £17.15 per hour
closing_date: 2026-10-09T07:00:00+01:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-clerk-to-the-governing-board-roundwood-park-school-harpenden-hertfordshire
hub_fingerprint: 8cb586ef4258eb0613932cb57dd2fd54db689a201e44777143c466290319fe66
---

---
action:
POSS | Teaching Vacancies | Hertfordshire | Harpenden, East of England, AL5 5FH | £27,600.00 - £28,906.00 Annually (FTE) Actual salary: 30 hours, £20,128 - £21,080, 37 hours, £24,824 - £25,999 | Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-assistant-katherine-warington-school
title: Finance Assistant
employer: Katherine Warington School
location: Harpenden, East of England, AL5 5FH
region: Hertfordshire
salary: £27,600.00 - £28,906.00 Annually (FTE) Actual salary: 30 hours, £20,128 - £21,080, 37 hours, £24,824 - £25,999
closing_date: 2026-10-20T08:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-assistant-katherine-warington-school
hub_fingerprint: f0a9ba0af2c3b9d18d3e63358bd5f548293d83c239f8dc49f1be30cf99a60e63
---

---
action:
POSS | Teaching Vacancies | Hertfordshire | Royston, East of England, SG8 6EF | £26,403.00 - £28,142.00 Annually (FTE) NJC Scale 4, point 7 to 11 . Actual salary £22,645.65 per annum on point 7. | Pastoral Support Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: pastoral-support-assistant-86b70375-dc6e-4bfd-89a7-4e3cc367dd50
title: Pastoral Support Assistant
employer: Melbourn Village College
location: Royston, East of England, SG8 6EF
region: Hertfordshire
salary: £26,403.00 - £28,142.00 Annually (FTE) NJC Scale 4, point 7 to 11 . Actual salary £22,645.65 per annum on point 7.
closing_date: 2026-10-26T09:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/pastoral-support-assistant-86b70375-dc6e-4bfd-89a7-4e3cc367dd50
hub_fingerprint: 1f26c326a5f5f341d5c5f6f329b879c584ca7175450904664ffa315ad09ec892
---

---
action:
POSS | Teaching Vacancies | Hertfordshire | Stevenage, SG1 5BZ | £12,521.00 - £13,197.00 Annually (Actual) | Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-assistant-brighter-futures-educational-trust
title: Finance Assistant
employer: Brighter Futures Educational Trust
location: Stevenage, SG1 5BZ
region: Hertfordshire
salary: £12,521.00 - £13,197.00 Annually (Actual)
closing_date: 2026-10-09T23:59:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-assistant-brighter-futures-educational-trust
hub_fingerprint: 958fa0f35f84b6c99499253be798aaea0b0ea06498be374f3bdc936b662d46c8
---

---
action:
POSS | Teaching Vacancies | Lancashire - East | Nelson, North West, BB9 0PR | £29,130.00 Annually (Actual) | Operations Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: operations-officer-marsden-heights-community-college
title: Operations Officer
employer: Marsden Heights Community College
location: Nelson, North West, BB9 0PR
region: Lancashire - East
salary: £29,130.00 Annually (Actual)
closing_date: 2026-10-18T23:59:00+01:00
reason: Borderline school administration title: operations officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/operations-officer-marsden-heights-community-college
hub_fingerprint: 571f54c80fe6edc577f3225dd7e27fb34df38e71ff09f08c865f66677a11b8e2
---

---
action:
POSS | Teaching Vacancies | Leicestershire | Wigston, LE18 2AH | £24,741.00 - £27,334.00 Annually (Actual) Grade 10 | Payroll, Pensions and People Data Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: payroll-pensions-and-people-data-manager
title: Payroll, Pensions and People Data Manager
employer: Learn Academies Trust
location: Wigston, LE18 2AH
region: Leicestershire
salary: £24,741.00 - £27,334.00 Annually (Actual) Grade 10
closing_date: 2026-10-16T09:00:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/payroll-pensions-and-people-data-manager
hub_fingerprint: 0c34cb7eabf5c6cbf42b5836a1ea671e062e19999dfbe3b4171b25cfaa8791f8
---

---
action:
POSS | Teaching Vacancies | Lincolnshire | Grimsby, Yorkshire and the Humber, DN37 9EH | £26,016.00 - £26,847.00 Annually (FTE) Grade C Points 4 to 6 (£26,016 to £26,847 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary for this role is £22,475.98 | Administration Officer (7666)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-7666
title: Administration Officer (7666)
employer: John Whitgift Academy
location: Grimsby, Yorkshire and the Humber, DN37 9EH
region: Lincolnshire
salary: £26,016.00 - £26,847.00 Annually (FTE) Grade C Points 4 to 6 (£26,016 to £26,847 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary for this role is £22,475.98
closing_date: 2026-10-14T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-7666
hub_fingerprint: ee3d94a11154437058679c17eb71cca5f3577fe88a91be2c056b9b8cfd5d3f21
---

---
action:
POSS | Teaching Vacancies | London | Barking, London, IG11 9AG | £32,372.00 - £33,343.00 Annually (Actual) Scale 6 (Point 18 – £36,693 to Point 20 – £37,794 Full time) Prorated salary range is likely to be approx: £32,372 – £33,343, (dependant on experience, week per year and continuous service). Based on working 35 hours per week, Term time plus 10 days. | Exams and Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: exams-and-data-officer-001df384-4611-4e33-97d4-7c89842c0e25
title: Exams and Data Officer
employer: Barking Abbey School, A Specialist Sports and Humanities College
location: Barking, London, IG11 9AG
region: London
salary: £32,372.00 - £33,343.00 Annually (Actual) Scale 6 (Point 18 – £36,693 to Point 20 – £37,794 Full time) Prorated salary range is likely to be approx: £32,372 – £33,343, (dependant on experience, week per year and continuous service). Based on working 35 hours per week, Term time plus 10 days.
closing_date: 2026-10-16T09:00:00+01:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/exams-and-data-officer-001df384-4611-4e33-97d4-7c89842c0e25
hub_fingerprint: 950c33a0d72f2fd8fb378a63f9f1ce6dd4a46f90fa0aa49c2b14bd2c7c010fa2
---

---
action:
POSS | Teaching Vacancies | London | Loughton, IG10 3HE | £22,841.00 - £27,511.00 Annually (Actual) | Governance Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-manager-epping-forest-schools-partnership-trust
title: Governance Manager
employer: Epping Forest Schools Partnership Trust
location: Loughton, IG10 3HE
region: London
salary: £22,841.00 - £27,511.00 Annually (Actual)
closing_date: 2026-11-02T12:00:00+00:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-manager-epping-forest-schools-partnership-trust
hub_fingerprint: d7f93e70103c38a5ff59370e99396ef0dbb05d77f661d941aad010476f31d4d4
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
POSS | Teaching Vacancies | Merseyside - Liverpool | Liverpool, North West, L26 0TY | £28,153.00 - £31,015.00 Annually (FTE) | SEND / Pastoral Senior Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-pastoral-senior-administration-officer
title: SEND / Pastoral Senior Administration Officer
employer: Finch Woods Academy
location: Liverpool, North West, L26 0TY
region: Merseyside - Liverpool
salary: £28,153.00 - £31,015.00 Annually (FTE)
closing_date: 2026-10-22T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-pastoral-senior-administration-officer
hub_fingerprint: ce61bf7b69b543daf40054330972d57d1fd80d061762ff7debbf2df5eba32da8
---

---
action:
POSS | Teaching Vacancies | North East | Peterlee, North East, SR8 2RN | Scale 5: £25,230 - £26,034 | HR Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-assistant-east-durham-college
title: HR Assistant
employer: East Durham College
location: Peterlee, North East, SR8 2RN
region: North East
salary: Scale 5: £25,230 - £26,034
closing_date: 2026-10-19T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-assistant-east-durham-college
hub_fingerprint: 74770fca5b56bb3fbb64bec969db713bcf4691e91bf0fc2e4c1b5d726c71ed16
---

---
action:
POSS | Teaching Vacancies | North East | South Shields, North East, NE34 0QA | £22,768.00 Annually (Actual) Band 4 SCP 6 (pending the outcome of Job Evaluation) | Pastoral Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: pastoral-administration-assistant-st-wilfrid-s-rc-college
title: Pastoral Administration Assistant
employer: St Wilfrid's RC College
location: South Shields, North East, NE34 0QA
region: North East
salary: £22,768.00 Annually (Actual) Band 4 SCP 6 (pending the outcome of Job Evaluation)
closing_date: 2026-10-12T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/pastoral-administration-assistant-st-wilfrid-s-rc-college
hub_fingerprint: 41245e0a44f12dd0a0bc5dd1f7a60e96458b22685dfd55541dbc7cb85576bf39
---

---
action:
POSS | Teaching Vacancies | Nottinghamshire | Nottingham, East Midlands, NG5 4LT | £24,430.00 - £26,930.00 Annually (Actual) | Office Manager
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-manager-the-good-shepherd-catholic-primary-arnold
title: Office Manager
employer: The Good Shepherd Catholic Primary, Arnold
location: Nottingham, East Midlands, NG5 4LT
region: Nottinghamshire
salary: £24,430.00 - £26,930.00 Annually (Actual)
closing_date: 2026-10-09T09:00:00+01:00
reason: Manager title below £28,000 salary ceiling requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-manager-the-good-shepherd-catholic-primary-arnold
hub_fingerprint: d2a9272874ed70c87ce209a64c403b43336f2d65befd69245a7d9890edbc4906
---

---
action:
POSS | Teaching Vacancies | Nottinghamshire | Retford, DN22 7GR | £31,015.00 - £31,015.00 Annually (FTE) | Governance Professional
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-diverse-academies-trust
title: Governance Professional
employer: Diverse Academies Trust
location: Retford, DN22 7GR
region: Nottinghamshire
salary: £31,015.00 - £31,015.00 Annually (FTE)
closing_date: 2026-10-18T23:59:00+01:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-diverse-academies-trust
hub_fingerprint: 0fd18e428f420f099b2c2f995102effc391d48e8ccccbe7d368c865a5e86a967
---

---
action:
POSS | Teaching Vacancies | Oxfordshire | Oxford, South East, OX2 7WP | £26,824.00 - £29,065.00 Annually (FTE) Grade 6, term-time only + INSET days, 10.5 to 14 hours per week | Data Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-assistant-the-swan-school
title: Data Assistant
employer: The Swan School
location: Oxford, South East, OX2 7WP
region: Oxfordshire
salary: £26,824.00 - £29,065.00 Annually (FTE) Grade 6, term-time only + INSET days, 10.5 to 14 hours per week
closing_date: 2026-10-12T08:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-assistant-the-swan-school
hub_fingerprint: 892ebd9d9afd408d2b8cf94ca3459f070f18a105ff6538fd43528304e69dd3fb
---

---
action:
POSS | Teaching Vacancies | Suffolk | Ipswich, East of England, IP2 8PL | £25,646.00 - £26,920.00 Annually (Actual) | Finance, HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-hr-administrator-stoke-high-school-ormiston-academy
title: Finance, HR Administrator
employer: Stoke High School - Ormiston Academy
location: Ipswich, East of England, IP2 8PL
region: Suffolk
salary: £25,646.00 - £26,920.00 Annually (Actual)
closing_date: 2026-10-12T12:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-hr-administrator-stoke-high-school-ormiston-academy
hub_fingerprint: 5174e727b5ae20360364041adbc03c2e945349443ffef44a6635aad085ba23bb
---

---
action:
POSS | Teaching Vacancies | Surrey | Oxted, South East, RH8 0AB | £25,940.00 - £31,224.00 Annually (FTE) P4.1 to P5.6 | HR Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-assistant-oxted-school
title: HR Assistant
employer: Oxted School
location: Oxted, South East, RH8 0AB
region: Surrey
salary: £25,940.00 - £31,224.00 Annually (FTE) P4.1 to P5.6
closing_date: 2026-10-26T12:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-assistant-oxted-school
hub_fingerprint: 4e3e29da62d2c153f864558bb07614c88075635cfd9b5eee210c42c7976515bc
---

---
action:
POSS | Teaching Vacancies | Sussex | Bognor Regis, South East, PO22 8EL | £25,583 to £25,989 | Finance Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-administrator-felpham-community-college
title: Finance Administrator
employer: Felpham Community College
location: Bognor Regis, South East, PO22 8EL
region: Sussex
salary: £25,583 to £25,989
closing_date: 2026-10-19T09:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-administrator-felpham-community-college
hub_fingerprint: ae2346932fc466325030a03c4e1a1f3f9dd2982352df3bc65a1f732dfd88d483
---

---
action:
POSS | Teaching Vacancies | West Midlands - Birmingham & Solihull | Birmingham, West Midlands, B44 0JL | Birmingham Pay scale Grade 3, points 9 - 22 depending on experience | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-kings-rise-academy
title: Office Administrator
employer: Kings Rise Academy
location: Birmingham, West Midlands, B44 0JL
region: West Midlands - Birmingham & Solihull
salary: Birmingham Pay scale Grade 3, points 9 - 22 depending on experience
closing_date: 2026-10-19T15:00:00+01:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-kings-rise-academy
hub_fingerprint: 8cc8102f49135953eeb5e4d0f14f575c71c3127e3c7de6d548ba155c1c473609
---

---
action:
POSS | Teaching Vacancies | West Midlands - Black Country | Walsall, West Midlands, WS2 7NR | £28,523.00 - £28,523.00 Annually (Actual) Actual Starting Salary: £25,162.69 (FTE £28,523) | Head of House PA
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: head-of-house-pa-b63da4ba-19ba-4c61-9d9c-22c58869178c
title: Head of House PA
employer: Bloxwich Academy
location: Walsall, West Midlands, WS2 7NR
region: West Midlands - Black Country
salary: £28,523.00 - £28,523.00 Annually (Actual) Actual Starting Salary: £25,162.69 (FTE £28,523)
closing_date: 2026-11-01T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/head-of-house-pa-b63da4ba-19ba-4c61-9d9c-22c58869178c
hub_fingerprint: 0e50613d60c62f31b101efcf3beae6d506d92424c760705be3716a93f5858c1e
---

---
action:
POSS | Teaching Vacancies | West Midlands - Black Country | Wednesbury, West Midlands, WS10 9AR | £21,500.00 Annually (Actual) Sandwell Grade B pt 5 | Clerical Assistant- School Office
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: clerical-assistant-school-office
title: Clerical Assistant- School Office
employer: St John's Church of England Primary Academy
location: Wednesbury, West Midlands, WS10 9AR
region: West Midlands - Black Country
salary: £21,500.00 Annually (Actual) Sandwell Grade B pt 5
closing_date: 2026-10-14T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/clerical-assistant-school-office
hub_fingerprint: 30cdfebedb585faf8cc69cb7e35856c761b7b790d929d5a2ead6e9526a8029ae
---

---
action:
POSS | Teaching Vacancies | West Midlands - Coventry & Warwickshire | Coventry, CV1 5LY | Grade 4 - £26,847 to £30,515 per annum | MAT Compliance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: mat-compliance-officer
title: MAT Compliance Officer
employer: Sidney Stringer Multi Academy Trust
location: Coventry, CV1 5LY
region: West Midlands - Coventry & Warwickshire
salary: Grade 4 - £26,847 to £30,515 per annum
closing_date: 2026-10-23T11:59:59+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/mat-compliance-officer
hub_fingerprint: 135318a455542e830355f9fc0ef434a619d90079079cb32efdbd98fbd9b82833
---

---
action:
POSS | Teaching Vacancies | West Midlands - Coventry & Warwickshire | Nuneaton, West Midlands, CV11 6BH | £27,266- £29,783 | Administration Officer - Learning Support
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-learning-support
title: Administration Officer - Learning Support
employer: North Warwickshire and South Leicestershire College
location: Nuneaton, West Midlands, CV11 6BH
region: West Midlands - Coventry & Warwickshire
salary: £27,266- £29,783
closing_date: 2026-10-18T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-learning-support
hub_fingerprint: e4568f82babd871e68894f596f39e07ae620abe11738f40946cd4e22a61a3343
---

---
action:
POSS | Teaching Vacancies | Wiltshire | Swindon, SN4 9DL | £14.20 - £15.90 Hourly | Clerk to Governors
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: clerk-to-governors-grove-learning-trust
title: Clerk to Governors
employer: Grove Learning Trust
location: Swindon, SN4 9DL
region: Wiltshire
salary: £14.20 - £15.90 Hourly
closing_date: 2026-11-02T23:59:00+00:00
reason: Borderline school administration title: clerk to governors
source_url: https://teaching-vacancies.service.gov.uk/jobs/clerk-to-governors-grove-learning-trust
hub_fingerprint: c40077e13386562f829dcfcaa363dac20cade2e9ea8f815d4b44168b9afce998
---

---
action:
POSS | Teaching Vacancies | Worcestershire | Worcester, West Midlands, WR4 9SG | £26,016.00 - £26,016.00 Annually (FTE) Actual pro rata salary for term time only and part time hours £21,710 per annum | Administrative Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-finance-assistant-hollymount-school
title: Administrative Finance Assistant
employer: Hollymount School
location: Worcester, West Midlands, WR4 9SG
region: Worcestershire
salary: £26,016.00 - £26,016.00 Annually (FTE) Actual pro rata salary for term time only and part time hours £21,710 per annum
closing_date: 2026-11-23T12:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-finance-assistant-hollymount-school
hub_fingerprint: 79b1c6540a8d2333b1689f8825705e1a0d264cf8b8d22f7c3dfab5249f64bc13
---

---
action:
POSS | Teaching Vacancies | Yorkshire - East | Hull, HU7 4EY | £26,248 - £27,274 FTE £18,322 - £19,038 Actual | Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-humber-education-trust
title: Administration Officer
employer: Humber Education Trust
location: Hull, HU7 4EY
region: Yorkshire - East
salary: £26,248 - £27,274 FTE £18,322 - £19,038 Actual
closing_date: 2026-10-19T08:00:59+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-humber-education-trust
hub_fingerprint: a36e0ae220160b9371b595dd3f85536af5e62249604e5aab61ca1ce9520bbb75
---

---
action:
POSS | Teaching Vacancies | Yorkshire - North | Scarborough, Yorkshire and the Humber, YO11 1HS | £26,016.00 - £26,847.00 Annually (FTE) Grade C Points 4 to 6 (£26,016 to £26,847 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary per annum for this job starts at £12,149.18 | Administration Officer (7631)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-7631
title: Administration Officer (7631)
employer: Friarage Community Academy
location: Scarborough, Yorkshire and the Humber, YO11 1HS
region: Yorkshire - North
salary: £26,016.00 - £26,847.00 Annually (FTE) Grade C Points 4 to 6 (£26,016 to £26,847 Full Time Equivalent) subject to pro rata. The minimum actual pro rata salary per annum for this job starts at £12,149.18
closing_date: 2026-10-15T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-7631
hub_fingerprint: 401c6fa56e518d35e062fe2975d34a61e6c2d3e8c957b665c4a00bd404a34c2f
---

---
action:
POSS | Teaching Vacancies | Yorkshire - South | Sheffield, Yorkshire and the Humber, S13 8HH | £27,274.00 - £29,542.00 | Attendance & Admin Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: attendance-admin-officer-athelstan-primary-school
title: Attendance & Admin Officer
employer: Athelstan Primary School
location: Sheffield, Yorkshire and the Humber, S13 8HH
region: Yorkshire - South
salary: £27,274.00 - £29,542.00
closing_date: 2026-10-20T23:59:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/attendance-admin-officer-athelstan-primary-school
hub_fingerprint: 3f543bf6ccb5a8f5a44c725100c16da0a55d5a4d58fafe59e212c112356333f4
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Huddersfield, Yorkshire and the Humber, HD3 4HA | £25,224.32 - £27,362.35 Annually (Actual) Band E. Term time plus 1 day, 37hrs per week | Administration Officer - Attendance
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-attendance-royds-hall-a-share-academy
title: Administration Officer - Attendance
employer: Royds Hall, A Share Academy
location: Huddersfield, Yorkshire and the Humber, HD3 4HA
region: Yorkshire - West
salary: £25,224.32 - £27,362.35 Annually (Actual) Band E. Term time plus 1 day, 37hrs per week
closing_date: 2026-10-15T09:00:00+01:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-attendance-royds-hall-a-share-academy
hub_fingerprint: 55bf079885a8f814085019b7a0bd5c9aac75a5fb54cd99a04c75bff07556091e
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Leeds, Yorkshire and the Humber, LS16 5EA | £35,837.00 - £37,629.00 Annually (Actual) | Exams and Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: exams-and-data-officer-abbey-grange-church-of-england-academy
title: Exams and Data Officer
employer: Abbey Grange Church of England Academy
location: Leeds, Yorkshire and the Humber, LS16 5EA
region: Yorkshire - West
salary: £35,837.00 - £37,629.00 Annually (Actual)
closing_date: 2026-10-12T09:00:00+01:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/exams-and-data-officer-abbey-grange-church-of-england-academy
hub_fingerprint: 36ecc516582918b43ea846731daafca8dec5541652242b8f325b3b2e795398b1
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Shipley, Yorkshire and the Humber, BD18 3JE | £35,570.00 - £40,444.00 Annually (FTE) Band S01 - S02, SCP 17 to SCP 28 (Actual salary £30,732 - £35,267), 37 hours per week, TTO+5 days | Operations Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: operations-officer-bradford-alternative-provision-academy
title: Operations Officer
employer: Bradford Alternative Provision Academy
location: Shipley, Yorkshire and the Humber, BD18 3JE
region: Yorkshire - West
salary: £35,570.00 - £40,444.00 Annually (FTE) Band S01 - S02, SCP 17 to SCP 28 (Actual salary £30,732 - £35,267), 37 hours per week, TTO+5 days
closing_date: 2026-10-21T09:00:00+01:00
reason: Borderline school administration title: operations officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/operations-officer-bradford-alternative-provision-academy
hub_fingerprint: 4013d770805e4cc0eea428d0a789b5eac00dccf12a763ecc5e86e7539853c0e0
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
