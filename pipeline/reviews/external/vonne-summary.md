# VONNE ETL proof-of-concept review

review_date: 2026-11-26
review_fingerprint: 99fff2009e95c14b1db55f0a9fcb6df61ec3666b9c68cfd05baf2ab9be59258c

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-11-26T17:13:28+00:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 1139
Approved NEJobs comparison rows: 0

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 3
- Detail pages fetched successfully: 3
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 12
- Tees Valley explicitly excluded: 3
- Outside or unmapped geography excluded: 0
- Generic/derived geography rows requiring review: 2
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
POSS | North East - County Durham & Darlington/Hartlepool | County Durham | £28,000 to 30,000 Per Annum | Service Support Coordinator – Durham and Darlington Women’s Diversion Service
employer: One Small Thing
closing_date: Wednesday, December 16, 2026 - 12:00
geography: CONFIRMED — location: approved location fallback
reason: provisional transferable-office review
source: VONNE
tracking_key: vonne-173798
vacancy_fingerprint: 6ff203e830963988c1f705ee7ee1b5cfbb187fa7416f465a9351c7f1236599f2
source_job_id: 173798
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173798
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Northumberland | £25,878 to 34,240 Per Annum | Criminal Justice Recovery Coordinator
employer: Waythrough
closing_date: Thursday, December 10, 2026 - 00:00
geography: CONFIRMED — location: approved location fallback
reason: annualised upper salary £34,240 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-173799
vacancy_fingerprint: b28bf79e9ddb7f063026dea14181d075857a155467b3a1481a3b2fb8cceb2610
source_job_id: 173799
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173799
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Northumberland | £24,000 Per Annum | Strategic Network Lead
employer: Northumberland Youth Work Network (NYWN)
closing_date: 08 January 2027
geography: CONFIRMED — location: approved location fallback
reason: transferable title with specialist or borderline wording: lead
source: VONNE
tracking_key: vonne-173793
vacancy_fingerprint: 84f590da44e53115376d842e9f242c9e380b58a9b0cbc25612b621dae0e2b447
source_job_id: 173793
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173793
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Business Crime Navigator](https://www.vonne.org.uk/vonne-jobs-details?cid=173723) — insufficient service-admin evidence.
- [Service Manager - Durham and Darlington Women’s Diversion Service](https://www.vonne.org.uk/vonne-jobs-details?cid=173787) — out-of-scope VONNE occupation.
- [South Tyneside Child and Young Person Mental Health Service Counsellor](https://www.vonne.org.uk/vonne-jobs-details?cid=173730) — insufficient service-admin evidence.
- [Support and Development Officer](https://www.vonne.org.uk/vonne-jobs-details?cid=173784) — insufficient service-admin evidence.
- [Trainee Debt Adviser](https://www.vonne.org.uk/vonne-jobs-details?cid=173801) — insufficient service-admin evidence.
- [Women’s Support and Engagement Practitioner](https://www.vonne.org.uk/vonne-jobs-details?cid=173797) — out-of-scope VONNE occupation.

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
