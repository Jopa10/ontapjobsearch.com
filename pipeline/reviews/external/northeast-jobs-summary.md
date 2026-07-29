# North East Jobs ETL proof-of-concept review

review_date: 2026-07-29
review_fingerprint: 41c6907fdea8ffe469778e8c3e816fb109ba6ad22692fce5784ec73f6e7d2af7

Edit only the `action:` line in each editable block:

- For a POSS job, use `action: select` to add it or `action: exclude` to reject it.
- For a selected HC job, use `action: exclude` to remove it.
- Leave `action:` blank for no change.
- Commit the edit, then rerun the NEJobs process for the same review date.
- Decisions are matched by `source_job_id` and expire when the review date changes.

Run generated: 2026-07-29T13:52:57+01:00
RSS input: https://www.northeastjobs.org.uk/RSSJobs.aspx?orgid=62
JobG8 comparison rows in target geographies: 110

## Funnel

- RSS vacancies read: 649
- Hard-pass title/teaser screen before detail requests: 581
- Detail candidates: 68
- Detail failures or unavailable snapshots: 25
- Outside the two target geographies: 0
- Tees Valley explicitly excluded: 8
- Target-geography candidates reviewed: 35

## Detail diagnostics

- 299841 — PMO Support Officer: HTTPError
- 299843 — PMO Support Officer: HTTPError
- 299778 — Early Help Administrator: HTTPError
- 299780 — Virtual School Education Support Officer: HTTPError
- 299809 — Application Support Officer (INTERNAL ONLY): HTTPError
- 299726 — Clerical Officer Receptionist: HTTPError
- 299764 — 0.4 Lecturer Coordinator in Counselling & Psychotherapy Studies: HTTPError
- 299744 — Receptionist/Student Services: HTTPError
- 299686 — Business Support - Springwater Academy: HTTPError
- 299693 — Administration Assistant: HTTPError
- 299650 — Attendance Officer: HTTPError
- 299563 — Administration Assistant - Conyers School (SPARK Education Trust): HTTPError
- 299570 — Information Management and Data Services Officer: HTTPError
- 299508 — Clerical Officer Receptionist: HTTPError
- 299489 — Finance & Office Administrator (Maternity Cover) – Office based, Newcastle City Centre: HTTPError
- 299408 — Tenant Engagement Officer: HTTPError
- 299411 — SEND Review Coordinator: HTTPError
- 299397 — Level 3 Academy Administrator Apprentice: HTTPError
- 299277 — Administrative Assistant: HTTPError
- 299075 — Attendance Administration Support Assistant: HTTPError
- 256120 — School Administrator: HTTPError
- 256122 — School Administrator: HTTPError
- 256124 — School Administrator: HTTPError
- 256126 — School Administrator: HTTPError
- 256127 — School Administrator: HTTPError

## Review outcomes

- HC: 12
- POSS: 23
- Hard pass: 0
- Final selected after manual actions: 13
- Final POSS awaiting decision: 22
- Manually excluded: 0
- Confirmed JobG8 duplicates: 0
- Possible JobG8 duplicates: 0
- Likely unique to North East Jobs: 35
- Rows in possible within-source duplicate groups: 0

## SELECTED

---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Meadowfield Depot, Durham (hybrid working options available) | Grade 4 £25,583 - £26,824 (Pay award pending) | Administration Assistant
employer: Durham County Council
closing_date: 09/08/2026
reason: clear transferable title: administration assistant
source_job_id: 299480
source_url: https://www.northeastjobs.org.uk/job/Administration_Assistant/299480
---

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
SELECTED | North East - County Durham & Darlington/Hartlepool | Highlight Active Wellbeing Hub | £13.47 per hour | Customer Service Advisor
employer: Hartlepool Borough Council
closing_date: 31/08/2026
reason: clear transferable title: customer service advisor
source_job_id: 299796
source_url: https://www.northeastjobs.org.uk/job/Customer_Service_Advisor/299796
---

---
action: select
SELECTED | North East - County Durham & Darlington/Hartlepool | Darlington Borough Council (derived for filtering) | £25,989 per annum (pay award pending) | Events Assistant
employer: Darlington Borough Council
closing_date: 11/08/2026
reason: provisional transferable-office review
source_job_id: 300044
source_url: https://www.northeastjobs.org.uk/job/Events_Assistant/300044
---

---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Framwellgate School Durham (derived for filtering) | £23,218 (FTE £25,583) | Receptionist and Events Co-ordinator at the Sjovoll Centre
employer: Framwellgate School Durham
closing_date: 10/08/2026 09:00
reason: clear transferable title: receptionist
source_job_id: 299718
source_url: https://www.northeastjobs.org.uk/job/Receptionist_and_Events_Co_ordinator_at_the_Sjovoll_Centre/299718
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
SELECTED | North East - Tyneside, Wearside & Northumberland | Hazlewood Community Primary School, Canterbury Way, Wideopen, Newcastle upon Tyne | £21,683 - £22,421 | DBS01116/26 - Admin Assistant - Hazlewood Community Primary School
employer: North Tyneside Council
closing_date: 21/08/2026 12:00
reason: clear transferable title: admin assistant
source_job_id: 299761
source_url: https://www.northeastjobs.org.uk/job/DBS01116_26_Admin_Assistant_Hazlewood_Community_Primary_School/299761
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
POSS | North East - County Durham & Darlington/Hartlepool | Peterlee | £26,403 - £28,142 per annum, pro rata (actual salary approx. £16,056 - £17,112) | Community Engagement Officer (Part Time)
employer: Peterlee Town Council
closing_date: 14/08/2026
reason: provisional transferable-office review
source_job_id: 299795
source_url: https://www.northeastjobs.org.uk/job/Community_Engagement_Officer_Part_Time/299795
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
POSS | North East - County Durham & Darlington/Hartlepool | Spectrum Business Park, Seaham (hybrid working options available) | Grade 7 £30,024 to £33,699 per annum (pay award pending) | Review Officer
employer: Durham County Council
closing_date: 09/08/2026
reason: annualised upper salary £33,699 exceeds North East review point £30,000
source_job_id: 298685
source_url: https://www.northeastjobs.org.uk/job/Review_Officer/298685
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
POSS | North East - Tyneside, Wearside & Northumberland | North Tyneside | £13.45 per hour | Fundraising & Partnerships Coordinator
employer: YMCA North Tyneside
closing_date: 03/08/2026
reason: transferable office/service title with specialist or borderline wording: fundraising
source_job_id: 299556
source_url: https://www.northeastjobs.org.uk/job/Fundraising_Partnerships_Coordinator/299556
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
POSS | North East - Tyneside, Wearside & Northumberland | Gateshead | £25,989 - £26,403 | PMO Secretariat
employer: Gateshead Council
closing_date: 02/08/2026
reason: provisional transferable-office review
source_job_id: 299845
source_url: https://www.northeastjobs.org.uk/job/PMO_Secretariat/299845
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
POSS | North East - Tyneside, Wearside & Northumberland | School Administrators required, various roles available throughout South Tyneside (derived for filtering) | From £14.54 - £15.20per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256125
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256125
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
