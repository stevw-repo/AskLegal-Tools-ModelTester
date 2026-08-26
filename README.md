# Ask.Legal Legal Analysis Model Tester

This private repository compares Ask.Legal legal-analysis responses across
manually deployed prompts, retrieval indexes, models, and retrieval settings.
It covers legal Q&A only.

The tester does not deploy or modify the Ask.Legal backend, Azure resources, or
Pinecone indexes. Before each run, deploy the configuration manually and record
the configuration in the experiment file.

## Repository layout

- `prompts/<jurisdiction>/` — new, versioned legal-analysis prompts.
- `suites/<jurisdiction>/<suite-version>/` — questions and optional expectations.
- `rubrics/` — instructions used by an agent to evaluate saved responses.
- `experiments/<jurisdiction>/<experiment-name>/` — experiment definition, one
  saved run per arm, structured evaluation, and final report.
- `tools/` — the Ask.Legal API runner.
- `tests/` — local unit tests for the runner.
- `legacy/` — the complete pre-reorganization workspace, retained unchanged for
  historical reference.
- `.agent/` — current context, decisions, and working state.

## Core terms

- **Experiment:** one comparison using one jurisdiction and one suite.
- **Arm:** one manually deployed configuration in that comparison.
- **Run:** one execution of one arm against the complete suite.
- **Evaluation:** independent scoring plus side-by-side comparison of the arms.
- **Report:** the final human-readable evaluation.

Most experiments have `arm-a` and `arm-b`. The format also permits additional
arms when needed. Each arm may be run only once inside an experiment.

## Requirements

- Python 3.10 or newer.
- PyYAML 6.x.

The runner otherwise uses the Python standard library.

## Create an experiment

1. Add any new prompt under `prompts/<jurisdiction>/`. Never edit a prompt
   version after it has been used in a completed run.
2. Add a versioned suite directory containing `questions.json` and, when useful,
   `expectations.json`.
3. Create `experiments/<jurisdiction>/<experiment-name>/experiment.yaml` using
   the format in `experiments/README.md`.
4. Record the complete safe configuration for each arm. Do not include secrets.

## Run one arm

First validate the experiment without making API calls:

```bash
python3 tools/run_experiment.py \
  experiments/hong-kong/2026-08-24-hk-gpt-5-4-vs-gpt-5-6-terra/experiment.yaml \
  --arm arm-a \
  --dry-run
```

After manually deploying the displayed configuration:

```bash
python3 tools/run_experiment.py \
  experiments/hong-kong/2026-08-24-hk-gpt-5-4-vs-gpt-5-6-terra/experiment.yaml \
  --arm arm-a \
  --confirm-deployed
```

Repeat for `arm-b` after manually deploying its configuration. The runner
refuses to overwrite an existing arm run.

If the ignored root `.env` does not already exist, create it from the tracked
example:

```bash
cp .env.example .env
```

```dotenv
ASKLEGAL_API_KEY=your-key-here
```

The root `.env` is ignored by Git. `ASKLEGAL_API_KEY` set directly in the
environment takes precedence when present. Never put credentials in an
experiment file, result, log, prompt, or chat.

Runs use up to 5 concurrent requests by default. Use `--parallel N` to choose a
different limit.

Each question is attempted once and retried up to two times when it receives a
transient failure: HTTP 429, HTTP 5xx, a network error or timeout, an empty
response, or the known Prisma connection-pool timeout returned as HTTP 401.
Ordinary authentication errors and HTTP 402 quota errors are not retried. Use
`--retries N` and `--retry-delay SECONDS` to override the defaults. Saved
responses record how many attempts were needed. The default retry waits are 2
seconds and then 4 seconds.

## Import Azure configuration

Paste an Azure App Service environment-variable export into the ignored local
file `.env.azure.local`. Dotenv (`NAME=VALUE`) and Azure JSON exports are both
accepted. Keep the file local and do not paste its contents into chat.

List variable names without displaying any values:

```bash
python3 tools/inspect_azure_env.py
```

The inspector separates likely secret names from configuration candidates. An
agent can then inspect only selected non-secret values and use them to fill the
arms in `experiment.yaml`. Never copy keys, tokens, passwords, connection
strings, certificates, or other secrets into an experiment.

## Evaluate the experiment

After all arms have run, ask an agent to:

1. Read the experiment, suite, optional expectations, rubric, and saved runs.
2. Score each response independently.
3. Compare corresponding responses side by side.
4. Write `evaluation.json` and `report.md` in the experiment directory.

The report ends the tester workflow. Any deployment or product decision is made
separately by humans.

## Verify locally

```bash
python3 -m unittest discover -s tests
python3 -m py_compile tools/run_experiment.py tools/inspect_azure_env.py
```
