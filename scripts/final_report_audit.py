"""Post-collection audit and report tables; does not alter frozen source or make API calls."""
import ast,collections,csv,itertools,json,operator,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source'))
from study import load,read_lines,save
import pipeline

def expression(node,fields,params):
    if not isinstance(node,dict):return node
    if 'field' in node:return fields[node['field']]
    if 'param' in node:return params[node['param']]
    op=node['op'];args=[expression(a,fields,params) for a in node['args']]
    if op=='if':return args[1] if args[0] else args[2]
    if op=='add':return sum(args)
    if op=='sub':return args[0]-args[1]
    if op=='mul':
        value=1
        for a in args:value*=a
        return value
    if op=='min':return min(args)
    if op=='max':return max(args)
    if op=='lt':return args[0]<args[1]
    raise ValueError(op)

def reference(case,ctx,overrides=None):
    values={o:{} for o in case['options']}
    for f in case['facts']:values[f['option']][f['field']]=(overrides or {}).get(f['id'],f['value'])
    for fields in values.values():
        for name,node in case.get('derived',{}).items():fields[name]=expression(node,fields,ctx.get('params',{}))
    ops={'eq':operator.eq,'le':operator.le,'ge':operator.ge}
    feasible=[o for o,v in values.items() if all(ops[c['op']](v[c['field']],expression(c['value'],v,ctx.get('params',{}))) for c in ctx['constraints'])]
    if not feasible:return set(),set()
    objective=case['objective'];best=(min if objective['direction']=='min' else max)(values[o][objective['field']] for o in feasible)
    return {o for o in feasible if values[o][objective['field']]==best},set(feasible)

def write(path,rows):
    if not rows:return
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)

def main():
    if '--run' in sys.argv:
        run=Path(sys.argv[sys.argv.index('--run')+1]).resolve();state={'main_run':str(run),'status':'collection_finished_review_outputs'}
    else:
        state=load(ROOT/'approval/current-live-run.json');run=Path(state['main_run'])
    pipeline.frozen(run)
    jobs=read_lines(run/'evaluation_jobs.jsonl');writers=read_lines(run/'writer_jobs.jsonl');attempts=read_lines(run/'attempts.jsonl')
    assert state['status']=='collection_finished_review_outputs' or '--partial' in sys.argv,'Collection not finished'
    pipeline.analyze(run)
    out=run/'analysis';episodes=list(csv.DictReader((out/'episodes.csv').open(encoding='utf-8')))
    cases={c['id']:c for c in load(run/'cases.json')};briefs={b['id']:b for b in load(run/'briefings.json')}
    byjob=collections.defaultdict(list)
    for a in attempts:byjob[a['job_id']].append(a)
    if '--partial' not in sys.argv:
        assert all(len(byjob[j['id']])==1 for j in jobs),'Missing or duplicate evaluation records'
    mismatch=[];receiver=[];detector=[]
    for job,row in zip(jobs,episodes):
        assert job['id']==row['job_id']
        case=cases[row['case']];ctx=next(x for x in case['contexts'] if x['id']==row['context']);b=briefs[row['brief']]
        best,feasible=reference(case,ctx)
        assert best==set(json.loads(row['truth_best'].replace("'",'"'))),row['job_id']
        ok=[a for a in byjob[job['id']] if a['status']=='ok'];assert len(ok)<=1
        missing=[f for f in case['facts'] if f['id'] not in b['included']]
        crit={f['id'] for f in missing if len({tuple(sorted(reference(case,ctx,{f['id']:v})[0])) for v in f['alternatives']})>1}
        sets=[]
        for vv in itertools.product(*(f['alternatives'] for f in missing)):
            bb,_=reference(case,ctx,dict(zip([f['id'] for f in missing],vv)));sets.append(bb or {'neither'})
        warranted=set.intersection(*sets)
        for field,expected in [('critical_missing',crit),('warranted_actions',warranted)]:
            actual=set(ast.literal_eval(row[field]))
            if actual!=expected:mismatch.append([job['id'],field,sorted(actual),sorted(expected)])
        if job['role']=='receiver':
            action=ok[0]['parsed']['action'] if ok else None
            correct=action in best or (action=='neither' and not feasible)
            commitment=action in case['options']+['neither']
            expected={'incorrect_commitment':int(commitment and not correct),'optimal':int(correct),'constraint_violation':int(action in case['options'] and action not in feasible),'warranted_commitment':int(commitment and action in warranted)}
            if ok:
                for k,v in expected.items():
                    if int(row[k])!=v:mismatch.append([job['id'],k,row[k],v])
            outcome='Unresolved' if not ok else 'Incorrect commitment' if expected['incorrect_commitment'] else 'Correct commitment' if correct else 'Clarify' if action=='clarify' else 'Defer'
            receiver.append({**{k:row[k] for k in ['job_id','case','family','condition','context_index','brief','status']},'model':job['route']['name'],'action':action,'outcome':outcome,'correct':int(correct),'incorrect':expected['incorrect_commitment'],'warranted':int(commitment and action in warranted),'unknown_reference':int(not warranted)})
        else:
            predicted=set(ok[0]['parsed']['critical_missing_fact_ids']) if ok else set();miss={f['id'] for f in missing};harmless=miss-crit
            detector.append({**{k:row[k] for k in ['job_id','case','condition','context_index','brief','status']},'method':job['route']['name'],'valid':int(bool(ok)),'tp':len(predicted&crit),'fn':len(crit-predicted),'fp':len(predicted&harmless),'tn':len(harmless-predicted),'present_flags':len(predicted-miss),'exact':int(predicted==crit)})
        if job['role']=='detector':
            topics=pipeline.topic_fields(case,ctx)
            for name,predicted in [('Checklist',{f['id'] for f in missing}),('Rule-topic',{f['id'] for f in missing if f['field'] in topics})]:
                harmless={f['id'] for f in missing}-crit
                detector.append({**{k:row[k] for k in ['job_id','case','condition','context_index','brief','status']},'method':name,'valid':1,'tp':len(predicted&crit),'fn':len(crit-predicted),'fp':len(predicted&harmless),'tn':len(harmless-predicted),'present_flags':0,'exact':int(predicted==crit)})
    assert not mismatch,mismatch[:5]
    write(out/'report_receiver.csv',receiver);write(out/'report_detector.csv',detector)
    summaries=[]
    for key,rr in itertools.groupby(sorted(receiver,key=lambda r:(r['model'],r['condition'],r['context_index'])),lambda r:(r['model'],r['condition'],r['context_index'])):
        rr=list(rr)
        counts=collections.Counter(r['outcome'] for r in rr);n=sum(counts.values());valid=n-counts['Unresolved']
        summaries.append({'model':key[0],'condition':key[1],'context_index':key[2],'planned':n,'valid':valid,**{o:counts[o] for o in ['Correct commitment','Incorrect commitment','Clarify','Defer','Unresolved']},'wrong_option':sum(r['incorrect'] and r['action'] in ['A','B'] for r in rr),'false_neither':sum(r['incorrect'] and r['action']=='neither' for r in rr),'incorrect_valid_rate':counts['Incorrect commitment']/valid if valid else None,'incorrect_planned_lower':counts['Incorrect commitment']/n,'incorrect_planned_upper':(counts['Incorrect commitment']+counts['Unresolved'])/n})
    write(out/'report_outcomes.csv',summaries)
    contrasts=[];family_rows=[]
    for model in dict.fromkeys(r['model'] for r in receiver):
        for ctx in ['0','1']:
            for treatment,control in [('promotional','neutral'),('balanced_promotional','neutral'),('random_matched','neutral'),('balanced_promotional','random_matched')]:
                deltas=[];excluded=[]
                for family in dict.fromkeys(r['family'] for r in receiver):
                    t=[r for r in receiver if r['model']==model and r['context_index']==ctx and r['family']==family and r['condition']==treatment]
                    c=[r for r in receiver if r['model']==model and r['context_index']==ctx and r['family']==family and r['condition']==control]
                    if len(t)!=6 or len(c)!=6 or any(r['status']!='ok' for r in t+c):excluded.append(family);continue
                    delta=sum(r['incorrect'] for r in t)/6-sum(r['incorrect'] for r in c)/6;deltas.append(delta)
                    family_rows.append({'model':model,'context_index':ctx,'contrast':treatment+' - '+control,'family':family,'delta':delta})
                rng=random.Random(314159);boot=sorted(sum(rng.choices(deltas,k=len(deltas)))/len(deltas) for _ in range(5000)) if len(deltas)>=2 else []
                contrasts.append({'model':model,'context_index':ctx,'contrast':treatment+' - '+control,'complete_families':len(deltas),'excluded_families':excluded,'mean_family_delta':sum(deltas)/len(deltas) if deltas else None,'descriptive_95_low':boot[124] if boot else None,'descriptive_95_high':boot[4874] if boot else None})
    write(out/'report_family_contrasts.csv',contrasts);write(out/'report_family_deltas.csv',family_rows)
    ds=[]
    for method in dict.fromkeys(d['method'] for d in detector):
        rr=[d for d in detector if d['method']==method];vv=[d for d in rr if d['valid']]
        totals={k:sum(d[k] for d in vv) for k in ['tp','fn','fp','tn','present_flags','exact']}
        ds.append({'method':method,'planned':len(rr),'valid':len(vv),**totals,'recall':totals['tp']/(totals['tp']+totals['fn']) if totals['tp']+totals['fn'] else None,'false_alarm_harmless_missing':totals['fp']/(totals['fp']+totals['tn']) if totals['fp']+totals['tn'] else None,'exact_rate':totals['exact']/len(vv) if vv else None})
    write(out/'report_detector_summary.csv',ds)
    valid_detector_ids={d['job_id'] for d in detector if d['method'] not in ['Checklist','Rule-topic'] and d['valid']}
    matched=[]
    for method in dict.fromkeys(d['method'] for d in detector):
        vv=[d for d in detector if d['method']==method and d['job_id'] in valid_detector_ids and d['valid']]
        totals={k:sum(d[k] for d in vv) for k in ['tp','fn','fp','tn','present_flags','exact']}
        matched.append({'method':method,'matched_valid_jobs':len(vv),**totals,'recall':totals['tp']/(totals['tp']+totals['fn']) if totals['tp']+totals['fn'] else None,'false_alarm_harmless_missing':totals['fp']/(totals['fp']+totals['tn']) if totals['fp']+totals['tn'] else None,'exact_rate':totals['exact']/len(vv) if vv else None})
    write(out/'report_detector_matched_valid.csv',matched)
    selection=[]
    from study import coverage
    for b in briefs.values():
        c=cases[b['case']];cov=[coverage(c,ctx,b['included']) for ctx in c['contexts']]
        selection.append({'case':b['case'],'condition':b['condition'],'writer_replicate':b['writer_replicate'],'included':b['included'],'omitted':[f['id'] for f in c['facts'] if f['id'] not in b['included']],'imbalance':cov[0]['selection_imbalance'],'critical_sensitive':cov[0]['critical_missing'],'critical_comparison':cov[1]['critical_missing'],'warranted_sensitive':cov[0]['warranted_actions'],'warranted_comparison':cov[1]['warranted_actions']})
    write(out/'report_selection.csv',selection)
    usage=collections.Counter()
    for a in attempts:
        for k,v in (a.get('usage') or {}).items():
            if isinstance(v,(int,float)):usage[k]+=v
    usage_rows=[]
    all_jobs={j['id']:j for j in writers+jobs}
    from study import parse_output
    response_models=collections.defaultdict(set)
    for attempt in attempts:
        if attempt['job_id'] in all_jobs and attempt['status']=='ok':
            job=all_jobs[attempt['job_id']]
            assert parse_output(job,attempt['raw_text'])==attempt['parsed']
            response_models[job['route']['name']].add((attempt.get('provider_response') or {}).get('model','not_reported'))
    for model,role in sorted({(j['route']['name'],j['role']) for j in all_jobs.values()}):
        aa=[x for x in attempts if x['job_id'] in all_jobs and all_jobs[x['job_id']]['route']['name']==model and all_jobs[x['job_id']]['role']==role]
        usage_rows.append({'model':model,'role':role,'attempts':len(aa),'unknown_usage':sum(x.get('usage_unknown',True) for x in aa),**{key:sum((x.get('usage') or {}).get(key,0) or 0 for x in aa) for key in ['prompt_tokens','completion_tokens','total_tokens']}})
    write(out/'report_usage.csv',usage_rows)
    selection_summary=[]
    for condition in dict.fromkeys(b['condition'] for b in briefs.values()):
        bb=[b for b in briefs.values() if b['condition']==condition];ss=[r for r in selection if r['condition']==condition]
        selection_summary.append({'condition':condition,'packets':len(bb),'distinct_texts':len({b['text'] for b in bb}),'zero_imbalance':sum(r['imbalance']==0 for r in ss),'critical_sensitive':sum(bool(r['critical_sensitive']) for r in ss),'critical_comparison':sum(bool(r['critical_comparison']) for r in ss),'unresolved_reference_sensitive':sum(not r['warranted_sensitive'] for r in ss),'unresolved_reference_comparison':sum(not r['warranted_comparison'] for r in ss)})
    write(out/'report_selection_summary.csv',selection_summary)
    for j in writers:
        payload=json.loads(j['user'])
        assert not any(k in payload for k in ['recipient','context','alternative_domains','answer_key'])
        assert all(set(f)=={'id','text'} for f in payload['facts'])
    for j in jobs:
        payload=json.loads(j['user']);assert payload['briefing']==briefs[j['metadata']['brief']]['text']
        if j['role']=='receiver':assert 'facts' not in payload and 'alternative_domains' not in payload
    reservations=read_lines(run/'reservations.jsonl')
    audit={'run_created_utc':load(run/'manifest.json')['created_utc'],'planned_writer_jobs':len(writers),'writer_attempts':sum(len(byjob[j['id']]) for j in writers),'evaluation_jobs':len(jobs),'evaluation_records':sum(len(byjob[j['id']]) for j in jobs),'evaluation_statuses':dict(collections.Counter(row['status'] for row in episodes)),'missing_jobs':[j['id'] for j in jobs if not byjob[j['id']]],'duplicate_evaluation_attempts':[j['id'] for j in jobs if len(byjob[j['id']])>1],'independently_recomputed_receiver_score_mismatches':mismatch,'known_reported_usage':dict(usage),'usage_unknown_attempts':sum(a.get('usage_unknown',True) for a in attempts),'billing':'Reported tokens exclude unknown usage; reservation estimates are not verified invoices.','review':'Automated recomputation, not independent human review.'}
    audit.update(reservations=len(reservations),reserved_usd=sum(r.get('usd_cap',0) for r in reservations),unique_briefing_ids=len(briefs),distinct_briefing_texts=len({b['text'] for b in briefs.values()}),sender_blindness_and_shared_briefings_checked=True,raw_successes_reparsed=True,provider_response_model_labels={k:sorted(v) for k,v in response_models.items()},collection_state=state['status'])
    save(out/'report_audit.json',audit)
    print(json.dumps({k:v for k,v in audit.items() if k!='missing_jobs'},indent=2))

if __name__=='__main__':main()
