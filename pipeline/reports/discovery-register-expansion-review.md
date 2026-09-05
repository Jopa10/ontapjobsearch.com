# Discovery register expansion review

Date: 5 September 2026

## Proposed and applied rules

- Employer-sector register: 20 exact current identities were added as active `private_sector` rules. Each has a direct `advertiser_type=Company` observation in the repository inventory and is matched only by exact employer identity.
- Role-relationship register: 159 explicit exact-title or named transferable-title relationships were added across Service Admin, Customer Service / Contact Centre, HR / Recruitment and Finance / Accounts.
- The largest additions cover recurring Service Admin variants such as `Administration Assistant`, `Sales Administrator`, `Operations Administrator`, combined receptionist/administrator titles, care-home administrator titles and `Service Co-ordinator`.
- Customer-service additions explicitly cover `Call Centre Agent`, `Call Centre Operator`, `Customer Service Coordinator`, `Customer Services Administrator` and closely named variants.
- All active additions retain private-target-only routing. Exact titles and explicit relationships refine ranking; governed same-family membership supplies the broader fallback. No public-sector target rule was added.

## Current-inventory impact

- Published jobs audited: 1,807.
- Job pages with at least one governed ranked target: 475, up from the pre-expansion production audit of 21.
- Eligible recommendation pairs before the six-result display limit: 2,663.
- Remaining slice fallbacks: 1,332.

## Assumptions

- A direct JobG8 `Company` observation plus an exact named identity is treated as repository evidence for the named commercial provider; the generic `Company` rule itself remains `unknown`.
- Agency adverts are not assumed to be private-sector jobs because the agency identity does not establish the hiring employer.
- Title variants are matched exactly. The resolver does not stem, infer or generate roles.
- Distance remains Haversine straight-line distance from canonical coordinates, capped at 15 miles. The target job's actual location is preserved.

## Gaps

- 1,463 current pages have an `unknown` source-employer sector, principally agency adverts, but this no longer blocks same-family private-target discovery.
- 528 pages have no eligible evidenced-private target within 15 miles.
- 756 pages have a broad or unresolved source location.
- 48 pages have neither a governed published family nor an exact approved source-role relationship.
- Repeated campaign adverts can create many eligible pairs; the page resolver still limits display to six and ranks by role priority, distance and posted date.

## Questionable entries held for review

- `hireful` — may be an intermediary rather than the hiring employer.
- `Charity Link` — company-channel evidence conflicts with a charity-indicating identity.
- `NHS Professionals` — NHS-linked staffing identity needs a deliberate ownership classification.
- `The Rosalind Franklin Institute` — repository fields do not establish whether the required sector is private, public, education or charity.

These four entries are `REVIEW`, inactive and `PENDING`; they cannot affect recommendations.
