# VONNE ETL proof-of-concept review

review_date: 2026-09-26
review_fingerprint: 1bbd0400e0e51cbe484cae7f8d93241cb0abc70255e674911f64f48a482377a7

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-09-26T12:42:10+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 336
Approved NEJobs comparison rows: 2

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 2
- Detail pages fetched successfully: 2
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 13
- Tees Valley explicitly excluded: 3
- Outside or unmapped geography excluded: 1
- Generic/derived geography rows requiring review: 1
- Retained target candidates: 11

## Outcomes
- HC: 0
- POSS: 1
- HARD_PASS: 10
- Final selected after remembered/manual actions: 0
- Final POSS awaiting decision: 1
- Manually excluded: 0
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
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Advice Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173461) — out-of-scope VONNE occupation.
- [Age Friendly Engagement Co-ordinator](https://www.vonne.org.uk/vonne-jobs-details?cid=173472) — insufficient service-admin evidence.
- [Community Health Activator - Researcher (CHAR)](https://www.vonne.org.uk/vonne-jobs-details?cid=173467) — insufficient service-admin evidence.
- [Employability Advisor](https://www.vonne.org.uk/vonne-jobs-details?cid=173454) — insufficient service-admin evidence.
- [Employability Advisor](https://www.vonne.org.uk/vonne-jobs-details?cid=173453) — insufficient service-admin evidence.
- [Grants and Funding Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173425) — out-of-scope VONNE occupation.
- [Parent Carer Project Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173466) — out-of-scope VONNE occupation.
- [Recovery Coach](https://www.vonne.org.uk/vonne-jobs-details?cid=173464) — insufficient service-admin evidence.
- [Recovery Coach](https://www.vonne.org.uk/vonne-jobs-details?cid=173463) — insufficient service-admin evidence.
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
