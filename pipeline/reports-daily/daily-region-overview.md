# Ontap daily regional overview

Generated: 2026-08-29T10:43:59+01:00

## SITEWIDE RECONCILIATION

| Measure | Count |
|---|---:|
| Unique live jobs | 1,376 |
| Unique JobG8 jobs | 956 |
| Unique non-JobG8 jobs | 420 |
| Regional/category slice placements | 1,418 |
| Jobs appearing on multiple slices | 42 |
| Extra slice placements | 42 |
| Unique jobs outside governed slices | 0 |
| Jobs found in non-LIVE slices | 0 |

**Reconciliation: 1,376 unique jobs + 42 extra slice placements = 1,418 regional/category slice placements.**

Latest source-count CSV: `pipeline/reports-daily/live-job-source-count-2026-08-29.csv` — **STALE — CSV says 1,409 for 2026-08-29**.

### Provider breakdown

| Provider | Unique live jobs | Jobs on 2+ slices | Extra slice placements |
|---|---:|---:|---:|
| JobG8 | 956 | 42 | 42 |
| NEJobs | 30 | 0 | 0 |
| NHS Jobs | 210 | 0 | 0 |
| Teaching Vacancies | 178 | 0 | 0 |
| VONNE | 2 | 0 | 0 |

> LIVE counts come directly from the current published `app/` JSON, deduplicated within each canonical region/family slice while preserving legitimate appearances in more than one family. This is the live-site authority for the reconciliation above; the dated source-count CSV is shown only as a freshness cross-check. The overview covers all 78 assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 78-market coverage has run, NOT LIVE Admin/Support and Customer Service may fall back to the latest all-region Module 2 profile (2026-08-17), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-08-29) used by the production family run, across 78 UK markets with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across 78 UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across 78, 78, 78 and 78 UK markets respectively, using their governed production boundaries and canonical geo. NOT LIVE Customer Service / Contact Centre was assessed from that same feed across 78 UK markets using its governed exact-title, salary and geography rules. All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

## LIVE

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire |  |  |  |  |  |  |  |  |
| Berkshire | 28 |  |  |  | 6 |  | 1 |  |
| Bristol & Bath | 20 |  |  |  |  | CHECK |  |  |
| Buckinghamshire | 21 |  |  |  |  |  |  |  |
| Cambridgeshire | 38 |  |  |  |  |  |  |  |
| Cheshire - East | 12 |  |  |  |  |  |  |  |
| Cheshire - Warrington & Halton | 1 |  |  |  |  |  |  |  |
| Cheshire - West | 3 |  |  |  |  |  |  |  |
| Cornwall | 5 |  |  |  |  |  |  |  |
| Cumbria - North |  |  |  |  |  |  |  |  |
| Cumbria - South |  | CHECK |  |  |  |  |  |  |
| Cumbria - West |  |  |  |  |  |  |  |  |
| Derbyshire | 8 |  |  |  |  |  |  |  |
| Devon | 36 |  |  |  |  | 10 |  |  |
| Dorset | 16 |  |  |  |  |  |  |  |
| Essex | 41 |  |  | 2 |  |  |  |  |
| Gloucestershire | 22 |  |  |  |  | 7 |  |  |
| Greater Manchester - Manchester & Salford | 27 |  | 7 |  | 11 |  | 3 |  |
| Greater Manchester - North |  |  |  |  |  |  |  |  |
| Greater Manchester - South | 7 |  |  |  |  |  |  |  |
| Greater Manchester - Wigan & Bolton | 5 |  |  |  |  |  |  |  |
| Hampshire | 56 | 9 |  |  |  |  |  | 4 |
| Herefordshire |  |  |  |  |  |  |  |  |
| Hertfordshire | 30 |  |  |  |  |  |  |  |
| Kent | 46 | 7 |  |  |  |  |  |  |
| Lancashire - Blackpool & Fylde |  |  |  |  |  |  |  |  |
| Lancashire - Central |  |  |  |  |  |  |  |  |
| Lancashire - East |  |  |  |  |  |  |  |  |
| Lancashire - North |  |  |  |  |  |  |  |  |
| Lancashire - West |  |  |  |  |  |  |  |  |
| Leicestershire | 34 |  |  |  |  |  |  |  |
| Lincolnshire | 17 |  |  |  |  |  |  |  |
| London | 125 | 16 | 18 | 8 | 27 |  | 7 | 3 |
| Merseyside - Liverpool | 10 |  |  |  |  |  |  |  |
| Merseyside - Sefton |  |  |  |  |  |  |  |  |
| Merseyside - St Helens & Knowsley |  |  |  |  |  |  |  |  |
| Merseyside - Wirral |  |  |  |  |  |  |  |  |
| Norfolk | 30 |  |  | CHECK |  |  |  |  |
| North East | 63 | 4 | 5 |  |  | CHECK |  |  |
| North Scotland |  |  |  |  |  |  |  |  |
| North Wales - East |  |  |  |  |  |  |  |  |
| North Wales - West |  |  |  |  |  |  |  |  |
| Northamptonshire | 23 |  |  |  |  |  |  |  |
| Northern Ireland - East | 6 |  |  |  |  | 9 |  |  |
| Northern Ireland - West |  |  |  |  |  |  |  |  |
| Nottinghamshire | 23 |  |  |  |  |  | 2 |  |
| Oxfordshire | 43 | 10 |  |  |  |  |  |  |
| Rutland |  |  |  |  |  |  |  |  |
| Scotland - Borders |  |  |  |  |  |  |  |  |
| Scotland Central - Edinburgh & Lothians | 5 |  |  |  |  |  |  |  |
| Scotland Central - Falkirk & Stirling |  |  |  |  |  |  |  |  |
| Scotland Central - Fife |  |  |  |  |  |  |  |  |
| Scotland Central - Tayside |  |  |  |  |  |  |  |  |
| Scotland West - Ayrshire |  |  |  |  |  |  |  |  |
| Scotland West - Glasgow | 12 |  |  |  |  |  |  |  |
| Scotland West - Lanarkshire |  |  |  |  |  |  |  |  |
| Scotland West - Renfrewshire & Inverclyde |  |  |  |  |  |  |  |  |
| Shropshire | 13 |  |  |  |  | 6 |  |  |
| Somerset | 20 |  |  |  |  |  |  |  |
| Staffordshire | 22 |  |  |  |  |  |  | 3 |
| Suffolk | 12 |  |  | CHECK |  |  |  |  |
| Surrey | 52 | 4 |  |  | 5 |  |  | 6 |
| Sussex | 31 | 7 |  |  |  |  |  |  |
| Wales - Mid |  |  |  |  |  |  |  |  |
| Wales - West |  |  |  |  |  |  |  |  |
| Wales South - Cardiff & Vale |  |  |  |  |  |  |  |  |
| Wales South - Gwent |  |  |  |  |  |  |  |  |
| Wales South - Swansea Bay |  |  |  |  |  |  |  |  |
| Wales South - Valleys |  |  |  |  |  |  |  |  |
| West Midlands - Birmingham & Solihull | 27 |  |  |  | 3 |  | 4 |  |
| West Midlands - Black Country | 12 |  |  |  |  |  |  |  |
| West Midlands - Coventry & Warwickshire | 30 |  |  |  |  |  |  |  |
| Wiltshire | 22 | 8 |  |  |  |  |  |  |
| Worcestershire | 10 |  |  |  |  |  |  |  |
| Yorkshire - East | 15 |  |  |  |  |  |  |  |
| Yorkshire - North | 25 |  |  |  |  | 10 |  |  |
| Yorkshire - South | 30 | 2 |  |  |  |  |  |  |
| Yorkshire - West | 42 | 2 | 3 |  |  | CHECK | 3 |  |

## NOT LIVE

> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire | 7 / 5.1 / 3/8 | 0 / 0.2 / 0/8 | 2 / 2.2 / 0/8 | 3 / 4.2 / 0/6 | 2 / 1.3 / 0/6 | 1 / 0.7 / 0/3 | 1 / 1.2 / 0/5 | 1 / 1.0 / 0/2 |
| Berkshire |  | 6 / 3.8 / 2/8 | 1 / 0.9 / 0/8 | 0 / 0.7 / 0/6 |  | 0 / 0.3 / 0/3 |  | 0 / 0.0 / 0/2 |
| Bristol & Bath |  | 1 / 1.2 / 0/8 | 8 / 7.0 / 7/8 | 1 / 3.7 / 1/6 | 5 / 2.2 / 0/6 |  | 2 / 2.0 / 0/5 | 1 / 1.0 / 0/2 |
| Buckinghamshire |  | 0 / 1.0 / 0/8 | 1 / 0.6 / 0/8 | 0 / 1.3 / 0/6 | 5 / 2.8 / 0/6 | 1 / 2.7 / 0/3 | 0 / 1.0 / 0/5 | 1 / 1.0 / 0/2 |
| Cambridgeshire |  | 0 / 0.1 / 0/8 | 3 / 3.1 / 0/8 | 1 / 1.5 / 0/6 | 3 / 2.2 / 0/6 | 3 / 7.0 / 2/3 | 0 / 0.2 / 0/5 | 1 / 1.0 / 0/2 |
| Cheshire - East |  | 1 / 1.0 / 0/8 | 1 / 1.8 / 0/8 | 0 / 0.3 / 0/6 | 0 / 1.0 / 0/6 | 0 / 0.0 / 0/3 | 0 / 0.0 / 0/5 | 2 / 2.0 / 0/2 |
| Cheshire - Warrington & Halton |  | 1 / 1.5 / 0/8 | 1 / 1.8 / 0/8 | 1 / 1.3 / 0/6 | 1 / 0.2 / 0/6 | 4 / 5.0 / 1/3 | 0 / 0.2 / 0/5 | 0 / 0.0 / 0/2 |
| Cheshire - West |  | 1 / 1.9 / 0/8 | 0 / 2.6 / 0/8 | 1 / 0.8 / 0/6 | 4 / 1.7 / 0/6 | 3 / 3.3 / 0/3 | 0 / 0.2 / 0/5 | 0 / 0.0 / 0/2 |
| Cornwall |  | 3 / 1.9 / 0/8 | 0 / 0.6 / 0/8 | 0 / 0.0 / 0/6 | 1 / 0.2 / 0/6 | 0 / 0.7 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Cumbria - North | 1 / 1.9 / 0/8 | 1 / 3.8 / 3/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.3 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Cumbria - South | 1 / 1.2 / 0/8 |  | 0 / 0.8 / 0/8 | 0 / 0.0 / 0/6 | 0 / 0.5 / 0/6 | 1 / 1.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Cumbria - West | 3 / 2.0 / 0/8 | 0 / 1.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 1 / 0.7 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Derbyshire |  | 1 / 0.5 / 0/8 | 2 / 2.5 / 0/8 | 0 / 0.5 / 0/6 | 2 / 0.8 / 0/6 | 4 / 3.7 / 0/3 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 |
| Devon |  | 0 / 0.0 / 0/8 | 4 / 3.5 / 0/8 | 1 / 2.3 / 0/6 | 2 / 0.5 / 0/6 |  | 1 / 1.4 / 0/5 | 1 / 1.0 / 0/2 |
| Dorset |  | 2 / 1.4 / 0/8 | 4 / 4.8 / 2/8 | 0 / 0.3 / 0/6 | 1 / 0.8 / 0/6 | 5 / 4.7 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Essex |  | 1 / 0.9 / 0/8 | 2 / 1.9 / 0/8 |  | 4 / 2.5 / 0/6 | 5 / 7.7 / 2/3 | 1 / 1.2 / 0/5 | 1 / 1.0 / 0/2 |
| Gloucestershire |  | 0 / 0.2 / 0/8 | 1 / 1.5 / 0/8 | 0 / 0.0 / 0/6 | 3 / 2.2 / 0/6 |  | 2 / 1.4 / 0/5 | 1 / 1.5 / 0/2 |
| Greater Manchester - Manchester & Salford |  | 1 / 1.2 / 0/8 |  | 2 / 4.7 / 2/6 |  | 3 / 4.3 / 0/3 |  | 2 / 2.0 / 0/2 |
| Greater Manchester - North | 2 / 3.4 / 1/8 | 0 / 0.0 / 0/8 | 0 / 0.2 / 0/8 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 | 0 / 0.2 / 0/5 | 0 / 0.0 / 0/2 |
| Greater Manchester - South |  | 1 / 1.2 / 0/8 | 0 / 0.9 / 0/8 | 0 / 0.5 / 0/6 | 0 / 0.0 / 0/6 | 1 / 0.3 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Greater Manchester - Wigan & Bolton |  | 0 / 0.0 / 0/8 | 0 / 0.9 / 0/8 | 0 / 0.3 / 0/6 | 0 / 0.0 / 0/6 | 1 / 0.3 / 0/3 | 1 / 1.0 / 0/5 | 1 / 1.0 / 0/2 |
| Hampshire |  |  | 9 / 6.5 / 5/8 | 1 / 2.3 / 0/6 | 6 / 4.5 / 2/6 | 3 / 4.3 / 0/3 | 3 / 3.6 / 0/5 |  |
| Herefordshire | 0 / 1.6 / 0/8 | 0 / 0.1 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 1 / 2.3 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Hertfordshire |  | 3 / 2.4 / 0/8 | 3 / 3.5 / 0/8 | 1 / 1.8 / 0/6 | 2 / 1.3 / 0/6 | 1 / 1.0 / 0/3 | 0 / 0.2 / 0/5 | 2 / 1.5 / 0/2 |
| Kent |  |  | 4 / 4.8 / 0/8 | 3 / 5.3 / 2/6 | 2 / 2.7 / 0/6 | 3 / 4.7 / 1/3 | 1 / 1.8 / 0/5 | 0 / 0.0 / 0/2 |
| Lancashire - Blackpool & Fylde | 1 / 0.9 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/6 | 2 / 0.7 / 0/6 | 0 / 0.3 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Lancashire - Central | 2 / 3.0 / 0/8 | 1 / 0.4 / 0/8 | 0 / 0.2 / 0/8 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.7 / 0/3 | 0 / 0.4 / 0/5 | 0 / 0.0 / 0/2 |
| Lancashire - East | 1 / 2.6 / 0/8 | 1 / 0.9 / 0/8 | 2 / 0.2 / 0/8 | 0 / 0.3 / 0/6 | 1 / 1.0 / 0/6 | 2 / 1.3 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Lancashire - North | 1 / 1.0 / 0/8 | 2 / 1.6 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Lancashire - West | 1 / 1.7 / 0/7 | 0 / 0.1 / 0/7 | 1 / 1.6 / 0/7 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Leicestershire |  | 0 / 0.1 / 0/8 | 0 / 1.5 / 0/8 | 1 / 1.3 / 0/6 | 2 / 0.8 / 0/6 | 3 / 5.0 / 1/3 | 1 / 1.0 / 0/5 | 3 / 3.0 / 0/2 |
| Lincolnshire |  | 2 / 2.1 / 0/8 | 1 / 1.0 / 0/8 | 2 / 1.5 / 0/6 | 3 / 2.7 / 0/6 | 3 / 4.3 / 0/3 | 2 / 1.6 / 0/5 | 1 / 1.0 / 0/2 |
| London |  |  |  |  |  | 5 / 5.7 / 1/3 |  |  |
| Merseyside - Liverpool |  | 0 / 0.5 / 0/8 | 0 / 0.4 / 0/8 | 0 / 0.5 / 0/6 | 2 / 1.7 / 0/6 | 0 / 0.7 / 0/3 | 0 / 0.2 / 0/5 | 0 / 0.0 / 0/2 |
| Merseyside - Sefton | 0 / 0.1 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Merseyside - St Helens & Knowsley | 0 / 2.7 / 0/7 | 0 / 0.0 / 0/7 | 0 / 1.0 / 0/7 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 1 / 2.3 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Merseyside - Wirral | 1 / 1.8 / 0/8 | 1 / 0.5 / 0/8 | 1 / 1.0 / 0/8 | 0 / 0.3 / 0/6 | 1 / 0.2 / 0/6 | 0 / 0.0 / 0/3 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 |
| Norfolk |  | 2 / 1.5 / 0/8 | 0 / 1.0 / 0/8 |  | 2 / 1.5 / 0/6 | 4 / 6.0 / 2/3 | 0 / 0.2 / 0/5 | 1 / 1.0 / 0/2 |
| North East |  |  |  | 1 / 1.2 / 0/6 | 4 / 4.2 / 0/6 |  | 1 / 1.2 / 0/5 | 2 / 2.0 / 0/2 |
| North Scotland | 5 / 6.1 / 3/7 | 0 / 0.0 / 0/7 | 4 / 3.3 / 0/7 | 0 / 0.3 / 0/6 | 0 / 0.0 / 0/6 | 2 / 2.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| North Wales - East | 4 / 4.6 / 1/7 | 0 / 0.3 / 0/7 | 1 / 1.6 / 0/7 | 0 / 0.0 / 0/6 | 1 / 0.3 / 0/6 | 2 / 2.3 / 0/3 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 |
| North Wales - West | 2 / 1.7 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 | 0 / 0.2 / 0/5 | 0 / 0.0 / 0/2 |
| Northamptonshire |  | 0 / 0.0 / 0/8 | 4 / 2.9 / 0/8 | 1 / 1.3 / 0/6 | 3 / 2.0 / 0/6 | 2 / 5.0 / 2/3 | 2 / 2.8 / 1/5 | 0 / 0.0 / 0/2 |
| Northern Ireland - East |  | 2 / 2.0 / 0/7 | 0 / 0.0 / 0/7 | 2 / 1.2 / 0/6 | 0 / 0.0 / 0/6 |  | 0 / 0.2 / 0/5 | 1 / 1.0 / 0/2 |
| Northern Ireland - West | 5 / 4.1 / 0/7 | 0 / 0.0 / 0/7 | 1 / 1.0 / 0/7 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.3 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Nottinghamshire |  | 1 / 0.6 / 0/8 | 0 / 2.0 / 0/8 | 2 / 2.3 / 0/6 | 2 / 1.8 / 0/6 | 4 / 5.3 / 2/3 |  | 1 / 1.0 / 0/2 |
| Oxfordshire |  |  | 4 / 3.5 / 0/8 | 2 / 1.8 / 0/6 | 6 / 4.2 / 1/6 | 2 / 3.7 / 0/3 | 0 / 0.2 / 0/5 | 0 / 0.0 / 0/2 |
| Rutland | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Scotland - Borders | 1 / 1.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Scotland Central - Edinburgh & Lothians |  | 0 / 0.1 / 0/7 | 3 / 2.6 / 0/7 | 1 / 2.8 / 0/6 | 0 / 0.0 / 0/6 | 0 / 2.0 / 0/3 | 0 / 0.4 / 0/5 | 0 / 0.0 / 0/2 |
| Scotland Central - Falkirk & Stirling | 2 / 3.1 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 1 / 1.3 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Scotland Central - Fife | 1 / 1.6 / 0/7 | 0 / 0.0 / 0/7 | 2 / 1.1 / 0/7 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 1 / 1.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Scotland Central - Tayside | 4 / 4.3 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.3 / 0/7 | 1 / 1.0 / 0/6 | 0 / 0.0 / 0/6 | 1 / 1.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Scotland West - Ayrshire | 0 / 0.6 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 1 / 0.3 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Scotland West - Glasgow |  | 0 / 0.0 / 0/7 | 2 / 3.1 / 0/7 | 0 / 0.3 / 0/6 | 0 / 0.3 / 0/6 | 0 / 0.7 / 0/3 | 1 / 1.0 / 0/5 | 3 / 2.5 / 0/2 |
| Scotland West - Lanarkshire | 0 / 0.7 / 0/7 | 0 / 0.1 / 0/7 | 0 / 0.6 / 0/7 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Scotland West - Renfrewshire & Inverclyde | 1 / 1.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.4 / 0/7 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 1.3 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Shropshire |  | 2 / 2.5 / 0/8 | 0 / 1.5 / 0/8 | 2 / 1.7 / 0/6 | 0 / 0.3 / 0/6 |  | 2 / 1.8 / 0/5 | 0 / 0.0 / 0/2 |
| Somerset |  | 5 / 4.6 / 2/8 | 1 / 1.0 / 0/8 | 0 / 0.3 / 0/6 | 0 / 0.0 / 0/6 | 3 / 5.0 / 1/3 | 0 / 0.2 / 0/5 | 0 / 0.0 / 0/2 |
| Staffordshire |  | 0 / 0.2 / 0/8 | 2 / 1.5 / 0/8 | 0 / 0.0 / 0/6 | 2 / 1.2 / 0/6 | 2 / 2.7 / 0/3 | 0 / 0.2 / 0/5 |  |
| Suffolk |  | 1 / 1.2 / 0/8 | 2 / 1.6 / 0/8 |  | 0 / 0.0 / 0/6 | 3 / 3.0 / 0/3 | 1 / 1.0 / 0/5 | 1 / 0.5 / 0/2 |
| Surrey |  |  | 1 / 4.9 / 3/8 | 3 / 4.2 / 0/6 |  | 5 / 5.7 / 2/3 | 2 / 1.8 / 0/5 |  |
| Sussex |  |  | 3 / 3.4 / 0/8 | 1 / 2.0 / 0/6 | 3 / 2.2 / 0/6 | 4 / 4.7 / 0/3 | 6 / 6.0 / 5/5 | 2 / 2.0 / 0/2 |
| Wales - Mid | 0 / 0.1 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Wales - West | 2 / 1.7 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/6 | 1 / 1.0 / 0/3 | 0 / 0.2 / 0/5 | 0 / 0.0 / 0/2 |
| Wales South - Cardiff & Vale | 3 / 4.3 / 1/7 | 0 / 0.0 / 0/7 | 3 / 1.9 / 0/7 | 1 / 1.5 / 0/6 | 0 / 0.8 / 0/6 | 2 / 2.3 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Wales South - Gwent | 2 / 3.1 / 0/7 | 0 / 0.1 / 0/7 | 0 / 0.1 / 0/7 | 1 / 1.5 / 0/6 | 0 / 0.0 / 0/6 | 1 / 1.0 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Wales South - Swansea Bay | 2 / 3.1 / 1/7 | 0 / 0.1 / 0/7 | 2 / 2.4 / 0/7 | 0 / 0.8 / 0/6 | 0 / 0.0 / 0/6 | 1 / 0.3 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| Wales South - Valleys | 0 / 1.4 / 1/7 | 0 / 0.0 / 0/7 | 0 / 0.4 / 0/7 | 3 / 2.7 / 0/6 | 0 / 0.7 / 0/6 | 0 / 0.3 / 0/3 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/2 |
| West Midlands - Birmingham & Solihull |  | 1 / 1.1 / 0/8 | 2 / 3.2 / 0/8 | 3 / 4.7 / 2/6 |  | 2 / 2.7 / 0/3 |  | 3 / 3.0 / 0/2 |
| West Midlands - Black Country |  | 1 / 1.2 / 0/8 | 1 / 1.0 / 0/8 | 2 / 1.2 / 0/6 | 0 / 0.3 / 0/6 | 1 / 1.0 / 0/3 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 |
| West Midlands - Coventry & Warwickshire |  | 0 / 0.0 / 0/8 | 1 / 0.6 / 0/8 | 0 / 0.7 / 0/6 | 3 / 2.3 / 0/6 | 1 / 2.7 / 0/3 | 3 / 3.2 / 0/5 | 0 / 0.0 / 0/2 |
| Wiltshire |  |  | 3 / 2.2 / 0/8 | 3 / 3.3 / 0/6 | 0 / 0.8 / 0/6 | 4 / 4.7 / 0/3 | 0 / 1.0 / 0/5 | 1 / 1.0 / 0/2 |
| Worcestershire |  | 1 / 1.8 / 0/8 | 2 / 2.8 / 0/8 | 0 / 0.3 / 0/6 | 0 / 1.5 / 0/6 | 0 / 1.7 / 0/3 | 0 / 0.4 / 0/5 | 0 / 0.5 / 0/2 |
| Yorkshire - East |  | 1 / 1.0 / 0/8 | 1 / 1.6 / 0/8 | 1 / 1.0 / 0/6 | 1 / 0.3 / 0/6 | 5 / 5.0 / 0/3 | 1 / 1.4 / 0/5 | 2 / 2.5 / 0/2 |
| Yorkshire - North |  | 4 / 4.4 / 0/8 | 2 / 0.9 / 0/8 | 0 / 0.2 / 0/6 | 5 / 1.3 / 0/6 |  | 2 / 1.4 / 0/5 | 0 / 0.0 / 0/2 |
| Yorkshire - South |  |  | 2 / 2.0 / 0/8 | 3 / 3.0 / 0/6 | 2 / 1.7 / 0/6 | 1 / 4.3 / 2/3 | 0 / 0.0 / 0/5 | 1 / 1.0 / 0/2 |
| Yorkshire - West |  |  |  | 5 / 4.3 / 0/6 | 5 / 4.2 / 1/6 |  |  | 2 / 2.0 / 0/2 |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Live regions | 46 / 78 | 11 / 78 | 4 / 78 | 4 / 78 | 5 / 78 | 8 / 78 | 6 / 78 | 4 / 78 |
| Live slice placements | 1176 | 69 + 1 CHECK | 33 | 10 + 2 CHECK | 52 | 42 + 3 CHECK | 20 | 16 |

**Live slices: 88 / 624.**
