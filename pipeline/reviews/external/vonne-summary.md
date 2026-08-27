# VONNE ETL proof-of-concept review

review_date: 2026-08-27
review_fingerprint: b5cbb5ea11cc52d40a31ab6d72464f4f8dbabf1d2dc70859778a8c2e2d76c4a2

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are same-day only and do not publish anything.

Run generated: 2026-08-27T11:36:41+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 252
Approved NEJobs comparison rows: 30

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 4
- Detail pages fetched successfully: 4
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 11
- Tees Valley explicitly excluded: 0
- Outside or unmapped geography excluded: 1
- Generic/derived geography rows requiring review: 3
- Retained target candidates: 14

## Outcomes
- HC: 0
- POSS: 6
- HARD_PASS: 8
- Final selected after same-day actions: 4
- Final POSS awaiting decision: 0
- Manually excluded: 2

## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

---
action: select
SELECTED | North East | Regionwide | £30,150 Per Annum | Housing Support Officer
employer: Handcrafted
closing_date: Tuesday, September 1, 2026 - 17:00
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173358
vacancy_fingerprint: bc1c2200fdc8dcfa64f31abb48d4a2d0d40df53ed9b1bdd1bf5d91948b802f74
source_job_id: 173358
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173358
---

---
action: select
SELECTED | North East - County Durham & Darlington/Hartlepool | Hybrid | £31,500 Pro Rata | Trusts and Community Fundraising Officer
employer: Durham County Carers Support
closing_date: 25 September 2026
geography: DERIVED_REVIEW — employer-derived geography: area found in address: durham
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173349
vacancy_fingerprint: 11f227685f5e3a482053104d6ecbb8156ab3f437a2d893c21e97e1500a6be808
source_job_id: 173349
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173349
---

---
action: select
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £26,402 to 28,141 Per Annum | Health & Wellbeing Projects Support Officer
employer: VONNE
closing_date: Sunday, September 13, 2026 - 00:00
geography: CONFIRMED — location: approved location fallback
reason: provisional transferable-office review
source: VONNE
tracking_key: vonne-173310
vacancy_fingerprint: 8a7ab286013372c433a61a3c5bcaad36cea77bc6812442d255b413a5866b6bce
source_job_id: 173310
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173310
---

---
action: select
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £25,334 to 26,419 Per Annum | Marketing Coordinator
employer: Age UK North Tyneside
closing_date: Wednesday, September 2, 2026 - 12:00
geography: CONFIRMED — location: approved location fallback
reason: provisional transferable-office review
source: VONNE
tracking_key: vonne-173347
vacancy_fingerprint: 5ffc42da06b53f655acf29768aa1d1b990d1701bd3b16f82985d7f2b2005e8dd
source_job_id: 173347
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173347
---


## POSS — choose SELECT or EXCLUDE

- None.

## EXCLUDED BY REVIEW

---
action: exclude
EXCLUDED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £34,434 to 36,363 Per Annum | Health & Wellbeing Coordinator
employer: VONNE
closing_date: Sunday, September 13, 2026 - 00:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £36,363 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173309
vacancy_fingerprint: 25bce1025449c1002f480b7b77769ff54b70b170d8a01bd59a5f484ec7758404
source_job_id: 173309
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173309
---

---
action: exclude
EXCLUDED | North East - Tyneside, Wearside & Northumberland | Newcastle | £34,625 Per Annum | Project Lead
employer: Changing Lives
closing_date: 09 September 2026
geography: CONFIRMED — location: exact area
reason: transferable title with specialist or borderline wording: lead
source: VONNE
tracking_key: vonne-173363
vacancy_fingerprint: 2b3c14a2b6daf54c403013deddf082d852b216bd0f345f8373fe1b1a1bdf2c8d
source_job_id: 173363
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173363
---


## HARD_PASS

- [Experienced & Trainee Telephone Debt Caseworker](https://www.vonne.org.uk/vonne-jobs-details?cid=173346) — out-of-scope VONNE occupation.
- [Facilities and Compliance Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173354) — out-of-scope VONNE occupation.
- [Families Advice and Support Team Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173348) — out-of-scope VONNE occupation.
- [Gardening and Handyperson Supervisor](https://www.vonne.org.uk/vonne-jobs-details?cid=173184) — insufficient service-admin evidence.
- [Project Worker: Disability Heritage in North Tyneside: The NTDF Story](https://www.vonne.org.uk/vonne-jobs-details?cid=173231) — out-of-scope VONNE occupation.
- [Temporary Centre Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173361) — out-of-scope VONNE occupation.
- [Welfare Benefits Advisor](https://www.vonne.org.uk/vonne-jobs-details?cid=172790) — insufficient service-admin evidence.
- [Young Carer Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173355) — out-of-scope VONNE occupation.

## Safety boundary
- The script writes CSV and Markdown review outputs only.
- There is no command-line option or function that writes approved or live JSON.
- It does not change `pipeline/output-external`, `pipeline/output-admin-service`, `app`, or existing workflows.
- Only factual fields are retained; full VONNE role descriptions are not stored.
- Source attribution remains `VONNE`, with stable `vonne-<cid>` tracking keys and original source URLs.
- VONNE's website terms prohibit unauthorised reproduction; this POC is intentionally bounded and review-only.
- Generic `Hybrid`, `Home-based` and `Regionwide` locations are forced to POSS unless a target geography is confirmed.
- Tees Valley wording is explicitly excluded using Ontap's existing North East rules.
- Monday/Thursday operation is not scheduled in this POC; it can be aligned later if the review proves reliable.
