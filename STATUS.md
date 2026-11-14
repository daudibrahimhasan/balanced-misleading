# Current status

## Objective

Prepare an exploratory six-case omission study and competence pilot, then wait for Govardhan Reddy's human review and explicit final go. No model calls or study collection are authorized until that go and the technical gates are satisfied.

## Canonical inputs

- Plan: https://docs.google.com/document/d/1UNlPj2cU38PA7VzWCqd9kOQzmgSEjc77aonBI545XrE/edit
- Paper: https://docs.google.com/document/d/1hWacDlUdl_Tlyz4ObjvRS0kho9pjLVJCCPKF1rrSXeU/edit
- Prepared protocol: `docs/PROTOCOL.md`; handoff: `docs/READY_FOR_GURU.md`.
- Original authored cases: `docs/development-scenarios.md`.
- Executable proposals: `data/pilot-cases.proposed.json`; competence controls: `data/competence-cases.proposed.json`; diagnostic variants: `data/detector-controls.proposed.json`.
- Human-review hashes: `docs/guru-case-review.md`; alternative-outcome table: `docs/guru-reference-table.csv`.
- The old `data/development.json` is a separate software fixture. The Adaption CSV is unchanged raw generated material.
- Credentials load from the shared absolute environment file, preserving runtime values; no duplicate credential file.

## Implemented and checked

Six-case arithmetic expressions and context parameters; explicit receiver premises; case-specific budgets; required invariants; source-order rendering; recipient-blind writer; writer repetitions and provenance; multi-receiver shared briefings; explicit neither/tie handling; finite-domain disclosure to detectors; omitted-only false-alarm rates; deterministic checklist/topic baselines; random-subset reference enumeration; per-context incorrect-commitment contrasts and outcome vectors; source/data/config hashes; request reservations and failure journals; approval and competence gates.

All 23 automated tests pass. A hand-authored software fixture exercised 54 writer and 1,248 evaluation jobs with no model calls. Those outputs are marked NOT RESEARCH. The six full-evidence and 48 paired-outcome specifications agree with the checker; exact objective thresholds, positive controls and no-feasible/tie controls are tested. These checks do not establish human review or model performance.

## Proposed stages

1. Competence: 42 full-evidence calls across DeepSeek V4.1 Flash, Mistral Large 4 and Nemotron 3 Ultra; 100% valid and correct initial responses proposed.
2. Exploratory, only after competence and separate approval: 1,302 calls (54 writer, 936 receiver, 312 detector), six development cases, three writer draws, two evaluation repetitions. One writer family, three receivers, separate detector family. No held-out or general superiority claim.
3. Proposed cost allocation: competence cap US$5 and exploratory cap US$25; actual prices and total token costs unverified. A new run version must carry forward earlier spending.

Configurations are `awaiting_guru`, both approval records are false, endpoints are empty, request-price ceilings are zero and API verification is false. No inference has started. Approval material hashes cover source/config/case specifications. Live competence evidence and human acceptance are required before exploratory execution; imported software fixtures cannot pass the model screen.

## Remaining before launch

Guru must review the new bounded domains, shared premises, compound source mappings, valence labels, formulas, controls, role subset, budgets and scoring. API endpoints, credential bindings, sampling/reasoning settings and actual per-request ceilings must be verified and approved in the final configuration. Regenerate plans/digests after changes; record the actual dated human go and reviewed case hashes. Do not fabricate that record or mark proposals reviewed.

The manuscript and plan are being aligned to these proposals. Publication and detector-superiority claims remain out of scope. No empirical results, independent human sign-off or submission exist.
