# VONNE ETL proof-of-concept review

review_date: 2026-09-05
review_fingerprint: 7061a2ea4cb06c56d00249d0def5f029ff385bd4a848f7b6422fa81def19eb44

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are same-day only and do not publish anything.

Run generated: 2026-09-05T13:11:50+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 275
Approved NEJobs comparison rows: 19

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 5
- Detail pages fetched successfully: 5
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 10
- Tees Valley explicitly excluded: 1
- Outside or unmapped geography excluded: 0
- Generic/derived geography rows requiring review: 1
- Retained target candidates: 14

## Outcomes
- HC: 0
- POSS: 8
- HARD_PASS: 6
- Final selected after same-day actions: 5
- Final POSS awaiting decision: 2
- Manually excluded: 1

## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

---
action: select
SELECTED | North East | Hybrid | £ Per Annum | Project Development Co-ordinator
employer: National Energy Action
closing_date: 17 September 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173385
vacancy_fingerprint: 8c5d0bc5abb7a5c5bfb5d8f4fff9916e89cc3ec5fe45d71db4a8e141e12b0c66
source_job_id: 173385
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173385
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
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £23,370 to 23,790 | Receptionist
employer: Foundation of Light
closing_date: Friday, September 11, 2026 - 00:00
geography: CONFIRMED — location: approved location fallback
reason: possible cross-source duplicate requires review
source: VONNE
tracking_key: vonne-173374
vacancy_fingerprint: 6f57a4f078d03479daa7126537cb9614a4fe68d8551b871ecea57b2098e876d8
source_job_id: 173374
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173374
---

---
action: select
SELECTED | North East - Tyneside, Wearside & Northumberland | Northumberland | £30,075 Per Annum | Womens Specialist ISC Coach
employer: Changing Lives
closing_date: 16 September 2026
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £30,075 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173392
vacancy_fingerprint: 2ac04f9f1b86a7905bf4d7895c084339bc6730bbe03f168a8617ef240daa2e23
source_job_id: 173392
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173392
---

---
action: select
SELECTED | North East - Tyneside, Wearside & Northumberland | Northumberland | £30,075 Pro Rata | Womens Specialist ISC Coach - Part Time
employer: Changing Lives
closing_date: 16 September 2026
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £30,075 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173391
vacancy_fingerprint: 52bd0af4f0d255daf201e0884581ed4ac54cde52049d930ddc0326b8686e6857
source_job_id: 173391
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173391
---


## POSS — choose SELECT or EXCLUDE

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | County Durham | £24,454 Per Annum | Administrator (26.13)
employer: Age UK County Durham
closing_date: Wednesday, September 30, 2026 - 12:00
geography: CONFIRMED — location: approved location fallback
reason: possible cross-source duplicate requires review
source: VONNE
tracking_key: vonne-173394
vacancy_fingerprint: 519ce27938398f49fcbce718a2199f9949683fdc41baa95ab1c29252c8391d66
source_job_id: 173394
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173394
---

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | County Durham | £24,454 Per Annum | Project Administrator (26.12)
employer: Age UK County Durham
closing_date: Wednesday, September 30, 2026 - 12:00
geography: CONFIRMED — location: approved location fallback
reason: possible cross-source duplicate requires review
source: VONNE
tracking_key: vonne-173393
vacancy_fingerprint: 076c2df7b5819c647117c3b816981009bb4a7072315f7abc14f5c71d30a5e73b
source_job_id: 173393
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173393
---


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


## HARD_PASS

- [Chief Executive Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173376) — out-of-scope VONNE occupation.
- [Gardening and Handyperson Supervisor](https://www.vonne.org.uk/vonne-jobs-details?cid=173184) — insufficient service-admin evidence.
- [NEYA Trainee Youth Voice Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173381) — out-of-scope VONNE occupation.
- [Part time Play & Youth Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173388) — out-of-scope VONNE occupation.
- [Stock Controller](https://www.vonne.org.uk/vonne-jobs-details?cid=173378) — insufficient service-admin evidence.
- [Support Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=172597) — out-of-scope VONNE occupation.

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
