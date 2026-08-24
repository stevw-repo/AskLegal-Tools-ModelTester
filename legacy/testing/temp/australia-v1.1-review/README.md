# Australia run log index

**Gateway:** `asklegal-dev`  
**Source:** Cloudflare AI Gateway  
**Retrieved:** 29 July 2026  
**Test window:** 29 July 2026, 16:11:03–16:13:17 GMT+8

## Selection

The 18 retained Cloudflare answer-generation logs were matched to
`testing/suites/australia/au-federal-state-v1.json` by both:

1. exact user query; and
2. conversation ID from `testing/results/australia/au-prompt-v1.1.md`.

All 18 returned HTTP 200. The Cloudflare request bodies were inspected to verify
the deployed system prompt and the six retrieved passages supplied to each
answer. Short embedding and preprocessing calls were excluded. Two later
answer-generation logs in the filtered view were excluded because neither their
queries nor conversation IDs matched this test run.

## Critical version finding

Every retained request begins with:

```text
# Answer Generation System Prompt - Australia v1.0
```

No retained request contains the v1.1 system prompt. The result filename therefore
does not describe the answer prompt that was actually tested.

## Files

- `log-summary.csv` — sorted by suite ID; includes Cloudflare log and conversation
  IDs, token/cost/timing fields, payload sizes, and the deployed prompt version.
- `au-prompt-v1.1-review.md` — log-informed legal-quality and retrieval review.

The compact export does not duplicate the full proprietary retrieved passages or
authentication material. The Cloudflare log IDs provide the canonical record for
reopening each complete request in the gateway.
