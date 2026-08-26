# Singapore Legal Analysis Model Comparison

## Scope and tested configurations

This saved-answer evaluation compares **GPT-5.4 (arm-a)** with **GPT-5.6 Terra (arm-b)** on 15 Singapore Legal Analysis questions. Both arms recorded **low reasoning effort** and otherwise identical configuration: the same routing prompt, embedding model, Singapore Pinecone index and namespace, retrieval top-k, no reranker, Singapore v1.4 answer prompt, Azure endpoint, and API version. The recorded main model is the only configuration difference.

Each answer was scored independently under `rubrics/legal-analysis-v1.md` before matching answers were compared side by side. This is an evaluation of saved answers, not legal advice.

## Independent scores

| Arm | Legal correctness | Issue coverage | Grounding and citations | Jurisdiction discipline | Usefulness and safety | Overall |
|---|---:|---:|---:|---:|---:|---:|
| arm-a — GPT-5.4 | 4.07 | 4.33 | 3.87 | 4.80 | 4.40 | 4.29 |
| arm-b — GPT-5.6 Terra | 4.20 | 4.67 | 3.73 | 4.93 | 4.60 | 4.43 |

Means are arithmetic means across all 15 independently scored answers for each arm. Overall is the mean of all five dimensions across those answers.

## Pairwise preference totals

| Preference | Questions |
|---|---:|
| arm-a | 4 |
| arm-b | 8 |
| Tie | 3 |
| **Total** | **15** |

## Question-level comparisons

| Question | Preference | Confidence | Key reason |
|---|---|---|---|
| sg-001 | arm-b | confident | Gives the one-month wrongful-dismissal and usual six-month post-employment salary deadlines; arm-a gives only generic urgency. |
| sg-002 | tie | close | Arm-a is better grounded; arm-b is more complete on evidence, losses, itemisation, and possible SCT use. |
| sg-003 | tie | close | Both accurately apply the CPFTA six-month presumption and full repair, replacement, price-reduction, and rescission sequence. |
| sg-004 | arm-b | close | Better coverage of repudiation, net completion costs, IP/work product, system security, and limitation. |
| sg-005 | tie | close | Both are strong on negligence, causation, contributory fault, damages, evidence, and limitation, but omit concrete pre-action protocol steps. |
| sg-006 | arm-b | close | More complete on HDB transfer/buy-out, CPF allocation, parenting, and package settlement; both have current-procedure and maintenance-eligibility defects. |
| sg-007 | arm-b | confident | Identifies Muslim status as a potentially dispositive fact and includes the administration process; arm-a omits that regime check. |
| sg-008 | arm-a | confident | Similar substantive quality, but arm-a grounds oppression and derivative relief in statute and cases; arm-b cites none. |
| sg-009 | arm-b | close | More focused and avoids arm-a's questionable six-year retention suggestion; both overstate mutual trust and confidence. |
| sg-010 | arm-a | confident | Avoids arm-b's inadequately supported three-year knowledge-based defamation limitation statement. |
| sg-011 | arm-a | confident | Explains CPC attendance and the protection against self-incriminating answers; arm-b omits both despite stronger phone-power coverage. |
| sg-012 | arm-b | confident | Adds the direct Singapore-grant route and the current 2024 probate rule to the sound re-sealing analysis. |
| sg-013 | arm-a | close | Adds more precise SOPA response rules, the Magistrate's Court route, and a particularly usable defects matrix. |
| sg-014 | arm-b | close | Similar civil analysis, but arm-b more clearly distinguishes professional misconduct from negligence; both incompletely treat Noor Azlin's history. |
| sg-015 | arm-b | close | Gives more precise s 12A conditions, freezing evidence, wrongful-termination risk, anti-suit relief, and Indonesia-focused preservation planning. |

## Recurring strengths and weaknesses

### Arm-a — GPT-5.4

Strengths:

- Often provides dense statutory and case grounding, particularly in corporate law, criminal procedure, consumer remedies, and construction payment.
- Consistently offers detailed evidence-preservation steps and practical claim framing.
- Its strongest answers identify high-impact procedural protections, notably the police interviewee's self-incrimination protection.

Weaknesses:

- Occasionally omits a decisive fact, deadline, alternative route, or statutory power: examples include the exact employment deadline, Muslim intestacy, direct Singapore probate, and CPC phone access.
- Some procedural and case-history material is outdated or incomplete, including the Family Justice Rules 2014 references and the first-instance Noor Azlin causation disposition.
- Several answers are more diffuse than necessary for the practical decision.

### Arm-b — GPT-5.6 Terra

Strengths:

- More consistently checks threshold facts and alternative routes, including Muslim intestacy, direct Singapore probate, IP/system security, and Indonesia-focused asset protection.
- Action plans are generally focused on the most urgent practical risk.
- Often distinguishes related legal routes clearly, including oppression versus derivative recovery and negligence versus professional discipline.

Weaknesses:

- Citation density is uneven: sg-008 has no authorities, while several PDPA propositions lack controlling sections.
- Sg-010 gives an inadequately supported three-year defamation limitation statement, and sg-011 omits self-incrimination and compulsory-attendance protections.
- It shares currency defects with arm-a on mutual trust and confidence, Family Justice Rules 2014, and the later Noor Azlin history.

## Critical failures

No critical failures were recorded for either arm. The identified defects were reflected in dimension scores and, where material to the pair, in the comparison findings.

## Limitations

- No expectation file or gold answers were available.
- No retrieval or gateway logs were available, so the retrieved basis for an authority and the accuracy of citations could not be checked against source context.
- No external source checking was performed. Citation plausibility was not treated as proof of accuracy; findings rely only on repository inputs and the judge's legal analysis.
- One `gpt-5.6-sol` LLM judge evaluated this jurisdiction and saw the arm identifiers and model names. Model identity was therefore not blinded, although answer-inspection order was alternated; there was no second judge or inter-rater agreement check.
- Each arm has one saved run only. There are no repeated runs for assessing model-response variability.
- The 15-question suite supports descriptive findings only. No statistical inference is warranted.
- The evaluation relies on the recorded configurations and does not independently verify what was deployed.

These are comparative findings only. No deployment, promotion, or release recommendation is made.
