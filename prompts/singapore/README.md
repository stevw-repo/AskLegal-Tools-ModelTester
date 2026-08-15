# Ask.Legal Singapore Prompt Context

## Purpose

Ask.Legal Singapore is being prepared as a prompt-engineering experiment. The goal is to test whether the Singapore answer-generation prompt should be based on the existing Hong Kong prompt or the existing England & Wales prompt.

This folder therefore preserves two Singapore variants:

- `sg-prompt-v1.0-a.md` - Singapore prompt adapted from `prompts/hong-kong/hk-prompt-v1.0.md`.
- `sg-prompt-v1.0-b.md` - Singapore prompt adapted from `prompts/england-wales/ew-prompt-v5.0.md`.

No pipeline, retrieval, database, or application-layer changes are in scope for this work.

## Design Principle

Both variants should answer only Singapore law questions and should use Singapore legal terminology:

- Use "Singapore law", "Singapore legislation", "Acts", "subsidiary legislation", "rules", "Practice Directions", and "Singapore case law".
- Use "Singapore-qualified lawyer" or "advocate and solicitor of Singapore" rather than "Hong Kong barrister" or "English lawyer".
- Use "customer" or "user" consistently with the source prompt style.
- Do not refer to Hong Kong ordinances, UK legislation, England & Wales courts, or non-Singapore official legislation websites.

## Singapore Sources and Citation Assumptions

The prompts are written for a retrieval setting where relevant authorities appear inside the `<data>` tag.

Key official public references for Singapore law are:

- Singapore Statutes Online: https://sso.agc.gov.sg/
- Singapore Courts judgments page: https://www.judiciary.gov.sg/judgments
- Singapore Courts public site: https://www.judiciary.gov.sg/
- Singapore Law Watch, operated by the Singapore Academy of Law, may be useful as a legal current-awareness and judgment-discovery source: https://www.singaporelawwatch.sg/

Prompt-level citation policy should remain conservative:

- Cite statutes, cases, Practice Directions, rules, and other legal authorities only where the formal citation or official title appears in `<data>`.
- If the model relies on general Singapore legal knowledge because `<data>` does not cover an issue, state the principle in plain terms without inventing a citation.
- Do not tell users that `<data>` was empty or insufficient.
- Do not fabricate Act names, section numbers, neutral citations, court references, or URLs.
- Quote statutory text only where the exact text appears in `<data>` or in the user's own query.

## Court Hierarchy Guidance

Where authorities conflict or overlap, prefer Singapore authorities and use hierarchy before recency. The prompt should use this as internal reasoning, not as user-facing explanation unless relevant.

General hierarchy for prompt purposes:

1. Court of Appeal of Singapore.
2. Appellate Division of the High Court, where relevant.
3. General Division of the High Court / High Court.
4. Specialist Singapore courts or divisions where directly relevant, including the Singapore International Commercial Court and the Family Division of the High Court.
5. State Courts, Family Courts, tribunals, boards, and administrative bodies, subject to their statutory role and relevance.

Factual similarity and recency remain tie-breakers after hierarchy.

## Variant A - HK-Derived

Variant A intentionally keeps the Hong Kong prompt's lighter structure:

- Concise default answer style.
- Structured IRAC only where useful.
- More compact workflow.
- Less rigid issue classification.

This variant tests whether the HK prompt's pragmatic, flexible style transfers well to Singapore law.

## Variant B - E&W-Derived

Variant B intentionally keeps the England & Wales prompt's stricter structure:

- Stronger grounding rules.
- Mandatory issue control for substantive and remedial issues.
- Forum, procedure, deadlines, forms, and next steps kept in `## Recommended Action Plan`.
- Analysis issues must match the issues identified.
- More explicit quality checks.

This variant tests whether the E&W prompt's more disciplined authority handling and output structure improves Singapore answers.

## Evaluation Notes

When testing the two variants, compare:

- Citation accuracy and whether all citations are present in `<data>`.
- Whether the answer avoids hallucinated Singapore statutes, sections, case names, and court references.
- Whether the prompt handles missing facts by asking for clarification only when facts are material.
- Whether procedure and forum guidance is kept separate from legal-rule analysis.
- Whether the final answer is useful to both lay users and commercial users.
- Whether the mandatory disclaimer appears once and only once.
