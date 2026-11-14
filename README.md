# Balanced but Misleading

**Can epistemic scores miss decision-changing omissions?**

Daud Ibrahim Hassan, Govardhan Reddy, and Elvina Chow.

## Current status: waiting for Guru

Six fictional development cases are implemented as **proposed, unreviewed specifications**. All 23 automated tests pass. A multi-model offline workflow check exercised 54 writer fixtures and 1,248 evaluation fixtures. Those answers were hand-authored software fixtures, not model results.

No study API calls have been made. Both approval records remain false. Paid endpoints, credential bindings and per-request cost ceilings are explicitly unset; they must be verified before a run is approved.

Start with [Guru's review checklist](docs/READY_FOR_GURU.md) and the [proposed protocol](docs/PROTOCOL.md).

- [Team planning doc](https://docs.google.com/document/d/1UNlPj2cU38PA7VzWCqd9kOQzmgSEjc77aonBI545XrE/edit)
- [Canonical paper](https://docs.google.com/document/d/1hWacDlUdl_Tlyz4ObjvRS0kho9pjLVJCCPKF1rrSXeU/edit)
- [Original six scenario specifications](docs/development-scenarios.md)
- [Formal proposed dataset](data/pilot-cases.proposed.json)
- [Case hashes for review](docs/guru-case-review.md) and [reference table](docs/guru-reference-table.csv)
- [Current state and remaining work](STATUS.md)

## Offline checks

Python 3.11 or newer:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python source/pipeline.py validate data/pilot-cases.proposed.json
```

The six-case file contains the proposed domains, shared premises, arithmetic expressions, per-case budgets, paired fact IDs, independently specified paired-outcome checks and pending review records. The original `data/development.json` remains a separate software fixture.

To regenerate the prepared review material without contacting models:

```powershell
python scripts/prepare_scenarios.py
python scripts/prepare_guru_package.py
python scripts/check_prepared_pipeline.py
```

These commands write new local plans beneath ignored `results/`. Preparation refuses to overwrite an existing positive human approval. Review changes before rerunning the data generator: its domains and valence labels are proposals, not facts approved by the team.

## Proposed collection

The competence configuration plans 42 full-evidence receiver calls: six paired cases plus neither/tie controls across three models. Acceptance is 100% correct, valid responses on the fixed screen before any attempt is made; no replacement of failures with selected retries. Guru must accept that criterion.

The separate exploratory proposal plans 1,302 calls: 54 writer, 936 receiver and 312 detector calls. It uses three writer draws per case/condition, shared briefings across three receiver models, two evaluation repetitions, and a detector model distinct from the writer. It is a six-case development study, not held-out evidence. Settings remain subject to Guru's review.

The proposed stage caps are US$5 competence and US$25 exploratory, within a US$30 allocation; these are guards, not an established cost. The configuration does not contain a working endpoint or a verified request price. Credentials are never committed.

## Information boundaries and scoring

Writers see fact IDs/text, a condition instruction and a per-case fact budget. They do not see either recipient context. Rendering uses source-fact order and prints no IDs. Required invariant facts are retained.

Receivers see the briefing, rule, context parameters, shared premises and actions: an option, `neither`, `clarify`, or `defer`. They do not see omitted facts or alternative domains. Detectors additionally see the complete facts and all declared alternative domains, but no planted-omission or correct-choice labels. This explicitly scoped detector task resolves hidden-domain ambiguity.

The primary outcome is **incorrect commitment**, including feasible-but-suboptimal choices and incorrect neither responses. Constraint violation is secondary. Report correct/warranted, correct/unwarranted, incorrect, clarify, defer and unresolved outcomes by context. Warrant is relative to evaluator-declared finite alternatives; it is not proof of what a receiver could infer from unbounded unknowns.

Best-set change and absence of a common optimum under ties are different concepts. No-feasible completions are represented by neither. Objective gaps use the actual derived objective and are reported only for feasible choices, in each case's units.

Selection imbalance is favorable inclusion rate minus adverse inclusion rate. A proposed score pass is exactly zero. Coverage, a deterministic source checklist and a static rule-topic baseline are compared descriptively with the scoped LLM detector. Harmless-missing facts, rather than present facts, form the omitted-fact false-alarm denominator. No full JANUS metric or matched-FPR superiority claim is implemented.

## Execution remains blocked

`execute --live` is the only network execution path. Prepared configurations require dated human approval by Govardhan Reddy of the exact source/config/specification digest, every reviewed case hash, verified API routes and positive request ceilings. Exploratory collection also requires actual competence results accepted by the team on the same cases and receiver routes.

Changing code, scientific settings or inputs requires a new plan and renewed approval. Do not set approval fields based on an AI review. The team will record Guru's actual review and go message before changing them.

The runner explicitly loads `D:\Apart Sprint\.env` with runtime variables preserved. Public configurations contain environment-variable names only. Do not create another credential file.

All attempts and pre-call reservations are retained; there are no automatic retries. Never silently replace failed cases or pool incompatible versions.

## Outputs and figures

Analysis writes `episodes.csv`, context-specific `summary.csv`, `paired_family_contrasts.csv`, `baselines.csv` and `audit.json`. Enumerated random-subset reference diagnostics are computed offline and are not receiver-model observations. Family intervals are descriptive, with unresolved counts and bounds reported separately.

Optional `source/figures.py` uses the separate renderer at `D:\Apart Sprint\Figures-maker\render.py`; the core checks and pipeline do not depend on that tool. Software-fixture figures are labeled NOT RESEARCH. No experimental figures or findings exist yet.
