# Australia v1.1 rerun log index

**Gateway:** `asklegal-dev`  
**Source:** Cloudflare AI Gateway  
**Retrieved:** 29 July 2026  
**Test window:** 29 July 2026, 16:41:48–16:44:09 GMT+8

## Selection and validation

The 18 retained answer-generation logs were matched to
`testing/suites/australia/au-federal-state-v1.json` by both:

1. exact user query; and
2. conversation ID from `testing/results/australia/au-prompt-v1.1.md`.

Validation result:

- 18 of 18 exact query matches;
- 18 of 18 conversation-ID matches;
- 18 unique Cloudflare log IDs;
- 18 unique conversation IDs;
- 18 of 18 HTTP 200 responses; and
- 18 of 18 requests begin with
  `# Answer Generation System Prompt - Australia v1.1`.

Short embedding and preprocessing calls were excluded. The selected answer calls
were isolated using `Tokens In > 5000`, then checked against the local suite and
result file. The first unrelated long-form call after the test window was at
16:15:57, before this rerun.

## Files

- `log-summary.csv` — sorted by suite ID, with Cloudflare log and conversation
  IDs, token/cost/timing fields, payload sizes, and deployed prompt version.
- `au-prompt-v1.1-rerun-review.md` — log-informed answer, prompt-compliance, and
  retrieval review.

The compact export does not duplicate the complete proprietary retrieved
passages, streamed provider response objects, or authentication material. The
Cloudflare log IDs are the canonical references for reopening each full request.
