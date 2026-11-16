# Premise-boundary review

This is a post hoc offline audit of Elvina's 16 November review, not a corrected
experiment. No model calls were made and no frozen records or labels were changed.

The implemented information boundary supplied only the selected briefing plus the
recipient rule and limited premises. Original setup assertions that both offers
are full-time, both early-termination options are 12-month leases, and both signing
payments include first-month rent were not all retained as known premises. The
conversion instead allowed these facts to become unknown and their values to vary
in the reference domains. A requirement to be full-time is not a statement that
both options are full-time. Adding the requirement itself is not the central error;
withholding the original fulfillment assertion changes the task.

Elvina's exclusion list is reproduced in label-sensitivity.csv:
job_health F5/F6; job_schedule F5/F6; lease_break F5/F6;
job_moving F7/F8; lease_deposit F5/F6.

| Condition | Original sensitive / comparison | After listed exclusions |
|---|---|---|
| Balance-instructed | 17/18; 13/18 | 4/18; 3/18 |
| Promotional | 18/18; 0/18 | 18/18; 0/18 |
| Neutral | 9/18; 9/18 | 3/18; 3/18 |
| Matched random | 7/18; 10/18 | 4/18; 2/18 |

All 18 balance-instructed selections omit only neutral-labeled facts. None omits
the planted candidate or paired fact. The residual 4/18 and 3/18 cases concern
lease-duration facts in lease_deposit and lease_parking; they do not establish a
balanced omission of the planted favorable/adverse evidence.

The 19 false-neither actions are real recorded outcomes under the explicit extended
run action set. Unknown qualification is not proof that neither qualifies, so the
quoted job_schedule response is still incorrect under those instructions. However,
the added action set and omitted original premises change the evaluation relative
to the earlier authored specification. These errors cannot be presented as a faithful
measurement of behavior on the original information setup.

The exclusion calculation is a label sensitivity check. It is not the result of
receivers being given restored premises. A spec-faithful rerun would need reviewed,
always-known setup assertions; consistency between those assertions and reference
alternatives; a reviewed action set; and a newly versioned screen and collection.
No such rerun is authorized or claimed here.

The original headline is numerically correct for the implemented conversion but
requires a material qualification. A scoring reimplementation cannot establish
source-specification fidelity when both implementations share the same altered
assumptions. The manuscript and submission abstract should disclose the mismatch,
report the sensitivity result separately, and avoid treating the main count as a
clean confirmation of the intended recipient-specific mechanism. Raw evidence
should be retained. Any revision must also distinguish the post hoc sensitivity
from prespecified analysis and retain mixed matched-random comparisons.

## Revision implemented

The paper now centers the executed qualification task and explicitly labels this
reframe as post hoc. Its abstract, Methods, Results, Discussion and Conclusion
report the mismatch and sensitivity counts. The original comparisons remain.
Elvina is credited for identifying the mismatch. This preserves useful as-run
observations without claiming faithful confirmation of the original setup.

`python scripts/premise_boundary_audit.py` reproduces the exclusion calculation,
checks that all balanced omissions are neutral and avoid the candidate pair, and
exports all false-neither inputs and public justifications. `summary.json` records
input hashes. All 19 justifications cite absent or unknown qualification evidence
on LLM-assisted inspection; this semantic assessment awaits independent human
coding. The lexical screen in the CSV is only a reproducible text check, not a
substitute for that coding. The observations span four families and seven distinct
briefing/context inputs. Submitted actions remain unchanged.
