# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs, VONNE, Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-10-26
generated_at: 2026-10-26T08:17:00+00:00

**103 job(s) await a human decision; 1 already answered (104 review rows).**

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
| JobG8 | OK | 2026-10-26 | 104 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | STALE | 2026-10-25 | 0 | — |
| Teaching Vacancies | STALE | 2026-10-25 | 0 | — |
| NHS Jobs | OK | 2026-10-26 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 104 to review

---
action: select
POSS | JobG8 | Berkshire | Berkshire | — | Finance Administration Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2048189
title: Finance Administration Assistant
employer: 
location: Berkshire
region: Berkshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administration assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 27006172761d3df2d593dbb9bb83b212ff81ec656e212c6e84f769bdc6351048
---

---
action: select
POSS | JobG8 | Berkshire | Berkshire | — | Part-Time Finance Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2152925
title: Part-Time Finance Administrator
employer: 
location: Berkshire
region: Berkshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 293667a53a98b4921f87d049ebc51b5e2dc66ce1ba311edcc44c74eba43a896c
---

---
action: select
POSS | JobG8 | Bristol & Bath | Bath | — | Part Time Accounts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2053456
title: Part Time Accounts Administrator
employer: 
location: Bath
region: Bristol & Bath
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Accounts administration is transferable unless specialist accounting barriers are mandatory; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: e64d80cc39ae9ee7ccfe56445bb9f7666ba96e441ae1a6dc0798a395bd2855cd
---

---
action: select
POSS | JobG8 | Bristol & Bath | Bath | — | Part Time Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2088889
title: Part Time Accounts Assistant
employer: 
location: Bath
region: Bristol & Bath
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: accounts assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: f5a63e888a6bdde321bd40af1a83b987bc76bdcf8efeef9d1b17f5276081dc03
---

---
action: select
POSS | JobG8 | Bristol & Bath | Bath | — | Part time Finance Assistant - 22. 5 hours per week
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2070922
title: Part time Finance Assistant - 22. 5 hours per week
employer: 
location: Bath
region: Bristol & Bath
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: finance assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: b8dea17c0c6eccafcc63ca97a544e00397bd456129184291d9637e4b9b6bf207
---

---
action: select
POSS | JobG8 | Bristol & Bath | Bath | — | Payroll Manager (Part Time)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2042147
title: Payroll Manager (Part Time)
employer: 
location: Bath
region: Bristol & Bath
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: f56db2ce6d7623bd8461be9e7e460add879b7b4c4993776d98ce9273a2b996bd
---

---
action: select
POSS | JobG8 | Bristol & Bath | Bath | £39000 - £47000 per year | Payroll Manager (Part Time)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225660760
title: Payroll Manager (Part Time)
employer: 
location: Bath
region: Bristol & Bath
salary: £39000 - £47000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: df31c64f3f6a505b2edf715990ccf949179f2936b00367e35ea358fbf353425f
---

---
action: select
POSS | JobG8 | Bristol & Bath | Bristol | £45000 per year | Salesforce & Sales Pipeline Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108225065
title: Salesforce & Sales Pipeline Coordinator
employer: 
location: Bristol
region: Bristol & Bath
salary: £45000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £45,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: bc8847ef435924804eb0aceaa8ea30737cd198152eb50281b2391b073c27b6fb
---

---
action: select
POSS | JobG8 | Cambridgeshire | Peterborough | £40000 per year | HR MANAGER - PART-TIME
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225692804
title: HR MANAGER - PART-TIME
employer: 
location: Peterborough
region: Cambridgeshire
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 0d6e234d076e325d74bd4e495db57cd374d63b9f29436831494de9425772271a
---

---
action: select
POSS | JobG8 | Cheshire - East | Wilmslow | — | Part-Time Payroll Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2039760
title: Part-Time Payroll Assistant
employer: 
location: Wilmslow
region: Cheshire - East
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: payroll assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: d2dc81411db5fb912afc59530c76d12181ea5f821ec74b497bb39fa4cb440869
---

---
action: select
POSS | JobG8 | Cheshire - West | Northwich | — | Part Time Payroll Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2052993
title: Part Time Payroll Assistant
employer: 
location: Northwich
region: Cheshire - West
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: payroll assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: f73c5467588aa2e1aeeab20d399fb30957d4ab03c85ee9f1e84b2d74cdc0c192
---

---
action: select
POSS | JobG8 | Cornwall | Bodmin | — | Part time Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2062617
title: Part time Payroll Manager
employer: 
location: Bodmin
region: Cornwall
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 32d6f180f5f5e510da63af187c9ed1193dc9e31eef8a35463dede9d8f5611270
---

---
action: select
POSS | JobG8 | Cornwall | Redruth | — | Part Time Bookkeeper
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2057224
title: Part Time Bookkeeper
employer: 
location: Redruth
region: Cornwall
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: bookkeeper; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 227e67349cb45c18c526b75104c9498009016f9d2c4ef0c1c14366d63b3edbda
---

---
action: select
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | £42000 - £45000 per year (Progression + Benefits) | HR / Office Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225719729
title: HR / Office Manager
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: £42000 - £45000 per year (Progression + Benefits)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 64ec8ca2ed0c54bfc357f9d535213a7787056c4341a8a2861ba5c179613cb7c5
---

---
action: select
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | — | HR Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2166644
title: HR Manager
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: b3b968a6228be0563b6b4bc6eac4edd845307a7a85f1cfa552fc04bb45df325a
---

---
action: select
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | £42000 - £45000 per year (Progression + Benefits) | HR Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225726635
title: HR Manager
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: £42000 - £45000 per year (Progression + Benefits)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: d2b026a20ae73c9b553f4cd4c161af9e6dbf4558feef57e1bd59efd419db99bc
---

---
action: select
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | £43,149 per annum | Human Resources and Organisational Development Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2174236
title: Human Resources and Organisational Development Manager
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: £43,149 per annum
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 740815e27eaf4230d70a887d52bebe6b93d9e1aa3fb125ab1844c8375500a2e8
---

---
action: select
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | £43,149 per annum | Office and Facilities Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2174237
title: Office and Facilities Manager
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: £43,149 per annum
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 38ae2d7aecf1a64087c476072d7eb2eb9b33a3633a85ea943562c21c25965e24
---

---
action: select
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | £42000 - £45000 per year (Progression + Benefits) | Office Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225726636
title: Office Manager
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: £42000 - £45000 per year (Progression + Benefits)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: a723d8745cc74a09d20692408116bd870a7b79e7b3099bc532bce40c48ac2a0a
---

---
action: select
POSS | JobG8 | Hampshire | Hampshire | — | Finance Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2057669
title: Finance Administrator
employer: 
location: Hampshire
region: Hampshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: c5b2f5651c01d6d4be80da78dea5af150e36b0aaf31c88fbe2f9e51f461d3dbf
---

---
action: select
POSS | JobG8 | Hampshire | Hampshire | £30000 - £35000 per year | Part Time HR Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225725644
title: Part Time HR Manager
employer: 
location: Hampshire
region: Hampshire
salary: £30000 - £35000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 93227d5b0f45dfeeff32a7a24290b101bf77770d3d6ec08671e55102475c4b23
---

---
action: select
POSS | JobG8 | Herefordshire | Ross-on-wye | — | Accounts Assistant - Hybrid Working
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2039485
title: Accounts Assistant - Hybrid Working
employer: 
location: Ross-on-wye
region: Herefordshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: accounts assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: b34c10e49285cf69daa3d16bdd7f881ff13561931c02e8f83af4b6b4f6062ab6
---

---
action: select
POSS | JobG8 | Hertfordshire | Hertfordshire | — | Bookkeeper / Administrator Part Time
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2172257
title: Bookkeeper / Administrator Part Time
employer: 
location: Hertfordshire
region: Hertfordshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator, bookkeeper; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: b3aae474b33fd7e4bf2b32b3ef906fbe5526b33091f00df5fccc056c2d76b845
---

---
action: select
POSS | JobG8 | Hertfordshire | Hertfordshire | £35000 - £40000 per year | Commercial Property Legal Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2175492
title: Commercial Property Legal Assistant
employer: 
location: Hertfordshire
region: Hertfordshire
salary: £35000 - £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: legal assistant; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: cf6ab7cda57745d39b9580af98290e07e72387f3682b2dcb7f7b2282edf88ed2
---

---
action: select
POSS | JobG8 | Hertfordshire | Hertfordshire | — | Finance Assistant - Part time
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2060294
title: Finance Assistant - Part time
employer: 
location: Hertfordshire
region: Hertfordshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: finance assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: ee74192c938fd3b848bc53395dbd0a187b28349afe01eba7b4b6f6d7c7aca96f
---

---
action: select
POSS | JobG8 | Hertfordshire | Hertfordshire | — | Part Time Accounts Payable Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2055885
title: Part Time Accounts Payable Administrator
employer: 
location: Hertfordshire
region: Hertfordshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 44e84b6b9412765d9e1823f8945d3615181c65e318d8e7ab688fbc881a97ddc6
---

---
action: select
POSS | JobG8 | Hertfordshire | Hertfordshire | — | Part-time Accounts Receivable Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2051739
title: Part-time Accounts Receivable Administrator
employer: 
location: Hertfordshire
region: Hertfordshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: ec49d7a7c9c66d69102ac877caea92479d0b2643dfd6a12398559c5bf2b179d9
---

---
action: select
POSS | JobG8 | Kent | Dartford | £40000 - £45000 per year | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225726540
title: Payroll Manager
employer: 
location: Dartford
region: Kent
salary: £40000 - £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: 844253b7e86065b2ed362d8208cf3b2c6ae479301776ef933f8d365972947bf3
---

---
action: select
POSS | JobG8 | Kent | Kent | — | Accounts and Office Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2157148
title: Accounts and Office Administrator
employer: 
location: Kent
region: Kent
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator, office administrator; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: dfeec5b375589d930f82c904952e29533b89f89934c46bcf8bd2abc3a06d998a
---

---
action: select
POSS | JobG8 | Leicestershire | Leicestershire | — | Finance Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225706585
title: Finance Assistant
employer: 
location: Leicestershire
region: Leicestershire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - owner-approved ordinary office role; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 71146c496e83d5b39a6f3e1636671c2d91d04286909c00eca8db369d2cfbd49d
---

---
action: select
POSS | JobG8 | Lincolnshire | Lincolnshire | — | Payroll Technician
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2068930
title: Payroll Technician
employer: 
location: Lincolnshire
region: Lincolnshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: bc5b41111d54a636bae551819490395b10cfc52337bd4a3b630d8e1540eefe73
---

---
action: select
POSS | JobG8 | London | Borehamwood | £17 - £20 per hour | Care Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225762327
title: Care Support Worker
employer: 
location: Borehamwood
region: London
salary: £17 - £20 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 0a9ac6359678205baab817b5232b4c3526364f532f17aa76a3c02de2257a705b
---

---
action: select
POSS | JobG8 | London | Brixton | £16 - £18 per hour | Part Time Office Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225674119
title: Part Time Office Manager
employer: 
location: Brixton
region: London
salary: £16 - £18 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: a3cc199c15ffad3edae5d60874c30f08b170ce6ffd573ec051e3f693eb1205c6
---

---
action: select
POSS | JobG8 | London | London | £35000 - £41000 per year | Billings Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2063583
title: Billings Administrator
employer: 
location: London
region: London
salary: £35000 - £41000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: 7a886a7ab2d25c205d00bfbad2032276dc1feb3496a0890198297d5d815f4068
---

---
action: select
POSS | JobG8 | London | London | — | Bookkeeping & AI Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2062388
title: Bookkeeping & AI Manager
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 6dc70399039e6a9cfd42cdc4975ff72d547178f79fcf65a9a61bdd239e76057a
---

---
action: select
POSS | JobG8 | London | London | — | Finance and Operations Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2087368
title: Finance and Operations Assistant
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: c08bec6e3c0e054f14a4d1ee07ccd91118707c0c19f5341406848448f8e3659a
---

---
action: select
POSS | JobG8 | London | London | — | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2053404
title: Finance Manager
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: f045a5d4956b2771a672ccaf73ba4829d4c753a98570ffe0d671802ae103dd4b
---

---
action: select
POSS | JobG8 | London | London | — | Finance Manager (part-time)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2092583
title: Finance Manager (part-time)
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 01b28acf7dc2d1d6596a5aff16cdf2f627673ae6a84dcd0bb4214ea3e35149a7
---

---
action: select
POSS | JobG8 | London | London | £21.35 per hour | Housing Team Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225698771
title: Housing Team Administrator
employer: 
location: London
region: London
salary: £21.35 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: a16aa9794b94366bd62a6072319b148f96f677a99c644f74c903fb06611d5b4d
---

---
action: select
POSS | JobG8 | London | London | £50000 per year | HR Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225694962
title: HR Manager
employer: 
location: London
region: London
salary: £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 7ed0ad6d8e2515fb1658b4b0ae980d56a2be374c92271c9ee73c759b1ebbb80e
---

---
action: select
POSS | JobG8 | London | London | — | Part Time Property & Finance Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2078541
title: Part Time Property & Finance Officer
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 08684dd28fbaf4065ca5c0d1c6431aa37aa2d4c0341a2bffd2b22c7f88347c53
---

---
action: select
POSS | JobG8 | London | London | £36000 - £42000 per year (Plus bonus and benefits) | Payouts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225698168
title: Payouts Administrator
employer: 
location: London
region: London
salary: £36000 - £42000 per year (Plus bonus and benefits)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: eac9bc5e8ab215e3ae8ea549f1d7cffdce5bbcfef2714f630d53f2453684b6bb
---

---
action: select
POSS | JobG8 | London | London | £31,936 - £35,027 per annum | Service Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108062183
title: Service Manager
employer: 
location: London
region: London
salary: £31,936 - £35,027 per annum
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 9ecaa09b6ab6fc2309a9acb9be9dce90d14cbdc368ce76f0983007d2c619961a
---

---
action: select
POSS | JobG8 | London | London | £44367 per year | Spurgeons - Finance Business Partner
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225705616
title: Spurgeons - Finance Business Partner
employer: 
location: London
region: London
salary: £44367 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: bc3c650a4ff1fc3a1b49c8a6f3f6acd7fdd41d47296e8044c109315fbbb3571f
---

---
action: select
POSS | JobG8 | London | Morden | — | Office Manager & Compliance Coordinator PART TIME
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225708270
title: Office Manager & Compliance Coordinator PART TIME
employer: 
location: Morden
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 9a02679c9228abea86c835dc8b83b70239da64322d0b2644892f832efd88d1a5
---

---
action: select
POSS | JobG8 | Merseyside - Liverpool | Liverpool | — | Financial Services Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225734026
title: Financial Services Administrator
employer: 
location: Liverpool
region: Merseyside - Liverpool
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - title register: high-confidence title pattern: administrator; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 7dba52d676740d412dee8cf132b9746941caf10e8b053e3b740340d19e37a8ef
---

---
action: select
POSS | JobG8 | Merseyside - Liverpool | Liverpool | — | HR Manager - Temporary to Permanent
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225698676
title: HR Manager - Temporary to Permanent
employer: 
location: Liverpool
region: Merseyside - Liverpool
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 4a93eecc5c8fa77d228d2a7db8f289f3b6247f73f2aa9aa4482d831ff2bbec37
---

---
action: select
POSS | JobG8 | Merseyside - St Helens & Knowsley | Knowsley | — | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2050536
title: Accounts Assistant
employer: 
location: Knowsley
region: Merseyside - St Helens & Knowsley
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: accounts assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 0ef19b2019c2dc598d5bbef04e5eee5628a8b2a1bbc0b09496795a82292b8fe4
---

---
action: select
POSS | JobG8 | Norfolk | Norfolk | — | Accounts Office Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2126041
title: Accounts Office Administrator
employer: 
location: Norfolk
region: Norfolk
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator, office administrator; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: a10263602cb095c36624b8b0431154f8df4f2622f1b7ed191bbf8cea8679e457
---

---
action: select
POSS | JobG8 | Norfolk | Norfolk | — | Accounts Office Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225722938
title: Accounts Office Administrator
employer: 
location: Norfolk
region: Norfolk
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator, office administrator; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 12e4ea1fc4e844f448a765ec9f6f82c8499ab7b01b0cf596e6104a5993106cc5
---

---
action: select
POSS | JobG8 | Norfolk | Norfolk | — | Finance Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2087990
title: Finance Assistant
employer: 
location: Norfolk
region: Norfolk
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - owner-approved ordinary office role; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 72c1d30ca09ae6df94e0c05447ba799dfe1094e85d5841670f49e63e03762db2
---

---
action: select
POSS | JobG8 | North East - County Durham & Darlington/Hartlepool | County Durham | £30000 - £45000 per year | Commercial Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225646128
title: Commercial Administrator
employer: 
location: County Durham
region: North East - County Durham & Darlington/Hartlepool
salary: £30000 - £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - title register: high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: a401fb2c409f09540bc2a16e557ccf83525a25a28708599519a0fcb38b0f439d
---

---
action: select
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Tyne And Wear | — | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2077376
title: Accounts Assistant
employer: 
location: Tyne And Wear
region: North East - Tyneside, Wearside & Northumberland
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: accounts assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: b036dae1f0c55aeb1f4a7a6c1fda34ea08aaf6741549c55cad9f52333b3d37f7
---

---
action: select
POSS | JobG8 | North Scotland | Fraserburgh | £40000 per year | Service Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 107991122
title: Service Manager
employer: 
location: Fraserburgh
region: North Scotland
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: e471e62b6d35b44978c7277ab63ccb82e99390c5edab0f3ec49350ee579c997b
---

---
action: select
POSS | JobG8 | North Wales - East | Wrexham | — | Credit Control
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2076239
title: Credit Control
employer: 
location: Wrexham
region: North Wales - East
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: d3745d2763d244c4241930a12b8f632765dcfa6753850dcf8d07b8d92596026c
---

---
action: select
POSS | JobG8 | Northamptonshire | Northamptonshire | — | Part-Time Finance Officer (with Administrative Support)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2129537
title: Part-Time Finance Officer (with Administrative Support)
employer: 
location: Northamptonshire
region: Northamptonshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 56385a4f6837912e09cf8a336f97c5aa275b280980bd187161e457c985bba1a7
---

---
action: select
POSS | JobG8 | Northern Ireland - East | Belfast | £20.1 - £24.21 per hour (£20.10- £24.41) | Band 6 - Finance Business Partner
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225666942
title: Band 6 - Finance Business Partner
employer: 
location: Belfast
region: Northern Ireland - East
salary: £20.1 - £24.21 per hour (£20.10- £24.41)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: 15f90239e664807a8ec73d9717f2d77d8b5496e92785de54d5c1e5f5e8718ebd
---

---
action: select
POSS | JobG8 | Nottinghamshire | Nottinghamshire | — | Finance Officer: Purchase Ledger & Income
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2174181
title: Finance Officer: Purchase Ledger & Income
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 32df142719224597c5fdc2b1e30c1b1c3cfe02b24b875f94c3154af2b73548c7
---

---
action: select
POSS | JobG8 | Nottinghamshire | Nottinghamshire | — | Group Financial Controller
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2056429
title: Group Financial Controller
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: d065081564330a4dd754d6030458a067642400067a6400daa3ed17d2752298a7
---

---
action: select
POSS | JobG8 | Nottinghamshire | Nottinghamshire | £10000 per year (/month) | Part Time HR Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225746065
title: Part Time HR Manager
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: £10000 per year (/month)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 2969897db114c03ce3d4b3fc127e49884ba59ded62b868ca9853a4e732be3a5a
---

---
action: select
POSS | JobG8 | Oxfordshire | Oxfordshire | £37,751.95 - £40,655.94 per annum | HR and Payroll Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2174234
title: HR and Payroll Officer
employer: 
location: Oxfordshire
region: Oxfordshire
salary: £37,751.95 - £40,655.94 per annum
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: 9f39410f475f06bde47036968b1a6393f4f4305f861c52315b42d49e90856fd3
---

---
action: select
POSS | JobG8 | Oxfordshire | Oxfordshire | £23.07 per hour | Temporary Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225727890
title: Temporary Finance Manager
employer: 
location: Oxfordshire
region: Oxfordshire
salary: £23.07 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: 67dcff2a77a2b3615b74dc99ae9a6887b05174f21dabd49d873e853a5c275815
---

---
action: select
POSS | JobG8 | Scotland Central - Edinburgh & Lothians | Edinburgh | £35000 per year | Office Manager/Administrator- Edinburgh - 4 day week
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2137033
title: Office Manager/Administrator- Edinburgh - 4 day week
employer: 
location: Edinburgh
region: Scotland Central - Edinburgh & Lothians
salary: £35000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 7a533e4dd28f8f111276f23997ae1b72db44b45b73aa1504b341e722cd22e08e
---

---
action: select
POSS | JobG8 | Scotland Central - Falkirk & Stirling | Stirling | £47000 - £51000 per year | Finance Business Partner
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2074273
title: Finance Business Partner
employer: 
location: Stirling
region: Scotland Central - Falkirk & Stirling
salary: £47000 - £51000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: a26df74582b27d4faead48cd2a599defa85030f63d8ca30811fb9bca9c4a7aa7
---

---
action: select
POSS | JobG8 | Scotland Central - Falkirk & Stirling | Stirling | — | Payroll Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2057368
title: Payroll Coordinator
employer: 
location: Stirling
region: Scotland Central - Falkirk & Stirling
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: payroll coordinator; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 514d5257d67f97dbb5fd7cc82c9495c3dea3de1ad5a5f054532d5e43b9734ed9
---

---
action: select
POSS | JobG8 | Scotland West - Glasgow | Glasgow | — | Accounts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2055742
title: Accounts Administrator
employer: 
location: Glasgow
region: Scotland West - Glasgow
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Basic accounts administration is transferable unless specialist qualifications are mandatory; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: cb12ffda8f255c8bffd27a0e77fbd7f161d130b68db35049618d02d3b298595d
---

---
action: select
POSS | JobG8 | Shropshire | Shropshire | — | Payroll Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2092604
title: Payroll Assistant
employer: 
location: Shropshire
region: Shropshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: payroll assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 9e5c9ae7dfa309939578e1017d0626d38afbf0cbf9d67e6e96d35048a45b5742
---

---
action: select
POSS | JobG8 | Somerset | Somerset | £35000 - £48000 per year | Accounts and Office Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2038056
title: Accounts and Office Manager
employer: 
location: Somerset
region: Somerset
salary: £35000 - £48000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: 126a0e8ede7f2849f993a052c66edbd91d4ad2b6ebc48f44610b39726ab1a1ce
---

---
action: select
POSS | JobG8 | Somerset | Somerset | £30000 - £40000 per year | Accounts Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225367093
title: Accounts Manager
employer: 
location: Somerset
region: Somerset
salary: £30000 - £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: 2bbafca1f9682ed67b6c0d853e7b13069d1e04b12ff8518d2849fe678fa1fedb
---

---
action: select
POSS | JobG8 | Somerset | Somerset | — | P/T ACCOUNTS ADMINISTRATOR / BOOKKEEPER
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225667966
title: P/T ACCOUNTS ADMINISTRATOR / BOOKKEEPER
employer: 
location: Somerset
region: Somerset
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator, bookkeeper; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: a2cd686e90234662521a774dbc23d0fe5b200c83e370895dddbe2a5b1aedbe83
---

---
action: select
POSS | JobG8 | Somerset | Somerset | — | P/T Accounts Administrator/Bookkeeper
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2055734
title: P/T Accounts Administrator/Bookkeeper
employer: 
location: Somerset
region: Somerset
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator, bookkeeper; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 80b978ef6e50cb479b1b295c0316bf0df5eeb240cc2a9dbea38b31fc372b4a3d
---

---
action: select
POSS | JobG8 | Somerset | Somerset | — | Payroll Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2044538
title: Payroll Administrator
employer: 
location: Somerset
region: Somerset
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator, payroll administrator; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 9db535b8f1b3a838d5bc3300f54da8db449a296a1c5e7e61f984ce7b755090ae
---

---
action: select
POSS | JobG8 | Somerset | Somerset | — | Senior Accounts Technician
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2088068
title: Senior Accounts Technician
employer: 
location: Somerset
region: Somerset
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 4cf721096e550b66c604be11d1e27a85a695de969741a6d1f10c681adb8e9dbf
---

---
action: select
POSS | JobG8 | Staffordshire | Staffordshire | £15080 per year (£14.50 per hour) | Part-time Accounts Office Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225690802
title: Part-time Accounts Office Manager
employer: 
location: Staffordshire
region: Staffordshire
salary: £15080 per year (£14.50 per hour)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: e2937961323f2794ca4c1b595e6459d86579aa83a3a320e0f0d265d661c8600e
---

---
action: select
POSS | JobG8 | Staffordshire | Staffordshire | — | Payroll and Benefits Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2104362
title: Payroll and Benefits Officer
employer: 
location: Staffordshire
region: Staffordshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 1ca910065b6ed0d683d8ca2f71bba788c640f5e3fd3d8adbf04641c83f55beb1
---

---
action: select
POSS | JobG8 | Surrey | Surrey | — | Bookkeeper
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2044193
title: Bookkeeper
employer: 
location: Surrey
region: Surrey
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: bookkeeper; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 86c51b7e3f21f4507330f6413f63e29f67b1b8de303191f18ba255c453f66b88
---

---
action: select
POSS | JobG8 | Surrey | Surrey | £38875 - £42161 per year | HR Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225688512
title: HR Manager
employer: 
location: Surrey
region: Surrey
salary: £38875 - £42161 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 3ab90b38c3d8a32333acba528c5a58bc1da4ec682b2f171f16ab4546fc50234e
---

---
action: select
POSS | JobG8 | Surrey | Surrey | — | Part Time Finance Manager 4 days per week 32 hours
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2087513
title: Part Time Finance Manager 4 days per week 32 hours
employer: 
location: Surrey
region: Surrey
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 4bec413181d0479dcf0b9ad24ff1533b1ef6821f2c0d92aa99cfd57034d090cd
---

---
action: select
POSS | JobG8 | Surrey | Surrey | — | Payroll Assistant - Part time
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2089890
title: Payroll Assistant - Part time
employer: 
location: Surrey
region: Surrey
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: payroll assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 40a3e3730e685cac3b89e73eb0dd2e6911a7550989902f1bda119dbf2d636664
---

---
action: select
POSS | JobG8 | Sussex | Sussex | — | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2037053
title: Accounts Assistant
employer: 
location: Sussex
region: Sussex
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: accounts assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 3695daa159b19caee89c0317b3a4313207c0bc2ddc4dadbc610d5d0512e7bbd7
---

---
action: select
POSS | JobG8 | Sussex | Sussex | — | Accounts Payable
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2074351
title: Accounts Payable
employer: 
location: Sussex
region: Sussex
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: d8f087d83702ed8cee8f392340c3d74667943d2872fe5a357fa2ef071e8bab41
---

---
action: select
POSS | JobG8 | Wales South - Cardiff & Vale | Cardiff | — | Financial Controller
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2057279
title: Financial Controller
employer: 
location: Cardiff
region: Wales South - Cardiff & Vale
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 97a9e3ac320b14ff447a1ffe6dbba930c412649fd3dd99586f9888a0b083d401
---

---
action: select
POSS | JobG8 | Wales South - Valleys | Pontypridd | — | Hr Manager Part-Time
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108220656
title: Hr Manager Part-Time
employer: 
location: Pontypridd
region: Wales South - Valleys
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 951dc33152140e0a88d586e6d21138d3d8eab0ccc9e8a46abfada12b548474c3
---

---
action: select
POSS | JobG8 | West Midlands - Birmingham & Solihull | Birmingham | £32000 - £35000 per year | Office Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225694384
title: Office Manager
employer: 
location: Birmingham
region: West Midlands - Birmingham & Solihull
salary: £32000 - £35000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: c1dee148413f41d93a796643a2050e835ac9637be79b19ebd793c956f699e840
---

---
action: select
POSS | JobG8 | West Midlands - Birmingham & Solihull | Sutton Coldfield | — | Experienced Bookkeeper / Accounts Professional
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225690795
title: Experienced Bookkeeper / Accounts Professional
employer: 
location: Sutton Coldfield
region: West Midlands - Birmingham & Solihull
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: bookkeeper; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 5bb63063e3f6e0a2ebccb03473efd0e4489b5b9eb2849940189249e7d9a4ebc9
---

---
action: select
POSS | JobG8 | West Midlands - Birmingham & Solihull | Sutton Coldfield | — | Part-time Payroll Clerk
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2055533
title: Part-time Payroll Clerk
employer: 
location: Sutton Coldfield
region: West Midlands - Birmingham & Solihull
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: payroll clerk; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 7096aada721a9b3fdb75f9b938014d16f74adc30504ababe72a4c69934670d31
---

---
action: select
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | £40,000 - £42,000 per annum | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2138590
title: Finance Manager
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: £40,000 - £42,000 per annum
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 1d61bcdd77d77a54b4367cf9fe012773988f9d99841d8d91e2601e32267a6705
---

---
action: select
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | — | Part Time Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2079095
title: Part Time Finance Manager
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: f421e13a90240a3fbc7a29c7bf5ee1a0b7aa015e2d280e392ede4225096c23da
---

---
action: select
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | £36000 - £42000 per year (Hybrid working, Generous A/L etc) | Part Time Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225689484
title: Part Time Finance Manager
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: £36000 - £42000 per year (Hybrid working, Generous A/L etc)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: ede7b557d0fc51e5ddb7865832bd52b1f9b8f90b2ba4dec84caaa055b9994c56
---

---
action: select
POSS | JobG8 | Wiltshire | Wiltshire | — | Part-time Finance Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2041620
title: Part-time Finance Officer
employer: 
location: Wiltshire
region: Wiltshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 321f70b820114863ea9172789aa81e5676be9192394dbdc9c6971732e3c53829
---

---
action: select
POSS | JobG8 | Yorkshire - East | Goole | £38000 - £42000 per year | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225629342
title: Payroll Manager
employer: 
location: Goole
region: Yorkshire - East
salary: £38000 - £42000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: c10270716140ce6e9f8d2ee1ec057241a1f800de44bd986542bb0b1f65d04de3
---

---
action: select
POSS | JobG8 | Yorkshire - East | Goole | — | Payroll Processor
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225702204
title: Payroll Processor
employer: 
location: Goole
region: Yorkshire - East
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 64da4d75f546ee63db9ffeda2fcd8b22bf2f4efedc5e96c93b607ef7265b4486
---

---
action: select
POSS | JobG8 | Yorkshire - East | Hessle | — | Finance & Reporting Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2165745
title: Finance & Reporting Administrator
employer: 
location: Hessle
region: Yorkshire - East
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 4c8c308a0a16cb325ce8a550c2697b92c5a508209e66767c370053fdbd9777e7
---

---
action: select
POSS | JobG8 | Yorkshire - East | Hull | — | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2060366
title: Accounts Assistant
employer: 
location: Hull
region: Yorkshire - East
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: accounts assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: c1063b7b5a7e6d210ec12bb167b457ca669e7f11c6ce67b3697809c4495380c5
---

---
action: select
POSS | JobG8 | Yorkshire - East | Hull | — | Finance Procurement Administrator ( Part-Time)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225754589
title: Finance Procurement Administrator ( Part-Time)
employer: 
location: Hull
region: Yorkshire - East
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 37a0bfb3bf399fa0ee851c4e9524d75fd2ff5e052a453af92ffd3035eab06be4
---

---
action: select
POSS | JobG8 | Yorkshire - North | York | — | Part Time Finance Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2087398
title: Part Time Finance Assistant
employer: 
location: York
region: Yorkshire - North
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: finance assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: d9197084fcec42e4ab05a550f646d0af18b94ee42f48df15f4c4acc2eb13f6bf
---

---
action: select
POSS | JobG8 | Yorkshire - North | York | — | Part Time Finance Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225696188
title: Part Time Finance Assistant
employer: 
location: York
region: Yorkshire - North
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: finance assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 7fa6b9340b43ed12093061f5ca93929c13eab21f764d0342550c054415996637
---

---
action: select
POSS | JobG8 | Yorkshire - South | Brinsworth | £40000 - £45000 per year | Hr Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225733777
title: Hr Manager
employer: 
location: Brinsworth
region: Yorkshire - South
salary: £40000 - £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: aaffde3809e6328533f5b93085e33f54ba1767004f0786de17e1c516dd338d0d
---

---
action: select
POSS | JobG8 | Yorkshire - South | Sheffield | — | Income Assistant / Finance Administrator - Local Authority
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2067582
title: Income Assistant / Finance Administrator - Local Authority
employer: 
location: Sheffield
region: Yorkshire - South
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 76ba72b8fa2b29778cb8d492ef4a6fcf1a1c044fb13c82a962e84d1b1e54985a
---

---
action: select
POSS | JobG8 | Yorkshire - South | Sheffield | — | Part time Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2052120
title: Part time Finance Manager
employer: 
location: Sheffield
region: Yorkshire - South
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 2b4c841b705a3705917f12c9993374663f16c23094364cf1423a4add26604351
---

---
action: select
POSS | JobG8 | Yorkshire - West | Leeds | — | Payroll Specialist (Stand alone)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2075044
title: Payroll Specialist (Stand alone)
employer: 
location: Leeds
region: Yorkshire - West
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 8e64b0c5a5f7449e7ffe08f53b1f954625bc22f199629204f3da99430cd79e5f
---

---
action: select
POSS | JobG8 | Yorkshire - West | Wakefield | — | Credit Control
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2164237
title: Credit Control
employer: 
location: Wakefield
region: Yorkshire - West
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 26ce0493a7c159cb4a7a35952ebf4caf8a31b895b85c32f5f5fbcc05e560d006
---

---
action: select
POSS | JobG8 | Yorkshire - West | Wakefield | — | Part- Time Accounts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2064618
title: Part- Time Accounts Administrator
employer: 
location: Wakefield
region: Yorkshire - West
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: e3e2904181dc1d44286b84d0a4e02ccc956941a19e343998e90b5dec0d1f7af2
---

---
action: select
POSS | JobG8 | Yorkshire - West | Wakefield | — | Purchase Ledger Clerk
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2165855
title: Purchase Ledger Clerk
employer: 
location: Wakefield
region: Yorkshire - West
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: a8683e00852362799264209064859afe50763b20d138227e330c6f3cf9137d08
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
