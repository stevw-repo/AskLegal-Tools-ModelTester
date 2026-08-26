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
name: 2026-08-24-hk-gpt-5-4-vs-gpt-5-6-terra
jurisdiction: hong-kong

api:
  base_url: https://api-dev.ask.legal
  jurisdiction: hongkong

suite: suites/hong-kong/legal-analysis-model-comparison-v1/questions.json
rubric: rubrics/legal-analysis-v1.md

arms:
  arm-a:
    label: GPT-5.4
    configuration:
      routing_prompt: intent-router-current
      embedding_model: text-embedding-3-small
      index: ask-legal-chatbot-hk-dataset-v8
      index_host: https://example.pinecone.io
      pinecone_namespace: default
      retrieval_top_k: 8
      reranker_model: none
      model: gpt-5.4
      reasoning_effort: medium
      answer_prompt: hong-kong-v2.0
      azure_openai_endpoint: https://example.openai.azure.com/
      azure_openai_api_version: 2024-12-01-preview

  arm-b:
    label: GPT-5.6 Terra
    configuration:
      routing_prompt: intent-router-current
      embedding_model: text-embedding-3-small
      index: ask-legal-chatbot-hk-dataset-v8
      index_host: https://example.pinecone.io
      pinecone_namespace: default
      retrieval_top_k: 8
      reranker_model: none
      model: gpt-5.6-terra
      reasoning_effort: medium
      answer_prompt: hong-kong-v2.0
      azure_openai_endpoint: https://example.openai.azure.com/
      azure_openai_api_version: 2024-12-01-preview
```

Add `expectations` only when the suite has them. Configuration fields are
flexible: record the values needed to understand the comparison, but never
include secrets. The runner rejects unsupported experiment/API fields and
secret-looking configuration keys. It saves configuration for the report and
does not send it to the API.
