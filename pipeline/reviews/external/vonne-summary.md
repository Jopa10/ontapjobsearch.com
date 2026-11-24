# VONNE ETL proof-of-concept review

review_date: 2026-11-24
review_fingerprint: 3e6bc835bf843877aae744c4aeda300fb09a387b111a28f1f7be6819494c3467

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-11-24T18:07:33+00:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 1091
Approved NEJobs comparison rows: 0

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 4
- Detail pages fetched successfully: 4
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 11
- Tees Valley explicitly excluded: 3
- Outside or unmapped geography excluded: 0
- Generic/derived geography rows requiring review: 2
- Retained target candidates: 12

## Outcomes
- HC: 0
- POSS: 7
- HARD_PASS: 5
- Final selected after remembered/manual actions: 0
- Final POSS awaiting decision: 7
- Manually excluded: 0
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

- None.

## POSS — choose SELECT or EXCLUDE

---
action:
POSS | North East | Hybrid | £31,000 Per Annum | Sunderland Good Food Partnership Co-Ordinator
employer: OASES
closing_date: 08 December 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173769
vacancy_fingerprint: 1f72c572a5045f884a0b2f097607feadc19219fccfe4fc27d5fc8b92d274b3d0
source_job_id: 173769
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173769
---
---
action:
POSS | North East - County Durham & Darlington/Hartlepool | County Durham | £26,000 to 28,403 Per Annum | Hospital Discharge Partnership Coordinator
employer: Citizens Advice Darlington Redcar & Cleveland
closing_date: Monday, November 30, 2026 - 17:00
geography: CONFIRMED — location: approved location fallback
reason: provisional transferable-office review
source: VONNE
tracking_key: vonne-173726
vacancy_fingerprint: 39d71f5e1d6c45ac60285e0fab04d3f72d8df2bb061d0e4b346745830a9e31d8
source_job_id: 173726
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173726
---
---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Hybrid | £ Pro Rata | Independent Sexual Violence Advisor (ISVA)
employer: Rape and Sexual Abuse Counselling Centre (Darlington and County Durham)
closing_date: 07 December 2026
geography: DERIVED_REVIEW — employer-derived geography: area found in address: darlington
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173736
vacancy_fingerprint: 7f6b1cc06aa7b624ef8729732e782384d57ac6bb9660b64803b1291ce9c96c91
source_job_id: 173736
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173736
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
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Business Crime Navigator](https://www.vonne.org.uk/vonne-jobs-details?cid=173723) — insufficient service-admin evidence.
- [Service Manager - Durham and Darlington Women’s Diversion Service](https://www.vonne.org.uk/vonne-jobs-details?cid=173787) — out-of-scope VONNE occupation.
- [South Tyneside Child and Young Person Mental Health Service Counsellor](https://www.vonne.org.uk/vonne-jobs-details?cid=173730) — insufficient service-admin evidence.
- [Support and Development Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173784) — insufficient service-admin evidence.
- [Team Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173717) — out-of-scope VONNE occupation.

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
