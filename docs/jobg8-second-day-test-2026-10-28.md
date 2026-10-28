# Isolated second-day 50k technical test — 28 October 2026

Status: STARTED, not yet passed. Check actual Actions status before continuing or retrying.

- Run: https://github.com/Jopa10/ontapjobsearch.com/actions/runs/40663109840
- Run SHA: c05b8f73bbbb39eb6854fb412df39e97cf9141b6
- Source code: ec47ea496fcb896d8c50ad349f05c5cec6816d24, including final Glasgow/city-regional inventory fix.
- Saved review data: copied from main d58b6b217df17dd2e31972f07e2bdd296e3803ac before the fresh first-pass selection. Normal fingerprint/carry-forward and withhold policy apply. No new owner decisions invented.
- Fresh supplier test account: 825072. Download obtained today; ZIP integrity passed. Source Jobs.xml timestamp 2026-10-28 08:54:44; 50,000 rows, 49,974 unique reference IDs.
- ZIP SHA-256: 256b177a1cd1832625a8d2f756de7abd48fdde5b93262ae81a83f52e8f8e6890
- XML SHA-256: c80a44b9d22d15a561f19918337801f66efb897941726972bf2ff4656ed0bdc9
- This is a newly captured 28 October supplier input, not yesterday's replay.

## Scope and retained results

The unscheduled push-triggered workflow uses its own branch and concurrency group, with read-only contents permission and no deployment/email/production-write steps. It processes fresh JobG8 input, applies existing saved decisions with unanswered jobs withheld, composes isolated app output, checks metadata conflict withholding, generates the canonical search inventory and daily regional overview, runs a full Next.js build, and packages a snapshot. Results and logs are retained for 14 days in artifact `jobg8-fresh-50k-2026-10-28-results`.

Receipt: `test-results/receipt.json`. Regional report/workbook: `test-results/daily-region-overview-50k-2026-10-28.md` and `.xlsx`. A snapshot is available if the pipeline reaches packaging. Read step logs/receipt for exact completion and limits. No preview deployment or HTTP-preview verification is included in this run; no real AWS archive upload is included. External source data may be retained from the approved source snapshot.

## Production baseline checked read-only

Normal 20k ingest 40650593299, Apply/publish 40655067964, verified pages 40657953701, deployment 40658276284 and regional overview 40659211852 all completed successfully today. The separate daily-status run 40655078560 was failed; it is not presented as green. Main retains expected-max 20000 and 07:30/15:30 schedule, with today's morning cycle recorded complete. No production merge, supplier switch, deployment or schedule change was made for this test.

## Resume after interruption

1. Open the run above and check actual status; do not start another trial merely because chat disconnected.
2. If running, let it continue. If failed, inspect the precise failed step and saved receipt/artifact before a targeted fix or retry.
3. If successful, download the artifact, reconcile fresh inventory/reviews/quarantine and Glasgow, inspect the regional overview, and report results and remaining limits. Processing/build success alone is not a production-release authorization.
4. Production remains at 20k. No merge, feed switch or production deployment is authorized.
