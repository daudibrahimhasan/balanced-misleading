# AI x Epistemics Research Sprint

**Balanced but Misleading: Can Epistemic Scores Miss Decision-Changing Omissions?**

This repository contains the research pipeline for Daud Ibrahim Hassan, Govardhan Reddy, and Elvina Chow. It is offline-tested software, not a completed experiment. The selected models are DeepSeek V4.1 Flash, Mistral Large 4, and Nemotron 3 Ultra. Scientific settings and scenario review remain pending; no experimental results are reported here.

The canonical team plan is [the Google Doc](https://docs.google.com/document/d/1UNlPj2cU38PA7VzWCqd9kOQzmgSEjc77aonBI545XrE/edit). Read [STATUS.md](STATUS.md) for current decisions and [docs/scenario-format.md](docs/scenario-format.md) for the data handoff.

The canonical [paper draft](https://docs.google.com/document/d/1hWacDlUdl_Tlyz4ObjvRS0kho9pjLVJCCPKF1rrSXeU/edit) includes six development scenarios awaiting independent review. They have not yet been integrated into the pipeline dataset. This repository ships only the illustrative `lease_access_01` fixture. The Adaption export is not part of the experiment dataset.

## Start here

Run commands in this folder with Python 3.11 or newer:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python source/pipeline.py validate data/development.json
python source/smoke.py results/offline-smoke
```

Optional figure generation: `python source/figures.py results/offline-smoke`. This wrapper requires the separately installed workspace renderer described below; it is not a standalone dependency of the core pipeline. The other commands above run without it.

The smoke command creates a new run and refuses to overwrite it. Its responses are hand-authored test fixtures, explicitly marked as such in the manifest and figure. They do not measure a model and must not appear in the research results. The figure renderer is reused from `D:\Apart Sprint\Figures-maker`; its installed dependencies are needed only for figures. Outputs go to `D:\Apart Sprint\Figures-maker\output\ai-x-epistemics\<run-name>`.

## Normal workflow

1. Elvina has delivered six development scenarios in the Doc. Guru's independent review is pending. Check source-to-field mapping, decision rules and answer keys, then convert reviewed cases to the format in `data/development.json`. The shipped fixture has no human review and no favorable/adverse annotations.
2. Copy `config/pilot.example.json` to a new non-secret config, select routes and frozen parameters, and agree on the budget. Keep development and held-out scenario families separate. Models are explicit per role, not defaults inherited from an old sprint.
3. Plan without making API requests:

```powershell
python source/pipeline.py plan data/development.json config/pilot.example.json results/pilot-plan
```

4. Collect writer responses. The offline import interface accepts JSONL records shaped as `{"job_id":"<exported ID>","raw_text":"<literal JSON response>"}` with optional `usage`. Jobs contain model-facing `system` and `user` strings; metadata is not sent to models. Do not send the complete scenario/answer-key file to a receiver or detector.

```powershell
python source/pipeline.py import results/pilot-plan results/pilot-plan/writer_jobs.jsonl path/to/writer-answers.jsonl
python source/pipeline.py prepare results/pilot-plan
python source/pipeline.py import results/pilot-plan results/pilot-plan/evaluation_jobs.jsonl path/to/evaluation-answers.jsonl
python source/pipeline.py analyze results/pilot-plan
python source/figures.py results/pilot-plan
```

`prepare` requires a valid writer response for every planned writer job. It stops instead of silently dropping a failed case. It creates neutral, promotional, balance-constrained promotional, random-matched, and full-evidence briefings. Every briefing is reused verbatim in both recipient contexts. Receiver and detector calls are independent. Each role can use a different route. To compare additional models, plan separately named runs with distinct configs; do not merge unlike routes or scientific versions silently.

## Live execution (not run yet)

Only `execute --live` contacts endpoints. It explicitly loads `D:\Apart Sprint\.env` with `override=False`, preserving supplied runtime variables. No local credential file is needed. Do not put secret values in config, prompts, URLs or model parameters. Config contains only the name of the credential variable.

Supported adapters: `openai_chat` (full HTTPS chat-completions endpoint) and `anthropic_messages` (full HTTPS messages endpoint with an explicit `api_version`). Provide an exact model ID, `key_env`, output cap, and provider-supported `parameters`. Routes have not been live-tested. Unsupported parameters fail rather than changing settings automatically.

Before planning, set config status to `approved_pilot` for authorized development inference or `frozen` for main collection. A main collection also requires `phase: heldout` and independently reviewed, held-out cases. Status flags record a team decision; they do not grant permission by themselves.

Each route must include a positive `max_request_usd`: a conservative, manually verified ceiling covering complete input, output/reasoning, and provider charges for ONE attempt. The runner reserves it before sending. These caps are estimates, not measured invoices. Unknown usage and failures remain in the journal and consume reservations. Check provider billing separately.

```powershell
python source/pipeline.py execute results/authorized-pilot results/authorized-pilot/writer_jobs.jsonl --live
python source/pipeline.py prepare results/authorized-pilot
python source/pipeline.py execute results/authorized-pilot results/authorized-pilot/evaluation_jobs.jsonl --live
```

There are cumulative request, output-token, reserved-dollar, and conservative timeout reservations. The timeout budget reserves the full configured timeout per attempt, even when it finishes early. Socket timeouts are not a provider billing guarantee. There are no automatic retries. Use `--retry-failed` deliberately; earlier attempts remain, including uncertain calls. Successful jobs are never rerun. After a crash, inspect the reservation and attempt journals before removing a stale `.execute.lock` file. Do not run imports concurrently with live execution.

Run manifests hash the source, data, config, writer jobs and prepared evaluation jobs. Each new run also keeps its Python source snapshot and interpreter version. Any change requires a separate run. Do not weaken this check to continue collection with modified scientific settings. Held-out planning requires an explicit `development_family_ids` list, rejects overlap with that list and the bundled development fixture, and requires an independent reviewer. The team must keep the declared development-family list complete.

## What the analysis means

- `episodes.csv`: every planned evaluation job, including invalid or unrun jobs; response actions, reference answers, coverage, critical omissions and possible action sets under joint missing-fact completions.
- `summary.csv`: valid and unresolved denominators, observed action rates, and worst/best-case violation bounds across all planned responses. Detector confusion counts include harmless-missing false flags and flags on present facts separately.
- `paired_family_contrasts.csv`: treatment-minus-neutral violation differences, averaged across repeats and context twins within each packet, then equally weighted across families. Only complete paired packets enter these contrasts. Incomplete counts are reported. A 5,000-draw family bootstrap supplies intervals only with at least two complete families. A single fixture cannot support an uncertainty claim. Different sample sizes and family counts must remain visible.
- `audit.json`: attempts, missing usage and interpretation limits. Read alongside both tables; valid-only plots do not resolve missing outcomes.

The implemented balance diagnostic is **selection imbalance only**: favorable inclusion rate minus adverse inclusion rate. It is null if valence labels are incomplete or a class is empty. It is not the complete JANUS five-dimensional evaluation, human misleadingness, or a safety certificate. A detector's labels are predictions, not ground truth. Text accuracy in extractive mode comes from verbatim rendering; textual fact-to-field correctness still needs human review.

Objective gaps are reported for feasible choices only, in each scenario's own units. Infeasible choices, clarification, and deferral remain separate; no arbitrary penalty is invented. Criticality tests only the finite alternatives specified by authors. The single-fact labels hold other facts fixed; joint completion sets are a separate sufficiency diagnostic. Completeness assumptions limit external validity.

## Still to agree

Full balance scoring/rubric, valence annotations, exact model versions and settings, reviewed scenario families, sample sizes, cost assumptions, primary endpoint, clarification/deferral scoring, false-alarm thresholds, free-text transfer and submission ownership. The code does not manufacture those decisions. Free-text matching, full JANUS integration and matched-FPR detector curves must be implemented after that protocol is agreed; current inputs are extractive facts and raw detector confusion counts. The paper's proposed scoring refinements are not all implemented in this version.

Sources for interfaces: [Chat Completions](https://developers.openai.com/api/reference/resources/chat), [Claude Messages](https://platform.claude.com/docs/en/api/messages). Research starting points: [JANUS and released artifacts](https://github.com/PolydorosG/JANUS), [omission detection](https://arxiv.org/abs/2608.31016), [evidence criticality](https://arxiv.org/abs/2609.39608). These links identify sources, not results reproduced in this project.
