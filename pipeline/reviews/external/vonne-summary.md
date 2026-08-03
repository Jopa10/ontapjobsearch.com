# VONNE ETL proof-of-concept review

review_date: 2026-08-03
review_fingerprint: 0142d7f19cf3e313c82b833b3b3274d57ceead7a0b2b2dd59dd49bcfe8c00de6

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are same-day only and do not publish anything.

Run generated: 2026-08-03T10:41:50+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 70
Approved NEJobs comparison rows: 13

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 4
- Detail pages fetched successfully: 4
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 11
- Tees Valley explicitly excluded: 0
- Outside or unmapped geography excluded: 0
- Generic/derived geography rows requiring review: 5
- Retained target candidates: 15

## Outcomes
- HC: 0
- POSS: 5
- HARD_PASS: 10
- Final selected after same-day actions: 5
- Final POSS awaiting decision: 0
- Manually excluded: 0

## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

---
action: select
SELECTED | North East | Hybrid | £30,000 Per Annum | Project Lead
employer: People's Powerhouse
closing_date: 16 August 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173270
source_job_id: 173270
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173270
---

---
action: select
SELECTED | North East - Tyneside, Wearside & Northumberland | Regionwide | £113 Per Day | Accreditation and Outreach Officer
employer: The Young Women's Film Academy
closing_date: Friday, August 21, 2026 - 17:00
geography: CONFIRMED — based: exact area
reason: provisional transferable-office review
source: VONNE
tracking_key: vonne-173252
source_job_id: 173252
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173252
---

---
action: select
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £29,024 to 31,856 Pro Rata | Family Learning Coordinator (9 Months Fixed Term)
employer: Children North East
closing_date: Tuesday, August 11, 2026 - 12:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £31,856 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173262
source_job_id: 173262
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173262
---

---
action: select
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £29,024 to 31,856 Pro Rata | School Family Coordinator
employer: Children North East
closing_date: Tuesday, August 11, 2026 - 12:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £31,856 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173267
source_job_id: 173267
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173267
---

---
action: select
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £34,434 to 36,363 Pro Rata | VCSE Health & Wellbeing Research Partnerships Coordinator (Maternity Cover)
employer: VONNE
closing_date: Sunday, August 23, 2026 - 00:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £36,363 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173253
source_job_id: 173253
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173253
---


## POSS — choose SELECT or EXCLUDE

- None.

## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Chair of Trustees](https://www.vonne.org.uk/vonne-jobs-details?cid=173279) — out-of-scope VONNE occupation.
- [Convention Producer](https://www.vonne.org.uk/vonne-jobs-details?cid=173273) — out-of-scope VONNE occupation.
- [Good Neighbours Project Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173285) — out-of-scope VONNE occupation.
- [Making Waves Programme Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173266) — out-of-scope VONNE occupation.
- [Peripatetic Project Worker - Young Peoples Services](https://www.vonne.org.uk/vonne-jobs-details?cid=173264) — out-of-scope VONNE occupation.
- [Project Manager (CEO)](https://www.vonne.org.uk/vonne-jobs-details?cid=173269) — out-of-scope VONNE occupation.
- [Senior Young Dads Worker (Neurodiverse)](https://www.vonne.org.uk/vonne-jobs-details?cid=173274) — out-of-scope VONNE occupation.
- [Sessional Project Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173260) — out-of-scope VONNE occupation.
- [Trustees](https://www.vonne.org.uk/vonne-jobs-details?cid=173265) — out-of-scope VONNE occupation.
- [Young Carers Contact and Group Practitioner (Youth Worker)](https://www.vonne.org.uk/vonne-jobs-details?cid=173275) — out-of-scope VONNE occupation.

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
