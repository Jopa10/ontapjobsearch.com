# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: NEJobs, VONNE, Teaching Vacancies, NHS Jobs**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-11-18
generated_at: 2026-11-18T08:26:05+00:00

**206 job(s) await a human decision; 0 already answered (206 review rows).**

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
| JobG8 | OK | 2026-11-18 | 206 | — |
| NEJobs | STALE | 2026-09-18 | 0 | — |
| VONNE | STALE | 2026-11-17 | 0 | — |
| Teaching Vacancies | STALE | 2026-11-17 | 0 | — |
| NHS Jobs | STALE | 2026-11-17 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.

## JobG8 — 206 to review

---
action:
POSS | JobG8 | Bedfordshire | Bedfordshire | £30000 - £33000 per year | Payroll Manager (Part-time)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2338478
title: Payroll Manager (Part-time)
employer: 
location: Bedfordshire
region: Bedfordshire
salary: £30000 - £33000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 3fe66d24a88a99e2082cb9c92699795442bbedc58d9b5c1857fc26e8ca5eb60e
---

---
action:
POSS | JobG8 | Berkshire | Berkshire | £14 - £14.5 per hour (dependent on experience) | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225798575
title: Learning Support Assistant
employer: 
location: Berkshire
region: Berkshire
salary: £14 - £14.5 per hour (dependent on experience)
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 3a70d654be6ef9d1f945cda6ee481118b92c1b4a5afe1d000c72ce645dbe65c0
---

---
action:
POSS | JobG8 | Berkshire | Berkshire | £20.96 per hour | Repairs Office and Customer Services Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2213072
title: Repairs Office and Customer Services Manager
employer: 
location: Berkshire
region: Berkshire
salary: £20.96 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: fbee809a3c71bb9f7eb0411412f3df2088619d00ffae756e919ac3d1b3bc6a9d
---

---
action:
POSS | JobG8 | Berkshire | Berkshire | £43000 - £50000 per year | Route Planner
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225801404
title: Route Planner
employer: 
location: Berkshire
region: Berkshire
salary: £43000 - £50000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: planner; manual review required: annualised upper salary £50,000 exceeds regional review point £42,000
source_url: 
hub_fingerprint: 2f9461d8b848ec50b25ef842514d91885017017e55333aa523ef5329320df601
---

---
action:
POSS | JobG8 | Berkshire | Bracknell | £14 per hour | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225807600
title: Learning Support Assistant
employer: 
location: Bracknell
region: Berkshire
salary: £14 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 09690548b49860b152a47c7aef0e812d8d0d96d68c4d26eb73dd11d7f06f9e9a
---

---
action:
POSS | JobG8 | Berkshire | Bracknell | £33300 - £34300 per year | Residential Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225432456
title: Residential Support Worker
employer: 
location: Bracknell
region: Berkshire
salary: £33300 - £34300 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 2f63337c33bb7a96dda78fd5632dbf30cb25e47c53fbed434b771ef50bf098d7
---

---
action:
POSS | JobG8 | Berkshire | Bracknell | £31200 - £32300 per year | Waking Night Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225432422
title: Waking Night Support Worker
employer: 
location: Bracknell
region: Berkshire
salary: £31200 - £32300 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 6b6e62db9e143e7e08e636c8b837f074c624eaf5173b24e65c75b217e86a2147
---

---
action:
POSS | JobG8 | Berkshire | Maidenhead | £32916 - £51048 per year | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225816593
title: Learning Support Assistant
employer: 
location: Maidenhead
region: Berkshire
salary: £32916 - £51048 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 9c6c76feb868b4d25ba5b690c79dd2ecd7036cab3c63116fad59d8efa44297c3
---

---
action:
POSS | JobG8 | Berkshire | Reading | £16 - £18 per hour | Complex Care Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225806109
title: Complex Care Support Worker
employer: 
location: Reading
region: Berkshire
salary: £16 - £18 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: b8b4e536672bff94bbe203fe64ec7ec178ad5e46cefa40a363b074301bdd098c
---

---
action:
POSS | JobG8 | Berkshire | Reading | £19 - £28 per hour | Complex Care Workers
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225473061
title: Complex Care Workers
employer: 
location: Reading
region: Berkshire
salary: £19 - £28 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 1445bdb1e9028e621816f8d191632d81095451f2989a9daff82f12b7d36c659b
---

---
action:
POSS | JobG8 | Berkshire | Reading | £170 - £190 per daily | Workplace Experience Ambassador / Facilities Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225829984
title: Workplace Experience Ambassador / Facilities Coordinator
employer: 
location: Reading
region: Berkshire
salary: £170 - £190 per daily
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £49,400 exceeds regional review point £42,000
source_url: 
hub_fingerprint: 0cec0938a1e48e36909f229fb81e1c8033e55955869f852c1e9b440d2e7a05fa
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
POSS | JobG8 | Bristol & Bath | Bristol | — | Finance Manager - Part Time
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2320239
title: Finance Manager - Part Time
employer: 
location: Bristol
region: Bristol & Bath
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 141a778b7a05029caa9cd736c5d5a6993b42a075977958c91c993c911ed152e9
---

---
action:
POSS | JobG8 | Bristol & Bath | Bristol | — | School Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2307604
title: School Finance Manager
employer: 
location: Bristol
region: Bristol & Bath
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 6950148b1de5699ee3095562eaaee81c9b6dc7e39580db96e72d7dbd5cb897dd
---

---
action:
POSS | JobG8 | Cambridgeshire | Peterborough | £20 per hour | Credit Controller / Accounts Receivable Analyst
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2332604
title: Credit Controller / Accounts Receivable Analyst
employer: 
location: Peterborough
region: Cambridgeshire
salary: £20 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: credit controller; manual review required: annualised upper salary £39,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 9efece33ac73b0134f15d473fc3c1b2b2e1d219f372e9e1248a67ddc5bd04fcc
---

---
action:
POSS | JobG8 | Cornwall | St. Austell | £55,000 per year (FTE) | Finance Manager (part time)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2297516
title: Finance Manager (part time)
employer: 
location: St. Austell
region: Cornwall
salary: £55,000 per year (FTE)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 752a831305401f8cc6fa43da2a4d9356b67f023d33563771e588161ce9f61485
---

---
action:
POSS | JobG8 | Dorset | Bournemouth | £14.24 per hour | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225803440
title: Learning Support Assistant
employer: 
location: Bournemouth
region: Dorset
salary: £14.24 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 035d24bf96ed09bded2ea05a021fb75bb9dc6b4780870806b42d992270963423
---

---
action:
POSS | JobG8 | Dorset | Bournemouth | £21 - £23 per hour | Recovery Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225810515
title: Recovery Worker
employer: 
location: Bournemouth
region: Dorset
salary: £21 - £23 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 988013b8d2f21f268e99d4a2b38b973d8074c9f04b7212a738b311dd611091cb
---

---
action:
POSS | JobG8 | Dorset | Dorset | £39000 per year | Care Home Service Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225817964
title: Care Home Service Manager
employer: 
location: Dorset
region: Dorset
salary: £39000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: a12519a8e126d0589494fa57fcae752f885b210eb05dcb85f5f2fe5d07bcfd46
---

---
action:
POSS | JobG8 | Dorset | Dorset | — | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2337784
title: Finance Manager
employer: 
location: Dorset
region: Dorset
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 9a0a03edc4cafecd91c565859b49aa89d2782d7e89e99eb49a2a048121f4f0a1
---

---
action:
POSS | JobG8 | Dorset | Dorset | £40000 - £50000 per year | Logistics Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225816259
title: Logistics Coordinator
employer: 
location: Dorset
region: Dorset
salary: £40000 - £50000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £50,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: ef98216e607a9a25b62af3e192b38170bb34714dad96175d98638df03b1b0cc8
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
POSS | JobG8 | Dorset | Dorset | £17 per hour | Procurement Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225829975
title: Procurement Administrator
employer: 
location: Dorset
region: Dorset
salary: £17 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Procurement administration is eligible unless substantial expertise or qualifications are mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: b065511e022c6479d035fdc4f6fb0c42aaa8257f5fe17dd6ae2780c97468a4ca
---

---
action:
POSS | JobG8 | Dorset | Dorset | £40000 - £45000 per year | Stores & Logistics Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225817654
title: Stores & Logistics Coordinator
employer: 
location: Dorset
region: Dorset
salary: £40000 - £45000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £45,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 434206f6411d717922645dfeda1128dbe7a5b757d33c6cb7d7a8719ba4105f3f
---

---
action:
POSS | JobG8 | Dorset | Ferndown | £15.47 per hour | Care Assistant - Bank - Care Home
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225754044
title: Care Assistant - Bank - Care Home
employer: 
location: Ferndown
region: Dorset
salary: £15.47 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 872e905e232e44937c1772e71d5e369806a1895d6a9b0b5e1fe8e827ddeab7c0
---

---
action:
POSS | JobG8 | Essex | Basildon | £95 - £105 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225811943
title: Learning Support Assistant
employer: 
location: Basildon
region: Essex
salary: £95 - £105 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: f610b5792f9bfd9a5e2b249a55c8c33e942440b0ea1f1b0b462050f10121cfde
---

---
action:
POSS | JobG8 | Essex | Billericay | £100 - £105 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225811942
title: Learning Support Assistant
employer: 
location: Billericay
region: Essex
salary: £100 - £105 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 9cd8e79a8912f42540d41fe76241a17b6cf15cf83a6ce3292f5dfc5a8b76511b
---

---
action:
POSS | JobG8 | Essex | Billericay | £16 per hour | Skilled Support Workers and Care Assistants
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225773041
title: Skilled Support Workers and Care Assistants
employer: 
location: Billericay
region: Essex
salary: £16 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 87a5e5bc17cbe7e2f28e1299dd1166460de4d5f2f784d55385c5bab97595daa9
---

---
action:
POSS | JobG8 | Essex | Chelmsford | £96.86 - £106 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225811939
title: Learning Support Assistant
employer: 
location: Chelmsford
region: Essex
salary: £96.86 - £106 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 2bf3d88db44edbaa22a396a74c6b30e69172b5415c64b56c5f9bf8fbf9d10a6b
---

---
action:
POSS | JobG8 | Essex | Chelmsford | £21 - £23 per hour | Recovery Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225810531
title: Recovery Worker
employer: 
location: Chelmsford
region: Essex
salary: £21 - £23 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: cb7d30a95fcb4edc0dfc12d410ceef037888f3a636c7953b99dd6b0aae00f104
---

---
action:
POSS | JobG8 | Essex | Colchester | £65 - £70 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225820107
title: Learning Support Assistant
employer: 
location: Colchester
region: Essex
salary: £65 - £70 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: af0e88fc6ff0f9adfe665ea5cb5a6813b6dda3016f9de1100fe4850cc35ccf49
---

---
action:
POSS | JobG8 | Essex | Essex | — | Accounts Assistant Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2296336
title: Accounts Assistant Manager
employer: 
location: Essex
region: Essex
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 33154e99c9f8ef198778e9ca5ee8870f9c61cb4cd8f589ac7eace19b19df604d
---

---
action:
POSS | JobG8 | Essex | Essex | £95 - £105 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225811940
title: Learning Support Assistant
employer: 
location: Essex
region: Essex
salary: £95 - £105 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: bc366a2e90ead79af3b86171f14eb7948ebd786280d215b154ca1421e0fd2977
---

---
action:
POSS | JobG8 | Essex | Essex | Competitive | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2299181
title: Payroll Manager
employer: 
location: Essex
region: Essex
salary: Competitive
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: d6908fb615936b324ff4cc6b535de4ba669e7726824f6ed028177d54fd97f140
---

---
action:
POSS | JobG8 | Essex | Essex | £16 per hour | Skilled Support Workers and Care Assistants
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225772984
title: Skilled Support Workers and Care Assistants
employer: 
location: Essex
region: Essex
salary: £16 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 9c7b5b753de11627aa98cb69472d1f8267f4eb488434b91ab9c041a738809733
---

---
action:
POSS | JobG8 | Essex | Essex | £16 per hour | Support Workers and Care Assistants
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225790423
title: Support Workers and Care Assistants
employer: 
location: Essex
region: Essex
salary: £16 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: ed8ef61b276ce598876a040820522da8691f4504d692a01a2d084fe4bff0819e
---

---
action:
POSS | JobG8 | Essex | Harlow | £105 - £120 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225793563
title: Learning Support Assistant
employer: 
location: Harlow
region: Essex
salary: £105 - £120 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 2e63e95c1e0658b86ea12b78a7954fcfe51345d74bf24fbbb2620c9ecc7788b6
---

---
action:
POSS | JobG8 | Essex | Southend-on-sea | £109 - £117 per daily (£150 Love2Shop Voucher Referral) | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225814909
title: Learning Support Assistant
employer: 
location: Southend-on-sea
region: Essex
salary: £109 - £117 per daily (£150 Love2Shop Voucher Referral)
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 28766817539975f8abd465e735333f6c4f612505c7ebaa522825d1b37d1062ab
---

---
action:
POSS | JobG8 | Essex | Southend-on-sea | £21 - £23 per hour | Recovery Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225810545
title: Recovery Worker
employer: 
location: Southend-on-sea
region: Essex
salary: £21 - £23 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 44bc6165338a77b178cf9af0334f681052ee0816977193f8594810f9f52f9949
---

---
action:
POSS | JobG8 | Gloucestershire | Gloucestershire | — | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2306979
title: Finance Manager
employer: 
location: Gloucestershire
region: Gloucestershire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 88b800330159b41d4520035e7a3601d069fd034ed1acb28a123bdbbfa232acad
---

---
action:
POSS | JobG8 | Gloucestershire | Gloucestershire | £40000 per year | Part Time Finance Manager - Excellent benefits!
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2308010
title: Part Time Finance Manager - Excellent benefits!
employer: 
location: Gloucestershire
region: Gloucestershire
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: f98bdbb9ee84d4337662ac1c1b122e74707f92cebe581555bcca4921526b0d8e
---

---
action:
POSS | JobG8 | Greater Manchester - Manchester & Salford | Eccles | — | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2306325
title: Finance Manager
employer: 
location: Eccles
region: Greater Manchester - Manchester & Salford
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 8417d58a6846727dfd53e29084545556c9359acb7fc41c0c23fb0a4826ac51d3
---

---
action:
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | — | Accounts Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2219234
title: Accounts Manager
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 27be349064c5da96279ed2f8d58f0f45d1e6224045313de52b5ea52a051c9c5e
---

---
action:
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | £112 - £115 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225811624
title: Learning Support Assistant
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: £112 - £115 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 9ed8634e8e5129aa1f638a1c2825ad2d5c2549fac2133d61c47b644bf7654204
---

---
action:
POSS | JobG8 | Greater Manchester - Manchester & Salford | Manchester | £22.50 per hour | Senior Bookkeeper
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2259468
title: Senior Bookkeeper
employer: 
location: Manchester
region: Greater Manchester - Manchester & Salford
salary: £22.50 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: 79551eda02e272c9bd3393e630720a677531de9a064d11d344ead1ddad456516
---

---
action:
POSS | JobG8 | Greater Manchester - Manchester & Salford | Salford | £15.47 per hour | Care Assistant - Bank - Care Home
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225813732
title: Care Assistant - Bank - Care Home
employer: 
location: Salford
region: Greater Manchester - Manchester & Salford
salary: £15.47 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 4e1362ed37caa35bb5742f6027cfa7135bc91c235a59743d0293bd99b89b072d
---

---
action:
POSS | JobG8 | Greater Manchester - Manchester & Salford | Salford | £15.47 per hour | Night Care Assistant - Bank
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225828943
title: Night Care Assistant - Bank
employer: 
location: Salford
region: Greater Manchester - Manchester & Salford
salary: £15.47 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: bffef5026363324e689f7f31a8d443fbe2813e5f207c6f5558be55cba23b6ac8
---

---
action:
POSS | JobG8 | Greater Manchester - Manchester & Salford | Swinton | £14.25 - £16.65 per hour (PAYE or Umbrella) | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225781910
title: Learning Support Assistant
employer: 
location: Swinton
region: Greater Manchester - Manchester & Salford
salary: £14.25 - £16.65 per hour (PAYE or Umbrella)
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 09981b0f6118a949eca3547ad0219a2d979161d51bc4111b8585d41b792efd76
---

---
action:
POSS | JobG8 | Greater Manchester - North | Oldham | £38000 - £45000 per year | Executive Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225828065
title: Executive Assistant
employer: 
location: Oldham
region: Greater Manchester - North
salary: £38000 - £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-reviewed adverts confirm corporate executive office support; manual review required: annualised upper salary £45,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 0e4350bb61ca8029c0007c1a3f3e593c70ff6d6a64dcae2b1fe4c4162940c607
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
POSS | JobG8 | Greater Manchester - Wigan & Bolton | Bolton | £30316 - £32842 per year (25 Days Holidays Plus Bank Holidays) | Hr Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225805696
title: Hr Manager
employer: 
location: Bolton
region: Greater Manchester - Wigan & Bolton
salary: £30316 - £32842 per year (25 Days Holidays Plus Bank Holidays)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: dad8b43084d05e0a2ae815a11b787783fab18e7cad21f33e200f9dfc5d70d4de
---

---
action:
POSS | JobG8 | Hampshire | Emsworth | £25186 - £26244 per year | Care Assistant (Older Adults)
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 1401786385
title: Care Assistant (Older Adults)
employer: 
location: Emsworth
region: Hampshire
salary: £25186 - £26244 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 9d55e98bc5ed1971f6369fec17706c5369695d80fec9b8875adb9ea3fe640d22
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
source_job_id: 2220507
title: Finance Manager
employer: 
location: Hampshire
region: Hampshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 9f79133a6c2bd621091811995a0cc9b8ef7a19382054834167c984aaef558263
---

---
action:
POSS | JobG8 | Hampshire | Hampshire | — | Financial Controller (Part time) - Ringwood - &;60-65K pro rata
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2308276
title: Financial Controller (Part time) - Ringwood - &;60-65K pro rata
employer: 
location: Hampshire
region: Hampshire
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: c1dc41db7d4bb70788e374b35b4b70f3cad844c587d6311fb5bc93e3a16da6cb
---

---
action:
POSS | JobG8 | Hampshire | Hampshire | £23 per hour | Intensive Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225813013
title: Intensive Support Worker
employer: 
location: Hampshire
region: Hampshire
salary: £23 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 926d40753a59e6cd3e6c2eac35d2c7f23b680e08ea42ae6d4b7b922dbcdcc1c2
---

---
action:
POSS | JobG8 | Hampshire | Havant | £28697 - £31573 per year (plus £3,000 market supplement) | Children's Home Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 1401786512
title: Children's Home Support Worker
employer: 
location: Havant
region: Hampshire
salary: £28697 - £31573 per year (plus £3,000 market supplement)
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: e6c43d62883693c5d7df29c18d87cd58006e77fe1ede65fb0062ebaacc06763a
---

---
action:
POSS | JobG8 | Hampshire | Havant | £85 - £100 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225804067
title: Learning Support Assistant
employer: 
location: Havant
region: Hampshire
salary: £85 - £100 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 2a0acb4f30c6d757213c31531f5498d9e3e29e81e285e0c6369a5ed93fafc51f
---

---
action:
POSS | JobG8 | Hampshire | Romsey | £28697 - £31573 per year | Children's Home Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 1401786332
title: Children's Home Support Worker
employer: 
location: Romsey
region: Hampshire
salary: £28697 - £31573 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 495bb1e253f1bd2428f69449d306c9f73bd6436d641234f13aeeeb20b20c14ba
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
POSS | JobG8 | Kent | Ashford | £95 - £98 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225808616
title: Learning Support Assistant
employer: 
location: Ashford
region: Kent
salary: £95 - £98 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 9c87029fe64364de809ee495bd36b37a49d59169462cb47fcc19eb33cbfc125f
---

---
action:
POSS | JobG8 | Kent | Kent | £18 - £20 per hour | Children's Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225844545
title: Children's Support Worker
employer: 
location: Kent
region: Kent
salary: £18 - £20 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 1741f0befccd820ff78ed97ebffdf5f6b6e428eb0e887b99841631a1b0ec29a0
---

---
action:
POSS | JobG8 | Kent | Kent | £18.50 per hour | Healthcare Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225815423
title: Healthcare Assistant
employer: 
location: Kent
region: Kent
salary: £18.50 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: b3eb607d1a8b2bf8265d00bfe48c13b536708d4d225570fd15f9d2c17c8a1ecb
---

---
action:
POSS | JobG8 | Kent | Kent | — | Procurement Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2313811
title: Procurement Administrator
employer: 
location: Kent
region: Kent
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Procurement administration is eligible unless substantial expertise or qualifications are mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: 6791d2faeae9df212bdc68292f3186604376ebf5f5f1dc4361b779373c6790ea
---

---
action:
POSS | JobG8 | Kent | Kent | — | PT Senior Payroll Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2307014
title: PT Senior Payroll Officer
employer: 
location: Kent
region: Kent
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 1a99b7c7520985fe1768883679ae053689332f6be346e3566b7b5e85b83039ca
---

---
action:
POSS | JobG8 | Lancashire - East | Blackburn | — | Fractional Financial Controller
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2305188
title: Fractional Financial Controller
employer: 
location: Blackburn
region: Lancashire - East
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: 0361cc42830e6743e0b045ae2b209907b4aa89eb0acfebc65352c83549942bf9
---

---
action:
POSS | JobG8 | Lancashire - East | Blackburn | £38000 - £50000 per year (Benefits package) | Purchasing Coordinator / Buyer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225786516
title: Purchasing Coordinator / Buyer
employer: 
location: Blackburn
region: Lancashire - East
salary: £38000 - £50000 per year (Benefits package)
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £50,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 3f2b5d43f4574cc6f9a96ab10f0d6f5f40682f3ceded82ca0db516275db58b0a
---

---
action:
POSS | JobG8 | Leicestershire | Leicestershire | £14.99 - £15 per hour | Accounts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225781329
title: Accounts Administrator
employer: 
location: Leicestershire
region: Leicestershire
salary: £14.99 - £15 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Basic accounts administration is transferable unless specialist qualifications are mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: a04aad0c100871b56ea361b6346bd529303b9da4b808d8c4c2d4fb4e8501db9e
---

---
action:
POSS | JobG8 | Leicestershire | Leicestershire | £22.11 per hour | Freight Analyst / Freight Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2331066
title: Freight Analyst / Freight Administrator
employer: 
location: Leicestershire
region: Leicestershire
salary: £22.11 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: 199cafc06c9c9b280a6559449c9385913650441b90560ff6ed901b127f1117fc
---

---
action:
POSS | JobG8 | Leicestershire | Leicestershire | £21.11 - £22.11 per hour (Long Term Contract) | Freight Analyst / Freight Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225813751
title: Freight Analyst / Freight Administrator
employer: 
location: Leicestershire
region: Leicestershire
salary: £21.11 - £22.11 per hour (Long Term Contract)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: 465e52145f2eae957b697adbfbefde77f28ae855d850da79476cce385a43c7eb
---

---
action:
POSS | JobG8 | Lincolnshire | Lincolnshire | — | Customer Service Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2222521
title: Customer Service Manager
employer: 
location: Lincolnshire
region: Lincolnshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 33b698d6f944ea3508e973e53fc126eaf2279913d07a989fb0e0b942adbd4924
---

---
action:
POSS | JobG8 | Lincolnshire | Lincolnshire | — | Interim Chief Finance Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2339353
title: Interim Chief Finance Officer
employer: 
location: Lincolnshire
region: Lincolnshire
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 11411331b859f57ea88f64dfe98efc168cdae41b0a46e3fc7f90524bb926a89b
---

---
action:
POSS | JobG8 | London | Brixton | £100 - £120 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225775014
title: Learning Support Assistant
employer: 
location: Brixton
region: London
salary: £100 - £120 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 7498a8e920d2eea6ff2a915a4d5676a94fada26956aa026f4ed05c61cf63f915
---

---
action:
POSS | JobG8 | London | Carshalton | £14 - £16 per hour | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225818222
title: Learning Support Assistant
employer: 
location: Carshalton
region: London
salary: £14 - £16 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: c8a484a9179581384f1e00b4ec672b32078792efb43e691026b62adc39a55012
---

---
action:
POSS | JobG8 | London | City | £100 - £115 per daily | Behaviour Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225798661
title: Behaviour Support Worker
employer: 
location: City
region: London
salary: £100 - £115 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: e4793697ea35748831dff3595f7ec2c6c8d751b62432d1ccc97a7bc3d0484ca1
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
POSS | JobG8 | London | City | £17 per hour (mileage) | Housing Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225793478
title: Housing Support Worker
employer: 
location: City
region: London
salary: £17 per hour (mileage)
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 67a05af6339233ac43e279b5e0f9046a4fa1a8b8a349e7a00409fd8c47512e5c
---

---
action:
POSS | JobG8 | London | City | £90 - £110 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225775181
title: Learning Support Assistant
employer: 
location: City
region: London
salary: £90 - £110 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 2343f71d624c3849c26479078ef2e803e76963a86d05e5e5fe8e26670b5331df
---

---
action:
POSS | JobG8 | London | City | £16.11 - £17.11 per hour | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225827595
title: Learning Support Assistant
employer: 
location: City
region: London
salary: £16.11 - £17.11 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: cb434c5d772c4a399fabb0908dde06bbc1f373b0a0a0e92c0590ccd9ef0cf066
---

---
action:
POSS | JobG8 | London | City Of Westminster | £100 - £110 per daily | Behaviour Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225791285
title: Behaviour Support Worker
employer: 
location: City Of Westminster
region: London
salary: £100 - £110 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 53a71e4b36844e75ee31bee72892b56f30f113245809182c43774ef99156f710
---

---
action:
POSS | JobG8 | London | Croydon | £23 per hour | Interim Part Time Finance Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2298027
title: Interim Part Time Finance Assistant
employer: 
location: Croydon
region: London
salary: £23 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: finance assistant; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: bbef67224e51af6e099323d1faa8a94921e01e6764e302e65ff99f6a820fafb0
---

---
action:
POSS | JobG8 | London | Croydon | £100 - £115 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225810943
title: Learning Support Assistant
employer: 
location: Croydon
region: London
salary: £100 - £115 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: afc81fcc73400c77fbdad1d775b280e24ca1eca2a088f39a5fe976837c22b582
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
POSS | JobG8 | London | Edgware | £18 per hour | Care and Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225773100
title: Care and Support Worker
employer: 
location: Edgware
region: London
salary: £18 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 8267a25f3a45ac089dbd3822266f1b7145048cef498d70ebe051a5a95ddd2671
---

---
action:
POSS | JobG8 | London | Hackney | £90 - £120 per daily (depending on experience) | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225791199
title: Learning Support Assistant
employer: 
location: Hackney
region: London
salary: £90 - £120 per daily (depending on experience)
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: d2de45c99411c45a7eeb27f14679739a24c44260e4fa02367226b19134c3a2d7
---

---
action:
POSS | JobG8 | London | Hammersmith And Fulham | £101 - £120 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225800459
title: Learning Support Assistant
employer: 
location: Hammersmith And Fulham
region: London
salary: £101 - £120 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 61db4aee2a2f659af7993ee6450c3cddaec6bd2de85cc2ed2e86309816956029
---

---
action:
POSS | JobG8 | London | Harrow | — | Senior Finance Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2304930
title: Senior Finance Officer
employer: 
location: Harrow
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 5f8866220e91db5585952c2729f509a1f09894c723709e54bf0585cefb8fde61
---

---
action:
POSS | JobG8 | London | Islington | £25.39 per hour | LD - Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225830323
title: LD - Support Worker
employer: 
location: Islington
region: London
salary: £25.39 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: bf4bfac9dac10b55551d6dec31de074b0e0f9dd9f130e27556f6c54eaa32757d
---

---
action:
POSS | JobG8 | London | Islington | £18 - £20 per hour | Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225746326
title: Support Worker
employer: 
location: Islington
region: London
salary: £18 - £20 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 1fb8172f1fc909f235c42815fdce5f446190eee4a60a5012783c871f331dcfa2
---

---
action:
POSS | JobG8 | London | London | £100 - £110 per daily | Behaviour Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225811326
title: Behaviour Support Worker
employer: 
location: London
region: London
salary: £100 - £110 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: bf7334185de0548e8d0aa0f3f65ab6c29ea59750488201d952bfe9c35fcc3c06
---

---
action:
POSS | JobG8 | London | London | £30 - £40 per hour | Communication Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225784099
title: Communication Support Worker
employer: 
location: London
region: London
salary: £30 - £40 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 5d53172adf77c21871762ab91bfc3397bc141496211ddd3768a9c9d5fbcece92
---

---
action:
POSS | JobG8 | London | London | £45000 per year | customs clearance coordinator - Nights
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225822907
title: customs clearance coordinator - Nights
employer: 
location: London
region: London
salary: £45000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £45,000 exceeds regional review point £42,000
source_url: 
hub_fingerprint: c663270c870e8791b4dd16964a289b40907e6eaa1f8c257ac15bec09a80f6cb0
---

---
action:
POSS | JobG8 | London | London | £24 - £25 per hour | Early Years High Needs Co-ordinator - Education Qualified
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225792965
title: Early Years High Needs Co-ordinator - Education Qualified
employer: 
location: London
region: London
salary: £24 - £25 per hour
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: co-ordinator; manual review required: annualised upper salary £48,750 exceeds regional review point £42,000
source_url: 
hub_fingerprint: 0ee0de617f61b662608ae5d52eee3921adbc633f6fd9be990eb65942d8edf89c
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
POSS | JobG8 | London | London | £45000 - £50000 per year (Plus package) | Fieldview Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225798055
title: Fieldview Administrator
employer: 
location: London
region: London
salary: £45000 - £50000 per year (Plus package)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: d19a7e70f956a5a494b666edcb30b46687f7de98c39faaf079a7c799347fa074
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
POSS | JobG8 | London | London | — | Financial Controller Family/Founders Office
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2316704
title: Financial Controller Family/Founders Office
employer: 
location: London
region: London
salary: 
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: 1635c574185a2238d309d07066219c40a934d70ebff75d9e66fb4df1bdae7441
---

---
action:
POSS | JobG8 | London | London | £168 per daily | HR Administrator - Pre-Employment Checks & DBS
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225783285
title: HR Administrator - Pre-Employment Checks & DBS
employer: 
location: London
region: London
salary: £168 per daily
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: 441bbcd59499ccdec25e3e195c84967489349f3416b7577df3ac8cb007660388
---

---
action:
POSS | JobG8 | London | London | £50000 per year | HRIS Coordinator (Workday)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2212226
title: HRIS Coordinator (Workday)
employer: 
location: London
region: London
salary: £50000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £50,000 exceeds regional review point £42,000
source_url: 
hub_fingerprint: 2299cd0ec1605c1d532fce6d761940e27fb5e4de83766a3f854d07c24a50e5ce
---

---
action:
POSS | JobG8 | London | London | — | Human Resources Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2250856
title: Human Resources Manager
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 8fa340f683a27c59d475a8777842af91c5f1dccea9a85a301077815450d4f7a6
---

---
action:
POSS | JobG8 | London | London | £21 - £23 per hour | Interim Accounts Payable Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2163803
title: Interim Accounts Payable Assistant
employer: 
location: London
region: London
salary: £21 - £23 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: 37d3ea0f4034d39352adff2b0381cce54b619c180f341af58684e882bd6dba0f
---

---
action:
POSS | JobG8 | London | London | £93 - £115 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225791271
title: Learning Support Assistant
employer: 
location: London
region: London
salary: £93 - £115 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 39f104a57208043cf38e8cef8735ab7466508e7ccb717fac47746b0e4c06b977
---

---
action:
POSS | JobG8 | London | London | £24000 - £28000 per year | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225796743
title: Learning Support Assistant
employer: 
location: London
region: London
salary: £24000 - £28000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 14a03eb001a3187bdea575fbe918b320d38c2129caefb95beba60469f156a219
---

---
action:
POSS | JobG8 | London | London | £95 - £110 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225805893
title: Learning Support Assistant
employer: 
location: London
region: London
salary: £95 - £110 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 29d4070ade816dda192a0a1d92ddacf5227cdc0539b940e8ef09d10c59a2cf54
---

---
action:
POSS | JobG8 | London | London | £100 - £115 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225810916
title: Learning Support Assistant
employer: 
location: London
region: London
salary: £100 - £115 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 005d29deb1f13c242276376abc48d63ef0d97ff28cd1efcb12ad784510fc04b9
---

---
action:
POSS | JobG8 | London | London | £92.56 - £115 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225812225
title: Learning Support Assistant
employer: 
location: London
region: London
salary: £92.56 - £115 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 5c7613c95fd005beedf3b249099803fc870c4c935085a32697f387a16037149b
---

---
action:
POSS | JobG8 | London | London | £17.5 per hour | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225818434
title: Learning Support Assistant
employer: 
location: London
region: London
salary: £17.5 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: dc331170581dac2fb7fb03d1942d49a957d7ded750c03728b033b9b517ba8530
---

---
action:
POSS | JobG8 | London | London | — | Part Time Finance Manager / Financial Controller
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2307731
title: Part Time Finance Manager / Financial Controller
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: financial controller duties need specialist/seniority review; part-time earnings are unclear
source_url: 
hub_fingerprint: 5d31f14f1cff1e0330bbb52cbeb3c4d0bd52117ded65fccfb5266662765e6d41
---

---
action:
POSS | JobG8 | London | London | £42000 - £45000 per year | Part-time Bookkeeper
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2300516
title: Part-time Bookkeeper
employer: 
location: London
region: London
salary: £42000 - £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: bookkeeper; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: a1bc2721bed8e5b624f0402e4db266705458310cdea24a3cd46bfab2ed64dd3b
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
POSS | JobG8 | London | London | £160 - £175 per daily | Payroll Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225797989
title: Payroll Administrator
employer: 
location: London
region: London
salary: £160 - £175 per daily
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator, payroll administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: a897064e20e25ce28a62a2a1bf4f4cea7d9f5713747f303f2a4bb97771a131cd
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
POSS | JobG8 | London | London | £25.48 per hour | Receptionist
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225808013
title: Receptionist
employer: 
location: London
region: London
salary: £25.48 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - title register: high-confidence title pattern: receptionist; manual review required: Receptionist salary over £40k
source_url: 
hub_fingerprint: 673c4ba0cf7d935701e9e3e6230429502125d3c0b6f7b78ba6a42a3f1203c99b
---

---
action:
POSS | JobG8 | London | London | — | Senior Development Underwriter - Financial Institutions
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2298210
title: Senior Development Underwriter - Financial Institutions
employer: 
location: London
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 64c29f9ce3140317c670fb5ed563bbefb6f9d76b522aed060df2af0f5502b24d
---

---
action:
POSS | JobG8 | London | London | £50000 per year | Service Advisor Supervisor
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2251304
title: Service Advisor Supervisor
employer: 
location: London
region: London
salary: £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: service advisor; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: f6a0b5dc88c7bbd8bdbb1c4c7b835422afa0444953e5a4e9c74a26e2e5f7685e
---

---
action:
POSS | JobG8 | London | Newham | £92.56 - £115 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225812223
title: Learning Support Assistant
employer: 
location: Newham
region: London
salary: £92.56 - £115 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 52df29892f6fbf36745c32d69f2dfc6e1ae5d856d685f195f56ad26833e00358
---

---
action:
POSS | JobG8 | London | Newham | — | Senior Finance Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225828488
title: Senior Finance Officer
employer: 
location: Newham
region: London
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 78b2e8b3c340a4327b73470f0121bbdfc4e44e12cef506640273447d61233e45
---

---
action:
POSS | JobG8 | London | Romford | Competitive | Payroll Officer / Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225818607
title: Payroll Officer / Manager
employer: 
location: Romford
region: London
salary: Competitive
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: abac4d1762ac112f3903ad23c5842fbc363cb357b7c83b27b1ab5e2feb1921ba
---

---
action:
POSS | JobG8 | London | Sutton | £36000 - £40000 per year | Part Time Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2319441
title: Part Time Finance Manager
employer: 
location: Sutton
region: London
salary: £36000 - £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: c203a95dd556e2169fc7b37839260c6916187fe2888a5a870a848302b8a5048c
---

---
action:
POSS | JobG8 | London | Uxbridge | £45,000 per year | Executive Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225787273
title: Executive Assistant
employer: 
location: Uxbridge
region: London
salary: £45,000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-reviewed adverts confirm corporate executive office support; manual review required: annualised upper salary £45,000 exceeds regional review point £42,000
source_url: 
hub_fingerprint: d16935349b0b3de6122803161269f671e43fec5dd9de9462df42a55da3fafffe
---

---
action:
POSS | JobG8 | London | Uxbridge | £90 - £95 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225829443
title: Learning Support Assistant
employer: 
location: Uxbridge
region: London
salary: £90 - £95 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 6dc89645514e084eda7e21c30b993cf8d623be5ebb17cc7601e54213a3be2f50
---

---
action:
POSS | JobG8 | London | Wandsworth | £140 - £180 per daily | Communication Support Worker (BSL Level 6)
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225796819
title: Communication Support Worker (BSL Level 6)
employer: 
location: Wandsworth
region: London
salary: £140 - £180 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 6ae8cbf9d2c6245b38505235f3e02782af20478fef721e16465aa962ac7befe8
---

---
action:
POSS | JobG8 | Merseyside - Wirral | Birkenhead | £27000 - £30000 per year | Accounts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225767605
title: Accounts Administrator
employer: 
location: Birkenhead
region: Merseyside - Wirral
salary: £27000 - £30000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Basic accounts administration is transferable unless specialist qualifications are mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: e5623a9280ad1626db0faf7555047485c45380ea7d08e157784a0ebf787777f4
---

---
action:
POSS | JobG8 | Norfolk | Norfolk | — | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2338337
title: Finance Manager
employer: 
location: Norfolk
region: Norfolk
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: d348d2f62c1f686d7de60710e615adf8a5d30f7a79ed927a60bc5a80e2dfb3d5
---

---
action:
POSS | JobG8 | Norfolk | Norfolk | £29,542 per year | Office Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225801996
title: Office Manager
employer: 
location: Norfolk
region: Norfolk
salary: £29,542 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 1cb47777aef65f9a187cd090a1203b58eb4ae9d787b817f81c626607ec90261a
---

---
action:
POSS | JobG8 | North East - County Durham & Darlington/Hartlepool | Darlington | £15.58 per hour | Care Assistant - Bank - Care Home
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225818672
title: Care Assistant - Bank - Care Home
employer: 
location: Darlington
region: North East - County Durham & Darlington/Hartlepool
salary: £15.58 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 5f1fce8cd0b546e4d65cd151606fbfbe12dc0813054d4c413e9ebdacd973dd25
---

---
action:
POSS | JobG8 | North East - County Durham & Darlington/Hartlepool | Darlington | £12.85 per hour | Female Support Worker (Driver)
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 108314529
title: Female Support Worker (Driver)
employer: 
location: Darlington
region: North East - County Durham & Darlington/Hartlepool
salary: £12.85 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: d157e1311a7a5c551ed073e67250a9bee39792a81e464e87a9d481b2bf4e41b3
---

---
action:
POSS | JobG8 | North East - County Durham & Darlington/Hartlepool | Durham | £16 - £20 per hour (Mileage Paid if business insured) | Children and Family Support Worker Durham
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225805941
title: Children and Family Support Worker Durham
employer: 
location: Durham
region: North East - County Durham & Darlington/Hartlepool
salary: £16 - £20 per hour (Mileage Paid if business insured)
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 5dc209615ac2cb824e4e443262def0decdb5be7fb6d42a1b1dcfe0140cacbb90
---

---
action:
POSS | JobG8 | North East - County Durham & Darlington/Hartlepool | Durham | £95 - £110 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225817899
title: Learning Support Assistant
employer: 
location: Durham
region: North East - County Durham & Darlington/Hartlepool
salary: £95 - £110 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 6d04e303260f78042f6464dd39a1b0c6f47ed2919b5bbd8f9a68ccfe9454ebb9
---

---
action:
POSS | JobG8 | North East - County Durham & Darlington/Hartlepool | Peterlee | £13.6 - £17.55 per hour | Housing Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225611014
title: Housing Support Worker
employer: 
location: Peterlee
region: North East - County Durham & Darlington/Hartlepool
salary: £13.6 - £17.55 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 583a79a59718c55a878b7a1f9d74e10f1a22a988f1cd1a990df2cf123c17b14b
---

---
action:
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Cramlington | £110 - £130 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225830353
title: Learning Support Assistant
employer: 
location: Cramlington
region: North East - Tyneside, Wearside & Northumberland
salary: £110 - £130 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: f2e0ebedb6cd9593ce0aa1a93a0a592366497db1d061da5d3c3c210009f321dd
---

---
action:
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Newcastle Upon Tyne | £16 - £20 per hour (Mileage Paid if business insured) | Children and Families Support Worker Newcastle/Gateshead
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225803517
title: Children and Families Support Worker Newcastle/Gateshead
employer: 
location: Newcastle Upon Tyne
region: North East - Tyneside, Wearside & Northumberland
salary: £16 - £20 per hour (Mileage Paid if business insured)
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: f6a6d5d9416c3594f9075c312e8ad07c7473f45428f712d6aa5ee5d39859a93c
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
action:
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Newcastle Upon Tyne | £18 - £20 per hour | Recovery Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_222630684
title: Recovery Worker
employer: 
location: Newcastle Upon Tyne
region: North East - Tyneside, Wearside & Northumberland
salary: £18 - £20 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 54b4c2b2eeec3890751462bb4fc0828fafea2d192d53c3ba2ec05bba33748bae
---

---
action:
POSS | JobG8 | North East - Tyneside, Wearside & Northumberland | Tyne And Wear | competitive | Payroll Manager - Part Time
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2304646
title: Payroll Manager - Part Time
employer: 
location: Tyne And Wear
region: North East - Tyneside, Wearside & Northumberland
salary: competitive
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: a9fabb2ef54f3725cf5ae57aa2871bc04d6ed2857f2bbe8647da9ad5863a3c42
---

---
action:
POSS | JobG8 | North Scotland | Aberdeen | £38999 - £39000 per year | Supply Chain Data & Migration Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225800562
title: Supply Chain Data & Migration Coordinator
employer: 
location: Aberdeen
region: North Scotland
salary: £38999 - £39000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £39,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 21e2c2104b761b0c2b45d0a017d14a1829b701f7924917abffcb5618d9e94d2a
---

---
action:
POSS | JobG8 | North Scotland | Elgin | £40000 per year | Service Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108257604
title: Service Manager
employer: 
location: Elgin
region: North Scotland
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 271d2065b9352b08f5d63cc2d371671a92de0a2fb48e2a53472aad3848f51536
---

---
action:
POSS | JobG8 | North Scotland | Fraserburgh | £40000 per year | Service Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108258130
title: Service Manager
employer: 
location: Fraserburgh
region: North Scotland
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: f0d2efc0abd9c577bc86aa7f95ff2ab9822b589b3ef121de5b16c6ccf664427a
---

---
action:
POSS | JobG8 | North Scotland | Inverness | £40000 per year | Executive Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108314961
title: Executive Assistant
employer: 
location: Inverness
region: North Scotland
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-reviewed adverts confirm corporate executive office support; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: a6627289a8c32e734258a50ecf7a5a3cfa68c77d157d2c936b3dbb5919259ecf
---

---
action:
POSS | JobG8 | Nottinghamshire | Mansfield | £30500 - £32500 per year | Residential Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225777013
title: Residential Support Worker
employer: 
location: Mansfield
region: Nottinghamshire
salary: £30500 - £32500 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 8be2fafcef6b493479bb6b8d4e7e1813083696d8f402c182de31318c220e2b92
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
POSS | JobG8 | Nottinghamshire | Nottinghamshire | £115 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225803408
title: Learning Support Assistant
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: £115 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: ba16b0970e61f549eb0f8592c432fe9436a049a28d45732db3c9369e953a13e6
---

---
action:
POSS | JobG8 | Nottinghamshire | Nottinghamshire | £45000 - £50000 per year | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2263000
title: Payroll Manager
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: £45000 - £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: 0861726bf7f01b68c72952a38d093aba24d61f19cb5d2967b63c31076f9c9c3e
---

---
action:
POSS | JobG8 | Nottinghamshire | Nottinghamshire | £45000 - £50000 per year | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2300552
title: Payroll Manager
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: £45000 - £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: f4e4d15d43973f1074f9e09b3745fd27a02124b6a3f6ead42c9e444a21bae7d9
---

---
action:
POSS | JobG8 | Nottinghamshire | Nottinghamshire | £45000 - £50000 per year | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2308495
title: Payroll Manager
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: £45000 - £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: c2e910f60829cffb822c69a04f3c17dce96c3ac896ce7a8ce50d2586bd960f12
---

---
action:
POSS | JobG8 | Nottinghamshire | Nottinghamshire | £45000 - £50000 per year (plus benefits) | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225599921
title: Payroll Manager
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: £45000 - £50000 per year (plus benefits)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: 70c00435cca860fe09bfa70fce3952f500016937f8ca8165e38ae3c09fb2295f
---

---
action:
POSS | JobG8 | Nottinghamshire | Nottinghamshire | £45000 - £50000 per year | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225821161
title: Payroll Manager
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: £45000 - £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: 7f86f7ad9f282716d5a116813b419c210a4a837e534372351f4787fddfa85ebe
---

---
action:
POSS | JobG8 | Nottinghamshire | Nottinghamshire | £23.07 - £25.64 per hour (2 days in office) | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225826003
title: Payroll Manager
employer: 
location: Nottinghamshire
region: Nottinghamshire
salary: £23.07 - £25.64 per hour (2 days in office)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: 7edc62edb346837c0435476c207bb519b85f1643dca75ee3b89aeb5032ecfa4d
---

---
action:
POSS | JobG8 | Oxfordshire | Oxford | £18.50 per hour | Healthcare Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225831481
title: Healthcare Assistant
employer: 
location: Oxford
region: Oxfordshire
salary: £18.50 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: b98422e22354bf105a82a82dc7ecea839cf6841ef7dae56f381e0f3fae997ebe
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
POSS | JobG8 | Oxfordshire | Oxfordshire | £19.12 per hour (PAYE or 25.58 Umbrella) | Facilities Co-ordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108303136
title: Facilities Co-ordinator
employer: 
location: Oxfordshire
region: Oxfordshire
salary: £19.12 per hour (PAYE or 25.58 Umbrella)
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: co-ordinator; manual review required: annualised upper salary £37,284 exceeds regional review point £37,000
source_url: 
hub_fingerprint: be7c61672af9c1b5b357df4ce55b78fd778ed432c0474849bd4922529901eb90
---

---
action:
POSS | JobG8 | Scotland Central - Edinburgh & Lothians | Edinburgh | £36000 - £39000 per year | Finance Analyst (12-month Fixed Term Contract)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2312031
title: Finance Analyst (12-month Fixed Term Contract)
employer: 
location: Edinburgh
region: Scotland Central - Edinburgh & Lothians
salary: £36000 - £39000 per year
closing_date: 
reason: possible manual_select candidate for review/swap
source_url: 
hub_fingerprint: b37f0a79bc6c75c18245e396bb71b9763180d72c6d59deed7fbde0f1897ac6c7
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
POSS | JobG8 | Scotland West - Glasgow | Glasgow | £40000 per year | Service Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108276039
title: Service Manager
employer: 
location: Glasgow
region: Scotland West - Glasgow
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 1dc3559c734c060b08766921b8f854c1e439ef14e7511e80a8da07b5d4dc7b87
---

---
action:
POSS | JobG8 | Somerset | Somerset | £20 - £25 per hour | Payroll Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225793456
title: Payroll Coordinator
employer: 
location: Somerset
region: Somerset
salary: £20 - £25 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: payroll coordinator; manual review required: annualised upper salary £48,750 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 615f6dde44eac7c7ff2da6991bc61ed50d2c07b97acc3995a12f3e17b1c39deb
---

---
action:
POSS | JobG8 | Somerset | Somerset | £22 per hour | Project Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225830835
title: Project Administrator
employer: 
location: Somerset
region: Somerset
salary: £22 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - title register: high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: fd62425abe86b0712329ebb8402aa880fe8f6fa4d89b07261a533674f2292113
---

---
action:
POSS | JobG8 | Suffolk | Suffolk | £40000 - £50000 per year | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2171238
title: Finance Manager
employer: 
location: Suffolk
region: Suffolk
salary: £40000 - £50000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 29206c2d4d3fb3be2d327145f156437d3d5ba980a9d5140e3a138925a2c83de1
---

---
action:
POSS | JobG8 | Suffolk | Suffolk | — | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2312466
title: Finance Manager
employer: 
location: Suffolk
region: Suffolk
salary: 
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: f31eaa513a179ad21eaaad93955ba90870c96f192e29fc42e6f6b2daf85f1529
---

---
action:
POSS | JobG8 | Surrey | Knaphill | £18 - £20 per hour | Children's Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225844588
title: Children's Support Worker
employer: 
location: Knaphill
region: Surrey
salary: £18 - £20 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: f0bca91effecec93b29e1ab6edd157d2615a4486dfeba256ae3e50b3ccae3132
---

---
action:
POSS | JobG8 | Surrey | Knaphill | £18.5 - £20.5 per hour | Waking Night Support Worker GU22
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225812877
title: Waking Night Support Worker GU22
employer: 
location: Knaphill
region: Surrey
salary: £18.5 - £20.5 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 202f9e3cba454ca2a27de072673a7f4394168a3feb0c8b424cbee8c307e9edbb
---

---
action:
POSS | JobG8 | Surrey | Redhill | £30000 - £31000 per year | Housing Support Officer
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225828819
title: Housing Support Officer
employer: 
location: Redhill
region: Surrey
salary: £30000 - £31000 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 8bcca6ea9199c1de8966155cde91810fe25266e72b2620188e56c87fa940a096
---

---
action:
POSS | JobG8 | Surrey | Reigate | £95 - £100 per daily | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225800217
title: Learning Support Assistant
employer: 
location: Reigate
region: Surrey
salary: £95 - £100 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 49877bd54a094dbbe8a6dc86b88135345a22bdd00421c3dd9167132ea9f745fe
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
POSS | JobG8 | Surrey | Surrey | £20 - £22 per hour (Pension,parking) | Financial Services Income Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225769320
title: Financial Services Income Manager
employer: 
location: Surrey
region: Surrey
salary: £20 - £22 per hour (Pension,parking)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: d2ae3e57d1655c8b0e668b6828b6493d3c78bd61fab990661fe0f51d405cf769
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
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-approved only for explicit executive or office PA descriptions; direct-care and legal PA work stays excluded; agreed context rule satisfied; manual review required: annualised upper salary £50,000 exceeds regional review point £42,000
source_url: 
hub_fingerprint: e10e13669390d42ed467fd8c385c396825d98587c70e3f1b0d6b6a65516265e9
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
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-approved only for explicit executive or office PA descriptions; direct-care and legal PA work stays excluded; agreed context rule satisfied; manual review required: annualised upper salary £50,000 exceeds regional review point £42,000
source_url: 
hub_fingerprint: 526cf9d583080af82cf77e9d59c856e1ec3df71161dd7c933107e79a11f2c8c0
---

---
action:
POSS | JobG8 | Sussex | Eastbourne | £21 - £23 per hour | Recovery Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225810561
title: Recovery Worker
employer: 
location: Eastbourne
region: Sussex
salary: £21 - £23 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: b168b8b70677a178026017019de141beece104c6a200c2329ff94a3b9ab7e523
---

---
action:
POSS | JobG8 | Sussex | Sussex | £19966 - £20606 per year | Learning Support Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225798181
title: Learning Support Assistant
employer: 
location: Sussex
region: Sussex
salary: £19966 - £20606 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: fd42a81729ab3411223591178007dc428b6cab4d6180e23ec48a034141be05a3
---

---
action:
POSS | JobG8 | Sussex | Sussex | £47,000 per year (FTE) | Payroll Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2307873
title: Payroll Officer
employer: 
location: Sussex
region: Sussex
salary: £47,000 per year (FTE)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: 802b296b8fdd79d33ddffc532cf2cbcd5b8e7a9d85a29d909e6f9a151e1be01b
---

---
action:
POSS | JobG8 | Sussex | Sussex | £47000 per year (pro rata for 3 days) | Payroll Officer
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225826910
title: Payroll Officer
employer: 
location: Sussex
region: Sussex
salary: £47000 per year (pro rata for 3 days)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: a199643507c53b0de1a5b7aac8d62658d1389bedb6809da7c2d7b2df82a464c5
---

---
action:
POSS | JobG8 | Wales South - Cardiff & Vale | Cardiff | Dependent on experience | Payroll Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225778100
title: Payroll Manager
employer: 
location: Cardiff
region: Wales South - Cardiff & Vale
salary: Dependent on experience
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time earnings are unclear
source_url: 
hub_fingerprint: 4cfed8dc1001f71569a33c60749beb5f3b286a81e25eb628e1d2ed43bea88efc
---

---
action:
POSS | JobG8 | Wales South - Gwent | Newport | £40000 per year | Retail Marketing Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2296700
title: Retail Marketing Coordinator
employer: 
location: Newport
region: Wales South - Gwent
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 2036c4d239857c76ded7503b9eb0b2b204cf0274297b4fe24356144b631c40b0
---

---
action:
POSS | JobG8 | Wales South - Gwent | Rogerstone | £19.16 per hour | Administrative Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225829957
title: Administrative Assistant
employer: 
location: Rogerstone
region: Wales South - Gwent
salary: £19.16 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - title register: high-confidence title pattern: administrative assistant; manual review required: annualised upper salary £37,362 exceeds regional review point £37,000
source_url: 
hub_fingerprint: a34655e66314289424097c11effae49d79cd912d7e044d23f4b19d1ec1c5d60b
---

---
action:
POSS | JobG8 | Wales South - Gwent | Usk | £21 - £24.2 per hour | Senior Finance Business Partner
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225829232
title: Senior Finance Business Partner
employer: 
location: Usk
region: Wales South - Gwent
salary: £21 - £24.2 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: actual part-time annual earnings over £40k
source_url: 
hub_fingerprint: 7c01cc54e14bc53b34b9ba21bb22eac963082b68b27bcc71377c1f4f640c4b73
---

---
action:
POSS | JobG8 | Wales South - Swansea Bay | Bridgend | £15.75 per hour | Accounts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2298988
title: Accounts Administrator
employer: 
location: Bridgend
region: Wales South - Swansea Bay
salary: £15.75 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Basic accounts administration is transferable unless specialist qualifications are mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: 89d2eb593725803c90cf199f0a8eba64a000ca30e652789ab597f9d7a73457c1
---

---
action:
POSS | JobG8 | Wales South - Swansea Bay | Bridgend | £15.75 per hour | Accounts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225820308
title: Accounts Administrator
employer: 
location: Bridgend
region: Wales South - Swansea Bay
salary: £15.75 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Basic accounts administration is transferable unless specialist qualifications are mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: 6fb97d66025fb39a04b441c1ea36c76d309ebbb57f5598c00bafe721576a5866
---

---
action:
POSS | JobG8 | Wales South - Swansea Bay | Bridgend | £35000 - £40000 per year (excellent benefits) | Office Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225800333
title: Office Manager
employer: 
location: Bridgend
region: Wales South - Swansea Bay
salary: £35000 - £40000 per year (excellent benefits)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 1067627e632d11fba5c21c5c40b8ef004eefea530a0f845532d98d4f30224ed1
---

---
action:
POSS | JobG8 | Wales South - Swansea Bay | Port Talbot | £27495 per year | Logistics Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225828428
title: Logistics Administrator
employer: 
location: Port Talbot
region: Wales South - Swansea Bay
salary: £27495 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Logistics administration is eligible unless specialist logistics expertise is mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: 884b85675a004c621b1824dd99606af833e2d61c45e50be5b064573d647d0105
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
reason: manual review required: title classification: HIGH_CONFIDENCE - Owner-reviewed adverts confirm corporate executive office support; manual review required: annualised upper salary £50,000 exceeds regional review point £42,000
source_url: 
hub_fingerprint: e2db3649d33586b7c079548223c46e2a518d156192e5d4c43afffd710e8a7c37
---

---
action:
POSS | JobG8 | West Midlands - Black Country | Wednesbury | £40,000 per year | Light Rail Fleet Planner
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225745718
title: Light Rail Fleet Planner
employer: 
location: Wednesbury
region: West Midlands - Black Country
salary: £40,000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: planner; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: da552ebc655296d855ab6cbc9dfb215627cfaf67ed3e548c2926e2091822bad7
---

---
action:
POSS | JobG8 | West Midlands - Black Country | West Bromwich | £45,000 per year (FTE) | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2328412
title: Finance Manager
employer: 
location: West Bromwich
region: West Midlands - Black Country
salary: £45,000 per year (FTE)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: dd330134104089cbd9f987cf60f1b1ea656610a784b73399242e29224c95d736
---

---
action:
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | £28,000 - £32,000 per year | Accounts Administrator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2304291
title: Accounts Administrator
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: £28,000 - £32,000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - Basic accounts administration is transferable unless specialist qualifications are mandatory; manual review required: description appears to make specialist qualifications or substantial prior experience mandatory
source_url: 
hub_fingerprint: 58c24b665b7c8214e0e3d4d3513d351c6e6639ab31033f527ad91acef373ec3d
---

---
action:
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | £40000 per year | Accounts Assistant
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2310650
title: Accounts Assistant
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: accounts assistant; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: e27221fe69f21728def832b4c31276bb4927d81434ef6242c2e34576f25a102a
---

---
action:
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | £20 - £23 per hour | Credit Controller
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2313027
title: Credit Controller
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: £20 - £23 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: credit controller; manual review required: annualised upper salary £44,850 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 8ed992e247dd7d07196567155150382cb11ef59b52d80cc56860e606497f8e6d
---

---
action:
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | £40000 per year | Credit Controller
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2330740
title: Credit Controller
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: credit controller; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 8f1d0b5909120a427807d58145db4fc6ef425d2d5749b32da08e738f3a2bad84
---

---
action:
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | £21 per hour | Customer Service Support Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225787869
title: Customer Service Support Coordinator
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: £21 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: customer service support; manual review required: annualised upper salary £40,950 exceeds regional review point £37,000
source_url: 
hub_fingerprint: a5ee9b5e3857e6560a38f5c31871cfa94d095f415be924c0607f81d0f30b5ed4
---

---
action:
POSS | JobG8 | West Midlands - Coventry & Warwickshire | Warwickshire | £45000 per year | Group Credit Controller
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2211441
title: Group Credit Controller
employer: 
location: Warwickshire
region: West Midlands - Coventry & Warwickshire
salary: £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: credit controller; manual review required: annualised upper salary £45,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 8796ba834dd298e78166c2f0562ecb378b397e3a5962b651699bae3a62a9b24c
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
POSS | JobG8 | Wiltshire | Salisbury | £26200 per year | Housing Support Worker
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225821606
title: Housing Support Worker
employer: 
location: Salisbury
region: Wiltshire
salary: £26200 per year
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 369923641a0960768dc839bec5a782824dfc36eb873139231fce3e1cb297338f
---

---
action:
POSS | JobG8 | Wiltshire | Salisbury | £92 - £100 per daily | Learning support assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225775965
title: Learning support assistant
employer: 
location: Salisbury
region: Wiltshire
salary: £92 - £100 per daily
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 8dc07add9c6c94bddce78723672a99401f135ec1b47d8a1c44dd51db3e275b1f
---

---
action:
POSS | JobG8 | Worcestershire | Worcestershire | £40000 per year | Retail Marketing Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2296702
title: Retail Marketing Coordinator
employer: 
location: Worcestershire
region: Worcestershire
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: ELASTIC_FIT - elastic-fit title pattern: coordinator; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: c8fc1c2b63dbfdda51325230c72d5f720ca357c39ee6749c0b40de652f4ca931
---

---
action:
POSS | JobG8 | Yorkshire - North | Harrogate | £45000 per year | Credit Controller
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108320734
title: Credit Controller
employer: 
location: Harrogate
region: Yorkshire - North
salary: £45000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: credit controller; manual review required: annualised upper salary £45,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: c760ac93be4556fe10ae31bb4e172a95f927469fa4cd64b39d84f59e6967b017
---

---
action:
POSS | JobG8 | Yorkshire - North | Harrogate | £40000 per year | Credit Controller (Debt Recovery)
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108326695
title: Credit Controller (Debt Recovery)
employer: 
location: Harrogate
region: Yorkshire - North
salary: £40000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: credit controller; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: c4030ec6c88257b18e7ddb02b53d91a4867fdacc20bb4b486a1f30a618d5bc34
---

---
action:
POSS | JobG8 | Yorkshire - North | Scarborough | £40,000 per year | Value Stream Scheduler
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 108283303
title: Value Stream Scheduler
employer: 
location: Scarborough
region: Yorkshire - North
salary: £40,000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: scheduler; manual review required: annualised upper salary £40,000 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 4ec8b2650cd76bc8dd42c8e70ddf4df0f4bfff75c05031f6e7ba6c8a8ee98d61
---

---
action:
POSS | JobG8 | Yorkshire - South | Doncaster | £15.75 per hour | Care Assistant
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225826966
title: Care Assistant
employer: 
location: Doncaster
region: Yorkshire - South
salary: £15.75 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 915cc915934913b7640cd38087b3e63b772cace5ab5ccf4a4b23ae654a7714f6
---

---
action:
POSS | JobG8 | Yorkshire - West | Bradford | £25 per hour | Highways Technical Administrator - Section 278 / Section 38
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225827271
title: Highways Technical Administrator - Section 278 / Section 38
employer: 
location: Bradford
region: Yorkshire - West
salary: £25 per hour
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: administrator; manual review required: Office/finance role salary over £40k
source_url: 
hub_fingerprint: aca5a5871710051e57d5fa012f272ac6ac1ed416b00ae28227a17764c18b1970
---

---
action:
POSS | JobG8 | Yorkshire - West | Bradford | £18 - £19 per hour | Housing Support Officer
source_key: jobg8
source: JobG8
category: support_worker
source_job_id: 23643_225817936
title: Housing Support Officer
employer: 
location: Bradford
region: Yorkshire - West
salary: £18 - £19 per hour
closing_date: 
reason: JobG8 selector marked this vacancy POSS
source_url: 
hub_fingerprint: 349f051ff8674a5ed87583b152444de508e09362b816dd057ce42eab2e9a5b17
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
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 68ac2c94cd5b1cb1ba0bd3de799a9d198e7be651ce9641fec48a250e79ca7513
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
POSS | JobG8 | Yorkshire - West | Ilkley | £45,000 - £50,000 per year (FTE) | Finance Manager
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2319200
title: Finance Manager
employer: 
location: Ilkley
region: Yorkshire - West
salary: £45,000 - £50,000 per year (FTE)
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: part-time manager role requires owner review
source_url: 
hub_fingerprint: 838c792db00f1fac2391e76838d6ee57b3012587ad6675ec5d7f5bc09e57ec96
---

---
action:
POSS | JobG8 | Yorkshire - West | Leeds | £41869 per year | Bus Service Coordinator
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 23643_225807355
title: Bus Service Coordinator
employer: 
location: Leeds
region: Yorkshire - West
salary: £41869 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - high-confidence title pattern: service coordinator; manual review required: annualised upper salary £41,869 exceeds regional review point £37,000
source_url: 
hub_fingerprint: 044c95a54817886f31d5ff58307cfa16fe774b2e4d8720687474b28151c2df28
---

---
action:
POSS | JobG8 | Yorkshire - West | Leeds | £43000 per year | Payroll Team Leader
source_key: jobg8
source: JobG8
category: admin_service
source_job_id: 2305440
title: Payroll Team Leader
employer: 
location: Leeds
region: Yorkshire - West
salary: £43000 per year
closing_date: 
reason: manual review required: title classification: HIGH_CONFIDENCE - explicit part-time finance role rule; manual review required: salary over £40k under normal selection rules
source_url: 
hub_fingerprint: 79ac810f4c4a213f8fbba635cba03f07b9f2f7c09401c5fd9b13412a631c797f
---
