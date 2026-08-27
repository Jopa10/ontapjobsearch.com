# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **821**
Original title-rule Other / Unclassified: **3,505**
Jobs resolved by description-majority pass: **64**
Remaining Other / Unclassified after register-first + title + description passes: **1,844**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Other / Unclassified | 1,844 | 18.4% |
| Professional Finance / Accountancy | 1,199 | 12.0% |
| Sales / Business Development | 997 | 10.0% |
| Admin / Customer Service | 967 | 9.7% |
| IT / Data / Software | 718 | 7.2% |
| Healthcare / Clinical | 703 | 7.0% |
| Management / Team Leadership | 503 | 5.0% |
| Engineering / Technical | 475 | 4.8% |
| Operations / General Management | 329 | 3.3% |
| Care / Support Work | 322 | 3.2% |
| Marketing / Digital / Creative | 299 | 3.0% |
| HR / Recruitment | 241 | 2.4% |
| Retail / Store | 224 | 2.2% |
| Legal / Conveyancing | 222 | 2.2% |
| Market Research / Field Interviewing | 154 | 1.5% |
| Construction / Trades / Property | 134 | 1.3% |
| Financial Advice / Mortgages | 83 | 0.8% |
| Property / Housing / Planning | 83 | 0.8% |
| Compliance / Risk / Quality | 74 | 0.7% |
| Insurance / Claims | 72 | 0.7% |
| Education / Teaching | 61 | 0.6% |
| Procurement / Buying / Supply Chain | 57 | 0.6% |
| Driving / Warehouse / Logistics | 47 | 0.5% |
| Charity / Fundraising / Community | 46 | 0.5% |
| Security / Emergency Services | 27 | 0.3% |
| Hospitality / Catering | 25 | 0.2% |
| Manufacturing / Production | 23 | 0.2% |
| Employment Support / Careers | 22 | 0.2% |
| Cleaning / Domestic / Facilities | 19 | 0.2% |
| Science / Laboratory | 18 | 0.2% |
| Agriculture / Environment | 12 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Professional Finance / Accountancy | 1,199 | 250 | 949 | 78 | 10.0 | 57 | 40 | 75 | London (151); Yorkshire - West (54); Greater Manchester - Manchester & Salford (50); Leicestershire (39); Yorkshire - North (38) |
| Sales / Business Development | 997 | 0 | 997 | 80 | 7.0 | 55 | 32 | 73 | London (146); Hampshire (41); Greater Manchester - Manchester & Salford (35); Kent (33); Hertfordshire (30) |
| Admin / Customer Service | 967 | 376 | 591 | 78 | 5.0 | 44 | 27 | 171 | London (150); Surrey (47); Hampshire (35); Kent (31); Leicestershire (31) |
| IT / Data / Software | 718 | 0 | 718 | 62 | 5.0 | 33 | 19 | 64 | London (145); Hampshire (50); Kent (43); Greater Manchester - Manchester & Salford (42); Scotland Central - Edinburgh & Lothians (26) |
| Healthcare / Clinical | 703 | 0 | 703 | 85 | 4 | 37 | 20 | 62 | London (104); Hampshire (36); Surrey (36); Sussex (29); North East - Tyneside, Wearside & Northumberland (22) |
| Management / Team Leadership | 503 | 0 | 503 | 82 | 4.0 | 38 | 16 | 26 | London (40); Oxfordshire (24); Sussex (19); Essex (19); Hampshire (18) |
| Engineering / Technical | 475 | 0 | 475 | 63 | 4 | 31 | 12 | 37 | London (78); Kent (25); Greater Manchester - Manchester & Salford (24); Bristol & Bath (20); Hertfordshire (16) |
| Operations / General Management | 329 | 0 | 329 | 61 | 3 | 22 | 7 | 32 | London (62); Yorkshire - West (12); Hampshire (11); Essex (10); Oxfordshire (10) |
| Care / Support Work | 322 | 126 | 196 | 64 | 3.0 | 19 | 7 | 32 | London (32); Hampshire (19); Oxfordshire (15); Somerset (14); Surrey (12) |
| Marketing / Digital / Creative | 299 | 0 | 299 | 54 | 3.0 | 11 | 4 | 31 | London (98); Greater Manchester - Manchester & Salford (17); Berkshire (10); Yorkshire - West (10); Surrey (9) |
| HR / Recruitment | 241 | 66 | 175 | 51 | 2 | 14 | 3 | 31 | London (37); Bristol & Bath (21); Hampshire (14); Kent (9); Yorkshire - West (7) |
| Retail / Store | 224 | 0 | 224 | 61 | 2 | 9 | 3 | 30 | London (28); Yorkshire - North (14); Oxfordshire (12); Wiltshire (9); Cambridgeshire (8) |
| Legal / Conveyancing | 222 | 0 | 222 | 50 | 2.0 | 11 | 2 | 11 | London (56); Greater Manchester - Manchester & Salford (10); Bristol & Bath (9); West Midlands - Birmingham & Solihull (9); Wiltshire (8) |
| Market Research / Field Interviewing | 154 | 0 | 154 | 36 | 2.0 | 8 | 1 | 49 | Wiltshire (11); Devon (9); London (9); Scotland Central - Tayside (8); Berkshire (7) |
| Construction / Trades / Property | 134 | 0 | 134 | 43 | 2 | 6 | 1 | 14 | London (23); Greater Manchester - Manchester & Salford (6); Bristol & Bath (5); Cambridgeshire (5); Essex (5) |
| Financial Advice / Mortgages | 83 | 0 | 83 | 35 | 2 | 2 | 1 | 4 | London (10); Leicestershire (5); West Midlands - Birmingham & Solihull (4); Wiltshire (4); Sussex (3) |
| Property / Housing / Planning | 83 | 0 | 83 | 34 | 1.0 | 2 | 1 | 12 | London (11); Sussex (6); West Midlands - Coventry & Warwickshire (4); Hertfordshire (4); Nottinghamshire (3) |
| Compliance / Risk / Quality | 74 | 0 | 74 | 28 | 1.0 | 2 | 1 | 4 | London (19); Greater Manchester - Manchester & Salford (5); Bristol & Bath (4); Scotland West - Glasgow (4); Hertfordshire (3) |
| Insurance / Claims | 72 | 0 | 72 | 19 | 1 | 2 | 1 | 10 | London (34); Norfolk (5); West Midlands - Birmingham & Solihull (3); East Midlands (2); Staffordshire (2) |
| Education / Teaching | 61 | 0 | 61 | 21 | 1 | 2 | 1 | 10 | London (16); Cumbria - South (6); Lancashire - North (4); Wiltshire (3); Sussex (3) |
| Procurement / Buying / Supply Chain | 57 | 0 | 57 | 24 | 1.0 | 1 | 1 | 11 | London (14); Essex (4); Derbyshire (2); Sussex (2); Devon (2) |
| Driving / Warehouse / Logistics | 47 | 3 | 44 | 27 | 1 | 1 | 0 | 5 | London (8); West Midlands - Birmingham & Solihull (2); West Midlands - Coventry & Warwickshire (2); Leicestershire (2); Staffordshire (2) |
| Charity / Fundraising / Community | 46 | 0 | 46 | 16 | 1.5 | 1 | 1 | 4 | London (17); Buckinghamshire (4); Surrey (3); Yorkshire - North (2); Hampshire (2) |
| Security / Emergency Services | 27 | 0 | 27 | 13 | 1 | 1 | 0 | 1 | Hampshire (7); London (4); Berkshire (3); Bristol & Bath (2); Nottinghamshire (2) |
| Hospitality / Catering | 25 | 0 | 25 | 8 | 2.0 | 2 | 0 | 2 | London (7); Gloucestershire (5); Norfolk (3); Lincolnshire (2); Oxfordshire (2) |
| Manufacturing / Production | 23 | 0 | 23 | 15 | 1 | 0 | 0 | 3 | Gloucestershire (2); Worcestershire (2); Sussex (2); Yorkshire - West (2); London (2) |
| Employment Support / Careers | 22 | 0 | 22 | 13 | 1 | 0 | 0 | 2 | London (4); Bristol & Bath (3); Wales - Mid (2); Yorkshire - North (2); Lancashire - Blackpool & Fylde (1) |
| Cleaning / Domestic / Facilities | 19 | 0 | 19 | 11 | 1 | 0 | 0 | 2 | Northamptonshire (4); Bedfordshire (2); Wiltshire (2); Bristol & Bath (2); Dorset (1) |
| Science / Laboratory | 18 | 0 | 18 | 10 | 1.0 | 0 | 0 | 5 | London (3); Gloucestershire (2); Worcestershire (1); Derbyshire (1); Nottinghamshire (1) |
| Agriculture / Environment | 12 | 0 | 12 | 7 | 1 | 0 | 0 | 1 | Cheshire - Warrington & Halton (3); London (2); Kent (2); Oxfordshire (1); Devon (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 5,748 |
| still_unclassified | 1,844 |
| title_rule_pass2 | 1,523 |
| existing_register:admin_service | 276 |
| existing_register:finance_accounts | 250 |
| existing_register:support_worker | 126 |
| existing_register:customer_service_contact_centre | 100 |
| existing_register:hr_recruitment | 66 |
| description_majority | 64 |
| existing_register:warehouse_logistics | 3 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 12 | Contracts Manager |
| 9 | Sub Agent |
| 8 | Technical Lead |
| 7 | Housing Estates Officer |
| 6 | Autocentre Manager |
| 6 | Functional Specialist |
| 6 | Bid Manager |
| 6 | Client Relationship Manager |
| 6 | Aftersales Manager |
| 6 | Social Impact & Community Enterprise Manager (Food Insecurity) - 6m FTC |
| 6 | Contract Manager |
| 5 | Productivity Manager |
| 5 | Tenancy Sustainment Officer |
| 5 | Planner |
| 5 | Technical Manager |
| 5 | Service Delivery Manager |
| 5 | Remote Game Tester |
| 5 | Senior User Researcher |
| 4 | Property Valuer |
| 4 | Butchery Manager |
| 4 | Customer Representative Field Based |
| 4 | Financial Analyst |
| 4 | Insolvency Manager |
| 4 | General Foreman |
| 4 | Associate Director |
| 4 | Associate Director of Commercial Partnerships |
| 4 | Contractual Advisor |
| 3 | Repairs Planner |
| 3 | Senior Planner |
| 3 | Executive Search Consultant |
| 3 | Senior Authorised Person |
| 3 | Vulnerability Researcher |
| 3 | Media Measurement Lead |
| 3 | Property Officer |
| 3 | Installer Development Representative |
| 3 | Hire Desk Manager |
| 3 | Senior Cost Consultant |
| 3 | Personal Banker |
| 3 | Senior Data Architect |
| 3 | Cost Controller |
| 3 | Customer Relations Manager |
| 3 | Beauty Consultant |
| 3 | Hairdresser |
| 3 | Senior Cost Manager |
| 3 | Ward Manager |
| 3 | Pre-reg 2027 |
| 3 | Cost & Productivity Manager |
| 3 | Field Manager |
| 3 | Partnerships Manager |
| 3 | Packaging Technologist |
| 3 | Cost & Productivity Manager (TMT) |
| 3 | Head Installer |
| 3 | Development Manager |
| 3 | Head of IT |
| 3 | Technical Author |
| 3 | Development Executive |
| 3 | Head of Commercial |
| 3 | Team Manager |
| 3 | Data Governance Analyst |
| 3 | Head of Customer Care |
| 3 | Technical Lead, Full Stack Java |
| 3 | Subject Lead History and Politics |
| 2 | Site Services Manager |
| 2 | Showroom Manager |
| 2 | Commercial Director |
| 2 | Transaction Manager |
| 2 | Passive Fire Manager |
| 2 | Shift Leader |
| 2 | Business Advisory |
| 2 | Senior Quality Practitioner |
| 2 | SEMH Mentor |
| 2 | NCR Facilitator |
| 2 | Trainee Crewing and Travel Manager |
| 2 | Final Mile Territory Manager |
| 2 | Senior Analyst |
