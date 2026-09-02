# JobG8 Claims Support family validation

Feed: **2026-09-02.xlsx**
Jobs in feed: **10,000**
Broad insurance/claims universe: **200** raw rows
IN after advert-level boundary rules: **36** raw rows
BORDERLINE: **1** raw rows
OUT: **163** raw rows
Content-unique IN jobs: **35** (removed **1** exact-content duplicate rows)

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
| IN | 36 |
| BORDERLINE | 1 |
| OUT | 163 |

## Content-unique IN regional shape

| Jobs | Ontap region |
|---:|---|
| 4 | Essex |
| 3 | Yorkshire - West |
| 3 | London |
| 2 | Staffordshire |
| 2 | Scotland West - Glasgow |
| 2 | West Midlands - Birmingham & Solihull |
| 2 | Greater Manchester - Manchester & Salford |
| 2 | Norfolk |
| 1 | Bristol & Bath |
| 1 | Kent |
| 1 | Oxfordshire |
| 1 | Greater Manchester - Wigan & Bolton |
| 1 | Cheshire - West |
| 1 | Leicestershire |
| 1 | North East - Tyneside, Wearside & Northumberland |
| 1 | Scotland Central - Fife |
| 1 | Merseyside - Liverpool |
| 1 | Wales South - Cardiff & Vale |
| 1 | Hampshire |
| 1 | Lancashire - Central |
| 1 | Gloucestershire |

## JobG8 classifications feeding content-unique IN jobs

| Jobs | JobG8 classification |
|---:|---|
| 25 | Insurance & Superannuation |
| 4 | Call Centre / CustomerService |
| 2 | Legal |
| 2 | Administration |
| 1 | Accounting |
| 1 | Banking & Financial Services |

## Recurring content-unique IN titles

| Jobs | Title |
|---:|---|
| 9 | Claims Handler |
| 7 | Casualty Claims Handler |
| 3 | HNW / Private Clients Claims Technician |
| 2 | Credit Hire Claims Handler |
| 1 | Legal Expenses Claims Handler |
| 1 | Insurance Coordinator |
| 1 | Senior Customer Service Adviser |
| 1 | Claims Administrator |
| 1 | Commercial Claims Handler |
| 1 | Claims Assistant |
| 1 | Real Estate Claims Handler |
| 1 | Motor Claims Handler |
| 1 | Senior Claims Handler FTC |
| 1 | Customer Service Advisor - Weekends |
| 1 | Experience Insurance Claims Clerk |
| 1 | Experienced Motor Claims Handler |
| 1 | Third-Party Capture Claims Handler |
| 1 | Senior Motor Fraud Claims Handler |

## Salary guard check

Content-unique IN jobs with usable annualised maximum: **10**.
IN jobs still over £50k: **0** (must be zero).
