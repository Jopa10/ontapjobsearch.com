# VONNE ETL proof-of-concept review

review_date: 2026-09-10
review_fingerprint: 05d9ae8b894555be5716d7ec7a6ca64ce8b1f8df76443d55f29a4a3a20c3c289

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-09-10T12:42:15+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 255
Approved NEJobs comparison rows: 13

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 7
- Detail pages fetched successfully: 7
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 8
- Tees Valley explicitly excluded: 0
- Outside or unmapped geography excluded: 2
- Generic/derived geography rows requiring review: 0
- Retained target candidates: 13

## Outcomes
- HC: 0
- POSS: 8
- HARD_PASS: 5
- Final selected after remembered/manual actions: 2
- Final POSS awaiting decision: 3
- Manually excluded: 3
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

- None.

## POSS — choose SELECT or EXCLUDE

---
action: exclude
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
POSS | North East - County Durham & Darlington/Hartlepool | County Durham | £27,476 Per Annum | HR Administrator
employer: Durham Cathedral
closing_date: Friday, October 2, 2026 - 09:00
geography: CONFIRMED — location: approved location fallback
reason: transferable title with specialist or borderline wording: hr
source: VONNE
tracking_key: vonne-173410
vacancy_fingerprint: f65f0813d779a37799fe069207dcaadc4a3b07e03f174b525fb8ad7176d32b76
source_job_id: 173410
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173410
---
---
action: exclude
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
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Regionwide | £16,393 Per Annum | Community Engagement Officer
employer: West End Refugee Service
closing_date: Sunday, October 4, 2026 - 23:59
geography: CONFIRMED — based: exact area
reason: provisional transferable-office review
source: VONNE
tracking_key: vonne-173396
vacancy_fingerprint: c3cd68a07de16db765d401e6c8582cc80135e96b6fd57c8ec1f681d259c96e10
source_job_id: 173396
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173396
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Northumberland | £29,998 to 33,000 Per Annum | Community Transport Network and Operations Development Coordinator
employer: WATBUS (Community Transport)
closing_date: Monday, September 21, 2026 - 12:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £33,000 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173398
vacancy_fingerprint: f0aa4caa78e6f26eca1fba4fcba8da7a9759467a67e7607e373092401816c500
source_job_id: 173398
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173398
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £34,434 to 36,363 Per Annum | Health & Wellbeing Coordinator
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
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £26,402 to 28,141 Per Annum | Health & Wellbeing Projects Support Officer
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
POSS | North East - Tyneside, Wearside & Northumberland | Northumberland | £30,075 Per Annum | Womens Specialist ISC Coach
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
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Marketing and Communications Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173409) — insufficient service-admin evidence.
- [Right Turn Case Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173406) — out-of-scope VONNE occupation.
- [Safe Accommodation Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173405) — out-of-scope VONNE occupation.
- [Support Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=172597) — out-of-scope VONNE occupation.
- [Support Worker - Housing First Project Gateshead](https://www.vonne.org.uk/vonne-jobs-details?cid=171329) — confirmed JobG8 duplicate.

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
