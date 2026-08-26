# Australia Legal Analysis Model Comparison

## Scope and tested configurations

This report evaluates 15 saved Australia Ask.Legal Legal Analysis answers from each arm using `rubrics/legal-analysis-v1.md`. Answers were scored independently before each matching pair was compared. For odd-numbered question IDs, arm B was inspected first; for even-numbered IDs, arm A was inspected first.

The experiment compares **GPT-5.4** (arm A) with **GPT-5.6 Terra** (arm B). Both were recorded with **low reasoning effort** and otherwise identical configuration: `intent-router-current`, `text-embedding-3-small`, Pinecone index `ask-legal-chatbot-au-dataset-v2` in the default namespace, retrieval top-k 8, no reranker, and answer prompt `australia-v1.1`. The recorded configuration differs only in the model field.

This is a saved-answer evaluation, not legal advice. It does not verify what was deployed beyond the experiment records.

## Independent scores

Scores are arithmetic means across the 15 independently assessed answers. Overall is the mean of all 75 dimension scores for the arm.

| Arm | Legal correctness | Issue coverage | Grounding and citations | Jurisdiction discipline | Usefulness and safety | Overall |
|---|---:|---:|---:|---:|---:|---:|
| Arm A — GPT-5.4 | 3.67 | 4.20 | 3.13 | 4.60 | 4.27 | 3.97 |
| Arm B — GPT-5.6 Terra | 3.93 | 4.33 | 3.47 | 4.73 | 4.80 | 4.25 |

## Pairwise preference totals

| Preferred result | Questions |
|---|---:|
| Arm A — GPT-5.4 | 5 |
| Arm B — GPT-5.6 Terra | 6 |
| Tie | 4 |
| **Total** | **15** |

## Question-level comparisons

| Question | Preference | Confidence | Key reason |
|---|---|---|---|
| au-001 | Arm A | Close | Both are strong; arm A states the 21-day general-protections dismissal deadline directly. |
| au-002 | Tie | Close | Both give sound leak-causation and evidence analysis and share the same overbroad 14-day VCAT formulation. |
| au-003 | Arm B | Confident | Arm B cites the central ACL goods remedies and adds Queensland sale-of-goods law; arm A omits both and detours into motor-vehicle jurisdiction. |
| au-004 | Arm A | Confident | Arm A addresses the NSW 10% deposit cap and ACL misrepresentation; arm B omits the salient deposit issue. |
| au-005 | Tie | Close | Arm A gives more limitation detail but includes a questionable s 48 formulation; arm B is cleaner but thinner on applicable SA law. |
| au-006 | Arm B | Confident | Arm B gives a useful conditional family-law analysis; arm A only requests clarification and does not answer the question. |
| au-007 | Arm A | Confident | Arm A includes the statutory-legacy threshold; arm B's omission can materially change the stated inheritance result. |
| au-008 | Arm B | Close | Both identify the right remedies, but arm B maps personal, derivative, constitutional and injunctive routes more clearly. |
| au-009 | Tie | Close | Arm A is stronger on after-hours surveillance; arm B is broader on overlapping privacy and surveillance statutes. |
| au-010 | Arm B | Confident | Arm B correctly treats serious harm as an element; arm A incorrectly presents it as a defence under the wrong provisions. |
| au-011 | Arm A | Confident | Arm A identifies the specific s 464C custodial legal-advice protection; arm B relies mainly on the admissions provision in s 464J. |
| au-012 | Arm B | Close | Arm B is more precise on will validity, asset situs, broker requirements and tax, while arm A adds remote procedural detours. |
| au-013 | Arm A | Close | Both are strong; arm A adds ACAT's own-costs rule and exceptions. |
| au-014 | Tie | Close | Both give useful causation and tax-review workflows but neither grounds the core review and NSW negligence rules adequately. |
| au-015 | Arm B | Close | Both cover the main issues; arm B is more focused, although neither identifies the statutory interstate judgment-registration mechanism. |

## Recurring strengths and weaknesses

### Arm A — GPT-5.4

Strengths:

- Frequently detailed issue spotting, evidence preservation and practical next steps.
- Strong treatment of selected statutory details, notably the NSW building deposit cap, Victorian intestacy threshold and Victorian custodial legal-advice right.
- Generally disciplined separation of Commonwealth and State issues.

Weaknesses:

- Often overlong, with peripheral case and statutory discussion obscuring the principal answer.
- Two material reliability failures: a non-answer on family law and an incorrect serious-harm proposition in defamation.
- Several answers omit the principal statutory provisions while citing peripheral authorities.

### Arm B — GPT-5.6 Terra

Strengths:

- Consistently clear, proportionate structure and strong practical action plans.
- Good use of transparent assumptions and conditional analysis where facts are missing.
- Strong jurisdiction discipline and comparatively reliable treatment of central statutory schemes.

Weaknesses:

- Occasionally omits a dispositive qualifier or salient issue, particularly the Victorian statutory-legacy threshold and NSW building deposit cap.
- Grounding is thin in some areas, including statutory directors' duties, NSW professional negligence and interstate judgment enforcement.
- Some requested defences or procedural details are compressed too aggressively.

## Critical failures

Arm A has two listed critical failures:

- **au-006:** It did not answer the substantive family-law question and only requested relationship-status clarification, despite being able to provide conditional married and de facto analysis.
- **au-010:** It materially misstated serious harm as a defamation defence under ss 33 and 39 and relied on a 2019 case for that proposition.

Arm B has **no listed critical failures**.

## Limitations

- No expectation file or gold answers were available.
- No retrieval or gateway logs were available, so retrieved support and citation provenance could not be assessed.
- No external source checking was performed. A citation was not assumed accurate merely because it looked plausible.
- One `gpt-5.6-sol` LLM judge evaluated this jurisdiction and saw the arm identifiers and model names. Model identity was therefore not blinded, although answer-inspection order was alternated; there was no second judge or inter-rater agreement check.
- Each arm has only one saved run; there were no repeated runs to assess variability.
- The 15-question suite does not support statistical inference or causal attribution beyond the recorded configuration difference.

## Findings only

Arm B has the higher overall mean, 4.25 versus 3.97, and leads the pairwise count 6 to 5 with 4 ties. Its clearest advantages are substantive conditional analysis and avoidance of arm A's two material reliability failures. Arm A's clearest advantages are selected statutory details that arm B omitted. These are comparative findings only; this report makes no deployment or promotion recommendation.
