# Ontap daily job review

> **NOT READY TO REVIEW — waiting for: JobG8, NEJobs, VONNE, Teaching Vacancies, NHS Jobs**
> Do not start reviewing yet. Rebuild this review after those source refreshes complete.

review_date: 2026-08-27
generated_at: 2026-08-27T08:55:57+00:00

**0 job(s) need a human decision.**

Edit only each `action:` line:
- `action: select` = include the vacancy.
- `action: exclude` = reject the vacancy.
- Leave `action:` blank while you are still deciding it.
- Up to 15 unresolved/bad action rows per source are fail-closed at job level: those jobs are withheld and flagged while the rest of that source can continue.
- More than 15 unresolved/bad action rows in one source isolate that source from the run; they do not block other clean sources.
- Unchanged decisions are remembered by the source pipelines; they should not keep returning here.
- If the vacancy facts change, its fingerprint changes and it must be reviewed again.

## Source status

| Source | Status | Review date | Needs review | Note |
|---|---|---|---:|---|
| JobG8 | STALE | 2026-08-26 | 0 | — |
| NEJobs | STALE | 2026-08-26 | 0 | — |
| VONNE | STALE | 2026-08-26 | 0 | — |
| Teaching Vacancies | STALE | 2026-08-26 | 0 | — |
| NHS Jobs | STALE | 2026-08-26 | 0 | automatic Tier A/B publish; NHS POSS stays in the NHS-specific review and is optional |

> **Attention:** one or more active source reviews are stale or missing. Those sources contribute no jobs to this file and must not be treated as zero inventory.
