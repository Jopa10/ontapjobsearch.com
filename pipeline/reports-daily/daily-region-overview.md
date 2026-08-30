# Ontap daily regional overview

Generated: 2026-08-30T10:52:57+01:00

## SITEWIDE RECONCILIATION

| Measure | Count |
|---|---:|
| Unique live jobs | 1,374 |
| Unique JobG8 jobs | 956 |
| Unique non-JobG8 jobs | 418 |
| Regional/category slice placements | 1,416 |
| Jobs appearing on multiple slices | 42 |
| Extra slice placements | 42 |
| Unique jobs outside governed slices | 0 |
| Jobs found in non-LIVE slices | 0 |

**Reconciliation: 1,374 unique jobs + 42 extra slice placements = 1,416 regional/category slice placements.**

Latest source-count CSV: `pipeline/reports-daily/live-job-source-count-2026-08-29.csv` — **STALE — CSV says 1,409 for 2026-08-29**.

### Provider breakdown

| Provider | Unique live jobs | Jobs on 2+ slices | Extra slice placements |
|---|---:|---:|---:|
| JobG8 | 956 | 42 | 42 |
| NEJobs | 30 | 0 | 0 |
| NHS Jobs | 209 | 0 | 0 |
| Teaching Vacancies | 177 | 0 | 0 |
| VONNE | 2 | 0 | 0 |

> LIVE counts come directly from the current published `app/` JSON, deduplicated within each canonical region/family slice while preserving legitimate appearances in more than one family. This is the live-site authority for the reconciliation above; the dated source-count CSV is shown only as a freshness cross-check. The overview covers all 78 assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 78-market coverage has run, NOT LIVE Admin/Support and Customer Service may fall back to the latest all-region Module 2 profile (2026-08-17), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-08-30) used by the production family run, across 78 UK markets with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across 78 UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across 78, 78, 78 and 78 UK markets respectively, using their governed production boundaries and canonical geo. NOT LIVE Customer Service / Contact Centre was assessed from that same feed across 78 UK markets using its governed exact-title, salary and geography rules. All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

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
| Devon | 35 |  |  |  |  | 10 |  |  |
| Dorset | 16 |  |  |  |  |  |  |  |
| Essex | 40 |  |  | 2 |  |  |  |  |
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
| Bedfordshire | 8 / 5.6 / 4/9 | 0 / 0.2 / 0/9 | 2 / 2.2 / 0/9 | 3 / 4.0 / 0/7 | 1 / 1.1 / 0/7 | 1 / 0.8 / 0/4 | 1 / 1.2 / 0/6 | 1 / 1.0 / 0/3 |
| Berkshire |  | 6 / 4.0 / 3/9 | 1 / 0.9 / 0/9 | 0 / 0.6 / 0/7 |  | 0 / 0.2 / 0/4 |  | 0 / 0.0 / 0/3 |
| Bristol & Bath |  | 0 / 1.1 / 0/9 | 8 / 7.1 / 8/9 | 1 / 3.3 / 1/7 | 5 / 2.6 / 0/7 |  | 2 / 2.0 / 0/6 | 2 / 1.3 / 0/3 |
| Buckinghamshire |  | 0 / 0.9 / 0/9 | 1 / 0.7 / 0/9 | 0 / 1.1 / 0/7 | 4 / 3.0 / 0/7 | 1 / 2.2 / 0/4 | 0 / 0.8 / 0/6 | 2 / 1.3 / 0/3 |
| Cambridgeshire |  | 0 / 0.1 / 0/9 | 3 / 3.1 / 0/9 | 1 / 1.4 / 0/7 | 3 / 2.3 / 0/7 | 3 / 6.0 / 2/4 | 0 / 0.2 / 0/6 | 1 / 1.0 / 0/3 |
| Cheshire - East |  | 0 / 0.8 / 0/9 | 1 / 1.7 / 0/9 | 0 / 0.3 / 0/7 | 0 / 0.9 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.0 / 0/6 | 2 / 2.0 / 0/3 |
| Cheshire - Warrington & Halton |  | 1 / 1.4 / 0/9 | 1 / 1.7 / 0/9 | 1 / 1.3 / 0/7 | 1 / 0.3 / 0/7 | 4 / 4.8 / 1/4 | 0 / 0.2 / 0/6 | 0 / 0.0 / 0/3 |
| Cheshire - West |  | 1 / 1.8 / 0/9 | 1 / 2.4 / 0/9 | 1 / 0.9 / 0/7 | 4 / 2.0 / 0/7 | 3 / 3.2 / 0/4 | 0 / 0.2 / 0/6 | 0 / 0.0 / 0/3 |
| Cornwall |  | 3 / 2.0 / 0/9 | 0 / 0.6 / 0/9 | 0 / 0.0 / 0/7 | 1 / 0.3 / 0/7 | 0 / 0.5 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Cumbria - North | 1 / 1.8 / 0/9 | 2 / 3.7 / 3/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.2 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Cumbria - South | 1 / 1.2 / 0/9 |  | 1 / 0.9 / 0/9 | 0 / 0.0 / 0/7 | 0 / 0.4 / 0/7 | 1 / 1.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Cumbria - West | 2 / 2.0 / 0/9 | 1 / 1.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 1 / 0.8 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Derbyshire |  | 0 / 0.4 / 0/9 | 2 / 2.4 / 0/9 | 0 / 0.4 / 0/7 | 2 / 1.0 / 0/7 | 4 / 3.8 / 0/4 | 0 / 0.0 / 0/6 | 1 / 1.0 / 0/3 |
| Devon |  | 0 / 0.1 / 0/9 | 4 / 3.6 / 0/9 | 1 / 2.1 / 0/7 | 2 / 0.7 / 0/7 |  | 1 / 1.3 / 0/6 | 2 / 1.3 / 0/3 |
| Dorset |  | 1 / 1.2 / 0/9 | 4 / 4.7 / 2/9 | 0 / 0.3 / 0/7 | 2 / 1.0 / 0/7 | 5 / 4.8 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Essex |  | 1 / 0.9 / 0/9 | 2 / 1.9 / 0/9 |  | 3 / 2.6 / 0/7 | 5 / 7.0 / 2/4 | 1 / 1.2 / 0/6 | 1 / 1.0 / 0/3 |
| Gloucestershire |  | 0 / 0.2 / 0/9 | 0 / 1.2 / 0/9 | 0 / 0.0 / 0/7 | 4 / 2.4 / 0/7 |  | 2 / 1.5 / 0/6 | 1 / 1.3 / 0/3 |
| Greater Manchester - Manchester & Salford |  | 1 / 1.2 / 0/9 |  | 2 / 4.3 / 2/7 |  | 4 / 4.2 / 0/4 |  | 2 / 2.0 / 0/3 |
| Greater Manchester - North | 2 / 3.2 / 1/9 | 0 / 0.0 / 0/9 | 0 / 0.2 / 0/9 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.2 / 0/6 | 0 / 0.0 / 0/3 |
| Greater Manchester - South |  | 0 / 1.0 / 0/9 | 0 / 0.8 / 0/9 | 0 / 0.4 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Greater Manchester - Wigan & Bolton |  | 0 / 0.0 / 0/9 | 0 / 0.8 / 0/9 | 0 / 0.3 / 0/7 | 0 / 0.0 / 0/7 | 1 / 0.5 / 0/4 | 1 / 1.0 / 0/6 | 1 / 1.0 / 0/3 |
| Hampshire |  |  | 9 / 6.8 / 6/9 | 1 / 2.1 / 0/7 | 5 / 4.4 / 1/7 | 3 / 4.0 / 0/4 | 3 / 3.5 / 0/6 |  |
| Herefordshire | 0 / 1.4 / 0/9 | 1 / 0.3 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 1.8 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Hertfordshire |  | 3 / 2.4 / 0/9 | 3 / 3.4 / 0/9 | 1 / 1.7 / 0/7 | 2 / 1.4 / 0/7 | 1 / 1.0 / 0/4 | 0 / 0.2 / 0/6 | 2 / 1.7 / 0/3 |
| Kent |  |  | 4 / 4.7 / 0/9 | 4 / 5.1 / 2/7 | 2 / 2.6 / 0/7 | 3 / 4.2 / 1/4 | 1 / 1.7 / 0/6 | 0 / 0.0 / 0/3 |
| Lancashire - Blackpool & Fylde | 1 / 0.9 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/7 | 2 / 0.9 / 0/7 | 0 / 0.2 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Lancashire - Central | 2 / 2.9 / 0/9 | 0 / 0.2 / 0/9 | 0 / 0.2 / 0/9 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.5 / 0/4 | 0 / 0.3 / 0/6 | 0 / 0.0 / 0/3 |
| Lancashire - East | 1 / 2.4 / 0/9 | 1 / 0.9 / 0/9 | 2 / 0.4 / 0/9 | 0 / 0.3 / 0/7 | 1 / 1.0 / 0/7 | 2 / 1.5 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Lancashire - North | 1 / 1.0 / 0/9 | 2 / 1.7 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Lancashire - West | 1 / 1.6 / 0/8 | 0 / 0.1 / 0/8 | 1 / 1.5 / 0/8 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Leicestershire |  | 0 / 0.1 / 0/9 | 0 / 1.4 / 0/9 | 1 / 1.3 / 0/7 | 2 / 1.0 / 0/7 | 1 / 3.8 / 1/4 | 1 / 1.0 / 0/6 | 3 / 3.0 / 0/3 |
| Lincolnshire |  | 2 / 2.1 / 0/9 | 2 / 1.1 / 0/9 | 2 / 1.6 / 0/7 | 3 / 2.7 / 0/7 | 2 / 3.8 / 0/4 | 2 / 1.7 / 0/6 | 2 / 1.3 / 0/3 |
| London |  |  |  |  |  | 4 / 5.2 / 1/4 |  |  |
| Merseyside - Liverpool |  | 0 / 0.4 / 0/9 | 0 / 0.3 / 0/9 | 0 / 0.4 / 0/7 | 1 / 1.4 / 0/7 | 0 / 0.5 / 0/4 | 0 / 0.2 / 0/6 | 0 / 0.0 / 0/3 |
| Merseyside - Sefton | 0 / 0.1 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Merseyside - St Helens & Knowsley | 0 / 2.4 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.9 / 0/8 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 1 / 2.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Merseyside - Wirral | 1 / 1.7 / 0/9 | 1 / 0.6 / 0/9 | 1 / 1.0 / 0/9 | 0 / 0.3 / 0/7 | 1 / 0.3 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.0 / 0/6 | 1 / 1.0 / 0/3 |
| Norfolk |  | 2 / 1.6 / 0/9 | 0 / 0.9 / 0/9 |  | 2 / 1.6 / 0/7 | 4 / 5.5 / 2/4 | 0 / 0.2 / 0/6 | 1 / 1.0 / 0/3 |
| North East |  |  |  | 1 / 1.1 / 0/7 | 4 / 4.1 / 0/7 |  | 1 / 1.2 / 0/6 | 2 / 2.0 / 0/3 |
| North Scotland | 4 / 5.9 / 3/8 | 0 / 0.0 / 0/8 | 4 / 3.5 / 0/8 | 0 / 0.3 / 0/7 | 0 / 0.0 / 0/7 | 3 / 2.2 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| North Wales - East | 4 / 4.5 / 1/8 | 0 / 0.2 / 0/8 | 1 / 1.5 / 0/8 | 0 / 0.0 / 0/7 | 1 / 0.4 / 0/7 | 2 / 2.2 / 0/4 | 0 / 0.0 / 0/6 | 1 / 1.0 / 0/3 |
| North Wales - West | 2 / 1.8 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.2 / 0/6 | 1 / 0.3 / 0/3 |
| Northamptonshire |  | 0 / 0.0 / 0/9 | 6 / 3.3 / 1/9 | 1 / 1.3 / 0/7 | 2 / 1.7 / 0/7 | 2 / 4.2 / 2/4 | 2 / 2.7 / 1/6 | 0 / 0.0 / 0/3 |
| Northern Ireland - East |  | 2 / 2.0 / 0/8 | 0 / 0.0 / 0/8 | 2 / 1.3 / 0/7 | 0 / 0.0 / 0/7 |  | 0 / 0.2 / 0/6 | 1 / 1.0 / 0/3 |
| Northern Ireland - West | 5 / 4.2 / 0/8 | 0 / 0.0 / 0/8 | 1 / 1.0 / 0/8 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.2 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Nottinghamshire |  | 0 / 0.6 / 0/9 | 0 / 1.8 / 0/9 | 2 / 2.3 / 0/7 | 2 / 1.9 / 0/7 | 4 / 5.0 / 2/4 |  | 1 / 1.0 / 0/3 |
| Oxfordshire |  |  | 4 / 3.6 / 0/9 | 2 / 1.9 / 0/7 | 6 / 4.4 / 2/7 | 2 / 3.2 / 0/4 | 0 / 0.2 / 0/6 | 1 / 0.3 / 0/3 |
| Rutland | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Scotland - Borders | 1 / 1.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Scotland Central - Edinburgh & Lothians |  | 0 / 0.1 / 0/8 | 3 / 2.6 / 0/8 | 1 / 2.6 / 0/7 | 0 / 0.0 / 0/7 | 0 / 1.5 / 0/4 | 0 / 0.3 / 0/6 | 0 / 0.0 / 0/3 |
| Scotland Central - Falkirk & Stirling | 2 / 3.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 1 / 1.2 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Scotland Central - Fife | 1 / 1.5 / 0/8 | 0 / 0.0 / 0/8 | 2 / 1.2 / 0/8 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 1 / 1.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Scotland Central - Tayside | 3 / 4.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.2 / 0/8 | 1 / 1.0 / 0/7 | 0 / 0.0 / 0/7 | 1 / 1.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Scotland West - Ayrshire | 0 / 0.5 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 1 / 0.4 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Scotland West - Glasgow |  | 0 / 0.0 / 0/8 | 2 / 3.0 / 0/8 | 0 / 0.3 / 0/7 | 0 / 0.3 / 0/7 | 0 / 0.5 / 0/4 | 0 / 0.8 / 0/6 | 3 / 2.7 / 0/3 |
| Scotland West - Lanarkshire | 0 / 0.6 / 0/8 | 0 / 0.1 / 0/8 | 0 / 0.5 / 0/8 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Scotland West - Renfrewshire & Inverclyde | 1 / 1.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.4 / 0/8 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 1.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Shropshire |  | 2 / 2.4 / 0/9 | 0 / 1.3 / 0/9 | 2 / 1.7 / 0/7 | 0 / 0.3 / 0/7 |  | 2 / 1.8 / 0/6 | 0 / 0.0 / 0/3 |
| Somerset |  | 4 / 4.7 / 3/9 | 2 / 1.2 / 0/9 | 0 / 0.3 / 0/7 | 1 / 0.1 / 0/7 | 3 / 4.5 / 1/4 | 0 / 0.2 / 0/6 | 0 / 0.0 / 0/3 |
| Staffordshire |  | 0 / 0.2 / 0/9 | 2 / 1.6 / 0/9 | 0 / 0.0 / 0/7 | 2 / 1.3 / 0/7 | 1 / 2.2 / 0/4 | 0 / 0.2 / 0/6 |  |
| Suffolk |  | 0 / 1.1 / 0/9 | 2 / 1.7 / 0/9 |  | 0 / 0.0 / 0/7 | 1 / 2.5 / 0/4 | 1 / 1.0 / 0/6 | 1 / 0.7 / 0/3 |
| Surrey |  |  | 2 / 4.7 / 3/9 | 3 / 4.0 / 0/7 |  | 5 / 5.5 / 2/4 | 2 / 1.8 / 0/6 |  |
| Sussex |  |  | 3 / 3.3 / 0/9 | 1 / 1.9 / 0/7 | 3 / 2.3 / 0/7 | 4 / 4.5 / 0/4 | 6 / 6.0 / 6/6 | 3 / 2.3 / 0/3 |
| Wales - Mid | 0 / 0.1 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Wales - West | 2 / 1.8 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/7 | 1 / 1.0 / 0/4 | 0 / 0.2 / 0/6 | 0 / 0.0 / 0/3 |
| Wales South - Cardiff & Vale | 3 / 4.1 / 1/8 | 0 / 0.0 / 0/8 | 2 / 1.9 / 0/8 | 1 / 1.4 / 0/7 | 1 / 0.9 / 0/7 | 1 / 2.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Wales South - Gwent | 2 / 3.0 / 0/8 | 0 / 0.1 / 0/8 | 0 / 0.1 / 0/8 | 1 / 1.4 / 0/7 | 0 / 0.0 / 0/7 | 1 / 1.0 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Wales South - Swansea Bay | 1 / 2.8 / 1/8 | 0 / 0.1 / 0/8 | 2 / 2.4 / 0/8 | 0 / 0.7 / 0/7 | 0 / 0.0 / 0/7 | 0 / 0.2 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| Wales South - Valleys | 0 / 1.2 / 1/8 | 0 / 0.0 / 0/8 | 0 / 0.4 / 0/8 | 4 / 2.9 / 0/7 | 0 / 0.6 / 0/7 | 0 / 0.2 / 0/4 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/3 |
| West Midlands - Birmingham & Solihull |  | 1 / 1.1 / 0/9 | 2 / 3.1 / 0/9 | 3 / 4.4 / 2/7 |  | 2 / 2.8 / 0/4 |  | 3 / 3.0 / 0/3 |
| West Midlands - Black Country |  | 1 / 1.2 / 0/9 | 1 / 1.0 / 0/9 | 1 / 1.0 / 0/7 | 0 / 0.3 / 0/7 | 2 / 1.5 / 0/4 | 0 / 0.0 / 0/6 | 1 / 1.0 / 0/3 |
| West Midlands - Coventry & Warwickshire |  | 0 / 0.0 / 0/9 | 1 / 0.7 / 0/9 | 0 / 0.6 / 0/7 | 3 / 2.4 / 0/7 | 2 / 2.5 / 0/4 | 3 / 3.2 / 0/6 | 0 / 0.0 / 0/3 |
| Wiltshire |  |  | 3 / 2.3 / 0/9 | 3 / 3.3 / 0/7 | 1 / 0.9 / 0/7 | 4 / 4.5 / 0/4 | 0 / 0.8 / 0/6 | 1 / 1.0 / 0/3 |
| Worcestershire |  | 1 / 1.7 / 0/9 | 2 / 2.7 / 0/9 | 0 / 0.3 / 0/7 | 1 / 1.4 / 0/7 | 0 / 1.2 / 0/4 | 0 / 0.3 / 0/6 | 0 / 0.3 / 0/3 |
| Yorkshire - East |  | 1 / 1.0 / 0/9 | 1 / 1.6 / 0/9 | 1 / 1.0 / 0/7 | 1 / 0.4 / 0/7 | 5 / 5.0 / 0/4 | 1 / 1.3 / 0/6 | 2 / 2.3 / 0/3 |
| Yorkshire - North |  | 4 / 4.3 / 0/9 | 2 / 1.0 / 0/9 | 0 / 0.1 / 0/7 | 4 / 1.7 / 0/7 |  | 2 / 1.5 / 0/6 | 2 / 0.7 / 0/3 |
| Yorkshire - South |  |  | 2 / 2.0 / 0/9 | 2 / 2.9 / 0/7 | 2 / 1.7 / 0/7 | 1 / 3.5 / 2/4 | 0 / 0.0 / 0/6 | 1 / 1.0 / 0/3 |
| Yorkshire - West |  |  |  | 4 / 4.1 / 0/7 | 7 / 4.6 / 2/7 |  |  | 2 / 2.0 / 0/3 |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Live regions | 46 / 78 | 11 / 78 | 4 / 78 | 4 / 78 | 5 / 78 | 8 / 78 | 6 / 78 | 4 / 78 |
| Live slice placements | 1174 | 69 + 1 CHECK | 33 | 10 + 2 CHECK | 52 | 42 + 3 CHECK | 20 | 16 |

**Live slices: 88 / 624.**
