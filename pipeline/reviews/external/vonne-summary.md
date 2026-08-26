# VONNE ETL proof-of-concept review

review_date: 2026-08-26
review_fingerprint: 095b80e161824f0946a7126f13754160d985d649486bf62c1ddc0d8455c240f5

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-08-26T08:26:39+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 230
Approved NEJobs comparison rows: 22

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 4
- Detail pages fetched successfully: 4
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 11
- Tees Valley explicitly excluded: 1
- Outside or unmapped geography excluded: 1
- Generic/derived geography rows requiring review: 3
- Retained target candidates: 13

## Outcomes
- HC: 0
- POSS: 5
- HARD_PASS: 8
- Final selected after remembered/manual actions: 3
- Final POSS awaiting decision: 0
- Manually excluded: 2
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

- None.

## POSS — choose SELECT or EXCLUDE

---
action: exclude
POSS | North East | Home-based | £25,664 Per Annum | Mentor (HEAT) - North East England
employer: The Wise Group
closing_date: 27 August 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173344
source_job_id: 173344
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173344
---
---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Hybrid | £31,500 Pro Rata | Trusts and Community Fundraising Officer
employer: Durham County Carers Support
closing_date: 25 September 2026
geography: DERIVED_REVIEW — employer-derived geography: area found in address: durham
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173349
source_job_id: 173349
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173349
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
source_job_id: 173310
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173310
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £25,334 to 26,419 Per Annum | Marketing Coordinator
employer: Age UK North Tyneside
closing_date: Wednesday, September 2, 2026 - 12:00
geography: CONFIRMED — location: approved location fallback
reason: provisional transferable-office review
source: VONNE
tracking_key: vonne-173347
source_job_id: 173347
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173347
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Energy Advice Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173343) — out-of-scope VONNE occupation.
- [Experienced &Trainee Telephone Debt Caseworker](https://www.vonne.org.uk/vonne-jobs-details?cid=173346) — out-of-scope VONNE occupation.
- [Experienced Manager – Adult Training Services](https://www.vonne.org.uk/vonne-jobs-details?cid=173342) — out-of-scope VONNE occupation.
- [Facilities and Compliance Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173354) — out-of-scope VONNE occupation.
- [Families Advice and Support Team Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173348) — out-of-scope VONNE occupation.
- [Project Worker: Disability Heritage in North Tyneside: The NTDF Story](https://www.vonne.org.uk/vonne-jobs-details?cid=173231) — out-of-scope VONNE occupation.
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
