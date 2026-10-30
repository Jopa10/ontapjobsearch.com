# JobG8 Claims Support regional viability diagnostic

Canonical UK assessment universe: **78 markets**.
Observed feed dates: **7** (2026-10-24 to 2026-10-30).
Latest feed: **2026-10-30**.
Content-unique IN jobs on latest feed: **102**; unmapped/unknown region: **17**.

Diagnostic only: this does not activate a slice. `STRONG_REVIEW_CANDIDATE` is deliberately an evidence signal, not an automatic LIVE gate.

For this diagnostic, a region is `STRONG_REVIEW_CANDIDATE` when the latest feed has 6+ Claims Support jobs and at least 3 observed feed dates have 6+ jobs. `WATCH` means latest 4+ and at least 3 observed feed dates at 4+. This mirrors the existing 6+ recurrence style used elsewhere in Ontap as a conservative review signal; explicit approval is still required.

Strong review candidates: **4**.
Watch regions: **3**.

## Regional evidence

| Region | Latest | Avg | Median | 6+ days | Recent counts | Evidence |
|---|---:|---:|---:|---:|---|---|
| Greater Manchester - Manchester & Salford | 13 | 13.29 | 14.0 | 7 | 15 / 15 / 14 / 16 / 9 / 11 / 13 | STRONG_REVIEW_CANDIDATE |
| London | 11 | 12.00 | 12.0 | 7 | 14 / 14 / 12 / 13 / 9 / 11 / 11 | STRONG_REVIEW_CANDIDATE |
| Essex | 9 | 7.57 | 8.0 | 6 | 6 / 6 / 5 / 8 / 9 / 10 / 9 | STRONG_REVIEW_CANDIDATE |
| Yorkshire - West | 7 | 4.43 | 4.0 | 1 | 5 / 5 / 4 / 4 / 2 / 4 / 7 | WATCH |
| Bristol & Bath | 6 | 6.14 | 8.0 | 5 | 8 / 8 / 8 / 8 / 2 / 3 / 6 | STRONG_REVIEW_CANDIDATE |
| Staffordshire | 6 | 4.86 | 5.0 | 1 | 5 / 5 / 4 / 4 / 5 / 5 / 6 | WATCH |
| Scotland West - Glasgow | 5 | 7.86 | 9.0 | 4 | 11 / 11 / 9 / 9 / 5 / 5 / 5 | WATCH |
| West Midlands - Birmingham & Solihull | 3 | 4.71 | 5.0 | 3 | 6 / 6 / 5 / 7 / 3 / 3 / 3 | THIN |
| Sussex | 2 | 3.00 | 4.0 | 0 | 4 / 4 / 4 / 4 / 1 / 2 / 2 | THIN |
| Wales South - Cardiff & Vale | 2 | 2.29 | 3.0 | 0 | 3 / 3 / 3 / 3 / 0 / 2 / 2 | THIN |
| Berkshire | 2 | 2.00 | 2.0 | 0 | 2 / 2 / 2 / 2 / 2 / 2 / 2 | THIN |
| Cheshire - East | 2 | 2.00 | 2.0 | 0 | 2 / 2 / 2 / 2 / 2 / 2 / 2 | THIN |
| Lancashire - Central | 2 | 1.29 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 2 / 2 | THIN |
| Suffolk | 2 | 1.29 | 2.0 | 0 | 0 / 0 / 1 / 2 / 2 / 2 / 2 | THIN |
| Hampshire | 1 | 3.57 | 5.0 | 0 | 5 / 5 / 5 / 5 / 2 / 2 / 1 | THIN |
| North East | 1 | 2.57 | 3.0 | 0 | 4 / 4 / 3 / 4 / 1 / 1 / 1 | THIN |
| Merseyside - Liverpool | 1 | 2.29 | 3.0 | 0 | 3 / 3 / 3 / 4 / 1 / 1 / 1 | THIN |
| Greater Manchester - Wigan & Bolton | 1 | 2.14 | 3.0 | 0 | 3 / 3 / 3 / 3 / 1 / 1 / 1 | THIN |
| Kent | 1 | 1.86 | 2.0 | 0 | 3 / 3 / 2 / 2 / 1 / 1 / 1 | THIN |
| Gloucestershire | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Greater Manchester - South | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Surrey | 1 | 1.00 | 1.0 | 0 | 1 / 1 / 1 / 1 / 1 / 1 / 1 | THIN |
| Nottinghamshire | 1 | 0.86 | 1.0 | 0 | 1 / 1 / 1 / 1 / 0 / 1 / 1 | THIN |
| Cheshire - West | 1 | 0.71 | 1.0 | 0 | 1 / 1 / 0 / 0 / 1 / 1 / 1 | THIN |
| Leicestershire | 1 | 0.71 | 1.0 | 0 | 1 / 1 / 0 / 0 / 1 / 1 / 1 | THIN |
| Scotland West - Renfrewshire & Inverclyde | 1 | 0.71 | 1.0 | 0 | 1 / 1 / 0 / 0 / 1 / 1 / 1 | THIN |
| Shropshire | 1 | 0.43 | 0.0 | 0 | 0 / 0 / 0 / 0 / 1 / 1 / 1 | THIN |
| Yorkshire - South | 0 | 1.71 | 3.0 | 0 | 3 / 3 / 3 / 3 / 0 / 0 / 0 | THIN |
| Lancashire - Blackpool & Fylde | 0 | 0.14 | 0.0 | 0 | 0 / 0 / 1 / 0 / 0 / 0 / 0 | THIN |
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
| Northamptonshire | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
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
| Somerset | 0 | 0.00 | 0.0 | 0 | 0 / 0 / 0 / 0 / 0 / 0 / 0 | THIN |
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
