# Current status

## Current: Version 6 passed; main collection not launched

All 42 initial responses in `results/repair-v6-screen-20261115T184213Z` are valid and correct: DeepSeek V4.1 Flash 1017, GLM-5.3-Flash and Nemotron 3.5 Super VL each passed 14/14. No request failures, retries or replacement answers occurred in this version. All 26 software tests pass. Canonical repair report: `docs/repair-validation.md`; exact prompts: `docs/prompt-templates.md`; current configuration: `config/competence.repair-v6.json`.

Repairs: newer DeepSeek checkpoint via Deploy; reason-first receiver JSON with explicit action consistency; GLM API JSON-object mode; NVIDIA reasoning off, one in-flight request and six-second start spacing. Labels, rules and action-based scoring were not relaxed. These are development-stage changes informed by earlier failures, not held-out confirmation. All previous screen versions and diagnostics remain preserved and are summarized in the repair report.

Offline main plan: `results/repair-v6-screen-20261115T184213Z-main-plan-review`, 54 writer jobs and 1302 total proposed calls. `config/exploratory.repair-v6.proposed.json` is in awaiting-main-launch status, not executable as is. Main has not started. Invoice costs and remaining provider balances must not be inferred from reservation allowances. Earlier sections below are historical where they conflict with this latest state.

Latest Nemotron candidate check: official NVIDIA 3.5 Super/Lightning documentation reviewed. Both direct NVIDIA routes returned a correct JSON probe (Super VL 5.17 s; Lightning 2.55 s). User-requested Super VL candidate screen: `approval/nemotron-super-candidate-screen.json`, run-local report under `results/nemotron-super-screen-20261115T174750Z`. All 14 planned initial calls were attempted; 13 completed valid and correct, and one did not complete successfully. The original gate therefore did not pass. `config/competence.nemotron-lineup.proposed.json` prepares Super VL as MiniMax's replacement, with execution disabled. No main run restarted; DeepSeek's previous 11/14 remains a separate unresolved competence blocker.

## Version 3 completed: main gate did not pass

Daud renewed start authorization for DeepSeek V4.1 Flash (Modal), GLM-5.3-Flash (Deploy) and MiniMax M3.1 Flash (NVIDIA), conditional on the unchanged competence criterion. All 42 initial screen calls completed as attempts at `results/glm-study-20261115T174120Z/competence`. Report: `screen-report.md`, `competence-result.json`, `screen-problems.json`; pointer: `approval/current-live-run.json`.

DeepSeek: 14 valid, 11 correct. GLM: 14 valid, 14 correct. MiniMax: eight valid, eight correct, plus four HTTP 503 and two HTTP 429 failures. No retries or successful replacements. GLM passes its own screen; the required three-model 100% valid/correct gate did not pass. No main study was launched. The stop record is true because the fixed gate failed, not because a new human stop was invented.

Version 3 settings were frozen before collection: temperature 0, 4096 output-token cap, 180-second timeout, one in-flight request per route, GLM low reasoning effort. All 23 tests passed before launch; a separate offline check verified per-route concurrency and reservation accounting. The USD 0.63 reservation total is not billed spend. Earlier failed versions remain separate and are not pooled. The sections below are historical state where they conflict with this version.

Latest operational audit: `results/route-reliability-20261115T171738Z/reliability-report.md`. Across 37 small completion probes covering all 11 configured slots and selected models, the chosen Modal DeepSeek route and free OpenRouter Nemotron 3 Ultra / 3.5 Super VL routes each completed 3/3 repeated probes. This is an operational shortlist, not a scientific screen pass. OpenRouter key metadata reports 50 free requests/day; the proposed layout using these routes would need 936 OpenRouter evaluation calls. Current free quotas do not support claiming a full uninterrupted run. MiniMax and Gemma failed repeated-route checks; NVIDIA Mistral/GLM/GPT-OSS timed out. No main collection restarted, and the original gate remains in force.

## Latest decision: strict gate retained, main not launched

Daud explicitly authorized replacing Nemotron 3 Ultra with MiniMax M3.1 Flash. The revised 42-item screen is frozen at `results/minimax-study-20261115T170917Z/competence`; its configuration is `config/competence.minimax-approved.json`. Output cap 4096, timeout 120 seconds and three concurrent requests were fixed before this screen. A separate offline concurrency check verified pre-request reservation accounting and request-cap enforcement. All 23 tests passed before launch.

The screen stopped without passing. Per model, 14 items were planned. DeepSeek: six valid responses, five correct (one action/explanation inconsistency). MiniMax: three valid correct responses and two HTTP errors. Mistral: three request timeouts and three interrupted reservations with unknown usage. There are 17 reservations total: nine valid answers, five completed request failures and three interrupted requests. Unattempted jobs remain missing. No scientific main-run directory or main requests were created. Records: `approval/current-live-run.json`, `approval/competence-minimax-result.json` and the run-local `competence-result.json`.

After these failures, Daud explicitly instructed: "Keep the original gate; stop before the main study". Do not waive the gate or resume main collection. This supersedes earlier conditional launch instructions. The earlier Nemotron screen and availability probes remain separate and are not pooled with this screen. The stage summaries below are historical preparation state where they conflict with this latest decision.

## Objective

Run the prepared six-case study under Daud's 15 November authorization, beginning with the competence screen and preserving the existing acceptance criterion and budget guards. Daud reports completing Guru's review task. This is Daud's authorization, not an approval attributed to Govardhan Reddy. Record: `approval/daud-launch-authorization.json`.

Latest preflight: all 23 tests pass. No study inference calls launched. Daud selected Modal. Read-only catalog checks returned HTTP 200 for all four configured Modal routes; all list only DeepSeek V4.1 Flash. Mistral Large 4 and Nemotron 3 Ultra are not listed by any configured Modal endpoint. A clarification is pending: use NVIDIA for those two or supply their Modal endpoints. Verified request ceilings also remain outstanding. Catalog evidence: `results/modal-catalog-20261115.json`. The final configuration and digest cannot be frozen until routing and pricing are resolved. The sections below describing the original Guru handoff are historical preparation state and do not revoke Daud's new authorization.

## Canonical inputs

## Live execution update: 15 November

Daud explicitly selected Modal for DeepSeek and NVIDIA for Mistral/Nemotron. The 42-item screen was frozen at `results/competence-live-20261115T164403Z`; its report is `approval/competence-result.json` (`not_passed`, human acceptance false). Two DeepSeek items were valid and correct. Mistral timed out and Nemotron returned HTTP 503. The screen was stopped when the fixed acceptance criterion became unattainable; all planned jobs remain, and any interrupted reserved request is recorded with unknown usage. No successful retries replace failures.

Four separate 64-token infrastructure probes across the two configured NVIDIA credential slots reproduced Mistral read timeouts and Nemotron `Service temporarily overloaded` HTTP 503. Evidence: `results/nvidia-route-diagnosis-20261115.json`. Main study has not started. Provider recovery or an explicitly versioned route change is required before a fresh competence screen; retain the failed version. Monetary reservations are estimates, not invoices or provider-enforced spend limits. Daud's authorization is recorded under his name, not Guru's. All 23 tests passed before launch.

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

The canonical manuscript and plan are aligned to these proposals. On 14 November, Elvina's Introduction, Related Work, Methods and Limitations edits were reconciled and merged into the paper. The older neither/clarification wording, rotating model roles and incomplete detector inputs were not carried over. Existing reference numbering is preserved; MASK-OFF and detailed new sabotage-by-omission claims remain pending accessible primary-source verification. Abstract, results, interpretation, future work and conclusion remain pending collection. Publication and detector-superiority claims remain out of scope. No empirical results, independent human sign-off or submission exist.
