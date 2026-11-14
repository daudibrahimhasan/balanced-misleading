"""Exercise prepared multi-model workflow with hand-authored answers, never models."""
import datetime as dt
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source'))
import pipeline
from study import load, save, read_lines, choose, coverage

run=ROOT/'results'/('prepared-software-fixture-'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
pipeline.plan(ROOT/'data/pilot-cases.proposed.json',ROOT/'config/exploratory.proposed.json',run)
manifest=load(run/'manifest.json');manifest['kind']='offline_smoke_fixture';manifest['warning']='HAND-AUTHORED SOFTWARE FIXTURE; NOT RESEARCH OR MODEL PERFORMANCE';save(run/'manifest.json',manifest)
cases=load(run/'cases.json');records=[]
for j in read_lines(run/'writer_jobs.jsonl'):
    c=next(c for c in cases if c['id']==j['metadata']['case'])
    ids=[f['id'] for f in c['facts'] if f['id'] not in {c['matched_fact_id'],'F1'}]
    records.append({'job_id':j['id'],'raw_text':json.dumps({'included_fact_ids':ids})})
assert len(records)==54
path=run/'hand_authored_writers.jsonl';path.write_text('\n'.join(json.dumps(r) for r in records),encoding='utf-8')
pipeline.import_answers(run,run/'writer_jobs.jsonl',path);pipeline.prepare(run)
briefs={b['id']:b for b in load(run/'briefings.json')};records=[]
for j in read_lines(run/'evaluation_jobs.jsonl'):
    c=next(c for c in cases if c['id']==j['metadata']['case']);ctx=next(x for x in c['contexts'] if x['id']==j['metadata']['context'])
    b=briefs[j['metadata']['brief']];truth=choose(c,ctx)
    parsed={'action':truth['best'][0] if truth['best'] else 'neither'} if j['role']=='receiver' else {'critical_missing_fact_ids':coverage(c,ctx,b['included'])['critical_missing']}
    records.append({'job_id':j['id'],'raw_text':json.dumps(parsed)})
assert len(records)==1248
path=run/'hand_authored_evaluations.jsonl';path.write_text('\n'.join(json.dumps(r) for r in records),encoding='utf-8')
pipeline.import_answers(run,run/'evaluation_jobs.jsonl',path);pipeline.analyze(run)
print('SOFTWARE FIXTURE ONLY:',len(records),'evaluation jobs and 54 writer fixtures; zero model requests. Artifacts:',run)
