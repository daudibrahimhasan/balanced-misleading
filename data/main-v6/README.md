# Main development run evidence

Six fictional development families; not held-out validation. The frozen run is
`main-v6-writer-amendment-20261115T214437Z`.

The continuation carries the original writer-stage records forward. One invalid
writer response was explicitly retried with the same prompt/settings; both remain
in `attempts.jsonl`. `prior-writer-stage/` preserves the pre-amendment journals and
configuration. Reserved evaluation requests interrupted by worker exits were
recorded as unknown and were not resent; recovery resumed
only never-reserved jobs. `recovery-events.jsonl` records that event.

The manifest's `kind: planned_not_executed` is the immutable planning label, not a
final collection status. See the raw live attempts and `analysis/report_audit.json`
for completed counts, failures, usage and checks. Source/config/case/job hashes are
retained exactly. Absolute original workspace paths are historical provenance.
Credential environment-variable names and public provider endpoints are retained;
secret values and authorization headers are excluded. The package was checked
against configured secret values before publication.

`analysis/report_outcomes.csv` includes every planned receiver job and its unresolved
count. `report_detector_matched_valid.csv` compares detector/baselines on the same
valid jobs. Intervals in `paired_family_contrasts.csv` are descriptive equal-family
bootstrap intervals on complete packets. Repeated calls do not create new families.

Automated independent recomputation is not independent human review. No final
coauthor approval or submission is claimed. Main report: `../../paper/` and the
canonical Google Doc linked in the repository README.
