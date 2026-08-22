# JobG8 Claims Support regional viability diagnostic

Observed feed dates: **7** (2026-08-16 to 2026-08-22).
Latest feed: **2026-08-22**.
Content-unique IN jobs on latest feed: **29**; unmapped/unknown region: **8**.

Diagnostic only: this does not activate a slice. `STRONG_REVIEW_CANDIDATE` is deliberately an evidence signal, not an automatic LIVE gate.

For this diagnostic, a region is `STRONG_REVIEW_CANDIDATE` when the latest feed has 6+ Claims Support jobs and at least 3 observed feed dates have 6+ jobs. `WATCH` means latest 4+ and at least 3 observed feed dates at 4+. This mirrors the existing 6+ recurrence style used elsewhere in Ontap as a conservative review signal; explicit approval is still required.

Strong review candidates: **0**.
Watch regions: **0**.

## Regional evidence

| Region | Latest | Avg | Median | 6+ days | Recent counts | Evidence |
|---|---:|---:|---:|---:|---|---|
| Yorkshire - West | 3 | 4.00 | 4.0 | 0 | 4 / 4 / 5 / 5 / 4 / 3 / 3 | THIN |
| Staffordshire | 3 | 2.71 | 3.0 | 0 | 2 / 2 / 2 / 4 / 3 / 3 / 3 | THIN |
| Bristol & Bath | 3 | 2.14 | 3.0 | 0 | 0 / 0 / 3 / 3 / 3 / 3 / 3 | THIN |
| Northamptonshire | 2 | 2.29 | 2.0 | 0 | 2 / 2 / 2 / 3 / 3 / 2 / 2 | THIN |
| Oxfordshire | 2 | 2.00 | 2.0 | 0 | 2 / 2 / 2 / 2 / 3 / 1 / 2 | THIN |
| Kent | 2 | 1.57 | 2.0 | 0 | 1 / 1 / 1 / 2 / 2 / 2 / 2 | THIN |
| Norfolk | 2 | 1.14 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 2 | THIN |
| Cambridgeshire | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Buckinghamshire | 1 | 0.71 | 1.0 | 0 | 0 / 0 / 1 / 1 / 1 / 1 / 1 | THIN |
| Essex | 1 | 0.71 | 1.0 | 0 | 0 / 0 / 1 / 1 / 1 / 1 / 1 | THIN |
| Gloucestershire | 1 | 0.29 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 1 / 1 | THIN |
| Greater Manchester - Manchester & Salford | 0 | 1.86 | 3.0 | 0 | 3 / 3 / 3 / 3 / 1 / 0 / 0 | THIN |
| West Midlands - Birmingham & Solihull | 0 | 1.57 | 2.0 | 0 | 3 / 3 / 2 / 2 / 1 / 0 / 0 | THIN |
| Yorkshire - North | 0 | 0.71 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 0 / 0 | THIN |
| London | 0 | 0.57 | 1.0 | 0 | 1 / 1 / 1 / 1 / 0 / 0 / 0 | THIN |
| Berkshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cumbria - North | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cumbria - South | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Devon | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Dorset | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Greater Manchester - South | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Hampshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Hertfordshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Lancashire - North | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| North East | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Nottinghamshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Somerset | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Surrey | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Sussex | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| West Midlands - Coventry & Warwickshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Wiltshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Yorkshire - East | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Yorkshire - South | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
