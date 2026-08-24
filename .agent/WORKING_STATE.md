# Working State

- Updated: 2026-08-24
- Machine/session: `stevw-s14` / Codex desktop
- Goal: Implement the approved simple repository reorganization for legal-Q&A
  configuration comparisons.
- Status: Complete. The reorganization and local validation are finished; no
  live Ask.Legal experiment was run.

## Completed

- Re-read the current repository instructions and continuity records.
- Confirmed the local worktree was clean and matched the cached `origin/main`.
- Confirmed Python 3.12.3 and PyYAML 6.0.1 are available.
- Moved the previous workspace into `legacy/`.
- Added the new root architecture documentation, conventions, rubric, and
  continuity records.
- Added `tools/run_experiment.py` for one manually deployed arm per run.
- Added optional expectations, raw-stream retention, input paths, configuration
  recording, TLS controls, parallel execution, and overwrite protection.
- Added runner and Azure-inspector tests; 18 unit and dry-run tests now pass.
- Replaced the obsolete `api.txt` flow with persistent local
  `ASKLEGAL_API_KEY` storage in the ignored root `.env`.
- Added ignored `.env.azure.local` plus a names-only Azure-settings inspector for
  safely identifying experiment configuration candidates.
- Tested the inspector against the populated local Azure settings file. It
  displayed names only, separated five likely secrets, and did not display any
  values. Corrected the secret-name filter for OpenAI keys, database URLs, and
  non-secret token-limit settings.

## Validation

- `python3 -m unittest discover -s tests -v` — 18 tests passed.
- `python3 -m py_compile tools/run_experiment.py tests/test_run_experiment.py` —
  passed.
- `python3 tools/run_experiment.py --help` — passed.
- `git diff --check` — passed.
- Compared every file tracked at `HEAD` with its expected current or `legacy/`
  location; all historical files are byte-for-byte identical.
- No API request was made and no credential value was read.

## Constraints

- `origin/main` was fetched and verified current before final staging.
- Never print or copy the local `.env` credential into tracked files or chat.

## Exact next steps

1. Set `ASKLEGAL_API_KEY` in the existing ignored root `.env`; on another
   machine, copy `.env.example` to `.env` first.
2. Add the first new versioned legal-analysis prompt under `prompts/`.
3. Add its versioned questions and optional expectations under `suites/`.
4. Create an experiment from the example in `experiments/README.md`.
5. Validate each arm with `--dry-run`, manually deploy it, then run with
   `--confirm-deployed`.
6. After all arm runs exist, use `rubrics/legal-analysis-v1.md` to create
   `evaluation.json` and `report.md`.

## Repository handoff

- The user explicitly authorized committing and pushing this completed change
  set to `origin/main` on 2026-08-24.
