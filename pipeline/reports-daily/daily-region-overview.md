# Ontap daily regional overview

Production source commit: `a63e09d440f5263a01ab2d42e166dec78e99d87d`

Generated: 2026-11-25T10:01:35+00:00

[Download this overview as Excel](./daily-region-overview.xlsx)

## SITEWIDE RECONCILIATION

| Measure | Count |
|---|---:|
| Unique live jobs | 5,719 |
| Unique JobG8 jobs | 5,424 |
| Unique non-JobG8 jobs | 295 |
| Regional/category slice placements | 7,289 |
| Jobs appearing on multiple slices | 1,556 |
| Extra slice placements | 1,570 |
| Unique jobs outside governed slices | 0 |
| Jobs found in non-LIVE slices | 0 |

**Reconciliation: 5,719 unique jobs + 1,570 extra slice placements = 7,289 regional/category slice placements.**

Latest source-count CSV: `pipeline/reports-daily/live-job-source-count-2026-11-25.csv` — **STALE — CSV says 5,993 for 2026-11-25**.

### Provider breakdown

| Provider | Unique live jobs | Jobs on 2+ slices | Extra slice placements |
|---|---:|---:|---:|
| JobG8 | 5,424 | 1,556 | 1,570 |
| NHS Jobs | 287 | 0 | 0 |
| Teaching Vacancies | 8 | 0 | 0 |

## JOBG8 FEED RECEIVED

**JobG8 jobs received: 42,710** (feed date: 2026-11-25)

| JobG8 classification | Jobs received | Ontap jobs classified/published |
|---|---:|---:|
| Accounting | 7,950 | 1,733 |
| Education | 7,741 | 57 |
| Transport & Logistics | 7,078 | 161 |
| Healthcare & Medical | 4,608 | 394 |
| Sales & Marketing | 3,186 | 896 |
| Legal | 2,810 | 483 |
| Banking & Financial Services | 1,765 | 62 |
| Administration | 1,580 | 1,022 |
| Real Estate & Property | 1,333 | 67 |
| HR / Recruitment | 1,193 | 153 |
| I.T. & Communications | 1,013 | 1 |
| Insurance & Superannuation | 860 | 25 |
| Call Centre / CustomerService | 744 | 363 |
| Community & Sport | 538 | 65 |
| Government & Defence | 194 | 8 |
| Advert / Media / Entertainment | 117 | 13 |
| Total across classifications | 42,710 | 5,503 |

## JOBG8 XML RECONCILIATION

| Check | XML feed total | Sum of ‘Jobs received’ | Difference (sum − XML) | Result |
|---|---:|---:|---:|---|
| JobG8 feed categories | 42,710 | 42,710 | 0 | **PASS** |

**JobG8 feed reconciliation: PASS.** Difference is 0 jobs (summed categories minus XML total).

## JOBG8 LAST 10 FEED DATES — TOTALS ONLY

Saved history contains 10 of the latest 10 feed dates. Older feed totals were not saved and are not backfilled.

| Feed date | JobG8 jobs received | Ontap jobs classified/published |
|---|---:|---:|
| 2026-11-25 | 42,710 | 5,503 |
| 2026-11-24 | 44,363 | 5,579 |
| 2026-11-23 | 44,175 | 5,655 |
| 2026-11-22 | 43,884 | 5,626 |
| 2026-11-21 | 44,000 | 5,630 |
| 2026-11-20 | 43,256 | 5,506 |
| 2026-11-19 | 43,590 | 5,586 |
| 2026-11-18 | 40,302 | 5,431 |
| 2026-11-17 | 40,395 | 5,372 |
| 2026-11-16 | 39,741 | 5,246 |

## JOBG8 LAST 10 FEED DATES — SELECTED JOBS BY CLASSIFICATION

Each dated column shows Ontap jobs classified/published in that JobG8 classification.

| JobG8 classification | 2026-11-25 | 2026-11-24 | 2026-11-23 | 2026-11-22 | 2026-11-21 | 2026-11-20 | 2026-11-19 | 2026-11-18 | 2026-11-17 | 2026-11-16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Accounting | 1733 | 1718 | 1764 | 1767 | 1764 | 1738 | 1743 | 1732 | 1703 | 1667 |
| Administration | 1022 | 1031 | 1046 | 1047 | 1041 | 1042 | 1047 | 995 | 995 | 985 |
| Advert / Media / Entertainment | 13 | 14 | 16 | 16 | 16 | 16 | 17 | 19 | 19 | 19 |
| Banking & Financial Services | 62 | 61 | 59 | 58 | 58 | 57 | 62 | 13 | 13 | 13 |
| Call Centre / CustomerService | 363 | 404 | 409 | 402 | 397 | 368 | 374 | 367 | 345 | 357 |
| Community & Sport | 65 | 67 | 64 | 66 | 69 | 67 | 70 | 64 | 62 | 61 |
| Education | 57 | 49 | 48 | 47 | 48 | 48 | 50 | 50 | 50 | 50 |
| Government & Defence | 8 | 8 | 7 | 7 | 7 | 8 | 9 | 9 | 7 | 6 |
| Healthcare & Medical | 394 | 414 | 405 | 401 | 409 | 403 | 398 | 341 | 343 | 286 |
| HR / Recruitment | 153 | 151 | 148 | 148 | 146 | 141 | 143 | 138 | 135 | 139 |
| I.T. & Communications | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Insurance & Superannuation | 25 | 24 | 24 | 24 | 24 | 25 | 24 | 26 | 25 | 24 |
| Legal | 483 | 470 | 467 | 451 | 451 | 410 | 424 | 455 | 451 | 443 |
| Real Estate & Property | 67 | 69 | 72 | 71 | 72 | 73 | 77 | 78 | 77 | 75 |
| Sales & Marketing | 896 | 922 | 953 | 946 | 948 | 929 | 961 | 955 | 962 | 957 |
| Transport & Logistics | 161 | 176 | 172 | 174 | 179 | 180 | 186 | 188 | 184 | 163 |

## PAGES

**Published/indexable URLs: 6,101** — 5,719 individual job pages, 260 regional/category pages, 114 city pages and 8 core pages.

| Level | Page type | Area | Family | URL | Page count | Live jobs | In sitemap |
|---|---|---|---|---|---:|---:|---|
| Summary | All published/indexable URLs | Sitewide |  |  | 6,101 |  | Yes |
| Summary | Individual job | Sitewide |  | /jobs/[id] | 5,719 | 5,719 | Yes |
| Summary | Regional/category | Sitewide |  | Multiple | 260 |  | Yes |
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
| Detail | Regional/category | West Yorkshire | Support Worker | /west-yorkshire/support-worker | 1 | 8 | Yes |
| Detail | Regional/category | South Yorkshire | Support Worker | /south-yorkshire/support-worker | 1 | 8 | Yes |
| Detail | Regional/category | North East | Support Worker | /north-east/support-worker | 1 | 28 | Yes |
| Detail | Regional/category | Sussex | Support Worker | /sussex/support-worker | 1 | 48 | Yes |
| Detail | Regional/category | Cumbria South | Support Worker | /cumbria-south/support-worker | 1 | 1 | Yes |
| Detail | Regional/category | Hampshire | Support Worker | /hampshire/support-worker | 1 | 30 | Yes |
| Detail | Regional/category | West Yorkshire | Service Administrator Jobs | /west-yorkshire/service-administrator-jobs | 1 | 156 | Yes |
| Detail | Regional/category | South Yorkshire | Service Administrator Jobs | /south-yorkshire/service-administrator-jobs | 1 | 58 | Yes |
| Detail | Regional/category | North Yorkshire | Service Administrator Jobs | /north-yorkshire/service-administrator-jobs | 1 | 49 | Yes |
| Detail | Regional/category | North East | Service Administrator Jobs | /north-east/service-administrator-jobs | 1 | 109 | Yes |
| Detail | Regional/category | London | Service Administrator Jobs | /london/service-administrator-jobs | 1 | 459 | Yes |
| Detail | Regional/category | London | Central Service Administrator Jobs | /london/central-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | North Service Administrator Jobs | /london/north-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | East Service Administrator Jobs | /london/east-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | South Service Administrator Jobs | /london/south-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | London | West Service Administrator Jobs | /london/west-service-administrator-jobs | 1 |  | Yes |
| Detail | Regional/category | Hampshire | Service Administrator Jobs | /hampshire/service-administrator-jobs | 1 | 161 | Yes |
| Detail | Regional/category | Coventry Warwickshire | Service Administrator Jobs | /coventry-warwickshire/service-administrator-jobs | 1 | 96 | Yes |
| Detail | Regional/category | Surrey | Service Administrator Jobs | /surrey/service-administrator-jobs | 1 | 155 | Yes |
| Detail | Regional/category | Kent | Service Administrator Jobs | /kent/service-administrator-jobs | 1 | 115 | Yes |
| Detail | Regional/category | Sussex | Service Administrator Jobs | /sussex/service-administrator-jobs | 1 | 122 | Yes |
| Detail | City | Newcastle | admin and office jobs | /newcastle/service-administrator-jobs | 1 | 48 | Yes |
| Detail | City | Southampton | support worker jobs | /southampton/support-worker | 1 | 9 | Yes |
| Detail | City | Sheffield | admin and office jobs | /sheffield/service-administrator-jobs | 1 | 42 | Yes |
| Detail | City | Leeds | admin and office jobs | /leeds/service-administrator-jobs | 1 | 98 | Yes |
| Detail | City | Coventry | admin and office jobs | /coventry/service-administrator-jobs | 1 | 23 | Yes |
| Detail | City | Southampton | admin and office jobs | /southampton/service-administrator-jobs | 1 | 14 | Yes |
| Detail | City | Brighton & Hove | admin and office jobs | /brighton-hove/service-administrator-jobs | 1 | 14 | Yes |
| Detail | City | Bradford | admin and office jobs | /bradford/service-administrator-jobs | 1 | 26 | Yes |
| Detail | City | Huddersfield | admin and office jobs | /huddersfield/service-administrator-jobs | 1 | 17 | Yes |
| Detail | City | York | admin and office jobs | /york/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Barnsley | admin and office jobs | /barnsley/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Doncaster | admin and office jobs | /doncaster/service-administrator-jobs | 1 | 20 | Yes |
| Detail | City | Bristol | admin and office jobs | /bristol/service-administrator-jobs | 1 | 68 | Yes |
| Detail | City | Manchester | admin and office jobs | /manchester/service-administrator-jobs | 1 | 152 | Yes |
| Detail | City | Cambridge | admin and office jobs | /cambridge/service-administrator-jobs | 1 | 37 | Yes |
| Detail | City | Birmingham | admin and office jobs | /birmingham/service-administrator-jobs | 1 | 131 | Yes |
| Detail | City | Peterborough | admin and office jobs | /peterborough/service-administrator-jobs | 1 | 22 | Yes |
| Detail | City | Warrington | admin and office jobs | /warrington/service-administrator-jobs | 1 | 29 | Yes |
| Detail | City | Liverpool | admin and office jobs | /liverpool/service-administrator-jobs | 1 | 43 | Yes |
| Detail | City | Hull | admin and office jobs | /hull/service-administrator-jobs | 1 | 3 | Yes |
| Detail | City | Oxford | admin and office jobs | /oxford/service-administrator-jobs | 1 | 14 | Yes |
| Detail | City | Belfast | admin and office jobs | /belfast/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Glasgow | admin and office jobs | /glasgow/service-administrator-jobs | 1 | 42 | Yes |
| Detail | City | Edinburgh | admin and office jobs | /edinburgh/service-administrator-jobs | 1 | 34 | Yes |
| Detail | City | Cardiff | admin and office jobs | /cardiff/service-administrator-jobs | 1 | 23 | Yes |
| Detail | City | Exeter | admin and office jobs | /exeter/service-administrator-jobs | 1 | 22 | Yes |
| Detail | City | Milton Keynes | admin and office jobs | /milton-keynes/service-administrator-jobs | 1 | 28 | Yes |
| Detail | City | Farnham | admin and office jobs | /farnham/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Northampton | admin and office jobs | /northampton/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Poole | admin and office jobs | /poole/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Portsmouth | admin and office jobs | /portsmouth/service-administrator-jobs | 1 | 19 | Yes |
| Detail | City | Stoke-on-trent | admin and office jobs | /stoke-on-trent/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Hemel Hempstead | admin and office jobs | /hemel-hempstead/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Basingstoke | admin and office jobs | /basingstoke/service-administrator-jobs | 1 | 7 | Yes |
| Detail | City | Chelmsford | admin and office jobs | /chelmsford/service-administrator-jobs | 1 | 13 | Yes |
| Detail | City | Gloucester | admin and office jobs | /gloucester/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Leicester | admin and office jobs | /leicester/service-administrator-jobs | 1 | 21 | Yes |
| Detail | City | Maidstone | admin and office jobs | /maidstone/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Newtownabbey | admin and office jobs | /newtownabbey/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Plymouth | admin and office jobs | /plymouth/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Sunderland | admin and office jobs | /sunderland/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Worcester | admin and office jobs | /worcester/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Altrincham | admin and office jobs | /altrincham/service-administrator-jobs | 1 | 5 | Yes |
| Detail | City | Ashford | admin and office jobs | /ashford/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Aylesbury | admin and office jobs | /aylesbury/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Bedford | admin and office jobs | /bedford/service-administrator-jobs | 1 | 16 | Yes |
| Detail | City | Bournemouth | admin and office jobs | /bournemouth/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Chester Le Street | admin and office jobs | /chester-le-street/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Macclesfield | admin and office jobs | /macclesfield/service-administrator-jobs | 1 | 15 | Yes |
| Detail | City | Rotherham | admin and office jobs | /rotherham/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Scarborough | admin and office jobs | /scarborough/service-administrator-jobs | 1 | 3 | Yes |
| Detail | City | Shrewsbury | admin and office jobs | /shrewsbury/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Warwick | admin and office jobs | /warwick/service-administrator-jobs | 1 | 18 | Yes |
| Detail | City | Wigston | admin and office jobs | /wigston/service-administrator-jobs | 1 | 0 | Yes |
| Detail | City | Dartford | admin and office jobs | /dartford/service-administrator-jobs | 1 | 11 | Yes |
| Detail | City | Stockport | admin and office jobs | /stockport/service-administrator-jobs | 1 | 17 | Yes |
| Detail | City | Swansea | admin and office jobs | /swansea/service-administrator-jobs | 1 | 9 | Yes |
| Detail | City | Walsall | admin and office jobs | /walsall/service-administrator-jobs | 1 | 13 | Yes |
| Detail | City | Bath | admin and office jobs | /bath/service-administrator-jobs | 1 | 8 | Yes |
| Detail | City | Eastleigh | admin and office jobs | /eastleigh/service-administrator-jobs | 1 | 4 | Yes |
| Detail | City | Harrogate | admin and office jobs | /harrogate/service-administrator-jobs | 1 | 14 | Yes |
| Detail | City | Watford | admin and office jobs | /watford/service-administrator-jobs | 1 | 11 | Yes |
| Detail | City | Crawley | admin and office jobs | /crawley/service-administrator-jobs | 1 | 12 | Yes |
| Detail | City | Swindon | admin and office jobs | /swindon/service-administrator-jobs | 1 | 14 | Yes |
| Detail | City | Horsham | admin and office jobs | /horsham/service-administrator-jobs | 1 | 6 | Yes |
| Detail | City | Lincoln | admin and office jobs | /lincoln/service-administrator-jobs | 1 | 18 | Yes |
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
| Detail | Regional/category | Yorkshire - East | Admin & Customer Service | /job-search/east-yorkshire/service-administrator-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Northern Ireland - East | Admin & Customer Service | /job-search/northern-ireland-east/service-administrator-jobs | 1 | 8 | Yes |
| Detail | Regional/category | London | Customer Service & Contact Centre | /job-search/london/customer-service-jobs | 1 | 10 | Yes |
| Detail | Regional/category | London | HR & Recruitment | /job-search/london/hr-recruitment-jobs | 1 | 32 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Admin & Customer Service | /job-search/manchester-salford/service-administrator-jobs | 1 | 127 | Yes |
| Detail | Regional/category | London | Finance & Accounts | /job-search/london/finance-accounts-jobs | 1 | 203 | Yes |
| Detail | Regional/category | Oxfordshire | Admin & Customer Service | /job-search/oxfordshire/service-administrator-jobs | 1 | 67 | Yes |
| Detail | Regional/category | Bristol & Bath | Admin & Customer Service | /job-search/bristol-bath/service-administrator-jobs | 1 | 65 | Yes |
| Detail | Regional/category | Essex | Admin & Customer Service | /job-search/essex/service-administrator-jobs | 1 | 116 | Yes |
| Detail | Regional/category | Hampshire | Customer Service & Contact Centre | /job-search/hampshire/customer-service-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Cambridgeshire | Admin & Customer Service | /job-search/cambridgeshire/service-administrator-jobs | 1 | 49 | Yes |
| Detail | Regional/category | Gloucestershire | Admin & Customer Service | /job-search/gloucestershire/service-administrator-jobs | 1 | 83 | Yes |
| Detail | Regional/category | London | Support Worker | /job-search/london/support-worker | 1 | 92 | Yes |
| Detail | Regional/category | Devon | Finance & Accounts | /job-search/devon/finance-accounts-jobs | 1 | 23 | Yes |
| Detail | Regional/category | Dorset | Admin & Customer Service | /job-search/dorset/service-administrator-jobs | 1 | 53 | Yes |
| Detail | Regional/category | Staffordshire | Customer Service & Contact Centre | /job-search/staffordshire/customer-service-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Devon | Admin & Customer Service | /job-search/devon/service-administrator-jobs | 1 | 59 | Yes |
| Detail | Regional/category | Surrey | Customer Service & Contact Centre | /job-search/surrey/customer-service-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Wiltshire | Admin & Customer Service | /job-search/wiltshire/service-administrator-jobs | 1 | 40 | Yes |
| Detail | Regional/category | Northamptonshire | Admin & Customer Service | /job-search/northamptonshire/service-administrator-jobs | 1 | 61 | Yes |
| Detail | Regional/category | Berkshire | Admin & Customer Service | /job-search/berkshire/service-administrator-jobs | 1 | 80 | Yes |
| Detail | Regional/category | Nottinghamshire | Admin & Customer Service | /job-search/nottinghamshire/service-administrator-jobs | 1 | 67 | Yes |
| Detail | Regional/category | Buckinghamshire | Admin & Customer Service | /job-search/buckinghamshire/service-administrator-jobs | 1 | 74 | Yes |
| Detail | Regional/category | Surrey | Support Worker | /job-search/surrey/support-worker | 1 | 11 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Customer Service & Contact Centre | /job-search/manchester-salford/customer-service-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Hampshire | HR & Recruitment | /job-search/hampshire/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Hertfordshire | Admin & Customer Service | /job-search/hertfordshire/service-administrator-jobs | 1 | 94 | Yes |
| Detail | Regional/category | Staffordshire | Admin & Customer Service | /job-search/staffordshire/service-administrator-jobs | 1 | 70 | Yes |
| Detail | Regional/category | Norfolk | Admin & Customer Service | /job-search/norfolk/service-administrator-jobs | 1 | 40 | Yes |
| Detail | Regional/category | Sussex | Finance & Accounts | /job-search/sussex/finance-accounts-jobs | 1 | 37 | Yes |
| Detail | Regional/category | Yorkshire - West | Finance & Accounts | /job-search/west-yorkshire/finance-accounts-jobs | 1 | 87 | Yes |
| Detail | Regional/category | Gloucestershire | Finance & Accounts | /job-search/gloucestershire/finance-accounts-jobs | 1 | 29 | Yes |
| Detail | Regional/category | Bristol & Bath | Finance & Accounts | /job-search/bristol-bath/finance-accounts-jobs | 1 | 28 | Yes |
| Detail | Regional/category | Sussex | Customer Service & Contact Centre | /job-search/sussex/customer-service-jobs | 1 | 3 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Admin & Customer Service | /job-search/birmingham-solihull/service-administrator-jobs | 1 | 111 | Yes |
| Detail | Regional/category | Yorkshire - West | HR & Recruitment | /job-search/west-yorkshire/hr-recruitment-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Greater Manchester - South | Admin & Customer Service | /job-search/greater-manchester-south/service-administrator-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Hampshire | Finance & Accounts | /job-search/hampshire/finance-accounts-jobs | 1 | 67 | Yes |
| Detail | Regional/category | North East | Finance & Accounts | /job-search/north-east/finance-accounts-jobs | 1 | 35 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Finance & Accounts | /job-search/birmingham-solihull/finance-accounts-jobs | 1 | 44 | Yes |
| Detail | Regional/category | Wiltshire | Support Worker | /job-search/wiltshire/support-worker | 1 | 18 | Yes |
| Detail | Regional/category | Somerset | Admin & Customer Service | /job-search/somerset/service-administrator-jobs | 1 | 47 | Yes |
| Detail | Regional/category | London | Customer Sales & Sales Advisor | /job-search/london/customer-sales-jobs | 1 | 82 | Yes |
| Detail | Regional/category | Yorkshire - West | Customer Sales & Sales Advisor | /job-search/west-yorkshire/customer-sales-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Customer Sales & Sales Advisor | /job-search/manchester-salford/customer-sales-jobs | 1 | 18 | Yes |
| Detail | Regional/category | Leicestershire | Admin & Customer Service | /job-search/leicestershire/service-administrator-jobs | 1 | 81 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Admin & Customer Service | /job-search/warrington-halton/service-administrator-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Cornwall | Admin & Customer Service | /job-search/cornwall/service-administrator-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Suffolk | Admin & Customer Service | /job-search/suffolk/service-administrator-jobs | 1 | 58 | Yes |
| Detail | Regional/category | Derbyshire | Admin & Customer Service | /job-search/derbyshire/service-administrator-jobs | 1 | 57 | Yes |
| Detail | Regional/category | Cheshire - East | Admin & Customer Service | /job-search/cheshire-east/service-administrator-jobs | 1 | 28 | Yes |
| Detail | Regional/category | Lincolnshire | Admin & Customer Service | /job-search/lincolnshire/service-administrator-jobs | 1 | 28 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Admin & Customer Service | /job-search/merseyside-liverpool/service-administrator-jobs | 1 | 38 | Yes |
| Detail | Regional/category | Shropshire | Admin & Customer Service | /job-search/shropshire/service-administrator-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Greater Manchester - Wigan & Bolton | Admin & Customer Service | /job-search/wigan-bolton/service-administrator-jobs | 1 | 27 | Yes |
| Detail | Regional/category | West Midlands - Black Country | Admin & Customer Service | /job-search/black-country/service-administrator-jobs | 1 | 64 | Yes |
| Detail | Regional/category | London | Legal Assistant & Paralegal | /job-search/london/paralegal-jobs | 1 | 117 | Yes |
| Detail | Regional/category | Suffolk | Legal Assistant & Paralegal | /job-search/suffolk/paralegal-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Essex | Legal Assistant & Paralegal | /job-search/essex/paralegal-jobs | 1 | 32 | Yes |
| Detail | Regional/category | Norfolk | Legal Assistant & Paralegal | /job-search/norfolk/paralegal-jobs | 1 | 18 | Yes |
| Detail | Regional/category | London | Marketing | /job-search/london/marketing-jobs | 1 | 159 | Yes |
| Detail | Regional/category | Surrey | Marketing | /job-search/surrey/marketing-jobs | 1 | 28 | Yes |
| Detail | Regional/category | Greater Manchester - North | Finance & Accounts | /job-search/greater-manchester-north/finance-accounts-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Scotland Central - Fife | Admin & Customer Service | /job-search/fife/service-administrator-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Bristol & Bath | Legal Assistant & Paralegal | /job-search/bristol-bath/paralegal-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Staffordshire | Marketing | /job-search/staffordshire/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Marketing | /job-search/manchester-salford/marketing-jobs | 1 | 33 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Marketing | /job-search/birmingham-solihull/marketing-jobs | 1 | 26 | Yes |
| Detail | Regional/category | Berkshire | HR & Recruitment | /job-search/berkshire/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | HR & Recruitment | /job-search/manchester-salford/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Nottinghamshire | HR & Recruitment | /job-search/nottinghamshire/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | HR & Recruitment | /job-search/birmingham-solihull/hr-recruitment-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Sussex | HR & Recruitment | /job-search/sussex/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Essex | HR & Recruitment | /job-search/essex/hr-recruitment-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Cheshire - West | Admin & Customer Service | /job-search/cheshire-west/service-administrator-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Scotland Central - Edinburgh & Lothians | Admin & Customer Service | /job-search/edinburgh-lothians/service-administrator-jobs | 1 | 39 | Yes |
| Detail | Regional/category | Worcestershire | Admin & Customer Service | /job-search/worcestershire/service-administrator-jobs | 1 | 42 | Yes |
| Detail | Regional/category | Berkshire | Marketing | /job-search/berkshire/marketing-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Kent | Support Worker | /job-search/kent/support-worker | 1 | 26 | Yes |
| Detail | Regional/category | North East | Customer Sales & Sales Advisor | /job-search/north-east/customer-sales-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Oxfordshire | Support Worker | /job-search/oxfordshire/support-worker | 1 | 7 | Yes |
| Detail | Regional/category | Yorkshire - North | Finance & Accounts | /job-search/north-yorkshire/finance-accounts-jobs | 1 | 23 | Yes |
| Detail | Regional/category | Shropshire | Finance & Accounts | /job-search/shropshire/finance-accounts-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Bedfordshire | Admin & Customer Service | /job-search/bedfordshire/service-administrator-jobs | 1 | 37 | Yes |
| Detail | Regional/category | Bristol & Bath | Customer Sales & Sales Advisor | /job-search/bristol-bath/customer-sales-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Buckinghamshire | Marketing | /job-search/buckinghamshire/marketing-jobs | 1 | 22 | Yes |
| Detail | Regional/category | Wales South - Cardiff & Vale | Admin & Customer Service | /job-search/cardiff-vale/service-administrator-jobs | 1 | 23 | Yes |
| Detail | Regional/category | Berkshire | Customer Sales & Sales Advisor | /job-search/berkshire/customer-sales-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Hertfordshire | Customer Sales & Sales Advisor | /job-search/hertfordshire/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Kent | Customer Sales & Sales Advisor | /job-search/kent/customer-sales-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Customer Sales & Sales Advisor | /job-search/glasgow/customer-sales-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Surrey | Customer Sales & Sales Advisor | /job-search/surrey/customer-sales-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Sussex | Customer Sales & Sales Advisor | /job-search/sussex/customer-sales-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Bristol & Bath | Marketing | /job-search/bristol-bath/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Gloucestershire | Marketing | /job-search/gloucestershire/marketing-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Hertfordshire | Marketing | /job-search/hertfordshire/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Kent | Marketing | /job-search/kent/marketing-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Oxfordshire | Marketing | /job-search/oxfordshire/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | North Scotland | Admin & Customer Service | /job-search/north-scotland/service-administrator-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Scotland Central - Tayside | Admin & Customer Service | /job-search/tayside/service-administrator-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Wales South - Valleys | Admin & Customer Service | /job-search/south-wales-valleys/service-administrator-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Cambridgeshire | Marketing | /job-search/cambridgeshire/marketing-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Cheshire - West | Marketing | /job-search/cheshire-west/marketing-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Essex | Marketing | /job-search/essex/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Marketing | /job-search/merseyside-liverpool/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | North East | Marketing | /job-search/north-east/marketing-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Finance & Accounts | /job-search/warrington-halton/finance-accounts-jobs | 1 | 20 | Yes |
| Detail | Regional/category | Buckinghamshire | Customer Service & Contact Centre | /job-search/buckinghamshire/customer-service-jobs | 1 | 3 | Yes |
| Detail | Regional/category | North East | Customer Service & Contact Centre | /job-search/north-east/customer-service-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Devon | Customer Sales & Sales Advisor | /job-search/devon/customer-sales-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Hampshire | Customer Sales & Sales Advisor | /job-search/hampshire/customer-sales-jobs | 1 | 24 | Yes |
| Detail | Regional/category | North Scotland | Customer Sales & Sales Advisor | /job-search/north-scotland/customer-sales-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Northern Ireland - East | Marketing | /job-search/northern-ireland-east/marketing-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Yorkshire - North | Marketing | /job-search/north-yorkshire/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Essex | Finance & Accounts | /job-search/essex/finance-accounts-jobs | 1 | 42 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Finance & Accounts | /job-search/manchester-salford/finance-accounts-jobs | 1 | 63 | Yes |
| Detail | Regional/category | Berkshire | Finance & Accounts | /job-search/berkshire/finance-accounts-jobs | 1 | 37 | Yes |
| Detail | Regional/category | Buckinghamshire | Finance & Accounts | /job-search/buckinghamshire/finance-accounts-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Cambridgeshire | Finance & Accounts | /job-search/cambridgeshire/finance-accounts-jobs | 1 | 31 | Yes |
| Detail | Regional/category | Cheshire - East | Finance & Accounts | /job-search/cheshire-east/finance-accounts-jobs | 1 | 22 | Yes |
| Detail | Regional/category | Cheshire - West | Finance & Accounts | /job-search/cheshire-west/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Dorset | Finance & Accounts | /job-search/dorset/finance-accounts-jobs | 1 | 27 | Yes |
| Detail | Regional/category | Hertfordshire | Finance & Accounts | /job-search/hertfordshire/finance-accounts-jobs | 1 | 33 | Yes |
| Detail | Regional/category | Kent | Finance & Accounts | /job-search/kent/finance-accounts-jobs | 1 | 52 | Yes |
| Detail | Regional/category | Lancashire - East | Finance & Accounts | /job-search/lancashire-east/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Leicestershire | Finance & Accounts | /job-search/leicestershire/finance-accounts-jobs | 1 | 25 | Yes |
| Detail | Regional/category | Norfolk | Finance & Accounts | /job-search/norfolk/finance-accounts-jobs | 1 | 18 | Yes |
| Detail | Regional/category | Northamptonshire | Finance & Accounts | /job-search/northamptonshire/finance-accounts-jobs | 1 | 32 | Yes |
| Detail | Regional/category | Nottinghamshire | Finance & Accounts | /job-search/nottinghamshire/finance-accounts-jobs | 1 | 36 | Yes |
| Detail | Regional/category | Oxfordshire | Finance & Accounts | /job-search/oxfordshire/finance-accounts-jobs | 1 | 29 | Yes |
| Detail | Regional/category | Suffolk | Finance & Accounts | /job-search/suffolk/finance-accounts-jobs | 1 | 22 | Yes |
| Detail | Regional/category | Surrey | Finance & Accounts | /job-search/surrey/finance-accounts-jobs | 1 | 62 | Yes |
| Detail | Regional/category | Wales South - Cardiff & Vale | Finance & Accounts | /job-search/cardiff-vale/finance-accounts-jobs | 1 | 10 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Finance & Accounts | /job-search/coventry-warwickshire/finance-accounts-jobs | 1 | 61 | Yes |
| Detail | Regional/category | Wiltshire | Finance & Accounts | /job-search/wiltshire/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Yorkshire - South | Finance & Accounts | /job-search/south-yorkshire/finance-accounts-jobs | 1 | 30 | Yes |
| Detail | Regional/category | Norfolk | Marketing | /job-search/norfolk/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Yorkshire - West | Marketing | /job-search/west-yorkshire/marketing-jobs | 1 | 19 | Yes |
| Detail | Regional/category | West Midlands - Birmingham & Solihull | Legal Assistant & Paralegal | /job-search/birmingham-solihull/paralegal-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Yorkshire - North | Legal Assistant & Paralegal | /job-search/north-yorkshire/paralegal-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Yorkshire - West | Legal Assistant & Paralegal | /job-search/west-yorkshire/paralegal-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Berkshire | Legal Assistant & Paralegal | /job-search/berkshire/paralegal-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Legal Assistant & Paralegal | /job-search/manchester-salford/paralegal-jobs | 1 | 31 | Yes |
| Detail | Regional/category | Kent | Legal Assistant & Paralegal | /job-search/kent/paralegal-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Legal Assistant & Paralegal | /job-search/merseyside-liverpool/paralegal-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Surrey | Legal Assistant & Paralegal | /job-search/surrey/paralegal-jobs | 1 | 17 | Yes |
| Detail | Regional/category | Buckinghamshire | Legal Assistant & Paralegal | /job-search/buckinghamshire/paralegal-jobs | 1 | 19 | Yes |
| Detail | Regional/category | Cheshire - Warrington & Halton | Marketing | /job-search/warrington-halton/marketing-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Essex | Customer Sales & Sales Advisor | /job-search/essex/customer-sales-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Gloucestershire | HR & Recruitment | /job-search/gloucestershire/hr-recruitment-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Greater Manchester - North | Admin & Customer Service | /job-search/greater-manchester-north/service-administrator-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Hampshire | Legal Assistant & Paralegal | /job-search/hampshire/paralegal-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Herefordshire | Admin & Customer Service | /job-search/herefordshire/service-administrator-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Lancashire - East | Admin & Customer Service | /job-search/lancashire-east/service-administrator-jobs | 1 | 27 | Yes |
| Detail | Regional/category | Merseyside - Liverpool | Finance & Accounts | /job-search/merseyside-liverpool/finance-accounts-jobs | 1 | 21 | Yes |
| Detail | Regional/category | Nottinghamshire | Marketing | /job-search/nottinghamshire/marketing-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Oxfordshire | Legal Assistant & Paralegal | /job-search/oxfordshire/paralegal-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Somerset | Finance & Accounts | /job-search/somerset/finance-accounts-jobs | 1 | 15 | Yes |
| Detail | Regional/category | Staffordshire | Finance & Accounts | /job-search/staffordshire/finance-accounts-jobs | 1 | 16 | Yes |
| Detail | Regional/category | Sussex | Marketing | /job-search/sussex/marketing-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Wales South - Swansea Bay | Admin & Customer Service | /job-search/swansea-bay/service-administrator-jobs | 1 | 14 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Marketing | /job-search/coventry-warwickshire/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Worcestershire | Finance & Accounts | /job-search/worcestershire/finance-accounts-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Yorkshire - East | Finance & Accounts | /job-search/east-yorkshire/finance-accounts-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Cumbria - North | Admin & Customer Service | /job-search/cumbria-north/service-administrator-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Dorset | Customer Sales & Sales Advisor | /job-search/dorset/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Hertfordshire | Legal Assistant & Paralegal | /job-search/hertfordshire/paralegal-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Lancashire - Central | Admin & Customer Service | /job-search/lancashire-central/service-administrator-jobs | 1 | 20 | Yes |
| Detail | Regional/category | North Wales - East | Admin & Customer Service | /job-search/north-wales-east/service-administrator-jobs | 1 | 18 | Yes |
| Detail | Regional/category | Northamptonshire | Customer Sales & Sales Advisor | /job-search/northamptonshire/customer-sales-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Nottinghamshire | Legal Assistant & Paralegal | /job-search/nottinghamshire/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Oxfordshire | Customer Sales & Sales Advisor | /job-search/oxfordshire/customer-sales-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Scotland Central - Falkirk & Stirling | Admin & Customer Service | /job-search/falkirk-stirling/service-administrator-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Suffolk | Customer Sales & Sales Advisor | /job-search/suffolk/customer-sales-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Wales South - Gwent | Admin & Customer Service | /job-search/gwent/service-administrator-jobs | 1 | 14 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Legal Assistant & Paralegal | /job-search/coventry-warwickshire/paralegal-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Yorkshire - West | Customer Service & Contact Centre | /job-search/west-yorkshire/customer-service-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Cambridgeshire | Customer Sales & Sales Advisor | /job-search/cambridgeshire/customer-sales-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Nottinghamshire | Customer Sales & Sales Advisor | /job-search/nottinghamshire/customer-sales-jobs | 1 | 13 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Customer Sales & Sales Advisor | /job-search/coventry-warwickshire/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Worcestershire | Customer Sales & Sales Advisor | /job-search/worcestershire/customer-sales-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Northamptonshire | Marketing | /job-search/northamptonshire/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Marketing | /job-search/glasgow/marketing-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Cornwall | Finance & Accounts | /job-search/cornwall/finance-accounts-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Derbyshire | Finance & Accounts | /job-search/derbyshire/finance-accounts-jobs | 1 | 20 | Yes |
| Detail | Regional/category | North East | HR & Recruitment | /job-search/north-east/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Staffordshire | HR & Recruitment | /job-search/staffordshire/hr-recruitment-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Surrey | HR & Recruitment | /job-search/surrey/hr-recruitment-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Hertfordshire | Customer Service & Contact Centre | /job-search/hertfordshire/customer-service-jobs | 1 | 2 | Yes |
| Detail | Regional/category | Kent | Customer Service & Contact Centre | /job-search/kent/customer-service-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Merseyside - St Helens & Knowsley | Admin & Customer Service | /job-search/st-helens-knowsley/service-administrator-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Cheshire - East | Customer Sales & Sales Advisor | /job-search/cheshire-east/customer-sales-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Gloucestershire | Customer Sales & Sales Advisor | /job-search/gloucestershire/customer-sales-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Leicestershire | Customer Sales & Sales Advisor | /job-search/leicestershire/customer-sales-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Norfolk | Customer Sales & Sales Advisor | /job-search/norfolk/customer-sales-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Legal Assistant & Paralegal | /job-search/glasgow/paralegal-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Yorkshire - South | Marketing | /job-search/south-yorkshire/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | West Midlands - Black Country | Finance & Accounts | /job-search/black-country/finance-accounts-jobs | 1 | 28 | Yes |
| Detail | Regional/category | Leicestershire | HR & Recruitment | /job-search/leicestershire/hr-recruitment-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Suffolk | HR & Recruitment | /job-search/suffolk/hr-recruitment-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Merseyside - Wirral | Admin & Customer Service | /job-search/merseyside-wirral/service-administrator-jobs | 1 | 12 | Yes |
| Detail | Regional/category | Scotland West - Lanarkshire | Admin & Customer Service | /job-search/lanarkshire/service-administrator-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Berkshire | Support Worker | /job-search/berkshire/support-worker | 1 | 10 | Yes |
| Detail | Regional/category | Dorset | Support Worker | /job-search/dorset/support-worker | 1 | 26 | Yes |
| Detail | Regional/category | Essex | Support Worker | /job-search/essex/support-worker | 1 | 28 | Yes |
| Detail | Regional/category | Greater Manchester - Manchester & Salford | Support Worker | /job-search/manchester-salford/support-worker | 1 | 10 | Yes |
| Detail | Regional/category | Nottinghamshire | Support Worker | /job-search/nottinghamshire/support-worker | 1 | 15 | Yes |
| Detail | Regional/category | Derbyshire | Customer Sales & Sales Advisor | /job-search/derbyshire/customer-sales-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Lincolnshire | Legal Assistant & Paralegal | /job-search/lincolnshire/paralegal-jobs | 1 | 4 | Yes |
| Detail | Regional/category | Sussex | Legal Assistant & Paralegal | /job-search/sussex/paralegal-jobs | 1 | 22 | Yes |
| Detail | Regional/category | Yorkshire - South | Legal Assistant & Paralegal | /job-search/south-yorkshire/paralegal-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Dorset | Marketing | /job-search/dorset/marketing-jobs | 1 | 1 | Yes |
| Detail | Regional/category | Leicestershire | Marketing | /job-search/leicestershire/marketing-jobs | 1 | 8 | Yes |
| Detail | Regional/category | Bedfordshire | Finance & Accounts | /job-search/bedfordshire/finance-accounts-jobs | 1 | 14 | Yes |
| Detail | Regional/category | Buckinghamshire | HR & Recruitment | /job-search/buckinghamshire/hr-recruitment-jobs | 1 | 2 | Yes |
| Detail | Regional/category | West Midlands - Black Country | HR & Recruitment | /job-search/black-country/hr-recruitment-jobs | 1 | 3 | Yes |
| Detail | Regional/category | Lancashire - Blackpool & Fylde | Admin & Customer Service | /job-search/blackpool-fylde/service-administrator-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Bedfordshire | Customer Sales & Sales Advisor | /job-search/bedfordshire/customer-sales-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Cambridgeshire | Legal Assistant & Paralegal | /job-search/cambridgeshire/paralegal-jobs | 1 | 4 | Yes |
| Detail | Regional/category | North East | Legal Assistant & Paralegal | /job-search/north-east/paralegal-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Scotland Central - Edinburgh & Lothians | Legal Assistant & Paralegal | /job-search/edinburgh-lothians/paralegal-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Hampshire | Marketing | /job-search/hampshire/marketing-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Shropshire | Marketing | /job-search/shropshire/marketing-jobs | 1 | 10 | Yes |
| Detail | Regional/category | Greater Manchester - South | Finance & Accounts | /job-search/greater-manchester-south/finance-accounts-jobs | 1 | 9 | Yes |
| Detail | Regional/category | Lancashire - Central | Finance & Accounts | /job-search/lancashire-central/finance-accounts-jobs | 1 | 11 | Yes |
| Detail | Regional/category | Merseyside - Wirral | Finance & Accounts | /job-search/merseyside-wirral/finance-accounts-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Scotland Central - Edinburgh & Lothians | Finance & Accounts | /job-search/edinburgh-lothians/finance-accounts-jobs | 1 | 13 | Yes |
| Detail | Regional/category | Somerset | Customer Sales & Sales Advisor | /job-search/somerset/customer-sales-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Bedfordshire | Legal Assistant & Paralegal | /job-search/bedfordshire/paralegal-jobs | 1 | 6 | Yes |
| Detail | Regional/category | Devon | Legal Assistant & Paralegal | /job-search/devon/paralegal-jobs | 1 | 5 | Yes |
| Detail | Regional/category | Greater Manchester - Wigan & Bolton | Finance & Accounts | /job-search/wigan-bolton/finance-accounts-jobs | 1 | 7 | Yes |
| Detail | Regional/category | Scotland West - Glasgow | Finance & Accounts | /job-search/glasgow/finance-accounts-jobs | 1 | 14 | Yes |
| Detail | Regional/category | West Midlands - Coventry & Warwickshire | Customer Service & Contact Centre | /job-search/coventry-warwickshire/customer-service-jobs | 1 | 3 | Yes |

## CITY OPPORTUNITIES

**556 mapped towns/localities with live jobs or an existing city page.** Counts use all 5,719 unique live Ontap jobs across every role and provider: 3,120 have an exact recognised town/locality and 2,599 have only broader or unrecognised location evidence. CREATE means 4+ current Service Admin jobs and no existing city page; London is held separately.

| Status | Town/city/locality | Region | All live jobs | Existing pages | Current routes | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre | Other / unclassified |
|---|---|---|---:|---:|---||---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CREATE | Eastbourne | Sussex | 16 | 0 |  | 7 | 5 | 2 | 1 | 0 | 0 | 1 | 0 | 0 |
| CREATE | Mansfield | Nottinghamshire | 14 | 0 |  | 7 | 1 | 4 | 1 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Loughborough | Leicestershire | 12 | 0 |  | 9 | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 |
| CREATE | Tamworth | Staffordshire | 12 | 0 |  | 9 | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 0 |
| CREATE | Fareham | Hampshire | 11 | 0 |  | 7 | 2 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| CREATE | Oldbury | West Midlands - Black Country | 11 | 0 |  | 10 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| CREATE | Leamington Spa | West Midlands - Coventry & Warwickshire | 10 | 0 |  | 5 | 0 | 1 | 3 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Tunbridge Wells | Kent | 10 | 0 |  | 6 | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Worthing | Sussex | 10 | 0 |  | 4 | 5 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Aberdeen | North Scotland | 9 | 0 |  | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Southend-on-sea | Essex | 9 | 0 |  | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Bury St Edmunds | Suffolk | 8 | 0 |  | 7 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Castleford | Yorkshire - West | 8 | 0 |  | 6 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Halifax | Yorkshire - West | 8 | 0 |  | 7 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Shirley | West Midlands - Birmingham & Solihull | 8 | 0 |  | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | St. Ives | Cambridgeshire | 8 | 0 |  | 5 | 0 | 2 | 0 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Washington | North East - Tyneside, Wearside & Northumberland | 8 | 0 |  | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| CREATE | Bury | Greater Manchester - North | 7 | 0 |  | 6 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Middlewich | Cheshire - East | 7 | 0 |  | 5 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| CREATE | Rochdale | Greater Manchester - North | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Runcorn | Cheshire - Warrington & Halton | 7 | 0 |  | 6 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| CREATE | Staines | Surrey | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Wellington | Shropshire | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Blackpool | Lancashire - Blackpool & Fylde | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Camberley | Surrey | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Daventry | Northamptonshire | 6 | 0 |  | 4 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Leigh | Greater Manchester - Wigan & Bolton | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Reigate | Surrey | 6 | 0 |  | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| CREATE | West Bromwich | West Midlands - Black Country | 6 | 0 |  | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Wigan | Greater Manchester - Wigan & Bolton | 6 | 0 |  | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Winchester | Hampshire | 6 | 0 |  | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Bicester | Oxfordshire | 5 | 0 |  | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Caterham | Surrey | 5 | 0 |  | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Cullompton | Devon | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Epsom | Surrey | 5 | 0 |  | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Havant | Hampshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Maidenhead | Berkshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Richmond | Yorkshire - North | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Rugeley | Staffordshire | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Slough | Berkshire | 5 | 0 |  | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Stirling | Scotland Central - Falkirk & Stirling | 5 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Taunton | Somerset | 5 | 0 |  | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Telford | Shropshire | 5 | 0 |  | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| CREATE | Bridgend | Wales South - Swansea Bay | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Bridgwater | Somerset | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Bromsgrove | Worcestershire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Burnley | Lancashire - East | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Darlington | North East - County Durham & Darlington/Hartlepool | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Gainsborough | Lincolnshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Gosport | Hampshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Grantham | Lincolnshire | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Hessle | Yorkshire - East | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Livingston | Scotland Central - Edinburgh & Lothians | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Penwortham | Lancashire - Central | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Rogerstone | Wales South -gwent | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Sowerby Bridge | Yorkshire - West | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CREATE | Widnes | Cheshire - Warrington & Halton | 4 | 0 |  | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Manchester | Greater Manchester - Manchester & Salford | 167 | 1 | /manchester/service-administrator-jobs | 117 | 9 | 9 | 13 | 8 | 8 | 2 | 1 | 0 |
| LIVE PAGE | Birmingham | West Midlands - Birmingham & Solihull | 131 | 1 | /birmingham/service-administrator-jobs | 91 | 0 | 0 | 7 | 22 | 9 | 2 | 0 | 0 |
| LIVE PAGE | Leeds | Yorkshire - West | 99 | 1 | /leeds/service-administrator-jobs | 76 | 0 | 3 | 5 | 8 | 3 | 2 | 2 | 0 |
| LIVE PAGE | Bristol | Bristol & Bath | 78 | 1 | /bristol/service-administrator-jobs | 56 | 0 | 15 | 4 | 2 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Sheffield | Yorkshire - South | 43 | 1 | /sheffield/service-administrator-jobs | 32 | 1 | 0 | 5 | 3 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Glasgow | Scotland West - Glasgow | 42 | 1 | /glasgow/service-administrator-jobs | 34 | 0 | 3 | 3 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Liverpool | Merseyside - Liverpool | 42 | 1 | /liverpool/service-administrator-jobs | 37 | 0 | 0 | 1 | 3 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Nottingham | Nottinghamshire | 35 | 1 | /nottingham/jobs | 13 | 7 | 7 | 2 | 3 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Edinburgh | Scotland Central - Edinburgh & Lothians | 34 | 1 | /edinburgh/service-administrator-jobs | 32 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Warrington | Cheshire - Warrington & Halton | 29 | 1 | /warrington/service-administrator-jobs | 26 | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Milton Keynes | Buckinghamshire | 28 | 1 | /milton-keynes/service-administrator-jobs | 19 | 0 | 0 | 7 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bradford | Yorkshire - West | 27 | 1 | /bradford/service-administrator-jobs | 20 | 1 | 4 | 0 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Reading | Berkshire | 27 | 1 | /reading/jobs | 16 | 4 | 4 | 0 | 2 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Southampton | Hampshire | 26 | 2 | /southampton/service-administrator-jobs, /southampton/support-worker | 10 | 9 | 5 | 0 | 0 | 1 | 1 | 0 | 0 |
| LIVE PAGE | Cambridge | Cambridgeshire | 25 | 1 | /cambridge/service-administrator-jobs | 22 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Coventry | West Midlands - Coventry & Warwickshire | 24 | 1 | /coventry/service-administrator-jobs | 16 | 0 | 2 | 0 | 0 | 5 | 0 | 1 | 0 |
| LIVE PAGE | Cardiff | Wales South - Cardiff & Vale | 23 | 1 | /cardiff/service-administrator-jobs | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Exeter | Devon | 23 | 1 | /exeter/service-administrator-jobs | 20 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Huddersfield | Yorkshire - West | 23 | 1 | /huddersfield/service-administrator-jobs | 13 | 3 | 5 | 1 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Leicester | Leicestershire | 23 | 1 | /leicester/service-administrator-jobs | 16 | 0 | 4 | 0 | 1 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Norwich | Norfolk | 23 | 1 | /norwich/jobs | 10 | 0 | 7 | 2 | 4 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Peterborough | Cambridgeshire | 23 | 1 | /peterborough/service-administrator-jobs | 17 | 0 | 4 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Newcastle | North East - Tyneside, Wearside & Northumberland | 22 | 1 | /newcastle/service-administrator-jobs | 13 | 3 | 5 | 0 | 0 | 0 | 0 | 1 | 0 |
| LIVE PAGE | Doncaster | Yorkshire - South | 21 | 1 | /doncaster/service-administrator-jobs | 16 | 1 | 0 | 2 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Portsmouth | Hampshire | 21 | 1 | /portsmouth/service-administrator-jobs | 17 | 1 | 1 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Northampton | Northamptonshire | 20 | 1 | /northampton/service-administrator-jobs | 10 | 0 | 7 | 0 | 0 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Blackburn | Lancashire - East | 19 | 1 | /blackburn/jobs | 18 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Gloucester | Gloucestershire | 19 | 1 | /gloucester/service-administrator-jobs | 15 | 0 | 3 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Oxford | Oxfordshire | 19 | 1 | /oxford/service-administrator-jobs | 13 | 4 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Chelmsford | Essex | 18 | 1 | /chelmsford/service-administrator-jobs | 11 | 3 | 2 | 1 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wakefield | Yorkshire - West | 18 | 1 | /wakefield/jobs | 12 | 2 | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| LIVE PAGE | Warwick | West Midlands - Coventry & Warwickshire | 18 | 1 | /warwick/service-administrator-jobs | 12 | 0 | 1 | 1 | 0 | 3 | 0 | 1 | 0 |
| LIVE PAGE | Chester | Cheshire - West | 17 | 1 | /chester/jobs | 14 | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Guildford | Surrey | 17 | 1 | /guildford/jobs | 8 | 1 | 5 | 3 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Poole | Dorset | 17 | 1 | /poole/service-administrator-jobs | 11 | 2 | 2 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Stockport | Greater Manchester - South | 17 | 1 | /stockport/service-administrator-jobs | 16 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Bedford | Bedfordshire | 16 | 1 | /bedford/service-administrator-jobs | 10 | 0 | 4 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Bournemouth | Dorset | 16 | 1 | /bournemouth/service-administrator-jobs | 5 | 8 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Derby | Derbyshire | 16 | 1 | /derby/jobs | 14 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Ipswich | Suffolk | 16 | 1 | /ipswich/jobs | 9 | 0 | 5 | 0 | 0 | 1 | 1 | 0 | 0 |
| LIVE PAGE | Macclesfield | Cheshire - East | 16 | 1 | /macclesfield/service-administrator-jobs | 14 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | York | Yorkshire - North | 16 | 1 | /york/service-administrator-jobs | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bolton | Greater Manchester - Wigan & Bolton | 15 | 1 | /bolton/jobs | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Crawley | Sussex | 14 | 1 | /crawley/service-administrator-jobs | 9 | 2 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Dudley | West Midlands - Black Country | 14 | 1 | /dudley/jobs | 13 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Harrogate | Yorkshire - North | 14 | 1 | /harrogate/service-administrator-jobs | 13 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Swindon | Wiltshire | 14 | 1 | /swindon/service-administrator-jobs | 13 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Bracknell | Berkshire | 13 | 1 | /bracknell/jobs | 8 | 1 | 2 | 0 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Brighton & Hove | Sussex | 13 | 1 | /brighton-hove/service-administrator-jobs | 7 | 3 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Preston | Lancashire - Central | 13 | 1 | /preston/jobs | 10 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Walsall | West Midlands - Black Country | 13 | 1 | /walsall/service-administrator-jobs | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Chesterfield | Derbyshire | 12 | 1 | /chesterfield/jobs | 9 | 0 | 1 | 0 | 0 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Watford | Hertfordshire | 12 | 1 | /watford/service-administrator-jobs | 7 | 0 | 3 | 0 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Basingstoke | Hampshire | 11 | 1 | /basingstoke/service-administrator-jobs | 5 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Colchester | Essex | 11 | 1 | /colchester/jobs | 5 | 5 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Corby | Northamptonshire | 11 | 1 | /corby/jobs | 8 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Dartford | Kent | 11 | 1 | /dartford/service-administrator-jobs | 10 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Horsham | Sussex | 10 | 1 | /horsham/service-administrator-jobs | 6 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Luton | Bedfordshire | 10 | 1 | /luton/jobs | 7 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Sunderland | North East - Tyneside, Wearside & Northumberland | 10 | 1 | /sunderland/service-administrator-jobs | 5 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Woking | Surrey | 10 | 1 | /woking/jobs | 9 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Plymouth | Devon | 9 | 1 | /plymouth/service-administrator-jobs | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Redditch | Worcestershire | 9 | 1 | /redditch/jobs | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Salford | Greater Manchester - Manchester & Salford | 9 | 1 | /salford/jobs | 5 | 1 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Shrewsbury | Shropshire | 9 | 1 | /shrewsbury/service-administrator-jobs | 6 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Swansea | Wales South - Swansea Bay | 9 | 1 | /swansea/service-administrator-jobs | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wrexham | North Wales - East | 9 | 1 | /wrexham/jobs | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Aylesbury | Buckinghamshire | 8 | 1 | /aylesbury/service-administrator-jobs | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Bath | Bristol & Bath | 8 | 1 | /bath/service-administrator-jobs | 5 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Cheltenham | Gloucestershire | 8 | 1 | /cheltenham/jobs | 5 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Kettering | Northamptonshire | 8 | 1 | /kettering/jobs | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Newport | Wales South -gwent | 8 | 1 | /newport/jobs | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Rugby | West Midlands - Coventry & Warwickshire | 8 | 1 | /rugby/jobs | 4 | 0 | 2 | 0 | 1 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Sittingbourne | Kent | 8 | 1 | /sittingbourne/jobs | 3 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Belfast | Northern Ireland - East | 7 | 1 | /belfast/service-administrator-jobs | 5 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Canterbury | Kent | 7 | 1 | /canterbury/jobs | 3 | 0 | 0 | 1 | 0 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Farnham | Surrey | 7 | 1 | /farnham/service-administrator-jobs | 4 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |
| LIVE PAGE | Gateshead | North East - Tyneside, Wearside & Northumberland | 7 | 1 | /gateshead/jobs | 4 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Hemel Hempstead | Hertfordshire | 7 | 1 | /hemel-hempstead/service-administrator-jobs | 3 | 0 | 1 | 0 | 0 | 3 | 0 | 0 | 0 |
| LIVE PAGE | Hertford | Hertfordshire | 7 | 1 | /hertford/jobs | 5 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | High Wycombe | Buckinghamshire | 7 | 1 | /high-wycombe/jobs | 6 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Maidstone | Kent | 7 | 1 | /maidstone/service-administrator-jobs | 5 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Solihull | West Midlands - Birmingham & Solihull | 7 | 1 | /solihull/jobs | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Stoke-on-trent | Staffordshire | 7 | 1 | /stoke-on-trent/service-administrator-jobs | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Worcester | Worcestershire | 7 | 1 | /worcester/service-administrator-jobs | 3 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Ashford | Kent | 6 | 1 | /ashford/service-administrator-jobs | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Barnsley | Yorkshire - South | 6 | 1 | /barnsley/service-administrator-jobs | 3 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Eastleigh | Hampshire | 6 | 1 | /eastleigh/service-administrator-jobs | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Hereford | Herefordshire | 6 | 1 | /hereford/jobs | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Northallerton | Yorkshire - North | 6 | 1 | /northallerton/jobs | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Redhill | Surrey | 6 | 1 | /redhill/jobs | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Rotherham | Yorkshire - South | 6 | 1 | /rotherham/service-administrator-jobs | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wirral | Merseyside - Wirral | 6 | 1 | /wirral/jobs | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Altrincham | Greater Manchester - South | 5 | 1 | /altrincham/service-administrator-jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Carlisle | Cumbria - North | 5 | 1 | /carlisle/jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Crewe | Cheshire - East | 5 | 1 | /crewe/jobs | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| LIVE PAGE | Dundee | Scotland Central - Tayside | 5 | 1 | /dundee/jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Durham | North East - County Durham & Darlington/Hartlepool | 5 | 1 | /durham/jobs | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | King's Lynn | Norfolk | 5 | 1 | /kings-lynn/jobs | 2 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Leatherhead | Surrey | 5 | 1 | /leatherhead/jobs | 2 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 |
| LIVE PAGE | Stafford | Staffordshire | 5 | 1 | /stafford/jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Stevenage | Hertfordshire | 5 | 1 | /stevenage/jobs | 3 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Trafford | Greater Manchester - South | 5 | 1 | /trafford/jobs | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Hull | Yorkshire - East | 3 | 1 | /hull/service-administrator-jobs | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Oldham | Greater Manchester - North | 3 | 1 | /oldham/jobs | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Scarborough | Yorkshire - North | 3 | 1 | /scarborough/service-administrator-jobs | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Yeovil | Somerset | 3 | 1 | /yeovil/jobs | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Abingdon | Oxfordshire | 2 | 1 | /abingdon/jobs | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Lincoln | Lincolnshire | 2 | 1 | /lincoln/service-administrator-jobs | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Witney | Oxfordshire | 1 | 1 | /witney/jobs | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Chester Le Street |  | 0 | 1 | /chester-le-street/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Newtownabbey |  | 0 | 1 | /newtownabbey/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LIVE PAGE | Wigston |  | 0 | 1 | /wigston/service-administrator-jobs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Uxbridge | London | 21 | 0 |  | 14 | 3 | 1 | 0 | 0 | 2 | 0 | 1 | 0 |
| HOLD – LONDON | Croydon | London | 13 | 0 |  | 10 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Surbiton | London | 13 | 0 |  | 8 | 1 | 1 | 2 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Bromley | London | 8 | 0 |  | 4 | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Kingston Upon Thames | London | 8 | 0 |  | 5 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Harrow | London | 7 | 0 |  | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hounslow | London | 7 | 0 |  | 2 | 3 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Beckenham | London | 6 | 0 |  | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Sutton | London | 6 | 0 |  | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| HOLD – LONDON | Newham | London | 5 | 0 |  | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Brentford | London | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Edgware | London | 4 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hayes | London | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Barking | London | 3 | 0 |  | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Borehamwood | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Greenford | London | 3 | 0 |  | 1 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Ilford | London | 3 | 0 |  | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Morden | London | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | New Malden | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Orpington | London | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Romford | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Ruislip | London | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | South Croydon | London | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Twickenham | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wembley | London | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Bexley | London | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Dagenham | London | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Enfield | London | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Erith | London | 2 | 0 |  | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Holloway | London | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Isleworth | London | 2 | 0 |  | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Islington | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Lambeth | London | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Loughton | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Northwood | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wallington | London | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Wandsworth | London | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| HOLD – LONDON | Bexleyheath | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Brimsdown | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Brixton | London | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Carshalton | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Chessington | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Feltham | London | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hackney | London | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hammersmith And Fulham | London | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Hillingdon | London | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Northolt | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Purley | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Southall | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Southwark | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | West Drayton | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | West Wickham | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| HOLD – LONDON | Woodford Green | London | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hastings | Sussex | 10 | 0 |  | 1 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Basildon | Essex | 9 | 0 |  | 3 | 2 | 2 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Sevenoaks | Kent | 8 | 0 |  | 3 | 2 | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Trowbridge | Wiltshire | 8 | 0 |  | 1 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Salisbury | Wiltshire | 7 | 0 |  | 0 | 4 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| MONITOR | Weybridge | Surrey | 7 | 0 |  | 3 | 0 | 1 | 0 | 2 | 1 | 0 | 0 | 0 |
| MONITOR | Ferndown | Dorset | 6 | 0 |  | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Heanor | Derbyshire | 6 | 0 |  | 2 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hove | Sussex | 6 | 0 |  | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newbury | Berkshire | 6 | 0 |  | 3 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Wokingham | Berkshire | 6 | 0 |  | 2 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Braintree | Essex | 5 | 0 |  | 1 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brinsworth | Yorkshire - South | 5 | 0 |  | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dorchester | Dorset | 5 | 0 |  | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Frome | Somerset | 5 | 0 |  | 2 | 0 | 1 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Godalming | Surrey | 5 | 0 |  | 1 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 |
| MONITOR | Horley | Surrey | 5 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| MONITOR | Worksop | Nottinghamshire | 5 | 0 |  | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Alton | Hampshire | 4 | 0 |  | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Andover | Hampshire | 4 | 0 |  | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Batley | Yorkshire - West | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Chippenham | Wiltshire | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Dorking | Surrey | 4 | 0 |  | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | East Grinstead | Sussex | 4 | 0 |  | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Felixstowe | Suffolk | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Haywards Heath | Sussex | 4 | 0 |  | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Newmarket | Suffolk | 4 | 0 |  | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Nuneaton | West Midlands - Coventry & Warwickshire | 4 | 0 |  | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Oswestry | Shropshire | 4 | 0 |  | 3 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Tonbridge | Kent | 4 | 0 |  | 0 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Wellingborough | Northamptonshire | 4 | 0 |  | 3 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wilmslow | Cheshire - East | 4 | 0 |  | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Winsford | Cheshire - West | 4 | 0 |  | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Aldershot | Hampshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ashington | North East - Tyneside, Wearside & Northumberland | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bagshot | Surrey | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| MONITOR | Birkenhead | Merseyside - Wirral | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bishop Auckland | North East - County Durham & Darlington/Hartlepool | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Blandford Forum | Dorset | 3 | 0 |  | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Blyth | North East - Tyneside, Wearside & Northumberland | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Burgess Hill | Sussex | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chelmsley Wood | West Midlands - Birmingham & Solihull | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chorley | Lancashire - Central | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Christchurch | Dorset | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Cirencester | Gloucestershire | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Conwy | North Wales - East | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cosham | Hampshire | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Dereham | Norfolk | 3 | 0 |  | 0 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Eccles | Greater Manchester - Manchester & Salford | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Falmouth | Cornwall | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Flint | North Wales - East | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gillingham | Kent | 3 | 0 |  | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Goole | Yorkshire - East | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Harpenden | Hertfordshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Heathfield | Sussex | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kidderminster | Worcestershire | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Kingswinford | West Midlands - Black Country | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kirkcaldy | Scotland Central - Fife | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knaphill | Surrey | 3 | 0 |  | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knutsford | Cheshire - East | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leyland | Lancashire - Central | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Lowestoft | Suffolk | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Maldon | Essex | 3 | 0 |  | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Malton | Yorkshire - North | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Montrose | North Scotland | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | New Milton | Hampshire | 3 | 0 |  | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newton-le-willows | Merseyside - St Helens & Knowsley | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Northfleet | Kent | 3 | 0 |  | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Perth | Scotland Central - Tayside | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Prenton | Merseyside - Wirral | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ramsbottom | Greater Manchester - North | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Romsey | Hampshire | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sherborne | Dorset | 3 | 0 |  | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Albans | Hertfordshire | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Helens | Merseyside - St Helens & Knowsley | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Leonards-on-sea | Sussex | 3 | 0 |  | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stone | Staffordshire | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Thame | Oxfordshire | 3 | 0 |  | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Wallingford | Oxfordshire | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wareham | Dorset | 3 | 0 |  | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Waterlooville | Hampshire | 3 | 0 |  | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Welwyn Garden City | Hertfordshire | 3 | 0 |  | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weston-super-mare | Somerset | 3 | 0 |  | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wimborne | Dorset | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Windsor | Berkshire | 3 | 0 |  | 0 | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Witham | Essex | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Woodbridge | Suffolk | 3 | 0 |  | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Accrington | Lancashire - East | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Addlestone | Surrey | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Ashton-under-lyne | Greater Manchester - South | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bedlington | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bexhill-on-sea | Sussex | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bordon | Hampshire | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brentwood | Essex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bridlington | Yorkshire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brierley Hill | West Midlands - Black Country | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Brighouse | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Buckingham | Buckinghamshire | 2 | 0 |  | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| MONITOR | Buxton | Derbyshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Clacton-on-sea | Essex | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cleckheaton | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Consett | North East - County Durham & Darlington/Hartlepool | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dalkeith | Scotland Central - Edinburgh & Lothians | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Devizes | Wiltshire | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dewsbury | Yorkshire - West | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Dover | Kent | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Droitwich | Worcestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ellesmere Port | Cheshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ely | Cambridgeshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Epping | Essex | 2 | 0 |  | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Evesham | Worcestershire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Falkirk | Scotland Central - Falkirk & Stirling | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fetcham | Surrey | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Folkestone | Kent | 2 | 0 |  | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gravesend | Kent | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grays | Essex | 2 | 0 |  | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| MONITOR | Great Yarmouth | Norfolk | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hailsham | Sussex | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Halesowen | West Midlands - Black Country | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Harlow | Essex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hartlepool | North East - County Durham & Darlington/Hartlepool | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hatfield | Hertfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Herne Bay | Kent | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hook | Hampshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hook Norton | Oxfordshire | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Huntingdon | Cambridgeshire | 2 | 0 |  | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Ilminster | Somerset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Irchester | Northamptonshire | 2 | 0 |  | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Knaresborough | Yorkshire - North | 2 | 0 |  | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Knowsley | Merseyside - St Helens & Knowsley | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ledbury | Herefordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leigh-on-sea | Essex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Leighton Buzzard | Bedfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lewes | Sussex | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Littlehampton | Sussex | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Liversedge | Yorkshire - West | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Marlborough | Wiltshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Marlow | Buckinghamshire | 2 | 0 |  | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Melksham | Wiltshire | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Nelson | Lancashire - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newark | Nottinghamshire | 2 | 0 |  | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| MONITOR | Newquay | Cornwall | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Normanton | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | North Shields | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pontypridd | Wales South - Valleys | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Potters Bar | Hertfordshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Prestatyn | North Wales - East | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Radstock | Somerset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ramsgate | Kent | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ripley | Derbyshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rochester | Kent | 2 | 0 |  | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Sandwich | Kent | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shefford | Bedfordshire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shepperton | Surrey | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Silsden | Yorkshire - West | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Skipton | Yorkshire - North | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Snodland | Kent | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | South Shields | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Southsea | Hampshire | 2 | 0 |  | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Southwick | Sussex | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stratford-upon-avon | West Midlands - Coventry & Warwickshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stretford | Greater Manchester - Manchester & Salford | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stroud | Gloucestershire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Studley | West Midlands - Coventry & Warwickshire | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Sudbury | Suffolk | 2 | 0 |  | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Sutton Coldfield | West Midlands - Birmingham & Solihull | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tadley | Hampshire | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tewkesbury | Gloucestershire | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Totton | Hampshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Truro | Cornwall | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Urmston | Greater Manchester - South | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wallsend | North East - Tyneside, Wearside & Northumberland | 2 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| MONITOR | Waltham Abbey | Essex | 2 | 0 |  | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wells | Somerset | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Westbury | Wiltshire | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wickford | Essex | 2 | 0 |  | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wymondham | Norfolk | 2 | 0 |  | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Yate | Bristol & Bath | 2 | 0 |  | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Aberdare | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Alcester | West Midlands - Coventry & Warwickshire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Alnwick | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Antrim | Northern Ireland - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Axbridge | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Aylesford | Kent | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Bamber Bridge | Lancashire - Central | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Banbury | Oxfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Barrow-in-furness | Cumbria - South | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Battle | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Beaconsfield | Buckinghamshire | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Benfleet | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bentley | Yorkshire - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Beverley | Yorkshire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Biggleswade | Bedfordshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bishop's Stortford | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Blaydon-on-Tyne | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bodmin | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bognor Regis | Sussex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Boreham | Essex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bourne End | Buckinghamshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Broadstairs | Kent | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Bury St. Edmunds | Suffolk | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Caerphilly | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Calne | Wiltshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cannock | Staffordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chapelhall | Scotland West - Lanarkshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chatham | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Chertsey | Surrey | 1 | 0 |  | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Chesham | Buckinghamshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Clitheroe | Lancashire - East | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Coalville | Leicestershire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Coatbridge | Scotland West - Lanarkshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Colden Common | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Corsham | Wiltshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cramlington | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Cranleigh | Surrey | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Crewkerne | Somerset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Crowthorne | Berkshire | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Darwen | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Deal | Kent | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Denton | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Diss | Norfolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Dunfermline | Scotland Central - Fife | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Duxford | Cambridgeshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Egham | Surrey | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Elgin | North Scotland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Elland | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Emsworth | Hampshire | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Eye | Suffolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Farnborough | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Featherstone | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fleet | Hampshire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Fordingbridge | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Frinton-on-sea | Essex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Gerrards Cross | Buckinghamshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Glenfield | Leicestershire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Glenrothes | Scotland Central - Fife | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Grangemouth | Scotland Central - Falkirk & Stirling | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Greenhithe | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Halesworth | Suffolk | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Harwich | Essex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Haslingden | Lancashire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Haydock | Merseyside - St Helens & Knowsley | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hedge End | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Henley-on-thames | Oxfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hexham | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Heywood | Greater Manchester - North | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Hindhead | Surrey | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hoddesdon | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Honiton | Devon | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hyde | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Hythe | Kent | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Inverness | North Scotland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ivybridge | Devon | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Jarrow | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Keighley | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Kingsteignton | Devon | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Knebworth | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lancing | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lichfield | Staffordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lisburn | Northern Ireland - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Liskeard | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lutterworth | Leicestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lydney | Gloucestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Lyndhurst | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Margate | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Market Drayton | Shropshire | 1 | 0 |  | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| MONITOR | Middleton | Greater Manchester - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Midhurst | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Morpeth | North East - Tyneside, Wearside & Northumberland | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Motherwell | Scotland West - Lanarkshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Nantwich | Cheshire - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Narborough | Leicestershire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Neath | Wales South - Swansea Bay | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newton Aycliffe | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Newtownards | Northern Ireland - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | North Walsham | Norfolk | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Northwich | Cheshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Olney | Buckinghamshire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Peterlee | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pontyclun | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Pontypool | Wales South - Gwent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Prestonpans | Scotland Central - Edinburgh & Lothians | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rayleigh | Essex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Redruth | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Retford | Nottinghamshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Rhyl | North Wales - East | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ringwood | Hampshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Ripon | Yorkshire - North | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Ryde | Hampshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sale | Greater Manchester - South | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Saltash | Cornwall | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Saltdean | Sussex | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Scunthorpe | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Seaham | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sedgefield | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shaftesbury | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shepshed | Leicestershire | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sherburn In Elmet | Yorkshire - North | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Shoreham-by-sea | Sussex | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sleaford | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Smethwick | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Spalding | Lincolnshire | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St Helens | Merseyside - St Helens & Knowsley | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | St. Austell | Cornwall | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Stanford-le-hope | Essex | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stanley | North East - County Durham & Darlington/Hartlepool | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stockton-on-tees | North East - Tees Valley | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Stourbridge | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Sunbury-on-thames | Surrey | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Takeley | Essex | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tarporley | Cheshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Thatcham | Berkshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tiverton | Devon | 1 | 0 |  | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tonypandy | Wales South - Valleys | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Torquay | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Totnes | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Tredegar | Wales South - Gwent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Uttoxeter | Staffordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Verwood | Dorset | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wallasey | Merseyside - Wirral | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Waltham | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wantage | Oxfordshire | 1 | 0 |  | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| MONITOR | Warminster | Wiltshire | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wednesbury | West Midlands - Black Country | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Welwyn | Hertfordshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Westerham | Kent | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Wetherby | Yorkshire - West | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Weymouth | Dorset | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Whyteleafe | Surrey | 1 | 0 |  | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Willand | Devon | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Woodhall Spa | Lincolnshire | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Worsley | Greater Manchester - Manchester & Salford | 1 | 0 |  | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| MONITOR | Yatton | Bristol & Bath | 1 | 0 |  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

> LIVE counts come directly from the current published `app/` JSON, deduplicated within each canonical region/family slice while preserving legitimate appearances in more than one family. This is the live-site authority for the reconciliation above; the dated source-count CSV is shown only as a freshness cross-check. The overview covers all 78 assessable UK markets; LIVE status remains controlled only by the slice register. Before same-feed 78-market coverage has run, NOT LIVE Admin/Support and Customer Service may fall back to the latest all-region Module 2 profile (2026-08-17), and Service Admin may also add current Teaching Vacancies regional candidate output. `—` means not assessed / no current source; it does NOT mean zero. NOT LIVE Service Admin and Support Worker were assessed from the same JobG8 daily feed (2026-11-25) used by the production family run, across 78 UK markets with the config-driven production wrappers, persistent review decisions and canonical geo. NOT LIVE Sales Advisor was assessed from that same feed across 78 UK markets using the governed Customer Sales classifier, canonical geo, campaign dedupe and final production QA. Sales diagnostic counts are evidence only and never activate a slice automatically; LIVE Sales Advisor counts continue to come from the current published Customer Sales configured-slice JSON. NOT LIVE Paralegal, Marketing, Finance / Accounts and HR / Recruitment were assessed from that same feed across 78, 78, 78 and 78 UK markets respectively, using their governed production boundaries and canonical geo. NOT LIVE Customer Service / Contact Centre was assessed from that same feed across 78 UK markets using its governed exact-title, salary and geography rules. All diagnostic counts are evidence only and never activate a slice automatically. Rolling family history stores one snapshot per feed date, replaces same-date reruns, retains the latest 14 feed dates and is used only as decision evidence for NOT LIVE slices.

## LIVE

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire | 43 |  | 7 | 6 |  | 14 |  |  |
| Berkshire | 79 | 10 | 14 | 17 | 20 | 35 | 3 |  |
| Bristol & Bath | 76 |  | 16 | 9 | 9 | 27 |  |  |
| Buckinghamshire | 83 |  |  | 19 | 22 | 35 | 2 | 3 |
| Cambridgeshire | 67 |  | 7 | 4 | 9 | 30 |  |  |
| Cheshire - East | 29 |  | 4 |  |  | 22 |  |  |
| Cheshire - Warrington & Halton | 39 |  |  |  | 6 | 20 |  |  |
| Cheshire - West | 21 |  |  |  | 4 | 9 |  |  |
| Cornwall | 11 |  |  |  |  | 6 |  |  |
| Cumbria - North | 5 |  |  |  |  |  |  |  |
| Cumbria - South |  | 1 |  |  |  |  |  |  |
| Cumbria - West |  |  |  |  |  |  |  |  |
| Derbyshire | 57 |  | 5 |  |  | 20 |  |  |
| Devon | 61 |  | 3 | 5 |  | 22 |  |  |
| Dorset | 57 | 26 | 8 |  | 1 | 26 |  |  |
| Essex | 117 | 28 | 10 | 32 | 10 | 42 | 5 |  |
| Gloucestershire | 84 |  | 8 |  | 6 | 29 | 2 |  |
| Greater Manchester - Manchester & Salford | 160 | 10 | 18 | 31 | 33 | 62 | 3 | 8 |
| Greater Manchester - North | 21 |  |  |  |  | 20 |  |  |
| Greater Manchester - South | 37 |  |  |  | CHECK | 9 |  |  |
| Greater Manchester - Wigan & Bolton | 26 |  |  |  |  | 7 |  |  |
| Hampshire | 168 | 30 | 24 | 10 | 6 | 67 | 4 | 9 |
| Herefordshire | 8 |  |  |  |  | CHECK |  |  |
| Hertfordshire | 101 |  | 8 | 14 | 10 | 33 |  | 2 |
| Kent | 117 | 26 | 14 | 14 | 21 | 52 |  | 4 |
| Lancashire - Blackpool & Fylde | 6 |  |  |  |  |  |  |  |
| Lancashire - Central | 20 |  |  |  |  | 11 |  |  |
| Lancashire - East | 27 |  |  |  |  | 11 |  |  |
| Lancashire - North |  |  |  |  |  |  |  |  |
| Lancashire - West |  |  |  |  |  |  |  |  |
| Leicestershire | 82 |  | 6 |  | 8 | 23 | 9 |  |
| Lincolnshire | 28 |  |  | 4 |  | CHECK |  |  |
| London | 456 | 91 | 82 | 116 | 159 | 201 | 32 | 10 |
| Merseyside - Liverpool | 43 |  |  | 9 | 5 | 21 |  |  |
| Merseyside - Sefton |  |  |  |  |  |  |  |  |
| Merseyside - St Helens & Knowsley | 10 |  |  |  |  |  |  |  |
| Merseyside - Wirral | 12 |  |  |  |  | 6 |  |  |
| Norfolk | 40 |  | 10 | 18 | 10 | 18 |  |  |
| North East | 87 | 28 | 19 | 10 | 16 | 35 | 3 | 8 |
| North Scotland | 14 |  | 1 |  |  |  |  |  |
| North Wales - East | 18 |  |  |  |  |  |  |  |
| North Wales - West |  |  |  |  |  |  |  |  |
| Northamptonshire | 66 |  | 13 |  | 8 | 30 |  |  |
| Northern Ireland - East | 10 |  |  |  | 2 | CHECK | CHECK |  |
| Northern Ireland - West |  |  |  |  |  |  |  |  |
| Nottinghamshire | 67 | 15 | 13 | 8 | 12 | 35 | 4 |  |
| Oxfordshire | 68 | 7 | 6 | 6 | 10 | 29 |  |  |
| Rutland |  |  |  |  |  |  |  |  |
| Scotland - Borders |  |  |  |  |  |  |  |  |
| Scotland Central - Edinburgh & Lothians | 41 |  |  | 6 |  | 13 |  |  |
| Scotland Central - Falkirk & Stirling | 8 |  |  |  |  |  |  |  |
| Scotland Central - Fife | 8 |  |  |  |  |  |  |  |
| Scotland Central - Tayside | 8 |  |  |  |  |  |  |  |
| Scotland West - Ayrshire |  |  |  |  |  |  |  |  |
| Scotland West - Glasgow | 42 |  | 12 | 5 | 5 | 14 |  |  |
| Scotland West - Lanarkshire | 3 |  |  |  |  |  |  |  |
| Scotland West - Renfrewshire & Inverclyde |  |  |  |  |  |  |  |  |
| Shropshire | 39 |  |  |  | 10 | 14 |  |  |
| Somerset | 47 |  | 5 |  |  | 15 |  |  |
| Staffordshire | 63 |  |  |  | 5 | 16 | 4 | 4 |
| Suffolk | 57 |  | 11 | 12 |  | 22 | 1 |  |
| Surrey | 155 | 11 | 17 | 17 | 26 | 62 | 8 | 10 |
| Sussex | 127 | 48 | 12 | 22 | 12 | 37 | 3 | 3 |
| Wales - Mid |  |  |  |  |  |  |  |  |
| Wales - West |  |  |  |  |  |  |  |  |
| Wales South - Cardiff & Vale | 23 |  |  |  |  | 10 |  |  |
| Wales South - Gwent | 14 |  |  |  |  |  |  |  |
| Wales South - Swansea Bay | 14 |  |  |  |  |  |  |  |
| Wales South - Valleys | 7 |  |  |  |  |  |  |  |
| West Midlands - Birmingham & Solihull | 151 |  |  | 10 | 26 | 44 | 6 |  |
| West Midlands - Black Country | 63 |  |  |  |  | 28 | 3 |  |
| West Midlands - Coventry & Warwickshire | 104 |  | 8 | 8 | 8 | 60 | CHECK | 3 |
| Wiltshire | 41 | 18 |  |  |  | 9 |  |  |
| Worcestershire | 42 |  | 5 |  |  | 13 |  |  |
| Yorkshire - East | 13 |  |  |  |  | 8 |  |  |
| Yorkshire - North | 50 |  |  | 9 | 5 | 23 |  |  |
| Yorkshire - South | 74 | 8 |  | 9 | 8 | 30 |  |  |
| Yorkshire - West | 186 | 8 | 16 | 17 | 19 | 87 | 8 | 7 |

## NOT LIVE

> Cells show `today / 14d avg / 6+ days` over observed feed dates (maximum 14). The 6+ measure is a watch signal only, not an automatic activation threshold.

| Region | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bedfordshire |  | 3 / 4.5 / 0/14 |  |  | 3 / 3.3 / 0/14 |  | 0 / 0.0 / 0/14 | 3 / 3.6 / 0/14 |
| Berkshire |  |  |  |  |  |  |  | 5 / 3.3 / 0/14 |
| Bristol & Bath |  | 17 / 12.1 / 14/14 |  |  |  |  | 4 / 4.1 / 0/14 | 3 / 3.4 / 0/14 |
| Buckinghamshire |  | 4 / 2.6 / 0/14 | 5 / 5.4 / 7/14 |  |  |  |  |  |
| Cambridgeshire |  | 3 / 2.1 / 0/14 |  |  |  |  | 1 / 0.9 / 0/14 | 2 / 2.4 / 0/14 |
| Cheshire - East |  | 5 / 6.3 / 8/14 |  | 0 / 0.1 / 0/14 | 3 / 2.7 / 0/14 |  | 0 / 0.0 / 0/14 | 1 / 1.4 / 0/14 |
| Cheshire - Warrington & Halton |  | 8 / 6.6 / 14/14 | 2 / 2.1 / 0/14 | 1 / 0.9 / 0/14 |  |  | 0 / 0.1 / 0/14 | 2 / 2.1 / 0/14 |
| Cheshire - West |  | 5 / 4.0 / 0/14 | 1 / 1.2 / 0/14 | 4 / 3.6 / 0/14 |  |  | 1 / 1.0 / 0/14 | 1 / 0.6 / 0/14 |
| Cornwall |  | 4 / 4.1 / 0/14 | 3 / 1.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |  | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 |
| Cumbria - North |  | 4 / 6.6 / 10/14 | 4 / 4.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 | 2 / 1.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Cumbria - South | 7 / 8.4 / 12/14 |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Cumbria - West | 2 / 2.4 / 1/14 | 9 / 5.2 / 4/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.4 / 0/14 | 0 / 0.0 / 0/14 |
| Derbyshire |  | 8 / 6.6 / 10/14 |  | 4 / 4.1 / 0/14 | 11 / 10.4 / 14/14 |  | 5 / 3.4 / 0/14 | 3 / 2.1 / 0/14 |
| Devon |  | 14 / 13.4 / 14/14 |  |  | 1 / 2.2 / 0/14 |  | 4 / 2.5 / 0/14 | 4 / 5.0 / 2/14 |
| Dorset |  |  |  | 3 / 3.7 / 1/14 |  |  | 3 / 3.0 / 0/14 | 6 / 5.8 / 9/14 |
| Essex |  |  |  |  |  |  |  | 4 / 5.3 / 4/14 |
| Gloucestershire |  | 20 / 13.1 / 14/14 |  | 7 / 6.4 / 12/14 |  |  |  | 3 / 4.0 / 3/14 |
| Greater Manchester - Manchester & Salford |  |  |  |  |  |  |  |  |
| Greater Manchester - North |  | 5 / 3.8 / 4/14 | 4 / 3.1 / 0/14 | 0 / 1.5 / 0/14 | 2 / 2.1 / 0/14 |  | 0 / 0.1 / 0/14 | 1 / 1.1 / 0/14 |
| Greater Manchester - South |  | 0 / 0.1 / 0/14 | 3 / 3.1 / 0/14 | 3 / 3.6 / 0/14 |  |  | 2 / 1.6 / 0/14 | 0 / 0.0 / 0/14 |
| Greater Manchester - Wigan & Bolton |  | 5 / 3.1 / 0/14 | 1 / 1.1 / 0/14 | 1 / 1.0 / 0/14 | 1 / 1.0 / 0/14 |  | 1 / 0.4 / 0/14 | 5 / 5.3 / 5/14 |
| Hampshire |  |  |  |  |  |  |  |  |
| Herefordshire |  | 2 / 2.0 / 0/14 | 1 / 0.8 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.4 / 0/14 |  | 1 / 1.1 / 0/14 | 0 / 0.0 / 0/14 |
| Hertfordshire |  | 3 / 3.6 / 2/14 |  |  |  |  | 4 / 3.6 / 0/14 |  |
| Kent |  |  |  |  |  |  | 4 / 4.0 / 0/14 |  |
| Lancashire - Blackpool & Fylde |  | 5 / 1.7 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.1 / 0/14 | 4 / 3.8 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - Central |  | 5 / 3.7 / 0/14 | 3 / 3.5 / 0/14 | 1 / 0.1 / 0/14 | 4 / 4.4 / 0/14 |  | 1 / 0.9 / 0/14 | 1 / 0.4 / 0/14 |
| Lancashire - East |  | 8 / 3.6 / 1/14 | 2 / 1.6 / 0/14 | 2 / 2.9 / 0/14 | 1 / 0.9 / 0/14 |  | 0 / 0.9 / 0/14 | 2 / 1.9 / 0/14 |
| Lancashire - North | 4 / 3.3 / 0/14 | 2 / 1.9 / 0/14 | 2 / 2.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.4 / 0/14 | 2 / 1.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Lancashire - West | 5 / 5.4 / 7/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.0 / 0/14 | 4 / 3.8 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.4 / 0/14 |
| Leicestershire |  | 5 / 5.6 / 5/14 |  | 6 / 4.1 / 1/14 |  |  |  | 4 / 3.7 / 1/14 |
| Lincolnshire |  | 10 / 8.1 / 13/14 | 7 / 5.7 / 6/14 |  | 1 / 0.4 / 0/14 |  | 0 / 0.0 / 0/14 | 2 / 1.9 / 0/14 |
| London |  |  |  |  |  |  |  |  |
| Merseyside - Liverpool |  | 1 / 0.6 / 0/14 | 1 / 1.4 / 0/14 |  |  |  | 1 / 0.7 / 0/14 | 2 / 1.4 / 0/14 |
| Merseyside - Sefton | 2 / 2.3 / 0/14 | 1 / 0.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Merseyside - St Helens & Knowsley |  | 1 / 0.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 5 / 5.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Merseyside - Wirral |  | 4 / 2.7 / 0/14 | 1 / 0.1 / 0/14 | 2 / 2.0 / 0/14 | 1 / 3.4 / 0/14 |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Norfolk |  | 9 / 7.9 / 13/14 |  |  |  |  | 3 / 2.4 / 0/14 | 4 / 4.0 / 0/14 |
| North East |  |  |  |  |  |  |  |  |
| North Scotland |  | 3 / 2.8 / 0/14 |  | 8 / 6.8 / 12/14 | 0 / 0.0 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.2 / 0/14 |
| North Wales - East |  | 15 / 11.6 / 14/14 | 0 / 1.1 / 0/14 | 2 / 1.1 / 0/14 | 1 / 0.9 / 0/14 | 4 / 3.9 / 0/14 | 2 / 2.1 / 0/14 | 2 / 1.9 / 0/14 |
| North Wales - West | 3 / 2.0 / 0/14 | 2 / 2.0 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 | 1 / 0.3 / 0/14 | 0 / 0.0 / 0/14 |
| Northamptonshire |  | 4 / 2.4 / 0/14 |  | 3 / 3.2 / 2/14 |  |  | 6 / 5.1 / 6/14 | 1 / 1.6 / 0/14 |
| Northern Ireland - East |  | 0 / 0.2 / 0/14 | 1 / 2.1 / 0/14 | 0 / 0.0 / 0/14 |  |  |  | 1 / 0.5 / 0/14 |
| Northern Ireland - West | 4 / 4.8 / 5/14 | 1 / 0.6 / 0/14 | 1 / 3.6 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 1.1 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.6 / 0/14 |
| Nottinghamshire |  |  |  |  |  |  |  | 3 / 1.8 / 0/14 |
| Oxfordshire |  |  |  |  |  |  | 5 / 6.0 / 11/14 | 4 / 3.1 / 0/14 |
| Rutland | 1 / 0.3 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.3 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland - Borders | 2 / 1.4 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.5 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Edinburgh & Lothians |  | 1 / 1.6 / 0/14 | 1 / 2.8 / 0/14 |  | 3 / 2.9 / 0/14 |  | 0 / 0.0 / 0/14 | 0 / 0.1 / 0/14 |
| Scotland Central - Falkirk & Stirling |  | 0 / 0.6 / 0/14 | 1 / 1.9 / 0/14 | 3 / 3.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 2.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland Central - Fife |  | 2 / 0.7 / 0/14 | 2 / 2.1 / 0/14 | 2 / 1.9 / 0/14 | 0 / 0.0 / 0/14 | 4 / 2.4 / 0/14 | 1 / 1.5 / 0/14 | 0 / 0.3 / 0/14 |
| Scotland Central - Tayside |  | 0 / 0.1 / 0/14 | 3 / 3.0 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.4 / 0/14 | 0 / 0.0 / 0/14 | 1 / 2.1 / 0/14 |
| Scotland West - Ayrshire | 6 / 6.0 / 14/14 | 2 / 1.3 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.9 / 0/14 | 0 / 0.0 / 0/14 | 2 / 2.5 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland West - Glasgow |  | 2 / 0.8 / 0/14 |  |  |  |  | 5 / 2.1 / 0/14 | 5 / 2.8 / 0/14 |
| Scotland West - Lanarkshire |  | 1 / 1.0 / 0/14 | 0 / 1.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 1.1 / 0/14 | 0 / 0.3 / 0/14 | 0 / 0.0 / 0/14 |
| Scotland West - Renfrewshire & Inverclyde | 2 / 3.5 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.9 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Shropshire |  | 4 / 3.4 / 0/14 | 8 / 7.3 / 13/14 | 3 / 2.9 / 0/14 |  |  | 1 / 2.9 / 0/14 | 4 / 2.6 / 0/14 |
| Somerset |  | 14 / 10.9 / 14/14 |  | 2 / 2.0 / 0/14 | 0 / 0.0 / 0/14 |  | 0 / 0.9 / 0/14 | 0 / 0.2 / 0/14 |
| Staffordshire |  | 5 / 4.6 / 0/14 | 8 / 6.2 / 8/14 | 2 / 2.8 / 1/14 |  |  |  |  |
| Suffolk |  | 17 / 12.4 / 11/14 |  |  | 6 / 5.3 / 8/14 |  |  | 4 / 3.4 / 0/14 |
| Surrey |  |  |  |  |  |  |  |  |
| Sussex |  |  |  |  |  |  |  |  |
| Wales - Mid | 1 / 1.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 1 / 0.9 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 |
| Wales - West | 0 / 0.9 / 0/14 | 3 / 3.8 / 1/14 | 0 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 1.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Cardiff & Vale |  | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 3 / 4.0 / 0/14 | 2 / 1.9 / 0/14 |  | 0 / 0.0 / 0/14 | 0 / 0.5 / 0/14 |
| Wales South - Gwent |  | 2 / 1.6 / 0/14 | 2 / 1.8 / 0/14 | 2 / 1.5 / 0/14 | 0 / 0.0 / 0/14 | 1 / 3.0 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.5 / 0/14 |
| Wales South - Swansea Bay |  | 3 / 2.3 / 0/14 | 0 / 0.0 / 0/14 | 2 / 1.4 / 0/14 | 0 / 0.0 / 0/14 | 5 / 4.7 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 |
| Wales South - Valleys |  | 2 / 1.3 / 0/14 | 0 / 0.1 / 0/14 | 0 / 0.0 / 0/14 | 0 / 0.0 / 0/14 | 2 / 3.8 / 0/14 | 1 / 1.0 / 0/14 | 0 / 0.5 / 0/14 |
| West Midlands - Birmingham & Solihull |  | 2 / 1.2 / 0/14 | 5 / 4.3 / 0/14 |  |  |  |  | 4 / 3.3 / 0/14 |
| West Midlands - Black Country |  | 8 / 5.6 / 8/14 | 3 / 3.8 / 2/14 | 0 / 0.4 / 0/14 | 1 / 1.1 / 0/14 |  |  | 3 / 3.1 / 0/14 |
| West Midlands - Coventry & Warwickshire |  | 5 / 6.7 / 12/14 |  |  |  |  |  |  |
| Wiltshire |  |  | 2 / 2.1 / 0/14 | 8 / 7.8 / 14/14 | 0 / 3.9 / 3/14 |  | 3 / 2.1 / 0/14 | 1 / 1.1 / 0/14 |
| Worcestershire |  | 8 / 6.0 / 9/14 |  | 3 / 3.6 / 0/14 | 3 / 1.8 / 0/14 |  | 2 / 2.0 / 0/14 | 3 / 2.3 / 0/14 |
| Yorkshire - East |  | 3 / 2.6 / 0/14 | 4 / 3.5 / 0/14 | 5 / 3.3 / 0/14 | 2 / 1.1 / 0/14 |  | 0 / 0.2 / 0/14 | 0 / 0.0 / 0/14 |
| Yorkshire - North |  | 10 / 11.1 / 14/14 | 2 / 5.3 / 7/14 |  |  |  | 0 / 0.0 / 0/14 | 0 / 0.6 / 0/14 |
| Yorkshire - South |  |  | 5 / 5.2 / 6/14 |  |  |  | 0 / 1.1 / 0/14 | 3 / 4.4 / 0/14 |
| Yorkshire - West |  |  |  |  |  |  |  |  |

## HEADLINE

| Measure | Service admin | Support worker | Sales advisor | Paralegal | Marketing | Finance / Accounts | HR / Recruitment | CS / Contact centre |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Live regions | 65 / 78 | 16 / 78 | 30 / 78 | 28 / 78 | 33 / 78 | 53 / 78 | 19 / 78 | 12 / 78 |
| Live slice placements | 3901 | 365 | 382 | 447 | 511 + 1 CHECK | 1512 + 3 CHECK | 100 + 2 CHECK | 71 |

**Live slices: 256 / 624.**
