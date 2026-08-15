# Ask.Legal Prompt Testing

This folder contains reusable query suites, API test scripts, and generated Markdown results for Ask.Legal prompt testing.

## Folder Layout

- `suites/<jurisdiction>/` - JSON query suites.
- `scripts/` - local test runners and runner tests.
- `results/<jurisdiction>/` - generated Markdown outputs from Ask.Legal API runs.

## Query Suite Format

Suites are JSON arrays. Each item must contain only `id` and `query`:

```json
[
  {
    "id": "sg-001",
    "query": "I agreed over WhatsApp to sell my used laptop to someone in Singapore for S$900..."
  }
]
```

Keep suite objects simple unless the user explicitly asks for more metadata.

## Singapore A/B Prompt Workflow

Prompt version A and B are manually deployed by development. The API runner does not switch prompts.

1. Ask development to deploy `prompts/singapore/sg-prompt-v1.0-a.md`.
2. Run:

```bash
python3 testing/scripts/run_asklegal_tests.py --prompt-version sg-prompt-v1.0-a
```

3. Ask development to deploy `prompts/singapore/sg-prompt-v1.0-b.md`.
4. Run:

```bash
python3 testing/scripts/run_asklegal_tests.py --prompt-version sg-prompt-v1.0-b
```

The generated result files are:

- `testing/results/singapore/sg-prompt-v1.0-a.md`
- `testing/results/singapore/sg-prompt-v1.0-b.md`

Result files are overwritten by default.

The runner sends queries concurrently by default with 4 workers and writes results in suite order.

To change the worker count, pass `--parallel`:

```bash
python3 testing/scripts/run_asklegal_tests.py \
  --prompt-version sg-prompt-v1.0-b \
  --parallel 4
```

Use `--parallel 1` when a deliberately sequential run is needed.

## API Authentication

The runner reads an Ask.Legal API key from `api.txt` by default. You can also provide it with the `ASKLEGAL_API_KEY` environment variable or `--api-key-file`.

Do not commit, paste, or copy the API key into result files, prompt files, or documentation. The runner records only that the API base URL was used, not the credential value.

## API Targets

Use the same runner for local and dev testing.

Local backend:

```bash
python3 testing/scripts/run_asklegal_tests.py \
  --prompt-version sg-prompt-v1.0-b \
  --base-url http://localhost:3003
```

This is the preferred method when Ask.Legal is running locally. In Codex, local backend requests may need to run outside the sandbox because sandboxed `localhost` may not reach the host backend.

Dev backend:

```bash
python3 testing/scripts/run_asklegal_tests.py \
  --prompt-version sg-prompt-v1.0-b \
  --base-url https://dev.ask.legal \
  --insecure
```

Use the dev target for shared dev-environment testing. Use `--insecure` only when the dev TLS certificate cannot be verified by the local trust store.

## Useful Commands

Validate and list the Singapore suite without API calls:

```bash
python3 testing/scripts/run_asklegal_tests.py --prompt-version sg-prompt-v1.0-a --dry-run
```

Use a different API base URL:

```bash
python3 testing/scripts/run_asklegal_tests.py --prompt-version sg-prompt-v1.0-a --base-url https://dev.ask.legal
```

Use a trusted PEM certificate bundle when the development environment uses a private or company CA:

```bash
python3 testing/scripts/run_asklegal_tests.py \
  --prompt-version sg-prompt-v1.0-a \
  --ca-bundle /path/to/company-ca.pem
```

For development testing only, explicitly bypass certificate verification:

```bash
python3 testing/scripts/run_asklegal_tests.py \
  --prompt-version sg-prompt-v1.0-a \
  --insecure
```

Certificate verification remains enabled by default. `--ca-bundle` and `--insecure` cannot be used together, and result files record which TLS mode was used.

Use a non-default API key file:

```bash
python3 testing/scripts/run_asklegal_tests.py \
  --prompt-version sg-prompt-v1.0-a \
  --api-key-file /path/to/api-key.txt
```

Use a different suite or jurisdiction:

```bash
python3 testing/scripts/run_asklegal_tests.py \
  --prompt-version hk-prompt-v1.0 \
  --jurisdiction hong-kong \
  --suite testing/suites/hong-kong/hk-example-v1.json
```

## Local Verification

```bash
python3 -m json.tool testing/suites/singapore/sg-contract-tort-v1.json
python3 -m py_compile testing/scripts/run_asklegal_tests.py
python3 -m unittest testing/scripts/test_run_asklegal_tests.py
```
