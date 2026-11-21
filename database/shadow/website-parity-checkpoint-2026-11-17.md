# Tuesday 17 November 2026 — Neon Preview migration checkpoint

Status: **Full Tuesday SELECT/REVIEW payload write/readback and full-feed selector parity passed. The website storage blocker is resolved, a complete Neon-backed Preview build passed, and final comparison against the completed Tuesday website publication passed. Preview safeguards, EXCLUDE retention boundaries and real Neon rollback verification passed. Production remains unchanged.**

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

1. The owner explicitly dropped the optional before/after selector-rule comparison as unnecessary for migration once revised outputs match production. Do not restart it. Workflow 44080130595 restored and verified the refreshed saved feed successfully; its unneeded selector comparisons were cancelled when switching to automatic daily-refresh testing.
2. Complete actual subsequent publication-day refreshes, returning/absent-advert and duplicate/update checks. Follow-up checks are scheduled for 18, 19 and 20 November around 10:00 Europe/London. Today's stale-date rejection and fixture retention tests do not replace actual daily rollover evidence.
3. Complete the master-advert inactivity/expiry and recoverable archive-before-purge path for the agreed 90 days after inactivity. The daily selected/review snapshot path is distinct; older master imports currently have expiry disabled. Three-day EXCLUDE fixture boundaries have passed. No production or historical Neon purge has been performed.
4. Finish cutover-specific production fail-closed and deployment rollback preparation before seeking any production switch approval. Preview environment/storage/date/corrupt-snapshot safeguards and actual Preview database transaction rollback have passed; no production traffic rollback has been exercised.

The full Neon-backed website build, final 316-file inventory/source/order parity, and six live HTTP/SEO checks are complete. Do not repeat them without a relevant code/data change.

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

### Final Tuesday published-inventory comparison

- Final comparison workflow **44073576579**, deployment **dpl_371jhLTVUajoQKeH8FiqgqxiNXG5**, uses the actual production publication commit **dc31cdb5ca846cc29f712700a59f80d807cf4912**.
- Confirmed current production deployment **dpl_EQ21vBWBmt2dDL8bMANXb1v6zkM8** is READY on that same source commit. It was not changed by these tests.
- All **316** original website job inventory files matched the newly generated Neon-backed files by ordered **(job ID, source, Apply URL)** tuples: **0 differing files**, no missing/extra inventory members or introduced ordering differences.
- Scope occurrences across those compared website files: **7,927 JobG8**, **360 NHS Jobs**, **45 Teaching Vacancies**. These are repeated placements across files, not unique job counts.
- Final snapshot in Neon: **6,990** publisher rows / **256** scopes; **6,680** JobG8 scope occurrences / **5,372** unique JobG8 IDs; **310** approved external-source scope occurrences. Compressed bytes **5,600,375**; uncompressed **24,286,392**; SHA-256 `d1a387b3b6b95242403cd71265ff1558818f13204273691f869fcb9b91e9af7e`.
- Latest recorded database bytes after snapshot replacement **686,579,712**, below the unchanged 800 MiB ceiling with the 64 MiB reserve.
- Final full website build workflow **44073576579** passed; evidence artifact **14323974863**; deployment **dpl_371jhLTVUajoQKeH8FiqgqxiNXG5** is READY. Next.js generated **6,036** pages. Authenticated live route checks also passed in workflow **44076082639**, artifact **14325496308**.

### Continuation instructions

The owner has authorised continuing these Preview tests without routine permission stops. Reuse passed evidence; only stop for a real missing credential, required policy decision, destructive/production action or guardrail. Keep PR #336 unmerged. The rule replay transport is blocked by HTTP 400 from the signed archive URL; no baseline/revised decision comparison has yet run. Renew only `ONTAP_SAVED_FEED_URL` for Tuesday's exact archive and bump `rule-replay-request.json` to continue the prepared test.

Daily snapshot payload rows are currently keyed by date and advert, while the older master importer still has expiry disabled. This is a test snapshot path, not proof of a bounded recurring master-state store or of the 90-day archive/purge implementation. The admission guard must remain enabled; a future daily import that cannot fit must stop before writes and report the storage gate.

### Final authenticated HTTP and SEO verification — passed

Workflow **44076082639**, evidence artifact **14325496308**, passed against the final READY deployment.

All six returned HTTP **200** with Preview `X-Robots-Tag: noindex`:
- `/` — server HTML and canonical.
- `/north-east/service-administrator-jobs` — server HTML and canonical.
- `/newcastle/service-administrator-jobs` — server HTML and canonical.
- `/nottingham/jobs` — registered broad-city route, server HTML and canonical.
- `/jobs/23643_225841577` — canonical and server-rendered `JobPosting` JSON-LD.
- `/sitemap.xml` — production canonical domain URLs.

Apply links were not followed. The earlier Newcastle broad-city sample was not registered and correctly returned 404; the final test uses Nottingham from the approved broad-city register. The connector's share-link authentication failed, so the successful check used the existing authenticated Vercel CLI without changing protection settings.

PR **#336** was rechecked: **open, draft, unmerged**. Current production deployment remains **dpl_EQ21vBWBmt2dDL8bMANXb1v6zkM8** on Tuesday publication source **dc31cdb5ca846cc29f712700a59f80d807cf4912**. All requested work that needs neither a new feed day nor renewed archive access is recorded above; the master expiry/cutover gates remain explicitly open.

## Automatic today refresh — subsequent checkpoint

The owner requested an automatic latest-completed-publication refresh instead of a pinned Tuesday request. See `daily-refresh-checkpoint-2026-11-17.md` for the current executable workflow, automatic discovery, exact counts and idempotency receipts. The optional before/after rule replay is no longer a required migration gate. Existing passed payload, selector, website, safeguards and rollback evidence remains valid; do not repeat it unnecessarily.
