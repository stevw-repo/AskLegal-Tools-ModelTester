# Task 3: Australia recent legal changes query suite

## Handoff status

- Deliverable: `testing/suites/australia/au-recent-legal-changes-v1.json`
- Documentation: `testing/suites/README.md`
- Legal-currency date: revalidated 13 August 2026
- Latest API test: completed on 13 August 2026 against the direct Ask.Legal
  development backend using prompt label `au-prompt-v1.1-recent-legal-changes`;
  all 16 queries completed without API errors.
- Latest result:
  `testing/results/australia/au-prompt-v1.1-recent-legal-changes.md`
- Latest evaluation:
  `testing/temp/australia-v1.1-2026-08-13-audit/recent-legal-changes-evaluation.md`
- Evaluation verdict: partially updated but not reliably current; 3 pass,
  10 partial, and 3 fail/stale. None of the five linked tax-reform questions fully
  passed. Aged care improved from fail to partial relative to the 5 August review,
  while Payday Super regressed from partial to fail.
- Scope: prompt-output testing only. No application, retrieval, deployment, or
  production changes are included.

## Suite contract

The suite must remain a JSON array of exactly 16 objects. Each object contains only
`id` and `query`. IDs are consecutive from `au-rc-001` through `au-rc-016`, and all
queries are first-person Australian-law scenarios.

## Coverage and current-law review signals

| ID | Topic | Signal a current answer should recognise |
|---|---|---|
| `au-rc-001` | Negative gearing—grandfathering | The pre-7:30 pm ACT-time cutoff on 12 May 2026 and the contract-entry rule, rather than settlement alone. |
| `au-rc-002` | Negative gearing—established property | From 2027-28, excess residential deductions for a post-cutoff established dwelling are quarantined rather than offset against salary; current law governs how they can be applied or carried forward and denies simply adding prevented deductions to cost base. |
| `au-rc-003` | Negative gearing—new build | New residential dwellings are excepted, but the statutory definition depends on requirements in a legislative instrument; an answer should verify the instrument in force and distinguish the new-build CGT treatment. |
| `au-rc-004` | CGT transition | For an asset held across 1 July 2027, the 2026 Act contains deemed sale/reacquisition and deferral machinery, preserving old treatment for the pre-start component and applying indexation/current rules to the later component. |
| `au-rc-005` | CGT minimum rate | The 30% minimum-rate regime applies to relevant post-1 July 2027 gains, but current law contains an exception for recipients of specified income-support payments, including age pension. |
| `au-rc-006` | Division 296 | The 2026 legislation applies from 2026-27, uses an indexed $3 million large-balance threshold, a proportional earnings calculation, and an indexed $10 million very-large-balance tier with additional tax treatment. |
| `au-rc-007` | Payday Super | From 1 July 2026 the revised regime uses qualifying earnings, 12%, payday contributions generally received within 7 business days, and a revised SG charge; the ATO clearing house closed from that date. |
| `au-rc-008` | Merger control | From 1 January 2026 qualifying acquisitions are subject to mandatory, suspensory ACCC notification. The stated facts engage the very-large-acquirer revenue threshold unless an exemption or waiver applies. |
| `au-rc-009` | AML/CTF tranche two | From 1 July 2026 designated services supplied by lawyers and other tranche-two entities can trigger enrolment and risk-based AML/CTF duties; privilege is protected but is not a blanket exclusion from the regime. |
| `au-rc-010` | Privacy tort | The federal statutory tort for serious invasions of privacy commenced on 10 June 2025 and is not confined to APP entities. OAIC does not directly administer the tort. |
| `au-rc-011` | Family property | For the July 2025 proceeding, the post-10 June 2025 property framework expressly addresses the economic effects of family violence, liabilities, wastage, disclosure, and companion-animal orders; shared ownership or care cannot be ordered. |
| `au-rc-012` | Ransomware payments | A business carrying on business in Australia with prior-year turnover at least $3 million must report a ransomware or cyber-extortion payment, including one made on its behalf, within 72 hours. Other incident-reporting regimes must be analysed separately. |
| `au-rc-013` | Aged care | The rights-based Aged Care Act commenced on 1 November 2025, with a Statement of Rights, registered supporters, complaints arrangements, and protection from reprisal. |
| `au-rc-014` | Paid Parental Leave | For a child born from 1 July 2026, the scheme provides 130 days, with 20 days reserved for a partner where applicable; the pre-birth claim is adjusted after proof of birth. ATO pays a 12% super contribution after the relevant financial year. |
| `au-rc-015` | Wage underpayment | Intentional underpayment from 1 January 2025 can be a federal criminal offence, alongside civil exposure. FWO investigates/refers; AFP or CDPP initiate criminal proceedings, with cooperation and small-business mechanisms requiring precise treatment. |
| `au-rc-016` | Social-media minimum age | Since 10 December 2025, covered platforms—not children or parents—must take reasonable steps to prevent under-16 accounts. Coverage depends on the Act and the 2025 Rules as amended in March 2026. |

## Official sources checked on 4 August 2026

- ATO, [Tax reform—boosting home ownership, reforming negative gearing and CGT](https://www.ato.gov.au/about-ato/new-legislation/in-detail/individuals/tax-reform-boosting-home-ownership-reforming-negative-gearing-and-capital-gains-tax)
- Federal Register of Legislation, [Treasury Laws Amendment (Tax Reform No. 1) Act 2026](https://www.legislation.gov.au/C2026A00049/latest)
- Federal Register of Legislation, [Treasury Laws Amendment (Building a Stronger and Fairer Super System) Act 2026](https://www.legislation.gov.au/C2026A00008/latest)
- ATO, [Payday Super](https://softwaredevelopers.ato.gov.au/PaydaySuper)
- ACCC, [Mergers and acquisitions](https://www.accc.gov.au/business/mergers-and-acquisitions) and [notification thresholds](https://www.accc.gov.au/business/mergers-and-acquisitions/thresholds-for-notifying-acquisitions)
- Department of Home Affairs, [Overview of the AML/CTF Amendment Act](https://www.homeaffairs.gov.au/about-us/our-portfolios/criminal-justice/anti-money-laundering-and-counter-terrorism-financing/anti-money-laundering-and-counter-terrorism-financing-amendment-act/overview-of-the-aml-ctf-amendment-act)
- OAIC, [Statutory tort for serious invasions of privacy](https://www.oaic.gov.au/privacy/your-privacy-rights/more-privacy-rights/statutory-tort-for-serious-invasions-of-privacy)
- Attorney-General's Department, [Family law changes from June 2025](https://www.ag.gov.au/families-and-marriage/publications/family-law-changes-june-2025-information-family-law-professionals)
- Australian Cyber Security Centre, [Ransomware payment and cyber extortion payment reporting](https://www.cyber.gov.au/report-and-recover/report/ransomware-payment-and-cyber-extortion-payment-reporting)
- Department of Health, Disability and Ageing, [What the new Aged Care Act means for you](https://www.health.gov.au/our-work/aged-care-act/about/what-it-means)
- Services Australia, [Paid Parental Leave scheme changes](https://www.servicesaustralia.gov.au/paid-parental-leave-scheme-changes?context=64479)
- Fair Work Ombudsman, [Criminalising wage underpayments](https://www.fairwork.gov.au/about-us/workplace-laws/legislation-changes/closing-loopholes/criminalising-wage-underpayments-and-other-issues)
- eSafety Commissioner, [Social media age restrictions](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions)

## Validation command

```bash
python3 -c "import json; from pathlib import Path; p=Path('testing/suites/australia/au-recent-legal-changes-v1.json'); data=json.loads(p.read_text()); expected=[f'au-rc-{i:03d}' for i in range(1,17)]; assert len(data)==16; assert [x['id'] for x in data]==expected; assert all(set(x)=={'id','query'} for x in data); assert all(isinstance(x['query'],str) and x['query'].strip() for x in data); assert len({x['query'] for x in data})==16; print('validated 16 Australia recent-law queries')"
```
