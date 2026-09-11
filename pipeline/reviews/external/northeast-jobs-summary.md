# North East Jobs ETL proof-of-concept review

review_date: 2026-09-11
review_fingerprint: 907a7c81aa363470dab0eab477562b11486e9282705ac00f4f6bf74b7132a347

Edit only the `action:` line in each editable block:

- For a POSS job, use `action: select` to add it or `action: exclude` to reject it.
- For a selected HC job, use `action: exclude` to remove it.
- Leave `action:` blank for no change.
- Commit the edit; the review workflow will remember the decision.
- Decisions are carried forward only while the same vacancy review facts remain unchanged.

Run generated: 2026-09-11T12:18:18+01:00
RSS input: https://www.northeastjobs.org.uk/RSSJobs.aspx?orgid=62
JobG8 comparison rows in target geographies: 261

## Funnel

- RSS vacancies read: 714
- Hard-pass title/teaser screen before detail requests: 664
- Detail candidates: 50
- Detail failures or unavailable snapshots: 0
- Outside the two target geographies: 7
- Tees Valley explicitly excluded: 11
- Target-geography candidates reviewed: 32

## Detail diagnostics

- No unresolved detail-page failures.

## Review outcomes

- HC: 15
- POSS: 16
- Hard pass: 1
- Final selected after remembered/manual actions: 18
- Final POSS awaiting decision: 9
- Manually excluded: 4
- Confirmed JobG8 duplicates: 0
- Possible JobG8 duplicates: 1
- Likely unique to North East Jobs: 31
- Rows in possible within-source duplicate groups: 0

- Manual review warning: manual review date 2026-09-10 is not 2026-09-11; old actions ignored

## SELECTED

---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Education Development Centre, Spennymoor | Grade 5 £27,274 - £29,542 | Admin Assistant
employer: Durham County Council
closing_date: 27/09/2026
reason: clear transferable title: admin assistant
source_job_id: 301820
source_url: https://www.northeastjobs.org.uk/job/Admin_Assistant/301820
---
---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Age UK County Durham (derived for filtering) | £24,454 per annum, pro rata (£14,870.70) + pension contribution generous holidays | Administrator
employer: Age UK County Durham
closing_date: 30/09/2026 12:00
reason: clear transferable title: administrator
source_job_id: 301544
source_url: https://www.northeastjobs.org.uk/job/Administrator/301544
---
---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Corten House, Durham | Grade 4 (£26,427 - £27,709) | Passenger Transport Administration Assistant
employer: Durham County Council
closing_date: 16/09/2026
reason: clear transferable title: administration assistant
source_job_id: 301481
source_url: https://www.northeastjobs.org.uk/job/Passenger_Transport_Administration_Assistant/301481
---
---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Age UK County Durham (derived for filtering) | £24,454 per annum, pro rata (£14,870.70) + pension contribution generous holidays | Project Administrator
employer: Age UK County Durham
closing_date: 30/09/2026 12:00
reason: clear transferable title: administrator
source_job_id: 301543
source_url: https://www.northeastjobs.org.uk/job/Project_Administrator/301543
---
---
action:
SELECTED | North East - County Durham & Darlington/Hartlepool | Spennymoor, DL16 7JB | £26,403 - £28,598 pro rata (pay award pending) | School Secretary
employer: Durham County Council
closing_date: 21/09/2026 12:00
reason: clear transferable title: secretary
source_job_id: 301524
source_url: https://www.northeastjobs.org.uk/job/School_Secretary/301524
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Sir Charles Parsons School, Westbourne Avenue, Walker, Newcastle upon Tyne, NE6 4ED | £27,274 - £28,153 per annum pro rata (Actual salary £22,786 - £23,520 per annum) | Administration Assistant Level 3
employer: Newcastle City Council
closing_date: 18/09/2026 12:00
reason: clear transferable title: administration assistant
source_job_id: 301513
source_url: https://www.northeastjobs.org.uk/job/Administration_Assistant_Level_3/301513
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Lemington Riverside, Rokeby Street, Newcastle upon Tyne, NE15 8RR | £25,185 per annum pro rata (Actual salary £21,187 per annum) | Administrative Assistant - Level 1
employer: Newcastle City Council
closing_date: 25/09/2026 12:00
reason: clear transferable title: administrative assistant
source_job_id: 301338
source_url: https://www.northeastjobs.org.uk/job/Administrative_Assistant_Level_1/301338
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | South Tyneside Council (derived for filtering) | £29,542 pa pro rata | Assisted Travel Senior Business Support Officer, 30hpw
employer: South Tyneside Council
closing_date: 16/10/2026 12:00
reason: clear transferable title: business support officer
source_job_id: 301777
source_url: https://www.northeastjobs.org.uk/job/Assisted_Travel_Senior_Business_Support_Officer_30hpw/301777
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | North Tyneside | Grade 5 £26403 to £27254 per annum | Business Support Assistant
employer: North Tyneside Council
closing_date: 22/09/2026 00:00
reason: clear transferable title: business support assistant
source_job_id: 297597
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Assistant/297597
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Sunderland | £26,427 - £26,847 per annum pro rata | Business Support Assistant - Children's Social Care
employer: Together for Children - Sunderland
closing_date: 20/09/2026
reason: clear transferable title: business support assistant
source_job_id: 301377
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Assistant_Children_s_Social_Care/301377
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Sunderland | Grade 2 (SCP 5-6) £26,427 - £26,847 per annum pro rata | Business Support Assistant in Careers & NEET
employer: Together for Children - Sunderland
closing_date: 20/09/2026
reason: clear transferable title: business support assistant
source_job_id: 301568
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Assistant_in_Careers_NEET/301568
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Dubmire Primary Academy / Aim High Academy Trust | Grade 3 (SCP 7-11 £27,274 - £29,071 pro rata) | Business Support Officer
employer: AIM High Academy Trust
closing_date: 18/09/2026 09:00
reason: clear transferable title: business support officer
source_job_id: 301610
source_url: https://www.northeastjobs.org.uk/job/Business_Support_Officer/301610
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | South Tyneside Council (derived for filtering) | £29,542 pa | Customer Service Advisor x 2 Posts
employer: South Tyneside Council
closing_date: 17/09/2026 12:00
reason: clear transferable title: customer service advisor
source_job_id: 301438
source_url: https://www.northeastjobs.org.uk/job/Customer_Service_Advisor_x_2_Posts/301438
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | Longbenton High School Hailsham Ave, Newcastle upon Tyne NE12 8ER | £24,551 | DBS01122/26 - Business Administrator Apprentice - Longbenton High School
employer: North Tyneside Council
closing_date: 14/09/2026 12:00
reason: clear transferable title: administrator
source_job_id: 300866
source_url: https://www.northeastjobs.org.uk/job/DBS01122_26_Business_Administrator_Apprentice_Longbenton_High_School/300866
---
---
action:
SELECTED | North East - Tyneside, Wearside & Northumberland | North Tyneside Council (derived for filtering) | £25,583 - £25,989 pro rata | DBS01125/26 - Receptionist - Norham High School
employer: North Tyneside Council
closing_date: 15/09/2026 12:00
reason: clear transferable title: receptionist
source_job_id: 301184
source_url: https://www.northeastjobs.org.uk/job/DBS01125_26_Receptionist_Norham_High_School/301184
---
## POSS — choose SELECT or EXCLUDE

---
action: select
POSS | North East - County Durham & Darlington/Hartlepool | New College Durham - Framwellgate Moor | Support Grade F02 - F03; £32,012 to £32,975 per annum | Personal Development Coach Coordinator
employer: New College Durham
closing_date: 20/09/2026
reason: annualised upper salary £32,975 exceeds North East review point £30,000
source_job_id: 301004
source_url: https://www.northeastjobs.org.uk/job/Personal_Development_Coach_Coordinator/301004
---
---
action: exclude
POSS | North East - County Durham & Darlington/Hartlepool | Civic Centre, Hartlepool | £47,665 - £51,928 per annum | Practice Development Coordinator
employer: Hartlepool Borough Council
closing_date: 21/09/2026 12:00
reason: annualised upper salary £51,928 exceeds North East review point £30,000
source_job_id: 301368
source_url: https://www.northeastjobs.org.uk/job/Practice_Development_Coordinator/301368
---
---
action:
POSS | North East - County Durham & Darlington/Hartlepool | Start Whitby Street Hartlepool TS24 7AB | £32,578 - £34,811 per annum | Recovery Coordinator
employer: Hartlepool Borough Council
closing_date: 28/09/2026
reason: annualised upper salary £34,811 exceeds North East review point £30,000
source_job_id: 301502
source_url: https://www.northeastjobs.org.uk/job/Recovery_Coordinator/301502
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle upon Tyne | Approximately £28,500 (£38,900 FTE) | Access Arrangements Coordinator
employer: Royal Grammar School
closing_date: 14/09/2026 09:00
reason: annualised upper salary £38,900 exceeds North East review point £30,000
source_job_id: 301670
source_url: https://www.northeastjobs.org.uk/job/Access_Arrangements_Coordinator/301670
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland City Council (derived for filtering) | Grade 5 (SCP 17-22) £31,022 - £33,699 | Active Sunderland Weight Management Support Officer
employer: Sunderland City Council
closing_date: 14/09/2026
reason: annualised upper salary £33,699 exceeds North East review point £30,000
source_job_id: 301079
source_url: https://www.northeastjobs.org.uk/job/Active_Sunderland_Weight_Management_Support_Officer/301079
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Housing Options and Homelessness Service | £34,811 pa | Armed Forces Support Officer
employer: South Tyneside Council
closing_date: 24/09/2026 12:00
reason: annualised upper salary £34,811 exceeds North East review point £30,000
source_job_id: 301778
source_url: https://www.northeastjobs.org.uk/job/Armed_Forces_Support_Officer/301778
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Houghton Le Spring (derived for filtering) | £27,274 to £29,071 (actual pro-rata £12,680 to £13,516) | Attendance Administrator
employer: AIM High Academy Trust
closing_date: 21/09/2026 12:00
reason: transferable office/service title with specialist or borderline wording: attendance
source_job_id: 301579
source_url: https://www.northeastjobs.org.uk/job/Attendance_Administrator/301579
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Walbottle Village Primary School The Green, Walbottle Newcastle-Upon-Tyne NE15 8JL / Beech Hill Primary School Linhope Road West Denton Newcastle-Upon-Tyne Tyne and Wear NE5 2LW | £30,023 - £32,046 per annum pro rata (Actual salary £10,184 - £10,870 per annum) | Attendance Officer
employer: Valour Multi Academy Trust
closing_date: 21/09/2026 12:00
reason: transferable office/service title with specialist or borderline wording: attendance
source_job_id: 301699
source_url: https://www.northeastjobs.org.uk/job/Attendance_Officer/301699
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Kyloe House, Stannington, United Kingdom | £25,485.96 - £27,646.17 (equated salary quoted) | Behaviour Support Officer - Kyloe House
employer: Northumberland County Council
closing_date: 17/09/2026 00:00
reason: provisional transferable-office review
source_job_id: 301477
source_url: https://www.northeastjobs.org.uk/job/Behaviour_Support_Officer_Kyloe_House/301477
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle City Council (derived for filtering) | £27,274 - £28,153 pro rata, per annum (plus enhancements for out of hours) | Customer Service Advisor
employer: Newcastle City Council
closing_date: 23/09/2026 22:59
reason: possible JobG8 duplicate requires review
source_job_id: 300841
source_url: https://www.northeastjobs.org.uk/job/Customer_Service_Advisor/300841
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland City Council (derived for filtering) | Grade 5 (SCP 17-22) £31,022 - £33,699 | Driving Assessment Officer
employer: Sunderland City Council
closing_date: 14/09/2026
reason: annualised upper salary £33,699 exceeds North East review point £30,000
source_job_id: 301282
source_url: https://www.northeastjobs.org.uk/job/Driving_Assessment_Officer/301282
---
---
action: exclude
POSS | North East - Tyneside, Wearside & Northumberland | Sunderland City Council (derived for filtering) | 4 (SCP 12 - 17) £28,598 - £31,022 | Environmental Enforcement Support Officer
employer: Sunderland City Council
closing_date: 16/09/2026
reason: annualised upper salary £31,022 exceeds North East review point £30,000
source_job_id: 301401
source_url: https://www.northeastjobs.org.uk/job/Environmental_Enforcement_Support_Officer/301401
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Northumberland County Council (derived for filtering) | £32,578 - 35,570 | Family Group Conference Coordinator
employer: Northumberland County Council
closing_date: 22/09/2026 00:00
reason: annualised upper salary £35,570 exceeds North East review point £30,000
source_job_id: 301692
source_url: https://www.northeastjobs.org.uk/job/Family_Group_Conference_Coordinator/301692
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | Newcastle City Council (derived for filtering) | £37,563 - £41,177 per annum | Housing Support Officer
employer: Newcastle City Council
closing_date: 21/09/2026 22:59
reason: transferable office/service title with specialist or borderline wording: housing
source_job_id: 300255
source_url: https://www.northeastjobs.org.uk/job/Housing_Support_Officer/300255
---
---
action: select
POSS | North East - Tyneside, Wearside & Northumberland | Eddie Ferguson House, Blyth, United Kingdom | £32,578 - £35,570 | Tenant Engagement Officer
employer: Northumberland County Council
closing_date: 20/09/2026
reason: annualised upper salary £35,570 exceeds North East review point £30,000
source_job_id: 301243
source_url: https://www.northeastjobs.org.uk/job/Tenant_Engagement_Officer/301243
---
---
action:
POSS | North East - Tyneside, Wearside & Northumberland | County Hall MORPETH, United Kingdom | £29,542 - 32,046 | Virtual School Education Support Officer
employer: Northumberland County Council
closing_date: 23/09/2026 00:00
reason: annualised upper salary £32,046 exceeds North East review point £30,000
source_job_id: 301765
source_url: https://www.northeastjobs.org.uk/job/Virtual_School_Education_Support_Officer/301765
---
## EXCLUDED BY REVIEW

- None.

## Hard passes

- [Highways Technical Support Officer (INTERNAL ONLY)](https://www.northeastjobs.org.uk/job/Highways_Technical_Support_Officer_INTERNAL_ONLY/301268) — not open to external applicants.

## Safety boundary

- A normal run is review-only and writes no publishable JSON.
- Approved JSON requires an explicit PUBLISH confirmation and an exact same-day review-set match.
- Only factual vacancy fields are retained; full descriptions are not stored.
- Public role overviews are original Ontap text assembled from those factual fields.
- Detail pages are fetched only after a provisional title/teaser screen.
- North East Jobs terms require written permission for commercial reuse of site material.
- The source had no retrievable robots.txt (404) when the POC was designed.
- HC/POSS rules are provisional and do not amend Ontap's permanent selection policy.
