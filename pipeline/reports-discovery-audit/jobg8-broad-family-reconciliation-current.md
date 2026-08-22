# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **1,117**
Original title-rule Other / Unclassified: **3,067**
Jobs resolved by description-majority pass: **160**
Remaining Other / Unclassified after register-first + title + description passes: **1,422**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Admin / Customer Service | 1,557 | 15.6% |
| Other / Unclassified | 1,422 | 14.2% |
| Professional Finance / Accountancy | 1,239 | 12.4% |
| Sales / Business Development | 892 | 8.9% |
| Legal / Conveyancing | 808 | 8.1% |
| Healthcare / Clinical | 564 | 5.6% |
| HR / Recruitment | 480 | 4.8% |
| Management / Team Leadership | 363 | 3.6% |
| IT / Data / Software | 356 | 3.6% |
| Care / Support Work | 335 | 3.4% |
| Engineering / Technical | 303 | 3.0% |
| Marketing / Digital / Creative | 226 | 2.3% |
| Financial Advice / Mortgages | 224 | 2.2% |
| Retail / Store | 215 | 2.1% |
| Market Research / Field Interviewing | 160 | 1.6% |
| Construction / Trades / Property | 141 | 1.4% |
| Insurance / Claims | 137 | 1.4% |
| Operations / General Management | 114 | 1.1% |
| Property / Housing / Planning | 80 | 0.8% |
| Compliance / Risk / Quality | 64 | 0.6% |
| Procurement / Buying / Supply Chain | 63 | 0.6% |
| Education / Teaching | 60 | 0.6% |
| Charity / Fundraising / Community | 43 | 0.4% |
| Driving / Warehouse / Logistics | 40 | 0.4% |
| Employment Support / Careers | 32 | 0.3% |
| Hospitality / Catering | 21 | 0.2% |
| Security / Emergency Services | 15 | 0.1% |
| Science / Laboratory | 14 | 0.1% |
| Manufacturing / Production | 13 | 0.1% |
| Agriculture / Environment | 10 | 0.1% |
| Cleaning / Domestic / Facilities | 9 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Admin / Customer Service | 1,557 | 667 | 890 | 85 | 9 | 53 | 39 | 247 | London (240); Surrey (76); North East - Tyneside, Wearside & Northumberland (57); Hampshire (53); Kent (40) |
| Professional Finance / Accountancy | 1,239 | 218 | 1,021 | 78 | 10.5 | 53 | 42 | 64 | London (183); Bristol & Bath (46); Yorkshire - West (40); Devon (39); Greater Manchester - Manchester & Salford (37) |
| Sales / Business Development | 892 | 0 | 892 | 76 | 7.5 | 50 | 30 | 73 | London (124); North East - Tyneside, Wearside & Northumberland (70); Hampshire (35); Kent (26); Yorkshire - West (24) |
| Legal / Conveyancing | 808 | 0 | 808 | 65 | 5 | 35 | 20 | 23 | London (164); Essex (62); Suffolk (58); Norfolk (33); Yorkshire - West (31) |
| Healthcare / Clinical | 564 | 0 | 564 | 78 | 4.0 | 32 | 13 | 52 | London (81); Hampshire (31); Sussex (29); Surrey (22); North East - Tyneside, Wearside & Northumberland (19) |
| HR / Recruitment | 480 | 119 | 361 | 62 | 4.0 | 29 | 14 | 47 | London (72); Bristol & Bath (26); Hampshire (22); Yorkshire - West (17); Berkshire (15) |
| Management / Team Leadership | 363 | 0 | 363 | 74 | 3.0 | 28 | 7 | 29 | London (24); Oxfordshire (18); Kent (17); Hampshire (13); Sussex (11) |
| IT / Data / Software | 356 | 0 | 356 | 55 | 3 | 19 | 6 | 30 | London (70); Hampshire (39); Bristol & Bath (20); Gloucestershire (15); Greater Manchester - Manchester & Salford (13) |
| Care / Support Work | 335 | 110 | 225 | 68 | 3.0 | 20 | 4 | 35 | London (34); Hampshire (25); Sussex (16); Surrey (13); Somerset (9) |
| Engineering / Technical | 303 | 0 | 303 | 59 | 3 | 22 | 7 | 25 | London (40); Bristol & Bath (17); Greater Manchester - Manchester & Salford (11); Hampshire (11); Gloucestershire (10) |
| Marketing / Digital / Creative | 226 | 0 | 226 | 51 | 2 | 8 | 3 | 27 | London (66); Surrey (10); Greater Manchester - Manchester & Salford (10); Kent (8); Yorkshire - North (7) |
| Financial Advice / Mortgages | 224 | 0 | 224 | 54 | 2.5 | 16 | 5 | 6 | London (22); Bristol & Bath (13); Hampshire (11); Yorkshire - West (11); Essex (10) |
| Retail / Store | 215 | 0 | 215 | 63 | 2 | 10 | 3 | 25 | London (16); Yorkshire - North (13); Greater Manchester - Manchester & Salford (10); Wiltshire (8); Oxfordshire (7) |
| Market Research / Field Interviewing | 160 | 0 | 160 | 40 | 1.0 | 7 | 3 | 52 | London (11); Wiltshire (11); Worcestershire (10); Northamptonshire (5); Dorset (5) |
| Construction / Trades / Property | 141 | 0 | 141 | 42 | 2.0 | 7 | 1 | 9 | London (28); Greater Manchester - Manchester & Salford (9); Cambridgeshire (7); Kent (5); Bristol & Bath (5) |
| Insurance / Claims | 137 | 0 | 137 | 30 | 2.5 | 4 | 1 | 11 | London (45); Yorkshire - West (9); Merseyside - Liverpool (8); Essex (6); Norfolk (4) |
| Operations / General Management | 114 | 0 | 114 | 42 | 1.0 | 6 | 1 | 12 | London (22); Oxfordshire (7); Hampshire (7); Devon (6); Essex (5) |
| Property / Housing / Planning | 80 | 0 | 80 | 36 | 1.0 | 1 | 1 | 10 | London (13); Sussex (4); Hertfordshire (4); Cumbria - North (3); Nottinghamshire (3) |
| Compliance / Risk / Quality | 64 | 0 | 64 | 24 | 1.0 | 1 | 1 | 5 | London (19); Cambridgeshire (4); Scotland Central - Edinburgh & Lothians (4); Wiltshire (3); Bristol & Bath (3) |
| Procurement / Buying / Supply Chain | 63 | 0 | 63 | 27 | 2 | 2 | 0 | 11 | London (8); Essex (5); Derbyshire (3); Surrey (3); Yorkshire - West (2) |
| Education / Teaching | 60 | 0 | 60 | 22 | 1.0 | 3 | 1 | 8 | London (13); Cumbria - South (6); Sussex (5); Lancashire - North (4); Wiltshire (3) |
| Charity / Fundraising / Community | 43 | 0 | 43 | 18 | 1.0 | 1 | 1 | 4 | London (14); Buckinghamshire (4); Surrey (3); Yorkshire - West (2); Hampshire (2) |
| Driving / Warehouse / Logistics | 40 | 3 | 37 | 26 | 1.0 | 1 | 0 | 4 | London (5); Kent (2); West Midlands - Coventry & Warwickshire (2); West Midlands - Birmingham & Solihull (2); Berkshire (2) |
| Employment Support / Careers | 32 | 0 | 32 | 15 | 1 | 1 | 1 | 2 | London (12); Wales - Mid (2); Hampshire (2); Cornwall (2); Cheshire - East (2) |
| Hospitality / Catering | 21 | 0 | 21 | 9 | 1 | 1 | 0 | 0 | London (8); Gloucestershire (4); Lincolnshire (2); Oxfordshire (2); Essex (1) |
| Security / Emergency Services | 15 | 0 | 15 | 7 | 1 | 0 | 0 | 2 | London (4); Hampshire (3); Bristol & Bath (2); Greater Manchester - South (1); Cambridgeshire (1) |
| Science / Laboratory | 14 | 0 | 14 | 9 | 1 | 0 | 0 | 3 | Gloucestershire (3); Worcestershire (1); Kent (1); London (1); Hampshire (1) |
| Manufacturing / Production | 13 | 0 | 13 | 10 | 1.0 | 0 | 0 | 1 | Worcestershire (2); Wiltshire (2); Norfolk (1); Hampshire (1); London (1) |
| Agriculture / Environment | 10 | 0 | 10 | 5 | 2 | 0 | 0 | 2 | London (2); Kent (2); Cheshire - Warrington & Halton (2); Oxfordshire (1); Devon (1) |
| Cleaning / Domestic / Facilities | 9 | 0 | 9 | 6 | 1.0 | 0 | 0 | 1 | Northamptonshire (2); Hertfordshire (2); Dorset (1); London (1); Essex (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 5,877 |
| title_rule_pass2 | 1,424 |
| still_unclassified | 1,422 |
| existing_register:admin_service | 422 |
| existing_register:customer_service_contact_centre | 245 |
| existing_register:finance_accounts | 218 |
| description_majority | 160 |
| existing_register:hr_recruitment | 119 |
| existing_register:support_worker | 110 |
| existing_register:warehouse_logistics | 3 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 8 | Sub Agent |
| 6 | Functional Specialist |
| 6 | Technical Manager |
| 6 | Social Impact & Community Enterprise Manager (Food Insecurity) - 6m FTC |
| 6 | Technical Lead |
| 5 | Contracts Manager |
| 5 | Implementation Consultant |
| 5 | Tenancy Sustainment Officer |
| 5 | People Business Partner |
| 5 | Theatre Scrub Practitioner - RN/ODP |
| 4 | Transaction Manager |
| 4 | Customer Representative Field Based |
| 4 | Productivity Manager |
| 4 | Bid Manager |
| 4 | Pensions Lead |
| 4 | Virtual Assistant (Remote, UK- Based) |
| 3 | Property Valuer |
| 3 | Psychology Graduate |
| 3 | Senior Planner |
| 3 | Executive Search Consultant |
| 3 | Media Measurement Lead |
| 3 | Property Officer |
| 3 | Installer Development Representative |
| 3 | Project Director |
| 3 | Insolvency Manager |
| 3 | Dementia Adviser |
| 3 | Planner |
| 3 | Case Manager |
| 3 | General Foreman |
| 3 | Research Officer |
| 3 | Maths Graduate |
| 3 | Freelance Interpreter |
| 3 | Remote Online Paid Research Panelist (Part-Time) - Data Entry Clerk Welcome |
| 3 | Associate Director of Commercial Partnerships |
| 3 | Personal Lines Account Handler |
| 2 | Commercial Director |
| 2 | Treasurer |
| 2 | Principal Commercial Officer |
| 2 | Repairs Planner |
| 2 | Property Portfolio Manager |
| 2 | Business Advisory |
| 2 | NCR Facilitator |
| 2 | Principal Consultant |
| 2 | Protection Advisor |
| 2 | Senior Authorised Person |
| 2 | Debt Advice Caseworker |
| 2 | Vulnerability Researcher |
| 2 | Technical Director |
| 2 | Final Mile Territory Manager |
| 2 | SEMH Mentor |
| 2 | Placement & Brokerage Officer |
| 2 | Mammographer |
| 2 | Marine Sub Agent |
| 2 | Senior Analyst |
| 2 | Hire Desk Manager |
| 2 | Design Director |
| 2 | IT Manager |
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
| 2 | Aftersales Manager |
| 2 | Head of Reward |
| 2 | Director of People and Culture - Salisbury - PT - Up to £66K |
| 2 | Commercial Business Partner |
| 2 | Private Client Director |
| 2 | Chief Financial Officer |
