# Project Context

## Repository and handoff

- This workspace is designed to be transferred as a private Git repository;
  system prompts, generated test outputs, and retained diagnostics should not be
  made public without a separate content and confidentiality review.
- `README.md` is the human onboarding entry point. `AGENTS.md` defines project
  scope and conventions, while this directory contains the durable agent handoff.
- The test runner uses Python 3.10 or newer and only the Python standard library.
- Local credentials belong in the ignored root `api.txt` file or the
  `ASKLEGAL_API_KEY` environment variable. Never commit credentials, `.env`
  files, private keys, certificate bundles, HAR captures, or partial API data.

## Ask.Legal test runner

- The Ask.Legal development backend permits a maximum of five concurrent
  requests. Keep the sum of `--parallel` workers across simultaneous runner
  processes at or below five; exceeding this limit produces HTTP 429 responses.
- The direct development API target currently used by successful Australian
  tests is `https://asklegal-backend-dev.azurewebsites.net`.
- Development TLS testing currently requires the runner's `--insecure` option.
- Load API authentication from the local `api.txt` file and never print or
  persist its contents.
- The production endpoint is `https://ask.legal`; its API expects the
  jurisdiction value `hongkong` rather than the workspace slug `hong-kong`.
- In this environment, the production TLS chain is not trusted by the system
  certificate store. The 2026-08-14 production run used disabled verification
  only under the user's explicit authorisation.
- Production testing returned HTTP 429 with two or more concurrent workers;
  use `--parallel 1` for a complete run unless the production allocation changes.

## Hong Kong answer-generation corpus

- The database includes `type=regulatory` records, particularly the HKEX Main
  Board and GEM Listing Rules and related regulatory documents.
- The database includes annotated Hong Kong ordinances in `type=principle`.
  Each such record contains enacted ordinance text and annotation/commentary;
  these layers have different legal status and must not be conflated.
- Hong Kong answer generation must not reproduce verbatim content fetched from
  `type=principle`, including ordinance text embedded in an annotated record.
  Exact authority names, citations, provision identifiers, and indispensable
  short legal terms remain usable.
- The current Hong Kong draft is
  `prompts/hong-kong/hk-prompt-v2.0.md`; it is based primarily on the current
  Singapore v1.4 and Australian v1.1 prompt structure, adapted for Hong Kong.

## Hong Kong prompt testing

- The reusable general suite is
  `testing/suites/hong-kong/hk-general-v1.json`.
- It contains 18 first-person queries: 12 commercial or business and 6 personal
  or consumer; 16 are in English and 2 are in Traditional Chinese.
- The suite includes Hong Kong-specific checks for Main Board versus GEM source
  status, cross-border arbitration, time-sensitive construction-payment law,
  and the personal-injury quantum safeguard.
