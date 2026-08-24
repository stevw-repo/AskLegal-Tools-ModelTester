# Singapore General Query Suite Design

## Objective

Replace the narrow Singapore contract-and-tort query suite with an 18-question, coverage-first suite spanning common areas of Singapore law. The suite will emphasize commercial law while retaining representative personal and consumer matters.

## Output

- Create `testing/suites/singapore/sg-general-v1.json`.
- Remove `testing/suites/singapore/sg-contract-tort-v1.json`.
- Update `testing/suites/README.md` so its Singapore guidance describes the replacement suite.
- Do not run the Ask.Legal API; this task covers suite preparation and local validation only.

## Coverage

Twelve questions will address commercial or business matters:

1. B2B supply contracts and exclusion clauses.
2. Misrepresentation and professional negligence.
3. Directors' duties and minority shareholder rights.
4. Business financing and personal guarantees.
5. Employment dismissal, restraints, and confidentiality.
6. Intellectual property ownership and infringement.
7. PDPA obligations and a customer-data breach.
8. Competition law and restrictive arrangements.
9. Commercial leases.
10. Construction payment disputes.
11. Insolvency and recovery of unpaid debts.
12. Cross-border trade, governing law, and arbitration.

Six questions will address personal or consumer matters:

13. Consumer protection and defective goods.
14. Residential tenancy.
15. Personal injury and negligence.
16. Divorce, maintenance, and child arrangements.
17. Wills, intestacy, and probate.
18. Criminal liability and immediate procedural steps.

## Query Construction

- Use English, Singapore-specific facts, and a first-person perspective throughout.
- Use IDs `sg-001` through `sg-018` with no gaps or duplicates.
- Each JSON object contains only `id` and `query`.
- Use approximately four short, ten medium, and four detailed multi-issue queries.
- Vary whether the user states only a situation or expressly requests issue spotting, practical steps, risk assessment, or structured legal analysis.
- Include realistic sums, dates, documents, evidence, and competing accounts where useful, without making every query legally sophisticated.
- Give every coverage area one principal query. Natural secondary issue overlap is permitted, but it should not obscure the principal area being tested.

## Validation

Local validation will confirm:

- valid JSON;
- exactly 18 objects;
- sequential and unique IDs;
- only `id` and `query` fields;
- non-empty first-person queries; and
- the intended 12-to-6 commercial/personal coverage balance by manual review.

No application pipeline, retrieval, deployment, production configuration, or API behavior will be changed.
