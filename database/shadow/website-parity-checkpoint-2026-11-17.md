# Tuesday 17 November 2026 — Neon Preview migration checkpoint

Status: **Full Tuesday SELECT/REVIEW payload write/readback and full-feed selector parity passed. The website storage blocker is resolved, a complete Neon-backed Preview build passed, and final comparison against the completed Tuesday website publication is in progress. Preview safeguards, EXCLUDE retention boundaries and real Neon rollback verification passed. Production remains unchanged.**

## Exact Tuesday source and production reference

- Production JobG8 run: **44039319889**, successful; selector/app source revision **6e001e11000854fd211f984c7d4db9f8b40e51e1**.
- PR #342 (optional qualifications and overlapping salary ranges) is merged and its merge is an ancestor of that production revision.
- Post-publication review files were refreshed by commit **c3073794abc4b3246a4504434b2366fee2bfaba1**, a descendant of the production revision. The first test attempt used the pre-publication review snapshot and was corrected.
- Saved source: `jobg8/raw/2026-11-17.zip`; SHA-256 **8638a31e4baca46665fed119fc2ddb227e48959a5da3b055189ae41d6ed55486**.
- Feed contained **40,395 Job nodes**.
- Production artifacts:
  - `service-admin-output`: ID **14311541647**, SHA-256 `4810e5e48995767e5db4f234b5defde7aaa01907abea56239769d010bcaa6f71`.
  - `support-worker-output`: ID **14311691542**, SHA-256 `09bfd854487b24e2ded737285d26503799b03dba9eb296a9ac5a4802080dd369`.

## Neon Preview full-payload test

Successful workflow: **44061689853**; evidence artifact **14318955715**; Preview verifier deployment `https://ontapjobsearch-8ziqubbsu-ontap1.vercel.app`.

- **5,372 SELECTED IDs** and **206 review-list IDs** were prepared. After 17 overlaps with SELECTED, Neon contained **5,561 distinct records**, including **189 REVIEW-only records**.
- **21,414,231 payload bytes**; exact IDs, full payload hashes, decision reasons, selector revision, and archived feed-row positions all matched on readback.
- EXCLUDE payloads stored: **0**.
- Existing 11 November snapshot remained unchanged: **5,491 records**.
- Neon size: **650,870,784 → 668,901,376 bytes**; growth **18,030,592 bytes**; remaining headroom above the protected reserve: **102,850,560 bytes**.

## Website Preview attempt

Workflow **44059470460** used Tuesday production artifacts as the immutable comparison reference and selected rows read from Neon. Its preflight verified the selected IDs and Apply URLs, then stopped at the explicit **“Insufficient Neon test database headroom”** guard in `build-latest-preview.mjs`, before writing `published_scope_rows` or running the Next.js site build. No safeguard was bypassed. The final Neon database has even less headroom than at that attempt, so do not repeat this build until the site snapshot storage estimate is reduced or the approved database capacity changes.

## Remaining gates

1. Run daily Neon refreshes on at least two more publication days to verify that the date follows the current feed and that retention/expiry behaves as intended; Tuesday alone does not prove rollover.
2. Finish a separate rule-change replay against the exact Tuesday feed. Tuesday production used the merged rules and Neon holds those production decisions, but no isolated before/after ID comparison was completed. The PR #336 branch’s selector core is stale relative to PR #342, so do not use it as the revised-rule replay until aligned to the production source.
3. Complete Neon-backed website route/build, scope ordering, external-source composition, and SEO checks after resolving the headroom blocker. Tuesday’s attempt did not establish full website parity.
4. Test production safeguards and rollback before any cutover.

## Guardrails and branch state

- Preview only. No production publishing or production data changes.
- PR #336 remains draft, open, and unmerged.
- Keep the current daily publishing process and SEO requirements unchanged.


## Full-feed Python selector replay — completed 17 November

Successful Preview-only workflow: **44065809719**; evidence artifact **14321382604**.

- Reused the exact saved feed `jobg8/raw/2026-11-17.zip`, SHA-256 `8638a31e4baca46665fed119fc2ddb227e48959a5da3b055189ae41d6ed55486`.
- Ran the exact production selector revision used for Tuesday’s publication: `6e001e11000854fd211f984c7d4db9f8b40e51e1`. Input was the full feed in its original row order; the Tuesday production outputs were comparison references only.
- Comparator result: **PASS** across **256 scopes**; **0 scopes with differences**; **5,372 unique JobG8 IDs** in both the replay and production reference; **0 missing** and **0 extra** IDs. Scope membership and JobG8 ordering matched exactly.
- Production artifacts were downloaded and their SHA-256 digests verified against the pinned values above.
- The feed emitted duplicate-metadata quarantine warnings for IDs **644940444** and **644940753**; these caused no difference against Tuesday’s published output.
- No Neon write, production publish, rule edit, PR merge, or production change occurred in this test.

This completes the full-feed selector replay/parity check. It does not replace the outstanding Neon-backed website build, multi-day daily-refresh/expiry checks, the separate counterfactual rule-change comparison, or production-safeguard/rollback checks.

## Follow-on tests authorised 17 November

### Storage blocker and first successful full website build

- Resolved the headroom blocker by storing one gzip-compressed, SHA-256-verified publisher snapshot in `ontap_shadow.publisher_snapshots`; retained the 800 MiB ceiling and 64 MiB reserve.
- Workflow **44071501186** passed; evidence artifact **14323187865**; deployment **dpl_2LriLpZGD1ava8XsZf729CLC7Vgp** READY.
- **6,990 publisher rows**, including **6,680 JobG8 scope occurrences / 5,372 unique JobG8 IDs** and **310 external-source occurrences**, read back exactly across **256 scopes**.
- Original snapshot bytes **24,309,971**; compressed **5,601,670**; database after write **680,615,936 bytes**.
- Existing publisher/city code generated **66 active city pages / 1,342 city entries** and Next.js generated **6,036 static pages**.
- This first build used the 08:20 review snapshot for website/config source and selector-time external inputs. It proves storage/readback/build, but is not the final website parity reference.
- Final website parity must use completed Tuesday publication commit **dc31cdb5ca846cc29f712700a59f80d807cf4912** (09:14), with approved external-source pipeline outputs from that same commit. JobG8 IDs/order must still match the pinned selector artifacts. Workflow **44073576579** is the current final-comparison run.
- Diagnostic intermediate workflow **44073443578** used the earlier website reference and its obsolete Preview deployment was cancelled once the correct completed-publication reference was pinned.

### Safeguards, three-day EXCLUDE window, and actual Preview rollback

Workflow **44072468086**, evidence artifact **14323811386**, passed.

- **7/7** meaningful isolated tests passed: reject production/wrong Neon project/no TLS; reject storage over budget; reject stale dates across rollover; exact compressed ID/payload/position readback and corrupt snapshot rejection; EXCLUDE payload retained through day two and purged exactly on day three; eligible return clears exclusion timer; outside-feed exclusion rejected without payload loss.
- EXCLUDE boundary tests used isolated PostgreSQL-compatible fixtures and the existing `applyExcludeReviewWindow` implementation. They did not purge existing Neon evidence.
- Real Neon rollback probe deliberately altered a checksum inside a transaction, confirmed readback rejection, rolled back, and verified the previous **6,990-row** snapshot exactly by checksum and payload. **0 permanent writes** from the probe. Database size **680,624,128 bytes**.
- This verifies Preview database rollback, not a production traffic rollback/cutover drill.

### Full-feed before/after rule replay

- Implemented a separate workflow comparing Tuesday's exact production selector checkout with only the two approved rule files restored to pre-PR-342 revision **eac8997cc3a48cc1ce3cbee16c77faffc3e4ec8f**.
- Confirmed both production rule-file blob SHAs exactly equal the merged PR-342 versions, so this isolates the approved changes.
- Planned evidence includes every service-admin audit decision, all output scopes, exact changed IDs, eligibility/rank effects, revised-output parity against Tuesday's production artifact, and changed-decision Neon write/readback plus existing full-payload hash verification.
- Runs **44071842938** and **44072034435** both stopped at archive transport (HTTP 400), before selectors or Neon writes. The second attempt normalized the signed URL consistently with the earlier successful harness.
- **Blocked: owner must renew GitHub Actions secret `ONTAP_SAVED_FEED_URL` for the exact archive `jobg8/raw/2026-11-17.zip`.** Do not claim the before/after rule replay passed or use the selected-only subset as input.

### Subsequent daily checks and retention distinction

- Enabled three follow-up checks for **18, 19 and 20 November**, around **10:00 Europe/London**, after normal publication.
- Derive the date from each completed feed/publication, reuse saved selector evidence, then test latest-date readback, returning/absent IDs, duplicates, payload updates and retention.
- Existing policy from `retention-assessment-2026-11-03.md`: selected/review advert evidence retained **90 days after inactivity**, permanent public identity preserved, expired adverts must not expose an active Apply link; EXCLUDE payload review window is separately **3 days**.
- The current selected/review daily snapshot table is not yet proof of master-advert inactivity/expiry or verified archive-before-purge. Existing shadow master imports explicitly have expiry disabled. Keep this as a separate remaining gate and do not silently shorten retention or purge historical evidence.
