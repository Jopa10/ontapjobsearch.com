# JobG8 Claims Support family validation

Feed: **2026-08-30.xlsx**
Jobs in feed: **10,000**
Broad insurance/claims universe: **101** raw rows
IN after advert-level boundary rules: **10** raw rows
BORDERLINE: **0** raw rows
OUT: **91** raw rows
Content-unique IN jobs: **10** (removed **0** exact-content duplicate rows)

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
| IN | 10 |
| BORDERLINE | 0 |
| OUT | 91 |

## Content-unique IN regional shape

| Jobs | Ontap region |
|---:|---|
| 3 | Norfolk |
| 2 | Kent |
| 1 | Staffordshire |
| 1 | Bristol & Bath |
| 1 | Oxfordshire |

## JobG8 classifications feeding content-unique IN jobs

| Jobs | JobG8 classification |
|---:|---|
| 3 | Insurance & Superannuation |
| 2 | Administration |
| 2 | Call Centre / CustomerService |
| 2 | Legal |
| 1 | Accounting |

## Recurring content-unique IN titles

| Jobs | Title |
|---:|---|
| 2 | Claims Handler |
| 1 | Insurance Administrator Friendly team + 25 days A/L |
| 1 | Legal Expenses Claims Handler |
| 1 | Insurance Coordinator |
| 1 | Senior Customer Service Adviser |
| 1 | Claims Administrator |
| 1 | Motor Claims Handler |
| 1 | Experienced Motor Claims Handler |
| 1 | Third-Party Capture Claims Handler |

## Salary guard check

Content-unique IN jobs with usable annualised maximum: **9**.
IN jobs still over £50k: **0** (must be zero).
