# VONNE ETL proof-of-concept review

review_date: 2026-11-04
review_fingerprint: 6ceda9a97fa899f5c8aeaca519f0c839f775f461f41d2a79e3e987ef42a72176

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-11-04T14:48:50+00:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 1081
Approved NEJobs comparison rows: 0

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 1
- Detail pages fetched successfully: 1
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 14
- Tees Valley explicitly excluded: 1
- Outside or unmapped geography excluded: 1
- Generic/derived geography rows requiring review: 3
- Retained target candidates: 13

## Outcomes
- HC: 0
- POSS: 3
- HARD_PASS: 10
- Final selected after remembered/manual actions: 0
- Final POSS awaiting decision: 2
- Manually excluded: 1
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
action:
POSS | North East | Hybrid | £80,000 Per Annum | Regional Director, North East
employer: AllChild
closing_date: 23 November 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173648
vacancy_fingerprint: 7869cf771a4a80e0655ec6751efee7552c837ee65b86bc5114b41a0d54eb3e17
source_job_id: 173648
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173648
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
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Access to Work Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173559) — out-of-scope VONNE occupation.
- [Bid Writer (Trusts and Foundations)](https://www.vonne.org.uk/vonne-jobs-details?cid=173383) — insufficient service-admin evidence.
- [Cancer and Dementia Care Community Link Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173588) — out-of-scope VONNE occupation.
- [Domestic Abuse Refuge Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173561) — out-of-scope VONNE occupation.
- [Family Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173625) — out-of-scope VONNE occupation.
- [Grants Administration Officer (Small and Medium Grants)](https://www.vonne.org.uk/vonne-jobs-details?cid=173618) — insufficient service-admin evidence.
- [Housing Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173636) — out-of-scope VONNE occupation.
- [Income and Project Delivery Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173614) — insufficient service-admin evidence.
- [Monitoring and Co-ordination Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173633) — out-of-scope VONNE occupation.
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
