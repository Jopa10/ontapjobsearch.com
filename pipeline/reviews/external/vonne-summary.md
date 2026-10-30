# VONNE ETL proof-of-concept review

review_date: 2026-10-30
review_fingerprint: 783cb97fe4c6a632462706dad9e156b38537fb07de2b4a80545b2983445706cc

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-10-30T13:22:21+00:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 442
Approved NEJobs comparison rows: 0

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 3
- Detail pages fetched successfully: 3
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 12
- Tees Valley explicitly excluded: 0
- Outside or unmapped geography excluded: 1
- Generic/derived geography rows requiring review: 3
- Retained target candidates: 14

## Outcomes
- HC: 0
- POSS: 4
- HARD_PASS: 10
- Final selected after remembered/manual actions: 0
- Final POSS awaiting decision: 1
- Manually excluded: 3
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

- None.

## POSS — choose SELECT or EXCLUDE

---
action:
POSS | North East | Home-based | £35,000 to 39,000 Per Annum | Embedded Outreach Officer
employer: King's College Cambridge
closing_date: Monday, November 30, 2026 - 17:00
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173627
vacancy_fingerprint: 39d05d5987a989470769e6863d6bc036e0277cdd5a64bb01a9750805dee7287e
source_job_id: 173627
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173627
---
---
action: exclude
POSS | North East - County Durham & Darlington/Hartlepool | County Durham | £26,439 Per Annum | Carer Support Coordinator
employer: Durham County Carers Support
closing_date: Friday, November 13, 2026 - 17:00
geography: CONFIRMED — location: approved location fallback
reason: provisional transferable-office review
source: VONNE
tracking_key: vonne-173457
vacancy_fingerprint: 26158f8f4312bf2fbfa437f194700f9dc9f1c4216a3fd43891b81c9caf879132
source_job_id: 173457
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173457
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Flexible | £29,503 Per Annum | Employment Support Advisor
employer: North Tyneside Carers' Centre
closing_date: 06 November 2026
geography: DERIVED_REVIEW — employer-derived geography: geography phrase: north tyneside
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173582
vacancy_fingerprint: f1178a0e4cbcd10bc69ae022e8d3d130365fd73b4ee5b71246c4d3c40fbcaae6
source_job_id: 173582
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173582
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £26,718 to 28,772 Per Annum | Student Communities Coordinator, Sunderland
employer: University of Sunderland Students' Union
closing_date: Sunday, November 1, 2026 - 23:59
geography: CONFIRMED — location: approved location fallback
reason: provisional transferable-office review
source: VONNE
tracking_key: vonne-173537
vacancy_fingerprint: adcd4c9a8d25ee0199412663f63c1250fb2f70b87f2f50682cb00dc6660abcea
source_job_id: 173537
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173537
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Access to Work Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173559) — out-of-scope VONNE occupation.
- [Advice Services Manager (Community)](https://www.vonne.org.uk/vonne-jobs-details?cid=173555) — out-of-scope VONNE occupation.
- [Bid Writer (Trusts and Foundations)](https://www.vonne.org.uk/vonne-jobs-details?cid=173383) — insufficient service-admin evidence.
- [Cancer and Dementia Care Community Link Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173588) — out-of-scope VONNE occupation.
- [Chief Executive](https://www.vonne.org.uk/vonne-jobs-details?cid=173526) — out-of-scope VONNE occupation.
- [Domestic Abuse Refuge Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173561) — out-of-scope VONNE occupation.
- [Family Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173625) — out-of-scope VONNE occupation.
- [Grants Administration Officer (Small and Medium Grants)](https://www.vonne.org.uk/vonne-jobs-details?cid=173618) — insufficient service-admin evidence.
- [Income and Project Delivery Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173614) — insufficient service-admin evidence.
- [Outreach Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173624) — out-of-scope VONNE occupation.

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
