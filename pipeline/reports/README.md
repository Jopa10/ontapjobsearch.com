# Pipeline report lifecycle

Ontap report outputs fall into three lifecycles.

## Operational

Recurring production/reconciliation outputs belong in `pipeline/reports-daily/` or in a clearly named persistent operational report surface.

Examples include live-job source counts/history, daily region overview, selection/validation reports and newly-published ledgers.

## Analysis

Deliberate compiler/research outputs belong in the specialist Module 1/2/3 report areas. They are useful analysis products but are not production publishing inputs unless a workflow explicitly says otherwise.

## One-off diagnostics

Dated recovery/failure/observer output should normally remain in GitHub Actions logs/artifacts or Git history rather than accumulate in the working report tree.

Do not add a new `reports-*` folder for a one-off investigation. Reuse an existing lifecycle or keep the output ephemeral.

Before moving or deleting an existing report path, search workflow/script references first. Report tidy-up must not break a live workflow merely to make the tree look cleaner.
