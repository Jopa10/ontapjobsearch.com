# North East Jobs ETL proof-of-concept review

review_date: 2026-07-29
review_fingerprint: 7cfdf9de38277b762e3f267917c70b702aa4a353b654345c2b3b7ca93b49d2da

Edit only the `action:` line in each editable block:

- For a POSS job, use `action: select` to add it or `action: exclude` to reject it.
- For a selected HC job, use `action: exclude` to remove it.
- Leave `action:` blank for no change.
- Commit the edit, then rerun the NEJobs process for the same review date.
- Decisions are matched by `source_job_id` and expire when the review date changes.

Run generated: 2026-07-29T13:37:22+01:00
RSS input: https://www.northeastjobs.org.uk/RSSJobs.aspx?orgid=62
JobG8 comparison rows in target geographies: 110

## Funnel

- RSS vacancies read: 649
- Hard-pass title/teaser screen before detail requests: 581
- Detail candidates: 68
- Detail failures or unavailable snapshots: 22
- Outside the two target geographies: 1
- Tees Valley explicitly excluded: 7
- Target-geography candidates reviewed: 38

## Detail diagnostics

- 299845 — PMO Secretariat: HTTPError
- 299778 — Early Help Administrator: HTTPError
- 299795 — Community Engagement Officer (Part Time): HTTPError
- 299809 — Application Support Officer (INTERNAL ONLY): HTTPError
- 299761 — DBS01116/26 - Admin Assistant - Hazlewood Community Primary School: HTTPError
- 299764 — 0.4 Lecturer Coordinator in Counselling & Psychotherapy Studies: HTTPError
- 299680 — Attendance Officer (Primary): HTTPError
- 299693 — Administration Assistant: HTTPError
- 299718 — Receptionist and Events Co-ordinator at the Sjovoll Centre: HTTPError
- 299563 — Administration Assistant - Conyers School (SPARK Education Trust): HTTPError
- 299556 — Fundraising & Partnerships Coordinator: HTTPError
- 299508 — Clerical Officer Receptionist: HTTPError
- 299480 — Administration Assistant: HTTPError
- 299408 — Tenant Engagement Officer: HTTPError
- 299411 — SEND Review Coordinator: HTTPError
- 299397 — Level 3 Academy Administrator Apprentice: HTTPError
- 299277 — Administrative Assistant: HTTPError
- 299075 — Attendance Administration Support Assistant: HTTPError
- 256120 — School Administrator: HTTPError
- 256122 — School Administrator: HTTPError
- 256125 — School Administrator: HTTPError
- 256126 — School Administrator: HTTPError

## Review outcomes

- HC: 11
- POSS: 27
- Hard pass: 0
- Final selected after manual actions: 11
- Final POSS awaiting decision: 27
- Manually excluded: 0
- Confirmed JobG8 duplicates: 0
- Possible JobG8 duplicates: 0
- Likely unique to North East Jobs: 38
- Rows in possible within-source duplicate groups: 2

## SELECTED

---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Town Hall | £25,583 per annum | Business Support Officer (Level 1)
employer: Darlington Borough Council
closing_date: 09/08/2026
reason: clear transferable title: business support officer
source_job_id: 299898
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Officer_Level_1/299898
---

---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Annfield Plain, Greencroft | Grade 3 £25,185 - £25,989 (Pay award pending) | Clerical Officer Receptionist
employer: Durham County Council
closing_date: 29/07/2026
reason: clear transferable title: receptionist, clerical
source_job_id: 299726
source_url: https://www.northeastjobs.org.uk/job/Clerical_Officer_Receptionist/299726
---

---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Highlight Active Wellbeing Hub | £13.47 per hour | Customer Service Advisor
employer: Hartlepool Borough Council
closing_date: 31/08/2026
reason: clear transferable title: customer service advisor
source_job_id: 299796
source_url: https://www.northeastjobs.org.uk/job/Customer_Service_Advisor/299796
---

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Northumberland County Council (derived for filtering) | £25,583 - 25,989 | Administration Assistant
employer: Northumberland County Council
closing_date: 31/07/2026 00:00
reason: clear transferable title: administration assistant
source_job_id: 300074
source_url: https://www.northeastjobs.org.uk/job/Administration_Assistant/300074
---

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | St Benet Biscop Catholic Academy, Ridge Terrace, Bedlington, NE22 6ED | £25,583 per annum pro rata, actual £22,533 per annum | Administration Assistant
employer: Bishop Bewick Catholic Education Trust
closing_date: 17/08/2026 12:00
reason: clear transferable title: administration assistant
source_job_id: 300098
source_url: https://www.northeastjobs.org.uk/job/Administration_Assistant/300098
---

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Newcastle Upon Tyne | £26,403 - £27,254 per annum, pay award pending; (actual salary £14,271 - £14,731) | Administrative Assistant
employer: Newcastle City Council
closing_date: 05/08/2026 22:59
reason: clear transferable title: administrative assistant
source_job_id: 300057
source_url: https://www.northeastjobs.org.uk/job/Administrative_Assistant/300057
---

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | North Tyneside | Grade 5 £26403 to £27254 per annum | Business Support Assistant
employer: North Tyneside Council
closing_date: 07/08/2026 00:00
reason: clear transferable title: business support assistant
source_job_id: 297597
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Assistant/297597
---

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Sunderland | £25948 - £25989 per annum pro rata | Business Support Assistant - Children's Social Care
employer: Together for Children - Sunderland
closing_date: 10/08/2026
reason: clear transferable title: business support assistant
source_job_id: 300179
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Assistant_Children_s_Social_Care/300179
---

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | South Tyneside Council (derived for filtering) | £28,598 pa pro rata | Business Support Officer, 32hpw
employer: South Tyneside Council
closing_date: 17/08/2026 12:00
reason: clear transferable title: business support officer
source_job_id: 300058
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Officer_32hpw/300058
---

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Newcastle upon Tyne | Salary from: £21,547.50 per annum | Receptionist & Administrator (HR / School)
employer: Talbot House Children's Charity
closing_date: 09/08/2026
reason: clear transferable title: administrator, receptionist
source_job_id: 299953
source_url: https://www.northeastjobs.org.uk/job/Receptionist_Administrator_HR_School/299953
---

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Studio West, West Denton Way, Newcastle upon Tyne, NE5 2SZ | £26,403 - £27,254 per annum. Actual Salary £19,324 - £19,947 per annum | Receptionist/Student Services
employer: Northern Leaders Trust
closing_date: 30/07/2026 09:00
reason: clear transferable title: receptionist
source_job_id: 299744
source_url: https://www.northeastjobs.org.uk/job/Receptionist_Student_Services/299744
---


## POSS — choose SELECT or EXCLUDE

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | The Horizon School, CETL, Brierton Lane, Hartlepool | Band 7 £23,175 - £24,314 pa | Attendance & Support Officer
employer: Hartlepool Borough Council
closing_date: 04/09/2026 12:00
reason: transferable office/service title with specialist or borderline wording: attendance
source_job_id: 299877
source_url: https://www.northeastjobs.org.uk/job/Attendance_Support_Officer/299877
---

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Darlington Borough Council (derived for filtering) | £25,989 per annum (pay award pending) | Events Assistant
employer: Darlington Borough Council
closing_date: 11/08/2026
reason: provisional transferable-office review
source_job_id: 300044
source_url: https://www.northeastjobs.org.uk/job/Events_Assistant/300044
---

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Barnard Castle | £27,128.40 | Facilities Coordinator
employer: The Bowes Museum
closing_date: 24/08/2026 08:00
reason: transferable office/service title with specialist or borderline wording: facilities
source_job_id: 300105
source_url: https://www.northeastjobs.org.uk/job/Facilities_Coordinator/300105
---

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Green Lane Council Offices, Spennymoor (Plus Hybrid Working) | Grade 9 £35,412 - £39,152 | Information Management and Data Services Officer
employer: Durham County Council
closing_date: 02/08/2026
reason: annualised upper salary £39,152 exceeds North East review point £30,000
source_job_id: 299570
source_url: https://www.northeastjobs.org.uk/job/Information_Management_and_Data_Services_Officer/299570
---

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Spectrum Business Park, Seaham (hybrid working options available) | Grade 7 £30,024 to £33,699 per annum (pay award pending) | Review Officer
employer: Durham County Council
closing_date: 09/08/2026
reason: annualised upper salary £33,699 exceeds North East review point £30,000
source_job_id: 298685
source_url: https://www.northeastjobs.org.uk/job/Review_Officer/298685
---

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Durham (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256127
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256127
---

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Bowlees Visitor Centre, Newbiggin | Grade 9 £35,412 - £39,152 (pro rata) | Visitor Services Officer
employer: Durham County Council
closing_date: 10/08/2026
reason: annualised upper salary £39,152 exceeds North East review point £30,000
source_job_id: 299897
source_url: https://www.northeastjobs.org.uk/job/Visitor_Services_Officer/299897
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle City Council (derived for filtering) | £26,403 - £27,254 per annum, pro rata (pay award pending) actual salary £14,271 - £14,731 | Administrative Assistant (HR)
employer: Newcastle City Council
closing_date: 09/08/2026 22:59
reason: transferable office/service title with specialist or borderline wording: hr
source_job_id: 300042
source_url: https://www.northeastjobs.org.uk/job/Administrative_Assistant_HR/300042
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Alnwick (derived for filtering) | Band 5 - £22,850 - £24,787 (being pro-rata of £28,598 - £31,022) | Attendance Officer
employer: The Duchess's Community High School
closing_date: 31/07/2026 12:00
reason: transferable office/service title with specialist or borderline wording: attendance
source_job_id: 299650
source_url: https://www.northeastjobs.org.uk/job/Attendance_Officer/299650
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland City Council (derived for filtering) | Grade 2 (SCP 5 - 6) £25,949 - £25,989 | Customer Enabling Services Support Assistant (Payroll)
employer: Sunderland City Council
closing_date: 06/09/2026
reason: transferable office/service title with specialist or borderline wording: payroll
source_job_id: 299864
source_url: https://www.northeastjobs.org.uk/job/Customer_Enabling_Services_Support_Assistant_Payroll/299864
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland City Council (derived for filtering) | Grade 2 (SCP 5 - 6) £25,949 - £25,989 | Customer Enabling Services Support Assistant/Courier
employer: Sunderland City Council
closing_date: 02/08/2026
reason: provisional transferable-office review
source_job_id: 299831
source_url: https://www.northeastjobs.org.uk/job/Customer_Enabling_Services_Support_Assistant_Courier/299831
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle Upon Tyne | SCP 23-25, FTE salary (£34,434.00 - £36,363.00) | Data and Exams Officer
employer: Walbottle Academy
closing_date: 24/08/2026 09:00
reason: annualised upper salary £36,363 exceeds North East review point £30,000
source_job_id: 300012
source_url: https://www.northeastjobs.org.uk/job/Data_and_Exams_Officer/300012
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle upon Tyne | £29,064 | Finance & Office Administrator (Maternity Cover) – Office based, Newcastle City Centre
employer: Rape Crisis Tyneside & Northumberland
closing_date: 30/07/2026 12:00
reason: transferable office/service title with specialist or borderline wording: finance
source_job_id: 299489
source_url: https://www.northeastjobs.org.uk/job/Finance_Office_Administrator_Maternity_Cover_Office_based_Newcastle_City_Centre/299489
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | North Tyneside | Grade 6 £28,598.00 - £30,024.00 | Homeless Support Officer
employer: North Tyneside Council
closing_date: 06/08/2026 00:00
reason: annualised upper salary £30,024 exceeds North East review point £30,000
source_job_id: 300070
source_url: https://www.northeastjobs.org.uk/job/Homeless_Support_Officer/300070
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle City Council (derived for filtering) | £29,064 - £31,022 per annum (Pay Award Pending) | Housing Assistant
employer: Newcastle City Council
closing_date: 04/08/2026 22:59
reason: transferable office/service title with specialist or borderline wording: housing
source_job_id: 298231
source_url: https://www.northeastjobs.org.uk/job/Housing_Assistant/298231
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Adult Social Care, South Tyneside | £41,771 pa | Local Area Coordinator – Primrose
employer: South Tyneside Council
closing_date: 28/08/2026 12:00
reason: annualised upper salary £41,771 exceeds North East review point £30,000
source_job_id: 299943
source_url: https://www.northeastjobs.org.uk/job/Local_Area_Coordinator_Primrose/299943
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Callerton Academy, Bedeburn Road, Newcastle upon Tyne NE5 4JQ | £26,403 - £27,254 per annum. Actual salary £24,676.65 - £25,472.00 per annum | MCR Pathways Programme Coordinator
employer: Gosforth Group
closing_date: 05/08/2026 09:00
reason: provisional transferable-office review
source_job_id: 300079
source_url: https://www.northeastjobs.org.uk/job/MCR_Pathways_Programme_Coordinator/300079
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | North Tyneside | Grade 5 £26,403 - £27,254 pa | Neighbourhood Housing Assistant
employer: North Tyneside Council
closing_date: 12/08/2026 00:00
reason: transferable office/service title with specialist or borderline wording: housing
source_job_id: 295153
source_url: https://www.northeastjobs.org.uk/job/Neighbourhood_Housing_Assistant/295153
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | South Tyneside Council (derived for filtering) | £33,699 pa pro rata | Participation and Engagement Officer (SEND), 29.6 hpw
employer: South Tyneside Council
closing_date: 10/08/2026 12:00
reason: transferable office/service title with specialist or borderline wording: send
source_job_id: 299890
source_url: https://www.northeastjobs.org.uk/job/Participation_and_Engagement_Officer_SEND_29_6_hpw/299890
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £39,152 - £41,771 | PMO Support Officer
employer: Gateshead Council
closing_date: 02/08/2026
reason: possible duplicate within North East Jobs
source_job_id: 299841
source_url: https://www.northeastjobs.org.uk/job/PMO_Support_Officer/299841
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £39,152 - £41,771 | PMO Support Officer
employer: Gateshead Council
closing_date: 02/08/2026
reason: possible duplicate within North East Jobs
source_job_id: 299843
source_url: https://www.northeastjobs.org.uk/job/PMO_Support_Officer/299843
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | North Tyneside (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256121
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256121
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | School Administrators required, various roles available throughout Gateshead (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256124
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256124
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | South Tyneside Council (derived for filtering) | £28,598 pa | SEND Travel Needs Assessment Officer
employer: South Tyneside Council
closing_date: 14/08/2026 12:00
reason: transferable office/service title with specialist or borderline wording: send
source_job_id: 300099
source_url: https://www.northeastjobs.org.uk/job/SEND_Travel_Needs_Assessment_Officer/300099
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle upon Tyne | £32,597 - £35,412 per annum (pay award pending) | Social Care Assessment Officer
employer: Newcastle City Council
closing_date: 11/08/2026 22:59
reason: annualised upper salary £35,412 exceeds North East review point £30,000
source_job_id: 298838
source_url: https://www.northeastjobs.org.uk/job/Social_Care_Assessment_Officer/298838
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £29,540 - £32,061 | Street Works Permit Support Officer
employer: Gateshead Council
closing_date: 09/08/2026
reason: annualised upper salary £32,061 exceeds North East review point £30,000
source_job_id: 299906
source_url: https://www.northeastjobs.org.uk/job/Street_Works_Permit_Support_Officer/299906
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | County Hall MORPETH, United Kingdom | £28598 -31022 | Virtual School Education Support Officer
employer: Northumberland County Council
closing_date: 06/08/2026
reason: annualised upper salary £31,022 exceeds North East review point £30,000
source_job_id: 299780
source_url: https://www.northeastjobs.org.uk/job/Virtual_School_Education_Support_Officer/299780
---


## EXCLUDED BY REVIEW

- None.

## Hard passes

- None after geography and deduplication checks.

## Safety boundary

- A normal run is review-only and writes no publishable JSON.
- Approved JSON requires an explicit PUBLISH confirmation and an exact same-day review-set match.
- Only factual vacancy fields are retained; full descriptions are not stored.
- Public role overviews are original Ontap text assembled from those factual fields.
- Detail pages are fetched only after a provisional title/teaser screen.
- North East Jobs terms require written permission for commercial reuse of site material.
- The source had no retrievable robots.txt (404) when the POC was designed.
- HC/POSS rules are provisional and do not amend Ontap's permanent selection policy.
