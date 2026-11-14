import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "source"))
import pipeline
from study import (choose, coverage, critical, digest, load, parse_output, possible_choices,
                   public_facts, read_lines, render, save, validate, warranted_actions)

ROOT = Path(__file__).resolve().parents[1]


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.case = load(ROOT / "data" / "development.json")[0]

    def test_reference_and_missing_unknown(self):
        c = self.case
        validate([c])
        a, b = c["contexts"]
        self.assertEqual(choose(c, a)["best"], ["B"])
        self.assertEqual(choose(c, b)["best"], ["A"])
        self.assertTrue(critical(c, a, "F3"))
        self.assertFalse(critical(c, b, "F3"))
        self.assertEqual(possible_choices(c, a, c["example_included"]), [("A",), ("B",)])
        self.assertEqual(possible_choices(c, b, c["example_included"]), [("A",)])
        self.assertIsNone(coverage(c, a, c["example_included"])["selection_imbalance"])

    def test_bad_keys_duplicate_fields_and_heldout(self):
        for mutation in (lambda c: c["contexts"][0].update(expected_best=["A"]),
                         lambda c: c["facts"].append(copy.deepcopy(c["facts"][0])),
                         lambda c: c["facts"][2].update(alternatives=[False])):
            c = copy.deepcopy(self.case)
            mutation(c)
            with self.assertRaises(ValueError):
                validate([c])
        with self.assertRaises(ValueError):
            validate([self.case], heldout=True)

    def test_ties_and_no_feasible_option(self):
        c = self.case
        self.assertEqual(choose(c, c["contexts"][1], {"F1": 1000})["best"], ["A", "B"])
        self.assertEqual(choose(c, c["contexts"][0], {"F4": False})["best"], [])

    def test_renderer_does_not_leak_labels(self):
        text = render(self.case, ["F1", "F2"])
        self.assertNotIn("F3", text)
        self.assertNotIn("stairs", text)
        with self.assertRaises(ValueError):
            render(self.case, ["F1", "F1"])
        self.assertEqual(render(self.case, ["F2", "F1"]), text)

    def test_common_optimum_under_ties_and_fact_boundaries(self):
        self.assertEqual(warranted_actions([("A",), ("A", "B")]), ["A"])
        self.assertEqual(warranted_actions([("A",), ("B",)]), [])
        self.assertEqual(warranted_actions([(), ()]), ["neither"])
        self.assertEqual(warranted_actions([(), ("A",)]), [])
        self.assertTrue(all(set(f) == {"id", "text"} for f in public_facts(self.case)))
        c = copy.deepcopy(self.case)
        del c["facts"][0]["alternatives"]
        with self.assertRaises(ValueError):
            validate([c])


class FlowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.run = Path(self.temp.name) / "run"
        self.config = load(ROOT / "config" / "pilot.example.json")
        for route in self.config["roles"].values():
            route["model"] = "OFFLINE_FIXTURE"
        path = Path(self.temp.name) / "config.json"
        save(path, self.config)
        pipeline.plan(ROOT / "data" / "development.json", path, self.run)

    def import_writer(self):
        answers = Path(self.temp.name) / "writers.jsonl"
        answers.write_text("".join(json.dumps({"job_id": j["id"], "raw_text": json.dumps({"included_fact_ids": ["F1", "F2", "F4", "F5"]})}) + "\n"
            for j in read_lines(self.run / "writer_jobs.jsonl")), encoding="utf-8")
        pipeline.import_answers(self.run, self.run / "writer_jobs.jsonl", answers)

    def test_offline_flow_and_information_boundaries(self):
        for j in read_lines(self.run / "writer_jobs.jsonl"):
            payload = json.loads(j["user"])
            self.assertNotIn("recipient", payload)
            self.assertNotIn("step-free access are mandatory", j["user"])
        self.import_writer()
        pipeline.prepare(self.run)
        jobs = read_lines(self.run / "evaluation_jobs.jsonl")
        self.assertEqual(len(jobs), 40)
        for j in jobs:
            self.assertNotIn("truth", j["user"])
            self.assertNotIn("expected_best", j["user"])
            if j["role"] == "receiver" and j["metadata"]["condition"] != "full_evidence":
                self.assertNotIn("stairs", j["user"])
            if j["role"] == "detector":
                self.assertNotIn("matched_fact_id", j["user"])
        answers = Path(self.temp.name) / "evaluations.jsonl"
        records = []
        for j in jobs:
            parsed = {"action": "clarify"} if j["role"] == "receiver" else {"critical_missing_fact_ids": []}
            records.append(json.dumps({"job_id": j["id"], "raw_text": json.dumps(parsed)}))
        answers.write_text("\n".join(records), encoding="utf-8")
        pipeline.import_answers(self.run, self.run / "evaluation_jobs.jsonl", answers)
        pipeline.analyze(self.run)
        self.assertEqual(load(self.run / "analysis" / "audit.json")["successful_evaluation_jobs"], 40)
        import csv
        with (self.run / "analysis" / "paired_family_contrasts.csv").open() as f:
            contrasts = list(csv.DictReader(f))
        self.assertTrue(all(r["ci_low"] == "" for r in contrasts))
        with self.assertRaises(ValueError):
            pipeline.import_answers(self.run, self.run / "evaluation_jobs.jsonl", answers)

    def test_feasible_wrong_choices_drive_primary_contrast(self):
        self.import_writer()
        pipeline.prepare(self.run)
        case = load(ROOT / "data" / "development.json")[0]
        records = []
        for j in read_lines(self.run / "evaluation_jobs.jsonl"):
            meta = j["metadata"]
            ctx = next(c for c in case["contexts"] if c["id"] == meta["context"])
            if j["role"] == "receiver":
                action = choose(case, ctx)["best"][0]
                if meta["condition"] == "promotional" and ctx["id"] == "access_not_required":
                    action = "B"  # Feasible, but costs more than A.
                parsed = {"action": action}
            else:
                parsed = {"critical_missing_fact_ids": []}
            records.append(json.dumps({"job_id": j["id"], "raw_text": json.dumps(parsed)}))
        answers = Path(self.temp.name) / "answers.jsonl"
        answers.write_text("\n".join(records), encoding="utf-8")
        pipeline.import_answers(self.run, self.run / "evaluation_jobs.jsonl", answers)
        pipeline.analyze(self.run)
        import csv
        with (self.run / "analysis" / "episodes.csv").open() as f:
            rows = list(csv.DictReader(f))
        wrong = [r for r in rows if r["role"] == "receiver" and r["condition"] == "promotional"
                 and r["context"] == "access_not_required"]
        self.assertTrue(all(r["incorrect_commitment"] == "1" and r["constraint_violation"] == "0" for r in wrong))
        with (self.run / "analysis" / "paired_family_contrasts.csv").open() as f:
            contrast = next(r for r in csv.DictReader(f) if r["contrast"] == "promotional - neutral")
        self.assertEqual(float(contrast["mean_family_delta"]), 0.5)
        self.assertEqual(contrast["metric"], "incorrect_commitment")

    def test_frozen_config_and_jobs_cannot_change(self):
        save(self.run / "config.json", {**self.config, "seed": 2})
        with self.assertRaises(ValueError):
            pipeline.frozen(self.run)

    def test_job_tampering_and_cross_family_leakage_rejected(self):
        jobs = read_lines(self.run / "writer_jobs.jsonl")
        jobs[0]["user"] = "changed"
        (self.run / "writer_jobs.jsonl").write_text("\n".join(json.dumps(j) for j in jobs), encoding="utf-8")
        with self.assertRaises(ValueError):
            pipeline.frozen(self.run)
        case = load(ROOT / "data" / "development.json")[0]
        case.update(split="heldout", review={"author": "one", "reviewer": "two", "status": "reviewed"})
        config = copy.deepcopy(self.config)
        config.update(phase="heldout", development_family_ids=[case["family"]])
        data, cfg = Path(self.temp.name) / "heldout.json", Path(self.temp.name) / "heldout-config.json"
        save(data, [case])
        save(cfg, config)
        with self.assertRaises(ValueError):
            pipeline.plan(data, cfg, Path(self.temp.name) / "rejected-heldout")

    def test_failures_not_silently_dropped(self):
        j = read_lines(self.run / "writer_jobs.jsonl")[0]
        answer = Path(self.temp.name) / "bad.jsonl"
        answer.write_text(json.dumps({"job_id": j["id"], "raw_text": "not json"}), encoding="utf-8")
        pipeline.import_answers(self.run, self.run / "writer_jobs.jsonl", answer)
        self.assertEqual(read_lines(self.run / "attempts.jsonl")[0]["status"], "invalid_output")
        with self.assertRaises(ValueError):
            pipeline.prepare(self.run)

    def test_live_disabled_for_draft(self):
        with patch("pipeline.request_model") as network:
            with self.assertRaises(ValueError):
                pipeline.execute(self.run, self.run / "writer_jobs.jsonl")
            network.assert_not_called()

    def test_environment_preserves_runtime(self):
        from dotenv import load_dotenv
        env = Path(self.temp.name) / "fixture.env"
        env.write_text("EPISTEMICS_TEST_VALUE=file\n", encoding="utf-8")
        with patch.dict(os.environ, {"EPISTEMICS_TEST_VALUE": "runtime"}):
            load_dotenv(env, override=False)
            self.assertEqual(os.environ["EPISTEMICS_TEST_VALUE"], "runtime")

    def test_request_reservations_and_resume(self):
        config = copy.deepcopy(self.config)
        config["status"] = "approved_pilot"
        config["guards"]["max_requests"] = 1
        for route in config["roles"].values():
            route.update(endpoint="https://invalid.example/v1/chat/completions", key_env="EPISTEMICS_TEST_KEY", max_request_usd=0.1)
        cfg = Path(self.temp.name) / "live-config.json"
        save(cfg, config)
        run = Path(self.temp.name) / "guard-test"
        pipeline.plan(ROOT / "data" / "development.json", cfg, run)
        with patch.dict(os.environ, {"EPISTEMICS_TEST_KEY": "fake-unit-test-key"}), patch("pipeline.request_model", side_effect=TimeoutError) as network:
            pipeline.execute(run, run / "writer_jobs.jsonl")
            pipeline.execute(run, run / "writer_jobs.jsonl", retry_failed=True)
            self.assertEqual(network.call_count, 1)
        self.assertEqual(len(read_lines(run / "reservations.jsonl")), 1)
        self.assertTrue(read_lines(run / "attempts.jsonl")[0]["usage_unknown"])


if __name__ == "__main__":
    unittest.main()
