# Experiments

Each experiment compares manually deployed configurations within one
jurisdiction. Most experiments have `arm-a` and `arm-b`, with one run per arm.

## Directory layout

```text
experiments/<jurisdiction>/<experiment-name>/
├── experiment.yaml
├── runs/
│   ├── arm-a/
│   └── arm-b/
├── evaluation.json
└── report.md
```

The runner creates each arm's run directory. Do not create it before running.

## Experiment format

```yaml
format_version: 1
name: 2026-08-24-hk-v7-v8
jurisdiction: hong-kong

api:
  base_url: https://dev.ask.legal
  jurisdiction: hongkong

suite: suites/hong-kong/hk-general-v1/questions.json
expectations: suites/hong-kong/hk-general-v1/expectations.json
rubric: rubrics/legal-analysis-v1.md

arms:
  arm-a:
    label: HK-v7
    configuration:
      query_analysis_model: model-name
      query_analysis_prompt: prompts/hong-kong/hk-query-analysis-v1.md
      query_rewrite_model: model-name
      query_rewrite_prompt: prompts/hong-kong/hk-query-rewrite-v1.md
      embedding_model: embedding-model-name
      index: HK-v7
      retrieval_top_k: 6
      reranker_model: reranker-name
      answer_model: answer-model-name
      answer_prompt: prompts/hong-kong/hk-answer-v1.md

  arm-b:
    label: HK-v8
    configuration:
      query_analysis_model: model-name
      query_analysis_prompt: prompts/hong-kong/hk-query-analysis-v1.md
      query_rewrite_model: model-name
      query_rewrite_prompt: prompts/hong-kong/hk-query-rewrite-v1.md
      embedding_model: embedding-model-name
      index: HK-v8
      retrieval_top_k: 6
      reranker_model: reranker-name
      answer_model: answer-model-name
      answer_prompt: prompts/hong-kong/hk-answer-v1.md
```

Remove `expectations` when the suite has none. Configuration fields are flexible:
record the values needed to understand the comparison, but never include secrets.
The runner saves these values for the report; it does not send them to the API.
