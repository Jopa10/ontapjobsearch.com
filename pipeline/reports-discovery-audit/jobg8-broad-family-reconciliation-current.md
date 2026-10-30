# JobG8 register-first broad-family reconciliation

Jobs reconciled: **20,000**
Jobs assigned first from an existing selected Ontap register: **1,828**
Original title-rule Other / Unclassified: **5,526**
Jobs resolved by description-majority pass: **337**
Remaining Other / Unclassified after register-first + title + description passes: **3,231**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Other / Unclassified | 3,231 | 16.2% |
| Professional Finance / Accountancy | 2,828 | 14.1% |
| Sales / Business Development | 2,339 | 11.7% |
| Admin / Customer Service | 2,239 | 11.2% |
| Legal / Conveyancing | 1,631 | 8.2% |
| HR / Recruitment | 1,108 | 5.5% |
| IT / Data / Software | 927 | 4.6% |
| Engineering / Technical | 735 | 3.7% |
| Driving / Warehouse / Logistics | 634 | 3.2% |
| Marketing / Digital / Creative | 574 | 2.9% |
| Construction / Trades / Property | 522 | 2.6% |
| Education / Teaching | 509 | 2.5% |
| Care / Support Work | 487 | 2.4% |
| Insurance / Claims | 466 | 2.3% |
| Healthcare / Clinical | 325 | 1.6% |
| Management / Team Leadership | 269 | 1.3% |
| Property / Housing / Planning | 243 | 1.2% |
| Operations / General Management | 204 | 1.0% |
| Compliance / Risk / Quality | 182 | 0.9% |
| Charity / Fundraising / Community | 123 | 0.6% |
| Procurement / Buying / Supply Chain | 115 | 0.6% |
| Financial Advice / Mortgages | 112 | 0.6% |
| Security / Emergency Services | 55 | 0.3% |
| Employment Support / Careers | 37 | 0.2% |
| Retail / Store | 35 | 0.2% |
| Cleaning / Domestic / Facilities | 28 | 0.1% |
| Manufacturing / Production | 16 | 0.1% |
| Hospitality / Catering | 15 | 0.1% |
| Market Research / Field Interviewing | 8 | 0.0% |
| Agriculture / Environment | 2 | 0.0% |
| Science / Laboratory | 1 | 0.0% |
| **TOTAL** | **20,000** | **100.0%** |

## Refined family totals by salary band

Salary uses the midpoint of the available structured minimum/maximum after annualising hourly, daily, weekly or monthly amounts. Five-figure values are treated as annual even when the source period is inconsistent. The first column combines genuinely sub-£20k jobs with missing or unusable salary so every family reconciles exactly to its total.

| Broad family | Below £20k / unknown | £20k–<£35k | £35k–£45k | Over £45k | Total |
|---|---:|---:|---:|---:|---:|
| Other / Unclassified | 1,691 | 555 | 347 | 638 | 3,231 |
| Professional Finance / Accountancy | 968 | 648 | 443 | 769 | 2,828 |
| Sales / Business Development | 568 | 583 | 465 | 723 | 2,339 |
| Admin / Customer Service | 499 | 1,369 | 289 | 82 | 2,239 |
| Legal / Conveyancing | 1,003 | 164 | 115 | 349 | 1,631 |
| HR / Recruitment | 235 | 409 | 286 | 178 | 1,108 |
| IT / Data / Software | 529 | 39 | 78 | 281 | 927 |
| Engineering / Technical | 291 | 107 | 126 | 211 | 735 |
| Driving / Warehouse / Logistics | 176 | 276 | 131 | 51 | 634 |
| Marketing / Digital / Creative | 216 | 108 | 125 | 125 | 574 |
| Construction / Trades / Property | 155 | 114 | 129 | 124 | 522 |
| Education / Teaching | 295 | 60 | 65 | 89 | 509 |
| Care / Support Work | 137 | 240 | 57 | 53 | 487 |
| Insurance / Claims | 265 | 35 | 66 | 100 | 466 |
| Healthcare / Clinical | 81 | 61 | 59 | 124 | 325 |
| Management / Team Leadership | 64 | 55 | 63 | 87 | 269 |
| Property / Housing / Planning | 48 | 38 | 78 | 79 | 243 |
| Operations / General Management | 92 | 7 | 29 | 76 | 204 |
| Compliance / Risk / Quality | 71 | 19 | 24 | 68 | 182 |
| Charity / Fundraising / Community | 87 | 19 | 12 | 5 | 123 |
| Procurement / Buying / Supply Chain | 38 | 44 | 15 | 18 | 115 |
| Financial Advice / Mortgages | 12 | 29 | 34 | 37 | 112 |
| Security / Emergency Services | 19 | 14 | 8 | 14 | 55 |
| Employment Support / Careers | 3 | 28 | 6 | 0 | 37 |
| Retail / Store | 27 | 6 | 0 | 2 | 35 |
| Cleaning / Domestic / Facilities | 8 | 18 | 2 | 0 | 28 |
| Manufacturing / Production | 6 | 3 | 3 | 4 | 16 |
| Hospitality / Catering | 6 | 7 | 1 | 1 | 15 |
| Market Research / Field Interviewing | 1 | 2 | 0 | 5 | 8 |
| Agriculture / Environment | 0 | 2 | 0 | 0 | 2 |
| Science / Laboratory | 1 | 0 | 0 | 0 | 1 |
| **TOTAL** | **7,592** | **5,059** | **3,056** | **4,293** | **20,000** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Professional Finance / Accountancy | 2,828 | 575 | 2,253 | 91 | 14 | 66 | 51 | 417 | London (552); Hampshire (112); Surrey (88); Berkshire (76); Hertfordshire (73) |
| Sales / Business Development | 2,339 | 0 | 2,339 | 82 | 9.5 | 54 | 41 | 482 | London (600); Berkshire (80); Hampshire (71); Hertfordshire (53); Bristol & Bath (51) |
| Admin / Customer Service | 2,239 | 923 | 1,316 | 84 | 12.0 | 58 | 45 | 451 | London (493); Surrey (71); Hampshire (64); Hertfordshire (62); Kent (52) |
| Legal / Conveyancing | 1,631 | 0 | 1,631 | 76 | 11.0 | 54 | 41 | 95 | London (292); Greater Manchester - Manchester & Salford (88); Surrey (62); Sussex (53); Yorkshire - West (52) |
| HR / Recruitment | 1,108 | 139 | 969 | 75 | 5 | 38 | 30 | 241 | London (292); Hampshire (37); Devon (27); Bristol & Bath (27); Berkshire (23) |
| IT / Data / Software | 927 | 0 | 927 | 63 | 7 | 38 | 22 | 108 | London (243); Hampshire (44); Berkshire (36); Bristol & Bath (36); Greater Manchester - Manchester & Salford (28) |
| Engineering / Technical | 735 | 0 | 735 | 73 | 4 | 33 | 20 | 130 | London (172); Bristol & Bath (25); Hampshire (22); Berkshire (19); Oxfordshire (17) |
| Driving / Warehouse / Logistics | 634 | 13 | 621 | 68 | 4.5 | 34 | 14 | 171 | London (60); Hampshire (25); Kent (24); Northamptonshire (19); Leicestershire (18) |
| Marketing / Digital / Creative | 574 | 0 | 574 | 55 | 4 | 24 | 17 | 79 | London (179); Nottinghamshire (19); Greater Manchester - Manchester & Salford (18); Berkshire (17); Sussex (16) |
| Construction / Trades / Property | 522 | 0 | 522 | 60 | 2.5 | 21 | 9 | 60 | London (184); Essex (28); Hampshire (17); Berkshire (14); Sussex (14) |
| Education / Teaching | 509 | 0 | 509 | 57 | 3 | 24 | 7 | 147 | London (91); Gloucestershire (29); Bristol & Bath (16); Sussex (15); Hertfordshire (14) |
| Care / Support Work | 487 | 178 | 309 | 67 | 3 | 19 | 10 | 121 | London (72); Hampshire (28); Sussex (27); Devon (14); Kent (14) |
| Insurance / Claims | 466 | 0 | 466 | 52 | 4.0 | 23 | 9 | 45 | London (103); Yorkshire - West (28); Greater Manchester - Manchester & Salford (28); Essex (19); West Midlands - Birmingham & Solihull (19) |
| Healthcare / Clinical | 325 | 0 | 325 | 53 | 3 | 15 | 5 | 73 | London (58); Bristol & Bath (17); Essex (13); Berkshire (12); Surrey (10) |
| Management / Team Leadership | 269 | 0 | 269 | 56 | 2.0 | 11 | 3 | 37 | London (68); Sussex (14); Hampshire (12); Yorkshire - West (7); Devon (7) |
| Property / Housing / Planning | 243 | 0 | 243 | 46 | 2.0 | 11 | 3 | 38 | London (68); Kent (12); Essex (10); Gloucestershire (8); Cambridgeshire (7) |
| Operations / General Management | 204 | 0 | 204 | 39 | 2 | 8 | 2 | 33 | London (69); Hampshire (11); Bristol & Bath (8); Berkshire (7); Devon (6) |
| Compliance / Risk / Quality | 182 | 0 | 182 | 41 | 2 | 6 | 1 | 29 | London (61); Essex (7); North East - Tyneside, Wearside & Northumberland (7); Sussex (6); Hampshire (6) |
| Charity / Fundraising / Community | 123 | 0 | 123 | 36 | 1.0 | 4 | 1 | 20 | London (35); Bedfordshire (6); Hampshire (5); Yorkshire - West (5); Shropshire (4) |
| Procurement / Buying / Supply Chain | 115 | 0 | 115 | 35 | 2 | 3 | 1 | 21 | London (21); Hertfordshire (8); Kent (5); Essex (4); Gloucestershire (4) |
| Financial Advice / Mortgages | 112 | 0 | 112 | 38 | 1.0 | 5 | 1 | 21 | London (17); Surrey (8); Kent (6); Hampshire (6); Yorkshire - West (5) |
| Security / Emergency Services | 55 | 0 | 55 | 21 | 1 | 1 | 1 | 11 | London (15); Sussex (3); Berkshire (3); Hampshire (3); Wiltshire (2) |
| Employment Support / Careers | 37 | 0 | 37 | 15 | 1 | 1 | 0 | 14 | London (8); North East - County Durham & Darlington/Hartlepool (2); Northamptonshire (1); Kent (1); Lincolnshire (1) |
| Retail / Store | 35 | 0 | 35 | 18 | 1.0 | 1 | 0 | 3 | London (9); Scotland Central - Edinburgh & Lothians (3); Surrey (2); Hertfordshire (2); North East - Tyneside, Wearside & Northumberland (2) |
| Cleaning / Domestic / Facilities | 28 | 0 | 28 | 17 | 1 | 1 | 0 | 4 | London (7); Essex (2); Hampshire (1); West Midlands (1); Merseyside - Wirral (1) |
| Manufacturing / Production | 16 | 0 | 16 | 12 | 1.0 | 0 | 0 | 2 | Nottinghamshire (2); London (2); Greater Manchester - Manchester & Salford (1); Suffolk (1); Shropshire (1) |
| Hospitality / Catering | 15 | 0 | 15 | 6 | 1.0 | 1 | 0 | 3 | London (6); Cambridgeshire (2); Hampshire (1); Northamptonshire (1); Scotland Central - Falkirk & Stirling (1) |
| Market Research / Field Interviewing | 8 | 0 | 8 | 6 | 1.0 | 0 | 0 | 1 | London (2); Monmouthshire (1); North Wales - East (1); Wales South - Gwent (1); Wiltshire (1) |
| Agriculture / Environment | 2 | 0 | 2 | 1 | 2 | 0 | 0 | 0 | Shropshire (2) |
| Science / Laboratory | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | Hertfordshire (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 12,868 |
| still_unclassified | 3,231 |
| title_rule_pass2 | 1,736 |
| existing_register:admin_service | 629 |
| existing_register:finance_accounts | 575 |
| description_majority | 337 |
| existing_register:customer_service_contact_centre | 294 |
| existing_register:support_worker | 178 |
| existing_register:hr_recruitment | 139 |
| existing_register:warehouse_logistics | 13 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 26 | Disability Assessor |
| 17 | Corporate Associate |
| 15 | Pitch Executive |
| 15 | Pitch Executive (5.00pm - 1:30am) |
| 14 | Associate - Corporate |
| 14 | Associate - disputes |
| 13 | Account Handler |
| 13 | Disputes Associate |
| 12 | Estate Planning Consultant |
| 12 | Property Lister |
| 10 | Neighbourhood Officer |
| 10 | SOC Analyst Programme |
| 8 | Sports Coach |
| 8 | Transaction Manager |
| 8 | Occupational Health Advisor |
| 8 | Partnership Executive |
| 7 | Customer Relations Manager |
| 7 | CRM Manager |
| 7 | Repairs Planner |
| 7 | Change Manager |
| 6 | Customer Consultant |
| 6 | Senior Manager |
| 6 | ER Specialist |
| 6 | Estates Manager |
| 6 | Operations Assistant |
| 6 | Territory Representative |
| 6 | Repairs Manager |
| 6 | People Business Partner |
| 5 | Block Manager |
| 5 | Learning & Development Manager |
| 5 | Tenancy Sustainment Officer |
| 5 | Data Architect |
| 5 | Immigration Partner |
| 5 | Portfolio Analyst |
| 5 | Account Director |
| 5 | Business Change Manager |
| 5 | Early Years Educator |
| 5 | Nursery Manager |
| 5 | Business Intelligence Analyst |
| 5 | Customer Services Executive |
| 5 | Behaviour Mentor |
| 5 | Stores Operative |
| 5 | Project Support Officer |
| 5 | Lead Identity Manager |
| 5 | Recovery Worker (Drug and Alcohol) |
| 5 | Planner - Transportation |
| 4 | Revenue Controller |
| 4 | Nursery Practitioner |
| 4 | Estate Manager |
| 4 | Team Assistant |
| 4 | Bid Manager |
| 4 | Mentor / Coach |
| 4 | Head of Property |
| 4 | Chair of Trustees |
| 4 | Tax & Trusts Manager |
| 4 | HSE Advisor |
| 4 | Housing Options Officer |
| 4 | Resourcer |
| 4 | Facilities Officer |
| 4 | Activity Co-ordinator |
| 4 | Material Handler |
| 4 | National Account Director |
| 4 | Letting Negotiator |
| 4 | Corporate Producer |
| 4 | Trust Manager |
| 3 | Playworker |
| 3 | Senior Credit Controller |
| 3 | Customer Experience Manager |
| 3 | Senior Associate (Family Law) |
| 3 | Financial Analyst |
| 3 | Contract Manager |
| 3 | Sports Coach / TA |
| 3 | Philanthropy Manager |
| 3 | Paid Media Manager |
| 3 | Group Reporting Manager |
