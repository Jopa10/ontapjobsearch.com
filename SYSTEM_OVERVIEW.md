# Ontap System Overview

**Last updated:** 19 August 2026  
**Status:** First architecture audit complete; target shape ready for owner review.

This is the short owner view of how Ontap is organised. It mirrors the five canonical system buckets in `SYSTEM_MAP.md`.

## Recent canonical changes

- 19 August 2026 — Completed the first architecture audit. The conclusion is to preserve the working core, simplify the surrounding workflows/reports, and make the true operational entry points obvious rather than rewrite the pipeline.
- 19 August 2026 — Verified the main JobG8 workflow, master review/publish orchestration, external-source review/publish paths, website job-data path and Google Indexing API.
- 19 August 2026 — Added the first repo-level governance and canonical system records.

## 1. Pipeline

The working core is credible and should be preserved.

The main JobG8 process runs twice daily. NEJobs, VONNE and Teaching Vacancies have separate review paths. After review, one master **Apply and publish Ontap daily review** workflow coordinates the source-specific publishers and the final verified-page publish.

The main cleanup opportunity is around that core: duplicated JobG8 download/materialisation logic, older standalone category workflows, stale documentation and historical scaffolding.

**Recommendation:** simplify around the current working contracts; do not rewrite the selection pipeline.

## 2. Reports / diagnostics

Routine operational reporting is real and useful, especially `pipeline/reports-daily/` and the single daily owner review.

Compiler Modules 1/2/3 are also legitimate specialist analysis tools. They should simply be kept visibly separate from routine production workflows/reports.

The target is three obvious lifecycles: **daily operations / specialist analysis / archive or one-off diagnostics**.

## 3. Website / UX

The website already has a scalable direction.

Published job JSON under `app/` feeds the job/search/detail layer. Newer region/category slices are driven by the slice register and job-slice catalog through the dynamic `/job-search/...` mechanism rather than requiring a bespoke new page every time.

**Recommendation:** use that dynamic mechanism for future expansion. Existing static pages should only be rationalised later, after SEO and user-facing dependencies are checked.

## 4. Content / positioning

No content-architecture cleanup is recommended from this audit. Persistent product content belongs in the canonical system only where it materially affects how Ontap works.

## 5. Operations / infrastructure

The important operational workflows are now identifiable:

- source refresh/review;
- one master daily review;
- one owner-facing apply/publish orchestrator;
- final verified-page publishing;
- Google indexing and operational monitoring.

GitHub Actions still contains dated fix/recovery/observer workflows, experiments and older standalone routes alongside these real controls. Those are the clearest cleanup candidates.

The Google Indexing API remains a confirmed live path with the 200-notification safety limit and automatic GitHub Issue alerting.

## Proposed cleanup order

1. workflow hygiene — remove/archive proven one-shot repair scaffolding;
2. fix the stale pipeline README;
3. consolidate duplicated JobG8 materialisation/download logic;
4. retire superseded standalone category workflows only after final coverage checks;
5. rationalise report lifecycles;
6. leave website/static-route cleanup until last because it carries the most SEO/user-facing risk.

## Owner decision point

The audit is now complete enough to move from **audit** to **agree target shape**. No production refactor has been carried out yet.

The aim remains: a new agent or developer should be able to understand the current system from the repository without needing old ChatGPT or Codex conversations.