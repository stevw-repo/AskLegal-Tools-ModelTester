# Working State

- Updated: 2026-08-25
- Machine/session: `stevw-s14` / Codex desktop
- Goal: Compare GPT-5.4 and GPT-5.6 Terra independently across four Ask.Legal
  Legal Analysis jurisdictions.
- Status: Both runs, structured evaluations, and reports are complete for all
  four jurisdictions. All 120 saved answers succeeded; all 120 independent
  scores and 60 pairwise comparisons passed final validation. Shareable PDF
  exports of all four reports have also been generated and visually verified.

## Verified results

- Hong Kong: 15 succeeded, 0 failed. `hk-006` succeeded on attempt 3 and
  `hk-012` on attempt 2.
- Singapore: 15 succeeded, 0 failed. `sg-001` succeeded on attempt 2.
- England & Wales: 15 succeeded, 0 failed. `ew-005` succeeded on attempt 2.
- Australia: 15 succeeded, 0 failed. `au-007` and `au-012` succeeded on
  attempt 2.
- Total: 60 succeeded and 0 failed across 60 questions.
- Correction supplied by the user: all four completed GPT-5.4 runs used `low`
  reasoning effort. Their fresh experiment definitions and `run.json` records
  have been corrected from `medium` to `low`.
- These runs used concurrency 5, two automatic retries, a 2-second base retry
  delay, and a 0.5-second submission delay. Automatic retries recovered all
  observed HTTP 500 responses.
- GPT-5.6 Terra: Hong Kong, Singapore, England & Wales, and Australia each
  succeeded 15/15, for 60/60 total. `hk-002`, `au-009`, `au-012`, and `au-014`
  succeeded on attempt 2; the last retried an empty response and the others
  retried HTTP 500 responses.
- Both arms record `low` reasoning effort and have identical safe configuration
  after removing only the `model` field.
- Hong Kong: overall mean 4.35 for GPT-5.4 and 4.55 for GPT-5.6 Terra;
  preferences 2/11/2 (GPT-5.4/Terra/tie); one critical failure per arm.
- Singapore: overall mean 4.29 and 4.43; preferences 4/8/3; no critical
  failures.
- England & Wales: overall mean 4.04 and 4.64; preferences 1/13/1; one critical
  failure for GPT-5.4 and none for Terra.
- Australia: overall mean 3.97 and 4.25; preferences 5/6/4; two critical
  failures for GPT-5.4 and none for Terra.
- Speed analysis: among 51 matched questions where neither arm retried,
  GPT-5.6 Terra completed faster on 50. Its paired median duration ratio was
  0.694, approximately 31% lower than GPT-5.4. Terra's paired median response
  length was also approximately 20% shorter; rough milliseconds-per-character
  normalization was approximately 12% lower. These client-observed completion
  times include routing, retrieval, generation, streaming, network conditions,
  and output length, and come from one concurrent run per arm.

## Artifacts and validation

- Fresh runs are under each jurisdiction's
  `2026-08-25-*-gpt-5-4-vs-gpt-5-6-terra-retry/runs/` directory.
- Each of the eight saved arm runs contains 15 non-empty successful response
  records and 15 existing non-empty raw response files.
- Fresh verification on 2026-08-25: all four run summaries and response files
  passed artifact checks; `python3 -m unittest discover -s tests` passed 34
  tests; Python compilation and `git diff --check` passed.
- Final evaluation verification on 2026-08-25: four valid structured
  evaluations, four reports, 120 complete score records, 60 complete pairwise
  comparisons, exact arithmetic, report/evaluation agreement, methodology
  disclosures, 34 passing tests, Python compilation, and `git diff --check`.
- Email-ready PDFs are under `output/pdf/`: one three-page A4 report each for
  Hong Kong, Singapore, England & Wales, and Australia. Every rendered page was
  visually inspected for clipping, overlap, table wrapping, headers, footers,
  and page numbering.

## Next steps

- Human review of the four reports. No deployment, promotion, or release action
  is part of this tester workflow.
