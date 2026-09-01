# Ontap daily regional overview

Generated: 2026-09-01T13:08:23+01:00

## SITEWIDE RECONCILIATION

| Measure | Count |
|---|---:|
| Unique live jobs | 1,671 |
| Unique JobG8 jobs | 1,308 |
| Unique non-JobG8 jobs | 363 |
| Regional/category slice placements | 1,722 |
| Jobs appearing on multiple slices | 51 |
| Extra slice placements | 51 |
| Unique jobs outside governed slices | 0 |
| Jobs found in non-LIVE slices | 0 |

**Reconciliation: 1,671 unique jobs + 51 extra slice placements = 1,722 regional/category slice placements.**

Latest source-count CSV: `pipeline/reports-daily/live-job-source-count-2026-09-01.csv` — **STALE — CSV says 1,690 for 2026-09-01**.

### Provider breakdown

| Provider | Unique live jobs | Jobs on 2+ slices | Extra slice placements |
|---|---:|---:|---:|
| JobG8 | 1,308 | 51 | 51 |
| NEJobs | 19 | 0 | 0 |
| NHS Jobs | 223 | 0 | 0 |
| Teaching Vacancies | 119 | 0 | 0 |
| VONNE | 2 | 0 | 0 |

> LIVE counts come directly from the current published `app/` JSON, deduplicated within each canonical region/family slice while preserving legitimate appearances in more than one family. This is the live-site authority for the reconciliation above; the dated source-count CSV is shown only as a freshness cross-check. The overview covers all 78 assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 78-market coverage has run, NOT LIVE Admin/Support and Customer Service may fall back to the latest all-region Module 2 profile (2026-08-17), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-09-01) used by the production family run, across 78 UK markets with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across 78 UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across 78, 78, 78 and 78 UK markets respectively, using their governed production boundaries and canonical geo. NOT LIVE Customer Service / Contact Centre was assessed from that same feed across 78 UK markets using its governed exact-title, salary and geography rules. All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

## LIVE

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire | CHECK |  |  |  |  |  |  |  |
| Berkshire | 29 |  |  |  | 13 |  | 2 |  |
| Bristol & Bath | 26 |  | CHECK |  |  | CHECK |  |  |
| Buckinghamshire | 30 |  |  |  | CHECK |  |  |  |
| Cambridgeshire | 28 |  |  |  |  |  |  |  |
| Cheshire - East | 11 |  |  |  |  |  |  |  |
| Cheshire - Warrington & Halton | 1 |  |  |  |  |  |  |  |
| Cheshire - West | 10 |  |  |  |  |  |  |  |
| Cornwall | 3 |  |  |  |  |  |  |  |
| Cumbria - North |  |  |  |  |  |  |  |  |
| Cumbria - South |  | 2 |  |  |  |  |  |  |
| Cumbria - West |  |  |  |  |  |  |  |  |
| Derbyshire | 12 |  |  |  |  |  |  |  |
| Devon | 31 |  |  |  |  | CHECK |  |  |
| Dorset | 18 |  |  |  |  |  |  |  |
| Essex | 45 |  |  | 6 |  |  |  |  |
| Gloucestershire | 32 |  |  |  |  | CHECK |  |  |
| Greater Manchester - Manchester & Salford | 38 |  | 19 |  | 22 |  | 4 |  |
| Greater Manchester - North |  |  |  |  |  |  |  |  |
| Greater Manchester - South | 10 |  |  |  |  |  |  |  |
| Greater Manchester - Wigan & Bolton | 6 |  |  |  |  |  |  |  |
| Hampshire | 78 | 6 |  |  |  |  |  | 12 |
| Herefordshire |  |  |  |  |  |  |  |  |
| Hertfordshire | 44 |  |  |  |  |  |  |  |
| Kent | 66 | 2 |  |  |  |  |  |  |
| Lancashire - Blackpool & Fylde |  |  |  |  |  |  |  |  |
| Lancashire - Central |  |  |  |  |  |  |  |  |
| Lancashire - East |  |  |  |  |  |  |  |  |
| Lancashire - North |  |  |  |  |  |  |  |  |
| Lancashire - West |  |  |  |  |  |  |  |  |
| Leicestershire | 40 |  |  |  |  |  |  |  |
| Lincolnshire | 16 |  |  |  |  |  |  |  |
| London | 175 | 12 | 42 | 14 | 70 |  | 12 | 6 |
| Merseyside - Liverpool | 16 |  |  |  |  |  |  |  |
| Merseyside - Sefton |  |  |  |  |  |  |  |  |
| Merseyside - St Helens & Knowsley |  |  |  |  |  |  |  |  |
| Merseyside - Wirral |  |  |  |  |  |  |  |  |
| Norfolk | 31 |  |  | CHECK |  |  |  |  |
| North East | 66 | 1 | 10 |  |  | CHECK |  |  |
| North Scotland |  |  |  |  |  |  |  |  |
| North Wales - East |  |  |  |  |  |  |  |  |
| North Wales - West |  |  |  |  |  |  |  |  |
| Northamptonshire | 25 |  |  |  |  |  |  |  |
| Northern Ireland - East | 6 |  |  |  |  | CHECK |  |  |
| Northern Ireland - West |  |  |  |  |  |  |  |  |
| Nottinghamshire | 28 |  |  |  |  |  | 3 |  |
| Oxfordshire | 43 | 4 |  |  |  |  |  |  |
| Rutland |  |  |  |  |  |  |  |  |
| Scotland - Borders |  |  |  |  |  |  |  |  |
| Scotland Central - Edinburgh & Lothians | 9 |  |  |  |  |  |  |  |
| Scotland Central - Falkirk & Stirling |  |  |  |  |  |  |  |  |
| Scotland Central - Fife |  |  |  |  |  |  |  |  |
| Scotland Central - Tayside |  |  |  |  |  |  |  |  |
| Scotland West - Ayrshire |  |  |  |  |  |  |  |  |
| Scotland West - Glasgow | 16 |  |  |  |  |  |  |  |
| Scotland West - Lanarkshire |  |  |  |  |  |  |  |  |
| Scotland West - Renfrewshire & Inverclyde |  |  |  |  |  |  |  |  |
| Shropshire | 13 |  |  |  |  | CHECK |  |  |
| Somerset | 21 |  |  |  |  |  |  |  |
| Staffordshire | 24 |  |  |  |  |  |  | 5 |
| Suffolk | 17 |  |  | 1 |  |  |  |  |
| Surrey | 65 | 4 |  |  | 12 |  |  | 13 |
| Sussex | 40 | 3 |  |  |  |  |  |  |
| Wales - Mid |  |  |  |  |  |  |  |  |
| Wales - West |  |  |  |  |  |  |  |  |
| Wales South - Cardiff & Vale |  |  |  |  |  |  |  |  |
| Wales South - Gwent |  |  |  |  |  |  |  |  |
| Wales South - Swansea Bay |  |  |  |  |  |  |  |  |
| Wales South - Valleys |  |  |  |  |  |  |  |  |
| West Midlands - Birmingham & Solihull | 40 |  |  |  | 3 |  | 3 |  |
| West Midlands - Black Country | 10 |  |  |  |  |  |  |  |
| West Midlands - Coventry & Warwickshire | 31 |  |  |  |  |  |  |  |
| Wiltshire | 16 | 2 |  |  |  |  |  |  |
| Worcestershire | 15 |  |  |  |  |  |  |  |
| Yorkshire - East | 18 |  |  |  |  |  |  |  |
| Yorkshire - North | 21 |  |  |  |  | CHECK |  |  |
| Yorkshire - South | 33 | CHECK |  |  |  |  |  |  |
| Yorkshire - West | 50 | 1 | 6 |  |  | CHECK | 4 |  |

## NOT LIVE

> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire |  | 0 / 0.2 / 0/11 | 2 / 2.2 / 0/11 | 4 / 3.8 / 0/9 | 1 / 1.1 / 0/9 | 1 / 0.7 / 0/6 | 1 / 1.0 / 0/8 | 1 / 1.0 / 0/5 |
| Berkshire |  | 0 / 3.5 / 3/11 | 7 / 1.7 / 1/11 | 2 / 0.7 / 0/9 |  | 2 / 0.5 / 0/6 |  | 1 / 0.2 / 0/5 |
| Bristol & Bath |  | 1 / 1.0 / 0/11 |  | 3 / 2.9 / 1/9 | 7 / 2.6 / 1/9 |  | 2 / 1.8 / 0/8 | 5 / 2.0 / 0/5 |
| Buckinghamshire |  | 0 / 0.7 / 0/11 | 1 / 0.6 / 0/11 | 1 / 1.0 / 0/9 |  | 1 / 2.0 / 0/6 | 1 / 0.8 / 0/8 | 6 / 2.4 / 1/5 |
| Cambridgeshire |  | 0 / 0.1 / 0/11 | 3 / 2.5 / 0/11 | 1 / 1.2 / 0/9 | 6 / 2.6 / 1/9 | 3 / 4.5 / 2/6 | 0 / 0.1 / 0/8 | 1 / 1.0 / 0/5 |
| Cheshire - East |  | 0 / 0.6 / 0/11 | 3 / 1.5 / 0/11 | 0 / 0.2 / 0/9 | 3 / 1.0 / 0/9 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/8 | 3 / 1.8 / 0/5 |
| Cheshire - Warrington & Halton |  | 1 / 1.4 / 0/11 | 6 / 2.1 / 1/11 | 2 / 1.3 / 0/9 | 1 / 0.3 / 0/9 | 7 / 4.7 / 2/6 | 0 / 0.1 / 0/8 | 0 / 0.0 / 0/5 |
| Cheshire - West |  | 0 / 1.5 / 0/11 | 0 / 2.0 / 0/11 | 2 / 1.0 / 0/9 | 6 / 2.2 / 1/9 | 1 / 2.2 / 0/6 | 1 / 0.2 / 0/8 | 1 / 0.2 / 0/5 |
| Cornwall |  | 0 / 1.5 / 0/11 | 1 / 0.5 / 0/11 | 0 / 0.0 / 0/9 | 0 / 0.2 / 0/9 | 0 / 0.3 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Cumbria - North | 1 / 1.6 / 0/11 | 0 / 2.8 / 3/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.2 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Cumbria - South | 1 / 1.1 / 0/11 |  | 1 / 0.7 / 0/11 | 0 / 0.0 / 0/9 | 2 / 0.6 / 0/9 | 0 / 0.7 / 0/6 | 1 / 0.1 / 0/8 | 0 / 0.0 / 0/5 |
| Cumbria - West | 1 / 1.8 / 0/11 | 1 / 0.8 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.5 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Derbyshire |  | 0 / 0.4 / 0/11 | 3 / 2.5 / 0/11 | 2 / 0.6 / 0/9 | 2 / 0.9 / 0/9 | 2 / 3.2 / 0/6 | 0 / 0.0 / 0/8 | 3 / 1.4 / 0/5 |
| Devon |  | 0 / 0.1 / 0/11 | 5 / 3.2 / 0/11 | 3 / 2.1 / 0/9 | 6 / 1.2 / 1/9 |  | 2 / 1.1 / 0/8 | 3 / 1.0 / 0/5 |
| Dorset |  | 1 / 1.0 / 0/11 | 5 / 3.9 / 2/11 | 0 / 0.2 / 0/9 | 3 / 1.4 / 0/9 | 1 / 3.2 / 0/6 | 0 / 0.0 / 0/8 | 1 / 0.2 / 0/5 |
| Essex |  | 1 / 0.7 / 0/11 | 5 / 2.1 / 0/11 |  | 6 / 2.8 / 1/9 | 4 / 5.7 / 2/6 | 1 / 1.1 / 0/8 | 4 / 2.0 / 0/5 |
| Gloucestershire |  | 0 / 0.2 / 0/11 | 4 / 1.4 / 0/11 | 0 / 0.0 / 0/9 | 8 / 2.9 / 1/9 |  | 2 / 1.2 / 0/8 | 3 / 1.6 / 0/5 |
| Greater Manchester - Manchester & Salford |  | 2 / 1.3 / 0/11 |  | 3 / 3.9 / 2/9 |  | 3 / 3.7 / 0/6 |  | 3 / 2.2 / 0/5 |
| Greater Manchester - North | 3 / 3.1 / 1/11 | 0 / 0.0 / 0/11 | 0 / 0.2 / 0/11 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 | 0 / 0.1 / 0/8 | 1 / 0.2 / 0/5 |
| Greater Manchester - South |  | 0 / 0.8 / 0/11 | 1 / 0.7 / 0/11 | 1 / 0.4 / 0/9 | 2 / 0.2 / 0/9 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/8 | 3 / 0.6 / 0/5 |
| Greater Manchester - Wigan & Bolton |  | 0 / 0.0 / 0/11 | 1 / 0.7 / 0/11 | 1 / 0.3 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.3 / 0/6 | 1 / 1.0 / 0/8 | 1 / 1.0 / 0/5 |
| Hampshire |  |  | 14 / 7.4 / 7/11 | 0 / 1.7 / 0/9 | 10 / 5.0 / 2/9 | 1 / 2.8 / 0/6 | 4 / 3.5 / 0/8 |  |
| Herefordshire | 0 / 1.4 / 0/11 | 0 / 0.2 / 0/11 | 0 / 0.0 / 0/11 | 1 / 0.1 / 0/9 | 0 / 0.0 / 0/9 | 0 / 1.2 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Hertfordshire |  | 3 / 2.3 / 0/11 | 10 / 4.0 / 1/11 | 1 / 1.6 / 0/9 | 9 / 2.1 / 1/9 | 1 / 1.0 / 0/6 | 1 / 0.2 / 0/8 | 4 / 1.6 / 0/5 |
| Kent |  |  | 8 / 4.5 / 1/11 | 3 / 4.3 / 2/9 | 7 / 2.8 / 1/9 | 1 / 3.2 / 1/6 | 2 / 1.6 / 0/8 | 2 / 0.8 / 0/5 |
| Lancashire - Blackpool & Fylde | 1 / 0.8 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/9 | 2 / 0.9 / 0/9 | 1 / 0.3 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Lancashire - Central | 3 / 2.8 / 0/11 | 0 / 0.2 / 0/11 | 1 / 0.3 / 0/11 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 1 / 0.5 / 0/6 | 0 / 0.2 / 0/8 | 0 / 0.0 / 0/5 |
| Lancashire - East | 3 / 2.5 / 0/11 | 0 / 0.7 / 0/11 | 0 / 0.3 / 0/11 | 0 / 0.2 / 0/9 | 3 / 1.1 / 0/9 | 1 / 1.2 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Lancashire - North | 1 / 1.0 / 0/11 | 0 / 1.2 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Lancashire - West | 0 / 1.3 / 0/10 | 0 / 0.1 / 0/10 | 1 / 1.2 / 0/10 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Leicestershire |  | 0 / 0.1 / 0/11 | 3 / 1.6 / 0/11 | 2 / 1.3 / 0/9 | 1 / 0.9 / 0/9 | 2 / 3.0 / 1/6 | 2 / 0.9 / 0/8 | 3 / 3.0 / 0/5 |
| Lincolnshire |  | 0 / 1.7 / 0/11 | 4 / 1.2 / 0/11 | 3 / 1.6 / 0/9 | 3 / 2.7 / 0/9 | 1 / 2.8 / 0/6 | 1 / 1.4 / 0/8 | 2 / 1.0 / 0/5 |
| London |  |  |  |  |  | 10 / 5.2 / 2/6 |  |  |
| Merseyside - Liverpool |  | 0 / 0.4 / 0/11 | 0 / 0.3 / 0/11 | 1 / 0.4 / 0/9 | 6 / 2.0 / 1/9 | 1 / 0.5 / 0/6 | 0 / 0.1 / 0/8 | 0 / 0.0 / 0/5 |
| Merseyside - Sefton | 0 / 0.1 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Merseyside - St Helens & Knowsley | 1 / 2.0 / 0/10 | 0 / 0.0 / 0/10 | 1 / 0.8 / 0/10 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 1 / 1.7 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Merseyside - Wirral | 1 / 1.5 / 0/11 | 0 / 0.5 / 0/11 | 1 / 1.0 / 0/11 | 1 / 0.3 / 0/9 | 3 / 0.6 / 0/9 | 1 / 0.2 / 0/6 | 0 / 0.0 / 0/8 | 1 / 1.0 / 0/5 |
| Norfolk |  | 0 / 1.1 / 0/11 | 0 / 0.7 / 0/11 |  | 2 / 1.6 / 0/9 | 2 / 4.2 / 2/6 | 0 / 0.2 / 0/8 | 1 / 0.8 / 0/5 |
| North East |  |  |  | 0 / 0.9 / 0/9 | 6 / 4.1 / 1/9 |  | 1 / 1.1 / 0/8 | 4 / 2.4 / 0/5 |
| North Scotland | 6 / 5.6 / 4/10 | 0 / 0.0 / 0/10 | 6 / 3.0 / 1/10 | 0 / 0.2 / 0/9 | 0 / 0.0 / 0/9 | 1 / 1.5 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| North Wales - East | 5 / 4.5 / 1/10 | 0 / 0.2 / 0/10 | 1 / 1.3 / 0/10 | 0 / 0.0 / 0/9 | 1 / 0.4 / 0/9 | 1 / 1.5 / 0/6 | 0 / 0.0 / 0/8 | 1 / 1.0 / 0/5 |
| North Wales - West | 3 / 1.8 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 | 1 / 0.2 / 0/8 | 1 / 0.4 / 0/5 |
| Northamptonshire |  | 0 / 0.0 / 0/11 | 11 / 3.6 / 1/11 | 1 / 1.3 / 0/9 | 6 / 2.2 / 1/9 | 2 / 3.3 / 2/6 | 3 / 2.5 / 1/8 | 1 / 0.2 / 0/5 |
| Northern Ireland - East |  | 1 / 1.8 / 0/10 | 0 / 0.0 / 0/10 | 1 / 1.2 / 0/9 | 0 / 0.0 / 0/9 |  | 0 / 0.1 / 0/8 | 1 / 1.0 / 0/5 |
| Northern Ireland - West | 4 / 4.1 / 0/10 | 0 / 0.0 / 0/10 | 3 / 1.0 / 0/10 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.2 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Nottinghamshire |  | 1 / 0.5 / 0/11 | 3 / 1.8 / 0/11 | 2 / 2.1 / 0/9 | 4 / 2.0 / 0/9 | 1 / 3.7 / 2/6 |  | 1 / 1.0 / 0/5 |
| Oxfordshire |  |  | 5 / 3.0 / 0/11 | 2 / 1.7 / 0/9 | 10 / 4.6 / 2/9 | 1 / 2.8 / 0/6 | 1 / 0.2 / 0/8 | 3 / 0.8 / 0/5 |
| Rutland | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/11 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Scotland - Borders | 2 / 1.1 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 1 / 0.2 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Scotland Central - Edinburgh & Lothians |  | 0 / 0.1 / 0/10 | 4 / 2.2 / 0/10 | 4 / 2.4 / 0/9 | 1 / 0.1 / 0/9 | 1 / 1.2 / 0/6 | 1 / 0.4 / 0/8 | 1 / 0.2 / 0/5 |
| Scotland Central - Falkirk & Stirling | 2 / 2.8 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 1 / 1.2 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Scotland Central - Fife | 2 / 1.5 / 0/10 | 0 / 0.0 / 0/10 | 2 / 1.0 / 0/10 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.7 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Scotland Central - Tayside | 5 / 3.8 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.2 / 0/10 | 1 / 1.2 / 0/9 | 0 / 0.2 / 0/9 | 0 / 0.7 / 0/6 | 0 / 0.0 / 0/8 | 1 / 0.2 / 0/5 |
| Scotland West - Ayrshire | 1 / 0.5 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 1 / 0.4 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/8 | 1 / 0.6 / 0/5 |
| Scotland West - Glasgow |  | 0 / 0.0 / 0/10 | 4 / 3.1 / 0/10 | 0 / 0.2 / 0/9 | 0 / 0.2 / 0/9 | 0 / 0.3 / 0/6 | 0 / 0.6 / 0/8 | 3 / 2.4 / 0/5 |
| Scotland West - Lanarkshire | 0 / 0.5 / 0/10 | 0 / 0.1 / 0/10 | 0 / 0.4 / 0/10 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Scotland West - Renfrewshire & Inverclyde | 1 / 1.0 / 0/10 | 0 / 0.0 / 0/10 | 1 / 0.4 / 0/10 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.7 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Shropshire |  | 0 / 1.8 / 0/11 | 0 / 1.1 / 0/11 | 2 / 1.7 / 0/9 | 1 / 0.3 / 0/9 |  | 2 / 1.9 / 0/8 | 0 / 0.0 / 0/5 |
| Somerset |  | 1 / 3.5 / 3/11 | 2 / 1.3 / 0/11 | 1 / 0.3 / 0/9 | 4 / 0.6 / 0/9 | 2 / 3.3 / 1/6 | 0 / 0.1 / 0/8 | 2 / 0.4 / 0/5 |
| Staffordshire |  | 0 / 0.2 / 0/11 | 1 / 1.4 / 0/11 | 0 / 0.0 / 0/9 | 2 / 1.2 / 0/9 | 3 / 2.5 / 0/6 | 0 / 0.1 / 0/8 |  |
| Suffolk |  | 0 / 0.9 / 0/11 | 3 / 1.6 / 0/11 |  | 2 / 0.3 / 0/9 | 1 / 1.8 / 0/6 | 1 / 1.0 / 0/8 | 1 / 0.4 / 0/5 |
| Surrey |  |  | 6 / 4.5 / 4/11 | 5 / 4.0 / 0/9 |  | 5 / 5.2 / 2/6 | 3 / 2.0 / 0/8 |  |
| Sussex |  |  | 7 / 3.6 / 1/11 | 4 / 2.0 / 0/9 | 5 / 2.6 / 0/9 | 4 / 4.2 / 0/6 | 6 / 5.8 / 6/8 | 4 / 2.8 / 0/5 |
| Wales - Mid | 0 / 0.1 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Wales - West | 3 / 1.9 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.7 / 0/6 | 0 / 0.1 / 0/8 | 0 / 0.0 / 0/5 |
| Wales South - Cardiff & Vale | 5 / 4.1 / 1/10 | 0 / 0.0 / 0/10 | 3 / 1.7 / 0/10 | 2 / 1.3 / 0/9 | 2 / 0.9 / 0/9 | 0 / 1.2 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Wales South - Gwent | 1 / 2.7 / 0/10 | 0 / 0.1 / 0/10 | 1 / 0.3 / 0/10 | 2 / 1.3 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.7 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Wales South - Swansea Bay | 1 / 2.9 / 1/10 | 0 / 0.1 / 0/10 | 1 / 1.8 / 0/10 | 1 / 0.7 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.3 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| Wales South - Valleys | 2 / 1.4 / 1/10 | 0 / 0.0 / 0/10 | 0 / 0.3 / 0/10 | 4 / 2.6 / 0/9 | 0 / 0.4 / 0/9 | 0 / 0.2 / 0/6 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 |
| West Midlands - Birmingham & Solihull |  | 1 / 1.0 / 0/11 | 11 / 4.0 / 1/11 | 3 / 3.9 / 2/9 |  | 3 / 2.7 / 0/6 |  | 5 / 3.4 / 0/5 |
| West Midlands - Black Country |  | 1 / 1.1 / 0/11 | 1 / 1.0 / 0/11 | 3 / 1.1 / 0/9 | 1 / 0.4 / 0/9 | 1 / 1.3 / 0/6 | 0 / 0.0 / 0/8 | 1 / 1.0 / 0/5 |
| West Midlands - Coventry & Warwickshire |  | 0 / 0.0 / 0/11 | 6 / 1.3 / 1/11 | 1 / 0.6 / 0/9 | 5 / 2.4 / 0/9 | 3 / 2.2 / 0/6 | 3 / 3.1 / 0/8 | 2 / 0.4 / 0/5 |
| Wiltshire |  |  | 3 / 2.0 / 0/11 | 4 / 3.0 / 0/9 | 3 / 1.1 / 0/9 | 0 / 2.7 / 0/6 | 0 / 0.6 / 0/8 | 1 / 1.0 / 0/5 |
| Worcestershire |  | 0 / 1.3 / 0/11 | 1 / 2.1 / 0/11 | 2 / 0.4 / 0/9 | 3 / 1.6 / 0/9 | 0 / 0.8 / 0/6 | 0 / 0.2 / 0/8 | 1 / 0.4 / 0/5 |
| Yorkshire - East |  | 0 / 0.7 / 0/11 | 0 / 1.2 / 0/11 | 2 / 1.0 / 0/9 | 2 / 0.4 / 0/9 | 2 / 4.0 / 0/6 | 1 / 1.2 / 0/8 | 4 / 2.8 / 0/5 |
| Yorkshire - North |  | 1 / 3.5 / 0/11 | 3 / 0.9 / 0/11 | 0 / 0.1 / 0/9 | 12 / 2.7 / 1/9 |  | 2 / 1.5 / 0/8 | 2 / 1.0 / 0/5 |
| Yorkshire - South |  |  | 4 / 2.0 / 0/11 | 4 / 3.1 / 0/9 | 6 / 2.0 / 1/9 | 0 / 2.3 / 2/6 | 0 / 0.0 / 0/8 | 2 / 1.0 / 0/5 |
| Yorkshire - West |  |  |  | 4 / 4.0 / 0/9 | 15 / 5.4 / 3/9 |  |  | 3 / 2.6 / 0/5 |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Live regions | 47 / 78 | 11 / 78 | 5 / 78 | 4 / 78 | 6 / 78 | 8 / 78 | 6 / 78 | 4 / 78 |
| Live slice placements | 1403 + 1 CHECK | 37 + 1 CHECK | 77 + 1 CHECK | 21 + 1 CHECK | 120 + 1 CHECK | 0 + 8 CHECK | 28 | 36 |

**Live slices: 91 / 624.**
