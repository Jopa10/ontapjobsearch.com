# Customer Sales — governed 33-region diagnostic

Diagnostic only. No Customer Sales slice is LIVE and no production selector is changed.

- Current JobG8 rows analysed: 10000
- Campaign-deduped Customer Sales jobs across the 33 regions: 142
- Exact overlap with current main Service Admin pages: 3
- Incremental versus current main Service Admin pages: 139
- Regions with 6+ jobs: 7
- Conditional account-role jobs requiring boundary attention: 16
- Regions with >=40% top-employer concentration (where 3+ jobs): 4

| Region | Jobs | Employers | Direct | Customer crossover | Account review | Service Admin overlap | Top employer share | 3+ employer groups | Band |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| London | 33 | 29 | 20 | 8 | 5 | 1 | 9.1% | 1 | 6_PLUS |
| Greater Manchester - Manchester & Salford | 7 | 6 | 4 | 2 | 1 | 0 | 28.6% | 0 | 6_PLUS |
| North East | 7 | 4 | 7 | 0 | 0 | 0 | 42.9% | 1 | 6_PLUS |
| Cambridgeshire | 6 | 6 | 4 | 1 | 1 | 0 | 16.7% | 0 | 6_PLUS |
| Kent | 6 | 5 | 5 | 1 | 0 | 1 | 33.3% | 0 | 6_PLUS |
| Yorkshire - West | 6 | 5 | 4 | 0 | 2 | 0 | 33.3% | 0 | 6_PLUS |
| Yorkshire - South | 6 | 4 | 6 | 0 | 0 | 0 | 50.0% | 1 | 6_PLUS |
| Bristol & Bath | 5 | 5 | 4 | 1 | 0 | 0 | 20.0% | 0 | 3_TO_5 |
| Dorset | 5 | 5 | 4 | 1 | 0 | 0 | 20.0% | 0 | 3_TO_5 |
| Northamptonshire | 5 | 5 | 4 | 0 | 1 | 0 | 20.0% | 0 | 3_TO_5 |
| Nottinghamshire | 5 | 5 | 4 | 1 | 0 | 0 | 20.0% | 0 | 3_TO_5 |
| Surrey | 5 | 5 | 4 | 1 | 0 | 0 | 20.0% | 0 | 3_TO_5 |
| Essex | 5 | 4 | 5 | 0 | 0 | 0 | 40.0% | 0 | 3_TO_5 |
| Norfolk | 5 | 4 | 3 | 0 | 2 | 0 | 40.0% | 0 | 3_TO_5 |
| Buckinghamshire | 4 | 4 | 4 | 0 | 0 | 0 | 25.0% | 0 | 3_TO_5 |
| Hampshire | 4 | 4 | 3 | 1 | 0 | 0 | 25.0% | 0 | 3_TO_5 |
| Sussex | 4 | 4 | 3 | 0 | 1 | 0 | 25.0% | 0 | 3_TO_5 |
| Devon | 3 | 3 | 1 | 0 | 2 | 0 | 33.3% | 0 | 3_TO_5 |
| Gloucestershire | 3 | 3 | 2 | 1 | 0 | 0 | 33.3% | 0 | 3_TO_5 |
| Hertfordshire | 3 | 3 | 2 | 1 | 0 | 0 | 33.3% | 0 | 3_TO_5 |
| West Midlands - Birmingham & Solihull | 3 | 3 | 2 | 1 | 0 | 0 | 33.3% | 0 | 3_TO_5 |
| Greater Manchester - South | 2 | 2 | 0 | 2 | 0 | 0 | 50.0% | 0 | 1_TO_2 |
| Wiltshire | 2 | 2 | 2 | 0 | 0 | 0 | 50.0% | 0 | 1_TO_2 |
| Yorkshire - North | 2 | 2 | 2 | 0 | 0 | 0 | 50.0% | 0 | 1_TO_2 |
| Berkshire | 1 | 1 | 0 | 0 | 1 | 0 | 100.0% | 0 | 1_TO_2 |
| Cumbria - South | 1 | 1 | 0 | 1 | 0 | 0 | 100.0% | 0 | 1_TO_2 |
| Oxfordshire | 1 | 1 | 1 | 0 | 0 | 0 | 100.0% | 0 | 1_TO_2 |
| Staffordshire | 1 | 1 | 1 | 0 | 0 | 0 | 100.0% | 0 | 1_TO_2 |
| West Midlands - Coventry & Warwickshire | 1 | 1 | 1 | 0 | 0 | 1 | 100.0% | 0 | 1_TO_2 |
| Yorkshire - East | 1 | 1 | 1 | 0 | 0 | 0 | 100.0% | 0 | 1_TO_2 |
| Cumbria - North | 0 | 0 | 0 | 0 | 0 | 0 | 0.0% | 0 | ZERO |
| Lancashire - North | 0 | 0 | 0 | 0 | 0 | 0 | 0.0% | 0 | ZERO |
| Somerset | 0 | 0 | 0 | 0 | 0 | 0 | 0.0% | 0 | ZERO |

## Interpretation guardrails

`6_PLUS` is a diagnostic volume band, not LIVE approval.
Conditional Account Manager / Account Executive jobs remain visible for review rather than silently becoming automatic title approvals.
Sales + Service Admin overlap is allowed; the overlap column is informational, not an exclusion rule.
Employer concentration and campaign dedupe must be reviewed before any region is proposed for LIVE status.
