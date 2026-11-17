# Tuesday 17 November 2026 — Neon Preview migration checkpoint

Status: **Full Tuesday SELECT/REVIEW payload write and readback passed. Full Neon-backed website Preview was blocked by the existing database-headroom safeguard. Production remains unchanged.**

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
