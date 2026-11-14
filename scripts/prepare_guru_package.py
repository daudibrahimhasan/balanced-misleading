"""Offline planning only. Configurations and approvals remain blocked pending Guru."""
import copy
import csv
import datetime as dt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'source'))
import pipeline
from study import load, save, choose, specification_hash, digest, possible_choices, warranted_actions

names=['DeepSeek V4.1 Flash','Mistral Large 4','Nemotron 3 Ultra']
models=['deepseek-ai/DeepSeek-V4.1-Flash','mistralai/mistral-large-4-1t-a52b','nvidia/nemotron-3-ultra-550b-a55b']
routes=[{'name':name,'adapter':'openai_chat','endpoint':'','model':model,'key_env':key,'max_output_tokens':1000,
         'max_request_usd':0,'parameters':{}} for name,model,key in zip(names,models,['STUDY_DEEPSEEK_KEY','STUDY_MISTRAL_KEY','STUDY_NEMOTRON_KEY'])]
base={'status':'awaiting_guru','phase':'development','seed':314159,'repeats':1,'writer_repeats':1,
      'roles':{'writer':routes[0],'receiver':routes[1],'detector':routes[2]},
      'role_routes':{'receiver':routes,'detector':[routes[2]]},'require_guru_go':True,
      'guards':{'max_requests':60,'max_seconds':3600,'max_output_tokens_total':60000,'max_reserved_usd':5,'timeout_seconds':60},
      'api_routes_verified':False,
      'notes':'PROPOSED. No launch authorization. Paid endpoints, credential variable bindings and request cost ceilings need verification before freezing. No credentials are stored here.'}
competence=copy.deepcopy(base);competence.update(purpose='competence',approval_file='approval/guru-competence-go.json')
main=copy.deepcopy(base);main.update(purpose='balance_study',writer_repeats=3,repeats=2,enumerate_reference_subsets=True,
    approval_file='approval/guru-exploratory-go.json',require_competence_report='approval/competence-result.json')
main['guards'].update(max_requests=1500,max_seconds=90000,max_output_tokens_total=1500000,max_reserved_usd=25)
main['balance_pass_epsilon']=0
save(ROOT/'config/competence.proposed.json',competence);save(ROOT/'config/exploratory.proposed.json',main)

root=ROOT/'results'/('guru-review-'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
comp=pipeline.competence(ROOT/'data/competence-cases.proposed.json',ROOT/'config/competence.proposed.json',root/'competence')
expl=pipeline.plan(ROOT/'data/pilot-cases.proposed.json',ROOT/'config/exploratory.proposed.json',root/'exploratory')

cases=load(ROOT/'data/pilot-cases.proposed.json')
reference=[]
for c in cases:
    for ctx in c['contexts']:
        for f in c['facts']:
            for v in f['alternatives']:
                r=choose(c,ctx,{f['id']:v})
                reference.append({'case':c['id'],'context':ctx['id'],'varied_fact':f['id'],'value':v,'best':r['best'],'objective':r['objective']})
pipeline.write_csv(ROOT/'docs/guru-reference-table.csv',reference)

for config,folder in [(competence,'competence'),(main,'exploratory')]:
    manifest=load(root/folder/'manifest.json')
    approval_path=ROOT/config['approval_file']
    if approval_path.exists() and load(approval_path).get('approved'):
        raise ValueError('Refusing to overwrite an existing human approval')
    save(approval_path,{'approved':False,'reviewer':'Govardhan Reddy','reviewer_type':'human','date':'',
        'material_digest':manifest['approval_material_digest'],'reviewed_case_hashes':[],
        'evidence':'Pending actual human review and explicit final go. Never set approved on the strength of AI checks.'})

briefs_per_case=3*main['writer_repeats']+main['writer_repeats']+1
receiver_calls=len(cases)*briefs_per_case*2*len(routes)*main['repeats']
detector_calls=len(cases)*briefs_per_case*2*main['repeats']
save(ROOT/'docs/preparation-status.json',{
    'status':'awaiting_guru','live_requests':0,'competence_plan':str(root/'competence'),
    'exploratory_plan':str(root/'exploratory'),'competence_receiver_calls':comp['evaluation_jobs'],
    'exploratory_writer_calls':expl['writer_jobs'],'exploratory_receiver_calls':receiver_calls,
    'exploratory_detector_calls':detector_calls,'exploratory_total_calls':expl['writer_jobs']+receiver_calls+detector_calls,
    'estimated_cost_usd':None,'budget_ceiling_usd':30,
    'blocking_inputs':['Guru human review and final go','Verified paid endpoints and credential bindings','Verified per-request cost ceilings','Competence result before exploratory collection'],
    'case_spec_hashes':{c['id']:specification_hash(c) for c in cases}})
print('Prepared review-only plans:',root)
print('Competence calls:',comp['evaluation_jobs'],'Exploratory calls:',expl['writer_jobs']+receiver_calls+detector_calls)
print('No API requests. Approvals remain false. Endpoints and cost ceilings remain explicitly unset.')
