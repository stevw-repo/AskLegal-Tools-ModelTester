# Proposal: Australia Answer Prompt v1.1

## Applicability and safe-procedure patch

**Status:** Proposal only — not implemented  
**Prepared from:** Australia v1.0 prompt, 18-query federal–State test run,
Cloudflare answer-generation logs, and the log-informed review  
**Proposed implementation surface:**

- `prompts/australia/au-prompt-v1.0.md`, copied to a new version when
  implementation is authorised; and
- the corresponding embedded prompt in
  `AskLegal-Backend/src/prompts/aiPrompts-au.js`.

No prompt or backend file has been changed by this proposal.

## Recommendation

Make six small edits to the existing prompt. Keep the present role, source
restrictions, IRAC workflow, required headings, disclaimer, and language rules.
Do not introduce a new answer format or hard-code statutes from the test suite.

The patch has one central principle:

> A retrieved authority is a candidate source, not proof that it governs the
> user's issue.

The model must establish the jurisdiction and legal stream for every statute,
deadline, remedy, and institution before using it. If the retrieved material
does not establish a precise procedural proposition, the safe response is to
withhold that precision and direct the user to verify the operative notice or
current rule.

## Why this is the minimum useful change

The existing prompt already contains most of the necessary architecture. The
failures arose because several instructions are expressed only as general
principles:

- “do not substitute” did not require the model to identify why a statute
  applies;
- “prefer” interstate appellate authority did not state the
  *Farah/Hill* methodology;
- “do not tell the user sources are lacking” did not prevent phrases such as
  “the materials provided”;
- “concise” did not create a measurable length constraint;
- the action-plan instructions did not distinguish a primary statutory pathway
  from collateral remedies; and
- the quality check did not test institution names, decision-specific
  deadlines, empty References sections, or alternative citation forms.

The proposal changes those instructions directly. It does not add another
workflow, output section, or model call.

## Failure-to-change map

| Observed problem | Exact failure | Proposed control |
|---|---|---|
| au-002 | Victorian provisions were treated as applicable because the seller and contractual terms were Victorian. | Require the territorial, subject-matter, or choice-of-law basis for every statute; party location and contract wording are not sufficient by themselves. |
| au-009 | `Family Law Act 1975 (Cth) s 44(5)` was used for a WA de facto property deadline. | Tie each deadline to the claim's governing legal stream and prohibit analogous deadlines. |
| au-010 | Obsolete “Migration and Refugee Division” terminology and a general ART deadline/extension framework were applied to migration. | Use a named body and numeric deadline only when the material ties them to that decision type and relevant date. |
| au-012 | A subcontractors' charge displaced the ordinary Queensland payment-claim and adjudication pathway. | Require the ordinary primary pathway before collateral or exceptional remedies. |
| au-016 | The answer treated conflicting intermediate appellate authority as a free choice. | State the plainly-wrong or compelling-reason discipline expressly. |
| au-003, au-005, au-012 | The answer disclosed what “the materials provided” did not contain. | Ban direct and indirect references to retrieval, materials, source coverage, and source quantity. |
| au-006, au-015 | Cases appeared in multiple citation forms. | Require one selected citation form per case. |
| au-007 | A procedural issue was listed but not analysed as a substantive issue. | Extend the final consistency check to exclude type-C issues from the issue list. |
| Suite-wide | Thirteen answers exceeded 2,000 words and formatting rules were repeatedly broken. | Add a default 1,000–1,500-word range and a consolidated final output audit. |

## Exact proposed prompt edits

The references below use the current v1.0 Markdown prompt as the baseline.

### Edit 1 — replace Jurisdictional scope item 5

**Current text**

> 5. Where a matter is governed by Commonwealth law, do not substitute a State
> or Territory analogue, and vice versa. Where both operate on the same facts,
> address each in its own right.

**Proposed text**

> 5. **Apply, do not analogise.** Tie each statute, statutory deadline, and
> statutory remedy to the jurisdiction and legal stream governing that
> proposition. Do not substitute a Commonwealth provision, another State or
> Territory provision, or an analogous remedy merely because it is the closest
> result in `<data>`. A party's residence, incorporation, or place of business,
> and a contractual forum or governing-law clause, do not by themselves
> establish that a particular statute applies; identify the territorial,
> subject-matter, or choice-of-law basis. Where more than one law operates,
> address each separately.

#### Rationale

The existing instruction identifies the desired result but does not tell the
model how to verify applicability. The proposed wording creates an operational
test:

1. identify the legal stream;
2. identify the connection that makes the statute applicable; and
3. reject a retrieved analogue if that connection is absent.

This directly prevents the reasoning used in au-002 and au-009. It also reduces
the risk that NSW material in au-012 will be used merely because the parties or
contract are connected with NSW.

#### Risk and mitigation

The model may become too cautious about a genuinely extraterritorial statute.
The wording does not prohibit cross-border operation; it requires the model to
identify the basis for it.

---

### Edit 2 — replace Source hierarchy item 5

**Current text**

> 5. **Cross-jurisdictional weight** - A decision of another State or
> Territory's courts is persuasive rather than binding, but on the common law
> of Australia and on uniform or corresponding national legislation, an
> intermediate appellate court decision should be preferred unless a higher
> authority in `<data>` departs from it.

**Proposed text**

> 5. **Cross-jurisdictional weight** - On the interpretation of Commonwealth
> legislation, uniform national legislation, or the common law of Australia,
> neither an intermediate appellate court nor a trial judge should depart from
> a decision of another Australian intermediate appellate court unless
> convinced that the decision is plainly wrong or there is a compelling legal
> reason to do so. Do not treat the decision as optional merely because it
> comes from another jurisdiction. If coordinate appellate decisions conflict,
> identify the conflict and resolve it by this discipline, controlling High
> Court authority, the applicable statutory text, and the strength of the
> reasoning — not by unconfined preference or recency alone. Name or cite the
> authorities for this methodology only if their names and citations appear in
> `<data>`; otherwise state the methodology without attribution or citation.

#### Rationale

This supplies the rule missing from au-016. The current prompt says another
State's appellate decision “should be preferred,” but does not explain the
threshold for departure or how to handle conflicting coordinate decisions.

The formulation follows the High Court's methodology in
[*Hill v Zuda Pty Ltd* [2022] HCA 21](https://www.hcourt.gov.au/cases-and-judgments/judgments/judgments-1998-current/hill-v-zuda-pty-ltd).
The final sentence preserves the existing source-only citation restriction.

#### Risk and mitigation

The rule could be applied to materially different cases or non-uniform State
statutes. Its stated scope is limited to Commonwealth legislation, uniform
national legislation, and the common law of Australia.

---

### Edit 3 — consolidate the hidden-source rules

Replace the three Source handling rules beginning:

- “Where `<data>` does not cover an issue at all...”;
- “Never tell the user that you are relying on `<data>`...”;
- “Never reveal the quantity or nature of the sources used.”

with these two bullets:

> - Where `<data>` does not cover an issue at all, you may state the relevant
> general Australian legal principle in your own words, **without citation**.
> Do not invent authorities.
>
> - In the answer, never mention or imply `<data>`, retrieval, “materials
> provided”, “source materials”, “available material”, the source set, source
> quantity, source coverage, or what sources do or do not contain. Express any
> limitation as legal or factual uncertainty or as a direct verification step,
> and never ask the user for additional sources.

#### Rationale

The existing three instructions repeat the prohibition but do not capture the
phrases the model actually used. The replacement:

- gives an explicit output-language constraint;
- covers direct and indirect disclosures; and
- tells the model how to communicate uncertainty without revealing the hidden
  source set.

It directly addresses au-003, au-005, and au-012, with secondary benefit for
au-004, au-008, au-011, au-013, and au-015.

#### Risk and mitigation

The model must not conceal legal uncertainty. The replacement expressly
requires it to state the uncertainty as a legal or factual limitation or a
verification step.

---

### Edit 4 — replace Step 4's level-of-detail paragraph

**Current text**

> Default to the structured workflow from Step 5 onward, using the Level-2
> headers listed in the Formatting and citation section. Reserve a concise,
> non-structured answer for narrow single-point factual questions only.

**Proposed text**

> Default to the structured workflow from Step 5 onward, using the Level-2
> headers listed in the Formatting and citation section. Reserve a concise,
> non-structured answer for a narrow single-point factual question only. For an
> ordinary substantive query, normally use 1,000–1,500 words excluding
> References and the disclaimer; exceed that range only where the user requests
> a detailed memorandum or additional detail is necessary to avoid a material
> omission. State each proposition and conclusion once. Do not repeat the
> analysis in the action plan or a risk table, and use a table only where it
> materially shortens or clarifies the answer.

#### Rationale

“Concise” did not constrain the run: 13 of 18 answers exceeded 2,000 words, and
the median was about 2,280 words. The proposed range is measurable while
retaining an exception for genuinely complex questions.

#### Risk and mitigation

Complex federal–State questions may need more than 1,500 words. The exception
permits additional detail where compression would create a material omission.

---

### Edit 5 — strengthen Step 6 for primary pathways, institutions, and deadlines

Insert this paragraph after the opening paragraph of Step 6:

> Where the user asks about a named statutory scheme or process, address its
> ordinary primary pathway first. Treat collateral, exceptional,
> insolvency-related, or enforcement remedies as separate options, never as
> substitutes for the primary pathway.

Replace the current forum and deadline bullets with:

> - the appropriate **forum**, identified by jurisdiction. Use a specific body,
> division, or jurisdictional-area name only where `<data>` ties that name to
> the user's type of decision and the relevant date. If the sources conflict
> between legacy and current structures, do not blend them; describe the review
> body generically and direct the user to the operative decision notice;
>
> - **limitation periods and statutory deadlines** — state a numeric period,
> trigger date, extension power, or citation only where `<data>` expressly ties
> it to the particular decision or claim and its governing legal stream. Never
> transfer a general tribunal rule, another claim type's deadline, or another
> jurisdiction's period. If the exact rule is not established, do not guess:
> tell the user to act urgently and verify the operative notice or current rule;

#### Rationale

The primary-pathway sentence prevents the au-012 pattern: a subcontractors'
charge cannot stand in for the ordinary payment-claim, payment-schedule, and
adjudication route.

The forum and deadline bullets prevent:

- a federal deadline being used for a WA claim in au-009;
- stale AAT terminology being blended with the ART in au-010; and
- a general ART period or extension provision being applied to a migration
  decision.

The intended safe failure mode is an urgent verification instruction, not a
precise but unsupported deadline.

#### Risk and mitigation

When retrieval is incomplete, the answer will sometimes be less specific.
That is safer for strict deadlines than transferring a nearby rule. The
retrieval proposal addresses the missing-coverage side separately.

---

### Edit 6 — make the final output audit mechanical

#### 6A. Replace the bolding instruction

**Current**

> - **Bold** key terms.

**Proposed**

> - **Bold** short analytical labels or key non-citation terms sparingly. Never
> bold or italicise legislation or a citation; italicise a case name only.

#### 6B. Replace the References instruction

**Current**

> - Use inline citations and end with a `## References` section. List every
> authority cited inline once only, using an unnumbered bullet list. List
> legislation first, followed by cases. Do not bold citations; italicise case
> names only. For legislation, combine all cited provisions from the same
> instrument into one reference entry.

**Proposed**

> - Use inline citations and, only if at least one authority is cited, end with
> a `## References` section. List every authority cited inline once only, using
> an unnumbered bullet list. List legislation first, followed by cases. Select
> one citation form for each case, preferring an authorised report where
> available. Do not bold citations; italicise case names only. For legislation,
> combine all cited provisions from the same instrument into one reference
> entry.

#### 6C. Replace Quality check item 1

> 1. **Citation and reference audit** - every substantive citation component
> comes from `<data>`; every legislation citation has title, jurisdiction, and
> pinpoint; each case uses one selected citation form; legislation is plain
> text and only case names are italicised; every inline authority appears once
> in References; and References is omitted if no authority is cited. Remove
> incomplete, inferred, duplicate, alternative-form, source-description, or
> meta-comment entries.

#### 6D. Replace Quality check item 2

> 2. **Consistency** - only substantive and remedial/standing issues appear
> under Legal Issues Identified; every analysed issue matches that list exactly
> in item, numbering, and order; procedural issues appear only in the action
> plan.

#### 6E. Replace Quality check item 5

> 5. **Jurisdiction and applicability** - for every statute, deadline, and
> remedy, confirm the governing legal stream and the factual or legal connection
> that makes it applicable. No Commonwealth/State or interstate substitution
> has occurred; a party location, contract clause, or appearance in `<data>` is
> not treated as sufficient by itself. Confirm that any date-sensitive
> institution name or procedure applies to the user's decision and date.

#### 6F. Add Quality check item 7

> 7. **Hidden-source and concision audit** - remove every reference to
> retrieval, materials, sources, source coverage, or missing source content.
> Remove repeated propositions and conclusions, and keep the answer within the
> default length unless an exception applies.

#### Rationale

These mechanical checks address:

- alternative citations in au-006 and au-015;
- bolded and italicised legislation across the suite;
- the meta-reference in au-016;
- the issue/analysis mismatch in au-007;
- repeated disclosure of the hidden source set; and
- excessive length.

They also resolve the present tension between “end with References” and an
answer that cites no authority.

## Recommended implementation sequence

1. Create `prompts/australia/au-prompt-v1.1.md` rather than overwriting the
   tested v1.0 prompt.
2. Apply the six edits exactly, without adding test-specific statute names.
3. Mirror the complete prompt into `src/prompts/aiPrompts-au.js`.
4. Update the backend prompt-version assertion if the heading changes to v1.1.
5. Deploy the answer-prompt change together with the retrieval change, so the
   next suite run tests the combined mitigation.
6. Run the unchanged 18-query suite with parallelism 5.
7. Export the same Cloudflare answer-generation logs for comparison.

## Regression tests and acceptance criteria

### Critical answer-safety gates

| Query | Acceptance criterion |
|---|---|
| **au-002** | No Victorian statute is applied unless the answer establishes a territorial or choice-of-law basis. The forum clause is kept distinct from governing and mandatory law. |
| **au-009** | The WA de facto deadline is sourced only to the WA legal stream. `Family Law Act 1975 (Cth) s 44(5)` is not used as a proxy. |
| **au-010** | No “Migration and Refugee Division” or “MRD”; no general ART deadline or extension rule is applied to migration. If the exact rule is unavailable, the answer directs the user to the decision notice without guessing. |
| **au-012** | The ordinary Queensland payment-claim, payment-schedule, and adjudication route is addressed before charges or insolvency remedies. NSW legislation is not used merely because of incorporation or the contract. |
| **au-016** | The answer applies the plainly-wrong or compelling-reason discipline and does not describe the choice as an unconfined legal preference. No empty or meta-only References section appears. |

### Suite-wide gates

- Zero answer matches for:
  - `<data>`;
  - “materials provided”;
  - “source materials”;
  - “available material”;
  - “retrieved sources”;
  - “source set”; or
  - any statement about what hidden sources contain or omit.
- Each case uses one formal citation form only.
- Legislation is neither bolded nor italicised.
- References is omitted when no authority is cited.
- Every authority cited inline appears once in References.
- Every substantive answer has an exact issue/analysis item match.
- No type-C procedural item appears under Legal Issues Identified.
- The median substantive answer is no more than 1,500 words.
- No substantive answer exceeds 2,000 words unless the query expressly asks
  for a detailed memorandum or the review records a material-omission reason.
- Every answer contains exactly one disclaimer.

### Positive regressions to preserve

- au-013 continues to explain constitutional inconsistency accurately.
- au-017 and au-018 continue to ask for the missing State or Territory before
  giving State-specific advice.
- au-014 and au-015 continue without requesting a State unnecessarily.
- Required heading order and same-language output remain unchanged.

## Expected effect

The patch should turn unsupported precision into cautious, usable advice:

- wrong-jurisdiction statutes and deadlines should be omitted rather than
  transferred;
- stale or conflicting institution names should not be blended;
- primary statutory pathways should not be displaced by nearby remedies;
- interstate common-law authority should be treated under the correct
  methodology; and
- answers should become materially shorter and easier to audit.

The expected improvement is not that the prompt will manufacture missing legal
coverage. It is that the model will use retrieved material only when its
applicability has been established and will fail safely when it has not.

## What this proposal cannot solve

Prompt wording cannot supply a missing statute, current tribunal provision, or
case. Even after this patch:

- au-003 still needs Commonwealth environmental material;
- au-004 still needs the federal Notifiable Data Breaches provisions;
- au-005 still needs operative federal pregnancy-discrimination and process
  material;
- au-006 still needs limitation and concerns-notice material;
- au-011 still needs South Australian territorial/offence law and the federal
  double-punishment provision;
- au-012 still needs the ordinary Queensland security-of-payment provisions;
  and
- au-016 needs *Farah/Hill* retrieval for a fully cited answer.

Those gaps are addressed, as far as a minimal runtime change can address them,
in the separate retrieval proposal. Corpus omissions or substantively stale
source text require corpus-side work and are outside this proposal.

## Rollback

The change is prompt-only. Rollback consists of redeploying the unchanged v1.0
prompt. No data, index, API, or persistence migration is involved.
