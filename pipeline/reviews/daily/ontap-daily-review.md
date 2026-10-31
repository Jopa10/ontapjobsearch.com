# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-10-31
generated_at: 2026-10-31T17:47:07+00:00

**47 job(s) await a human decision; 0 already answered (47 review rows).**

Edit only each `action:` line:
- `action: sel` (or `action: select`) = include the vacancy.
- `action: exc` (or `action: exclude`) = reject the vacancy.
- Leave `action:` blank while you are still deciding it.
- Up to 15 unresolved/bad action rows per source are fail-closed at job level: those jobs are withheld and flagged while the rest of that source can continue.
- More than 15 unresolved/bad action rows in one source isolate that source from the run; they do not block other clean sources.
- Unchanged decisions are remembered by the source pipelines; they should not keep returning here.
- If the vacancy facts change, its fingerprint changes and it must be reviewed again.

## Source status

| Source | Status | Review date | Needs review | Note |
|---|---|---|---:|---|
| JobG8 | OK | 2026-10-31 | 6 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | OK | 2026-10-31 | 1 | — |
| Teaching Vacancies | OK | 2026-10-31 | 40 | — |
| NHS Jobs | OK | 2026-10-31 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 6 to review

---
action:
POSS | JobG8 | Bristol & Bath | Bristol | £46,000 - £49,000 per year | Finance Business Partner - Charity
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2210130
title: Finance Business Partner - Charity
employer: 
location: Bristol
region: Bristol & Bath
salary: £46,000 - £49,000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: 6afdadf48f52f7ab37232fb565914b68af95d17b2f6cf6b0300a1b7380b17ad8
---

---
action:
POSS | JobG8 | Hampshire | Andover | £28697 - £31573 per year | Children's Home Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 1401785886
title: Children's Home Support Worker
employer: 
location: Andover
region: Hampshire
salary: £28697 - £31573 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 08c02bef280d28ae26a81f1b66395cd185858c3871da3fea368dd21909ac52c4
---

---
action:
POSS | JobG8 | Hampshire | Eastleigh | £32780 - £35564 per year (Market Supplement, plus Enhancements) | Secure Children's Home Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 1401786178
title: Secure Children's Home Support Worker
employer: 
location: Eastleigh
region: Hampshire
salary: £32780 - £35564 per year (Market Supplement, plus Enhancements)
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: ca9e1e80eace037b2b0dce5235d90e749553c799f86532c283ba45955ab83c8b
---

---
action:
POSS | JobG8 | Hampshire | Havant | £34273 - £37570 per year | Support Worker (Out of Hours)
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 1401785879
title: Support Worker (Out of Hours)
employer: 
location: Havant
region: Hampshire
salary: £34273 - £37570 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 88d6b43c6ddc8aaaf796ae4363cd99c407f41f6ca42ddf754034433948e5a7d5
---

---
action:
POSS | JobG8 | Hampshire | Southampton | £26018 - £27111 per year | Care Assistant (Older Adults)
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 1401786204
title: Care Assistant (Older Adults)
employer: 
location: Southampton
region: Hampshire
salary: £26018 - £27111 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 6cf78a055c60ede24ca0ad391cde270e9c7b8322ebe9d0f5898cf18f7d6d0ccd
---

---
action:
POSS | JobG8 | Oxfordshire | Oxfordshire | £45000 per year | Service Advisor
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108035379
title: Service Advisor
employer: 
location: Oxfordshire
region: Oxfordshire
salary: £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - owner-approved ordinary office role; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: 70fab3eb291c620ec821b8358fc5ab2957e217548862df8d80daf4b7dfd6da84
---

## VONNE — 1 to review

---
action:
POSS | VONNE | North East | Home-based | £35,000 to 39,000 Per Annum | Embedded Outreach Officer
source_key: vonne
source: VONNE
category: admin_service
source_job_id: 173627
title: Embedded Outreach Officer
employer: King's College Cambridge
location: Home-based
region: North East
salary: £35,000 to 39,000 Per Annum
closing_date: Monday, November 30, 2026 - 17:00
reason: North East geography is generic or derived and requires review
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173627
hub_fingerprint: f5e85f8c875dbbd1755d42a3fd3fadd1ec753490ebcaa5a54409942083552920
---

## Teaching Vacancies — 40 to review

---
action:
POSS | Teaching Vacancies | Berkshire | Reading, South East, RG5 4RF | £15,377.30 - £16,389.90 Annually (Actual) Grade 4 SCP 7 to 11 | Data & Exams Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-exams-assistant-waingels
title: Data & Exams Assistant
employer: Waingels
location: Reading, South East, RG5 4RF
region: Berkshire
salary: £15,377.30 - £16,389.90 Annually (Actual) Grade 4 SCP 7 to 11
closing_date: 2026-11-17T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-exams-assistant-waingels
hub_fingerprint: 40daef59e56fffc1eb5e4f892d4c5ac4c1255a97142c32693ba2db17c7cd9426
---

---
action:
POSS | Teaching Vacancies | Berkshire | Slough, SL3 8TX | FTE range £40,547.00 - £44,799.00 | Executive Assistant (Governance & Compliance Professional)
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: executive-assistant-governance-compliance-professional
title: Executive Assistant (Governance & Compliance Professional)
employer: Pioneer Educational Trust
location: Slough, SL3 8TX
region: Berkshire
salary: FTE range £40,547.00 - £44,799.00
closing_date: 2026-11-23T09:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/executive-assistant-governance-compliance-professional
hub_fingerprint: 907bd5db0ca605ceca13002f3422ba6cc8c820dd6a0e8ddf115b1ed3cff8eb26
---

---
action:
POSS | Teaching Vacancies | Cheshire - Warrington & Halton | Warrington, North West, WA2 0LN | £16,899.00 - £17,556.00 Annually (Actual) Grade 4: NJC SCP 6 to SCP 7 (Full year salary range £26,847 to £27,274; Actual Salary: £16,899 to £17,282 per annum) | Administrative Support Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-support-officer-padgate-academy-warrington
title: Administrative Support Officer
employer: Padgate Academy
location: Warrington, North West, WA2 0LN
region: Cheshire - Warrington & Halton
salary: £16,899.00 - £17,556.00 Annually (Actual) Grade 4: NJC SCP 6 to SCP 7 (Full year salary range £26,847 to £27,274; Actual Salary: £16,899 to £17,282 per annum)
closing_date: 2026-11-09T12:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-support-officer-padgate-academy-warrington
hub_fingerprint: a9e70965b87688612a80e1a56f39f07baef25e4c81cfe40cd91c2933f32b216a
---

---
action:
POSS | Teaching Vacancies | Cornwall | Liskeard, PL14 3EA | £32,046.00 - £34,811.00 Annually (FTE) Actual salary approx. £21,727 - £23,602 per annum | Governance Professional to Trust Board and Local Governing Committees
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-to-trust-board-and-local-governing-committees-1594a72d-d462-43fb-b443-b41012e611bd
title: Governance Professional to Trust Board and Local Governing Committees
employer: South East Cornwall Multi Academy Regional Trust
location: Liskeard, PL14 3EA
region: Cornwall
salary: £32,046.00 - £34,811.00 Annually (FTE) Actual salary approx. £21,727 - £23,602 per annum
closing_date: 2026-11-06T09:00:00+00:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-to-trust-board-and-local-governing-committees-1594a72d-d462-43fb-b443-b41012e611bd
hub_fingerprint: 3163723353a8c50ef50a1609120e9553eb1d28873d6c24a5a71ffa0bdd4bca16
---

---
action:
POSS | Teaching Vacancies | Derbyshire | Bakewell, East Midlands, DE45 1JA | £26,016.00 - £26,427.00 Annually (FTE) Actual Salary £14,306 to £14,532 per annum | School Business Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: school-business-assistant-lady-manners-school-bakewell-derbyshire
title: School Business Assistant
employer: Lady Manners School
location: Bakewell, East Midlands, DE45 1JA
region: Derbyshire
salary: £26,016.00 - £26,427.00 Annually (FTE) Actual Salary £14,306 to £14,532 per annum
closing_date: 2026-11-02T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/school-business-assistant-lady-manners-school-bakewell-derbyshire
hub_fingerprint: a390fbfbb469351d803783398bbade7cc9688da05466c79df40188b0dffd5ca9
---

---
action:
POSS | Teaching Vacancies | Derbyshire | Derby, DE22 1GB | £18,000.00 Annually (Actual) | Business Administration Apprentice Level 3
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: business-administration-apprentice-level-3-embark-multi-academy-trust
title: Business Administration Apprentice Level 3
employer: Embark Multi Academy Trust
location: Derby, DE22 1GB
region: Derbyshire
salary: £18,000.00 Annually (Actual)
closing_date: 2026-11-01T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/business-administration-apprentice-level-3-embark-multi-academy-trust
hub_fingerprint: 17b259c31c68bca8dc65a49d85a9d39fa82a83fbc6453bfc355fede98e690797
---

---
action:
POSS | Teaching Vacancies | Derbyshire | Hope Valley, East Midlands, S33 6SD | £26,427.00 - £26,847.00 Annually (FTE) Actual Salary £13,823 to £14,043 | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-d23e1267-9b18-4deb-8377-a4ade5fb90cf
title: Receptionist
employer: Hope Valley College
location: Hope Valley, East Midlands, S33 6SD
region: Derbyshire
salary: £26,427.00 - £26,847.00 Annually (FTE) Actual Salary £13,823 to £14,043
closing_date: 2026-11-02T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-d23e1267-9b18-4deb-8377-a4ade5fb90cf
hub_fingerprint: e6d284d149f2e863ff482e7eb99a70c916090b08b04ae6f1439faa3c5f2494de
---

---
action:
POSS | Teaching Vacancies | Essex | Brentwood, CM13 2HG | £29,361.00 - £30,776.00 Annually (FTE) | Operational Support Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: operational-support-assistant
title: Operational Support Assistant
employer: Discovery Educational Trust
location: Brentwood, CM13 2HG
region: Essex
salary: £29,361.00 - £30,776.00 Annually (FTE)
closing_date: 2026-11-15T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/operational-support-assistant
hub_fingerprint: a86d2532e556cd7f29d2e81a35860eb12cd70a4087bb4dadb40277fdae3873b3
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
closing_date: 2026-11-02T09:00:59+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/reception-and-administration-assistant-didsbury-high-school
hub_fingerprint: 01d656f3698f6eff35cdc94e5a7ee824ad991c40acaa621c0e1579ef59cd884d
---

---
action:
POSS | Teaching Vacancies | Greater Manchester - Manchester & Salford | Manchester, North West, M28 0SY | £25,820.00 - £28,323.00 Annually (FTE) United Learning Band 2 Vocational Payscale points 1 - 5 | Business Admin Apprentice - Data & Exams
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: business-admin-apprentice-data-exams
title: Business Admin Apprentice - Data & Exams
employer: The Lowry Academy
location: Manchester, North West, M28 0SY
region: Greater Manchester - Manchester & Salford
salary: £25,820.00 - £28,323.00 Annually (FTE) United Learning Band 2 Vocational Payscale points 1 - 5
closing_date: 2026-11-01T08:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/business-admin-apprentice-data-exams
hub_fingerprint: 51d985f2e6c15c7b8af98e168e590a99d9f7fcab1a6c79778b7e1479b9b7d0e1
---

---
action:
POSS | Teaching Vacancies | Hampshire | Portsmouth, South East, PO1 1FG | £22,814.00 - £24,728.00 Annually (Actual) | Administrative Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-officer-105487cf-80e2-4f7a-a8ea-cac5b40a9e6d
title: Administrative Officer
employer: Arundel Court Primary Academy and Nursery
location: Portsmouth, South East, PO1 1FG
region: Hampshire
salary: £22,814.00 - £24,728.00 Annually (Actual)
closing_date: 2026-11-01T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-officer-105487cf-80e2-4f7a-a8ea-cac5b40a9e6d
hub_fingerprint: 0d87644a8d5b77b89b3ab50bc07234b5a372fddab1bb7efab5c85f1793ef7d85
---

---
action:
POSS | Teaching Vacancies | Lancashire - East | Blackburn, North West, BB1 4ED | £34,357.00 Annually (FTE) 5 Inset days per year, plus an additional 3 planning days, at least one personal day per year | Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-officer-the-hyndburn-academy-blackburn-lancashire
title: Data Officer
employer: The Hyndburn Academy
location: Blackburn, North West, BB1 4ED
region: Lancashire - East
salary: £34,357.00 Annually (FTE) 5 Inset days per year, plus an additional 3 planning days, at least one personal day per year
closing_date: 2026-11-16T17:00:00+00:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-officer-the-hyndburn-academy-blackburn-lancashire
hub_fingerprint: 15c017ab5902be33a8f1ee4ee685a20589062efa57916b394779c771c984d67d
---

---
action:
POSS | Teaching Vacancies | Lancashire - East | Nelson, North West, BB9 0PR | £35,000.00 Annually (FTE) Local Government Pension, Health Care Cash Plan, Generous Staff Discount scheme, 3 extra inset days for planning, at least one personal leave day per year | Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-officer-marsden-heights-community-college
title: Data Officer
employer: Marsden Heights Community College
location: Nelson, North West, BB9 0PR
region: Lancashire - East
salary: £35,000.00 Annually (FTE) Local Government Pension, Health Care Cash Plan, Generous Staff Discount scheme, 3 extra inset days for planning, at least one personal leave day per year
closing_date: 2026-11-08T17:00:00+00:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-officer-marsden-heights-community-college
hub_fingerprint: 2fc0809e11b5cfb50d7e4302178cbf4260ecf179048b76635180e8c8d6beab27
---

---
action:
POSS | Teaching Vacancies | Leicestershire | Leicester, LE4 1EZ | £36,621.00 - £40,458.00 Annually (FTE) Approximate Starting Salary of £22,269.52 | Finance Business Partner
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-business-partner-discovery-schools-academies-trust-ltd
title: Finance Business Partner
employer: Discovery Schools Academies Trust Ltd
location: Leicester, LE4 1EZ
region: Leicestershire
salary: £36,621.00 - £40,458.00 Annually (FTE) Approximate Starting Salary of £22,269.52
closing_date: 2026-11-02T09:00:00+00:00
reason: Part-time finance requires actual earnings/hours and qualification checks
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-business-partner-discovery-schools-academies-trust-ltd
hub_fingerprint: 4eb23f701c13d5f7bff090bd6cb4ab968e51a07ca1a6549bc995828d7a322573
---

---
action:
POSS | Teaching Vacancies | London | Barking, London, IG11 0FU | £27,803.00 Annually (Actual) 5.12 Support Scale Already Pro-Rata | Attendance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: attendance-officer-riverside-bridge-school
title: Attendance Officer
employer: Riverside Bridge School
location: Barking, London, IG11 0FU
region: London
salary: £27,803.00 Annually (Actual) 5.12 Support Scale Already Pro-Rata
closing_date: 2026-11-03T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/attendance-officer-riverside-bridge-school
hub_fingerprint: 5286d83dac1f9538d319fc73996703d5fba1403ba378caaa20c50c425c553626
---

---
action:
POSS | Teaching Vacancies | London | Beckenham, London, BR3 1RF | £30,843.00 - £32,655.00 Annually (FTE) | Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-1d8ea2cf-23c2-491e-9778-888fe22529fb
title: Administration Officer
employer: Worsley Bridge Primary School
location: Beckenham, London, BR3 1RF
region: London
salary: £30,843.00 - £32,655.00 Annually (FTE)
closing_date: 2026-11-05T12:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-1d8ea2cf-23c2-491e-9778-888fe22529fb
hub_fingerprint: 82585250193bc9696bb0c1cb5ce6941e2639248fa246c50a1d88daf45291b745
---

---
action:
POSS | Teaching Vacancies | London | Carshalton, London, SM5 2PT | £30,408.00 - £32,655.00 Annually (FTE) | Finance & Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-administration-assistant-st-mary-s-rc-infants-school
title: Finance & Administration Assistant
employer: St Mary's RC Infants School
location: Carshalton, London, SM5 2PT
region: London
salary: £30,408.00 - £32,655.00 Annually (FTE)
closing_date: 2026-11-03T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-administration-assistant-st-mary-s-rc-infants-school
hub_fingerprint: 598884d4f0b7ea5790123f66b54a04ed06aa53f96b65d36cc940e319ccb6f160
---

---
action:
POSS | Teaching Vacancies | London | Feltham, TW13 4AB | £30,867.00 - £35,158.00 Annually (FTE) (SA6) (pay award pending) | Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-assistant-reach-schools
title: Finance Assistant
employer: Reach Schools
location: Feltham, TW13 4AB
region: London
salary: £30,867.00 - £35,158.00 Annually (FTE) (SA6) (pay award pending)
closing_date: 2026-11-06T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-assistant-reach-schools
hub_fingerprint: d3e4fa9bf6d6b3b107ce71a04a2c4284d3f90a095a437916fbcee48bf3925688
---

---
action:
POSS | Teaching Vacancies | London | London, London, E17 8HA | £31,290.00 - £33,129.00 Annually (FTE) Term-Time + 5 Inset days & 4 Plus days | Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-sybourn-primary-school-london
title: Administration Officer
employer: Sybourn Primary School
location: London, London, E17 8HA
region: London
salary: £31,290.00 - £33,129.00 Annually (FTE) Term-Time + 5 Inset days & 4 Plus days
closing_date: 2026-11-06T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-sybourn-primary-school-london
hub_fingerprint: 5a82d24380536d6c2373b279786f746f894d74c44968cc8ce93b4e5cf2cff493
---

---
action:
POSS | Teaching Vacancies | London | London, London, SE11 4AX | £33,036.00 Annually (FTE) | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-evolve-academy
title: Office Administrator
employer: Evolve Academy
location: London, London, SE11 4AX
region: London
salary: £33,036.00 Annually (FTE)
closing_date: 2026-10-31T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-evolve-academy
hub_fingerprint: 1c595b8ccad4c8e5153abb23157ac455d36e90b292ccfa42c85830f2550b7947
---

---
action:
POSS | Teaching Vacancies | London | Northolt, London, UB5 6AG | Grade 6 Pt 18 - 20 (£36,834 - £37,935) pro rata salary of £32,725 - £33,703Ppa | Transition, Assessment and Medical/Welfare Coordinator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: transition-assessment-and-medical-welfare-coordinator
title: Transition, Assessment and Medical/Welfare Coordinator
employer: Belvue School
location: Northolt, London, UB5 6AG
region: London
salary: Grade 6 Pt 18 - 20 (£36,834 - £37,935) pro rata salary of £32,725 - £33,703Ppa
closing_date: 2026-11-12T12:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/transition-assessment-and-medical-welfare-coordinator
hub_fingerprint: 2f91bf4e979b98586e74d747ab87be6b91fd13628e183f58f542c77ceae6878e
---

---
action:
POSS | Teaching Vacancies | London | Woodford Green, London, IG8 7DQ | £26,433.00 - £27,586.00 Annually (Actual) LBR4 (£30,288 - £31,611 full time equivalent) | Sixth Form Independent Study Supervisor
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: sixth-form-independent-study-supervisor
title: Sixth Form Independent Study Supervisor
employer: Woodbridge High School
location: Woodford Green, London, IG8 7DQ
region: London
salary: £26,433.00 - £27,586.00 Annually (Actual) LBR4 (£30,288 - £31,611 full time equivalent)
closing_date: 2026-11-09T09:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/sixth-form-independent-study-supervisor
hub_fingerprint: 6f62c9ef655ee246d733ab464506284137faf559e09117d4b260c4db5abbf749
---

---
action:
POSS | Teaching Vacancies | North East | Blyth, NE24 2SY | £25,147.00 - £26,414.00 Annually (Actual) Whole Time | HR & Payroll Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-payroll-administrator-emmanuel-schools-foundation-blyth-not-recorded
title: HR & Payroll Administrator
employer: Emmanuel Schools Foundation
location: Blyth, NE24 2SY
region: North East
salary: £25,147.00 - £26,414.00 Annually (Actual) Whole Time
closing_date: 2026-11-12T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-payroll-administrator-emmanuel-schools-foundation-blyth-not-recorded
hub_fingerprint: ae6df7a792d9bc36c269f5779bc2de6204735718d67e67b492010c0ebb96c09b
---

---
action:
POSS | Teaching Vacancies | Nottinghamshire | Nottingham, East Midlands, NG9 3DU | £22,630.72 - £23,356.04 Annually (Actual) NJE Grade 3, Pts 5 to 7 £26,427 - £27,274 (FTE) | Attendance and Inclusion Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: attendance-and-inclusion-administration-officer-alderman-white-school
title: Attendance and Inclusion Administration Officer
employer: Alderman White School
location: Nottingham, East Midlands, NG9 3DU
region: Nottinghamshire
salary: £22,630.72 - £23,356.04 Annually (Actual) NJE Grade 3, Pts 5 to 7 £26,427 - £27,274 (FTE)
closing_date: 2026-11-02T09:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/attendance-and-inclusion-administration-officer-alderman-white-school
hub_fingerprint: 6c61b9df79795adb41de75bccaf1897ac3c43aa2c7fe3b9587c2e78da347fe04
---

---
action:
POSS | Teaching Vacancies | Oxfordshire | Witney, South East, OX28 1DX | £27,151.00 - £28,981.00 Annually (Actual) Grade 7 | Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: data-officer-wood-green-school-witney-oxfordshire
title: Data Officer
employer: Wood Green School
location: Witney, South East, OX28 1DX
region: Oxfordshire
salary: £27,151.00 - £28,981.00 Annually (Actual) Grade 7
closing_date: 2026-11-04T12:00:00+00:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/data-officer-wood-green-school-witney-oxfordshire
hub_fingerprint: af4f10dd7e97bf41ce82f77a12165a7004f641944868b3fd94bb8b79b369c105
---

---
action:
POSS | Teaching Vacancies | Suffolk | Beccles, East of England, NR34 7BQ | £19,350- £22,735 actual pa | Finance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-officer-beccles-high-school
title: Finance Officer
employer: Beccles High School
location: Beccles, East of England, NR34 7BQ
region: Suffolk
salary: £19,350- £22,735 actual pa
closing_date: 2026-12-20T00:00:00+00:00
reason: Part-time finance requires actual earnings/hours and qualification checks
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-officer-beccles-high-school
hub_fingerprint: 4a5356c76d977c8c145bcf16e9282ef27043d6688a16732aea68d3666a436baa
---

---
action:
POSS | Teaching Vacancies | Suffolk | Ipswich, East of England, IP1 6QD | £26,016.00 - £26,847.00 Annually (FTE) | SEND Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-administrator-castle-hill-junior-school
title: SEND Administrator
employer: Castle Hill Junior School
location: Ipswich, East of England, IP1 6QD
region: Suffolk
salary: £26,016.00 - £26,847.00 Annually (FTE)
closing_date: 2026-11-05T13:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-administrator-castle-hill-junior-school
hub_fingerprint: 3fc3d115d1d750fbf2201a85f394c8425dc30ee14c91c7d821d5298db1adee4e
---

---
action:
POSS | Teaching Vacancies | Surrey | Sunbury-on-Thames, South East, TW16 6LF | £24,570.00 - £26,730.00 Annually (Actual) P5 (FTE £28,700 to £31,224pa) | SEND Adminstrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-adminstrator
title: SEND Adminstrator
employer: Sunbury Manor School
location: Sunbury-on-Thames, South East, TW16 6LF
region: Surrey
salary: £24,570.00 - £26,730.00 Annually (Actual) P5 (FTE £28,700 to £31,224pa)
closing_date: 2026-11-02T09:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-adminstrator
hub_fingerprint: 8d3f1f622369904927fb2d936e92da7017300125e9979d6de93c772eedd9d0e8
---

---
action:
POSS | Teaching Vacancies | Sussex | Lewes, South East, BN7 3AE | Between £25,729 - £28,796 per annum | EAG Advisor
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: eag-advisor
title: EAG Advisor
employer: Plumpton College
location: Lewes, South East, BN7 3AE
region: Sussex
salary: Between £25,729 - £28,796 per annum
closing_date: 2026-11-01T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/eag-advisor
hub_fingerprint: 65330ec985d2cf1ad11a914e74a0b39a443c12afcf4dbe6316f31294628f1435
---

---
action:
POSS | Teaching Vacancies | West Midlands - Black Country | Halesowen, West Midlands, B63 4HY | £22,812.00 - £22,812.00 Monthly | Administration Assistant - Level 2
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-assistant-level-2-huntingtree-primary-school
title: Administration Assistant - Level 2
employer: Huntingtree Primary School
location: Halesowen, West Midlands, B63 4HY
region: West Midlands - Black Country
salary: £22,812.00 - £22,812.00 Monthly
closing_date: 2026-11-08T23:59:00+00:00
reason: Salary period needs verification
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-assistant-level-2-huntingtree-primary-school
hub_fingerprint: 8e7ea3615ad44fba107a44d85a251885d963b5c581ca1edb6b5f5264e86520d6
---

---
action:
POSS | Teaching Vacancies | Wiltshire | Salisbury, South West, SP1 1QX | £26,847.00 - £27,709.00 Annually (FTE) Grade E, pay point 6-8, £26,847 - £27,709 per annum (DOE) FTE | Clerk to Governors
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: clerk-to-governors-st-andrew-s-church-of-england-voluntary-aided-primary-school-laverstock
title: Clerk to Governors
employer: St Andrew's Church of England Voluntary Aided Primary School, Laverstock
location: Salisbury, South West, SP1 1QX
region: Wiltshire
salary: £26,847.00 - £27,709.00 Annually (FTE) Grade E, pay point 6-8, £26,847 - £27,709 per annum (DOE) FTE
closing_date: 2026-11-18T23:59:00+00:00
reason: Borderline school administration title: clerk to governors
source_url: https://teaching-vacancies.service.gov.uk/jobs/clerk-to-governors-st-andrew-s-church-of-england-voluntary-aided-primary-school-laverstock
hub_fingerprint: 843580bd06ce2b6fec39b8be9f16dd22c8a51ab62c0ea23b2b0d58cb9085d048
---

---
action:
POSS | Teaching Vacancies | Wiltshire | Salisbury, South West, SP4 6JZ | £26,847.00 - £27,709.00 Annually (FTE) Grade E, pay point 6-8, £26,847 - £27,709 per annum (DOE) FTE | Clerk to Governors
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: clerk-to-governors-gomeldon-primary-school
title: Clerk to Governors
employer: Gomeldon Primary School
location: Salisbury, South West, SP4 6JZ
region: Wiltshire
salary: £26,847.00 - £27,709.00 Annually (FTE) Grade E, pay point 6-8, £26,847 - £27,709 per annum (DOE) FTE
closing_date: 2026-11-22T23:59:00+00:00
reason: Borderline school administration title: clerk to governors
source_url: https://teaching-vacancies.service.gov.uk/jobs/clerk-to-governors-gomeldon-primary-school
hub_fingerprint: b46f094eaae6940cee885eca2ad73745ee4f1c795a6b2fad08f2ac6b85c874d0
---

---
action:
POSS | Teaching Vacancies | Worcestershire | Pershore, West Midlands, WR10 2ER | £21,938.00 Annually (FTE) SC4 | Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-assistant-pinvin-cofe-academy-pershore-worcestershire
title: Finance Assistant
employer: Pinvin CofE Academy
location: Pershore, West Midlands, WR10 2ER
region: Worcestershire
salary: £21,938.00 Annually (FTE) SC4
closing_date: 2026-11-30T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-assistant-pinvin-cofe-academy-pershore-worcestershire
hub_fingerprint: 328262491bea67c72c4c3fd1afe5ccad2319bf490a63885a6820c140c6af5ce8
---

---
action:
POSS | Teaching Vacancies | Worcestershire | Worcester, WR4 9SG | £27,273.00 - £27,273.00 Annually (FTE) Casual zero hour contract - hourly rate | Governance Professional/Clerk
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-clerk-the-black-pear-trust-worcester-not-recorded
title: Governance Professional/Clerk
employer: The Black Pear Trust
location: Worcester, WR4 9SG
region: Worcestershire
salary: £27,273.00 - £27,273.00 Annually (FTE) Casual zero hour contract - hourly rate
closing_date: 2026-11-04T12:00:00+00:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-clerk-the-black-pear-trust-worcester-not-recorded
hub_fingerprint: 39f3f9a18e6c01661c51631710fe8625933be49e575ca4b3d10fd33108ad5054
---

---
action:
POSS | Teaching Vacancies | Yorkshire - North | York, YO24 2RU | £19,740.94 - £20,616.86 Annually (Actual) Grade 5, Level 1-4 (£27,631 to £28,857 FTE) | Trust Data Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: trust-data-officer-excel-learning-trust
title: Trust Data Officer
employer: Excel Learning Trust
location: York, YO24 2RU
region: Yorkshire - North
salary: £19,740.94 - £20,616.86 Annually (Actual) Grade 5, Level 1-4 (£27,631 to £28,857 FTE)
closing_date: 2026-11-15T23:59:00+00:00
reason: Borderline school administration title: data officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/trust-data-officer-excel-learning-trust
hub_fingerprint: ae80d379c2539a5e78349fa075c237173b1af05d68dd801c84411d47d60780a4
---

---
action:
POSS | Teaching Vacancies | Yorkshire - North | York, Yorkshire and the Humber, YO32 4BZ | Grade 4, Level 1-4 (£25,948 to £27,188 p.a.) reduced pro rata to £22,280 to £23,345 (calculated on full time hours) | Administration Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-officer-dc55f46b-8083-476b-9b89-86e66dc7015f
title: Administration Officer
employer: Joseph Rowntree School
location: York, Yorkshire and the Humber, YO32 4BZ
region: Yorkshire - North
salary: Grade 4, Level 1-4 (£25,948 to £27,188 p.a.) reduced pro rata to £22,280 to £23,345 (calculated on full time hours)
closing_date: 2026-11-08T23:59:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-officer-dc55f46b-8083-476b-9b89-86e66dc7015f
hub_fingerprint: 66215d6dea054a2084a17569ba441f7fdb901e712a223a38e40c660ed64b2b55
---

---
action:
POSS | Teaching Vacancies | Yorkshire - South | Doncaster, DN9 1HQ | £31,000.00 - £40,000.00 Annually (FTE) | Governance Professional
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: governance-professional-isle-education-trust
title: Governance Professional
employer: Isle Education Trust
location: Doncaster, DN9 1HQ
region: Yorkshire - South
salary: £31,000.00 - £40,000.00 Annually (FTE)
closing_date: 2026-11-12T09:00:00+00:00
reason: Borderline school administration title: governance professional
source_url: https://teaching-vacancies.service.gov.uk/jobs/governance-professional-isle-education-trust
hub_fingerprint: 16f34e5b2225e2ede4143d6720a2260bbdec00d60e1f18b5b53f9df9becb7a61
---

---
action:
POSS | Teaching Vacancies | Yorkshire - South | Rotherham, Yorkshire and the Humber, S60 5EJ | £26,427 to £26,847 | SEND Admin Support Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-admin-support-assistant
title: SEND Admin Support Assistant
employer: Brinsworth Academy
location: Rotherham, Yorkshire and the Humber, S60 5EJ
region: Yorkshire - South
salary: £26,427 to £26,847
closing_date: 2026-11-02T09:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-admin-support-assistant
hub_fingerprint: 524666e77a3d8f05b7a2073604539f962bf1105c7f8f2ff5c28b81bce3f594c2
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Elland, HX5 0RY | £32,578.00 - £34,811.00 Annually (Actual) | HR Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-officer-great-heights-academy-trust
title: HR Officer
employer: Great Heights Academy Trust
location: Elland, HX5 0RY
region: Yorkshire - West
salary: £32,578.00 - £34,811.00 Annually (Actual)
closing_date: 2026-11-09T09:00:00+00:00
reason: Administrative duties evidenced in description
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-officer-great-heights-academy-trust
hub_fingerprint: 01a04c84fff204f8c5affce01a6ca7a5541c4b7c7fe4cc3176b6e60f3f98c4ea
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Elland, HX5 0RY | £32,578.00 - £34,811.00 Annually (Actual) | Operations Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: operations-officer-great-heights-academy-trust
title: Operations Officer
employer: Great Heights Academy Trust
location: Elland, HX5 0RY
region: Yorkshire - West
salary: £32,578.00 - £34,811.00 Annually (Actual)
closing_date: 2026-11-02T12:00:00+00:00
reason: Borderline school administration title: operations officer
source_url: https://teaching-vacancies.service.gov.uk/jobs/operations-officer-great-heights-academy-trust
hub_fingerprint: 1d0a7cb63fdb62935c33aa85a37883caed5c0b9d46a635059d48403d7f44187e
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
