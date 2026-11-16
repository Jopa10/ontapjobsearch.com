# Monday 16 November 2026 — Neon website publication parity checkpoint

Status: **PARTIAL PASS** — complete selected JobG8 membership and two essential advert fields match; full page/region/city parity not yet established.

## Independently verified evidence

Production publication: GitHub Actions run `43824436796`, artifacts `14208439791` (service-admin-output) and `14209236979` (support-worker-output), from the published Monday job outputs.

Production artifacts contain 250 JSON files, 247 containing at least one JobG8 advert, with 6,494 JobG8 region/family occurrences and **5,246 distinct JobG8 IDs**.

Neon Preview source: `ontap_shadow.selected_review_payload_records`. The read-only Next.js route automatically chooses `max(feed_date)` and queries only records from that feed date. Verified date: `2026-11-16`. Counts: 5,246 SELECTED, 335 REVIEW, total 5,581 distinct records. A raw review collection of 390 includes overlaps with SELECTED and is not the distinct REVIEW count.

Comparison of sorted selected rows, using SHA-256 with exact lexical ID ordering and newline delimiters:
- IDs: `6dbe5fbb544157878afa4322ac67b2bc1a7e5a4a573717d735fb6c51d8f345f0` — exact match
- ID + title: `b7d844ff3302f6774341dffc3df212ed0b9d29553bc22376a6209576f17ab9bc` — exact match
- ID + Apply URL: `ad36f01a591c3002393031d8b776fb722e252d7e8c6ebe17d1702943866c3043` — exact match
- Selected rows with absent title / Apply URL: 0 / 0.

Source code: PR #336 `feat/neon-shadow-database`, commits `96789f1b5b0a9ba3b14fbed440093ad66e337be4` and `7e34f11488cee60d031c054dc841dd8921ad76a5`.

Vercel deployment: `dpl_EAezr7FRRfnnD6AtCtcUEqYDiPpM` (READY), route `/shadow-neon-preview/parity`, HTTP 200. The route is Preview-only, verifies project identity, uses a TLS Neon connection and a read-only database transaction, and emits no full advert payload or raw IDs.

## Remaining test gates (NOT passed)

1. Neon selected/review payload table contains raw advert and global decision, but not the per-scope `published_output_appearances` / ordered region/family output records needed by the existing full-site builder.
2. Store or reconstruct independently and verify all 250 publication output JSON files with ordered IDs and published display rows from Neon; do not simply copy production artifacts into Neon and call that an independent match.
3. Exercise the existing regional publisher, city derivation, all job detail routes, homepage, sitemap/structured data and Apply links in a full Next.js Preview built from the **same** latest completed Neon publication; compare against that day's immutable published output and actual production HTML.
4. Preserve non-JobG8 external source composition and alias/canonical handling without changing live totals.
5. Only after a full independent pass discuss cutover. No production configuration or publishing changes are authorized.

Do not call this FULL PUBLICATION PARITY passed based on selected IDs/title/URL equality alone.
