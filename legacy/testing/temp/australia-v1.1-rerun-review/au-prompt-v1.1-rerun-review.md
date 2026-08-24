# Australia v1.1 Federal–State Suite Rerun Review

## Log-informed answer, prompt, and retrieval report

**Review date:** 29 July 2026  
**Test run:** 29 July 2026, 16:41:48–16:44:09 GMT+8  
**Model:** `gpt-5.4`, low reasoning effort  
**Parallelism:** 5  
**Suite:** `testing/suites/australia/au-federal-state-v1.json`  
**Answers:** `testing/results/australia/au-prompt-v1.1.md`  
**Cloudflare index:** `testing/temp/australia-v1.1-rerun-review/log-summary.csv`

## Executive verdict

**This is a valid v1.1 test, but the suite is not yet satisfactory as a whole.**

All 18 Cloudflare request bodies contain:

```text
# Answer Generation System Prompt - Australia v1.1
```

The prompt change produces one clear substantive success: **au-016 now states
the plainly-wrong / compelling-reason discipline for interstate intermediate
appellate decisions**, even though retrieval remains a complete topical miss.
au-001 also stops importing the NSW psychological-injury defence into a likely
Victorian claim.

Two central failures remain:

1. **au-010 uses the obsolete “Migration and Refugee Division” label** for the
   current Administrative Review Tribunal and presents a generic route where the
   cancellation type controls the forum and deadline.
2. **au-012 still displaces the ordinary Queensland security-of-payment
   sequence with the collateral subcontractors’ charge process.**

The full scorecard is:

| Rating | Queries | Count |
|---|---|---:|
| **Satisfactory** | au-002, au-008, au-013, au-014, au-015, au-016, au-017, au-018 | 8 |
| **Needs revision** | au-001, au-003, au-004, au-005, au-006, au-007, au-009, au-011 | 8 |
| **Not satisfactory** | au-010, au-012 | 2 |

Relative to the earlier 16:11–16:13 run—which was labelled v1.1 locally but
actually sent v1.0—the pass count rises from 7 to 8 and the material-failure
count falls from 4 to 2. The principal movements are:

- au-001: **Not satisfactory → Needs revision**
- au-016: **Not satisfactory → Satisfactory**

Because model output is stochastic, not every wording difference can be
attributed to the prompt. The au-016 change is strong evidence of prompt effect:
the exact v1.1 rule appears in the answer despite its absence from all six
retrieved passages.

## Evidence and method

The Cloudflare answer calls were isolated by the test window and
`Tokens In > 5000`. Each retained call was then matched using:

- the exact suite query;
- the exact conversation ID in the result file;
- the Cloudflare log ID;
- the system-prompt heading;
- the six retrieved passages; and
- HTTP, token, cost, cache, reasoning, duration, and endpoint metadata.

Validation result:

| Check | Result |
|---|---:|
| Retained answer logs | 18 |
| Exact query matches | 18/18 |
| Conversation-ID matches | 18/18 |
| Unique log IDs | 18 |
| Unique conversation IDs | 18 |
| v1.1 prompt heading | 18/18 |
| HTTP 200 | 18/18 |

The legal review used the rendered answers, the retrieved payload attached to
each answer request, and current official sources where current law determined
whether an omission or statement was material.

## Exact issue register

### au-001 — Needs revision

**What improved:** The answer correctly identifies Victoria as the likely
workers’ compensation and workplace-safety jurisdiction and keeps the
Commonwealth dismissal stream separate. Unlike the earlier run, it does not
substitute NSW `s 11A` or NSW cases for Victorian psychological-injury law.

**Exact remaining issue:** The six passages are Victorian but mostly current
only to 2011–15 and contain no current mental-injury eligibility test, Victorian
psychosocial-safety pathway, or Commonwealth dismissal deadline. The answer
therefore says the psychological-injury test is unavailable and advises urgent
filing without stating the key 21-day dismissal period.

For injuries on or after 31 March 2024, Victoria applies specific mental-injury
eligibility and exclusion rules:
[WorkSafe Victoria — worker’s injury claim form](https://www.worksafe.vic.gov.au/workers-injury-claim-form).
Unfair-dismissal and general-protections dismissal applications ordinarily have
a 21-day period:
[Fair Work Ombudsman — ending employment](https://www.fairwork.gov.au/tools-and-resources/fact-sheets/minimum-workplace-entitlements/ending-employment).

**Required correction:** Retrieve the current Victorian mental-injury,
reasonable-management-action, psychosocial-safety, and Commonwealth dismissal
rules. Preserve the answer’s improved jurisdiction split.

### au-002 — Satisfactory, with a prompt-compliance defect

**Exact result:** The answer correctly separates the national ACL framework, its
Queensland application, Queensland electrical-safety regulation, and the
Victorian seller’s forum clause. It does not treat the Victorian clause as
displacing mandatory Queensland regulation or ACL remedies.

**Residual issue:** QCAT is presented as plausible rather than verified for this
specific installation dispute, which is appropriately cautious. However, the
answer twice refers to “materials available”, contrary to the v1.1 hidden-source
rule.

### au-003 — Needs revision

**Exact issue:** All six passages concern WA or local planning, mining, and
environmental processes. None covers the Commonwealth EPBC referral,
controlled-action, assessment, approval, or early-works rules. The answer
correctly says the streams are separate but can state the Commonwealth pathway
only in general terms.

Current official guidance confirms that Commonwealth and State approvals remain
distinct, that a protected-matter impact may require referral, and that a
controlled action needs federal assessment and approval before it starts:
[DCCEEW — referrals and environmental assessments](https://www.dcceew.gov.au/environment/epbc/approvals).

**Required correction:** Retrieve the Commonwealth protected-matter referral and
controlled-action pathway alongside the WA and local tracks.

### au-004 — Needs revision

**Exact issue:** The answer recognises potentially concurrent Commonwealth,
Victorian, and Tasmanian regimes, but retrieval contains only general federal
confidentiality/privacy material. It does not contain `Privacy Act 1988 (Cth)
pt IIIC`. The prioritised 72-hour plan therefore does not anchor suspected-breach
assessment or notifications to the operative federal provisions.

The current Act requires reasonable and expeditious assessment, with reasonable
steps to complete it within 30 days, and requires a statement to the Commissioner
as soon as practicable where an eligible data breach is established:
[Privacy Act 1988 (Cth) ss 26WH and 26WK](https://www.legislation.gov.au/C2004A03712/latest/text).

**Required correction:** Retrieve `ss 26WE, 26WH and 26WK–26WL` and current
Victorian and Tasmanian complaint or notification routes.

### au-005 — Needs revision

**Exact issue:** Retrieval is ACT-heavy and mostly current only to 2018. It
supplies no operative federal employment provision equivalent to the ACT
analysis and no dependable current comparison of complaint sequence, remedies,
deadlines, or duplication risk. The answer consequently recommends the ACT
route mainly because that is the route retrieval describes more fully, rather
than because the user’s objectives make it preferable. It also exposes the
hidden source set repeatedly.

The directly relevant federal provisions include the pregnancy definition and
employment prohibition in `Sex Discrimination Act 1984 (Cth) ss 7 and 14`:
[Federal Register of Legislation](https://www.legislation.gov.au/C2004A02868/latest/text).

**Required correction:** Retrieve the current federal substantive provisions and
complaint route, then compare the ACT and federal pathways on equal footing.

### au-006 — Needs revision

**Exact issue:** The closest-connection and forum analysis is useful, but none of
the six passages contains current limitation or concerns-notice provisions. The
answer states a general one-year period and possible three-year extension, then
describes the mandatory pre-action question as something still to check.

Current NSW uniform legislation requires a compliant concerns notice before
proceedings, subject to the stated statutory exceptions:
[Defamation Act 2005 (NSW) ss 12A–12B](https://legislation.nsw.gov.au/view/whole/html/inforce/current/act-2005-077).

**Required correction:** Retrieve the current limitation and concerns-notice
rules for the likely governing jurisdiction and calculate the sequence from the
publication date.

### au-007 — Needs revision

**Exact issue:** The answer correctly rejects both “NSW because payroll is
there” and “NT because the injury occurred there” as automatic rules. However,
the passages are mainly 2011–14 material, omit Queensland despite the worker’s
Queensland project history, and use ACT material as the main comparator. That is
not enough to apply every genuinely contending scheme’s ordered connection test.

**Required correction:** Retrieve current ACT, NSW, Queensland, and NT
connection provisions and apply each scheme without using one jurisdiction’s
text as a generic substitute.

### au-008 — Satisfactory

**Exact result:** The answer rejects Victorian incorporation and signing as the
determinant of land law. It separates NSW and Queensland land, conveyancing,
registration, and duty streams, while limiting Commonwealth corporate law to
genuinely national issues.

**Residual issue:** No specific current transfer-duty provisions are retrieved,
so the answer appropriately avoids numeric duty advice.

### au-009 — Needs revision

**Exact result:** The answer correctly separates WA de facto property,
Commonwealth parenting, and the federal superannuation overlay. It does not
transfer the Commonwealth `Family Law Act 1975 (Cth) s 44` period to the WA
property claim.

**Exact remaining issue:** The action plan omits the generally applicable
two-year WA de facto property/financial application period, despite the user
asking for first steps. The retrieved introduction mentions a two-year concept
ambiguously but does not tie the WA trigger and leave rule to `Family Court Act
1997 (WA) s 205ZB`.

Current WA court guidance states that a de facto property or financial
application generally must be filed within two years after breakdown, with
permission required after that:
[Family Court of Western Australia — property and financial](https://familycourt.wa.gov.au/P/property_and_financial.aspx).

**Required correction:** Retrieve current `s 205ZB` and state its trigger,
period, and out-of-time permission rule.

### au-010 — Not satisfactory

**Exact issue:** The answer repeatedly describes the current ART body as the
“Migration and Refugee Division”. That is legacy AAT terminology. The current
ART has separate **Migration** and **Protection** jurisdictional areas:
[Administrative Review Tribunal Act 2024 (Cth) s 196](https://www.legislation.gov.au/C2024A00040/latest/text);
[ART — structure](https://www.art.gov.au/about-us/structure).

The answer also presents “usually” available migration merits review and
Federal Court/Federal Circuit and Family Court routes without knowing the
cancellation type. Some cancellation decisions have decision-specific review
availability and strict, non-general timing rules. Its warning not to assume a
period is correct, but it does not cure the wrong forum name or the overly broad
route.

**Retrieval cause:** One passage is current general ART material to February
2026, but the migration-specific passage is current only to February 2024 and
expressly contains the obsolete division label. The model blends current and
legacy structures despite the v1.1 instruction not to do so.

**Required correction:** Retrieve current decision-specific migration-review
material. Use no jurisdictional-area name, numeric period, or extension rule
unless it is tied to the cancellation provision in the notice.

### au-011 — Needs revision

**Exact result:** The answer identifies plausible Commonwealth and Tasmanian
offence streams, explains that the same conduct can engage both, and gives
sensible pre-interview evidence-preservation advice.

**Exact remaining issue:** It does not identify a South Australian offence or
territorial rule even though the messages were sent there, and it omits the
federal double-punishment safeguard. `Crimes Act 1914 (Cth) s 4C(2)` prevents
Commonwealth punishment for the same act or omission after State or Territory
punishment:
[Federal Register of Legislation](https://www.legislation.gov.au/C1914A00012/latest/text).

**Retrieval cause:** Four of six slots are copies of the same child-grooming
topic, which is unrelated to the facts. No slot covers `s 4C` or the relevant
South Australian stream.

**Required correction:** Retrieve `s 4C`, relevant SA territorial/offence
material, and one current Tasmanian offence passage; deduplicate the grooming
material.

### au-012 — Not satisfactory

**Exact result:** The answer correctly rejects the proposition that a NSW
choice-of-law clause automatically displaces mandatory Queensland construction
or licensing legislation. It also distinguishes PPSA collateral rights from
State payment remedies.

**Exact issue:** It treats the subcontractors’ charge as the primary Queensland
payment pathway and supplies detailed charge deadlines, but does not explain the
ordinary Chapter 3 sequence: payment claim, payment schedule, consequences of
non-response/non-payment, adjudication, judgment-debt recovery, and suspension.
The current Act places these steps in `ss 75–79` and the following provisions:
[Building Industry Fairness (Security of Payment) Act 2017 (Qld), ch 3](https://www.legislation.qld.gov.au/view/whole/pdf/inforce/current/act-2017-043).

**Retrieval cause:** The six passages contain no occurrence of “payment claim”
or “payment schedule” and only one incidental reference to adjudication. The
v1.1 primary-pathway instruction cannot select a pathway that retrieval did not
supply under the prompt’s strict source rules.

**Required correction:** Retrieve and address the Chapter 3 progress-payment
pathway first. Keep charges, PPSA, insolvency, licensing, and NSW contract law as
separate secondary streams.

### au-013 — Satisfactory

**Exact result:** The answer correctly explains that a Commonwealth licence does
not automatically create a positive right overriding State law. It distinguishes
simultaneous-obedience, rights-conflict, covering-the-field, and
alter/impair/detract analyses. Retrieval is tightly focused on `s 109`.

### au-014 — Satisfactory

**Exact result:** The answer treats copyright ownership and infringement as
principally Commonwealth issues, correctly explains why a State is not required
for useful analysis, and preserves the contractor/assignment/licence distinction.

**Residual issue:** Retrieval includes an irrelevant parallel-import/integrated-
circuit passage, but it does not contaminate the answer.

### au-015 — Satisfactory

**Exact result:** The answer treats directors’ duties, oppression, derivative
action, and corporate injunctive relief as principally Commonwealth
corporations-law questions. It does not invent a State-law dependency merely
because location is omitted.

### au-016 — Satisfactory

**Exact result:** This is the clearest v1.1 improvement. The answer states that
interstate intermediate appellate decisions on the common law of Australia are
not freely optional and should not be departed from unless plainly wrong or
there is a compelling reason. It anchors the analysis in binding High Court
principle and treats recency and factual similarity as relevant but not
decisive.

That is consistent with the current High Court formulation:
[*Hill v Zuda Pty Ltd*](https://www.hcourt.gov.au/cases-and-judgments/judgments/judgments-1998-current/hill-v-zuda-pty-ltd);
[*Lendlease Corporation Ltd v Pallas* [2025] HCA 19, [109]](https://www.hcourt.gov.au/sites/default/files/eresources/2025-07-03/HCA/Lendlease%20Corporation%20Ltd%20v%20Pallas%20%28S108-2024%29%20%5B2025%5D%20HCA%2019.pdf).

**Retrieval significance:** Retrieval remains a complete miss: one foreign-law
passage, four copies of the same interlocutory-appeal topic, and one hypothetical-
appeal passage. None contains the methodology. The answer’s corrected rule is
therefore evidence that the v1.1 prompt edit itself is effective.

### au-017 — Satisfactory

**Exact result:** The model asks for the State or Territory before analysing the
seven-day termination notice, bond, carpet liability, or tribunal. It does not
apply a generic Australian tenancy regime.

### au-018 — Satisfactory

**Exact result:** The model asks where the fall occurred before applying a
limitation period, civil-liability statute, court, or pre-court process. It
correctly requests only the additional facts that could change the jurisdiction
or pathway and ignores unrelated product-liability retrieval.

## v1.1 prompt-effect review

### 1. Interstate precedent rule — successful

au-016 now contains the targeted plainly-wrong / compelling-reason discipline.
The relevant rule is absent from retrieval, making this the strongest evidence
that the answer-prompt edit caused the improvement.

### 2. Hidden-source prohibition — unsuccessful

Seven answers still mention or imply the hidden source set:

- au-001 — “The materials here do not set out...”
- au-002 — “materials available”, “present materials”
- au-004 — repeated “the materials identify...”
- au-005 — “material provided”, “material available”
- au-010 — “the material provided states...”
- au-011 — “authorities available here”
- au-012 — repeated “the materials indicate...”

This is an actual v1.1 compliance failure, not a deployment issue. The ban is
present in the system prompt sent to every request.

### 3. Primary-pathway prioritisation — unsuccessful where retrieval is absent

au-012 still makes the collateral subcontractors’ charge the centre of the
answer. Retrieval supplies charge material but no ordinary payment-claim or
payment-schedule content. Under the prompt’s source restrictions, the answer
cannot safely construct the missing statutory sequence in detail.

### 4. Decision-specific forum and deadline guard — partially successful

- **Successful caution:** au-001 does not invent a Commonwealth dismissal
  period, au-009 does not transfer the federal `s 44` period to WA, and au-010
  repeatedly warns the user to follow the operative notice.
- **Material failure:** au-010 still names a legacy migration division by
  blending old migration material with the current ART.
- **Coverage cost:** au-001 and au-009 omit important current periods because
  retrieval does not supply decision/claim-specific authority.

### 5. Jurisdictional clarification gate — successful

au-017 and au-018 both stop at the correct jurisdictional gate and ask for the
missing State or Territory before giving deadline, forum, or remedy advice.

### 6. Length and structure — unchanged problem

Thirteen of 18 answers exceed 2,000 words. The median is 2,277 words, and the
longest answer is au-013 at 3,742 words. The substantive answers repeat issue,
rule, application, conclusion, action-plan, table, and risk material. The two
clarification answers remain appropriately short.

## Retrieval-pipeline verdict

**The limited Stage 0/Stage 1 change appears to reduce wrong-State substitution,
but it does not solve multi-stream coverage, freshness, topicality, or
duplication.**

Positive observations:

- au-001 now retrieves Victorian rather than substituting a NSW psychological-
  injury rule.
- au-002 supports Queensland ACL application and electrical safety while
  retaining the Victorian contractual context.
- au-008, au-013, au-014, and au-015 retrieve the correct governing stream.
- au-017 and au-018 remain safe because the answer prompt does not use retrieved
  material before the missing jurisdiction is supplied.

Residual failure classes:

| Failure class | Queries | Exact observation |
|---|---|---|
| **Missing governing stream** | au-003, au-004, au-005, au-006, au-007, au-009, au-011, au-012 | A Commonwealth, State, or procedural stream expressly requested by the user is absent or incomplete. |
| **Current/legacy blend** | au-001, au-005, au-007, au-010 | Material is stale or mixes a current general framework with an obsolete specialist structure. |
| **Duplicate waste** | au-011, au-016 | Four slots repeat child-grooming material in au-011; four slots repeat interlocutory-appeal material in au-016. |
| **Complete topical miss** | au-016 | No retrieved passage addresses Australian interstate-precedent methodology. |
| **Adjacent remedy displaces primary route** | au-012 | Charge material crowds out the ordinary progress-payment pathway. |

The State-safe filter is therefore doing the narrow job it was designed to do.
It prevents one class of jurisdictional contamination; it does not guarantee
that every Commonwealth/State/Territory stream named in a multi-stream question
is represented among the six results.

## Gateway performance

| Metric | Valid v1.1 rerun | Earlier v1.0-prompt run | Change |
|---|---:|---:|---:|
| Input tokens | 189,431 | 186,671 | +2,760 (+1.5%) |
| Output tokens | 62,865 | 60,427 | +2,438 (+4.0%) |
| Cost | US$1.369033 | US$1.257019 | +US$0.112014 (+8.9%) |
| Summed duration | 824,724 ms | 790,192 ms | +34,532 ms (+4.4%) |
| Retrieved context | 449,005 chars | 452,050 chars | −3,045 (−0.7%) |
| Response size | 268,784 chars | 265,688 chars | +3,096 (+1.2%) |

Per-answer medians and ranges:

| Metric | Median | Range |
|---|---:|---:|
| Input tokens | 9,747.5 | 7,637–17,510 |
| Output tokens | 3,719 | 380–5,576 |
| Cost | US$0.082776 | US$0.018889–US$0.110623 |
| Duration | 48,127 ms | 6,056–70,840 ms |
| Retrieved context | 22,308 chars | 12,124–57,557 chars |
| Response length | 2,277 words | 224–3,742 words |

The duration total is not wall-clock suite time because the run used parallelism
5.

## Release decision

**Do not approve v1.1 as a satisfactory federal–State suite result yet.**

The prompt edit for interstate precedent should be retained. The current
prompt/pipeline combination still needs to clear these acceptance checks:

1. au-010 uses current ART terminology and only a cancellation-specific route.
2. au-012 addresses the ordinary Queensland Chapter 3 pathway before charges.
3. No answer mentions materials, sources, authorities “available here”,
   retrieval, source coverage, or source quantity.
4. au-001 receives current Victorian mental-injury and Commonwealth dismissal
   material.
5. au-003, au-004, au-005, au-006, au-007, au-009, and au-011 each receive all
   governing streams necessary to answer the question asked.
6. Duplicate retrieval does not consume multiple slots.

The valid rerun demonstrates that v1.1 fixes one high-value prompt problem. The
remaining two material failures are traceable to an obsolete retrieved
migration source and a missing primary Queensland payment pathway, while the
hidden-source wording is a direct answer-prompt compliance failure.
