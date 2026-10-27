# JobG8 expanded feed test — 27 October 2026

Status: INCOMPLETE. Production feed and production code have not been changed. No deployment or alert sending performed.

## Baseline from owner screenshots
- Live unique jobs: 4,144; JobG8: 3,615; other sources: 529.
- Slice placements: 4,952; jobs across multiple slices: 799; extra placements: 808.
- Jobs outside governed slices: 0; jobs in non-LIVE slices: 0.
- Existing input: 20,000 jobs.

## Confirmed test findings
- Separate TEST account 825072 supplied exactly 50,000 jobs, rather than anticipated 44,000.
- First successful download: 36,967,263 ZIP bytes; Jobs.xml: 176,005,196 bytes; approximately 11.9 seconds download.
- Initial downloaded file subsequently failed reopening as ZIP. A fresh download was obtained and its ZIP CRC integrity test passed. Cause of initial local file issue not established.
- Existing native XML adapter converted all 50,000 rows successfully, 31 columns, in 28.6 seconds on this workspace. Test invocation explicitly set expected-min/max to 50000; production limits unchanged.
- Preserved feed timestamp: 2026-10-27T12:31:22.
- Existing feed-health validation PASSED on all 50,000 rows: reference, title, advertiser, area/location, application URL and description all 100% populated; application URLs 100% valid http(s); references 100% unique.
- Production daily workflow and existing direct-fetch test both retain expected-max 20000. Existing direct-fetch test reads the LIVE secret, so must not be dispatched unchanged for this trial.
- next.config.ts contains exclusions for pipeline archives, external manifests/reviews and large decision reports. Deployment size has NOT been verified for the expanded feed.

## Current execution / resume
Isolated local checkout: /workspace/scratch/adf0f4fc1910/feed-test/repo.
Validated download: /workspace/scratch/adf0f4fc1910/feed-test/verified.zip.
Converted workbook: checkout pipeline/input/jobg8.xlsx.
50k Service Admin selector launched in isolated checkout via python -m scripts.service_admin_pipeline_north_yorkshire. Its completion/result is not yet confirmed. Log: /workspace/scratch/adf0f4fc1910/feed-test/selection-50000.log. Session 17347.

## Still outstanding
- Confirm selector completion and inspect review and selection counts.
- Run staged selection comparisons at 20k/25k/30k/35k/44k/50k from the same captured feed, preserving separate outputs and timings.
- Compare potential duplicates, review volume, selected inventory and geography/family gains.
- Verify full composition/build and function sizes in isolation before claiming production readiness.
- Save further results on this branch. Do not switch the production feed without owner approval.

Raw feed URLs/credentials must not be committed. No production readiness conclusion yet.
