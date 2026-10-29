# Service Admin audit changes — 29 October 2026

## Authorisation and isolation

Owner authorised implementation and same-input comparison after the successful day-three test. Baseline run 40848659957, artifact 12893406332, source 125fc37a7f8785442b1905655a7b25161b562bcc are retained unchanged. Test branch only: `test/service-admin-selection-20261029`. Production remains 20k. No main merge, supplier switch, deployment or email is authorised by this change.

## Approved changes

1. All 62 INCLUDE titles in the owner's title proposal workbook are added to the existing refinement register. Their description-context boundaries remain explicit; applicable specialist requirements go to review. Common Admin/Administration Officer, Admin Support Officer, Administration Clerk and Administrative Support variants are recognised without rejecting a place/contract suffix. Practical warehouse/engineering/transport/manufacturing administration can match without admitting physical workers or managers. Absolute barriers, qualifications, language requirements and existing decisions remain.
2. The workbook remains the geographic authority. Factual additions use its existing canonical reference towns, recorded in `service-admin-selection-geography-2026-10-29.csv`; Derby is corrected from East Midlands to Derbyshire. No new market or LIVE activation is created. Regions not LIVE remain ineligible. Previously provisional labels in the review workbook were not canonical operational names and are reconciled here. Primrose Valley is North Yorkshire (Scarborough/Filey context), not East Yorkshire; Burscough/Lathom are Lancashire West, not Liverpool; Bispham uses Blackpool & Fylde; Haydock/Kirkby use St Helens & Knowsley. Sherburn in Elmet uses North Yorkshire. Six owner-deferred towns remain unchanged: Ramsey, Pampisford, Midge Hall, Romanby, The Ridgeway, Woodlands. Additionally Staveley, Fulwood, Halton, Newbridge and Monkswood are held because their proposed mappings were ambiguous or incorrect without corroborating precise feed evidence. Missing/broad locations are not forced into a market.
3. Otherwise eligible Service Admin roles may pass without numeric pay. Structured salary retains priority; explicit supported numeric description pay retains credibility, maximum and review checks. Non-numeric descriptions such as Salary: Competitive/DOE/negotiable are retained; competitive markets/benefits are not salary evidence. Truly missing pay remains empty in data and the website's existing Salary not stated fallback applies. Numeric pay with unclear periods remains subject to existing uncertainty handling. Part-time managers still require review; accountant, language, IT and other hard exclusions remain. No invented salary.

## Deferred policy

Generic managers/seniors/team leaders and Document Controller role suitability/pay ceilings remain for separate discussion. Salary absence alone is governed by item 3; stated Document Controller pay retains its existing £45k boundary. Batch selections are not reused as permanent rules.

## Validation

Focused title/pay and geography checks run before the full comparison. The wider structured-geography suite has a baseline failure: expected Ashton Under Lyne versus existing Ashton-Under-Lyne display spelling; reproduced on the unchanged baseline lookup. This is not introduced by the patch and is not described as passing.

The isolated workflow verifies the captured XML hash and 50,000 rows, runs the existing regression suite, processes/reviews/composes the feed with job-level withholding, verifies quarantine, generates regional report and workbook, and runs the full build. It downloads the unchanged successful baseline and produces job-level inventory/selector CSV differences plus JSON/Markdown summaries. Final counts and newly added adverts must be inspected before recommending release. Fixture/snapshot branches must never be merged into production: carry reviewed source changes only onto current main after approval.
