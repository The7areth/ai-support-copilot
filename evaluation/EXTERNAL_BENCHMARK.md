# External evaluation: BANKING77 duplicate-charge slice

## Measured result

The frozen baseline was evaluated on all 40 examples labeled `transaction_charged_twice` in BANKING77's original test split. This intent was selected before scoring because it directly overlaps the existing duplicate-payment runbook. No test queries were added to the runbooks, and no thresholds or parameters were changed after seeing the results.

| Measurement | Result | Approximate 95% Wilson interval |
|---|---:|---:|
| Billing category selected | 32/40 (80.0%) | 65.2–89.5% |
| Billing runbook retrieved in top 3 | 33/40 (82.5%) | 68.1–91.3% |
| Ticket escalated under our policy | 39/40 (97.5%) | 87.1–99.6% |

These intervals describe binomial sampling uncertainty, not dataset representativeness. The data may contain correlated queries. The escalation target comes from **our application policy**, not original human escalation annotations. Many abstentions also escalate, so a high escalation rate does not establish successful retrieval. No specificity or false-positive rate can be estimated from this positive-only slice.

**This is not overall real-world support accuracy.** It is a narrow external transfer test of one existing intent. The remaining nine runbooks, mixed incidents, semantic answer correctness, successful resolution and actual local LLM outputs are not validated by it. The errors show why the 100% synthetic regression result must not be used as a general performance claim.

## Provenance and reproducibility

- Dataset: [PolyAI BANKING77](https://github.com/PolyAI-LDN/task-specific-datasets), online banking queries with existing intent labels.
- Authors: Iñigo Casanueva, Tadas Temčinas, Daniela Gerz, Matthew Henderson, Ivan Vulić.
- Paper: [Efficient Intent Detection with Dual Sentence Encoders](https://arxiv.org/abs/2003.04807), 2020.
- Source data license: [CC BY 4.0](https://github.com/PolyAI-LDN/task-specific-datasets/blob/master/LICENSE).
- File: `banking_data/test.csv`; 3,080 rows, 77 intents.
- SHA-256: `d12d6e3bc4c3103966ae786dc435913c0c563dfa328f5a3646d0e62cfeeb474d`.
- Mapping: original `transaction_charged_twice` label maps to the existing `billing` category/runbook.
- `external_report.json` contains the results for every selected row, including errors. Original query text is not republished.

Download the original test CSV from the dataset repository, then run from this project's root:

```bash
python -m evaluation.external_benchmark /path/to/test.csv
```

The evaluator checks expected split counts and records a fingerprint. Compare the recorded SHA-256 with the one above before comparing results. The original synthetic benchmark remains separate.

## What is required for a real-world accuracy claim

1. Define the deployment domain: whose documentation, which products and which incident types are covered. Banking transfer performance is not a substitute for this.
2. Obtain permission to use a representative sample of real, anonymized historical tickets. Keep customer text outside this public repository. Sample ordinary traffic as well as unclear, mixed, security and out-of-scope incidents; report deliberate oversampling separately.
3. Have knowledgeable reviewers label category, relevant sources, whether escalation is necessary and whether the proposed answer is grounded and useful. Label the expected outcomes before viewing predictions. Have two reviewers independently label a subset and adjudicate disagreements.
4. Separate development data from a frozen test set. Group duplicates/conversation threads and split chronologically where practical. Tune the threshold only on development data. Ensure runbooks reflect information available when the ticket was received.
5. Measure category macro-F1, retrieval Recall@3, escalation precision/recall, coverage, accuracy among answered cases, unsupported-claim rate and per-category failures. Evaluate LLM summaries separately with a recorded model version and human rubric.
6. Report sample sizes and uncertainty, not just one percentage. A rough 95% margin of ±5 percentage points for a proportion near 50% needs around 385 independent examples; stratification, correlation and rare safety cases can require more. Smaller pilots are useful but less precise.
7. Test prospective shadow mode with humans retaining control. Do not claim resolution rate or reduced handling time without measuring them in the intended workflow.

The included `real_ticket_labels.csv` is an empty schema, not fabricated evidence. Keep completed files private. For each row, use a de-identified ID rather than a customer identifier. `answer_grounded` and `answer_useful` are reviewer judgments of a frozen prediction; leave them empty until reviewed.
