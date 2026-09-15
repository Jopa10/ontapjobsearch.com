# VONNE ETL proof-of-concept review

review_date: 2026-09-15
review_fingerprint: b21ce9f9063c5a0b77198f3b970de07d78c14574fabae41892e0253b76aa4301

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-09-15T12:59:46+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 367
Approved NEJobs comparison rows: 10

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 4
- Detail pages fetched successfully: 4
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 11
- Tees Valley explicitly excluded: 0
- Outside or unmapped geography excluded: 3
- Generic/derived geography rows requiring review: 0
- Retained target candidates: 12

## Outcomes
- HC: 0
- POSS: 4
- HARD_PASS: 8
- Final selected after remembered/manual actions: 0
- Final POSS awaiting decision: 3
- Manually excluded: 1
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
closing_date: Tuesday, September 22, 2026 - 12:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £33,000 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173398
vacancy_fingerprint: 5113c142a6e91ff41d8e8d98644536cd0018f128d39996978e7820eaf9dc9817
source_job_id: 173398
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173398
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Administration Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173413) — insufficient service-admin evidence.
- [Marketing and Communications Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173409) — insufficient service-admin evidence.
- [Money Advice/Debt Caseworker](https://www.vonne.org.uk/vonne-jobs-details?cid=173416) — out-of-scope VONNE occupation.
- [Recovery Navigator](https://www.vonne.org.uk/vonne-jobs-details?cid=173414) — insufficient service-admin evidence.
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
