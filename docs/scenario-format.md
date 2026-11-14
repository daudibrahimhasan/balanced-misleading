# Scenario format and human review

The original prose is preserved in `docs/development-scenarios.md`. The prepared six-case conversion is `data/pilot-cases.proposed.json`. All newly supplied domains, valence labels and formal mappings remain proposals.

A case contains:

- `id`, `family`, `domain`, `split`, option IDs and a promotion target. Renamed numerical variants are not new independent families.
- `facts`: ID, option, base field, true value, source sentence, explicit alternatives and valence. The true value must occur in its domain. Domain types must match. Singleton domains represent explicitly invariant scope, not hidden uncertainty.
- `derived`: ordered expressions using field/parameter nodes and whitelisted operations. No code strings or eval. The same evaluator supplies decisions, counterfactuals and objective gaps.
- `contexts`: text, constraints, parameters and expected optimal choices. Cases differ in one constraint or one parameter. Shared premises are separately forwarded to receivers.
- `objective`: field name, including a derived field, and min/max direction.
- `matched_fact_id`, `paired_fact_id`, `example_included`, a per-case `fact_budget`, and optional `required_fact_ids` for invariant source facts retained in every briefing.
- `expected_checks`: proposed independent reference tables covering the candidate/paired combinations. The validator compares these with the checker; human review still must verify the field-to-prose mapping and assumptions.
- `review`: author, conversion provenance, pending/reviewed status, reviewer, reviewer type, date and specification hash. Do not fill in human endorsement from an AI check.
- `proposal_notes`: domains, compound source sentences or judgments requiring an explicit decision.

The initial six actual states have unique best choices. Separate controls allow true-state ties and no feasible option. Tied optimal options are all accepted; no feasible option is represented by the receiver action neither.

Example expressions:

```json
{
  "signing_cost": {
    "op": "add",
    "args": [
      {"field": "deposit"},
      {"op": "if", "args": [{"field": "first_month_due"}, {"field": "monthly_rent"}, 0]}
    ]
  }
}
```

Parameters such as needs_parking, months and move_cost appear both in context prose and machine-readable rules. Guru checks their agreement. The validator does not understand natural language or certify that a plausible domain is scientifically appropriate.

Domain scope matters. Best-set change varies one fact while other facts stay at their true values. Joint sufficiency enumerates all omitted facts and intersects their optimum sets. These are different labels. The detector receives all domains for the scoped verification task. Receivers do not; warrant and clarification-resolution diagnostics must therefore be described as relative to the evaluator's finite reference scope.

```powershell
python source/pipeline.py validate data/pilot-cases.proposed.json
python -m unittest discover -s tests -v
```

Use `docs/READY_FOR_GURU.md` for the final review record. Source facts, answer keys, evaluator labels and prompts remain separate. No case or plan can be called human-reviewed merely because validation passed.
