# Ask.Legal Australia Prompt Context

## Purpose

`au-prompt-v1.0.md` is the first Australian answer-generation prompt. It is derived from `prompts/singapore/sg-prompt-v1.4.md`, which is itself the England & Wales-derived Singapore variant (`sg-prompt-v1.0-b.md`) after four rounds of citation-discipline refinement. The Australian prompt therefore inherits the E&W structural discipline and the Singapore citation-audit work in a single lineage.

No pipeline, retrieval, database, or application-layer changes are in scope for this work.

## Design Principle

The prompt answers Australian law questions only and uses Australian legal terminology:

- Use "Australian law", "Commonwealth legislation", "State and Territory legislation", "Acts", "delegated legislation", "regulations", "court rules", "Practice Notes", and "Australian case law".
- Use "Australian legal practitioner", "solicitor", or "barrister" rather than "Singapore-qualified lawyer", "Hong Kong barrister", or "English lawyer".
- Do not refer to Singapore Acts, Hong Kong ordinances, UK or England & Wales legislation and courts, or non-Australian official legislation websites, except where an overseas authority appears in `<data>` as persuasive support for an Australian principle.

## Federal Structure - the Principal Adaptation

This is the material difference from the Hong Kong, England & Wales, and Singapore prompts, each of which addresses a single unified jurisdiction. Australia is a federation, so the prompt carries a dedicated `## Jurisdictional scope` section plus jurisdiction checks in Step 1, Step 3(a), Step 5, and quality check 5.

The chosen approach is **all-Australia with inference**:

- The prompt covers the Commonwealth and all eight States and Territories.
- It identifies the governing jurisdiction from the query facts and `<data>`, and names it in the answer wherever more than one could apply.
- It asks the user which State or Territory applies **only** where that choice is determinative - limitation periods, civil liability and negligence, residential tenancies, workers' compensation, land and conveyancing, stamp duty, criminal offences, defamation procedure.
- It does not ask where the governing law is Commonwealth, uniform across jurisdictions, or the general common law of Australia.
- It must not substitute a Commonwealth provision for a State or Territory analogue, or the reverse.

The common law of Australia is treated as a single body of law; State and Territory statutes are not.

## Court Hierarchy Guidance

Used as internal reasoning, not as user-facing explanation unless relevant.

1. High Court of Australia.
2. Intermediate appellate courts: Full Court of the Federal Court of Australia; State and Territory Courts of Appeal, Full Courts of the Supreme Courts, and Courts of Criminal Appeal.
3. Federal Court of Australia (single judge); State and Territory Supreme Courts.
4. Federal Circuit and Family Court of Australia; District and County Courts.
5. Local, Magistrates, and Children's Courts.
6. Tribunals, boards, commissions, and administrative bodies, subject to their statutory role and relevance: the Administrative Review Tribunal, the Fair Work Commission, and the State and Territory civil and administrative tribunals.

Two Australia-specific rules sit alongside the ladder:

- **Cross-jurisdictional weight.** Another State or Territory's decisions are persuasive rather than binding, but on the common law of Australia and on uniform or corresponding national legislation an intermediate appellate decision is preferred unless higher authority in `<data>` departs from it.
- **Overseas authority.** English, New Zealand, and Canadian authorities may be used only where they appear in `<data>` and only as persuasive support - never presented as the governing law of Australia.

Factual similarity and recency remain tie-breakers after hierarchy.

## Citation Style - AGLC

The prompt prescribes AGLC forms, at the depth Singapore v1.4 reached:

- Commonwealth Act: `Corporations Act 2001 (Cth) s 181(1)`
- State or Territory Act: `Civil Liability Act 2002 (NSW) s 5B(1)`
- Delegated legislation: `Corporations Regulations 2001 (Cth) reg 7.1.29`
- Court rules: `Uniform Civil Procedure Rules 2005 (NSW) r 14.28`
- Constitution: `Australian Constitution s 51(xx)` - the only citation without a year or jurisdiction marker
- Case, reported: `*Farah Constructions Pty Ltd v Say-Dee Pty Ltd* (2007) 230 CLR 89, 151`
- Case, medium neutral: `*Farah Constructions Pty Ltd v Say-Dee Pty Ltd* [2007] HCA 22, [134]`

Three rules deserve attention in testing because they are new relative to Singapore v1.4:

1. **Mandatory jurisdiction marker.** Every legislation citation must carry `(Cth)`, `(NSW)`, `(Vic)`, `(Qld)`, `(WA)`, `(SA)`, `(Tas)`, `(ACT)`, or `(NT)`, established from `<data>`. A title without a jurisdiction marker is ambiguous in a federation and must be omitted rather than guessed.
2. **Report series versus medium neutral.** Where `<data>` gives both, prefer the authorised report series. Where it gives one, use that one. The model must not convert between forms, because doing so requires supplying a volume, page, year, or court identifier it does not have.
3. **Pinpoint punctuation splits by source type.** No comma before a legislative pinpoint (`s 181`); a comma before a case pinpoint, page for reported (`230 CLR 89, 151`) and bracketed paragraph for medium neutral (`[2007] HCA 22, [134]`). This differs from the Singapore `at [12]` convention and is a likely early failure mode.

Party-name handling is grounding-safe by design: the prompt retains the party form as it appears in `<data>` (`R v`, `The King v`, `The Queen v`, `DPP v`, `Re`, `Ex parte`, `[No 2]`) rather than modernising it, so the model never has to infer the date of a decision from its style of cause.

## Sources and Citation Assumptions

The prompt is written for a retrieval setting where relevant authorities appear inside the `<data>` tag. Key official public references for Australian law are:

- Federal Register of Legislation: https://www.legislation.gov.au/
- AustLII: https://www.austlii.edu.au/
- High Court of Australia: https://www.hcourt.gov.au/
- Federal Court of Australia: https://www.fedcourt.gov.au/
- New South Wales: https://legislation.nsw.gov.au/
- Victoria: https://www.legislation.vic.gov.au/
- Queensland: https://www.legislation.qld.gov.au/
- Western Australia: https://www.legislation.wa.gov.au/
- South Australia: https://www.legislation.sa.gov.au/
- Tasmania: https://www.legislation.tas.gov.au/
- Australian Capital Territory: https://www.legislation.act.gov.au/
- Northern Territory: https://legislation.nt.gov.au/

Following Singapore v1.4, the prompt itself contains no URL guidance - v1.0-b's "you may point to the official homepage" line was removed at v1.4 and is not reinstated here. The list above is reference material for prompt engineers, not prompt content.

Prompt-level citation policy remains conservative:

- Cite legislation, delegated legislation, court rules, and cases only where the required components appear in `<data>`.
- If the model relies on general Australian legal knowledge because `<data>` does not cover an issue, state the principle in plain terms without inventing a citation.
- Do not tell users that `<data>` was empty or insufficient.
- Do not fabricate Act names, jurisdiction markers, section numbers, medium neutral citations, report series references, court identifiers, or URLs.
- Quote statutory text only where the exact text appears in `<data>` or in the user's own query.

## Evaluation Notes

When testing v1.0, compare against the Singapore baseline on the shared criteria - citation accuracy and grounding, hallucinated authorities, clarification behaviour on missing material facts, separation of procedure from rule analysis, usefulness to both lay and commercial users, and a single disclaimer - and add the Australia-specific checks:

- Whether the governing jurisdiction is correctly identified and named where more than one could apply.
- Whether the model asks for the State or Territory when, and only when, that choice is determinative.
- Whether any Commonwealth provision is applied to a matter governed by State or Territory law, or the reverse.
- Whether any State or Territory statute is applied to facts arising in a different State or Territory.
- Whether every legislation citation carries a jurisdiction marker drawn from `<data>`.
- Whether report series and medium neutral citations are used as supplied, without conversion between forms.
- Whether case pinpoint punctuation follows the AGLC split rather than the Singapore `at [12]` convention.

## Open Items

- **Chinese-language disclaimer.** Carried over unchanged from Singapore and England & Wales. Confirm whether it is wanted for the Australian deployment before v1.1.
- **Test suite.** No `testing/suites/australia/` suite exists yet. A general query suite modelled on `testing/suites/singapore/sg-general-v1.json` should deliberately over-sample federal/State boundary questions, since that is the untested part of this prompt.
