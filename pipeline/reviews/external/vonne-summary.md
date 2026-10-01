# VONNE ETL proof-of-concept review

review_date: 2026-10-01
review_fingerprint: 9159716e6238e0559296622724a42ee599cde9e8d10acb28fc8395034bf0bb73

This implementation is review-only. It has no approved-JSON or publishing mode.

Edit only the `action:` line in editable blocks:
- `action: select` promotes a POSS vacancy for discussion.
- `action: exclude` rejects a POSS vacancy or removes an HC vacancy.
- Actions are remembered while the same vacancy review facts remain unchanged; this review still does not publish anything.

Run generated: 2026-10-01T14:45:50+01:00
Listing input: https://www.vonne.org.uk/vonne-jobs
JobG8 comparison rows: 354
Approved NEJobs comparison rows: 0

## Funnel
- VONNE listings read: 15
- Detail-page candidates: 2
- Detail pages fetched successfully: 2
- Detail failures/listing fallbacks: 0
- Obvious hard passes not detail-fetched: 13
- Tees Valley explicitly excluded: 0
- Outside or unmapped geography excluded: 2
- Generic/derived geography rows requiring review: 2
- Retained target candidates: 13

## Outcomes
- HC: 0
- POSS: 4
- HARD_PASS: 9
- Final selected after remembered/manual actions: 0
- Final POSS awaiting decision: 4
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
---
action:
POSS | North East | Hybrid | £24,480 Per Annum | Project Assistant
employer: North East Chamber of Commerce
closing_date: 27 October 2026
geography: GENERIC_REVIEW — generic VONNE location requires manual North East check
reason: North East geography is generic or derived and requires review
source: VONNE
tracking_key: vonne-173489
vacancy_fingerprint: 614f3aa276c1067c98c18edf1a0144b16bb8bf36311bd7826b4c62486ff7f4ba
source_job_id: 173489
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173489
---
---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Darlington | £31,000 Per Annum | Shared Lives Carer in Darlington
employer: St Annes Community Services
closing_date: 01 November 2026
geography: CONFIRMED — location: exact area
reason: annualised upper salary £31,000 exceeds North East review point £30,000
source: VONNE
tracking_key: vonne-172562
vacancy_fingerprint: eb8b793916af3ab9b99e3ea1b533e1e9d92fb19db6343aaff2e2319719a7dba1
source_job_id: 172562
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=172562
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Tyne and Wear | £20,035 Per Annum | Digital Coordinator
employer: Hospitality and Hope
closing_date: Thursday, October 8, 2026 - 00:00
geography: CONFIRMED — location: approved location fallback
reason: provisional transferable-office review
source: VONNE
tracking_key: vonne-173475
vacancy_fingerprint: e89ee63e825c9e69ed1079063e87337212bf17209237b827b80cf63d8286e53f
source_job_id: 173475
source_url: https://www.vonne.org.uk/vonne-jobs-details?cid=173475
---
## EXCLUDED BY REVIEW

- None.

## HARD_PASS

- [Age Friendly Engagement Co-ordinator](https://www.vonne.org.uk/vonne-jobs-details?cid=173472) — insufficient service-admin evidence.
- [Community Health Activator - Researcher (CHAR)](https://www.vonne.org.uk/vonne-jobs-details?cid=173467) — insufficient service-admin evidence.
- [Grants and Funding Manager](https://www.vonne.org.uk/vonne-jobs-details?cid=173425) — out-of-scope VONNE occupation.
- [Learning Disability Skills Specialist (Part Time)](https://www.vonne.org.uk/vonne-jobs-details?cid=172581) — insufficient service-admin evidence.
- [Parent Carer Project Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173466) — out-of-scope VONNE occupation.
- [Recovery Coach](https://www.vonne.org.uk/vonne-jobs-details?cid=173464) — insufficient service-admin evidence.
- [Recovery Coach](https://www.vonne.org.uk/vonne-jobs-details?cid=173463) — insufficient service-admin evidence.
- [Team Leader - All-Age Caregivers](https://www.vonne.org.uk/vonne-jobs-details?cid=173477) — insufficient service-admin evidence.
- [Young Carer Support Worker](https://www.vonne.org.uk/vonne-jobs-details?cid=173481) — out-of-scope VONNE occupation.

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
