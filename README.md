# Ontap Job Search

Ontap is a UK job-discovery site built with Next.js. Its production inventory is assembled by governed feed/review pipelines, published into repository-backed JSON, verified, and deployed from `main` through Vercel's Git integration.

This README is an entry point, not the system authority. Before making a persistent change, read:

- `AGENTS.md` — repository operating and governance rules;
- `SYSTEM_OVERVIEW.md` — concise owner view of what is live;
- `SYSTEM_MAP.md` — authoritative technical architecture and operating paths;
- `SYSTEM_AUDIT.md` — architecture-audit history and verified cleanup decisions;
- `pipeline/README.md` — pipeline-specific operating model.

The files under `docs/stage0.md` to `docs/stage3.md` are early planning records. They are not current production instructions.

## Production shape

- **Application:** Next.js 16, React 19 and TypeScript.
- **Primary inventory source:** twice-daily JobG8 processing, with governed NEJobs, VONNE, Teaching Vacancies and NHS Jobs paths.
- **Control state:** the regional/category slice register, family classifiers, review state and city-page register.
- **Publication:** source-specific guarded publishers feed the shared verified-page publisher, which writes current website JSON and reports.
- **Deployment:** normal Vercel Git deployment from `main`; Vercel CLI is manual recovery only.
- **Search:** a compact published-job index is generated at build time.
- **Indexing:** sitemap/structured-data handling plus the quota-governed Google Indexing API workflow.

Do not bypass the governed review/publish chain by manually editing live job JSON unless an explicitly reviewed recovery procedure requires it.

## Local application setup

Requirements:

- Node.js 20+
- npm
- the environment variables required by the route or admin function being exercised

Install and run:

```bash
npm install
npm run dev
```

The development command regenerates `generated/published-jobs-search.json` before starting Next.js.

Production build:

```bash
npm run build
npm run start
```

`npm run build` regenerates the published-job search index, generates the Prisma client and runs the Next.js build.

## Checks

```bash
npm run lint
npm run test:frontend
```

The pipeline has its own Python test suite under `pipeline/tests/`. Run the relevant focused tests for any pipeline change; the GitHub Actions workflows remain the authoritative integration environment for scheduled feeds and publication.

Useful scripts:

```bash
npm run campaign:url -- --url <ontap-url> --source <source> --medium <medium> --campaign <campaign>
npm run db:migrate
npm run db:seed
```

Database commands support the legacy/admin surfaces. They are not the production vacancy-publication path.

## Repository areas

- `app/` — application routes and published route data.
- `components/`, `lib/` — shared UI and domain logic.
- `pipeline/` — source ingestion, classification, review, registers, outputs and reports.
- `.github/workflows/` — scheduled and owner-triggered operating workflows.
- `tests/`, `pipeline/tests/` — frontend/domain and pipeline tests.
- `generated/` — build-generated search data.

## Change discipline

Preserve existing public URLs and working architecture unless a concrete business, reliability, UX or discoverability reason justifies change. Persistent system changes must update the relevant canonical documentation in the same commit.

Copyright © 2026 Ontap Job Search. All rights reserved.
