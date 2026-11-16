# Balanced but Misleading

**Can epistemic scores miss decision-changing omissions?**

Daud Ibrahim Hassan and Elvina Chow, Independent Researchers.

Six fictional development families about leases and job offers. The study compares
neutral, promotional, balance-instructed promotional, valence-matched random and
full-evidence briefings under explicit decision rules. This is a development
experiment with tuned prompts, not held-out validation or a general model ranking.

- [Canonical paper](https://docs.google.com/document/d/1hWacDlUdl_Tlyz4ObjvRS0kho9pjLVJCCPKF1rrSXeU/edit)
- [Report PDF](paper/Balanced-but-Misleading-report.pdf)
- [Readable manuscript](paper/manuscript.md)
- [Results and audit](docs/RESULTS.md)
- [Main run evidence](data/main-v6)
- [Figures, source data and chart specifications](figures/results)
- [Remaining review](docs/FINAL_REVIEW.md)
- [Team plan](https://docs.google.com/document/d/1UNlPj2cU38PA7VzWCqd9kOQzmgSEjc77aonBI545XrE/edit)

## Main observation and post-collection correction

The completed run tests a partially observed qualification task. A post-collection
review by Elvina found that the conversion withheld some setup assertions that her
authored cases established as known. The revised paper reports that executed task;
it does not present the new interpretation as a prespecified hypothesis.

Of 930 valid receiver responses, 19 select neither even though a qualifying option
exists. All 19 public justifications cite missing qualification evidence: 13 GLM
outputs and six Nemotron outputs, across four families and seven distinct
briefing/context inputs. This is an output-level diagnosis with LLM-assisted
inspection, not independent human coding or a proven internal mechanism.

All 18 balance-instructed packets omit only neutral-labeled facts; none omits the
planted candidate or paired fact. The as-run critical-omission counts are 17/18
sensitive and 13/18 comparison. Excluding the reviewer-identified setup facts
reduces them to **4/18 and 3/18**. This is a label sensitivity analysis, not a
corrected receiver experiment. Original condition contrasts remain mixed.

[Premise audit, exclusions and all 19 justifications](docs/reviews/premise-boundary-20261116).
The frozen run is unchanged. The contribution is a reproducible separation of
selection balance, qualification evidence and abstention semantics, including the
effect of task conversion on the headline. No general promotional effect or
failure of the full JANUS framework is established.

![Incorrect commitments by model and context](figures/results/incorrect-commitments/figure.png)

Bars use valid-response denominators. The 15 unresolved evaluations remain in the
audit and all-planned bounds. These constructed development results do not establish
held-out performance, effects on people, or a full JANUS evaluation.

## Models and collection

DeepSeek V4.1 Flash 1017 is the writer; all three models are receivers; Nemotron
3.5 Super VL is the scoped detector. GLM-5.3-Flash is the third receiver family.
Exact requested model IDs, public provider routes, returned model labels, prompts,
settings and source/data/job hashes are preserved in the evidence.

The repaired development competence screen passed 42/42 initial responses. The
main design has 54 writer jobs, 936 receiver jobs and 312 detector jobs. One invalid
writer selection received an explicitly authorized identical retry. Interrupted
reserved evaluation jobs remain unresolved and were not resent. The main evaluation has 1,233 valid responses and 15 unresolved outcomes, with a
record for every planned job. Read the audit for counts and exclusions. Earlier failed screens are separate, not replaced by successes.

The immutable cases retain their original pending review metadata. Daud authorized
collection and reports completing the earlier review task; this is not independent
human validation of the formal conversion. Final coauthor review remains open.
Historical handoff files are retained for provenance, not current authorship or
launch instructions. [Repair history](docs/repair-validation.md).

## Reproduce the analysis without model calls

Python 3.11 or newer:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python source/pipeline.py analyze data/main-v6
python scripts/final_report_audit.py --run data/main-v6
python scripts/premise_boundary_audit.py
```

Analysis does not require provider credentials. Do not rerun generators over the
frozen cases or treat the separate `data/development.json` software fixture as
empirical evidence. Exact source snapshots are included with each run.

## Scoring and scope

The primary endpoint is incorrect commitment, including feasible suboptimal
choices and false neither responses. Constraint violation is secondary. Correct
choice, reference-warranted choice, clarification, deferral and unresolved requests
are distinct outcomes. The submitted action is scored even when its explanation
disagrees. Tied optima are accepted.

Criticality varies one fact over a declared finite domain while holding others
true. Reference warrant intersects best-action sets over joint completions.
Receivers do not see these domains, so warrant is an evaluator-scoped diagnostic.
Selection imbalance is favorable inclusion fraction minus adverse inclusion
fraction; exactly zero is a score pass. This is not a full JANUS implementation.

Same-information detector baselines are a missing-fact checklist and static
rule-topic heuristic. False alarms use harmless omitted facts; present-fact flags
are reported separately. Matched-valid comparisons and all-planned baseline
results are both supplied. No matched-FPR superiority claim is made.

Repeated calls do not create independent families. Family contrasts and bootstrap
intervals are descriptive. Missing-response bounds and excluded families are
explicit. No human-harm, spontaneous-intent, held-out or deployment claim follows.

## Evidence and figures

All attempts, failures, reservations, writer retry and recovery events are
retained. Reported tokens exclude unknown usage. Reservation allowances are not
provider invoices. Credentials and authorization headers are excluded.

Figures use Montserrat and the workspace research-figures renderer. PNG, SVG,
source CSV and validated JSON specifications are included. Regenerating the exact
style needs that separate renderer at `D:/Apart Sprint/Figures-maker`; core scoring
and audit reproduction do not. The pipeline diagram is conceptual, not a result.

## Preexisting tools and sprint work

The generic workspace research guidance and research-figures renderer predate this
sprint; the renderer file is dated September 2026. They supply workflow and
visualization, not results or conclusions. The project repository begins on
14 November 2026. The six-case formalization, project-specific evaluator, prompts,
model experiments, analysis and manuscript are the work reported for this sprint.
The original scenario prose and full version history are retained.
