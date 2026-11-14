"""Score actual full-evidence competence attempts. Never grants human acceptance."""
import argparse
from collections import defaultdict
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source'))
import pipeline
from study import load, read_lines, choose, specification_hash, digest, save

def report(run, output):
    config,cases=pipeline.frozen(run)
    if config.get('purpose')!='competence':raise ValueError('Not a competence run')
    manifest=load(run/'manifest.json');jobs=read_lines(run/'evaluation_jobs.jsonl');success=pipeline.latest_success(run)
    attempts=read_lines(run/'attempts.jsonl')
    by_model=defaultdict(lambda:{'planned':0,'valid':0,'correct':0,'live_evidence':0})
    for j in jobs:
        if j['role']!='receiver' or j['metadata']['condition']!='full_evidence':raise ValueError('Unexpected competence job')
        counts=by_model[j['route']['model']];counts['planned']+=1
        answer=success.get(j['id'])
        if not answer:continue
        counts['valid']+=1;counts['live_evidence']+=answer.get('origin')=='live' and bool(answer.get('provider_response'))
        case=next(c for c in cases if c['id']==j['metadata']['case'])
        ctx=next(c for c in case['contexts'] if c['id']==j['metadata']['context'])
        truth=choose(case,ctx);action=answer['parsed']['action']
        counts['correct']+=action in truth['best'] or (action=='neither' and not truth['feasible'])
    passed=bool(jobs) and all(c['correct']==c['valid']==c['live_evidence']==c['planned'] for c in by_model.values())
    passed=passed and all(len([a for a in attempts if a['job_id']==j['id']])==1 for j in jobs)
    result={'status':'passed' if passed else 'not_passed','human_accepted':False,'source_hash':pipeline.source_hash(),
        'competence_run':str(run),'by_model':dict(by_model),'case_spec_hashes':[specification_hash(c) for c in cases],
        'receiver_route_hashes':[digest(r) for r in config.get('role_routes',{}).get('receiver',[config['roles']['receiver']])],
        'criteria':'100% valid and full-evidence correct across every preplanned item and model, with live provider evidence. A tied optimum permits any best option. No post-hoc reruns to replace failed items.',
        'note':'Passing is a software-computed screen, not human acceptance or an omission-study result.'}
    if manifest.get('kind')=='offline_smoke_fixture':result['status']='software_fixture_only'
    save(output,result);return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('run',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();print(report(a.run,a.output)['status'])
