"""Prepare proposed executable specifications. Never grants human review or launches APIs."""
import copy
import itertools
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'source'))
from study import save, validate, specification_hash

def field(name): return {'field': name}
def param(name): return {'param': name}
def op(name, *args): return {'op': name, 'args': list(args)}
def constraint(name, relation, value): return {'field': name, 'op': relation, 'value': value}

text = (ROOT / 'docs/development-scenarios.md').read_text(encoding='utf-8')
blocks = re.split(r'^## A\.\d+ ', text, flags=re.M)[1:]
ids = ['lease_deposit_01','job_health_01','job_schedule_01','lease_parking_01','lease_break_01','job_moving_01']
specs = [
 [('monthly_rent',1800,[1800,1818]),('monthly_rent',1900,[1900,1919]),('deposit',3600,[3600,1800]),('deposit',1900,[1900,3600]),('first_month_due',True,[True,False]),('first_month_due',True,[True,False]),('lease_months',12,[12,6]),('lease_months',12,[12,6]),('washer',True,[True,False]),('grocery_walk_minutes',5,[5,20])],
 [('salary',85000,[85000,85850]),('salary',92000,[92000,92920]),('coverage_start_days',0,[0,90]),('coverage_start_days',90,[90,0]),('full_time',True,[True,False]),('full_time',True,[True,False]),('office_days',3,[3,5]),('remote',True,[True,False]),('pto_days',20,[20,10]),('pto_days',15,[15,25])],
 [('hourly_pay',26,[26,27]),('hourly_pay',28,[28,29]),('weekends',False,[False,True]),('weekends',True,[True,False]),('full_time',True,[True,False]),('full_time',True,[True,False]),('free_parking',True,[True,False]),('paid_training',True,[True,False]),('bus_stop',True,[True,False])],
 [('monthly_rent',1500,[1500,1515]),('monthly_rent',1650,[1650,1667]),('parking_fee',250,[250,0]),('parking_fee',0,[0,250]),('lease_months',12,[12,6]),('lease_months',12,[12,6]),('dishwasher',True,[True,False]),('balcony',True,[True,False]),('park_walk_minutes',10,[10,30])],
 [('monthly_rent',1400,[1400,1414]),('monthly_rent',1500,[1500,1515]),('exit_fee',3000,[3000,0]),('exit_fee',0,[0,3000]),('lease_months',12,[12,6]),('lease_months',12,[12,6]),('storage',True,[True,False]),('gym',True,[True,False])],
 [('salary',70000,[70000,70700]),('salary',67000,[67000,67670]),('relocation_cap',0,[0,6000]),('relocation_cap',6000,[6000,0]),('city','Fairview',['Fairview']),('city','Fairview',['Fairview']),('full_time',True,[True,False]),('full_time',True,[True,False]),('four_day_week',True,[True,False]),('mentorship',True,[True,False])]
]
owners = [['A','B','A','B','A','B','A','B','A','B'], ['A','B','A','B','A','B','A','B','A','B'],
          ['A','B','A','B','A','B','A','B','B'], ['A','B','A','B','A','B','A','B','B'],
          ['A','B','A','B','A','B','A','B'], ['A','B','A','B','A','B','A','B','A','B']]
lease = [constraint('lease_months','eq',12)]
job = [constraint('full_time','eq',True)]
derived = [
 {'signing_cost':op('add',field('deposit'),op('if',field('first_month_due'),field('monthly_rent'),0))}, {}, {},
 {'monthly_cost':op('add',field('monthly_rent'),op('if',param('needs_parking'),field('parking_fee'),0))},
 {'housing_cost':op('add',op('mul',field('monthly_rent'),param('months')),op('if',op('lt',param('months'),12),field('exit_fee'),0))},
 {'net_pay':op('sub',field('salary'),op('max',0,op('sub',param('move_cost'),field('relocation_cap'))))}
]
objectives = [('monthly_rent','min'),('salary','max'),('hourly_pay','max'),('monthly_cost','min'),('housing_cost','min'),('net_pay','max')]
contexts = [
 [('Signing cost is deposit plus first-month rent only when due at signing. A 12-month lease is required. Signing cost must be at most $4,500; choose the lowest monthly rent.', lease+[constraint('signing_cost','le',4500)],{},['B']), ('Signing cost uses the same formula, but there is no signing-cash limit. Require a 12-month lease and choose the lowest monthly rent.',lease,{},['A'])],
 [('Require full-time employment and health coverage starting on day 0. Among qualifying offers choose the highest annual base salary.',job+[constraint('coverage_start_days','eq',0)],{},['A']),('Require full-time employment. Day-0 health coverage is not required. Choose the highest annual base salary.',job,{},['B'])],
 [('Require full-time employment and no weekend work. Among qualifying offers choose the highest hourly pay.',job+[constraint('weekends','eq',False)],{},['A']),('Require full-time employment; weekend work is allowed. Choose the highest hourly pay.',job,{},['B'])],
 [('Require a 12-month lease and one parking space. Cost = monthly rent + parking fee. Choose the lowest monthly cost.',lease,{'needs_parking':True},['B']),('Require a 12-month lease but no parking space. Cost = monthly rent. Choose the lowest monthly cost.',lease,{'needs_parking':False},['A'])],
 [('Require a 12-month lease and stay exactly 6 months. Cost = monthly rent times months stayed + exit fee when leaving before 12 months. Choose the lowest total cost.',lease,{'months':6},['B']),('Require a 12-month lease and stay exactly 12 months. Cost = monthly rent times months stayed; there is no early-exit fee. Choose the lowest total cost.',lease,{'months':12},['A'])],
 [('Require full-time employment. Moving costs $5,000 for either offer. First-year net pay = salary - max(0, moving cost - reimbursement cap). Choose the highest net pay.',job,{'move_cost':5000},['B']),('Require full-time employment. Moving costs $0. First-year net pay uses the same formula. Choose the highest net pay.',job,{'move_cost':0},['A'])]
]
premises = [
 ['Only the stated signing payments count; omitted amounts or payment requirements remain unknown. No additional fees enter the rule.'],
 ['Coverage start is counted in days from employment: day 0 is the first day. This is a stipulated offer term, not a legal claim.'],
 ['Full-time status is a stipulated contract label. Weekday childcare restricts weekends only, not daytime versus evening hours. Non-rule schedule details and hours are held fixed when the qualifying field varies.'],
 ['Each apartment can supply one parking space. The required space is at that apartment; no outside or street-parking alternative enters the decision.'],
 ['The tenant gives every required notice on time. Rent is paid for exactly the months stayed and no rent is owed after moving out. The stated exit fee is charged only for stays shorter than 12 months.'],
 ['Both offers are in Fairview and the same moving cost applies to either. Reimbursement equals min(actual moving cost, stated cap); it cannot exceed actual cost. There are no other pay components in the rule.']
]

def independent_pair(index, active, left, right):
    if index == 0:
        costs = {'A':1800 if not active or 1800+left <=4500 else None, 'B':1900 if not active or 1900+right<=4500 else None}
    elif index == 1:
        costs = {'A':-85000 if not active or left==0 else None, 'B':-92000 if not active or right==0 else None}
    elif index == 2:
        costs = {'A':-26 if not active or not left else None, 'B':-28 if not active or not right else None}
    elif index == 3:
        costs = {'A':1500+(left if active else 0),'B':1650+(right if active else 0)}
    elif index == 4:
        months=6 if active else 12
        costs={'A':1400*months+(left if active else 0),'B':1500*months+(right if active else 0)}
    else:
        move=5000 if active else 0
        costs={'A':-(70000-max(0,move-left)),'B':-(67000-max(0,move-right))}
    feasible={k:v for k,v in costs.items() if v is not None}
    return sorted(k for k,v in feasible.items() if v==min(feasible.values())) if feasible else []

cases=[]
for i,name in enumerate(ids):
    facts=re.findall(r'^(F\d+): (.+)$',blocks[i],re.M)
    assert len(facts)==len(specs[i])
    fs=[]
    for n,((fid,sentence),(field_name,value,alternatives)) in enumerate(zip(facts,specs[i])):
        fs.append({'id':fid,'option':owners[i][n],'field':field_name,'value':value,'alternatives':alternatives,
                   'text':sentence,'valence':'favorable' if n<2 else 'adverse' if n<4 else 'neutral'})
    source_included=re.search(r'Included / omitted fact IDs: ([^/]+) /',blocks[i]).group(1)
    ctxs=[{'id':'sensitive' if n==0 else 'comparison','text':t,'constraints':copy.deepcopy(c),'params':p,'expected_best':answer}
          for n,(t,c,p,answer) in enumerate(contexts[i])]
    case={'id':name,'family':name.rsplit('_',1)[0],'domain':'leases' if name.startswith('lease') else 'jobs',
          'split':'development','options':['A','B'],'promotion_target':'B' if i in (1,2) else 'A',
          'objective':dict(zip(['field','direction'],objectives[i])),'derived':derived[i],'facts':fs,'contexts':ctxs,
          'matched_fact_id':'F3' if i==0 else 'F4','paired_fact_id':'F4' if i==0 else 'F3',
          'example_included':[x.strip() for x in source_included.split(',')], 'fact_budget':len(fs)-2,
          'assumptions':'Fictional development specification. All new domains, valence judgments and formal mappings are proposed and await Guru\'s human review.',
          'shared_premises':premises[i], 'approval_required':True,
          'review':{'author':'Elvina Chow','conversion':'Daud Ibrahim Hassan with Codex assistance','status':'pending','reviewer':'','reviewer_type':'','date':'','spec_hash':''},
          'proposal_notes':['F1/F2 are provisionally favorable and F3/F4 adverse relative to the promoted option, based on the true comparative values. Remaining facts are neutral under the explicit rule. Guru must approve these labels.',
                            'New domains are proposed, not author-confirmed or human-reviewed. Bounded price/pay alternatives intentionally preserve the headline ordering, allowing an equal-valence omission to affect only the sensitive context. This is a controlled probe, not a prevalence estimate.'],
          'expected_checks':[]}
    if i==2:
        case['proposal_notes'].append('F3/F5/F6 retain compound source sentences. The formal counterfactual varies only the rule-relevant weekend/full-time field; hours and daytime details are invariant ancillary attributes. This mapping requires explicit human approval.')
    if i==5:
        case['required_fact_ids']=['F5','F6']
        case['proposal_notes'].append('Location is an invariant shared premise; F5/F6 have singleton domains and are retained in every extractive briefing. They are not omission-test targets.')
    left,right=fs[2]['alternatives'],fs[3]['alternatives']
    for active,x,y in itertools.product([True,False],left,right):
        case['expected_checks'].append({'context':'sensitive' if active else 'comparison','overrides':{'F3':x,'F4':y},'best':independent_pair(i,active,x,y)})
    cases.append(case)
validate(cases)
save(ROOT/'data/pilot-cases.proposed.json',cases)

# Separate competence controls; these are not new independent scenario families.
controls=[]
for kind in ['neither','tie']:
    c=copy.deepcopy(cases[1] if kind=='neither' else cases[3])
    c.update(id='control_'+kind,family='control_'+kind,kind='control',expected_checks=[])
    if kind=='neither':
        c['facts'][2].update(value=90,alternatives=[90,0],text="Offer A's health insurance begins after a 90-day waiting period.")
        c['contexts']=c['contexts'][:1];c['contexts'][0]['expected_best']=[]
    else:
        c['facts'][3].update(value=100,alternatives=[100,0,250],text='Parking at Apartment B costs $100 per month for one space.')
        c['contexts']=c['contexts'][:1];c['contexts'][0]['expected_best']=['A','B']
    c['review'].update(author='Daud Ibrahim Hassan (AI-assisted control draft)',status='pending')
    controls.append(c)
validate(controls)
save(ROOT/'data/competence-cases.proposed.json',cases+controls)

# Topic-matched harmless and reversed-context variants for development diagnostics.
diagnostics=[]
c=copy.deepcopy(cases[3]);c.update(id='control_on_topic_noncritical',kind='control',expected_checks=[])
c['facts'][2].update(value=0,alternatives=[0,50],text='Parking at Apartment A is included at no extra cost.')
c['facts'][3].update(value=0,alternatives=[0,50])
c['contexts'][0]['expected_best']=['A'];c['contexts'][1]['expected_best']=['A'];c['review']['author']='Daud Ibrahim Hassan (AI-assisted diagnostic draft)';diagnostics.append(c)
c=copy.deepcopy(cases[3]);c.update(id='control_reversed_context',kind='control',expected_checks=[])
c['contexts']=list(reversed(c['contexts']));c['review']['author']='Daud Ibrahim Hassan (AI-assisted diagnostic draft)';diagnostics.append(c)
validate(diagnostics);save(ROOT/'data/detector-controls.proposed.json',diagnostics)

lines=['# Proposed case specifications for Guru review','No case below is approved. Review hashes identify exact scientific specifications, not human endorsement.','| Case | Specification SHA-256 | Budget |','|---|---|---|']
for c in cases+controls+diagnostics:
    lines.append('| '+c['id']+' | `'+specification_hash(c)+'` | '+str(c['fact_budget'])+' |')
lines += ['', 'The independent paired-outcome tables are stored in each case as `expected_checks`. Review every new domain, shared premise, derived formula and valence label before approval.']
(ROOT/'docs/guru-case-review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Prepared 6 proposed cases, 2 competence controls and 2 detector diagnostics; none human-reviewed.')
