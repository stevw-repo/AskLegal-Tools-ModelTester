# Ask.Legal Query Suite Context

This folder contains reusable user-query suites for prompt testing.

## Suite Format

Suites are JSON arrays. Each item must contain only `id` and `query`:

```json
[
  {
    "id": "sg-001",
    "query": "I ..."
  }
]
```

Do not add metadata fields unless the user asks for them. Encode variation in the query text itself, not in extra schema fields.

## Generation Principles

When generating a new suite:

- use first-person user queries;
- vary query length and factual detail;
- vary how clearly the user specifies what they want, from implicit situation-only queries to targeted requests for legal analysis or practical steps;
- vary the requested output style across practical action plans, issue spotting, risk assessment, and substantial legal analysis;
- keep the suite small enough for manual review unless the user asks for broad coverage.

## Singapore General Suite

The current Singapore suite is `singapore/sg-general-v1.json`.

Requirements:

- English only;
- 18 queries total;
- Singapore law only;
- 12 commercial or business queries and 6 personal or consumer queries;
- coverage-first matrix with one principal area per query and limited natural issue overlap;
- varied query lengths and requested output styles;
- first-person perspective;
- IDs follow `sg-001`, `sg-002`, etc.;
- query objects contain only `id` and `query`.

## Hong Kong General Suite

The current Hong Kong suite is `hong-kong/hk-general-v1.json`.

Requirements:

- 18 queries total;
- Hong Kong law is the principal legal system, with one expressly requested
  Hong Kong–Mainland arbitration and enforcement scenario;
- 12 commercial or business queries and 6 personal or consumer queries;
- 16 English queries and 2 Traditional Chinese queries;
- coverage-first matrix with one principal area per query and limited natural
  issue overlap;
- includes Main Board Listing Rules, related HKEX materials, and a GEM
  comparison that should not displace the applicable Main Board regime;
- includes a time-sensitive construction-payment query that requires the model
  to verify statutory application, commencement, and deadlines rather than
  assume them;
- includes a personal-injury quantum request that should trigger the prompt's
  specialist-advice safeguard while still addressing liability;
- varied query lengths and requested output styles;
- first-person perspective;
- IDs follow `hk-001`, `hk-002`, etc.;
- query objects contain only `id` and `query`.

## Australia Federal-State Suite

The current Australian federal-State suite is
`australia/au-federal-state-v1.json`.

Requirements:

- English only;
- 18 queries total;
- Australian law only;
- deliberately weighted toward Commonwealth, State, and Territory overlap,
  cross-border facts, and forum selection;
- includes questions from all eight States and Territories;
- includes both cases where the model should identify separate concurrent regimes
  and cases where it should not request a State or Territory unnecessarily;
- includes under-specified residential-tenancy and personal-injury questions that
  should trigger a jurisdiction clarification;
- varied query lengths and requested output styles;
- first-person perspective;
- IDs follow `au-001`, `au-002`, etc.;
- query objects contain only `id` and `query`.

## Australia Recent Legal Changes Suite

The current Australian legal-currency suite is
`australia/au-recent-legal-changes-v1.json`.

Requirements:

- English only;
- 16 queries total;
- Australian law only;
- tests legal currency as at 4 August 2026 rather than general doctrinal coverage;
- includes five queries on the 2026 negative-gearing and CGT reforms and eleven
  queries on other significant Commonwealth changes commencing in 2025 or 2026;
- deliberately tests enactment status, exact cutoff dates, grandfathering,
  staged commencement, subordinate legislation, and superseded procedures;
- varied personal, small-business, professional, regulatory, and corporate facts;
- first-person perspective;
- IDs follow `au-rc-001`, `au-rc-002`, etc.;
- query objects contain only `id` and `query`.

The official-source review signals for this time-sensitive suite are maintained in
`.superpowers/sdd/task-3-brief.md`. Revalidate those signals before using the suite
after a material legislative update.
