# Hong Kong Legal Analysis Model Comparison

## 1. Scope and tested configurations

This is an independent LLM-as-judge evaluation of 15 saved Hong Kong Ask.Legal legal-analysis answers per arm. Each answer was scored independently under rubrics/legal-analysis-v1.md before the matching pair was compared. To reduce ordering bias, arm-b was inspected first for odd-numbered question IDs and arm-a first for even-numbered IDs.

The experiment compares **GPT-5.4** (arm-a) with **GPT-5.6 Terra** (arm-b). Both recorded configurations use **low reasoning effort** and are otherwise identical: intent-router-current, text-embedding-3-small, ask-legal-chatbot-hk-dataset-v8 in the default namespace, retrieval top-k 8, no reranker, and hong-kong-v2.0 as the answer prompt. The recorded main `model` field is the only differing configuration field.

This report evaluates saved answers, not legal advice. It does not independently establish that the recorded configurations were deployed.

## 2. Independent scores

Means are arithmetic means across all 15 answers for each arm. Overall is the mean of all five dimensions across the 15 answers.

| Arm | Legal correctness | Issue coverage | Grounding and citations | Jurisdiction discipline | Usefulness and safety | Overall |
|---|---:|---:|---:|---:|---:|---:|
| arm-a — GPT-5.4 | 4.07 | 4.60 | 3.60 | 4.93 | 4.53 | 4.35 |
| arm-b — GPT-5.6 Terra | 4.47 | 4.80 | 3.93 | 4.80 | 4.73 | 4.55 |

## 3. Pairwise preference totals

| Preference | Count |
|---|---:|
| arm-a — GPT-5.4 | 2 |
| arm-b — GPT-5.6 Terra | 11 |
| Tie | 2 |
| **Total** | **15** |

## 4. Question-level comparisons

| Question | Preference | Confidence | Key reason |
|---|---|---|---|
| hk-001 | arm-b | Close | More accurately confines statutory retaliation protection while separating ordinary commission and notice claims. |
| hk-002 | arm-b | Close | Reaches the same sound result with tighter causation analysis and fewer weakly connected authorities. |
| hk-003 | arm-b | Close | Better explains the post-acceptance Sale of Goods Ordinance s 55 remedy and avoids unsupported additional statutes. |
| hk-004 | arm-b | Close | More direct on electronic formation and the value credit due for any usable partial work. |
| hk-005 | Tie | Close | Both give sound negligence and limitation guidance but wrongly route low-value personal-injury claims to Small Claims. |
| hk-006 | arm-b | Close | More completely separates parenting arrangements, child maintenance and spousal maintenance. |
| hk-007 | arm-a | Confident | Correctly checks domicile before applying succession law to movable bank balances; arm-b does not. |
| hk-008 | Tie | Close | Both give strong minority-remedy analysis but wrongly say an exact 25% holding can block a 75% special resolution. |
| hk-009 | arm-b | Close | More distinctly addresses later use, retention and security of monitoring data. |
| hk-010 | arm-b | Confident | Gives a materially safer account of the interim-injunction threshold and fuller privilege and malicious-falsehood analysis. |
| hk-011 | arm-b | Close | Ties safe interview and lawyer-access advice more directly to the questioning directions. |
| hk-012 | arm-b | Close | More focused on foreign-domicile evidence and the estate-duty cutoff. |
| hk-013 | arm-a | Close | Uniquely checks arbitration and forum clauses before selecting the Small Claims Tribunal. |
| hk-014 | arm-b | Confident | Gives the better loss analysis and avoids arm-a's dated direction to HKICPA, although it should still name the current regulator. |
| hk-015 | arm-b | Confident | Makes Mainland asset preservation and reciprocal enforcement central to a Shenzhen-assets dispute. |

## 5. Recurring strengths and weaknesses

### Arm-a — GPT-5.4

Strengths:

- Thorough issue spotting, evidence-preservation checklists and practical action plans.
- Strong conflict-of-laws discipline on hk-007.
- Useful attention to arbitration and forum clauses on hk-013.
- Consistently stays within Hong Kong law and usually qualifies conclusions appropriately.

Weaknesses:

- Frequently includes long authority lists whose connection to the actual proposition or facts is weak, reducing auditability.
- Incorrectly places low-value personal-injury claims in the Small Claims Tribunal on hk-005.
- Incorrectly treats exactly 25% of voting rights as enough to block a 75%-threshold special resolution on hk-008.
- Gives a dated accounting-complaint route on hk-014 and is occasionally insufficiently cautious about exceptional interim relief.

### Arm-b — GPT-5.6 Terra

Strengths:

- More selective and concise use of legal rules and authorities.
- Strong distinctions between available remedies and procedural risks, especially on consumer rights, defamation, police interviews and cross-border enforcement.
- Practical next steps are consistently tied to the relevant facts.
- Generally stronger legal precision and issue coverage, reflected in the independent means.

Weaknesses:

- Shares arm-a's incorrect Small Claims guidance on hk-005.
- Shares arm-a's incorrect special-resolution blocking advice for an exact 25% holding on hk-008.
- Fails to check domicile before applying intestacy rules to the bank accounts on hk-007.
- Does not name or adequately ground the current accounting regulator on hk-014.

## 6. Critical failures

Each arm has one critical failure:

- **arm-a, hk-005:** incorrectly states that a personal-injury claim under HK$75,000 may be brought in the Small Claims Tribunal, which does not have jurisdiction over personal-injury claims.
- **arm-b, hk-005:** the same incorrect Small Claims Tribunal guidance.

The hk-008 special-resolution error is also material and appears in both arms, but it was recorded as a substantial correctness defect rather than an additional critical failure.

## 7. Limitations

- No expectation file or gold answers were available.
- No retrieval logs or sanitized gateway logs were available.
- No external source checking was performed. Citations were not treated as accurate merely because they appeared plausible, and their existence, currency and proposition-level support could not be independently verified.
- One `gpt-5.6-sol` LLM judge evaluated this jurisdiction and saw the arm identifiers and model names. Model identity was therefore not blinded, although answer-inspection order was alternated; there was no second judge or inter-rater agreement check.
- Only one saved run per arm was available; there were no repeated runs.
- The 15-question suite does not support statistical inference.
- Differences cannot be attributed causally beyond the recorded model change, and the recorded deployment was not independently verified.

## 8. Findings only

The recorded results show a higher independent overall mean for arm-b, 4.55 versus 4.35, and pairwise preferences of 11 for arm-b, 2 for arm-a and 2 ties. Arm-b's advantage is primarily in precision, selective grounding and remedy analysis. Arm-a remains materially stronger on the hk-007 conflict-of-laws issue and narrowly stronger on hk-013's dispute-resolution caveat. Both arms require correction of the shared hk-005 and hk-008 errors.

This report stops at comparative findings and makes no deployment, promotion or release recommendation.
