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
- The API runner loads credentials from `ASKLEGAL_API_KEY` or the ignored root
  `.env` file. `.env.example` documents the required variable without a secret.
- The runner validates an experiment with `--dry-run`, requires
  `--confirm-deployed` for a live run, saves one JSONL record and raw stream per
  question, and refuses to overwrite an existing arm run.
- Python 3.12.3 and PyYAML 6.0.1 were available on machine `stevw-s14` on
  2026-08-24.
- Historical pre-reorganization material is retained under `legacy/`.

## Important paths

- `README.md` — human workflow.
- `AGENTS.md` — repository operating rules.
- `tools/run_experiment.py` — one-arm Ask.Legal API runner.
- `tools/inspect_azure_env.py` — names-only inspection of local Azure settings.
- `tests/test_run_experiment.py` — runner unit tests.
- `rubrics/legal-analysis-v1.md` — current evaluation rubric.
- `legacy/` — historical workspace.

## Verified commands

- `python3 -m unittest discover -s tests -v` — 18 tests passed on 2026-08-24.
- `python3 -m py_compile tools/run_experiment.py tools/inspect_azure_env.py` —
  passed on 2026-08-24.
- `git diff --check` — passed on 2026-08-24.
