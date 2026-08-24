# Ask.Legal System Prompts

This private workspace contains Ask.Legal system prompts, reusable query suites,
generated prompt-test results, and the local Python test runner. It is limited to
prompt engineering and prompt-output testing; it does not define or modify the
application, retrieval, database, deployment, or production layers.

## Start here

Before changing prompts or running tests, read:

1. `AGENTS.md` for project scope and conventions.
2. `docs/agent/CONTEXT.md` for verified operational facts.
3. `docs/agent/DECISIONS.md` for durable decisions and their rationale.
4. `docs/agent/WORKING_STATE.md` for the current status and exact next steps.

These files are the authoritative handoff package. Update them whenever work
changes a durable fact, decision, blocker, or next step.

## Repository layout

- `prompts/<jurisdiction>/` — versioned jurisdiction-specific prompts and notes.
- `testing/suites/<jurisdiction>/` — reusable JSON query suites.
- `testing/results/<jurisdiction>/` — generated Markdown API outputs.
- `testing/scripts/` — the standalone Ask.Legal test runner and unit tests.
- `testing/temp/` — retained review and diagnostic working material.
- `docs/agent/` — durable context, decisions, and current working state.

## Set up another device

Requirements: Git and Python 3.10 or newer. The test runner uses only Python's
standard library.

```bash
git clone https://github.com/stevw-repo/AskLegal-Tools-SystemPrompt.git
cd AskLegal-Tools-SystemPrompt
python3 -m unittest testing/scripts/test_run_asklegal_tests.py
```

Provide Ask.Legal authentication locally in one of these ways:

- set the `ASKLEGAL_API_KEY` environment variable; or
- create an untracked `api.txt` in the repository root containing the API key.

Never commit an API key, token, certificate, `.env` file, or HAR capture. The
repository ignore rules exclude the standard local credential and capture files,
but review staged changes before every push.

## Run prompt tests

Read `testing/README.md` for the complete workflow and target-specific cautions.
The final testing pipeline is:

```bash
python3 testing/scripts/run_asklegal_tests.py \
  --prompt-version <prompt-version> \
  --jurisdiction <api-jurisdiction> \
  --suite testing/suites/<jurisdiction>/<suite>.json \
  --dry-run
```

Remove `--dry-run` only after confirming the target, deployed prompt version,
jurisdiction value, concurrency, TLS mode, and local credential source.

## Current handoff

The latest completed work and unresolved issues are maintained in
`docs/agent/WORKING_STATE.md`. In particular, consult it before rerunning Hong
Kong production tests or evaluating the unresolved `hk-018` truncation.
