# Australia v1.1 recent-law currency review

## Run details

- Prompt label: `au-prompt-v1.1`
- Suite: `testing/suites/australia/au-recent-legal-changes-v1.json`
- Result: `testing/results/australia/au-prompt-v1.1.md`
- API target: `https://asklegal-backend-dev.azurewebsites.net`
- Run generated: 5 August 2026 at 10:20:18 UTC
- Transport result: 16 of 16 queries completed without API errors.
- Evaluation baseline: the official-source signals in
  `.superpowers/sdd/task-3-brief.md`, verified on 4 August 2026.

## Overall verdict

The deployed Ask.Legal system is **partially updated but not reliably current**.
Only 3 of 16 answers fully applied the material current-law signals. Ten answers
recognised at least part of a new regime but omitted, hedged, or misstated a
material current rule. Three answers materially relied on superseded law or gave
the wrong current-law result.

| Rating | Count | Share |
|---|---:|---:|
| Pass | 3 | 18.75% |
| Partial | 10 | 62.50% |
| Fail / stale | 3 | 18.75% |

Recognition of a reform in 13 of 16 answers should not be mistaken for dependable
currency. Several answers knew that a new regime existed but could not apply the
operative threshold, exception, deadline, commencement date, or transitional rule.

## Linked tax-reform result

The system is **not reliably updated with the linked negative-gearing and CGT
regime**. None of the five targeted tax-reform answers earned a full pass.

- `au-rc-001` reached the correct practical outcome for a pre-cutoff contract, but
  did so using the old general negative-gearing position. It did not identify or
  apply `Income Tax Assessment Act 1997 (Cth) s 26-155`, the 7:30 pm ACT-time
  cutoff, or the express contract-entry rule. The correct conclusion was therefore
  coincidental rather than evidence of current-law knowledge.
- `au-rc-002` gave the wrong bottom line for a post-cutoff established dwelling. It
  said the $30,000 loss could offset salary and that there was no statutory carry-
  forward rule. Current law instead quarantines the excess from 2027-28, permits
  its statutory application/carry-forward, and prevents the denied expenditure
  simply entering cost base.
- `au-rc-003` recognised that a new-build exception and a legislative instrument
  matter, but said the operative reform provisions were unavailable and did not
  state the actual enacted negative-gearing or CGT treatment.
- `au-rc-004` correctly retrieved much of the deemed sale/reacquisition and deferred-
  gain machinery, but failed the minimum-rate component and suggested the later
  component might still receive discount treatment where the new regime instead
  requires the specific post-1 July 2027 treatment to be applied.
- `au-rc-005` retrieved Division 119 and recognised a specified-payment exception,
  but failed to identify age pension as an express statutory exception despite that
  fact being the point of the scenario.

This pattern suggests that parts of Schedule 1 of the 2026 Tax Reform Act are
retrievable, while Schedule 2 and some Division 119 detail are absent, incomplete,
or not being selected consistently.

## Per-query scorecard

Rating method:

- **Pass:** identifies and correctly applies all material freshness signals needed
  for the requested outcome.
- **Partial:** recognises the new regime but omits, hedges, or misstates a material
  rule, date, threshold, exception, deadline, or remedy.
- **Fail / stale:** applies superseded law, denies the operative reform, or gives a
  materially wrong bottom line.

| ID | Rating | Evaluation |
|---|---|---|
| `au-rc-001` | Fail / stale | Correct result for the wrong reason; did not know or apply the new grandfathering provision and cutoff. |
| `au-rc-002` | Fail / stale | Wrongly allowed a post-cutoff established-property loss against salary and denied the statutory quarantine/carry-forward treatment. |
| `au-rc-003` | Partial | Identified the new-build and instrument issues but could not state or apply the operative reform. |
| `au-rc-004` | Partial | Strong recognition of the 1 July 2027 transition, but material errors/omissions on the later component and 30% minimum-rate rule. |
| `au-rc-005` | Partial | Identified Division 119 and a payments exception but failed to recognise that age pension expressly qualifies. |
| `au-rc-006` | Pass | Correctly recognised enacted Division 296, first application in 2026-27, proportional earnings, indexed $3 million threshold, and indexed $10 million tier. |
| `au-rc-007` | Partial | Recognised Payday Super and the shift away from quarterly OTE, but failed to give the requested 12% of qualifying earnings and 7-business-day receipt rule. |
| `au-rc-008` | Partial | Correctly rejected voluntary review and recognised mandatory standstill, but failed to apply the clear $500 million / $10 million threshold to the stated $560 million / $14 million facts. |
| `au-rc-009` | Pass | Correctly recognised tranche-two lawyer coverage from 1 July 2026, likely designated services, core AML/CTF duties, and that privilege is not a blanket exemption. |
| `au-rc-010` | Partial | Correctly recognised the federal tort, elements, APP-entity independence and court route, but omitted the exact 1-year-awareness / 3-year-longstop limitation and incomplete remedies. |
| `au-rc-011` | Pass | Correctly applied the post-10 June 2025 family-property framework to economic effects of family violence, liabilities, wastage, disclosure and the exhaustive companion-animal orders. |
| `au-rc-012` | Partial | Correctly recognised mandatory reporting, the $3 million threshold, payment by an insurer on the company's behalf, and parallel regimes, but omitted the decisive 72-hour deadline and did not ground the duty in s 27 of the Cyber Security Act 2024 (Cth). |
| `au-rc-013` | Fail / stale | Relied on the Aged Care Act 1997 and User Rights Principles 2014 instead of applying the rights-based Aged Care Act 2024 in force from 1 November 2025; did not properly address the registered-supporter regime. |
| `au-rc-014` | Partial | Correctly identified 130 days, the 20-day partner reservation and birth-date control, but missed the automatic claim adjustment and the 12% ATO-paid super contribution timing. |
| `au-rc-015` | Partial | Correctly recognised post-1 January 2025 criminal wage-underpayment exposure and the importance of intent, but incorrectly treated small-business status as uncertain for a 40-employee employer and muddled the cooperation-agreement analysis. |
| `au-rc-016` | Partial | Correctly placed the duty on a likely covered platform and rejected parental consent, but failed to recognise that the duty had commenced on 10 December 2025, did not apply the March 2026 rule criteria, and understated/misstated current corporate penalty exposure. |

## Highest-priority currency gaps

1. **Negative gearing for residential property:** the system did not retrieve or
   apply the core 2026 reform in either side of the cutoff test.
2. **Tax Reform Act detail:** incomplete coverage of Division 119 exceptions and the
   interaction between the preserved pre-start gain and post-start CGT treatment.
3. **Exact compliance deadlines and thresholds:** Payday Super, merger thresholds,
   privacy limitation periods, ransomware reporting and social-media commencement.
4. **Superseded aged-care law:** the answer used the repealed/replaced 1997 framework
   for post-1 November 2025 conduct.
5. **Administrative detail with direct user impact:** Paid Parental Leave automatic
   adjustment and super payment, and non-small-business treatment in wage cases.

## Interpretation and next step

The results test the **deployed Ask.Legal answer system**, not model weights in
isolation. The repeated phrases that the relevant provisions were not in the
available materials, together with selective retrieval of some 2026 provisions,
support an inference of uneven source coverage or source selection. They do not by
themselves prove whether the base model's internal knowledge is current.

The appropriate next step is to provide this review to the team responsible for
the Australian legal source corpus or retrieval configuration, with priority on
the five gap areas above. No retrieval, database, pipeline, deployment, or
production change has been made in this workspace. After the relevant official
sources are confirmed available to the deployed system, rerun the same unchanged
suite and compare pass rates query by query.
