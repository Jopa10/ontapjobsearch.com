# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs, VONNE, Teaching Vacancies**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-10-29
generated_at: 2026-10-29T08:18:00+00:00

**49 job(s) await a human decision; 2 already answered (51 review rows).**

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
| JobG8 | OK | 2026-10-29 | 51 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | STALE | 2026-10-28 | 0 | — |
| Teaching Vacancies | STALE | 2026-10-28 | 0 | — |
| NHS Jobs | OK | 2026-10-29 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 51 to review

---
action:
POSS | JobG8 | Cambridgeshire | St. Ives | — | Part Time Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2196956
title: Part Time Accounts Assistant
employer: 
location: St. Ives
region: Cambridgeshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: accounts assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 8805e719930dc50243b2646f5b5ea7b20b978ac78a6e74a83f19c6296213436d
---

---
action:
POSS | JobG8 | Dorset | Dorset | £17 per hour | Procurement Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225765658
title: Procurement Administrator
employer: 
location: Dorset
region: Dorset
salary: £17 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Procurement administration is eligible unless substantial expertise or qualifications are mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: 3e09c38b2926034329a24f03bca0db6cf69e87c94eebb3b69ce202831af35e54
---

---
action:
POSS | JobG8 | Essex | Essex | — | Part Time Managing Partner - Finance & Strategy
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225765308
title: Part Time Managing Partner - Finance & Strategy
employer: 
location: Essex
region: Essex
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 8f3c23d539896b993fd433b8421f1a6d085d0e998f444c034cf9643f4c496e0e
---

---
action:
POSS | JobG8 | Greater Manchester - North | Rochdale | £38463 per year | Procurement Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225774127
title: Procurement Coordinator
employer: 
location: Rochdale
region: Greater Manchester - North
salary: £38463 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £38,463 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 5991f1505e0549cbe6e9230bc6e9a82db03611740b8cfe4fc452927133b3c9d2
---

---
action:
POSS | JobG8 | Greater Manchester - Wigan & Bolton | Bolton | £48000 per year | HR Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225773365
title: HR Manager
employer: 
location: Bolton
region: Greater Manchester - Wigan & Bolton
salary: £48000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: a79d790699f32f43530f96c26b6aa3531f54b61e9aff9603b142f35aa62a3ec8
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
POSS | JobG8 | Hertfordshire | Hertfordshire | £130 - £180 per daily | Ophthalmology Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225763630
title: Ophthalmology Administrator
employer: 
location: Hertfordshire
region: Hertfordshire
salary: £130 - £180 per daily
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: bc23bac023c08c9e0d3f400396d4043847caaa4504aa8d787805ed383295742f
---

---
action:
POSS | JobG8 | Hertfordshire | Hertfordshire | £130 - £180 per daily | Opthalmology Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225763809
title: Opthalmology Administrator
employer: 
location: Hertfordshire
region: Hertfordshire
salary: £130 - £180 per daily
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: 3ee4d2a417580ff58fbaa42f23839c25dd3bc994fa570c41cb577a40a507c876
---

---
action:
POSS | JobG8 | Hertfordshire | Hertfordshire | £38000 - £40000 per year (pro rata) | People Operations Coordinator (HR & AI Curious)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225740953
title: People Operations Coordinator (HR & AI Curious)
employer: 
location: Hertfordshire
region: Hertfordshire
salary: £38000 - £40000 per year (pro rata)
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: f5ac8436a09c62172911ab3166128676c4034ceeeb7db6853f34027c6b08f8a3
---

---
action:
POSS | JobG8 | Kent | Kent | £25000 - £38000 per year | Exhibition Logistics & Sales Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225766642
title: Exhibition Logistics & Sales Coordinator
employer: 
location: Kent
region: Kent
salary: £25000 - £38000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £38,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 9d35d77d47ad42c9e855dc421952ba717d06cd09b206f7a396ab0245bbbf08f6
---

---
action:
POSS | JobG8 | Kent | Kent | — | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225771731
title: Finance Manager
employer: 
location: Kent
region: Kent
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 0137012b60627a6b727b40dc1ca41f65f05a148cf5cd3ac144c33bf3fc46c6b7
---

---
action:
POSS | JobG8 | Kent | Kent | — | Purchase Ledger Clerk
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225759058
title: Purchase Ledger Clerk
employer: 
location: Kent
region: Kent
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 301b42c347fd84bc78618a5b53f5e69c8146e1d550a0f2b2ec631e0b629f35c2
---

---
action:
POSS | JobG8 | Kent | Kent | £35000 - £42000 per year | Service Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225764426
title: Service Coordinator
employer: 
location: Kent
region: Kent
salary: £35000 - £42000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: service coordinator; manual review required: annualised upper salary £42,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: d7e3c34239253d16f85c588afc09a248ace05bd49d640c6c570cdd5a6267b283
---

---
action:
POSS | JobG8 | London | City | £12.71 - £17.1 per hour | Housing support worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225768476
title: Housing support worker
employer: 
location: City
region: London
salary: £12.71 - £17.1 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 57cf770ac9e6e6d56a919c008bec58746b4241c2cb8e83b14d87d0593902447c
---

---
action:
POSS | JobG8 | London | Hayes | £20 - £25 per hour | Administrative Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225771912
title: Administrative Assistant
employer: 
location: Hayes
region: London
salary: £20 - £25 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - title register: high-confidence title pattern: administrative assistant; manual review required: annualised upper salary £48,750 exceeds regional review point £42,000
source_url: 
hub_fingerprint: 4bb4630c48f3bbefad6ec3129025b3f5070c90dfaed503e33031b14562ed1eb1
---

---
action:
POSS | JobG8 | London | London | £140 - £170 per daily | 6th Form Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225769386
title: 6th Form Administrator
employer: 
location: London
region: London
salary: £140 - £170 per daily
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: ce095cc878c03bd3dbfd7ecb0f25ced1519c6f0fa2e19e9146e2fa3eb768a981
---

---
action:
POSS | JobG8 | London | London | £50000 per year | Executive Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225768715
title: Executive Assistant
employer: 
location: London
region: London
salary: £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-reviewed adverts confirm corporate executive office support; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory; annualised upper salary £50,000 exceeds regional review point £42,000
source_url: 
hub_fingerprint: 9c5ebaa68b0501f254cecb7269f3a1fc644103cf2e78e4b62964a46c13f3a627
---

---
action:
POSS | JobG8 | London | London | £35525 - £50000 per year | Prestige Service Advisor
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225764139
title: Prestige Service Advisor
employer: 
location: London
region: London
salary: £35525 - £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: service advisor; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: 4cecc8025cb907085c955332ae8632b420be0c507f8d86cd7c214913eff4ef26
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
POSS | JobG8 | London | London | £22 - £23 per hour (Competitive) | Recovery Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225766801
title: Recovery Coordinator
employer: 
location: London
region: London
salary: £22 - £23 per hour (Competitive)
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £44,850 exceeds regional review point £42,000
source_url: 
hub_fingerprint: e4bd9373dad7ac871cd3c7723a9d22afba8e9c8c03a11890c615b4a31f9f926f
---

---
action:
POSS | JobG8 | Norfolk | Norfolk | £32000 - £45000 per year (Plus Excellent Commission and Benefi) | Executive HR Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225751289
title: Executive HR Assistant
employer: 
location: Norfolk
region: Norfolk
salary: £32000 - £45000 per year (Plus Excellent Commission and Benefi)
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: hr assistant; manual review required: annualised upper salary £45,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 26226d622897657fb4363afe539ff04b7f2d7b3bcd2428b0ff2b997628f429eb
---

---
action:
POSS | JobG8 | Norfolk | Norfolk | — | Part-Time Finance Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2195180
title: Part-Time Finance Assistant
employer: 
location: Norfolk
region: Norfolk
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: finance assistant; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: fb8375af2f59fbbcd56c63bb76f05b668add41c402f6a88e8f9dfb5e0735b0fe
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
action:
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Newcastle Upon Tyne | £13.6 - £17.43 per hour | Housing Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225744992
title: Housing Support Worker
employer: 
location: Newcastle Upon Tyne
region: North East - Tyneside, Wearside & Northumberland
salary: £13.6 - £17.43 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 8995d2270b0a8dc98a652c12190c5db54db4cded91f8e6bb07504678f8c89144
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
action:
POSS | JobG8 | North Scotland | Aberdeen | £34000 - £38000 per year | Procurement Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225770731
title: Procurement Coordinator
employer: 
location: Aberdeen
region: North Scotland
salary: £34000 - £38000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £38,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 458f63f934a95d79eba662d7c962c2ee6b4ba6e24a0d46822fe2ea887bae3e41
---

---
action:
POSS | JobG8 | Nottinghamshire | Nottinghamshire | £42839 - £47181 per year | HR Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225763314
title: HR Manager
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: £42839 - £47181 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: c55267e343c2f62a959bc4d2e1d6d5ec14348e1b9db77305a2b86ed36c5a3740
---

---
action:
POSS | JobG8 | Nottinghamshire | Nottinghamshire | £17 - £22 per hour | Supplier Queries Coordinator - Customer Service
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225770640
title: Supplier Queries Coordinator - Customer Service
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: £17 - £22 per hour
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £42,900 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 97ded942de8d1732d822713563c5e39dc3d74f924ae3e55df70a3ab934f2e36c
---

---
action:
POSS | JobG8 | Oxfordshire | Oxfordshire | £45000 - £50000 per year (Access to excellent benefits package) | Executive Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225771691
title: Executive Assistant
employer: 
location: Oxfordshire
region: Oxfordshire
salary: £45000 - £50000 per year (Access to excellent benefits package)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-reviewed adverts confirm corporate executive office support; manual review required: annualised upper salary £50,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 045ee72db5158fd91dd7740021ef17469770331ee2212763b2e03758a3101c18
---

---
action:
POSS | JobG8 | Oxfordshire | Oxfordshire | £45000 - £50000 per year (Bonus) | Executive Assistant & Commercial Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225768558
title: Executive Assistant & Commercial Coordinator
employer: 
location: Oxfordshire
region: Oxfordshire
salary: £45000 - £50000 per year (Bonus)
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £50,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: acd2d51e3c3902ace3126af146111de95774f0383a3df5413ae96725a4cd83a8
---

---
action:
POSS | JobG8 | Oxfordshire | Oxfordshire | £30000 - £40000 per year (bonus and great team) | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225773998
title: Payroll Manager
employer: 
location: Oxfordshire
region: Oxfordshire
salary: £30000 - £40000 per year (bonus and great team)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 82672ee82505bedca99e6b756bbe60361997f26a355f6b56356625b1f3bc01e1
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
POSS | JobG8 | Scotland Central - Fife | Fife | £13.5 - £14.5 per hour | HR Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225750573
title: HR Administrator
employer: 
location: Fife
region: Scotland Central - Fife
salary: £13.5 - £14.5 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - HR administration is transferable unless CIPD or substantial prior expertise is mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: 98c43c870876d073faa14eaba00d1aff5f321a31d585828e0f15e55c1bd3bfd6
---

---
action:
POSS | JobG8 | Scotland Central - Tayside | Dundee | £13.98 - £23.22 per hour | Customer Service Advisor
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225766783
title: Customer Service Advisor
employer: 
location: Dundee
region: Scotland Central - Tayside
salary: £13.98 - £23.22 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: customer service advisor, service advisor; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: dd6603dc247a456f40df923f09d09be50639c3a664e3c137c9c7291725cb3f89
---

---
action:
POSS | JobG8 | Shropshire | Shropshire | £39999 per year | Logistics Co-Ordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108238832
title: Logistics Co-Ordinator
employer: 
location: Shropshire
region: Shropshire
salary: £39999 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: co-ordinator; manual review required: annualised upper salary £39,999 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 1e03f15bc059200cd544a797580555a8c60ab1645f38fabef804802534ea69b9
---

---
action:
POSS | JobG8 | Surrey | Staines | £30000 - £40000 per year | Learning & Development Co-ordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225774316
title: Learning & Development Co-ordinator
employer: 
location: Staines
region: Surrey
salary: £30000 - £40000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: co-ordinator; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 53d67fd38849ca3675a5f10aa7795f07dba285319960042e33e86e7fa0a50fcc
---

---
action:
POSS | JobG8 | Surrey | Staines | £40000 per year | Office Reception & Facilities Co-ordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225768328
title: Office Reception & Facilities Co-ordinator
employer: 
location: Staines
region: Surrey
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: co-ordinator; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 3990d0c12fadb769b60a998b0b72fb49e44781db2402ce5c2df995082c560532
---

---
action:
POSS | JobG8 | Surrey | Surrey | £32000 - £38000 per year | Accounts & Credit Control Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225761019
title: Accounts & Credit Control Coordinator
employer: 
location: Surrey
region: Surrey
salary: £32000 - £38000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £38,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: c1f3d51fa6d0caa64ddc038b6739c988882730d05a042673bcb30f10fd0607bd
---

---
action:
POSS | JobG8 | Surrey | Surrey | — | Experienced Bookkeeper
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2198536
title: Experienced Bookkeeper
employer: 
location: Surrey
region: Surrey
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: bookkeeper; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: bde250bb1948ad852fe9b962b6d12bd6c47b48ba88c23e2340198c4446333358
---

---
action:
POSS | JobG8 | Surrey | Surrey | £18.3 - £19.5 per hour (Pension,parking) | Office Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225772560
title: Office Manager
employer: 
location: Surrey
region: Surrey
salary: £18.3 - £19.5 per hour (Pension,parking)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 8d8d29f3e6c124be7296ba1490886bd6c31499468f8aaf2ae899f5bfea25dbe6
---

---
action:
POSS | JobG8 | Surrey | Surrey | £25000 - £27000 per year (Pension & Bonuses) | Part-Time Office Manager / Facilities Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225775724
title: Part-Time Office Manager / Facilities Coordinator
employer: 
location: Surrey
region: Surrey
salary: £25000 - £27000 per year (Pension & Bonuses)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 438bef097c2fdf49afb6aec6c5426400a93e8defcc1a34adb3a3ee9c577175e2
---

---
action:
POSS | JobG8 | Surrey | Surrey | £45000 - £50000 per year | Personal Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225763983
title: Personal Assistant
employer: 
location: Surrey
region: Surrey
salary: £45000 - £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-approved only for explicit executive or office PA descriptions; direct-care and legal PA work stays excluded; agreed context rule satisfied; manual review required: annualised upper salary £50,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 042d7832795f27ab70369b73c0e2399d02840745a2a88e4b792142009f6ebea8
---

---
action:
POSS | JobG8 | Surrey | Surrey | £50000 per year | Personal Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225766700
title: Personal Assistant
employer: 
location: Surrey
region: Surrey
salary: £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-approved only for explicit executive or office PA descriptions; direct-care and legal PA work stays excluded; agreed context rule satisfied; manual review required: annualised upper salary £50,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 837db87582a9551c7bdf31517afc5e3214dfbb8e6ed4989901d6e43ad9828a7b
---

---
action:
POSS | JobG8 | Surrey | Surrey | £35000 - £40000 per year (Hybrid working) | Personal Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225772603
title: Personal Assistant
employer: 
location: Surrey
region: Surrey
salary: £35000 - £40000 per year (Hybrid working)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-approved only for explicit executive or office PA descriptions; direct-care and legal PA work stays excluded; agreed context rule satisfied; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: b28de0c69d681b8b34f7fafbd3474b88c11f10ecd37d0c16e26d753c6c2e71ff
---

---
action:
POSS | JobG8 | Sussex | Lancing | £13.68 - £28.22 per hour | Adult Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225766854
title: Adult Support Worker
employer: 
location: Lancing
region: Sussex
salary: £13.68 - £28.22 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 65cc16ed5d358608de4cf295d1ff17e918c0d2a3f7ea721b767122cecac8e25c
---

---
action:
POSS | JobG8 | West Midlands - Birmingham & Solihull | Birmingham | £45000 - £50000 per year | Executive Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225771531
title: Executive Assistant
employer: 
location: Birmingham
region: West Midlands - Birmingham & Solihull
salary: £45000 - £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-reviewed adverts confirm corporate executive office support; manual review required: annualised upper salary £50,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 849729d145ccd1789a3d30f281d2adaf3599acb709947d441441a6f32eb8cf8c
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
POSS | JobG8 | Yorkshire - West | Leeds | £38000 - £40000 per year | Service Department Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225767311
title: Service Department Coordinator
employer: 
location: Leeds
region: Yorkshire - West
salary: £38000 - £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-reviewed advert confirms customer-facing service administration; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 8e96d0bb6d2f63c7490ce9179abcbad9d797898e0d92cf82387073d835b974b6
---

---
action:
POSS | JobG8 | Yorkshire - West | Leeds | £38000 - £40000 per year | Service Scheduler
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225767345
title: Service Scheduler
employer: 
location: Leeds
region: Yorkshire - West
salary: £38000 - £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: scheduler; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 277385d4a9c1a816a1edcc33fac81590891100fd97678affd1cadaa5ec5af834
---

## NHS Jobs — 0 to review

_No new or changed human decisions required._
