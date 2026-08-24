# Decisions

## 2026-08-24 — Use a simple experiment-centered legal-analysis repository

- Decision: Organize new work around jurisdiction-specific experiments with
  normally two arms and exactly one API run per arm.
- Rationale: Ask.Legal now needs to compare prompts, Pinecone index versions,
  models, and retrieval values without introducing a general experiment platform.
- Scope: Legal Q&A only; jurisdictions are not compared with each other.

## 2026-08-24 — Record user-supplied external configuration directly

- Decision: Store one plain configuration block per arm. The user supplies the
  values; the repository does not fetch backend configuration or record Git
  commits, provenance states, role identities, approvals, or promotions.
- Rationale: Auditability is sufficient, exact reproducibility is not required,
  and operational configuration remains in Azure, Pinecone, and the backend.
- Pinecone: A new index is used for each update, and its index name is its version.

## 2026-08-24 — Save structured results and use agent-led evaluation

- Decision: Save canonical API responses as JSONL and raw streams per query.
  Gateway logs are optional attachments.
- Evaluation: An agent scores each answer independently, performs side-by-side
  comparison, and writes `evaluation.json` plus `report.md`.
- End state: The report ends the tester workflow; humans make subsequent
  decisions outside the repository.

## 2026-08-24 — Retain the prior workspace only as legacy material

- Decision: Move the complete existing prompt-testing workspace under `legacy/`
  without migrating its prompts, suites, results, or reviews into the new model.
- Rationale: A clean start is simpler than normalizing inconsistent historical
  artifacts. Existing Git history remains available.

## 2026-08-24 — Store the local API key in an ignored `.env`

- Decision: Use `ASKLEGAL_API_KEY` in the ignored root `.env` for simple,
  persistent local authentication. A tracked `.env.example` contains only the
  empty variable name.
- Rationale: The user prefers straightforward persistent storage over interactive
  entry or operating-system keyring integration.

## 2026-08-24 — Import Azure settings through an ignored local file

- Decision: Use `.env.azure.local` as the local paste target for Azure settings.
  A helper prints variable names only and separates likely secrets from
  configuration candidates before selected values are used in an experiment.
- Rationale: This lets an agent help populate configurations without putting the
  full Azure settings export or secret values into Git or chat.
