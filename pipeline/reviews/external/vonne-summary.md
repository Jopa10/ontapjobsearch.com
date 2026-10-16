# VONNE ETL proof-of-concept review

review_date: 2026-10-16
review_fingerprint: 0657071379a2c50ee89f3a5cf6713d63fc29e9c7c4060d510464a901f1c0183f

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-10-16T12:47:24+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 413
Approved NEJobs comparison rows: 0

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 5
- Detail pages fetched successfully: 5
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 10
- Tees Valley explicitly excluded: 0
- Outside or unmapped geography excluded: 3
- Generic/derived geography rows requiring review: 3
- Retained target candidates: 12

## Outcomes
- HC: 1
- POSS: 6
- HARD_PASS: 5
- Final selected after remembered/manual actions: 1
- Final POSS awaiting decision: 4
- Manually excluded: 2
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £25,880 Per Annum | Contact Centre Adviser - Consumer
employer: Citizens Advice Gateshead
closing_date: Friday, October 23, 2026 - 09:00
geography: CONFIRMED — location: approved location fallback
reason: clear transferable title: contact centre
source: VONNE
tracking_key: vonne-173530
vacancy_fingerprint: 48a133cf6dd62ccaf528f1e4c9ae33813dd3f80af77a8f77feab91e62a7f965a
source_job_id: 173530
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173530
---
## POSS — choose SELECT or EXCLUDE

---
action:
POSS | North East | Hybrid | £ Pro Rata | Payroll and People Systems Assistant
employer: National Energy Action
closing_date: 27 October 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173536
vacancy_fingerprint: 39bbcedd8cd9ba8da0d7036ea75f4a86f459d3ea9f3c418311b96d292d8e7189
source_job_id: 173536
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173536
---
---
action:
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
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £24,796 to 28,153 Per Annum | Administrator (VAWG TEAM)
employer: The Angelou Centre
closing_date: Saturday, October 31, 2026 - 05:00
geography: CONFIRMED — location: approved location fallback
reason: possible cross-source duplicate requires review
source: VONNE
tracking_key: vonne-173521
vacancy_fingerprint: 1b881bdff0978f7131882da6166feea86cc94020d825071b96d436091c31b1c4
source_job_id: 173521
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173521
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £30,303 to 35,781 Per Annum | Housing Coordinator
employer: The Angelou Centre
closing_date: Saturday, October 31, 2026 - 05:00
geography: CONFIRMED — location: approved location fallback
reason: possible cross-source duplicate requires review
source: VONNE
tracking_key: vonne-173522
vacancy_fingerprint: 61c24dc341e1a13672ae87098d2c61e64cb2480c2d25c2dd52f8d24aa08c9c73
source_job_id: 173522
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173522
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Hybrid | £ | Social Welfare Adviser
employer: Citizens Advice Gateshead
closing_date: 23 October 2026
geography: DERIVED_REVIEW — employer-derived geography: area found in address: gateshead
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173531
vacancy_fingerprint: f66ce826443620503db801f7cc0a1c849b114fa6d8758b2c2a30486161b27452
source_job_id: 173531
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173531
---
---
action:
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

- [Chief Executive](https://www.vonne.org.uk/vonne-jobs-details?cid=173526) — out-of-scope VONNE occupation.
- [COMMUNITY LINK WORKER](https://www.vonne.org.uk/vonne-jobs-details?cid=173544) — out-of-scope VONNE occupation.
- [Employability and Skills Mentor](https://www.vonne.org.uk/vonne-jobs-details?cid=173545) — insufficient service-admin evidence.
- [Independent Advocate](https://www.vonne.org.uk/vonne-jobs-details?cid=173539) — insufficient service-admin evidence.
- [Interim Chief Executive Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173518) — out-of-scope VONNE occupation.

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
