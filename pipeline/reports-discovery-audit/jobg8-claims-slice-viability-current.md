# JobG8 Claims Support regional viability diagnostic

Canonical UK assessment universe: **78 markets**.
Observed feed dates: **7** (2026-09-06 to 2026-09-12).
Latest feed: **2026-09-12**.
Content-unique IN jobs on latest feed: **55**; unmapped/unknown region: **4**.

Diagnostic only: this does not activate a slice. `STRONG_REVIEW_CANDIDATE` is deliberately an evidence signal, not an automatic LIVE gate.

For this diagnostic, a region is `STRONG_REVIEW_CANDIDATE` when the latest feed has 6+ Claims Support jobs and at least 3 observed feed dates have 6+ jobs. `WATCH` means latest 4+ and at least 3 observed feed dates at 4+. This mirrors the existing 6+ recurrence style used elsewhere in Ontap as a conservative review signal; explicit approval is still required.

Strong review candidates: **1**.
Watch regions: **4**.

## Regional evidence

| Region | Latest | Avg | Median | 6+ days | Recent counts | Evidence |
|---|---:|---:|---:|---:|---|---|
| Essex | 8 | 6.86 | 8.0 | 5 | 4 / 4 / 7 / 9 / 8 / 8 / 8 | STRONG_REVIEW_CANDIDATE |
| London | 5 | 4.43 | 5.0 | 0 | 3 / 3 / 5 / 5 / 5 / 5 / 5 | WATCH |
| Greater Manchester - Manchester & Salford | 5 | 3.71 | 4.0 | 0 | 2 / 2 / 4 / 4 / 4 / 5 / 5 | WATCH |
| Staffordshire | 5 | 3.43 | 4.0 | 0 | 2 / 1 / 2 / 4 / 5 / 5 / 5 | WATCH |
| Greater Manchester - Wigan & Bolton | 4 | 3.43 | 4.0 | 0 | 2 / 2 / 4 / 4 / 4 / 4 / 4 | WATCH |
| Scotland West - Glasgow | 3 | 2.71 | 3.0 | 0 | 2 / 2 / 3 / 3 / 3 / 3 / 3 | THIN |
| Yorkshire - West | 2 | 2.71 | 3.0 | 0 | 3 / 4 / 3 / 3 / 2 / 2 / 2 | THIN |
| Kent | 2 | 2.00 | 2.0 | 0 | 2 / 2 / 2 / 2 / 2 / 2 / 2 | THIN |
| West Midlands - Birmingham & Solihull | 2 | 2.00 | 2.0 | 0 | 2 / 2 / 2 / 2 / 2 / 2 / 2 | THIN |
| Northamptonshire | 2 | 1.86 | 2.0 | 0 | 1 / 2 / 2 / 2 / 2 / 2 / 2 | THIN |
| Dorset | 2 | 1.43 | 2.0 | 0 | 0 / 0 / 2 / 2 / 2 / 2 / 2 | THIN |
| Cheshire - West | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Hampshire | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Leicestershire | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| North East | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Oxfordshire | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Scotland Central - Fife | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Bristol & Bath | 1 | 0.71 | 1.0 | 0 | 0 / 0 / 1 / 1 / 1 / 1 / 1 | THIN |
| Cheshire - East | 1 | 0.71 | 1.0 | 0 | 0 / 0 / 1 / 1 / 1 / 1 / 1 | THIN |
| Merseyside - Liverpool | 1 | 0.71 | 1.0 | 0 | 0 / 0 / 1 / 1 / 1 / 1 / 1 | THIN |
| Greater Manchester - North | 1 | 0.57 | 1.0 | 0 | 0 / 0 / 0 / 1 / 1 / 1 / 1 | THIN |
| Suffolk | 1 | 0.29 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 1 / 1 | THIN |
| Wales South - Swansea Bay | 0 | 0.71 | 1.0 | 0 | 0 / 1 / 1 / 1 / 1 / 1 / 0 | THIN |
| Wales South - Cardiff & Vale | 0 | 0.43 | 0.0 | 0 | 1 / 1 / 1 / 0 / 0 / 0 / 0 | THIN |
| Gloucestershire | 0 | 0.29 | 0.0 | 0 | 1 / 1 / 0 / 0 / 0 / 0 / 0 | THIN |
| Lancashire - Central | 0 | 0.29 | 0.0 | 0 | 1 / 1 / 0 / 0 / 0 / 0 / 0 | THIN |
| Norfolk | 0 | 0.29 | 0.0 | 0 | 1 / 1 / 0 / 0 / 0 / 0 / 0 | THIN |
| Greater Manchester - South | 0 | 0.14 | 0.0 | 0 | 0 / 1 / 0 / 0 / 0 / 0 / 0 | THIN |
| Bedfordshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Berkshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Buckinghamshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cambridgeshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cheshire - Warrington & Halton | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cornwall | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cumbria - North | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cumbria - South | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Cumbria - West | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Derbyshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Devon | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
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
| North Scotland | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| North Wales - East | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| North Wales - West | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Northern Ireland - East | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Northern Ireland - West | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Nottinghamshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Rutland | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland - Borders | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland Central - Edinburgh & Lothians | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland Central - Falkirk & Stirling | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland Central - Tayside | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland West - Ayrshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland West - Lanarkshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Scotland West - Renfrewshire & Inverclyde | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Shropshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Somerset | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Surrey | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Sussex | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Wales - Mid | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Wales - West | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Wales South - Gwent | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Wales South - Valleys | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| West Midlands - Black Country | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| West Midlands - Coventry & Warwickshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Wiltshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Worcestershire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Yorkshire - East | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Yorkshire - North | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
| Yorkshire - South | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
