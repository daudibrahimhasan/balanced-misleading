"""Recover a stopped evaluation process without replacing completed or uncertain attempts."""
import sys,datetime as dt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'source'))
import pipeline
from study import load,save,read_lines,append
s=load(ROOT/'approval/current-live-run.json');run=Path(s['main_run']);pipeline.frozen(run)
attempted={a['job_id'] for a in read_lines(run/'attempts.jsonl')}
pending=[r for r in read_lines(run/'reservations.jsonl') if r['job_id'] not in attempted]
jobs={j['id']:j for j in read_lines(run/'evaluation_jobs.jsonl')}
for r in pending:
 append(run/'attempts.jsonl',{'job_id':r['job_id'],'model':jobs[r['job_id']]['route']['model'],'origin':'live','status':'interrupted','usage':None,'usage_unknown':True,'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'note':'Prior worker exited. Reserved request may have reached provider; retained as unknown and not automatically retried.'})
lock=run/'.execute.lock'
if lock.exists():lock.unlink()
append(run/'recovery-events.jsonl',{'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'reason':'No live collection process remained; saved state was stale','interrupted_reservations':len(pending),'policy':'Resume only never-reserved jobs; no duplicate successful or uncertain calls.'})
s.update(status='evaluations_running');save(ROOT/'approval/current-live-run.json',s)
print(pipeline.execute(run,run/'evaluation_jobs.jsonl'),flush=True)
print(pipeline.analyze(run),flush=True)
s.update(status='collection_finished_review_outputs');save(ROOT/'approval/current-live-run.json',s)
