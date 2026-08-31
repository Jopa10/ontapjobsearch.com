# VONNE ETL proof-of-concept review

review_date: 2026-08-31
review_fingerprint: 5e1a3f00387f915058aeb065473403b79b2db622918f90b0e69a41deee5f04ec

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-08-31T15:18:24+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 142
Approved NEJobs comparison rows: 30

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 5
- Detail pages fetched successfully: 5
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 10
- Tees Valley explicitly excluded: 1
- Outside or unmapped geography excluded: 0
- Generic/derived geography rows requiring review: 2
- Retained target candidates: 14

## Outcomes
- HC: 1
- POSS: 5
- HARD_PASS: 8
- Final selected after remembered/manual actions: 3
- Final POSS awaiting decision: 0
- Manually excluded: 3
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £23,370 to 23,790 | Receptionist
employer: Foundation of Light
closing_date: Friday, September 11, 2026 - 00:00
geography: CONFIRMED — location: approved location fallback
reason: clear transferable title: receptionist
source: VONNE
tracking_key: vonne-173374
vacancy_fingerprint: 6141356550a9d381b72bc7d60456c938933c2c5ec3444cf244833d6c2d5fee42
source_job_id: 173374
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173374
---
## POSS — choose SELECT or EXCLUDE

---
action: select
POSS | North East | Regionwide | £30,150 Per Annum | Housing Support Officer
employer: Handcrafted
closing_date: Tuesday, September 1, 2026 - 17:00
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173358
vacancy_fingerprint: bc1c2200fdc8dcfa64f31abb48d4a2d0d40df53ed9b1bdd1bf5d91948b802f74
source_job_id: 173358
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173358
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
vacancy_fingerprint: 25bce1025449c1002f480b7b77769ff54b70b170d8a01bd59a5f484ec7758404
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
vacancy_fingerprint: 8a7ab286013372c433a61a3c5bcaad36cea77bc6812442d255b413a5866b6bce
source_job_id: 173310
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173310
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £29,02431,856 Pro Rata | Project Coordinator - Neuro Team
employer: Children North East
closing_date: Friday, September 11, 2026 - 12:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £2,902,431,856 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173367
vacancy_fingerprint: 3dcdfbfb593f024c4838ab4e9c9c8311016c207f82745eaf9fa18a53e680a6fa
source_job_id: 173367
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173367
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle | £34,625 Per Annum | Project Lead
employer: Changing Lives
closing_date: 09 September 2026
geography: CONFIRMED — location: exact area
reason: transferable title with specialist or borderline wording: lead
source: VONNE
tracking_key: vonne-173363
vacancy_fingerprint: 2b3c14a2b6daf54c403013deddf082d852b216bd0f345f8373fe1b1a1bdf2c8d
source_job_id: 173363
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173363
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Chief Executive Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173376) — out-of-scope VONNE occupation.
- [Finance Manager - Part time](https://www.vonne.org.uk/vonne-jobs-details?cid=173366) — out-of-scope VONNE occupation.
- [Fundraising and Partnerships Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=172769) — out-of-scope VONNE occupation.
- [Outreach Adviser (Schools)](https://www.vonne.org.uk/vonne-jobs-details?cid=173370) — insufficient service-admin evidence.
- [Project Worker: Disability Heritage in North Tyneside: The NTDF Story](https://www.vonne.org.uk/vonne-jobs-details?cid=173231) — out-of-scope VONNE occupation.
- [Temporary Centre Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173361) — out-of-scope VONNE occupation.
- [Women's Project Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173373) — out-of-scope VONNE occupation.
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
