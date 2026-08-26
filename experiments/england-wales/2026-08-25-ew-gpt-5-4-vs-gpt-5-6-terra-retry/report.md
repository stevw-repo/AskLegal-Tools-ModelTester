# England & Wales Legal Analysis Model Comparison

## Scope and tested configurations

This report evaluates the 15 saved England & Wales Legal Analysis answers in each arm using `rubrics/legal-analysis-v1.md`. Each answer was scored independently before matching answers were compared side by side. To reduce ordering bias, Arm B was inspected first for odd-numbered question IDs and Arm A first for even-numbered IDs.

- **Arm A — GPT-5.4:** `gpt-5.4`, low reasoning.
- **Arm B — GPT-5.6 Terra:** `gpt-5.6-terra`, low reasoning.

The recorded configurations are otherwise identical: routing prompt, embedding model, Pinecone index and namespace, retrieval top-k, no reranker, England & Wales v2 answer prompt, Azure endpoint and API version. Both runs saved 15 successful answers. This evaluation concerns the saved answers and does not independently verify deployment state.

## Independent mean scores

Scores use the rubric's 1–5 scale. Overall is the mean of all five dimensions across all 15 answers in that arm.

| Arm | Legal correctness | Issue coverage | Grounding & citations | Jurisdiction discipline | Usefulness & safety | Overall |
|---|---:|---:|---:|---:|---:|---:|
| Arm A — GPT-5.4 | 3.87 | 4.13 | 3.00 | 5.00 | 4.20 | 4.04 |
| Arm B — GPT-5.6 Terra | 4.47 | 4.67 | 4.13 | 4.93 | 5.00 | 4.64 |

The largest mean difference was grounding and citations, where Arm B scored 4.13 and Arm A scored 3.00. Both arms remained strongly disciplined to England and Wales.

## Pairwise preference totals

| Preferred arm | Questions |
|---|---:|
| Arm A | 1 |
| Arm B | 13 |
| Tie | 1 |
| **Total** | **15** |

Of Arm B's 13 preferences, ten were confident and three were close. Arm A's single preference was close; the tie was close.

## Question-level comparisons

| Question | Preference | Confidence | Key reason |
|---|---|---|---|
| ew-001 | Arm B | Confident | Adds the distinct ERA s 104 statutory-right dismissal route and a fuller alternative-dismissal analysis. |
| ew-002 | Arm A | Close | Both omit core 1985 provisions, but Arm A includes deposit non-protection, prescribed information and the one-to-three-times sanction. |
| ew-003 | Arm B | Confident | Gives the clearer CRA remedy sequence and expressly explains the first-six-month presumption. |
| ew-004 | Arm B | Confident | Reaches the same contract/damages result with cleaner authority and no internal-source citations. |
| ew-005 | Arm B | Confident | Leads safely with the imminent limitation issue; Arm A contains an impossible future-dated citation. |
| ew-006 | Arm B | Confident | Better separates child, CMS, spousal, housing, pension and overall-settlement regimes. |
| ew-007 | Tie | Close | Arm A catches domicile; Arm B states the cohabitant maintenance standard. Each omits one material threshold point. |
| ew-008 | Arm B | Confident | Anchors conflicts, unfair prejudice, derivative standing and reflective loss in the correct statutory routes. |
| ew-009 | Arm B | Close | Arm B is more proportionate and operationally safe; Arm A spots more special-category issues but relies on dated guidance. |
| ew-010 | Arm B | Close | Both are strong, but Arm B is cleaner, more concise and more cautious about litigation and injunctions. |
| ew-011 | Arm B | Confident | States the right of a voluntary attendee to leave and distinguishes bringing, surrendering, unlocking and extracting the phone. |
| ew-012 | Arm B | Confident | Focuses on proving the French will and obtaining the correct English grant rather than peripheral administration jurisdiction. |
| ew-013 | Arm B | Confident | Adds the debtor-status-dependent Debt Claims Protocol and a better warning against insolvency pressure. |
| ew-014 | Arm B | Close | Adds insurance-protection and limitation cautions and avoids an oversimplified court-forum threshold. |
| ew-015 | Arm B | Confident | Gives a more commercially useful German asset-preservation analysis with cleaner authority. |

## Recurring strengths and weaknesses

### Arm A — GPT-5.4

Strengths:

- Comprehensive issue spotting and detailed evidence checklists.
- Consistent England-and-Wales jurisdiction discipline.
- Frequent attention to causation, mitigation, limitation and enforcement practicality.

Weaknesses:

- Long, sometimes dated or peripheral authority lists often obscure the governing rule.
- Internal retrieval filenames are presented as authority in ew-004, ew-010 and ew-015.
- Key routes are omitted or underdeveloped in several answers, including ERA s 104, CA 2006 ss 994/996, the voluntary attendee's right to leave and the Debt Claims Protocol.
- Some procedural guidance is incomplete or overbroad, including the court-forum statement in ew-014 and cross-border choice-of-law treatment in ew-012.

### Arm B — GPT-5.6 Terra

Strengths:

- Clear separation of claims, parties, forums and remedies.
- More direct use of governing statutory provisions and leading authorities.
- Concise, safe action plans that foreground urgent deadlines and evidence preservation.
- Strong treatment of claim ownership and procedural posture in company, criminal interview and cross-border disputes.

Weaknesses:

- Some important secondary frameworks remain omitted: the principal 1985 housing duties in ew-002, the domicile threshold in ew-007, DPIA specifics in ew-009 and Hague 2005 recognition in ew-015.
- The cross-border succession answer does not fully distinguish administration law from the law governing beneficial succession.
- Several recent citations could not be verified within the supplied record.

## Critical failures

- **Arm A:** One. The ew-005 reference list cites `Ringe v Eden Springs (UK) Ltd [2112] EWHC 0014 (QB)`, an impossible future-dated citation. The substantive limitation advice in that answer remains usable, but the citation is a critical grounding failure.
- **Arm B:** None identified.

## Limitations

- No expectation file or gold answers were available.
- No retrieval logs or gateway logs were available, so citation support and retrieved context could not be checked.
- No external source checking was performed. A plausible-looking citation was not treated as proof of accuracy, and recent authorities remain unverified unless an error was internally apparent.
- One `gpt-5.6-sol` LLM judge evaluated this jurisdiction and saw the arm identifiers and model names. Model identity was therefore not blinded, although answer-inspection order was alternated; there was no second judge or inter-rater agreement check.
- There was one saved run per arm and no repeated runs, so response variability was not assessed.
- The 15-question suite is purposive and does not support statistical inference.
- The evaluation does not independently verify which recorded backend configuration was deployed.

These are findings about the saved answers only. No deployment or promotion recommendation is made.
