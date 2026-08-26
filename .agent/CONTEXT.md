# Project Context

## Verified facts

- The repository tests Ask.Legal legal-analysis responses only.
- Ask.Legal configurations are manually deployed outside this repository.
- Pinecone index names, such as `HK-v7`, serve as index versions.
- The repository stores prompts, suites, experiment definitions, API artifacts,
  structured evaluations, and Markdown reports; it does not store Pinecone index
  contents.
- Most experiments compare two arms, with one 10–20-question run per arm.
- Evaluation is performed manually by an agent using independent scoring and
  side-by-side comparison.
- The shared public dev API is `https://api-dev.ask.legal`. The runner loads
  `ASKLEGAL_API_KEY` from the ignored root `.env` file; no internal AI-Service
  credential or jurisdiction-specific service URL is needed.
- The runner validates an experiment with `--dry-run`, requires
  `--confirm-deployed` for a live run, saves one JSONL record and raw stream per
  question, and refuses to overwrite an existing arm run.
- Runs use up to 5 concurrent requests by default. Explicit `--parallel N`
  execution remains available and applies the configured delay between request
  submissions.
- Each question is retried up to two times by default after transient HTTP,
  network, timeout, or empty-response failures. Default waits are 2 seconds and
  4 seconds. Ordinary authentication failures and HTTP 402 quota failures are
  not retried. Saved responses record attempt counts, and `run.json` records the
  retry settings.
- Each saved response records client-observed `duration_ms`, measured from query
  start until the complete streamed answer (or retry sequence) finishes. This is
  end-to-end completion latency, not model-only latency or time to first token.
- The runner rejects unsupported experiment/API fields and secret-looking
  configuration keys. A blank API answer is saved as a failed question rather
  than counted as a successful response.
- Python 3.12.3 and PyYAML 6.0.1 were available on machine `stevw-s14` on
  2026-08-24.
- Historical pre-reorganization material is retained under `legacy/`.
- Four active model-comparison suites contain 15 questions each for Hong Kong,
  Singapore, England and Wales, and Australia. Their public API jurisdiction
  values are `hongkong`, `singapore`, `english`, and `australia` respectively.
- The complete Ask.Legal Core path is Frontend → Backend → AI-Service. The
  Backend handles the public API, persistence, accounting, and stream adaptation;
  AI-Service owns routing, query refinement, legal retrieval, and generation.
- AI-Service uses `DOC_INTAKE_MODEL` for both the intent router/query refinement
  and the final legal answer. There is no separate legal-answer deployment
  setting. Legal retrieval separately uses `EMBEDDING_MODEL` and the
  jurisdiction's Pinecone index.
- Four completed experiments compare the complete main-model deployments
  `gpt-5.4` and `gpt-5.6-terra` independently for those jurisdictions. Both
  arms use `low` reasoning and differ only by `model`.
- The four completed model comparisons each contain `evaluation.json` and
  `report.md`. One independent `gpt-5.6-sol` judge evaluated each jurisdiction
  under `rubrics/legal-analysis-v1.md`, followed by a separate `gpt-5.5` audit.
  Model identity was visible to the judge; there was no second judge, external
  source checking, retrieval/gateway logs, gold answers, or repeated runs.
- The runner sends ordinary Legal Analysis requests through the public API. It
  does not inject routing features or access AI-Service directly.
- Current legal-answer prompt labels are Hong Kong v2.0, Singapore v1.4,
  Australia v1.1, and England & Wales v2. The England & Wales v2 label is the
  user's assigned version for its otherwise unversioned source header.

## Important paths

- `README.md` — human workflow.
- `AGENTS.md` — repository operating rules.
- `tools/run_experiment.py` — one-arm public Ask.Legal API runner.
- `tools/inspect_azure_env.py` — names-only inspection of local Azure settings.
- `tests/test_run_experiment.py` — runner unit tests.
- `tests/test_active_experiments.py` — validation for every active experiment,
  suite, rubric, expectation file, and referenced prompt.
- `rubrics/legal-analysis-v1.md` — current evaluation rubric.
- `legacy/` — historical workspace.
- `suites/*/legal-analysis-model-comparison-v1/questions.json` — four active
  15-question model-comparison suites.
- `experiments/*/2026-08-24-*/experiment.yaml` — four active two-arm model
  comparisons.
- `experiments/*/2026-08-25-*-retry/experiment.yaml` — completed model
  comparisons; each has successful GPT-5.4 `arm-a` and GPT-5.6 Terra `arm-b`
  artifacts produced with concurrency 5 and automatic retries.

## Verified commands

- `python3 -m unittest discover -s tests -v` — 34 tests passed on 2026-08-25.
- `python3 -m py_compile tools/run_experiment.py tools/inspect_azure_env.py` —
  passed on 2026-08-24.
- `git diff --check` — passed on 2026-08-24.
- All eight active complete-model-set experiment arms passed runner dry-run
  validation on 2026-08-24; no API request or output file was created.
- The four active suites passed JSON/schema checks with 15 questions each and
  60 unique question IDs on 2026-08-24. Each active arm pair differs only by
  `model`.
- A one-question Hong Kong request to `https://api-dev.ask.legal` succeeded on
  2026-08-24 using the ignored `.env` key: a conversation ID, non-empty answer,
  and raw response were received. No experiment run artifact was created.
- `https://dev.ask.legal` is the frontend host and returned HTTP 405 for
  `POST /api/ai/embedChat`; it must not be used as the runner API base URL.
- The four active experiments use the verified API base URL
  `https://api-dev.ask.legal`. The user confirmed the GPT-5.4 deployment for
  the first arm before testing.
- The first live Hong Kong `arm-a` run used 15 concurrent requests and saved a
  complete diagnostic artifact, but it is not evaluable: 4 questions succeeded
  and 11 failed. Seven HTTP 401 bodies explicitly report Prisma connection-pool
  acquisition timeouts with `connection limit: 5`; four HTTP 500 bodies are
  generic. The user then clarified that the concurrency override had mistakenly
  been changed in production rather than dev. The failed run used `--delay 0`,
  so all 15 authentication requests also hit dev's five-connection Prisma pool
  at once.
- A second Hong Kong `arm-a` attempt used 15 workers with a 0.5-second delay and
  produced 10 successes plus 5 generic HTTP 500 failures. Both failed attempts
  are preserved under the experiment's `diagnostics/` directory. The user then
  selected concurrency 5 for the canonical rerun and future runs.
- The canonical Hong Kong `arm-a` concurrency-5 run completed with 14 successes
  and one generic HTTP 500 failure for `hk-005`. Its `run.json`, responses, and
  raw bodies are saved under `runs/arm-a`; it is incomplete for evaluation.
- A Singapore `arm-a` concurrency-5 run completed with 12 successes and three
  generic HTTP 500 failures (`sg-001`, `sg-003`, and `sg-013`); its artifacts are
  saved under `runs/arm-a` and are incomplete for evaluation.
- The England & Wales `arm-a` process was interrupted at the user's request
  after all 15 requests had been submitted but only 7 terminal results had
  appeared (5 successes and 2 errors). The runner writes only after the full
  suite, so no England & Wales canonical run artifact exists. Australia `arm-a`
  was not started.
- Four fresh 2026-08-25 experiments repeated GPT-5.4 `arm-a` at concurrency 3,
  one jurisdiction at a time. Hong Kong completed 14/15 with a generic HTTP 500
  for `hk-002`; Singapore completed 14/15 with a generic HTTP 500 for `sg-002`;
  England & Wales completed 15/15; Australia completed 5/15, with a generic HTTP
  500 for `au-003` and HTTP 402 `Insufficient tokens` for `au-007` through
  `au-015`.
- The concurrency-3 runs produced 48 successful responses out of 60. Reduced
  concurrency did not eliminate generic HTTP 500 responses. Nine Australian
  failures were caused by API-key token exhaustion during the last run, not by
  the Australian engine or concurrency.
