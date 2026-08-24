# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **1,053**
Original title-rule Other / Unclassified: **3,063**
Jobs resolved by description-majority pass: **155**
Remaining Other / Unclassified after register-first + title + description passes: **1,423**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Admin / Customer Service | 1,482 | 14.8% |
| Other / Unclassified | 1,423 | 14.2% |
| Professional Finance / Accountancy | 1,296 | 13.0% |
| Legal / Conveyancing | 861 | 8.6% |
| Sales / Business Development | 780 | 7.8% |
| Healthcare / Clinical | 569 | 5.7% |
| HR / Recruitment | 490 | 4.9% |
| IT / Data / Software | 363 | 3.6% |
| Management / Team Leadership | 359 | 3.6% |
| Engineering / Technical | 341 | 3.4% |
| Care / Support Work | 328 | 3.3% |
| Financial Advice / Mortgages | 231 | 2.3% |
| Marketing / Digital / Creative | 231 | 2.3% |
| Retail / Store | 206 | 2.1% |
| Market Research / Field Interviewing | 168 | 1.7% |
| Insurance / Claims | 149 | 1.5% |
| Construction / Trades / Property | 143 | 1.4% |
| Operations / General Management | 115 | 1.1% |
| Property / Housing / Planning | 77 | 0.8% |
| Procurement / Buying / Supply Chain | 64 | 0.6% |
| Education / Teaching | 62 | 0.6% |
| Compliance / Risk / Quality | 60 | 0.6% |
| Charity / Fundraising / Community | 43 | 0.4% |
| Driving / Warehouse / Logistics | 41 | 0.4% |
| Employment Support / Careers | 36 | 0.4% |
| Security / Emergency Services | 18 | 0.2% |
| Hospitality / Catering | 16 | 0.2% |
| Science / Laboratory | 15 | 0.1% |
| Manufacturing / Production | 13 | 0.1% |
| Cleaning / Domestic / Facilities | 10 | 0.1% |
| Agriculture / Environment | 10 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Admin / Customer Service | 1,482 | 595 | 887 | 86 | 8.0 | 51 | 38 | 212 | London (232); Surrey (76); Hampshire (52); Kent (41); Essex (37) |
| Professional Finance / Accountancy | 1,296 | 223 | 1,073 | 80 | 10.0 | 57 | 44 | 60 | London (186); Bristol & Bath (51); Yorkshire - West (43); Sussex (41); Kent (41) |
| Legal / Conveyancing | 861 | 0 | 861 | 66 | 5.5 | 34 | 21 | 13 | London (164); Essex (84); Suffolk (74); Norfolk (53); Yorkshire - West (32) |
| Sales / Business Development | 780 | 0 | 780 | 75 | 7 | 49 | 25 | 50 | London (121); Hampshire (35); Greater Manchester - Manchester & Salford (24); Hertfordshire (23); Yorkshire - West (23) |
| Healthcare / Clinical | 569 | 0 | 569 | 78 | 4.0 | 29 | 13 | 53 | London (89); Hampshire (31); Sussex (29); Surrey (26); Berkshire (21) |
| HR / Recruitment | 490 | 122 | 368 | 62 | 4.0 | 29 | 15 | 45 | London (75); Bristol & Bath (27); Hampshire (22); Yorkshire - West (18); Hertfordshire (15) |
| IT / Data / Software | 363 | 0 | 363 | 55 | 3 | 22 | 8 | 28 | London (77); Hampshire (40); Bristol & Bath (19); Greater Manchester - Manchester & Salford (13); Gloucestershire (12) |
| Management / Team Leadership | 359 | 0 | 359 | 76 | 3.0 | 27 | 7 | 25 | London (24); Oxfordshire (20); Kent (16); Sussex (12); Hertfordshire (11) |
| Engineering / Technical | 341 | 0 | 341 | 59 | 4 | 26 | 9 | 31 | London (40); Northamptonshire (20); Bristol & Bath (15); Gloucestershire (11); Hampshire (11) |
| Care / Support Work | 328 | 110 | 218 | 66 | 3.0 | 20 | 4 | 31 | London (35); Hampshire (27); Sussex (15); Surrey (13); Greater Manchester - Manchester & Salford (9) |
| Financial Advice / Mortgages | 231 | 0 | 231 | 54 | 2.5 | 16 | 5 | 5 | London (22); Bristol & Bath (13); Essex (12); Yorkshire - West (12); Hampshire (11) |
| Marketing / Digital / Creative | 231 | 0 | 231 | 53 | 2 | 11 | 2 | 25 | London (65); Surrey (10); Greater Manchester - Manchester & Salford (9); Kent (7); Yorkshire - North (7) |
| Retail / Store | 206 | 0 | 206 | 61 | 2 | 13 | 3 | 23 | London (18); Greater Manchester - Manchester & Salford (11); Yorkshire - North (10); Wiltshire (7); Oxfordshire (7) |
| Market Research / Field Interviewing | 168 | 0 | 168 | 41 | 1 | 8 | 2 | 55 | London (12); Wiltshire (12); Worcestershire (9); North Scotland (6); Herefordshire (6) |
| Insurance / Claims | 149 | 0 | 149 | 33 | 2 | 5 | 2 | 12 | London (47); Yorkshire - West (10); Merseyside - Liverpool (8); Essex (7); Norfolk (5) |
| Construction / Trades / Property | 143 | 0 | 143 | 42 | 2.0 | 5 | 1 | 9 | London (27); Greater Manchester - Manchester & Salford (9); Cambridgeshire (7); Essex (7); Devon (5) |
| Operations / General Management | 115 | 0 | 115 | 40 | 1.0 | 6 | 1 | 10 | London (23); Oxfordshire (9); Hampshire (7); Essex (6); Devon (6) |
| Property / Housing / Planning | 77 | 0 | 77 | 34 | 1.0 | 2 | 1 | 9 | London (13); Sussex (5); West Midlands - Coventry & Warwickshire (4); Hertfordshire (4); Cumbria - North (3) |
| Procurement / Buying / Supply Chain | 64 | 0 | 64 | 27 | 2 | 2 | 0 | 12 | London (8); Essex (5); Derbyshire (3); Surrey (3); Yorkshire - West (2) |
| Education / Teaching | 62 | 0 | 62 | 24 | 1.0 | 3 | 1 | 8 | London (12); Cumbria - South (6); Sussex (5); Lancashire - North (4); Surrey (4) |
| Compliance / Risk / Quality | 60 | 0 | 60 | 24 | 1.0 | 1 | 1 | 4 | London (18); Scotland Central - Edinburgh & Lothians (4); Wiltshire (3); Bristol & Bath (3); West Midlands - Birmingham & Solihull (3) |
| Charity / Fundraising / Community | 43 | 0 | 43 | 17 | 1 | 1 | 1 | 3 | London (15); Buckinghamshire (4); Surrey (3); Yorkshire - West (2); Hampshire (2) |
| Driving / Warehouse / Logistics | 41 | 3 | 38 | 26 | 1.0 | 1 | 0 | 4 | London (5); Kent (2); West Midlands - Coventry & Warwickshire (2); West Midlands - Birmingham & Solihull (2); Berkshire (2) |
| Employment Support / Careers | 36 | 0 | 36 | 16 | 1.0 | 1 | 1 | 2 | London (13); Wales - Mid (2); Hampshire (2); Cornwall (2); Yorkshire - North (2) |
| Security / Emergency Services | 18 | 0 | 18 | 8 | 1.0 | 1 | 0 | 2 | London (5); Hampshire (4); Bristol & Bath (2); Greater Manchester - South (1); Cambridgeshire (1) |
| Hospitality / Catering | 16 | 0 | 16 | 8 | 1.0 | 1 | 0 | 0 | London (5); Gloucestershire (4); Oxfordshire (2); Essex (1); Lincolnshire (1) |
| Science / Laboratory | 15 | 0 | 15 | 8 | 1.0 | 0 | 0 | 3 | Gloucestershire (3); London (2); Oxfordshire (2); Worcestershire (1); Kent (1) |
| Manufacturing / Production | 13 | 0 | 13 | 11 | 1 | 0 | 0 | 1 | Worcestershire (2); Norfolk (1); Hampshire (1); Suffolk (1); North East - Tyneside, Wearside & Northumberland (1) |
| Cleaning / Domestic / Facilities | 10 | 0 | 10 | 7 | 1 | 0 | 0 | 1 | Northamptonshire (2); Hertfordshire (2); Dorset (1); London (1); Essex (1) |
| Agriculture / Environment | 10 | 0 | 10 | 5 | 2 | 0 | 0 | 1 | Cheshire - Warrington & Halton (3); London (2); Kent (2); Oxfordshire (1); Devon (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 5,947 |
| still_unclassified | 1,423 |
| title_rule_pass2 | 1,422 |
| existing_register:admin_service | 431 |
| existing_register:finance_accounts | 223 |
| existing_register:customer_service_contact_centre | 164 |
| description_majority | 155 |
| existing_register:hr_recruitment | 122 |
| existing_register:support_worker | 110 |
| existing_register:warehouse_logistics | 3 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 9 | Sub Agent |
| 6 | Functional Specialist |
| 6 | Contracts Manager |
| 6 | Technical Manager |
| 6 | Social Impact & Community Enterprise Manager (Food Insecurity) - 6m FTC |
| 6 | Technical Lead |
| 6 | Theatre Scrub Practitioner - RN/ODP |
| 5 | Implementation Consultant |
| 5 | Tenancy Sustainment Officer |
| 5 | People Business Partner |
| 5 | Bid Manager |
| 5 | General Foreman |
| 4 | Transaction Manager |
| 4 | Insolvency Manager |
| 4 | Productivity Manager |
| 4 | Planner |
| 4 | Pensions Lead |
| 3 | Property Valuer |
| 3 | Psychology Graduate |
| 3 | Senior Planner |
| 3 | Executive Search Consultant |
| 3 | Customer Representative Field Based |
| 3 | Senior Authorised Person |
| 3 | Technical Director |
| 3 | Media Measurement Lead |
| 3 | Property Officer |
| 3 | Installer Development Representative |
| 3 | Project Director |
| 3 | IT Manager |
| 3 | Aftersales Manager |
| 3 | Wealth Planner |
| 3 | Cost Manager |
| 3 | Case Manager |
| 3 | Research Officer |
| 3 | Remote Online Paid Research Panelist (Part-Time) - Data Entry Clerk Welcome |
| 3 | Personal Lines Account Handler |
| 3 | Development Executive |
| 2 | Commercial Director |
| 2 | Treasurer |
| 2 | Principal Commercial Officer |
| 2 | Property Portfolio Manager |
| 2 | Business Advisory |
| 2 | NCR Facilitator |
| 2 | Protection Advisor |
| 2 | Senior Quality Practitioner |
| 2 | Debt Advice Caseworker |
| 2 | Vulnerability Researcher |
| 2 | Senior Reward Analyst |
| 2 | SEMH Mentor |
| 2 | Placement & Brokerage Officer |
| 2 | Mammographer |
| 2 | Marine Sub Agent |
| 2 | Senior Analyst |
| 2 | Hire Desk Manager |
| 2 | Design Director |
| 2 | M&E Commercial Director |
| 2 | Corporate Senior Associate |
| 2 | Regional Quality/Safety Lead |
| 2 | Senior Land Acquisition Manager |
| 2 | Housing Options Officer (temp: North London) |
| 2 | Tribunal Advocate |
| 2 | Associate Associate Director - Town Planning |
| 2 | Architectural Technologist |
| 2 | Senior Cost Consultant |
| 2 | Aspiring Child Counsellor |
| 2 | Health & Social Care Assessor |
| 2 | Framework Manager |
| 2 | Head of Reward |
| 2 | Commercial Business Partner |
| 2 | Private Client Director |
| 2 | Chief Financial Officer |
| 2 | Telehandler |
| 2 | Stock Condition Manager |
| 2 | HSE Advisor |
| 2 | Dementia Adviser |
