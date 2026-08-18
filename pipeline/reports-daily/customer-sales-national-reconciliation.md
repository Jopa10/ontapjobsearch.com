# Customer Sales national reconciliation

Branch-only diagnostic. Nothing here is live/published.

## Funnel

| Stage | All mapped/unknown rows | Ontap 33 regions |
|---|---:|---:|
| Current JobG8 feed | 10,000 | — |
| Broad Sales / Business Development possibles | 933 | 589 |
| Of those broad possibles: in Customer Sales scope | 225 (24.1%) | 109 (18.5%) |
| Customer/service crossover additions outside broad Sales/BD titles | +208 | +70 |
| Total in-scope Customer Sales rows | 433 | 179 |
| Campaign/dedupe-adjusted regional jobs | 217 | 125 |

Broad possibles outside the current Ontap 33 but mapped to another region: **258**. Broad possibles with unknown geography: **86**.

**Important:** campaign dedupe is deliberately regional. The same national campaign may count once in each genuinely relevant region, but repeated near-identical JobG8 rows inside one region count once.

## Ontap 33 — regional reconciliation

| Region | Broad possibles | In scope | Crossover adds | After campaign/dedupe | Employers | Top employer |
|---|---:|---:|---:|---:|---:|---|
| London | 124 | 36 | 9 | 29 | 23 | EE (5) |
| Bristol & Bath | 20 | 7 | 0 | 7 | 6 | Ernest Gordon Recruitment (2) |
| North East | 34 | 51 | 41 | 6 | 3 | EE (3) |
| Cambridgeshire | 19 | 6 | 1 | 6 | 6 | Red Recruit Ltd (1) |
| Hampshire | 34 | 5 | 1 | 5 | 5 | Mulberry Recruitment (1) |
| Yorkshire - West | 32 | 5 | 0 | 5 | 5 | SRG (1) |
| Kent | 30 | 5 | 1 | 5 | 4 | Tony Alan Recruitment (2) |
| Greater Manchester - Manchester & Salford | 26 | 5 | 2 | 5 | 5 | Chapman Tate Associates (1) |
| Gloucestershire | 16 | 5 | 0 | 5 | 5 | RE Recruitment (1) |
| Essex | 11 | 5 | 2 | 5 | 4 | Employment Specialists Ltd (2) |
| Buckinghamshire | 10 | 5 | 1 | 5 | 5 | ACS Recruitment Solutions Ltd (1) |
| Hertfordshire | 24 | 4 | 1 | 4 | 3 | Fortrade (2) |
| Yorkshire - South | 15 | 4 | 0 | 4 | 4 | Reed (1) |
| Yorkshire - North | 13 | 4 | 0 | 4 | 4 | CITRUS CONNECT LTD (1) |
| Devon | 13 | 5 | 3 | 3 | 3 | EE (1) |
| Surrey | 18 | 3 | 1 | 3 | 3 | First Military Recruitment Ltd (1) |
| Berkshire | 17 | 3 | 0 | 3 | 3 | Sandown Group (1) |
| Northamptonshire | 12 | 3 | 0 | 3 | 3 | Get Staffed Online Recruitment Limited (1) |
| Dorset | 10 | 3 | 1 | 3 | 3 | Kuehne+Nagel (1) |
| West Midlands - Birmingham & Solihull | 24 | 2 | 0 | 2 | 2 | Warwick Recruit Ltd (1) |
| Staffordshire | 12 | 2 | 0 | 2 | 2 | Red Recruit Ltd (1) |
| Norfolk | 7 | 2 | 1 | 2 | 2 | Reed (1) |
| Nottinghamshire | 6 | 2 | 1 | 2 | 2 | SF Partners (1) |
| Yorkshire - East | 6 | 2 | 1 | 2 | 2 | Consortium Professional Recruitment Ltd (1) |
| Greater Manchester - South | 1 | 2 | 2 | 2 | 2 | Jobwise Ltd (1) |
| Sussex | 16 | 1 | 0 | 1 | 1 | Global 4 Communications Ltd (1) |
| Oxfordshire | 10 | 1 | 0 | 1 | 1 | Vision Personnel (1) |
| Cumbria - South | 0 | 1 | 1 | 1 | 1 | Adecco (1) |
| Wiltshire | 9 | 0 | 0 | 0 | 0 |  |
| Lancashire - North | 6 | 0 | 0 | 0 | 0 |  |
| Cumbria - North | 5 | 0 | 0 | 0 | 0 |  |
| West Midlands - Coventry & Warwickshire | 5 | 0 | 0 | 0 | 0 |  |
| Somerset | 4 | 0 | 0 | 0 | 0 |  |

## Main reasons broad possibles fall out

| Rule-out bucket | Rows |
|---|---:|
| OUT_TITLE | 455 |
| OUT_OTHER_SALES | 172 |
| OUT_ACCOUNT_AMBIGUOUS | 36 |
| OUT_ACCOUNT_SPECIALIST | 20 |
| OUT_FIELD_CAMPAIGN | 17 |
| OUT_PURE_SERVICE | 8 |

## Largest repeated campaign groups

| Region | Employer | Repeated rows | Example title(s) |
|---|---|---:|---|
| Cheshire - Warrington & Halton | EE | 41 | Call Centre Agent - Uncapped Commission; Call Centre Operator - Uncapped Commission; Contact Centre Agent - Uncapped Commission |
| North East | EE | 41 | Call Centre Agent; Call Centre Operator; Customer Service Advisor |
| Cornwall | EE | 24 | Call Centre Agent; Call Centre Operator; Customer Service Advisor |
| Greater Manchester - Wigan & Bolton | EE | 15 | Call Centre Agent - Uncapped Commission; Call Centre Operator - Uncapped Commission; Contact Centre Agent - Uncapped Commission |
| Other / Unknown | EE | 13 | Call Centre Agent - Uncapped Commission; Call Centre Operator - Uncapped Commission; Contact Centre Agent - Uncapped Commission |
| Merseyside - St Helens & Knowsley | EE | 12 | Call Centre Agent - Uncapped Commission; Call Centre Operator - Uncapped Commission; Contact Centre Agent - Uncapped Commission |
| Other / Unknown | EE | 12 | Call Centre Agent; Call Centre Operator; Customer Service Advisor |
| Cheshire - East | EE | 11 | Call Centre Agent - Uncapped Commission; Call Centre Operator - Uncapped Commission; Contact Centre Agent - Uncapped Commission |
| Cheshire - West | EE | 9 | Call Centre Agent - Uncapped Commission; Call Centre Operator - Uncapped Commission; Contact Centre Agent - Uncapped Commission |
| Wales South - Valleys | EE | 7 | Call Centre Agent; Call Centre Operator; Customer Service Advisor |
| North East | EE | 6 | Sales Advisor - Part Time |
| Northern Ireland - East | EE | 5 | Sales Advisor |
| Scotland Central - Tayside | EE | 5 | Apprentice Sales Advisor - Uncapped Commission |
| Wales South - Swansea Bay | EE | 5 | Call Centre Agent; Call Centre Operator; Customer Service Advisor |
| Cheshire - Warrington & Halton | EE | 4 | Apprentice Sales Advisor - Uncapped Commission |
| London | EE | 4 | Call Centre Agent; Call Centre Operator; Customer Service Advisor |
| Other / Unknown | EE | 4 | Call Centre Agent; Call Centre Operator; Customer Service Advisor |
| Devon | EE | 3 | Customer Service Advisor |
| London | EE | 3 | Call Centre Agent; Call Centre Operator; Customer Service Representative |
| Other / Unknown | EE | 3 | Sales Advisor |

## Mapped regions outside the current Ontap 33

| Region | Broad possibles | In scope | After campaign/dedupe |
|---|---:|---:|---:|
| Cheshire - West | 18 | 13 | 5 |
| Lincolnshire | 14 | 5 | 5 |
| Wales South - Cardiff & Vale | 5 | 5 | 5 |
| Cheshire - Warrington & Halton | 31 | 46 | 3 |
| Wales South - Swansea Bay | 13 | 7 | 3 |
| Cheshire - East | 10 | 13 | 3 |
| Suffolk | 9 | 3 | 3 |
| Bedfordshire | 5 | 3 | 3 |
| Greater Manchester - Wigan & Bolton | 9 | 16 | 2 |
| North Scotland | 9 | 2 | 2 |
| Northern Ireland - East | 9 | 6 | 2 |
| Shropshire | 8 | 2 | 2 |
| Merseyside - St Helens & Knowsley | 7 | 13 | 2 |
| Worcestershire | 6 | 2 | 2 |
| North Wales - East | 5 | 2 | 2 |
| Lancashire - West | 4 | 2 | 2 |
| Merseyside - Liverpool | 3 | 2 | 2 |
| Northern Ireland - West | 3 | 2 | 2 |
| Cornwall | 2 | 25 | 2 |
| Wales South - Valleys | 2 | 10 | 2 |
| Scotland Central - Tayside | 10 | 5 | 1 |
| Scotland West - Glasgow | 10 | 1 | 1 |
| Leicestershire | 6 | 1 | 1 |
| Scotland Central - Fife | 6 | 2 | 1 |
| East Midlands | 5 | 1 | 1 |
| Scotland Central - Edinburgh & Lothians | 5 | 1 | 1 |
| West Midlands - Black Country | 5 | 1 | 1 |
| Derbyshire | 4 | 1 | 1 |
| West Lothian | 2 | 1 | 1 |
| West Midlands | 1 | 1 | 1 |

## Interpretation

The broad headline is a discovery universe, not publishable inventory. The decision point for a third Ontap family is the campaign/dedupe-adjusted regional column, plus employer breadth and manual QA of the largest slices.
