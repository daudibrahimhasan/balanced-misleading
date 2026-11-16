# Status

Completed development collection, audited analysis, figures and manuscript.
Final coauthor review and independent validation of the formal assumptions remain open.

- Authors: Daud Ibrahim Hassan and Elvina Chow, Independent Researchers.
- Paper: https://docs.google.com/document/d/1hWacDlUdl_Tlyz4ObjvRS0kho9pjLVJCCPKF1rrSXeU/edit
- Plan: https://docs.google.com/document/d/1UNlPj2cU38PA7VzWCqd9kOQzmgSEjc77aonBI545XrE/edit
- Report: `paper/Balanced-but-Misleading-report.pdf`; readable snapshot: `paper/manuscript.md`.
- Frozen evidence: `data/main-v6`; numerical report: `docs/RESULTS.md`.
- Figures and their data/specs: `figures/results`; final review: `docs/FINAL_REVIEW.md`.

The repaired competence screen passed 42/42 initial responses after tuning on the
same development cases. Main collection has 54 valid writer outputs in 55 attempts
and all 1,248 evaluation records: 1,233 valid, six interrupted, seven invalid and
two timeouts. No interrupted request was resent. Both recoveries and the single
explicit writer retry remain in the evidence.

Frozen models: DeepSeek V4.1 Flash 1017, GLM-5.3-Flash and Nemotron 3.5 Super VL.
Temperature 0; output cap 4096; timeout 180 seconds; one in-flight request per route.
GLM uses JSON mode; Deploy reasoning effort is low; Nemotron reasoning is off with
six-second request-start spacing. Source/config/data/job hashes are unchanged.

Checks: 26 software tests pass; raw successful responses reparse; independently
implemented choice/criticality/warrant calculations agree with all recorded scores;
no missing job records or duplicate evaluation attempts. Published analysis
reproduces offline with every packaged hash unchanged. Configured secret-value
scan found no matches. Reported main usage is 989,578 tokens, with eight attempts
of unknown usage. US$19.545 is a reservation allowance, not a verified invoice.

Interpretation revision (16 November): Elvina identified original setup facts that
were not consistently supplied as known premises in the executed task. The paper
now reports that partially observed qualification task and labels the new reframe
as post hoc. Balanced critical omissions are 17/18; 13/18 as-run and 4/18; 3/18 after
specified exclusions. No balanced packet drops the planted candidate pair.
All 19 false-neither outputs cite missing qualification evidence on LLM-assisted
inspection; they span four families and seven distinct briefing/context inputs.
The new offline audit is scripts/premise_boundary_audit.py; its outputs are in
docs/reviews/premise-boundary-20261116. Frozen evidence and source remain unchanged.

The revised native manuscript and clean 13-page PDF are verified, including the
221-word abstract, original result table/figure, references and authors. All 41
frozen evidence hashes match. The new offline audit reproduces the reported counts.
Next: final coauthor review of the reframed interpretation and independent human
coding of the 19 justifications. No new inference or external submission is claimed.
