# VONNE ETL proof-of-concept review

review_date: 2026-08-13
review_fingerprint: 370e08a10facbfbb81e2733059d90780fbf249a79a582b395bec418e40f22243

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are same-day only and do not publish anything.

Run generated: 2026-08-13T09:03:14+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 296
Approved NEJobs comparison rows: 5

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 5
- Detail pages fetched successfully: 5
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 10
- Tees Valley explicitly excluded: 1
- Outside or unmapped geography excluded: 0
- Generic/derived geography rows requiring review: 0
- Retained target candidates: 14

## Outcomes
- HC: 1
- POSS: 8
- HARD_PASS: 5
- Final selected after same-day actions: 1
- Final POSS awaiting decision: 8
- Manually excluded: 0

## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £26,213 Pro Rata | Information and Communications Administrator (Living Well North Tyneside)
employer: North Tyneside VODA
closing_date: Monday, August 31, 2026 - 17:00
geography: CONFIRMED — location: approved location fallback
reason: clear transferable title: administrator
source: VONNE
tracking_key: vonne-173321
source_job_id: 173321
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173321
---


## POSS — choose SELECT or EXCLUDE

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Durham | £34,592 Per Annum | Bereavement Counsellor
employer: Age UK County Durham
closing_date: 04 September 2026
geography: CONFIRMED — location: exact area
reason: annualised upper salary £34,592 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173322
source_job_id: 173322
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173322
---

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Durham | £34,592 Per Annum | Counsellor/Psychotherapist
employer: Age UK County Durham
closing_date: 04 September 2026
geography: CONFIRMED — location: exact area
reason: annualised upper salary £34,592 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173323
source_job_id: 173323
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173323
---

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | County Durham | £26,761 to 28,966 Pro Rata | Therapeutic Coordinator
employer: Rape and Sexual Abuse Counselling Centre (Darlington and County Durham)
closing_date: Monday, August 24, 2026 - 12:00
geography: CONFIRMED — location: approved location fallback
reason: provisional transferable-office review
source: VONNE
tracking_key: vonne-173311
source_job_id: 173311
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173311
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle | £ Per Annum | Finance Officer
employer: National Energy Action
closing_date: 17 August 2026
geography: CONFIRMED — location: exact area
reason: transferable title with specialist or borderline wording: finance
source: VONNE
tracking_key: vonne-173303
source_job_id: 173303
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173303
---

---
action:
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
action:
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £32,126 Per Annum | Project Team Leader - Domestic Abuse Service Gateshead (Female*)
employer: Oasis Community Housing
closing_date: 20 August 2026
geography: CONFIRMED — location: exact area
reason: annualised upper salary £32,126 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-171327
source_job_id: 171327
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=171327
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £34,434 to 36,363 Pro Rata | VCSE Health & Wellbeing Research Partnerships Coordinator (Maternity Cover)
employer: VONNE
closing_date: Sunday, August 23, 2026 - 00:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £36,363 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173253
source_job_id: 173253
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173253
---


## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Community Café Cook](https://www.vonne.org.uk/vonne-jobs-details?cid=173318) — out-of-scope VONNE occupation.
- [Deputy Chief Executive Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173324) — out-of-scope VONNE occupation.
- [Health Improvement Practitioner - Physical Activity Specialist](https://www.vonne.org.uk/vonne-jobs-details?cid=173287) — out-of-scope VONNE occupation.
- [Retail & Online Sales Assistant](https://www.vonne.org.uk/vonne-jobs-details?cid=173300) — insufficient service-admin evidence.
- [Workplace Health Development Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173308) — out-of-scope VONNE occupation.

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
