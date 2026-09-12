# JobG8 Claims Support family validation

Feed: **2026-09-12.xlsx**
Jobs in feed: **10,000**
Broad insurance/claims universe: **370** raw rows
IN after advert-level boundary rules: **56** raw rows
BORDERLINE: **0** raw rows
OUT: **314** raw rows
Content-unique IN jobs: **55** (removed **1** exact-content duplicate rows)

Diagnostic only: no LIVE slice, publishing rule or production family status is changed.

## Boundary now being tested

- IN: claims handlers, claims administrators/clerks/advisers/technicians and clearly claims-led customer/admin support.
- IN: senior claims handlers remain eligible when the advert is ordinary claims ownership and the salary is within scope.
- OUT: general insurance broking/account-handler/account-executive/sales roles.
- OUT: loss/claims adjusters, Lloyd's-market adjuster work, lawyers/solicitors, managers/team leaders and large/major-loss specialists.
- OUT: annualised salary maximum **over £50,000**. Exactly £50,000 is not excluded by salary alone.
- Legal-expenses/pre-litigation claims handling can remain IN; substantively litigated/legal file-handling is OUT.

## Decision breakdown

| Decision | Raw rows |
|---|---:|
| IN | 56 |
| BORDERLINE | 0 |
| OUT | 314 |

## Content-unique IN regional shape

| Jobs | Ontap region |
|---:|---|
| 8 | Essex |
| 5 | London |
| 5 | Staffordshire |
| 5 | Greater Manchester - Manchester & Salford |
| 4 | Greater Manchester - Wigan & Bolton |
| 3 | Scotland West - Glasgow |
| 2 | Kent |
| 2 | West Midlands - Birmingham & Solihull |
| 2 | Yorkshire - West |
| 2 | Northamptonshire |
| 2 | Dorset |
| 1 | Oxfordshire |
| 1 | Cheshire - West |
| 1 | Leicestershire |
| 1 | North East - Tyneside, Wearside & Northumberland |
| 1 | Scotland Central - Fife |
| 1 | Hampshire |
| 1 | Bristol & Bath |
| 1 | Cheshire - East |
| 1 | Merseyside - Liverpool |
| 1 | Greater Manchester - North |
| 1 | Suffolk |

## JobG8 classifications feeding content-unique IN jobs

| Jobs | JobG8 classification |
|---:|---|
| 50 | Insurance & Superannuation |
| 2 | Administration |
| 1 | Accounting |
| 1 | Call Centre / CustomerService |
| 1 | Legal |

## Recurring content-unique IN titles

| Jobs | Title |
|---:|---|
| 9 | Claims Handler |
| 7 | Casualty Claims Handler |
| 3 | Commercial Claims Handler |
| 3 | HNW / Private Clients Claims Technician |
| 3 | Credit Hire Claims Handler |
| 3 | Motor Claims Handler |
| 2 | Senior Claims Handler |
| 2 | Insurance Claims Handler |
| 2 | Property Claims Handler |
| 1 | Insurance Coordinator |
| 1 | Senior Customer Service Adviser |
| 1 | Claims Administrator |
| 1 | Real Estate Claims Handler |
| 1 | Senior Claims Handler FTC |
| 1 | Third Party Claims Handler |
| 1 | Insurance Administrator Friendly team + 25 days A/L |
| 1 | Employer Liability and Public Liability Claims Handler (6 - Month FTC) |
| 1 | Claims Handler - Home / Motor / Insurance - Remote |
| 1 | Claims Handler (FTC) |
| 1 | Claims Handler - insurance/construction - hybrid following probation |
| 1 | Junior Claims Technician - Marine |
| 1 | Claims & Customer Service Advisor |
| 1 | Liability Claims Handler - EL/PL |
| 1 | Claims Handler - EL & PL |
| 1 | Legal Claims Handler - Healthcare London |

## Salary guard check

Content-unique IN jobs with usable annualised maximum: **17**.
IN jobs still over £50k: **0** (must be zero).
