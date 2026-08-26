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

## 2026-08-24 — Compare GPT-5.4 and GPT-5.6 Terra in four separate engines (superseded)

- Decision: Create one two-arm answer-model experiment for each of Hong Kong,
  Singapore, England and Wales, and Australia, using the deployment names
  `gpt-5.4` and `gpt-5.6-terra`.
- Isolation: Each jurisdiction uses its own engine, index, 15-question suite,
  runs, evaluation, and report. Do not pool jurisdiction scores.
- Fairness: Hold the recorded safe engine configuration constant within each
  jurisdiction and explicitly set both answer models to `medium` reasoning
  effort. The arm configurations differ only by `answer_model`.
- Suite design: Cover broad, realistic legal-analysis scenarios rather than
  treating 15 questions as a statistically conclusive benchmark.

Superseded on 2026-08-24 by the complete-main-model-set decision below. The
four-engine and suite-design portions remain in effect.

## 2026-08-24 — Compare the complete main model set

- Decision: In each arm, change the `DOC_INTAKE_MODEL` deployment as a whole.
  Do not isolate final answer generation from routing or query refinement.
- Scope: The selected model handles the intent router, refined retrieval query,
  and final Legal Analysis answer. Embedding and Pinecone retrieval settings stay
  fixed between the two arms.
- Workflow: Send one ordinary Legal Analysis request per question through the
  existing public Ask.Legal API. Do not access AI-Service directly, prepare
  routes, or inject saved route features.
- Configuration: Use `model: gpt-5.4` for arm A and
  `model: gpt-5.6-terra` for arm B. The originally recorded assumption that
  both used `medium` reasoning was incorrect. The user confirmed that GPT-5.4
  used `low`, then deployed GPT-5.6 Terra without changing anything else, so
  both arms use `low` reasoning and differ only by `model`.
- Prompt labels: Record Hong Kong v2.0, Singapore v1.4, Australia v1.1, and
  England & Wales v2; the user assigned the England & Wales v2 label.

## 2026-08-24 — Keep API access on the existing public endpoint

- Decision: Use `https://api-dev.ask.legal` plus the existing persistent
  `ASKLEGAL_API_KEY` for every experiment.
- Rationale: The complete model set is manually deployed behind the existing
  API, so direct AI-Service access adds no value to this comparison.
- Excluded: Do not require `AI_SERVER_API_KEY`, per-jurisdiction AI-Service URLs,
  direct internal endpoints, or richer internal response machinery.
- Correction: The earlier `https://dev.ask.legal` value is the frontend host,
  not the API host; a live request verified the corrected value.

## 2026-08-24 — Keep runner safeguards small and explicit

- Decision: Count blank answers as failures, reject unsupported experiment/API
  fields, and prevent secret-looking configuration keys from entering tracked
  experiment files.
- Rationale: These checks protect saved experiment integrity without changing
  the public API, `.env`, one-run-per-arm, or report workflow.
- Configuration terminology: Record the shared routing/query-refinement prompt
  once as `routing_prompt`; do not represent one router prompt as separate
  analysis and rewrite prompts.

## 2026-08-24 — Use 15 concurrent questions per run (superseded)

- Decision: Default the runner to 15 concurrent requests, matching each active
  suite's 15 questions. `--parallel N` remains available as an override.
- Operational constraint: The Backend source defaults API-key concurrency to 5
  unless the key has an override. Confirm a limit of at least 15 before running
  an arm so rate-limit failures do not consume its one saved run.

Superseded on 2026-08-24 after two failed 15-worker Hong Kong attempts.

## 2026-08-24 — Use 5 concurrent questions per run

- Decision: Default the runner to 5 concurrent requests.
- Rationale: A 15-request burst produced database-pool timeouts, while a
  staggered 15-worker attempt still produced five HTTP 500 failures. Five
  matches the Backend's default API-key concurrency and Prisma pool limit.

## 2026-08-25 — Test fresh arm-A runs at concurrency 3

- Decision: Create new dated experiments rather than overwrite the 2026-08-24
  runs, then execute each jurisdiction sequentially with `--parallel 3`.
- Rationale: This preserves the one-run-per-arm rule and tests whether the
  recurring HTTP 500 failures are load-related while keeping every other
  recorded configuration unchanged.
- Outcome: England & Wales was clean, but Hong Kong, Singapore, and Australia
  each had one generic HTTP 500. Australia then exhausted the API key's token
  allowance, causing nine HTTP 402 failures. Concurrency 3 therefore did not
  fully resolve the intermittent server errors.

## 2026-08-25 — Retry transient question failures automatically

- Decision: Keep default concurrency at 5 and retry each question up to two
  times, waiting 2 seconds and then 4 seconds by default.
- Retry: HTTP 429, HTTP 5xx, network errors or timeouts, empty responses, and
  HTTP 401 only when its body reports the known Prisma connection-pool timeout.
- Do not retry: ordinary authentication/authorization failures or HTTP 402
  quota failures.
- Audit: Record each question's attempt count in `responses.jsonl` and the retry
  settings in `run.json`. Expose `--retries` and `--retry-delay` overrides.

## 2026-08-25 — Evaluate jurisdictions independently with one common judge

- Decision: Use one independent `gpt-5.6-sol` judge per jurisdiction with the
  same legal-analysis rubric and output schema, then use a separate `gpt-5.5`
  reviewer to audit all four completed evaluations.
- Method: Score each answer independently before pairwise comparison and
  alternate answer-inspection order by question ID. Do not pool jurisdiction
  scores or make deployment, promotion, or release recommendations.
- Limitations: The judges saw arm identifiers and model names, and there was no
  second judge, external source checking, retrieval/gateway logs, gold answers,
  repeated runs, or statistical inference.
