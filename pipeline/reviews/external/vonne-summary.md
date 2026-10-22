# VONNE ETL proof-of-concept review

review_date: 2026-10-22
review_fingerprint: 23bf4382bde425e616b76c7c51123ae6eca5aa65c29fbcdb70077115ff9821ef

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-10-22T13:16:06+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 410
Approved NEJobs comparison rows: 0

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 5
- Detail pages fetched successfully: 5
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 10
- Tees Valley explicitly excluded: 0
- Outside or unmapped geography excluded: 1
- Generic/derived geography rows requiring review: 3
- Retained target candidates: 14

## Outcomes
- HC: 1
- POSS: 5
- HARD_PASS: 8
- Final selected after remembered/manual actions: 1
- Final POSS awaiting decision: 0
- Manually excluded: 5
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
reason: transferable title with specialist or borderline wording: housing
source: VONNE
tracking_key: vonne-173522
vacancy_fingerprint: 5cff7a254c5e2857818e5d08eba57442fdd870b1ae43512b72aca1e745557b98
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
- [Chief Executive](https://www.vonne.org.uk/vonne-jobs-details?cid=173526) — out-of-scope VONNE occupation.
- [Community Link Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173544) — out-of-scope VONNE occupation.
- [Employability and Skills Mentor](https://www.vonne.org.uk/vonne-jobs-details?cid=173545) — insufficient service-admin evidence.
- [Independent Advocate](https://www.vonne.org.uk/vonne-jobs-details?cid=173539) — insufficient service-admin evidence.
- [Payroll and People Systems Assistant](https://www.vonne.org.uk/vonne-jobs-details?cid=173536) — confirmed JobG8 duplicate.

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
