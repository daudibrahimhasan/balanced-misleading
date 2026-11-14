# Scenario handoff

Elvina can work in plain text in the shared Doc. Daud converts it to JSON. Guru independently checks both the human-readable statements and their structured fields. Automation can check arithmetic and rule consistency; it cannot prove that the prose correctly describes those fields.

Each packet needs:

1. Unique `id`, `family`, `domain`, and `split` (`development` or `heldout`). A family is a distinct decision structure, not renamed options or changed numbers.
2. `review`: author, status and reviewer. Keep the implementation example unreviewed until a real independent review happens.
3. At least two `options`, a `promotion_target`, and one numerical `objective` field with direction `min` or `max`.
4. `facts`: ID, option ID, field, true value, allowed finite `alternatives`, source text, and `valence` (`favorable`, `adverse`, `neutral`, or null pending review). Every option must define every field referenced by a rule or objective. A field must be defined once. Alternatives include the true value and use one type. Do not duplicate the same fact in another sentence, because that can make a supposed omission remain visible.
5. Two `contexts`, each with an ID, plain-language text, formal constraints (`eq`, `le`, `ge`), and independently calculated `expected_best`. Context 1 is the critical context; context 2 is the harmless context. The contexts must add/remove or change only one constraint. Use unique full-evidence best answers for the initial protocol.
6. `matched_fact_id`: a fact whose allowed alternatives change the best choice in context 1 but not context 2.
7. `example_included`: fact IDs for a sample briefing which omits the matched fact. This is an explanatory fixture, not a model response.
8. `assumptions`: explicit scope, no hidden constraints, uncertainties and reference alternatives. Do not invent legal or clinical truths.

See `data/development.json` for the complete lease example. To check a converted file:

```powershell
python source/pipeline.py validate path/to/scenarios.json
```

Current solver scope is deliberately small: mandatory field constraints followed by one numerical objective. Complex trade-offs, probabilistic utilities, negotiation and unspecified preferences need a different agreed rule, not a guessed answer. Ties and no-feasible-option states are handled during counterfactual enumeration, but initial full-evidence cases must have a unique best option.

Source facts, receiver prompts, detector prompts and answer keys are separate. Do not include `expected_best`, `matched_fact_id`, alternative answer sets, or review labels in model-facing text. The detector sees the actual full source evidence, not an annotated target omission. Keep held-out families out of prompt iteration.
