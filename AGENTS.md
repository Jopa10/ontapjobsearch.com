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

## Documentation rules

- Any persistent system-level change must update the relevant bucket in `SYSTEM_MAP.md` in the same change.
- If the change affects what is live, active, scheduled, user-facing or operationally important, update `SYSTEM_OVERVIEW.md` too.
- Trivial cosmetic edits, wording tweaks, one-off analysis and temporary diagnostic work do not require canonical documentation updates unless they create a persistent new system component.
- Code and required canonical documentation updates should be committed together.
- `SYSTEM_MAP.md` prioritises technical accuracy and operational usefulness.
- `SYSTEM_OVERVIEW.md` must remain concise and understandable to a non-technical owner while accurately reflecting the technical system.
- Keep the visible `Last updated` date and `Recent canonical changes` section current whenever either canonical file changes.
- Never invent system facts. If something cannot be confirmed from the repository, mark it `UNKNOWN / NEEDS AUDIT`.

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
