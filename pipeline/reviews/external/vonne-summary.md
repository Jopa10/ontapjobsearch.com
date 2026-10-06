# VONNE ETL proof-of-concept review

review_date: 2026-10-06
review_fingerprint: 10a3ac62ec08ea3a66b2d744e6eeaf604f18f1b890a734c8896c3d395d4bc2d2

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-10-06T14:31:33+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 372
Approved NEJobs comparison rows: 0

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 3
- Detail pages fetched successfully: 3
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 12
- Tees Valley explicitly excluded: 0
- Outside or unmapped geography excluded: 2
- Generic/derived geography rows requiring review: 2
- Retained target candidates: 13

## Outcomes
- HC: 0
- POSS: 8
- HARD_PASS: 5
- Final selected after remembered/manual actions: 0
- Final POSS awaiting decision: 8
- Manually excluded: 0
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

- None.

## POSS — choose SELECT or EXCLUDE

---
action:
POSS | North East | Regionwide | £29,542 to 30,515 Pro Rata | Going Green Together Project Officer (Maternity Cover)
employer: VONNE
closing_date: Monday, October 12, 2026 - 11:59
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173468
vacancy_fingerprint: 473cc7b424b8ffe7e0574bf796b773b5212da99c870656e1ac126920e92d4405
source_job_id: 173468
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173468
---
---
action:
POSS | North East | Hybrid | £24,480 Per Annum | Project Assistant
employer: North East Chamber of Commerce
closing_date: 27 October 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173489
vacancy_fingerprint: 614f3aa276c1067c98c18edf1a0144b16bb8bf36311bd7826b4c62486ff7f4ba
source_job_id: 173489
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173489
---
---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Darlington | £31,000 Per Annum | Shared Lives Carer in Darlington
employer: St Annes Community Services
closing_date: 01 November 2026
geography: CONFIRMED — location: exact area
reason: annualised upper salary £31,000 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-172562
vacancy_fingerprint: eb8b793916af3ab9b99e3ea1b533e1e9d92fb19db6343aaff2e2319719a7dba1
source_job_id: 172562
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=172562
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £33,323 Per Annum | Business Support Coach
employer: Society Matters CIC
closing_date: 02 November 2026
geography: CONFIRMED — location: exact area
reason: annualised upper salary £33,323 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173500
vacancy_fingerprint: e5d14a4bd7e6bcd346e2effe5bb567c7379d7782f9597b4e2a2cfc17e4639d77
source_job_id: 173500
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173500
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £28,366 to 31,518 Pro Rata | Grant Holder Support Officer
employer: North Tyneside VODA
closing_date: Monday, October 26, 2026 - 17:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £31,518 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173497
vacancy_fingerprint: 75468d164acfac9275b9bfbe745f8d272212d8fb197101a8c7a81b3e1fa2f7a8
source_job_id: 173497
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173497
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £28,366 to 31,518 Per Annum | Grant Holder Support Officer
employer: Connected Voice
closing_date: Monday, October 26, 2026 - 17:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £31,518 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173484
vacancy_fingerprint: 15891c6b102ec572bf3f7dbd5cee39bf27e8826c46768d20565728c755378952
source_job_id: 173484
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173484
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | South Tyneside | £15 Per Hour | Project Lead (STARCH)
employer: Churches Together in South Tyneside
closing_date: 30 October 2026
geography: CONFIRMED — location: geography phrase: south tyneside
reason: transferable title with specialist or borderline wording: lead
source: VONNE
tracking_key: vonne-173401
vacancy_fingerprint: 4921c718296e6f405987f2a4bd1abab5f3d27cdad2440f10f086adf8ffd317fd
source_job_id: 173401
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173401
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £50,565 Per Annum | Solicitor
employer: Citizens Advice Gateshead
closing_date: 30 October 2026
geography: CONFIRMED — location: exact area
reason: annualised upper salary £50,565 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173501
vacancy_fingerprint: 4d00ed2155f640268193e0ee1605ec4cc0efe1b8e02e611794da864f457f3446
source_job_id: 173501
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173501
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Children and Young People’s Mental Health](https://www.vonne.org.uk/vonne-jobs-details?cid=173496) — insufficient service-admin evidence.
- [Learning Disability Skills Specialist (Part Time)](https://www.vonne.org.uk/vonne-jobs-details?cid=172581) — insufficient service-admin evidence.
- [Team Leader - All-Age Caregivers](https://www.vonne.org.uk/vonne-jobs-details?cid=173477) — insufficient service-admin evidence.
- [Young Carer Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173481) — out-of-scope VONNE occupation.
- [Youth Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173495) — out-of-scope VONNE occupation.

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
