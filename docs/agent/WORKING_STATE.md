# Working State

- Updated: 2026-08-15
- Goal: Publish this prompt-engineering workspace as a handoff-ready private
  GitHub repository for use on another device.
- Repository name: `AskLegal-Tools-SystemPrompt` (selected by the user).
- Status: Complete. The private GitHub repository exists under `stevw-repo`, and
  the local `main` branch is pushed to and tracks `origin/main`.

## Current repository handoff

- `README.md` is the onboarding entry point for a new device.
- `AGENTS.md` defines the prompt-only scope, file conventions, API handling, and
  continuity requirements.
- `docs/agent/CONTEXT.md` records verified project and runner facts.
- `docs/agent/DECISIONS.md` records durable decisions, including private GitHub
  visibility and exclusions.
- `docs/agent/WORKING_STATE.md` records the current goal, validation, status,
  and exact next steps.
- Remote: `https://github.com/stevw-repo/AskLegal-Tools-SystemPrompt`.
- The root `api.txt` credential file must remain local and untracked.

## Latest substantive project state

- Hong Kong prompt v2 is `prompts/hong-kong/hk-prompt-v2.0.md`.
- The reusable Hong Kong suite is
  `testing/suites/hong-kong/hk-general-v1.json`.
- Complete development and sequential production outputs are in
  `testing/results/hong-kong/`.
- `hk-018` remains an unresolved output-truncation failure caused by an upstream
  output content filter. The development team should propagate that finish
  reason as incomplete/error before relying on retries or fallback behavior.
- Production has an observed effective concurrency limit of one for this
  workload. Its TLS-disabled run was authorised only for the 2026-08-14 test;
  do not treat that as continuing authorisation for a future run.
- The next substantive task is to review the Hong Kong development and
  production result files against prompt-v2 requirements, especially source
  status, non-copying, citations, response language, and disclaimer compliance.

## Repository preparation completed

- Reviewed project instructions and the existing continuity files.
- Confirmed the folder did not previously contain a Git repository.
- Confirmed GitHub CLI 2.96.0 is installed and reauthenticated as `stevw-repo`
  using GitHub's browser device flow.
- Added a root onboarding guide and expanded ignore rules for credentials,
  environment files, keys and certificates, captures, caches, and macOS
  metadata.
- Preserved `.superpowers/sdd/task-3-brief.md` because
  `testing/suites/README.md` references its Australian legal-currency review
  signals; the other transient `.superpowers/sdd/` artifacts remain ignored.
- Created the initial local `main` commit `dc69ce6` with message
  `Initial handoff-ready prompt workspace`.
- Created the private GitHub repository `stevw-repo/AskLegal-Tools-SystemPrompt`,
  configured `origin`, and pushed `main` successfully.

## Validation completed

- Python 3.12.10 compiled the runner and its test module successfully.
- All 11 runner unit tests passed.
- All 24 candidate tracked JSON files parsed successfully.
- Reviewed the candidate tracked file list and confirmed `api.txt`, `.DS_Store`,
  Finder `Icon` metadata files, and Python caches are excluded.
- Confirmed that no value loaded from the local `api.txt` appears in a staged
  file, without printing or copying the credential.
- Found no common GitHub, OpenAI, AWS, Google, Slack, JWT, or private-key
  fingerprints in the staged snapshot. The broader credential-assignment scan
  matched only the runner's expected API-key-loading code; JSON sensitive-key
  path inspection found no credential fields.
- New handoff and continuity files pass Git whitespace validation. Existing
  prompts and generated Markdown results retain their intentional historical
  line endings and Markdown hard breaks.

## Exact next steps

1. On another device, clone
   `https://github.com/stevw-repo/AskLegal-Tools-SystemPrompt.git` using an
   authorised GitHub account.
2. Configure `ASKLEGAL_API_KEY` locally or create an untracked root `api.txt`;
   never retrieve the existing local credential from Git history because it is
   intentionally absent.
3. Run `python3 -m unittest testing/scripts/test_run_asklegal_tests.py` to verify
   the new environment.
4. Resume the substantive Hong Kong development-versus-production output review
   described above, treating `hk-018` as an unresolved truncation failure.
