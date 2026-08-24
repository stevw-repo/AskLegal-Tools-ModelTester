# Legal Analysis Evaluation Rubric v1

Evaluate saved Ask.Legal responses after every arm has completed its run. The
evaluation has two parts: independent scoring and side-by-side comparison.

## Inputs

Read:

- the experiment configuration;
- the suite questions;
- any optional expectations;
- every arm's `run.json` and `responses.jsonl`;
- sanitized gateway logs when available.

Do not infer that a configured model, prompt, or index was deployed beyond what
the experiment records. Do not make deployment or release decisions.

## Independent scoring

Score every response from 1 to 5 on each dimension:

1. **Legal correctness** — governing law, rules, conclusions, and legal currency.
2. **Issue coverage** — addresses the material issues and any `must_cover` items.
3. **Grounding and citations** — authorities are supportable and citations are
   accurate; use retrieved-context logs when available.
4. **Jurisdiction discipline** — applies only the relevant jurisdiction and
   handles missing jurisdictional facts safely.
5. **Usefulness and safety** — practical, appropriately qualified, and avoids
   `must_not_claim` and `critical_failures` items.

Use this scale:

- `5` — strong; no material defect.
- `4` — good; limited non-material defects.
- `3` — mixed; useful but requires material correction or supplementation.
- `2` — poor; substantial defect or potentially misleading guidance.
- `1` — unsafe or fundamentally wrong.

Record concise reasons and identify every critical failure. A gold answer, when
present, is a benchmark rather than mandatory wording.

## Side-by-side comparison

For each question, compare all arms and record:

- preferred arm, or `tie`;
- the most important reason;
- material regressions in any arm;
- whether the preference is confident or close.

Then summarize recurring strengths and weaknesses by configuration. Do not claim
that a changed variable caused a difference unless the experiment isolates it.

## Required files

Write `evaluation.json` with this top-level shape:

```json
{
  "format_version": 1,
  "judge": {
    "model": "model used by the evaluating agent",
    "rubric": "rubrics/legal-analysis-v1.md"
  },
  "independent_scores": [],
  "pairwise_comparisons": [],
  "summary": {}
}
```

Write `report.md` as the final human-readable report. It should state the tested
configurations, summarize independent scores, explain question-level preferences,
identify critical failures and limitations, and stop without a deployment or
promotion recommendation.
