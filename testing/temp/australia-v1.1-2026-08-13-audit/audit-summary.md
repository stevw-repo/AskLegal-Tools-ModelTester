# Australia v1.1 response audit

## Audit scope

- Audit date: 13 August 2026
- Prompt under review: `prompts/australia/au-prompt-v1.1.md`
- Federal–State result: `testing/results/australia/au-prompt-v1.1-federal-state.md`
- Recent-law result: `testing/results/australia/au-prompt-v1.1-recent-legal-changes.md`
- Responses reviewed: 34 of 34
- Transport integrity: both result files contained all expected responses, no
  `ERROR:` lines, no empty-response markers, and no missing conversation IDs.

This is an output audit. It tests legal correctness, legal currency,
jurisdiction handling, responsiveness, prompt compliance, citation presentation,
and practical usefulness. It does not prove whether a cited authority appeared
in the hidden retrieval payload because answer-generation logs were not part of
this run.

## Executive verdict

**Do not approve the current Australian output set as release-ready.**

| Suite | Strong / satisfactory | Material revision | Fail / unsafe | Total |
|---|---:|---:|---:|---:|
| Federal–State | 7 | 8 | 3 | 18 |
| Recent legal changes | 3 | 10 | 3 | 16 |
| **Combined** | **10 (29.4%)** | **18 (52.9%)** | **6 (17.6%)** | **34** |

The result is mixed rather than uniformly poor. The model often identifies the
right broad legal stream and produces a usable action plan. It is not dependable
when the answer requires an exact 2025–26 commencement rule, threshold, deadline,
exception, or a disciplined refusal to apply an arbitrary State regime.

## Highest-risk findings

1. **Wrong or superseded law.** `au-rc-002` wrongly allows the post-cutoff
   established-property loss against salary. `au-rc-007` applies the old 10.5%
   ordinary-time-earnings and quarterly regime after Payday Super commenced.
2. **Wrong-jurisdiction analysis.** `au-001` identifies Victoria as the likely
   workers' compensation jurisdiction but devotes a substantive issue to the NSW
   psychological-injury exclusion. `au-017` asks for the missing State and then
   supplies Queensland rights, QCAT, and Queensland deadlines anyway.
3. **Primary pathway omitted.** `au-012` discusses the Queensland subcontractor
   charge mechanism but never explains the ordinary payment-claim, payment-
   schedule, adjudication, debt-recovery, and suspension pathway.
4. **Exact compliance content missing.** The responses omit or hedge material
   rules on the tax cutoff, merger thresholds, privacy limitation period,
   ransomware 72-hour deadline, paid-parental-leave super contribution, wage
   underpayment offence, and social-media commencement and penalty.
5. **Hidden-source disclosure remains systemic.** Prohibited phrases such as
   “materials provided”, “available authorities”, and “material available” occur
   in 23 of 34 answers: 10 of 18 Federal–State answers and 13 of 16 recent-law
   answers.

## Positive findings

- `au-002`, `au-003`, and `au-008` separate Commonwealth and State streams well.
- `au-013`–`au-016` generally handle nationwide Commonwealth law and the common
  law of Australia correctly without demanding an unnecessary State.
- `au-rc-006`, `au-rc-009`, and `au-rc-011` apply their principal current-law
  reforms successfully.
- All 34 answers include exactly one disclaimer and a `## References` section.
- The current environmental answer, `au-003`, now covers the Commonwealth EPBC
  referral/assessment/approval stream that was missing in the prior review.

## Prompt-compliance audit

| Check | Result | Assessment |
|---|---:|---|
| Exactly one disclaimer | 34/34 | Pass |
| `## References` section | 34/34 | Pass |
| No hidden-source wording | 11/34 | Fail systemically |
| Correct missing-jurisdiction gate | 0/2 cleanly | `au-017` applies Qld law; `au-018` gives a generic numeric period after asking |
| Concision | Median 2,225 words (Federal–State); 2,214.5 (recent-law) | Weak; 22/34 answers exceed 2,000 words |
| Citation presentation | Multiple visible defects | Dual reported/medium-neutral forms, all-caps Act title, and incomplete Tasmanian instrument title |

The disclaimer and reference controls are reliable. The hidden-source and
conciseness controls are not. The jurisdictional clarification gate has
regressed materially in `au-017`.

## Current-law verification

The legal-currency benchmarks were rechecked on 13 August 2026 against primary
or official sources, including:

- [Treasury Laws Amendment (Tax Reform No. 1) Act 2026](https://www.legislation.gov.au/C2026A00049/latest)
- [ACCC notification thresholds](https://www.accc.gov.au/business/mergers-and-acquisitions/thresholds-for-notifying-acquisitions)
- [OAIC statutory privacy tort](https://www.oaic.gov.au/privacy/your-privacy-rights/more-privacy-rights/statutory-tort-for-serious-invasions-of-privacy)
- [Cyber.gov.au ransomware-payment reporting](https://www.cyber.gov.au/report-and-recover/report/ransomware-payment-and-cyber-extortion-payment-reporting)
- [Services Australia paid-parental-leave changes](https://www.servicesaustralia.gov.au/paid-parental-leave-scheme-changes?context=64479)
- [Fair Work Ombudsman criminal underpayments](https://www.fairwork.gov.au/about-us/workplace-laws/legislation-changes/closing-loopholes/criminalising-wage-underpayments-and-other-issues)
- [eSafety social-media age restrictions](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions)
- [WorkSafe Victoria mental-injury eligibility](https://www.worksafe.vic.gov.au/practice-directive-mental-injury-eligibility)
- [Queensland security-of-payment Act](https://www.legislation.qld.gov.au/view/pdf/current/act-2017-043)
- [Family Court of Western Australia property guidance](https://familycourt.wa.gov.au/P/property_and_financial.aspx)

No material change was found that displaced the suite's existing legal-currency
signals. The detailed reasoning and query-level verdicts are in:

- `federal-state-evaluation.md`
- `recent-legal-changes-evaluation.md`

## Recommended acceptance gates for the next rerun

1. Zero answers may mention materials, sources, retrieval, available authorities,
   or source coverage.
2. `au-001` must apply current Victorian mental-injury law and keep NSW law out
   unless the connection test actually selects NSW.
3. `au-012` must address the Queensland Chapter 3 primary pathway before a
   subcontractor charge.
4. `au-017` and `au-018` must stop after seeking the missing State or Territory;
   neither should provide a State-specific or generic numeric rule first.
5. All five tax-reform questions must apply the enacted 2026 Act, not analogous
   historic provisions.
6. Payday Super, merger control, privacy tort, ransomware reporting, PPL,
   criminal underpayment, and social-media answers must state the exact operative
   dates, thresholds, deadlines, and exceptions tested by the query.
7. Case citations must use one supplied citation form in accordance with the
   prompt, and every legislation citation must use the complete instrument title,
   year, jurisdiction, and pinpoint.

