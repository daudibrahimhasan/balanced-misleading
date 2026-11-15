import copy,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source'))
import pipeline
from study import load,save,read_lines,make_job,parse_output

class PacingTests(unittest.TestCase):
    def test_justification_first_does_not_override_submitted_action(self):
        cfg=load(ROOT/'config/competence.proposed.json')
        payload={'recipient':{'options':['A','B']}}
        job=make_job('receiver',payload,{},cfg)
        self.assertLess(job['system'].index('"reason"'),job['system'].index('"action"'))
        self.assertEqual(parse_output(job,'{"reason":"B is the only qualifying option","action":"A"}')['action'],'A')
    def config(self):
        cfg=load(ROOT/'config/competence.proposed.json')
        route=copy.deepcopy(cfg['role_routes']['receiver'][0]);route.update(endpoint='https://offline.invalid/v1/chat/completions',key_env='PACING_TEST_KEY',max_request_usd=.01,max_concurrent_requests=1,min_interval_seconds=6)
        cfg.update(require_guru_go=False,status='approved_pilot',max_concurrency=1,role_routes={'receiver':[route]})
        cfg['guards']['max_requests']=3
        return cfg

    def test_spacing_preserves_reservations_and_first_attempts(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);save(p/'cfg.json',self.config());pipeline.competence(ROOT/'data/competence-cases.proposed.json',p/'cfg.json',p/'run')
            clock=[100.0];starts=[]
            def sleep(seconds):clock[0]+=seconds
            def request(*args):
                starts.append(clock[0]);clock[0]+=1
                return '{"action":"A"}',{},'stop',{'id':'offline-test'}
            with patch.dict(os.environ,{'PACING_TEST_KEY':'not-a-key'}),patch.object(pipeline.time,'monotonic',lambda:clock[0]),patch.object(pipeline.time,'sleep',sleep),patch.object(pipeline,'request_model',request):
                result=pipeline.execute(p/'run',p/'run/evaluation_jobs.jsonl')
            self.assertEqual(starts,[100,106,112]);self.assertEqual(result['requests_sent'],3)
            self.assertEqual(len(read_lines(p/'run/reservations.jsonl')),3)
            self.assertEqual(len(read_lines(p/'run/attempts.jsonl')),3)

    def test_paced_route_cannot_allow_parallel_requests(self):
        with tempfile.TemporaryDirectory() as t:
            cfg=self.config();cfg['max_concurrency']=2;cfg['role_routes']['receiver'][0]['max_concurrent_requests']=2
            p=Path(t);save(p/'cfg.json',cfg);pipeline.competence(ROOT/'data/competence-cases.proposed.json',p/'cfg.json',p/'run')
            with patch.dict(os.environ,{'PACING_TEST_KEY':'not-a-key'}),patch.object(pipeline,'request_model') as request:
                with self.assertRaisesRegex(ValueError,'pacing'):
                    pipeline.execute(p/'run',p/'run/evaluation_jobs.jsonl')
                request.assert_not_called()
