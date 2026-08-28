# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **776**
Original title-rule Other / Unclassified: **3,508**
Jobs resolved by description-majority pass: **65**
Remaining Other / Unclassified after register-first + title + description passes: **1,893**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Other / Unclassified | 1,893 | 18.9% |
| Professional Finance / Accountancy | 1,113 | 11.1% |
| Sales / Business Development | 1,020 | 10.2% |
| Admin / Customer Service | 933 | 9.3% |
| IT / Data / Software | 831 | 8.3% |
| Healthcare / Clinical | 647 | 6.5% |
| Engineering / Technical | 493 | 4.9% |
| Management / Team Leadership | 466 | 4.7% |
| Marketing / Digital / Creative | 362 | 3.6% |
| Operations / General Management | 361 | 3.6% |
| Care / Support Work | 287 | 2.9% |
| HR / Recruitment | 237 | 2.4% |
| Legal / Conveyancing | 221 | 2.2% |
| Retail / Store | 209 | 2.1% |
| Market Research / Field Interviewing | 154 | 1.5% |
| Construction / Trades / Property | 135 | 1.4% |
| Property / Housing / Planning | 80 | 0.8% |
| Compliance / Risk / Quality | 71 | 0.7% |
| Financial Advice / Mortgages | 65 | 0.7% |
| Insurance / Claims | 65 | 0.7% |
| Education / Teaching | 60 | 0.6% |
| Procurement / Buying / Supply Chain | 57 | 0.6% |
| Driving / Warehouse / Logistics | 47 | 0.5% |
| Charity / Fundraising / Community | 46 | 0.5% |
| Security / Emergency Services | 31 | 0.3% |
| Hospitality / Catering | 27 | 0.3% |
| Employment Support / Careers | 21 | 0.2% |
| Manufacturing / Production | 21 | 0.2% |
| Cleaning / Domestic / Facilities | 19 | 0.2% |
| Science / Laboratory | 17 | 0.2% |
| Agriculture / Environment | 11 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Professional Finance / Accountancy | 1,113 | 239 | 874 | 79 | 10 | 54 | 40 | 72 | London (152); Yorkshire - West (52); Greater Manchester - Manchester & Salford (43); Leicestershire (39); Yorkshire - North (30) |
| Sales / Business Development | 1,020 | 0 | 1,020 | 82 | 7.0 | 53 | 30 | 77 | London (149); Greater Manchester - Manchester & Salford (54); Hampshire (44); Kent (34); Hertfordshire (32) |
| Admin / Customer Service | 933 | 352 | 581 | 80 | 5.0 | 41 | 25 | 172 | London (143); Surrey (48); Hampshire (34); Leicestershire (28); Kent (27) |
| IT / Data / Software | 831 | 0 | 831 | 65 | 5 | 35 | 20 | 67 | London (187); Hampshire (51); Greater Manchester - Manchester & Salford (51); Kent (49); Bristol & Bath (31) |
| Healthcare / Clinical | 647 | 0 | 647 | 79 | 4 | 34 | 16 | 67 | London (106); Hampshire (38); Surrey (31); Sussex (28); North East - Tyneside, Wearside & Northumberland (21) |
| Engineering / Technical | 493 | 0 | 493 | 63 | 4 | 29 | 12 | 38 | London (95); Kent (24); Greater Manchester - Manchester & Salford (22); Bristol & Bath (21); Hampshire (16) |
| Management / Team Leadership | 466 | 0 | 466 | 77 | 4 | 33 | 13 | 24 | London (41); Essex (20); Oxfordshire (18); Sussex (18); Hampshire (16) |
| Marketing / Digital / Creative | 362 | 0 | 362 | 58 | 3.0 | 19 | 4 | 33 | London (116); Greater Manchester - Manchester & Salford (19); Surrey (10); Yorkshire - West (10); Berkshire (8) |
| Operations / General Management | 361 | 0 | 361 | 61 | 3 | 24 | 9 | 35 | London (67); Yorkshire - West (14); Hampshire (13); West Midlands - Birmingham & Solihull (12); Hertfordshire (11) |
| Care / Support Work | 287 | 115 | 172 | 63 | 2 | 16 | 6 | 32 | London (35); Hampshire (17); Oxfordshire (13); Kent (13); Somerset (12) |
| HR / Recruitment | 237 | 67 | 170 | 48 | 3.0 | 13 | 3 | 34 | London (41); Bristol & Bath (21); Hampshire (12); Kent (7); Greater Manchester - Manchester & Salford (7) |
| Legal / Conveyancing | 221 | 0 | 221 | 51 | 2 | 11 | 2 | 9 | London (62); Greater Manchester - Manchester & Salford (11); West Midlands - Birmingham & Solihull (9); Bristol & Bath (8); Wiltshire (8) |
| Retail / Store | 209 | 0 | 209 | 57 | 2 | 8 | 3 | 28 | London (26); Yorkshire - North (14); Oxfordshire (11); Wiltshire (9); Cambridgeshire (9) |
| Market Research / Field Interviewing | 154 | 0 | 154 | 36 | 2.0 | 8 | 1 | 49 | Wiltshire (11); Devon (9); London (9); Scotland Central - Tayside (8); Berkshire (7) |
| Construction / Trades / Property | 135 | 0 | 135 | 42 | 2.0 | 5 | 1 | 14 | London (26); Greater Manchester - Manchester & Salford (7); Bristol & Bath (6); Hampshire (5); Dorset (5) |
| Property / Housing / Planning | 80 | 0 | 80 | 32 | 1.0 | 1 | 1 | 12 | London (10); Nottinghamshire (4); Sussex (4); West Midlands - Coventry & Warwickshire (4); Surrey (4) |
| Compliance / Risk / Quality | 71 | 0 | 71 | 27 | 1 | 2 | 1 | 4 | London (18); Greater Manchester - Manchester & Salford (6); Bristol & Bath (4); Cambridgeshire (3); West Midlands - Birmingham & Solihull (3) |
| Financial Advice / Mortgages | 65 | 0 | 65 | 31 | 2 | 1 | 0 | 3 | London (9); West Midlands - Birmingham & Solihull (4); Leicestershire (4); Bristol & Bath (3); Hampshire (3) |
| Insurance / Claims | 65 | 0 | 65 | 17 | 1 | 1 | 1 | 10 | London (30); Norfolk (3); Greater Manchester - Manchester & Salford (3); East Midlands (2); Staffordshire (2) |
| Education / Teaching | 60 | 0 | 60 | 20 | 1.0 | 2 | 1 | 10 | London (16); Cumbria - South (6); Lancashire - North (4); Sussex (3); Wiltshire (2) |
| Procurement / Buying / Supply Chain | 57 | 0 | 57 | 23 | 1 | 1 | 1 | 11 | London (14); Essex (3); Sussex (3); Derbyshire (2); Devon (2) |
| Driving / Warehouse / Logistics | 47 | 3 | 44 | 27 | 1 | 1 | 0 | 6 | London (7); West Midlands - Birmingham & Solihull (2); Leicestershire (2); Worcestershire (2); Staffordshire (2) |
| Charity / Fundraising / Community | 46 | 0 | 46 | 17 | 2 | 1 | 1 | 4 | London (15); Buckinghamshire (4); West Midlands - Birmingham & Solihull (3); Yorkshire - North (2); Hampshire (2) |
| Security / Emergency Services | 31 | 0 | 31 | 14 | 1.0 | 2 | 0 | 1 | London (7); Hampshire (6); Berkshire (3); Bristol & Bath (2); Nottinghamshire (2) |
| Hospitality / Catering | 27 | 0 | 27 | 10 | 2.0 | 1 | 0 | 4 | London (5); Lincolnshire (3); Norfolk (3); Gloucestershire (3); Oxfordshire (2) |
| Employment Support / Careers | 21 | 0 | 21 | 13 | 1 | 0 | 0 | 2 | London (3); Yorkshire - North (3); Bristol & Bath (3); Lancashire - Blackpool & Fylde (1); Wales - Mid (1) |
| Manufacturing / Production | 21 | 0 | 21 | 15 | 1 | 0 | 0 | 3 | Sussex (2); Yorkshire - West (2); London (2); Suffolk (1); Worcestershire (1) |
| Cleaning / Domestic / Facilities | 19 | 0 | 19 | 10 | 1.0 | 0 | 0 | 2 | Northamptonshire (4); Bristol & Bath (3); Wiltshire (2); Lincolnshire (2); London (1) |
| Science / Laboratory | 17 | 0 | 17 | 8 | 1.0 | 0 | 0 | 4 | Gloucestershire (3); London (3); Nottinghamshire (2); Worcestershire (1); Derbyshire (1) |
| Agriculture / Environment | 11 | 0 | 11 | 6 | 1.5 | 0 | 0 | 0 | London (3); Cheshire - Warrington & Halton (3); Kent (2); Devon (1); Gloucestershire (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 5,786 |
| still_unclassified | 1,893 |
| title_rule_pass2 | 1,480 |
| existing_register:admin_service | 259 |
| existing_register:finance_accounts | 239 |
| existing_register:support_worker | 115 |
| existing_register:customer_service_contact_centre | 93 |
| existing_register:hr_recruitment | 67 |
| description_majority | 65 |
| existing_register:warehouse_logistics | 3 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 13 | Contracts Manager |
| 9 | Sub Agent |
| 8 | Aftersales Manager |
| 8 | Technical Lead |
| 8 | Bid Manager |
| 6 | Client Relationship Manager |
| 6 | Tenancy Sustainment Officer |
| 6 | Autocentre Manager |
| 6 | Social Impact & Community Enterprise Manager (Food Insecurity) - 6m FTC |
| 6 | Service Delivery Manager |
| 6 | Contract Manager |
| 6 | Housing Estates Officer |
| 5 | Planner |
| 5 | Customer Relations Manager |
| 5 | Technical Manager |
| 5 | Ward Manager |
| 5 | Associate Director |
| 5 | Field Manager |
| 5 | Account Director |
| 4 | Insolvency Manager |
| 4 | Property Valuer |
| 4 | Shift Manager |
| 4 | Associate Director of Commercial Partnerships |
| 4 | Productivity Manager |
| 4 | Videographer |
| 4 | General Foreman |
| 4 | Contractual Advisor |
| 4 | Head Installer |
| 4 | Remote Game Tester |
| 4 | Senior User Researcher |
| 3 | Repairs Planner |
| 3 | Media Measurement Lead |
| 3 | Property Officer |
| 3 | Installer Development Representative |
| 3 | Hire Desk Manager |
| 3 | Senior Cost Consultant |
| 3 | Financial Analyst |
| 3 | Personal Banker |
| 3 | Senior Data Architect |
| 3 | Hairdresser |
| 3 | AI Governance Lead |
| 3 | Pre-reg 2027 |
| 3 | Partnerships Manager |
| 3 | Packaging Technologist |
| 3 | Cost & Productivity Manager (TMT) |
| 3 | ASB Officer |
| 3 | Development Manager |
| 3 | Technical Author |
| 3 | Development Executive |
| 3 | Team Manager |
| 3 | Therapy Assistant |
| 3 | IT Manager |
| 3 | Data Governance Analyst |
| 3 | Door to Door Canvasser |
| 3 | Paid Media Manager |
| 3 | Head of Customer Care |
| 3 | Subject Lead History and Politics |
| 3 | Insite Operations Support Manager |
| 2 | NCR Facilitator |
| 2 | Trainee Crewing and Travel Manager |
| 2 | Senior Analyst |
| 2 | Design Director |
| 2 | Corporate Senior Associate |
| 2 | Regional Quality/Safety Lead |
| 2 | Concession Manager |
| 2 | Senior Authorised Person |
| 2 | Senior Planner |
| 2 | Head of Planning |
| 2 | Architectural Technologist |
| 2 | Aspiring Child Counsellor |
| 2 | Stock Condition Manager |
| 2 | Cost Controller |
| 2 | Beauty Consultant |
| 2 | Cost Manager |
| 2 | Hire Desk Controller |
