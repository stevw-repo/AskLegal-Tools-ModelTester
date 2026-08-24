# Ask.Legal Model Tester Instructions

## Scope

This repository is for testing and comparing Ask.Legal legal-analysis responses.
Experiments may vary prompts, query-analysis models and prompts, query-rewrite
models and prompts, embedding models, Pinecone index versions, retrieval values,
rerankers, and answer-generation models and prompts.

Legal document generation and cross-jurisdiction comparisons are out of scope.
Each experiment belongs to exactly one jurisdiction.

Do not modify or design the Ask.Legal application, backend pipeline, Azure
deployment, Pinecone index, database, or production configuration in this
repository. Those systems are manually configured outside this repository.

## Simplicity rules

- The user supplies the configuration recorded for each arm. Do not infer,
  retrieve, or independently reference backend configuration.
- Do not add configuration provenance states, role tracking, approvals,
  promotion rules, or release workflows.
- Most experiments use two arms and one run per arm.
- Keep the workflow understandable from the experiment directory alone.

## Folder conventions

- `prompts/<jurisdiction>/` contains new legal-analysis prompt versions.
- `suites/<jurisdiction>/<suite-version>/questions.json` contains API queries.
- `suites/<jurisdiction>/<suite-version>/expectations.json` contains optional
  evaluation expectations.
- `rubrics/` contains reusable agent-evaluation instructions.
- `experiments/<jurisdiction>/<experiment-name>/experiment.yaml` defines the
  comparison and both configurations.
- `experiments/<jurisdiction>/<experiment-name>/runs/<arm>/` contains the one
  saved run for that arm.
- `evaluation.json` and `report.md` are written in the experiment directory.
- `legacy/` contains the pre-reorganization workspace. Do not edit its contents
  unless the user specifically asks for historical repair.
- `tools/` contains the current runner; `tests/` contains its tests.

## Versioning

- Use lowercase jurisdiction slugs.
- Give every prompt and suite an explicit human-readable version.
- Once a prompt or suite has been used in a completed run, do not edit it.
  Create a new version instead.
- Treat each Pinecone index name, such as `HK-v7`, as its index version.
- Give each experiment a unique, descriptive folder name, preferably beginning
  with an ISO date.
- Never overwrite a completed arm run or reuse an experiment folder for a new
  comparison.

## Experiment rules

- Questions contain exactly `id` and `query`.
- Expectations are optional and separate from questions. Supported fields are
  `id`, `must_cover`, `must_not_claim`, `critical_failures`, and `gold_answer`.
- Store the complete safe configuration for each arm directly in
  `experiment.yaml`, even where values repeat between arms.
- Never store passwords, API keys, tokens, connection strings, or other secrets.
- Manually deploy an arm before running it. The runner records the configuration
  but does not send it to the Ask.Legal API.
- One live run is permitted per arm. Create a new experiment to rerun.

## Evaluation rules

- Evaluation is performed manually by an agent after the runs are saved.
- Evaluate each answer independently and compare matching answers side by side.
- Write structured findings to `evaluation.json` and the final human-readable
  analysis to `report.md`.
- Do not make deployment, approval, promotion, or release decisions.

## API authentication and logs

- Load authentication from `ASKLEGAL_API_KEY` or the ignored root `.env` file.
- Never print, document, or copy the key into tracked files or chat.
- Preserve raw API streams for each query.
- Gateway logs are optional. If available, place sanitized exports under the
  corresponding arm's `logs/` directory. Never store authentication material.

## Azure configuration import

- The user may paste Azure settings into the ignored `.env.azure.local` file.
- Never display or read the complete file into chat or tool output.
- First run `python3 tools/inspect_azure_env.py`; it prints names only.
- Treat names marked as likely secrets as prohibited experiment content.
- Inspect values only for selected configuration candidates needed by the
  experiment, and persist only those non-secret values in `experiment.yaml`.
- If a value may itself contain credentials or a signed URL, stop and exclude it.

## Verification

After changing the runner or schemas, run:

```bash
python3 -m unittest discover -s tests
python3 -m py_compile tools/run_experiment.py tools/inspect_azure_env.py
```

Maintain the current facts, decisions, and working state under `.agent/`.
