# JobG8 expanded-feed pre-production verification — 27 October 2026

Production has not been changed. Release PR: https://github.com/Jopa10/ontapjobsearch.com/pull/332 (unmerged).

## Tested revisions and input

- Release source: `ec47ea496fcb896d8c50ad349f05c5cec6816d24`.
- Final preview source/snapshot: `4d950d053179656c6d4389564e2d8c57573cf330`.
- Successful reviewed publication trial: https://github.com/Jopa10/ontapjobsearch.com/actions/runs/40559394726.
- Captured supplier test ZIP SHA-256: `34cd8f355278405f6d47ec3734b7e9e341a9f54baaec23b236b515dc5a1233d6`.
- Source timestamp: 27 October 2026, 12:31:22. This is a replay of the captured test feed, not a claim of a fresh download on each run.
- 50,000 rows; 49,977 unique reference IDs; 23 duplicate-reference groups; 21 IDs with conflicting metadata.

## Output and corrections

The final local canonical inventory contains **6,039 jobs: 5,477 JobG8, 352 NHS Jobs and 210 Teaching Vacancies**.

The trial exposed and fixed three defects on the test branch: the enrichment-specific 15-conflict abort now withholds every conflicting ID while clean jobs continue; detailed North East review regions now produce editable source blocks so saved approvals can be applied; a derived city page sharing regional slugs no longer hides LIVE configured regional inventory. The latter restored 23 Glasgow JobG8 jobs, removed none, and required no new selection decisions or LIVE register changes.

All feed loading/restoration ceilings are aligned to 50,000. The release branch contains code, tests and canonical documentation only; test fixtures and generated expanded inventory remain on separate test branches.

## Saved approval reconciliation

Counts are saved decision records by category, including historical decisions, not 1,258 jobs presumed eligible today.

| Category | Saved selects | Absent from captured feed | Published | Current selector/geography exclusion | Metadata conflicts withheld |
| --- | ---: | ---: | ---: | ---: | ---: |
| Service Admin | 1,175 | 950 | 167 | 55 | 3 |
| Support Worker | 83 | 66 | 15 | 2 | 0 |
| Total | 1,258 | 1,016 | 182 | 57 | 3 |

No saved selection with SELECTED pipeline status remains absent from the canonical inventory. No unexplained omission remains in this reconciliation. Existing exclusion diagnostics include accountant rules, missing pay, pay ceilings, excluded titles and invalid geography; these were recorded, not overridden by the audit. Both Commercial Administrator `23643_225646128` and Call Centre Advisor `23643_225673082` are present. All 21 conflicting metadata IDs remain absent.

The rebuilt trial owner queue is 389 unanswered: 321 JobG8 and 68 Teaching Vacancies. The applied Commercial Administrator no longer awaits a decision. NEJobs is explicitly STALE at 18 September, not a verified zero source. The trial uses the existing automatic `withhold` publication policy, so unanswered jobs do not block clean supply.

## Validation limits and CI status

- Successful GitHub Actions reviewed-source processing and full Next.js build, with receipt and snapshot artifact retained for 14 days.
- 33 focused Python checks passed. Five focused Node checks passed, including city/regional source ownership and canonical deduplication. An existing deduplication test import was aligned with the current source module.
- Wider frontend suite: 105 passed, three failed. The same three failures were reproduced on the original checkout: unused indexing capacity expectation, old mobile-navigation markup expectation, and job-sector TSX parsing in this test runtime.
- Additional PR CI failures were inspected: structured geography expects `Ashton Under Lyne` instead of `Ashton-Under-Lyne` (also reproduced on baseline); hybrid integration CI has no input feed fixture; a live Teaching Vacancies proof-of-concept audit encountered an advert with no pay. These are not claimed green and were not silently bypassed or changed as part of the feed test.
- The actual AWS archive upload/permissions and a real supplier-side return to a 20k live feed have not been exercised by this isolated replay.
- Final Vercel READY state, packaged function sizes and HTTP results are recorded in the accompanying final verification receipt when complete.

## Rollback — prepared, not executed

The live site before release is production deployment `dpl_GrjvAP3Ko53hwzuR7CT7kEjGcyoW`, commit `723899cb79250fd5271f9ce11053e6e3752a88f2`; the public deployment-version endpoint was verified against it during testing.

1. Coordinate JobG8 restoring the live supply to 20k if it has already been expanded. Keep the functioning ceiling until the supplier input is confirmed at or below 20k. Reducing the guard alone rejects a 50k feed; it does not truncate it.
2. Apply the prepared `restore-20000-ceilings.patch` to restore the six feed-lifecycle workflow/default files. Its application was checked against the release working tree. This can retain the unrelated review/inventory defect fixes; it reverses the limit expansion specifically.
3. Run the normal verified pipeline against the actual restored feed. Do not mix expanded-feed review decisions with a different dated archive. The isolated adapter checks already demonstrated rejection of 50k under the old limit and acceptance/health validation of 20k.
4. If immediate website recovery is required, use the recorded stable production deployment through the existing release mechanism. Restoring the website alone does not restore the supplier feed or future ingest settings.
5. For a complete code fallback, revert the release changes while preserving subsequent main updates. Do not reset main or copy the test-fixture branches into production. A separate old-code 20k rollback preview also reached READY: `dpl_FRCzHCKGuS1xGzEDwzrUD3jv4d9T`, commit `5e1aece0538536e0c5b7a948fb0f11a40b74b7f7`.

Tomorrow's remaining live evidence is the fresh supplier feed, scheduled cycle, real archive access and the normal production deployment after explicit release authorization. A preview is not production approval, and the test branches must not be merged as the release.
