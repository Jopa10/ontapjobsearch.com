# Ontap England market naming evidence — 22 August 2026

## Scope

Supplement to `geography-market-reconciliation-2026-08-22.md` on the audit branch only. No production geography, URL or LIVE-slice change.

## Finding

The 55 candidate catchments should not be merged merely because a broader geographic term is also used by jobseekers. Established UK job-board search surfaces show that broad and local terms coexist.

Examples observed on Reed:

- Cheshire: https://www.reed.co.uk/jobs/jobs-in-cheshire
- Warrington: https://www.reed.co.uk/jobs/jobs-in-warrington
- Greater Manchester: https://www.reed.co.uk/jobs/jobs-in-greater-manchester
- Lancashire: https://www.reed.co.uk/jobs/jobs-in-lancashire
- Cumbria: https://www.reed.co.uk/jobs/jobs-in-cumbria
- Merseyside: https://www.reed.co.uk/jobs/jobs-in-merseyside
- Liverpool: https://www.reed.co.uk/jobs/jobs-in-liverpool
- Wirral: https://www.reed.co.uk/jobs/jobs-in-wirral
- Leicestershire: https://www.reed.co.uk/jobs/jobs-in-leicestershire
- Rutland: https://www.reed.co.uk/jobs/jobs-in-rutland

This is evidence that the terms are genuine job-search locations; it is **not** Google search-volume evidence and must not be treated as a substitute for Keyword Planner.

## Recommended architecture

1. Freeze one complete, non-overlapping routing geography underneath the product.
2. Preserve the 55-market working set while final catchment QA is completed.
3. Do not force broad search terms to replace smaller routing catchments.
4. Where search demand supports it, create aggregate/search landing behaviour across multiple catchments, e.g. `Greater Manchester jobs`, `Cheshire jobs`, `Lancashire jobs`, `Cumbria jobs`, `Merseyside jobs`.
5. Keep city pages as a further local/SEO layer rather than using city pages to define regional coverage.

This lets `Liverpool` and `Wirral` remain distinct routing/searchable markets while a broader `Merseyside` search can surface both; likewise Greater Manchester can be searched broadly without deleting the existing Manchester/Salford and South catchments or preventing North and Wigan/Bolton from being added.

## Still requiring direct keyword-volume evidence

Before changing public titles/slugs or adding aggregate landing pages, compare likely public terms in Google Keyword Planner. Highest-priority groups:

- Cheshire / East Cheshire / West Cheshire / Warrington / Chester
- Greater Manchester / Manchester / South Manchester / Stockport / Bolton / Wigan / Rochdale / Oldham
- Lancashire / Preston / Blackburn / Blackpool / Lancaster / East Lancashire
- Cumbria / Carlisle / Kendal / Barrow / West Cumbria / Workington
- Merseyside / Liverpool / Wirral
- Black Country / Dudley / Wolverhampton / Walsall / West Bromwich
- Leicestershire / Leicester / Rutland / Oakham

## Current audit conclusion

The geography problem is now best treated separately from search naming:

- **coverage/routing:** current working set = 55 England markets (33 existing + exact 22 omitted non-NE markets; North East retains its deliberate aggregate treatment)
- **search naming/landing:** broad terms can aggregate those markets and local/city terms can sit below them

No existing regional URL should be removed during this audit.
