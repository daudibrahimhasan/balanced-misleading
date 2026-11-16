"""Post hoc, offline audit of the executed information boundary. No model calls."""
import collections
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'data/main-v6'
OUT = ROOT / 'docs/reviews/premise-boundary-20261116'
EXCLUDE = {
    'job_health_01': {'F5', 'F6'},
    'job_schedule_01': {'F5', 'F6'},
    'lease_break_01': {'F5', 'F6'},
    'job_moving_01': {'F7', 'F8'},
    'lease_deposit_01': {'F5', 'F6'},
}


def write_csv(name, rows):
    with (OUT / name).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    episodes = list(csv.DictReader((RUN / 'analysis/episodes.csv').open(encoding='utf-8')))
    jobs = {x['id']: x for x in map(json.loads, (RUN / 'evaluation_jobs.jsonl').read_text(encoding='utf-8').splitlines())}
    attempts = {x['job_id']: x for x in map(json.loads, (RUN / 'attempts.jsonl').read_text(encoding='utf-8').splitlines())}
    cases = {x['id']: x for x in json.loads((RUN / 'cases.json').read_text(encoding='utf-8'))}
    briefs = json.loads((RUN / 'briefings.json').read_text(encoding='utf-8'))
    unique = {}
    for row in episodes:
        unique.setdefault((row['brief'], row['context_index']), row)
    sensitivity = []
    for row in unique.values():
        critical = set(json.loads(row['critical_missing']))
        excluded = critical & EXCLUDE.get(row['case'], set())
        sensitivity.append(dict(brief=row['brief'], case=row['case'], condition=row['condition'],
                                writer_replicate=row['writer_replicate'], context_index=row['context_index'],
                                critical_original=';'.join(sorted(critical)),
                                excluded_by_review=';'.join(sorted(excluded)),
                                critical_after_exclusion=';'.join(sorted(critical - excluded))))
    write_csv('label-sensitivity.csv', sensitivity)
    receiver = [r for r in episodes if r['role'] == 'receiver' and r['status'] == 'ok']
    false = [r for r in receiver if r['action'] == 'neither' and r['incorrect_commitment'] == '1']
    rationale_rows = []
    for row in false:
        job = jobs[row['job_id']]
        payload = json.loads(job['user'])
        reason = attempts[row['job_id']]['parsed']['reason']
        # This tag makes a reproducible lexical screen, not independent semantic coding.
        mentions_missing = any(s in reason.lower() for s in ['unknown', 'unstated', 'not stated', 'not specified', 'not confirmed', 'unspecified', 'missing', 'not establish', 'no full-time', 'lacks'])
        rationale_rows.append({k: row[k] for k in ['job_id', 'brief', 'case', 'condition', 'context', 'model', 'truth_best']} |
                              dict(action='neither', reason=reason, lexical_missing_screen=mentions_missing,
                                   semantic_review='LLM-assisted inspection: cites missing qualification evidence; independent human coding pending',
                                   briefing=payload['briefing'], recipient=json.dumps(payload['recipient'], ensure_ascii=False)))
    write_csv('false-neither.csv', rationale_rows)
    counts = {}
    for condition in ['balanced_promotional', 'promotional', 'neutral', 'random_matched']:
        counts[condition] = {}
        for ctx in ['0', '1']:
            rr = [r for r in sensitivity if r['condition'] == condition and r['context_index'] == ctx]
            counts[condition][ctx] = dict(n=len(rr), as_run=sum(bool(r['critical_original']) for r in rr),
                                         after_exclusion=sum(bool(r['critical_after_exclusion']) for r in rr))
    balanced = [b for b in briefs if b['condition'] == 'balanced_promotional']
    omitted = [(b, [f for f in cases[b['case']]['facts'] if f['id'] not in b['included']]) for b in balanced]
    assert len(balanced) == 18
    assert all(f['valence'] == 'neutral' for _, ff in omitted for f in ff)
    assert all(not {cases[b['case']]['matched_fact_id'], cases[b['case']]['paired_fact_id']} & {f['id'] for f in ff} for b, ff in omitted)
    assert len(receiver) == 930 and len(false) == 19
    assert counts['balanced_promotional']['0'] == dict(n=18, as_run=17, after_exclusion=4)
    assert counts['balanced_promotional']['1'] == dict(n=18, as_run=13, after_exclusion=3)
    inputs = {(r['case'], r['context'], json.loads(jobs[r['job_id']]['user'])['briefing']) for r in false}
    summary = dict(scope='Post hoc as-run audit; no corrected receiver experiment; no independent rationale coding.',
                   valid_receivers=len(receiver), false_neither=len(false), distinct_inputs=len(inputs),
                   packet_ids=len({r['brief'] for r in false}), families=dict(collections.Counter(r['family'] for r in false)),
                   models=dict(collections.Counter(r['model'] for r in false)),
                   conditions=dict(collections.Counter(r['condition'] for r in false)), sensitivity=counts,
                   exclusions={k: sorted(v) for k, v in EXCLUDE.items()}, balanced_candidate_pair_omissions=0)
    assert summary['distinct_inputs'] == 7 and summary['packet_ids'] == 10
    summary['input_sha256'] = {name: hashlib.sha256((RUN / name).read_bytes()).hexdigest() for name in
                               ['analysis/episodes.csv', 'evaluation_jobs.jsonl', 'attempts.jsonl', 'cases.json', 'briefings.json']}
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
