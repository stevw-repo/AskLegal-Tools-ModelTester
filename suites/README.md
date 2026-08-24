# Evaluation Suites

Each versioned suite has this layout:

```text
suites/<jurisdiction>/<suite-version>/
├── questions.json
└── expectations.json
```

`questions.json` is required. It is a JSON array whose items contain exactly
`id` and `query`:

```json
[
  {
    "id": "hk-001",
    "query": "I need help with a Hong Kong law question."
  }
]
```

`expectations.json` is optional. It may provide evaluation guidance or a gold
answer for some or all questions:

```json
[
  {
    "id": "hk-001",
    "must_cover": ["The central legal issue"],
    "must_not_claim": ["An unsupported deadline"],
    "critical_failures": ["Applies a non-Hong Kong legal regime"],
    "gold_answer": null
  }
]
```

All expectation fields other than `id` are optional. Keep expectations concise;
they guide evaluation and are not sent to Ask.Legal.

Once a suite version has been used in a completed run, create a new suite
version rather than editing it.
