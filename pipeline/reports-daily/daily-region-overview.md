# Ontap daily regional overview

Generated: 2026-09-03T10:06:12+01:00

[Download this overview as Excel](./daily-region-overview.xlsx)

## SITEWIDE RECONCILIATION

| Measure | Count |
|---|---:|
| Unique live jobs | 1,805 |
| Unique JobG8 jobs | 1,463 |
| Unique non-JobG8 jobs | 342 |
| Regional/category slice placements | 1,867 |
| Jobs appearing on multiple slices | 60 |
| Extra slice placements | 62 |
| Unique jobs outside governed slices | 0 |
| Jobs found in non-LIVE slices | 0 |

**Reconciliation: 1,805 unique jobs + 62 extra slice placements = 1,867 regional/category slice placements.**

Latest source-count CSV: `pipeline/reports-daily/live-job-source-count-2026-09-03.csv` — **STALE — CSV says 1,829 for 2026-09-03**.

### Provider breakdown

| Provider | Unique live jobs | Jobs on 2+ slices | Extra slice placements |
|---|---:|---:|---:|
| JobG8 | 1,463 | 60 | 62 |
| NEJobs | 16 | 0 | 0 |
| NHS Jobs | 224 | 0 | 0 |
| Teaching Vacancies | 101 | 0 | 0 |
| VONNE | 1 | 0 | 0 |

## JOBG8 FEED RECEIVED

**JobG8 jobs received: 10,000** (feed date: 2026-09-03)

| JobG8 classification | Jobs received | Ontap jobs |
|---|---:|---:|
| Sales & Marketing | 2,380 | 273 |
| I.T. & Communications | 1,675 | 38 |
| Administration | 1,329 | 701 |
| Healthcare & Medical | 878 | 51 |
| Call Centre / CustomerService | 834 | 243 |
| Accounting | 429 | 23 |
| Banking & Financial Services | 396 | 10 |
| Legal | 358 | 35 |
| HR / Recruitment | 340 | 30 |
| Retail & Consumer Products | 337 | 10 |
| Real Estate & Property | 229 | 11 |
| Consulting & Corporate Strategy | 209 | 7 |
| Insurance & Superannuation | 183 | 23 |
| Executive Positions | 161 |  |
| Advert / Media / Entertainment | 153 | 7 |
| Science & Technology | 109 | 1 |
| Total Ontap JobG8 jobs published today | 10,000 | 1,463 |

> LIVE counts come directly from the current published `app/` JSON, deduplicated within each canonical region/family slice while preserving legitimate appearances in more than one family. This is the live-site authority for the reconciliation above; the dated source-count CSV is shown only as a freshness cross-check. The overview covers all 78 assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 78-market coverage has run, NOT LIVE Admin/Support and Customer Service may fall back to the latest all-region Module 2 profile (2026-08-17), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-09-03) used by the production family run, across 78 UK markets with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across 78 UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across 78, 78, 78 and 78 UK markets respectively, using their governed production boundaries and canonical geo. NOT LIVE Customer Service / Contact Centre was assessed from that same feed across 78 UK markets using its governed exact-title, salary and geography rules. All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

## LIVE

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire | 8 |  |  |  |  |  |  |  |
| Berkshire | 30 |  | 8 |  | 12 |  | 1 |  |
| Bristol & Bath | 28 |  | 7 |  | 6 | CHECK |  |  |
| Buckinghamshire | 27 |  |  |  | 12 |  |  |  |
| Cambridgeshire | 22 |  |  |  |  |  |  |  |
| Cheshire - East | 11 |  |  |  |  |  |  |  |
| Cheshire - Warrington & Halton | 2 |  |  |  |  |  |  |  |
| Cheshire - West | 8 |  |  |  |  |  |  |  |
| Cornwall | 3 |  |  |  |  |  |  |  |
| Cumbria - North |  |  |  |  |  |  |  |  |
| Cumbria - South |  | 2 |  |  |  |  |  |  |
| Cumbria - West |  |  |  |  |  |  |  |  |
| Derbyshire | 10 |  |  |  |  |  |  |  |
| Devon | 25 |  |  |  |  | CHECK |  |  |
| Dorset | 20 |  |  |  |  |  |  |  |
| Essex | 45 |  |  | 6 |  |  |  |  |
| Gloucestershire | 28 |  |  |  | 7 | CHECK |  |  |
| Greater Manchester - Manchester & Salford | 38 |  | 22 |  | 16 |  | 1 |  |
| Greater Manchester - North |  |  |  |  |  |  |  |  |
| Greater Manchester - South | 10 |  |  |  |  |  |  |  |
| Greater Manchester - Wigan & Bolton | 7 |  |  |  |  |  |  |  |
| Hampshire | 73 | 7 |  |  |  |  |  | 10 |
| Herefordshire |  |  |  |  |  |  |  |  |
| Hertfordshire | 38 |  | 9 |  | 11 |  |  |  |
| Kent | 67 | 2 | 10 |  | 7 |  |  |  |
| Lancashire - Blackpool & Fylde |  |  |  |  |  |  |  |  |
| Lancashire - Central |  |  |  |  |  |  |  |  |
| Lancashire - East |  |  |  |  |  |  |  |  |
| Lancashire - North |  |  |  |  |  |  |  |  |
| Lancashire - West |  |  |  |  |  |  |  |  |
| Leicestershire | 31 |  |  |  |  |  |  |  |
| Lincolnshire | 13 |  |  |  |  |  |  |  |
| London | 186 | 14 | 44 | 19 | 68 |  | 14 | 5 |
| Merseyside - Liverpool | 12 |  |  |  |  |  |  |  |
| Merseyside - Sefton |  |  |  |  |  |  |  |  |
| Merseyside - St Helens & Knowsley |  |  |  |  |  |  |  |  |
| Merseyside - Wirral |  |  |  |  |  |  |  |  |
| Norfolk | 28 |  |  | CHECK |  |  |  |  |
| North East | 145 | 1 | 12 |  |  | CHECK |  |  |
| North Scotland |  |  |  |  |  |  |  |  |
| North Wales - East |  |  |  |  |  |  |  |  |
| North Wales - West |  |  |  |  |  |  |  |  |
| Northamptonshire | 23 |  |  |  |  |  |  |  |
| Northern Ireland - East | 29 |  |  |  |  | CHECK |  |  |
| Northern Ireland - West |  |  |  |  |  |  |  |  |
| Nottinghamshire | 22 |  |  |  |  |  | 3 |  |
| Oxfordshire | 39 | 2 |  |  | 7 |  |  |  |
| Rutland |  |  |  |  |  |  |  |  |
| Scotland - Borders |  |  |  |  |  |  |  |  |
| Scotland Central - Edinburgh & Lothians | 11 |  |  |  |  |  |  |  |
| Scotland Central - Falkirk & Stirling |  |  |  |  |  |  |  |  |
| Scotland Central - Fife |  |  |  |  |  |  |  |  |
| Scotland Central - Tayside |  |  |  |  |  |  |  |  |
| Scotland West - Ayrshire |  |  |  |  |  |  |  |  |
| Scotland West - Glasgow | 20 |  | 7 |  |  |  |  |  |
| Scotland West - Lanarkshire |  |  |  |  |  |  |  |  |
| Scotland West - Renfrewshire & Inverclyde |  |  |  |  |  |  |  |  |
| Shropshire | 11 |  |  |  |  | CHECK |  |  |
| Somerset | 20 |  |  |  |  |  |  |  |
| Staffordshire | 22 |  |  |  |  |  |  | 4 |
| Suffolk | 20 |  |  | 1 |  |  |  |  |
| Surrey | 60 | 3 | 5 |  | 10 |  |  | 11 |
| Sussex | 37 | 4 | 7 |  |  |  |  |  |
| Wales - Mid |  |  |  |  |  |  |  |  |
| Wales - West |  |  |  |  |  |  |  |  |
| Wales South - Cardiff & Vale | 10 |  |  |  |  |  |  |  |
| Wales South - Gwent |  |  |  |  |  |  |  |  |
| Wales South - Swansea Bay |  |  |  |  |  |  |  |  |
| Wales South - Valleys |  |  |  |  |  |  |  |  |
| West Midlands - Birmingham & Solihull | 35 |  |  |  | 2 |  | 1 |  |
| West Midlands - Black Country | 7 |  |  |  |  |  |  |  |
| West Midlands - Coventry & Warwickshire | 27 |  |  |  |  |  |  |  |
| Wiltshire | 11 | 3 |  |  |  |  |  |  |
| Worcestershire | 15 |  |  |  |  |  |  |  |
| Yorkshire - East | 20 |  |  |  |  |  |  |  |
| Yorkshire - North | 21 |  |  |  |  | CHECK |  |  |
| Yorkshire - South | 26 | CHECK |  |  |  |  |  |  |
| Yorkshire - West | 53 | 2 | 5 |  |  | CHECK | 3 |  |

## NOT LIVE

> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire |  | 0 / 0.2 / 0/13 | 1 / 2.1 / 0/13 | 4 / 3.8 / 0/11 | 1 / 1.1 / 0/11 | 1 / 0.8 / 0/8 | 1 / 1.0 / 0/10 | 1 / 1.0 / 0/7 |
| Berkshire |  | 0 / 3.0 / 3/13 |  | 2 / 0.9 / 0/11 |  | 1 / 0.6 / 0/8 |  | 1 / 0.4 / 0/7 |
| Bristol & Bath |  | 0 / 0.8 / 0/13 |  | 3 / 3.0 / 1/11 |  |  | 2 / 1.8 / 0/10 | 5 / 2.9 / 0/7 |
| Buckinghamshire |  | 0 / 0.6 / 0/13 | 1 / 0.7 / 0/13 | 1 / 1.0 / 0/11 |  | 2 / 2.1 / 0/8 | 1 / 0.8 / 0/10 | 6 / 3.4 / 3/7 |
| Cambridgeshire |  | 1 / 0.2 / 0/13 | 3 / 2.6 / 0/13 | 1 / 1.2 / 0/11 | 6 / 3.2 / 3/11 | 3 / 4.1 / 2/8 | 0 / 0.1 / 0/10 | 1 / 1.0 / 0/7 |
| Cheshire - East |  | 0 / 0.5 / 0/13 | 3 / 1.8 / 0/13 | 0 / 0.2 / 0/11 | 1 / 1.1 / 0/11 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/10 | 3 / 2.1 / 0/7 |
| Cheshire - Warrington & Halton |  | 1 / 1.3 / 0/13 | 1 / 1.9 / 1/13 | 2 / 1.5 / 0/11 | 1 / 0.5 / 0/11 | 7 / 5.2 / 4/8 | 0 / 0.1 / 0/10 | 0 / 0.0 / 0/7 |
| Cheshire - West |  | 0 / 1.2 / 0/13 | 1 / 1.8 / 0/13 | 2 / 1.2 / 0/11 | 6 / 2.9 / 3/11 | 1 / 1.9 / 0/8 | 1 / 0.4 / 0/10 | 1 / 0.4 / 0/7 |
| Cornwall |  | 0 / 1.2 / 0/13 | 1 / 0.8 / 0/13 | 0 / 0.0 / 0/11 | 0 / 0.2 / 0/11 | 0 / 0.2 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.9 / 0/7 |
| Cumbria - North | 1 / 1.5 / 0/13 | 0 / 2.4 / 3/13 | 0 / 0.0 / 0/13 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.1 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Cumbria - South | 1 / 1.1 / 0/13 |  | 1 / 0.8 / 0/13 | 0 / 0.0 / 0/11 | 2 / 0.8 / 0/11 | 0 / 0.5 / 0/8 | 1 / 0.3 / 0/10 | 0 / 0.0 / 0/7 |
| Cumbria - West | 0 / 1.5 / 0/13 | 0 / 0.6 / 0/13 | 0 / 0.0 / 0/13 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.4 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Derbyshire |  | 0 / 0.3 / 0/13 | 3 / 2.5 / 0/13 | 2 / 0.8 / 0/11 | 3 / 1.2 / 0/11 | 2 / 2.9 / 0/8 | 0 / 0.0 / 0/10 | 3 / 1.9 / 0/7 |
| Devon |  | 3 / 0.6 / 0/13 | 5 / 3.5 / 0/13 | 2 / 2.1 / 0/11 | 5 / 2.0 / 2/11 |  | 1 / 1.1 / 0/10 | 2 / 1.3 / 0/7 |
| Dorset |  | 1 / 1.0 / 0/13 | 3 / 3.8 / 2/13 | 0 / 0.2 / 0/11 | 3 / 1.6 / 0/11 | 1 / 2.6 / 0/8 | 0 / 0.0 / 0/10 | 3 / 0.7 / 0/7 |
| Essex |  | 0 / 0.6 / 0/13 | 6 / 2.6 / 1/13 |  | 7 / 3.5 / 3/11 | 5 / 5.6 / 2/8 | 1 / 1.1 / 0/10 | 4 / 2.6 / 0/7 |
| Gloucestershire |  | 1 / 0.4 / 0/13 | 4 / 1.8 / 0/13 | 0 / 0.0 / 0/11 |  |  | 1 / 1.2 / 0/10 | 2 / 1.9 / 0/7 |
| Greater Manchester - Manchester & Salford |  | 3 / 1.3 / 0/13 |  | 4 / 3.9 / 2/11 |  | 4 / 3.8 / 0/8 |  | 3 / 2.4 / 0/7 |
| Greater Manchester - North | 3 / 3.1 / 1/13 | 0 / 0.0 / 0/13 | 0 / 0.2 / 0/13 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/8 | 0 / 0.1 / 0/10 | 1 / 0.4 / 0/7 |
| Greater Manchester - South |  | 0 / 0.7 / 0/13 | 0 / 0.6 / 0/13 | 1 / 0.5 / 0/11 | 2 / 0.5 / 0/11 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/10 | 3 / 1.3 / 0/7 |
| Greater Manchester - Wigan & Bolton |  | 0 / 0.0 / 0/13 | 1 / 0.8 / 0/13 | 1 / 0.5 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.2 / 0/8 | 1 / 1.0 / 0/10 | 1 / 1.0 / 0/7 |
| Hampshire |  |  | 13 / 8.3 / 9/13 | 0 / 1.4 / 0/11 | 10 / 5.9 / 4/11 | 1 / 2.4 / 0/8 | 4 / 3.6 / 0/10 |  |
| Herefordshire | 0 / 1.2 / 0/13 | 1 / 0.4 / 0/13 | 0 / 0.0 / 0/13 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.9 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Hertfordshire |  | 3 / 2.4 / 0/13 |  | 1 / 1.5 / 0/11 |  | 1 / 1.0 / 0/8 | 1 / 0.4 / 0/10 | 3 / 2.0 / 0/7 |
| Kent |  |  |  | 5 / 4.3 / 2/11 |  | 0 / 2.2 / 1/8 | 2 / 1.7 / 0/10 | 3 / 1.4 / 0/7 |
| Lancashire - Blackpool & Fylde | 0 / 0.7 / 0/13 | 0 / 0.0 / 0/13 | 0 / 0.0 / 0/13 | 0 / 0.0 / 0/11 | 2 / 1.1 / 0/11 | 0 / 0.2 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Lancashire - Central | 3 / 2.8 / 0/13 | 0 / 0.2 / 0/13 | 1 / 0.4 / 0/13 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 1 / 0.6 / 0/8 | 0 / 0.2 / 0/10 | 0 / 0.0 / 0/7 |
| Lancashire - East | 4 / 2.7 / 0/13 | 1 / 0.8 / 0/13 | 0 / 0.2 / 0/13 | 0 / 0.2 / 0/11 | 3 / 1.5 / 0/11 | 1 / 1.1 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Lancashire - North | 2 / 1.2 / 0/13 | 0 / 1.0 / 0/13 | 1 / 0.2 / 0/13 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/8 | 1 / 0.3 / 0/10 | 0 / 0.0 / 0/7 |
| Lancashire - West | 0 / 1.1 / 0/12 | 0 / 0.1 / 0/12 | 1 / 1.2 / 0/12 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Leicestershire |  | 0 / 0.1 / 0/13 | 2 / 1.6 / 0/13 | 2 / 1.5 / 0/11 | 2 / 1.2 / 0/11 | 2 / 2.8 / 1/8 | 1 / 0.8 / 0/10 | 2 / 2.6 / 0/7 |
| Lincolnshire |  | 0 / 1.5 / 0/13 | 5 / 1.8 / 0/13 | 2 / 1.5 / 0/11 | 2 / 2.6 / 0/11 | 1 / 2.4 / 0/8 | 2 / 1.5 / 0/10 | 1 / 1.0 / 0/7 |
| London |  |  |  |  |  | 7 / 5.6 / 4/8 |  |  |
| Merseyside - Liverpool |  | 0 / 0.3 / 0/13 | 0 / 0.2 / 0/13 | 2 / 0.6 / 0/11 | 7 / 2.7 / 2/11 | 1 / 0.6 / 0/8 | 0 / 0.1 / 0/10 | 0 / 0.0 / 0/7 |
| Merseyside - Sefton | 0 / 0.1 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Merseyside - St Helens & Knowsley | 1 / 1.8 / 0/12 | 0 / 0.0 / 0/12 | 1 / 0.8 / 0/12 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 1 / 1.5 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Merseyside - Wirral | 1 / 1.5 / 0/13 | 0 / 0.4 / 0/13 | 1 / 1.0 / 0/13 | 1 / 0.5 / 0/11 | 2 / 0.7 / 0/11 | 1 / 0.4 / 0/8 | 0 / 0.0 / 0/10 | 1 / 1.0 / 0/7 |
| Norfolk |  | 0 / 0.9 / 0/13 | 1 / 0.7 / 0/13 |  | 1 / 1.5 / 0/11 | 2 / 3.6 / 2/8 | 0 / 0.2 / 0/10 | 1 / 0.9 / 0/7 |
| North East |  |  |  | 1 / 1.0 / 0/11 | 6 / 4.5 / 3/11 |  | 1 / 1.1 / 0/10 | 8 / 7.9 / 3/7 |
| North Scotland | 5 / 5.5 / 4/12 | 0 / 0.0 / 0/12 | 6 / 3.5 / 3/12 | 0 / 0.2 / 0/11 | 0 / 0.0 / 0/11 | 1 / 1.5 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| North Wales - East | 4 / 4.5 / 1/12 | 0 / 0.2 / 0/12 | 2 / 1.5 / 0/12 | 0 / 0.0 / 0/11 | 1 / 0.5 / 0/11 | 1 / 1.4 / 0/8 | 0 / 0.0 / 0/10 | 1 / 1.0 / 0/7 |
| North Wales - West | 3 / 2.0 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/8 | 1 / 0.4 / 0/10 | 1 / 0.6 / 0/7 |
| Northamptonshire |  | 0 / 0.0 / 0/13 | 10 / 4.5 / 3/13 | 1 / 1.3 / 0/11 | 4 / 2.5 / 0/11 | 1 / 2.9 / 2/8 | 3 / 2.6 / 1/10 | 1 / 0.4 / 0/7 |
| Northern Ireland - East |  | 1 / 1.6 / 0/12 | 0 / 0.0 / 0/12 | 2 / 1.3 / 0/11 | 1 / 0.1 / 0/11 |  | 3 / 0.4 / 0/10 | 2 / 1.0 / 0/7 |
| Northern Ireland - West | 20 / 5.2 / 1/12 | 0 / 0.0 / 0/12 | 3 / 1.3 / 0/12 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.1 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Nottinghamshire |  | 2 / 0.8 / 0/13 | 4 / 2.2 / 0/13 | 2 / 2.1 / 0/11 | 4 / 2.4 / 0/11 | 1 / 3.0 / 2/8 |  | 1 / 1.0 / 0/7 |
| Oxfordshire |  |  | 4 / 3.2 / 0/13 | 2 / 1.7 / 0/11 |  | 1 / 2.4 / 0/8 | 1 / 0.4 / 0/10 | 3 / 1.4 / 0/7 |
| Rutland | 0 / 0.0 / 0/13 | 0 / 0.0 / 0/13 | 0 / 0.0 / 0/13 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Scotland - Borders | 2 / 1.4 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.1 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.1 / 0/7 |
| Scotland Central - Edinburgh & Lothians |  | 0 / 0.1 / 0/12 | 3 / 2.4 / 0/12 | 3 / 2.5 / 0/11 | 1 / 0.3 / 0/11 | 1 / 1.1 / 0/8 | 1 / 0.5 / 0/10 | 1 / 0.4 / 0/7 |
| Scotland Central - Falkirk & Stirling | 1 / 2.4 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 1.0 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Scotland Central - Fife | 2 / 1.6 / 0/12 | 0 / 0.0 / 0/12 | 2 / 1.2 / 0/12 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.5 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Scotland Central - Tayside | 5 / 4.0 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.2 / 0/12 | 1 / 1.2 / 0/11 | 0 / 0.2 / 0/11 | 0 / 0.5 / 0/8 | 0 / 0.0 / 0/10 | 1 / 0.4 / 0/7 |
| Scotland West - Ayrshire | 1 / 0.6 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/12 | 1 / 0.5 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/10 | 1 / 0.7 / 0/7 |
| Scotland West - Glasgow |  | 0 / 0.0 / 0/12 |  | 1 / 0.4 / 0/11 | 1 / 0.3 / 0/11 | 0 / 0.2 / 0/8 | 0 / 0.5 / 0/10 | 4 / 3.4 / 1/7 |
| Scotland West - Lanarkshire | 0 / 0.4 / 0/12 | 0 / 0.1 / 0/12 | 0 / 0.3 / 0/12 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 1 / 0.1 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Scotland West - Renfrewshire & Inverclyde | 1 / 1.0 / 0/12 | 0 / 0.0 / 0/12 | 1 / 0.5 / 0/12 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.5 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Shropshire |  | 1 / 1.6 / 0/13 | 1 / 1.1 / 0/13 | 3 / 1.9 / 0/11 | 1 / 0.4 / 0/11 |  | 2 / 1.9 / 0/10 | 0 / 0.0 / 0/7 |
| Somerset |  | 2 / 3.4 / 3/13 | 4 / 1.7 / 0/13 | 1 / 0.5 / 0/11 | 4 / 1.2 / 0/11 | 1 / 2.6 / 1/8 | 1 / 0.2 / 0/10 | 2 / 0.9 / 0/7 |
| Staffordshire |  | 0 / 0.2 / 0/13 | 2 / 1.5 / 0/13 | 0 / 0.0 / 0/11 | 1 / 1.3 / 0/11 | 3 / 2.6 / 0/8 | 0 / 0.1 / 0/10 |  |
| Suffolk |  | 0 / 0.8 / 0/13 | 3 / 1.8 / 0/13 |  | 1 / 0.5 / 0/11 | 1 / 1.6 / 0/8 | 1 / 1.0 / 0/10 | 1 / 0.6 / 0/7 |
| Surrey |  |  |  | 6 / 4.2 / 1/11 |  | 3 / 4.6 / 2/8 | 3 / 2.2 / 0/10 |  |
| Sussex |  |  |  | 4 / 2.4 / 0/11 | 5 / 2.9 / 0/11 | 3 / 3.9 / 0/8 | 5 / 5.6 / 6/10 | 5 / 3.3 / 0/7 |
| Wales - Mid | 0 / 0.1 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Wales - West | 4 / 2.2 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.5 / 0/8 | 1 / 0.3 / 0/10 | 0 / 0.0 / 0/7 |
| Wales South - Cardiff & Vale |  | 0 / 0.0 / 0/12 | 3 / 1.9 / 0/12 | 2 / 1.5 / 0/11 | 1 / 1.0 / 0/11 | 0 / 0.9 / 0/8 | 0 / 0.0 / 0/10 | 1 / 0.4 / 0/7 |
| Wales South - Gwent | 1 / 2.4 / 0/12 | 0 / 0.1 / 0/12 | 0 / 0.2 / 0/12 | 2 / 1.5 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.5 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Wales South - Swansea Bay | 4 / 3.3 / 1/12 | 0 / 0.1 / 0/12 | 1 / 1.7 / 0/12 | 0 / 0.6 / 0/11 | 0 / 0.1 / 0/11 | 0 / 0.2 / 0/8 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 |
| Wales South - Valleys | 7 / 3.4 / 4/12 | 0 / 0.0 / 0/12 | 2 / 0.7 / 0/12 | 4 / 2.8 / 0/11 | 0 / 0.4 / 0/11 | 0 / 0.1 / 0/8 | 0 / 0.0 / 0/10 | 2 / 1.1 / 0/7 |
| West Midlands - Birmingham & Solihull |  | 1 / 1.0 / 0/13 | 10 / 4.9 / 3/13 | 4 / 4.0 / 2/11 |  | 3 / 2.8 / 0/8 |  | 5 / 3.9 / 0/7 |
| West Midlands - Black Country |  | 1 / 1.1 / 0/13 | 1 / 1.0 / 0/13 | 3 / 1.5 / 0/11 | 1 / 0.5 / 0/11 | 1 / 1.2 / 0/8 | 0 / 0.0 / 0/10 | 1 / 1.0 / 0/7 |
| West Midlands - Coventry & Warwickshire |  | 0 / 0.0 / 0/13 | 6 / 2.0 / 3/13 | 1 / 0.6 / 0/11 | 3 / 2.6 / 0/11 | 2 / 2.2 / 0/8 | 3 / 3.1 / 0/10 | 1 / 0.6 / 0/7 |
| Wiltshire |  |  | 3 / 2.2 / 0/13 | 4 / 3.2 / 0/11 | 1 / 1.1 / 0/11 | 0 / 2.1 / 0/8 | 0 / 0.5 / 0/10 | 2 / 1.3 / 0/7 |
| Worcestershire |  | 0 / 1.1 / 0/13 | 1 / 1.9 / 0/13 | 2 / 0.7 / 0/11 | 3 / 1.6 / 0/11 | 0 / 0.6 / 0/8 | 0 / 0.2 / 0/10 | 2 / 0.7 / 0/7 |
| Yorkshire - East |  | 0 / 0.6 / 0/13 | 0 / 1.0 / 0/13 | 2 / 1.2 / 0/11 | 2 / 0.7 / 0/11 | 2 / 3.5 / 0/8 | 1 / 1.2 / 0/10 | 5 / 3.4 / 0/7 |
| Yorkshire - North |  | 1 / 3.2 / 0/13 | 3 / 1.2 / 0/13 | 0 / 0.1 / 0/11 | 12 / 4.4 / 3/11 |  | 2 / 1.6 / 0/10 | 1 / 1.0 / 0/7 |
| Yorkshire - South |  |  | 4 / 2.3 / 0/13 | 3 / 3.1 / 0/11 | 5 / 2.5 / 1/11 | 0 / 1.8 / 2/8 | 0 / 0.0 / 0/10 | 2 / 1.4 / 0/7 |
| Yorkshire - West |  |  |  | 5 / 4.2 / 0/11 | 16 / 7.5 / 5/11 |  |  | 3 / 2.7 / 0/7 |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Live regions | 48 / 78 | 11 / 78 | 11 / 78 | 4 / 78 | 11 / 78 | 8 / 78 | 6 / 78 | 4 / 78 |
| Live slice placements | 1454 | 40 + 1 CHECK | 136 | 26 + 1 CHECK | 158 | 0 + 8 CHECK | 23 | 30 |

**Live slices: 103 / 624.**
