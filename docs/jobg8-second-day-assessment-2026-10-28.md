# Fresh 28 October 50k test — inspected assessment

Successful completion: https://github.com/Jopa10/ontapjobsearch.com/actions/runs/40693625932
Results: https://github.com/Jopa10/ontapjobsearch.com/actions/runs/40693625932/artifacts/12819074076
Source code ec47ea496fcb896d8c50ad349f05c5cec6816d24; successful recovery b52cdcadcfe3ce623b9a98d00b74a71152e84276. Earlier failed attempts were harness/reporting/recovery setup errors; their green processing steps do not constitute full-run passes. Successful recovery reused the retained 28 October processing checkpoint and SHA-verified captured 28 October XML, without repeating selection.

## Assessment

PASS for isolated fresh-feed processing, publication generation, same-date 624-row family coverage, regional report/workbook generation and full Next.js build. Not a completed production deployment or blanket production-release certification.

Inspected saved receipt, prior receipt, completed Actions log, full build log, regional Markdown, workbook structure/error cells and packaged canonical JSON. Independent canonical count: 6,041 jobs, comprising 5,490 JobG8, 341 NHS Jobs and 210 Teaching Vacancies. This agrees with the regional report and receipt. All 23 conflicting metadata IDs are absent from canonical inventory. Fresh feed contains 50,000 rows; classification counts sum to 50,000 with reconciliation PASS. Published JobG8 classification counts total 5,490.

Report reconciliation: 6,041 unique jobs plus 1,295 additional placements equals 7,336 slice placements; zero jobs outside governed slices or in non-LIVE slices. Glasgow city and configured regional inventory appear in report; this is generated inventory evidence, not HTTP verification. Yesterday's final trial had 5,477 JobG8, so today's output is 13 higher; total inventory is two higher after source mix changes.

Workbook contains the expected six sheets: Sitewide, JobG8 categories, PAGES, CITY OPPORTUNITIES, LIVE and NOT LIVE. No Excel error-typed cells found. No visual layout QA was performed in this assessment. Dated history columns are production history, not earlier 50k trials. Both report formats are retained in the result artifact.

## Limits and next release evidence

No deployment or fresh HTTP preview-route verification was performed. Real AWS archive upload and deployed packaged-function size remain unverified for this new snapshot. Full-build success is not proof of deployment size or actual production behavior. External data may be retained from approved source state; do not claim all sources are freshly fetched. No full per-saved-approval omission audit or broad CI re-evaluation was performed in this final inspection. The initial focused suite passed 33 tests; earlier documented wider CI failures are not claimed resolved.

Production remains unchanged at 20k, with no merge, supplier switch, production deployment or schedule change authorised by this test. Coordinate a later controlled changeover separately, ensuring approved live CPC supplier account, expanded ceilings and a genuine eligible/reviewed cycle. Preserve the already published 20k site until the new production inventory/deployment is verified; don't bypass completed-cycle guards or relabel a cycle.
