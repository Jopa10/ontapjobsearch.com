# Ontap daily regional overview

Production source commit: `b07c183feed32682fbbe8ef5e2f78cd7f087b383`

Generated: 2026-11-20T09:56:53+00:00

[Download this overview as Excel](./daily-region-overview.xlsx)

## SITEWIDE RECONCILIATION

| Measure | Count |
|---|---:|
| Unique live jobs | 5,758 |
| Unique JobG8 jobs | 5,435 |
| Unique non-JobG8 jobs | 323 |
| Regional/category slice placements | 7,335 |
| Jobs appearing on multiple slices | 1,560 |
| Extra slice placements | 1,577 |
| Unique jobs outside governed slices | 0 |
| Jobs found in non-LIVE slices | 0 |

**Reconciliation: 5,758 unique jobs + 1,577 extra slice placements = 7,335 regional/category slice placements.**

Latest source-count CSV: `pipeline/reports-daily/live-job-source-count-2026-11-20.csv` — **STALE — CSV says 6,395 for 2026-11-20**.

### Provider breakdown

| Provider | Unique live jobs | Jobs on 2+ slices | Extra slice placements |
|---|---:|---:|---:|
| JobG8 | 5,435 | 1,560 | 1,577 |
| NHS Jobs | 306 | 0 | 0 |
| Teaching Vacancies | 17 | 0 | 0 |

## JOBG8 FEED RECEIVED

**JobG8 jobs received: 43,256** (feed date: 2026-11-20)

| JobG8 classification | Jobs received | Ontap jobs classified/published |
|---|---:|---:|
| Transport & Logistics | 8,194 | 180 |
| Accounting | 7,931 | 1,738 |
| Education | 7,369 | 48 |
| Healthcare & Medical | 4,470 | 403 |
| Sales & Marketing | 3,320 | 929 |
| Legal | 2,584 | 410 |
| Banking & Financial Services | 1,814 | 57 |
| Administration | 1,607 | 1,042 |
| Real Estate & Property | 1,334 | 73 |
| HR / Recruitment | 1,183 | 141 |
| I.T. & Communications | 1,050 | 1 |
| Insurance & Superannuation | 793 | 25 |
| Call Centre / CustomerService | 735 | 368 |
| Community & Sport | 514 | 67 |
| Government & Defence | 238 | 8 |
| Advert / Media / Entertainment | 120 | 16 |
| Total across classifications | 43,256 | 5,506 |

## JOBG8 XML RECONCILIATION

| Check | XML feed total | Sum of ‘Jobs received’ | Difference (sum − XML) | Result |
|---|---:|---:|---:|---|
| JobG8 feed categories | 43,256 | 43,256 | 0 | **PASS** |

**JobG8 feed reconciliation: PASS.** Difference is 0 jobs (summed categories minus XML total).

## JOBG8 LAST 10 FEED DATES — TOTALS ONLY

Saved history contains 10 of the latest 10 feed dates. Older feed totals were not saved and are not backfilled.

| Feed date | JobG8 jobs received | Ontap jobs classified/published |
|---|---:|---:|
| 2026-11-20 | 43,256 | 5,506 |
| 2026-11-19 | 43,590 | 5,586 |
| 2026-11-18 | 40,302 | 5,431 |
| 2026-11-17 | 40,395 | 5,372 |
| 2026-11-16 | 39,741 | 5,246 |
| 2026-11-15 | 40,045 | 5,243 |
| 2026-11-14 | 39,902 | 5,230 |
| 2026-11-13 | 43,156 | 5,445 |
| 2026-11-12 | 43,462 | 5,447 |
| 2026-11-11 | 44,280 | 5,491 |

## JOBG8 LAST 10 FEED DATES — SELECTED JOBS BY CLASSIFICATION

Each dated column shows Ontap jobs classified/published in that JobG8 classification.

| JobG8 classification | 2026-11-20 | 2026-11-19 | 2026-11-18 | 2026-11-17 | 2026-11-16 | 2026-11-15 | 2026-11-14 | 2026-11-13 | 2026-11-12 | 2026-11-11 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Accounting | 1738 | 1743 | 1732 | 1703 | 1667 | 1662 | 1658 | 1433 | 1430 | 1452 |
| Administration | 1042 | 1047 | 995 | 995 | 985 | 984 | 972 | 1159 | 1159 | 1154 |
| Advert / Media / Entertainment | 16 | 17 | 19 | 19 | 19 | 19 | 19 | 21 | 21 | 19 |
| Banking & Financial Services | 57 | 62 | 13 | 13 | 13 | 13 | 13 | 14 | 12 | 12 |
| Call Centre / CustomerService | 368 | 374 | 367 | 345 | 357 | 356 | 357 | 366 | 368 | 358 |
| Community & Sport | 67 | 70 | 64 | 62 | 61 | 61 | 59 | 62 | 59 | 58 |
| Education | 48 | 50 | 50 | 50 | 50 | 50 | 50 | 63 | 67 | 70 |
| Government & Defence | 8 | 9 | 9 | 7 | 6 | 7 | 7 | 7 | 7 | 7 |
| Healthcare & Medical | 403 | 398 | 341 | 343 | 286 | 287 | 283 | 375 | 385 | 407 |
| HR / Recruitment | 141 | 143 | 138 | 135 | 139 | 138 | 137 | 171 | 180 | 182 |
| I.T. & Communications | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 3 | 3 | 7 |
| Insurance & Superannuation | 25 | 24 | 26 | 25 | 24 | 24 | 25 | 23 | 22 | 23 |
| Legal | 410 | 424 | 455 | 451 | 443 | 442 | 444 | 438 | 448 | 435 |
| Real Estate & Property | 73 | 77 | 78 | 77 | 75 | 75 | 78 | 92 | 90 | 93 |
| Sales & Marketing | 929 | 961 | 955 | 962 | 957 | 961 | 964 | 1064 | 1045 | 1059 |
| Transport & Logistics | 180 | 186 | 188 | 184 | 163 | 163 | 163 | 154 | 151 | 155 |

## PAGES

**Published/indexable URLs: 6,141** — 5,758 individual job pages, 261 regional/category pages, 114 city pages and 8 core pages.

| Level | Page type | Area | Family | URL | Page count | Live jobs | In sitemap |
|---|---|---|---|---|---:|---:|---|
| Summary | All published/indexable URLs | Sitewide |  |  | 6,141 |  | Yes |
| Summary | Individual job | Sitewide |  | /jobs/[id] | 5,758 | 5,758 | Yes |
| Summary | Regional/category | Sitewide |  | Multiple | 261 |  | Yes |
| Summary | City | Sitewide |  | Multiple | 114 |  | Yes |
| Summary | Core | Sitewide |  | Multiple | 8 |  | Yes |
| Detail | Core | Sitewide |  | / | 1 |  | Yes |
| Detail | Core | Sitewide |  | /browse-jobs | 1 |  | Yes |
| Detail | Core | Sitewide |  | /about | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | Ai At Work | /ai-at-work | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | Reception And Office Admin | /ai-at-work/reception-and-office-admin | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | Accounts And Finance Admin | /ai-at-work/accounts-and-finance-admin | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | Ai Job Advert Watch | /ai-at-work/ai-job-advert-watch | 1 |  | Yes |
| Detail | Regional/category | Ai At Work | October 2026 | /ai-at-work/ai-job-advert-watch/october-2026 | 1 |  | Yes |
| Detail | Core | Sitewide |  | /ai-tips | 1 |  | Yes |
| Detail | Regional/category | Ai Course Reviews | Ai Course Reviews | /ai-course-reviews | 1 |  | Yes |
| Detail | Core | Sitewide |  | /contact | 1 |  | Yes |
| Detail | Core | Sitewide |  | /privacy-policy | 1 |  | Yes |
| Detail | Core | Sitewide |  | /terms-of-service | 1 |  | Yes |
| Detail | Core | Sitewide |  | /sector-switching | 1 |  | Yes |
| Detail | Regional/category | West Yorkshire | Support Worker | /west-yorkshire/support-worker | 1 | 7 | Yes |
| Detail | Regional/category | South Yorkshire | Support Worker | /south-yorkshire/support-worker | 1 | 5 | Yes |
| Detail | Regional/category | North East | Support Worker | /north-east/support-worker | 1 | 21 | Yes |
| Detail | Regional/category | Sussex | Support Worker | /sussex/support-worker | 1 | 56 | Yes |
| Detail | Regional/category | Cumbria South | Support Worker | /cumbria-south/support-worker | 1 | 3 | Yes |
| Detail | Regional/category | Hampshire | Support Worker | /hampshire/support-worker | 1 | 31 | Yes |
| Detail | Regional/category | West Yorkshire | Service Administrator Jobs | /west-yorkshire/service-administrator-jobs | 1 | 149 | Yes |
| Detail | Regional/category | South Yorkshire | Service Administrator Jobs | /south-yorkshire/service-administrator-jobs | 1 | 63 | Yes |
| Detail | Regional/category | North Yorkshire | Service Administrator Jobs | /north-yorkshire/service-administrator-jobs | 1 | 43 | Yes |
| Detail | Regional/category | North East | Service Administrator Jobs | /north-east/service-administrator-jobs | 1 | 104 | Yes |
| Detail | Regional/category | London | Service Administrator Jobs | /london/service-administrator-jobs | 1 | 454 | Yes |
| Detail | Regional/category | London | Central Service Administrator Jobs | /london/central-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | North Service Administrator Jobs | /london/north-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | East Service Administrator Jobs | /london/east-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | South Service Administrator Jobs | /london/south-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | West Service Administrator Jobs | /london/west-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | Hampshire | Service Administrator Jobs | /hampshire/service-administrator-jobs | 1 | 157 | Yes |
| Detail | Regional/category | Coventry Warwickshire | Service Administrator Jobs | /coventry-warwickshire/service-administrator-jobs | 1 | 86 | Yes |
| Detail | Regional/category | Surrey | Service Administrator Jobs | /surrey/service-administrator-jobs | 1 | 165 | Yes |
| Detail | Regional/category | Kent | Service Administrator Jobs | /kent/service-administrator-jobs | 1 | 123 | Yes |
| Detail | Regional/category | Sussex | Service Administrator Jobs | /sussex/service-administrator-jobs | 1 | 132 | Yes |
| Detail | City | Newcastle | admin and office jobs | /newcastle/service-administrator-jobs | 1 | 29 | Yes |
| Detail | City | Southampton | support worker jobs | /southampton/support-worker | 1 | 9 | Yes |
| Detail | City | Sheffield | admin and office jobs | /sheffield/service-administrator-jobs | 1 | 41 | Yes |
| Detail | City | Leeds | admin and office jobs | /leeds/service-administrator-jobs | 1 | 95 | Yes |
| Detail | City | Coventry | admin and office jobs | /coventry/service-administrator-jobs | 1 | 19 | Yes |
| Detail | City | Southampton | admin and office jobs | /southampton/service-administrator-jobs | 1 | 15 | Yes |
| Detail | City | Brighton & Hove | admin and office jobs | /brighton-hove/service-administrator-jobs | 1 | 13 | Yes |
| Detail | City | Bradford | admin and office jobs | /bradford/service-administrator-jobs | 1 | 30 | Yes |
| Detail | City | Huddersfield | admin and office jobs | /huddersfield/service-administrator-jobs | 1 | 17 | Yes |
| Detail | City | York | admin and office jobs | /york/service-administrator-jobs | 1 | 11 | Yes |
| Detail | City | Barnsley | admin and office jobs | /barnsley/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Doncaster | admin and office jobs | /doncaster/service-administrator-jobs | 1 | 15 | Yes |
| Detail | City | Bristol | admin and office jobs | /bristol/service-administrator-jobs | 1 | 74 | Yes |
| Detail | City | Manchester | admin and office jobs | /manchester/service-administrator-jobs | 1 | 144 | Yes |
| Detail | City | Cambridge | admin and office jobs | /cambridge/service-administrator-jobs | 1 | 38 | Yes |
| Detail | City | Birmingham | admin and office jobs | /birmingham/service-administrator-jobs | 1 | 136 | Yes |
| Detail | City | Peterborough | admin and office jobs | /peterborough/service-administrator-jobs | 1 | 24 | Yes |
| Detail | City | Warrington | admin and office jobs | /warrington/service-administrator-jobs | 1 | 29 | Yes |
| Detail | City | Liverpool | admin and office jobs | /liverpool/service-administrator-jobs | 1 | 44 | Yes |
| Detail | City | Hull | admin and office jobs | /hull/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Oxford | admin and office jobs | /oxford/service-administrator-jobs | 1 | 17 | Yes |
| Detail | City | Belfast | admin and office jobs | /belfast/service-administrator-jobs | 1 | 13 | Yes |
| Detail | City | Glasgow | admin and office jobs | /glasgow/service-administrator-jobs | 1 | 41 | Yes |
| Detail | City | Edinburgh | admin and office jobs | /edinburgh/service-administrator-jobs | 1 | 35 | Yes |
| Detail | City | Cardiff | admin and office jobs | /cardiff/service-administrator-jobs | 1 | 22 | Yes |
| Detail | City | Exeter | admin and office jobs | /exeter/service-administrator-jobs | 1 | 24 | Yes |
| Detail | City | Milton Keynes | admin and office jobs | /milton-keynes/service-administrator-jobs | 1 | 29 | Yes |
| Detail | City | Farnham | admin and office jobs | /farnham/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Northampton | admin and office jobs | /northampton/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Poole | admin and office jobs | /poole/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Portsmouth | admin and office jobs | /portsmouth/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Stoke-on-trent | admin and office jobs | /stoke-on-trent/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Hemel Hempstead | admin and office jobs | /hemel-hempstead/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Basingstoke | admin and office jobs | /basingstoke/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Chelmsford | admin and office jobs | /chelmsford/service-administrator-jobs | 1 | 12 | Yes |
| Detail | City | Gloucester | admin and office jobs | /gloucester/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Leicester | admin and office jobs | /leicester/service-administrator-jobs | 1 | 25 | Yes |
| Detail | City | Maidstone | admin and office jobs | /maidstone/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Newtownabbey | admin and office jobs | /newtownabbey/service-administrator-jobs | 1 | 1 | Yes |
| Detail | City | Plymouth | admin and office jobs | /plymouth/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Sunderland | admin and office jobs | /sunderland/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Worcester | admin and office jobs | /worcester/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Altrincham | admin and office jobs | /altrincham/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Ashford | admin and office jobs | /ashford/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Aylesbury | admin and office jobs | /aylesbury/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Bedford | admin and office jobs | /bedford/service-administrator-jobs | 1 | 14 | Yes |
| Detail | City | Bournemouth | admin and office jobs | /bournemouth/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Chester Le Street | admin and office jobs | /chester-le-street/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Macclesfield | admin and office jobs | /macclesfield/service-administrator-jobs | 1 | 15 | Yes |
| Detail | City | Rotherham | admin and office jobs | /rotherham/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Scarborough | admin and office jobs | /scarborough/service-administrator-jobs | 1 | 3 | Yes |
| Detail | City | Shrewsbury | admin and office jobs | /shrewsbury/service-administrator-jobs | 1 | 12 | Yes |
| Detail | City | Warwick | admin and office jobs | /warwick/service-administrator-jobs | 1 | 19 | Yes |
| Detail | City | Wigston | admin and office jobs | /wigston/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Dartford | admin and office jobs | /dartford/service-administrator-jobs | 1 | 11 | Yes |
| Detail | City | Stockport | admin and office jobs | /stockport/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Swansea | admin and office jobs | /swansea/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Walsall | admin and office jobs | /walsall/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Bath | admin and office jobs | /bath/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Eastleigh | admin and office jobs | /eastleigh/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Harrogate | admin and office jobs | /harrogate/service-administrator-jobs | 1 | 13 | Yes |
| Detail | City | Watford | admin and office jobs | /watford/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Crawley | admin and office jobs | /crawley/service-administrator-jobs | 1 | 10 | Yes |
| Detail | City | Swindon | admin and office jobs | /swindon/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Horsham | admin and office jobs | /horsham/service-administrator-jobs | 1 | 6 | Yes |
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
| Detail | City | Ipswich | All roles | /ipswich/jobs | 1 |  | Yes |
| Detail | City | Solihull | All roles | /solihull/jobs | 1 |  | Yes |
| Detail | City | Derby | All roles | /derby/jobs | 1 |  | Yes |
| Detail | City | Cheltenham | All roles | /cheltenham/jobs | 1 |  | Yes |
| Detail | City | Bracknell | All roles | /bracknell/jobs | 1 |  | Yes |
| Detail | City | Canterbury | All roles | /canterbury/jobs | 1 |  | Yes |
| Detail | City | Blackburn | All roles | /blackburn/jobs | 1 |  | Yes |
| Detail | City | Corby | All roles | /corby/jobs | 1 |  | Yes |
| Detail | City | Crewe | All roles | /crewe/jobs | 1 |  | Yes |
| Detail | City | Stevenage | All roles | /stevenage/jobs | 1 |  | Yes |
| Detail | City | Chesterfield | All roles | /chesterfield/jobs | 1 |  | Yes |
| Detail | City | Woking | All roles | /woking/jobs | 1 |  | Yes |
| Detail | City | Abingdon | All roles | /abingdon/jobs | 1 |  | Yes |
| Detail | City | King's Lynn | All roles | /kings-lynn/jobs | 1 |  | Yes |
| Detail | City | Newport | All roles | /newport/jobs | 1 |  | Yes |
| Detail | City | Oldham | All roles | /oldham/jobs | 1 |  | Yes |
| Detail | City | Redhill | All roles | /redhill/jobs | 1 |  | Yes |
| Detail | City | Sittingbourne | All roles | /sittingbourne/jobs | 1 |  | Yes |
| Detail | City | Wrexham | All roles | /wrexham/jobs | 1 |  | Yes |
| Detail | City | Kettering | All roles | /kettering/jobs | 1 |  | Yes |
| Detail | City | High Wycombe | All roles | /high-wycombe/jobs | 1 |  | Yes |
| Detail | City | Dudley | All roles | /dudley/jobs | 1 |  | Yes |
| Detail | City | Dundee | All roles | /dundee/jobs | 1 |  | Yes |
| Detail | City | Wirral | All roles | /wirral/jobs | 1 |  | Yes |
| Detail | City | Luton | All roles | /luton/jobs | 1 |  | Yes |
| Detail | City | Trafford | All roles | /trafford/jobs | 1 |  | Yes |
| Detail | Regional/category | Yorkshire - East | Admin & Customer Service | /job-search/east-yorkshire/service-administrator-jobs | 1 | 18 | Yes |
| Detail | Regional/category | Northern Ireland - East | Admin & Customer Service | /job-search/northern-ireland-east/service-administrator-jobs | 1 | 17 | Yes |
| Detail | Regional/category | London | Customer Service & Contact Centre | /job-search/london/customer-service-jobs | 1 | 11 | Yes |
| Detail | Regional/category | London | HR & Recruitment | /job-search/london/hr-recruitment-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Admin & Customer Service | /job-search/manchester-salford/service-administrator-jobs | 1 | 118 | Yes |
| Detail | Regional/category | London | Finance & Accounts | /job-search/london/finance-accounts-jobs | 1 | 205 | Yes |
| Detail | Regional/category | Oxfordshire | Admin & Customer Service | /job-search/oxfordshire/service-administrator-jobs | 1 | 79 | Yes |
| Detail | Regional/category | Bristol & Bath | Admin & Customer Service | /job-search/bristol-bath/service-administrator-jobs | 1 | 73 | Yes |
| Detail | Regional/category | Essex | Admin & Customer Service | /job-search/essex/service-administrator-jobs | 1 | 118 | Yes |
| Detail | Regional/category | Hampshire | Customer Service & Contact Centre | /job-search/hampshire/customer-service-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Cambridgeshire | Admin & Customer Service | /job-search/cambridgeshire/service-administrator-jobs | 1 | 51 | Yes |
| Detail | Regional/category | Gloucestershire | Admin & Customer Service | /job-search/gloucestershire/service-administrator-jobs | 1 | 85 | Yes |
| Detail | Regional/category | London | Support Worker | /job-search/london/support-worker | 1 | 100 | Yes |
| Detail | Regional/category | Devon | Finance & Accounts | /job-search/devon/finance-accounts-jobs | 1 | 23 | Yes |
| Detail | Regional/category | Dorset | Admin & Customer Service | /job-search/dorset/service-administrator-jobs | 1 | 55 | Yes |
| Detail | Regional/category | Staffordshire | Customer Service & Contact Centre | /job-search/staffordshire/customer-service-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Devon | Admin & Customer Service | /job-search/devon/service-administrator-jobs | 1 | 70 | Yes |
| Detail | Regional/category | Surrey | Customer Service & Contact Centre | /job-search/surrey/customer-service-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Wiltshire | Admin & Customer Service | /job-search/wiltshire/service-administrator-jobs | 1 | 48 | Yes |
| Detail | Regional/category | Northamptonshire | Admin & Customer Service | /job-search/northamptonshire/service-administrator-jobs | 1 | 64 | Yes |
| Detail | Regional/category | Berkshire | Admin & Customer Service | /job-search/berkshire/service-administrator-jobs | 1 | 72 | Yes |
| Detail | Regional/category | Nottinghamshire | Admin & Customer Service | /job-search/nottinghamshire/service-administrator-jobs | 1 | 69 | Yes |
| Detail | Regional/category | Buckinghamshire | Admin & Customer Service | /job-search/buckinghamshire/service-administrator-jobs | 1 | 77 | Yes |
| Detail | Regional/category | Surrey | Support Worker | /job-search/surrey/support-worker | 1 | 10 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Customer Service & Contact Centre | /job-search/manchester-salford/customer-service-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Hampshire | HR & Recruitment | /job-search/hampshire/hr-recruitment-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Hertfordshire | Admin & Customer Service | /job-search/hertfordshire/service-administrator-jobs | 1 | 93 | Yes |
| Detail | Regional/category | Staffordshire | Admin & Customer Service | /job-search/staffordshire/service-administrator-jobs | 1 | 69 | Yes |
| Detail | Regional/category | Norfolk | Admin & Customer Service | /job-search/norfolk/service-administrator-jobs | 1 | 46 | Yes |
| Detail | Regional/category | Sussex | Finance & Accounts | /job-search/sussex/finance-accounts-jobs | 1 | 42 | Yes |
| Detail | Regional/category | Yorkshire - West | Finance & Accounts | /job-search/west-yorkshire/finance-accounts-jobs | 1 | 86 | Yes |
| Detail | Regional/category | Gloucestershire | Finance & Accounts | /job-search/gloucestershire/finance-accounts-jobs | 1 | 30 | Yes |
| Detail | Regional/category | Bristol & Bath | Finance & Accounts | /job-search/bristol-bath/finance-accounts-jobs | 1 | 27 | Yes |
| Detail | Regional/category | Sussex | Customer Service & Contact Centre | /job-search/sussex/customer-service-jobs | 1 | 5 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Admin & Customer Service | /job-search/birmingham-solihull/service-administrator-jobs | 1 | 109 | Yes |
| Detail | Regional/category | Yorkshire - West | HR & Recruitment | /job-search/west-yorkshire/hr-recruitment-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Greater Manchester - South | Admin & Customer Service | /job-search/greater-manchester-south/service-administrator-jobs | 1 | 39 | Yes |
| Detail | Regional/category | Hampshire | Finance & Accounts | /job-search/hampshire/finance-accounts-jobs | 1 | 60 | Yes |
| Detail | Regional/category | North East | Finance & Accounts | /job-search/north-east/finance-accounts-jobs | 1 | 33 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Finance & Accounts | /job-search/birmingham-solihull/finance-accounts-jobs | 1 | 40 | Yes |
| Detail | Regional/category | Wiltshire | Support Worker | /job-search/wiltshire/support-worker | 1 | 15 | Yes |
| Detail | Regional/category | Somerset | Admin & Customer Service | /job-search/somerset/service-administrator-jobs | 1 | 41 | Yes |
| Detail | Regional/category | London | Customer Sales & Sales Advisor | /job-search/london/customer-sales-jobs | 1 | 95 | Yes |
| Detail | Regional/category | Yorkshire - West | Customer Sales & Sales Advisor | /job-search/west-yorkshire/customer-sales-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Customer Sales & Sales Advisor | /job-search/manchester-salford/customer-sales-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Leicestershire | Admin & Customer Service | /job-search/leicestershire/service-administrator-jobs | 1 | 78 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Admin & Customer Service | /job-search/warrington-halton/service-administrator-jobs | 1 | 30 | Yes |
| Detail | Regional/category | Cornwall | Admin & Customer Service | /job-search/cornwall/service-administrator-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Suffolk | Admin & Customer Service | /job-search/suffolk/service-administrator-jobs | 1 | 58 | Yes |
| Detail | Regional/category | Derbyshire | Admin & Customer Service | /job-search/derbyshire/service-administrator-jobs | 1 | 59 | Yes |
| Detail | Regional/category | Cheshire - East | Admin & Customer Service | /job-search/cheshire-east/service-administrator-jobs | 1 | 29 | Yes |
| Detail | Regional/category | Lincolnshire | Admin & Customer Service | /job-search/lincolnshire/service-administrator-jobs | 1 | 30 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Admin & Customer Service | /job-search/merseyside-liverpool/service-administrator-jobs | 1 | 40 | Yes |
| Detail | Regional/category | Shropshire | Admin & Customer Service | /job-search/shropshire/service-administrator-jobs | 1 | 42 | Yes |
| Detail | Regional/category | Greater Manchester - Wigan & Bolton | Admin & Customer Service | /job-search/wigan-bolton/service-administrator-jobs | 1 | 33 | Yes |
| Detail | Regional/category | West Midlands - Black Country | Admin & Customer Service | /job-search/black-country/service-administrator-jobs | 1 | 62 | Yes |
| Detail | Regional/category | London | Legal Assistant & Paralegal | /job-search/london/paralegal-jobs | 1 | 111 | Yes |
| Detail | Regional/category | Suffolk | Legal Assistant & Paralegal | /job-search/suffolk/paralegal-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Essex | Legal Assistant & Paralegal | /job-search/essex/paralegal-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Norfolk | Legal Assistant & Paralegal | /job-search/norfolk/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | London | Marketing | /job-search/london/marketing-jobs | 1 | 146 | Yes |
| Detail | Regional/category | Surrey | Marketing | /job-search/surrey/marketing-jobs | 1 | 31 | Yes |
| Detail | Regional/category | Greater Manchester - North | Finance & Accounts | /job-search/greater-manchester-north/finance-accounts-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Scotland Central - Fife | Admin & Customer Service | /job-search/fife/service-administrator-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Bristol & Bath | Legal Assistant & Paralegal | /job-search/bristol-bath/paralegal-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Staffordshire | Marketing | /job-search/staffordshire/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Marketing | /job-search/manchester-salford/marketing-jobs | 1 | 32 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Marketing | /job-search/birmingham-solihull/marketing-jobs | 1 | 31 | Yes |
| Detail | Regional/category | Berkshire | HR & Recruitment | /job-search/berkshire/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | HR & Recruitment | /job-search/manchester-salford/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Nottinghamshire | HR & Recruitment | /job-search/nottinghamshire/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | HR & Recruitment | /job-search/birmingham-solihull/hr-recruitment-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Sussex | HR & Recruitment | /job-search/sussex/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Essex | HR & Recruitment | /job-search/essex/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Cheshire - West | Admin & Customer Service | /job-search/cheshire-west/service-administrator-jobs | 1 | 23 | Yes |
| Detail | Regional/category | Scotland Central - Edinburgh & Lothians | Admin & Customer Service | /job-search/edinburgh-lothians/service-administrator-jobs | 1 | 40 | Yes |
| Detail | Regional/category | Worcestershire | Admin & Customer Service | /job-search/worcestershire/service-administrator-jobs | 1 | 43 | Yes |
| Detail | Regional/category | Berkshire | Marketing | /job-search/berkshire/marketing-jobs | 1 | 23 | Yes |
| Detail | Regional/category | Kent | Support Worker | /job-search/kent/support-worker | 1 | 27 | Yes |
| Detail | Regional/category | North East | Customer Sales & Sales Advisor | /job-search/north-east/customer-sales-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Oxfordshire | Support Worker | /job-search/oxfordshire/support-worker | 1 | 9 | Yes |
| Detail | Regional/category | Yorkshire - North | Finance & Accounts | /job-search/north-yorkshire/finance-accounts-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Shropshire | Finance & Accounts | /job-search/shropshire/finance-accounts-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Bedfordshire | Admin & Customer Service | /job-search/bedfordshire/service-administrator-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Bristol & Bath | Customer Sales & Sales Advisor | /job-search/bristol-bath/customer-sales-jobs | 1 | 15 | Yes |
| Detail | Regional/category | Buckinghamshire | Marketing | /job-search/buckinghamshire/marketing-jobs | 1 | 22 | Yes |
| Detail | Regional/category | Wales South - Cardiff & Vale | Admin & Customer Service | /job-search/cardiff-vale/service-administrator-jobs | 1 | 22 | Yes |
| Detail | Regional/category | Berkshire | Customer Sales & Sales Advisor | /job-search/berkshire/customer-sales-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Hertfordshire | Customer Sales & Sales Advisor | /job-search/hertfordshire/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Kent | Customer Sales & Sales Advisor | /job-search/kent/customer-sales-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Customer Sales & Sales Advisor | /job-search/glasgow/customer-sales-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Surrey | Customer Sales & Sales Advisor | /job-search/surrey/customer-sales-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Sussex | Customer Sales & Sales Advisor | /job-search/sussex/customer-sales-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Bristol & Bath | Marketing | /job-search/bristol-bath/marketing-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Gloucestershire | Marketing | /job-search/gloucestershire/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Hertfordshire | Marketing | /job-search/hertfordshire/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Kent | Marketing | /job-search/kent/marketing-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Oxfordshire | Marketing | /job-search/oxfordshire/marketing-jobs | 1 | 7 | Yes |
| Detail | Regional/category | North Scotland | Admin & Customer Service | /job-search/north-scotland/service-administrator-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Scotland Central - Tayside | Admin & Customer Service | /job-search/tayside/service-administrator-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Wales South - Valleys | Admin & Customer Service | /job-search/south-wales-valleys/service-administrator-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Cambridgeshire | Marketing | /job-search/cambridgeshire/marketing-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Cheshire - West | Marketing | /job-search/cheshire-west/marketing-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Essex | Marketing | /job-search/essex/marketing-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Marketing | /job-search/merseyside-liverpool/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | North East | Marketing | /job-search/north-east/marketing-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Finance & Accounts | /job-search/warrington-halton/finance-accounts-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Buckinghamshire | Customer Service & Contact Centre | /job-search/buckinghamshire/customer-service-jobs | 1 | 3 | Yes |
| Detail | Regional/category | North East | Customer Service & Contact Centre | /job-search/north-east/customer-service-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Devon | Customer Sales & Sales Advisor | /job-search/devon/customer-sales-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Hampshire | Customer Sales & Sales Advisor | /job-search/hampshire/customer-sales-jobs | 1 | 25 | Yes |
| Detail | Regional/category | North Scotland | Customer Sales & Sales Advisor | /job-search/north-scotland/customer-sales-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Northern Ireland - East | Marketing | /job-search/northern-ireland-east/marketing-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Yorkshire - North | Marketing | /job-search/north-yorkshire/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Essex | Finance & Accounts | /job-search/essex/finance-accounts-jobs | 1 | 49 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Finance & Accounts | /job-search/manchester-salford/finance-accounts-jobs | 1 | 60 | Yes |
| Detail | Regional/category | Berkshire | Finance & Accounts | /job-search/berkshire/finance-accounts-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Buckinghamshire | Finance & Accounts | /job-search/buckinghamshire/finance-accounts-jobs | 1 | 37 | Yes |
| Detail | Regional/category | Cambridgeshire | Finance & Accounts | /job-search/cambridgeshire/finance-accounts-jobs | 1 | 32 | Yes |
| Detail | Regional/category | Cheshire - East | Finance & Accounts | /job-search/cheshire-east/finance-accounts-jobs | 1 | 24 | Yes |
| Detail | Regional/category | Cheshire - West | Finance & Accounts | /job-search/cheshire-west/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Dorset | Finance & Accounts | /job-search/dorset/finance-accounts-jobs | 1 | 29 | Yes |
| Detail | Regional/category | Hertfordshire | Finance & Accounts | /job-search/hertfordshire/finance-accounts-jobs | 1 | 32 | Yes |
| Detail | Regional/category | Kent | Finance & Accounts | /job-search/kent/finance-accounts-jobs | 1 | 54 | Yes |
| Detail | Regional/category | Lancashire - East | Finance & Accounts | /job-search/lancashire-east/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Leicestershire | Finance & Accounts | /job-search/leicestershire/finance-accounts-jobs | 1 | 25 | Yes |
| Detail | Regional/category | Norfolk | Finance & Accounts | /job-search/norfolk/finance-accounts-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Northamptonshire | Finance & Accounts | /job-search/northamptonshire/finance-accounts-jobs | 1 | 30 | Yes |
| Detail | Regional/category | Nottinghamshire | Finance & Accounts | /job-search/nottinghamshire/finance-accounts-jobs | 1 | 33 | Yes |
| Detail | Regional/category | Oxfordshire | Finance & Accounts | /job-search/oxfordshire/finance-accounts-jobs | 1 | 25 | Yes |
| Detail | Regional/category | Suffolk | Finance & Accounts | /job-search/suffolk/finance-accounts-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Surrey | Finance & Accounts | /job-search/surrey/finance-accounts-jobs | 1 | 70 | Yes |
| Detail | Regional/category | Wales South - Cardiff & Vale | Finance & Accounts | /job-search/cardiff-vale/finance-accounts-jobs | 1 | 7 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Finance & Accounts | /job-search/coventry-warwickshire/finance-accounts-jobs | 1 | 54 | Yes |
| Detail | Regional/category | Wiltshire | Finance & Accounts | /job-search/wiltshire/finance-accounts-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Yorkshire - South | Finance & Accounts | /job-search/south-yorkshire/finance-accounts-jobs | 1 | 27 | Yes |
| Detail | Regional/category | Norfolk | Marketing | /job-search/norfolk/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Yorkshire - West | Marketing | /job-search/west-yorkshire/marketing-jobs | 1 | 25 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Legal Assistant & Paralegal | /job-search/birmingham-solihull/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Yorkshire - North | Legal Assistant & Paralegal | /job-search/north-yorkshire/paralegal-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Yorkshire - West | Legal Assistant & Paralegal | /job-search/west-yorkshire/paralegal-jobs | 1 | 15 | Yes |
| Detail | Regional/category | Berkshire | Legal Assistant & Paralegal | /job-search/berkshire/paralegal-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Legal Assistant & Paralegal | /job-search/manchester-salford/paralegal-jobs | 1 | 29 | Yes |
| Detail | Regional/category | Kent | Legal Assistant & Paralegal | /job-search/kent/paralegal-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Legal Assistant & Paralegal | /job-search/merseyside-liverpool/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Surrey | Legal Assistant & Paralegal | /job-search/surrey/paralegal-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Buckinghamshire | Legal Assistant & Paralegal | /job-search/buckinghamshire/paralegal-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Marketing | /job-search/warrington-halton/marketing-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Essex | Customer Sales & Sales Advisor | /job-search/essex/customer-sales-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Gloucestershire | HR & Recruitment | /job-search/gloucestershire/hr-recruitment-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Greater Manchester - North | Admin & Customer Service | /job-search/greater-manchester-north/service-administrator-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Hampshire | Legal Assistant & Paralegal | /job-search/hampshire/paralegal-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Herefordshire | Admin & Customer Service | /job-search/herefordshire/service-administrator-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Lancashire - East | Admin & Customer Service | /job-search/lancashire-east/service-administrator-jobs | 1 | 28 | Yes |
| Detail | Regional/category | Lincolnshire | Finance & Accounts | /job-search/lincolnshire/finance-accounts-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Finance & Accounts | /job-search/merseyside-liverpool/finance-accounts-jobs | 1 | 24 | Yes |
| Detail | Regional/category | Nottinghamshire | Marketing | /job-search/nottinghamshire/marketing-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Oxfordshire | Legal Assistant & Paralegal | /job-search/oxfordshire/paralegal-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Somerset | Finance & Accounts | /job-search/somerset/finance-accounts-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Staffordshire | Finance & Accounts | /job-search/staffordshire/finance-accounts-jobs | 1 | 18 | Yes |
| Detail | Regional/category | Sussex | Marketing | /job-search/sussex/marketing-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Wales South - Swansea Bay | Admin & Customer Service | /job-search/swansea-bay/service-administrator-jobs | 1 | 11 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Marketing | /job-search/coventry-warwickshire/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Worcestershire | Finance & Accounts | /job-search/worcestershire/finance-accounts-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Yorkshire - East | Finance & Accounts | /job-search/east-yorkshire/finance-accounts-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Cumbria - North | Admin & Customer Service | /job-search/cumbria-north/service-administrator-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Dorset | Customer Sales & Sales Advisor | /job-search/dorset/customer-sales-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Hertfordshire | Legal Assistant & Paralegal | /job-search/hertfordshire/paralegal-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Lancashire - Central | Admin & Customer Service | /job-search/lancashire-central/service-administrator-jobs | 1 | 17 | Yes |
| Detail | Regional/category | North Wales - East | Admin & Customer Service | /job-search/north-wales-east/service-administrator-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Northamptonshire | Customer Sales & Sales Advisor | /job-search/northamptonshire/customer-sales-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Nottinghamshire | Legal Assistant & Paralegal | /job-search/nottinghamshire/paralegal-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Oxfordshire | Customer Sales & Sales Advisor | /job-search/oxfordshire/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Scotland Central - Falkirk & Stirling | Admin & Customer Service | /job-search/falkirk-stirling/service-administrator-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Suffolk | Customer Sales & Sales Advisor | /job-search/suffolk/customer-sales-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Wales South - Gwent | Admin & Customer Service | /job-search/gwent/service-administrator-jobs | 1 | 16 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Legal Assistant & Paralegal | /job-search/coventry-warwickshire/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Yorkshire - West | Customer Service & Contact Centre | /job-search/west-yorkshire/customer-service-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Cambridgeshire | Customer Sales & Sales Advisor | /job-search/cambridgeshire/customer-sales-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Nottinghamshire | Customer Sales & Sales Advisor | /job-search/nottinghamshire/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Customer Sales & Sales Advisor | /job-search/coventry-warwickshire/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Worcestershire | Customer Sales & Sales Advisor | /job-search/worcestershire/customer-sales-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Northamptonshire | Marketing | /job-search/northamptonshire/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Marketing | /job-search/glasgow/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Cornwall | Finance & Accounts | /job-search/cornwall/finance-accounts-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Derbyshire | Finance & Accounts | /job-search/derbyshire/finance-accounts-jobs | 1 | 24 | Yes |
| Detail | Regional/category | North East | HR & Recruitment | /job-search/north-east/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Staffordshire | HR & Recruitment | /job-search/staffordshire/hr-recruitment-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Surrey | HR & Recruitment | /job-search/surrey/hr-recruitment-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Hertfordshire | Customer Service & Contact Centre | /job-search/hertfordshire/customer-service-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Kent | Customer Service & Contact Centre | /job-search/kent/customer-service-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Merseyside - St Helens & Knowsley | Admin & Customer Service | /job-search/st-helens-knowsley/service-administrator-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Cheshire - East | Customer Sales & Sales Advisor | /job-search/cheshire-east/customer-sales-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Gloucestershire | Customer Sales & Sales Advisor | /job-search/gloucestershire/customer-sales-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Leicestershire | Customer Sales & Sales Advisor | /job-search/leicestershire/customer-sales-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Norfolk | Customer Sales & Sales Advisor | /job-search/norfolk/customer-sales-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Legal Assistant & Paralegal | /job-search/glasgow/paralegal-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Yorkshire - South | Marketing | /job-search/south-yorkshire/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | West Midlands - Black Country | Finance & Accounts | /job-search/black-country/finance-accounts-jobs | 1 | 24 | Yes |
| Detail | Regional/category | Leicestershire | HR & Recruitment | /job-search/leicestershire/hr-recruitment-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Suffolk | HR & Recruitment | /job-search/suffolk/hr-recruitment-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Merseyside - Wirral | Admin & Customer Service | /job-search/merseyside-wirral/service-administrator-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Scotland West - Lanarkshire | Admin & Customer Service | /job-search/lanarkshire/service-administrator-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Berkshire | Support Worker | /job-search/berkshire/support-worker | 1 | 14 | Yes |
| Detail | Regional/category | Dorset | Support Worker | /job-search/dorset/support-worker | 1 | 19 | Yes |
| Detail | Regional/category | Essex | Support Worker | /job-search/essex/support-worker | 1 | 29 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Support Worker | /job-search/manchester-salford/support-worker | 1 | 7 | Yes |
| Detail | Regional/category | Nottinghamshire | Support Worker | /job-search/nottinghamshire/support-worker | 1 | 19 | Yes |
| Detail | Regional/category | Derbyshire | Customer Sales & Sales Advisor | /job-search/derbyshire/customer-sales-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Lincolnshire | Legal Assistant & Paralegal | /job-search/lincolnshire/paralegal-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Sussex | Legal Assistant & Paralegal | /job-search/sussex/paralegal-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Yorkshire - South | Legal Assistant & Paralegal | /job-search/south-yorkshire/paralegal-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Dorset | Marketing | /job-search/dorset/marketing-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Leicestershire | Marketing | /job-search/leicestershire/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Bedfordshire | Finance & Accounts | /job-search/bedfordshire/finance-accounts-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Buckinghamshire | HR & Recruitment | /job-search/buckinghamshire/hr-recruitment-jobs | 1 | 2 | Yes |
| Detail | Regional/category | West Midlands - Black Country | HR & Recruitment | /job-search/black-country/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Lancashire - Blackpool & Fylde | Admin & Customer Service | /job-search/blackpool-fylde/service-administrator-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Bedfordshire | Customer Sales & Sales Advisor | /job-search/bedfordshire/customer-sales-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Cambridgeshire | Legal Assistant & Paralegal | /job-search/cambridgeshire/paralegal-jobs | 1 | 4 | Yes |
| Detail | Regional/category | North East | Legal Assistant & Paralegal | /job-search/north-east/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Scotland Central - Edinburgh & Lothians | Legal Assistant & Paralegal | /job-search/edinburgh-lothians/paralegal-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Hampshire | Marketing | /job-search/hampshire/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Shropshire | Marketing | /job-search/shropshire/marketing-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Greater Manchester - South | Finance & Accounts | /job-search/greater-manchester-south/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Lancashire - Central | Finance & Accounts | /job-search/lancashire-central/finance-accounts-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Merseyside - Wirral | Finance & Accounts | /job-search/merseyside-wirral/finance-accounts-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Scotland Central - Edinburgh & Lothians | Finance & Accounts | /job-search/edinburgh-lothians/finance-accounts-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Somerset | Customer Sales & Sales Advisor | /job-search/somerset/customer-sales-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Bedfordshire | Legal Assistant & Paralegal | /job-search/bedfordshire/paralegal-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Devon | Legal Assistant & Paralegal | /job-search/devon/paralegal-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Greater Manchester - Wigan & Bolton | Finance & Accounts | /job-search/wigan-bolton/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Finance & Accounts | /job-search/glasgow/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Customer Service & Contact Centre | /job-search/coventry-warwickshire/customer-service-jobs | 1 | 3 | Yes |

## CITY OPPORTUNITIES

**562 mapped towns/localities with live jobs or an existing city page.** Counts use all 5,758 unique live Ontap jobs across every role and provider: 3,141 have an exact recognised town/locality and 2,617 have only broader or unrecognised location evidence. CREATE means 4+ current Service Admin jobs and no existing city page; London is held separately.

| Status | Town/city/locality | Region | All live jobs | Existing pages | Current routes | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre | Other / unclassified |
|---|---|---|---:|---:|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CREATE | Eastbourne | Sussex | 15 | 0 |  | 6 | 5 | 2 | 1 | 0 | 0 | 1 | 0 | 0 |
| CREATE | Mansfield | Nottinghamshire | 13 | 0 |  | 6 | 3 | 3 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Tamworth | Staffordshire | 12 | 0 |  | 9 | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 0 |
| CREATE | Castleford | Yorkshire - West | 11 | 0 |  | 5 | 1 | 1 | 1 | 3 | 0 | 0 | 0 | 0 |
| CREATE | Fareham | Hampshire | 11 | 0 |  | 7 | 2 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| CREATE | Loughborough | Leicestershire | 11 | 0 |  | 8 | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 |
| CREATE | Oldbury | West Midlands - Black Country | 11 | 0 |  | 10 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| CREATE | St. Ives | Cambridgeshire | 11 | 0 |  | 7 | 0 | 3 | 0 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Worthing | Sussex | 11 | 0 |  | 5 | 5 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Aberdeen | North Scotland | 9 | 0 |  | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Leigh | Greater Manchester - Wigan & Bolton | 9 | 0 |  | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Tunbridge Wells | Kent | 9 | 0 |  | 5 | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Havant | Hampshire | 8 | 0 |  | 7 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Leamington Spa | West Midlands - Coventry & Warwickshire | 8 | 0 |  | 4 | 0 | 0 | 3 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Maidenhead | Berkshire | 8 | 0 |  | 5 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Southend-on-sea | Essex | 8 | 0 |  | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Staines | Surrey | 8 | 0 |  | 7 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Taunton | Somerset | 8 | 0 |  | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Telford | Shropshire | 8 | 0 |  | 7 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Washington | North East - Tyneside, Wearside & Northumberland | 8 | 0 |  | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| CREATE | West Bromwich | West Midlands - Black Country | 8 | 0 |  | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Winchester | Hampshire | 8 | 0 |  | 6 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Batley | Yorkshire - West | 7 | 0 |  | 4 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| CREATE | Halifax | Yorkshire - West | 7 | 0 |  | 6 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Middlewich | Cheshire - East | 7 | 0 |  | 5 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| CREATE | Slough | Berkshire | 7 | 0 |  | 4 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Blackpool | Lancashire - Blackpool & Fylde | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Brentwood | Essex | 6 | 0 |  | 5 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Bury | Greater Manchester - North | 6 | 0 |  | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Bury St Edmunds | Suffolk | 6 | 0 |  | 5 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Daventry | Northamptonshire | 6 | 0 |  | 4 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Birkenhead | Merseyside - Wirral | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Brinsworth | Yorkshire - South | 5 | 0 |  | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Chippenham | Wiltshire | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Cullompton | Devon | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Darlington | North East - County Durham & Darlington/Hartlepool | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Grantham | Lincolnshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Hessle | Yorkshire - East | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Rochdale | Greater Manchester - North | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Stirling | Scotland Central - Falkirk & Stirling | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Wellington | Shropshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Wigan | Greater Manchester - Wigan & Bolton | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Wilmslow | Cheshire - East | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Aldershot | Hampshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Caterham | Surrey | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Flint | North Wales - East | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Gainsborough | Lincolnshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Livingston | Scotland Central - Edinburgh & Lothians | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Penwortham | Lancashire - Central | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Rogerstone | Wales South -gwent | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Rugeley | Staffordshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Shepperton | Surrey | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Shirley | West Midlands - Birmingham & Solihull | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Manchester | Greater Manchester - Manchester & Salford | 156 | 1 | /manchester/service-administrator-jobs | 107 | 6 | 9 | 13 | 8 | 10 | 2 | 1 | 0 |
| LIVE PAGE | Birmingham | West Midlands - Birmingham & Solihull | 136 | 1 | /birmingham/service-administrator-jobs | 91 | 0 | 0 | 6 | 26 | 11 | 2 | 0 | 0 |
| LIVE PAGE | Leeds | Yorkshire - West | 97 | 1 | /leeds/service-administrator-jobs | 73 | 1 | 3 | 6 | 9 | 2 | 1 | 2 | 0 |
| LIVE PAGE | Bristol | Bristol & Bath | 82 | 1 | /bristol/service-administrator-jobs | 63 | 0 | 13 | 4 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Liverpool | Merseyside - Liverpool | 43 | 1 | /liverpool/service-administrator-jobs | 39 | 0 | 0 | 1 | 2 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Sheffield | Yorkshire - South | 43 | 1 | /sheffield/service-administrator-jobs | 37 | 2 | 0 | 1 | 2 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Glasgow | Scotland West - Glasgow | 41 | 1 | /glasgow/service-administrator-jobs | 32 | 0 | 3 | 2 | 3 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Edinburgh | Scotland Central - Edinburgh & Lothians | 35 | 1 | /edinburgh/service-administrator-jobs | 32 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Nottingham | Nottinghamshire | 34 | 1 | /nottingham/jobs | 15 | 8 | 3 | 2 | 3 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Bradford | Yorkshire - West | 32 | 1 | /bradford/service-administrator-jobs | 22 | 2 | 5 | 0 | 3 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Leicester | Leicestershire | 29 | 1 | /leicester/service-administrator-jobs | 20 | 0 | 6 | 0 | 2 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Milton Keynes | Buckinghamshire | 29 | 1 | /milton-keynes/service-administrator-jobs | 20 | 0 | 0 | 7 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Warrington | Cheshire - Warrington & Halton | 29 | 1 | /warrington/service-administrator-jobs | 25 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Southampton | Hampshire | 28 | 2 | /southampton/service-administrator-jobs, /southampton/support-worker | 12 | 9 | 6 | 0 | 0 | 0 | 1 | 0 | 0 |
| LIVE PAGE | Exeter | Devon | 26 | 1 | /exeter/service-administrator-jobs | 23 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Peterborough | Cambridgeshire | 25 | 1 | /peterborough/service-administrator-jobs | 19 | 0 | 4 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Cambridge | Cambridgeshire | 24 | 1 | /cambridge/service-administrator-jobs | 19 | 0 | 2 | 1 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Oxford | Oxfordshire | 24 | 1 | /oxford/service-administrator-jobs | 15 | 5 | 3 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Huddersfield | Yorkshire - West | 22 | 1 | /huddersfield/service-administrator-jobs | 14 | 2 | 5 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Newcastle | North East - Tyneside, Wearside & Northumberland | 22 | 1 | /newcastle/service-administrator-jobs | 12 | 2 | 7 | 0 | 0 | 0 | 0 | 1 | 0 |
| LIVE PAGE | Northampton | Northamptonshire | 22 | 1 | /northampton/service-administrator-jobs | 11 | 0 | 8 | 0 | 0 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Norwich | Norfolk | 22 | 1 | /norwich/jobs | 11 | 0 | 7 | 2 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Reading | Berkshire | 22 | 1 | /reading/jobs | 12 | 4 | 3 | 0 | 2 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Blackburn | Lancashire - East | 21 | 1 | /blackburn/jobs | 20 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Cardiff | Wales South - Cardiff & Vale | 21 | 1 | /cardiff/service-administrator-jobs | 21 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Coventry | West Midlands - Coventry & Warwickshire | 21 | 1 | /coventry/service-administrator-jobs | 13 | 0 | 2 | 0 | 0 | 5 | 0 | 1 | 0 |
| LIVE PAGE | Bolton | Greater Manchester - Wigan & Bolton | 20 | 1 | /bolton/jobs | 19 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Gloucester | Gloucestershire | 20 | 1 | /gloucester/service-administrator-jobs | 17 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Poole | Dorset | 18 | 1 | /poole/service-administrator-jobs | 13 | 1 | 2 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Warwick | West Midlands - Coventry & Warwickshire | 18 | 1 | /warwick/service-administrator-jobs | 12 | 0 | 1 | 1 | 0 | 3 | 0 | 1 | 0 |
| LIVE PAGE | Chester | Cheshire - West | 17 | 1 | /chester/jobs | 14 | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Derby | Derbyshire | 17 | 1 | /derby/jobs | 15 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Chelmsford | Essex | 16 | 1 | /chelmsford/service-administrator-jobs | 9 | 3 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Ipswich | Suffolk | 16 | 1 | /ipswich/jobs | 11 | 0 | 4 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Macclesfield | Cheshire - East | 16 | 1 | /macclesfield/service-administrator-jobs | 14 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Portsmouth | Hampshire | 16 | 1 | /portsmouth/service-administrator-jobs | 14 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Stockport | Greater Manchester - South | 16 | 1 | /stockport/service-administrator-jobs | 15 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Swindon | Wiltshire | 16 | 1 | /swindon/service-administrator-jobs | 15 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Doncaster | Yorkshire - South | 15 | 1 | /doncaster/service-administrator-jobs | 12 | 0 | 0 | 1 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Guildford | Surrey | 15 | 1 | /guildford/jobs | 7 | 1 | 6 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bedford | Bedfordshire | 14 | 1 | /bedford/service-administrator-jobs | 8 | 0 | 4 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Bournemouth | Dorset | 14 | 1 | /bournemouth/service-administrator-jobs | 6 | 5 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bracknell | Berkshire | 13 | 1 | /bracknell/jobs | 8 | 1 | 2 | 0 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Harrogate | Yorkshire - North | 13 | 1 | /harrogate/service-administrator-jobs | 12 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wakefield | Yorkshire - West | 13 | 1 | /wakefield/jobs | 9 | 0 | 2 | 1 | 0 | 0 | 1 | 0 | 0 |
| LIVE PAGE | Brighton & Hove | Sussex | 12 | 1 | /brighton-hove/service-administrator-jobs | 6 | 3 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Chesterfield | Derbyshire | 12 | 1 | /chesterfield/jobs | 10 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Crawley | Sussex | 12 | 1 | /crawley/service-administrator-jobs | 7 | 2 | 1 | 0 | 0 | 1 | 0 | 1 | 0 |
| LIVE PAGE | Dartford | Kent | 12 | 1 | /dartford/service-administrator-jobs | 10 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Preston | Lancashire - Central | 12 | 1 | /preston/jobs | 9 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Shrewsbury | Shropshire | 12 | 1 | /shrewsbury/service-administrator-jobs | 9 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Dudley | West Midlands - Black Country | 11 | 1 | /dudley/jobs | 10 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Salford | Greater Manchester - Manchester & Salford | 11 | 1 | /salford/jobs | 6 | 1 | 1 | 0 | 0 | 3 | 0 | 0 | 0 |
| LIVE PAGE | York | Yorkshire - North | 11 | 1 | /york/service-administrator-jobs | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Altrincham | Greater Manchester - South | 10 | 1 | /altrincham/service-administrator-jobs | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bath | Bristol & Bath | 10 | 1 | /bath/service-administrator-jobs | 7 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Belfast | Northern Ireland - East | 10 | 1 | /belfast/service-administrator-jobs | 9 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Cheltenham | Gloucestershire | 10 | 1 | /cheltenham/jobs | 6 | 0 | 1 | 0 | 1 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Colchester | Essex | 10 | 1 | /colchester/jobs | 3 | 4 | 1 | 0 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Hemel Hempstead | Hertfordshire | 10 | 1 | /hemel-hempstead/service-administrator-jobs | 6 | 0 | 1 | 0 | 0 | 3 | 0 | 0 | 0 |
| LIVE PAGE | High Wycombe | Buckinghamshire | 10 | 1 | /high-wycombe/jobs | 8 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Maidstone | Kent | 10 | 1 | /maidstone/service-administrator-jobs | 6 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Redhill | Surrey | 10 | 1 | /redhill/jobs | 9 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Walsall | West Midlands - Black Country | 10 | 1 | /walsall/service-administrator-jobs | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Watford | Hertfordshire | 10 | 1 | /watford/service-administrator-jobs | 6 | 0 | 3 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wrexham | North Wales - East | 10 | 1 | /wrexham/jobs | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Corby | Northamptonshire | 9 | 1 | /corby/jobs | 7 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Horsham | Sussex | 9 | 1 | /horsham/service-administrator-jobs | 6 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Kettering | Northamptonshire | 9 | 1 | /kettering/jobs | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Luton | Bedfordshire | 9 | 1 | /luton/jobs | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Newport | Wales South -gwent | 9 | 1 | /newport/jobs | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Rotherham | Yorkshire - South | 9 | 1 | /rotherham/service-administrator-jobs | 5 | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Rugby | West Midlands - Coventry & Warwickshire | 9 | 1 | /rugby/jobs | 4 | 0 | 3 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Sittingbourne | Kent | 9 | 1 | /sittingbourne/jobs | 4 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Stoke-on-trent | Staffordshire | 9 | 1 | /stoke-on-trent/service-administrator-jobs | 8 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Sunderland | North East - Tyneside, Wearside & Northumberland | 9 | 1 | /sunderland/service-administrator-jobs | 4 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Woking | Surrey | 9 | 1 | /woking/jobs | 8 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Ashford | Kent | 8 | 1 | /ashford/service-administrator-jobs | 5 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Basingstoke | Hampshire | 8 | 1 | /basingstoke/service-administrator-jobs | 3 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Canterbury | Kent | 8 | 1 | /canterbury/jobs | 4 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Hull | Yorkshire - East | 8 | 1 | /hull/service-administrator-jobs | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Redditch | Worcestershire | 8 | 1 | /redditch/jobs | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Stevenage | Hertfordshire | 8 | 1 | /stevenage/jobs | 4 | 0 | 2 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Swansea | Wales South - Swansea Bay | 8 | 1 | /swansea/service-administrator-jobs | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Worcester | Worcestershire | 8 | 1 | /worcester/service-administrator-jobs | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Aylesbury | Buckinghamshire | 7 | 1 | /aylesbury/service-administrator-jobs | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Dundee | Scotland Central - Tayside | 7 | 1 | /dundee/jobs | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Leatherhead | Surrey | 7 | 1 | /leatherhead/jobs | 4 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Solihull | West Midlands - Birmingham & Solihull | 7 | 1 | /solihull/jobs | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Barnsley | Yorkshire - South | 6 | 1 | /barnsley/service-administrator-jobs | 4 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Crewe | Cheshire - East | 6 | 1 | /crewe/jobs | 4 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Eastleigh | Hampshire | 6 | 1 | /eastleigh/service-administrator-jobs | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Gateshead | North East - Tyneside, Wearside & Northumberland | 6 | 1 | /gateshead/jobs | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Northallerton | Yorkshire - North | 6 | 1 | /northallerton/jobs | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Plymouth | Devon | 6 | 1 | /plymouth/service-administrator-jobs | 5 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Trafford | Greater Manchester - South | 6 | 1 | /trafford/jobs | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Carlisle | Cumbria - North | 5 | 1 | /carlisle/jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Farnham | Surrey | 5 | 1 | /farnham/service-administrator-jobs | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| LIVE PAGE | Hereford | Herefordshire | 5 | 1 | /hereford/jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wirral | Merseyside - Wirral | 5 | 1 | /wirral/jobs | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Abingdon | Oxfordshire | 4 | 1 | /abingdon/jobs | 3 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Durham | North East - County Durham & Darlington/Hartlepool | 4 | 1 | /durham/jobs | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Hertford | Hertfordshire | 4 | 1 | /hertford/jobs | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | King's Lynn | Norfolk | 4 | 1 | /kings-lynn/jobs | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Oldham | Greater Manchester - North | 4 | 1 | /oldham/jobs | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Stafford | Staffordshire | 4 | 1 | /stafford/jobs | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Yeovil | Somerset | 4 | 1 | /yeovil/jobs | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Scarborough | Yorkshire - North | 3 | 1 | /scarborough/service-administrator-jobs | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Lincoln | Lincolnshire | 2 | 1 | /lincoln/service-administrator-jobs | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Witney | Oxfordshire | 2 | 1 | /witney/jobs | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Newtownabbey | Northern Ireland - East | 1 | 1 | /newtownabbey/service-administrator-jobs | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Chester Le Street |  | 0 | 1 | /chester-le-street/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wigston |  | 0 | 1 | /wigston/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Uxbridge | London | 20 | 0 |  | 16 | 1 | 0 | 0 | 0 | 2 | 0 | 1 | 0 |
| HOLD – LONDON | Croydon | London | 13 | 0 |  | 9 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Surbiton | London | 10 | 0 |  | 6 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Kingston Upon Thames | London | 8 | 0 |  | 6 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Bexley | London | 6 | 0 |  | 4 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Bromley | London | 6 | 0 |  | 3 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Harrow | London | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Beckenham | London | 5 | 0 |  | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Edgware | London | 5 | 0 |  | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Sutton | London | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| HOLD – LONDON | Brentford | London | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Enfield | London | 4 | 0 |  | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hounslow | London | 4 | 0 |  | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Islington | London | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| HOLD – LONDON | Newham | London | 4 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Romford | London | 4 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Barking | London | 3 | 0 |  | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Borehamwood | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Erith | London | 3 | 0 |  | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Feltham | London | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Ilford | London | 3 | 0 |  | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Lambeth | London | 3 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| HOLD – LONDON | Morden | London | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | New Malden | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Orpington | London | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | South Croydon | London | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Twickenham | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wallington | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wembley | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Dagenham | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Greenford | London | 2 | 0 |  | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hammersmith And Fulham | London | 2 | 0 |  | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hayes | London | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Hillingdon | London | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Isleworth | London | 2 | 0 |  | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Loughton | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Northwood | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Southall | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wandsworth | London | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Barnet | London | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Bexleyheath | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Brixton | London | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hackney | London | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Mitcham | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Northolt | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Rainham | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Ruislip | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Sidcup | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Southwark | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Teddington | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | West Drayton | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | West Wickham | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Woodford Green | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hastings | Sussex | 10 | 0 |  | 1 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Basildon | Essex | 9 | 0 |  | 3 | 2 | 2 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Sevenoaks | Kent | 8 | 0 |  | 3 | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Trowbridge | Wiltshire | 8 | 0 |  | 2 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Salisbury | Wiltshire | 7 | 0 |  | 1 | 3 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| MONITOR | Godalming | Surrey | 6 | 0 |  | 2 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 |
| MONITOR | Winsford | Cheshire - West | 6 | 0 |  | 3 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| MONITOR | Braintree | Essex | 5 | 0 |  | 1 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dorchester | Dorset | 5 | 0 |  | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Felixstowe | Suffolk | 5 | 0 |  | 3 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Heanor | Derbyshire | 5 | 0 |  | 2 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Horley | Surrey | 5 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| MONITOR | Hove | Sussex | 5 | 0 |  | 3 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newbury | Berkshire | 5 | 0 |  | 2 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Wokingham | Berkshire | 5 | 0 |  | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Worksop | Nottinghamshire | 5 | 0 |  | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Andover | Hampshire | 4 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bicester | Oxfordshire | 4 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dorking | Surrey | 4 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | East Grinstead | Sussex | 4 | 0 |  | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Farnborough | Hampshire | 4 | 0 |  | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Ferndown | Dorset | 4 | 0 |  | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Haywards Heath | Sussex | 4 | 0 |  | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Huntingdon | Cambridgeshire | 4 | 0 |  | 3 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | New Milton | Hampshire | 4 | 0 |  | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newmarket | Suffolk | 4 | 0 |  | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Nuneaton | West Midlands - Coventry & Warwickshire | 4 | 0 |  | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Reigate | Surrey | 4 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Runcorn | Cheshire - Warrington & Halton | 4 | 0 |  | 3 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Sowerby Bridge | Yorkshire - West | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stone | Staffordshire | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Waterlooville | Hampshire | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wellingborough | Northamptonshire | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Weybridge | Surrey | 4 | 0 |  | 2 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Alton | Hampshire | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bagshot | Surrey | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| MONITOR | Banbury | Oxfordshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bishop Auckland | North East - County Durham & Darlington/Hartlepool | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Blandford Forum | Dorset | 3 | 0 |  | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bordon | Hampshire | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridgwater | Somerset | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Burgess Hill | Sussex | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Burnley | Lancashire - East | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Camberley | Surrey | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chelmsley Wood | West Midlands - Birmingham & Solihull | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Christchurch | Dorset | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cirencester | Gloucestershire | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Coalville | Leicestershire | 3 | 0 |  | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| MONITOR | Conwy | North Wales - East | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dereham | Norfolk | 3 | 0 |  | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Eccles | Greater Manchester - Manchester & Salford | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ellesmere Port | Cheshire - West | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Epsom | Surrey | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Falmouth | Cornwall | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gillingham | Kent | 3 | 0 |  | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Goole | Yorkshire - East | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gosport | Hampshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hailsham | Sussex | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Harpenden | Hertfordshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Heathfield | Sussex | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kirkcaldy | Scotland Central - Fife | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knutsford | Cheshire - East | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lancing | Sussex | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Maldon | Essex | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Malton | Yorkshire - North | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Montrose | North Scotland | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newark | Nottinghamshire | 3 | 0 |  | 1 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Newton-le-willows | Merseyside - St Helens & Knowsley | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | North Shields | North East - Tyneside, Wearside & Northumberland | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Northfleet | Kent | 3 | 0 |  | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Perth | Scotland Central - Tayside | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pontypridd | Wales South - Valleys | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Potters Bar | Hertfordshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Richmond | Yorkshire - North | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sherborne | Dorset | 3 | 0 |  | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Leonards-on-sea | Sussex | 3 | 0 |  | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sutton Coldfield | West Midlands - Birmingham & Solihull | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Thame | Oxfordshire | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Tonbridge | Kent | 3 | 0 |  | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Wareham | Dorset | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Welwyn Garden City | Hertfordshire | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Windsor | Berkshire | 3 | 0 |  | 0 | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Witham | Essex | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Accrington | Lancashire - East | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Addlestone | Surrey | 2 | 0 |  | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Antrim | Northern Ireland - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ashington | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Aylesford | Kent | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Battle | Sussex | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bexhill-on-sea | Sussex | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridgend | Wales South - Swansea Bay | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridlington | Yorkshire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brierley Hill | West Midlands - Black Country | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brighouse | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Broadstairs | Kent | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bromsgrove | Worcestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Buckingham | Buckinghamshire | 2 | 0 |  | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| MONITOR | Buxton | Derbyshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Caerphilly | Wales South - Valleys | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cannock | Staffordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chorley | Lancashire - Central | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Clacton-on-sea | Essex | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cleckheaton | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Consett | North East - County Durham & Darlington/Hartlepool | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Corsham | Wiltshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cramlington | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cranleigh | Surrey | 2 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Dalkeith | Scotland Central - Edinburgh & Lothians | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Darwen | Lancashire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Denton | Greater Manchester - South | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dewsbury | Yorkshire - West | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Dover | Kent | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Droitwich | Worcestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Elgin | North Scotland | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Epping | Essex | 2 | 0 |  | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Evesham | Worcestershire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Falkirk | Scotland Central - Falkirk & Stirling | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fetcham | Surrey | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fleet | Hampshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fordingbridge | Hampshire | 2 | 0 |  | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Frome | Somerset | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gravesend | Kent | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grays | Essex | 2 | 0 |  | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| MONITOR | Great Yarmouth | Norfolk | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Halesowen | West Midlands - Black Country | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Harlow | Essex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hatfield | Hertfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hedge End | Hampshire | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Henley-on-thames | Oxfordshire | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Herne Bay | Kent | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hook | Hampshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hook Norton | Oxfordshire | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ilminster | Somerset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Inverness | North Scotland | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Irchester | Northamptonshire | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kingswinford | West Midlands - Black Country | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knaresborough | Yorkshire - North | 2 | 0 |  | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Knowsley | Merseyside - St Helens & Knowsley | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leigh-on-sea | Essex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leighton Buzzard | Bedfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lewes | Sussex | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leyland | Lancashire - Central | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Littlehampton | Sussex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lowestoft | Suffolk | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lydney | Gloucestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Marlborough | Wiltshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Marlow | Buckinghamshire | 2 | 0 |  | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Melksham | Wiltshire | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Normanton | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pontefract | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Prenton | Merseyside - Wirral | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Radstock | Somerset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ramsbottom | Greater Manchester - North | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ramsgate | Kent | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ringwood | Hampshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Romsey | Hampshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Royston | Hertfordshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sandwich | Kent | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sedgefield | North East - County Durham & Darlington/Hartlepool | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shefford | Bedfordshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Silsden | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Skipton | Yorkshire - North | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | South Shields | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Southsea | Hampshire | 2 | 0 |  | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Southwick | Sussex | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St Helens | Merseyside - St Helens & Knowsley | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Albans | Hertfordshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Helens | Merseyside - St Helens & Knowsley | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stratford-upon-avon | West Midlands - Coventry & Warwickshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stretford | Greater Manchester - Manchester & Salford | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stroud | Gloucestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Studley | West Midlands - Coventry & Warwickshire | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Sudbury | Suffolk | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Sunbury-on-thames | Surrey | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tewkesbury | Gloucestershire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tonypandy | Wales South - Valleys | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Totton | Hampshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Truro | Cornwall | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ulverston | Cumbria - South | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wallingford | Oxfordshire | 2 | 0 |  | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wallsend | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Waltham Abbey | Essex | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Warminster | Wiltshire | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wells | Somerset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | West Malling | Kent | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weston-super-mare | Somerset | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wickford | Essex | 2 | 0 |  | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Widnes | Cheshire - Warrington & Halton | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wimborne | Dorset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Woodbridge | Suffolk | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wymondham | Norfolk | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Aberdare | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Abergavenny | Wales South - Gwent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Axbridge | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bamber Bridge | Lancashire - Central | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Barrow-in-furness | Cumbria - South | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Beaconsfield | Buckinghamshire | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bedale | Yorkshire - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bedlington | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Belper | Derbyshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Benfleet | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bentley | Yorkshire - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Biggleswade | Bedfordshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bishop's Stortford | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Blaydon-on-Tyne | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Blyth | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bodmin | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bognor Regis | Sussex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Boreham | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridgnorth | Shropshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bury St. Edmunds | Suffolk | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Calne | Wiltshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chapelhall | Scotland West - Lanarkshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chatham | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chesham | Buckinghamshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Clitheroe | Lancashire - East | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Coatbridge | Scotland West - Lanarkshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cobham | Surrey | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Colden Common | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cosham | Hampshire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Crowthorne | Berkshire | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Deal | Kent | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Devizes | Wiltshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Diss | Norfolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dunfermline | Scotland Central - Fife | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Duxford | Cambridgeshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Egham | Surrey | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ely | Cambridgeshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Emsworth | Hampshire | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Esher | Surrey | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fairford | Gloucestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Featherstone | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Folkestone | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Frinton-on-sea | Essex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gerrards Cross | Buckinghamshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Glenfield | Leicestershire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Glenrothes | Scotland Central - Fife | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grangemouth | Scotland Central - Falkirk & Stirling | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hartlepool | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Harwich | Essex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Haslingden | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hexham | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Heywood | Greater Manchester - North | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Hindhead | Surrey | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Holmfirth | Yorkshire - West | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Honiton | Devon | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hyde | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hythe | Kent | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ivybridge | Devon | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Jarrow | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kidderminster | Worcestershire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Kidlington | Oxfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kingsteignton | Devon | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Kirriemuir | Scotland Central - Tayside | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knaphill | Surrey | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knowle | West Midlands - Birmingham & Solihull | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ledbury | Herefordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lichfield | Staffordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lisburn | Northern Ireland - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Liskeard | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Liversedge | Yorkshire - West | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lutterworth | Leicestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lyndhurst | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Market Harborough | Leicestershire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Midhurst | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Mold | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Morpeth | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Motherwell | Scotland West - Lanarkshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Mountain Ash | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Nantwich | Cheshire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Nelson | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newquay | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newton Abbot | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newton Aycliffe | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newtownards | Northern Ireland - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Northwich | Cheshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Olney | Buckinghamshire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Oswestry | Shropshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Oxted | Surrey | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Paignton | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Penicuik | Scotland Central - Edinburgh & Lothians | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Peterlee | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pontypool | Wales South - Gwent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Port Talbot | Wales South - Swansea Bay | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Portishead | Bristol & Bath | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Prestatyn | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Prestonpans | Scotland Central - Edinburgh & Lothians | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pulborough | Sussex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Radcliffe | Greater Manchester - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rayleigh | Essex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Redruth | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rhyl | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ripley | Derbyshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rochester | Kent | 1 | 0 |  | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Ross-on-wye | Herefordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rossett | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rushden | Northamptonshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ryde | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Saltash | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Saltdean | Sussex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Scunthorpe | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Seaham | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Selby | Yorkshire - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shaftesbury | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sherburn In Elmet | Yorkshire - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shildon | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shoreham-by-sea | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Skegness | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sleaford | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Smethwick | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Snodland | Kent | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Austell | Cornwall | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Stanford-le-hope | Essex | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stanley | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stockton-on-tees | North East - Tees Valley | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stourbridge | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Swadlincote | Derbyshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tadley | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Takeley | Essex | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tarporley | Cheshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tavistock | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Thatcham | Berkshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Thornaby | North East - Tees Valley | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tiverton | Devon | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Torquay | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tredegar | Wales South - Gwent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tring | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Uckfield | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Urmston | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Uttoxeter | Staffordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Verwood | Dorset | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Waltham | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wednesbury | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Welwyn | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Westbury | Wiltshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Westerham | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weymouth | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Whyteleafe | Surrey | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Willand | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Woodhall Spa | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Worsley | Greater Manchester - Manchester & Salford | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Yarm | North East - Tees Valley | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Yate | Bristol & Bath | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

> LIVE counts come directly from the current published `app/` JSON, deduplicated within each canonical region/family slice while preserving legitimate appearances in more than one family. This is the live-site authority for the reconciliation above; the dated source-count CSV is shown only as a freshness cross-check. The overview covers all 78 assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 78-market coverage has run, NOT LIVE Admin/Support and Customer Service may fall back to the latest all-region Module 2 profile (2026-08-17), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-11-20) used by the production family run, across 78 UK markets with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across 78 UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across 78, 78, 78 and 78 UK markets respectively, using their governed production boundaries and canonical geo. NOT LIVE Customer Service / Contact Centre was assessed from that same feed across 78 UK markets using its governed exact-title, salary and geography rules. All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

## LIVE

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire | 42 |  | 6 | 4 |  | 17 |  |  |
| Berkshire | 71 | 14 | 13 | 16 | 23 | 34 | 3 |  |
| Bristol & Bath | 82 |  | 15 | 10 | 7 | 26 |  |  |
| Buckinghamshire | 86 |  |  | 19 | 22 | 36 | 2 | 3 |
| Cambridgeshire | 73 |  | 9 | 4 | 11 | 31 |  |  |
| Cheshire - East | 30 |  | 5 |  |  | 24 |  |  |
| Cheshire - Warrington & Halton | 34 |  |  |  | 6 | 17 |  |  |
| Cheshire - West | 23 |  |  |  | 4 | 11 |  |  |
| Cornwall | 10 |  |  |  |  | 6 |  |  |
| Cumbria - North | 5 |  |  |  |  |  |  |  |
| Cumbria - South |  | 3 |  |  |  |  |  |  |
| Cumbria - West |  |  |  |  |  |  |  |  |
| Derbyshire | 59 |  | 4 |  |  | 24 |  |  |
| Devon | 71 |  | 3 | 6 |  | 22 |  |  |
| Dorset | 60 | 19 | 9 |  | 1 | 28 |  |  |
| Essex | 119 | 29 | 11 | 19 | 12 | 48 | 4 |  |
| Gloucestershire | 86 |  | 5 |  | 5 | 30 | 2 |  |
| Greater Manchester - Manchester & Salford | 153 | 7 | 19 | 29 | 32 | 59 | 4 | 7 |
| Greater Manchester - North | 19 |  |  |  |  | 19 |  |  |
| Greater Manchester - South | 40 |  |  |  | CHECK | 9 |  |  |
| Greater Manchester - Wigan & Bolton | 32 |  |  |  |  | 9 |  |  |
| Hampshire | 162 | 31 | 25 | 10 | 9 | 60 | 5 | 7 |
| Herefordshire | 7 |  |  |  |  | CHECK |  |  |
| Hertfordshire | 99 |  | 8 | 13 | 8 | 32 |  | 2 |
| Kent | 123 | 27 | 16 | 12 | 21 | 54 |  | 3 |
| Lancashire - Blackpool & Fylde | 6 |  |  |  |  |  |  |  |
| Lancashire - Central | 17 |  |  |  |  | 10 |  |  |
| Lancashire - East | 28 |  |  |  |  | 11 |  |  |
| Lancashire - North |  |  |  |  |  |  |  |  |
| Lancashire - West |  |  |  |  |  |  |  |  |
| Leicestershire | 80 |  | 7 |  | 9 | 23 | 7 |  |
| Lincolnshire | 33 |  |  | 2 |  | 10 |  |  |
| London | 449 | 99 | 94 | 111 | 146 | 204 | 36 | 11 |
| Merseyside - Liverpool | 44 |  |  | 8 | 5 | 24 |  |  |
| Merseyside - Sefton |  |  |  |  |  |  |  |  |
| Merseyside - St Helens & Knowsley | 9 |  |  |  |  |  |  |  |
| Merseyside - Wirral | 11 |  |  |  |  | 8 |  |  |
| Norfolk | 46 |  | 10 | 8 | 9 | 21 |  |  |
| North East | 95 | 21 | 21 | 8 | 16 | 33 | 4 | 9 |
| North Scotland | 14 |  | 3 |  |  |  |  |  |
| North Wales - East | 21 |  |  |  |  |  |  |  |
| North Wales - West |  |  |  |  |  |  |  |  |
| Northamptonshire | 70 |  | 13 |  | 8 | 29 |  |  |
| Northern Ireland - East | 15 |  |  |  | 1 | CHECK | CHECK |  |
| Northern Ireland - West |  |  |  |  |  |  |  |  |
| Nottinghamshire | 69 | 19 | 8 | 5 | 12 | 32 | 4 |  |
| Oxfordshire | 79 | 9 | 8 | 7 | 7 | 25 |  |  |
| Rutland |  |  |  |  |  |  |  |  |
| Scotland - Borders |  |  |  |  |  |  |  |  |
| Scotland Central - Edinburgh & Lothians | 43 |  |  | 6 |  | 14 |  |  |
| Scotland Central - Falkirk & Stirling | 8 |  |  |  |  |  |  |  |
| Scotland Central - Fife | 9 |  |  |  |  |  |  |  |
| Scotland Central - Tayside | 11 |  |  |  |  |  |  |  |
| Scotland West - Ayrshire |  |  |  |  |  |  |  |  |
| Scotland West - Glasgow | 41 |  | 12 | 4 | 9 | 11 |  |  |
| Scotland West - Lanarkshire | 3 |  |  |  |  |  |  |  |
| Scotland West - Renfrewshire & Inverclyde |  |  |  |  |  |  |  |  |
| Shropshire | 45 |  |  |  | 7 | 12 |  |  |
| Somerset | 41 |  | 7 |  |  | 12 |  |  |
| Staffordshire | 63 |  |  |  | 5 | 18 | 6 | 5 |
| Suffolk | 58 |  | 10 | 1 |  | 21 | 1 |  |
| Surrey | 164 | 10 | 21 | 10 | 29 | 70 | 8 | 12 |
| Sussex | 137 | 55 | 10 | 25 | 13 | 42 | 3 | 5 |
| Wales - Mid |  |  |  |  |  |  |  |  |
| Wales - West |  |  |  |  |  |  |  |  |
| Wales South - Cardiff & Vale | 21 |  |  |  |  | 7 |  |  |
| Wales South - Gwent | 16 |  |  |  |  |  |  |  |
| Wales South - Swansea Bay | 11 |  |  |  |  |  |  |  |
| Wales South - Valleys | 10 |  |  |  |  |  |  |  |
| West Midlands - Birmingham & Solihull | 154 |  |  | 8 | 31 | 40 | 6 |  |
| West Midlands - Black Country | 61 |  |  |  |  | 24 | 3 |  |
| West Midlands - Coventry & Warwickshire | 95 |  | 8 | 7 | 8 | 54 | CHECK | 3 |
| Wiltshire | 49 | 15 |  |  |  | 12 |  |  |
| Worcestershire | 44 |  | 5 |  |  | 14 |  |  |
| Yorkshire - East | 18 |  |  |  |  | 8 |  |  |
| Yorkshire - North | 44 |  |  | 9 | 5 | 19 |  |  |
| Yorkshire - South | 74 | 5 |  | 4 | 8 | 27 |  |  |
| Yorkshire - West | 180 | 7 | 20 | 15 | 25 | 86 | 5 | 7 |

## NOT LIVE

> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire |  | 5 / 4.3 / 0/14 |  |  | 2 / 3.4 / 0/14 |  | 0 / 0.5 / 0/14 | 4 / 4.0 / 0/14 |
| Berkshire |  |  |  |  |  |  |  | 4 / 1.9 / 0/14 |
| Bristol & Bath |  | 15 / 9.4 / 14/14 |  |  |  |  | 4 / 4.3 / 0/14 | 4 / 4.0 / 0/14 |
| Buckinghamshire |  | 3 / 2.1 / 0/14 | 6 / 6.1 / 10/14 |  |  |  |  |  |
| Cambridgeshire |  | 2 / 1.5 / 0/14 |  |  |  |  | 0 / 0.9 / 0/14 | 4 / 2.0 / 0/14 |
| Cheshire - East |  | 7 / 5.6 / 4/14 |  | 0 / 0.6 / 0/14 | 3 / 2.4 / 0/14 |  | 0 / 0.0 / 0/14 | 1 / 2.1 / 0/14 |
| Cheshire - Warrington & Halton |  | 7 / 6.5 / 14/14 | 2 / 2.5 / 0/14 | 1 / 0.9 / 0/14 |  |  | 0 / 0.4 / 0/14 | 2 / 2.1 / 0/14 |
| Cheshire - West |  | 4 / 3.1 / 0/14 | 1 / 1.9 / 0/14 | 4 / 4.0 / 0/14 |  |  | 1 / 1.0 / 0/14 | 1 / 0.2 / 0/14 |
| Cornwall |  | 5 / 4.9 / 5/14 | 2 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |  | 0 / 0.0 / 0/14 | 0 / 0.5 / 0/14 |
| Cumbria - North |  | 3 / 7.6 / 11/14 | 5 / 4.9 / 1/14 | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 | 2 / 2.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Cumbria - South | 11 / 6.1 / 7/14 |  | 0 / 0.2 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.5 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Cumbria - West | 1 / 3.6 / 2/14 | 6 / 4.6 / 4/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Derbyshire |  | 7 / 5.6 / 5/14 |  | 4 / 3.8 / 0/14 | 10 / 8.8 / 10/14 |  | 5 / 1.6 / 0/14 | 1 / 2.2 / 0/14 |
| Devon |  | 15 / 13.6 / 14/14 |  |  | 1 / 3.1 / 0/14 |  | 2 / 2.7 / 0/14 | 5 / 5.4 / 6/14 |
| Dorset |  |  |  | 2 / 4.6 / 3/14 |  |  | 3 / 2.6 / 0/14 | 7 / 4.6 / 4/14 |
| Essex |  |  |  |  |  |  |  | 5 / 5.5 / 6/14 |
| Gloucestershire |  | 14 / 9.3 / 14/14 |  | 7 / 5.8 / 10/14 |  |  |  | 6 / 3.0 / 3/14 |
| Greater Manchester - Manchester & Salford |  |  |  |  |  |  |  |  |
| Greater Manchester - North |  | 6 / 2.4 / 2/14 | 3 / 2.1 / 0/14 | 1 / 2.3 / 0/14 | 2 / 2.2 / 0/14 |  | 0 / 0.7 / 0/14 | 1 / 1.4 / 0/14 |
| Greater Manchester - South |  | 0 / 1.1 / 0/14 | 3 / 3.0 / 0/14 | 3 / 3.9 / 0/14 |  |  | 2 / 1.6 / 0/14 | 0 / 0.0 / 0/14 |
| Greater Manchester - Wigan & Bolton |  | 3 / 2.8 / 0/14 | 1 / 1.5 / 0/14 | 1 / 1.6 / 0/14 | 1 / 1.0 / 0/14 |  | 0 / 0.3 / 0/14 | 6 / 3.8 / 1/14 |
| Hampshire |  |  |  |  |  |  |  |  |
| Herefordshire |  | 2 / 2.0 / 0/14 | 1 / 0.7 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.1 / 0/14 |  | 1 / 1.4 / 0/14 | 0 / 0.0 / 0/14 |
| Hertfordshire |  | 4 / 4.6 / 7/14 |  |  |  |  | 4 / 3.3 / 0/14 |  |
| Kent |  |  |  |  |  |  | 3 / 4.1 / 0/14 |  |
| Lancashire - Blackpool & Fylde |  | 2 / 1.2 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 2 / 0.8 / 0/14 | 4 / 3.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - Central |  | 4 / 3.4 / 0/14 | 3 / 3.5 / 0/14 | 0 / 0.0 / 0/14 | 5 / 4.1 / 0/14 |  | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - East |  | 4 / 2.6 / 0/14 | 2 / 1.3 / 0/14 | 3 / 3.4 / 0/14 | 1 / 0.5 / 0/14 |  | 1 / 1.3 / 0/14 | 2 / 1.8 / 0/14 |
| Lancashire - North | 4 / 2.6 / 0/14 | 2 / 1.6 / 0/14 | 2 / 1.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.7 / 0/14 | 2 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - West | 6 / 4.9 / 5/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.0 / 0/14 | 4 / 3.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.7 / 0/14 |
| Leicestershire |  | 6 / 6.3 / 10/14 |  | 4 / 3.2 / 0/14 |  |  |  | 4 / 3.0 / 1/14 |
| Lincolnshire |  | 11 / 7.0 / 10/14 | 7 / 5.3 / 5/14 |  | 0 / 0.0 / 0/14 |  | 0 / 0.4 / 0/14 | 2 / 1.0 / 0/14 |
| London |  |  |  |  |  |  |  |  |
| Merseyside - Liverpool |  | 1 / 0.2 / 0/14 | 1 / 1.8 / 0/14 |  |  |  | 1 / 1.7 / 0/14 | 1 / 1.0 / 0/14 |
| Merseyside - Sefton | 2 / 2.7 / 0/14 | 1 / 0.2 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.8 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Merseyside - St Helens & Knowsley |  | 1 / 0.3 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 5 / 4.9 / 2/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Merseyside - Wirral |  | 3 / 2.3 / 0/14 | 0 / 0.0 / 0/14 | 2 / 2.0 / 0/14 | 3 / 3.9 / 0/14 |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Norfolk |  | 10 / 6.4 / 9/14 |  |  |  |  | 2 / 2.8 / 0/14 | 5 / 3.1 / 0/14 |
| North East |  |  |  |  |  |  |  |  |
| North Scotland |  | 3 / 2.5 / 0/14 |  | 8 / 4.3 / 7/14 | 0 / 0.0 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.2 / 0/14 |
| North Wales - East |  | 13 / 7.9 / 11/14 | 1 / 1.4 / 0/14 | 1 / 1.0 / 0/14 | 1 / 0.5 / 0/14 | 4 / 3.4 / 0/14 | 2 / 2.2 / 0/14 | 2 / 1.8 / 0/14 |
| North Wales - West | 2 / 2.0 / 0/14 | 2 / 1.8 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Northamptonshire |  | 2 / 2.1 / 0/14 |  | 2 / 4.6 / 7/14 |  |  | 6 / 3.8 / 3/14 | 0 / 2.1 / 0/14 |
| Northern Ireland - East |  | 1 / 0.2 / 0/14 | 2 / 1.9 / 0/14 | 0 / 0.0 / 0/14 |  |  |  | 0 / 0.1 / 0/14 |
| Northern Ireland - West | 3 / 5.5 / 7/14 | 1 / 0.3 / 0/14 | 3 / 4.2 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 2.1 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.3 / 0/14 |
| Nottinghamshire |  |  |  |  |  |  |  | 2 / 0.9 / 0/14 |
| Oxfordshire |  |  |  |  |  |  | 7 / 5.4 / 8/14 | 4 / 2.1 / 0/14 |
| Rutland | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland - Borders | 2 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Edinburgh & Lothians |  | 2 / 1.2 / 0/14 | 4 / 2.7 / 0/14 |  | 3 / 2.7 / 0/14 |  | 0 / 0.0 / 0/14 | 1 / 0.1 / 0/14 |
| Scotland Central - Falkirk & Stirling |  | 1 / 0.3 / 0/14 | 2 / 1.7 / 0/14 | 3 / 3.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 2.7 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Fife |  | 1 / 0.6 / 0/14 | 2 / 2.3 / 0/14 | 2 / 1.5 / 0/14 | 0 / 0.0 / 0/14 | 4 / 1.3 / 0/14 | 1 / 1.9 / 0/14 | 1 / 0.3 / 0/14 |
| Scotland Central - Tayside |  | 0 / 0.1 / 0/14 | 3 / 3.0 / 0/14 | 1 / 0.5 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.2 / 0/14 | 0 / 0.0 / 0/14 | 3 / 2.1 / 0/14 |
| Scotland West - Ayrshire | 6 / 5.5 / 9/14 | 2 / 0.6 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.5 / 0/14 | 0 / 0.0 / 0/14 | 2 / 2.1 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland West - Glasgow |  | 1 / 0.3 / 0/14 |  |  |  |  | 3 / 1.4 / 0/14 | 4 / 2.3 / 0/14 |
| Scotland West - Lanarkshire |  | 1 / 1.3 / 0/14 | 1 / 1.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.4 / 0/14 | 0 / 0.6 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland West - Renfrewshire & Inverclyde | 4 / 4.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Shropshire |  | 3 / 4.4 / 5/14 | 8 / 6.1 / 8/14 | 3 / 2.5 / 0/14 |  |  | 3 / 3.4 / 0/14 | 3 / 2.6 / 0/14 |
| Somerset |  | 12 / 8.6 / 14/14 |  | 1 / 2.5 / 0/14 | 0 / 0.0 / 0/14 |  | 1 / 1.5 / 0/14 | 0 / 1.0 / 0/14 |
| Staffordshire |  | 4 / 4.4 / 0/14 | 7 / 5.7 / 7/14 | 2 / 3.9 / 1/14 |  |  |  |  |
| Suffolk |  | 16 / 7.9 / 6/14 |  |  | 6 / 3.9 / 3/14 |  |  | 4 / 3.1 / 0/14 |
| Surrey |  |  |  |  |  |  |  |  |
| Sussex |  |  |  |  |  |  |  |  |
| Wales - Mid | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.6 / 0/14 | 0 / 0.3 / 0/14 | 0 / 0.0 / 0/14 |
| Wales - West | 1 / 1.4 / 0/14 | 5 / 2.9 / 1/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.7 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.2 / 0/14 |
| Wales South - Cardiff & Vale |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 4 / 3.8 / 0/14 | 2 / 1.5 / 0/14 |  | 0 / 0.0 / 0/14 | 1 / 0.4 / 0/14 |
| Wales South - Gwent |  | 2 / 1.2 / 0/14 | 1 / 1.6 / 0/14 | 2 / 0.8 / 0/14 | 0 / 0.0 / 0/14 | 3 / 2.8 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.4 / 0/14 |
| Wales South - Swansea Bay |  | 4 / 2.1 / 0/14 | 0 / 0.0 / 0/14 | 2 / 0.7 / 0/14 | 0 / 0.0 / 0/14 | 5 / 4.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Valleys |  | 2 / 0.6 / 0/14 | 0 / 0.5 / 0/14 | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 4 / 4.2 / 0/14 | 1 / 1.0 / 0/14 | 1 / 0.4 / 0/14 |
| West Midlands - Birmingham & Solihull |  | 2 / 0.5 / 0/14 | 5 / 3.6 / 0/14 |  |  |  |  | 4 / 4.4 / 4/14 |
| West Midlands - Black Country |  | 7 / 3.9 / 3/14 | 3 / 5.2 / 7/14 | 0 / 0.7 / 0/14 | 1 / 2.4 / 0/14 |  |  | 4 / 3.4 / 0/14 |
| West Midlands - Coventry & Warwickshire |  | 9 / 6.6 / 12/14 |  |  |  |  |  |  |
| Wiltshire |  |  | 2 / 3.0 / 0/14 | 7 / 5.9 / 9/14 | 3 / 4.9 / 3/14 |  | 2 / 2.0 / 0/14 | 0 / 0.9 / 0/14 |
| Worcestershire |  | 7 / 5.2 / 4/14 |  | 3 / 4.2 / 0/14 | 2 / 1.4 / 0/14 |  | 2 / 1.6 / 0/14 | 3 / 1.2 / 0/14 |
| Yorkshire - East |  | 3 / 1.9 / 0/14 | 3 / 3.4 / 0/14 | 4 / 3.6 / 0/14 | 1 / 1.9 / 0/14 |  | 0 / 0.5 / 0/14 | 0 / 0.0 / 0/14 |
| Yorkshire - North |  | 10 / 12.6 / 14/14 | 5 / 5.3 / 6/14 |  |  |  | 0 / 0.0 / 0/14 | 1 / 0.7 / 0/14 |
| Yorkshire - South |  |  | 5 / 3.9 / 2/14 |  |  |  | 0 / 2.1 / 0/14 | 5 / 3.8 / 0/14 |
| Yorkshire - West |  |  |  |  |  |  |  |  |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Live regions | 65 / 78 | 16 / 78 | 30 / 78 | 28 / 78 | 33 / 78 | 53 / 78 | 19 / 78 | 12 / 78 |
| Live slice placements | 3972 | 370 | 405 | 380 | 514 + 1 CHECK | 1517 + 2 CHECK | 103 + 2 CHECK | 74 |

**Live slices: 256 / 624.**
