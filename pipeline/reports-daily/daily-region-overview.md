# Ontap daily regional overview

Production source commit: `895b2099fd25b6b54f928459eb88f46ecdc13fce`

Generated: 2026-10-29T08:58:35+00:00

[Download this overview as Excel](./daily-region-overview.xlsx)

## SITEWIDE RECONCILIATION

| Measure | Count |
|---|---:|
| Unique live jobs | 3,984 |
| Unique JobG8 jobs | 3,442 |
| Unique non-JobG8 jobs | 542 |
| Regional/category slice placements | 4,734 |
| Jobs appearing on multiple slices | 738 |
| Extra slice placements | 750 |
| Unique jobs outside governed slices | 0 |
| Jobs found in non-LIVE slices | 0 |

**Reconciliation: 3,984 unique jobs + 750 extra slice placements = 4,734 regional/category slice placements.**

Latest source-count CSV: `pipeline/reports-daily/live-job-source-count-2026-10-29.csv` — **STALE — CSV says 4,083 for 2026-10-29**.

### Provider breakdown

| Provider | Unique live jobs | Jobs on 2+ slices | Extra slice placements |
|---|---:|---:|---:|
| JobG8 | 3,442 | 738 | 750 |
| NHS Jobs | 336 | 0 | 0 |
| Teaching Vacancies | 206 | 0 | 0 |

## JOBG8 FEED RECEIVED

**JobG8 jobs received: 20,000** (feed date: 2026-10-29)

| JobG8 classification | Jobs received | Ontap jobs classified/published |
|---|---:|---:|
| Accounting | 3,182 | 698 |
| Sales & Marketing | 3,155 | 629 |
| Administration | 1,873 | 1,000 |
| Legal | 1,803 | 254 |
| I.T. & Communications | 1,495 | 11 |
| HR / Recruitment | 1,411 | 190 |
| Real Estate & Property | 1,207 | 70 |
| Education | 1,057 | 6 |
| Healthcare & Medical | 998 | 107 |
| Transport & Logistics | 926 | 39 |
| Call Centre / CustomerService | 889 | 355 |
| Insurance & Superannuation | 542 | 21 |
| Banking & Financial Services | 526 | 16 |
| Community & Sport | 500 | 50 |
| Government & Defence | 260 | 6 |
| Advert / Media / Entertainment | 176 | 27 |
| Total across classifications | 20,000 | 3,479 |

## JOBG8 XML RECONCILIATION

| Check | XML feed total | Sum of ‘Jobs received’ | Difference (sum − XML) | Result |
|---|---:|---:|---:|---|
| JobG8 feed categories | 20,000 | 20,000 | 0 | **PASS** |

**JobG8 feed reconciliation: PASS.** Difference is 0 jobs (summed categories minus XML total).

## JOBG8 LAST 10 FEED DATES — TOTALS ONLY

Saved history contains 10 of the latest 10 feed dates. Older feed totals were not saved and are not backfilled.

| Feed date | JobG8 jobs received | Ontap jobs classified/published |
|---|---:|---:|
| 2026-10-29 | 20,000 | 3,479 |
| 2026-10-28 | 20,000 | 3,580 |
| 2026-10-27 | 20,000 | 3,662 |
| 2026-10-26 | 20,000 | 3,695 |
| 2026-10-25 | 20,000 | 3,633 |
| 2026-10-24 | 20,000 | 3,887 |
| 2026-10-23 | 20,000 | 3,914 |
| 2026-10-22 | 20,000 | 3,910 |
| 2026-10-21 | 20,000 | 3,902 |
| 2026-10-20 | 20,000 | 3,876 |

## JOBG8 LAST 10 FEED DATES — SELECTED JOBS BY CLASSIFICATION

Each dated column shows Ontap jobs classified/published in that JobG8 classification.

| JobG8 classification | 2026-10-29 | 2026-10-28 | 2026-10-27 | 2026-10-26 | 2026-10-25 | 2026-10-24 | 2026-10-23 | 2026-10-22 | 2026-10-21 | 2026-10-20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Accounting | 698 | 744 | 805 | 850 | 815 | 906 | 916 | 918 | 928 | 941 |
| Administration | 1000 | 1024 | 1026 | 1015 | 1000 | 1110 | 1126 | 1152 | 1118 | 1101 |
| Advert / Media / Entertainment | 27 | 27 | 28 | 26 | 27 | 28 | 25 | 24 | 23 | 18 |
| Banking & Financial Services | 16 | 17 | 18 | 18 | 17 | 17 | 18 | 18 | 17 | 12 |
| Call Centre / CustomerService | 355 | 340 | 346 | 342 | 337 | 354 | 378 | 371 | 369 | 370 |
| Community & Sport | 50 | 47 | 47 | 47 | 46 | 44 | 44 | 40 | 46 | 47 |
| Education | 6 | 6 | 7 | 7 | 7 | 7 | 8 | 8 | 9 | 9 |
| Government & Defence | 6 | 6 | 6 | 6 | 6 | 6 | 7 | 7 | 6 | 5 |
| Healthcare & Medical | 107 | 109 | 108 | 101 | 100 | 100 | 98 | 93 | 88 | 85 |
| HR / Recruitment | 190 | 184 | 181 | 187 | 177 | 185 | 183 | 187 | 186 | 188 |
| I.T. & Communications | 11 | 10 | 10 | 9 | 9 | 9 | 9 | 7 | 8 | 8 |
| Insurance & Superannuation | 21 | 19 | 23 | 24 | 24 | 25 | 22 | 23 | 22 | 23 |
| Legal | 254 | 305 | 303 | 294 | 293 | 293 | 282 | 273 | 268 | 252 |
| Real Estate & Property | 70 | 71 | 68 | 72 | 71 | 72 | 67 | 66 | 70 | 68 |
| Sales & Marketing | 629 | 635 | 650 | 660 | 667 | 688 | 688 | 686 | 710 | 721 |
| Transport & Logistics | 39 | 36 | 36 | 37 | 37 | 43 | 43 | 37 | 34 | 28 |

## PAGES

**Published/indexable URLs: 4,297** — 3,984 individual job pages, 217 regional/category pages, 88 city pages and 8 core pages.

| Level | Page type | Area | Family | URL | Page count | Live jobs | In sitemap |
|---|---|---|---|---|---:|---:|---|
| Summary | All published/indexable URLs | Sitewide |  |  | 4,297 |  | Yes |
| Summary | Individual job | Sitewide |  | /jobs/[id] | 3,984 | 3,984 | Yes |
| Summary | Regional/category | Sitewide |  | Multiple | 217 |  | Yes |
| Summary | City | Sitewide |  | Multiple | 88 |  | Yes |
| Summary | Core | Sitewide |  | Multiple | 8 |  | Yes |
| Detail | Core | Sitewide |  | / | 1 |  | Yes |
| Detail | Core | Sitewide |  | /browse-jobs | 1 |  | Yes |
| Detail | Core | Sitewide |  | /about | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | Ai At Work | /ai-at-work | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | Ai Job Advert Watch | /ai-at-work/ai-job-advert-watch | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | October 2026 | /ai-at-work/ai-job-advert-watch/october-2026 | 1 |  | Yes |
| Detail | Core | Sitewide |  | /ai-tips | 1 |  | Yes |
| Detail | Regional/category | Ai Course Reviews | Ai Course Reviews | /ai-course-reviews | 1 |  | Yes |
| Detail | Core | Sitewide |  | /contact | 1 |  | Yes |
| Detail | Core | Sitewide |  | /privacy-policy | 1 |  | Yes |
| Detail | Core | Sitewide |  | /terms-of-service | 1 |  | Yes |
| Detail | Core | Sitewide |  | /sector-switching | 1 |  | Yes |
| Detail | Regional/category | West Yorkshire | Support Worker | /west-yorkshire/support-worker | 1 | 0 | Yes |
| Detail | Regional/category | South Yorkshire | Support Worker | /south-yorkshire/support-worker | 1 | 1 | Yes |
| Detail | Regional/category | North East | Support Worker | /north-east/support-worker | 1 | 2 | Yes |
| Detail | Regional/category | Sussex | Support Worker | /sussex/support-worker | 1 | 19 | Yes |
| Detail | Regional/category | Cumbria South | Support Worker | /cumbria-south/support-worker | 1 | 2 | Yes |
| Detail | Regional/category | Hampshire | Support Worker | /hampshire/support-worker | 1 | 14 | Yes |
| Detail | Regional/category | West Yorkshire | Service Administrator Jobs | /west-yorkshire/service-administrator-jobs | 1 | 118 | Yes |
| Detail | Regional/category | South Yorkshire | Service Administrator Jobs | /south-yorkshire/service-administrator-jobs | 1 | 55 | Yes |
| Detail | Regional/category | North Yorkshire | Service Administrator Jobs | /north-yorkshire/service-administrator-jobs | 1 | 36 | Yes |
| Detail | Regional/category | North East | Service Administrator Jobs | /north-east/service-administrator-jobs | 1 | 71 | Yes |
| Detail | Regional/category | London | Service Administrator Jobs | /london/service-administrator-jobs | 1 | 344 | Yes |
| Detail | Regional/category | London | Central Service Administrator Jobs | /london/central-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | North Service Administrator Jobs | /london/north-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | East Service Administrator Jobs | /london/east-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | South Service Administrator Jobs | /london/south-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | West Service Administrator Jobs | /london/west-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | Hampshire | Service Administrator Jobs | /hampshire/service-administrator-jobs | 1 | 118 | Yes |
| Detail | Regional/category | Coventry Warwickshire | Service Administrator Jobs | /coventry-warwickshire/service-administrator-jobs | 1 | 78 | Yes |
| Detail | Regional/category | Surrey | Service Administrator Jobs | /surrey/service-administrator-jobs | 1 | 101 | Yes |
| Detail | Regional/category | Kent | Service Administrator Jobs | /kent/service-administrator-jobs | 1 | 102 | Yes |
| Detail | Regional/category | Sussex | Service Administrator Jobs | /sussex/service-administrator-jobs | 1 | 80 | Yes |
| Detail | City | Newcastle | admin and office jobs | /newcastle/service-administrator-jobs | 1 | 26 | Yes |
| Detail | City | Southampton | support worker jobs | /southampton/support-worker | 1 | 0 | Yes |
| Detail | City | Sheffield | admin and office jobs | /sheffield/service-administrator-jobs | 1 | 24 | Yes |
| Detail | City | Leeds | admin and office jobs | /leeds/service-administrator-jobs | 1 | 83 | Yes |
| Detail | City | Coventry | admin and office jobs | /coventry/service-administrator-jobs | 1 | 21 | Yes |
| Detail | City | Southampton | admin and office jobs | /southampton/service-administrator-jobs | 1 | 11 | Yes |
| Detail | City | Brighton & Hove | admin and office jobs | /brighton-hove/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Bradford | admin and office jobs | /bradford/service-administrator-jobs | 1 | 25 | Yes |
| Detail | City | Huddersfield | admin and office jobs | /huddersfield/service-administrator-jobs | 1 | 12 | Yes |
| Detail | City | York | admin and office jobs | /york/service-administrator-jobs | 1 | 12 | Yes |
| Detail | City | Barnsley | admin and office jobs | /barnsley/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Doncaster | admin and office jobs | /doncaster/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Bristol | admin and office jobs | /bristol/service-administrator-jobs | 1 | 58 | Yes |
| Detail | City | Manchester | admin and office jobs | /manchester/service-administrator-jobs | 1 | 118 | Yes |
| Detail | City | Cambridge | admin and office jobs | /cambridge/service-administrator-jobs | 1 | 35 | Yes |
| Detail | City | Birmingham | admin and office jobs | /birmingham/service-administrator-jobs | 1 | 94 | Yes |
| Detail | City | Peterborough | admin and office jobs | /peterborough/service-administrator-jobs | 1 | 21 | Yes |
| Detail | City | Warrington | admin and office jobs | /warrington/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Liverpool | admin and office jobs | /liverpool/service-administrator-jobs | 1 | 32 | Yes |
| Detail | City | Hull | admin and office jobs | /hull/service-administrator-jobs | 1 | 21 | Yes |
| Detail | City | Oxford | admin and office jobs | /oxford/service-administrator-jobs | 1 | 11 | Yes |
| Detail | City | Belfast | admin and office jobs | /belfast/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Glasgow | admin and office jobs | /glasgow/service-administrator-jobs | 1 | 37 | Yes |
| Detail | City | Edinburgh | admin and office jobs | /edinburgh/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Cardiff | admin and office jobs | /cardiff/service-administrator-jobs | 1 | 21 | Yes |
| Detail | City | Exeter | admin and office jobs | /exeter/service-administrator-jobs | 1 | 21 | Yes |
| Detail | City | Milton Keynes | admin and office jobs | /milton-keynes/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Farnham | admin and office jobs | /farnham/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Northampton | admin and office jobs | /northampton/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Poole | admin and office jobs | /poole/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Portsmouth | admin and office jobs | /portsmouth/service-administrator-jobs | 1 | 17 | Yes |
| Detail | City | Stoke-on-trent | admin and office jobs | /stoke-on-trent/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Hemel Hempstead | admin and office jobs | /hemel-hempstead/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Basingstoke | admin and office jobs | /basingstoke/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Chelmsford | admin and office jobs | /chelmsford/service-administrator-jobs | 1 | 13 | Yes |
| Detail | City | Gloucester | admin and office jobs | /gloucester/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Leicester | admin and office jobs | /leicester/service-administrator-jobs | 1 | 14 | Yes |
| Detail | City | Maidstone | admin and office jobs | /maidstone/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Newtownabbey | admin and office jobs | /newtownabbey/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Plymouth | admin and office jobs | /plymouth/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Sunderland | admin and office jobs | /sunderland/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Worcester | admin and office jobs | /worcester/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Altrincham | admin and office jobs | /altrincham/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Ashford | admin and office jobs | /ashford/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Aylesbury | admin and office jobs | /aylesbury/service-administrator-jobs | 1 | 11 | Yes |
| Detail | City | Bedford | admin and office jobs | /bedford/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Bournemouth | admin and office jobs | /bournemouth/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Chester Le Street | admin and office jobs | /chester-le-street/service-administrator-jobs | 1 | 1 | Yes |
| Detail | City | Macclesfield | admin and office jobs | /macclesfield/service-administrator-jobs | 1 | 3 | Yes |
| Detail | City | Rotherham | admin and office jobs | /rotherham/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Scarborough | admin and office jobs | /scarborough/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Shrewsbury | admin and office jobs | /shrewsbury/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Warwick | admin and office jobs | /warwick/service-administrator-jobs | 1 | 17 | Yes |
| Detail | City | Wigston | admin and office jobs | /wigston/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Dartford | admin and office jobs | /dartford/service-administrator-jobs | 1 | 14 | Yes |
| Detail | City | Stockport | admin and office jobs | /stockport/service-administrator-jobs | 1 | 14 | Yes |
| Detail | City | Swansea | admin and office jobs | /swansea/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Walsall | admin and office jobs | /walsall/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Bath | admin and office jobs | /bath/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Eastleigh | admin and office jobs | /eastleigh/service-administrator-jobs | 1 | 3 | Yes |
| Detail | City | Harrogate | admin and office jobs | /harrogate/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Watford | admin and office jobs | /watford/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Crawley | admin and office jobs | /crawley/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Swindon | admin and office jobs | /swindon/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Horsham | admin and office jobs | /horsham/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Lincoln | admin and office jobs | /lincoln/service-administrator-jobs | 1 | 19 | Yes |
| Detail | City | Nottingham | All roles | /nottingham/jobs | 1 |  | Yes |
| Detail | City | Wakefield | All roles | /wakefield/jobs | 1 |  | Yes |
| Detail | City | Bolton | All roles | /bolton/jobs | 1 |  | Yes |
| Detail | City | Reading | All roles | /reading/jobs | 1 |  | Yes |
| Detail | City | Chester | All roles | /chester/jobs | 1 |  | Yes |
| Detail | City | Durham | All roles | /durham/jobs | 1 |  | Yes |
| Detail | City | Gateshead | All roles | /gateshead/jobs | 1 |  | Yes |
| Detail | City | Northallerton | All roles | /northallerton/jobs | 1 |  | Yes |
| Detail | City | Norwich | All roles | /norwich/jobs | 1 |  | Yes |
| Detail | City | Salford | All roles | /salford/jobs | 1 |  | Yes |
| Detail | City | Redditch | All roles | /redditch/jobs | 1 |  | Yes |
| Detail | City | Guildford | All roles | /guildford/jobs | 1 |  | Yes |
| Detail | City | Carlisle | All roles | /carlisle/jobs | 1 |  | Yes |
| Detail | City | Preston | All roles | /preston/jobs | 1 |  | Yes |
| Detail | City | Witney | All roles | /witney/jobs | 1 |  | Yes |
| Detail | City | Yeovil | All roles | /yeovil/jobs | 1 |  | Yes |
| Detail | City | Hertford | All roles | /hertford/jobs | 1 |  | Yes |
| Detail | City | Leatherhead | All roles | /leatherhead/jobs | 1 |  | Yes |
| Detail | City | Rugby | All roles | /rugby/jobs | 1 |  | Yes |
| Detail | City | Colchester | All roles | /colchester/jobs | 1 |  | Yes |
| Detail | City | Hereford | All roles | /hereford/jobs | 1 |  | Yes |
| Detail | City | Stafford | All roles | /stafford/jobs | 1 |  | Yes |
| Detail | Regional/category | Yorkshire - East | Admin & Customer Service | /job-search/east-yorkshire/service-administrator-jobs | 1 | 34 | Yes |
| Detail | Regional/category | Northern Ireland - East | Admin & Customer Service | /job-search/northern-ireland-east/service-administrator-jobs | 1 | 9 | Yes |
| Detail | Regional/category | London | Customer Service & Contact Centre | /job-search/london/customer-service-jobs | 1 | 10 | Yes |
| Detail | Regional/category | London | HR & Recruitment | /job-search/london/hr-recruitment-jobs | 1 | 34 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Admin & Customer Service | /job-search/manchester-salford/service-administrator-jobs | 1 | 93 | Yes |
| Detail | Regional/category | London | Finance & Accounts | /job-search/london/finance-accounts-jobs | 1 | 62 | Yes |
| Detail | Regional/category | Oxfordshire | Admin & Customer Service | /job-search/oxfordshire/service-administrator-jobs | 1 | 59 | Yes |
| Detail | Regional/category | Bristol & Bath | Admin & Customer Service | /job-search/bristol-bath/service-administrator-jobs | 1 | 56 | Yes |
| Detail | Regional/category | Essex | Admin & Customer Service | /job-search/essex/service-administrator-jobs | 1 | 80 | Yes |
| Detail | Regional/category | Hampshire | Customer Service & Contact Centre | /job-search/hampshire/customer-service-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Cambridgeshire | Admin & Customer Service | /job-search/cambridgeshire/service-administrator-jobs | 1 | 55 | Yes |
| Detail | Regional/category | Gloucestershire | Admin & Customer Service | /job-search/gloucestershire/service-administrator-jobs | 1 | 52 | Yes |
| Detail | Regional/category | London | Support Worker | /job-search/london/support-worker | 1 | 41 | Yes |
| Detail | Regional/category | Dorset | Admin & Customer Service | /job-search/dorset/service-administrator-jobs | 1 | 39 | Yes |
| Detail | Regional/category | Staffordshire | Customer Service & Contact Centre | /job-search/staffordshire/customer-service-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Devon | Admin & Customer Service | /job-search/devon/service-administrator-jobs | 1 | 63 | Yes |
| Detail | Regional/category | Surrey | Customer Service & Contact Centre | /job-search/surrey/customer-service-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Wiltshire | Admin & Customer Service | /job-search/wiltshire/service-administrator-jobs | 1 | 41 | Yes |
| Detail | Regional/category | Northamptonshire | Admin & Customer Service | /job-search/northamptonshire/service-administrator-jobs | 1 | 65 | Yes |
| Detail | Regional/category | Berkshire | Admin & Customer Service | /job-search/berkshire/service-administrator-jobs | 1 | 62 | Yes |
| Detail | Regional/category | Nottinghamshire | Admin & Customer Service | /job-search/nottinghamshire/service-administrator-jobs | 1 | 54 | Yes |
| Detail | Regional/category | Buckinghamshire | Admin & Customer Service | /job-search/buckinghamshire/service-administrator-jobs | 1 | 59 | Yes |
| Detail | Regional/category | Surrey | Support Worker | /job-search/surrey/support-worker | 1 | 9 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Customer Service & Contact Centre | /job-search/manchester-salford/customer-service-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Hampshire | HR & Recruitment | /job-search/hampshire/hr-recruitment-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Hertfordshire | Admin & Customer Service | /job-search/hertfordshire/service-administrator-jobs | 1 | 81 | Yes |
| Detail | Regional/category | Staffordshire | Admin & Customer Service | /job-search/staffordshire/service-administrator-jobs | 1 | 56 | Yes |
| Detail | Regional/category | Norfolk | Admin & Customer Service | /job-search/norfolk/service-administrator-jobs | 1 | 53 | Yes |
| Detail | Regional/category | Sussex | Finance & Accounts | /job-search/sussex/finance-accounts-jobs | 1 | 27 | Yes |
| Detail | Regional/category | Yorkshire - West | Finance & Accounts | /job-search/west-yorkshire/finance-accounts-jobs | 1 | 30 | Yes |
| Detail | Regional/category | Gloucestershire | Finance & Accounts | /job-search/gloucestershire/finance-accounts-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Bristol & Bath | Finance & Accounts | /job-search/bristol-bath/finance-accounts-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Sussex | Customer Service & Contact Centre | /job-search/sussex/customer-service-jobs | 1 | 4 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Admin & Customer Service | /job-search/birmingham-solihull/service-administrator-jobs | 1 | 93 | Yes |
| Detail | Regional/category | Yorkshire - West | HR & Recruitment | /job-search/west-yorkshire/hr-recruitment-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Greater Manchester - South | Admin & Customer Service | /job-search/greater-manchester-south/service-administrator-jobs | 1 | 31 | Yes |
| Detail | Regional/category | Hampshire | Finance & Accounts | /job-search/hampshire/finance-accounts-jobs | 1 | 29 | Yes |
| Detail | Regional/category | North East | Finance & Accounts | /job-search/north-east/finance-accounts-jobs | 1 | 22 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Finance & Accounts | /job-search/birmingham-solihull/finance-accounts-jobs | 1 | 18 | Yes |
| Detail | Regional/category | Wiltshire | Support Worker | /job-search/wiltshire/support-worker | 1 | 4 | Yes |
| Detail | Regional/category | Somerset | Admin & Customer Service | /job-search/somerset/service-administrator-jobs | 1 | 29 | Yes |
| Detail | Regional/category | London | Customer Sales & Sales Advisor | /job-search/london/customer-sales-jobs | 1 | 78 | Yes |
| Detail | Regional/category | Yorkshire - West | Customer Sales & Sales Advisor | /job-search/west-yorkshire/customer-sales-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Customer Sales & Sales Advisor | /job-search/manchester-salford/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Leicestershire | Admin & Customer Service | /job-search/leicestershire/service-administrator-jobs | 1 | 51 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Admin & Customer Service | /job-search/warrington-halton/service-administrator-jobs | 1 | 23 | Yes |
| Detail | Regional/category | Cornwall | Admin & Customer Service | /job-search/cornwall/service-administrator-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Suffolk | Admin & Customer Service | /job-search/suffolk/service-administrator-jobs | 1 | 32 | Yes |
| Detail | Regional/category | Derbyshire | Admin & Customer Service | /job-search/derbyshire/service-administrator-jobs | 1 | 34 | Yes |
| Detail | Regional/category | Cheshire - East | Admin & Customer Service | /job-search/cheshire-east/service-administrator-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Lincolnshire | Admin & Customer Service | /job-search/lincolnshire/service-administrator-jobs | 1 | 30 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Admin & Customer Service | /job-search/merseyside-liverpool/service-administrator-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Shropshire | Admin & Customer Service | /job-search/shropshire/service-administrator-jobs | 1 | 29 | Yes |
| Detail | Regional/category | Greater Manchester - Wigan & Bolton | Admin & Customer Service | /job-search/wigan-bolton/service-administrator-jobs | 1 | 27 | Yes |
| Detail | Regional/category | West Midlands - Black Country | Admin & Customer Service | /job-search/black-country/service-administrator-jobs | 1 | 45 | Yes |
| Detail | Regional/category | London | Legal Assistant & Paralegal | /job-search/london/paralegal-jobs | 1 | 69 | Yes |
| Detail | Regional/category | Suffolk | Legal Assistant & Paralegal | /job-search/suffolk/paralegal-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Essex | Legal Assistant & Paralegal | /job-search/essex/paralegal-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Norfolk | Legal Assistant & Paralegal | /job-search/norfolk/paralegal-jobs | 1 | 7 | Yes |
| Detail | Regional/category | London | Marketing | /job-search/london/marketing-jobs | 1 | 87 | Yes |
| Detail | Regional/category | Surrey | Marketing | /job-search/surrey/marketing-jobs | 1 | 15 | Yes |
| Detail | Regional/category | Scotland Central - Fife | Admin & Customer Service | /job-search/fife/service-administrator-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Bristol & Bath | Legal Assistant & Paralegal | /job-search/bristol-bath/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Staffordshire | Marketing | /job-search/staffordshire/marketing-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Marketing | /job-search/manchester-salford/marketing-jobs | 1 | 19 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Marketing | /job-search/birmingham-solihull/marketing-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Berkshire | HR & Recruitment | /job-search/berkshire/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | HR & Recruitment | /job-search/manchester-salford/hr-recruitment-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Nottinghamshire | HR & Recruitment | /job-search/nottinghamshire/hr-recruitment-jobs | 1 | 7 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | HR & Recruitment | /job-search/birmingham-solihull/hr-recruitment-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Sussex | HR & Recruitment | /job-search/sussex/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Essex | HR & Recruitment | /job-search/essex/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Cheshire - West | Admin & Customer Service | /job-search/cheshire-west/service-administrator-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Scotland Central - Edinburgh & Lothians | Admin & Customer Service | /job-search/edinburgh-lothians/service-administrator-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Worcestershire | Admin & Customer Service | /job-search/worcestershire/service-administrator-jobs | 1 | 30 | Yes |
| Detail | Regional/category | Berkshire | Marketing | /job-search/berkshire/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Kent | Support Worker | /job-search/kent/support-worker | 1 | 9 | Yes |
| Detail | Regional/category | North East | Customer Sales & Sales Advisor | /job-search/north-east/customer-sales-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Oxfordshire | Support Worker | /job-search/oxfordshire/support-worker | 1 | 1 | Yes |
| Detail | Regional/category | Northern Ireland - East | Finance & Accounts | /job-search/northern-ireland-east/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Bedfordshire | Admin & Customer Service | /job-search/bedfordshire/service-administrator-jobs | 1 | 35 | Yes |
| Detail | Regional/category | Bristol & Bath | Customer Sales & Sales Advisor | /job-search/bristol-bath/customer-sales-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Buckinghamshire | Marketing | /job-search/buckinghamshire/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Wales South - Cardiff & Vale | Admin & Customer Service | /job-search/cardiff-vale/service-administrator-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Berkshire | Customer Sales & Sales Advisor | /job-search/berkshire/customer-sales-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Hertfordshire | Customer Sales & Sales Advisor | /job-search/hertfordshire/customer-sales-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Kent | Customer Sales & Sales Advisor | /job-search/kent/customer-sales-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Customer Sales & Sales Advisor | /job-search/glasgow/customer-sales-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Surrey | Customer Sales & Sales Advisor | /job-search/surrey/customer-sales-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Sussex | Customer Sales & Sales Advisor | /job-search/sussex/customer-sales-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Bristol & Bath | Marketing | /job-search/bristol-bath/marketing-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Gloucestershire | Marketing | /job-search/gloucestershire/marketing-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Hertfordshire | Marketing | /job-search/hertfordshire/marketing-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Kent | Marketing | /job-search/kent/marketing-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Oxfordshire | Marketing | /job-search/oxfordshire/marketing-jobs | 1 | 3 | Yes |
| Detail | Regional/category | North Scotland | Admin & Customer Service | /job-search/north-scotland/service-administrator-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Scotland Central - Tayside | Admin & Customer Service | /job-search/tayside/service-administrator-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Wales South - Valleys | Admin & Customer Service | /job-search/south-wales-valleys/service-administrator-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Cambridgeshire | Marketing | /job-search/cambridgeshire/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Essex | Marketing | /job-search/essex/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Marketing | /job-search/merseyside-liverpool/marketing-jobs | 1 | 2 | Yes |
| Detail | Regional/category | North East | Marketing | /job-search/north-east/marketing-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Finance & Accounts | /job-search/warrington-halton/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | North East | Customer Service & Contact Centre | /job-search/north-east/customer-service-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Devon | Customer Sales & Sales Advisor | /job-search/devon/customer-sales-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Hampshire | Customer Sales & Sales Advisor | /job-search/hampshire/customer-sales-jobs | 1 | 26 | Yes |
| Detail | Regional/category | North Scotland | Customer Sales & Sales Advisor | /job-search/north-scotland/customer-sales-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Greater Manchester - South | Marketing | /job-search/greater-manchester-south/marketing-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Northern Ireland - East | Marketing | /job-search/northern-ireland-east/marketing-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Yorkshire - North | Marketing | /job-search/north-yorkshire/marketing-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Essex | Finance & Accounts | /job-search/essex/finance-accounts-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Finance & Accounts | /job-search/manchester-salford/finance-accounts-jobs | 1 | 22 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | HR & Recruitment | /job-search/coventry-warwickshire/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Berkshire | Finance & Accounts | /job-search/berkshire/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Buckinghamshire | Finance & Accounts | /job-search/buckinghamshire/finance-accounts-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Cambridgeshire | Finance & Accounts | /job-search/cambridgeshire/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Cheshire - West | Finance & Accounts | /job-search/cheshire-west/finance-accounts-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Dorset | Finance & Accounts | /job-search/dorset/finance-accounts-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Hertfordshire | Finance & Accounts | /job-search/hertfordshire/finance-accounts-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Kent | Finance & Accounts | /job-search/kent/finance-accounts-jobs | 1 | 23 | Yes |
| Detail | Regional/category | Leicestershire | Finance & Accounts | /job-search/leicestershire/finance-accounts-jobs | 1 | 23 | Yes |
| Detail | Regional/category | Norfolk | Finance & Accounts | /job-search/norfolk/finance-accounts-jobs | 1 | 22 | Yes |
| Detail | Regional/category | Northamptonshire | Finance & Accounts | /job-search/northamptonshire/finance-accounts-jobs | 1 | 18 | Yes |
| Detail | Regional/category | Nottinghamshire | Finance & Accounts | /job-search/nottinghamshire/finance-accounts-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Oxfordshire | Finance & Accounts | /job-search/oxfordshire/finance-accounts-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Suffolk | Finance & Accounts | /job-search/suffolk/finance-accounts-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Surrey | Finance & Accounts | /job-search/surrey/finance-accounts-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Wales South - Cardiff & Vale | Finance & Accounts | /job-search/cardiff-vale/finance-accounts-jobs | 1 | 6 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Finance & Accounts | /job-search/coventry-warwickshire/finance-accounts-jobs | 1 | 24 | Yes |
| Detail | Regional/category | Yorkshire - South | Finance & Accounts | /job-search/south-yorkshire/finance-accounts-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Norfolk | Marketing | /job-search/norfolk/marketing-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Yorkshire - West | Marketing | /job-search/west-yorkshire/marketing-jobs | 1 | 13 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Legal Assistant & Paralegal | /job-search/birmingham-solihull/paralegal-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Yorkshire - North | Legal Assistant & Paralegal | /job-search/north-yorkshire/paralegal-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Yorkshire - West | Legal Assistant & Paralegal | /job-search/west-yorkshire/paralegal-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Berkshire | Legal Assistant & Paralegal | /job-search/berkshire/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Legal Assistant & Paralegal | /job-search/manchester-salford/paralegal-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Kent | Legal Assistant & Paralegal | /job-search/kent/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Legal Assistant & Paralegal | /job-search/merseyside-liverpool/paralegal-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Surrey | Legal Assistant & Paralegal | /job-search/surrey/paralegal-jobs | 1 | 18 | Yes |
| Detail | Regional/category | Buckinghamshire | Legal Assistant & Paralegal | /job-search/buckinghamshire/paralegal-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Marketing | /job-search/warrington-halton/marketing-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Essex | Customer Sales & Sales Advisor | /job-search/essex/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Gloucestershire | HR & Recruitment | /job-search/gloucestershire/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Greater Manchester - North | Admin & Customer Service | /job-search/greater-manchester-north/service-administrator-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Hampshire | Legal Assistant & Paralegal | /job-search/hampshire/paralegal-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Herefordshire | Admin & Customer Service | /job-search/herefordshire/service-administrator-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Lancashire - East | Admin & Customer Service | /job-search/lancashire-east/service-administrator-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Finance & Accounts | /job-search/merseyside-liverpool/finance-accounts-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Nottinghamshire | Marketing | /job-search/nottinghamshire/marketing-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Oxfordshire | Legal Assistant & Paralegal | /job-search/oxfordshire/paralegal-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Staffordshire | Finance & Accounts | /job-search/staffordshire/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Sussex | Marketing | /job-search/sussex/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Wales South - Swansea Bay | Admin & Customer Service | /job-search/swansea-bay/service-administrator-jobs | 1 | 10 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Marketing | /job-search/coventry-warwickshire/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Worcestershire | Finance & Accounts | /job-search/worcestershire/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Yorkshire - East | Finance & Accounts | /job-search/east-yorkshire/finance-accounts-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Cumbria - North | Admin & Customer Service | /job-search/cumbria-north/service-administrator-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Dorset | Customer Sales & Sales Advisor | /job-search/dorset/customer-sales-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Hertfordshire | Legal Assistant & Paralegal | /job-search/hertfordshire/paralegal-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Lancashire - Central | Admin & Customer Service | /job-search/lancashire-central/service-administrator-jobs | 1 | 11 | Yes |
| Detail | Regional/category | North Wales - East | Admin & Customer Service | /job-search/north-wales-east/service-administrator-jobs | 1 | 15 | Yes |
| Detail | Regional/category | Northamptonshire | Customer Sales & Sales Advisor | /job-search/northamptonshire/customer-sales-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Nottinghamshire | Legal Assistant & Paralegal | /job-search/nottinghamshire/paralegal-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Oxfordshire | Customer Sales & Sales Advisor | /job-search/oxfordshire/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Scotland Central - Falkirk & Stirling | Admin & Customer Service | /job-search/falkirk-stirling/service-administrator-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Suffolk | Customer Sales & Sales Advisor | /job-search/suffolk/customer-sales-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Wales South - Gwent | Admin & Customer Service | /job-search/gwent/service-administrator-jobs | 1 | 8 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Legal Assistant & Paralegal | /job-search/coventry-warwickshire/paralegal-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Yorkshire - West | Customer Service & Contact Centre | /job-search/west-yorkshire/customer-service-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Cambridgeshire | Customer Sales & Sales Advisor | /job-search/cambridgeshire/customer-sales-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Nottinghamshire | Customer Sales & Sales Advisor | /job-search/nottinghamshire/customer-sales-jobs | 1 | 6 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Customer Sales & Sales Advisor | /job-search/coventry-warwickshire/customer-sales-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Worcestershire | Customer Sales & Sales Advisor | /job-search/worcestershire/customer-sales-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Northamptonshire | Marketing | /job-search/northamptonshire/marketing-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Marketing | /job-search/glasgow/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Derbyshire | Finance & Accounts | /job-search/derbyshire/finance-accounts-jobs | 1 | 6 | Yes |
| Detail | Regional/category | North East | HR & Recruitment | /job-search/north-east/hr-recruitment-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Staffordshire | HR & Recruitment | /job-search/staffordshire/hr-recruitment-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Surrey | HR & Recruitment | /job-search/surrey/hr-recruitment-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Hertfordshire | Customer Service & Contact Centre | /job-search/hertfordshire/customer-service-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Kent | Customer Service & Contact Centre | /job-search/kent/customer-service-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Merseyside - St Helens & Knowsley | Admin & Customer Service | /job-search/st-helens-knowsley/service-administrator-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Cheshire - East | Customer Sales & Sales Advisor | /job-search/cheshire-east/customer-sales-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Gloucestershire | Customer Sales & Sales Advisor | /job-search/gloucestershire/customer-sales-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Leicestershire | Customer Sales & Sales Advisor | /job-search/leicestershire/customer-sales-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Norfolk | Customer Sales & Sales Advisor | /job-search/norfolk/customer-sales-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Legal Assistant & Paralegal | /job-search/glasgow/paralegal-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Yorkshire - South | Marketing | /job-search/south-yorkshire/marketing-jobs | 1 | 3 | Yes |
| Detail | Regional/category | West Midlands - Black Country | Finance & Accounts | /job-search/black-country/finance-accounts-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Leicestershire | HR & Recruitment | /job-search/leicestershire/hr-recruitment-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Suffolk | HR & Recruitment | /job-search/suffolk/hr-recruitment-jobs | 1 | 6 | Yes |

## CITY OPPORTUNITIES

**508 mapped towns/localities with live jobs or an existing city page.** Counts use all 3,984 unique live Ontap jobs across every role and provider: 2,342 have an exact recognised town/locality and 1,642 have only broader or unrecognised location evidence. CREATE means 4+ current Service Admin jobs and no existing city page; London is held separately.

| Status | Town/city/locality | Region | All live jobs | Existing pages | Current routes | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre | Other / unclassified |
|---|---|---|---:|---:|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CREATE | Ipswich | Suffolk | 11 | 0 |  | 9 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Crewe | Cheshire - East | 10 | 0 |  | 8 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Solihull | West Midlands - Birmingham & Solihull | 10 | 0 |  | 9 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Abingdon | Oxfordshire | 8 | 0 |  | 6 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Cheltenham | Gloucestershire | 8 | 0 |  | 5 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Chesterfield | Derbyshire | 8 | 0 |  | 7 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Chichester | Sussex | 8 | 0 |  | 7 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | King's Lynn | Norfolk | 8 | 0 |  | 5 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Brinsworth | Yorkshire - South | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Canterbury | Kent | 7 | 0 |  | 4 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Corby | Northamptonshire | 7 | 0 |  | 5 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Dundee | Scotland Central - Tayside | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Luton | Bedfordshire | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | St. Ives | Cambridgeshire | 7 | 0 |  | 5 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| CREATE | Stevenage | Hertfordshire | 7 | 0 |  | 4 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Stirling | Scotland Central - Falkirk & Stirling | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Blackburn | Lancashire - East | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Bracknell | Berkshire | 6 | 0 |  | 5 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Cannock | Staffordshire | 6 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| CREATE | Daventry | Northamptonshire | 6 | 0 |  | 4 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Farnborough | Hampshire | 6 | 0 |  | 4 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Gosport | Hampshire | 6 | 0 |  | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Leigh | Greater Manchester - Wigan & Bolton | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Richmond | Yorkshire - North | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Stratford-upon-avon | West Midlands - Coventry & Warwickshire | 6 | 0 |  | 4 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Trafford | Greater Manchester - South | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Wigan | Greater Manchester - Wigan & Bolton | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Wrexham | North Wales - East | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Banbury | Oxfordshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Bridlington | Yorkshire - East | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Chatham | Kent | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Coalville | Leicestershire | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Colwyn Bay | North Wales - East | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Didcot | Oxfordshire | 5 | 0 |  | 4 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Halifax | Yorkshire - West | 5 | 0 |  | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Hatfield | Hertfordshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | High Wycombe | Buckinghamshire | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Kettering | Northamptonshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Newport | Wales South -gwent | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Rugeley | Staffordshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Selby | Yorkshire - North | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Slough | Berkshire | 5 | 0 |  | 4 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Sutton Coldfield | West Midlands - Birmingham & Solihull | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Telford | Shropshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Welwyn Garden City | Hertfordshire | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| CREATE | Widnes | Cheshire - Warrington & Halton | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Beverley | Yorkshire - East | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Blyth | North East - Tyneside, Wearside & Northumberland | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Bridgend | Wales South - Swansea Bay | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Chesham | Buckinghamshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Chorley | Lancashire - Central | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Dudley | West Midlands - Black Country | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Kingswinford | West Midlands - Black Country | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Lewes | Sussex | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Melksham | Wiltshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Shirley | West Midlands - Birmingham & Solihull | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Staines | Surrey | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Waterlooville | Hampshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Wellingborough | Northamptonshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | West Bromwich | West Midlands - Black Country | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Manchester | Greater Manchester - Manchester & Salford | 118 | 1 | /manchester/service-administrator-jobs | 87 | 0 | 1 | 6 | 9 | 8 | 4 | 3 | 0 |
| LIVE PAGE | Birmingham | West Midlands - Birmingham & Solihull | 93 | 1 | /birmingham/service-administrator-jobs | 74 | 0 | 0 | 3 | 5 | 7 | 4 | 0 | 0 |
| LIVE PAGE | Leeds | Yorkshire - West | 82 | 1 | /leeds/service-administrator-jobs | 50 | 0 | 0 | 3 | 11 | 8 | 5 | 5 | 0 |
| LIVE PAGE | Bristol | Bristol & Bath | 63 | 1 | /bristol/service-administrator-jobs | 48 | 0 | 9 | 4 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Liverpool | Merseyside - Liverpool | 32 | 1 | /liverpool/service-administrator-jobs | 26 | 0 | 0 | 2 | 1 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Nottingham | Nottinghamshire | 31 | 1 | /nottingham/jobs | 17 | 0 | 3 | 1 | 6 | 4 | 0 | 0 | 0 |
| LIVE PAGE | Cambridge | Cambridgeshire | 29 | 1 | /cambridge/service-administrator-jobs | 25 | 0 | 3 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Bradford | Yorkshire - West | 27 | 1 | /bradford/service-administrator-jobs | 22 | 0 | 4 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Reading | Berkshire | 25 | 1 | /reading/jobs | 15 | 0 | 9 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Peterborough | Cambridgeshire | 24 | 1 | /peterborough/service-administrator-jobs | 17 | 0 | 3 | 0 | 2 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Sheffield | Yorkshire - South | 24 | 1 | /sheffield/service-administrator-jobs | 22 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Exeter | Devon | 22 | 1 | /exeter/service-administrator-jobs | 21 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Cardiff | Wales South - Cardiff & Vale | 21 | 1 | /cardiff/service-administrator-jobs | 20 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Coventry | West Midlands - Coventry & Warwickshire | 21 | 1 | /coventry/service-administrator-jobs | 15 | 0 | 0 | 2 | 1 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Hull | Yorkshire - East | 21 | 1 | /hull/service-administrator-jobs | 19 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Northampton | Northamptonshire | 20 | 1 | /northampton/service-administrator-jobs | 15 | 0 | 4 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Portsmouth | Hampshire | 19 | 1 | /portsmouth/service-administrator-jobs | 14 | 0 | 2 | 1 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Dartford | Kent | 18 | 1 | /dartford/service-administrator-jobs | 14 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Milton Keynes | Buckinghamshire | 18 | 1 | /milton-keynes/service-administrator-jobs | 16 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Newcastle | North East - Tyneside, Wearside & Northumberland | 18 | 1 | /newcastle/service-administrator-jobs | 15 | 0 | 2 | 0 | 0 | 0 | 0 | 1 | 0 |
| LIVE PAGE | Warrington | Cheshire - Warrington & Halton | 18 | 1 | /warrington/service-administrator-jobs | 16 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Warwick | West Midlands - Coventry & Warwickshire | 18 | 1 | /warwick/service-administrator-jobs | 12 | 0 | 2 | 2 | 0 | 1 | 1 | 0 | 0 |
| LIVE PAGE | Doncaster | Yorkshire - South | 17 | 1 | /doncaster/service-administrator-jobs | 15 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Edinburgh | Scotland Central - Edinburgh & Lothians | 16 | 1 | /edinburgh/service-administrator-jobs | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Swindon | Wiltshire | 16 | 1 | /swindon/service-administrator-jobs | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bolton | Greater Manchester - Wigan & Bolton | 15 | 1 | /bolton/jobs | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Glasgow | Scotland West - Glasgow | 15 | 1 | /glasgow/service-administrator-jobs | 0 | 0 | 4 | 5 | 6 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Leicester | Leicestershire | 15 | 1 | /leicester/service-administrator-jobs | 12 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | 0 |
| LIVE PAGE | Southampton | Hampshire | 14 | 2 | /southampton/service-administrator-jobs, /southampton/support-worker | 9 | 0 | 3 | 1 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Basingstoke | Hampshire | 13 | 1 | /basingstoke/service-administrator-jobs | 7 | 2 | 2 | 0 | 0 | 0 | 0 | 2 | 0 |
| LIVE PAGE | Bournemouth | Dorset | 13 | 1 | /bournemouth/service-administrator-jobs | 8 | 0 | 4 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Chelmsford | Essex | 13 | 1 | /chelmsford/service-administrator-jobs | 11 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Guildford | Surrey | 13 | 1 | /guildford/jobs | 5 | 1 | 5 | 0 | 0 | 1 | 0 | 1 | 0 |
| LIVE PAGE | Norwich | Norfolk | 13 | 1 | /norwich/jobs | 8 | 0 | 3 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Stockport | Greater Manchester - South | 13 | 1 | /stockport/service-administrator-jobs | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wakefield | Yorkshire - West | 13 | 1 | /wakefield/jobs | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Huddersfield | Yorkshire - West | 12 | 1 | /huddersfield/service-administrator-jobs | 9 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Oxford | Oxfordshire | 12 | 1 | /oxford/service-administrator-jobs | 11 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Redditch | Worcestershire | 12 | 1 | /redditch/jobs | 10 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | York | Yorkshire - North | 12 | 1 | /york/service-administrator-jobs | 11 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Aylesbury | Buckinghamshire | 11 | 1 | /aylesbury/service-administrator-jobs | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Brighton & Hove | Sussex | 10 | 1 | /brighton-hove/service-administrator-jobs | 6 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Gloucester | Gloucestershire | 10 | 1 | /gloucester/service-administrator-jobs | 7 | 0 | 1 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Maidstone | Kent | 10 | 1 | /maidstone/service-administrator-jobs | 6 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Gateshead | North East - Tyneside, Wearside & Northumberland | 9 | 1 | /gateshead/jobs | 8 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Hertford | Hertfordshire | 9 | 1 | /hertford/jobs | 7 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Rugby | West Midlands - Coventry & Warwickshire | 9 | 1 | /rugby/jobs | 6 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Stafford | Staffordshire | 9 | 1 | /stafford/jobs | 8 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bath | Bristol & Bath | 8 | 1 | /bath/service-administrator-jobs | 5 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Plymouth | Devon | 8 | 1 | /plymouth/service-administrator-jobs | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Poole | Dorset | 8 | 1 | /poole/service-administrator-jobs | 7 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Salford | Greater Manchester - Manchester & Salford | 8 | 1 | /salford/jobs | 5 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Watford | Hertfordshire | 8 | 1 | /watford/service-administrator-jobs | 5 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Worcester | Worcestershire | 8 | 1 | /worcester/service-administrator-jobs | 5 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Altrincham | Greater Manchester - South | 7 | 1 | /altrincham/service-administrator-jobs | 6 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Ashford | Kent | 7 | 1 | /ashford/service-administrator-jobs | 4 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Chester | Cheshire - West | 7 | 1 | /chester/jobs | 6 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Colchester | Essex | 7 | 1 | /colchester/jobs | 4 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Crawley | Sussex | 7 | 1 | /crawley/service-administrator-jobs | 5 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Eastleigh | Hampshire | 7 | 1 | /eastleigh/service-administrator-jobs | 3 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Leatherhead | Surrey | 7 | 1 | /leatherhead/jobs | 5 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Rotherham | Yorkshire - South | 7 | 1 | /rotherham/service-administrator-jobs | 6 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Shrewsbury | Shropshire | 7 | 1 | /shrewsbury/service-administrator-jobs | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bedford | Bedfordshire | 6 | 1 | /bedford/service-administrator-jobs | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Belfast | Northern Ireland - East | 6 | 1 | /belfast/service-administrator-jobs | 4 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Farnham | Surrey | 6 | 1 | /farnham/service-administrator-jobs | 2 | 0 | 0 | 3 | 0 | 0 | 1 | 0 | 0 |
| LIVE PAGE | Hemel Hempstead | Hertfordshire | 6 | 1 | /hemel-hempstead/service-administrator-jobs | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Hereford | Herefordshire | 6 | 1 | /hereford/jobs | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Witney | Oxfordshire | 6 | 1 | /witney/jobs | 5 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Harrogate | Yorkshire - North | 5 | 1 | /harrogate/service-administrator-jobs | 4 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Lincoln | Lincolnshire | 5 | 1 | /lincoln/service-administrator-jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Preston | Lancashire - Central | 5 | 1 | /preston/jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Swansea | Wales South - Swansea Bay | 5 | 1 | /swansea/service-administrator-jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Walsall | West Midlands - Black Country | 5 | 1 | /walsall/service-administrator-jobs | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Yeovil | Somerset | 5 | 1 | /yeovil/jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Barnsley | Yorkshire - South | 4 | 1 | /barnsley/service-administrator-jobs | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Horsham | Sussex | 4 | 1 | /horsham/service-administrator-jobs | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Scarborough | Yorkshire - North | 4 | 1 | /scarborough/service-administrator-jobs | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Stoke-on-trent | Staffordshire | 4 | 1 | /stoke-on-trent/service-administrator-jobs | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Sunderland | North East - Tyneside, Wearside & Northumberland | 4 | 1 | /sunderland/service-administrator-jobs | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Carlisle | Cumbria - North | 3 | 1 | /carlisle/jobs | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Macclesfield | Cheshire - East | 3 | 1 | /macclesfield/service-administrator-jobs | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Northallerton | Yorkshire - North | 3 | 1 | /northallerton/jobs | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Durham | North East - County Durham & Darlington/Hartlepool | 2 | 1 | /durham/jobs | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Chester Le Street | North East - County Durham & Darlington/Hartlepool | 1 | 1 | /chester-le-street/service-administrator-jobs | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Newtownabbey |  | 0 | 1 | /newtownabbey/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wigston |  | 0 | 1 | /wigston/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Uxbridge | London | 18 | 0 |  | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Borehamwood | London | 7 | 0 |  | 5 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| HOLD – LONDON | Sutton | London | 7 | 0 |  | 3 | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Croydon | London | 6 | 0 |  | 2 | 1 | 1 | 0 | 2 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Barking | London | 5 | 0 |  | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Bromley | London | 5 | 0 |  | 3 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Chessington | London | 5 | 0 |  | 1 | 0 | 0 | 0 | 3 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Hayes | London | 5 | 0 |  | 3 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Beckenham | London | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Kingston Upon Thames | London | 4 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Southwark | London | 4 | 0 |  | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Surbiton | London | 4 | 0 |  | 3 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wallington | London | 4 | 0 |  | 0 | 1 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| HOLD – LONDON | Harrow | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hillingdon | London | 3 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| HOLD – LONDON | Hounslow | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Islington | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Romford | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Ruislip | London | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Teddington | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Barnet | London | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Bexley | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Edgware | London | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Edmonton | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Feltham | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Greenford | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hornchurch | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Isleworth | London | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Loughton | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Mitcham | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | West Wickham | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Brentford | London | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Brixton | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Bushey | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Carshalton | London | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Chislehurst | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | City Of Westminster | London | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Dagenham | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Enfield | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Erith | London | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hackney | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hammersmith And Fulham | London | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Ilford | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Lambeth | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Morden | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Newham | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Orpington | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Pinner | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Sidcup | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | South Croydon | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Southall | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Stanmore | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Twickenham | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wandsworth | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wembley | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | West Drayton | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Woodford Green | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Eastbourne | Sussex | 6 | 0 |  | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fareham | Hampshire | 6 | 0 |  | 2 | 0 | 1 | 1 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Hook Norton | Oxfordshire | 6 | 0 |  | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Mansfield | Nottinghamshire | 6 | 0 |  | 1 | 0 | 2 | 2 | 0 | 0 | 1 | 0 | 0 |
| MONITOR | Sittingbourne | Kent | 6 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| MONITOR | Fleet | Hampshire | 5 | 0 |  | 2 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Havant | Hampshire | 5 | 0 |  | 2 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Newbury | Berkshire | 5 | 0 |  | 0 | 0 | 3 | 1 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Andover | Hampshire | 4 | 0 |  | 1 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Batley | Yorkshire - West | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brentwood | Essex | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Dereham | Norfolk | 4 | 0 |  | 3 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dorking | Surrey | 4 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | East Grinstead | Sussex | 4 | 0 |  | 2 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Gravesend | Kent | 4 | 0 |  | 3 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Great Yarmouth | Norfolk | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Hastings | Sussex | 4 | 0 |  | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hessle | Yorkshire - East | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Nuneaton | West Midlands - Coventry & Warwickshire | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rochester | Kent | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Trowbridge | Wiltshire | 4 | 0 |  | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wilmslow | Cheshire - East | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wokingham | Berkshire | 4 | 0 |  | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Aldershot | Hampshire | 3 | 0 |  | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Basildon | Essex | 3 | 0 |  | 1 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Bury | Greater Manchester - North | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cranleigh | Surrey | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Crowthorne | Berkshire | 3 | 0 |  | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Devizes | Wiltshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dover | Kent | 3 | 0 |  | 1 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| MONITOR | Droitwich | Worcestershire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ely | Cambridgeshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Emsworth | Hampshire | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Epsom | Surrey | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Evesham | Worcestershire | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Felixstowe | Suffolk | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ferndown | Dorset | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Goole | Yorkshire - East | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hailsham | Sussex | 3 | 0 |  | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Halesowen | West Midlands - Black Country | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Harlow | Essex | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Haslemere | Surrey | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Horley | Surrey | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hove | Sussex | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knaphill | Surrey | 3 | 0 |  | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Knutsford | Cheshire - East | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leamington Spa | West Midlands - Coventry & Warwickshire | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lisburn | Northern Ireland - East | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Liskeard | Cornwall | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Maidenhead | Berkshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Malton | Yorkshire - North | 3 | 0 |  | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Middleton | Greater Manchester - North | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ossett | Yorkshire - West | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ramsgate | Kent | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Redhill | Surrey | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rochdale | Greater Manchester - North | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Royston | Hertfordshire | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Rushden | Northamptonshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Salisbury | Wiltshire | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sevenoaks | Kent | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Helens | Merseyside - St Helens & Knowsley | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stourbridge | West Midlands - Black Country | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sutton-in-ashfield | Nottinghamshire | 3 | 0 |  | 1 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| MONITOR | Takeley | Essex | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Thetford | Norfolk | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tonbridge | Kent | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Torquay | Devon | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weybridge | Surrey | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Winchester | Hampshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Witham | Essex | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Woking | Surrey | 3 | 0 |  | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Accrington | Lancashire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Addlestone | Surrey | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Alton | Hampshire | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Attleborough | Norfolk | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Aylesford | Kent | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Barnstaple | devon | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Barrow-in-furness | Cumbria - South | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Beccles | Suffolk | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bicester | Oxfordshire | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Bognor Regis | Sussex | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Boston | Lincolnshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridgnorth | Shropshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Broadstairs | Kent | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bromsgrove | Worcestershire | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Buckingham | Buckinghamshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Burgess Hill | Sussex | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Camberley | Surrey | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Castleford | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chepstow | Wales South - Gwent | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cirencester | Gloucestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cleethorpes | Lincolnshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cobham | Surrey | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Corsham | Wiltshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dunstable | Bedfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fetcham | Surrey | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Flint | North Wales - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fordingbridge | Hampshire | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Frinton-on-sea | Essex | 2 | 0 |  | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Godalming | Surrey | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grimsby | Lincolnshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Haywards Heath | Sussex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hitchin | Hertfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Holmfirth | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Huntingdon | Cambridgeshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ilkley | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Inverness | North Scotland | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leyland | Lancashire - Central | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Livingston | Scotland Central - Edinburgh & Lothians | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lydney | Gloucestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Montrose | North Scotland | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newark | Nottinghamshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newhaven | Sussex | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newquay | Cornwall | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Normanton | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Northfleet | Kent | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ramsbottom | Greater Manchester - North | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Redruth | Cornwall | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Reigate | Surrey | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ringwood | Hampshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rossendale | Lancashire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Runcorn | Cheshire - Warrington & Halton | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shaftesbury | Dorset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shepperton | Surrey | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sherborne | Dorset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shildon | North East - County Durham & Darlington/Hartlepool | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Southam | West Midlands - Coventry & Warwickshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Albans | Hertfordshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stanley | North East - County Durham & Darlington/Hartlepool | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stonehouse | Gloucestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tamworth | Staffordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Taunton | Somerset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Thatcham | Berkshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Totnes | Devon | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tunbridge Wells | Kent | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Waltham Abbey | Essex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Waltham Cross | Hertfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wednesbury | West Midlands - Black Country | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Westbury | Wiltshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wimborne | Dorset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Winsford | Cheshire - West | 2 | 0 |  | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Worksop | Nottinghamshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Worsley | Greater Manchester - Manchester & Salford | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Worthing | Sussex | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Aberdeen | North Scotland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Alcester | West Midlands - Coventry & Warwickshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Alderley Edge | Cheshire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Antrim | Northern Ireland - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Arbroath | Scotland Central - Tayside | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Astwood Bank | Worcestershire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Barry | Wales South - Cardiff & Vale | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Beaconsfield | Buckinghamshire | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Beaminster | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bedale | Yorkshire - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bentley | Yorkshire - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Berkhamsted | Hertfordshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bideford | Devon | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Billingham | North East - Tees Valley | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Bishop's Stortford | Hertfordshire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Blaby | Leicestershire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Blandford Forum | Dorset | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bodmin | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Braintree | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brierley Hill | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brighouse | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Broadstone | Dorset | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Buckhurst Hill | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Burnley | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bury St. Edmunds | Suffolk | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Caerphilly | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Camborne | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Carryduff | Northern Ireland - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Caterham | Surrey | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cheadle | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cheddar | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chelmsley Wood | West Midlands - Birmingham & Solihull | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chertsey | Surrey | 1 | 0 |  | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Chippenham | Wiltshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Christchurch | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Church Stretton | Shropshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Clevedon | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Clitheroe | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Colne | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Corbridge | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cosham | Hampshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cottingham | Yorkshire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cradley Heath | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cramlington | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cromer | Norfolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cullompton | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cwmbran | Wales South - Gwent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Darlington | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Denton | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Downham Market | Norfolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dunmow | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dursley | Gloucestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Edenbridge | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Elland | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ellesmere Port | Cheshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Esher | Surrey | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fakenham | Norfolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Falkirk | Scotland Central - Falkirk & Stirling | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Falmouth | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Featherstone | Yorkshire - West | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Folkestone | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Forfar | Scotland Central - Tayside | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Frodsham | Cheshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gillingham | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Glenrothes | Scotland Central - Fife | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grangemouth | Scotland Central - Falkirk & Stirling | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grantham | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grays | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hartlepool | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Heanor | Derbyshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Henley-on-thames | Oxfordshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Herne Bay | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Heywood | Greater Manchester - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hindhead | Surrey | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hockley | Essex | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hook | Hampshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Houghton Le Spring | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hyde | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ilkeston | Derbyshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kenilworth | West Midlands - Coventry & Warwickshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Keynsham | Bristol & Bath | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knowsley | Merseyside - St Helens & Knowsley | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Larne | Northern Ireland - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ledbury | Herefordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leighton Buzzard | Bedfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Loughborough | Leicestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lyndhurst | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Maesteg | Wales South - Swansea Bay | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Maldon | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Malvern | Worcestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Market Harborough | Leicestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Marlborough | Wiltshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Midhurst | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Mirfield | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Mold | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Morley | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Mountain Ash | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | New Milton | Hampshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | New Romney | Kent | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newport Pagnell | Buckinghamshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newton Abbot | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newton Aycliffe | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Oldham | Greater Manchester - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ongar | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Oswestry | Shropshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Otley | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Penicuik | Scotland Central - Edinburgh & Lothians | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Penzance | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Perth | Scotland Central - Tayside | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Peterhead | North Scotland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Petersfield | Hampshire | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pitlochry | Scotland Central - Tayside | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pontyclun | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pontypridd | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Portishead | Bristol & Bath | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Potters Bar | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Potton | Bedfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pudsey | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ripon | Yorkshire - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Romsey | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Scunthorpe | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shoreham-by-sea | Sussex | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sleaford | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Smethwick | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Snodland | Kent | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Southend-on-sea | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Spalding | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Spondon | Derbyshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St Helens | Merseyside - St Helens & Knowsley | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Asaph | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Neots | Cambridgeshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stamford | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stanford-le-hope | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stone | Staffordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Swadlincote | Derbyshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Swanley | Kent | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tadley | Hampshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tadworth | Surrey | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Tewkesbury | Gloucestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Thame | Oxfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Thurso | North Scotland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tipton | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tonypandy | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tring | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Truro | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Uckfield | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wantage | Oxfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ware | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Warminster | Wiltshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Washington | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wellington | Shropshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | West Malling | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Westcliff-on-sea | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weston-super-mare | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wetherby | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weymouth | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Windsor | Berkshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wisbech | Cambridgeshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Woodbridge | Suffolk | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Yate | Bristol & Bath | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

> LIVE counts come directly from the current published `app/` JSON, deduplicated within each canonical region/family slice while preserving legitimate appearances in more than one family. This is the live-site authority for the reconciliation above; the dated source-count CSV is shown only as a freshness cross-check. The overview covers all 78 assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 78-market coverage has run, NOT LIVE Admin/Support and Customer Service may fall back to the latest all-region Module 2 profile (2026-08-17), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-10-29) used by the production family run, across 78 UK markets with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across 78 UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across 78, 78, 78 and 78 UK markets respectively, using their governed production boundaries and canonical geo. NOT LIVE Customer Service / Contact Centre was assessed from that same feed across 78 UK markets using its governed exact-title, salary and geography rules. All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

## LIVE

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire | 35 |  |  |  |  |  |  |  |
| Berkshire | 61 |  | 19 | 8 | 10 | 9 | 4 |  |
| Bristol & Bath | 66 |  | 13 | 8 | 6 | 10 |  |  |
| Buckinghamshire | 61 |  |  | 7 | 7 | 8 |  | CHECK |
| Cambridgeshire | 68 |  | 6 |  | 8 | 11 |  |  |
| Cheshire - East | 17 |  | 5 |  |  | CHECK |  |  |
| Cheshire - Warrington & Halton | 25 |  |  |  | 2 | 9 |  |  |
| Cheshire - West | 8 |  |  |  | CHECK | 6 |  |  |
| Cornwall | 12 |  |  |  |  | CHECK |  |  |
| Cumbria - North | 3 |  |  |  |  |  |  |  |
| Cumbria - South |  | 2 |  |  |  |  |  |  |
| Cumbria - West |  |  |  |  |  |  |  |  |
| Derbyshire | 34 |  |  |  |  | 6 |  |  |
| Devon | 63 |  | 3 |  |  | CHECK |  |  |
| Dorset | 42 |  | 9 |  |  | 14 |  |  |
| Essex | 82 |  | 8 | 9 | 5 | 18 | 4 |  |
| Gloucestershire | 54 |  | 6 |  | 1 | 14 | 3 |  |
| Greater Manchester - Manchester & Salford | 124 |  | 8 | 12 | 19 | 22 | 7 | 10 |
| Greater Manchester - North | 13 |  |  |  |  | CHECK |  |  |
| Greater Manchester - South | 32 |  |  |  | 2 |  |  |  |
| Greater Manchester - Wigan & Bolton | 27 |  |  |  |  |  |  |  |
| Hampshire | 126 | 14 | 26 | 14 |  | 29 | 5 | 12 |
| Herefordshire | 7 |  |  |  |  | CHECK |  |  |
| Hertfordshire | 84 |  | 11 | 9 | 7 | 21 |  | 7 |
| Kent | 106 | 9 | 19 | 8 | 11 | 23 |  | 6 |
| Lancashire - Blackpool & Fylde |  |  |  |  |  |  |  |  |
| Lancashire - Central | 11 |  |  |  |  |  |  |  |
| Lancashire - East | 13 |  |  |  |  | CHECK |  |  |
| Lancashire - North |  |  |  |  |  |  |  |  |
| Lancashire - West |  |  |  |  |  |  |  |  |
| Leicestershire | 52 |  | 4 |  |  | 22 | 5 |  |
| Lincolnshire | 30 |  |  |  |  | CHECK |  |  |
| London | 343 | 41 | 78 | 69 | 87 | 62 | 34 | 10 |
| Merseyside - Liverpool | 32 |  |  | 4 | 2 | 10 |  |  |
| Merseyside - Sefton |  |  |  |  |  |  |  |  |
| Merseyside - St Helens & Knowsley | 5 |  |  |  |  |  |  |  |
| Merseyside - Wirral |  |  |  |  |  |  |  |  |
| Norfolk | 52 |  | 6 | 7 | 3 | 22 |  |  |
| North East | 74 | 2 | 5 |  | 6 | 22 | 9 | 7 |
| North Scotland | 5 |  | 2 |  |  |  |  |  |
| North Wales - East | 15 |  |  |  |  |  |  |  |
| North Wales - West |  |  |  |  |  |  |  |  |
| Northamptonshire | 68 |  | 10 |  | 3 | 18 |  |  |
| Northern Ireland - East | 11 |  |  |  | 1 | 9 | CHECK |  |
| Northern Ireland - West |  |  |  |  |  |  |  |  |
| Nottinghamshire | 54 |  | 6 | 7 | 18 | 13 | 7 |  |
| Oxfordshire | 59 | 1 | 8 | 5 | 3 | 20 |  |  |
| Rutland |  |  |  |  |  |  |  |  |
| Scotland - Borders |  |  |  |  |  |  |  |  |
| Scotland Central - Edinburgh & Lothians | 19 |  |  |  |  |  |  |  |
| Scotland Central - Falkirk & Stirling | 9 |  |  |  |  |  |  |  |
| Scotland Central - Fife | 6 |  |  |  |  |  |  |  |
| Scotland Central - Tayside | 11 |  |  |  |  |  |  |  |
| Scotland West - Ayrshire |  |  |  |  |  |  |  |  |
| Scotland West - Glasgow | 15 |  | 7 | 5 | 9 |  |  |  |
| Scotland West - Lanarkshire |  |  |  |  |  |  |  |  |
| Scotland West - Renfrewshire & Inverclyde |  |  |  |  |  |  |  |  |
| Shropshire | 29 |  |  |  |  | CHECK |  |  |
| Somerset | 29 |  |  |  |  | CHECK |  |  |
| Staffordshire | 56 |  |  |  | 3 | 9 | 6 | 1 |
| Suffolk | 32 |  | 5 | 4 |  | 12 | 6 |  |
| Surrey | 104 | 9 | 16 | 17 | 15 | 21 | 10 | 12 |
| Sussex | 80 | 18 | 10 |  | 10 | 27 | 4 | 4 |
| Wales - Mid |  |  |  |  |  |  |  |  |
| Wales - West |  |  |  |  |  |  |  |  |
| Wales South - Cardiff & Vale | 22 |  |  |  |  | 6 |  |  |
| Wales South - Gwent | 8 |  |  |  |  |  |  |  |
| Wales South - Swansea Bay | 10 |  |  |  |  |  |  |  |
| Wales South - Valleys | 5 |  |  |  |  |  |  |  |
| West Midlands - Birmingham & Solihull | 112 |  |  | 4 | 11 | 17 | 9 |  |
| West Midlands - Black Country | 46 |  |  |  |  | 10 |  |  |
| West Midlands - Coventry & Warwickshire | 88 |  | 9 | 8 | 10 | 24 | 4 |  |
| Wiltshire | 41 | 4 |  |  |  | CHECK |  |  |
| Worcestershire | 30 |  | 7 |  |  | 11 |  |  |
| Yorkshire - East | 36 |  |  |  |  | 8 |  |  |
| Yorkshire - North | 38 |  |  | 16 | 3 | CHECK |  |  |
| Yorkshire - South | 59 | 1 |  |  | 3 | 13 |  |  |
| Yorkshire - West | 156 | CHECK | 11 | 11 | 13 | 30 | 6 | 13 |

## NOT LIVE

> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire |  | 0 / 0.0 / 0/14 | 8 / 6.7 / 10/14 | 5 / 2.6 / 0/14 | 3 / 3.1 / 0/14 | 4 / 5.4 / 8/14 | 1 / 0.7 / 0/14 | 4 / 4.1 / 0/14 |
| Berkshire |  | 3 / 3.6 / 0/14 |  |  |  |  |  | 1 / 2.0 / 0/14 |
| Bristol & Bath |  | 7 / 5.0 / 4/14 |  |  |  |  | 3 / 2.5 / 0/14 | 4 / 3.1 / 0/14 |
| Buckinghamshire |  | 0 / 0.0 / 0/14 | 3 / 3.9 / 5/14 |  |  |  | 9 / 5.3 / 9/14 |  |
| Cambridgeshire |  | 0 / 0.2 / 0/14 |  | 7 / 4.7 / 8/14 |  |  | 1 / 0.6 / 0/14 | 3 / 2.7 / 0/14 |
| Cheshire - East |  | 0 / 0.0 / 0/14 |  | 0 / 0.0 / 0/14 | 0 / 0.9 / 0/14 |  | 1 / 2.4 / 0/14 | 2 / 1.9 / 0/14 |
| Cheshire - Warrington & Halton |  | 0 / 0.0 / 0/14 | 4 / 3.6 / 0/14 | 2 / 2.0 / 0/14 |  |  | 2 / 2.0 / 0/14 | 1 / 1.8 / 0/14 |
| Cheshire - West |  | 0 / 0.0 / 0/14 | 3 / 2.6 / 0/14 | 4 / 2.4 / 0/14 |  |  | 0 / 0.8 / 0/14 | 1 / 1.0 / 0/14 |
| Cornwall |  | 2 / 2.0 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |  | 0 / 0.0 / 0/14 | 1 / 0.6 / 0/14 |
| Cumbria - North |  | 1 / 0.7 / 0/14 | 0 / 0.2 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 2.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Cumbria - South | 3 / 1.9 / 0/14 |  | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.8 / 0/14 | 2 / 1.5 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Cumbria - West | 5 / 4.1 / 0/14 | 0 / 0.7 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Derbyshire |  | 0 / 0.6 / 0/14 | 8 / 4.7 / 2/14 | 2 / 2.6 / 0/14 | 1 / 0.9 / 0/14 |  | 4 / 4.6 / 3/14 | 2 / 1.3 / 0/14 |
| Devon |  | 3 / 3.4 / 0/14 |  | 4 / 3.2 / 0/14 | 4 / 3.4 / 0/14 |  | 5 / 4.8 / 0/14 | 4 / 3.3 / 0/14 |
| Dorset |  | 4 / 2.3 / 0/14 |  | 4 / 4.9 / 4/14 | 8 / 7.0 / 10/14 |  | 2 / 1.9 / 0/14 | 4 / 2.9 / 0/14 |
| Essex |  | 3 / 4.6 / 0/14 |  |  |  |  |  | 4 / 2.5 / 0/14 |
| Gloucestershire |  | 2 / 2.2 / 0/14 |  | 4 / 3.4 / 0/14 |  |  |  | 1 / 1.0 / 0/14 |
| Greater Manchester - Manchester & Salford |  | 3 / 2.6 / 0/14 |  |  |  |  |  |  |
| Greater Manchester - North |  | 1 / 1.0 / 0/14 | 1 / 0.9 / 0/14 | 2 / 1.2 / 0/14 | 0 / 0.1 / 0/14 |  | 1 / 0.1 / 0/14 | 0 / 0.1 / 0/14 |
| Greater Manchester - South |  | 0 / 0.0 / 0/14 | 4 / 3.2 / 0/14 | 3 / 1.6 / 0/14 |  | 2 / 2.9 / 0/14 | 1 / 3.1 / 0/14 | 1 / 1.0 / 0/14 |
| Greater Manchester - Wigan & Bolton |  | 0 / 0.0 / 0/14 | 1 / 1.0 / 0/14 | 1 / 0.6 / 0/14 | 0 / 0.6 / 0/14 | 5 / 4.6 / 0/14 | 2 / 1.9 / 0/14 | 2 / 2.4 / 0/14 |
| Hampshire |  |  |  |  | 12 / 7.6 / 11/14 |  |  |  |
| Herefordshire |  | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.4 / 0/14 |  | 1 / 0.1 / 0/14 | 0 / 0.4 / 0/14 |
| Hertfordshire |  | 1 / 0.5 / 0/14 |  |  |  |  | 5 / 5.2 / 5/14 |  |
| Kent |  |  |  |  |  |  | 2 / 3.9 / 2/14 |  |
| Lancashire - Blackpool & Fylde | 5 / 4.1 / 0/14 | 1 / 0.1 / 0/14 | 0 / 0.8 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.4 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - Central |  | 1 / 0.2 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.3 / 0/14 | 4 / 2.9 / 0/14 | 1 / 0.1 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - East |  | 0 / 0.0 / 0/14 | 2 / 2.0 / 0/14 | 2 / 1.1 / 0/14 | 2 / 1.9 / 0/14 |  | 2 / 1.3 / 0/14 | 2 / 1.5 / 0/14 |
| Lancashire - North | 1 / 0.9 / 0/14 | 1 / 0.5 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.4 / 0/14 | 0 / 0.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - West | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.8 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.7 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Leicestershire |  | 0 / 0.0 / 0/14 |  | 0 / 2.4 / 0/14 | 8 / 5.1 / 4/14 |  |  | 3 / 2.7 / 0/14 |
| Lincolnshire |  | 1 / 1.1 / 0/14 | 4 / 5.1 / 6/14 | 3 / 3.6 / 0/14 | 2 / 2.6 / 0/14 |  | 1 / 1.8 / 0/14 | 1 / 0.6 / 0/14 |
| London |  |  |  |  |  |  |  |  |
| Merseyside - Liverpool |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |  |  |  | 3 / 1.9 / 0/14 | 0 / 0.2 / 0/14 |
| Merseyside - Sefton | 2 / 1.8 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Merseyside - St Helens & Knowsley |  | 0 / 0.0 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 2.5 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Merseyside - Wirral | 3 / 3.7 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.3 / 0/14 | 0 / 0.8 / 0/14 | 2 / 3.4 / 0/14 | 2 / 2.1 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 |
| Norfolk |  | 2 / 3.0 / 0/14 |  |  |  |  | 4 / 4.4 / 0/14 | 1 / 0.2 / 0/14 |
| North East |  |  |  | 7 / 6.0 / 7/14 |  |  |  |  |
| North Scotland |  | 0 / 0.0 / 0/14 |  | 3 / 3.9 / 0/14 | 0 / 0.0 / 0/14 | 2 / 2.9 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.4 / 0/14 |
| North Wales - East |  | 0 / 0.1 / 0/14 | 2 / 1.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.4 / 0/14 | 1 / 1.5 / 0/14 | 1 / 0.3 / 0/14 |
| North Wales - West | 1 / 1.5 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Northamptonshire |  | 2 / 1.3 / 0/14 |  | 6 / 5.5 / 8/14 |  |  | 5 / 4.6 / 3/14 | 2 / 1.9 / 0/14 |
| Northern Ireland - East |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 |  |  |  | 0 / 0.0 / 0/14 |
| Northern Ireland - West | 3 / 2.5 / 0/14 | 0 / 0.0 / 0/14 | 3 / 3.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 0.9 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 |
| Nottinghamshire |  | 1 / 1.8 / 0/14 |  |  |  |  |  | 2 / 2.4 / 0/14 |
| Oxfordshire |  |  |  |  |  |  | 3 / 1.1 / 0/14 | 1 / 1.9 / 0/14 |
| Rutland | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland - Borders | 0 / 0.2 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Edinburgh & Lothians |  | 0 / 0.0 / 0/14 | 1 / 1.2 / 0/14 | 6 / 2.8 / 1/14 | 0 / 0.4 / 0/14 | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Falkirk & Stirling |  | 0 / 0.0 / 0/14 | 1 / 0.1 / 0/14 | 2 / 1.1 / 0/14 | 0 / 0.0 / 0/14 | 2 / 2.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Fife |  | 0 / 0.0 / 0/14 | 2 / 1.9 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.4 / 0/14 | 2 / 3.7 / 0/14 | 1 / 0.3 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Tayside |  | 1 / 0.9 / 0/14 | 0 / 2.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.8 / 0/14 | 1 / 1.0 / 0/14 | 1 / 0.2 / 0/14 |
| Scotland West - Ayrshire | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.4 / 0/14 |
| Scotland West - Glasgow |  | 0 / 0.3 / 0/14 |  |  |  | 3 / 4.2 / 0/14 | 2 / 2.0 / 0/14 | 3 / 3.9 / 2/14 |
| Scotland West - Lanarkshire | 4 / 3.2 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 3 / 2.3 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland West - Renfrewshire & Inverclyde | 4 / 2.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 |
| Shropshire |  | 3 / 2.9 / 0/14 | 6 / 3.3 / 2/14 | 1 / 0.1 / 0/14 | 2 / 1.3 / 0/14 |  | 5 / 3.1 / 0/14 | 4 / 3.2 / 0/14 |
| Somerset |  | 1 / 1.9 / 0/14 | 4 / 2.5 / 0/14 | 2 / 1.1 / 0/14 | 1 / 2.4 / 0/14 |  | 3 / 1.6 / 0/14 | 4 / 3.6 / 0/14 |
| Staffordshire |  | 0 / 0.9 / 0/14 | 3 / 3.7 / 0/14 | 3 / 2.3 / 0/14 |  |  |  |  |
| Suffolk |  | 0 / 1.4 / 0/14 |  |  | 2 / 2.8 / 0/14 |  |  | 1 / 1.0 / 0/14 |
| Surrey |  |  |  |  |  |  |  |  |
| Sussex |  |  |  | 12 / 7.0 / 8/14 |  |  |  |  |
| Wales - Mid | 1 / 2.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.2 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 |
| Wales - West | 1 / 0.9 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Cardiff & Vale |  | 1 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 3 / 1.2 / 0/14 | 0 / 0.1 / 0/14 |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Gwent |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.5 / 0/14 | 0 / 0.9 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Swansea Bay |  | 2 / 1.2 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 3.4 / 0/14 | 0 / 0.3 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Valleys |  | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 1 / 2.1 / 0/14 |
| West Midlands - Birmingham & Solihull |  | 0 / 0.0 / 0/14 | 2 / 1.6 / 0/14 |  |  |  |  | 5 / 4.6 / 4/14 |
| West Midlands - Black Country |  | 0 / 0.0 / 0/14 | 2 / 2.2 / 0/14 | 0 / 0.9 / 0/14 | 4 / 3.7 / 0/14 |  | 6 / 6.2 / 11/14 | 4 / 4.6 / 2/14 |
| West Midlands - Coventry & Warwickshire |  | 2 / 2.1 / 0/14 |  |  |  |  |  | 5 / 3.0 / 0/14 |
| Wiltshire |  |  | 1 / 1.1 / 0/14 | 2 / 1.1 / 0/14 | 4 / 2.1 / 0/14 |  | 0 / 0.0 / 0/14 | 3 / 1.6 / 0/14 |
| Worcestershire |  | 1 / 0.1 / 0/14 |  | 2 / 2.6 / 0/14 | 0 / 1.2 / 0/14 |  | 0 / 0.0 / 0/14 | 0 / 1.4 / 0/14 |
| Yorkshire - East |  | 0 / 0.0 / 0/14 | 3 / 3.5 / 0/14 | 3 / 3.2 / 0/14 | 2 / 1.1 / 0/14 |  | 2 / 1.6 / 0/14 | 1 / 1.0 / 0/14 |
| Yorkshire - North |  | 1 / 0.7 / 0/14 | 2 / 2.4 / 0/14 |  |  |  | 1 / 1.0 / 0/14 | 1 / 2.2 / 0/14 |
| Yorkshire - South |  |  | 2 / 2.6 / 0/14 | 5 / 4.7 / 3/14 |  |  | 4 / 2.7 / 0/14 | 4 / 4.0 / 0/14 |
| Yorkshire - West |  |  |  |  |  |  |  |  |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Live regions | 62 / 78 | 11 / 78 | 27 / 78 | 20 / 78 | 29 / 78 | 46 / 78 | 17 / 78 | 11 / 78 |
| Live slice placements | 3015 | 101 + 1 CHECK | 317 | 232 | 278 + 1 CHECK | 586 + 11 CHECK | 123 + 1 CHECK | 82 + 1 CHECK |

**Live slices: 223 / 624.**
