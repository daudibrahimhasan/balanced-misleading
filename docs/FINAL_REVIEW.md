# Final coauthor review

Elvina, please flag blocking issues first. For each issue, give the paper section
or file/row, what is wrong, and the evidence or correction needed. Separate
blocking errors from wording suggestions. Please do not mark the whole package
independently validated because the automated checks pass.

- [Current paper](https://docs.google.com/document/d/1hWacDlUdl_Tlyz4ObjvRS0kho9pjLVJCCPKF1rrSXeU/edit)
- [Report PDF](../paper/Balanced-but-Misleading-report.pdf)
- [Numerical results and audit](RESULTS.md)
- [Frozen main evidence](../data/main-v6)
- [Literature checks](literature-check.md)

## What needs your review

1. **Interpretation.** A zero selection-imbalance score can coexist with critical
   omissions. This does not establish that the full JANUS metric fails, that
   balance-instructed writing is worse than matched random selection, or that
   models deliberately target a reader. Writers never see recipient contexts.
   Check that the abstract and conclusion stay within the observed results.
2. **The actual omitted facts.** Balance-instructed writers frequently drop shared
   qualification facts, not just the planted candidate pair. Such omissions can
   matter in both contexts. Check the formal conversion against your original
   scenarios and the declared alternatives, compound mappings and valence labels.
   These choices still need independent human validation.
3. **Wrong choices versus false neither.** The prespecified primary endpoint is
   incorrect commitment: a suboptimal/infeasible option or an incorrect claim that
   neither option qualifies. Clarification, deferral and unresolved requests are
   separate. Review the explanation of false-neither errors; missing evidence is
   not evidence that no option qualifies. Submitted actions are never repaired
   from their explanations.
4. **Numbers and comparisons.** Check the paper against
   `data/main-v6/analysis/report_outcomes.csv`, `report_selection_summary.csv`,
   `report_detector_matched_valid.csv` and `report_family_contrasts.csv`.
   Repeats are nested within six families. Intervals are descriptive, complete
   families and exclusions are explicit, and missing outcomes are not successes.
   The detector and simple baselines use the same valid jobs in the main comparison;
   false alarms use harmless omitted facts, with present-fact flags separate.
5. **Literature and authorship.** Check the closest-work comparisons, APA references,
   your name/affiliation and your contribution statement. Current authors are
   Daud Ibrahim Hassan and Elvina Chow, both Independent Researchers. Final
   coauthor approval has not been inferred from your earlier drafting work.

## Already checked automatically

The audit reparses successful raw responses and uses a separately implemented
arithmetic/reference calculation to check choices, single-fact criticality,
joint-completion warrant and receiver endpoint scores. It also checks job counts,
duplicates, frozen hashes, writer blindness, shared briefing text and recorded
usage. The 26 software tests pass. These checks do not validate whether the
constructed alternatives or valence judgments are realistic.

To rerun the published analysis without API calls:

```powershell
python -m pip install -r requirements.txt
python source/pipeline.py analyze data/main-v6
python scripts/final_report_audit.py --run data/main-v6
```

Keep the raw run unchanged. A scientific correction should identify the affected
records and use a versioned analysis or new run, not silently replace failures.
Historical review templates remain in the repository as provenance, not current
authorship or independent approval. The report is prepared for review; external
submission is a separate action.
