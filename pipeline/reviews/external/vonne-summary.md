# VONNE ETL proof-of-concept review

review_date: 2026-09-01
review_fingerprint: 74d362880f4a056d47b65d4d727baea0c76f2cc30e02a862c79d40738df34065

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-09-01T12:55:38+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 250
Approved NEJobs comparison rows: 19

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 5
- Detail pages fetched successfully: 5
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 10
- Tees Valley explicitly excluded: 2
- Outside or unmapped geography excluded: 0
- Generic/derived geography rows requiring review: 1
- Retained target candidates: 13

## Outcomes
- HC: 0
- POSS: 5
- HARD_PASS: 8
- Final selected after remembered/manual actions: 1
- Final POSS awaiting decision: 1
- Manually excluded: 3
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

- None.

## POSS — choose SELECT or EXCLUDE

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
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £23,370 to 23,790 | Receptionist
employer: Foundation of Light
closing_date: Friday, September 11, 2026 - 00:00
geography: CONFIRMED — location: approved location fallback
reason: possible cross-source duplicate requires review
source: VONNE
tracking_key: vonne-173374
vacancy_fingerprint: 6f57a4f078d03479daa7126537cb9614a4fe68d8551b871ecea57b2098e876d8
source_job_id: 173374
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173374
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Chief Executive Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173376) — out-of-scope VONNE occupation.
- [Finance Manager - Part time](https://www.vonne.org.uk/vonne-jobs-details?cid=173366) — out-of-scope VONNE occupation.
- [Fundraising and Partnerships Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=172769) — out-of-scope VONNE occupation.
- [Outreach Adviser (Schools)](https://www.vonne.org.uk/vonne-jobs-details?cid=173370) — insufficient service-admin evidence.
- [Project Worker: Disability Heritage in North Tyneside: The NTDF Story](https://www.vonne.org.uk/vonne-jobs-details?cid=173231) — out-of-scope VONNE occupation.
- [Stock Controller](https://www.vonne.org.uk/vonne-jobs-details?cid=173378) — insufficient service-admin evidence.
- [Temporary Centre Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173361) — out-of-scope VONNE occupation.
- [Women's Project Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173373) — out-of-scope VONNE occupation.

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
