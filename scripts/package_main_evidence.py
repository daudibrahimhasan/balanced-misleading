"""Copy finished immutable evidence and audit it against configured secret values."""
import hashlib,json,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source'))
from study import load,save
import pipeline
state=load(ROOT/'approval/current-live-run.json');assert state['status']=='collection_finished_review_outputs'
run=Path(state['main_run']);pipeline.frozen(run)
audit=load(run/'analysis/report_audit.json');assert not audit['missing_jobs'] and not audit['duplicate_evaluation_attempts']
target=ROOT/'data/main-v6';target.mkdir(parents=True,exist_ok=True)
files=['attempts.jsonl','briefings.json','cases.json','config.json','continuation.json','evaluation_jobs.jsonl','manifest.json','random_subset_reference.csv','recovery-events.jsonl','reservations.jsonl','stage.json','writer_jobs.jsonl']
for name in files:shutil.copy2(run/name,target/name)
shutil.copytree(run/'source_snapshot',target/'source_snapshot',dirs_exist_ok=True)
shutil.copytree(run/'analysis',target/'analysis',dirs_exist_ok=True,ignore=shutil.ignore_patterns('REVIEW_NEXT.md'))
original=Path(state['previous_main_run']);(target/'prior-writer-stage').mkdir(exist_ok=True)
for name in ['manifest.json','config.json','attempts.jsonl','reservations.jsonl','writer_jobs.jsonl']:
    shutil.copy2(original/name,target/'prior-writer-stage'/name)
from dotenv import dotenv_values
secret_values=[]
for k,v in dotenv_values(r'D:\Apart Sprint\.env').items():
    if v and len(v)>=12 and any(s in k.lower() for s in ['key','token','secret','password','api']) and not v.startswith('http'):secret_values.append(v)
flagged=[]
for path in target.rglob('*'):
    if path.is_file():
        text=path.read_text(encoding='utf-8',errors='ignore')
        if any(v in text for v in secret_values):flagged.append(str(path.relative_to(target)))
assert not flagged,{'configured_secret_matches':flagged}
(target/'README.md').write_text('''# Main development run evidence

Six fictional development families; not held-out validation. The frozen run is
`main-v6-writer-amendment-20261115T214437Z`.

The continuation carries the original writer-stage records forward. One invalid
writer response was explicitly retried with the same prompt/settings; both remain
in `attempts.jsonl`. `prior-writer-stage/` preserves the pre-amendment journals and
configuration. Reserved evaluation requests interrupted by worker exits were
recorded as unknown and were not resent; recovery resumed
only never-reserved jobs. `recovery-events.jsonl` records that event.

The manifest's `kind: planned_not_executed` is the immutable planning label, not a
final collection status. See the raw live attempts and `analysis/report_audit.json`
for completed counts, failures, usage and checks. Source/config/case/job hashes are
retained exactly. Absolute original workspace paths are historical provenance.
Credential environment-variable names and public provider endpoints are retained;
secret values and authorization headers are excluded. The package was checked
against configured secret values before publication.

`analysis/report_outcomes.csv` includes every planned receiver job and its unresolved
count. `report_detector_matched_valid.csv` compares detector/baselines on the same
valid jobs. Intervals in `paired_family_contrasts.csv` are descriptive equal-family
bootstrap intervals on complete packets. Repeated calls do not create new families.

Automated independent recomputation is not independent human review. No final
coauthor approval or submission is claimed. Main report: `../../paper/` and the
canonical Google Doc linked in the repository README.
''',encoding='utf-8')
hashes={str(p.relative_to(target)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(target.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'}
save(target/'SHA256SUMS.json',hashes)
print(json.dumps({'evidence':str(target),'files':len(hashes),'configured_secret_matches':len(flagged)}))
