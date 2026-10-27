# Full-chain trial: conflict fix and rollback evidence

The real full run exposed a blocker omitted from the earlier snapshot build: metadata enrichment aborted at 21 conflicting DisplayReference IDs because of its 15-ID ceiling. Raw XML contains 50000 rows, 49977 unique references and 23 duplicate-reference groups; 21 groups have conflicting enrichment metadata. Earlier rounded 100.0% uniqueness reporting must not be interpreted as all IDs unique.

Four selected jobs across five slice rows were affected. Owner explicitly approved withholding every conflicting ID while allowing clean inventory to continue, rather than increasing the arbitrary threshold. Fix commit 4f975c0916145a793b605f0465439b8e79e20664 on unmerged PR #332 implements that narrow change with canonical docs. All 10 focused pytest checks passed. Real 50k admin enrichment now passes: 21 IDs quarantined, 5 rows withheld, 6686 remaining rows enriched. Support Worker selection/enrichment also passed. No conflicted metadata is selected arbitrarily.

Duplicate report completed in 796.58 seconds; all-live-family selection completed in 1174.13 seconds. Full run is not yet complete; subsequent coverage/review/composition/build stages are still being verified.

Rollback: old 20k guard rejects full 50k safely before writing a workbook; accepts a 20000-row prefix of this same real feed. Its regenerated workbook passed health validation. One initial temporary rollback workbook was unreadable; the failed attempt is preserved in receipts, followed by successful regeneration and validation. Exact reason for that temporary artifact issue is not established.

Original pre-change commit 5e1aece0538536e0c5b7a948fb0f11a40b74b7f7 was deployed separately to Vercel PREVIEW and reached READY: dpl_FRCzHCKGuS1xGzEDwzrUD3jv4d9T, https://ontapjobsearch-859s92kpl-ontap1.vercel.app. This verifies original saved-site deployment, not restoration of supplier-side feed limits. A supplier-side expansion would still require JobG8 to restore the 20k supply during rollback; lowering the guard alone rejects a 50k feed.

Production and live supplier feed unchanged. No main merge, production publish or alert send performed.
