# VONNE ETL proof-of-concept review

review_date: 2026-10-12
review_fingerprint: 8b2f8bd614d9da734e0b526915008f466419c54b326aa4d6c2f4a94a7c56e815

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-10-12T16:55:22+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 290
Approved NEJobs comparison rows: 0

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 6
- Detail pages fetched successfully: 6
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 9
- Tees Valley explicitly excluded: 0
- Outside or unmapped geography excluded: 2
- Generic/derived geography rows requiring review: 2
- Retained target candidates: 13

## Outcomes
- HC: 2
- POSS: 9
- HARD_PASS: 2
- Final selected after remembered/manual actions: 2
- Final POSS awaiting decision: 9
- Manually excluded: 0
## Detail diagnostics
- No unresolved detail-page failures.

## SELECTED

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £24,796 to 28,153 Per Annum | Administrator (VAWG TEAM)
employer: The Angelou Centre
closing_date: Saturday, October 31, 2026 - 05:00
geography: CONFIRMED — location: approved location fallback
reason: clear transferable title: administrator
source: VONNE
tracking_key: vonne-173521
vacancy_fingerprint: 6bde09698b989e1267db4b77ce6013d78818bfcbc18d48a2533b8d50c9d4eef6
source_job_id: 173521
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173521
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £25,880 Per Annum | Contact Centre Adviser - Consumer
employer: Citizens Advice Gateshead
closing_date: Friday, October 23, 2026 - 09:00
geography: CONFIRMED — location: approved location fallback
reason: clear transferable title: contact centre
source: VONNE
tracking_key: vonne-173530
vacancy_fingerprint: 48a133cf6dd62ccaf528f1e4c9ae33813dd3f80af77a8f77feab91e62a7f965a
source_job_id: 173530
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173530
---
## POSS — choose SELECT or EXCLUDE

---
action:
POSS | North East | Hybrid | £ | Are you an excellent communicator with a passion for helping others? We have the perfect opportunity !
employer: Social Welfare Adviser
closing_date: 23 October 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173531
vacancy_fingerprint: b07b5d977c969bd85ed2e92be19e6bd5627a46bb321866006adf1e8eb17ea0a0
source_job_id: 173531
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173531
---
---
action:
POSS | North East | Hybrid | £51,928 Per Annum | Could you lead the next chapter of Community Action Northumberland?
employer: Chief Executive
closing_date: 02 November 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173526
vacancy_fingerprint: 4fcc153ec86848d32ff2901cf66ca179190c941e10f722c0db25bdaf508ae482
source_job_id: 173526
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173526
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £33,323 Per Annum | Business Support Coach
employer: Society Matters CIC
closing_date: 02 November 2026
geography: CONFIRMED — location: exact area
reason: annualised upper salary £33,323 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173500
vacancy_fingerprint: e5d14a4bd7e6bcd346e2effe5bb567c7379d7782f9597b4e2a2cfc17e4639d77
source_job_id: 173500
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173500
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £28,366 to 31,518 Pro Rata | Grant Holder Support Officer
employer: Voluntary and Community Action Sunderland
closing_date: Monday, October 26, 2026 - 17:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £31,518 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173508
vacancy_fingerprint: 8299e3d1056736b8272504c0f62b20d222e5d414101af412de37dad17b8b5368
source_job_id: 173508
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173508
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £28,366 to 31,518 Pro Rata | Grant Holder Support Officer
employer: Inspire South Tyneside
closing_date: Monday, October 26, 2026 - 17:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £31,518 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-172176
vacancy_fingerprint: 9e86bf11e8f53d9040f1830cca6e2ffd94d6c09c03bf3f929c00c3e644a1f406
source_job_id: 172176
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=172176
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £28,366 to 31,518 Pro Rata | Grant Holder Support Officer
employer: North Tyneside VODA
closing_date: Monday, October 26, 2026 - 17:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £31,518 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173497
vacancy_fingerprint: 75468d164acfac9275b9bfbe745f8d272212d8fb197101a8c7a81b3e1fa2f7a8
source_job_id: 173497
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173497
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £30,303 to 35,781 Per Annum | Housing Coordinator
employer: The Angelou Centre
closing_date: Saturday, October 31, 2026 - 05:00
geography: CONFIRMED — location: approved location fallback
reason: possible cross-source duplicate requires review
source: VONNE
tracking_key: vonne-173522
vacancy_fingerprint: 61c24dc341e1a13672ae87098d2c61e64cb2480c2d25c2dd52f8d24aa08c9c73
source_job_id: 173522
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173522
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | South Tyneside | £15 Per Hour | Project Lead (STARCH)
employer: Churches Together in South Tyneside
closing_date: 30 October 2026
geography: CONFIRMED — location: geography phrase: south tyneside
reason: transferable title with specialist or borderline wording: lead
source: VONNE
tracking_key: vonne-173401
vacancy_fingerprint: 4921c718296e6f405987f2a4bd1abab5f3d27cdad2440f10f086adf8ffd317fd
source_job_id: 173401
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173401
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £50,565 Per Annum | Solicitor
employer: Citizens Advice Gateshead
closing_date: 30 October 2026
geography: CONFIRMED — location: exact area
reason: possible cross-source duplicate requires review
source: VONNE
tracking_key: vonne-173501
vacancy_fingerprint: a88d73601f7b6d5f1dbbeabde86760e2454307e9b03d45a1b838d07686248076
source_job_id: 173501
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173501
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Children and Young People’s Mental Health](https://www.vonne.org.uk/vonne-jobs-details?cid=173496) — insufficient service-admin evidence.
- [Interim Chief Executive Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173518) — out-of-scope VONNE occupation.

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
