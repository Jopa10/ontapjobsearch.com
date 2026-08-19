# Ontap System Overview

**Last updated:** 19 August 2026  
**Status:** Agreed architecture cleanup 1–5 merged into `main` via PR #211.

This is the short owner view of how Ontap is organised. It mirrors the five canonical system buckets in `SYSTEM_MAP.md`.

## Recent canonical changes

- 19 August 2026 — Added fail-soft publication hierarchy: up to 15 problem jobs in one source are withheld and flagged while clean jobs continue; larger source problems isolate that source rather than blocking the whole Ontap publish.
- 19 August 2026 — Made NEJobs fail-soft in the owner publish workflow: an NEJobs publisher failure now keeps the last approved NEJobs snapshot, raises a workflow warning and lets the other clean sources continue publishing.
- 19 August 2026 — Merged architecture cleanup 1–5 into `main` via PR #211; the cleanup is now part of the canonical production repository state.
- 19 August 2026 — Implemented the agreed cleanup: removed proven one-off/recovery workflows, fixed stale pipeline documentation, shared the repeated JobG8 materialisation used by NEJobs/VONNE, retired superseded standalone category workflows/old May script, and removed dated one-off diagnostics.
- 19 August 2026 — Made the business-priority rule explicit: Ontap is not refactored for technical neatness alone.
- 19 August 2026 — Completed the first architecture audit and verified the main JobG8, review/publish, external-source, website-data and Google indexing paths.

## 1. Pipeline

The working core is being preserved.

The main JobG8 process remains the production ingest/process path. NEJobs, VONNE and Teaching Vacancies retain their review paths. After review, the single **Apply and publish Ontap daily review** workflow coordinates source publishers and the final verified-page publish.

The publish rule is now deliberately fail-soft:

**up to 15 bad/unresolved jobs in one source are withheld and flagged while the clean jobs continue; more than 15, or a source-integrity problem, isolates that source and keeps its last approved state; only a genuine whole-publication integrity failure should stop everything.**

This includes simple review mistakes such as a misspelt action: the affected job is withheld rather than allowing one bad row to derail hundreds or thousands of clean jobs.

The cleanup removes surrounding duplication rather than redesigning selection logic. NEJobs and VONNE now share one tested current-JobG8 materialisation helper instead of carrying repeated feed-download/conversion blocks.

The old May monolithic pipeline and the older standalone service-admin/support-worker workflows have been removed because the current full/reviewed pipeline covers those operational paths.

## 2. Reports / diagnostics

Routine operational reporting remains intact.

Dated one-off recovery/failure reports have been removed from the working tree. The rule going forward is:

**recurring operations / specialist analysis / one-off diagnostics in Actions artifacts or Git history.**

Compiler Modules 1/2/3 remain legitimate analysis tools. No broad report-folder move has been made where it could break live references just for tidiness.

## 3. Website / UX

**No website route cleanup is part of this refactor.**

The existing public routes, job JSON and SEO-facing structure remain untouched. The dynamic slice mechanism remains useful for future expansion, but that is not a reason to reorganise established routes.

Website/public-route work only moves up the priority list when there is a concrete business reason — for example evidence of impaired Google/AI discoverability, UX, reliability or inventory expansion.

## 4. Content / positioning

No content-architecture cleanup is included.

## 5. Operations / infrastructure

The operational controls are becoming clearer:

- scheduled source refresh/reviews;
- one master daily owner review;
- one owner-facing apply/publish orchestrator;
- final verified-page publishing;
- Google indexing and operational monitoring.

The owner publish now isolates failures at the smallest sensible level. Small job-level problems do not stop a source; source-level problems do not stop unrelated sources; the last approved state is retained wherever a source is isolated.

Proven one-shot/recovery workflows have been removed. Specialist analysis and genuine experiments remain where there is not enough evidence to call them obsolete.

The Google Indexing API remains unchanged, including the 200-notification safety limit and GitHub Issue alerting.

## Business rule

**Business priority wins over technical tidiness.** Cleanup is justified where it improves reliability, delivery speed, cost, UX, indexing/discoverability, AI discoverability or safe inventory growth — not simply because a cleaner-looking architecture is possible.

## Current state

Architecture cleanup 1–5 is merged into `main` via PR #211. It is no longer awaiting validation or merge; future interrogation should treat the cleaned architecture as the current canonical repository state.
