# VONNE ETL proof-of-concept review

review_date: 2026-11-09
review_fingerprint: e94887d68c25777ab7329d15861796157072fb36fc4f80878e06d9bc6a54515d

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-11-09T16:46:24+00:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 1176
Approved NEJobs comparison rows: 0

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 2
- Detail pages fetched successfully: 2
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 13
- Tees Valley explicitly excluded: 1
- Outside or unmapped geography excluded: 2
- Generic/derived geography rows requiring review: 4
- Retained target candidates: 12

## Outcomes
- HC: 0
- POSS: 6
- HARD_PASS: 6
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
POSS | North East | Hybrid | £31,076 Pro Rata | Counsellor
employer: Eating Distress North East
closing_date: 30 November 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173656
vacancy_fingerprint: a664633734d9bbb21d95cb2d15c49387680c810f4de19b6a99d1b400f3d16a73
source_job_id: 173656
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173656
---
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
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £26,893 to 34,068 Per Annum | Education Coordinator
employer: Northumbria Students Union
closing_date: Wednesday, December 2, 2026 - 12:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £34,068 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173674
vacancy_fingerprint: 907b4c71ff28143269faf4f196530e1725bf8b14ae2fbdf597f462c0d6662d2d
source_job_id: 173674
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173674
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle | £ | Placement Programme Lead
employer: Ouseburn Farm
closing_date: 22 November 2026
geography: CONFIRMED — location: exact area
reason: transferable title with specialist or borderline wording: lead
source: VONNE
tracking_key: vonne-173650
vacancy_fingerprint: 7ee29874d4f22edbdc8893d2d53d81686b72663478fa934b4952a0fa91e5a598
source_job_id: 173650
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173650
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Not stated |  | Treasurer
employer: Sunderland Minster
closing_date: 01 December 2026
geography: DERIVED_REVIEW — employer-derived geography: area found in address: sunderland
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173661
vacancy_fingerprint: 327f5e7dfcaa2e127f2d33d33df9cc3de8825a18e0544e3df0541865913e4b2f
source_job_id: 173661
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173661
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Family Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173625) — out-of-scope VONNE occupation.
- [Grants Administration Officer (Small and Medium Grants)](https://www.vonne.org.uk/vonne-jobs-details?cid=173618) — insufficient service-admin evidence.
- [Monitoring and Co-ordination Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173633) — out-of-scope VONNE occupation.
- [Outreach Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173624) — out-of-scope VONNE occupation.
- [Wellbeing & Campaigns Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173673) — out-of-scope VONNE occupation.
- [Young Carers’ Wellbeing Worker (Triage)](https://www.vonne.org.uk/vonne-jobs-details?cid=173676) — out-of-scope VONNE occupation.

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
