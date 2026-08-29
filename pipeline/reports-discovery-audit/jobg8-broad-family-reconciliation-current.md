# JobG8 register-first broad-family reconciliation

Jobs reconciled: **10,000**
Jobs assigned first from an existing selected Ontap register: **684**
Original title-rule Other / Unclassified: **3,545**
Jobs resolved by description-majority pass: **72**
Remaining Other / Unclassified after register-first + title + description passes: **1,895**

Every job is counted once and only once. Existing selected Ontap registers take priority; then conservative title rules; descriptions are used only for unresolved titles with a clear majority signal. Diagnostic only: no publishing logic is changed.

## Refined family totals

| Broad family | Jobs | Share |
|---|---:|---:|
| Other / Unclassified | 1,895 | 18.9% |
| Sales / Business Development | 1,148 | 11.5% |
| IT / Data / Software | 1,012 | 10.1% |
| Admin / Customer Service | 931 | 9.3% |
| Professional Finance / Accountancy | 851 | 8.5% |
| Healthcare / Clinical | 689 | 6.9% |
| Engineering / Technical | 566 | 5.7% |
| Management / Team Leadership | 475 | 4.8% |
| Marketing / Digital / Creative | 300 | 3.0% |
| Care / Support Work | 290 | 2.9% |
| Operations / General Management | 286 | 2.9% |
| HR / Recruitment | 227 | 2.3% |
| Retail / Store | 206 | 2.1% |
| Legal / Conveyancing | 200 | 2.0% |
| Market Research / Field Interviewing | 167 | 1.7% |
| Construction / Trades / Property | 125 | 1.2% |
| Property / Housing / Planning | 78 | 0.8% |
| Financial Advice / Mortgages | 77 | 0.8% |
| Insurance / Claims | 68 | 0.7% |
| Compliance / Risk / Quality | 65 | 0.7% |
| Education / Teaching | 61 | 0.6% |
| Procurement / Buying / Supply Chain | 58 | 0.6% |
| Charity / Fundraising / Community | 41 | 0.4% |
| Security / Emergency Services | 41 | 0.4% |
| Driving / Warehouse / Logistics | 40 | 0.4% |
| Hospitality / Catering | 23 | 0.2% |
| Employment Support / Careers | 21 | 0.2% |
| Manufacturing / Production | 19 | 0.2% |
| Cleaning / Domestic / Facilities | 16 | 0.2% |
| Agriculture / Environment | 12 | 0.1% |
| Science / Laboratory | 12 | 0.1% |
| **TOTAL** | **10,000** | **100.0%** |

## Opportunity and Ontap-region density

Geography uses the same geo_lookup Area→Cluster and controlled LocationFallback logic as Ontap Module 2. Existing-register jobs are already selected by a current Ontap register. New/uncovered is diagnostic only.

| Broad family | Total | Existing register | New / uncovered | Ontap regions | Median / region | Regions 5+ | Regions 10+ | Geo unknown | Top regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Sales / Business Development | 1,148 | 0 | 1,148 | 82 | 8.0 | 59 | 33 | 87 | London (155); Greater Manchester - Manchester & Salford (52); Hampshire (46); Hertfordshire (39); Berkshire (35) |
| IT / Data / Software | 1,012 | 0 | 1,012 | 67 | 7 | 41 | 27 | 82 | London (214); Hampshire (61); Greater Manchester - Manchester & Salford (60); Kent (47); Bristol & Bath (44) |
| Admin / Customer Service | 931 | 343 | 588 | 77 | 5 | 43 | 25 | 169 | London (144); Surrey (45); Hampshire (34); Leicestershire (26); Kent (25) |
| Professional Finance / Accountancy | 851 | 147 | 704 | 79 | 8 | 49 | 29 | 68 | London (127); Yorkshire - West (35); Yorkshire - North (25); Merseyside - Liverpool (24); Bristol & Bath (22) |
| Healthcare / Clinical | 689 | 0 | 689 | 80 | 3.0 | 35 | 17 | 71 | London (117); Hampshire (39); Surrey (37); Sussex (34); North East - Tyneside, Wearside & Northumberland (24) |
| Engineering / Technical | 566 | 0 | 566 | 65 | 5 | 33 | 18 | 44 | London (95); Greater Manchester - Manchester & Salford (39); Kent (27); Bristol & Bath (26); Hampshire (15) |
| Management / Team Leadership | 475 | 0 | 475 | 77 | 4 | 35 | 16 | 22 | London (39); Oxfordshire (19); Sussex (19); Kent (19); Essex (19) |
| Marketing / Digital / Creative | 300 | 0 | 300 | 52 | 3.0 | 17 | 3 | 29 | London (87); Greater Manchester - Manchester & Salford (13); Hampshire (11); Surrey (9); Buckinghamshire (9) |
| Care / Support Work | 290 | 130 | 160 | 64 | 2.0 | 17 | 4 | 33 | London (41); Oxfordshire (18); Hampshire (15); Surrey (13); Wiltshire (9) |
| Operations / General Management | 286 | 0 | 286 | 53 | 3 | 18 | 4 | 18 | London (43); Oxfordshire (16); Bristol & Bath (13); Hampshire (13); Devon (9) |
| HR / Recruitment | 227 | 62 | 165 | 44 | 3.0 | 11 | 3 | 36 | London (34); Bristol & Bath (22); Hampshire (11); Yorkshire - West (9); Essex (7) |
| Retail / Store | 206 | 0 | 206 | 58 | 2.0 | 9 | 3 | 28 | London (22); Yorkshire - North (15); Oxfordshire (10); Wiltshire (9); Kent (9) |
| Legal / Conveyancing | 200 | 0 | 200 | 50 | 2.0 | 10 | 1 | 10 | London (58); Wiltshire (9); Yorkshire - South (8); Greater Manchester - Manchester & Salford (8); Sussex (7) |
| Market Research / Field Interviewing | 167 | 0 | 167 | 37 | 2 | 9 | 2 | 55 | Wiltshire (12); London (10); Devon (9); Scotland Central - Tayside (8); Berkshire (7) |
| Construction / Trades / Property | 125 | 0 | 125 | 40 | 2.0 | 4 | 1 | 12 | London (20); Cambridgeshire (5); Essex (5); Greater Manchester - Manchester & Salford (5); Yorkshire - North (4) |
| Property / Housing / Planning | 78 | 0 | 78 | 33 | 1 | 2 | 0 | 12 | London (9); Hertfordshire (5); Sussex (4); West Midlands - Coventry & Warwickshire (4); Surrey (4) |
| Financial Advice / Mortgages | 77 | 0 | 77 | 35 | 2 | 1 | 0 | 3 | London (8); Wiltshire (4); Leicestershire (4); Greater Manchester - Manchester & Salford (4); Surrey (3) |
| Insurance / Claims | 68 | 0 | 68 | 20 | 1.0 | 2 | 1 | 9 | London (27); Norfolk (5); Essex (3); West Midlands - Birmingham & Solihull (3); Greater Manchester - Manchester & Salford (3) |
| Compliance / Risk / Quality | 65 | 0 | 65 | 27 | 1 | 2 | 1 | 5 | London (14); Greater Manchester - Manchester & Salford (5); West Midlands - Birmingham & Solihull (4); Bristol & Bath (3); Cambridgeshire (3) |
| Education / Teaching | 61 | 0 | 61 | 22 | 1.0 | 2 | 1 | 9 | London (13); Cumbria - South (6); Lancashire - North (4); Wiltshire (3); Yorkshire - West (3) |
| Procurement / Buying / Supply Chain | 58 | 0 | 58 | 23 | 1 | 1 | 1 | 11 | London (13); Yorkshire - West (4); Essex (3); Devon (3); Hampshire (3) |
| Charity / Fundraising / Community | 41 | 0 | 41 | 16 | 2.0 | 1 | 1 | 4 | London (11); Buckinghamshire (4); West Midlands - Birmingham & Solihull (3); Yorkshire - North (2); Hampshire (2) |
| Security / Emergency Services | 41 | 0 | 41 | 14 | 1.0 | 2 | 0 | 10 | London (8); Hampshire (6); Bristol & Bath (3); Berkshire (3); Nottinghamshire (2) |
| Driving / Warehouse / Logistics | 40 | 2 | 38 | 27 | 1 | 0 | 0 | 5 | London (3); Leicestershire (2); Worcestershire (2); Staffordshire (2); Buckinghamshire (2) |
| Hospitality / Catering | 23 | 0 | 23 | 11 | 1 | 0 | 0 | 4 | London (4); Lincolnshire (3); Oxfordshire (2); Gloucestershire (2); Sussex (2) |
| Employment Support / Careers | 21 | 0 | 21 | 12 | 1.0 | 0 | 0 | 2 | London (3); Yorkshire - North (3); Bristol & Bath (3); Wales - Mid (2); Lancashire - Blackpool & Fylde (1) |
| Manufacturing / Production | 19 | 0 | 19 | 13 | 1 | 0 | 0 | 2 | London (3); Gloucestershire (2); Sussex (2); Suffolk (1); Worcestershire (1) |
| Cleaning / Domestic / Facilities | 16 | 0 | 16 | 10 | 1.0 | 0 | 0 | 3 | Northamptonshire (3); Bristol & Bath (2); London (1); Wiltshire (1); Yorkshire - South (1) |
| Agriculture / Environment | 12 | 0 | 12 | 7 | 2 | 0 | 0 | 0 | London (3); Cheshire - Warrington & Halton (2); Kent (2); Sussex (2); Devon (1) |
| Science / Laboratory | 12 | 0 | 12 | 6 | 1.0 | 0 | 0 | 3 | London (3); Gloucestershire (2); Worcestershire (1); West Midlands - Coventry & Warwickshire (1); Yorkshire - West (1) |

## Reconciliation basis

| Basis | Jobs |
|---|---:|
| title_rule_pass1 | 5,818 |
| still_unclassified | 1,895 |
| title_rule_pass2 | 1,531 |
| existing_register:admin_service | 251 |
| existing_register:finance_accounts | 147 |
| existing_register:support_worker | 130 |
| existing_register:customer_service_contact_centre | 92 |
| description_majority | 72 |
| existing_register:hr_recruitment | 62 |
| existing_register:warehouse_logistics | 2 |

## Largest titles still genuinely unclassified

| Count | Title |
|---:|---|
| 21 | Contracts Manager |
| 15 | Junior Network Analyst |
| 11 | Trainee Junior Network Consultant |
| 10 | Trainee Network Analyst |
| 10 | Customer Representative Field Based |
| 9 | Sub Agent |
| 8 | Associate Director |
| 7 | Aftersales Manager |
| 7 | Technical Lead |
| 7 | Bid Manager |
| 6 | Client Relationship Manager |
| 6 | Customer Relations Manager |
| 6 | Contract Manager |
| 6 | Autocentre Manager |
| 6 | Social Impact & Community Enterprise Manager (Food Insecurity) - 6m FTC |
| 6 | Door to Door Canvasser |
| 6 | Housing Estates Officer |
| 5 | Tenancy Sustainment Officer |
| 5 | Planner |
| 5 | Ward Manager |
| 5 | Productivity Manager |
| 5 | General Foreman |
| 5 | Implementation Consultant |
| 4 | Insolvency Manager |
| 4 | Property Valuer |
| 4 | Head of IT |
| 4 | Shift Manager |
| 4 | Partnerships Manager |
| 4 | Remote Game Tester |
| 4 | Cost & Productivity - Senior Manager |
| 4 | Contractual Advisor |
| 4 | Head Installer |
| 4 | Subject Lead History and Politics |
| 3 | Property Officer |
| 3 | Installer Development Representative |
| 3 | Development Manager |
| 3 | Senior Cost Consultant |
| 3 | Senior Authorised Person |
| 3 | Head of Planning |
| 3 | Team Manager |
| 3 | Technical Manager |
| 3 | Hairdresser |
| 3 | Senior Contracts Manager |
| 3 | Pre-reg 2027 |
| 3 | Partnership Manager |
| 3 | Associate Director of Commercial Partnerships |
| 3 | Packaging Technologist |
| 3 | Technical Director |
| 3 | Media Measurement Lead |
| 3 | Cost & Productivity Senior Manager |
| 3 | Cost & Productivity Manager (TMT) |
| 3 | ASB Officer |
| 3 | Applications Specialist, Cardiology IT / PACS Systems |
| 3 | Vulnerability Researcher |
| 3 | Account Director |
| 3 | Portfolio Manager |
| 3 | CRO Analyst |
| 3 | 2nd Line Support |
| 3 | Service Delivery Manager |
| 3 | Senior User Researcher |
| 3 | Butchery Manager |
| 3 | Head of Knowledge Management |
| 3 | F5 SME |
| 2 | Supported Living Manager |
| 2 | NCR Facilitator |
| 2 | Insight and Measurement Manager |
| 2 | Senior Analyst |
| 2 | Hire Desk Manager |
| 2 | Design Director |
| 2 | Corporate Senior Associate |
| 2 | Regional Quality/Safety Lead |
| 2 | Technical Advisor |
| 2 | Concession Manager |
| 2 | Senior Land Acquisition Manager |
| 2 | Senior Planner |
