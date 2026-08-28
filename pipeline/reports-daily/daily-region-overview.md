# Ontap daily regional overview

Generated: 2026-08-28T14:49:27+01:00

## SITEWIDE RECONCILIATION

| Measure | Count |
|---|---:|
| Unique live jobs | 1,482 |
| Unique JobG8 jobs | 1,059 |
| Unique non-JobG8 jobs | 423 |
| Regional/category slice placements | 1,529 |
| Jobs appearing on multiple slices | 47 |
| Extra slice placements | 47 |
| Unique jobs outside governed slices | 0 |
| Jobs found in non-LIVE slices | 0 |

**Reconciliation: 1,482 unique jobs + 47 extra slice placements = 1,529 regional/category slice placements.**

Latest source-count CSV: `pipeline/reports-daily/live-job-source-count-2026-08-28.csv` — **STALE — CSV says 1,400 for 2026-08-28**.

### Provider breakdown

| Provider | Unique live jobs | Jobs on 2+ slices | Extra slice placements |
|---|---:|---:|---:|
| JobG8 | 1,059 | 47 | 47 |
| NEJobs | 30 | 0 | 0 |
| NHS Jobs | 206 | 0 | 0 |
| Teaching Vacancies | 185 | 0 | 0 |
| VONNE | 2 | 0 | 0 |

> LIVE counts come directly from the current published `app/` JSON, deduplicated within each canonical region/family slice while preserving legitimate appearances in more than one family. This is the live-site authority for the reconciliation above; the dated source-count CSV is shown only as a freshness cross-check. The overview covers all 78 assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 78-market coverage has run, NOT LIVE Admin/Support and Customer Service may fall back to the latest all-region Module 2 profile (2026-08-17), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-08-28) used by the production family run, across 78 UK markets with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across 78 UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across 78, 78, 78 and 78 UK markets respectively, using their governed production boundaries and canonical geo. NOT LIVE Customer Service / Contact Centre temporarily retains the overview builder's latest Module 2 profile fallback until the first eight-family coverage run. All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

## LIVE

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire |  |  |  |  |  |  |  |  |
| Berkshire | 25 |  |  |  | 7 |  | 1 |  |
| Bristol & Bath | 22 |  |  |  |  | 9 |  |  |
| Buckinghamshire | 23 |  |  |  |  |  |  |  |
| Cambridgeshire | 43 |  |  |  |  |  |  |  |
| Cheshire - East | 13 |  |  |  |  |  |  |  |
| Cheshire - Warrington & Halton | 6 |  |  |  |  |  |  |  |
| Cheshire - West | 4 |  |  |  |  |  |  |  |
| Cornwall | 6 |  |  |  |  |  |  |  |
| Cumbria - North |  |  |  |  |  |  |  |  |
| Cumbria - South |  | CHECK |  |  |  |  |  |  |
| Cumbria - West |  |  |  |  |  |  |  |  |
| Derbyshire | 8 |  |  |  |  |  |  |  |
| Devon | 34 |  |  |  |  | 9 |  |  |
| Dorset | 16 |  |  |  |  |  |  |  |
| Essex | 43 |  |  | 3 |  |  |  |  |
| Gloucestershire | 32 |  |  |  |  | 9 |  |  |
| Greater Manchester - Manchester & Salford | 34 |  | 8 |  | 10 |  | 4 |  |
| Greater Manchester - North |  |  |  |  |  |  |  |  |
| Greater Manchester - South | 7 |  |  |  |  |  |  |  |
| Greater Manchester - Wigan & Bolton | 5 |  |  |  |  |  |  |  |
| Hampshire | 54 | 11 |  |  |  |  |  | CHECK |
| Herefordshire |  |  |  |  |  |  |  |  |
| Hertfordshire | 30 |  |  |  |  |  |  |  |
| Kent | 50 | 10 |  |  |  |  |  |  |
| Lancashire - Blackpool & Fylde |  |  |  |  |  |  |  |  |
| Lancashire - Central |  |  |  |  |  |  |  |  |
| Lancashire - East |  |  |  |  |  |  |  |  |
| Lancashire - North |  |  |  |  |  |  |  |  |
| Lancashire - West |  |  |  |  |  |  |  |  |
| Leicestershire | 39 |  |  |  |  |  |  |  |
| Lincolnshire | 20 |  |  |  |  |  |  |  |
| London | 138 | 17 | 16 | 9 | 29 |  | 6 | CHECK |
| Merseyside - Liverpool | 9 |  |  |  |  |  |  |  |
| Merseyside - Sefton |  |  |  |  |  |  |  |  |
| Merseyside - St Helens & Knowsley |  |  |  |  |  |  |  |  |
| Merseyside - Wirral |  |  |  |  |  |  |  |  |
| Norfolk | 33 |  |  | CHECK |  |  |  |  |
| North East | 68 | 4 | 4 |  |  | 7 |  |  |
| North Scotland |  |  |  |  |  |  |  |  |
| North Wales - East |  |  |  |  |  |  |  |  |
| North Wales - West |  |  |  |  |  |  |  |  |
| Northamptonshire | 28 |  |  |  |  |  |  |  |
| Northern Ireland - East | 8 |  |  |  |  | 10 |  |  |
| Northern Ireland - West |  |  |  |  |  |  |  |  |
| Nottinghamshire | 23 |  |  |  |  |  | 3 |  |
| Oxfordshire | 51 | 6 |  |  |  |  |  |  |
| Rutland |  |  |  |  |  |  |  |  |
| Scotland - Borders |  |  |  |  |  |  |  |  |
| Scotland Central - Edinburgh & Lothians | 6 |  |  |  |  |  |  |  |
| Scotland Central - Falkirk & Stirling |  |  |  |  |  |  |  |  |
| Scotland Central - Fife |  |  |  |  |  |  |  |  |
| Scotland Central - Tayside |  |  |  |  |  |  |  |  |
| Scotland West - Ayrshire |  |  |  |  |  |  |  |  |
| Scotland West - Glasgow | 11 |  |  |  |  |  |  |  |
| Scotland West - Lanarkshire |  |  |  |  |  |  |  |  |
| Scotland West - Renfrewshire & Inverclyde |  |  |  |  |  |  |  |  |
| Shropshire | 15 |  |  |  |  | 10 |  |  |
| Somerset | 17 |  |  |  |  |  |  |  |
| Staffordshire | 27 |  |  |  |  |  |  | CHECK |
| Suffolk | 13 |  |  | CHECK |  |  |  |  |
| Surrey | 54 | 3 |  |  | 8 |  |  | 6 |
| Sussex | 32 | 7 |  |  |  |  |  |  |
| Wales - Mid |  |  |  |  |  |  |  |  |
| Wales - West |  |  |  |  |  |  |  |  |
| Wales South - Cardiff & Vale |  |  |  |  |  |  |  |  |
| Wales South - Gwent |  |  |  |  |  |  |  |  |
| Wales South - Swansea Bay |  |  |  |  |  |  |  |  |
| Wales South - Valleys |  |  |  |  |  |  |  |  |
| West Midlands - Birmingham & Solihull | 25 |  |  |  | 3 |  | 4 |  |
| West Midlands - Black Country | 11 |  |  |  |  |  |  |  |
| West Midlands - Coventry & Warwickshire | 31 |  |  |  |  |  |  |  |
| Wiltshire | 26 | 6 |  |  |  |  |  |  |
| Worcestershire | 12 |  |  |  |  |  |  |  |
| Yorkshire - East | 19 |  |  |  |  |  |  |  |
| Yorkshire - North | 23 |  |  |  |  | 13 |  |  |
| Yorkshire - South | 19 | 2 |  |  |  |  |  |  |
| Yorkshire - West | 45 | 3 | 3 |  |  | 8 | 3 |  |

## NOT LIVE

> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire | 6 / 4.7 / 2/7 | 0 / 0.3 / 0/7 | 2 / 2.3 / 0/7 | 4 / 4.4 / 0/5 | 2 / 1.2 / 0/5 | 0 / 0.5 / 0/2 | 1 / 1.2 / 0/4 | 2 |
| Berkshire |  | 5 / 3.3 / 0/7 | 0 / 0.9 / 0/7 | 0 / 0.8 / 0/5 |  | 0 / 0.5 / 0/2 |  | 7 |
| Bristol & Bath |  | 1 / 1.3 / 0/7 | 5 / 6.9 / 6/7 | 4 / 4.2 / 1/5 | 4 / 1.8 / 0/5 |  | 2 / 2.0 / 0/4 | 1 |
| Buckinghamshire |  | 0 / 1.1 / 0/7 | 0 / 0.6 / 0/7 | 1 / 1.6 / 0/5 | 4 / 2.4 / 0/5 | 3 / 3.5 / 0/2 | 1 / 1.2 / 0/4 | 4 |
| Cambridgeshire |  | 0 / 0.1 / 0/7 | 1 / 2.9 / 0/7 | 2 / 1.6 / 0/5 | 3 / 2.0 / 0/5 | 9 / 9.0 / 2/2 | 0 / 0.2 / 0/4 | 2 |
| Cheshire - East |  | 1 / 1.0 / 0/7 | 2 / 1.9 / 0/7 | 0 / 0.4 / 0/5 | 2 / 1.2 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.0 / 0/4 | 2 |
| Cheshire - Warrington & Halton |  | 1 / 1.6 / 0/7 | 0 / 1.9 / 0/7 | 1 / 1.4 / 0/5 | 0 / 0.0 / 0/5 | 7 / 6.0 / 1/2 | 0 / 0.2 / 0/4 | 1 |
| Cheshire - West |  | 2 / 2.0 / 0/7 | 0 / 3.0 / 0/7 | 1 / 0.8 / 0/5 | 2 / 1.2 / 0/5 | 2 / 3.0 / 0/2 | 0 / 0.2 / 0/4 | 1 |
| Cornwall |  | 3 / 1.7 / 0/7 | 0 / 0.7 / 0/7 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 | 0 / 0.0 / 0/4 | 55 |
| Cumbria - North | 1 / 2.0 / 0/7 | 2 / 4.3 / 3/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| Cumbria - South | 1 / 1.3 / 0/7 |  | 1 / 0.9 / 0/7 | 0 / 0.0 / 0/5 | 1 / 0.6 / 0/5 | 1 / 1.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| Cumbria - West | 2 / 1.9 / 0/7 | 0 / 1.1 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 1 / 0.5 / 0/2 | 0 / 0.0 / 0/4 | 1 |
| Derbyshire |  | 1 / 0.4 / 0/7 | 2 / 2.6 / 0/7 | 0 / 0.6 / 0/5 | 1 / 0.4 / 0/5 | 5 / 4.5 / 0/2 | 0 / 0.0 / 0/4 | 1 |
| Devon |  | 0 / 0.0 / 0/7 | 4 / 3.4 / 0/7 | 2 / 2.8 / 0/5 | 1 / 0.2 / 0/5 |  | 1 / 1.5 / 0/4 | — |
| Dorset |  | 1 / 1.1 / 0/7 | 5 / 5.0 / 2/7 | 0 / 0.4 / 0/5 | 1 / 0.8 / 0/5 | 4 / 4.0 / 0/2 | 0 / 0.0 / 0/4 | 3 |
| Essex |  | 0 / 0.7 / 0/7 | 1 / 1.9 / 0/7 |  | 3 / 2.2 / 0/5 | 9 / 9.0 / 2/2 | 1 / 1.2 / 0/4 | 3 |
| Gloucestershire |  | 0 / 0.3 / 0/7 | 1 / 1.6 / 0/7 | 0 / 0.0 / 0/5 | 5 / 2.4 / 0/5 |  | 1 / 1.0 / 0/4 | — |
| Greater Manchester - Manchester & Salford |  | 2 / 1.3 / 0/7 |  | 2 / 5.2 / 2/5 |  | 5 / 5.0 / 0/2 |  | 8 |
| Greater Manchester - North | 2 / 3.6 / 1/7 | 0 / 0.0 / 0/7 | 0 / 0.3 / 0/7 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.2 / 0/4 | 4 |
| Greater Manchester - South |  | 1 / 1.3 / 0/7 | 0 / 1.0 / 0/7 | 1 / 0.6 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.0 / 0/4 | 5 |
| Greater Manchester - Wigan & Bolton |  | 0 / 0.0 / 0/7 | 0 / 1.0 / 0/7 | 0 / 0.4 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 1 / 1.0 / 0/4 | 2 |
| Hampshire |  |  | 7 / 6.3 / 4/7 | 2 / 2.6 / 0/5 | 4 / 3.8 / 0/5 | 4 / 4.5 / 0/2 | 3 / 3.5 / 0/4 |  |
| Herefordshire | 3 / 1.9 / 0/7 | 1 / 0.3 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 2 / 2.5 / 0/2 | 0 / 0.0 / 0/4 | — |
| Hertfordshire |  | 2 / 2.3 / 0/7 | 4 / 3.6 / 0/7 | 2 / 2.0 / 0/5 | 2 / 1.6 / 0/5 | 1 / 1.0 / 0/2 | 0 / 0.2 / 0/4 | 5 |
| Kent |  |  | 4 / 4.7 / 0/7 | 5 / 5.8 / 2/5 | 2 / 2.8 / 0/5 | 6 / 6.0 / 2/2 | 2 / 2.2 / 0/4 | 4 |
| Lancashire - Blackpool & Fylde | 1 / 0.7 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/5 | 1 / 0.4 / 0/5 | 1 / 0.5 / 0/2 | 0 / 0.0 / 0/4 | — |
| Lancashire - Central | 2 / 3.1 / 0/7 | 0 / 0.3 / 0/7 | 0 / 0.3 / 0/7 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 | 0 / 0.5 / 0/4 | 1 |
| Lancashire - East | 1 / 2.9 / 0/7 | 2 / 0.9 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.4 / 0/5 | 2 / 1.0 / 0/5 | 1 / 0.5 / 0/2 | 0 / 0.0 / 0/4 | — |
| Lancashire - North | 1 / 1.0 / 0/7 | 2 / 1.6 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| Lancashire - West | 2 / 1.8 / 0/6 | 0 / 0.2 / 0/6 | 2 / 1.7 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| Leicestershire |  | 0 / 0.1 / 0/7 | 1 / 1.9 / 0/7 | 1 / 1.4 / 0/5 | 1 / 0.6 / 0/5 | 5 / 6.5 / 1/2 | 1 / 1.0 / 0/4 | 5 |
| Lincolnshire |  | 3 / 2.1 / 0/7 | 1 / 1.0 / 0/7 | 1 / 1.2 / 0/5 | 3 / 2.6 / 0/5 | 5 / 5.0 / 0/2 | 2 / 1.5 / 0/4 | 2 |
| London |  |  |  |  |  | 6 / 5.0 / 1/2 |  |  |
| Merseyside - Liverpool |  | 0 / 0.6 / 0/7 | 0 / 0.4 / 0/7 | 1 / 0.8 / 0/5 | 2 / 1.6 / 0/5 | 0 / 1.0 / 0/2 | 0 / 0.2 / 0/4 | 0 |
| Merseyside - Sefton | 0 / 0.2 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| Merseyside - St Helens & Knowsley | 0 / 3.2 / 0/6 | 0 / 0.0 / 0/6 | 1 / 1.2 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 3 / 3.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| Merseyside - Wirral | 1 / 1.9 / 0/7 | 1 / 0.4 / 0/7 | 1 / 1.0 / 0/7 | 0 / 0.4 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.0 / 0/4 | 2 |
| Norfolk |  | 3 / 1.6 / 0/7 | 0 / 1.1 / 0/7 |  | 1 / 1.4 / 0/5 | 7 / 7.0 / 2/2 | 0 / 0.2 / 0/4 | 3 |
| North East |  |  |  | 2 / 1.4 / 0/5 | 5 / 4.2 / 0/5 |  | 1 / 1.2 / 0/4 | 75 |
| North Scotland | 4 / 6.0 / 2/6 | 0 / 0.0 / 0/6 | 4 / 3.2 / 0/6 | 0 / 0.4 / 0/5 | 0 / 0.0 / 0/5 | 2 / 1.5 / 0/2 | 0 / 0.0 / 0/4 | — |
| North Wales - East | 5 / 4.7 / 1/6 | 0 / 0.3 / 0/6 | 1 / 1.7 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 2 / 2.0 / 0/2 | 0 / 0.0 / 0/4 | 2 |
| North Wales - West | 2 / 1.7 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.2 / 0/4 | 0 |
| Northamptonshire |  | 0 / 0.0 / 0/7 | 3 / 2.7 / 0/7 | 1 / 1.4 / 0/5 | 3 / 2.0 / 0/5 | 7 / 7.0 / 2/2 | 2 / 3.0 / 1/4 | 4 |
| Northern Ireland - East |  | 2 / 2.0 / 0/6 | 0 / 0.0 / 0/6 | 1 / 1.0 / 0/5 | 0 / 0.0 / 0/5 |  | 0 / 0.2 / 0/4 | — |
| Northern Ireland - West | 4 / 4.0 / 0/6 | 0 / 0.0 / 0/6 | 1 / 1.0 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 | 0 / 0.0 / 0/4 | 1 |
| Nottinghamshire |  | 0 / 0.4 / 0/7 | 1 / 2.3 / 0/7 | 3 / 2.4 / 0/5 | 1 / 1.6 / 0/5 | 6 / 6.0 / 2/2 |  | 3 |
| Oxfordshire |  |  | 5 / 3.6 / 0/7 | 2 / 1.8 / 0/5 | 4 / 3.6 / 0/5 | 4 / 4.0 / 0/2 | 0 / 0.2 / 0/4 | 1 |
| Rutland | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| Scotland - Borders | 1 / 1.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| Scotland Central - Edinburgh & Lothians |  | 0 / 0.2 / 0/6 | 3 / 2.5 / 0/6 | 2 / 3.0 / 0/5 | 0 / 0.0 / 0/5 | 3 / 3.5 / 0/2 | 0 / 0.5 / 0/4 | 2 |
| Scotland Central - Falkirk & Stirling | 4 / 3.5 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 2 / 2.0 / 0/2 | 0 / 0.0 / 0/4 | 0 |
| Scotland Central - Fife | 1 / 1.7 / 0/6 | 0 / 0.0 / 0/6 | 1 / 1.0 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| Scotland Central - Tayside | 4 / 4.3 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.3 / 0/6 | 1 / 1.0 / 0/5 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| Scotland West - Ayrshire | 0 / 0.7 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 1 / 0.4 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.0 / 0/4 | 0 |
| Scotland West - Glasgow |  | 0 / 0.0 / 0/6 | 3 / 3.3 / 0/6 | 0 / 0.4 / 0/5 | 0 / 0.4 / 0/5 | 1 / 1.0 / 0/2 | 1 / 1.0 / 0/4 | 0 |
| Scotland West - Lanarkshire | 0 / 0.8 / 0/6 | 0 / 0.2 / 0/6 | 1 / 0.7 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.0 / 0/4 | 0 |
| Scotland West - Renfrewshire & Inverclyde | 1 / 1.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.5 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 2 / 2.0 / 0/2 | 0 / 0.0 / 0/4 | 0 |
| Shropshire |  | 3 / 2.7 / 0/7 | 1 / 1.7 / 0/7 | 2 / 1.6 / 0/5 | 0 / 0.2 / 0/5 |  | 2 / 1.8 / 0/4 | — |
| Somerset |  | 4 / 4.3 / 1/7 | 1 / 1.0 / 0/7 | 0 / 0.4 / 0/5 | 1 / 0.2 / 0/5 | 5 / 6.0 / 1/2 | 0 / 0.2 / 0/4 | 0 |
| Staffordshire |  | 0 / 0.3 / 0/7 | 2 / 1.4 / 0/7 | 0 / 0.0 / 0/5 | 0 / 1.0 / 0/5 | 4 / 4.0 / 0/2 | 0 / 0.2 / 0/4 |  |
| Suffolk |  | 1 / 1.3 / 0/7 | 2 / 1.7 / 0/7 |  | 0 / 0.0 / 0/5 | 3 / 3.0 / 0/2 | 1 / 1.0 / 0/4 | — |
| Surrey |  |  | 3 / 5.7 / 3/7 | 4 / 4.2 / 0/5 |  | 6 / 6.0 / 2/2 | 1 / 1.8 / 0/4 |  |
| Sussex |  |  | 3 / 3.4 / 0/7 | 1 / 2.2 / 0/5 | 3 / 2.0 / 0/5 | 5 / 5.0 / 0/2 | 6 / 6.0 / 4/4 | 4 |
| Wales - Mid | 0 / 0.2 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.0 / 0/4 | 1 |
| Wales - West | 1 / 1.7 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 | 0 / 0.2 / 0/4 | — |
| Wales South - Cardiff & Vale | 3 / 4.5 / 1/6 | 0 / 0.0 / 0/6 | 1 / 1.7 / 0/6 | 2 / 1.6 / 0/5 | 1 / 0.8 / 0/5 | 2 / 2.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| Wales South - Gwent | 4 / 3.5 / 0/6 | 0 / 0.2 / 0/6 | 0 / 0.2 / 0/6 | 2 / 1.6 / 0/5 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| Wales South - Swansea Bay | 3 / 3.3 / 1/6 | 0 / 0.2 / 0/6 | 3 / 2.7 / 0/6 | 1 / 1.0 / 0/5 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 | 0 / 0.0 / 0/4 | 10 |
| Wales South - Valleys | 1 / 1.8 / 1/6 | 0 / 0.0 / 0/6 | 0 / 0.5 / 0/6 | 4 / 2.6 / 0/5 | 2 / 1.2 / 0/5 | 1 / 1.0 / 0/2 | 0 / 0.0 / 0/4 | 19 |
| West Midlands - Birmingham & Solihull |  | 1 / 1.1 / 0/7 | 4 / 3.7 / 0/7 | 3 / 5.0 / 2/5 |  | 2 / 2.5 / 0/2 |  | 1 |
| West Midlands - Black Country |  | 1 / 1.3 / 0/7 | 1 / 1.0 / 0/7 | 1 / 1.0 / 0/5 | 0 / 0.2 / 0/5 | 1 / 1.0 / 0/2 | 0 / 0.0 / 0/4 | — |
| West Midlands - Coventry & Warwickshire |  | 0 / 0.0 / 0/7 | 1 / 0.6 / 0/7 | 0 / 0.8 / 0/5 | 3 / 2.4 / 0/5 | 4 / 4.0 / 0/2 | 3 / 3.2 / 0/4 | 1 |
| Wiltshire |  |  | 3 / 2.3 / 0/7 | 4 / 3.4 / 0/5 | 1 / 0.8 / 0/5 | 6 / 5.5 / 1/2 | 1 / 1.5 / 0/4 | 4 |
| Worcestershire |  | 0 / 1.9 / 0/7 | 3 / 3.0 / 0/7 | 0 / 0.4 / 0/5 | 3 / 1.8 / 0/5 | 3 / 3.0 / 0/2 | 0 / 0.5 / 0/4 | 1 |
| Yorkshire - East |  | 1 / 1.0 / 0/7 | 1 / 1.7 / 0/7 | 0 / 0.8 / 0/5 | 0 / 0.0 / 0/5 | 6 / 5.5 / 1/2 | 1 / 1.5 / 0/4 | 5 |
| Yorkshire - North |  | 5 / 4.6 / 0/7 | 0 / 0.6 / 0/7 | 0 / 0.2 / 0/5 | 1 / 0.6 / 0/5 |  | 1 / 1.0 / 0/4 | 2 |
| Yorkshire - South |  |  | 0 / 2.0 / 0/7 | 3 / 3.0 / 0/5 | 2 / 1.6 / 0/5 | 6 / 6.0 / 2/2 | 0 / 0.0 / 0/4 | 11 |
| Yorkshire - West |  |  |  | 4 / 4.0 / 0/5 | 6 / 4.2 / 2/5 |  |  | 5 |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Live regions | 46 / 78 | 11 / 78 | 4 / 78 | 4 / 78 | 5 / 78 | 8 / 78 | 6 / 78 | 4 / 78 |
| Live slice placements | 1258 | 69 + 1 CHECK | 31 | 12 + 2 CHECK | 57 | 75 | 21 | 6 + 3 CHECK |

**Live slices: 88 / 624.**
