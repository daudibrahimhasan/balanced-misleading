"""Render valid receiver rates through the workspace's shared figure tooling."""
import argparse
import csv
import subprocess
import sys
from pathlib import Path
from study import load, save

RENDERER = Path(r"D:\Apart Sprint\Figures-maker\render.py")
OUTPUT_ROOT = Path(r"D:\Apart Sprint\Figures-maker\output\ai-x-epistemics")


def figures(run):
    with (run / "analysis" / "summary.csv").open(encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["role"] == "receiver" and r.get("constraint_violation_rate_valid")]
    if not rows:
        raise ValueError("No valid receiver outcomes to plot")
    smoke = load(run / "manifest.json").get("kind") == "offline_smoke_fixture"
    title = "OFFLINE SMOKE FIXTURE - NOT RESEARCH" if smoke else "Constraint violations among valid receiver responses"
    root = OUTPUT_ROOT / run.name
    data = run / "analysis" / "figure_data.csv"
    with data.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["condition", "model", "violation_rate"])
        writer.writeheader()
        for r in rows:
            writer.writerow({"condition": r["condition"], "model": r["model"] or "unspecified",
                             "violation_rate": r["constraint_violation_rate_valid"]})
    spec = {"chart_type": "grouped_bar", "title": title, "x": "condition", "y": "violation_rate",
            "group": "model", "y_format": "percent", "ylabel": "Constraint violation rate",
            "caption": "Valid responses only. Consult summary.csv for planned denominators and unresolved-outcome bounds. No uncertainty intervals shown."}
    spec_path = run / "analysis" / "figure_spec.json"
    save(spec_path, spec)
    subprocess.run([sys.executable, str(RENDERER), "--data", str(data), "--spec", str(spec_path), "--out", str(root)], check=True)
    return root


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run", type=Path)
    print(figures(p.parse_args().run))
