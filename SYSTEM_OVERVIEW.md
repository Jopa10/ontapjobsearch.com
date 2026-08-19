# Ontap System Overview

**Last updated:** 19 August 2026  
**Status:** Initial owner-readable baseline; repository audit pending.

This is the short owner view of how Ontap is organised. It mirrors the five canonical system buckets in `SYSTEM_MAP.md`.

## Recent canonical changes

- 19 August 2026 — Added the first repo-level governance and canonical system records. Detailed audit comes next.

## 1. Pipeline

This covers how jobs enter Ontap, get classified/selected/deduped, are combined, published and sent into indexing/discovery systems.

**Current position:** the repo clearly has a substantial pipeline area, but the full live path, duplicate logic and obsolete components have not yet been audited. Treat anything not explicitly verified in `SYSTEM_MAP.md` as `UNKNOWN / NEEDS AUDIT`.

## 2. Reports / diagnostics

This covers permanent reconciliation, inventory, click, QA and operational reports.

**Current position:** needs audit. The next pass will identify what is permanent, what is still useful, and what is temporary/obsolete.

## 3. Website / UX

This covers job search, job pages, cards/results, navigation, regional/category/city pages and other persistent user-facing behaviour.

**Current position:** the repo has clear application and component areas, but the detailed architecture and dependencies still need mapping.

## 4. Content / positioning

This covers persistent content structures and product messaging implemented in the repository, rather than temporary chat/social copy.

**Current position:** needs audit.

## 5. Operations / infrastructure

This covers GitHub Actions, schedules, deployment, Vercel, Google/indexing integrations, alerts and persistent configuration.

**Current position:** the repo contains GitHub automation and deployment/runtime configuration, but what is live, scheduled, duplicated or obsolete still needs audit.

## Owner rule of thumb

A persistent change to how Ontap works should appear in the relevant section of the canonical record. Small cosmetic/wording changes and one-off analysis should not create documentation noise.

The goal is simple: a new agent or developer should be able to understand the current system from the repository without needing old ChatGPT or Codex conversations.
