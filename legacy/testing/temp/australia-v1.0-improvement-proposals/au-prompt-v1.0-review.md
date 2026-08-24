# Australia v1.0 Federal–State Suite Review

## Log-informed second review

**Review date:** 29 July 2026  
**Test run:** 29 July 2026, 09:34–09:38 GMT+8  
**Model:** `gpt-5.4`, low reasoning effort  
**Parallelism:** 5  
**Suite:** `testing/suites/australia/au-federal-state-v1.json`  
**Answers:** `testing/results/australia/au-prompt-v1.0.md`  
**Gateway export:** `testing/results/australia/au-prompt-v1.0-logs/`

## Executive verdict

**The run is not satisfactory for production use.**

The model understands the basic shape of Australian federalism and usually
identifies whether a matter is Commonwealth, State/Territory, or concurrent. The
run nevertheless fails the suite as a whole because five answers contain a
material jurisdiction, procedure, or authority-hierarchy defect. Six more need a
specific correction before they should be relied on.

| Rating | Queries | Count |
|---|---|---:|
| **Satisfactory** | au-001, au-008, au-013, au-014, au-015, au-017, au-018 | 7 |
| **Needs revision** | au-003, au-004, au-005, au-006, au-007, au-011 | 6 |
| **Not satisfactory** | au-002, au-009, au-010, au-012, au-016 | 5 |

The ratings are unchanged from the first review. The logs materially improve the
diagnosis: the principal problem is **not fabricated authority names**. It is the
combination of:

1. retrieval returning incomplete, stale, duplicated, or wrong-jurisdiction
   material; and
2. the answer generator failing to reject, qualify, or compensate for that
   material.

The exact high-risk failures are:

- Victorian statutory provisions were applied to a Queensland consumer
  transaction without a governing-law basis;
- a Commonwealth filing provision was used as the source for a WA de facto
  property deadline;
- obsolete tribunal terminology and the wrong deadline framework were used for a
  migration review;
- the ordinary Queensland payment-claim and adjudication pathway was omitted; and
- the Australian interstate-precedent rule was materially understated.

## Evidence and method

The Cloudflare export contains exactly 18 answer-generation logs, matched to the
suite by both the exact user query and conversation ID. The gateway window
contained 72 events; 54 embedding and short preprocessing events were excluded.
Each retained log contains:

- the Australia v1.0 system prompt;
- the six retrieved context passages sent to the model;
- the exact suite query;
- the answer matched from the result file; and
- token, cost, duration, and conversation metadata.

No authentication material is present in the export.

For this review, each problem is classified as one or more of:

- **Retrieval/context defect:** the required authority was absent, irrelevant
  authority was retrieved, or retrieved text was stale or contradictory.
- **Answer-generation defect:** the model selected the wrong jurisdiction,
  misstated the law, omitted a necessary distinction, or failed to use an
  available qualification.
- **Prompt-compliance defect:** the answer broke a specific output or grounding
  instruction.
- **Prompt-design defect:** the governing prompt itself did not state the rule
  strongly or precisely enough.

These classifications overlap. A missing source does not excuse a wrong answer,
and a generation error can occur even when retrieval contributed to it.

## Root-cause summary

| Cause | Affected answers | Finding |
|---|---|---|
| **Material retrieval/context problem** | au-002, au-003, au-004, au-005, au-006, au-009, au-010, au-011, au-012, au-016 | 10 of 18 answers received materially incomplete, contaminated, stale, or off-topic context. |
| **Material answer-generation or prompt-compliance problem** | au-002, au-003, au-005, au-006, au-007, au-009, au-010, au-012, au-016 | 9 answers failed to reject bad context or broke an explicit instruction. |
| **Material prompt-design problem** | au-016; suite-wide citation and length behaviour | The cross-jurisdiction authority rule is incomplete, and formatting/conciseness instructions are not reliably enforced. |

### Citation provenance result

A name-level audit found that **every actual authority named in an answer's
`## References` section also appeared in that answer's retrieved context**. This is
good evidence against free-form citation invention in this run.

That audit does **not** prove that:

- the retrieved authority was current;
- the authority governed the correct jurisdiction;
- each pinpoint supported the proposition attached to it; or
- the answer selected the right authority from the retrieved set.

au-016 also contains a meta-entry saying no citations were included. That entry is
not an authority and should not appear in a References section.

## Exact issue register

### au-002 — Not satisfactory

**Question tested:** Queensland consumer transaction involving a Victorian seller,
a Queensland installer, and a Victorian forum term.

**Exact defect:** the answer applies `Australian Consumer Law and Fair Trading Act
2012 (Vic) ss 25–26` and says the provisions are relevant **“because the seller is
Victorian and relies on Victorian terms.”** Seller location and a forum clause do
not, without more, establish that those Victorian provisions govern a supply and
installation performed in Queensland.

**Why it matters:** this is direct cross-State statutory substitution, which is the
central error the suite is designed to detect.

**Log evidence:** the six retrieved passages included two Victorian sale-of-goods
passages alongside Queensland ACL-application and electrical-safety material. The
model copied the Victorian material into the answer instead of first establishing
its territorial or choice-of-law basis. The current Queensland application
provision expressly connects the Queensland ACL to persons carrying on business,
ordinarily resident, or otherwise connected with Queensland:
[Fair Trading Act 1989 (Qld) s 20](https://www.legislation.qld.gov.au/view/whole/html/inforce/2026-02-19/act-1989-084).

**Root cause:** retrieval contamination plus answer-generation failure.

**Required correction:** retain the ACL and Queensland electrical-safety analysis.
Remove the Victorian statutory analysis unless the answer first establishes why
that statute applies. Treat the forum clause separately from governing law and
mandatory Queensland law.

---

### au-003 — Needs revision

**Question tested:** separate Commonwealth, WA environmental, and local planning
approval tracks for a threatened-species project.

**Exact defects:**

1. None of the six retrieved passages concerns the Commonwealth environmental
   statute or Commonwealth protected-matter referral process. All six concern WA
   planning, mining, or environmental processes.
2. The Commonwealth analysis is therefore reduced to a generic conditional:
   **“if the threatened-species issue engages a Commonwealth protected matter.”**
   It does not identify or substantively explain the Commonwealth controlled-action
   and referral track.
3. The answer expressly says **“The materials provided do not include the
   Commonwealth environmental statute.”** This breaches the prompt instruction
   never to disclose that sources or data are missing.

**Why it matters:** the answer reaches the correct high-level result—that the
approval tracks can be cumulative—but cannot adequately answer the Commonwealth
half of the comparison.

**Root cause:** retrieval gap plus prompt-compliance failure.

**Required correction:** retrieve the Commonwealth environmental approval
framework and analyse it independently of WA and local approvals. If the authority
is still unavailable, state the general principle without discussing the hidden
source set.

---

### au-004 — Needs revision

**Question tested:** concurrent Commonwealth, Victorian, and Tasmanian obligations
after a health-data breach.

**Exact defects:**

1. The retrieved Commonwealth material includes general APP-entity,
   confidentiality, permitted-health-situation, and complaint provisions, but not
   the Notifiable Data Breaches scheme.
2. The answer recommends a 72-hour response plan but never anchors the federal
   assessment and notification duties to `Privacy Act 1988 (Cth) pt IIIC`,
   including the reasonable and expeditious assessment requirement, the 30-day
   assessment period, and notification as soon as practicable.
3. It uses generic labels such as **“federal privacy regulator”** rather than
   identifying the OAIC and does not clearly identify the relevant Victorian and
   Tasmanian complaint/regulatory destinations.

The current federal provisions are in `Privacy Act 1988 (Cth) ss 26WE, 26WH and
26WK–26WL`: [Privacy Act 1988 (Cth), pt IIIC](https://www.legislation.gov.au/C2004A03712/2026-06-04/2026-06-04/text/original/epub/OEBPS/document_1/document_1.html).

**Why it matters:** the high-level concurrent-regime framing is sound, but the user
asked what must happen immediately. The precise federal breach-assessment and
notification route is a central part of that advice.

**Root cause:** retrieval gap. The answer remains broadly useful, so this is a
revision rather than a fail.

**Required correction:** retrieve and cite the NDB provisions; name each regulator
or complaint body; and distinguish mandatory notification from prudent voluntary
contact.

---

### au-005 — Needs revision

**Question tested:** choice between Commonwealth and ACT pregnancy-discrimination
processes.

**Exact defects:**

1. The only federal retrieved passage supplies scope and definition material,
   principally `Sex Discrimination Act 1984 (Cth) ss 4, 4B and 9`. It does not
   supply the operative pregnancy-discrimination and employment provisions in
   ss 7 and 14.
2. The answer therefore discusses the federal substantive claim and federal
   process only in general terms, without a well-supported comparison of forum,
   remedies, and time limits.
3. It says **“They do not set out a specific statutory rule here requiring an
   election”**, revealing the limitations of the hidden source material contrary
   to the prompt.

The directly relevant current federal provisions are
[Sex Discrimination Act 1984 (Cth) ss 7 and 14](https://www.legislation.gov.au/C2004A02868/latest/textAustralian).

**Why it matters:** the answer correctly says Commonwealth and ACT regimes can
overlap, but it does not give the concrete pathway comparison the user requested.

**Root cause:** retrieval gap plus prompt-compliance failure.

**Required correction:** retrieve the operative federal provisions and current
federal complaint route, then compare them against the ACT pathway using exact
filing limits, remedies, costs exposure, and duplication/election rules.

---

### au-006 — Needs revision

**Question tested:** multistate online defamation, place of publication, governing
law, forum, and pre-action timing.

**Exact defects:**

1. Retrieval contains useful publication and choice-of-law material, including
   *Dow Jones & Co Inc v Gutnick*, but no limitation or concerns-notice material.
2. The answer is consequently precise on publication and closest connection but
   generic on the urgent limitation and pre-action steps.
3. The References section supplies both `(2002) 210 CLR 575` and `[2002] HCA 56`
   for *Gutnick*. That breaches the prompt's rule to prefer one authorised report
   citation rather than giving multiple forms.

For comparison, the current NSW provisions require a concerns notice before
proceedings and specify its contents:
[Defamation Act 2005 (NSW) ss 12A–12B](https://legislation.nsw.gov.au/view/whole/html/inforce/2025-03-02/act-2005-077).

**Why it matters:** the governing-law analysis is good, but the missing retrieved
procedure prevents the answer from giving the exact urgent steps the question
calls for.

**Root cause:** retrieval gap plus citation-formatting failure.

**Required correction:** retrieve current limitation and concerns-notice
provisions for the likely governing jurisdiction; state the date calculation and
pre-action sequence precisely; use one selected citation form per case.

---

### au-007 — Needs revision

**Question tested:** workers' compensation connection across ACT, NSW, Queensland,
and the Northern Territory.

**Exact defect:** `## Legal Issues` contains four numbered items, but
`## Legal Analysis` contains only three. The fourth issue—urgent practical
steps—is procedural and belongs in `## Recommended Action Plan`.

**Log evidence:** the retrieved passages cover NT, Queensland, and NSW workers'
compensation connection rules, although several are current only to 2011–2014.
There is no ACT passage. Despite that uneven context, the substantive connection
analysis is cautious and broadly sound.

**Why it matters:** this is not a material legal error, but it directly breaches
the prompt's issue/analysis numbering rule.

**Root cause:** answer-generation and prompt-compliance failure.

**Required correction:** list only the three substantive legal issues, and keep
urgent filing and evidence steps in the action plan. Refresh the old workers'
compensation source set before a production rerun.

---

### au-009 — Not satisfactory

**Question tested:** WA de facto property, federal parenting, and federal
superannuation within the WA court structure.

**Exact defect:** the answer correctly identifies `Family Court Act 1997 (WA)
pt 5A` as governing the de facto property stream, but cites `Family Law Act 1975
(Cth) s 44(5)` as the source of the two-year filing period.

The numerical period happens to be two years, but the governing WA source is
`Family Court Act 1997 (WA) s 205ZB`. The current provision also contains
WA-specific consent and hardship/leave rules:
[Family Court Act 1997 (WA) s 205ZB](https://www.legislation.wa.gov.au/legislation/prod/filestore.nsf/FileURL/mrdoc_49103.htm/$FILE/Family%20Court%20Act%201997%20-%20%5B04-n0-00%5D.html?OpenElement).

**Log evidence:** the six retrieved family-law passages correctly describe WA's
separate de facto regime, but provide the federal s 44 deadline and do not provide
s 205ZB. The model repeated the federal provision instead of withholding or
qualifying it for the WA property stream.

**Why it matters:** this is an exact Commonwealth-for-State substitution. It
produces the same number only by coincidence and fails the core jurisdiction test.

**Root cause:** retrieval gap plus answer-generation jurisdiction-check failure.

**Required correction:** cite s 205ZB for the WA property and maintenance stream.
Keep federal parenting and superannuation provisions in their separate streams.

---

### au-010 — Not satisfactory

**Question tested:** separate Commonwealth migration and NSW occupational-licence
review paths.

**Exact defects:**

1. The answer repeatedly uses **“Migration and Refugee Division of the ART”** and
   **“ART MRD.”** “Migration and Refugee Division” was AAT terminology. The ART
   statute now identifies separate Migration and Protection jurisdictional areas:
   [Administrative Review Tribunal Act 2024 (Cth) s 196](https://www.legislation.gov.au/C2024A00040/2026-05-18/2026-05-18/text/original/epub/OEBPS/document_1/document_1.html).
2. It says the prescribed ART period is **“generally 28 days”** and refers to ART
   Act extension provisions. The retrieved ART source itself says the general
   procedures discussed there exclude migration and protection decisions.
3. The migration application rule is separately governed. For the relevant class
   of review application, current `Migration Act 1958 (Cth) s 347` specifies
   14 days for a person in immigration detention and 28 days otherwise, and says
   the ART Act extension provision does not apply:
   [Migration Act 1958 (Cth) s 347](https://www.legislation.gov.au/C1958A00062/2026-01-22/2026-01-22/text/original/epub/OEBPS/document_2/document_2.html).
   The exact cancellation provision and decision notice still control
   reviewability and timing.

**Log evidence:** the six retrieved passages are internally inconsistent. A
February 2026 administrative-law passage still says “Migration and Refugee
Division”; two migration passages current only to February 2024 refer to the AAT;
another passage gives a general ART framework while expressly excluding migration
and protection decisions. The model copied the stale label and applied the general
framework despite the exception.

**Why it matters:** migration deadlines can be strict. The answer may cause a user
to look for a body that no longer exists or assume an extension framework that is
unavailable. The ART itself directs applicants to the exact deadline in the
decision letter:
[ART immigration and citizenship guidance](https://www.art.gov.au/applying-review/immigration-and-citizenship).

**Root cause:** stale and contradictory retrieval plus answer-generation failure.

**Required correction:** use current ART terminology; identify the statutory
migration review route from the cancellation provision; state the exact notice
deadline; and do not present general ART extension rules as applicable to migration.

---

### au-011 — Needs revision

**Question tested:** Commonwealth, Tasmanian, and South Australian criminal exposure
for interstate threatening messages, including whether offences can operate
together.

**Exact defects:**

1. The answer identifies `Criminal Code (Cth) s 474.17` and a Tasmanian offence,
   but leaves the South Australian limb at **“there may also be a South Australian
   connection.”**
2. It says Commonwealth and State offences can apply to the same conduct but omits
   the specific double-punishment safeguard in `Crimes Act 1914 (Cth) s 4C(2)`:
   punishment under State or Territory law prevents subsequent punishment under a
   Commonwealth law for the same act or omission.
3. No retrieved passage supplies South Australian threatening-message or stalking
   law, a South Australian territorial-nexus rule, or Commonwealth s 4C. Three of
   the six passages instead concern unrelated unauthorised access, computer fraud,
   or child-exploitation offences.

The federal safeguard appears in the current official
[Crimes Act 1914 (Cth) s 4C](https://www.legislation.gov.au/C1914A00012/2024-01-08/2024-01-08/text/original/epub/OEBPS/document_1/document_1.html).
Current South Australian legislation includes unlawful-threat and electronic
stalking/harassment provisions:
[Criminal Law Consolidation Act 1935 (SA)](https://www.legislation.sa.gov.au/_legislation-documents/lz/c/a/criminal-law-consolidation-act-1935/current/1935.2252.auth.pdf).

**Why it matters:** the answer is prudent about the police interview and correctly
recognises concurrent exposure, but it does not fully answer the user's express
question about the third jurisdiction or duplicate operation.

**Root cause:** retrieval miss. The answer's caution prevents this from becoming a
full fail.

**Required correction:** retrieve the South Australian offence and territorial
nexus provisions and Commonwealth s 4C; distinguish concurrent charging from
double punishment.

---

### au-012 — Not satisfactory

**Question tested:** Queensland security of payment and licensing despite NSW
incorporation and a NSW choice-of-law clause.

**Exact defects:**

1. The answer says the materials **“specifically identify the subcontractors'
   charge mechanism”** and then makes that the centre of the Queensland analysis.
2. It does not explain the ordinary statutory sequence of payment claim, payment
   schedule, failure to pay or schedule, adjudication application, and recovery or
   suspension rights.
3. It introduces NSW direct-debt and security-of-payment material even though all
   construction work, claims, and alleged defects arose in Queensland.
4. It repeatedly tells the user what **“the materials provided”** do or do not
   contain, including that Queensland licensing provisions were missing. This
   directly breaches the prompt.

The current ordinary Queensland pathway is in `Building Industry Fairness
(Security of Payment) Act 2017 (Qld) ss 75–79`:
[current Queensland Act](https://www.legislation.qld.gov.au/view/whole/pdf/current/act-2017-043).

**Log evidence:** the six retrieved passages focus on subcontractors' charges,
insolvency, generic multistate payment rights, and NSW direct-debt provisions. They
do not supply the Queensland ss 75–79 sequence or detailed Queensland licensing
rules. The answer follows that skewed set instead of making the ordinary payment
process the primary unresolved issue.

**Why it matters:** a subcontractors' charge is a separate, technical remedy. It
does not substitute for the ordinary security-of-payment process the user
specifically asked about.

**Root cause:** major retrieval miss plus answer-generation and prompt-compliance
failure.

**Required correction:** lead with Queensland ss 75–79 and the exact deadline
triggered by the actual payment history. Treat a subcontractors' charge as a
separate option. Remove NSW statutory detail unless it is necessary to explain why
the contractual clause cannot displace mandatory Queensland law.

---

### au-016 — Not satisfactory

**Question tested:** treatment of conflicting NSW and Victorian intermediate
appellate decisions on a common-law question in Queensland.

**Exact defects:**

1. All six retrieved passages are duplicates or near-duplicates about leave to
   appeal from interlocutory decisions. None concerns interstate precedent,
   *Farah Constructions*, or *Hill v Zuda*.
2. The answer says the Queensland court may choose the approach it regards as
   **“legally preferable.”** That materially understates the Australian
   intermediate-appellate methodology.
3. A court considering another Australian intermediate appellate decision on the
   common law of Australia should apply the *Farah/Hill* discipline and should not
   depart without the required plainly-wrong or compelling-reason basis. Conflicting
   coordinate authorities complicate the analysis but do not turn it into an
   unconstrained preference.
4. The References section contains only a statement that no citations were
   included. That is not a valid reference.

The High Court's current authoritative restatement is
[*Hill v Zuda Pty Ltd* [2022] HCA 21](https://www.hcourt.gov.au/cases-and-judgments/judgments/judgments-1998-current/hill-v-zuda-pty-ltd).

**Why it matters:** this query directly tests how a federal legal system handles
horizontal authority. The answer misses the controlling method.

**Root cause:** catastrophic retrieval miss, answer-generation omission, and
prompt-design weakness. The prompt's current cross-jurisdiction section says an
intermediate appellate decision should be preferred unless a higher authority in
the retrieved data departs, but does not state the *Farah/Hill* test or explain how
to handle conflicting coordinate decisions.

**Required correction:** add the *Farah/Hill* rule to the prompt; retrieve the
controlling High Court authority; and apply that method to the conflicting NSW and
Victorian cases before considering recency, unanimity, reasoning, and factual fit.

## Satisfactory answers

| Query | Why it passes | Residual issue or log observation |
|---|---|---|
| **au-001** | Correctly separates federal employment rights from Victorian workers' compensation and safety obligations and gives useful immediate steps. | Retrieval contained workers' compensation material only and was largely current to 2014–2015. Federal and safety propositions were therefore mostly general and uncited. Refreshing the source set would improve reliability. |
| **au-008** | Correctly treats the law of the land's location as controlling the NSW and Queensland conveyances and separates the Commonwealth corporate layer. | One retrieved passage concerned ACT strata management and the set was dated 2016–2023. The answer still avoided applying Victorian property law. |
| **au-013** | Correctly rejects automatic federal override and explains direct inconsistency, federal right or privilege, simultaneous obedience, and covering the field. | Strongest retrieval set in the run. The answer is much too long. |
| **au-014** | Correctly proceeds under Commonwealth copyright law without demanding a State and identifies the contractor-ownership problem and evidence steps. | Retrieval was mostly current only to January 2017. |
| **au-015** | Correctly proceeds under Commonwealth corporations law and distinguishes company loss, personal loss, oppression, derivative action, and directors' duties. | One of six retrieved passages was an irrelevant real-property result. Several cases are given in multiple citation forms. |
| **au-017** | Correctly refuses to give State-specific tenancy rights or tribunal advice until the property jurisdiction is known. | Retrieval was multistate and potentially tempting; the clarification gate worked as intended. |
| **au-018** | Correctly requests accident location, exact date, and procedural history before giving limitation and forum advice. | All six retrieved passages concerned product liability or food law rather than supermarket occupier negligence. The clarification gate prevented that retrieval error from entering the answer. |

## Retrieval audit

The logs confirm six context passages were supplied for every query. Retrieval
quality varied substantially.

| Query | Retrieval assessment |
|---|---|
| **au-001** | Narrow and old: workers' compensation only; no federal employment or Victorian safety source. |
| **au-002** | Mixed-jurisdiction contamination: two Victorian sale-of-goods passages inserted into a Queensland transaction. |
| **au-003** | WA-only set; no Commonwealth environmental authority. |
| **au-004** | General health confidentiality/privacy set; no federal NDB provisions. |
| **au-005** | ACT-heavy set; federal passage lacks the operative discrimination and employment provisions. |
| **au-006** | Good publication and choice-of-law material; no limitation or concerns-notice provisions. |
| **au-007** | Relevant NT/Queensland/NSW connection material, but no ACT source and several passages are 12–15 years old. |
| **au-008** | Broad multistate property set; some irrelevant and old material. |
| **au-009** | Correctly identifies WA's special family-law position but supplies the federal, not WA, application-period provision. |
| **au-010** | Stale and internally contradictory AAT/ART migration material. |
| **au-011** | Missing SA territorial/offence law and Commonwealth s 4C; half the set is unrelated cybercrime material. |
| **au-012** | Skewed toward charges, insolvency, and NSW direct debt; omits the ordinary Queensland payment/adjudication sequence. |
| **au-013** | Strong, focused Commonwealth inconsistency material. |
| **au-014** | Topically relevant but mostly current only to 2017. |
| **au-015** | Mostly useful corporations material with one irrelevant property result. |
| **au-016** | Complete miss: six repetitive interlocutory-appeal passages, no precedent methodology. |
| **au-017** | Multistate tenancy material; model correctly requested the jurisdiction. |
| **au-018** | Wrong cause-of-action family; model correctly requested the jurisdiction before using it. |

### Retrieval conclusion

The most important new finding from the logs is that **more context did not mean
better coverage**. au-011 received the largest context payload—43,506 characters
and 14,472 input tokens—but still lacked the South Australian and Commonwealth
provisions needed to answer the question. au-016 received 39,591 characters, but
all six passages concerned the wrong procedural topic.

Retrieval remediation requires work outside this prompt-engineering workspace. No
retrieval or application changes have been made as part of this review.

## Prompt-compliance and output-quality findings

### 1. Hidden-source leakage

The prompt says never to tell the user that sources or data are missing. The
answers nevertheless refer explicitly to the hidden source set.

The clearest examples are:

- au-003: “The materials provided do not include the Commonwealth environmental
  statute”;
- au-005: “They do not set out a specific statutory rule here”;
- au-012: repeated statements about what “the materials provided” contain or omit.

Less direct source-set language also appears in au-004, au-008, au-011, au-013, and
au-015. This behaviour should be treated as an output-compliance failure even when
the legal content is otherwise acceptable.

### 2. Excessive length

Thirteen of 18 answers exceed 2,000 words. The median is approximately 2,280 words.
The two clarification answers are short; the median among substantive answers is
therefore higher.

The answer generator produced 59,877 output tokens across the run. au-013 alone
used 5,129 output tokens, took 59.5 seconds, cost US$0.093447, and produced 21,137
response characters.

The repeated material normally appears across the issue list, each IRAC
conclusion, the action plan, and the risk table. A normal substantial answer should
target roughly 1,000–1,500 words unless the user asks for a detailed memorandum.

### 3. Citation formatting

The legal content is generally traceable to retrieved authority names, but citation
format is inconsistent with the prompt:

- legislation is repeatedly bolded in the body;
- legislation is italicised in References in au-007, au-009, au-010, and au-014;
- *Gutnick* is given in both authorised-report and medium-neutral form in au-006;
- several au-015 cases have multiple alternative citations; and
- au-016 creates a References section without an authority.

The failure is formatting and authority selection, not evidence of fabricated
authority names.

### 4. Structure

All 18 answers contain one disclaimer. The 16 substantive answers generally use
the required order. au-007 is the only issue/analysis count mismatch.

## Gateway performance

| Metric | Total | Per-answer median | Per-answer range |
|---|---:|---:|---:|
| Input tokens | 180,462 | 9,579 | 7,761–14,472 |
| Output tokens | 59,877 | 3,607 | 485–5,129 |
| Cost | US$1.286814 | US$0.073736 | US$0.017952–US$0.093447 |
| Duration | 701,242 ms summed | 40,827 ms | 7,307–59,467 ms |
| Retrieved context | — | 21,140 chars | 14,080–43,506 chars |
| Response size | — | 15,465 chars | 1,545–21,137 chars |

The summed duration is not wall-clock run time because the suite ran with
parallelism 5.

The logs show no input caching for 11 answers and 3,968 cached input tokens for
seven answers. Performance is acceptable for a diagnostic run, but the answer
length is a direct contributor to latency and cost.

## Remediation plan

### Priority 1 — answer-safety controls

1. Add a final jurisdiction check requiring every statute and deadline to be tied
   to the governing legal stream before it is used.
2. Prohibit applying another State's statute merely because a party is located
   there or the contract selects a forum.
3. Require a decision-specific deadline source for migration, family, construction,
   and other strict-time-limit matters.
4. Require the ordinary payment-claim/adjudication pathway to be addressed before
   secondary construction remedies.
5. Add the *Farah/Hill* plainly-wrong or compelling-reason methodology expressly to
   the prompt.

### Priority 2 — retrieval requirements for the development team

1. Add jurisdiction-aware reranking or filtering so a party's domicile does not
   pull an irrelevant State statute into a transaction governed elsewhere.
2. Add freshness controls for tribunal names and deadline provisions.
3. Penalise duplicate passages; au-016 used six slots on the same wrong topic.
4. Add minimum coverage checks for every jurisdiction or legal stream expressly
   requested.
5. For missing critical coverage, return no source for that proposition rather
   than an adjacent but misleading source.

These are recommendations only. They require work outside the permitted scope of
this workspace.

### Priority 3 — output discipline

1. Never mention retrieved materials, sources, context, or missing data to the
   user.
2. Use one formal citation per case, following the prompt's citation hierarchy.
3. Keep legislation in plain text; italicise case names only.
4. Omit `## References` when no authority is cited.
5. Target 1,000–1,500 words for an ordinary substantive answer and remove repeated
   conclusions.

## Release decision

**Do not approve Australia v1.0 on this run.**

The suite should be rerun unchanged after the five material failures are addressed.
A release candidate should, at minimum:

- have no Commonwealth/State substitution;
- use current tribunal names and decision-specific deadlines;
- state the *Farah/Hill* interstate-precedent rule;
- cover the primary statutory pathway requested by the user;
- avoid exposing the hidden source set; and
- contain no material wrong-jurisdiction retrieval in the rendered answer.

The clarification gates in au-017 and au-018 and the constitutional analysis in
au-013 should be preserved as positive regression targets.
