# VONNE ETL proof-of-concept review

review_date: 2026-09-23
review_fingerprint: ba632aff3a74238b54e3cbc311468da8d9a4bc2969dc1024dd0e644d7072d005

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-09-23T12:59:05+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 354
Approved NEJobs comparison rows: 3

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 1
- Detail pages fetched successfully: 1
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 14
- Tees Valley explicitly excluded: 4
- Outside or unmapped geography excluded: 1
- Generic/derived geography rows requiring review: 1
- Retained target candidates: 10

## Outcomes
- HC: 0
- POSS: 2
- HARD_PASS: 8
- Final selected after remembered/manual actions: 0
- Final POSS awaiting decision: 0
- Manually excluded: 2
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

- None.

## POSS — choose SELECT or EXCLUDE

---
action: exclude
POSS | North East | Hybrid | £ Pro Rata | Independent Advocates (2 posts)
employer: Families in Care
closing_date: 07 October 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173435
vacancy_fingerprint: 7ce84d65a50f70779c0068075334dd37c4e7639f59edc6322add3de76435387c
source_job_id: 173435
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173435
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
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Communications & Campaigns Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173449) — confirmed JobG8 duplicate.
- [Domestic Abuse Counsellor](https://www.vonne.org.uk/vonne-jobs-details?cid=173427) — insufficient service-admin evidence.
- [Employability Advisor](https://www.vonne.org.uk/vonne-jobs-details?cid=173454) — insufficient service-admin evidence.
- [Employability Advisor](https://www.vonne.org.uk/vonne-jobs-details?cid=173453) — insufficient service-admin evidence.
- [Family Practitioner](https://www.vonne.org.uk/vonne-jobs-details?cid=173441) — out-of-scope VONNE occupation.
- [Play & Youth Practitioner- Part-Time and Casual](https://www.vonne.org.uk/vonne-jobs-details?cid=173440) — out-of-scope VONNE occupation.
- [Recovery Navigator](https://www.vonne.org.uk/vonne-jobs-details?cid=173443) — insufficient service-admin evidence.
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
