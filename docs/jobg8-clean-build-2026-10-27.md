# Clean checkout build correction

The 253686693-byte jobs/all trace included the untracked local raw test workbook pipeline/input/jobg8.xlsx (45330498 bytes). This workbook is not committed/deployed; it is materialized for pipeline processing. Moved test-input workbook and temporary workbook outside the checkout without deleting them.

Repeated full Next production build with the final combined inventory: PASS, exit 0. Clean jobs/all NFT dependency sum: 208356195 bytes (208.4 decimal MB). Exactly 45330498 bytes lower than previous measurement. No source-code/tracing configuration change made. The 253.7 MB figure was a local test-input artifact and must not be used as the deployment size estimate.

Actual Vercel package acceptance remains untested; this is a local trace measurement. Final website inventory remains 5786 canonical jobs: 5253 JobG8, 323 NHS, 210 Teaching Vacancies. Source review possible rows 214 (not final owner unanswered count). Production unchanged.
