# Ontap daily regional overview

Production source commit: `da826405a952a7f0750aa29478144f6dd7961708`

Generated: 2026-10-19T08:57:29+01:00

[Download this overview as Excel](./daily-region-overview.xlsx)

## SITEWIDE RECONCILIATION

| Measure | Count |
|---|---:|
| Unique live jobs | 4,050 |
| Unique JobG8 jobs | 3,615 |
| Unique non-JobG8 jobs | 435 |
| Regional/category slice placements | 4,865 |
| Jobs appearing on multiple slices | 807 |
| Extra slice placements | 815 |
| Unique jobs outside governed slices | 0 |
| Jobs found in non-LIVE slices | 0 |

**Reconciliation: 4,050 unique jobs + 815 extra slice placements = 4,865 regional/category slice placements.**

Latest source-count CSV: `pipeline/reports-daily/live-job-source-count-2026-10-19.csv` — **STALE — CSV says 4,108 for 2026-10-19**.

### Provider breakdown

| Provider | Unique live jobs | Jobs on 2+ slices | Extra slice placements |
|---|---:|---:|---:|
| JobG8 | 3,615 | 807 | 815 |
| NHS Jobs | 298 | 0 | 0 |
| Teaching Vacancies | 137 | 0 | 0 |

## JOBG8 FEED RECEIVED

**JobG8 jobs received: 20,000** (feed date: 2026-10-19)

| JobG8 classification | Jobs received | Ontap jobs classified/published |
|---|---:|---:|
| Accounting | 3,979 | 894 |
| Sales & Marketing | 3,320 | 666 |
| Administration | 1,748 | 1,024 |
| Legal | 1,631 | 256 |
| I.T. & Communications | 1,374 | 7 |
| Transport & Logistics | 1,336 | 27 |
| HR / Recruitment | 1,263 | 166 |
| Real Estate & Property | 1,229 | 66 |
| Healthcare & Medical | 882 | 82 |
| Call Centre / CustomerService | 843 | 379 |
| Education | 658 | 4 |
| Community & Sport | 509 | 42 |
| Insurance & Superannuation | 476 | 22 |
| Banking & Financial Services | 366 | 10 |
| Government & Defence | 244 | 4 |
| Advert / Media / Entertainment | 142 | 19 |
| Total across classifications | 20,000 | 3,668 |

## JOBG8 XML RECONCILIATION

| Check | XML feed total | Sum of ‘Jobs received’ | Difference (sum − XML) | Result |
|---|---:|---:|---:|---|
| JobG8 feed categories | 20,000 | 20,000 | 0 | **PASS** |

**JobG8 feed reconciliation: PASS.** Difference is 0 jobs (summed categories minus XML total).

## JOBG8 LAST 10 FEED DATES — TOTALS ONLY

Saved history contains 9 of the latest 10 feed dates. Older feed totals were not saved and are not backfilled.

| Feed date | JobG8 jobs received | Ontap jobs classified/published |
|---|---:|---:|
| 2026-10-19 | 20,000 | 3,668 |
| 2026-10-18 | 20,000 | 3,666 |
| 2026-10-17 | 20,000 | 3,577 |
| 2026-10-16 | 20,000 | 3,239 |
| 2026-10-15 | 20,000 | 3,076 |
| 2026-10-14 | 20,000 | 3,005 |
| 2026-10-13 | 12,894 | 1,042 |
| 2026-10-12 | 13,516 | 1,117 |
| 2026-10-11 | 13,307 | 1,156 |

## JOBG8 LAST 10 FEED DATES — SELECTED JOBS BY CLASSIFICATION

Each dated column shows Ontap jobs classified/published in that JobG8 classification.

| JobG8 classification | 2026-10-19 | 2026-10-18 | 2026-10-17 | 2026-10-16 | 2026-10-15 | 2026-10-14 | 2026-10-13 | 2026-10-12 | 2026-10-11 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Accounting | 894 | 897 | 842 | 709 | 671 | 659 | 461 | 473 | 468 |
| Administration | 1024 | 1018 | 1047 | 1037 | 1026 | 1006 | 74 | 78 | 81 |
| Advert / Media / Entertainment | 19 | 19 | 21 | 20 | 19 | 20 | 4 | 6 | 6 |
| Banking & Financial Services | 10 | 10 | 11 | 10 | 9 | 9 | 0 | 1 | 1 |
| Call Centre / CustomerService | 379 | 377 | 388 | 374 | 360 | 351 | 65 | 36 | 36 |
| Community & Sport | 42 | 43 | 47 | 46 | 50 | 51 | 6 | 5 | 6 |
| Education | 4 | 4 | 4 | 3 | 2 | 2 | 2 | 2 | 2 |
| Government & Defence | 4 | 4 | 4 | 3 | 4 | 4 | 0 | 0 | 1 |
| Healthcare & Medical | 82 | 84 | 79 | 62 | 59 | 62 | 32 | 34 | 35 |
| HR / Recruitment | 166 | 165 | 170 | 159 | 129 | 120 | 5 | 5 | 5 |
| I.T. & Communications | 7 | 7 | 8 | 8 | 8 | 10 | 12 | 19 | 20 |
| Insurance & Superannuation | 22 | 22 | 21 | 21 | 20 | 20 | 10 | 36 | 37 |
| Legal | 256 | 256 | 259 | 257 | 241 | 240 | 157 | 155 | 197 |
| Real Estate & Property | 66 | 66 | 56 | 44 | 43 | 41 | 13 | 23 | 25 |
| Sales & Marketing | 666 | 667 | 593 | 461 | 412 | 386 | 187 | 187 | 180 |
| Transport & Logistics | 27 | 27 | 27 | 25 | 23 | 24 | 14 | 57 | 56 |

## PAGES

**Published/indexable URLs: 4,330** — 4,050 individual job pages, 196 regional/category pages, 76 city pages and 8 core pages.

| Level | Page type | Area | Family | URL | Page count | Live jobs | In sitemap |
|---|---|---|---|---|---:|---:|---|
| Summary | All published/indexable URLs | Sitewide |  |  | 4,330 |  | Yes |
| Summary | Individual job | Sitewide |  | /jobs/[id] | 4,050 | 4,050 | Yes |
| Summary | Regional/category | Sitewide |  | Multiple | 196 |  | Yes |
| Summary | City | Sitewide |  | Multiple | 76 |  | Yes |
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
| Detail | Regional/category | West Yorkshire | Support Worker | /west-yorkshire/support-worker | 1 | 1 | Yes |
| Detail | Regional/category | South Yorkshire | Support Worker | /south-yorkshire/support-worker | 1 | 0 | Yes |
| Detail | Regional/category | North East | Support Worker | /north-east/support-worker | 1 | 3 | Yes |
| Detail | Regional/category | Sussex | Support Worker | /sussex/support-worker | 1 | 12 | Yes |
| Detail | Regional/category | Cumbria South | Support Worker | /cumbria-south/support-worker | 1 | 2 | Yes |
| Detail | Regional/category | Hampshire | Support Worker | /hampshire/support-worker | 1 | 9 | Yes |
| Detail | Regional/category | West Yorkshire | Service Administrator Jobs | /west-yorkshire/service-administrator-jobs | 1 | 113 | Yes |
| Detail | Regional/category | South Yorkshire | Service Administrator Jobs | /south-yorkshire/service-administrator-jobs | 1 | 51 | Yes |
| Detail | Regional/category | North Yorkshire | Service Administrator Jobs | /north-yorkshire/service-administrator-jobs | 1 | 40 | Yes |
| Detail | Regional/category | North East | Service Administrator Jobs | /north-east/service-administrator-jobs | 1 | 95 | Yes |
| Detail | Regional/category | London | Service Administrator Jobs | /london/service-administrator-jobs | 1 | 353 | Yes |
| Detail | Regional/category | London | Central Service Administrator Jobs | /london/central-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | North Service Administrator Jobs | /london/north-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | East Service Administrator Jobs | /london/east-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | South Service Administrator Jobs | /london/south-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | West Service Administrator Jobs | /london/west-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | Hampshire | Service Administrator Jobs | /hampshire/service-administrator-jobs | 1 | 124 | Yes |
| Detail | Regional/category | Coventry Warwickshire | Service Administrator Jobs | /coventry-warwickshire/service-administrator-jobs | 1 | 58 | Yes |
| Detail | Regional/category | Surrey | Service Administrator Jobs | /surrey/service-administrator-jobs | 1 | 112 | Yes |
| Detail | Regional/category | Kent | Service Administrator Jobs | /kent/service-administrator-jobs | 1 | 96 | Yes |
| Detail | Regional/category | Sussex | Service Administrator Jobs | /sussex/service-administrator-jobs | 1 | 83 | Yes |
| Detail | City | Newcastle | admin and office jobs | /newcastle/service-administrator-jobs | 1 | 28 | Yes |
| Detail | City | Southampton | support worker jobs | /southampton/support-worker | 1 | 0 | Yes |
| Detail | City | Sheffield | admin and office jobs | /sheffield/service-administrator-jobs | 1 | 27 | Yes |
| Detail | City | Leeds | admin and office jobs | /leeds/service-administrator-jobs | 1 | 91 | Yes |
| Detail | City | Coventry | admin and office jobs | /coventry/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Southampton | admin and office jobs | /southampton/service-administrator-jobs | 1 | 15 | Yes |
| Detail | City | Brighton & Hove | admin and office jobs | /brighton-hove/service-administrator-jobs | 1 | 11 | Yes |
| Detail | City | Bradford | admin and office jobs | /bradford/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Huddersfield | admin and office jobs | /huddersfield/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | York | admin and office jobs | /york/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Barnsley | admin and office jobs | /barnsley/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Doncaster | admin and office jobs | /doncaster/service-administrator-jobs | 1 | 19 | Yes |
| Detail | City | Bristol | admin and office jobs | /bristol/service-administrator-jobs | 1 | 47 | Yes |
| Detail | City | Manchester | admin and office jobs | /manchester/service-administrator-jobs | 1 | 115 | Yes |
| Detail | City | Cambridge | admin and office jobs | /cambridge/service-administrator-jobs | 1 | 23 | Yes |
| Detail | City | Birmingham | admin and office jobs | /birmingham/service-administrator-jobs | 1 | 95 | Yes |
| Detail | City | Peterborough | admin and office jobs | /peterborough/service-administrator-jobs | 1 | 13 | Yes |
| Detail | City | Warrington | admin and office jobs | /warrington/service-administrator-jobs | 1 | 24 | Yes |
| Detail | City | Liverpool | admin and office jobs | /liverpool/service-administrator-jobs | 1 | 31 | Yes |
| Detail | City | Hull | admin and office jobs | /hull/service-administrator-jobs | 1 | 24 | Yes |
| Detail | City | Oxford | admin and office jobs | /oxford/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Belfast | admin and office jobs | /belfast/service-administrator-jobs | 1 | 3 | Yes |
| Detail | City | Glasgow | admin and office jobs | /glasgow/service-administrator-jobs | 1 | 32 | Yes |
| Detail | City | Edinburgh | admin and office jobs | /edinburgh/service-administrator-jobs | 1 | 23 | Yes |
| Detail | City | Cardiff | admin and office jobs | /cardiff/service-administrator-jobs | 1 | 26 | Yes |
| Detail | City | Exeter | admin and office jobs | /exeter/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Milton Keynes | admin and office jobs | /milton-keynes/service-administrator-jobs | 1 | 17 | Yes |
| Detail | City | Farnham | admin and office jobs | /farnham/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Northampton | admin and office jobs | /northampton/service-administrator-jobs | 1 | 19 | Yes |
| Detail | City | Poole | admin and office jobs | /poole/service-administrator-jobs | 1 | 17 | Yes |
| Detail | City | Portsmouth | admin and office jobs | /portsmouth/service-administrator-jobs | 1 | 13 | Yes |
| Detail | City | Stoke-on-trent | admin and office jobs | /stoke-on-trent/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Hemel Hempstead | admin and office jobs | /hemel-hempstead/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Basingstoke | admin and office jobs | /basingstoke/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Chelmsford | admin and office jobs | /chelmsford/service-administrator-jobs | 1 | 15 | Yes |
| Detail | City | Gloucester | admin and office jobs | /gloucester/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Leicester | admin and office jobs | /leicester/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Maidstone | admin and office jobs | /maidstone/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Newtownabbey | admin and office jobs | /newtownabbey/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Plymouth | admin and office jobs | /plymouth/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Sunderland | admin and office jobs | /sunderland/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Worcester | admin and office jobs | /worcester/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Altrincham | admin and office jobs | /altrincham/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Ashford | admin and office jobs | /ashford/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Aylesbury | admin and office jobs | /aylesbury/service-administrator-jobs | 1 | 12 | Yes |
| Detail | City | Bedford | admin and office jobs | /bedford/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Bournemouth | admin and office jobs | /bournemouth/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Chester Le Street | admin and office jobs | /chester-le-street/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Macclesfield | admin and office jobs | /macclesfield/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Rotherham | admin and office jobs | /rotherham/service-administrator-jobs | 1 | 3 | Yes |
| Detail | City | Scarborough | admin and office jobs | /scarborough/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Shrewsbury | admin and office jobs | /shrewsbury/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Warwick | admin and office jobs | /warwick/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Wigston | admin and office jobs | /wigston/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Dartford | admin and office jobs | /dartford/service-administrator-jobs | 1 | 13 | Yes |
| Detail | City | Stockport | admin and office jobs | /stockport/service-administrator-jobs | 1 | 17 | Yes |
| Detail | City | Swansea | admin and office jobs | /swansea/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Walsall | admin and office jobs | /walsall/service-administrator-jobs | 1 | 11 | Yes |
| Detail | City | Bath | admin and office jobs | /bath/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Eastleigh | admin and office jobs | /eastleigh/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Harrogate | admin and office jobs | /harrogate/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Watford | admin and office jobs | /watford/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Crawley | admin and office jobs | /crawley/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Swindon | admin and office jobs | /swindon/service-administrator-jobs | 1 | 11 | Yes |
| Detail | City | Horsham | admin and office jobs | /horsham/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Lincoln | admin and office jobs | /lincoln/service-administrator-jobs | 1 | 26 | Yes |
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
| Detail | Regional/category | Yorkshire - East | Admin & Customer Service | /job-search/east-yorkshire/service-administrator-jobs | 1 | 35 | Yes |
| Detail | Regional/category | Northern Ireland - East | Admin & Customer Service | /job-search/northern-ireland-east/service-administrator-jobs | 1 | 4 | Yes |
| Detail | Regional/category | London | Customer Service & Contact Centre | /job-search/london/customer-service-jobs | 1 | 8 | Yes |
| Detail | Regional/category | London | HR & Recruitment | /job-search/london/hr-recruitment-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Admin & Customer Service | /job-search/manchester-salford/service-administrator-jobs | 1 | 83 | Yes |
| Detail | Regional/category | London | Finance & Accounts | /job-search/london/finance-accounts-jobs | 1 | 87 | Yes |
| Detail | Regional/category | Oxfordshire | Admin & Customer Service | /job-search/oxfordshire/service-administrator-jobs | 1 | 60 | Yes |
| Detail | Regional/category | Bristol & Bath | Admin & Customer Service | /job-search/bristol-bath/service-administrator-jobs | 1 | 49 | Yes |
| Detail | Regional/category | Essex | Admin & Customer Service | /job-search/essex/service-administrator-jobs | 1 | 76 | Yes |
| Detail | Regional/category | Hampshire | Customer Service & Contact Centre | /job-search/hampshire/customer-service-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Cambridgeshire | Admin & Customer Service | /job-search/cambridgeshire/service-administrator-jobs | 1 | 37 | Yes |
| Detail | Regional/category | Gloucestershire | Admin & Customer Service | /job-search/gloucestershire/service-administrator-jobs | 1 | 50 | Yes |
| Detail | Regional/category | London | Support Worker | /job-search/london/support-worker | 1 | 33 | Yes |
| Detail | Regional/category | Dorset | Admin & Customer Service | /job-search/dorset/service-administrator-jobs | 1 | 53 | Yes |
| Detail | Regional/category | Staffordshire | Customer Service & Contact Centre | /job-search/staffordshire/customer-service-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Devon | Admin & Customer Service | /job-search/devon/service-administrator-jobs | 1 | 65 | Yes |
| Detail | Regional/category | Surrey | Customer Service & Contact Centre | /job-search/surrey/customer-service-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Wiltshire | Admin & Customer Service | /job-search/wiltshire/service-administrator-jobs | 1 | 33 | Yes |
| Detail | Regional/category | Northamptonshire | Admin & Customer Service | /job-search/northamptonshire/service-administrator-jobs | 1 | 52 | Yes |
| Detail | Regional/category | Berkshire | Admin & Customer Service | /job-search/berkshire/service-administrator-jobs | 1 | 70 | Yes |
| Detail | Regional/category | Nottinghamshire | Admin & Customer Service | /job-search/nottinghamshire/service-administrator-jobs | 1 | 50 | Yes |
| Detail | Regional/category | Buckinghamshire | Admin & Customer Service | /job-search/buckinghamshire/service-administrator-jobs | 1 | 61 | Yes |
| Detail | Regional/category | Surrey | Support Worker | /job-search/surrey/support-worker | 1 | 7 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Customer Service & Contact Centre | /job-search/manchester-salford/customer-service-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Hampshire | HR & Recruitment | /job-search/hampshire/hr-recruitment-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Hertfordshire | Admin & Customer Service | /job-search/hertfordshire/service-administrator-jobs | 1 | 92 | Yes |
| Detail | Regional/category | Staffordshire | Admin & Customer Service | /job-search/staffordshire/service-administrator-jobs | 1 | 47 | Yes |
| Detail | Regional/category | Norfolk | Admin & Customer Service | /job-search/norfolk/service-administrator-jobs | 1 | 50 | Yes |
| Detail | Regional/category | Sussex | Finance & Accounts | /job-search/sussex/finance-accounts-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Yorkshire - West | Finance & Accounts | /job-search/west-yorkshire/finance-accounts-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Gloucestershire | Finance & Accounts | /job-search/gloucestershire/finance-accounts-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Bristol & Bath | Finance & Accounts | /job-search/bristol-bath/finance-accounts-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Sussex | Customer Service & Contact Centre | /job-search/sussex/customer-service-jobs | 1 | 9 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Admin & Customer Service | /job-search/birmingham-solihull/service-administrator-jobs | 1 | 95 | Yes |
| Detail | Regional/category | Yorkshire - West | HR & Recruitment | /job-search/west-yorkshire/hr-recruitment-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Greater Manchester - South | Admin & Customer Service | /job-search/greater-manchester-south/service-administrator-jobs | 1 | 33 | Yes |
| Detail | Regional/category | Hampshire | Finance & Accounts | /job-search/hampshire/finance-accounts-jobs | 1 | 38 | Yes |
| Detail | Regional/category | North East | Finance & Accounts | /job-search/north-east/finance-accounts-jobs | 1 | 30 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Finance & Accounts | /job-search/birmingham-solihull/finance-accounts-jobs | 1 | 30 | Yes |
| Detail | Regional/category | Wiltshire | Support Worker | /job-search/wiltshire/support-worker | 1 | 4 | Yes |
| Detail | Regional/category | Somerset | Admin & Customer Service | /job-search/somerset/service-administrator-jobs | 1 | 38 | Yes |
| Detail | Regional/category | London | Customer Sales & Sales Advisor | /job-search/london/customer-sales-jobs | 1 | 83 | Yes |
| Detail | Regional/category | Yorkshire - West | Customer Sales & Sales Advisor | /job-search/west-yorkshire/customer-sales-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Customer Sales & Sales Advisor | /job-search/manchester-salford/customer-sales-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Leicestershire | Admin & Customer Service | /job-search/leicestershire/service-administrator-jobs | 1 | 62 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Admin & Customer Service | /job-search/warrington-halton/service-administrator-jobs | 1 | 27 | Yes |
| Detail | Regional/category | Cornwall | Admin & Customer Service | /job-search/cornwall/service-administrator-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Suffolk | Admin & Customer Service | /job-search/suffolk/service-administrator-jobs | 1 | 40 | Yes |
| Detail | Regional/category | Derbyshire | Admin & Customer Service | /job-search/derbyshire/service-administrator-jobs | 1 | 34 | Yes |
| Detail | Regional/category | Cheshire - East | Admin & Customer Service | /job-search/cheshire-east/service-administrator-jobs | 1 | 15 | Yes |
| Detail | Regional/category | Lincolnshire | Admin & Customer Service | /job-search/lincolnshire/service-administrator-jobs | 1 | 35 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Admin & Customer Service | /job-search/merseyside-liverpool/service-administrator-jobs | 1 | 25 | Yes |
| Detail | Regional/category | Shropshire | Admin & Customer Service | /job-search/shropshire/service-administrator-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Greater Manchester - Wigan & Bolton | Admin & Customer Service | /job-search/wigan-bolton/service-administrator-jobs | 1 | 21 | Yes |
| Detail | Regional/category | West Midlands - Black Country | Admin & Customer Service | /job-search/black-country/service-administrator-jobs | 1 | 54 | Yes |
| Detail | Regional/category | London | Legal Assistant & Paralegal | /job-search/london/paralegal-jobs | 1 | 59 | Yes |
| Detail | Regional/category | Suffolk | Legal Assistant & Paralegal | /job-search/suffolk/paralegal-jobs | 1 | 29 | Yes |
| Detail | Regional/category | Essex | Legal Assistant & Paralegal | /job-search/essex/paralegal-jobs | 1 | 27 | Yes |
| Detail | Regional/category | Norfolk | Legal Assistant & Paralegal | /job-search/norfolk/paralegal-jobs | 1 | 14 | Yes |
| Detail | Regional/category | London | Marketing | /job-search/london/marketing-jobs | 1 | 86 | Yes |
| Detail | Regional/category | Surrey | Marketing | /job-search/surrey/marketing-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Greater Manchester - North | Finance & Accounts | /job-search/greater-manchester-north/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Scotland Central - Fife | Admin & Customer Service | /job-search/fife/service-administrator-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Bristol & Bath | Legal Assistant & Paralegal | /job-search/bristol-bath/paralegal-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Staffordshire | Marketing | /job-search/staffordshire/marketing-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Marketing | /job-search/manchester-salford/marketing-jobs | 1 | 30 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Marketing | /job-search/birmingham-solihull/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Berkshire | HR & Recruitment | /job-search/berkshire/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | HR & Recruitment | /job-search/manchester-salford/hr-recruitment-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Nottinghamshire | HR & Recruitment | /job-search/nottinghamshire/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | HR & Recruitment | /job-search/birmingham-solihull/hr-recruitment-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Sussex | HR & Recruitment | /job-search/sussex/hr-recruitment-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Essex | HR & Recruitment | /job-search/essex/hr-recruitment-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Cheshire - West | Admin & Customer Service | /job-search/cheshire-west/service-administrator-jobs | 1 | 15 | Yes |
| Detail | Regional/category | Scotland Central - Edinburgh & Lothians | Admin & Customer Service | /job-search/edinburgh-lothians/service-administrator-jobs | 1 | 25 | Yes |
| Detail | Regional/category | Worcestershire | Admin & Customer Service | /job-search/worcestershire/service-administrator-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Berkshire | Marketing | /job-search/berkshire/marketing-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Kent | Support Worker | /job-search/kent/support-worker | 1 | 6 | Yes |
| Detail | Regional/category | North East | Customer Sales & Sales Advisor | /job-search/north-east/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Oxfordshire | Support Worker | /job-search/oxfordshire/support-worker | 1 | 2 | Yes |
| Detail | Regional/category | Yorkshire - North | Finance & Accounts | /job-search/north-yorkshire/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Northern Ireland - East | Finance & Accounts | /job-search/northern-ireland-east/finance-accounts-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Bedfordshire | Admin & Customer Service | /job-search/bedfordshire/service-administrator-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Bristol & Bath | Customer Sales & Sales Advisor | /job-search/bristol-bath/customer-sales-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Buckinghamshire | Marketing | /job-search/buckinghamshire/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Wales South - Cardiff & Vale | Admin & Customer Service | /job-search/cardiff-vale/service-administrator-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Berkshire | Customer Sales & Sales Advisor | /job-search/berkshire/customer-sales-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Hertfordshire | Customer Sales & Sales Advisor | /job-search/hertfordshire/customer-sales-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Kent | Customer Sales & Sales Advisor | /job-search/kent/customer-sales-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Customer Sales & Sales Advisor | /job-search/glasgow/customer-sales-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Surrey | Customer Sales & Sales Advisor | /job-search/surrey/customer-sales-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Sussex | Customer Sales & Sales Advisor | /job-search/sussex/customer-sales-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Bristol & Bath | Marketing | /job-search/bristol-bath/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Hertfordshire | Marketing | /job-search/hertfordshire/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Kent | Marketing | /job-search/kent/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Oxfordshire | Marketing | /job-search/oxfordshire/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | North Scotland | Admin & Customer Service | /job-search/north-scotland/service-administrator-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Scotland Central - Tayside | Admin & Customer Service | /job-search/tayside/service-administrator-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Wales South - Valleys | Admin & Customer Service | /job-search/south-wales-valleys/service-administrator-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Cambridgeshire | Marketing | /job-search/cambridgeshire/marketing-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Cheshire - West | Marketing | /job-search/cheshire-west/marketing-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Essex | Marketing | /job-search/essex/marketing-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Marketing | /job-search/merseyside-liverpool/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | North East | Marketing | /job-search/north-east/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Finance & Accounts | /job-search/warrington-halton/finance-accounts-jobs | 1 | 15 | Yes |
| Detail | Regional/category | North East | Customer Service & Contact Centre | /job-search/north-east/customer-service-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Devon | Customer Sales & Sales Advisor | /job-search/devon/customer-sales-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Hampshire | Customer Sales & Sales Advisor | /job-search/hampshire/customer-sales-jobs | 1 | 25 | Yes |
| Detail | Regional/category | Greater Manchester - South | Marketing | /job-search/greater-manchester-south/marketing-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Yorkshire - North | Marketing | /job-search/north-yorkshire/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Essex | Finance & Accounts | /job-search/essex/finance-accounts-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Finance & Accounts | /job-search/manchester-salford/finance-accounts-jobs | 1 | 23 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | HR & Recruitment | /job-search/coventry-warwickshire/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Berkshire | Finance & Accounts | /job-search/berkshire/finance-accounts-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Buckinghamshire | Finance & Accounts | /job-search/buckinghamshire/finance-accounts-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Cambridgeshire | Finance & Accounts | /job-search/cambridgeshire/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Cheshire - West | Finance & Accounts | /job-search/cheshire-west/finance-accounts-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Dorset | Finance & Accounts | /job-search/dorset/finance-accounts-jobs | 1 | 15 | Yes |
| Detail | Regional/category | Hertfordshire | Finance & Accounts | /job-search/hertfordshire/finance-accounts-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Kent | Finance & Accounts | /job-search/kent/finance-accounts-jobs | 1 | 27 | Yes |
| Detail | Regional/category | Leicestershire | Finance & Accounts | /job-search/leicestershire/finance-accounts-jobs | 1 | 23 | Yes |
| Detail | Regional/category | Norfolk | Finance & Accounts | /job-search/norfolk/finance-accounts-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Northamptonshire | Finance & Accounts | /job-search/northamptonshire/finance-accounts-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Nottinghamshire | Finance & Accounts | /job-search/nottinghamshire/finance-accounts-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Oxfordshire | Finance & Accounts | /job-search/oxfordshire/finance-accounts-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Suffolk | Finance & Accounts | /job-search/suffolk/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Surrey | Finance & Accounts | /job-search/surrey/finance-accounts-jobs | 1 | 25 | Yes |
| Detail | Regional/category | Wales South - Cardiff & Vale | Finance & Accounts | /job-search/cardiff-vale/finance-accounts-jobs | 1 | 6 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Finance & Accounts | /job-search/coventry-warwickshire/finance-accounts-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Yorkshire - South | Finance & Accounts | /job-search/south-yorkshire/finance-accounts-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Norfolk | Marketing | /job-search/norfolk/marketing-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Yorkshire - West | Marketing | /job-search/west-yorkshire/marketing-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Yorkshire - North | Legal Assistant & Paralegal | /job-search/north-yorkshire/paralegal-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Yorkshire - West | Legal Assistant & Paralegal | /job-search/west-yorkshire/paralegal-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Berkshire | Legal Assistant & Paralegal | /job-search/berkshire/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Legal Assistant & Paralegal | /job-search/manchester-salford/paralegal-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Kent | Legal Assistant & Paralegal | /job-search/kent/paralegal-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Legal Assistant & Paralegal | /job-search/merseyside-liverpool/paralegal-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Surrey | Legal Assistant & Paralegal | /job-search/surrey/paralegal-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Buckinghamshire | Legal Assistant & Paralegal | /job-search/buckinghamshire/paralegal-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Marketing | /job-search/warrington-halton/marketing-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Essex | Customer Sales & Sales Advisor | /job-search/essex/customer-sales-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Gloucestershire | HR & Recruitment | /job-search/gloucestershire/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Greater Manchester - North | Admin & Customer Service | /job-search/greater-manchester-north/service-administrator-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Hampshire | Legal Assistant & Paralegal | /job-search/hampshire/paralegal-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Herefordshire | Admin & Customer Service | /job-search/herefordshire/service-administrator-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Lancashire - East | Admin & Customer Service | /job-search/lancashire-east/service-administrator-jobs | 1 | 15 | Yes |
| Detail | Regional/category | Lincolnshire | Finance & Accounts | /job-search/lincolnshire/finance-accounts-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Finance & Accounts | /job-search/merseyside-liverpool/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Nottinghamshire | Marketing | /job-search/nottinghamshire/marketing-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Oxfordshire | Legal Assistant & Paralegal | /job-search/oxfordshire/paralegal-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Somerset | Finance & Accounts | /job-search/somerset/finance-accounts-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Staffordshire | Finance & Accounts | /job-search/staffordshire/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Sussex | Marketing | /job-search/sussex/marketing-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Wales South - Swansea Bay | Admin & Customer Service | /job-search/swansea-bay/service-administrator-jobs | 1 | 20 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Marketing | /job-search/coventry-warwickshire/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Worcestershire | Finance & Accounts | /job-search/worcestershire/finance-accounts-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Yorkshire - East | Finance & Accounts | /job-search/east-yorkshire/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Cumbria - North | Admin & Customer Service | /job-search/cumbria-north/service-administrator-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Dorset | Customer Sales & Sales Advisor | /job-search/dorset/customer-sales-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Hertfordshire | Legal Assistant & Paralegal | /job-search/hertfordshire/paralegal-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Lancashire - Central | Admin & Customer Service | /job-search/lancashire-central/service-administrator-jobs | 1 | 12 | Yes |
| Detail | Regional/category | North Wales - East | Admin & Customer Service | /job-search/north-wales-east/service-administrator-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Northamptonshire | Customer Sales & Sales Advisor | /job-search/northamptonshire/customer-sales-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Nottinghamshire | Legal Assistant & Paralegal | /job-search/nottinghamshire/paralegal-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Oxfordshire | Customer Sales & Sales Advisor | /job-search/oxfordshire/customer-sales-jobs | 1 | 15 | Yes |
| Detail | Regional/category | Scotland Central - Falkirk & Stirling | Admin & Customer Service | /job-search/falkirk-stirling/service-administrator-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Suffolk | Customer Sales & Sales Advisor | /job-search/suffolk/customer-sales-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Wales South - Gwent | Admin & Customer Service | /job-search/gwent/service-administrator-jobs | 1 | 6 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Legal Assistant & Paralegal | /job-search/coventry-warwickshire/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Yorkshire - West | Customer Service & Contact Centre | /job-search/west-yorkshire/customer-service-jobs | 1 | 16 | Yes |

## CITY OPPORTUNITIES

**518 mapped towns/localities with live jobs or an existing city page.** Counts use all 4,050 unique live Ontap jobs across every role and provider: 2,303 have an exact recognised town/locality and 1,747 have only broader or unrecognised location evidence. CREATE means 4+ current Service Admin jobs and no existing city page; London is held separately.

| Status | Town/city/locality | Region | All live jobs | Existing pages | Current routes | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre | Other / unclassified |
|---|---|---|---:|---:|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CREATE | Redditch | Worcestershire | 13 | 0 |  | 10 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| CREATE | Yeovil | Somerset | 10 | 0 |  | 9 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Carlisle | Cumbria - North | 9 | 0 |  | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Preston | Lancashire - Central | 9 | 0 |  | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Shirley | West Midlands - Birmingham & Solihull | 9 | 0 |  | 8 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Witney | Oxfordshire | 9 | 0 |  | 4 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Andover | Hampshire | 8 | 0 |  | 5 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Dundee | Scotland Central - Tayside | 8 | 0 |  | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Eastbourne | Sussex | 8 | 0 |  | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Halifax | Yorkshire - West | 8 | 0 |  | 6 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Leatherhead | Surrey | 8 | 0 |  | 6 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Hereford | Herefordshire | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Hertford | Hertfordshire | 7 | 0 |  | 6 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Stevenage | Hertfordshire | 7 | 0 |  | 5 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Chatham | Kent | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Cheltenham | Gloucestershire | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Dudley | West Midlands - Black Country | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Havant | Hampshire | 6 | 0 |  | 4 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| CREATE | Ipswich | Suffolk | 6 | 0 |  | 4 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Ripon | Yorkshire - North | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Rugby | West Midlands - Coventry & Warwickshire | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Runcorn | Cheshire - Warrington & Halton | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Stafford | Staffordshire | 6 | 0 |  | 4 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| CREATE | Sutton Coldfield | West Midlands - Birmingham & Solihull | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Welwyn Garden City | Hertfordshire | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Banbury | Oxfordshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Bracknell | Berkshire | 5 | 0 |  | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Camberley | Surrey | 5 | 0 |  | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Coalville | Leicestershire | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Crewe | Cheshire - East | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Dorking | Surrey | 5 | 0 |  | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Hatfield | Hertfordshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | High Wycombe | Buckinghamshire | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | King's Lynn | Norfolk | 5 | 0 |  | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Leigh | Greater Manchester - Wigan & Bolton | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Merthyr Tydfil | Wales South - Valleys | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Redhill | Surrey | 5 | 0 |  | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Slough | Berkshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Stratford-upon-avon | West Midlands - Coventry & Warwickshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Wigan | Greater Manchester - Wigan & Bolton | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Wrexham | North Wales - East | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Aberdeen | North Scotland | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Accrington | Lancashire - East | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Beverley | Yorkshire - East | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Burnley | Lancashire - East | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Chesham | Buckinghamshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Chesterfield | Derbyshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Halesowen | West Midlands - Black Country | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Kingswinford | West Midlands - Black Country | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Lowestoft | Suffolk | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Melksham | Wiltshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Neath | Wales South - Swansea Bay | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Newquay | Cornwall | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Oldbury | West Midlands - Black Country | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Pontypridd | Wales South - Valleys | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Richmond | Yorkshire - North | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Stirling | Scotland Central - Falkirk & Stirling | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Tamworth | Staffordshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Telford | Shropshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Tipton | West Midlands - Black Country | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Trafford | Greater Manchester - South | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Manchester | Greater Manchester - Manchester & Salford | 115 | 1 | /manchester/service-administrator-jobs | 77 | 0 | 3 | 6 | 14 | 8 | 4 | 3 | 0 |
| LIVE PAGE | Birmingham | West Midlands - Birmingham & Solihull | 94 | 1 | /birmingham/service-administrator-jobs | 74 | 0 | 0 | 0 | 4 | 13 | 3 | 0 | 0 |
| LIVE PAGE | Leeds | Yorkshire - West | 90 | 1 | /leeds/service-administrator-jobs | 56 | 0 | 1 | 3 | 14 | 8 | 4 | 4 | 0 |
| LIVE PAGE | Bristol | Bristol & Bath | 52 | 1 | /bristol/service-administrator-jobs | 37 | 0 | 9 | 3 | 3 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Liverpool | Merseyside - Liverpool | 31 | 1 | /liverpool/service-administrator-jobs | 25 | 0 | 0 | 0 | 3 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Nottingham | Nottinghamshire | 27 | 1 | /nottingham/jobs | 14 | 0 | 0 | 1 | 6 | 6 | 0 | 0 | 0 |
| LIVE PAGE | Sheffield | Yorkshire - South | 27 | 1 | /sheffield/service-administrator-jobs | 24 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Cardiff | Wales South - Cardiff & Vale | 26 | 1 | /cardiff/service-administrator-jobs | 26 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Reading | Berkshire | 26 | 1 | /reading/jobs | 17 | 0 | 7 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Hull | Yorkshire - East | 24 | 1 | /hull/service-administrator-jobs | 22 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Warrington | Cheshire - Warrington & Halton | 24 | 1 | /warrington/service-administrator-jobs | 18 | 0 | 0 | 0 | 4 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Edinburgh | Scotland Central - Edinburgh & Lothians | 23 | 1 | /edinburgh/service-administrator-jobs | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Northampton | Northamptonshire | 21 | 1 | /northampton/service-administrator-jobs | 14 | 0 | 6 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Bradford | Yorkshire - West | 20 | 1 | /bradford/service-administrator-jobs | 12 | 0 | 7 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Doncaster | Yorkshire - South | 19 | 1 | /doncaster/service-administrator-jobs | 17 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Southampton | Hampshire | 19 | 2 | /southampton/service-administrator-jobs, /southampton/support-worker | 11 | 0 | 4 | 1 | 0 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Exeter | Devon | 18 | 1 | /exeter/service-administrator-jobs | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Leicester | Leicestershire | 18 | 1 | /leicester/service-administrator-jobs | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Newcastle | North East - Tyneside, Wearside & Northumberland | 18 | 1 | /newcastle/service-administrator-jobs | 16 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| LIVE PAGE | Coventry | West Midlands - Coventry & Warwickshire | 17 | 1 | /coventry/service-administrator-jobs | 10 | 0 | 0 | 0 | 1 | 6 | 0 | 0 | 0 |
| LIVE PAGE | Milton Keynes | Buckinghamshire | 17 | 1 | /milton-keynes/service-administrator-jobs | 13 | 0 | 0 | 0 | 3 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Poole | Dorset | 17 | 1 | /poole/service-administrator-jobs | 14 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Dartford | Kent | 16 | 1 | /dartford/service-administrator-jobs | 12 | 0 | 3 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Stockport | Greater Manchester - South | 16 | 1 | /stockport/service-administrator-jobs | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Cambridge | Cambridgeshire | 15 | 1 | /cambridge/service-administrator-jobs | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Chelmsford | Essex | 15 | 1 | /chelmsford/service-administrator-jobs | 8 | 0 | 1 | 4 | 0 | 1 | 1 | 0 | 0 |
| LIVE PAGE | Portsmouth | Hampshire | 14 | 1 | /portsmouth/service-administrator-jobs | 10 | 0 | 1 | 1 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Horsham | Sussex | 13 | 1 | /horsham/service-administrator-jobs | 9 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Peterborough | Cambridgeshire | 13 | 1 | /peterborough/service-administrator-jobs | 10 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Aylesbury | Buckinghamshire | 12 | 1 | /aylesbury/service-administrator-jobs | 11 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Bath | Bristol & Bath | 12 | 1 | /bath/service-administrator-jobs | 9 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Brighton & Hove | Sussex | 12 | 1 | /brighton-hove/service-administrator-jobs | 10 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| LIVE PAGE | Chester | Cheshire - West | 12 | 1 | /chester/jobs | 10 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Ashford | Kent | 11 | 1 | /ashford/service-administrator-jobs | 6 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bolton | Greater Manchester - Wigan & Bolton | 11 | 1 | /bolton/jobs | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bournemouth | Dorset | 11 | 1 | /bournemouth/service-administrator-jobs | 7 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Eastleigh | Hampshire | 11 | 1 | /eastleigh/service-administrator-jobs | 7 | 1 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Swansea | Wales South - Swansea Bay | 11 | 1 | /swansea/service-administrator-jobs | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Swindon | Wiltshire | 11 | 1 | /swindon/service-administrator-jobs | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Walsall | West Midlands - Black Country | 11 | 1 | /walsall/service-administrator-jobs | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Crawley | Sussex | 10 | 1 | /crawley/service-administrator-jobs | 6 | 1 | 1 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Gateshead | North East - Tyneside, Wearside & Northumberland | 10 | 1 | /gateshead/jobs | 9 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Harrogate | Yorkshire - North | 10 | 1 | /harrogate/service-administrator-jobs | 6 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Maidstone | Kent | 10 | 1 | /maidstone/service-administrator-jobs | 7 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Norwich | Norfolk | 10 | 1 | /norwich/jobs | 9 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Sunderland | North East - Tyneside, Wearside & Northumberland | 10 | 1 | /sunderland/service-administrator-jobs | 9 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | York | Yorkshire - North | 10 | 1 | /york/service-administrator-jobs | 9 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Basingstoke | Hampshire | 9 | 1 | /basingstoke/service-administrator-jobs | 3 | 2 | 3 | 0 | 0 | 0 | 0 | 1 | 0 |
| LIVE PAGE | Huddersfield | Yorkshire - West | 9 | 1 | /huddersfield/service-administrator-jobs | 7 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Oxford | Oxfordshire | 9 | 1 | /oxford/service-administrator-jobs | 6 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Warwick | West Midlands - Coventry & Warwickshire | 9 | 1 | /warwick/service-administrator-jobs | 6 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 |
| LIVE PAGE | Gloucester | Gloucestershire | 8 | 1 | /gloucester/service-administrator-jobs | 6 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Lincoln | Lincolnshire | 8 | 1 | /lincoln/service-administrator-jobs | 7 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Wakefield | Yorkshire - West | 8 | 1 | /wakefield/jobs | 7 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Watford | Hertfordshire | 8 | 1 | /watford/service-administrator-jobs | 5 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Altrincham | Greater Manchester - South | 7 | 1 | /altrincham/service-administrator-jobs | 6 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Durham | North East - County Durham & Darlington/Hartlepool | 7 | 1 | /durham/jobs | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Plymouth | Devon | 6 | 1 | /plymouth/service-administrator-jobs | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Worcester | Worcestershire | 6 | 1 | /worcester/service-administrator-jobs | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Barnsley | Yorkshire - South | 5 | 1 | /barnsley/service-administrator-jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Hemel Hempstead | Hertfordshire | 5 | 1 | /hemel-hempstead/service-administrator-jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Northallerton | Yorkshire - North | 5 | 1 | /northallerton/jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Salford | Greater Manchester - Manchester & Salford | 5 | 1 | /salford/jobs | 3 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Stoke-on-trent | Staffordshire | 5 | 1 | /stoke-on-trent/service-administrator-jobs | 4 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bedford | Bedfordshire | 4 | 1 | /bedford/service-administrator-jobs | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Farnham | Surrey | 4 | 1 | /farnham/service-administrator-jobs | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Glasgow | Scotland West - Glasgow | 4 | 1 | /glasgow/service-administrator-jobs | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Macclesfield | Cheshire - East | 4 | 1 | /macclesfield/service-administrator-jobs | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Scarborough | Yorkshire - North | 4 | 1 | /scarborough/service-administrator-jobs | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Shrewsbury | Shropshire | 4 | 1 | /shrewsbury/service-administrator-jobs | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Belfast | Northern Ireland - East | 3 | 1 | /belfast/service-administrator-jobs | 1 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Rotherham | Yorkshire - South | 3 | 1 | /rotherham/service-administrator-jobs | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Chester Le Street |  | 0 | 1 | /chester-le-street/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Newtownabbey |  | 0 | 1 | /newtownabbey/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wigston |  | 0 | 1 | /wigston/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Uxbridge | London | 14 | 0 |  | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Croydon | London | 8 | 0 |  | 2 | 1 | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Sutton | London | 8 | 0 |  | 5 | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Sutton-in-ashfield | London | 8 | 0 |  | 7 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hayes | London | 7 | 0 |  | 4 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Barking | London | 5 | 0 |  | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Bromley | London | 5 | 0 |  | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Chessington | London | 5 | 0 |  | 2 | 0 | 1 | 0 | 2 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Harrow | London | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Kingston Upon Thames | London | 5 | 0 |  | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Romford | London | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Hillingdon | London | 4 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| HOLD – LONDON | Hornchurch | London | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Loughton | London | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wallington | London | 4 | 0 |  | 0 | 1 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| HOLD – LONDON | Borehamwood | London | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| HOLD – LONDON | Enfield | London | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hounslow | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Islington | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Ruislip | London | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Southwark | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Surbiton | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Barnet | London | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Beckenham | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Greenford | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hackney | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Isleworth | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Lambeth | London | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Newham | London | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Orpington | London | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Bexleyheath | London | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Brentford | London | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Broxbourne | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Bushey | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Carshalton | London | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Chislehurst | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | City Of Westminster | London | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Edgware | London | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Mitcham | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Sidcup | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | South Croydon | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Southall | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Teddington | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Welling | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wembley | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | West Drayton | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Guildford | Surrey | 11 | 0 |  | 3 | 0 | 5 | 1 | 0 | 1 | 0 | 1 | 0 |
| MONITOR | Daventry | Northamptonshire | 7 | 0 |  | 0 | 0 | 6 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | East Grinstead | Sussex | 7 | 0 |  | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 2 | 0 |
| MONITOR | Burgess Hill | Sussex | 6 | 0 |  | 2 | 0 | 2 | 0 | 1 | 0 | 0 | 1 | 0 |
| MONITOR | Hook Norton | Oxfordshire | 6 | 0 |  | 1 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Canterbury | Kent | 5 | 0 |  | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fareham | Hampshire | 5 | 0 |  | 0 | 0 | 3 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Malton | Yorkshire - North | 5 | 0 |  | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Mansfield | Nottinghamshire | 5 | 0 |  | 3 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newbury | Berkshire | 5 | 0 |  | 0 | 0 | 4 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Solihull | West Midlands - Birmingham & Solihull | 5 | 0 |  | 3 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Winchester | Hampshire | 5 | 0 |  | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Basildon | Essex | 4 | 0 |  | 1 | 0 | 1 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Brighouse | Yorkshire - West | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chichester | Sussex | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Corby | Northamptonshire | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Darlington | North East - County Durham & Darlington/Hartlepool | 4 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dereham | Norfolk | 4 | 0 |  | 2 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Droitwich | Worcestershire | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Epsom | Surrey | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Harlow | Essex | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hastings | Sussex | 4 | 0 |  | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Southend-on-sea | Essex | 4 | 0 |  | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tunbridge Wells | Kent | 4 | 0 |  | 2 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Woking | Surrey | 4 | 0 |  | 2 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Wokingham | Berkshire | 4 | 0 |  | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Abingdon | Oxfordshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Aldershot | Hampshire | 3 | 0 |  | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Batley | Yorkshire - West | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Billericay | Essex | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bognor Regis | Sussex | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brentwood | Essex | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Bridlington | Yorkshire - East | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bury St. Edmunds | Suffolk | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cannock | Staffordshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Castleford | Yorkshire - West | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chorley | Lancashire - Central | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Colchester | Essex | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Crowthorne | Berkshire | 3 | 0 |  | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Didcot | Oxfordshire | 3 | 0 |  | 1 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| MONITOR | Diss | Norfolk | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dorchester | Dorset | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Emsworth | Hampshire | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Farnborough | Hampshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Felixstowe | Suffolk | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fleet | Hampshire | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Horley | Surrey | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Huntingdon | Cambridgeshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kettering | Northamptonshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leamington Spa | West Midlands - Coventry & Warwickshire | 3 | 0 |  | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ledbury | Herefordshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Maidenhead | Berkshire | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Malvern | Worcestershire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Middleton | Greater Manchester - North | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newport | Wales South -gwent | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newton Abbot | Devon | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Oldham | Greater Manchester - North | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rochester | Kent | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ross-on-wye | Herefordshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Salisbury | Wiltshire | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sittingbourne | Kent | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Southam | West Midlands - Coventry & Warwickshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Albans | Hertfordshire | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Ives | Cambridgeshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Swanley | Kent | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Taunton | Somerset | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Trowbridge | Wiltshire | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Walton-on-thames | Surrey | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weston-super-mare | Somerset | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wetherby | Yorkshire - West | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Widnes | Cheshire - Warrington & Halton | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Windsor | Berkshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ascot | Berkshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Barnstaple | devon | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Beaminster | Dorset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bicester | Oxfordshire | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Bishop's Stortford | Hertfordshire | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Blackburn | Lancashire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Blyth | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Boston | Lincolnshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridgend | Wales South - Swansea Bay | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brinsworth | Yorkshire - South | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Buckingham | Buckinghamshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bury | Greater Manchester - North | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Caerphilly | Wales South - Valleys | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Caterham | Surrey | 2 | 0 |  | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cheadle | Greater Manchester - South | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chelmsley Wood | West Midlands - Birmingham & Solihull | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cirencester | Gloucestershire | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Clacton-on-sea | Essex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Devizes | Wiltshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dunmow | Essex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dunstable | Bedfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Elland | Yorkshire - West | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ely | Cambridgeshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Esher | Surrey | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Evesham | Worcestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ferndown | Dorset | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Flint | North Wales - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gosport | Hampshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grantham | Lincolnshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Great Yarmouth | Norfolk | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Grimsby | Lincolnshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hailsham | Sussex | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Haslemere | Surrey | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Henley-on-thames | Oxfordshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hessle | Yorkshire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hook | Hampshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hornsea | Yorkshire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Houghton Le Spring | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Inverness | North Scotland | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Keighley | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kidlington | Oxfordshire | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knaresborough | Yorkshire - North | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knowle | West Midlands - Birmingham & Solihull | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knutsford | Cheshire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lichfield | Staffordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lisburn | Northern Ireland - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Livingston | Scotland Central - Edinburgh & Lothians | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Loughborough | Leicestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Luton | Bedfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Mirfield | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Montrose | North Scotland | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newton Aycliffe | North East - County Durham & Darlington/Hartlepool | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Normanton | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Northfleet | Kent | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Northwich | Cheshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Otley | Yorkshire - West | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pershore | Worcestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Perth | Scotland Central - Tayside | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Petersfield | Hampshire | 2 | 0 |  | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Port Talbot | Wales South - Swansea Bay | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ramsbottom | Greater Manchester - North | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Redruth | Cornwall | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Reigate | Surrey | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rochdale | Greater Manchester - North | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Romsey | Hampshire | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Royston | Hertfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rugeley | Staffordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rushden | Northamptonshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sandy | Bedfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Scunthorpe | Lincolnshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Selby | Yorkshire - North | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sevenoaks | Kent | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shepperton | Surrey | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Staines | Surrey | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stonehouse | Gloucestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sudbury | Suffolk | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Swadlincote | Derbyshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Takeley | Essex | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Thatcham | Berkshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tonbridge | Kent | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Torquay | Devon | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tredegar | Wales South - Gwent | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Waltham Abbey | Essex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ware | Hertfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Waterlooville | Hampshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wednesbury | West Midlands - Black Country | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wellingborough | Northamptonshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weymouth | Dorset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Whitstable | Kent | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wilmslow | Cheshire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Winsford | Cheshire - West | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Worsley | Greater Manchester - Manchester & Salford | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Worthing | Sussex | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Yate | Bristol & Bath | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Abergavenny | Wales South - Gwent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Addlestone | Surrey | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Alcester | West Midlands - Coventry & Warwickshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Alderley Edge | Cheshire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Alnwick | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Alton | Hampshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Amersham | Buckinghamshire | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Arbroath | Scotland Central - Tayside | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ashington | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ashton-under-lyne | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Attleborough | Norfolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Aylesford | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bagshot | Surrey | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Beaconsfield | Buckinghamshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Beccles | Suffolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bedlington | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Belper | Derbyshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Benfleet | Essex | 1 | 0 |  | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Bentley | Yorkshire - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bideford | Devon | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Biggleswade | Bedfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Billingham | North East - Tees Valley | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Bingley | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Blandford Forum | Dorset | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Braintree | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brampton | Cumbria - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridgwater | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Broadstone | Dorset | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Buckhurst Hill | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Burford | Oxfordshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bury St Edmunds | Suffolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Camborne | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Carryduff | Northern Ireland - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Catterick Garrison | Yorkshire - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cheddar | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chertsey | Surrey | 1 | 0 |  | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Christchurch | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cleethorpes | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Clevedon | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Clitheroe | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cobham | Surrey | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Colden Common | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Colne | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Colwyn Bay | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Corbridge | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cottingham | Yorkshire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cradley Heath | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cramlington | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cranleigh | Surrey | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cullompton | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Darwen | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Denton | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dingwall | North Scotland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Downham Market | Norfolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dursley | Gloucestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Eccles | Greater Manchester - Manchester & Salford | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Edenbridge | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Egham | Surrey | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ellesmere Port | Cheshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Falkirk | Scotland Central - Falkirk & Stirling | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Falmouth | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Featherstone | Yorkshire - West | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ferryhill | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fetcham | Surrey | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Filey | Yorkshire - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Folkestone | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fordingbridge | Hampshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Forfar | Scotland Central - Tayside | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Frodsham | Cheshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gillingham | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Glastonbury | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Glenfield | Leicestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Glenrothes | Scotland Central - Fife | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Godalming | Surrey | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Goole | Yorkshire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grange-over-sands | Cumbria - South | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grangemouth | Scotland Central - Falkirk & Stirling | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gravesend | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Halstead | Essex | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Hartlepool | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Harwich | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Haslingden | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hayling Island | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Haywards Heath | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Heanor | Derbyshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Helston | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hitchin | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hockley | Essex | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hoddesdon | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Holmfirth | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ilkeston | Derbyshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Irchester | Northamptonshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kendal | Cumbria - South | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kenilworth | West Midlands - Coventry & Warwickshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Keynsham | Bristol & Bath | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kidderminster | Worcestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kingsbridge | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kirkcaldy | Scotland Central - Fife | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knaphill | Surrey | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Langport | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leigh-on-sea | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leighton Buzzard | Bedfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lewes | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lymm | Cheshire - Warrington & Halton | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Maesteg | Wales South - Swansea Bay | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Maldon | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Margate | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Marlborough | Wiltshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Morley | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Nantwich | Cheshire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | New Romney | Kent | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newark | Nottinghamshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newhaven | Sussex | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newmarket | Suffolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Nuneaton | West Midlands - Coventry & Warwickshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Okehampton | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ossett | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Oswestry | Shropshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Penrith | Cumbria - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Penzance | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Peterlee | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pitlochry | Scotland Central - Tayside | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pontyclun | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Potters Bar | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Potton | Bedfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pudsey | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ramsgate | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ringwood | Hampshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rossendale | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sale | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Seaham | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shaftesbury | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shepton Mallet | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sherborne | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shipley | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shoreham-by-sea | Sussex | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Smethwick | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Snodland | Kent | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | South Shields | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stamford | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stanley | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stone | Staffordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stourbridge | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stowmarket | Suffolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Street | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stroud | Gloucestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tadley | Hampshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Teignmouth | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tilbury | Essex | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tiptree | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tiverton | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Totnes | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Totton | Hampshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tring | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Truro | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Uckfield | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Uttoxeter | Staffordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Verwood | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wantage | Oxfordshire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Washington | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | West Bromwich | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | West Malling | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Westbury | Wiltshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weybridge | Surrey | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wickford | Essex | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wigton | Cumbria - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wimborne | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wisbech | Cambridgeshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Woodbridge | Suffolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Worksop | Nottinghamshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

> LIVE counts come directly from the current published `app/` JSON, deduplicated within each canonical region/family slice while preserving legitimate appearances in more than one family. This is the live-site authority for the reconciliation above; the dated source-count CSV is shown only as a freshness cross-check. The overview covers all 78 assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 78-market coverage has run, NOT LIVE Admin/Support and Customer Service may fall back to the latest all-region Module 2 profile (2026-08-17), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-10-19) used by the production family run, across 78 UK markets with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across 78 UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across 78, 78, 78 and 78 UK markets respectively, using their governed production boundaries and canonical geo. NOT LIVE Customer Service / Contact Centre was assessed from that same feed across 78 UK markets using its governed exact-title, salary and geography rules. All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

## LIVE

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire | 36 |  |  |  |  |  |  |  |
| Berkshire | 70 |  | 20 | 8 | 12 | 15 | 3 |  |
| Bristol & Bath | 59 |  | 13 | 5 | 5 | 12 |  |  |
| Buckinghamshire | 66 |  |  | 5 | 9 | 16 |  | CHECK |
| Cambridgeshire | 47 |  |  |  | 4 | 11 |  |  |
| Cheshire - East | 15 |  |  |  |  | CHECK |  |  |
| Cheshire - Warrington & Halton | 33 |  |  |  | 4 | 15 |  |  |
| Cheshire - West | 15 |  |  |  | 2 | 8 |  |  |
| Cornwall | 11 |  |  |  |  |  |  |  |
| Cumbria - North | 12 |  |  |  |  |  |  |  |
| Cumbria - South |  | 2 |  |  |  |  |  |  |
| Cumbria - West |  |  |  |  |  |  |  |  |
| Derbyshire | 34 |  |  |  |  |  |  |  |
| Devon | 65 |  | 2 |  |  | CHECK |  |  |
| Dorset | 57 |  | 9 |  |  | 15 |  |  |
| Essex | 83 |  | 11 | 26 | 6 | 25 | 7 |  |
| Gloucestershire | 52 |  |  |  | CHECK | 17 | 4 |  |
| Greater Manchester - Manchester & Salford | 118 |  | 9 | 10 | 30 | 22 | 7 | 10 |
| Greater Manchester - North | 12 |  |  |  |  | 9 |  |  |
| Greater Manchester - South | 34 |  |  |  | 1 |  |  |  |
| Greater Manchester - Wigan & Bolton | 21 |  |  |  |  |  |  |  |
| Hampshire | 133 | 9 | 25 | 12 |  | 38 | 13 | 9 |
| Herefordshire | 13 |  |  |  |  |  |  |  |
| Hertfordshire | 94 |  | 9 | 9 | 10 | 26 |  |  |
| Kent | 101 | 6 | 20 | 5 | 10 | 27 |  |  |
| Lancashire - Blackpool & Fylde |  |  |  |  |  |  |  |  |
| Lancashire - Central | 12 |  |  |  |  |  |  |  |
| Lancashire - East | 15 |  |  |  |  | CHECK |  |  |
| Lancashire - North |  |  |  |  |  |  |  |  |
| Lancashire - West |  |  |  |  |  |  |  |  |
| Leicestershire | 61 |  |  |  |  | 22 |  |  |
| Lincolnshire | 36 |  |  |  |  | 7 |  |  |
| London | 351 | 33 | 83 | 59 | 83 | 87 | 36 | 8 |
| Merseyside - Liverpool | 31 |  |  | 1 | 5 | 9 |  |  |
| Merseyside - Sefton |  |  |  |  |  |  |  |  |
| Merseyside - St Helens & Knowsley |  |  |  |  |  |  |  |  |
| Merseyside - Wirral |  |  |  |  |  |  |  |  |
| Norfolk | 50 |  |  | 14 | 6 | 20 |  |  |
| North East | 99 | 3 | 8 |  | 9 | 30 |  | 5 |
| North Scotland | 9 |  | CHECK |  |  |  |  |  |
| North Wales - East | 8 |  |  |  |  |  |  |  |
| North Wales - West |  |  |  |  |  |  |  |  |
| Northamptonshire | 57 |  | 16 |  |  | 16 |  |  |
| Northern Ireland - East | 6 |  |  |  | CHECK | 6 | CHECK |  |
| Northern Ireland - West |  |  |  |  |  |  |  |  |
| Nottinghamshire | 50 |  |  | 6 | 11 | 16 | 3 |  |
| Oxfordshire | 61 | 2 | 15 | 2 | 5 | 19 |  |  |
| Rutland |  |  |  |  |  |  |  |  |
| Scotland - Borders |  |  |  |  |  |  |  |  |
| Scotland Central - Edinburgh & Lothians | 25 |  |  |  |  |  |  |  |
| Scotland Central - Falkirk & Stirling | 6 |  |  |  |  |  |  |  |
| Scotland Central - Fife | 6 |  |  |  |  |  |  |  |
| Scotland Central - Tayside | 13 |  |  |  |  |  |  |  |
| Scotland West - Ayrshire |  |  |  |  |  |  |  |  |
| Scotland West - Glasgow | 2 |  | 10 |  |  |  |  |  |
| Scotland West - Lanarkshire |  |  |  |  |  |  |  |  |
| Scotland West - Renfrewshire & Inverclyde |  |  |  |  |  |  |  |  |
| Shropshire | 19 |  |  |  |  | CHECK |  |  |
| Somerset | 38 |  |  |  |  | 7 |  |  |
| Staffordshire | 47 |  |  |  | 6 | 8 |  | 2 |
| Suffolk | 40 |  | 6 | 24 |  | 11 |  |  |
| Surrey | 115 | 7 | 12 | 17 | 20 | 25 |  | 8 |
| Sussex | 86 | 12 | 11 |  | 12 | 36 | 2 | 9 |
| Wales - Mid |  |  |  |  |  |  |  |  |
| Wales - West |  |  |  |  |  |  |  |  |
| Wales South - Cardiff & Vale | 26 |  |  |  |  | 6 |  |  |
| Wales South - Gwent | 6 |  |  |  |  |  |  |  |
| Wales South - Swansea Bay | 20 |  |  |  |  |  |  |  |
| Wales South - Valleys | 12 |  |  |  |  |  |  |  |
| West Midlands - Birmingham & Solihull | 115 |  |  | CHECK | 8 | 29 | 8 |  |
| West Midlands - Black Country | 54 |  |  |  |  |  |  |  |
| West Midlands - Coventry & Warwickshire | 68 |  |  | 8 | 9 | 26 | 3 |  |
| Wiltshire | 33 | 4 |  |  |  | CHECK |  |  |
| Worcestershire | 37 |  |  |  |  | 19 |  |  |
| Yorkshire - East | 37 |  |  |  |  | 9 |  |  |
| Yorkshire - North | 45 |  |  | 17 | 5 | 10 |  |  |
| Yorkshire - South | 57 | CHECK |  |  |  | 14 |  |  |
| Yorkshire - West | 152 | 1 | 17 | 10 | 20 | 26 | 7 | 16 |

## NOT LIVE

> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire |  | 0 / 0.1 / 0/14 | 5 / 2.1 / 0/14 | 1 / 2.0 / 0/14 | 2 / 0.7 / 0/14 | 6 / 3.4 / 3/14 | 0 / 0.0 / 0/14 | 4 / 2.7 / 0/14 |
| Berkshire |  | 4 / 1.9 / 0/14 |  |  |  |  |  | 2 / 1.2 / 0/14 |
| Bristol & Bath |  | 4 / 1.9 / 0/14 |  |  |  |  | 3 / 1.3 / 0/14 | 2 / 0.8 / 0/14 |
| Buckinghamshire |  | 0 / 0.1 / 0/14 | 7 / 2.1 / 3/14 |  |  |  | 1 / 0.7 / 0/14 |  |
| Cambridgeshire |  | 1 / 0.4 / 0/14 | 9 / 3.1 / 3/14 | 3 / 2.4 / 1/14 |  |  | 0 / 0.4 / 0/14 | 2 / 1.1 / 0/14 |
| Cheshire - East |  | 0 / 0.4 / 0/14 | 6 / 3.4 / 6/14 | 0 / 0.1 / 0/14 | 1 / 0.5 / 0/14 |  | 2 / 1.6 / 0/14 | 2 / 1.6 / 0/14 |
| Cheshire - Warrington & Halton |  | 0 / 0.0 / 0/14 | 4 / 1.8 / 0/14 | 2 / 2.1 / 0/14 |  |  | 2 / 0.6 / 0/14 | 2 / 1.0 / 0/14 |
| Cheshire - West |  | 0 / 0.5 / 0/14 | 2 / 0.9 / 0/14 | 2 / 1.2 / 0/14 |  |  | 1 / 0.4 / 0/14 | 1 / 0.5 / 0/14 |
| Cornwall |  | 2 / 1.1 / 0/14 | 1 / 0.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 7 / 6.3 / 9/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Cumbria - North |  | 0 / 1.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.4 / 0/14 | 3 / 3.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 |
| Cumbria - South | 1 / 1.2 / 0/14 |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.2 / 0/14 | 1 / 1.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Cumbria - West | 3 / 1.5 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Derbyshire |  | 1 / 0.6 / 0/14 | 3 / 1.4 / 0/14 | 3 / 2.0 / 0/14 | 1 / 0.6 / 0/14 | 7 / 4.1 / 5/14 | 6 / 2.5 / 3/14 | 0 / 0.1 / 0/14 |
| Devon |  | 4 / 2.7 / 0/14 |  | 4 / 2.7 / 0/14 | 3 / 1.4 / 0/14 |  | 5 / 2.4 / 0/14 | 3 / 1.3 / 0/14 |
| Dorset |  | 2 / 0.9 / 0/14 |  | 4 / 3.3 / 0/14 | 5 / 2.2 / 0/14 |  | 2 / 0.9 / 0/14 | 2 / 0.8 / 0/14 |
| Essex |  | 5 / 3.0 / 0/14 |  |  |  |  |  | 3 / 1.9 / 0/14 |
| Gloucestershire |  | 2 / 0.8 / 0/14 | 7 / 2.3 / 3/14 | 4 / 1.9 / 0/14 |  |  |  | 1 / 0.7 / 0/14 |
| Greater Manchester - Manchester & Salford |  | 3 / 0.4 / 0/14 |  |  |  |  |  |  |
| Greater Manchester - North |  | 1 / 0.5 / 0/14 | 1 / 0.2 / 0/14 | 1 / 0.3 / 0/14 | 0 / 0.1 / 0/14 |  | 0 / 0.1 / 0/14 | 0 / 0.5 / 0/14 |
| Greater Manchester - South |  | 0 / 0.8 / 0/14 | 3 / 1.4 / 0/14 | 1 / 1.2 / 0/14 |  | 3 / 2.1 / 0/14 | 4 / 1.8 / 0/14 | 1 / 0.5 / 0/14 |
| Greater Manchester - Wigan & Bolton |  | 0 / 0.1 / 0/14 | 1 / 0.7 / 0/14 | 0 / 0.1 / 0/14 | 2 / 0.7 / 0/14 | 4 / 3.3 / 0/14 | 2 / 0.7 / 0/14 | 3 / 1.5 / 0/14 |
| Hampshire |  |  |  |  | 5 / 3.1 / 2/14 |  |  |  |
| Herefordshire |  | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.2 / 0/14 | 7 / 5.8 / 6/14 | 0 / 0.0 / 0/14 | 1 / 0.5 / 0/14 |
| Hertfordshire |  | 0 / 0.2 / 0/14 |  |  |  |  | 5 / 2.9 / 1/14 | 8 / 3.9 / 7/14 |
| Kent |  |  |  |  |  |  | 5 / 3.0 / 2/14 | 6 / 3.0 / 7/14 |
| Lancashire - Blackpool & Fylde | 3 / 2.2 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - Central |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.5 / 0/14 | 3 / 2.7 / 1/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - East |  | 0 / 0.5 / 0/14 | 2 / 1.4 / 0/14 | 1 / 0.8 / 0/14 | 1 / 0.5 / 0/14 |  | 1 / 0.5 / 0/14 | 2 / 0.7 / 0/14 |
| Lancashire - North | 1 / 0.5 / 0/14 | 1 / 1.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.4 / 0/14 | 1 / 1.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - West | 0 / 0.2 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.3 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.2 / 0/14 | 1 / 1.1 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.1 / 0/14 |
| Leicestershire |  | 0 / 0.0 / 0/14 | 6 / 2.8 / 4/14 | 3 / 2.0 / 0/14 | 4 / 3.0 / 0/14 |  | 7 / 2.9 / 4/14 | 2 / 1.3 / 0/14 |
| Lincolnshire |  | 1 / 0.8 / 0/14 | 5 / 3.1 / 0/14 | 4 / 2.6 / 0/14 | 5 / 4.6 / 0/14 |  | 2 / 1.5 / 0/14 | 0 / 0.0 / 0/14 |
| London |  |  |  |  |  |  |  |  |
| Merseyside - Liverpool |  | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 |  |  |  | 0 / 0.1 / 0/14 | 1 / 0.5 / 0/14 |
| Merseyside - Sefton | 1 / 0.9 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.4 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Merseyside - St Helens & Knowsley | 8 / 5.0 / 8/14 | 0 / 0.1 / 0/14 | 1 / 0.7 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Merseyside - Wirral | 4 / 2.5 / 0/14 | 0 / 0.1 / 0/14 | 1 / 0.4 / 0/14 | 1 / 1.1 / 0/14 | 4 / 2.2 / 0/14 | 2 / 1.5 / 0/14 | 1 / 0.5 / 0/14 | 0 / 0.0 / 0/14 |
| Norfolk |  | 3 / 3.4 / 2/14 | 6 / 2.6 / 3/14 |  |  |  | 4 / 2.1 / 0/14 | 0 / 0.0 / 0/14 |
| North East |  |  |  | 4 / 3.6 / 0/14 |  |  | 10 / 4.8 / 6/14 |  |
| North Scotland |  | 0 / 0.0 / 0/14 |  | 5 / 3.4 / 1/14 | 0 / 0.0 / 0/14 | 3 / 3.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 |
| North Wales - East |  | 0 / 0.3 / 0/14 | 1 / 1.6 / 1/14 | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 | 2 / 2.3 / 0/14 | 2 / 0.9 / 0/14 | 1 / 0.1 / 0/14 |
| North Wales - West | 2 / 1.3 / 0/14 | 1 / 0.5 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 | 2 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Northamptonshire |  | 1 / 0.7 / 0/14 |  | 4 / 3.1 / 0/14 | 9 / 5.1 / 7/14 |  | 6 / 2.6 / 2/14 | 2 / 1.0 / 0/14 |
| Northern Ireland - East |  | 0 / 0.0 / 0/14 | 0 / 0.3 / 0/14 | 0 / 0.3 / 0/14 |  |  |  | 0 / 0.0 / 0/14 |
| Northern Ireland - West | 2 / 1.6 / 0/14 | 0 / 0.0 / 0/14 | 3 / 1.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.2 / 0/14 | 1 / 0.5 / 0/14 | 0 / 0.0 / 0/14 |
| Nottinghamshire |  | 2 / 1.0 / 0/14 | 11 / 4.8 / 6/14 |  |  |  |  | 4 / 1.9 / 0/14 |
| Oxfordshire |  |  |  |  |  |  | 1 / 0.4 / 0/14 | 2 / 0.8 / 0/14 |
| Rutland | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland - Borders | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Edinburgh & Lothians |  | 0 / 0.0 / 0/14 | 0 / 0.2 / 0/14 | 2 / 2.1 / 0/14 | 1 / 1.2 / 0/14 | 2 / 1.6 / 1/14 | 0 / 0.2 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Falkirk & Stirling |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 3 / 1.7 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Fife |  | 0 / 0.0 / 0/14 | 2 / 0.6 / 0/14 | 1 / 0.5 / 0/14 | 1 / 0.7 / 0/14 | 4 / 2.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Tayside |  | 1 / 0.2 / 0/14 | 3 / 1.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.3 / 0/14 | 1 / 0.2 / 0/14 | 1 / 0.3 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland West - Ayrshire | 1 / 0.7 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 0.7 / 0/14 |
| Scotland West - Glasgow |  | 0 / 0.0 / 0/14 |  | 6 / 4.3 / 3/14 | 8 / 4.1 / 7/14 | 5 / 3.4 / 0/14 | 2 / 0.8 / 0/14 | 5 / 2.8 / 4/14 |
| Scotland West - Lanarkshire | 3 / 2.5 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.0 / 0/14 | 1 / 0.4 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland West - Renfrewshire & Inverclyde | 3 / 2.2 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.6 / 0/14 | 0 / 0.0 / 0/14 |
| Shropshire |  | 3 / 1.1 / 0/14 | 3 / 1.1 / 0/14 | 0 / 0.1 / 0/14 | 1 / 0.6 / 0/14 |  | 2 / 1.6 / 0/14 | 3 / 1.8 / 0/14 |
| Somerset |  | 2 / 2.1 / 0/14 | 2 / 2.1 / 0/14 | 1 / 0.5 / 0/14 | 2 / 1.4 / 0/14 |  | 1 / 0.9 / 0/14 | 3 / 1.5 / 0/14 |
| Staffordshire |  | 1 / 0.4 / 0/14 | 5 / 1.8 / 0/14 | 3 / 3.1 / 0/14 |  |  | 8 / 3.8 / 6/14 |  |
| Suffolk |  | 1 / 0.8 / 0/14 |  |  | 4 / 1.4 / 0/14 |  | 6 / 2.8 / 4/14 | 1 / 0.5 / 0/14 |
| Surrey |  |  |  |  |  |  | 9 / 4.2 / 6/14 |  |
| Sussex |  |  |  | 4 / 2.8 / 0/14 |  |  |  |  |
| Wales - Mid | 3 / 1.2 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Wales - West | 1 / 0.6 / 0/14 | 1 / 0.2 / 0/14 | 1 / 0.3 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Cardiff & Vale |  | 0 / 0.0 / 0/14 | 0 / 0.2 / 0/14 | 1 / 1.1 / 0/14 | 0 / 0.2 / 0/14 |  | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Gwent |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.0 / 0/14 | 1 / 0.4 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Swansea Bay |  | 1 / 0.2 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 4 / 3.1 / 0/14 | 1 / 0.4 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Valleys |  | 0 / 0.0 / 0/14 | 2 / 2.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.3 / 0/14 | 0 / 0.1 / 0/14 | 4 / 2.4 / 0/14 |
| West Midlands - Birmingham & Solihull |  | 0 / 0.0 / 0/14 | 1 / 0.4 / 0/14 |  |  |  |  | 4 / 2.4 / 0/14 |
| West Midlands - Black Country |  | 0 / 0.0 / 0/14 | 2 / 0.6 / 0/14 | 1 / 1.8 / 0/14 | 3 / 1.9 / 0/14 | 12 / 5.8 / 6/14 | 5 / 2.3 / 0/14 | 4 / 1.7 / 0/14 |
| West Midlands - Coventry & Warwickshire |  | 3 / 0.9 / 0/14 | 7 / 3.4 / 5/14 |  |  |  |  | 2 / 0.9 / 0/14 |
| Wiltshire |  |  | 1 / 0.9 / 0/14 | 1 / 2.2 / 2/14 | 1 / 1.4 / 0/14 |  | 0 / 0.1 / 0/14 | 1 / 0.5 / 0/14 |
| Worcestershire |  | 0 / 0.1 / 0/14 | 9 / 3.6 / 5/14 | 2 / 2.9 / 0/14 | 2 / 0.6 / 0/14 |  | 0 / 0.0 / 0/14 | 3 / 1.5 / 0/14 |
| Yorkshire - East |  | 0 / 0.1 / 0/14 | 4 / 1.3 / 0/14 | 3 / 2.0 / 0/14 | 1 / 0.2 / 0/14 |  | 1 / 0.5 / 0/14 | 1 / 0.5 / 0/14 |
| Yorkshire - North |  | 0 / 0.0 / 0/14 | 2 / 0.9 / 0/14 |  |  |  | 1 / 0.6 / 0/14 | 2 / 1.7 / 0/14 |
| Yorkshire - South |  |  | 3 / 2.1 / 0/14 | 4 / 2.6 / 0/14 | 7 / 5.4 / 5/14 |  | 3 / 1.6 / 0/14 | 4 / 2.2 / 0/14 |
| Yorkshire - West |  |  |  |  |  |  |  |  |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Live regions | 61 / 78 | 11 / 78 | 19 / 78 | 19 / 78 | 26 / 78 | 42 / 78 | 12 / 78 | 9 / 78 |
| Live slice placements | 3086 | 79 + 1 CHECK | 296 + 1 CHECK | 238 + 1 CHECK | 292 + 2 CHECK | 714 + 5 CHECK | 93 + 1 CHECK | 67 + 1 CHECK |

**Live slices: 199 / 624.**
