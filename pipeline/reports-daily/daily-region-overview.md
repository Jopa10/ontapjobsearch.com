# Ontap daily regional overview

Generated: 2026-08-31T21:29:54+01:00

## SITEWIDE RECONCILIATION

| Measure | Count |
|---|---:|
| Unique live jobs | 1,136 |
| Unique JobG8 jobs | 763 |
| Unique non-JobG8 jobs | 373 |
| Regional/category slice placements | 1,161 |
| Jobs appearing on multiple slices | 25 |
| Extra slice placements | 25 |
| Unique jobs outside governed slices | 0 |
| Jobs found in non-LIVE slices | 0 |

**Reconciliation: 1,136 unique jobs + 25 extra slice placements = 1,161 regional/category slice placements.**

Latest source-count CSV: `pipeline/reports-daily/live-job-source-count-2026-08-31.csv` — **STALE — CSV says 1,164 for 2026-08-31**.

### Provider breakdown

| Provider | Unique live jobs | Jobs on 2+ slices | Extra slice placements |
|---|---:|---:|---:|
| JobG8 | 763 | 25 | 25 |
| NEJobs | 30 | 0 | 0 |
| NHS Jobs | 181 | 0 | 0 |
| Teaching Vacancies | 160 | 0 | 0 |
| VONNE | 2 | 0 | 0 |

> LIVE counts come directly from the current published `app/` JSON, deduplicated within each canonical region/family slice while preserving legitimate appearances in more than one family. This is the live-site authority for the reconciliation above; the dated source-count CSV is shown only as a freshness cross-check. The overview covers all 78 assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 78-market coverage has run, NOT LIVE Admin/Support and Customer Service may fall back to the latest all-region Module 2 profile (2026-08-17), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-08-31) used by the production family run, across 78 UK markets with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across 78 UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across 78, 78, 78 and 78 UK markets respectively, using their governed production boundaries and canonical geo. NOT LIVE Customer Service / Contact Centre was assessed from that same feed across 78 UK markets using its governed exact-title, salary and geography rules. All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

## LIVE

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire |  |  |  |  |  |  |  |  |
| Berkshire | 21 |  |  |  | 4 |  | 1 |  |
| Bristol & Bath | 20 |  |  |  |  | CHECK |  |  |
| Buckinghamshire | 22 |  |  |  |  |  |  |  |
| Cambridgeshire | 35 |  |  |  |  |  |  |  |
| Cheshire - East | 8 |  |  |  |  |  |  |  |
| Cheshire - Warrington & Halton | 2 |  |  |  |  |  |  |  |
| Cheshire - West | 5 |  |  |  |  |  |  |  |
| Cornwall | 2 |  |  |  |  |  |  |  |
| Cumbria - North |  |  |  |  |  |  |  |  |
| Cumbria - South |  | CHECK |  |  |  |  |  |  |
| Cumbria - West |  |  |  |  |  |  |  |  |
| Derbyshire | 7 |  |  |  |  |  |  |  |
| Devon | 25 |  |  |  |  | CHECK |  |  |
| Dorset | 10 |  |  |  |  |  |  |  |
| Essex | 34 |  |  | 2 |  |  |  |  |
| Gloucestershire | 16 |  |  |  |  | CHECK |  |  |
| Greater Manchester - Manchester & Salford | 26 |  | 3 |  | 3 |  | 2 |  |
| Greater Manchester - North |  |  |  |  |  |  |  |  |
| Greater Manchester - South | 7 |  |  |  |  |  |  |  |
| Greater Manchester - Wigan & Bolton | 5 |  |  |  |  |  |  |  |
| Hampshire | 56 | 6 |  |  |  |  |  | 3 |
| Herefordshire |  |  |  |  |  |  |  |  |
| Hertfordshire | 26 |  |  |  |  |  |  |  |
| Kent | 43 | 1 |  |  |  |  |  |  |
| Lancashire - Blackpool & Fylde |  |  |  |  |  |  |  |  |
| Lancashire - Central |  |  |  |  |  |  |  |  |
| Lancashire - East |  |  |  |  |  |  |  |  |
| Lancashire - North |  |  |  |  |  |  |  |  |
| Lancashire - West |  |  |  |  |  |  |  |  |
| Leicestershire | 33 |  |  |  |  |  |  |  |
| Lincolnshire | 12 |  |  |  |  |  |  |  |
| London | 121 | 10 | 10 | 7 | 21 |  | 6 | 3 |
| Merseyside - Liverpool | 8 |  |  |  |  |  |  |  |
| Merseyside - Sefton |  |  |  |  |  |  |  |  |
| Merseyside - St Helens & Knowsley |  |  |  |  |  |  |  |  |
| Merseyside - Wirral |  |  |  |  |  |  |  |  |
| Norfolk | 20 |  |  | CHECK |  |  |  |  |
| North East | 63 | 1 | CHECK |  |  | CHECK |  |  |
| North Scotland |  |  |  |  |  |  |  |  |
| North Wales - East |  |  |  |  |  |  |  |  |
| North Wales - West |  |  |  |  |  |  |  |  |
| Northamptonshire | 20 |  |  |  |  |  |  |  |
| Northern Ireland - East | 3 |  |  |  |  | CHECK |  |  |
| Northern Ireland - West |  |  |  |  |  |  |  |  |
| Nottinghamshire | 18 |  |  |  |  |  | 2 |  |
| Oxfordshire | 33 | 5 |  |  |  |  |  |  |
| Rutland |  |  |  |  |  |  |  |  |
| Scotland - Borders |  |  |  |  |  |  |  |  |
| Scotland Central - Edinburgh & Lothians | 5 |  |  |  |  |  |  |  |
| Scotland Central - Falkirk & Stirling |  |  |  |  |  |  |  |  |
| Scotland Central - Fife |  |  |  |  |  |  |  |  |
| Scotland Central - Tayside |  |  |  |  |  |  |  |  |
| Scotland West - Ayrshire |  |  |  |  |  |  |  |  |
| Scotland West - Glasgow | 13 |  |  |  |  |  |  |  |
| Scotland West - Lanarkshire |  |  |  |  |  |  |  |  |
| Scotland West - Renfrewshire & Inverclyde |  |  |  |  |  |  |  |  |
| Shropshire | 8 |  |  |  |  | CHECK |  |  |
| Somerset | 12 |  |  |  |  |  |  |  |
| Staffordshire | 23 |  |  |  |  |  |  | 3 |
| Suffolk | 11 |  |  | CHECK |  |  |  |  |
| Surrey | 55 | 3 |  |  | 5 |  |  | 7 |
| Sussex | 33 | 1 |  |  |  |  |  |  |
| Wales - Mid |  |  |  |  |  |  |  |  |
| Wales - West |  |  |  |  |  |  |  |  |
| Wales South - Cardiff & Vale |  |  |  |  |  |  |  |  |
| Wales South - Gwent |  |  |  |  |  |  |  |  |
| Wales South - Swansea Bay |  |  |  |  |  |  |  |  |
| Wales South - Valleys |  |  |  |  |  |  |  |  |
| West Midlands - Birmingham & Solihull | 28 |  |  |  | 3 |  | 3 |  |
| West Midlands - Black Country | 11 |  |  |  |  |  |  |  |
| West Midlands - Coventry & Warwickshire | 23 |  |  |  |  |  |  |  |
| Wiltshire | 15 | 3 |  |  |  |  |  |  |
| Worcestershire | 8 |  |  |  |  |  |  |  |
| Yorkshire - East | 12 |  |  |  |  |  |  |  |
| Yorkshire - North | 10 |  |  |  |  | CHECK |  |  |
| Yorkshire - South | 31 | CHECK |  |  |  |  |  |  |
| Yorkshire - West | 40 | 1 | CHECK |  |  | CHECK | 3 |  |

## NOT LIVE

> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire | 7 / 5.7 / 5/10 | 0 / 0.2 / 0/10 | 2 / 2.2 / 0/10 | 2 / 3.8 / 0/8 | 1 / 1.1 / 0/8 | 0 / 0.6 / 0/5 | 0 / 1.0 / 0/7 | 1 / 1.0 / 0/4 |
| Berkshire |  | 3 / 3.9 / 3/10 | 1 / 1.2 / 0/10 | 0 / 0.5 / 0/8 |  | 0 / 0.2 / 0/5 |  | 0 / 0.0 / 0/4 |
| Bristol & Bath |  | 0 / 1.0 / 0/10 | 2 / 6.4 / 8/10 | 0 / 2.9 / 1/8 | 0 / 2.0 / 0/8 |  | 1 / 1.7 / 0/7 | 1 / 1.2 / 0/4 |
| Buckinghamshire |  | 0 / 0.8 / 0/10 | 0 / 0.6 / 0/10 | 0 / 1.0 / 0/8 | 1 / 3.0 / 1/8 | 1 / 2.2 / 0/5 | 0 / 0.7 / 0/7 | 2 / 1.5 / 0/4 |
| Cambridgeshire |  | 0 / 0.1 / 0/10 | 0 / 2.5 / 0/10 | 0 / 1.2 / 0/8 | 0 / 2.1 / 0/8 | 1 / 4.8 / 2/5 | 0 / 0.1 / 0/7 | 1 / 1.0 / 0/4 |
| Cheshire - East |  | 0 / 0.7 / 0/10 | 0 / 1.4 / 0/10 | 0 / 0.2 / 0/8 | 0 / 0.8 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/7 | 1 / 1.5 / 0/4 |
| Cheshire - Warrington & Halton |  | 1 / 1.4 / 0/10 | 0 / 1.7 / 0/10 | 1 / 1.2 / 0/8 | 0 / 0.2 / 0/8 | 2 / 4.2 / 1/5 | 0 / 0.1 / 0/7 | 0 / 0.0 / 0/4 |
| Cheshire - West |  | 0 / 1.6 / 0/10 | 0 / 2.2 / 0/10 | 1 / 0.9 / 0/8 | 0 / 1.8 / 0/8 | 0 / 2.4 / 0/5 | 0 / 0.1 / 0/7 | 0 / 0.0 / 0/4 |
| Cornwall |  | 0 / 1.6 / 0/10 | 0 / 0.5 / 0/10 | 0 / 0.0 / 0/8 | 0 / 0.2 / 0/8 | 0 / 0.4 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Cumbria - North | 1 / 1.7 / 0/10 | 0 / 3.1 / 3/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.2 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Cumbria - South | 0 / 1.1 / 0/10 |  | 0 / 0.7 / 0/10 | 0 / 0.0 / 0/8 | 0 / 0.4 / 0/8 | 0 / 0.8 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Cumbria - West | 1 / 1.9 / 0/10 | 0 / 0.8 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.6 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Derbyshire |  | 0 / 0.4 / 0/10 | 2 / 2.4 / 0/10 | 0 / 0.4 / 0/8 | 0 / 0.8 / 0/8 | 2 / 3.4 / 0/5 | 0 / 0.0 / 0/7 | 1 / 1.0 / 0/4 |
| Devon |  | 0 / 0.1 / 0/10 | 1 / 3.0 / 0/10 | 1 / 2.0 / 0/8 | 1 / 0.6 / 0/8 |  | 0 / 1.0 / 0/7 | 0 / 0.5 / 0/4 |
| Dorset |  | 0 / 1.0 / 0/10 | 0 / 3.8 / 2/10 | 0 / 0.2 / 0/8 | 2 / 1.2 / 0/8 | 0 / 3.6 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Essex |  | 0 / 0.7 / 0/10 | 1 / 1.8 / 0/10 |  | 1 / 2.4 / 0/8 | 2 / 6.0 / 2/5 | 1 / 1.1 / 0/7 | 2 / 1.5 / 0/4 |
| Gloucestershire |  | 0 / 0.2 / 0/10 | 0 / 1.1 / 0/10 | 0 / 0.0 / 0/8 | 1 / 2.2 / 0/8 |  | 0 / 1.1 / 0/7 | 1 / 1.2 / 0/4 |
| Greater Manchester - Manchester & Salford |  | 1 / 1.2 / 0/10 |  | 2 / 4.0 / 2/8 |  | 3 / 3.8 / 0/5 |  | 2 / 2.0 / 0/4 |
| Greater Manchester - North | 2 / 3.1 / 1/10 | 0 / 0.0 / 0/10 | 0 / 0.2 / 0/10 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.1 / 0/7 | 0 / 0.0 / 0/4 |
| Greater Manchester - South |  | 0 / 0.9 / 0/10 | 0 / 0.7 / 0/10 | 0 / 0.4 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Greater Manchester - Wigan & Bolton |  | 0 / 0.0 / 0/10 | 0 / 0.7 / 0/10 | 0 / 0.2 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.4 / 0/5 | 1 / 1.0 / 0/7 | 1 / 1.0 / 0/4 |
| Hampshire |  |  | 4 / 6.7 / 6/10 | 0 / 1.9 / 0/8 | 4 / 4.4 / 1/8 | 0 / 3.2 / 0/5 | 3 / 3.4 / 0/7 |  |
| Herefordshire | 1 / 1.5 / 0/10 | 0 / 0.2 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 1.4 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Hertfordshire |  | 0 / 2.2 / 0/10 | 2 / 3.4 / 0/10 | 1 / 1.6 / 0/8 | 0 / 1.2 / 0/8 | 1 / 1.0 / 0/5 | 0 / 0.1 / 0/7 | 0 / 1.0 / 0/4 |
| Kent |  |  | 1 / 4.2 / 0/10 | 0 / 4.5 / 2/8 | 1 / 2.2 / 0/8 | 1 / 3.6 / 1/5 | 1 / 1.6 / 0/7 | 1 / 0.5 / 0/4 |
| Lancashire - Blackpool & Fylde | 0 / 0.8 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/8 | 0 / 0.8 / 0/8 | 0 / 0.2 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Lancashire - Central | 2 / 2.8 / 0/10 | 0 / 0.2 / 0/10 | 0 / 0.2 / 0/10 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.4 / 0/5 | 0 / 0.3 / 0/7 | 0 / 0.0 / 0/4 |
| Lancashire - East | 1 / 2.4 / 0/10 | 0 / 0.8 / 0/10 | 0 / 0.3 / 0/10 | 0 / 0.2 / 0/8 | 0 / 0.9 / 0/8 | 0 / 1.2 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Lancashire - North | 1 / 1.0 / 0/10 | 0 / 1.3 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Lancashire - West | 0 / 1.4 / 0/9 | 0 / 0.1 / 0/9 | 0 / 1.2 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Leicestershire |  | 0 / 0.1 / 0/10 | 0 / 1.5 / 0/10 | 1 / 1.2 / 0/8 | 0 / 0.9 / 0/8 | 1 / 3.2 / 1/5 | 0 / 0.7 / 0/7 | 3 / 3.0 / 0/4 |
| Lincolnshire |  | 0 / 1.9 / 0/10 | 0 / 0.9 / 0/10 | 1 / 1.4 / 0/8 | 2 / 2.6 / 0/8 | 1 / 3.2 / 0/5 | 1 / 1.4 / 0/7 | 0 / 0.8 / 0/4 |
| London |  |  |  |  |  | 0 / 4.2 / 1/5 |  |  |
| Merseyside - Liverpool |  | 0 / 0.4 / 0/10 | 0 / 0.3 / 0/10 | 0 / 0.4 / 0/8 | 1 / 1.5 / 0/8 | 0 / 0.4 / 0/5 | 0 / 0.1 / 0/7 | 0 / 0.0 / 0/4 |
| Merseyside - Sefton | 0 / 0.1 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Merseyside - St Helens & Knowsley | 0 / 2.1 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.8 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 1 / 1.8 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Merseyside - Wirral | 1 / 1.6 / 0/10 | 0 / 0.5 / 0/10 | 1 / 1.0 / 0/10 | 0 / 0.2 / 0/8 | 0 / 0.2 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/7 | 1 / 1.0 / 0/4 |
| Norfolk |  | 0 / 1.2 / 0/10 | 0 / 0.8 / 0/10 |  | 1 / 1.5 / 0/8 | 1 / 4.6 / 2/5 | 0 / 0.3 / 0/7 | 0 / 0.8 / 0/4 |
| North East |  |  |  | 0 / 1.0 / 0/8 | 2 / 3.9 / 0/8 |  | 1 / 1.1 / 0/7 | 2 / 2.0 / 0/4 |
| North Scotland | 3 / 5.6 / 3/9 | 0 / 0.0 / 0/9 | 0 / 2.7 / 0/9 | 0 / 0.2 / 0/8 | 0 / 0.0 / 0/8 | 0 / 1.6 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| North Wales - East | 3 / 4.4 / 1/9 | 0 / 0.2 / 0/9 | 0 / 1.3 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.4 / 0/8 | 0 / 1.6 / 0/5 | 0 / 0.0 / 0/7 | 1 / 1.0 / 0/4 |
| North Wales - West | 1 / 1.7 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.1 / 0/7 | 0 / 0.2 / 0/4 |
| Northamptonshire |  | 0 / 0.0 / 0/10 | 1 / 2.9 / 0/10 | 1 / 1.4 / 0/8 | 1 / 1.8 / 0/8 | 1 / 3.6 / 2/5 | 1 / 2.4 / 1/7 | 0 / 0.0 / 0/4 |
| Northern Ireland - East |  | 1 / 1.9 / 0/9 | 0 / 0.0 / 0/9 | 1 / 1.2 / 0/8 | 0 / 0.0 / 0/8 |  | 0 / 0.1 / 0/7 | 1 / 1.0 / 0/4 |
| Northern Ireland - West | 3 / 4.1 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.8 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.2 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Nottinghamshire |  | 0 / 0.5 / 0/10 | 0 / 1.7 / 0/10 | 1 / 2.1 / 0/8 | 1 / 1.8 / 0/8 | 1 / 4.2 / 2/5 |  | 1 / 1.0 / 0/4 |
| Oxfordshire |  |  | 0 / 2.8 / 0/10 | 0 / 1.6 / 0/8 | 1 / 3.9 / 1/8 | 1 / 3.2 / 0/5 | 0 / 0.1 / 0/7 | 0 / 0.2 / 0/4 |
| Rutland | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/10 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Scotland - Borders | 1 / 1.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Scotland Central - Edinburgh & Lothians |  | 0 / 0.1 / 0/9 | 0 / 2.0 / 0/9 | 0 / 2.2 / 0/8 | 0 / 0.0 / 0/8 | 0 / 1.2 / 0/5 | 0 / 0.3 / 0/7 | 0 / 0.0 / 0/4 |
| Scotland Central - Falkirk & Stirling | 2 / 2.9 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 1 / 1.2 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Scotland Central - Fife | 1 / 1.4 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.9 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.8 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Scotland Central - Tayside | 2 / 3.7 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.2 / 0/9 | 2 / 1.2 / 0/8 | 1 / 0.2 / 0/8 | 0 / 0.8 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Scotland West - Ayrshire | 0 / 0.4 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.4 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/7 | 1 / 0.5 / 0/4 |
| Scotland West - Glasgow |  | 0 / 0.0 / 0/9 | 2 / 3.0 / 0/9 | 0 / 0.2 / 0/8 | 0 / 0.2 / 0/8 | 0 / 0.4 / 0/5 | 0 / 0.7 / 0/7 | 2 / 2.2 / 0/4 |
| Scotland West - Lanarkshire | 0 / 0.6 / 0/9 | 0 / 0.1 / 0/9 | 0 / 0.4 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Scotland West - Renfrewshire & Inverclyde | 1 / 1.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.3 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.8 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Shropshire |  | 0 / 2.0 / 0/10 | 0 / 1.2 / 0/10 | 1 / 1.6 / 0/8 | 0 / 0.2 / 0/8 |  | 2 / 1.9 / 0/7 | 0 / 0.0 / 0/4 |
| Somerset |  | 0 / 3.8 / 3/10 | 1 / 1.2 / 0/10 | 0 / 0.2 / 0/8 | 0 / 0.1 / 0/8 | 1 / 3.6 / 1/5 | 0 / 0.1 / 0/7 | 0 / 0.0 / 0/4 |
| Staffordshire |  | 0 / 0.2 / 0/10 | 0 / 1.4 / 0/10 | 0 / 0.0 / 0/8 | 0 / 1.1 / 0/8 | 2 / 2.4 / 0/5 | 0 / 0.1 / 0/7 |  |
| Suffolk |  | 0 / 1.0 / 0/10 | 0 / 1.5 / 0/10 |  | 1 / 0.1 / 0/8 | 0 / 2.0 / 0/5 | 1 / 1.0 / 0/7 | 0 / 0.2 / 0/4 |
| Surrey |  |  | 1 / 4.3 / 3/10 | 2 / 3.9 / 0/8 |  | 4 / 5.2 / 2/5 | 2 / 1.9 / 0/7 |  |
| Sussex |  |  | 3 / 3.3 / 0/10 | 1 / 1.8 / 0/8 | 2 / 2.2 / 0/8 | 3 / 4.2 / 0/5 | 5 / 5.7 / 5/7 | 3 / 2.5 / 0/4 |
| Wales - Mid | 0 / 0.1 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Wales - West | 2 / 1.8 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/9 | 0 / 0.0 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.8 / 0/5 | 0 / 0.1 / 0/7 | 0 / 0.0 / 0/4 |
| Wales South - Cardiff & Vale | 3 / 4.0 / 1/9 | 0 / 0.0 / 0/9 | 0 / 1.6 / 0/9 | 0 / 1.2 / 0/8 | 0 / 0.8 / 0/8 | 0 / 1.4 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Wales South - Gwent | 2 / 2.9 / 0/9 | 0 / 0.1 / 0/9 | 0 / 0.2 / 0/9 | 0 / 1.2 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.8 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Wales South - Swansea Bay | 3 / 3.1 / 1/9 | 0 / 0.1 / 0/9 | 0 / 1.9 / 0/9 | 0 / 0.6 / 0/8 | 0 / 0.0 / 0/8 | 0 / 0.4 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| Wales South - Valleys | 1 / 1.3 / 1/9 | 0 / 0.0 / 0/9 | 0 / 0.3 / 0/9 | 0 / 2.4 / 0/8 | 0 / 0.5 / 0/8 | 0 / 0.2 / 0/5 | 0 / 0.0 / 0/7 | 0 / 0.0 / 0/4 |
| West Midlands - Birmingham & Solihull |  | 0 / 1.0 / 0/10 | 3 / 3.3 / 0/10 | 1 / 4.0 / 2/8 |  | 2 / 2.6 / 0/5 |  | 3 / 3.0 / 0/4 |
| West Midlands - Black Country |  | 0 / 1.1 / 0/10 | 1 / 1.0 / 0/10 | 0 / 0.9 / 0/8 | 0 / 0.4 / 0/8 | 1 / 1.4 / 0/5 | 0 / 0.0 / 0/7 | 1 / 1.0 / 0/4 |
| West Midlands - Coventry & Warwickshire |  | 0 / 0.0 / 0/10 | 1 / 0.8 / 0/10 | 0 / 0.5 / 0/8 | 1 / 2.1 / 0/8 | 0 / 2.0 / 0/5 | 2 / 3.1 / 0/7 | 0 / 0.0 / 0/4 |
| Wiltshire |  |  | 0 / 1.9 / 0/10 | 0 / 2.9 / 0/8 | 0 / 0.9 / 0/8 | 0 / 3.2 / 0/5 | 0 / 0.7 / 0/7 | 1 / 1.0 / 0/4 |
| Worcestershire |  | 0 / 1.4 / 0/10 | 0 / 2.2 / 0/10 | 0 / 0.2 / 0/8 | 1 / 1.4 / 0/8 | 0 / 1.0 / 0/5 | 0 / 0.3 / 0/7 | 0 / 0.2 / 0/4 |
| Yorkshire - East |  | 0 / 0.8 / 0/10 | 0 / 1.3 / 0/10 | 0 / 0.9 / 0/8 | 0 / 0.2 / 0/8 | 2 / 4.4 / 0/5 | 1 / 1.3 / 0/7 | 2 / 2.5 / 0/4 |
| Yorkshire - North |  | 1 / 3.8 / 0/10 | 0 / 0.7 / 0/10 | 0 / 0.1 / 0/8 | 0 / 1.5 / 0/8 |  | 1 / 1.4 / 0/7 | 1 / 0.8 / 0/4 |
| Yorkshire - South |  |  | 0 / 1.8 / 0/10 | 3 / 3.0 / 0/8 | 0 / 1.5 / 0/8 | 0 / 2.8 / 2/5 | 0 / 0.0 / 0/7 | 0 / 0.8 / 0/4 |
| Yorkshire - West |  |  |  | 3 / 4.0 / 0/8 | 0 / 4.2 / 2/8 |  |  | 3 / 2.5 / 0/4 |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Live regions | 46 / 78 | 11 / 78 | 4 / 78 | 4 / 78 | 5 / 78 | 8 / 78 | 6 / 78 | 4 / 78 |
| Live slice placements | 1039 | 31 + 2 CHECK | 13 + 2 CHECK | 9 + 2 CHECK | 36 | 0 + 8 CHECK | 17 | 16 |

**Live slices: 88 / 624.**
