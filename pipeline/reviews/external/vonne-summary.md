# VONNE ETL proof-of-concept review

review_date: 2026-11-14
review_fingerprint: e96423edd67aceeb819e79758481f96e336d22594af0d7a47c9ca8fa099a5f4d

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-11-14T13:45:17+00:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 1018
Approved NEJobs comparison rows: 0

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 3
- Detail pages fetched successfully: 3
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 12
- Tees Valley explicitly excluded: 2
- Outside or unmapped geography excluded: 0
- Generic/derived geography rows requiring review: 0
- Retained target candidates: 13

## Outcomes
- HC: 0
- POSS: 6
- HARD_PASS: 7
- Final selected after remembered/manual actions: 0
- Final POSS awaiting decision: 6
- Manually excluded: 0
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

- None.

## POSS — choose SELECT or EXCLUDE

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Durham | £28,000 Per Annum | Support Worker
employer: Emmaus North East
closing_date: 31 December 2026
geography: CONFIRMED — location: exact area
reason: possible cross-source duplicate requires review
source: VONNE
tracking_key: vonne-173685
vacancy_fingerprint: 4dbabf7aeb40063930d204bde3bf4242013702296b5f91843b8728a09983368a
source_job_id: 173685
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173685
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £33,323 to 34,899 Per Annum | Business Engagement Officer
employer: Society Matters CIC
closing_date: Monday, December 14, 2026 - 09:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £34,899 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173703
vacancy_fingerprint: 3894a2f601419f83870376d3f0984f1991c6d76b04b071e616cd53876169b969
source_job_id: 173703
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173703
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £25,878 to 34,240 | Criminal Justice Recovery Coordinator
employer: Waythrough
closing_date: Friday, November 27, 2026 - 00:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £34,240 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173722
vacancy_fingerprint: 5519388993dcafa8850e292a0dccad2b5c655a22d5fd714aeebc2f8521d015fe
source_job_id: 173722
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173722
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | South Tyneside | £51,525 Pro Rata | Director of Culture, Enrichment and Creativity
employer: Groundwork South and North Tyneside
closing_date: 01 December 2026
geography: CONFIRMED — location: geography phrase: south tyneside
reason: annualised upper salary £51,525 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173704
vacancy_fingerprint: d8b3a0b86a8bc3a4cbd9a985e981f47de2c81bf28894812c7d2b755b157cccc5
source_job_id: 173704
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173704
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £23,778 Pro Rata | Finance and Admin Assistant
employer: Tyne and Wear Building Preservation Trust Limited
closing_date: Thursday, December 10, 2026 - 17:00
geography: CONFIRMED — location: approved location fallback
reason: transferable title with specialist or borderline wording: finance
source: VONNE
tracking_key: vonne-173707
vacancy_fingerprint: fd3d605595b9359680e360ca098216b05d4d00136b171a311893c9d9ea36b9f5
source_job_id: 173707
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173707
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £33,323 Per Annum | Good Work Grants Lead Officer
employer: Society Matters CIC
closing_date: 14 December 2026
geography: CONFIRMED — location: exact area
reason: transferable title with specialist or borderline wording: lead
source: VONNE
tracking_key: vonne-173702
vacancy_fingerprint: c8ff0702d0cadb59987d047e95cd6083b7009cc8ade06b11fc4012a595b4a9ab
source_job_id: 173702
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173702
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Business Crime Navigator](https://www.vonne.org.uk/vonne-jobs-details?cid=173723) — insufficient service-admin evidence.
- [CLA Triage Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173690) — out-of-scope VONNE occupation.
- [Project Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173712) — out-of-scope VONNE occupation.
- [School Based Counsellor](https://www.vonne.org.uk/vonne-jobs-details?cid=173700) — insufficient service-admin evidence.
- [Team Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173717) — out-of-scope VONNE occupation.
- [Visits Services Catering Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173714) — out-of-scope VONNE occupation.
- [Visits Services Play Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173713) — out-of-scope VONNE occupation.

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
