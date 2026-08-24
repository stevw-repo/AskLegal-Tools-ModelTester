# Prompts

Store new Ask.Legal legal-analysis prompts under a lowercase jurisdiction slug:

```text
prompts/hong-kong/hk-answer-v1.md
prompts/australia/au-answer-v1.md
```

Use explicit human-readable versions. After a prompt has been used in a
completed experiment run, do not edit it; create the next version.

Only legal Q&A prompts belong here. Historical prompts, including the prior
document-generation prompts, remain under `legacy/prompts/`.
