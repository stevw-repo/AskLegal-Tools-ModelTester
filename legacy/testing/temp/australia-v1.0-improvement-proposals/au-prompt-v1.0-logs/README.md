# Cloudflare AI Gateway Log Export — au-prompt-v1.0

This directory contains the 18 answer-generation logs for the Australian
federal/state query-suite run.

## Files

- `summary.csv` — sortable one-row-per-query metrics.
- `manifest.json` — export criteria, aggregate totals, and the query-to-log map.
- `au-001.json` to `au-018.json` — normalized per-query logs containing:
  - Cloudflare log and conversation identifiers;
  - timestamp, model, token, cache, reasoning, cost, and duration data;
  - the copied model request, including retrieved context;
  - the assembled Ask.Legal response.

## Selection and matching

- Gateway: `asklegal-dev`
- Local time window: `2026-07-29 09:34–09:38 GMT+8`
- Filter: input tokens greater than `5000`
- Events in the time window: `72`
- Matched answer-generation completions: `18`
- Excluded events: `54` embedding and short preprocessing calls

Each selected log was matched to a suite query by exact query text and then
verified against the conversation ID in `../au-prompt-v1.0.md`. All 18 matched.

## Normalization

Cloudflare's duplicated `streamed_data` array was omitted. The assembled
response is taken from the test result file after the exact suite-ID and
conversation-ID match. Authentication headers, cookies, API keys, and other
credentials were not exported.

## Aggregate usage

- Input tokens: `180,462`
- Output tokens: `59,877`
- Total logged cost: `US$1.286814`
- Sum of request durations: `701,242 ms`

The duration total is the sum of individual requests; it is not wall-clock run
time because the suite ran with five parallel workers.
