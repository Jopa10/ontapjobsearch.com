# Ontap daily regional overview

Generated: 2026-09-02T11:15:01+01:00

[Download this overview as Excel](./daily-region-overview.xlsx)

## SITEWIDE RECONCILIATION

| Measure | Count |
|---|---:|
| Unique live jobs | 1,752 |
| Unique JobG8 jobs | 1,390 |
| Unique non-JobG8 jobs | 362 |
| Regional/category slice placements | 1,801 |
| Jobs appearing on multiple slices | 49 |
| Extra slice placements | 49 |
| Unique jobs outside governed slices | 0 |
| Jobs found in non-LIVE slices | 0 |

**Reconciliation: 1,752 unique jobs + 49 extra slice placements = 1,801 regional/category slice placements.**

Latest source-count CSV: `pipeline/reports-daily/live-job-source-count-2026-09-02.csv` — **STALE — CSV says 1,772 for 2026-09-02**.

### Provider breakdown

| Provider | Unique live jobs | Jobs on 2+ slices | Extra slice placements |
|---|---:|---:|---:|
| JobG8 | 1,390 | 49 | 49 |
| NEJobs | 19 | 0 | 0 |
| NHS Jobs | 230 | 0 | 0 |
| Teaching Vacancies | 112 | 0 | 0 |
| VONNE | 1 | 0 | 0 |

## JOBG8 FEED RECEIVED

**JobG8 jobs received: 10,000** (feed date: 2026-09-02)

| JobG8 classification | Jobs received | Ontap jobs |
|---|---:|---:|
| Sales & Marketing | 2,489 | 225 |
| I.T. & Communications | 1,641 | 34 |
| Administration | 1,261 | 686 |
| Call Centre / CustomerService | 855 | 237 |
| Healthcare & Medical | 829 | 50 |
| Accounting | 414 | 24 |
| HR / Recruitment | 373 | 32 |
| Banking & Financial Services | 369 | 8 |
| Legal | 360 | 34 |
| Retail & Consumer Products | 327 | 10 |
| Real Estate & Property | 229 | 12 |
| Consulting & Corporate Strategy | 226 | 8 |
| Insurance & Superannuation | 175 | 21 |
| Advert / Media / Entertainment | 173 | 6 |
| Executive Positions | 165 | 2 |
| Science & Technology | 114 | 1 |
| Total Ontap JobG8 jobs published today | 10,000 | 1,390 |

> LIVE counts come directly from the current published `app/` JSON, deduplicated within each canonical region/family slice while preserving legitimate appearances in more than one family. This is the live-site authority for the reconciliation above; the dated source-count CSV is shown only as a freshness cross-check. The overview covers all 78 assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 78-market coverage has run, NOT LIVE Admin/Support and Customer Service may fall back to the latest all-region Module 2 profile (2026-08-17), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-09-02) used by the production family run, across 78 UK markets with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across 78 UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across 78, 78, 78 and 78 UK markets respectively, using their governed production boundaries and canonical geo. NOT LIVE Customer Service / Contact Centre was assessed from that same feed across 78 UK markets using its governed exact-title, salary and geography rules. All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

## LIVE

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire | 10 |  |  |  |  |  |  |  |
| Berkshire | 29 |  |  |  | 13 |  | 2 |  |
| Bristol & Bath | 25 |  | 8 |  |  | CHECK |  |  |
| Buckinghamshire | 28 |  |  |  | 12 |  |  |  |
| Cambridgeshire | 22 |  |  |  |  |  |  |  |
| Cheshire - East | 11 |  |  |  |  |  |  |  |
| Cheshire - Warrington & Halton | 2 |  |  |  |  |  |  |  |
| Cheshire - West | 10 |  |  |  |  |  |  |  |
| Cornwall | 28 |  |  |  |  |  |  |  |
| Cumbria - North |  |  |  |  |  |  |  |  |
| Cumbria - South |  | 2 |  |  |  |  |  |  |
| Cumbria - West |  |  |  |  |  |  |  |  |
| Derbyshire | 10 |  |  |  |  |  |  |  |
| Devon | 26 |  |  |  |  | CHECK |  |  |
| Dorset | 18 |  |  |  |  |  |  |  |
| Essex | 46 |  |  | 6 |  |  |  |  |
| Gloucestershire | 28 |  |  |  |  | CHECK |  |  |
| Greater Manchester - Manchester & Salford | 38 |  | 20 |  | 20 |  | 3 |  |
| Greater Manchester - North |  |  |  |  |  |  |  |  |
| Greater Manchester - South | 10 |  |  |  |  |  |  |  |
| Greater Manchester - Wigan & Bolton | 6 |  |  |  |  |  |  |  |
| Hampshire | 79 | 6 |  |  |  |  |  | 12 |
| Herefordshire |  |  |  |  |  |  |  |  |
| Hertfordshire | 41 |  |  |  |  |  |  |  |
| Kent | 62 | 2 |  |  |  |  |  |  |
| Lancashire - Blackpool & Fylde |  |  |  |  |  |  |  |  |
| Lancashire - Central |  |  |  |  |  |  |  |  |
| Lancashire - East |  |  |  |  |  |  |  |  |
| Lancashire - North |  |  |  |  |  |  |  |  |
| Lancashire - West |  |  |  |  |  |  |  |  |
| Leicestershire | 36 |  |  |  |  |  |  |  |
| Lincolnshire | 16 |  |  |  |  |  |  |  |
| London | 185 | 13 | 42 | 17 | 67 |  | 13 | 6 |
| Merseyside - Liverpool | 15 |  |  |  |  |  |  |  |
| Merseyside - Sefton |  |  |  |  |  |  |  |  |
| Merseyside - St Helens & Knowsley |  |  |  |  |  |  |  |  |
| Merseyside - Wirral |  |  |  |  |  |  |  |  |
| Norfolk | 30 |  |  | CHECK |  |  |  |  |
| North East | 134 | 2 | 13 |  |  | CHECK |  |  |
| North Scotland |  |  |  |  |  |  |  |  |
| North Wales - East |  |  |  |  |  |  |  |  |
| North Wales - West |  |  |  |  |  |  |  |  |
| Northamptonshire | 24 |  |  |  |  |  |  |  |
| Northern Ireland - East | 3 |  |  |  |  | CHECK |  |  |
| Northern Ireland - West |  |  |  |  |  |  |  |  |
| Nottinghamshire | 27 |  |  |  |  |  | 3 |  |
| Oxfordshire | 41 | 2 |  |  |  |  |  |  |
| Rutland |  |  |  |  |  |  |  |  |
| Scotland - Borders |  |  |  |  |  |  |  |  |
| Scotland Central - Edinburgh & Lothians | 11 |  |  |  |  |  |  |  |
| Scotland Central - Falkirk & Stirling |  |  |  |  |  |  |  |  |
| Scotland Central - Fife |  |  |  |  |  |  |  |  |
| Scotland Central - Tayside |  |  |  |  |  |  |  |  |
| Scotland West - Ayrshire |  |  |  |  |  |  |  |  |
| Scotland West - Glasgow | 22 |  |  |  |  |  |  |  |
| Scotland West - Lanarkshire |  |  |  |  |  |  |  |  |
| Scotland West - Renfrewshire & Inverclyde |  |  |  |  |  |  |  |  |
| Shropshire | 12 |  |  |  |  | CHECK |  |  |
| Somerset | 21 |  |  |  |  |  |  |  |
| Staffordshire | 22 |  |  |  |  |  |  | 4 |
| Suffolk | 15 |  |  | 1 |  |  |  |  |
| Surrey | 60 | 3 |  |  | 10 |  |  | 12 |
| Sussex | 38 | 4 |  |  |  |  |  |  |
| Wales - Mid |  |  |  |  |  |  |  |  |
| Wales - West |  |  |  |  |  |  |  |  |
| Wales South - Cardiff & Vale |  |  |  |  |  |  |  |  |
| Wales South - Gwent |  |  |  |  |  |  |  |  |
| Wales South - Swansea Bay |  |  |  |  |  |  |  |  |
| Wales South - Valleys |  |  |  |  |  |  |  |  |
| West Midlands - Birmingham & Solihull | 37 |  |  |  | 2 |  | 2 |  |
| West Midlands - Black Country | 7 |  |  |  |  |  |  |  |
| West Midlands - Coventry & Warwickshire | 28 |  |  |  |  |  |  |  |
| Wiltshire | 16 | 3 |  |  |  |  |  |  |
| Worcestershire | 13 |  |  |  |  |  |  |  |
| Yorkshire - East | 18 |  |  |  |  |  |  |  |
| Yorkshire - North | 20 |  |  |  |  | CHECK |  |  |
| Yorkshire - South | 35 | CHECK |  |  |  |  |  |  |
| Yorkshire - West | 51 | 1 | 6 |  |  | CHECK | 3 |  |

## NOT LIVE

> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire |  | 0 / 0.2 / 0/12 | 2 / 2.2 / 0/12 | 4 / 3.8 / 0/10 | 1 / 1.1 / 0/10 | 1 / 0.7 / 0/7 | 1 / 1.0 / 0/9 | 1 / 1.0 / 0/6 |
| Berkshire |  | 0 / 3.2 / 3/12 | 8 / 2.2 / 2/12 | 2 / 0.8 / 0/10 |  | 2 / 0.7 / 0/7 |  | 1 / 0.3 / 0/6 |
| Bristol & Bath |  | 0 / 0.9 / 0/12 |  | 3 / 2.9 / 1/10 | 8 / 3.2 / 2/10 |  | 2 / 1.8 / 0/9 | 4 / 2.3 / 0/6 |
| Buckinghamshire |  | 0 / 0.7 / 0/12 | 1 / 0.7 / 0/12 | 1 / 1.0 / 0/10 |  | 2 / 2.1 / 0/7 | 1 / 0.8 / 0/9 | 5 / 2.8 / 1/6 |
| Cambridgeshire |  | 0 / 0.1 / 0/12 | 3 / 2.6 / 0/12 | 1 / 1.2 / 0/10 | 6 / 2.9 / 2/10 | 3 / 4.3 / 2/7 | 0 / 0.1 / 0/9 | 1 / 1.0 / 0/6 |
| Cheshire - East |  | 0 / 0.6 / 0/12 | 3 / 1.7 / 0/12 | 0 / 0.2 / 0/10 | 2 / 1.1 / 0/10 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/9 | 3 / 2.0 / 0/6 |
| Cheshire - Warrington & Halton |  | 1 / 1.3 / 0/12 | 5 / 2.3 / 1/12 | 2 / 1.4 / 0/10 | 1 / 0.4 / 0/10 | 7 / 5.0 / 3/7 | 0 / 0.1 / 0/9 | 0 / 0.0 / 0/6 |
| Cheshire - West |  | 0 / 1.3 / 0/12 | 0 / 1.8 / 0/12 | 2 / 1.1 / 0/10 | 6 / 2.6 / 2/10 | 1 / 2.0 / 0/7 | 1 / 0.3 / 0/9 | 1 / 0.3 / 0/6 |
| Cornwall |  | 0 / 1.3 / 0/12 | 2 / 0.8 / 0/12 | 0 / 0.0 / 0/10 | 0 / 0.2 / 0/10 | 0 / 0.3 / 0/7 | 0 / 0.0 / 0/9 | 31 / 6.0 / 1/6 |
| Cumbria - North | 1 / 1.6 / 0/12 | 0 / 2.6 / 3/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.1 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Cumbria - South | 1 / 1.1 / 0/12 |  | 1 / 0.8 / 0/12 | 0 / 0.0 / 0/10 | 2 / 0.7 / 0/10 | 0 / 0.6 / 0/7 | 1 / 0.2 / 0/9 | 0 / 0.0 / 0/6 |
| Cumbria - West | 0 / 1.7 / 0/12 | 0 / 0.7 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.4 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Derbyshire |  | 0 / 0.3 / 0/12 | 3 / 2.5 / 0/12 | 2 / 0.7 / 0/10 | 3 / 1.1 / 0/10 | 2 / 3.0 / 0/7 | 0 / 0.0 / 0/9 | 3 / 1.7 / 0/6 |
| Devon |  | 3 / 0.4 / 0/12 | 5 / 3.3 / 0/12 | 3 / 2.2 / 0/10 | 6 / 1.7 / 2/10 |  | 1 / 1.1 / 0/9 | 2 / 1.2 / 0/6 |
| Dorset |  | 1 / 1.0 / 0/12 | 4 / 3.9 / 2/12 | 0 / 0.2 / 0/10 | 3 / 1.6 / 0/10 | 1 / 2.9 / 0/7 | 0 / 0.0 / 0/9 | 1 / 0.3 / 0/6 |
| Essex |  | 0 / 0.7 / 0/12 | 5 / 2.3 / 0/12 |  | 5 / 3.0 / 1/10 | 5 / 5.7 / 2/7 | 1 / 1.1 / 0/9 | 4 / 2.3 / 0/6 |
| Gloucestershire |  | 1 / 0.3 / 0/12 | 4 / 1.6 / 0/12 | 0 / 0.0 / 0/10 | 7 / 3.3 / 2/10 |  | 1 / 1.2 / 0/9 | 3 / 1.8 / 0/6 |
| Greater Manchester - Manchester & Salford |  | 1 / 1.2 / 0/12 |  | 4 / 3.9 / 2/10 |  | 4 / 3.7 / 0/7 |  | 3 / 2.3 / 0/6 |
| Greater Manchester - North | 3 / 3.1 / 1/12 | 0 / 0.0 / 0/12 | 0 / 0.2 / 0/12 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 | 0 / 0.1 / 0/9 | 1 / 0.3 / 0/6 |
| Greater Manchester - South |  | 0 / 0.8 / 0/12 | 1 / 0.8 / 0/12 | 1 / 0.5 / 0/10 | 2 / 0.4 / 0/10 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/9 | 3 / 1.0 / 0/6 |
| Greater Manchester - Wigan & Bolton |  | 0 / 0.0 / 0/12 | 1 / 0.8 / 0/12 | 1 / 0.4 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.3 / 0/7 | 1 / 1.0 / 0/9 | 1 / 1.0 / 0/6 |
| Hampshire |  |  | 14 / 7.9 / 8/12 | 0 / 1.5 / 0/10 | 10 / 5.5 / 3/10 | 1 / 2.6 / 0/7 | 4 / 3.6 / 0/9 |  |
| Herefordshire | 0 / 1.2 / 0/12 | 1 / 0.3 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 1.0 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Hertfordshire |  | 3 / 2.3 / 0/12 | 9 / 4.4 / 2/12 | 2 / 1.6 / 0/10 | 9 / 2.8 / 2/10 | 1 / 1.0 / 0/7 | 1 / 0.3 / 0/9 | 3 / 1.8 / 0/6 |
| Kent |  |  | 9 / 4.9 / 2/12 | 3 / 4.2 / 2/10 | 7 / 3.2 / 2/10 | 0 / 2.6 / 1/7 | 2 / 1.7 / 0/9 | 3 / 1.2 / 0/6 |
| Lancashire - Blackpool & Fylde | 0 / 0.8 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/10 | 2 / 1.0 / 0/10 | 0 / 0.3 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Lancashire - Central | 3 / 2.8 / 0/12 | 0 / 0.2 / 0/12 | 1 / 0.3 / 0/12 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 1 / 0.6 / 0/7 | 0 / 0.2 / 0/9 | 0 / 0.0 / 0/6 |
| Lancashire - East | 3 / 2.5 / 0/12 | 0 / 0.7 / 0/12 | 0 / 0.2 / 0/12 | 0 / 0.2 / 0/10 | 3 / 1.3 / 0/10 | 1 / 1.1 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Lancashire - North | 2 / 1.2 / 0/12 | 0 / 1.1 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 | 1 / 0.2 / 0/9 | 0 / 0.0 / 0/6 |
| Lancashire - West | 0 / 1.2 / 0/11 | 0 / 0.1 / 0/11 | 1 / 1.2 / 0/11 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Leicestershire |  | 0 / 0.1 / 0/12 | 2 / 1.6 / 0/12 | 2 / 1.4 / 0/10 | 2 / 1.1 / 0/10 | 2 / 2.9 / 1/7 | 1 / 0.8 / 0/9 | 2 / 2.7 / 0/6 |
| Lincolnshire |  | 0 / 1.6 / 0/12 | 5 / 1.5 / 0/12 | 2 / 1.5 / 0/10 | 3 / 2.7 / 0/10 | 1 / 2.6 / 0/7 | 2 / 1.4 / 0/9 | 1 / 1.0 / 0/6 |
| London |  |  |  |  |  | 7 / 5.4 / 3/7 |  |  |
| Merseyside - Liverpool |  | 0 / 0.3 / 0/12 | 0 / 0.2 / 0/12 | 1 / 0.5 / 0/10 | 6 / 2.3 / 1/10 | 1 / 0.6 / 0/7 | 0 / 0.1 / 0/9 | 0 / 0.0 / 0/6 |
| Merseyside - Sefton | 0 / 0.1 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Merseyside - St Helens & Knowsley | 1 / 1.9 / 0/11 | 0 / 0.0 / 0/11 | 1 / 0.8 / 0/11 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 1 / 1.6 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Merseyside - Wirral | 1 / 1.5 / 0/12 | 0 / 0.4 / 0/12 | 1 / 1.0 / 0/12 | 1 / 0.4 / 0/10 | 2 / 0.6 / 0/10 | 1 / 0.3 / 0/7 | 0 / 0.0 / 0/9 | 1 / 1.0 / 0/6 |
| Norfolk |  | 0 / 1.0 / 0/12 | 0 / 0.7 / 0/12 |  | 2 / 1.6 / 0/10 | 2 / 3.9 / 2/7 | 0 / 0.2 / 0/9 | 1 / 0.8 / 0/6 |
| North East |  |  |  | 1 / 1.0 / 0/10 | 6 / 4.3 / 2/10 |  | 1 / 1.1 / 0/9 | 78 / 19.3 / 2/6 |
| North Scotland | 5 / 5.5 / 4/11 | 0 / 0.0 / 0/11 | 6 / 3.3 / 2/11 | 0 / 0.2 / 0/10 | 0 / 0.0 / 0/10 | 1 / 1.6 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| North Wales - East | 5 / 4.5 / 1/11 | 0 / 0.2 / 0/11 | 2 / 1.5 / 0/11 | 0 / 0.0 / 0/10 | 1 / 0.5 / 0/10 | 1 / 1.4 / 0/7 | 0 / 0.0 / 0/9 | 1 / 1.0 / 0/6 |
| North Wales - West | 3 / 1.9 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 | 1 / 0.3 / 0/9 | 1 / 0.5 / 0/6 |
| Northamptonshire |  | 0 / 0.0 / 0/12 | 10 / 4.1 / 2/12 | 1 / 1.3 / 0/10 | 3 / 2.2 / 0/10 | 2 / 3.1 / 2/7 | 3 / 2.6 / 1/9 | 1 / 0.3 / 0/6 |
| Northern Ireland - East |  | 1 / 1.7 / 0/11 | 0 / 0.0 / 0/11 | 1 / 1.2 / 0/10 | 0 / 0.0 / 0/10 |  | 0 / 0.1 / 0/9 | 1 / 1.0 / 0/6 |
| Northern Ireland - West | 4 / 4.1 / 0/11 | 0 / 0.0 / 0/11 | 3 / 1.2 / 0/11 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.1 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Nottinghamshire |  | 0 / 0.4 / 0/12 | 4 / 2.0 / 0/12 | 2 / 2.1 / 0/10 | 4 / 2.2 / 0/10 | 1 / 3.3 / 2/7 |  | 1 / 1.0 / 0/6 |
| Oxfordshire |  |  | 4 / 3.1 / 0/12 | 2 / 1.7 / 0/10 | 9 / 5.0 / 3/10 | 1 / 2.6 / 0/7 | 1 / 0.3 / 0/9 | 3 / 1.2 / 0/6 |
| Rutland | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/12 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Scotland - Borders | 3 / 1.5 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 1 / 0.3 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.2 / 0/6 |
| Scotland Central - Edinburgh & Lothians |  | 0 / 0.1 / 0/11 | 3 / 2.3 / 0/11 | 3 / 2.5 / 0/10 | 1 / 0.2 / 0/10 | 1 / 1.1 / 0/7 | 1 / 0.4 / 0/9 | 1 / 0.3 / 0/6 |
| Scotland Central - Falkirk & Stirling | 1 / 2.5 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 1 / 1.1 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Scotland Central - Fife | 2 / 1.5 / 0/11 | 0 / 0.0 / 0/11 | 2 / 1.1 / 0/11 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.6 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Scotland Central - Tayside | 5 / 3.9 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.2 / 0/11 | 1 / 1.2 / 0/10 | 0 / 0.2 / 0/10 | 0 / 0.6 / 0/7 | 0 / 0.0 / 0/9 | 1 / 0.3 / 0/6 |
| Scotland West - Ayrshire | 1 / 0.5 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 1 / 0.5 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/9 | 1 / 0.7 / 0/6 |
| Scotland West - Glasgow |  | 0 / 0.0 / 0/11 | 7 / 3.6 / 2/11 | 0 / 0.2 / 0/10 | 0 / 0.2 / 0/10 | 0 / 0.3 / 0/7 | 0 / 0.6 / 0/9 | 10 / 4.2 / 2/6 |
| Scotland West - Lanarkshire | 0 / 0.5 / 0/11 | 0 / 0.1 / 0/11 | 0 / 0.4 / 0/11 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Scotland West - Renfrewshire & Inverclyde | 1 / 1.0 / 0/11 | 0 / 0.0 / 0/11 | 1 / 0.5 / 0/11 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.6 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Shropshire |  | 0 / 1.7 / 0/12 | 0 / 1.0 / 0/12 | 3 / 1.8 / 0/10 | 1 / 0.4 / 0/10 |  | 2 / 1.9 / 0/9 | 0 / 0.0 / 0/6 |
| Somerset |  | 2 / 3.5 / 3/12 | 3 / 1.4 / 0/12 | 1 / 0.4 / 0/10 | 4 / 0.9 / 0/10 | 1 / 2.9 / 1/7 | 0 / 0.1 / 0/9 | 2 / 0.7 / 0/6 |
| Staffordshire |  | 1 / 0.2 / 0/12 | 2 / 1.4 / 0/12 | 0 / 0.0 / 0/10 | 2 / 1.3 / 0/10 | 3 / 2.6 / 0/7 | 0 / 0.1 / 0/9 |  |
| Suffolk |  | 1 / 0.9 / 0/12 | 3 / 1.8 / 0/12 |  | 2 / 0.5 / 0/10 | 1 / 1.7 / 0/7 | 1 / 1.0 / 0/9 | 1 / 0.5 / 0/6 |
| Surrey |  |  | 6 / 4.6 / 5/12 | 5 / 4.1 / 0/10 |  | 4 / 4.9 / 2/7 | 3 / 2.1 / 0/9 |  |
| Sussex |  |  | 7 / 3.9 / 2/12 | 4 / 2.2 / 0/10 | 4 / 2.7 / 0/10 | 4 / 4.1 / 0/7 | 5 / 5.7 / 6/9 | 4 / 3.0 / 0/6 |
| Wales - Mid | 0 / 0.1 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Wales - West | 4 / 2.1 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.6 / 0/7 | 1 / 0.2 / 0/9 | 0 / 0.0 / 0/6 |
| Wales South - Cardiff & Vale | 9 / 4.8 / 3/11 | 0 / 0.0 / 0/11 | 3 / 1.8 / 0/11 | 2 / 1.4 / 0/10 | 2 / 1.0 / 0/10 | 0 / 1.0 / 0/7 | 0 / 0.0 / 0/9 | 2 / 0.5 / 0/6 |
| Wales South - Gwent | 1 / 2.5 / 0/11 | 0 / 0.1 / 0/11 | 1 / 0.4 / 0/11 | 2 / 1.4 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.6 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Wales South - Swansea Bay | 3 / 3.1 / 1/11 | 0 / 0.1 / 0/11 | 1 / 1.7 / 0/11 | 1 / 0.7 / 0/10 | 1 / 0.1 / 0/10 | 0 / 0.3 / 0/7 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 |
| Wales South - Valleys | 10 / 2.9 / 3/11 | 0 / 0.0 / 0/11 | 2 / 0.5 / 0/11 | 4 / 2.7 / 0/10 | 0 / 0.4 / 0/10 | 0 / 0.1 / 0/7 | 0 / 0.0 / 0/9 | 4 / 1.3 / 0/6 |
| West Midlands - Birmingham & Solihull |  | 1 / 1.0 / 0/12 | 11 / 4.6 / 2/12 | 4 / 3.9 / 2/10 |  | 3 / 2.7 / 0/7 |  | 5 / 3.7 / 0/6 |
| West Midlands - Black Country |  | 1 / 1.1 / 0/12 | 1 / 1.0 / 0/12 | 4 / 1.4 / 0/10 | 1 / 0.5 / 0/10 | 1 / 1.3 / 0/7 | 0 / 0.0 / 0/9 | 1 / 1.0 / 0/6 |
| West Midlands - Coventry & Warwickshire |  | 0 / 0.0 / 0/12 | 6 / 1.7 / 2/12 | 1 / 0.6 / 0/10 | 5 / 2.7 / 0/10 | 3 / 2.3 / 0/7 | 3 / 3.1 / 0/9 | 2 / 0.7 / 0/6 |
| Wiltshire |  |  | 3 / 2.1 / 0/12 | 4 / 3.1 / 0/10 | 2 / 1.2 / 0/10 | 0 / 2.3 / 0/7 | 0 / 0.6 / 0/9 | 2 / 1.2 / 0/6 |
| Worcestershire |  | 0 / 1.2 / 0/12 | 1 / 2.0 / 0/12 | 2 / 0.6 / 0/10 | 2 / 1.5 / 0/10 | 0 / 0.7 / 0/7 | 0 / 0.2 / 0/9 | 1 / 0.5 / 0/6 |
| Yorkshire - East |  | 0 / 0.7 / 0/12 | 0 / 1.1 / 0/12 | 2 / 1.1 / 0/10 | 2 / 0.6 / 0/10 | 2 / 3.7 / 0/7 | 1 / 1.2 / 0/9 | 4 / 3.0 / 0/6 |
| Yorkshire - North |  | 1 / 3.3 / 0/12 | 3 / 1.1 / 0/12 | 0 / 0.1 / 0/10 | 12 / 3.6 / 2/10 |  | 2 / 1.6 / 0/9 | 1 / 1.0 / 0/6 |
| Yorkshire - South |  |  | 4 / 2.2 / 0/12 | 4 / 3.2 / 0/10 | 5 / 2.3 / 1/10 | 0 / 2.0 / 2/7 | 0 / 0.0 / 0/9 | 3 / 1.7 / 0/6 |
| Yorkshire - West |  |  |  | 5 / 4.1 / 0/10 | 16 / 6.6 / 4/10 |  |  | 3 / 2.7 / 0/6 |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Live regions | 47 / 78 | 11 / 78 | 5 / 78 | 4 / 78 | 6 / 78 | 8 / 78 | 6 / 78 | 4 / 78 |
| Live slice placements | 1466 | 38 + 1 CHECK | 89 | 24 + 1 CHECK | 124 | 0 + 8 CHECK | 26 | 34 |

**Live slices: 91 / 624.**
