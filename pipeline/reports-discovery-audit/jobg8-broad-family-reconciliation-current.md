# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **1,290**
Original title-rule Other / Unclassified: **3,188**
Jobs resolved by description-majority pass: **161**
Remaining Other / Unclassified after register-first + title + description passes: **1,403**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Admin / Customer Service | 1,703 | 17.0% |
| Other / Unclassified | 1,403 | 14.0% |
| Professional Finance / Accountancy | 1,114 | 11.1% |
| Sales / Business Development | 809 | 8.1% |
| Healthcare / Clinical | 701 | 7.0% |
| Legal / Conveyancing | 686 | 6.9% |
| Care / Support Work | 431 | 4.3% |
| HR / Recruitment | 410 | 4.1% |
| Management / Team Leadership | 398 | 4.0% |
| Engineering / Technical | 309 | 3.1% |
| IT / Data / Software | 306 | 3.1% |
| Market Research / Field Interviewing | 235 | 2.4% |
| Financial Advice / Mortgages | 232 | 2.3% |
| Marketing / Digital / Creative | 227 | 2.3% |
| Retail / Store | 201 | 2.0% |
| Insurance / Claims | 135 | 1.4% |
| Construction / Trades / Property | 134 | 1.3% |
| Operations / General Management | 107 | 1.1% |
| Property / Housing / Planning | 73 | 0.7% |
| Procurement / Buying / Supply Chain | 61 | 0.6% |
| Compliance / Risk / Quality | 58 | 0.6% |
| Education / Teaching | 56 | 0.6% |
| Driving / Warehouse / Logistics | 41 | 0.4% |
| Charity / Fundraising / Community | 38 | 0.4% |
| Employment Support / Careers | 32 | 0.3% |
| Science / Laboratory | 24 | 0.2% |
| Hospitality / Catering | 23 | 0.2% |
| Cleaning / Domestic / Facilities | 16 | 0.2% |
| Manufacturing / Production | 14 | 0.1% |
| Security / Emergency Services | 13 | 0.1% |
| Agriculture / Environment | 10 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Admin / Customer Service | 1,703 | 754 | 949 | 83 | 11 | 53 | 45 | 277 | London (248); North East - Tyneside, Wearside & Northumberland (67); Surrey (60); Hampshire (57); Kent (46) |
| Professional Finance / Accountancy | 1,114 | 221 | 893 | 78 | 8.5 | 51 | 36 | 57 | London (201); Bristol & Bath (45); Yorkshire - West (39); Greater Manchester - Manchester & Salford (36); Oxfordshire (33) |
| Sales / Business Development | 809 | 0 | 809 | 79 | 6 | 50 | 26 | 68 | London (101); Hampshire (31); Cheshire - Warrington & Halton (31); North East - Tyneside, Wearside & Northumberland (28); Kent (28) |
| Healthcare / Clinical | 701 | 0 | 701 | 81 | 4 | 36 | 17 | 85 | London (124); Sussex (34); Hampshire (32); Surrey (26); Essex (24) |
| Legal / Conveyancing | 686 | 0 | 686 | 66 | 5.0 | 38 | 17 | 23 | London (142); Greater Manchester - Manchester & Salford (42); Essex (42); Suffolk (30); Sussex (24) |
| Care / Support Work | 431 | 176 | 255 | 74 | 3.0 | 32 | 9 | 48 | London (40); Hampshire (29); Sussex (19); Surrey (13); Berkshire (12) |
| HR / Recruitment | 410 | 135 | 275 | 62 | 3.5 | 30 | 11 | 43 | London (67); Hampshire (21); Bristol & Bath (21); Nottinghamshire (12); Greater Manchester - Manchester & Salford (11) |
| Management / Team Leadership | 398 | 0 | 398 | 73 | 4 | 29 | 9 | 32 | London (24); Kent (17); Oxfordshire (16); Hampshire (14); Suffolk (12) |
| Engineering / Technical | 309 | 0 | 309 | 61 | 3 | 18 | 6 | 31 | London (42); Bristol & Bath (13); Cumbria - South (12); Greater Manchester - Manchester & Salford (12); Hampshire (11) |
| IT / Data / Software | 306 | 0 | 306 | 53 | 3 | 17 | 7 | 17 | London (71); Hampshire (21); Bristol & Bath (17); Greater Manchester - Manchester & Salford (13); Surrey (11) |
| Market Research / Field Interviewing | 235 | 0 | 235 | 42 | 2.0 | 9 | 4 | 77 | London (23); Worcestershire (18); Wiltshire (10); Herefordshire (10); Berkshire (6) |
| Financial Advice / Mortgages | 232 | 0 | 232 | 52 | 3.0 | 17 | 5 | 7 | London (22); Bristol & Bath (14); Yorkshire - West (12); Cambridgeshire (11); Berkshire (10) |
| Marketing / Digital / Creative | 227 | 0 | 227 | 48 | 2.0 | 8 | 3 | 22 | London (70); Greater Manchester - Manchester & Salford (10); Surrey (10); West Midlands - Birmingham & Solihull (7); Yorkshire - North (5) |
| Retail / Store | 201 | 0 | 201 | 65 | 1 | 11 | 3 | 23 | London (18); Yorkshire - North (11); Wiltshire (10); Yorkshire - West (7); Greater Manchester - Manchester & Salford (7) |
| Insurance / Claims | 135 | 0 | 135 | 29 | 2 | 7 | 2 | 12 | London (44); Yorkshire - West (11); West Midlands - Birmingham & Solihull (6); Greater Manchester - Manchester & Salford (5); Bristol & Bath (5) |
| Construction / Trades / Property | 134 | 0 | 134 | 41 | 2 | 6 | 1 | 10 | London (28); Greater Manchester - Manchester & Salford (6); Essex (6); Nottinghamshire (5); Kent (5) |
| Operations / General Management | 107 | 0 | 107 | 38 | 2.0 | 3 | 1 | 11 | London (20); Devon (6); Hampshire (5); Surrey (4); Berkshire (4) |
| Property / Housing / Planning | 73 | 0 | 73 | 32 | 1.0 | 1 | 1 | 12 | London (17); Sussex (4); Nottinghamshire (3); Shropshire (3); Buckinghamshire (2) |
| Procurement / Buying / Supply Chain | 61 | 0 | 61 | 28 | 1.0 | 2 | 0 | 10 | London (8); Essex (5); Kent (4); Berkshire (4); Yorkshire - West (2) |
| Compliance / Risk / Quality | 58 | 0 | 58 | 20 | 1.5 | 1 | 1 | 3 | London (20); Cambridgeshire (4); Berkshire (3); Greater Manchester - Manchester & Salford (3); Wiltshire (3) |
| Education / Teaching | 56 | 0 | 56 | 21 | 1 | 3 | 1 | 8 | London (11); Sussex (6); Cumbria - South (6); Lancashire - North (4); Wiltshire (3) |
| Driving / Warehouse / Logistics | 41 | 4 | 37 | 24 | 1.0 | 1 | 0 | 6 | London (5); Essex (2); Sussex (2); West Midlands - Coventry & Warwickshire (2); North East - County Durham & Darlington/Hartlepool (2) |
| Charity / Fundraising / Community | 38 | 0 | 38 | 16 | 1.0 | 1 | 1 | 4 | London (14); Buckinghamshire (3); Yorkshire - West (2); Hampshire (2); Surrey (2) |
| Employment Support / Careers | 32 | 0 | 32 | 17 | 1 | 1 | 0 | 2 | London (7); Hampshire (3); Lancashire - Central (2); Wales - Mid (2); Lancashire - Blackpool & Fylde (2) |
| Science / Laboratory | 24 | 0 | 24 | 14 | 1.0 | 0 | 0 | 3 | London (4); Gloucestershire (3); Kent (2); Bristol & Bath (2); Yorkshire - West (1) |
| Hospitality / Catering | 23 | 0 | 23 | 10 | 2.0 | 1 | 0 | 1 | Gloucestershire (5); London (4); Norfolk (3); Lincolnshire (2); Oxfordshire (2) |
| Cleaning / Domestic / Facilities | 16 | 0 | 16 | 10 | 1.0 | 0 | 0 | 0 | Northamptonshire (4); Lincolnshire (2); Hertfordshire (2); London (2); Yorkshire - North (1) |
| Manufacturing / Production | 14 | 0 | 14 | 10 | 1.0 | 0 | 0 | 2 | Worcestershire (2); Wiltshire (2); Norfolk (1); Hampshire (1); London (1) |
| Security / Emergency Services | 13 | 0 | 13 | 6 | 1.5 | 0 | 0 | 2 | Hampshire (3); London (3); Bristol & Bath (2); Greater Manchester - South (1); Cheshire - East (1) |
| Agriculture / Environment | 10 | 0 | 10 | 6 | 1.0 | 0 | 0 | 2 | London (2); Kent (2); Oxfordshire (1); Devon (1); Wales South - Cardiff & Vale (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 5,590 |
| title_rule_pass2 | 1,556 |
| still_unclassified | 1,403 |
| existing_register:admin_service | 433 |
| existing_register:customer_service_contact_centre | 321 |
| existing_register:finance_accounts | 221 |
| existing_register:support_worker | 176 |
| description_majority | 161 |
| existing_register:hr_recruitment | 135 |
| existing_register:warehouse_logistics | 4 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 9 | Transaction Manager |
| 9 | Sub Agent |
| 9 | Technical Manager |
| 5 | Contracts Manager |
| 5 | Implementation Consultant |
| 4 | Functional Specialist |
| 4 | Customer Representative Field Based |
| 4 | Commissioning Manager |
| 4 | Contract Manager |
| 4 | Pensions Lead |
| 3 | Associate Director |
| 3 | Account Director |
| 3 | Psychology Graduate |
| 3 | Senior Planner |
| 3 | Executive Search Consultant |
| 3 | Final Mile Territory Manager |
| 3 | Installer Development Representative |
| 3 | Project Director |
| 3 | Productivity Manager |
| 3 | Framework Manager |
| 3 | Insolvency Manager |
| 3 | Telehandler |
| 2 | Enablement Support Officer - Housing |
| 2 | Commercial Assistant |
| 2 | Commercial Director |
| 2 | Protection adviser |
| 2 | Treasurer |
| 2 | Senior ICM Modeller - Flood Risk |
| 2 | Housing Options Officer |
| 2 | Information Governance Manager |
| 2 | Property Valuer |
| 2 | Principal Commercial Officer |
| 2 | Repairs Planner |
| 2 | Property Portfolio Manager |
| 2 | Business Advisory |
| 2 | NCR Facilitator |
| 2 | Principal Consultant |
| 2 | Protection Advisor |
| 2 | Senior Quality Practitioner |
| 2 | Senior Authorised Person |
| 2 | Debt Advice Caseworker |
| 2 | Portfolio Manager |
| 2 | Vulnerability Researcher |
| 2 | Technical Director |
| 2 | Senior Specification Technologist |
| 2 | Croupier |
| 2 | SEMH Mentor |
| 2 | Placement & Brokerage Officer |
| 2 | Mammographer |
| 2 | Dementia Adviser |
| 2 | Property Officer |
| 2 | Data Quality Advisor |
| 2 | Marine Sub Agent |
| 2 | Operations Assistant |
| 2 | Learning & Development Specialist |
| 2 | Lead Contract Support and Performance Manager |
| 2 | Hire Desk Manager |
| 2 | Design Director |
| 2 | Shift Leader |
| 2 | M&E Commercial Director |
| 2 | Corporate Senior Associate |
| 2 | Regional Quality/Safety Lead |
| 2 | Technical Advisor |
| 2 | Vehicle Recovery Lead |
| 2 | Service Lead |
| 2 | Senior Land Acquisition Manager |
| 2 | Reward Analyst |
| 2 | Senior Compensation Analyst |
| 2 | Housing Options Officer (temp: North London) |
| 2 | Tribunal Advocate |
| 2 | Associate Associate Director - Town Planning |
| 2 | Tenancy Sustainment Officer |
| 2 | Architectural Technologist |
| 2 | Learning & Development Partner |
| 2 | Aftersales Manager |
