# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **1,132**
Original title-rule Other / Unclassified: **3,028**
Jobs resolved by description-majority pass: **153**
Remaining Other / Unclassified after register-first + title + description passes: **1,406**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Admin / Customer Service | 1,560 | 15.6% |
| Other / Unclassified | 1,406 | 14.1% |
| Professional Finance / Accountancy | 1,248 | 12.5% |
| Sales / Business Development | 898 | 9.0% |
| Legal / Conveyancing | 817 | 8.2% |
| Healthcare / Clinical | 565 | 5.7% |
| HR / Recruitment | 479 | 4.8% |
| Management / Team Leadership | 360 | 3.6% |
| IT / Data / Software | 360 | 3.6% |
| Care / Support Work | 331 | 3.3% |
| Engineering / Technical | 310 | 3.1% |
| Financial Advice / Mortgages | 227 | 2.3% |
| Marketing / Digital / Creative | 219 | 2.2% |
| Retail / Store | 208 | 2.1% |
| Market Research / Field Interviewing | 158 | 1.6% |
| Construction / Trades / Property | 142 | 1.4% |
| Insurance / Claims | 137 | 1.4% |
| Operations / General Management | 114 | 1.1% |
| Property / Housing / Planning | 79 | 0.8% |
| Procurement / Buying / Supply Chain | 64 | 0.6% |
| Compliance / Risk / Quality | 63 | 0.6% |
| Education / Teaching | 60 | 0.6% |
| Charity / Fundraising / Community | 43 | 0.4% |
| Driving / Warehouse / Logistics | 42 | 0.4% |
| Employment Support / Careers | 32 | 0.3% |
| Hospitality / Catering | 19 | 0.2% |
| Science / Laboratory | 15 | 0.1% |
| Security / Emergency Services | 15 | 0.1% |
| Agriculture / Environment | 10 | 0.1% |
| Manufacturing / Production | 10 | 0.1% |
| Cleaning / Domestic / Facilities | 9 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Admin / Customer Service | 1,560 | 679 | 881 | 85 | 8 | 53 | 40 | 248 | London (241); Surrey (74); North East - Tyneside, Wearside & Northumberland (57); Hampshire (53); Kent (41) |
| Professional Finance / Accountancy | 1,248 | 220 | 1,028 | 78 | 11.0 | 54 | 42 | 65 | London (182); Bristol & Bath (48); Yorkshire - West (41); Devon (39); Sussex (39) |
| Sales / Business Development | 898 | 0 | 898 | 77 | 7 | 50 | 26 | 74 | London (128); North East - Tyneside, Wearside & Northumberland (70); Hampshire (34); Kent (26); Yorkshire - West (25) |
| Legal / Conveyancing | 817 | 0 | 817 | 65 | 5 | 33 | 21 | 23 | London (162); Essex (67); Suffolk (64); Norfolk (39); Yorkshire - West (31) |
| Healthcare / Clinical | 565 | 0 | 565 | 78 | 4.0 | 31 | 13 | 54 | London (83); Hampshire (31); Sussex (29); Surrey (23); North East - Tyneside, Wearside & Northumberland (18) |
| HR / Recruitment | 479 | 119 | 360 | 62 | 4.0 | 29 | 14 | 46 | London (71); Bristol & Bath (25); Hampshire (22); Yorkshire - West (17); Berkshire (15) |
| Management / Team Leadership | 360 | 0 | 360 | 74 | 3.0 | 26 | 7 | 30 | London (23); Oxfordshire (19); Kent (16); Hampshire (13); Sussex (12) |
| IT / Data / Software | 360 | 0 | 360 | 55 | 3 | 19 | 6 | 31 | London (73); Hampshire (39); Bristol & Bath (20); Gloucestershire (15); Greater Manchester - Manchester & Salford (13) |
| Care / Support Work | 331 | 111 | 220 | 68 | 2.5 | 19 | 4 | 34 | London (34); Hampshire (25); Sussex (17); Surrey (13); Greater Manchester - Manchester & Salford (9) |
| Engineering / Technical | 310 | 0 | 310 | 59 | 3 | 22 | 7 | 27 | London (41); Bristol & Bath (16); Hertfordshire (11); Gloucestershire (10); Sussex (10) |
| Financial Advice / Mortgages | 227 | 0 | 227 | 54 | 3.0 | 16 | 5 | 6 | London (21); Bristol & Bath (13); Hampshire (11); Essex (11); Yorkshire - West (11) |
| Marketing / Digital / Creative | 219 | 0 | 219 | 51 | 2 | 9 | 2 | 26 | London (62); Surrey (10); Greater Manchester - Manchester & Salford (9); Kent (8); Yorkshire - North (7) |
| Retail / Store | 208 | 0 | 208 | 61 | 2 | 10 | 2 | 25 | London (17); Yorkshire - North (12); Greater Manchester - Manchester & Salford (9); Wiltshire (8); Oxfordshire (7) |
| Market Research / Field Interviewing | 158 | 0 | 158 | 39 | 1 | 8 | 2 | 51 | Wiltshire (12); London (11); Worcestershire (9); North Scotland (6); Northamptonshire (5) |
| Construction / Trades / Property | 142 | 0 | 142 | 42 | 2.0 | 7 | 1 | 9 | London (27); Greater Manchester - Manchester & Salford (9); Cambridgeshire (7); Essex (6); Kent (5) |
| Insurance / Claims | 137 | 0 | 137 | 31 | 2 | 4 | 1 | 12 | London (43); Yorkshire - West (9); Merseyside - Liverpool (8); Essex (7); Norfolk (4) |
| Operations / General Management | 114 | 0 | 114 | 41 | 1 | 6 | 1 | 11 | London (22); Oxfordshire (8); Hampshire (7); Devon (6); Essex (5) |
| Property / Housing / Planning | 79 | 0 | 79 | 35 | 1 | 1 | 1 | 10 | London (13); Sussex (4); Hertfordshire (4); Cumbria - North (3); Nottinghamshire (3) |
| Procurement / Buying / Supply Chain | 64 | 0 | 64 | 27 | 2 | 2 | 0 | 12 | London (8); Essex (5); Derbyshire (3); Surrey (3); Yorkshire - West (2) |
| Compliance / Risk / Quality | 63 | 0 | 63 | 24 | 1.0 | 1 | 1 | 5 | London (18); Cambridgeshire (4); Scotland Central - Edinburgh & Lothians (4); Wiltshire (3); Bristol & Bath (3) |
| Education / Teaching | 60 | 0 | 60 | 23 | 1 | 3 | 1 | 8 | London (12); Cumbria - South (6); Sussex (5); Lancashire - North (4); Wiltshire (3) |
| Charity / Fundraising / Community | 43 | 0 | 43 | 17 | 1 | 1 | 1 | 4 | London (14); Buckinghamshire (4); Surrey (3); Yorkshire - West (2); Hampshire (2) |
| Driving / Warehouse / Logistics | 42 | 3 | 39 | 26 | 1.0 | 1 | 0 | 5 | London (5); Kent (2); West Midlands - Coventry & Warwickshire (2); West Midlands - Birmingham & Solihull (2); Berkshire (2) |
| Employment Support / Careers | 32 | 0 | 32 | 15 | 1 | 1 | 1 | 2 | London (12); Wales - Mid (2); Hampshire (2); Cornwall (2); Yorkshire - North (2) |
| Hospitality / Catering | 19 | 0 | 19 | 9 | 1 | 1 | 0 | 0 | London (6); Gloucestershire (4); Lincolnshire (2); Oxfordshire (2); Essex (1) |
| Science / Laboratory | 15 | 0 | 15 | 9 | 1 | 0 | 0 | 3 | Gloucestershire (3); Oxfordshire (2); Worcestershire (1); Kent (1); London (1) |
| Security / Emergency Services | 15 | 0 | 15 | 7 | 1 | 0 | 0 | 2 | London (4); Hampshire (3); Bristol & Bath (2); Greater Manchester - South (1); Cambridgeshire (1) |
| Agriculture / Environment | 10 | 0 | 10 | 5 | 2 | 0 | 0 | 2 | London (2); Kent (2); Cheshire - Warrington & Halton (2); Oxfordshire (1); Devon (1) |
| Manufacturing / Production | 10 | 0 | 10 | 8 | 1.0 | 0 | 0 | 1 | Worcestershire (2); Norfolk (1); Hampshire (1); Suffolk (1); North East - Tyneside, Wearside & Northumberland (1) |
| Cleaning / Domestic / Facilities | 9 | 0 | 9 | 6 | 1.0 | 0 | 0 | 1 | Northamptonshire (2); Hertfordshire (2); Dorset (1); London (1); Essex (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 5,902 |
| title_rule_pass2 | 1,407 |
| still_unclassified | 1,406 |
| existing_register:admin_service | 429 |
| existing_register:customer_service_contact_centre | 250 |
| existing_register:finance_accounts | 220 |
| description_majority | 153 |
| existing_register:hr_recruitment | 119 |
| existing_register:support_worker | 111 |
| existing_register:warehouse_logistics | 3 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 9 | Sub Agent |
| 6 | Functional Specialist |
| 6 | Technical Manager |
| 6 | Social Impact & Community Enterprise Manager (Food Insecurity) - 6m FTC |
| 6 | Technical Lead |
| 6 | Theatre Scrub Practitioner - RN/ODP |
| 5 | Contracts Manager |
| 5 | Implementation Consultant |
| 5 | Tenancy Sustainment Officer |
| 5 | People Business Partner |
| 5 | Bid Manager |
| 5 | General Foreman |
| 4 | Transaction Manager |
| 4 | Productivity Manager |
| 4 | Pensions Lead |
| 3 | Property Valuer |
| 3 | Psychology Graduate |
| 3 | Senior Planner |
| 3 | Executive Search Consultant |
| 3 | Customer Representative Field Based |
| 3 | Media Measurement Lead |
| 3 | Property Officer |
| 3 | Installer Development Representative |
| 3 | Project Director |
| 3 | Insolvency Manager |
| 3 | Dementia Adviser |
| 3 | Planner |
| 3 | Cost Manager |
| 3 | Case Manager |
| 3 | Research Officer |
| 3 | Maths Graduate |
| 3 | Remote Online Paid Research Panelist (Part-Time) - Data Entry Clerk Welcome |
| 3 | Associate Director of Commercial Partnerships |
| 3 | Personal Lines Account Handler |
| 3 | Virtual Assistant (Remote, UK- Based) |
| 2 | Commercial Director |
| 2 | Treasurer |
| 2 | Principal Commercial Officer |
| 2 | Property Portfolio Manager |
| 2 | Business Advisory |
| 2 | NCR Facilitator |
| 2 | Protection Advisor |
| 2 | Senior Quality Practitioner |
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
| 2 | Telehandler |
