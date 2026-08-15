# Proposal: Australian Retrieval

## Scope-safe coverage and diversity selector

**Status:** Read-only proposal — not implemented  
**Implementation baseline inspected:** `origin/develop/main` at
`e672c9284b030963b1a07c0e35af3cbcb3f324e4`  
**Primary change surface:**

- `src/services/australianRetrievalService.js`
- `src/test/australianRetrievalService.test.js`
- two added instructions in the existing Australian query-analysis prompt in
  `src/prompts/aiPrompts-au.js`
- optionally, one selection-summary callback in
  `src/services/legalQuestionService.js`

No backend, corpus, index, prompt, or pipeline file has been changed by this
proposal.

## Recommendation

Keep the current query-analysis model and three-field JSON contract, one
refined-question embedding, Pinecone index, `topK=18` candidate query,
six-source answer budget, and `principle` fallback. Add only two
query-refinement instructions concerning geographic connections and currency.

Replace only this behaviour:

```javascript
const matches = validCandidates.slice(0, AUSTRALIAN_RESULT_TOP_K);
```

with a deterministic selector that:

1. prevents a candidate whose only overlap is the shared `CTH` code from
   entering the initial Pinecone result, and repeats the same rule as an
   application-level validation check;
2. reserves distinct final-result slots for the requested jurisdictions when
   the scope can fit within six results;
3. removes exact duplicate content and caps repetitive identical topics;
4. prefers the newest record only when otherwise-equivalent records have the
   same jurisdiction/topic fingerprint;
5. makes a conditional, same-embedding supplemental query only for a requested
   jurisdiction missing from the initial 18 candidates; and
6. preserves the existing best-effort `principle` requirement without breaking
   the new coverage guarantees.

This is a deterministic selection change, not a reranker. It adds no model
call, no new embedding, no corpus field, no namespace, and no change to the
six-source prompt budget.

## Why this is the minimum useful retrieval change

The current pipeline already over-fetches 18 candidates but discards that
advantage by taking the first six valid records. The review shows that the
selection step, not only semantic search, is a material failure point:

- au-003 returned six WA sources and no Commonwealth environmental source;
- au-011 returned irrelevant cybercrime material but no South Australian
  threatening-message/territorial source or federal double-punishment source;
- au-012 concentrated on charges and generic/NSW material instead of the
  ordinary Queensland process;
- au-016 used all six slots on the same wrong interlocutory-appeal topic; and
- au-010 and au-011 contained same-topic duplicate or near-duplicate records.

The current implementation has already paid the latency and token-independent
cost of retrieving 18 candidates. A smarter deterministic choice from those 18
is therefore the smallest change with meaningful coverage upside.

## Exact current failure mechanisms

### 1. Shared `CTH` creates false cross-State eligibility

The current Pinecone filter is:

```javascript
{
    jurisdiction: { $in: jurisdictions }
}
```

The application-level scope check repeats the same “any code intersects”
semantics:

```javascript
match.metadata.jurisdiction.some((code) => jurisdictions.includes(code))
```

For a query scoped to `["CTH", "NSW"]`, a record tagged
`["CTH", "WA"]` passes through the common `CTH` value even though its specific
State treatment is WA.

This issue was already identified in the retrieval design document. The
existing `outside_search_scope` check does not correct it.

### 2. The final six have no jurisdiction-coverage requirement

After validation, the first six candidates win. A lower-ranked Commonwealth,
State, or Territory source is ignored even when the question expressly asks
for that legal stream.

### 3. Deduplication does not protect the main six

`getMatchDedupeKey()` is used only when considering a supplemental
`principle`. It prefers record ID, so identical text under different IDs is not
deduplicated. There is no topic-level diversity control for the first six.

### 4. `Current to` is unused

The selected source text contains a `Current to:` field, but final selection
does not use it. A globally newer-is-better rule would be unsafe because old
constitutional or common-law material may remain authoritative. A narrow
same-topic tie-break is safer.

## Proposed behaviour

### Stage 0 — add two query-refinement instructions

Add these two system messages to the existing Australian
`queryAnalysisPrompt` without changing its JSON schema:

> A party's residence, headquarters, incorporation, payroll location,
> contractual forum, governing-law clause, or document location does not by
> itself establish that jurisdiction's substantive law. Include a State or
> Territory only when its substantive law, procedure, or forum is genuinely
> part of the research question. Treat a contractual forum or governing-law
> clause as an issue to investigate, not proof that the nominated law applies.

> If the user asks about present rights and supplies no historical date, frame
> the research question in terms of current law. Preserve every material event,
> decision, separation, injury, or filing date, and do not convert a historical
> question into a current-law question.

#### Why these two lines are part of retrieval

The refined question, rather than the raw last message, is embedded. A false
geographic inference or omitted currency requirement therefore affects
semantic retrieval before the selector runs.

The first line reduces au-002-style retrieval driven by a party's location
rather than the legal issue. It still permits VIC where the Victorian clause
or forum genuinely requires research; it merely stops treating that fact as
proof that Victorian substantive law applies.

The second line makes current procedure explicit for au-010-type questions
without adding a date field, another model call, or another embedding. It does
not permit dropping a historical event date.

### Stage 1 — make the Pinecone filter State-safe

Replace the current any-code `$in` filter with a filter that distinguishes
genuine CTH-only material from mixed Commonwealth/other-State material.

Add:

```javascript
const AUSTRALIAN_STATE_TERRITORY_CODES =
    AUSTRALIAN_JURISDICTION_CODES.filter((code) => code !== "CTH");
```

For a narrowed query such as `["CTH", "QLD"]`, build:

```javascript
{
    $or: [
        { jurisdiction: { $in: ["QLD"] } },
        {
            $and: [
                { jurisdiction: { $in: ["CTH"] } },
                {
                    jurisdiction: {
                        $nin: AUSTRALIAN_STATE_TERRITORY_CODES
                    }
                }
            ]
        }
    ]
}
```

This admits:

- QLD-only and CTH+QLD records through the first branch;
- genuinely CTH-only records through the second branch; and
- all-nine general records through the first branch because they contain QLD.

It excludes VIC-only and CTH+VIC records from a QLD search.

Special cases:

```text
all nine query codes → retain the current broad all-nine filter
CTH-only query       → CTH present AND no State/Territory present
one or more States   → requested-State intersection OR genuine CTH-only
```

Use the resulting scope filter inside
`buildAustralianSourceTypeFilter()` so the supplemental `principle` query has
identical semantics.

Pinecone supports string-list metadata with `$in`, `$nin`, `$and`, and `$or`.
The implementation should nevertheless confirm the exact filter against the
populated development index before deployment:
[Pinecone metadata-filter documentation](https://docs.pinecone.io/guides/search/filter-by-metadata).

#### Why filter before `topK=18`

Application-only rejection would still let unrelated CTH+other-State records
consume the 18 Pinecone result positions. Filtering first gives semantically
relevant CTH-only and requested-State records the opportunity to enter the
candidate set. The next stage repeats the rule in code as defence in depth.

### Stage 2 — mirror State-safe compatibility in application code

Add a pure helper:

```javascript
isAustralianScopeCompatible(recordJurisdictions, queryJurisdictions)
```

with these rules:

1. If the query scope is all nine codes, retain the existing broad-recall
   behaviour.
2. If the query is exactly `["CTH"]`, accept only a record whose jurisdiction
   array is exactly `["CTH"]`.
3. For a query containing one or more States/Territories:
   - accept a `["CTH"]`-only record;
   - accept a record containing at least one requested State/Territory;
   - accept a general all-nine record because the corpus contract deliberately
     uses it as an unknown/general-scope fallback; and
   - reject a record whose only intersection is `CTH` and whose specific
     State/Territory codes are all outside the query.

Pseudocode:

```javascript
const isAustralianScopeCompatible = (recordCodes, queryCodes) => {
    if (queryCodes.length === AUSTRALIAN_JURISDICTION_CODES.length) {
        return true;
    }

    if (queryCodes.length === 1 && queryCodes[0] === "CTH") {
        return recordCodes.length === 1 && recordCodes[0] === "CTH";
    }

    const queryStates = queryCodes.filter((code) => code !== "CTH");
    const recordStates = recordCodes.filter((code) => code !== "CTH");

    if (recordStates.length === 0) {
        return recordCodes.includes("CTH");
    }

    return recordStates.some((code) => queryStates.includes(code));
};
```

Change the final scope branch in
`getAustralianMatchRejectionReason()` to use this helper. Use a specific
reason such as:

```text
outside_specific_scope
```

instead of treating the record as generically outside scope.

#### Why this solves the shared-CTH problem

`["CTH", "WA"]` no longer passes a `["CTH", "NSW"]` query through `CTH`,
even if a Pinecone filtering inconsistency or future query change returns it.
`["CTH"]`, `["NSW"]`, `["CTH", "NSW"]`, and the all-nine general fallback
remain eligible.

#### Important au-002 limitation

If the query-analysis model legitimately includes both QLD and VIC because the
Victorian seller and contractual clause are legally relevant, Victorian
material remains eligible. Retrieval should not decide governing law. The
answer-prompt applicability gate is what prevents that material from being
applied without a legal basis. The two proposals are intentionally
complementary.

### Stage 3 — build a shape-independent candidate profile

Selection needs only source text and the existing outer jurisdiction array.
Isolate record-envelope differences behind one accessor:

```javascript
getAustralianMatchText(match)
```

It should return the text already validated for answer handoff:

- current legacy path: parsed `_node_content.text`;
- v2 path after record-shape alignment: `metadata.text`.

The selection semantics do not depend on which envelope supplies the text.

From the text, extract only the controlled Context fields:

```text
Jurisdiction:
Topic:
Current to:
```

Build:

```javascript
{
    match,
    originalRank,
    jurisdictions,
    normalizedText,
    exactContentKey,
    topicFingerprint,
    currentToDate,
    sourceTypes
}
```

Recommended keys:

- `exactContentKey`: a hash of case-folded, whitespace-normalised complete
  text;
- `topicFingerprint`: case-folded, whitespace-normalised
  `Jurisdiction + Topic`;
- `currentToDate`: parsed date or `null`.

If Topic is absent, fall back to a unique ID-based fingerprint so unrelated
records are not accidentally collapsed.

### Stage 4 — remove exact duplicates and control topic repetition

Apply two conservative rules:

1. Keep only one candidate for an identical `exactContentKey`.
2. Permit at most two final records with the same `topicFingerprint` while a
   different-topic eligible candidate remains available.

When candidates share a topic fingerprint:

1. prefer the candidate with the newer valid `Current to` date;
2. otherwise preserve Pinecone rank.

If the topic cap leaves fewer than six results after all distinct topics are
exhausted, relax the cap and fill from the remaining candidates in original
rank order. Relevance is therefore not sacrificed merely to return fewer
sources.

#### Why cap at two rather than one

The distillation contract creates paragraph-level records. Two records under
one Topic may contain complementary rules or authorities. A cap of one risks
discarding a necessary companion paragraph. A cap of two would have freed four
of the six au-016 slots while preserving room for a companion source.

### Stage 5 — reserve jurisdiction coverage

For a non-broad query whose number of requested codes is six or fewer, reserve
one distinct candidate per requested code when candidates exist.

The query normally includes CTH, so this supports up to five requested
States/Territories within the existing six-result budget.

Use these deterministic rules:

1. Process requested codes in canonical order.
2. For CTH, reserve the highest-ranked unused candidate whose jurisdiction
   array is exactly `["CTH"]`.
3. For a State/Territory, reserve the highest-ranked unused candidate that
   contains that code and is not the all-nine general fallback. Use an
   all-nine record only if no specific candidate exists for that code.
4. A candidate may occupy only one reserved slot even if it contains multiple
   codes.
5. After reservation, fill remaining slots in Pinecone rank order subject to
   exact deduplication and the topic cap.
6. Return the chosen initial candidates in original Pinecone order so the
   answer prompt still sees relevance order.

For an all-nine broad scope, do not attempt impossible nine-jurisdiction
coverage within six slots. Apply only scope validation, exact deduplication,
topic diversity, and the existing source-type guarantee.

#### Why distinct reservation matters

A single all-nine or `["CTH", "WA"]` record should not consume both the CTH
and WA coverage guarantees. Distinct reservation increases the chance that
each requested legal stream receives actual explanatory material.

### Stage 6 — conditionally query a missing jurisdiction

After inspecting the initial 18, identify requested codes for which no
compatible candidate exists.

For each missing code, issue a supplemental Pinecone query using:

- the same embedding;
- `topK=3`;
- a code-specific metadata filter;
- the same metadata validation and State-safe compatibility rule; and
- no new model or embedding request.

The supplemental queries may run in parallel.

Merge non-duplicate results into the candidate pool and rerun the selector.
Do not run jurisdiction supplements when:

- the query scope is all nine;
- more than six codes would require coverage; or
- every requested code already has an eligible initial candidate.

Pseudocode:

```javascript
const missingCodes = getMissingCoverageCodes(
    validInitialCandidates,
    jurisdictions
);

const supplementalResponses = await Promise.all(
    missingCodes.map((code) => pineconeIndex.query({
        vector: embedding,
        topK: 3,
        includeMetadata: true,
        includeValues: true,
        filter: buildAustralianCoverageCodeFilter(code)
    }))
);
```

For a State/Territory code, `buildAustralianCoverageCodeFilter(code)` should
require that code. For CTH, it should require CTH and exclude all eight
State/Territory codes. The application-level compatibility check remains
mandatory.

#### Why this is conditional

Most requests still use one Pinecone query. Additional calls occur only when
the existing over-fetched set lacks a requested jurisdiction. This limits
latency while giving au-003- and au-011-type questions a recovery path.

### Stage 7 — preserve the `principle` guarantee

Run the existing `principle` requirement against the selected result:

1. if the selected six already contain a principle, return them;
2. otherwise prefer an unused compatible principle already present in the
   merged candidate pool;
3. if still absent, retain the existing scoped `type=principle` supplemental
   query;
4. add it to an unused slot or replace the lowest-ranked non-reserved filler;
5. if every slot is reserved, replace a reserved candidate only with a
   principle that specifically covers the same reserved code; and
6. if no such candidate exists, preserve jurisdiction coverage and record that
   the best-effort principle requirement was unsatisfied.

The final list remains capped at six.

## Consolidated algorithm

```text
Initial Pinecone query: same embedding, topK 18, State-safe scope filter
    ↓
Existing metadata validation
    ↓
State-safe compatibility check
    ↓
Build candidate profiles
    ↓
Exact-content deduplication
    ↓
Check requested-jurisdiction coverage
    ↓
Conditional same-embedding supplements for missing codes only
    ↓
Merge and deduplicate
    ↓
Reserve distinct jurisdiction slots
    ↓
Fill by Pinecone rank with max two per identical Topic
    ↓
Use Current-to date only as same-topic tie-break
    ↓
Preserve/add one principle without breaking reserved coverage
    ↓
Return at most six
```

## Suggested function-level change

### New pure helpers in `australianRetrievalService.js`

```javascript
isAustralianScopeCompatible(recordJurisdictions, queryJurisdictions)
buildAustralianCoverageCodeFilter(code)
getAustralianMatchText(match)
getAustralianCandidateProfile(match, originalRank)
dedupeAustralianCandidates(candidates)
getAustralianCoverageCodes(jurisdictions)
getMissingAustralianCoverageCodes(candidates, jurisdictions)
selectAustralianCandidates(candidates, jurisdictions)
```

The names are suggestions; the important constraint is that validation,
profiling, and selection remain independently testable.

### Existing functions to change

| Function | Minimal change |
|---|---|
| `buildAustralianMetadataFilter()` | Build State-safe CTH-only/requested-State semantics, with the existing broad rule only for all-nine scope. |
| `buildAustralianSourceTypeFilter()` | Compose `type=principle` with the new State-safe scope filter. |
| `getAustralianMatchRejectionReason()` | Replace any-intersection scope validation with `isAustralianScopeCompatible()`. |
| `retrieveAustralianMatches()` | Replace `validCandidates.slice(0, 6)` with profiling, conditional coverage supplements, and deterministic selection. Preserve the existing principle fallback. |
| `getMatchDedupeKey()` | Use content identity in addition to record ID, or supersede it with the candidate profile's exact-content key. |

### `legalQuestionService.js`

No answer-handoff change is required.

Optionally add an `onSelectionSummary` callback beside `onRejected`. It should
log counts and jurisdiction codes only, never source text or user content.

### `aiPrompts-au.js`

Keep the existing query-analysis JSON contract and examples. Add only the two
Stage 0 instructions. No answer-prompt wording is part of this retrieval
proposal; that is covered by the companion proposal.

## Freshness: what this change can and cannot solve

### It can improve

- selection between otherwise-equivalent same-topic records with different
  `Current to` dates;
- duplicate older material consuming multiple answer slots; and
- visibility of the dates attached to selected records.

### It cannot guarantee

- that a passage labelled current to 2026 is substantively current;
- that a corpus contains a later amendment;
- that an institution name inside a source has been updated correctly; or
- that old but still authoritative law should be displaced merely because of
  age.

For those reasons, the proposal does **not** impose a global age threshold.
au-010 demonstrates the limit: one passage labelled current to February 2026
still used obsolete terminology. The answer-prompt proposal therefore adds a
safe date-sensitive institution and deadline gate. A true currentness guarantee
requires corpus-side validation or update work, which is outside this minimal
runtime proposal.

## How the proposal addresses the reviewed failures

| Query | Expected retrieval effect | Remaining dependency |
|---|---|---|
| **au-002** | Prevents unrelated State records entering solely through shared CTH and ensures requested jurisdiction coverage. | VIC may remain legitimately in scope; the answer prompt must establish applicability before using it. |
| **au-003** | Reserves WA and CTH slots and conditionally searches CTH if none appears in the top 18. | The Commonwealth environmental record must exist and be semantically reachable in the corpus. |
| **au-004** | Reserves distinct CTH, VIC, and TAS material when the query scope contains them. | The federal NDB record must exist. |
| **au-005** | Prevents ACT sources occupying all slots and reserves CTH coverage. | The operative federal provisions must exist and rank within the CTH supplement. |
| **au-006** | Topic cap opens slots beyond repeated publication material, improving the chance of limitation and concerns-notice coverage. | No guarantee if those records are absent or outside the top 18. |
| **au-009** | Ensures separate WA and CTH material rather than allowing a mixed source to stand for both. | The answer prompt must not transfer the federal deadline to the WA stream. |
| **au-010** | Suppresses exact/repetitive migration-topic results and prefers the newer same-topic record when available. | Mislabelled stale content requires the answer-prompt safety gate or corpus correction. |
| **au-011** | Reserves distinct CTH, SA, and TAS sources and conditionally queries any missing code; duplicate child-grooming material is suppressed. | The required provisions must exist in the index. |
| **au-012** | Reserves Queensland coverage and diversifies repeated construction-payment topics, allowing lower-ranked primary-process material into the six. | The answer prompt must lead with the primary pathway; exact provisions must exist. |
| **au-016** | Caps the six identical interlocutory-appeal topics at two while diverse candidates remain, freeing four slots; jurisdiction reservation increases the chance of NSW/VIC/QLD/CTH authority. | *Farah/Hill* material must exist and rank within the candidate or supplemental set. |

## Required tests

Add focused unit tests to
`src/test/australianRetrievalService.test.js`.

### Scope-safety tests

1. The narrowed Pinecone filter for `["CTH", "NSW"]` encodes NSW intersection
   or genuine CTH-only scope.
2. The CTH-only filter excludes all eight State/Territory codes.
3. The all-nine filter retains broad current behaviour.
4. The `principle` filter composes the same State-safe scope.
5. `["CTH", "WA"]` is rejected in application code for
   `["CTH", "NSW"]`.
6. `["CTH"]` is accepted for `["CTH", "NSW"]`.
7. `["NSW"]` and `["CTH", "NSW"]` are accepted for
   `["CTH", "NSW"]`.
8. `["CTH", "NSW", "VIC"]` is accepted where NSW or VIC is requested.
9. An all-nine general record is accepted for a State-specific query.
10. A `["CTH"]`-only query rejects mixed `["CTH", "WA"]` records.
11. All-nine broad query scope retains broad-recall behaviour.

### Query-refinement contract tests

12. The prompt states that party location, incorporation, and a contractual
   forum or governing-law clause are not proof that substantive law applies.
13. The prompt requires a current-law formulation for present-rights questions
   while preserving material historical dates.
14. The response contract remains exactly `relevance`, `question`, and
    `jurisdictions`.

### Exact deduplication and topic-diversity tests

15. Different IDs with identical normalized text produce one candidate.
16. At most two records with the same jurisdiction/topic fingerprint are
   selected while other topics are available.
17. The topic cap relaxes only when needed to fill otherwise empty result
    slots.
18. A missing or malformed Topic field does not collapse unrelated records.
19. For the same fingerprint, the newer valid `Current to` record is preferred.
20. Invalid or absent dates preserve Pinecone rank.

### Coverage tests

21. A lower-ranked CTH candidate enters the final six for a
    `["CTH", "WA"]` query dominated by WA candidates.
22. CTH, SA, and TAS each receive a distinct slot when eligible candidates
    exist.
23. A single multijurisdiction record cannot consume more than one reserved
    slot.
24. All-nine scope does not attempt nine reservations.
25. A seven-code scope does not claim impossible complete coverage within six
    slots.

### Supplemental-query tests

26. No jurisdiction supplement runs when the initial 18 cover every requested
    code.
27. One same-embedding query runs for each missing requested code.
28. Supplemental results pass the same metadata and scope checks.
29. A CTH supplement cannot reintroduce an out-of-scope State record through
    shared CTH.
30. Supplemental results are content-deduplicated against initial candidates.

### Existing-behaviour regressions

31. No more than six matches are returned.
32. The `principle` fallback remains inside the Australian jurisdiction scope.
33. The only candidate reserved for a jurisdiction is not replaced by the
    principle fallback.
34. Where all six slots are reserved, a principle may replace a candidate only
    when it specifically covers the same reserved code.
35. Invalid outer, embedded, inconsistent, and non-canonical metadata continue
    to be rejected.
36. Non-Australian retrieval paths are unchanged.
37. Selection is deterministic for the same candidate order and metadata.

## Live acceptance criteria

Run the unchanged 18-query suite after implementation and capture the initial
18 candidate IDs as well as the selected six.

### Retrieval gates

- Zero selected matches whose only query overlap is shared `CTH` while all
  specific State/Territory codes are outside the query.
- Zero exact-content duplicates in a selected set.
- No more than two selected records with one normalized
  jurisdiction/topic fingerprint while an eligible different-topic candidate
  exists.
- For non-broad scopes of six codes or fewer, every requested code is
  represented by a distinct selected candidate when a compatible candidate
  exists in the initial or conditional supplemental results.
- Final result count never exceeds six.
- At least one `principle` is retained under the existing best-effort rule.
- No regression in invalid-metadata rejection.

### Query-specific expectations

- au-003: at least one distinct CTH and one WA source.
- au-004: distinct CTH, VIC, and TAS sources if each exists.
- au-005: at least one distinct CTH and ACT source.
- au-011: distinct CTH, SA, and TAS sources if each exists.
- au-012: Queensland coverage plus more than one construction-payment topic
  when available.
- au-016: no more than two sources carrying the repeated interlocutory-appeal
  topic.

These are retrieval expectations, not automatic answer-quality passes. The
answer review must still confirm legal applicability.

## Minimal observability recommendation

Add one structured selection summary per Australian request:

```json
{
  "initial_candidate_count": 18,
  "metadata_valid_count": 17,
  "specific_scope_rejected_count": 2,
  "exact_duplicate_suppressed_count": 1,
  "topic_cap_suppressed_count": 3,
  "requested_coverage": ["CTH", "SA", "TAS"],
  "achieved_distinct_coverage": ["CTH", "SA", "TAS"],
  "missing_coverage": [],
  "coverage_supplemental_queries": 1,
  "principle_supplemental_query": false,
  "selected_count": 6
}
```

Do not log the refined question, user content, source text, or credentials.
Selected source IDs are already persisted elsewhere.

This summary is not required for selection correctness, but it is the smallest
observability change that will let the next review distinguish:

- no matching source existed;
- a source existed below the first six;
- a source was rejected for scope;
- a duplicate was suppressed; and
- a supplemental query failed to find the missing jurisdiction.

## Performance impact

### Unchanged

- one query-analysis model call;
- one embedding;
- initial Pinecone `topK=18`;
- six final sources;
- answer-prompt token budget; and
- no reranker.

### Added

- small in-process string normalization and Context parsing over at most 18
  initial candidates;
- conditional Pinecone queries only for genuinely missing requested codes;
  and
- optional structured summary logging.

The normal path remains one Pinecone query. Supplemental calls should be
parallel and use the existing embedding.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Jurisdiction reservation promotes a lower-similarity source. | Reserve only one slot per requested code and fill all remaining slots by original rank. |
| Topic cap drops complementary paragraphs. | Permit two per topic and relax the cap when no diverse candidate can fill the result budget. |
| `Current to` creates a false global recency rule. | Use it only between records with the same jurisdiction/topic fingerprint. |
| Supplemental queries increase latency. | Run only for missing coverage, in parallel, with the existing embedding and `topK=3`. |
| General all-nine records are excluded accidentally. | Explicitly preserve them for State-specific and broad queries. |
| CTH-only search loses general all-nine material. | This is intentional for an express federal-only request; log missing coverage rather than admitting State material. |
| Selection logic becomes tied to legacy `_node_content`. | Put text access behind one helper; selection uses the same profile for direct `metadata.text`. |
| Retrieval is mistaken for governing-law determination. | Keep the query-analysis and prompt statements that scope is a retrieval policy; the answer prompt performs the legal applicability test. |

## Why not add a reranker or query-decomposition model

A reranker, multi-query decomposition stage, or additional LLM classification
could improve issue-level recall, but each would:

- add latency and cost;
- create a new model contract;
- require more extensive evaluation;
- complicate failure handling; and
- exceed the user's minimal-change preference.

The proposed selector first uses information and candidates the current system
already has. If the next run still misses issue-specific sources that are known
to exist in the top 18 or corpus, a reranker or query decomposition can then be
evaluated with evidence.

## Implementation and rollout sequence

1. Implement the scope-compatible pure helper and its tests.
2. Add the two query-refinement instructions and prompt-contract tests.
3. Add the candidate profile, exact-content dedupe, and topic cap.
4. Add jurisdiction reservation over the existing 18 candidates.
5. Add conditional missing-code supplements.
6. Integrate the existing `principle` guarantee with protected reserved slots.
7. Add the optional selection-summary callback.
8. Run the focused Australian retrieval tests.
9. Run the unchanged 18-query suite in development.
10. Export the same Cloudflare logs plus selection summaries.
11. Review answer quality before any production decision.

## Rollback

Rollback is confined to `australianRetrievalService.js` and its optional
logging callback. Restoring the current first-six selection returns the prior
behaviour. No corpus re-publication, re-embedding, index migration, API change,
or persistence migration is required.
