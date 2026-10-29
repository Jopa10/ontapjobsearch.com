# Independent pre-result audit — 29 October 2026

The same-input comparison run 40869488844 is still running; no final before/after counts are claimed.

## Geographic scope

Twelve of the 40 factual town corrections resolve to existing non-LIVE Service Admin markets: Thornaby (Tees Valley), Hamilton/Blantyre/Bellshill/Chapelhall (Lanarkshire), Ballymoney/Moy (Northern Ireland West), Lathom/Burscough (Lancashire West), Gourock (Renfrewshire & Inverclyde), Bispham (Blackpool & Fylde), Greenlaw (Borders). They should be recognised correctly but must not activate markets or silently publish there. This explains why 40 lookup changes will not yield 40 additional published jobs.

## Numeric advert pay hidden by nonnumeric SalaryAdditional

An independent scan of the captured 29 October 50k workbook found 13 records with no numeric structured amounts and a nonnumeric SalaryAdditional field that currently takes precedence over a clear numeric description rate. Twelve currently fail Service Admin title/geography checks. The one eligible Service Admin record is job 108206913, Payroll Specialist / Payroll Administrator: structured additional text Plus Holiday Pay; description states £17.50–£19.00 per hour. It was DAILY_REVIEW in the baseline because pay was unavailable. The changed missing-pay policy may allow it, but description pay should be recovered for display and numeric checking before release. At the standard 37.5 hours, the £19 upper rate annualises to £37,050, below the ordinary £40k review point. Do not invent actual weekly hours from this calculation.

This precedence behaviour existed before the current patch, but its interaction with the new missing-pay permission requires attention. Before promoting a release candidate, prefer supported numeric description pay over nonnumeric additional wording when structured numeric amounts are absent, preserve the additional wording separately/in display where appropriate, and test contradictory numeric descriptions against £50k and Document Controller £45k limits. Structured numeric salary must retain priority. Do not make excluded professional/technical roles eligible merely because a rate is recovered.

## Mixed industrial titles

Place-suffixed Admin Officer and ordinary engineering/warehouse administration match; Senior Administration Officer and administrator/forklift-driver combinations remain rejected. Mixed Engineer / Administrator titles can match the new industry-word exception: inspect the actual newly admitted adverts to confirm admin duties predominate before release. This is a review focus, not evidence yet that an unsuitable job was published.

Production remains unchanged. No main merge or deployment is authorised by this audit.
