# Ontap System Map

**Last updated:** 19 August 2026  
**Status:** Initial governance baseline; repository audit pending.

This is the authoritative technical map of the persistent Ontap system. It is organised into five canonical buckets. Facts not yet verified from the repository are marked `UNKNOWN / NEEDS AUDIT` rather than inferred from chat history.

## Recent canonical changes

- 19 August 2026 — Created the five-bucket canonical system map and governance framework. Full repository audit still required.

## 1. Pipeline

Purpose: how job data moves from source to published/indexed output.

Canonical stages:

`source → ingest → classify → select → dedupe → compose → publish → index`

Current verified structure:

- Repository contains a top-level `pipeline/` area. Detailed responsibilities, entry points, live feeds, shared modules and obsolete/duplicate components are `UNKNOWN / NEEDS AUDIT`.
- Published/user-facing application code exists under top-level `app/`. Exact boundary between generated pipeline output and application code is `UNKNOWN / NEEDS AUDIT`.
- Configuration exists under top-level `config/`. Pipeline ownership of individual configuration files is `UNKNOWN / NEEDS AUDIT`.

Audit must establish:

- every live source/feed;
- ingest entry points;
- classification/category mechanisms;
- selection rules and registers;
- dedupe mechanisms;
- composition mechanisms;
- publication destinations;
- Google/other indexing paths;
- duplicate, obsolete and orphaned pipeline folders/scripts;
- one clear operational entry point for routine runs.

## 2. Reports / diagnostics

Purpose: persistent outputs used to reconcile, inspect or monitor Ontap.

Current verified state:

- `UNKNOWN / NEEDS AUDIT`.

Audit must distinguish:

- permanent recurring reports;
- QA/reconciliation checks;
- operational diagnostics;
- one-off analysis that should not become permanent infrastructure;
- duplicate or obsolete reporting scripts/output folders.

## 3. Website / UX

Purpose: user-facing job search, job pages, navigation and presentation.

Current verified structure:

- Top-level `app/` contains application routes/pages.
- Top-level `components/` contains reusable website components.
- Top-level `lib/` exists and its website/runtime responsibilities are `UNKNOWN / NEEDS AUDIT`.

Audit must establish:

- major routes and page types;
- search architecture;
- job-detail architecture;
- job-card/result presentation;
- regional/category/city page mechanisms;
- data dependencies between website and pipeline outputs;
- persistent UX rules that materially affect job discovery/application.

## 4. Content / positioning

Purpose: persistent editorial, guidance and positioning structures implemented in the product/repository.

Current verified state:

- `UNKNOWN / NEEDS AUDIT`.

Audit must establish which persistent content structures live in the repository and distinguish them from temporary campaign copy or external social content.

## 5. Operations / infrastructure

Purpose: workflows, scheduling, deployment, alerts, indexing integrations and persistent environment/configuration mechanisms.

Current verified structure:

- Top-level `.github/` exists and contains GitHub repository automation/configuration.
- Repository contains `Dockerfile` and `docker-compose.yml`.
- Repository contains deployment/runtime-related configuration files including `ecosystem.config.js`.
- Exact live deployment path, scheduled workflows, alerts, Vercel integration, indexing workflows and secret dependencies are `UNKNOWN / NEEDS AUDIT`.

Audit must establish:

- every GitHub Actions workflow and whether it is live;
- schedules and manual triggers;
- deployment path(s);
- Vercel integration;
- Google indexing and IndexNow integration;
- alerts/issues/failure handling;
- required secrets/configuration, without recording secret values;
- obsolete workflows and duplicated operational mechanisms.

## Documentation rule

When a persistent system-level change alters any of these five buckets, update the affected section of this file in the same change. If live/active/user-facing state changes, update `SYSTEM_OVERVIEW.md` as well.
