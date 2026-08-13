# North East Jobs ETL proof-of-concept review

review_date: 2026-08-13
review_fingerprint: 8ab1dab005a917d0c2e21ac3590be327c282d4da534b800884a2a96caec833d8

Edit only the `action:` line in each editable block:

- For a POSS job, use `action: select` to add it or `action: exclude` to reject it.
- For a selected HC job, use `action: exclude` to remove it.
- Leave `action:` blank for no change.
- Commit the edit, then rerun the NEJobs process for the same review date.
- Decisions are matched by `source_job_id` and expire when the review date changes.

Run generated: 2026-08-13T08:55:53+01:00
RSS input: https://www.northeastjobs.org.uk/RSSJobs.aspx?orgid=62
JobG8 comparison rows in target geographies: 296

## Funnel

- RSS vacancies read: 644
- Hard-pass title/teaser screen before detail requests: 594
- Detail candidates: 50
- Detail failures or unavailable snapshots: 0
- Outside the two target geographies: 4
- Tees Valley explicitly excluded: 7
- Target-geography candidates reviewed: 39

## Detail diagnostics

- No unresolved detail-page failures.

## Review outcomes

- HC: 8
- POSS: 30
- Hard pass: 1
- Final selected after manual actions: 8
- Final POSS awaiting decision: 30
- Manually excluded: 0
- Confirmed JobG8 duplicates: 0
- Possible JobG8 duplicates: 5
- Likely unique to North East Jobs: 34
- Rows in possible within-source duplicate groups: 0

- Manual review warning: manual review date 2026-07-29 is not 2026-08-13; old actions ignored

## SELECTED

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | North Tyneside | Grade 05 (£26,403 - £27,254) pro rata per annum | Admin Assistant
employer: North Tyneside Council
closing_date: 20/08/2026 00:00
reason: clear transferable title: admin assistant
source_job_id: 300537
source_url: https://www.northeastjobs.org.uk/job/Admin_Assistant/300537
---

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Berwick, United Kingdom | £13.26 | Admin Assistant - Staff Bank (Berwick)
employer: Northumberland County Council
closing_date: 23/08/2026 00:00
reason: clear transferable title: admin assistant
source_job_id: 300726
source_url: https://www.northeastjobs.org.uk/job/Admin_Assistant_Staff_Bank_Berwick/300726
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
SELECTED | North East - Tyneside, Wearside & Northumberland | Prudhoe | SCP 2 - 5 (£24,413 - £25,583 (pro rata) depending upon qualifications and experience | Administrative Assistant
employer: Prudhoe Town Council
closing_date: 04/09/2026 12:00
reason: clear transferable title: administrative assistant
source_job_id: 300646
source_url: https://www.northeastjobs.org.uk/job/Administrative_Assistant/300646
---

---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Unit 43 Colbourne Crescent, Nelson Park Industrial Estate, Cramlington, United Kingdom | £20,742 - £21,072 | Business Support Administrator
employer: Northumberland County Council
closing_date: 20/08/2026
reason: clear transferable title: administrator
source_job_id: 300550
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Administrator/300550
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
SELECTED | North East - Tyneside, Wearside & Northumberland | North Tyneside | Grade 4 (£25,583 - £25,989) per annum | Casual Clerical Receptionist
employer: North Tyneside Council
closing_date: 21/08/2026 00:00
reason: clear transferable title: receptionist, clerical
source_job_id: 300594
source_url: https://www.northeastjobs.org.uk/job/Casual_Clerical_Receptionist/300594
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


## POSS — choose SELECT or EXCLUDE

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Bishop Auckland College (derived for filtering) | Harmonised pay scale points 23-35 (£28,571.40 - £37,659.47 pro rata) | 0.4 Lecturer Coordinator in Counselling & Psychotherapy Studies
employer: Bishop Auckland College
closing_date: 18/08/2026
reason: annualised upper salary £37,659 exceeds North East review point £30,000
source_job_id: 299764
source_url: https://www.northeastjobs.org.uk/job/0_4_Lecturer_Coordinator_in_Counselling_Psychotherapy_Studies/299764
---

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | CETL | £25,989 - £26,403 per annum | Administration Assistant
employer: Hartlepool Borough Council
closing_date: 21/08/2026
reason: possible JobG8 duplicate requires review
source_job_id: 300212
source_url: https://www.northeastjobs.org.uk/job/Administration_Assistant/300212
---

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | St Joseph’s Catholic Junior School, Birtley, Chester-le-Street, DH3 | Grade D, SCP 5 - 7 (£25,583 - £26,403 per annum, pro rata) | Administration Assistant
employer: Bishop Wilkinson Catholic Education Trust
closing_date: 20/08/2026
reason: possible JobG8 duplicate requires review
source_job_id: 300360
source_url: https://www.northeastjobs.org.uk/job/Administration_Assistant/300360
---

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Sacriston | £24,796 - £25,185 (Pro Rata) | Administrative Assistant
employer: Durham County Council
closing_date: 31/08/2026
reason: possible JobG8 duplicate requires review
source_job_id: 299277
source_url: https://www.northeastjobs.org.uk/job/Administrative_Assistant/299277
---

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Framwellgate Moor | Support Grade B; £26,970 per annum | Administrator
employer: New College Durham
closing_date: 26/08/2026
reason: possible JobG8 duplicate requires review
source_job_id: 300512
source_url: https://www.northeastjobs.org.uk/job/Administrator/300512
---

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Framwellgate Moor Campus, Durham, DH1 5ES | Support Grade D; £28,980 per annum | Apprenticeship Support Officer
employer: New College Durham
closing_date: 26/08/2026
reason: provisional transferable-office review
source_job_id: 300505
source_url: https://www.northeastjobs.org.uk/job/Apprenticeship_Support_Officer/300505
---

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | The Horizon School, CETL, Brierton Lane, Hartlepool | Band 7 £23,175 - £24,314 pa | Attendance & Support Officer
employer: Hartlepool Borough Council
closing_date: 04/09/2026 12:00
reason: transferable office/service title with specialist or borderline wording: attendance
source_job_id: 299877
source_url: https://www.northeastjobs.org.uk/job/Attendance_Support_Officer/299877
---

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Peterlee | £26,403 - £28,142 per annum, pro rata (actual salary approx. £16,056 - £17,112) | Community Engagement Officer (Part Time)
employer: Peterlee Town Council
closing_date: 14/08/2026
reason: provisional transferable-office review
source_job_id: 299795
source_url: https://www.northeastjobs.org.uk/job/Community_Engagement_Officer_Part_Time/299795
---

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Highlight Active Wellbeing Hub | £13.47 per hour | Customer Service Advisor
employer: Hartlepool Borough Council
closing_date: 31/08/2026
reason: possible JobG8 duplicate requires review
source_job_id: 299796
source_url: https://www.northeastjobs.org.uk/job/Customer_Service_Advisor/299796
---

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Barnard Castle | £27,128.40 | Facilities Coordinator
employer: The Bowes Museum
closing_date: 24/08/2026 08:00
reason: transferable office/service title with specialist or borderline wording: facilities
source_job_id: 300105
source_url: https://www.northeastjobs.org.uk/job/Facilities_Coordinator/300105
---

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Durham (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256127
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256127
---

---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Civic Centre, Crook | £40,777 to £45,091 p.a. (Grade 11) Pay award pending | Service Design Lead
employer: Durham County Council
closing_date: 13/08/2026
reason: transferable office/service title with specialist or borderline wording: lead
source_job_id: 300430
source_url: https://www.northeastjobs.org.uk/job/Service_Design_Lead/300430
---

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | Council Offices, Green Lane, Spennymoor | £30,024 to £33,699 p.a. (Grade 7) Pay Award pending | Technical and Support Officers
employer: Durham County Council
closing_date: 31/08/2026
reason: transferable office/service title with specialist or borderline wording: technical
source_job_id: 300579
source_url: https://www.northeastjobs.org.uk/job/Technical_and_Support_Officers/300579
---

---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle (derived for filtering) | Actual pro-rata salary is £27,703 - £29,601 per annum (pay award pending) | Attendance Officer
employer: North East Futures - UTC
closing_date: 08/09/2026 12:00
reason: transferable office/service title with specialist or borderline wording: attendance
source_job_id: 300632
source_url: https://www.northeastjobs.org.uk/job/Attendance_Officer/300632
---

---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | North Tyneside | GRADE 5 SCP 7 (£26,403) - SCP 9 (£27,254) per annum | Claims Support Officer
employer: North Tyneside Council
closing_date: 28/08/2026 00:00
reason: provisional transferable-office review
source_job_id: 300592
source_url: https://www.northeastjobs.org.uk/job/Claims_Support_Officer/300592
---

---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland City Council (derived for filtering) | Grade 3 (SCP 7- 11) £26,403-£28,142 | Customer Enabling Services Advocate
employer: Sunderland City Council
closing_date: 20/08/2026
reason: provisional transferable-office review
source_job_id: 300485
source_url: https://www.northeastjobs.org.uk/job/Customer_Enabling_Services_Advocate/300485
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
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland City Council (derived for filtering) | 4 (SCP 12 - 17) £28,598 - £31,022 | Environmental Enforcement Support Officer
employer: Sunderland City Council
closing_date: 13/08/2026
reason: annualised upper salary £31,022 exceeds North East review point £30,000
source_job_id: 300019
source_url: https://www.northeastjobs.org.uk/job/Environmental_Enforcement_Support_Officer/300019
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Northumberland County Council, County Hall, Morpeth, United Kingdom | £26,403 - £28,142 | Financial Assessments and Benefits Coordinator
employer: Northumberland County Council
closing_date: 16/08/2026
reason: provisional transferable-office review
source_job_id: 300551
source_url: https://www.northeastjobs.org.uk/job/Financial_Assessments_and_Benefits_Coordinator/300551
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
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Various Locations | £25,989 pa pro rata (£13.47 per hour) | Receptionist – Various Posts
employer: South Tyneside Council
closing_date: 25/08/2026 12:00
reason: annualised upper salary £50,678,550 exceeds North East review point £30,000
source_job_id: 300662
source_url: https://www.northeastjobs.org.uk/job/Receptionist_Various_Posts/300662
---

---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Northumberland (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256120
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256120
---

---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | North Tyneside (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256121
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256121
---

---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256122
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256122
---

---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | School Administrators required, various roles available throughout Gateshead (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256124
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256124
---

---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | School Administrators required, various roles available throughout South Tyneside (derived for filtering) | From £14.54 - £15.20per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256125
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256125
---

---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland (derived for filtering) | From £14.54 - £15.20 per hour | School Administrator
employer: First Class Supply & Training
closing_date: 31/08/2026
reason: agency-style advert with no structured employment location
source_job_id: 256126
source_url: https://www.northeastjobs.org.uk/job/School_Administrator/256126
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
action: select
POSS | North East - Tyneside, Wearside & Northumberland | County Hall MORPETH, United Kingdom | £21,122.40 - 22,513.60 per annum | Statutory SEND Coordinator
employer: Northumberland County Council
closing_date: 20/08/2026 00:00
reason: transferable office/service title with specialist or borderline wording: send
source_job_id: 300549
source_url: https://www.northeastjobs.org.uk/job/Statutory_SEND_Coordinator/300549
---

---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Town Hall, South Shields | £28,598 pa | Technical Support Officer – Licensing
employer: South Tyneside Council
closing_date: 24/08/2026 12:00
reason: transferable office/service title with specialist or borderline wording: technical
source_job_id: 300614
source_url: https://www.northeastjobs.org.uk/job/Technical_Support_Officer_Licensing/300614
---


## EXCLUDED BY REVIEW

- None.

## Hard passes

- [Apprenticeship Skills Coordinator - Technical Construction & Civil Engineering](https://www.northeastjobs.org.uk/job/Apprenticeship_Skills_Coordinator_Technical_Construction_Civil_Engineering/299766) — out-of-scope occupation: engineer.

## Safety boundary

- A normal run is review-only and writes no publishable JSON.
- Approved JSON requires an explicit PUBLISH confirmation and an exact same-day review-set match.
- Only factual vacancy fields are retained; full descriptions are not stored.
- Public role overviews are original Ontap text assembled from those factual fields.
- Detail pages are fetched only after a provisional title/teaser screen.
- North East Jobs terms require written permission for commercial reuse of site material.
- The source had no retrievable robots.txt (404) when the POC was designed.
- HC/POSS rules are provisional and do not amend Ontap's permanent selection policy.
