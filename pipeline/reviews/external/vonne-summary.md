# VONNE ETL proof-of-concept review

review_date: 2026-09-25
review_fingerprint: 9eacca165828e0215018409bf29e526dea4922587d256aff29e4a3ae714afac7

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-09-25T13:05:41+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 350
Approved NEJobs comparison rows: 2

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 2
- Detail pages fetched successfully: 2
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 13
- Tees Valley explicitly excluded: 4
- Outside or unmapped geography excluded: 0
- Generic/derived geography rows requiring review: 1
- Retained target candidates: 11

## Outcomes
- HC: 0
- POSS: 4
- HARD_PASS: 7
- Final selected after remembered/manual actions: 0
- Final POSS awaiting decision: 3
- Manually excluded: 1
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
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle | £ Pro Rata | Community Hub and Operations Lead
employer: Riverside Community Health Project
closing_date: 04 October 2026
geography: CONFIRMED — location: exact area
reason: transferable title with specialist or borderline wording: lead
source: VONNE
tracking_key: vonne-173448
vacancy_fingerprint: b9bd3c0080c2805600b11626f01318d26919158ea0461140fb3df8cf2fdd5705
source_job_id: 173448
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173448
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Northumberland | £ | Recovery Coach
employer: Waythrough
closing_date: 09 October 2026
geography: CONFIRMED — location: approved location fallback
reason: possible duplicate within VONNE
source: VONNE
tracking_key: vonne-173464
vacancy_fingerprint: da46a5d1d6bb658b5ddb5d1973d429eb58920c13ef850333665c8461be07d5c6
source_job_id: 173464
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173464
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Northumberland | £ | Recovery Coach
employer: Waythrough
closing_date: 09 October 2026
geography: CONFIRMED — location: approved location fallback
reason: possible duplicate within VONNE
source: VONNE
tracking_key: vonne-173463
vacancy_fingerprint: 9cca62eefb9367e0621b9c97b138c0a4f8c044a4e7905a73fac46f5e57040459
source_job_id: 173463
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173463
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Advice Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173461) — out-of-scope VONNE occupation.
- [Communications & Campaigns Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173449) — insufficient service-admin evidence.
- [Community Health Activator - Researcher (CHAR)](https://www.vonne.org.uk/vonne-jobs-details?cid=173467) — insufficient service-admin evidence.
- [Employability Advisor](https://www.vonne.org.uk/vonne-jobs-details?cid=173454) — insufficient service-admin evidence.
- [Employability Advisor](https://www.vonne.org.uk/vonne-jobs-details?cid=173453) — insufficient service-admin evidence.
- [Parent Carer Project Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173466) — out-of-scope VONNE occupation.
- [Wellbeing Facilitator](https://www.vonne.org.uk/vonne-jobs-details?cid=173458) — insufficient service-admin evidence.

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
