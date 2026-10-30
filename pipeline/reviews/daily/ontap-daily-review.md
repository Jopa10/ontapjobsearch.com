# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-10-30
generated_at: 2026-10-30T17:47:59+00:00

**149 job(s) await a human decision; 0 already answered (149 review rows).**

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
| JobG8 | OK | 2026-10-30 | 70 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | OK | 2026-10-30 | 1 | — |
| Teaching Vacancies | OK | 2026-10-30 | 78 | — |
| NHS Jobs | OK | 2026-10-30 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 70 to review

---
action:
POSS | JobG8 | Berkshire | Berkshire | £38221 - £45092 per year | Finance Operations Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2082495
title: Finance Operations Coordinator
employer: 
location: Berkshire
region: Berkshire
salary: £38221 - £45092 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £45,092 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 8989f8fe60f731c3234e2f44a636de8773db04a594e6bd9b308899d9ff5166d5
---

---
action:
POSS | JobG8 | Bristol & Bath | Bristol | £50,000 per year (FTE) | Chief Financial Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2097640
title: Chief Financial Officer
employer: 
location: Bristol
region: Bristol & Bath
salary: £50,000 per year (FTE)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: professional accountancy qualification wording needs review; salary over £40k under normal selection rules
source_url: 
hub_fingerprint: e4cbb649743652e26128df3f630dbe45cacad8d1aa5d2fd43d8e72f6ae6f942c
---

---
action:
POSS | JobG8 | Bristol & Bath | Bristol | — | Corporate Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2094922
title: Corporate Accounts Assistant
employer: 
location: Bristol
region: Bristol & Bath
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: dcce9a99597c73730f45ce99aba0425a3731a3562086899daec931e74493f871
---

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
POSS | JobG8 | Buckinghamshire | Buckinghamshire | £35000 - £38000 per year | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2198563
title: Accounts Assistant
employer: 
location: Buckinghamshire
region: Buckinghamshire
salary: £35000 - £38000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: accounts assistant; manual review required: annualised upper salary £38,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 28d229559217a9bf94676435467c70f56491a81413ca4ddb05d4d9b62f074dcd
---

---
action:
POSS | JobG8 | Buckinghamshire | Buckinghamshire | £35000 per year | Bookkeeper
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2099639
title: Bookkeeper
employer: 
location: Buckinghamshire
region: Buckinghamshire
salary: £35000 per year
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: db4eb5a841a7ff2e166840f2d1c6b132726b8d57373551c45ba97715ec67f8b0
---

---
action:
POSS | JobG8 | Buckinghamshire | Buckinghamshire | £42000 per year | Legal Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2204941
title: Legal Assistant
employer: 
location: Buckinghamshire
region: Buckinghamshire
salary: £42000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: legal assistant; manual review required: annualised upper salary £42,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 7e58e6fd6aaf2deb6b4559611f6cf2313d2904db5299a8ebc675bd03b3b93559
---

---
action:
POSS | JobG8 | Dorset | Dorchester | £36768 per year | Residential Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 108087516
title: Residential Support Worker
employer: 
location: Dorchester
region: Dorset
salary: £36768 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 097ff2293538bc15f48b48039ca07afb1a7cea2e721e29d394555f1a69eeaf47
---

---
action:
POSS | JobG8 | Dorset | Dorset | £40000 - £45000 per year | Document Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2171614
title: Document Administrator
employer: 
location: Dorset
region: Dorset
salary: £40000 - £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: fdf5a8c03648655232b97a826dde2e9c1aac6955971fa3065b58d7d75faade5e
---

---
action:
POSS | JobG8 | Dorset | Dorset | — | Part-Time Finance Manager - Poole - &;45,000 pro-rata
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2178788
title: Part-Time Finance Manager - Poole - &;45,000 pro-rata
employer: 
location: Dorset
region: Dorset
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: dc7b8fd737f88ee5e551f5853fa45bbfac73516e464323d4e9a586202176b82c
---

---
action:
POSS | JobG8 | Dorset | Dorset | £45000 - £50000 per year | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2203629
title: Payroll Manager
employer: 
location: Dorset
region: Dorset
salary: £45000 - £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: ac60cdc089eb24a14d148b5c9fce3633b952a0e2029af77aa70b510cb215d6b4
---

---
action:
POSS | JobG8 | Essex | Essex | — | Part Time Managing Partner - Finance & Strategy
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2187606
title: Part Time Managing Partner - Finance & Strategy
employer: 
location: Essex
region: Essex
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: 8e80e65175267f14032d7d1de5e292f59751fae1e789869951f17835a9d64ed5
---

---
action:
POSS | JobG8 | Essex | Essex | — | Part-Time - Accounts Assistant Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2158375
title: Part-Time - Accounts Assistant Manager
employer: 
location: Essex
region: Essex
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 921bb34d0d83a6bd4667cbe6caade631887ae2c1aaf8b8c0b6d6e092d4c3695c
---

---
action:
POSS | JobG8 | Essex | Essex | — | Part-Time Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2077481
title: Part-Time Finance Manager
employer: 
location: Essex
region: Essex
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 686b8aab7a8c99d4c85fa0cd2382be3008f7e1c6c9dffae9edf5c2cc65e07d44
---

---
action:
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | — | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2074951
title: Accounts Assistant
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: ad40993d1b8d1d7427d81df5d930dade068c88e83b4478214bbdd997fd56a26c
---

---
action:
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | £28000 per year | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2087713
title: Accounts Assistant
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: £28000 per year
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: af5e624fb60e792322c4687fac6ab116ad96513bf487aace461fa4d709bf012c
---

---
action:
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | £40000 per year | Assistant Company Secretary
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2097582
title: Assistant Company Secretary
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: secretary; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 8f6eee44dccb57ddb334831bb6a14162f163b1ad86e6a2020c0f8a10f7b24205
---

---
action:
POSS | JobG8 | Greater Manchester - North | Heywood | £30000 - £32000 per year | Bookkeeper
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2157322
title: Bookkeeper
employer: 
location: Heywood
region: Greater Manchester - North
salary: £30000 - £32000 per year
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: 96d97d09089e903a5407deb1358935237933c14015af88c437ad50cd2bce6c83
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
POSS | JobG8 | Hampshire | Hampshire | — | Finance Analyst
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2191973
title: Finance Analyst
employer: 
location: Hampshire
region: Hampshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 03d342c67f518841f7df7bf9e634e17d071df2967806472ee5af9e1bb01c233f
---

---
action:
POSS | JobG8 | Hampshire | Hampshire | — | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2193434
title: Finance Manager
employer: 
location: Hampshire
region: Hampshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 10484371214d9951a3c87ee7c3bef6b73943d1491c7f924567ffead6cc5be1dd
---

---
action:
POSS | JobG8 | Hampshire | Hampshire | — | Financial Controller
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2096244
title: Financial Controller
employer: 
location: Hampshire
region: Hampshire
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: e13f873f07fd0844af71cd19d988fc7024cca7ec3b9d30803e62ae55f454971b
---

---
action:
POSS | JobG8 | Hampshire | Hampshire | £45000 per year | Software Project Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2152700
title: Software Project Coordinator
employer: 
location: Hampshire
region: Hampshire
salary: £45000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: b108d3a83f272f2c16e9505acd63a72f505cfcf41dc4b30fee352149f07820cb
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
POSS | JobG8 | Hertfordshire | Hertfordshire | £35000 - £40000 per year | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2196083
title: Accounts Assistant
employer: 
location: Hertfordshire
region: Hertfordshire
salary: £35000 - £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: accounts assistant; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 80bfa06b4fc190c0f45d8246f7de6624726e96218932a5475ce9e1095eb0ca52
---

---
action:
POSS | JobG8 | Hertfordshire | Hertfordshire | — | Commercial Financial Analyst
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2192091
title: Commercial Financial Analyst
employer: 
location: Hertfordshire
region: Hertfordshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 33d9c710e755cb0791a9b14a198c63ec7d7fc4bf30e72b27ecdf234609dc326a
---

---
action:
POSS | JobG8 | Kent | Kent | — | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2176864
title: Accounts Assistant
employer: 
location: Kent
region: Kent
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: b7ebaeb8acc8f9fc9d4a83396b504e84c0f7aa10d018e719c7c5ea7fc52ca95f
---

---
action:
POSS | JobG8 | Kent | Kent | £21.00 per hour | Bookkeeper / Accounts Clerk / Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2157508
title: Bookkeeper / Accounts Clerk / Payroll Manager
employer: 
location: Kent
region: Kent
salary: £21.00 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: dddfd108ee185574a1b0445cc063bb5d496847173169748abffc5f7a583a8ae0
---

---
action:
POSS | JobG8 | Kent | Kent | £42,000 - £44,000 per year (FTE) | Part Time Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2098855
title: Part Time Finance Manager
employer: 
location: Kent
region: Kent
salary: £42,000 - £44,000 per year (FTE)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: 40e9b81960daf4d267cbe632eb5740cd9ae4c2105f890e2f1aa3d8708aa66f22
---

---
action:
POSS | JobG8 | Leicestershire | Leicestershire | £30000 per year | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2177260
title: Accounts Assistant
employer: 
location: Leicestershire
region: Leicestershire
salary: £30000 per year
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: e2356bc2231f64bd1c8c5a080e157a2d1ea3f2fb4fceb25abb278ae0448561e7
---

---
action:
POSS | JobG8 | London | Croydon | £41000 - £44485 per year | Service Advisor
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2207009
title: Service Advisor
employer: 
location: Croydon
region: London
salary: £41000 - £44485 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - owner-approved ordinary office role; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: 9a794afdc229efe23fabfe2d86367169a027973d2009090f9ecbb95ec5a032eb
---

---
action:
POSS | JobG8 | London | London | £40000 - £50000 per year | Bookkeeper
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2158143
title: Bookkeeper
employer: 
location: London
region: London
salary: £40000 - £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: bookkeeper; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: 848657ac3a10848afc192c6ea67e67dcb3c2021064f7bb3c46423d6eee200921
---

---
action:
POSS | JobG8 | London | London | — | Bookkeeping Manager - Accountancy Firm
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2101752
title: Bookkeeping Manager - Accountancy Firm
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: a8f857b66c6b222abfbafc00a7f9218fac2c9ebaea3e1341876e3a4fa8e26577
---

---
action:
POSS | JobG8 | London | London | £45000 per year | Finance Manager - Part Time
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2096178
title: Finance Manager - Part Time
employer: 
location: London
region: London
salary: £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: e19f74b4214b694e847fd34a6b80c65fc69a785b111a691c4874dc8b27004efb
---

---
action:
POSS | JobG8 | London | London | — | Finance Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2193191
title: Finance Officer
employer: 
location: London
region: London
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: 662c86741ebc29231196427d2a4f8178ebeceac498f4f31fa2f7a6e1b81f8133
---

---
action:
POSS | JobG8 | London | London | £24 per hour | Finance Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2205832
title: Finance Officer
employer: 
location: London
region: London
salary: £24 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - owner-approved ordinary office role; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: 074c2f17af380ec6d838f90974f25c63fe1908b3a28f189837f646334f61f4c7
---

---
action:
POSS | JobG8 | London | London | £23.80 per hour | Finance Service Centre Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2156666
title: Finance Service Centre Officer
employer: 
location: London
region: London
salary: £23.80 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: 394ba1d2e24b1fa84085c446af5efb82adfad6cb11fcc40d845ebb998439f1a4
---

---
action:
POSS | JobG8 | London | London | — | IBA Accounts Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2097968
title: IBA Accounts Manager
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 08ac539187307d511e3b91a5033b7b7b5aac24d0545e3c332804a82314dbe33c
---

---
action:
POSS | JobG8 | London | London | — | Part-Time Financial Controller (Property)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2197919
title: Part-Time Financial Controller (Property)
employer: 
location: London
region: London
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: 182c1012ba93960ea71ae64ec8681ce5f59bc7cc54aad2a4afa224fe88633418
---

---
action:
POSS | JobG8 | London | London | — | Project Support Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2194716
title: Project Support Officer
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Project plans, records and reporting support; verify specialist requirements and each advert.; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: 269009ea70789038bc3e987324f55dc08a3de4b7c2cc26ffd5c4de85157d015f
---

---
action:
POSS | JobG8 | London | London | £45000 per year | Property Litigation Secretary
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2192442
title: Property Litigation Secretary
employer: 
location: London
region: London
salary: £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: secretary; manual review required: annualised upper salary £45,000 exceeds regional review point £42,000
source_url: 
hub_fingerprint: 6989cb9e435645317a3b005a05acdec417b4beaaded7f0f00491a89d3b9179a3
---

---
action:
POSS | JobG8 | London | London | — | Senior Bookkeeper - Music, Sport, TV and Media Clients
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2101557
title: Senior Bookkeeper - Music, Sport, TV and Media Clients
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 287fe8c21877e1d7a5d874eaacdff7bd3beb7f96d042416e958abb2aef134fa5
---

---
action:
POSS | JobG8 | London | Teddington | £40000 - £45000 per year | Payroll Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2080591
title: Payroll Administrator
employer: 
location: Teddington
region: London
salary: £40000 - £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator, payroll administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: e86e0258b089f5b069c44ae54ea09e23fa369dc55314ec4e8560677fb639c57a
---

---
action:
POSS | JobG8 | Merseyside - Liverpool | Liverpool | — | Financial Controller
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2096447
title: Financial Controller
employer: 
location: Liverpool
region: Merseyside - Liverpool
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: 5c5d205b75c8a2715c6fba0d9ff6934786e827bc75ed6aea47a5562d82493877
---

---
action:
POSS | JobG8 | Norfolk | Norfolk | — | Management Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2209880
title: Management Accounts Assistant
employer: 
location: Norfolk
region: Norfolk
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: fb31d5ba170cc23f0639aa46e91a0cb016738e17499b7922f622d13dd3f5fb7c
---

---
action:
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Tyne And Wear | — | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2082621
title: Finance Manager
employer: 
location: Tyne And Wear
region: North East - Tyneside, Wearside & Northumberland
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: f48b2cd38390536d41fb707478e7d32cd24a8399cc3bec41235b6bac71b416a5
---

---
action:
POSS | JobG8 | Oxfordshire | Oxfordshire | £40000 per year | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2199114
title: Payroll Manager
employer: 
location: Oxfordshire
region: Oxfordshire
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 0f7f673b4ab60a43c56d55aae766c4e8985205538e98f83a9df38ffc0689fe12
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

---
action:
POSS | JobG8 | Scotland Central - Falkirk & Stirling | Stirling | £41,500 per year (FTE) | Part-Time Payroll Specialist
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2085251
title: Part-Time Payroll Specialist
employer: 
location: Stirling
region: Scotland Central - Falkirk & Stirling
salary: £41,500 per year (FTE)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: eaa9e6f61cb441489039e180dea0365d7c9034f0e2b16c891a3cc6280f973001
---

---
action:
POSS | JobG8 | Surrey | Surrey | £32000 - £38000 per year | Accounts & Credit Control Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2178784
title: Accounts & Credit Control Coordinator
employer: 
location: Surrey
region: Surrey
salary: £32000 - £38000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £38,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 217db89060a9be48df1cb84e3c526fd2890000e12fd023dae3a5e32a8fc4cb95
---

---
action:
POSS | JobG8 | Surrey | Surrey | — | Accounts Manager - Part-time
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2183323
title: Accounts Manager - Part-time
employer: 
location: Surrey
region: Surrey
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: aeda7e9b40a1b3512bea50ea0ef55df163b08b7f42a2110cd67f6bcee965c207
---

---
action:
POSS | JobG8 | Surrey | Surrey | — | Graduate Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2102430
title: Graduate Accounts Assistant
employer: 
location: Surrey
region: Surrey
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: 1805164640902fc4ab72321b1d07abb874539dc33dd6f08e81cd0074c53376a6
---

---
action:
POSS | JobG8 | Surrey | Surrey | — | Part-Time Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2077625
title: Part-Time Finance Manager
employer: 
location: Surrey
region: Surrey
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: f43cc2571bc4394348d848eae0893b45cf581331608ed37b3704d73e2f450ca0
---

---
action:
POSS | JobG8 | Surrey | Surrey | £44000 per year | Payroll & Credit Controller - Ref (8813)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2158445
title: Payroll & Credit Controller - Ref (8813)
employer: 
location: Surrey
region: Surrey
salary: £44000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: credit controller; manual review required: annualised upper salary £44,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 037c3cfbfcb81cfe44b30935e0e5abf11eaee8c4125721f7440ca39ad9845f1a
---

---
action:
POSS | JobG8 | Sussex | Sussex | £40000 - £50000 per year | Project Coordinator - Infrastructure (Solar, EV & Automation)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2156418
title: Project Coordinator - Infrastructure (Solar, EV & Automation)
employer: 
location: Sussex
region: Sussex
salary: £40000 - £50000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: 6a70235732d952e56e96706797cfe4ab2c3ccc698f680475d523b0402d54fda8
---

---
action:
POSS | JobG8 | Wales South - Swansea Bay | Bridgend | £15.75 per hour | Accounts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2087844
title: Accounts Administrator
employer: 
location: Bridgend
region: Wales South - Swansea Bay
salary: £15.75 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Basic accounts administration is transferable unless specialist qualifications are mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: 8a226ae8dac0bc9c32a41597a08a1fd0ee315e15b1641db28b0cecc40fb24cd5
---

---
action:
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | £140 - £150 per daily | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2082787
title: Accounts Assistant
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: £140 - £150 per daily
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: accounts assistant; manual review required: annualised upper salary £39,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 4ef338aed8e9644141d656072b8614c55ae7f684fa1f3b90c1ff108ea4c76a4e
---

---
action:
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | — | Interim Finance Manager - Part Time
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2203812
title: Interim Finance Manager - Part Time
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 805828fdeeacf54b665e8bc2e0e77f2190962743bfce64a698444206adc71f9a
---

---
action:
POSS | JobG8 | Worcestershire | Worcestershire | — | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2077486
title: Accounts Assistant
employer: 
location: Worcestershire
region: Worcestershire
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: 973abe5fbca8ee67c45cf68cbe9fc7af445b469430f70a496e1dbc62238b988c
---

---
action:
POSS | JobG8 | Worcestershire | Worcestershire | £40000 - £45000 per year | Business Central Administrator (Junior Developer)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2188485
title: Business Central Administrator (Junior Developer)
employer: 
location: Worcestershire
region: Worcestershire
salary: £40000 - £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: 4d05f06cabe02391a8c8a5d14408214c708a58277fa36fcd6f8ae12b7465d023
---

---
action:
POSS | JobG8 | Yorkshire - South | Sheffield | — | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2200700
title: Finance Manager
employer: 
location: Sheffield
region: Yorkshire - South
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 4b05244dab606b6f4ac9460cebba765b721ca95c88a4bb49a5bce004adbe4ee2
---

---
action:
POSS | JobG8 | Yorkshire - West | Halifax | £38,000 - £45,000 per year (FTE) | Part-Time Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2195229
title: Part-Time Finance Manager
employer: 
location: Halifax
region: Yorkshire - West
salary: £38,000 - £45,000 per year (FTE)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: 9786d4aaefaa997e06497af4fc5f753067cc85028bc981a759ad9c28d502c829
---

---
action:
POSS | JobG8 | Yorkshire - West | Holmfirth | — | Accounts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2187106
title: Accounts Administrator
employer: 
location: Holmfirth
region: Yorkshire - West
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Basic accounts administration is transferable unless specialist qualifications are mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: 061c7ba85bca45782da1fdd8e999b709e46486898fdd6cc13eb9157fd10c3da3
---

---
action:
POSS | JobG8 | Yorkshire - West | Huddersfield | £40000 - £45000 per year | Bookkeeper
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2097748
title: Bookkeeper
employer: 
location: Huddersfield
region: Yorkshire - West
salary: £40000 - £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: bookkeeper; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: b8432e7d983d93d8d358531fc09a8582c5d342124df675e1714b0a37b9625414
---

---
action:
POSS | JobG8 | Yorkshire - West | Ilkley | £45,000 - £50,000 per year (FTE) | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2203737
title: Finance Manager
employer: 
location: Ilkley
region: Yorkshire - West
salary: £45,000 - £50,000 per year (FTE)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 1387ffb209953fc302b5ebbda970afe1e67f36ac58e2ee01a7f4145666ea97c7
---

---
action:
POSS | JobG8 | Yorkshire - West | Leeds | £25,000 per year | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2195136
title: Accounts Assistant
employer: 
location: Leeds
region: Yorkshire - West
salary: £25,000 per year
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: 2fdef423ed445dd593936100a3b3881dc662cc2bdabefdf62d092f07a370d03c
---

---
action:
POSS | JobG8 | Yorkshire - West | Leeds | £18.00 - £20.00 per hour | Interim Finance Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2097433
title: Interim Finance Assistant
employer: 
location: Leeds
region: Yorkshire - West
salary: £18.00 - £20.00 per hour
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: cba38c6dd463b84fdc617358aaa2c63450d6675cdfd02644813f1f30c8232566
---

---
action:
POSS | JobG8 | Yorkshire - West | Leeds | £140 - £170 per daily | Payroll Clerk
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2197982
title: Payroll Clerk
employer: 
location: Leeds
region: Yorkshire - West
salary: £140 - £170 per daily
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: payroll clerk; manual review required: annualised upper salary £44,200 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 6aec0057a306ab22fba5894cd2f0285aa3b6e72436d3a450f841f07574f501f8
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

## Teaching Vacancies — 78 to review

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
POSS | Teaching Vacancies | Buckinghamshire | Milton Keynes, South East, MK2 3HQ | £24413 - £25583 per annum | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-lift-sir-herbert-leon
title: Receptionist
employer: Lift Sir Herbert Leon
location: Milton Keynes, South East, MK2 3HQ
region: Buckinghamshire
salary: £24413 - £25583 per annum
closing_date: 2026-11-17T13:08:02+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-lift-sir-herbert-leon
hub_fingerprint: 564c4d4771b043464c6910f7634c770f823cd1895ccae79e3f0f72abb0e7e24c
---

---
action:
POSS | Teaching Vacancies | Cambridgeshire | Cambridge, East of England, CB4 2QT | £25,823-£27,152 per annum | HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-cambridge-regional-college
title: HR Administrator
employer: Cambridge Regional College
location: Cambridge, East of England, CB4 2QT
region: Cambridgeshire
salary: £25,823-£27,152 per annum
closing_date: 2026-11-01T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-cambridge-regional-college
hub_fingerprint: 2c042a6e5bd35c719825d67f47744bd265cf4d43802c2845377a2eff615e48ad
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
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-officer-105487cf-80e2-4f7a-a8ea-cac5b40a9e6d
hub_fingerprint: e10153c142a24fbf7424e4458f0bf97b1284ef428c5dd5c79f428824fbd8ea91
---

---
action:
POSS | Teaching Vacancies | Hampshire | Portsmouth, South East, PO1 1RX | £26,033-£29,170 | SEN Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: sen-administrator-st-edmund-s-catholic-school-portsmouth-hampshire
title: SEN Administrator
employer: St Edmund's Catholic School
location: Portsmouth, South East, PO1 1RX
region: Hampshire
salary: £26,033-£29,170
closing_date: 2026-11-02T15:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/sen-administrator-st-edmund-s-catholic-school-portsmouth-hampshire
hub_fingerprint: fbeee0c4f6dcd5581b95ac1c65959d7bc15bfcde9d3de6599bbca011d3fec16c
---

---
action:
POSS | Teaching Vacancies | Kent | Dartford, South East, DA1 2JT | £25,429 per annum | Centre Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: centre-administrator-north-kent-college
title: Centre Administrator
employer: North Kent College
location: Dartford, South East, DA1 2JT
region: Kent
salary: £25,429 per annum
closing_date: 2026-11-01T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/centre-administrator-north-kent-college
hub_fingerprint: 99ee6e1a02d5f51574170975af2d0dca11c258834fc0c3c66557a522237aca37
---

---
action:
POSS | Teaching Vacancies | Kent | Gillingham, South East, ME7 2JG | £26,016.00 - £29,071.00 Annually (FTE) Medway D2 4 - 11 £22,047.56 - £25,024.19 Actual Salary | Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-assistant-barnsole-primary-school
title: Administration Assistant
employer: Barnsole Primary School
location: Gillingham, South East, ME7 2JG
region: Kent
salary: £26,016.00 - £29,071.00 Annually (FTE) Medway D2 4 - 11 £22,047.56 - £25,024.19 Actual Salary
closing_date: 2026-11-02T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-assistant-barnsole-primary-school
hub_fingerprint: 8d7524604c5697f9b6e89b95fbbb840ef5380c90866ebe8b3206ea1163a3aaa5
---

---
action:
POSS | Teaching Vacancies | Kent | Tonbridge, South East, TN9 2HE | Actual Pro Rata Salary £23,599 | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-hillview-school-for-girls-tonbridge-kent
title: Administrative Assistant
employer: Hillview School for Girls
location: Tonbridge, South East, TN9 2HE
region: Kent
salary: Actual Pro Rata Salary £23,599
closing_date: 2026-10-30T23:59:59+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-hillview-school-for-girls-tonbridge-kent
hub_fingerprint: edf695bfa1d202058bb4963ac45c9604696a743789c3221f1bb7ce2006682679
---

---
action:
POSS | Teaching Vacancies | Lancashire - Central | Preston, North West, PR4 6AQ | £23,155.61 - £23,895.24 Annually (Actual) FTE £26,016 - £26,847 | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-tarleton-academy
title: Receptionist
employer: Tarleton Academy
location: Preston, North West, PR4 6AQ
region: Lancashire - Central
salary: £23,155.61 - £23,895.24 Annually (Actual) FTE £26,016 - £26,847
closing_date: 2026-11-02T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-tarleton-academy
hub_fingerprint: ebd63c01e4e5e43ea690ac4e34d3d8fb72f4809f3e973cd1bd39a5400e52b2ad
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
POSS | Teaching Vacancies | London | Bexleyheath, London, DA6 7DA | £26039 - £26412 per annum | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-lift-bexleyheath-bexleyheath-kent
title: Receptionist
employer: Lift Bexleyheath
location: Bexleyheath, London, DA6 7DA
region: London
salary: £26039 - £26412 per annum
closing_date: 2026-11-09T13:15:04+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-lift-bexleyheath-bexleyheath-kent
hub_fingerprint: d5bb0cdbc5165a410379197cd1753c3805ab03920d0f77573ccdca83ee5ec53f
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
POSS | Teaching Vacancies | London | Chislehurst, London, BR7 6HE | £29,561 | Receptionist & Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-administrator-chislehurst-school-for-girls
title: Receptionist & Administrator
employer: Chislehurst School for Girls
location: Chislehurst, London, BR7 6HE
region: London
salary: £29,561
closing_date: 2026-11-03T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-administrator-chislehurst-school-for-girls
hub_fingerprint: 30ed6b23ecc77ec365845e45b5f3435e7bb231e3a1e13aeb9a17fc56c87c513a
---

---
action:
POSS | Teaching Vacancies | London | Croydon, London, CR2 6HS | £30,408 | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-harris-primary-academy-haling-park
title: Administrative Assistant
employer: Harris Primary Academy Haling Park
location: Croydon, London, CR2 6HS
region: London
salary: £30,408
closing_date: 2026-11-02T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-harris-primary-academy-haling-park
hub_fingerprint: e6c32a9cebf15174573cae81559dacfb8e739ea4e44f2dc6863d2d589c10934f
---

---
action:
POSS | Teaching Vacancies | London | Dagenham, London, RM10 7UR | £28,909.00 - £30,200.00 Annually (Actual) Salary Scale: Scale 5 (Pt12-15, £33,609 - £35,109) Prorated salary range is likely to be approx. £28,909 - £30,200 (also dependant on experience, weeks per year and continuous service) Based on working 35 hours per week, Term time only. (Subject to job evaluation) | SEND Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-administrator-eastbrook-school
title: SEND Administrator
employer: Eastbrook School
location: Dagenham, London, RM10 7UR
region: London
salary: £28,909.00 - £30,200.00 Annually (Actual) Salary Scale: Scale 5 (Pt12-15, £33,609 - £35,109) Prorated salary range is likely to be approx. £28,909 - £30,200 (also dependant on experience, weeks per year and continuous service) Based on working 35 hours per week, Term time only. (Subject to job evaluation)
closing_date: 2026-11-02T08:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-administrator-eastbrook-school
hub_fingerprint: 734d3a0331dd4511d4af8dfde72848445c10f8178c8ea092fc8a807468d93910
---

---
action:
POSS | Teaching Vacancies | London | Dagenham, London, RM9 4UN | £28,709.00 - £30,364.00 Annually (Actual) full time equivalent £31,290- £32,655 | Admin Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: admin-assistant-3fdfc1e3-6219-478b-b4d8-4889ed95e085
title: Admin Assistant
employer: Jo Richardson Community School
location: Dagenham, London, RM9 4UN
region: London
salary: £28,709.00 - £30,364.00 Annually (Actual) full time equivalent £31,290- £32,655
closing_date: 2026-11-11T08:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/admin-assistant-3fdfc1e3-6219-478b-b4d8-4889ed95e085
hub_fingerprint: 835ff8abadeb436a59a6a0946aeecaf7c339e5b48e7a7b38172f4e7728c7f4ed
---

---
action:
POSS | Teaching Vacancies | London | Feltham, London, TW13 4QP | Scale 3 (£23,507.84 - £23.844.13) | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-oak-hill-academy-west-london
title: Administrative Assistant
employer: Oak Hill Academy West London
location: Feltham, London, TW13 4QP
region: London
salary: Scale 3 (£23,507.84 - £23.844.13)
closing_date: 2026-10-30T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-oak-hill-academy-west-london
hub_fingerprint: 87fd16b2c3ec8400e1988b977b8b52085b3317ffab94bbcf1d6b976892c31449
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
POSS | Teaching Vacancies | London | Isleworth, London, TW7 5DB | £33,129.00 - £35,109.00 Annually (FTE) NJC Scale 5 £33,129 to £35,109 (pro rata) Pro rata salary based on working 36 hours a week for 5 days a week, 39 weeks per annum (N.B. this is ‘term time’ i.e. 195 days) | SEND Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-administrator-bolder-academy-isleworth
title: SEND Administrator
employer: Bolder Academy
location: Isleworth, London, TW7 5DB
region: London
salary: £33,129.00 - £35,109.00 Annually (FTE) NJC Scale 5 £33,129 to £35,109 (pro rata) Pro rata salary based on working 36 hours a week for 5 days a week, 39 weeks per annum (N.B. this is ‘term time’ i.e. 195 days)
closing_date: 2026-11-09T12:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-administrator-bolder-academy-isleworth
hub_fingerprint: 828fdc3b20cf8258fdf0911991e7c99af5ee71898db69674507cccd6e2485010
---

---
action:
POSS | Teaching Vacancies | London | London, London, E14 0AF | £33,700-£35,500 per annum | CTEC Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: ctec-administrator
title: CTEC Administrator
employer: New City College
location: London, London, E14 0AF
region: London
salary: £33,700-£35,500 per annum
closing_date: 2026-11-01T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/ctec-administrator
hub_fingerprint: 05860591e34c7ff8aead62efbe71ed2ea6340725314c3143c09f94b636a022f1
---

---
action:
POSS | Teaching Vacancies | London | London, London, E14 0AF | £33,700-£35,500 dependent upon experience | Recruitment and HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: recruitment-and-hr-administrator-new-city-college
title: Recruitment and HR Administrator
employer: New City College
location: London, London, E14 0AF
region: London
salary: £33,700-£35,500 dependent upon experience
closing_date: 2026-11-15T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/recruitment-and-hr-administrator-new-city-college
hub_fingerprint: f960d67a88fed35f94dc6d38cb95283d055233ff4c635c84ebd6066a0ada3ab3
---

---
action:
POSS | Teaching Vacancies | London | London, London, E17 5SD | £26,016.00 to £26,427.00 per annum (pro rata £22,951.04 to £23,313.62 per annum) plus London Weighting £2,376.00 per annum (pro rata £2,096.08) | Receptionist
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: receptionist-eden-girls-school-waltham-forest
title: Receptionist
employer: Eden Girls' School, Waltham Forest
location: London, London, E17 5SD
region: London
salary: £26,016.00 to £26,427.00 per annum (pro rata £22,951.04 to £23,313.62 per annum) plus London Weighting £2,376.00 per annum (pro rata £2,096.08)
closing_date: 2026-11-08T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/receptionist-eden-girls-school-waltham-forest
hub_fingerprint: a3df8bfd5d5a49e0640ee2ed0ec8622bec45421d593ad112864bacdf138a63e5
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
POSS | Teaching Vacancies | London | London, London, W2 5EZ | WA Scale 5, Spine Point Range 12 - 17, £26,631 - £29,184 FTE (£23,780 - £26,081 pro rata) | Sixth Form Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: sixth-form-administrator-westminster-academy
title: Sixth Form Administrator
employer: Westminster Academy
location: London, London, W2 5EZ
region: London
salary: WA Scale 5, Spine Point Range 12 - 17, £26,631 - £29,184 FTE (£23,780 - £26,081 pro rata)
closing_date: 2026-11-02T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/sixth-form-administrator-westminster-academy
hub_fingerprint: 06b1a1c423993560e9829b9b7c779bf5a3791234dd303da5eef29c194d31c0b6
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
POSS | Teaching Vacancies | Northamptonshire | Wellingborough, East Midlands, NN8 3HB | £16,624.20 - £16,889.23 Annually (FTE) Based on NJS Scale F6 - F7, FTE salary is £26,846 - £27,274 | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-st-barnabas-church-of-england-school
title: Administrator
employer: St Barnabas Church of England School
location: Wellingborough, East Midlands, NN8 3HB
region: Northamptonshire
salary: £16,624.20 - £16,889.23 Annually (FTE) Based on NJS Scale F6 - F7, FTE salary is £26,846 - £27,274
closing_date: 2026-11-06T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-st-barnabas-church-of-england-school
hub_fingerprint: 95dfcb7090b915916c44c627cecff0fb750dcce62bd4dcf96b3d6b71042ab77c
---

---
action:
POSS | Teaching Vacancies | Nottinghamshire | Mansfield, East Midlands, NG18 2DP | £22,569.72 - £22,569.72 Annually (Actual) | Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-assistant-horizons-academy-mansfield-nottinghamshire
title: Administration Assistant
employer: Horizons Academy
location: Mansfield, East Midlands, NG18 2DP
region: Nottinghamshire
salary: £22,569.72 - £22,569.72 Annually (Actual)
closing_date: 2026-11-08T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-assistant-horizons-academy-mansfield-nottinghamshire
hub_fingerprint: 095a3e9993e6cf95c06e0e92650acc5afbe0692b6280b406c9f8256b63376f46
---

---
action:
POSS | Teaching Vacancies | Nottinghamshire | Nottingham, East Midlands, NG4 2LR | £22,753 Actual Salary (£26,016 FTE) | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-netherfield-primary-school
title: Administrative Assistant
employer: Netherfield Primary School
location: Nottingham, East Midlands, NG4 2LR
region: Nottinghamshire
salary: £22,753 Actual Salary (£26,016 FTE)
closing_date: 2026-11-08T12:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-netherfield-primary-school
hub_fingerprint: 59e3df1a17e0264c90880b181aa347f63ac5a20726614c086a6d6511e7b83d30
---

---
action:
POSS | Teaching Vacancies | Nottinghamshire | Nottingham, East Midlands, NG8 2FT | £22,507.00 - £24,527.00 Annually (Actual) The salary advertised reflects the pro rata salary for this role, based on 45.6 weeks per year. The full-time equivalent FTE salary for this position is £25,666 - 27,970 per annum. | SEND Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: send-administrator-fernwood-school
title: SEND Administrator
employer: Fernwood School
location: Nottingham, East Midlands, NG8 2FT
region: Nottinghamshire
salary: £22,507.00 - £24,527.00 Annually (Actual) The salary advertised reflects the pro rata salary for this role, based on 45.6 weeks per year. The full-time equivalent FTE salary for this position is £25,666 - 27,970 per annum.
closing_date: 2026-11-02T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/send-administrator-fernwood-school
hub_fingerprint: 735bbb6dfb8c00920602acc79a81fd3db77393ddd82c2b579d02fe9c1a609dda
---

---
action:
POSS | Teaching Vacancies | Nottinghamshire | Nottingham, East Midlands, NG9 1AE | £22,611 Actual Salary (£26,016 FTE) | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-round-hill-primary-school-nottingham-nottinghamshire
title: Administrative Assistant
employer: Round Hill Primary School
location: Nottingham, East Midlands, NG9 1AE
region: Nottinghamshire
salary: £22,611 Actual Salary (£26,016 FTE)
closing_date: 2026-11-02T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-round-hill-primary-school-nottingham-nottinghamshire
hub_fingerprint: f64d1752b7107541e137809529d9905fc09d584a4fb1bea1945c16045cd6f940
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
POSS | Teaching Vacancies | Oxfordshire | Abingdon, South East, OX14 5NL | £27,709.00 - £30,023.00 Annually (FTE) Grade 6, SCP 8 - 13. Actual salary - £19,783.71 - £21,435.86 | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-thameside-primary-school-abingdon-oxfordshire
title: Office Administrator
employer: Thameside Primary School
location: Abingdon, South East, OX14 5NL
region: Oxfordshire
salary: £27,709.00 - £30,023.00 Annually (FTE) Grade 6, SCP 8 - 13. Actual salary - £19,783.71 - £21,435.86
closing_date: 2026-11-04T12:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-thameside-primary-school-abingdon-oxfordshire
hub_fingerprint: ddd2efad18026a19d58307a5e1868ff8607af69cda2b78adfc1a1eb9106067bc
---

---
action:
POSS | Teaching Vacancies | Oxfordshire | Oxford, OX2 9JE | £32,578.00 - £35,570.00 Annually (FTE) | Finance Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-officer-acer-trust-oxford-not-recorded
title: Finance Officer
employer: Acer Trust
location: Oxford, OX2 9JE
region: Oxfordshire
salary: £32,578.00 - £35,570.00 Annually (FTE)
closing_date: 2026-11-16T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-officer-acer-trust-oxford-not-recorded
hub_fingerprint: 468edadebe75a89a43cc4f3c6e923190e1b85227f212054d2a29bf6e9e083d10
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
POSS | Teaching Vacancies | Somerset | Taunton, TA2 7EG | FTE= £26,847, Actual= £12,427 | HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-the-oak-partnership-trust
title: HR Administrator
employer: The Oak Partnership Trust
location: Taunton, TA2 7EG
region: Somerset
salary: FTE= £26,847, Actual= £12,427
closing_date: 2026-11-03T23:59:59+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-the-oak-partnership-trust
hub_fingerprint: f5b69c3492a94b42c9cd3dfc38685a7be5bbdf434cd456ab27eb6fd610bcdc9f
---

---
action:
POSS | Teaching Vacancies | Staffordshire | Cannock, West Midlands, WS11 4AW | £26,426, Term time plus inset (actual salary paid pro rata). | Administrative Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrative-assistant-cardinal-griffin-catholic-college
title: Administrative Assistant
employer: Cardinal Griffin Catholic College
location: Cannock, West Midlands, WS11 4AW
region: Staffordshire
salary: £26,426, Term time plus inset (actual salary paid pro rata).
closing_date: 2026-11-06T08:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrative-assistant-cardinal-griffin-catholic-college
hub_fingerprint: 2f626c34ef997040bd2022fa82d50b44ad24a29a12aed664a399266b056231c6
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
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-officer-beccles-high-school
hub_fingerprint: 5b6530d9bf5f04230d9ace9f8ea873e15a31b749a5177759ae457ecfd935a246
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
POSS | Teaching Vacancies | Sussex | Worthing, South East, BN14 8AH | £26,268.00 Annually (Actual) Paid 47.6 week to include holiday and additional days | Finance Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-administrator-bohunt-school-worthing-worthing-west-sussex
title: Finance Administrator
employer: Bohunt School Worthing
location: Worthing, South East, BN14 8AH
region: Sussex
salary: £26,268.00 Annually (Actual) Paid 47.6 week to include holiday and additional days
closing_date: 2026-10-30T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-administrator-bohunt-school-worthing-worthing-west-sussex
hub_fingerprint: 1fa71dc737cff821fd8f1b33aa549565d7d8d65b95c5ae9f7349d18d36fe2110
---

---
action:
POSS | Teaching Vacancies | West Midlands - Birmingham & Solihull | Birmingham, West Midlands, B29 4HE | £23,408.04 - £25,392.13 Annually (Actual) SCP 12-17 | Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administrator-cf5e5aab-64b0-42ed-a819-f37cfdc52017
title: Administrator
employer: E-ACT Shenley Academy
location: Birmingham, West Midlands, B29 4HE
region: West Midlands - Birmingham & Solihull
salary: £23,408.04 - £25,392.13 Annually (Actual) SCP 12-17
closing_date: 2026-11-02T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administrator-cf5e5aab-64b0-42ed-a819-f37cfdc52017
hub_fingerprint: 37bed5572fa0da8fd63ba3f0a331e0ed4310b060e9e8f40d092d5449f520a2f2
---

---
action:
POSS | Teaching Vacancies | West Midlands - Birmingham & Solihull | Birmingham, West Midlands, B43 6LN | £26,427.00 - £26,847.00 Annually (FTE) | School Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: school-administrator-holy-name-catholic-primary-school
title: School Administrator
employer: Holy Name Catholic Primary School
location: Birmingham, West Midlands, B43 6LN
region: West Midlands - Birmingham & Solihull
salary: £26,427.00 - £26,847.00 Annually (FTE)
closing_date: 2026-11-09T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/school-administrator-holy-name-catholic-primary-school
hub_fingerprint: 1285a3291e3c1de33b54c7d4cae36c41e607965d65e27344174924c0539fb296
---

---
action:
POSS | Teaching Vacancies | West Midlands - Birmingham & Solihull | Sutton Coldfield, West Midlands, B73 6UE | £21,775.00 - £23,933.00 Annually (Actual) | School Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: school-administrator-395dae48-626d-47cd-88b7-92b46f8c8d1e
title: School Administrator
employer: Sutton Park Primary
location: Sutton Coldfield, West Midlands, B73 6UE
region: West Midlands - Birmingham & Solihull
salary: £21,775.00 - £23,933.00 Annually (Actual)
closing_date: 2026-11-01T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/school-administrator-395dae48-626d-47cd-88b7-92b46f8c8d1e
hub_fingerprint: 4212d39fefbdd211ef29fd753ede200dcedeca970b1e571cca8351dd41612174
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
POSS | Teaching Vacancies | Yorkshire - East | Hull, Yorkshire and the Humber, HU4 7EB | £26,016 - £27,274 FTE, £17,694 - £18,550 Actual | Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-assistant-christopher-pickering-primary-school
title: Administration Assistant
employer: Christopher Pickering Primary School
location: Hull, Yorkshire and the Humber, HU4 7EB
region: Yorkshire - East
salary: £26,016 - £27,274 FTE, £17,694 - £18,550 Actual
closing_date: 2026-10-31T08:00:59+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-assistant-christopher-pickering-primary-school
hub_fingerprint: 3dfb95e1a9d852654abb017e498a48eccde8f2ecc1d15914f0f593f1c80d25d0
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

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Halifax, Yorkshire and the Humber, HX2 9SU | £23,591.00 - £25,590.00 Annually (Actual) NJC Scale Point 5 Points 12-17 (3.3% pay award pending) | Finance Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: finance-assistant-the-north-halifax-grammar-school
title: Finance Assistant
employer: The North Halifax Grammar School
location: Halifax, Yorkshire and the Humber, HX2 9SU
region: Yorkshire - West
salary: £23,591.00 - £25,590.00 Annually (Actual) NJC Scale Point 5 Points 12-17 (3.3% pay award pending)
closing_date: 2026-10-30T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/finance-assistant-the-north-halifax-grammar-school
hub_fingerprint: 395c1e5c96e1f4cd6a9b5c1cf7fbcb4cdffebc3b6a4e3fb185e5ad4f63fe51e4
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Huddersfield, Yorkshire and the Humber, HD1 4ES | £25,951.00 to £27,733.00 per annum FTE | HR Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: hr-administrator-greenhead-college
title: HR Administrator
employer: Greenhead College
location: Huddersfield, Yorkshire and the Humber, HD1 4ES
region: Yorkshire - West
salary: £25,951.00 to £27,733.00 per annum FTE
closing_date: 2026-11-01T23:59:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/hr-administrator-greenhead-college
hub_fingerprint: 1e78d7227cf5a0937c6e08642988bc83861f41e570a38caaa797ab968f68073e
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Huddersfield, Yorkshire and the Humber, HD2 2JT | £25,583.00 - £25,989.00 Annually (FTE) Kirklees Grade 5 | Business Support Officer
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: business-support-officer-854eb79b-4156-4a90-8232-676cdd7ff0a7
title: Business Support Officer
employer: All Saints Catholic College
location: Huddersfield, Yorkshire and the Humber, HD2 2JT
region: Yorkshire - West
salary: £25,583.00 - £25,989.00 Annually (FTE) Kirklees Grade 5
closing_date: 2026-11-03T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/business-support-officer-854eb79b-4156-4a90-8232-676cdd7ff0a7
hub_fingerprint: d9a8af6fd76c27ded4bd7c8e2d14249baf6deb662dd976dfdea6eaf3714b2a21
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Mirfield, Yorkshire and the Humber, WF14 9EZ | £23,632.00 - £24,778.00 Annually (Actual) Grade 5, Scale Point 5-8. FTE - £26,427 - £27,709) | Administration Assistant
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: administration-assistant-the-mirfield-free-grammar-mirfield-west-yorkshire
title: Administration Assistant
employer: The Mirfield Free Grammar
location: Mirfield, Yorkshire and the Humber, WF14 9EZ
region: Yorkshire - West
salary: £23,632.00 - £24,778.00 Annually (Actual) Grade 5, Scale Point 5-8. FTE - £26,427 - £27,709)
closing_date: 2026-11-02T09:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/administration-assistant-the-mirfield-free-grammar-mirfield-west-yorkshire
hub_fingerprint: 2d0f11485ff8923f449b5400e4ad58d95c855bca0abd64a213cdb791de9d7cf7
---

---
action:
POSS | Teaching Vacancies | Yorkshire - West | Wetherby, Yorkshire and the Humber, LS23 6DX | £25,185-£25,989 | Office Administrator
source_key: teaching_vacancies
source: Teaching Vacancies
category: admin_service
source_job_id: office-administrator-primrose-lane-primary-school
title: Office Administrator
employer: Primrose Lane Primary School
location: Wetherby, Yorkshire and the Humber, LS23 6DX
region: Yorkshire - West
salary: £25,185-£25,989
closing_date: 2026-11-06T12:00:00+00:00
reason: Possible JobG8 duplicate requires review
source_url: https://teaching-vacancies.service.gov.uk/jobs/office-administrator-primrose-lane-primary-school
hub_fingerprint: 36eba92fc5da13964df8312e727cd867a93079f260317d80590395d1026e2f70
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
