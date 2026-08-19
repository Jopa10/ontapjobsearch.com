# Ontap System Overview

**Last updated:** 19 August 2026  
**Status:** Audit in progress; main live paths now partly verified.

This is the short owner view of how Ontap is organised. It mirrors the five canonical system buckets in `SYSTEM_MAP.md`.

## Recent canonical changes

- 19 August 2026 — Verified the main JobG8 daily workflow, daily review, external-source review schedules and Google Indexing API path. Detailed classification is being recorded in `SYSTEM_AUDIT.md`.
- 19 August 2026 — Added the first repo-level governance and canonical system records.

## 1. Pipeline

**What is definitely live:** there is now a clear main JobG8 workflow. It downloads the feed twice daily, validates it, runs the live category/slice processing, reattaches approved external-source jobs, enriches them and writes the daily outputs/reports.

**What needs fixing:** the pipeline area has accumulated many folders and older mechanisms. The existing pipeline README is already stale: it points to an old May pipeline script as the current stable version even though the scheduled production workflow uses newer modular scripts. Nothing is being deleted until references are checked.

## 2. Reports / diagnostics

**What is definitely live:** the main JobG8 workflow produces daily reports, and a separate daily owner review is generated and emailed each morning.

**What needs fixing:** reports currently live across several differently named report folders. We need to identify which are permanent, which are specialist diagnostics and which can be archived or consolidated.

## 3. Website / UX

**What is definitely present:** the live app is organised under `app/`, with shared components under `components/`. The app tree contains core job-search routes alongside many regional/city routes.

**What still needs audit:** whether those regional/city areas are cleanly template-driven or contain duplicated page logic.

## 4. Content / positioning

Still to audit. Only persistent content that forms part of how the product works belongs in the canonical system record; temporary social/campaign copy does not.

## 5. Operations / infrastructure

**Confirmed scheduled operations:**

- NEJobs review — daily.
- VONNE review — daily.
- Teaching Vacancies regional/master review — daily.
- Main JobG8 process — twice daily.
- Ontap owner daily review — daily.
- Google Indexing API — daily at 19:30.

**Confirmed concern:** GitHub Actions currently mixes genuine operational workflows with many test/fix/recovery/observer/one-off workflows. That is one of the clearest sources of system bloat and will be fully classified before anything is removed.

The Google Indexing API workflow is confirmed live and includes the 200-notification limit plus automatic GitHub Issue alerts for backlog/failure conditions.

## Owner rule of thumb

A persistent change to how Ontap works should appear in the relevant section of the canonical record. Small cosmetic/wording changes and one-off analysis should not create documentation noise.

The aim remains: a new agent or developer should be able to understand the current system from the repository without needing old ChatGPT or Codex conversations.
