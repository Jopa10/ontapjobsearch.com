# Weekly traffic report — agreed owner format

Approved 26 October 2026. Reuse this format; do not redesign it or add measures without the owner asking.

Deliver one plain Excel workbook with four tabs, in this order:
1. Summary — existing headline metrics with direct links to weekly totals; explain CPC/non-CPC and GA4/JobG8 arithmetic.
2. Weekly — every Saturday–Friday reporting period, clearly marked partial final period, and TOTAL. Columns: Period; GA4 apply_click; JobG8 dashboard; GA4 JobG8 CPC; GA4 CPC less dashboard; Other providers. Next table: GA4 apply_click referrer mix (ChatGPT, JobLeads, Google, Direct, Other/unattributed), all weeks and TOTAL. Put the separate GSC clicks/impressions table BELOW the referrer mix, never alongside apply clicks. GSC incoming-search clicks are not Apply clicks.
3. Job Detail — retain upper aggregated title, grouped location and region rankings. Add an apply_click view by Ontap job family, using each clicked listing’s actual family assignment (not a family guessed from its title); show counts and share of all apply_clicks, and keep unassigned/unavailable clicks visible. Family totals plus unassigned/unavailable must reconcile to the apply_click total. Lower table must rank specific job IDs by their OWN apply_click count across all originating pages, with exact title, job location, ID/URL and count. NEVER pair a city/region page total with one job title. If a job cannot be identified reliably, mark it unavailable rather than substituting a page or title-group total. Label top-N lists; do not imply they reconcile to all clicks.
4. Additional measures — the accepted standalone one-sheet additions page: weekly page views, distinct page-view users, sessions, returning browsers, saved-location returns; Jobs Near You panel views/viewers, location-button clicks, found/failed, manual submits, results-link clicks; search result-page views, new search submissions/results, results/no-results, distinct recorded typed locations; definitions and tracking coverage. Preserve its plain layout.

Checks before delivery:
- Family assignments must come from the clicked listing’s actual Ontap family; do not infer them from title wording. Keep unassigned/unavailable separate so the family view still reconciles.
- All weekly counts sum to the matching headline totals. All apply clicks = identified CPC + Other providers. CPC difference = GA4 CPC minus supplier clicks, NOT all apply clicks minus supplier.
- Other providers includes non-CPC plus unidentified destination data; do not silently represent unidentified as verified non-CPC. Referrer rows include unattributed remainder and tie to all apply clicks.
- Reconcile supplied JobG8 daily data to displayed monthly totals and avoid duplicate screenshot rows. No further historical retrieval beyond the supplied span unless requested.
- Keep source cutoffs/time zones explicit, and partial days separate from complete-week comparisons. GSC has its own settled-through date.
- Do not add weekly distinct users into a whole-period distinct-user total. Record tracking gaps as N/A, not zero. First observed event is not a verified deployment date.
- Location-button, location-success/failure, manual-submit and results-link events are separate counts, NOT an attributed funnel; results-link clicks are not apply clicks. Do not claim that 9 activations caused 10 onward clicks.
- Search outcomes start prospectively; mark tests and do not invent historical successful/failed searches or historical distinct attempted towns/regions.
- Small GA4/JobG8 discrepancies stay in tables; commentary should focus on material issues. Never replace the complete weekly table with a selected-week extract.
- Plain readable formatting; correctness and traceable totals take priority. No unsought charts, styling redesign, extra tabs or new measures.

When the owner says not to regenerate yet, record pending edits and wait. On the next authorized production, apply the agreed pending edits together. This reporting contract governs owner traffic workbooks only; it changes no website, publishing workflow or analytics collection.
