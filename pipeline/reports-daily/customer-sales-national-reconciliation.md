# Customer Sales national reconciliation

Branch-only diagnostic. Nothing here is live/published.

## Funnel

| Stage | All mapped/unknown rows | Ontap 33 regions |
|---|---:|---:|
| Current JobG8 feed | 10,000 | — |
| Broad Sales / Business Development possibles | 933 | 589 |
| In-scope Customer Sales rows | 225 (24.1% of broad) | 109 (18.5% of broad) |
| Campaign/dedupe-adjusted regional jobs | 181 | 103 |

Broad possibles outside the current Ontap 33 but mapped to another region: **258**. Broad possibles with unknown geography: **86**.

**Important:** campaign dedupe is deliberately regional. The same national campaign may count once in each genuinely relevant region, but repeated near-identical JobG8 rows inside one region count once.

## Ontap 33 — regional reconciliation

| Region | Broad possibles | In scope | After campaign/dedupe | Employers | Top employer |
|---|---:|---:|---:|---:|---|
| London | 124 | 27 | 26 | 22 | EE (3) |
| Bristol & Bath | 20 | 7 | 7 | 6 | Ernest Gordon Recruitment (2) |
| North East | 34 | 10 | 5 | 3 | GoFibre Broadband Limited (2) |
| Yorkshire - West | 32 | 5 | 5 | 5 | SRG (1) |
| Cambridgeshire | 19 | 5 | 5 | 5 | Red Recruit Ltd (1) |
| Gloucestershire | 16 | 5 | 5 | 5 | RE Recruitment (1) |
| Hampshire | 34 | 4 | 4 | 4 | Mulberry Recruitment (1) |
| Kent | 30 | 4 | 4 | 3 | Tony Alan Recruitment (2) |
| Yorkshire - South | 15 | 4 | 4 | 4 | Reed (1) |
| Yorkshire - North | 13 | 4 | 4 | 4 | CITRUS CONNECT LTD (1) |
| Buckinghamshire | 10 | 4 | 4 | 4 | ACS Recruitment Solutions Ltd (1) |
| Greater Manchester - Manchester & Salford | 26 | 3 | 3 | 3 | Chapman Tate Associates (1) |
| Hertfordshire | 24 | 3 | 3 | 2 | Fortrade (2) |
| Berkshire | 17 | 3 | 3 | 3 | Sandown Group (1) |
| Northamptonshire | 12 | 3 | 3 | 3 | Get Staffed Online Recruitment Limited (1) |
| Essex | 11 | 3 | 3 | 3 | Employment Specialists Ltd (1) |
| West Midlands - Birmingham & Solihull | 24 | 2 | 2 | 2 | Warwick Recruit Ltd (1) |
| Surrey | 18 | 2 | 2 | 2 | BODYPOWER SPORTS LTD (1) |
| Devon | 13 | 2 | 2 | 2 | Acorn by Synergie (1) |
| Staffordshire | 12 | 2 | 2 | 2 | Red Recruit Ltd (1) |
| Dorset | 10 | 2 | 2 | 2 | Kuehne+Nagel (1) |
| Sussex | 16 | 1 | 1 | 1 | Global 4 Communications Ltd (1) |
| Oxfordshire | 10 | 1 | 1 | 1 | Vision Personnel (1) |
| Norfolk | 7 | 1 | 1 | 1 | ALH Recruitment Ltd (1) |
| Nottinghamshire | 6 | 1 | 1 | 1 | GBR Recruitment Ltd (1) |
| Yorkshire - East | 6 | 1 | 1 | 1 | Consortium Professional Recruitment (1) |
| Wiltshire | 9 | 0 | 0 | 0 |  |
| Lancashire - North | 6 | 0 | 0 | 0 |  |
| Cumbria - North | 5 | 0 | 0 | 0 |  |
| West Midlands - Coventry & Warwickshire | 5 | 0 | 0 | 0 |  |
| Somerset | 4 | 0 | 0 | 0 |  |
| Greater Manchester - South | 1 | 0 | 0 | 0 |  |
| Cumbria - South | 0 | 0 | 0 | 0 |  |

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
| Cheshire - Warrington & Halton | EE | 12 | Sales Advisor - Uncapped Commission; Sales Agent - Uncapped Commission; Sales Representative - Uncapped Commission |
| North East | EE | 6 | Sales Advisor - Part Time |
| Northern Ireland - East | EE | 5 | Sales Advisor |
| Scotland Central - Tayside | EE | 5 | Apprentice Sales Advisor - Uncapped Commission |
| Cheshire - Warrington & Halton | EE | 4 | Apprentice Sales Advisor - Uncapped Commission |
| Cheshire - East | EE | 3 | Sales Advisor - Uncapped Commission; Sales Agent - Uncapped Commission; Sales Representative - Uncapped Commission |
| Cheshire - West | EE | 3 | Sales Advisor - Uncapped Commission; Sales Agent - Uncapped Commission; Sales Representative - Uncapped Commission |
| Greater Manchester - Wigan & Bolton | EE | 3 | Sales Advisor - Uncapped Commission; Sales Agent - Uncapped Commission; Sales Representative - Uncapped Commission |
| Merseyside - St Helens & Knowsley | EE | 3 | Sales Advisor - Uncapped Commission; Sales Agent - Uncapped Commission; Sales Representative - Uncapped Commission |
| Other / Unknown | EE | 3 | Sales Advisor - Uncapped Commission; Sales Agent - Uncapped Commission; Sales Representative - Uncapped Commission |
| Other / Unknown | EE | 3 | Sales Advisor |
| Other / Unknown | EE | 3 | Sales Advisor - Part Time Evenings |
| London | Cure Talent Ltd | 2 | Business Development Executive |
| Scotland Central - Fife | EE | 2 | Apprentice Sales Advisor - Uncapped Commission |
| Wales South - Valleys | EE | 2 | Sales Advisor - Part Time Evenings |

## Mapped regions outside the current Ontap 33

| Region | Broad possibles | In scope | After campaign/dedupe |
|---|---:|---:|---:|
| Cheshire - West | 18 | 7 | 5 |
| Lincolnshire | 14 | 5 | 5 |
| Wales South - Cardiff & Vale | 5 | 5 | 5 |
| Cheshire - Warrington & Halton | 31 | 17 | 3 |
| Wales South - Swansea Bay | 13 | 3 | 3 |
| Cheshire - East | 10 | 5 | 3 |
| Suffolk | 9 | 3 | 3 |
| Greater Manchester - Wigan & Bolton | 9 | 4 | 2 |
| North Scotland | 9 | 2 | 2 |
| Northern Ireland - East | 9 | 6 | 2 |
| Shropshire | 8 | 2 | 2 |
| Merseyside - St Helens & Knowsley | 7 | 4 | 2 |
| Bedfordshire | 5 | 2 | 2 |
| North Wales - East | 5 | 2 | 2 |
| Lancashire - West | 4 | 2 | 2 |
| Merseyside - Liverpool | 3 | 2 | 2 |
| Northern Ireland - West | 3 | 2 | 2 |
| Scotland Central - Tayside | 10 | 5 | 1 |
| Scotland West - Glasgow | 10 | 1 | 1 |
| Leicestershire | 6 | 1 | 1 |
| Scotland Central - Fife | 6 | 2 | 1 |
| Worcestershire | 6 | 1 | 1 |
| East Midlands | 5 | 1 | 1 |
| Scotland Central - Edinburgh & Lothians | 5 | 1 | 1 |
| West Midlands - Black Country | 5 | 1 | 1 |
| Derbyshire | 4 | 1 | 1 |
| Wales South - Valleys | 2 | 2 | 1 |
| West Lothian | 2 | 1 | 1 |
| West Midlands | 1 | 1 | 1 |
| Scotland Central - Falkirk & Stirling | 5 | 0 | 0 |

## Interpretation

The broad headline should not be treated as publishable inventory. The decision point for a third Ontap family is the campaign/dedupe-adjusted regional column, plus employer breadth and manual QA of the largest slices.
