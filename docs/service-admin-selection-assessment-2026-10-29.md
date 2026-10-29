# Service Admin selection comparison — 29 October 2026

## Tested result, not production approval

Run [40869488844](https://github.com/Jopa10/ontapjobsearch.com/actions/runs/40869488844) passed on tested source `0ae994fccdee924082bc5f3b594c664392cda599` at 13:33 UTC. Artifact [12900862757](https://github.com/Jopa10/ontapjobsearch.com/actions/runs/40869488844/artifacts/12900862757) contains receipts, full captured input, packaged inventory, before/after CSVs, report/workbook and build log. The unchanged baseline is run `40848659957`, artifact `12893406332`. Both used XML SHA256 `b46f114fc60c511d68283576cbc2bb235add929da638b747da05a12e0a016c83` (50,000 rows). Independent packaged canonical totals match receipts.

| Inventory | Before | First changed test |
|---|---:|---:|
| JobG8 | 5,435 | 5,917 |
| NHS | 357 | 336 |
| Teaching Vacancies | 204 | 204 |
| Total | 5,996 | 6,457 |

JobG8 gained 485 IDs and lost three IDs, a net gain of 482. All three removed IDs have exactly equal source/title/employer/location/full-description fingerprints to surviving copies: `2133805 → 2133802`, `2157921 → 2157920`, `2179530 → 23643_225761668`. The existing canonical deduplication therefore retained the vacancies. Supplier Apply URLs differ and no Apply link was clicked.

Of 485 added JobG8 IDs, recorded first-blocking reasons were: blank-pay exclusion 279; title no-match 87; missing town 37; outside target region 15; industry keyword engineer/warehouse/transport/manufacturing 22; part-time-pay/other review pathways 45. These are first recorded reasons, not exclusive root causes. Service Admin selector DAILY_REVIEW outcomes fell 362 to 251 (includes 88 already selected); unanswered POSSIBLE_SELECTION rows were 163. These are selector counts, not the cross-source master review total: reviewed plan reports 281 rows, one action and 280 withheld, zero unapplied actions. All 25 conflicted JobG8 metadata IDs remain absent. Forty town lookup corrections include 12 non-LIVE destination markets, which remain inactive.

NHS is not a stable-control comparison here. The baseline enriched 357/357 accepted adverts; the changed run encountered four description-enrichment failures among 374 requested adverts and isolated NHS, retaining its pre-existing approved 336-job state. No cap deferrals or fresh-duplicate withholding occurred in that fallback. JobG8 continued successfully. Do not attribute the NHS reduction to a deliberate source-policy change.

## Remaining corrective validation

Independent source review found two release-relevant seams:

1. Nonnumeric SalaryAdditional (e.g. Plus Holiday Pay) concealed numeric description pay. Thirteen full-feed records had that shape; the eligible Service Admin example was `108206913`, Payroll Specialist / Payroll Administrator, with £17.50–£19.00/hour. The follow-up patch recovers numeric description pay only when structured numeric amounts are absent, retains additional wording, and tests £50k and Document Controller £45k guards. Numeric structured supplier values retain priority.
2. The first missing-pay patch also automatically promoted some previously reviewed senior part-time finance roles. This interacts with the deferred seniority policy. The follow-up patch preserves the original review for part-time titles containing senior/manager/lead/leader/head/director/chief when pay is missing. Ordinary eligible missing-pay roles still pass. Preliminary 5,917 is therefore not the final candidate count.

The follow-up changes pass 65 targeted title/pay/geography checks locally; the original first test passed its own focused checks and full build. The broader structured-geography suite has a separately reproduced baseline display-spelling failure (Ashton Under Lyne vs Ashton-Under-Lyne). It is not claimed resolved.

Newly included engineering/warehouse/transport/manufacturing adverts were inspected from supplied full descriptions where available. Examples 23643_225171007 (engineering records/document control), 23643_225680093 (aftersales orders/spares/customer support), 23643_225704936 (warehouse order records/data entry) are administrative. Mixed planner/admin roles and specialist finance cases remain review risks. Some supplier descriptions are truncated excerpts ending click apply for full job details; do not claim those are complete adverts. Existing classifier limitations, such as an Accounts Assistant performing tax preparation, are not resolved by a salary change.

For source selections, 203 current-feed rows have a manual select/include marker; 54 are absent by exact ID, many because existing hard rules override earlier approvals or because canonical deduplication applies. Their current and baseline recorded reasons are preserved in `service-admin-selection-approval-exceptions-2026-10-29.csv`. No new approval/exclusion decisions are recorded by this audit. The three baseline published JobG8 losses are explained above; every other baseline published JobG8 ID remains canonical. Glasgow canonical inventory remains present (60 jobs across families).

## Verdict

NOT READY to promote the first tested patch: follow-up salary/seniority changes require a new same-input comparison and final advert/approval-exception review. Production stays at 20k. No main merge, deployment, supplier switch, activation, schedule change, job approval or email has occurred. After satisfactory validation, prepare a source-only candidate onto current main; never merge fixture or generated inventory branches. Separate HTTP/function-size/archive/supplier-account/rollback readiness and explicit owner release approval still apply for Friday.
