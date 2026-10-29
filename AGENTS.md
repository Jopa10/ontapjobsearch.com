# Ontap repository operating rules

This repository is the canonical source of truth for how Ontap works. Chat history, Codex history and other AI conversations are not authoritative system documentation.

## Required reading before persistent changes

At the start of every coding task, inspect the current repository instructions and the relevant sections of `SYSTEM_MAP.md` and `SYSTEM_OVERVIEW.md` before making persistent changes.

## Canonical system buckets

All persistent Ontap system changes belong to one or more of these five buckets:

1. **Pipeline** — feeds, ingest, classification, selection, dedupe, composition, publishing and indexing.
2. **Reports / diagnostics** — reconciliation, click reports, inventory breakdowns, QA checks and recurring operational reports.
3. **Website / UX** — search, job cards, pages, navigation, presentation and user-facing behaviour.
4. **Content / positioning** — AI-at-work content, sector-switcher content, homepage/landing-page messaging and persistent editorial/content structures.
5. **Operations / infrastructure** — GitHub Actions, scheduling, alerts, secrets/configuration, deployment, Vercel, Google/indexing integrations and other persistent infrastructure.

## Business-priority rule

- Business priority wins over technical tidiness.
- Do not refactor a working area merely because another structure looks cleaner.
- Structural cleanup needs a concrete business or operational reason: reliability, delivery speed, cost, user experience, indexing/discoverability, AI discoverability, or the ability to expand inventory safely.
- Website routes and public URLs are especially conservative: do not reorganise them for neatness. Change them only when there is evidence of a material business benefit or a specific defect, and preserve indexing/URL behaviour unless the change itself is intended to improve it.

## Publication failure-isolation rule

- Owner golden rule: failures, unresolved reviews or malformed data in Teaching Vacancies, NHS, NEJobs, VONNE or other non-paying sources must never block, delay or reduce clean JobG8 publication. Isolate the affected source; retain its approved state where safe or withhold it. Test this boundary whenever modifying review, composition or publication orchestration.

- A small number of bad, ambiguous, malformed or unresolved jobs must not derail publication of otherwise clean inventory.
- Permanent owner clarification, 29 October 2026: a handful of isolated selection/audit exceptions (for example 5–6 jobs among 5,000–6,000 clean jobs) must not block release readiness or publication of the clean remainder. Fix them if practical; otherwise withhold/quarantine and report the affected jobs, and continue. Do not keep repeating full-feed tests solely to resolve those isolated jobs when clean-inventory integrity is established. This is not permission to publish known unsuitable jobs or ignore a defect whose impact may extend across the feed; assess that scope before treating it as a small isolated exception.
- Up to 15 problem jobs in one source should fail closed at job level: withhold and flag those jobs while allowing the clean jobs from that source to continue.
- More than 15 problem jobs, or evidence of a source-level integrity problem, should isolate that source and retain its last approved state while other clean sources continue.
- Stop the whole owner publish only for a genuine system-level integrity failure where the combined/public output cannot safely be trusted.
- Prefer explicit warnings, run summaries and retained prior approved state over turning a local data-quality problem into a site-wide publication outage.

## Documentation rules

- Any persistent system-level change must update the relevant bucket in `SYSTEM_MAP.md` in the same change.
- If the change affects what is live, active, scheduled, user-facing or operationally important, update `SYSTEM_OVERVIEW.md` too.
- Trivial cosmetic edits, wording tweaks, one-off analysis and temporary diagnostic work do not require canonical documentation updates unless they create a persistent new system component.
- Code and required canonical documentation updates should be committed together.
- `SYSTEM_MAP.md` prioritises technical accuracy and operational usefulness.
- `SYSTEM_OVERVIEW.md` must remain concise and understandable to a non-technical owner while accurately reflecting the technical system.
- Keep the visible `Last updated` date and `Recent canonical changes` section current whenever either canonical file changes.
- Never invent system facts. If something cannot be confirmed from the repository, mark it `UNKNOWN / NEEDS AUDIT`.
- Treat registers, workflow definitions and current generated reports as authoritative for current counts, schedules and activation state. Dated launch snapshots may remain as history, but must be labelled as historical and must not be described as the current footprint.
- Avoid duplicating volatile counts in several current-state sections. Where a number is operationally useful, date it and name the file from which it was reconciled.

## Architecture discipline

- Inspect existing architecture before adding a new pipeline, workflow, report, service or major website mechanism.
- Reuse or extend shared mechanisms where practical.
- Do not casually create parallel scripts, duplicate workflows, new folders or alternative mechanisms where an existing shared mechanism can be used or consolidated.
- Prefer one clear entry point and one clear source of truth for each major responsibility.
- When replacing an existing mechanism, identify what becomes obsolete and either remove it safely or mark it for archive/removal.

## Agent neutrality

- Keep these instructions tool-neutral. Ontap must not depend on Codex-specific, Copilot-specific, Claude-specific or other vendor-specific behaviour.
- A competent new agent or human developer should be able to open the repository, read these files and continue safely without access to prior chats.

## Governance enforcement

A lightweight CI enforcement check may be added once the repository audit has identified which paths reliably represent meaningful system changes. Until then, do not add a brittle path-based rule that would create frequent false positives.

## Owner weekly traffic report

Before producing or changing the owner weekly traffic Excel report, read `pipeline/reports/WEEKLY_TRAFFIC_REPORT_FORMAT.md`. Preserve its approved tabs, definitions, period basis and reconciliation checks. Do not redesign the report from chat memory.

## Owner job review

Before preparing or applying an owner job review, read `pipeline/reviews/OWNER_REVIEW_PROCESS.md`. Reuse the approved single-sheet Excel format and fixed Review No. mapping. Do not redesign it or change selection rules from batch decisions. This is separate from the weekly traffic report contract.
