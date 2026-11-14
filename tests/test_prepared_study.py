import copy
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'source'))
import pipeline
from study import load, save, choose, validate, coverage, public_context, parse_output, make_job, read_lines, specification_hash


class PreparedStudyTests(unittest.TestCase):
    def setUp(self):
        self.cases=load(ROOT/'data/pilot-cases.proposed.json')
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name)

    def test_all_six_formal_rules_and_independent_pair_tables(self):
        self.assertEqual(len(validate(self.cases)),6)
        self.assertEqual(sum(len(c['expected_checks']) for c in self.cases),48)
        for c in self.cases:
            self.assertEqual(choose(c,c['contexts'][0])['best'],c['contexts'][0]['expected_best'])
            self.assertEqual(choose(c,c['contexts'][1])['best'],c['contexts'][1]['expected_best'])
            self.assertTrue(public_context(c,c['contexts'][0])['shared_premises'])
            self.assertEqual(c['fact_budget'],len(c['facts'])-2)
        bad=copy.deepcopy(self.cases);bad[0]['expected_checks'][0]['best']=['A']
        with self.assertRaises(ValueError):validate(bad)

    def test_balanced_positive_controls_preserve_comparison_context(self):
        for c in self.cases:
            included=[f['id'] for f in c['facts'] if f['id'] not in {c['matched_fact_id'],'F1'}]
            sensitive=coverage(c,c['contexts'][0],included)
            comparison=coverage(c,c['contexts'][1],included)
            self.assertEqual(sensitive['selection_imbalance'],0,c['id'])
            self.assertEqual(sensitive['warranted_actions'],[],c['id'])
            self.assertEqual(comparison['warranted_actions'],c['contexts'][1]['expected_best'],c['id'])

    def test_derived_objectives_thresholds_and_substitution_errors(self):
        for index,overrides in [(3,{'F4':100}),(3,{'F3':150}),(4,{'F4':2400}),(4,{'F3':600}),(5,{'F4':3000}),(5,{'F3':2000})]:
            c=self.cases[index]
            self.assertEqual(choose(c,c['contexts'][0],overrides)['best'],['A','B'])
        for index,base in [(3,'monthly_rent'),(4,'monthly_rent'),(5,'salary')]:
            c=copy.deepcopy(self.cases[index]);c['objective']['field']=base
            self.assertEqual(choose(c,c['contexts'][0])['best'],['A'])
            self.assertEqual(choose(self.cases[index],c['contexts'][0])['best'],['B'])
        c=self.cases[4]
        self.assertEqual(choose(c,c['contexts'][0])['objective'],9000)
        self.assertEqual(choose(c,c['contexts'][1])['objective'],16800)

    def test_neither_tie_controls_and_receiver_actions(self):
        cases=load(ROOT/'data/competence-cases.proposed.json');validate(cases)
        neither,tie=cases[-2:]
        self.assertEqual(choose(neither,neither['contexts'][0])['best'],[])
        self.assertEqual(choose(tie,tie['contexts'][0])['best'],['A','B'])
        config=load(ROOT/'config/competence.proposed.json')
        job=make_job('receiver',{'recipient':public_context(neither,neither['contexts'][0])},{},config)
        self.assertEqual(parse_output(job,'{"action":"neither"}')['action'],'neither')
        self.assertIn('Display order is fixed',make_job('writer',{}, {},config)['system'])

    def test_frozen_balance_run_cannot_fall_back_to_missing_valence(self):
        config=load(ROOT/'config/exploratory.proposed.json')
        case=copy.deepcopy(self.cases[0]);case['facts'][0]['valence']=None
        data,cfg=self.folder/'data.json',self.folder/'config.json';save(data,[case]);save(cfg,config)
        with self.assertRaisesRegex(ValueError,'valence'):
            pipeline.plan(data,cfg,self.folder/'run')

    def test_approval_and_route_gate_prevents_network(self):
        cfg=self.folder/'config.json';config=load(ROOT/'config/competence.proposed.json')
        config['status']='approved_pilot';save(cfg,config)
        run=self.folder/'run';pipeline.competence(ROOT/'data/competence-cases.proposed.json',cfg,run)
        with patch('pipeline.request_model') as request:
            with self.assertRaisesRegex(ValueError,'Waiting for Guru'):
                pipeline.execute(run,run/'evaluation_jobs.jsonl')
            request.assert_not_called()
        c=copy.deepcopy(self.cases[0]);before=specification_hash(c);c['facts'][0]['alternatives'].append(2100)
        self.assertNotEqual(before,specification_hash(c))

    def test_competence_plan_exact_42_jobs_and_full_evidence_scoring(self):
        run=self.folder/'run';pipeline.competence(ROOT/'data/competence-cases.proposed.json',ROOT/'config/competence.proposed.json',run)
        jobs=read_lines(run/'evaluation_jobs.jsonl');self.assertEqual(len(jobs),42)
        self.assertEqual(read_lines(run/'writer_jobs.jsonl'),[])
        cases=load(run/'cases.json');answers=[]
        for j in jobs:
            c=next(c for c in cases if c['id']==j['metadata']['case'])
            ctx=next(x for x in c['contexts'] if x['id']==j['metadata']['context'])
            best=choose(c,ctx)['best'];action=best[0] if best else 'neither'
            answers.append(json.dumps({'job_id':j['id'],'raw_text':json.dumps({'action':action})}))
        path=self.folder/'answers.jsonl';path.write_text('\n'.join(answers),encoding='utf-8')
        pipeline.import_answers(run,run/'evaluation_jobs.jsonl',path);pipeline.analyze(run)
        with (run/'analysis/episodes.csv').open(encoding='utf-8') as stream:rows=list(csv.DictReader(stream))
        self.assertTrue(all(r['optimal']=='1' and r['incorrect_commitment']=='0' for r in rows))
        import importlib.util
        spec=importlib.util.spec_from_file_location('competence_report',ROOT/'scripts/competence_report.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        report=module.report(run,self.folder/'screen.json')
        self.assertEqual(report['status'],'not_passed')  # Imported oracle fixtures are not model competence.
        self.assertFalse(report['human_accepted'])

    def test_detector_inputs_writer_repeats_and_required_facts(self):
        c=self.cases[-1];config=load(ROOT/'config/exploratory.proposed.json')
        data=self.folder/'data.json';save(data,[c]);run=self.folder/'run'
        pipeline.plan(data,ROOT/'config/exploratory.proposed.json',run)
        writers=read_lines(run/'writer_jobs.jsonl');self.assertEqual(len(writers),9)
        self.assertEqual({j['metadata']['writer_replicate'] for j in writers},{0,1,2})
        records=[]
        for j in writers:
            self.assertNotIn('recipient',json.loads(j['user']))
            records.append(json.dumps({'job_id':j['id'],'raw_text':json.dumps({'included_fact_ids':c['example_included']})}))
        answers=self.folder/'answers.jsonl';answers.write_text('\n'.join(records),encoding='utf-8')
        pipeline.import_answers(run,run/'writer_jobs.jsonl',answers);pipeline.prepare(run)
        for j in read_lines(run/'evaluation_jobs.jsonl'):
            payload=json.loads(j['user'])
            if j['role']=='detector':
                self.assertEqual(len(payload['alternative_domains']),len(c['facts']))
                self.assertNotIn('matched_fact_id',payload)
            else:self.assertNotIn('alternative_domains',payload)
        for b in load(run/'briefings.json'):
            self.assertTrue({'F5','F6'} <= set(b['included']))
        with self.assertRaises(ValueError):
            parse_output(writers[0],json.dumps({'included_fact_ids':['F1','F2','F3','F4','F7','F8','F9','F10']}))

    def test_omitted_only_false_alarm_and_topic_matched_controls(self):
        metrics=pipeline.detector_metrics(['F1','F3'],['F3'],['F3','F4'])
        self.assertEqual(metrics['tn'],1)
        self.assertEqual(metrics['flagged_present_n'],1)
        self.assertEqual(metrics['false_alarm_rate_harmless_missing'],0)
        c=load(ROOT/'data/detector-controls.proposed.json')[0];ctx=c['contexts'][0]
        self.assertFalse(coverage(c,ctx,c['example_included'])['critical_missing'])
        topic=pipeline.topic_fields(c,ctx)
        self.assertIn('parking_fee',topic)  # Topic overlap does not establish criticality.

    def test_provider_output_limit_field_is_explicit_and_checked(self):
        config=load(ROOT/'config/competence.proposed.json')
        config['roles']['receiver'].update(endpoint='https://invalid.example/v1/chat/completions',output_limit_field='max_tokens')
        job=make_job('receiver',{}, {},config)
        with patch('pipeline.urllib.request.urlopen') as network:
            network.return_value.__enter__.return_value.read.return_value=json.dumps({'choices':[{'message':{'content':'{"action":"A"}'},'finish_reason':'stop'}]}).encode()
            pipeline.request_model(job,'FAKE_UNIT_TEST_KEY',1)
            payload=json.loads(network.call_args.args[0].data)
            self.assertEqual(payload['max_tokens'],config['roles']['receiver']['max_output_tokens'])
            self.assertNotIn('max_completion_tokens',payload)
        job['route']['output_limit_field']='unsupported'
        with self.assertRaises(ValueError):pipeline.request_model(job,'FAKE_UNIT_TEST_KEY',1)


if __name__=='__main__':unittest.main()
