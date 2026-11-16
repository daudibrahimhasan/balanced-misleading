"""Generate visibly labeled, deterministic fixture outputs; NEVER calls an API."""
import argparse
import json
from pathlib import Path
import pipeline
from study import choose, coverage, load, read_lines, save


def smoke(out):
    config = load(pipeline.ROOT / "config" / "pilot.example.json")
    for route in config["roles"].values():
        route["model"] = "OFFLINE_FIXTURE_NOT_A_MODEL"
    config_path = out.parent / (out.name + "-fixture-config.json")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    save(config_path, config)
    pipeline.plan(pipeline.ROOT / "data" / "development.json", config_path, out)
    manifest = load(out / "manifest.json")
    manifest["kind"] = "offline_smoke_fixture"
    manifest["warning"] = "Hand-authored test responses, no inference, not empirical results"
    save(out / "manifest.json", manifest)
    case = load(out / "cases.json")[0]
    answers = []
    for j in read_lines(out / "writer_jobs.jsonl"):
        # Deliberately exercise correct and harmful paths, not measure any model.
        ids = ["F1", "F2", "F3", "F4"] if j["metadata"]["condition"] == "neutral" else ["F1", "F2", "F4", "F5"]
        answers.append({"job_id": j["id"], "raw_text": json.dumps({"included_fact_ids": ids})})
    path = out / "SMOKE_ONLY_writer_answers.jsonl"
    path.write_text("".join(json.dumps(a) + "\n" for a in answers), encoding="utf-8")
    pipeline.import_answers(out, out / "writer_jobs.jsonl", path)
    pipeline.prepare(out)
    briefs = {b["id"]: b for b in load(out / "briefings.json")}
    answers = []
    for j in read_lines(out / "evaluation_jobs.jsonl"):
        ctx = next(c for c in case["contexts"] if c["id"] == j["metadata"]["context"])
        b = briefs[j["metadata"]["brief"]]
        if j["role"] == "receiver":
            action = choose(case, ctx)["best"][0] if j["metadata"]["condition"] in ("neutral", "full_evidence") else "A"
            value = {"action": action, "reason": "Hand-authored smoke fixture, not model output"}
        else:
            value = {"critical_missing_fact_ids": coverage(case, ctx, b["included"])["critical_missing"],
                     "reason": "Oracle fixture to check scoring only; detector performance is NOT measured"}
        answers.append({"job_id": j["id"], "raw_text": json.dumps(value)})
    path = out / "SMOKE_ONLY_evaluation_answers.jsonl"
    path.write_text("".join(json.dumps(a) + "\n" for a in answers), encoding="utf-8")
    pipeline.import_answers(out, out / "evaluation_jobs.jsonl", path)
    pipeline.analyze(out)
    print(json.dumps({"smoke_fixture": str(out), "network_requests": 0, "warning": manifest["warning"]}, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("out", type=Path)
    smoke(p.parse_args().out)
