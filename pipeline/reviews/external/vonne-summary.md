# VONNE ETL proof-of-concept review

review_date: 2026-09-16
review_fingerprint: 475d5587c9755898de73017277a5bc0b5e5398502047a4ddfa2f77455515fec7

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-09-16T12:56:42+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 306
Approved NEJobs comparison rows: 10

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 2
- Detail pages fetched successfully: 2
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 13
- Tees Valley explicitly excluded: 1
- Outside or unmapped geography excluded: 3
- Generic/derived geography rows requiring review: 0
- Retained target candidates: 11

## Outcomes
- HC: 0
- POSS: 3
- HARD_PASS: 8
- Final selected after remembered/manual actions: 0
- Final POSS awaiting decision: 3
- Manually excluded: 0
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

- None.

## POSS — choose SELECT or EXCLUDE

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
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £ Per Annum | Support Worker - Young People's 16+ Supported Accommodation - Gateshead
employer: Oasis Community Housing
closing_date: 30 September 2026
geography: CONFIRMED — location: exact area
reason: possible cross-source duplicate requires review
source: VONNE
tracking_key: vonne-171330
vacancy_fingerprint: 45a5414b40fbfeff791b6b1d7a1c75f8d886794387d67eee5bf61d48a68f5960
source_job_id: 171330
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=171330
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Administration Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173413) — insufficient service-admin evidence.
- [Community Cancer Awareness Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173418) — out-of-scope VONNE occupation.
- [Community Link Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173419) — out-of-scope VONNE occupation.
- [Marketing and Communications Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173409) — insufficient service-admin evidence.
- [Money Advice/Debt Caseworker](https://www.vonne.org.uk/vonne-jobs-details?cid=173416) — out-of-scope VONNE occupation.
- [Recovery Navigator](https://www.vonne.org.uk/vonne-jobs-details?cid=173414) — insufficient service-admin evidence.
- [Right Turn Case Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173406) — out-of-scope VONNE occupation.
- [Safe Accommodation Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173405) — out-of-scope VONNE occupation.

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
