# JobG8 operational 33-region density

Feed: `2026-08-18.xlsx`
Operational footprint: **33 England regions** from `pipeline/config/job_slice_catalog.json`, with `Northern Ireland - East` explicitly excluded to match the daily regional overview.
North East geo sub-clusters are collapsed to the single operational `North East` region.
Median is calculated across **all 33 operational regions, including zeroes**.

| Broad family | Total feed | In 33 regions | Existing register in 33 | New / uncovered in 33 | Populated /33 | Median /33 | Regions 5+ | Regions 10+ | Outside 33 | Geo unknown | Top operational regions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Admin / Customer Service | 1,703 | 1,081 | 481 | 600 | 33 | 21 | 30 | 30 | 345 | 277 | London (248); North East (83); Surrey (60); Hampshire (57); Kent (46) |
| Professional Finance / Accountancy | 1,114 | 808 | 136 | 672 | 32 | 17 | 30 | 25 | 249 | 57 | London (201); Bristol & Bath (45); Yorkshire - West (39); Greater Manchester - Manchester & Salford (36); Oxfordshire (33) |
| Sales / Business Development | 809 | 497 | 0 | 497 | 31 | 11 | 29 | 19 | 244 | 68 | London (101); North East (32); Hampshire (31); Kent (28); Yorkshire - West (24) |
| Healthcare / Clinical | 701 | 489 | 0 | 489 | 33 | 9 | 27 | 16 | 127 | 85 | London (124); Sussex (34); Hampshire (32); North East (26); Surrey (26) |
| Legal / Conveyancing | 686 | 501 | 0 | 501 | 30 | 8 | 25 | 15 | 162 | 23 | London (142); Greater Manchester - Manchester & Salford (42); Essex (42); Sussex (24); West Midlands - Birmingham & Solihull (24) |
| Care / Support Work | 431 | 286 | 120 | 166 | 33 | 7 | 23 | 8 | 97 | 48 | London (40); Hampshire (29); North East (24); Sussex (19); Surrey (13) |
| HR / Recruitment | 410 | 295 | 93 | 202 | 33 | 6 | 24 | 10 | 72 | 43 | London (67); Hampshire (21); Bristol & Bath (21); Nottinghamshire (12); Greater Manchester - Manchester & Salford (11) |
| Management / Team Leadership | 398 | 255 | 0 | 255 | 32 | 6 | 22 | 8 | 111 | 32 | London (24); North East (21); Kent (17); Oxfordshire (16); Hampshire (14) |
| Engineering / Technical | 309 | 220 | 0 | 220 | 31 | 5 | 17 | 6 | 58 | 31 | London (42); Bristol & Bath (13); Cumbria - South (12); Greater Manchester - Manchester & Salford (12); Hampshire (11) |
| IT / Data / Software | 306 | 233 | 0 | 233 | 31 | 3 | 14 | 7 | 56 | 17 | London (71); Hampshire (21); Bristol & Bath (17); Greater Manchester - Manchester & Salford (13); North East (13) |
| Market Research / Field Interviewing | 235 | 80 | 0 | 80 | 20 | 1 | 5 | 2 | 78 | 77 | London (23); Wiltshire (10); Berkshire (6); Gloucestershire (6); Devon (6) |
| Financial Advice / Mortgages | 232 | 173 | 0 | 173 | 28 | 5 | 17 | 5 | 52 | 7 | London (22); Bristol & Bath (14); Yorkshire - West (12); Cambridgeshire (11); Berkshire (10) |
| Marketing / Digital / Creative | 227 | 170 | 0 | 170 | 28 | 3 | 8 | 3 | 35 | 22 | London (70); Greater Manchester - Manchester & Salford (10); Surrey (10); West Midlands - Birmingham & Solihull (7); Yorkshire - North (5) |
| Retail / Store | 201 | 120 | 0 | 120 | 28 | 3 | 10 | 3 | 58 | 23 | London (18); Yorkshire - North (11); Wiltshire (10); Yorkshire - West (7); Greater Manchester - Manchester & Salford (7) |
| Insurance / Claims | 135 | 110 | 0 | 110 | 22 | 1 | 7 | 2 | 13 | 12 | London (44); Yorkshire - West (11); North East (6); West Midlands - Birmingham & Solihull (6); Greater Manchester - Manchester & Salford (5) |
| Construction / Trades / Property | 134 | 99 | 0 | 99 | 24 | 2 | 6 | 1 | 25 | 10 | London (28); Greater Manchester - Manchester & Salford (6); Essex (6); Nottinghamshire (5); Kent (5) |
| Operations / General Management | 107 | 79 | 0 | 79 | 25 | 2 | 3 | 1 | 17 | 11 | London (20); Devon (6); Hampshire (5); Surrey (4); Berkshire (4) |
| Property / Housing / Planning | 73 | 48 | 0 | 48 | 22 | 1 | 1 | 1 | 13 | 12 | London (17); Sussex (4); Nottinghamshire (3); Buckinghamshire (2); Cumbria - North (2) |
| Procurement / Buying / Supply Chain | 61 | 42 | 0 | 42 | 20 | 1 | 2 | 0 | 9 | 10 | London (8); Essex (5); Kent (4); Berkshire (4); Yorkshire - West (2) |
| Compliance / Risk / Quality | 58 | 51 | 0 | 51 | 16 | 0 | 1 | 1 | 4 | 3 | London (20); Cambridgeshire (4); Berkshire (3); Greater Manchester - Manchester & Salford (3); Wiltshire (3) |
| Education / Teaching | 56 | 44 | 0 | 44 | 17 | 1 | 3 | 1 | 4 | 8 | London (11); Sussex (6); Cumbria - South (6); Lancashire - North (4); Wiltshire (3) |
| Driving / Warehouse / Logistics | 41 | 28 | 2 | 26 | 17 | 1 | 1 | 0 | 7 | 6 | London (5); North East (3); Essex (2); Sussex (2); West Midlands - Coventry & Warwickshire (2) |
| Charity / Fundraising / Community | 38 | 31 | 0 | 31 | 13 | 0 | 1 | 1 | 3 | 4 | London (14); Buckinghamshire (3); Yorkshire - West (2); Hampshire (2); Surrey (2) |
| Employment Support / Careers | 32 | 21 | 0 | 21 | 10 | 0 | 1 | 0 | 9 | 2 | London (7); Hampshire (3); Surrey (2); Yorkshire - West (2); North East (2) |
| Science / Laboratory | 24 | 16 | 0 | 16 | 9 | 0 | 0 | 0 | 5 | 3 | London (4); Gloucestershire (3); Kent (2); Bristol & Bath (2); Yorkshire - West (1) |
| Hospitality / Catering | 23 | 19 | 0 | 19 | 8 | 0 | 1 | 0 | 3 | 1 | Gloucestershire (5); London (4); Norfolk (3); Oxfordshire (2); Staffordshire (2) |
| Cleaning / Domestic / Facilities | 16 | 12 | 0 | 12 | 7 | 0 | 0 | 0 | 4 | 0 | Northamptonshire (4); Hertfordshire (2); London (2); Yorkshire - North (1); Dorset (1) |
| Manufacturing / Production | 14 | 7 | 0 | 7 | 6 | 0 | 0 | 0 | 5 | 2 | Wiltshire (2); Norfolk (1); Hampshire (1); London (1); North East (1) |
| Security / Emergency Services | 13 | 10 | 0 | 10 | 5 | 0 | 0 | 0 | 1 | 2 | Hampshire (3); London (3); Bristol & Bath (2); Greater Manchester - South (1); Cambridgeshire (1) |
| Agriculture / Environment | 10 | 6 | 0 | 6 | 4 | 0 | 0 | 0 | 2 | 2 | London (2); Kent (2); Oxfordshire (1); Devon (1) |
