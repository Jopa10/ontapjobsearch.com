# VONNE ETL proof-of-concept review

review_date: 2026-08-20
review_fingerprint: 410a84fe338e4ca1288fe4e5f81b64d837f1a96bb28203e60ff9777c7b822db9

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are same-day only and do not publish anything.

Run generated: 2026-08-20T10:34:33+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 274
Approved NEJobs comparison rows: 32

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 4
- Detail pages fetched successfully: 4
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 11
- Tees Valley explicitly excluded: 1
- Outside or unmapped geography excluded: 0
- Generic/derived geography rows requiring review: 5
- Retained target candidates: 14

## Outcomes
- HC: 0
- POSS: 6
- HARD_PASS: 8
- Final selected after same-day actions: 4
- Final POSS awaiting decision: 0
- Manually excluded: 2

## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

---
action: select
SELECTED | North East | Hybrid | £ Per Annum | Bid Writer
employer: People First Independent Advocacy
closing_date: 01 September 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173334
source_job_id: 173334
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173334
---

---
action: select
SELECTED | North East - Tyneside, Wearside & Northumberland | Northumberland | £31,005 Pro Rata | Community Engagement Tutor - Ashington Learning Hive
employer: Northern Learning Trust
closing_date: 07 September 2026
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £31,005 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173341
source_job_id: 173341
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173341
---

---
action: select
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £26,402 to 28,141 Per Annum | Health & Wellbeing Projects Support Officer
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
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £23,790 to 27,000 Per Annum | Youth Engagement Officer
employer: Foundation of Light
closing_date: Friday, August 28, 2026 - 00:00
geography: CONFIRMED — location: approved location fallback
reason: provisional transferable-office review
source: VONNE
tracking_key: vonne-173331
source_job_id: 173331
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173331
---


## POSS — choose SELECT or EXCLUDE

- None.

## EXCLUDED BY REVIEW

---
action: exclude
EXCLUDED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £34,434 to 36,363 Per Annum | Health & Wellbeing Coordinator
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
action: exclude
EXCLUDED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £34,434 to 36,363 Pro Rata | VCSE Health & Wellbeing Research Partnerships Coordinator (Maternity Cover)
employer: VONNE
closing_date: Sunday, August 23, 2026 - 00:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £36,363 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173253
source_job_id: 173253
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173253
---


## HARD_PASS

- [Business Development Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173336) — confirmed JobG8 duplicate.
- [DadVocate Programme Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173337) — out-of-scope VONNE occupation.
- [Energy Advice Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173343) — out-of-scope VONNE occupation.
- [Energy and Retrofit Advisor](https://www.vonne.org.uk/vonne-jobs-details?cid=173328) — insufficient service-admin evidence.
- [Experienced Manager – Adult Training Services](https://www.vonne.org.uk/vonne-jobs-details?cid=173342) — out-of-scope VONNE occupation.
- [Head of Business Development and Fundraising](https://www.vonne.org.uk/vonne-jobs-details?cid=172957) — out-of-scope VONNE occupation.
- [Positive Behaviour Support Project Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173327) — out-of-scope VONNE occupation.
- [Senior Young Dads Worker - Sunderland](https://www.vonne.org.uk/vonne-jobs-details?cid=173338) — out-of-scope VONNE occupation.

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
