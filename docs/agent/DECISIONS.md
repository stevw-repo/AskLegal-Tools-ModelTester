# Decisions

## 2026-08-15 — Publish the prompt workspace as a private repository

- Decision: Initialize this workspace as a Git repository and publish it to
  GitHub with private visibility for cross-device use. The user selected the
  exact repository name `AskLegal-Tools-SystemPrompt`.
- Scope: Include prompts, suites, generated results, retained review materials,
  test utilities, and durable briefing files. Exclude local credentials,
  environment files, private keys and certificates, captures, Python caches,
  and operating-system metadata.
- Rationale: The repository contains proprietary system prompts and test
  artifacts. Private-by-default publishing reduces accidental disclosure while
  preserving a complete, reproducible handoff.
- Revisit: Public visibility requires a separate content, privacy, and licensing
  review.

## 2026-08-13 — Use an 18-query coverage-first Hong Kong general suite

- Decision: Hong Kong general suite v1 uses 18 first-person queries, divided
  into 12 commercial or business matters and 6 personal or consumer matters.
- Language: Include 16 English and 2 Traditional Chinese queries so the same
  reusable suite tests Hong Kong substantive coverage and response-language
  handling without turning into a translation-specific suite.
- Hong Kong-specific stress tests: Include Main Board versus GEM status,
  regulatory guidance versus Listing Rules, Hong Kong–Mainland arbitration,
  construction-payment legal currency, and the personal-injury quantum
  safeguard.
- Rationale: This preserves the reviewable size and broad coverage model of the
  Singapore general suite while exercising the distinctive safeguards in Hong
  Kong prompt v2.

## 2026-08-13 — Separate legal status from database record type in Hong Kong v2

- Decision: Hong Kong prompt v2 ranks material by its legal nature and
  operative status, not merely by the database's `type` label.
- Annotated ordinances: enacted ordinance text is primary law; annotations and
  commentary are secondary explanation and cannot override the text or binding
  case law.
- Regulatory records: an applicable Main Board or GEM Listing Rule may impose a
  requirement, while guides, guidance letters, listing decisions, FAQs, policy
  statements, and consultation materials retain their own stated status.
- Non-copying rule: no content fetched from `type=principle` may be reproduced
  verbatim or closely mirrored, including embedded ordinance text. The narrow
  unavoidable exception is exact authority names, citations, provision
  identifiers, and indispensable short legal terms.
- Rationale: one retrieval record may combine content with different authority
  levels, and the user expressly requires answer prose to be synthesised rather
  than copied from principle sources.

## 2026-08-13 — Do not approve the current Australian response set

- Decision: The 13 August 2026 Australian v1.1 output set is not release-ready.
- Scope: Prompt-output evaluation only; no application, retrieval, database,
  deployment, or production change is authorised or included.
- Rationale: Of 34 responses, 10 meet the substantive benchmark, 18 require
  material revision, and 6 are materially wrong or unsafe. The principal risks
  are wrong-jurisdiction analysis, superseded 2026 law, omission of the ordinary
  statutory pathway, and hidden-source disclosure in 23 responses.
- Acceptance: Use the query-specific gates in
  `testing/temp/australia-v1.1-2026-08-13-audit/audit-summary.md` before approving
  a later rerun.
