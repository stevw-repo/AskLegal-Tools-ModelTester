# Ask.Legal Prompt Engineering Instructions

## Scope

This workspace is for Ask.Legal prompt engineering and prompt-output testing only.

Do not modify, design, or assume changes to:

- application pipelines;
- retrieval systems;
- databases;
- deployment infrastructure;
- production configuration.

If a task appears to require those layers, stop and ask the user.

## Folder Conventions

Use these top-level folders:

- `prompts/<jurisdiction>/` for jurisdiction-specific system prompts and prompt notes.
- `testing/suites/<jurisdiction>/` for reusable query suites.
- `testing/results/<jurisdiction>/` for generated Ask.Legal API outputs.
- `testing/scripts/` for local testing utilities.

## Prompt Naming

Use lowercase jurisdiction slugs and explicit prompt versions:

- `prompts/hong-kong/hk-prompt-v1.0.md`
- `prompts/england-wales/ew-prompt-v5.0.md`
- `prompts/singapore/sg-prompt-v1.0-a.md`
- `prompts/singapore/sg-prompt-v1.0-b.md`

For Singapore A/B testing, A and B are prompt labels only. The API does not switch prompt versions. The development team manually deploys the prompt before each test run.

## Query Suite Rules

Keep query suite objects simple. Do not add metadata fields unless the user asks for them.

For detailed query-suite generation requirements, read `testing/suites/README.md`.

## Testing Results

Save one Markdown result file per prompt version:

- `testing/results/singapore/sg-prompt-v1.0-a.md`
- `testing/results/singapore/sg-prompt-v1.0-b.md`

Overwrite result files by default unless the user asks for archival run folders.

## API Authentication

Use the local `api.txt` file as the default Ask.Legal API key source for the standalone runner. Never print, document, or copy the key into prompts, results, or chat.

## Testing Pipeline

Use `testing/scripts/run_asklegal_tests.py` as the final prompt testing pipeline. It sends the suite to the Ask.Legal API endpoint and writes one Markdown result file per prompt version.

Supported API targets:

- Local backend: `http://localhost:3003` for local prompt testing when Ask.Legal is running locally. In Codex, local backend requests may need approval to run outside the sandbox because sandboxed shell localhost may not reach the host backend.
- Dev backend: `https://dev.ask.legal` for shared dev-environment testing. Use `--insecure` only when dev TLS certificate verification fails.

The same `api.txt` API key flow is used for both targets.
