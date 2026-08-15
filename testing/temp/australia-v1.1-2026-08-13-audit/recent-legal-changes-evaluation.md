# Australia v1.1 recent legal changes evaluation

## Run details and rubric

- Result reviewed: `testing/results/australia/au-prompt-v1.1-recent-legal-changes.md`
- Suite: `testing/suites/australia/au-recent-legal-changes-v1.json`
- Review date: 13 August 2026
- Currency baseline: law in force and official guidance checked on 13 August 2026

Ratings:

- **Pass:** identifies and correctly applies all material current-law signals
  needed for the requested outcome.
- **Partial:** recognises the regime but omits, hedges, or misstates a material
  date, threshold, deadline, exception, rule, or remedy.
- **Fail / stale:** applies superseded law, denies or cannot identify the
  operative reform, or gives a materially wrong bottom line.

## Overall verdict

The system remains **partially updated but not reliably current**.

| Rating | Queries | Count | Share |
|---|---|---:|---:|
| Pass | au-rc-006, au-rc-009, au-rc-011 | 3 | 18.75% |
| Partial | au-rc-003, au-rc-004, au-rc-005, au-rc-008, au-rc-010, au-rc-012, au-rc-013, au-rc-014, au-rc-015, au-rc-016 | 10 | 62.50% |
| Fail / stale | au-rc-001, au-rc-002, au-rc-007 | 3 | 18.75% |

This is the same aggregate distribution as the 5 August 2026 review, but the
composition changed: aged care improved from fail to partial, while Payday Super
regressed from partial to fail. None of the five linked tax-reform answers fully
passes.

## Query-by-query scorecard

| ID | Rating | Evaluation and required correction |
|---|---|---|
| `au-rc-001` | **Fail / stale** | It notices that contract timing rather than settlement may control, but never applies the enacted 7:30 pm ACT-time cutoff on 12 May 2026 or `s 26-155`. It quotes unrelated 1996 and 2017/2019 transitional cutoffs and refuses the requested bottom line. The 6:30 pm AEST contract was before the 7:30 pm ACT-time cutoff and should receive the statutory pre-cutoff treatment. |
| `au-rc-002` | **Fail / stale** | Materially wrong bottom line: it says the $30,000 loss can reduce salary and denies automatic quarantine/carry-forward treatment. Current `s 26-155` quarantines post-cutoff established-dwelling excess deductions from 2027–28 and provides their statutory application; the prevented amount cannot simply be added to cost base. |
| `au-rc-003` | **Partial** | Correctly flags a new-build exception and the need to inspect a legislative instrument, but cannot state the enacted exception or definition, does not identify `s 26-155`/`s 26-160`, and gives only a generic CGT discussion. It must apply the actual new-residential-dwelling test and distinguish the post-2027 CGT discount/indexation choices. |
| `au-rc-004` | **Partial** | Strong on deemed sale/reacquisition, deferral, the pre/post-1 July 2027 split, and indexation. It incorrectly suggests both components may receive the old 50% discount and cannot identify the enacted 30% minimum-rate regime. The later component must be analysed under the new post-start rules rather than assumed discountable. |
| `au-rc-005` | **Partial** | Correctly rejects the statement that every gain is automatically taxed at 30% and recognises an income-support exception. It fails the scenario's decisive point by refusing to confirm that age pension is a specified qualifying payment. |
| `au-rc-006` | **Pass** | Correctly identifies enacted Division 296, first application in 2026–27, the special end-of-year first-year balance test, proportional/formula treatment, the indexed $3 million threshold, and the indexed $10 million tier. |
| `au-rc-007` | **Fail / stale** | Applies superseded law: 10.5%, ordinary time earnings, quarterly measurement, and the old extended quarterly timing. From 1 July 2026 the relevant regime uses qualifying earnings, 12%, and generally requires receipt within seven business days; the clearing house closed. This answer could cause immediate underpayment and late-payment noncompliance. |
| `au-rc-008` | **Partial** | Correctly recognises the mandatory post-1 January 2026 regime, standstill logic, and waiver pathway. It does not apply the clear very-large-acquirer threshold: $560 million acquirer revenue and $14 million target revenue exceed the $500 million/$10 million test unless an exemption or waiver applies. |
| `au-rc-009` | **Pass** | Correctly recognises tranche-two coverage from 1 July 2026, activity-based designated services, enrolment/program/risk/CDD/reporting duties, and that privilege is claim-specific rather than a blanket exclusion. |
| `au-rc-010` | **Partial** | Correctly identifies a strong statutory tort claim, APP-entity independence, elements, public-interest balance, defences, remedies, and court rather than OAIC administration. It omits the 10 June 2025 commencement and the earlier-of one-year-awareness/three-year-longstop limitation expressly requested. |
| `au-rc-011` | **Pass** | Correctly applies the post-10 June 2025 property framework to liabilities, wastage, disclosure, and companion animals; recognises threats to the dog; and correctly states that shared ownership or alternating care cannot be ordered. The family-violence economic-effect rule is less directly grounded than it should be, but the practical result is sound. |
| `au-rc-012` | **Partial** | Correctly rejects voluntary reporting, recognises insurer payment on the company's behalf, and separates privacy and critical-infrastructure streams. It omits the decisive $3 million threshold, 72-hour deadline, `Cyber Security Act 2024 (Cth) s 27`, and exact report content. “Measured in hours” is not an adequate urgent compliance answer. |
| `au-rc-013` | **Partial** | Major improvement: applies `Aged Care Act 2024 (Cth) s 23`, rejects reliance on the old Charter, and addresses visits, support, complaints, and reprisal. It omits the 1 November 2025 commencement and registered-supporter framework, and unnecessarily lists superseded 1997 Act/2014 Principles references. |
| `au-rc-014` | **Partial** | Correctly gives 130 days, a 110-day partnered claimant cap, and 20 reserved days. It fails to state that proof of birth adds the ten days to the pre-birth claim and omits the 12% ATO-paid super contribution after the relevant financial year. |
| `au-rc-015` | **Partial** | Correctly identifies serious civil and accessory exposure and says the “civil only” claim is unsafe. It treats criminal liability as merely possible depending on verification instead of applying the offence in force from 1 January 2025; it does not recognise that 40 employees makes this a non-small-business employer, and it omits the precise cooperation-agreement and AFP/CDPP roles. |
| `au-rc-016` | **Partial** | Correctly places the duty on a likely covered platform, rejects parental consent, and identifies reasonable-steps exposure. It omits commencement on 10 December 2025, does not actually apply the March 2026 amended Rules, and fails to state the 30,000-penalty-unit civil exposure in `s 63D`. |

## Current-law verification anchors

### Linked tax reform

The enacted [Treasury Laws Amendment (Tax Reform No. 1) Act 2026](https://www.legislation.gov.au/C2026A00049/latest)
contains the CGT transition/minimum-rate regime and the negative-gearing changes.
The statutory text confirms the 7:30 pm ACT-time cutoff on 12 May 2026, the
contract-entry rule, the new-dwelling exception and instrument power, quarantine
and application of prevented deductions, and the post-1 July 2027 CGT machinery.

### Other reforms

- The ACCC confirms mandatory notification from 1 January 2026, standstill until
  approval/waiver, and the $500 million/$10 million very-large-acquirer threshold:
  [ACCC thresholds](https://www.accc.gov.au/business/mergers-and-acquisitions/thresholds-for-notifying-acquisitions).
- The OAIC confirms commencement of the privacy tort on 10 June 2025, its reach
  beyond APP entities, the one-year/three-year limitation, remedies, and no direct
  OAIC administration: [OAIC](https://www.oaic.gov.au/privacy/your-privacy-rights/more-privacy-rights/statutory-tort-for-serious-invasions-of-privacy).
- The Attorney-General's Department confirms the post-10 June 2025 family
  property, disclosure, family-violence, and companion-animal rules:
  [AGD](https://www.ag.gov.au/families-and-marriage/publications/family-law-changes-june-2025-information-family-law-professionals).
- Cyber.gov.au confirms the $3 million threshold, payment-on-behalf rule, and
  72-hour duty under s 27:
  [ransomware reporting](https://www.cyber.gov.au/report-and-recover/report/ransomware-payment-and-cyber-extortion-payment-reporting).
- Services Australia confirms 130 days, 20 reserved days, the proof-of-birth
  adjustment, and the automatic 12% ATO super payment in the following financial
  year: [PPL changes](https://www.servicesaustralia.gov.au/paid-parental-leave-scheme-changes?context=64479).
- The Fair Work Ombudsman confirms the offence from 1 January 2025, the fewer-
  than-15 small-business threshold, and the separate cooperation-agreement route:
  [criminal underpayments](https://www.fairwork.gov.au/about-us/workplace-laws/legislation-changes/closing-loopholes/criminalising-wage-underpayments-and-other-issues).
- eSafety confirms that the platform duty commenced on 10 December 2025 and that
  children and parents are not penalised:
  [social-media age restrictions](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions).
- The Federal Register confirms the Rules as amended on 25 March 2026:
  [Online Safety Rules](https://www.legislation.gov.au/F2026L00370/asmade/text).

## Prompt and presentation defects

- Hidden-source wording appears in 13 of 16 answers; only `au-rc-006`,
  `au-rc-009`, and `au-rc-012` avoid the detected prohibited phrases.
- Ten of 16 answers exceed 2,000 words; the median is 2,214.5 words.
- Several answers turn source insufficiency into the central response instead of
  stating a clear current-law answer plus a targeted verification step.
- The suite remains particularly unreliable for exact operational details, even
  where it recognises the existence of a reform.

## Release decision

**Do not treat reform recognition as legal currency.** The next run should be
accepted only if all five tax questions apply the 2026 Act and each operational
compliance question states the exact date, threshold, deadline, exception, or
transition tested by the query.

