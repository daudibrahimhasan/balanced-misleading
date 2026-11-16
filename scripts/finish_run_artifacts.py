"""Wait for the active collection, then create analysis/figure review artifacts locally."""
import sys,time,datetime as dt,collections,json,csv,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'source'))
from study import load,read_lines,save
state=load(ROOT/'approval/current-live-run.json');run=Path(state['main_run'])
save(run/'postprocess-status.json',{'status':'waiting_for_collection','main_run':str(run),'scope':'Local analysis and figure artifacts only; manuscript interpretation and submission are not automated.'})
while True:
    current=load(ROOT/'approval/current-live-run.json')
    if current['main_run']!=str(run):
        save(run/'postprocess-status.json',{'status':'stopped_run_changed'});sys.exit(1)
    if current['status']=='collection_finished_review_outputs':break
    if current['status'] not in ['evaluations_running','writers_running','writer_retry_running']:
        save(run/'postprocess-status.json',{'status':'blocked','collection_status':current['status']});sys.exit(1)
    time.sleep(30)
try:
    import pipeline
    pipeline.frozen(run)
    attempts=read_lines(run/'attempts.jsonl');jobs=read_lines(run/'evaluation_jobs.jsonl');ids={j['id'] for j in jobs}
    ev=[a for a in attempts if a['job_id'] in ids];counts=collections.Counter(a['job_id'] for a in ev)
    missing=sorted(ids-set(counts));duplicates={k:v for k,v in counts.items() if v>1}
    audit={'planned_evaluations':len(jobs),'evaluation_attempts':len(ev),'missing_job_ids':missing,'repeated_evaluation_attempts':duplicates,'statuses':dict(collections.Counter(a['status'] for a in ev)),'unknown_usage':sum(a.get('usage_unknown',True) for a in attempts),'writer_attempts':len(attempts)-len(ev),'claim_scope':'Development experiment; retain failed writer attempt, missing outcomes and all planned denominators.'}
    save(run/'analysis/completion-review.json',audit)
    from figures import figures
    figure_path=str(figures(run))
    lines=['# Collection ready for review','',f"Evaluations planned: {len(jobs)}; attempted: {len(ev)}; missing: {len(missing)}.",f"Statuses: {audit['statuses']}.",'','Review analysis/summary.csv, paired_family_contrasts.csv, detector outcomes and completion-review.json before interpreting effects.','',f'Figures: {figure_path}','', 'The paper, captions, limitations, abstract and conclusion still require interpretation against these audited outputs. No external submission or teammate message was sent.']
    (run/'analysis/REVIEW_NEXT.md').write_text('\n'.join(lines),encoding='utf-8')
    save(run/'postprocess-status.json',{'status':'artifacts_ready_for_interpretation','figure_path':figure_path,'main_run':str(run)})
except Exception as e:
    save(run/'postprocess-status.json',{'status':'failed','error_type':type(e).__name__,'error':str(e)[:300]});raise
