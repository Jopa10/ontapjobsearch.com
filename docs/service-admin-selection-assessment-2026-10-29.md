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

## Corrective run result and independent final audit — 29 October 2026

Run [40893418259](https://github.com/Jopa10/ontapjobsearch.com/actions/runs/40893418259) passed all workflow steps on source `9fd67a6823a29406485f10f82471a8d075b57949`. Artifact `12911049472` was independently unpacked and compared with the unchanged baseline artifact `12893406332`. The XML SHA256 is identical to the baseline above; all 50,000 captured rows were reused.

| Source | Baseline | Corrective test |
|---|---:|---:|
| JobG8 | 5,435 | 5,908 |
| NHS Jobs | 357 | 382 |
| Teaching Vacancies | 204 | 204 |
| Total | 5,996 | 6,494 |

JobG8: 476 added, three removed, net +473. Independent comparisons of source/title/company/location/description confirm all three removed IDs remain represented by the same canonical duplicate swaps documented above. All 25 conflicted IDs remain absent. The corrective run enriched 382/382 NHS adverts successfully, unlike the first changed run's source fallback; the NHS change is not a controlled selector-only comparison. NHS composition retains its source-share cap (one Cumbria North job deferred). The final build completed successfully.

### Advert checks — concrete release blockers found

The green workflow is NOT sufficient for promotion. Inspection of supplied descriptions and a scan of newly published jobs found these counterexamples:

| Job ID | Title | Evidence / failure |
|---|---|---|
| 108218370 | Principal Database Administrator Fully Remote | Advert begins £80k–£90k and describes SQL Server/Azure/Cosmos database engineering and leading a production database estate. Newly INCLUDE_AUTOMATIC under generic administrator; salary remains missing. Both technical-role and numeric-pay safeguards have a gap. Baseline excluded for missing pay. |
| 2102520 | Group Financial Controller | Board-level group reporting/consolidation, line management and professionally qualified accountant required; £50–60k FTE in description. Baseline DAILY_REVIEW becomes automatic with missing pay. |
| 2114245 | Part time Financial Controller | ACA/ACCA/CIMA required and end-to-end statutory accounts; £65–70k FTE. Baseline DAILY_REVIEW becomes automatic with missing pay. Actual part-time earnings must not be invented from FTE. |
| 2158017 | Financial Controller | Senior Leadership Team role, qualified accountant required, £42–46k FTE; baseline DAILY_REVIEW becomes automatic. Title-only seniority correction does not catch substantive senior duties without a senior/manager token. |
| 2164943 | Payroll Analyst | Description £30.18ph rising to £39.55ph; requires degree or equivalent and payroll transformation/testing experience. Still missing pay and promoted from DAILY_REVIEW. Needs numeric parsing and specialist review, not an invented part-time annual salary. |
| 23643_225721151 / 23643_225757250 | Warehouse Administrator — Nights | Both supplied descriptions explicitly require operating forklifts/heavy lifting equipment and prior heavy-material handling. Former warehouse hard exclusions become automatic; this exceeds ordinary office administration scope. |

The original correction DOES work for `108206913`: report and canonical inventory show **£17.50–£19.00 per hour (Plus Holiday Pay)**, source description_fallback, annual upper £37,050. No weekly hours have been invented. The eight named senior part-time regressions (2101557, 2115678, 2115682, 2115685, 2115687, 2115700, 2163206, 2188775) now retain baseline DAILY_REVIEW and are absent from canonical inventory. However the controller counterexamples show the deferred-policy safeguard is incomplete.

Positive supplied-advert examples: 23643_225171007 Engineering Administrator maintains document-control records/trackers; 23643_225686176 supports hospital engineering audit records and maintenance registers; 23643_225704936 Warehouse & Logistics Administrator processes orders, data entry, invoicing and scheduling; 23643_225755118 Engineering Sales Administrator prepares quotations and orders. 2187356 Transport Planning Administrator accepts administration/operations support experience, whereas 23643_225720033 Transport Planner/Administrator explicitly requires transport-planning expertise and remains a borderline specialist case. Import/export duties in 23643_225680093 are not an import/export title; do not silently widen the existing title-based prohibition.

A diagnostic scan found 46 added IDs with blank displayed salary and at least one currency-number mention in the supplied description. This is NOT a count of 46 salary defects: some mentions are benefits, business figures or FTE and require interpretation. The definite £80k–£90k DBA example demonstrates the cap risk. Some adverts are supplier-truncated excerpts; no paid Apply URLs were clicked and no unavailable full text is claimed read.

### Approval reconciliation

There are 203 current-feed manual-select rows; 149 appear by exact JobG8 ID and 54 do not. All 54 also have EXCLUDE_AUTOMATIC in the original baseline: no newly lost exact-ID manual selections were identified. Current first-blocking reasons: 36 accountant/accountancy title exclusions, seven legal/paralegal, five Document Controller >£45k, two out-of-scope titles, one team-leader title, one IT service desk title, one salary >£50k, one unresolved town. Some IDs have conflicting title records; the earlier exceptions CSV is historical first-test evidence and must not be treated as an authoritative current title for a conflicted ID (e.g. 2055404 / 2055395 / 2055612). Conflict quarantine remains in force. No approvals or batch decisions were changed.

Selector DAILY_REVIEW is 260: 88 already SELECTED, **172 POSSIBLE_SELECTION**. Cross-source master plan is separately 290 rows, one action, 289 withheld, zero unapplied and zero action-quarantine rows. Withholding is not a permanent exclusion.

### Geography and regional reconciliation

Derby rows now resolve to Derbyshire. No selected Service Admin rows occur in the 12 corrected-town non-LIVE markets, and none of the 11 held ambiguous town labels appears as an admitted selector row. A Thornaby Account Manager appears through Customer Sales on the existing North East route; Service Admin still excludes it, so this is cross-family routing, not activation of Tees Valley Service Admin.

The saved regional report reconciles **6,494 unique jobs + 1,510 extra placements = 8,004 slice placements**; zero jobs outside governed slices and zero in non-LIVE slices. Glasgow retains 60 canonical JobG8 jobs across families. No activation register was changed by this audit.

### Final audit verdict

**NOT READY to promote this selector candidate.** The audit has found concrete numeric-description, specialist/qualified-finance and physical-warehouse exceptions despite a successful build. Preserve all captured inputs, baseline and current results. Repair narrowly within the approved safeguards and repeat the same-input comparison before preparing a release candidate; do not solve these by silently approving jobs or inventing policy. No source-only PR is prepared as release-ready from this result. Production remains 20k, and no main merge, deployment, supplier switch, market activation, schedule change, job approval or email occurred. Friday's separate expanded-feed release checks and explicit owner approval remain necessary.



## Owner-authorised safeguard repair — 29 October 2026

After the final advert audit, the owner authorised fixing item 1; approval/geography findings require no change. The isolated follow-up changes only Service Admin source safeguards/tests and canonical documentation:

- Recover explicit salary headings such as £80k–£90k, £27,000 plus benefits and FTE ranges; retain FTE/pro-rata basis. Recover £30.18ph increasing to £39.55ph, including intervening umbrella-basis wording, and use both rates for upper-pay checks. Currencyless acidity pH, benefit amounts and stated business budgets are counterexamples, not salary. Existing numeric structured pay and additional wording keep priority.
- Treat database/system administrator titles as technical IT work. Mandatory professionally qualified accountant (ACA/ACCA/CIMA) duties cannot pass through a part-time finance title. Financial Controller and specialist finance/payroll analyst duties retain review where not already excluded by pay/qualification safeguards. Ordinary AAT, payroll and credit-control office duties stay eligible, including missing pay.
- Warehouse-title exceptions do not admit adverts explicitly requiring forklift/heavy-equipment operation; ordinary stock records, order processing and liaison with forklift drivers still pass.

Validation before submission: 96 targeted title/pay/geography/duties checks passed, plus 33 importer/quarantine/North East/review-isolation checks. The seven concrete bad examples from the saved corrective artifact are all excluded when replayed through the patched selector; the Engineering Administrator, Warehouse & Logistics Administrator and Payroll Administrator counterexamples remain automatic. Payroll Administrator 108206913 retains £17.50–£19.00/hour (Plus Holiday Pay), annual upper £37,050. Payroll Analyst 2164943 now retains both £30.18 and £39.55 hourly rates; normal full-week annual upper is £77,122.50, not invented actual part-time earnings.

The local replay uses unchanged advert contents with a fixed known LIVE test town to isolate title/pay/duties behaviour; it is not a final published count or geography comparison. Full comparison must use the unchanged captured XML and original successful baseline via the existing isolated workflow. No new owner approvals, geo/register changes, production changes, deployment or supplier access are included. The last 5,908 JobG8 result remains evidence for the previous source, not a result for this repair. Release readiness remains pending the new full run and artifact audit.

Safeguard-repair comparison started: [run 40912470494](https://github.com/Jopa10/ontapjobsearch.com/actions/runs/40912470494), tested source `41cfa924cba48e9c8b39b762c9f338c1947be6af`. This supersedes 40893418259 for release validation; no result claimed yet.
