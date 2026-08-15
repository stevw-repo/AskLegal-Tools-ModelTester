# Australia “v1.1” Federal–State Suite Review

## Log-informed review and deployment audit

**Review date:** 29 July 2026  
**Test run:** 29 July 2026, 16:11–16:13 GMT+8  
**Model:** `gpt-5.4`, low reasoning effort  
**Parallelism:** 5  
**Suite:** `testing/suites/australia/au-federal-state-v1.json`  
**Answers:** `testing/results/australia/au-prompt-v1.1.md`  
**Cloudflare index:** `testing/temp/australia-v1.1-review/log-summary.csv`

## Executive verdict

**Do not treat this as a valid v1.1 answer-prompt test.**

The exact deployment issue is that all 18 Cloudflare answer-generation requests
contain `# Answer Generation System Prompt - Australia v1.0`. None contains
v1.1. The local v1.1 file is correctly versioned and contains the intended new
controls, but it was not the prompt sent to the model.

This run can still test the deployed retrieval change because the six retrieved
passages are visible in each final request. It cannot show whether the v1.1
answer-prompt changes fixed:

- interstate appellate precedent handling;
- hidden-source language;
- decision-specific forums and deadlines; or
- prioritisation of the ordinary primary statutory pathway.

On the answers actually produced—**v1.0 answer prompt plus the changed retrieval
pipeline**—the suite is not satisfactory as a whole:

| Rating | Queries | Count |
|---|---|---:|
| **Satisfactory** | au-002, au-008, au-013, au-014, au-015, au-017, au-018 | 7 |
| **Needs revision** | au-003, au-004, au-005, au-006, au-007, au-009, au-011 | 7 |
| **Not satisfactory** | au-001, au-010, au-012, au-016 | 4 |

Compared with the earlier v1.0 run, the pass count remains 7. au-002 improves
from fail to pass, au-009 improves from fail to revision, and au-001 regresses
from pass to fail. The number of material failures falls from five to four, but
the remaining failures still cover the suite’s central risks.

## Evidence and method

The 18 retained Cloudflare logs were matched by exact query and conversation ID.
All returned HTTP 200. The request payload for every answer was checked for:

- the deployed system-prompt heading;
- the exact suite query;
- the six retrieved context passages;
- Cloudflare conversation and log IDs; and
- token, cost, cache, reasoning, duration, and endpoint metadata.

Two later high-token logs were excluded because their queries and conversation
IDs did not match the suite. Embedding and short preprocessing calls were not
included in the answer-log export.

The legal review used the answer text, the six retrieved passages, the earlier
v1.0 export for comparison, and current primary or official sources where the
answer’s accuracy depended on current law.

## Exact deployment defect

This is not a cosmetic version-label problem.

The local v1.1 prompt adds four controls that directly target the old review’s
failures:

1. the *plainly wrong / compelling reason* discipline for interstate
   intermediate appellate decisions;
2. an explicit ban on phrases such as “materials provided”, “source materials”,
   and “available material”;
3. a requirement to address the ordinary primary statutory pathway before
   collateral remedies; and
4. decision-specific safeguards for forum names and numeric deadlines.

The run reproduces defects addressed by all four controls. Because Cloudflare
shows v1.0 in every request, those repetitions cannot be counted as evidence
that the v1.1 edits failed. They show that v1.1 was not exercised.

## Retrieval-pipeline verdict

**The limited Stage 0/Stage 1 change is partially helpful but insufficient on
its own.**

The State-safe filter is narrow by design. It can block a mixed
`CTH + unrequested State` record that previously passed merely through the
shared `CTH` code. It does not guarantee:

- coverage of every Commonwealth/State/Territory stream in the question;
- topical relevance within an allowed jurisdiction;
- current law;
- removal of duplicates; or
- retrieval of a missing primary pathway.

Those limitations are visible in the run:

| Retrieval result | Queries | Finding |
|---|---|---|
| **Focused / adequate for the core federalism issue** | au-008, au-013, au-014, au-015 | The governing stream is clear and the retrieved set supports the answer’s central distinction. |
| **Safe clarification despite weak context** | au-017, au-018 | The model asks for the missing State/Territory instead of applying an arbitrary regime. |
| **Some improvement, residual gap** | au-002, au-007, au-009, au-011 | Wrong-State use is reduced in the rendered answer, but the source set remains incomplete, stale, or repetitive. |
| **Material coverage or topical failure** | au-001, au-003, au-004, au-005, au-006, au-010, au-012, au-016 | A governing legal stream, current procedure, or the requested primary pathway is absent or displaced by adjacent material. |

### What improved

- **au-002:** the answer no longer applies Victorian sale-of-goods provisions to
  the Queensland installation merely because the seller and forum term are
  Victorian. It separates the forum clause from applicable substantive law.
- **au-009:** the answer no longer transfers the Commonwealth
  `Family Law Act 1975 (Cth) s 44` period to the WA de facto property claim.
- **au-011:** several specific wrong-State cybercrime results from the old run
  disappear, and the answer identifies Commonwealth, SA, and Tasmanian streams.
- **au-007:** the answer is more cautious about contract/payroll and injury
  location, although the retrieval set still does not cover all relevant
  connection tests.

### What did not improve

- **Coverage:** au-003 still has no Commonwealth EPBC/referral source; au-004 no
  federal NDB provisions; au-005 no operative federal pregnancy/employment
  provisions; au-006 no limitation/concerns-notice provisions; and au-012 no
  ordinary Queensland payment-claim/adjudication sequence.
- **Freshness:** au-001 uses 2014–15 workers’ compensation material and misses
  Victoria’s mental-injury changes effective 31 March 2024. au-010 still
  contains legacy migration-review terminology.
- **Duplication:** au-011 retrieves three copies of the same child-grooming topic.
  au-016 retrieves five copies of the same interlocutory-appeal topic plus an
  irrelevant foreign-law passage.
- **Topicality:** au-016 remains a complete miss for Australian interstate
  precedent methodology.

The result is consistent with the intended minimal scope: State filtering can
reduce one class of contamination, but it cannot repair missing coverage,
freshness, duplication, or semantic-topic selection.

## Exact issue register

### au-001 — Not satisfactory

**Exact issue:** the answer correctly identifies Victoria as the likely workers’
compensation jurisdiction, then states that the Victorian psychological-injury
test is unavailable and imports the NSW `s 11A` reasonable-management-action
provision and NSW cases into the practical analysis. It advises the user to
prepare for that defence even though no basis is established for NSW workers’
compensation law to govern.

The retrieval set caused the problem: it contains an NSW “specified actions”
passage but no current Victorian mental-injury test and no Commonwealth
employment or Victorian workplace-safety material. Current Victorian eligibility
rules changed for injuries on or after 31 March 2024 and include a DSM diagnosis,
significant dysfunction, predominant employment causation, and Victorian
exclusions: [WorkSafe Victoria — worker’s injury claim form](https://www.worksafe.vic.gov.au/workers-injury-claim-form).

**Required correction:** retrieve current Victorian mental-injury,
management-action, and workplace-safety material plus the relevant Commonwealth
employment stream. Do not use NSW `s 11A` as a substitute.

### au-002 — Satisfactory, with a retrieval limitation

**Exact result:** the answer treats the ACL/Queensland installation and safety
issues separately from the Victorian forum term and does not repeat the earlier
cross-State statutory substitution. That is the core federalism test.

**Residual issue:** two Victorian sale-of-goods passages remain in retrieval,
while the earlier Queensland electrical-safety passage disappears. The practical
safety/licensing route and the basis for QCAT jurisdiction are therefore more
generic than they should be.

### au-003 — Needs revision

**Exact issue:** all six passages concern WA/local/mining or WA environmental
processes. No passage covers the Commonwealth EPBC referral, controlled-action,
assessment, or approval track. The answer can only state the federal stream in
general terms and explicitly refers to “source material”.

A project that may significantly affect a protected matter can require a
Commonwealth referral and, if declared a controlled action, federal assessment
and approval independently of State approvals:
[DCCEEW — referrals and environmental assessments](https://www.dcceew.gov.au/environment/epbc/approvals).

**Required correction:** retrieve the Commonwealth protected-matter referral and
controlled-action pathway alongside the WA and local tracks.

### au-004 — Needs revision

**Exact issue:** the answer recognises concurrent Commonwealth, Victorian, and
Tasmanian obligations, but the retrieved Commonwealth passages are general
confidentiality/privacy material rather than `Privacy Act 1988 (Cth) pt IIIC`.
The 72-hour plan therefore does not anchor suspected-breach assessment,
notification to the Commissioner, or notification to individuals to the
operative provisions.

The federal scheme requires reasonable and expeditious assessment and, where an
eligible data breach is established, a statement to the Commissioner as soon as
practicable:
[Privacy Act 1988 (Cth) pt IIIC](https://www.legislation.gov.au/C2004A03712/latest/text).

**Required correction:** retrieve `ss 26WE, 26WH and 26WK–26WL` and current
Victorian/Tasmanian regulator or complaint routes.

### au-005 — Needs revision

**Exact issue:** retrieval is ACT-heavy. Its federal passage does not supply the
operative pregnancy-discrimination and employment provisions or a current
federal complaint path. The answer consequently gives a detailed ACT route but
only a generic Commonwealth route and does not provide a dependable comparison
of deadlines, remedies, or duplication risks. It also repeatedly exposes the
hidden source set.

The directly relevant federal provisions include
`Sex Discrimination Act 1984 (Cth) ss 7 and 14`:
[Federal Register of Legislation](https://www.legislation.gov.au/Current/C2004A02868).

**Required correction:** retrieve the federal substantive provisions and current
complaint route, then compare them against the ACT process on equal footing.

### au-006 — Needs revision

**Exact issue:** the answer’s place-of-publication and choice-of-law analysis is
useful, but retrieval contains no limitation or concerns-notice provisions. The
urgent pre-action portion is generic despite being expressly requested.

Current uniform defamation legislation includes a mandatory concerns-notice
gate, illustrated by
[Defamation Act 2005 (NSW) ss 12A–12B](https://legislation.nsw.gov.au/view/whole/html/2025-03-02/act-2005-077).

**Required correction:** retrieve the current limitation and concerns-notice
rules for the likely governing jurisdiction and calculate the procedural sequence
from the publication dates.

### au-007 — Needs revision

**Exact issue:** the answer correctly rejects both “NSW because payroll is
there” and “NT because the injury occurred there” as automatic rules. However,
the six passages are mainly 2011–14 material, omit a full Queensland connection
analysis despite the Queensland work history, and use an ACT passage as the
principal comparator. The answer also mentions “material provided”.

**Required correction:** retrieve current connection tests for each genuinely
contending scheme—ACT, NSW, Qld, and NT—then apply their ordered tests without
using one jurisdiction’s text as a generic substitute.

### au-008 — Satisfactory

**Exact result:** the answer correctly rejects Victorian incorporation/signing as
the determinant of land law. It separates NSW and Queensland land,
conveyancing, registration, and duty questions and limits Commonwealth corporate
law to genuinely national issues.

**Residual issue:** retrieval is general and contains no specific current
transfer-duty provisions, so numeric duty advice is appropriately avoided.

### au-009 — Needs revision

**Exact issue:** the prior direct error is fixed: the answer does not use the
Commonwealth `s 44` deadline for WA de facto property proceedings. It correctly
separates WA property/maintenance, federal parenting, and the superannuation
overlay. However, none of the six passages contains the WA application period,
and the action plan omits it.

WA court guidance states that a de facto property/financial application is
generally required within two years after breakdown, with court permission
needed out of time:
[Family Court of Western Australia — property and financial](https://familycourt.wa.gov.au/P/property_and_financial.aspx).

**Required correction:** retrieve current `Family Court Act 1997 (WA) s 205ZB`
and state the WA trigger, period, and leave rule.

### au-010 — Not satisfactory

**Exact issue:** the answer repeatedly calls the current ART pathway the
“Migration and Refugee Division”, a former AAT structure, and overlays generic
ART deadline/extension concepts on migration review. It warns that the letter
controls but still provides an unsafe generic framework.

The current scheme uses Migration and Protection **jurisdictional areas**, and
some cancellation reviews have decision-specific, non-extendable time rules.
For example, `Migration Act 1958 (Cth) s 500(6B)` prescribes nine days for
certain `s 501` or `s 501CA(4)` decisions and disapplies the general ART timing
provisions:
[Migration Act 1958 (Cth) s 500](https://www.legislation.gov.au/C1958A00062/latest/text).

**Required correction:** use current ART terminology and give no numeric period
or extension rule unless the source ties it to the exact cancellation decision.

### au-011 — Needs revision

**Exact issue:** the answer now identifies plausible SA, Tasmanian, and
Commonwealth offence streams, which is an improvement. It says concurrent
offences may apply, but omits the federal double-punishment safeguard. The
retrieved set contains no `Crimes Act 1914 (Cth) s 4C` and wastes three of six
slots on duplicate child-grooming passages unrelated to the facts.

Section 4C(2) prevents Commonwealth punishment for the same act or omission
after punishment under State or Territory law:
[Crimes Act 1914 (Cth) s 4C](https://www.legislation.gov.au/C1914A00012/latest/text).

**Required correction:** retrieve `s 4C` and relevant SA territorial/offence
material; deduplicate the child-grooming passages.

### au-012 — Not satisfactory

**Exact issue:** the answer correctly rejects the proposition that a NSW
choice-of-law clause automatically displaces mandatory Queensland law. But it
centres the collateral subcontractor-charge remedy and does not explain the
ordinary Queensland security-of-payment sequence requested by the user:
payment claim, payment schedule, non-payment consequences, adjudication, debt
recovery, and suspension rights.

Those primary steps appear in the current
[Building Industry Fairness (Security of Payment) Act 2017 (Qld), ch 3](https://www.legislation.qld.gov.au/view/whole/pdf/inforce/current/act-2017-043),
including `ss 75–79`.

**Required correction:** retrieve and address the Chapter 3 pathway first; keep
charges, PPSA, insolvency, and licensing as separate secondary streams.

### au-013 — Satisfactory

**Exact result:** the answer correctly explains that a Commonwealth licence does
not automatically create a positive right overriding State law. It distinguishes
direct inconsistency, covering-the-field questions, and the possibility of
simultaneous obedience. Retrieval is focused on Commonwealth inconsistency.

### au-014 — Satisfactory

**Exact result:** the answer correctly treats copyright ownership and
infringement as principally Commonwealth questions and does not demand a State
before giving useful analysis. One parallel-import/integrated-circuit passage is
irrelevant, but it does not contaminate the rendered answer.

### au-015 — Satisfactory

**Exact result:** the answer correctly treats directors’ duties, oppression,
derivative action, and urgent corporate relief as principally Commonwealth
corporations-law issues. It does not invent a State-law dependency merely
because location is omitted.

### au-016 — Not satisfactory

**Exact issue:** the answer says the NSW and Victorian appellate decisions are
“persuasive, not binding” and recommends choosing the reasoning that best fits,
often favouring the newer unanimous NSW decision. That materially understates
the Australian precedent discipline. A Queensland trial court should not treat
an interstate intermediate appellate decision on the common law of Australia as
freely optional merely because it comes from another State.

The current High Court formulation is that a trial judge or intermediate
appellate court should not depart from another Australian intermediate appellate
decision on Commonwealth law, uniform national legislation, or the common law
unless it is plainly wrong or there is a compelling reason:
[*Hill v Zuda Pty Ltd*](https://www.hcourt.gov.au/cases-and-judgments/judgments/judgments-1998-current/hill-v-zuda-pty-ltd);
see also [*Lendlease Corporation Ltd v Pallas* [2025] HCA 19, [109]](https://www.hcourt.gov.au/sites/default/files/eresources/2025-07-03/HCA/Lendlease%20Corporation%20Ltd%20v%20Pallas%20%28S108-2024%29%20%5B2025%5D%20HCA%2019.pdf).

Retrieval is a complete miss: five near-duplicate interlocutory-appeal passages
and one NSW foreign-law passage, with no precedent methodology.

**Required correction:** retrieve *Farah*, *Hill*, or equivalent precedent
methodology and rerun with the actual v1.1 prompt. The local v1.1 edit directly
targets this defect, but this run did not test it.

### au-017 — Satisfactory

**Exact result:** the model asks for the State or Territory before analysing a
seven-day termination notice, bond, carpet liability, or tribunal. That is the
correct jurisdictional gate.

### au-018 — Satisfactory

**Exact result:** the model asks where the fall occurred before applying a
limitation period, civil-liability statute, court, or pre-court process. It avoids
using the retrieved product-liability limitation material for a premises
negligence claim.

## Prompt-compliance and output findings

### Hidden-source leakage

Explicit or implicit source-set language appears in eight answers:

- au-001 — “materials provided”;
- au-002 — “material available”;
- au-003 — “source material”;
- au-005 — “material available” / “material provided”;
- au-007 — “material provided”;
- au-009 — “source material”;
- au-011 — “materials available”; and
- au-012 — “material available”.

This remains a compliance failure under v1.0. It is not a valid test of the
stronger v1.1 prohibition because v1.1 was not deployed.

### Length

Thirteen of 18 answers exceed 2,000 words, the same count as the old run. The
median rises from approximately 2,280 words to 2,384.5 words. The longest
answers are au-012 (3,448 words) and au-001 (3,360 words). The two clarification
answers remain appropriately short.

### Structure

The clarification gates work in au-017 and au-018. The substantive answers
generally follow the required sections, but the repeated issue statement,
conclusion, action plan, and risk material continue to inflate length.

## Gateway performance

| Metric | This run | Earlier v1.0 run | Change |
|---|---:|---:|---:|
| Input tokens | 186,671 | 180,462 | +6,209 (+3.4%) |
| Output tokens | 60,427 | 59,877 | +550 (+0.9%) |
| Cost | US$1.257019 | US$1.286814 | −US$0.029796 (−2.3%) |
| Summed duration | 790,192 ms | 701,242 ms | +88,950 ms (+12.7%) |
| Retrieved context | 452,050 chars | 429,124 chars | +22,926 (+5.3%) |
| Response size | 265,688 chars | 258,352 chars | +7,336 (+2.8%) |

Per-answer medians in this run:

| Metric | Median | Range |
|---|---:|---:|
| Input tokens | 9,874.5 | 7,232–17,011 |
| Output tokens | 3,590 | 327–4,984 |
| Cost | US$0.072707 | US$0.017177–US$0.098273 |
| Duration | 48,049.5 ms | 7,281–63,300 ms |
| Retrieved context | 21,921 chars | 11,468–55,321 chars |
| Response length | 2,384.5 words | 196–3,448 words |

The duration total is not wall-clock suite time because the run used
parallelism 5.

## Release and retest decision

**Do not approve v1.1 from this run.**

The next run should use the same 18 queries and verify, from Cloudflare before
substantive scoring, that every request begins with:

```text
# Answer Generation System Prompt - Australia v1.1
```

Minimum acceptance checks:

1. 18 of 18 logs show v1.1.
2. au-016 states the plainly-wrong / compelling-reason discipline.
3. au-010 uses current ART terminology and no unsupported generic deadline.
4. au-012 addresses the ordinary Queensland Chapter 3 pathway first.
5. No answer mentions materials, sources, retrieval, context, or source coverage.
6. au-001 does not substitute NSW `s 11A` for current Victorian mental-injury
   law.

The retrieval change should be judged as a narrow State-safety improvement, not
as a complete retrieval fix. It reduces some cross-State contamination but
leaves missing coverage, stale material, duplicates, and topical misses
unchanged.
