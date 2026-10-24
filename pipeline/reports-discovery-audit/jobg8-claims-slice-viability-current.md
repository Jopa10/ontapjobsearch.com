# JobG8 Claims Support regional viability diagnostic

Canonical UK assessment universe: **78 markets**.
Observed feed dates: **7** (2026-10-18 to 2026-10-24).
Latest feed: **2026-10-24**.
Content-unique IN jobs on latest feed: **125**; unmapped/unknown region: **15**.

Diagnostic only: this does not activate a slice. `STRONG_REVIEW_CANDIDATE` is deliberately an evidence signal, not an automatic LIVE gate.

For this diagnostic, a region is `STRONG_REVIEW_CANDIDATE` when the latest feed has 6+ Claims Support jobs and at least 3 observed feed dates have 6+ jobs. `WATCH` means latest 4+ and at least 3 observed feed dates at 4+. This mirrors the existing 6+ recurrence style used elsewhere in Ontap as a conservative review signal; explicit approval is still required.

Strong review candidates: **4**.
Watch regions: **7**.

## Regional evidence

| Region | Latest | Avg | Median | 6+ days | Recent counts | Evidence |
|---|---:|---:|---:|---:|---|---|
| London | 15 | 16.14 | 16.0 | 7 | 17 / 17 / 17 / 16 / 16 / 15 / 15 | STRONG_REVIEW_CANDIDATE |
| Greater Manchester - Manchester & Salford | 13 | 13.29 | 13.0 | 7 | 15 / 13 / 13 / 13 / 13 / 13 / 13 | STRONG_REVIEW_CANDIDATE |
| Scotland West - Glasgow | 11 | 10.43 | 10.0 | 7 | 10 / 10 / 10 / 10 / 11 / 11 / 11 | STRONG_REVIEW_CANDIDATE |
| Bristol & Bath | 8 | 7.14 | 7.0 | 7 | 7 / 7 / 7 / 7 / 7 / 7 / 8 | STRONG_REVIEW_CANDIDATE |
| Essex | 7 | 5.00 | 5.0 | 2 | 4 / 4 / 4 / 5 / 5 / 6 / 7 | WATCH |
| West Midlands - Birmingham & Solihull | 6 | 5.14 | 5.0 | 1 | 5 / 5 / 5 / 5 / 5 / 5 / 6 | WATCH |
| Hampshire | 5 | 5.00 | 5.0 | 0 | 5 / 5 / 5 / 5 / 5 / 5 / 5 | WATCH |
| Yorkshire - West | 5 | 4.57 | 4.0 | 1 | 6 / 5 / 4 / 4 / 4 / 4 / 5 | WATCH |
| Staffordshire | 5 | 3.29 | 4.0 | 0 | 1 / 1 / 3 / 4 / 4 / 5 / 5 | WATCH |
| North East | 4 | 4.00 | 4.0 | 0 | 4 / 4 / 4 / 4 / 4 / 4 / 4 | WATCH |
| Sussex | 4 | 4.00 | 4.0 | 0 | 4 / 4 / 4 / 4 / 4 / 4 / 4 | WATCH |
| Merseyside - Liverpool | 3 | 4.14 | 4.0 | 1 | 5 / 6 / 5 / 4 / 3 / 3 / 3 | THIN |
| Kent | 3 | 3.71 | 4.0 | 0 | 4 / 4 / 4 / 4 / 4 / 3 / 3 | THIN |
| Greater Manchester - Wigan & Bolton | 3 | 3.00 | 3.0 | 0 | 3 / 3 / 3 / 3 / 3 / 3 / 3 | THIN |
| Wales South - Cardiff & Vale | 3 | 3.00 | 3.0 | 0 | 3 / 3 / 3 / 3 / 3 / 3 / 3 | THIN |
| Yorkshire - South | 3 | 3.00 | 3.0 | 0 | 3 / 3 / 3 / 3 / 3 / 3 / 3 | THIN |
| Cheshire - East | 2 | 1.43 | 2.0 | 0 | 0 / 0 / 2 / 2 / 2 / 2 / 2 | THIN |
| Berkshire | 2 | 1.29 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 2 / 2 | THIN |
| Nottinghamshire | 1 | 1.71 | 2.0 | 0 | 2 / 2 / 2 / 2 / 2 / 1 / 1 | THIN |
| Cheshire - West | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Gloucestershire | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Leicestershire | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Scotland West - Renfrewshire & Inverclyde | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Surrey | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Greater Manchester - South | 1 | 0.43 | 0.0 | 0 | 0 / 0 / 0 / 0 / 1 / 1 / 1 | THIN |
| Lancashire - Central | 1 | 0.29 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 1 / 1 | THIN |
| Northamptonshire | 0 | 1.14 | 2.0 | 0 | 2 / 2 / 2 / 2 / 0 / 0 / 0 | THIN |
| Bedfordshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Buckinghamshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cambridgeshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cheshire - Warrington & Halton | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cornwall | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cumbria - North | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cumbria - South | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cumbria - West | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Derbyshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Devon | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Dorset | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Greater Manchester - North | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Herefordshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Hertfordshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Lancashire - Blackpool & Fylde | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Lancashire - East | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Lancashire - North | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Lancashire - West | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Lincolnshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Merseyside - Sefton | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Merseyside - St Helens & Knowsley | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Merseyside - Wirral | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Norfolk | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| North Scotland | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| North Wales - East | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| North Wales - West | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Northern Ireland - East | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Northern Ireland - West | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Oxfordshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Rutland | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland - Borders | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland Central - Edinburgh & Lothians | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland Central - Falkirk & Stirling | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland Central - Fife | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland Central - Tayside | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland West - Ayrshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland West - Lanarkshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Shropshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Somerset | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Suffolk | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Wales - Mid | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Wales - West | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Wales South - Gwent | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Wales South - Swansea Bay | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Wales South - Valleys | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| West Midlands - Black Country | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| West Midlands - Coventry & Warwickshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Wiltshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Worcestershire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Yorkshire - East | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Yorkshire - North | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
