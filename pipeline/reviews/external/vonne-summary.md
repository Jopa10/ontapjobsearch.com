# VONNE ETL proof-of-concept review

review_date: 2026-09-18
review_fingerprint: 8a15317104c45b7917bd81c584625c05d475f58b047912c43c0d9e25235f207e

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-09-18T12:39:26+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 188
Approved NEJobs comparison rows: 7

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 0
- Detail pages fetched successfully: 0
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 15
- Tees Valley explicitly excluded: 3
- Outside or unmapped geography excluded: 1
- Generic/derived geography rows requiring review: 1
- Retained target candidates: 11

## Outcomes
- HC: 0
- POSS: 2
- HARD_PASS: 9
- Final selected after remembered/manual actions: 0
- Final POSS awaiting decision: 2
- Manually excluded: 0
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

- None.

## POSS — choose SELECT or EXCLUDE

---
action:
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
action:
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £ Per Annum | Support Worker - Young People's 16+ Supported Accommodation - Gateshead
employer: Oasis Community Housing
closing_date: 30 September 2026
geography: CONFIRMED — location: exact area
reason: possible cross-source duplicate requires review
source: VONNE
tracking_key: vonne-171330
vacancy_fingerprint: 45a5414b40fbfeff791b6b1d7a1c75f8d886794387d67eee5bf61d48a68f5960
source_job_id: 171330
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=171330
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Chief Executive Officer (CEO)](https://www.vonne.org.uk/vonne-jobs-details?cid=173422) — out-of-scope VONNE occupation.
- [Community Cancer Awareness Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173418) — out-of-scope VONNE occupation.
- [Community Link Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173419) — out-of-scope VONNE occupation.
- [Domestic Abuse Counsellor](https://www.vonne.org.uk/vonne-jobs-details?cid=173427) — insufficient service-admin evidence.
- [Family Practitioner](https://www.vonne.org.uk/vonne-jobs-details?cid=173441) — out-of-scope VONNE occupation.
- [Language & Learning Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173423) — insufficient service-admin evidence.
- [Money Advice/Debt Caseworker](https://www.vonne.org.uk/vonne-jobs-details?cid=173416) — out-of-scope VONNE occupation.
- [Play & Youth Practitioner- Part-Time and Casual](https://www.vonne.org.uk/vonne-jobs-details?cid=173440) — out-of-scope VONNE occupation.
- [Recovery Navigator](https://www.vonne.org.uk/vonne-jobs-details?cid=173443) — insufficient service-admin evidence.

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
