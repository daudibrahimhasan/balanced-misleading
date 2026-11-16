# Completed development results

Authors: Daud Ibrahim Hassan and Elvina Chow, Independent Researchers.

The frozen run is `main-v6-writer-amendment-20261115T214437Z`. These are six fictional development families with
tuned prompts, not held-out validation. Final independent human review remains
outstanding. The raw journals, frozen inputs, source snapshots and analysis are
in [main evidence](../data/main-v6).

## Collection audit

- Writer jobs: 54; attempts: 55.
- Evaluation jobs: 1248; records: 1248.
- Evaluation statuses: `{'ok': 1233, 'interrupted': 6, 'invalid_output': 7, 'request_error': 2}`.
- Missing job records: 0; duplicate evaluation attempts: 0.
- Score/reference recomputation mismatches: 0.
- Packet IDs: 78; distinct briefing texts: 43.
- Known provider-reported usage: `{'completion_tokens': 268010, 'prompt_tokens': 721568, 'total_tokens': 989578}`.
- Attempts with unknown usage: 8.
- Reservation allowance: US$19.545, not a verified invoice.

One invalid writer response was explicitly retried with identical settings and both
attempts retained. Reserved requests interrupted by worker exits were not resent.
The recovery resumed only never-reserved jobs. Timing gaps and recovery events are
preserved. Unknown requests may have reached the provider; their token use is not
invented. Earlier failed competence versions are reported separately.

## Writer selections

Each row counts packet instances, not independent scenarios. A zero imbalance
score is equal favorable/adverse inclusion fraction. Criticality is single-fact
best-set change over the declared domains; unresolved reference means no action
is optimal across every allowed joint completion.

| condition | packets | distinct_texts | zero_imbalance | critical_sensitive | critical_comparison | unresolved_reference_sensitive | unresolved_reference_comparison |
| --- | --- | --- | --- | --- | --- | --- | --- |
| neutral | 18 | 8 | 18 | 9 | 9 | 9 | 9 |
| promotional | 18 | 11 | 0 | 18 | 0 | 18 | 0 |
| balanced_promotional | 18 | 10 | 18 | 17 | 13 | 17 | 13 |
| random_matched | 18 | 16 | 18 | 7 | 10 | 7 | 10 |
| full_evidence | 6 | 6 | 6 | 0 | 0 | 0 | 0 |

The balance-instructed arm frequently omits shared qualification facts. Its
omissions are not all the planted candidate omissions, and many matter in both
contexts. Fixed scores across recipient contexts are a construction property,
not an empirical discovery. This is our selection diagnostic, not full JANUS.

## Receiver outcomes

Context 0 is sensitive; context 1 is comparison. Incorrect commitment includes
wrong option and false neither. Clarify, defer and unresolved are separate.
Rates condition on valid responses; lower/upper all-planned bounds allocate
every unresolved response respectively to non-error/error. No unresolved request
is classified as a correct decision. Correct commitment is true-state correctness,
which does not automatically imply reference warrant.

| model | condition | context_index | planned | valid | wrong_option | false_neither | Clarify | Defer | Unresolved | incorrect_valid_rate | incorrect_planned_lower | incorrect_planned_upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DeepSeek V4.1 Flash 1017 | balanced_promotional | 0 | 36 | 35 | 0 | 0 | 24 | 0 | 1 | 0.0 | 0.0 | 0.027777777777777776 |
| DeepSeek V4.1 Flash 1017 | balanced_promotional | 1 | 36 | 36 | 0 | 0 | 15 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| DeepSeek V4.1 Flash 1017 | full_evidence | 0 | 12 | 11 | 0 | 0 | 0 | 0 | 1 | 0.0 | 0.0 | 0.08333333333333333 |
| DeepSeek V4.1 Flash 1017 | full_evidence | 1 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| DeepSeek V4.1 Flash 1017 | neutral | 0 | 36 | 36 | 0 | 0 | 17 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| DeepSeek V4.1 Flash 1017 | neutral | 1 | 36 | 35 | 0 | 0 | 14 | 0 | 1 | 0.0 | 0.0 | 0.027777777777777776 |
| DeepSeek V4.1 Flash 1017 | promotional | 0 | 36 | 36 | 0 | 0 | 34 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| DeepSeek V4.1 Flash 1017 | promotional | 1 | 36 | 36 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| DeepSeek V4.1 Flash 1017 | random_matched | 0 | 36 | 35 | 0 | 0 | 12 | 0 | 1 | 0.0 | 0.0 | 0.027777777777777776 |
| DeepSeek V4.1 Flash 1017 | random_matched | 1 | 36 | 36 | 7 | 0 | 8 | 0 | 0 | 0.19444444444444445 | 0.19444444444444445 | 0.19444444444444445 |
| GLM-5.3-Flash | balanced_promotional | 0 | 36 | 36 | 5 | 5 | 0 | 0 | 0 | 0.2777777777777778 | 0.2777777777777778 | 0.2777777777777778 |
| GLM-5.3-Flash | balanced_promotional | 1 | 36 | 36 | 0 | 2 | 2 | 0 | 0 | 0.05555555555555555 | 0.05555555555555555 | 0.05555555555555555 |
| GLM-5.3-Flash | full_evidence | 0 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| GLM-5.3-Flash | full_evidence | 1 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| GLM-5.3-Flash | neutral | 0 | 36 | 36 | 4 | 1 | 0 | 0 | 0 | 0.1388888888888889 | 0.1388888888888889 | 0.1388888888888889 |
| GLM-5.3-Flash | neutral | 1 | 36 | 36 | 0 | 2 | 4 | 0 | 0 | 0.05555555555555555 | 0.05555555555555555 | 0.05555555555555555 |
| GLM-5.3-Flash | promotional | 0 | 36 | 36 | 7 | 0 | 22 | 0 | 0 | 0.19444444444444445 | 0.19444444444444445 | 0.19444444444444445 |
| GLM-5.3-Flash | promotional | 1 | 36 | 36 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| GLM-5.3-Flash | random_matched | 0 | 36 | 36 | 4 | 3 | 1 | 0 | 0 | 0.19444444444444445 | 0.19444444444444445 | 0.19444444444444445 |
| GLM-5.3-Flash | random_matched | 1 | 36 | 36 | 9 | 0 | 5 | 0 | 0 | 0.25 | 0.25 | 0.25 |
| Nemotron 3.5 Super VL | balanced_promotional | 0 | 36 | 36 | 0 | 4 | 0 | 0 | 0 | 0.1111111111111111 | 0.1111111111111111 | 0.1111111111111111 |
| Nemotron 3.5 Super VL | balanced_promotional | 1 | 36 | 36 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| Nemotron 3.5 Super VL | full_evidence | 0 | 12 | 10 | 0 | 0 | 0 | 0 | 2 | 0.0 | 0.0 | 0.16666666666666666 |
| Nemotron 3.5 Super VL | full_evidence | 1 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| Nemotron 3.5 Super VL | neutral | 0 | 36 | 36 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| Nemotron 3.5 Super VL | neutral | 1 | 36 | 36 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| Nemotron 3.5 Super VL | promotional | 0 | 36 | 36 | 14 | 0 | 8 | 0 | 0 | 0.3888888888888889 | 0.3888888888888889 | 0.3888888888888889 |
| Nemotron 3.5 Super VL | promotional | 1 | 36 | 36 | 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| Nemotron 3.5 Super VL | random_matched | 0 | 36 | 36 | 4 | 2 | 0 | 0 | 0 | 0.16666666666666666 | 0.16666666666666666 | 0.16666666666666666 |
| Nemotron 3.5 Super VL | random_matched | 1 | 36 | 36 | 11 | 0 | 0 | 0 | 0 | 0.3055555555555556 | 0.3055555555555556 | 0.3055555555555556 |

The accompanying [all receiver rows](../data/main-v6/analysis/report_receiver.csv)
preserve exact actions and reference-warrant indicators. The prespecified secondary
constraint-violation measure is retained in
[episodes.csv](../data/main-v6/analysis/episodes.csv) and
[summary.csv](../data/main-v6/analysis/summary.csv).

## Detector and same-information baselines

These results use exactly the same valid detector jobs for all methods. Recall
uses critical omitted facts. False alarms use harmless omitted facts only.
Present-fact flags are separate. Exact-set agreement requires the whole target
set, including empty sets. Deterministic all-planned results are separately in
`report_detector_summary.csv`. This is not a matched-FPR superiority comparison.

| method | matched_valid_jobs | tp | fn | fp | tn | present_flags | exact | recall | false_alarm_harmless_missing | exact_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nemotron 3.5 Super VL | 303 | 74 | 105 | 87 | 292 | 171 | 79 | 0.4134078212290503 | 0.22955145118733508 | 0.2607260726072607 |
| Checklist | 303 | 179 | 0 | 379 | 0 | 0 | 40 | 1.0 | 1.0 | 0.132013201320132 |
| Rule-topic | 303 | 179 | 0 | 150 | 229 | 0 | 159 | 1.0 | 0.39577836411609496 | 0.5247524752475248 |

## Family contrasts and uncertainty

[Family contrasts](../data/main-v6/analysis/report_family_contrasts.csv) compare
promotional, balance-instructed and matched random against neutral, and
balance-instructed against matched random. Repetitions are averaged inside each
family/context before equally weighting complete families. Each row states the
complete-family count and names excluded families. Percentile bootstrap intervals
are descriptive with at most six families; no generalization or significance claim
is made. [Family-level deltas](../data/main-v6/analysis/report_family_deltas.csv)
are supplied for inspection. Supplemental contrasts do not replace the original
frozen primary analysis.

## Model identifiers and review

Requested routes and returned labels are both retained:
`{'DeepSeek V4.1 Flash 1017': ['deepseek-ai/deepseek-v4.1-flash-1017'], 'GLM-5.3-Flash': ['zai-org/glm-5.3-flash'], 'Nemotron 3.5 Super VL': ['private/nvidia/nemotron-3.5-super-120b-a12b']}`. These are provider-reported identities;
underlying weights were not independently inspected.

The audit reparsed raw successful outputs, checked writer blindness and shared
briefings, and independently reimplemented reference arithmetic and endpoint
checks. This is automated verification, not independent human validation of
scenario realism, domains or labels. See [final review](FINAL_REVIEW.md) and
[literature checks](literature-check.md). No final coauthor approval or external
submission is inferred from these files.
