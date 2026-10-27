# JobG8 controlled release checklist — Wednesday 28 October 2026, 10:00 Europe/London

Prepared on 27 October. This is a one-off release/handover record, not a new workflow or authorization to change production. No merge, supplier switch or production publish was performed while preparing it.

## Owner-confirmed scope — takes precedence over the later release section

**Leave the live 20k feed and its normal schedules alone. Run a separate second-day 50k test only when John explicitly says to start.** The 10am chat is a handover/check-in, not an automatic trigger. It does not authorize merging PR #332, changing the production feed/secret, publishing test inventory or deploying production.

Verified after this instruction: main still has `--expected-max 20000`, with 07:30/15:30 schedules; PR #332 remains open and unmerged; the isolated test workflow has no schedule and triggers only on matching changes pushed to its explicit test branch.

### Second-day test procedure

1. Inspect the normal 20k run and live site, without changing or restarting them.
2. Await John's explicit start instruction for the separate 50k second-day test.
3. Obtain a genuinely fresh 28 October supplier test feed using the approved separate test account/connection. Record its date, timestamp, row count and hash. Do not reuse the 27 October captured fixture and call it a second-day test.
4. Adapt the isolated test harness's date-pinned fixture/review assertions to the fresh input. Its existing fixture and assertions are explicitly dated 27 October. Preserve saved decisions with their normal matching/validation; do not carry changed-job approvals blindly.
5. Keep all test outputs, review state and workflow concurrency separate from main/production. Include the final city/regional inventory fix from source head `ec47ea496fcb896d8c50ad349f05c5cec6816d24`; the old Actions test branch predates that last fix, so its previous success alone is not proof the fresh trial uses the final code.
6. Run the fresh test through GitHub Actions and save the run link. Test processing, review/selection reconciliation, job-level quarantine, build, preview packaging and live preview routes/search as appropriate. Do not repeat the 27 October investigation or reinstall an obsolete snapshot.
7. Compare the fresh results with the dated trial evidence, explaining inventory/review changes. Keep clean paying jobs unaffected by isolated bad jobs. Report completion and limits clearly.
8. If approved fresh test input cannot be accessed, identify that missing input rather than silently using yesterday's fixture, requesting secrets in chat or changing the live secret.

The normal production completed-cycle guard does **not** prevent a correctly isolated second-day test at 10am. The 15:30 timing discussion below applies only to a later, separately authorized live feed ingest/release. Do not relabel or reset a production cycle to run the isolated test.

## Evidence to read first

- [Source PR #332](https://github.com/Jopa10/ontapjobsearch.com/pull/332), tested head `ec47ea496fcb896d8c50ad349f05c5cec6816d24`.
- [Final verification report](jobg8-final-preproduction-verification-2026-10-27.md).
- [Deployed verification receipt](diagnostics/jobg8-final-deployed-verification-2026-10-27.json).
- [Saved-approval reconciliation](diagnostics/jobg8-final-approval-reconciliation-2026-10-27.json).
- [20k ceiling rollback patch](diagnostics/jobg8-restore-20000-ceilings-2026-10-27.patch).
- Successful 50k reviewed publication/full build: [run 40559394726](https://github.com/Jopa10/ontapjobsearch.com/actions/runs/40559394726).
- Final [READY preview](https://ontapjobsearch-2j34oo1gc-ontap1.vercel.app): `4d950d053179656c6d4389564e2d8c57573cf330`; 6,039 jobs including 5,477 JobG8; largest reported packaged function 219.35 MB. Both saved approved jobs/searches and Glasgow city/regional routes passed; all 21 conflicting-ID routes returned 404.

These are dated trial results, not promises of tomorrow's exact counts. Test account 825072 is separate from live account 824660. A test feed is not automatically authorized for live CPC traffic.

## First checks at 10am — before changing anything

1. Read current AGENTS.md, SYSTEM_MAP.md, SYSTEM_OVERVIEW.md and the above records. Check PR head, current main, actual live deployment version and any concurrent publishing/deployments.
2. Inspect 28 October's morning JobG8 run, follow-on review/publish/deploy, archive outcome and `pipeline/reports-daily/jobg8-daily-cycle-state.json`. Determine whether it used 20k or expanded supply, whether it actually ran or skipped, and whether a cycle is still active.
3. Capture a fresh baseline: deployed SHA/deployment ID, feed date/raw rows/unique IDs, canonical total and JobG8/NHS/Teaching Vacancies counts from the deployed snapshot, unanswered review counts by source, stale sources, current function size and the morning run URLs. Do not substitute the trial's 6,039/5,477 figures for this baseline.
4. Confirm the production supplier arrangement: expansion of the existing live URL/account versus an approved replacement URL, and the supplier's route back to 20k. No credentials in chat, logs or commits. Do not put the separate test account into production without explicit approval.
5. Confirm source PR changes are still the tested code plus any explicitly reviewed differences. Merge only the source PR; never merge either snapshot/fixture branch. Recheck current CI and merge requirements.
6. Follow the owner-confirmed isolated second-day test scope above. Production release planning below is for a later, separately authorized action; do not ask to switch production merely because the test can be started.

## Timing: 10am is after the morning cycle

The current JobG8 workflow schedules 07:30 and 15:30 Europe/London, with completion markers and duplicate-trigger protection. It supports `cycle=auto|morning|evening`, not a force-run input.

If the 07:30 morning cycle has already completed, another morning/auto dispatch at 10am will skip. Do not treat that green skipped run as a new expanded-feed test. Do not delete completion markers, falsely label a morning rerun as evening, or silently bypass idempotency.

The existing no-code route is the next genuine uncompleted cycle (normally 15:30 evening). Evening ingest does not automatically start the morning-only publication chain, so owner-authorized publication must follow it explicitly if a same-day expanded live publish is wanted. If an earlier same-day rerun is requested, prepare a narrowly scoped recovery operation for review instead of improvising a bypass. Inspect actual state first; a failed/uncompleted morning cycle may already be retryable.

## Execute only after the owner's production go-ahead

1. Record the current stable production deployment, main SHA and supplier configuration identity (no secret values). The 27 October stable reference was deployment `dpl_GrjvAP3Ko53hwzuR7CT7kEjGcyoW`, SHA `723899cb79250fd5271f9ce11053e6e3752a88f2`; refresh this on the day.
2. Merge the source PR using the normal allowed process, preserving current main updates and required checks. Deploy/import ceilings must be ready before the live feed can exceed 20k. The PR itself retains the existing live supplier URL.
3. Coordinate the authorized supplier expansion/replacement. Run one genuine eligible JobG8 cycle through GitHub Actions; save its run URL immediately. Long processing must run independently of the chat. A chat disconnection is not a reason to restart a live job.
4. Verify the fresh feed's date, row count (within 5,000–50,000), required fields, duplicate/conflict evidence, and successful dated archive upload. Preserve the exact feed/review date across later Apply Decisions steps.
5. Verify all LIVE family outputs, job-level metadata withholding, existing source-isolation safeguards, current review fanout and selected-job reconciliation. Withhold unanswered/problem jobs; do not approve them by silence, weaken selection rules or let a non-paying source block clean JobG8 supply.
6. Use the existing Apply and publish workflow. For explicit clean-inventory publication despite unanswered reviews, use the already-supported `PUBLISH_AVAILABLE` policy, not ordinary `PUBLISH` with its different unresolved-review behavior. Do not dispatch a duplicate while the automatic chain is running or has already accomplished the intended publish.
7. Let the existing verified-page/production deployment chain run. Do not promote a test snapshot as production. Confirm READY, actual packaged functions below 250 MB, and live deployment-version SHA matching the workflow's expected deployed snapshot.
8. Verify fresh source counts and compare them with the baseline; investigate an unexplained fall in clean JobG8 inventory. Test current job/detail/search/regional routes, representative CPC Apply destinations without clicking paid Apply links, and known quarantined IDs from the fresh feed.
9. Verify the post-publish source/report totals and review queue. Reconcile every still-current saved select to publication or an explicit dated exclusion/quarantine explanation. Alert sends are a separate private-test workflow; do not switch on public email alerts or send manual test emails as part of this release.

## Success and intervention criteria

Success requires fresh-feed ingest, actual archive success, clean JobG8 processing, expected approval handling, verified production READY/version, usable job/search pages, source-count reconciliation and no unexplained clean-inventory loss. A workflow dispatch or skipped green cycle alone is not success. Tomorrow's count need not equal 5,477.

A few bad/conflicting or unanswered jobs must be withheld and flagged while clean jobs continue. A known non-paying source failure, stale NEJobs, or an explained selector exclusion is not a whole-site stop.

Intervene on a genuine integrity failure: bad/mismatched feed date/schema, wrong account, inability to trust combined output, uncontained conflicts, lost eligible approvals, unexplained clean JobG8 loss, failed production build/oversize function, wrong live SHA, or broken live job/search/apply destinations. Keep the last READY production site while diagnosing. An archive failure needs explicit investigation because the daily chain requires it; do not silently drop the archive step.

## Rollback order

1. If website behavior is materially broken, restore the recorded stable production deployment through the normal release mechanism.
2. Coordinate actual supplier restoration to 20k. Keep the functioning larger ceiling until the returned feed is confirmed at or below 20k; a 20k guard rejects 50k rather than truncating it.
3. Apply the prepared six-file ceiling rollback patch, or revert the agreed release changes if complete code recovery is needed. Preserve subsequent main updates; never reset main to a historical SHA.
4. Run and validate the genuine restored 20k pipeline with consistent feed/review/archive dates, then verify production version, source totals and pages again.
5. Record actions, timestamps, run/deployment IDs and remaining isolated jobs. Website recovery, code rollback and supplier rollback are separate operations; completing one does not complete all three.

## CI assessment as of 27 October

Latest source head has **four successful and three failed PR checks**.

| Check | Finding | Release assessment |
| --- | --- | --- |
| Config/register tests and Next.js build (`test`) | Passed. Optional feed-fixture generation/audit steps were skipped because no repository fixture was present. | Useful code/build proof, not fresh-feed proof. The dedicated 50k trial supplies the replay evidence. |
| NHS `dry-run` | Passed live fetch, composition/readiness and normal-composer smoke test. No evidence commit was pushed. | No identified blocker from this check. |
| Persistent-review actions | Passed. | Supports the review/fanout change. |
| Salary fallback | Passed. | No identified blocker from this check. |
| `structured-geo` | Fails only on Ashton Under Lyne versus Ashton-Under-Lyne spelling; reproduced on original checkout. | Existing test/data-normalization mismatch, not evidence that 50k broke geography. Keep logged; do not alter geography to satisfy it during rollout. |
| Pipeline/real-feed audit/frontend | Stops because the integration workflow has no input feed fixture; later frontend step does not run. | Missing test setup. It does not replace tomorrow's fresh-feed/archive verification. Do not describe the workflow as passed. |
| Teaching Vacancies proof of concept | Live advert lacks salary/pay-scale data and the source audit fails. | External-source issue, not a JobG8 capacity failure. Withhold/isolate the affected external data and preserve clean paying publication. |
| Separately executed full frontend suite | 105/108 passed; the same three failures reproduced on original checkout: unused-indexing-capacity expectation, old navigation-markup assertion, job-sector TSX parsing in that test runtime. | Existing issues; no claim that the complete suite is green. New city/source-routing and canonical-dedup checks passed. |

**Assessment:** no observed failed CI check has been shown to be a regression caused by the expanded-feed changes. This is not a blanket waiver or proof of all production behavior. The fresh live cycle and its archive/deploy evidence remain required.

Repository rulesets API returned no rulesets, but classic main branch-protection details were inaccessible to the integration (403). Therefore whether any failed check is an enforced merge requirement is **UNKNOWN**. Respect the actual GitHub merge UI/rules on the day; do not override protection or mark failed checks successful.
