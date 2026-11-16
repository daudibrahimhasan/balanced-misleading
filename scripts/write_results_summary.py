"""Write the numerical supplement from finished, audited tables only."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if '## Interpretation revision:' in (ROOT/'docs/RESULTS.md').read_text(encoding='utf-8'):
    raise SystemExit('Preserving the reviewed post hoc interpretation in docs/RESULTS.md. Reproduce its tables with final_report_audit.py and premise_boundary_audit.py instead.')
state=json.loads((ROOT/'approval/current-live-run.json').read_text());assert state['status']=='collection_finished_review_outputs'
run=Path(state['main_run']);a=run/'analysis';audit=json.loads((a/'report_audit.json').read_text());assert not audit['missing_jobs']
def read(name):return list(csv.DictReader((a/name).open(encoding='utf-8')))
def table(rows,columns):
    return '\n'.join(['| '+' | '.join(columns)+' |','| '+' | '.join(['---']*len(columns))+' |']+['| '+' | '.join(str(r.get(c,'')) for c in columns)+' |' for r in rows])
out=read('report_outcomes.csv');ds=read('report_detector_matched_valid.csv');selection=read('report_selection_summary.csv')
text=f'''# Completed development results

Authors: Daud Ibrahim Hassan and Elvina Chow, Independent Researchers.

The frozen run is `{run.name}`. These are six fictional development families with
tuned prompts, not held-out validation. Final independent human review remains
outstanding. The raw journals, frozen inputs, source snapshots and analysis are
in [main evidence](../data/main-v6).

## Collection audit

- Writer jobs: {audit['planned_writer_jobs']}; attempts: {audit['writer_attempts']}.
- Evaluation jobs: {audit['evaluation_jobs']}; records: {audit['evaluation_records']}.
- Evaluation statuses: `{audit['evaluation_statuses']}`.
- Missing job records: {len(audit['missing_jobs'])}; duplicate evaluation attempts: {len(audit['duplicate_evaluation_attempts'])}.
- Score/reference recomputation mismatches: {len(audit['independently_recomputed_receiver_score_mismatches'])}.
- Packet IDs: {audit['unique_briefing_ids']}; distinct briefing texts: {audit['distinct_briefing_texts']}.
- Known provider-reported usage: `{audit['known_reported_usage']}`.
- Attempts with unknown usage: {audit['usage_unknown_attempts']}.
- Reservation allowance: US${audit['reserved_usd']:.3f}, not a verified invoice.

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

{table(selection,['condition','packets','distinct_texts','zero_imbalance','critical_sensitive','critical_comparison','unresolved_reference_sensitive','unresolved_reference_comparison'])}

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

{table(out,['model','condition','context_index','planned','valid','wrong_option','false_neither','Clarify','Defer','Unresolved','incorrect_valid_rate','incorrect_planned_lower','incorrect_planned_upper'])}

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

{table(ds,['method','matched_valid_jobs','tp','fn','fp','tn','present_flags','exact','recall','false_alarm_harmless_missing','exact_rate'])}

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
`{audit['provider_response_model_labels']}`. These are provider-reported identities;
underlying weights were not independently inspected.

The audit reparsed raw successful outputs, checked writer blindness and shared
briefings, and independently reimplemented reference arithmetic and endpoint
checks. This is automated verification, not independent human validation of
scenario realism, domains or labels. See [final review](FINAL_REVIEW.md) and
[literature checks](literature-check.md). No final coauthor approval or external
submission is inferred from these files.
'''
(ROOT/'docs/RESULTS.md').write_text(text,encoding='utf-8')
print('Wrote docs/RESULTS.md from audited final tables')
