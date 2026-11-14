# Current status

## Objective
Implement Daud's part of Balanced but Misleading: a reproducible extractive-briefing pipeline, finite reference checker, model execution/logging, analysis and figure generation.

## Canonical inputs
- Full six-case specifications: `docs/development-scenarios.md`; exact current system prompts and payload boundaries: `docs/prompt-templates.md`. These are draft documentation, not integrated or independently reviewed experimental data. The paper retains only a summary and one worked example.
- Team plan: https://docs.google.com/document/d/1UNlPj2cU38PA7VzWCqd9kOQzmgSEjc77aonBI545XrE/edit
- Canonical paper: https://docs.google.com/document/d/1hWacDlUdl_Tlyz4ObjvRS0kho9pjLVJCCPKF1rrSXeU/edit . The research plan remains the scenario/review workspace. Relevant methods and six development specifications were transferred to the paper on 2026-11-14; no empirical results are claimed. Independent scenario and literature review remains pending.
- Development fixture: `data/development.json`. Fictional lease example, unreviewed, unassigned valence, never held-out evidence.
- Config template: `config/pilot.example.json`. No model/provider or scientific settings selected.
- Credentials: explicit shared `D:\Apart Sprint\.env`; preserve runtime values; no duplicate secret file.
- No manuscript, main dataset, empirical results or submission currently exists in this folder.

## Implemented
Reference constraints and objective solver; finite counterfactual criticality and joint missing-fact enumeration; scenario/key validation; fixed fact rendering; writer job export; response validation/import; matched random and full-evidence controls; paired-context receiver/detector export; guarded, append-only execution adapters; source/data/config/job hashes; raw outputs/usage/failure journals; episode and summary CSVs; family-level paired contrasts and bootstrap; shared figure-renderer integration.

## Checks
11 automated tests pass, covering the reference keys, unknown facts, ties, invalid scenarios, duplicate fields, independent review requirements, response failures, information boundaries, configuration and job tampering, family overlap, draft execution rejection, runtime environment precedence, request reservations and resume. Offline smoke v2 exercises 3 writer responses and 40 evaluation responses, all hand-authored fixtures, with zero network calls. CSVs and PNG/SVG generation were checked; fixture charts are explicitly labeled NOT RESEARCH. An earlier smoke artifact is retained with its original source hash. No live inference, dataset restoration, teammate messages, or publication has been performed.

## Frozen settings
None for scientific collection. Each planned run freezes implementation/data/config/jobs. Illustrative example and hand-authored smoke outputs are for software checks only.

## Review fixes (2026-11-14)
Primary family contrasts and plot inputs now use incorrect commitment, with constraint violation secondary. Writer payloads exclude recipient contexts. Renderer uses dataset source-fact order. Tie-aware warranted actions intersect joint completion optima; receiver diagnostics distinguish warranted, unwarranted-correct, and incorrect commitments and clarification justification. All facts still require declared alternatives. Public fact payloads expose IDs/text only. Thirteen automated tests pass, including feasible-suboptimal contrast, tie intersection, writer isolation and fact-boundary regressions. No model requests were made for these fixes. Old review-package exports remain snapshots of the pre-fix code.

Still blocked before scientific collection: reviewed derived objectives and all-fact alternatives for six cases, receiver `neither` support, final primary endpoint approval and prompt arms, fair detector baselines, independent review and frozen scientific settings. Bootstrap output is descriptive; no population-level claim is justified by six development families.

## Access checks
Separate provider access probes were performed; those establish access only, not task competence or experimental results. Access-probe scripts and logs are excluded from this repository. The selected study models are DeepSeek V4.1 Flash, Mistral Large 4, and Nemotron 3 Ultra. Scientific settings are not frozen.

## Next
Elvina has delivered six development scenarios and a paper draft in the team plan. Guru's independent review of rules and keys is pending. Integrate the reviewed cases into the pipeline; the Adaption CSV remains unchanged raw generated material. Resolve and freeze valence/balance rubric, endpoints, scoring of clarification versus no feasible option, sample/family split, model settings and thresholds. Current selection metric is not full JANUS; free-text and matched-FPR detector comparisons are not implemented. Measure one complete pilot episode's actual usage before budgeting scale-up. Model access checks are not experimental results.
