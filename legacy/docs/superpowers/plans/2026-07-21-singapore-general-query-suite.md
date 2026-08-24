# Singapore General Query Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Singapore contract-and-tort query suite with an 18-question, commercially weighted general Singapore law suite.

**Architecture:** Store the test inputs as one schema-minimal JSON array and keep the suite contract in the existing suite README. Validate the static artifact locally with Python's standard-library JSON parser and explicit schema assertions.

**Tech Stack:** JSON, Markdown, Python 3 standard library

## Global Constraints

- Use English, Singapore-specific facts, and a first-person perspective throughout.
- Use IDs `sg-001` through `sg-018` with no gaps or duplicates.
- Each JSON object contains only `id` and `query`.
- Use approximately four short, ten medium, and four detailed multi-issue queries.
- Cover twelve commercial or business matters and six personal or consumer matters.
- Do not run the Ask.Legal API.
- Do not change application pipelines, retrieval systems, databases, deployment infrastructure, or production configuration.
- This workspace is not a Git repository, so commit steps are unavailable.

## File Structure

- Create `testing/suites/singapore/sg-general-v1.json`: the complete reusable 18-question suite.
- Modify `testing/suites/README.md`: replace obsolete contract-and-tort requirements with the general-suite contract and coverage map.
- Delete `testing/suites/singapore/sg-contract-tort-v1.json`: remove the superseded suite.

---

### Task 1: Create and validate the general Singapore suite

**Files:**
- Create: `testing/suites/singapore/sg-general-v1.json`

**Interfaces:**
- Consumes: the suite schema documented in `testing/suites/README.md` and the approved coverage in `docs/superpowers/specs/2026-07-21-singapore-general-query-suite-design.md`.
- Produces: a JSON array of exactly 18 objects, each shaped as `{"id": string, "query": string}`.

- [ ] **Step 1: Run the pre-creation check**

Run:

```bash
python3 -c "from pathlib import Path; assert Path('testing/suites/singapore/sg-general-v1.json').is_file()"
```

Expected: FAIL with `AssertionError` because the replacement file does not exist yet.

- [ ] **Step 2: Create the suite with the approved coverage and query mix**

Create `testing/suites/singapore/sg-general-v1.json` with exactly this content:

```json
[
  {
    "id": "sg-001",
    "query": "I run a Singapore food-import business and signed a one-year agreement for a supplier to deliver 60,000 custom containers in monthly batches. The supplier promised by email that the first batch would arrive before my supermarket launch, but it arrived three weeks late and 8,000 containers leaked. The signed terms require defects to be reported within seven days, cap liability at the price of the affected batch, and exclude loss of profit and claims from my customers. I reported the leaks on day nine because they appeared only during filling. The supermarket has charged me S$42,000 for missed deliveries, and replacing the containers urgently cost S$18,000. Please analyse breach, whether the email promise and limitation clauses matter, what losses may be recoverable, and how I should preserve my position while continuing to trade."
  },
  {
    "id": "sg-002",
    "query": "I bought a small Singapore logistics company after an accounting firm reviewed its records and reported that its largest customer had renewed for three years. The seller had only an unsigned draft renewal, and the customer left two months after completion. The accountant says it relied on management information and points to a retainer limiting liability to twice its S$25,000 fee. The seller says I conducted my own due diligence. I paid S$900,000 for the company and believe it was worth far less without that customer. What claims might I have for misrepresentation or professional negligence, and what evidence and valuation work would I need?"
  },
  {
    "id": "sg-003",
    "query": "I own 25% of a Singapore private company and the other two shareholders are also its directors. Over the past year, they have paid a company owned by one director's spouse S$180,000 in management fees, moved a major customer to a new business they own, and stopped giving me management accounts. They have now called a meeting to issue enough new shares to reduce my stake below 10%, saying the company urgently needs cash, although they rejected my offer to invest on the same terms. The shareholders' agreement requires unanimous approval for related-party transactions but contains no exit mechanism. Please assess possible breaches of directors' duties and minority oppression, the remedies and urgent interim measures I could seek, and the records I should obtain before taking action."
  },
  {
    "id": "sg-004",
    "query": "I guaranteed a bank loan for my Singapore company after the relationship manager told me my exposure would be capped at S$80,000. The signed document appears to be an unlimited all-moneys guarantee. I signed it at the branch without independent advice, and the bank later increased the company's facility without notifying me. The company has now defaulted, and the bank is demanding S$240,000. Please assess whether the guarantee and increased facility are enforceable against me, what evidence matters, and how I should respond to the demand."
  },
  {
    "id": "sg-005",
    "query": "I was a senior sales manager at a Singapore medical-device company. My employer dismissed me immediately after discovering that I emailed a customer spreadsheet to my personal account, although I did so to work from home and did not send it elsewhere. It is withholding S$35,000 in commission and threatening an injunction because I accepted a competitor's offer. My contract has a twelve-month Asia-wide non-compete clause and confidentiality obligations with no time limit. Please assess the dismissal, unpaid commission, confidentiality risk, and whether the restraint is likely to be enforceable."
  },
  {
    "id": "sg-006",
    "query": "I paid a freelance developer in Singapore to create my company's booking platform and brand logo. Our emails describe the deliverables and price but do not expressly assign intellectual property. The developer has now licensed similar code and the same logo concept to a competitor, while claiming that I bought only a right to use the work. Who is likely to own the copyright, and what practical steps can I take to stop the competitor's launch?"
  },
  {
    "id": "sg-007",
    "query": "I operate a Singapore online retailer. A ransomware attack encrypted our customer database, and the attacker sent a sample containing names, addresses, telephone numbers, order histories, and password hashes for about 18,000 customers. Our cloud vendor says an administrator account was accessed using a password that one of my employees had reused; my employee says the vendor failed to enforce multi-factor authentication despite promising it in the service proposal. We restored the site from backups, but the attacker is demanding payment and threatens to publish the data within 48 hours. We have not contacted customers or any authority because we do not yet know whether all records were copied. Give me a prioritized action plan covering containment, investigation, evidence, notification obligations, communications, the cloud vendor, and potential liability."
  },
  {
    "id": "sg-008",
    "query": "I manage sales for a Singapore distributor. Two competing distributors suggested that we stop discounting below an agreed price and divide major customers between us. Our shared supplier supports the idea and has offered extra rebates if everyone follows it. No agreement has been signed, but my managing director told me to reply that we are interested and attend a meeting next week. What legal risk would this create for me and the company, and what should I do with the emails and meeting invitation?"
  },
  {
    "id": "sg-009",
    "query": "I lease a shophouse in Singapore for my restaurant. Repeated pipe leaks from the unit above have forced me to close twice, but my landlord says the lease makes all repairs my responsibility. I withheld one month's rent after the landlord ignored my notices, and it has now threatened to re-enter the premises. The lease also excludes liability for interruption to my business. What are my options and immediate risks?"
  },
  {
    "id": "sg-010",
    "query": "I am a Singapore electrical subcontractor owed S$160,000 on a completed commercial project. I served a payment claim under the contract, but the main contractor did not provide a payment response and now says it will deduct S$110,000 for delay and defective cabling. Most alleged defects were raised only after my claim, and the main contractor is holding both retention money and my final progress payment. Please explain whether adjudication may be available, the significance of the missing response, the deadlines and documents that matter, and how adjudication would interact with a later court or arbitration claim."
  },
  {
    "id": "sg-011",
    "query": "My Singapore company is owed S$185,000 for equipment supplied six months ago. The customer admits the invoices but says it cannot pay, has transferred several machines to a related company, and has offered 30 cents on the dollar if I agree this week. Other creditors are also demanding payment. Should I accept, sue for the debt, use an insolvency process, or try to challenge the asset transfers?"
  },
  {
    "id": "sg-012",
    "query": "I run a Singapore electronics wholesaler and bought S$1.4 million of components from a manufacturer in China for resale to customers in Indonesia. The signed contract chooses Singapore law and requires arbitration seated in Singapore, but it does not name an arbitral institution or specify the number of arbitrators. After delivery, independent tests found that many components were refurbished rather than new. The manufacturer denies this, has stopped answering technical questions, and holds no assets in Singapore. My Indonesian customers are threatening to terminate their orders, and the components are stored in Batam. Please analyse how I can commence and structure the arbitration, obtain urgent evidence or asset relief, handle the cross-border elements, and assess which losses I should claim."
  },
  {
    "id": "sg-013",
    "query": "I bought a new laptop from a Singapore shop four months ago, and it has failed three times despite two repairs. The shop says the warranty allows only another repair and refuses a replacement or refund. What can I do?"
  },
  {
    "id": "sg-014",
    "query": "I rented a condominium unit in Singapore for two years but left after ten months because persistent mould made my child's asthma worse. I had repeatedly sent the landlord photographs and medical notes. The landlord says I broke the lease, is keeping my S$8,000 deposit, and wants another two months' rent until a new tenant moves in. Am I liable, and how can I recover the deposit?"
  },
  {
    "id": "sg-015",
    "query": "I fractured my wrist after slipping on an unmarked wet floor in a Singapore shopping mall. The mall says its cleaner inspected the area ten minutes earlier. How do I assess a negligence claim?"
  },
  {
    "id": "sg-016",
    "query": "I have been married in Singapore for eleven years and am considering divorce. We have two children aged six and nine, an HDB flat in both names, my CPF savings, and a small business started during the marriage. My spouse earns much more than I do and says the children should live with him because I work irregular hours. I may want to move to Malaysia with the children to be near my parents. Please explain the likely issues concerning divorce, care arrangements, relocation, maintenance, and division of our assets, and what I should do before separating."
  },
  {
    "id": "sg-017",
    "query": "My father died in Singapore without a will, leaving a wife, three adult children, an HDB flat, and several bank accounts. Who inherits, and what must I do before dealing with his assets?"
  },
  {
    "id": "sg-018",
    "query": "I pushed someone during an argument outside a Singapore bar after he raised a bottle at me. He fell and broke his jaw, and the police want me to attend an interview tomorrow. Could I be charged, and what should I do before giving a statement?"
  }
]
```

- [ ] **Step 3: Run structural validation**

Run:

```bash
python3 -c "import json; from pathlib import Path; p=Path('testing/suites/singapore/sg-general-v1.json'); data=json.loads(p.read_text()); expected=[f'sg-{i:03d}' for i in range(1,19)]; assert isinstance(data,list) and len(data)==18; assert [x['id'] for x in data]==expected; assert all(set(x)=={'id','query'} for x in data); assert all(isinstance(x['query'],str) and x['query'].strip().startswith('I ') for x in data); print('validated 18 queries')"
```

Expected: PASS and print `validated 18 queries`.

- [ ] **Step 4: Review the coverage and length distribution**

Confirm this one-to-one mapping:

| IDs | Coverage | Classification |
|---|---|---|
| `sg-001`–`sg-012` | Supply contract; professional negligence; company law; guarantee; employment; IP; PDPA; competition; commercial lease; construction; insolvency; cross-border arbitration | 12 commercial/business |
| `sg-013`–`sg-018` | Consumer; residential tenancy; personal injury; family; probate; criminal | 6 personal/consumer |

Confirm the four intentionally short queries are `sg-013`, `sg-015`, `sg-017`, and `sg-018`; the four detailed multi-issue queries are `sg-001`, `sg-003`, `sg-007`, and `sg-012`; the remaining ten are medium length.

---

### Task 2: Complete the replacement and update suite documentation

**Files:**
- Modify: `testing/suites/README.md`
- Delete: `testing/suites/singapore/sg-contract-tort-v1.json`
- Verify: `testing/suites/singapore/sg-general-v1.json`

**Interfaces:**
- Consumes: the validated `testing/suites/singapore/sg-general-v1.json` from Task 1.
- Produces: a suite directory and README that identify only the current general Singapore suite.

- [ ] **Step 1: Confirm the documentation still describes the old suite**

Run:

```bash
rg -n "Contract and Tort|sg-contract-tort-v1|12 queries total|Contract Law and Tort Law only" testing/suites/README.md
```

Expected: PASS with matches in the obsolete Singapore suite section.

- [ ] **Step 2: Replace the obsolete README section**

Replace the section beginning `## Singapore Contract and Tort Suite` with:

```markdown
## Singapore General Suite

The current Singapore suite is `singapore/sg-general-v1.json`.

Requirements:

- English only;
- 18 queries total;
- Singapore law only;
- 12 commercial or business queries and 6 personal or consumer queries;
- coverage-first matrix with one principal area per query and limited natural issue overlap;
- varied query lengths and requested output styles;
- first-person perspective;
- IDs follow `sg-001`, `sg-002`, etc.;
- query objects contain only `id` and `query`.
```

- [ ] **Step 3: Delete the superseded suite**

Delete exactly:

```text
testing/suites/singapore/sg-contract-tort-v1.json
```

- [ ] **Step 4: Verify the replacement state**

Run:

```bash
python3 -c "from pathlib import Path; old=Path('testing/suites/singapore/sg-contract-tort-v1.json'); new=Path('testing/suites/singapore/sg-general-v1.json'); readme=Path('testing/suites/README.md').read_text(); assert not old.exists(); assert new.is_file(); assert 'sg-general-v1.json' in readme; assert 'sg-contract-tort-v1.json' not in readme; print('replacement state validated')"
```

Expected: PASS and print `replacement state validated`.

- [ ] **Step 5: Run final suite validation**

Run:

```bash
python3 -m json.tool testing/suites/singapore/sg-general-v1.json >/dev/null && python3 -c "import json; from pathlib import Path; data=json.loads(Path('testing/suites/singapore/sg-general-v1.json').read_text()); assert len(data)==18; assert len({x['id'] for x in data})==18; assert all(set(x)=={'id','query'} for x in data); print('final validation passed')"
```

Expected: PASS and print `final validation passed`.
